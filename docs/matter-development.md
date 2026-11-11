# Matter development device

This prototype starts a Matter-over-Thread root node with standard Basic
Information and a USB Serial/JTAG development console. It has no application
sensor or control endpoints. Acceptance is governed by `MOT-PLAT-004` and
`MOT-INFO-001`; a successful build alone does not establish commissioning.

It uses SDK test attestation and commissioning credentials, test vendor/product
IDs, and descriptive development names. It is not a certified or provisioned
product. Physical deployed-device controls are tracked in
[issue #15](https://github.com/altendky/motley/issues/15).

## Build and connect

Run the [firmware build check](firmware-build.md). Connect the Adafruit ESP32-C6
Feather through a USB data cable. Identify its serial device by USB identity
and confirm the chip and flash capacity with the pinned SDK's esptool before
flashing. The current partition layout expects at least 4 MiB flash and uses
DIO at 40 MHz; it contains NVS, PHY initialization data, and one factory image.
There is no OTA slot or factory-data partition in this milestone.

Use the verified bundle's `flash_args` and its relative image paths with the
same SDK's esptool `write-flash @flash_args`, from the bundle directory. Do not
substitute offsets from another example. Flashing replaces the running firmware;
it does not intentionally erase NVS. SDK startup fails visibly on an NVS error
instead of silently clearing commissioning state.

Open a serial terminal on that USB device at 115200 baud. A normal reboot logs
the full `g<commit>-clean|dirty` firmware identity and onboarding codes.
If the initial boot output was missed, request codes with:

```text
matter onboardingcodes ble
matter onboardingcodes ble manualpairingcode
```

The serial shell is a development interface. Keep a terminal attached while
commissioning to retain failure diagnostics. Do not publish commissioning codes
as ordinary build artifacts.

## Commission and inspect

Use Home Assistant's Matter add-device flow with the onboarding code, an
available Thread border router, and the phone's supported Bluetooth/Thread
commissioning setup. Development attestation may produce a warning or require
test-device setup in the commissioning platform. Record the installed Home
Assistant, Matter server, phone platform, and border-router versions when testing.

Inspect the HA device entry and independently read endpoint 0 Basic Information
(cluster `0x0028`) using the controller's Matter diagnostics or attribute reader:

| Attribute | ID | Expected development behavior |
| --- | --- | --- |
| VendorName / VendorID | `0x0001` / `0x0002` | Declared development vendor and test VID |
| ProductName / ProductID | `0x0003` / `0x0004` | Declared prototype product and test PID |
| HardwareVersion / HardwareVersionString | `0x0007` / `0x0008` | Prototype hardware declaration |
| SoftwareVersion | `0x0009` | Independent numeric development version |
| SoftwareVersionString | `0x000a` | Full current commit and cleanliness when it fits; match the receipt |
| UniqueID | `0x0012` | SDK-generated persistent device identity |

The firmware's version getter supplies Basic Information directly; the
constrained IDF image label is separate. Compare HA's displayed firmware version
with the actual attribute and `build-receipt.json`. An empty serial number is
intentional: the shared SDK test serial is disabled. UniqueID supplies the
stable device identifier for ordinary reboot, and may change on factory reset.

Power-cycle the board without changing firmware. Verify that the existing HA
device reconnects, its identity is stable, and attributes remain readable
without duplicate device registration or recommissioning. A root-only device
may have no application entities; actual HA device acceptance remains a test
obligation, and does not imply device-model certification.

## Intentional reset

Only when deliberately discarding the current commissioning state, enter:

```text
matter esp factoryreset
```

The SDK clears Matter/Thread state and reboots. Commission again using the
reported onboarding code. Ordinary reset, power cycling, opening the console,
or requesting onboarding codes does not request this factory reset. Remove an
obsolete HA entry through the controller as appropriate after intentional reset.

## Evidence still required

Record the tested receipt identity, board/chip/flash identification, boot log,
commissioning outcome, Basic Information values, HA firmware display, power-cycle
result, and deliberate reset/recommissioning result in the plan. Until observed,
those hardware criteria remain unverified. No sensing, heater switching, OTA,
or application watchdog-supervision claim is made by this prototype.
