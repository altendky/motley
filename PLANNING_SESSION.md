# Motley: ESP32-C6 Matter/Thread Device Framework - Planning Session

Date: 2026-04-16

## Project Overview

Create a configurable ESP32-C6 firmware framework called **motley** for building Matter-over-Thread devices. The framework should allow the same codebase to be configured for different device types and applications.

### Initial Target Application: Velux Skylight Controller

A controller for a Velux skylight/blind that:
- Interfaces with an existing Velux KLI 3-button remote (up/stop/down) by electronically triggering the remote's buttons
- The remote uses active-LOW buttons (internal pull-up, buttons short to GND when pressed)
- Uses a ULN2003AN Darlington transistor array to pull button lines LOW
- Remote is powered from a separate 3.3V regulator (replacing batteries)
- Exposes as a Matter Window Covering device type

### Hardware Platform

- **MCU**: Adafruit ESP32-C6 Feather (native Thread/802.15.4 support)
- **Protoboard**: Adafruit FeatherWing Proto
- **Button driver**: ULN2003AN (DIP-16) - inputs from ESP32 GPIOs, outputs to remote button pads
- **Power**: USB to ESP32, separate 3.3V regulator (MPM3610 breakout) for remote

### Framework Requirements

1. Configurable device types - same codebase should support:
   - Window coverings (blinds, skylights)
   - Relays/switches
   - Lights
   - Sensors (future)
2. Thread Router capability - mains-powered devices should act as Full Thread Devices (FTD) to extend mesh
3. Matter compliance - use esp-matter SDK, proper device type clusters
4. Configuration-driven - pin mappings, device type, behavior should be configurable (Kconfig or similar)

---

## Research Summary

### Reference Projects Analyzed

1. **esp-matter SDK** (https://github.com/espressif/esp-matter)
2. **lemauee/esp32c6-matter-over-thread-roof-window-controller** (https://github.com/lemauee/esp32c6-matter-over-thread-roof-window-controller)
3. **thorio/esphome-projects/velux-controller** (https://github.com/thorio/esphome-projects/tree/master/velux-controller)

---

### From esp-matter SDK

**Project Structure:**
```
esp-matter/
├── components/
│   └── esp_matter/           # Core Matter SDK wrapper
│       ├── data_model/       # Endpoints, clusters, attributes, features
│       └── utils/
├── connectedhomeip/          # Matter SDK submodule
├── device_hal/
│   └── device/               # HAL for different ESP32 devkits
├── examples/                 # Reference applications (20+ examples)
└── Kconfig                   # Root config
```

**Key Patterns:**
- Config structs with feature flags for device types
- Dynamic endpoint creation with `ENDPOINT_FLAG_NONE`
- Factory functions: `create()` and `add()` per device type
- Target-specific `sdkconfig.defaults.{target}` files

**Window Covering Device Type (0x0202):**
```cpp
namespace window_covering {
typedef struct config : app_with_group_config {
    cluster::window_covering::config_t window_covering;
    config(uint8_t end_product_type = 0) : window_covering(end_product_type) {
        identify.identify_type = chip::to_underlying(
            chip::app::Clusters::Identify::IdentifyTypeEnum::kActuator);
    }
} config_t;
}
```

**Features available:**
- `lift` - basic lift control
- `tilt` - tilt control
- `position_aware_lift` - with position tracking (target/current percent)
- `position_aware_tilt` - with position tracking

**Thread Configuration (sdkconfig.defaults.esp32c6):**
```ini
CONFIG_IDF_TARGET="esp32c6"
CONFIG_OPENTHREAD_ENABLED=y
CONFIG_OPENTHREAD_SRP_CLIENT=y
CONFIG_OPENTHREAD_DNS_CLIENT=y
CONFIG_ENABLE_WIFI_STATION=n
CONFIG_ENABLE_OTA_REQUESTOR=y
CONFIG_MRP_LOCAL_ACTIVE_RETRY_INTERVAL_FOR_THREAD=5000
CONFIG_MRP_LOCAL_IDLE_RETRY_INTERVAL_FOR_THREAD=5000
```

---

### From lemauee's Roof Window Controller

**Project Structure:**
```
esp32c6-matter-over-thread-roof-window-controller/
├── main/
│   ├── app_main.cpp
│   ├── relay/
│   │   ├── relay.cpp/.h          # Low-level GPIO
│   │   └── relay_driver.cpp/.h   # Matter integration
│   ├── switch/
│   │   └── switch_driver.cpp/.h  # Button input handling
│   ├── reset_button/
│   └── user_led/
├── sdkconfig.defaults
├── sdkconfig.defaults.esp32c6
└── partitions.csv
```

**Key Finding:** Uses `on_off_plugin_unit` + `generic_switch` instead of Window Covering cluster (simpler approach).

**Thread Safety Pattern (CRITICAL):**
```cpp
// All Matter attribute updates from callbacks MUST use ScheduleLambda:
chip::DeviceLayer::SystemLayer().ScheduleLambda([endpoint_id, newPosition]() {
    chip::app::Clusters::Switch::Attributes::CurrentPosition::Set(
        endpoint_id, newPosition);
});
```

**Handle-Based Driver Pattern:**
```cpp
endpoint_t *ep = create(node, &config, ENDPOINT_FLAG_NONE, driver_handle);
// Later in callback:
relay_handle_t handle = (relay_handle_t)priv_data;
```

**Uses `iot_button` component for debounced inputs:**
```cpp
button_config_t button_config{};
button_config.type = BUTTON_TYPE_GPIO;
button_config.gpio_button_config.gpio_num = SWITCH_GPIOS[i_gpio];
button_config.gpio_button_config.active_level = 0;  // Active low
button_handle_t button_handle = iot_button_create(&button_config);
```

---

### From ESPHome Velux Controller (Hardware Details)

**Button Press Duration: 200ms**
```yaml
switch:
  - platform: gpio
    id: output_up
    pin: GPIO12
    on_turn_on:
      then:
        - delay: 200ms
        - switch.turn_off: output_up
```

**5-Wire Interface:**
- 2 wires for power (3.3V, GND)
- 3 wires for buttons (UP, STOP, DOWN)

**Transistor Switching:**
- Uses MMBT3904 NPN transistors (similar to ULN2003AN functionality)
- Base resistor: 1kΩ (current limiting)
- Buttons are active-LOW (remote has internal pull-ups)

**Bidirectional Design (optional):**
- Output GPIO (via transistor) to simulate button presses
- Sense GPIO (direct connection) to detect physical button presses
- Filter logic: ignore sense line when ESP is driving output

**Position Estimation:**
```yaml
cover:
  - platform: time_based
    has_built_in_endstop: true
    open_duration: 30s   # Calibrate to your window
    close_duration: 30s
```

---

## Open Questions Requiring Your Input

### 1. Matter Device Type Approach

**Option A: Window Covering Cluster (Recommended)**
- Proper Matter Window Covering (0x0202) with position tracking
- More complex but semantically correct for HomeKit/Google Home
- Shows as a single "Window Covering" device with up/down/stop controls
- Position can be estimated via timing (like ESPHome's time_based cover)

**Option B: On/Off Plugin Units**
- Simpler: 3 separate on/off endpoints (up/stop/down)
- Easier to implement but less elegant in smart home apps
- Would show as 3 separate switches in HomeKit/Google Home

**Which do you prefer?**

---

### 2. Bidirectional Control

**Option A: Output Only (Recommended for initial implementation)**
- ESP32 only sends commands to remote
- Simpler wiring (only 3 output GPIOs needed)
- Can add sensing later

**Option B: Bidirectional**
- Wire GPIO inputs to sense when physical buttons are pressed
- Sync state with Matter fabric when user presses physical remote
- Requires additional GPIOs and wiring (3 more sense lines)

**Do you want to support sensing physical button presses initially?**

---

### 3. Build Configuration System

**Option A: Kconfig Menu (Recommended)**
- Select device type via `idf.py menuconfig`
- Single firmware source, configuration stored in sdkconfig
- Easy to change pin mappings and device type

**Option B: CMake Variants**
- Build different apps (e.g., `velux-controller`, `relay-switch`)
- Separate builds per device type
- Better for fundamentally different device types

**Option C: Both Kconfig + Variants**
- Kconfig for pin mappings/tuning within a device type
- CMake variants for fundamentally different device types

**How should different device configurations be selected at build time?**

---

### 4. Code Organization Style

**Option A: C with Structs (Recommended)**
- ESP-IDF style C with config structs and function pointers
- Matches esp-matter patterns closely
- Smaller binary size

**Option B: C++ with Classes**
- Modern C++ with device/driver classes
- More abstraction, type safety
- Larger binary, but more maintainable for complex projects

**What's your preferred code organization style?**

---

### 5. Initial Scope

Should the initial implementation include:

- [ ] Full Window Covering cluster with position estimation?
- [ ] Just basic up/stop/down commands?
- [ ] OTA update support?
- [ ] Status LED indication?
- [ ] Factory reset button?
- [ ] CHIP shell for debugging?

---

## Proposed Project Structure

```
motley/
├── CMakeLists.txt
├── sdkconfig.defaults
├── sdkconfig.defaults.esp32c6
├── partitions.csv
├── main/
│   ├── CMakeLists.txt
│   ├── idf_component.yml
│   ├── Kconfig.projbuild          # Device type & pin configuration
│   ├── app_main.cpp
│   ├── drivers/
│   │   ├── gpio_output.h/.cpp     # Low-level GPIO output abstraction
│   │   ├── button_press.h/.cpp    # Timed button pulse driver
│   │   └── window_covering_driver.h/.cpp  # Matter integration
│   ├── devices/
│   │   └── window_covering.h/.cpp # Window covering endpoint setup
│   └── common/
│       ├── status_led.h/.cpp      # Status indication
│       └── reset_button.h/.cpp    # Factory reset handling
└── README.md
```

---

## Key Implementation Details

### GPIO Pin Selection (Adafruit ESP32-C6 Feather)

Available GPIOs on Feather headers:
- A0 (GPIO0), A1 (GPIO1), A2 (GPIO2), A3 (GPIO3), A4 (GPIO4), A5 (GPIO5)
- SCK (GPIO19), MOSI (GPIO20), MISO (GPIO21)
- RX (GPIO17), TX (GPIO16)
- SDA (GPIO23), SCL (GPIO22)
- D5 (GPIO5), D6 (GPIO6), D9 (GPIO9), D10 (GPIO10), D11 (GPIO11), D12 (GPIO12), D13 (GPIO13)

**Suggested pin assignments:**
- UP button: GPIO10
- STOP button: GPIO11
- DOWN button: GPIO12
- Status LED: GPIO13 (or use onboard NeoPixel on GPIO8)
- Factory reset: Boot button (GPIO9)

### Button Press Timing

```cpp
#define BUTTON_PRESS_DURATION_MS 200  // From ESPHome reference
```

### Thread Router Configuration

For mains-powered FTD (Full Thread Device) to extend mesh:
```ini
CONFIG_OPENTHREAD_FTD=y
CONFIG_OPENTHREAD_BORDER_ROUTER=n
CONFIG_OPENTHREAD_CHILD_MAX=10
```

---

## Next Steps (After Questions Answered)

1. Initialize git repository
2. Create project structure
3. Set up CMakeLists.txt and Kconfig
4. Implement GPIO output driver
5. Implement button press timing driver
6. Create Window Covering Matter endpoint
7. Wire up Matter callbacks to drivers
8. Test commissioning and control
9. Add OTA support
10. Add status LED and factory reset

---

## Additional Notes

- The ULN2003AN you're using is a better choice than discrete transistors - it has built-in base resistors and flyback diodes
- 200ms button pulse is proven to work with KLI remotes
- Thread retry intervals should be longer (5 seconds) for mesh reliability
- All Matter attribute updates must use `ScheduleLambda()` for thread safety
