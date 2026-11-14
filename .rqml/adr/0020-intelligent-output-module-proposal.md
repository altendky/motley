# ADR-0020: Intelligent AC-output exploratory architecture

- **Status:** Accepted for the authorized exploratory schematic/placement study; product qualification pending
- **Date:** 2026-11-14
- **Classification:** derived_from_requirements
- **Related requirements:** draft `MOT-AC-001` through `MOT-AC-015`, `MOT-ENG-010`, `MOT-STOR-001`, `MOT-HW-001/002/004/005/006/007/008`
- **Related ADRs:** ADR-0011, ADR-0014, ADR-0017
- **Affected components:** controller/output interfaces, line-reference circuit, output MCU/programming, sensing and power stage

## Context

The preceding native CAD had direct HEAT_EN/CUT_EN connections and a zero-cross
optotriac. The later discussion calls for both phase-angle and whole-cycle
control, independent feedback and local communication-loss handling. The
developer clarified that sixteen outputs is a cost-sensitive target rather than
a hard minimum, ESP-assisted programming includes initial blank-device
commissioning, and international mains support is desired. A subsequent
clarification requires globally unique identity-based tracking for configuration,
faults and updates, with one new board at the selected default address at a time
and an explicit inventory of default/reserved addresses. Other boards at
nonconflicting addresses may remain on the same bus.
Higher-current variants are deferred to issue #30 while the initial 300 W design
proceeds. The developer also requires watchdog supervision and response on every
MCU and accepts an easy local recovery switch/jumper; general inductive-load
support is deferred.

## Decision drivers

- Keep line-sensitive timing and electrical fault handling operating locally.
- Allow inexpensive internal modular wiring and at least the initial two outputs.
- Preserve independent observed voltage and current, including unloaded short detection.
- Avoid requiring a separate programmer for initial assembly or recovery.
- Keep the PCB and component choices open to higher current and regional variants.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| ESP directly times every output | No additional output MCU | Central timing/IO scales with outputs; local communication-failure behavior needs other hardware |
| MCU per output with isolated sensing/drive | Local timing, acquisition, cutoff and fallback; reusable board | Firmware, programming selection, regulator and pin/storage budget |
| Application-specific AC controller/monitor | Potentially fewer functions to implement in firmware | No sourced, assessed part has yet covered the required combination |

## Decision

Use the per-output MCU architecture for the developer-authorized exploratory
CAD update, with these responsibilities:

| Main ESP / controller board | Each single-output board |
| --- | --- |
| Sensor acquisition, temperature loop, Matter and user configuration | Line-synchronized phase-angle and whole-cycle scheduling |
| Send mode/level, validity and fallback settings; collect diagnostics | Observe outlet voltage and time-resolved current; compare with effective target |
| Provide one isolated line-reference source for the common mains feed | Inhibit firing and operate its own cutoff relay on applicable faults |
| Coordinate addressing and ESP-assisted commissioning/recovery | Enforce communication expiry, hardware-off defaults and retained-fault/rearm rules |

The low-voltage MCU, bus and service interface remain on the accessible isolated
side. Optotriac, sensing components and relay insulation span the mains boundary.
Retain a per-output cutoff in this proposal; a shared master cutoff remains a
separate trade-off, not a simultaneous CAD change.

For short connections inside one enclosure, prefer a dedicated I2C output bus
plus a separate shared line-reference wire. The study interface is **GND,
selected 5 V, SDA, SCL, SYNC, raw mains-derived 5 V** on a provisional 2.54 mm
six-contact header. Selected power runs logic/sensing, including during USB
commissioning; raw power runs the relay/opto actuators. Local
timers generate gate pulses rather than relying on bus transaction timing. The
reference applies only to outputs fed from that same AC source/phase. Long or
external output cables would reopen the physical-bus choice. Assess the ESP-C6
LP-I2C software/peripheral constraints before assigning that block; do not remove
the existing two-bus Qwiic access. Move LP Qwiic power and pulls to main 3.3 V so
output communication does not depend on switched sensor power; retain HP sensor
power switching. A separate fault/inhibit line remains optional.

Keep runtime address and global hardware identity distinct. The ESP's persistent
registry is keyed by the complete namespaced hardware UID, with a revalidated
current bus/endpoint mapping. Settings, fault records and update targets follow
the identity. A new board at an old address does not inherit those records;
reassignment to a prior logical role requires explicit rebinding. This is device
identity, not authentication. Use a manufacturer/UID-scheme namespace sufficient
to preserve uniqueness across supported MCU families, without truncating the UID.

Adding one new default-address board at a time makes software-assigned runtime
addresses a useful baseline to compare with switch/jumper overrides; neither the allocation pool
nor a discovery algorithm is selected yet. Draft `MOT-AC-015` and the
[address inventory](../../docs/ac-output-module.md#identity-commissioning-and-address-plan)
exclude I2C special ranges and the C011 ROM address `0x64`, account for reachable
sensor/mux addresses, and require an explicit reservation for any application
commissioning default. Select capacity after reviewing inexpensive expansion
above sixteen. Qualification must include actual
bus loading and total power; the present 5 V / 1 A supply is not qualified for
sixteen outputs. The existing roughly 36 mA relay coil would alone total about
0.58 A for sixteen boards, before MCU, ESP and sensor demand.

The study uses **STM32C011F6P6 (32 KB, TSSOP20)** provisionally.
ST documents an immutable factory **96-bit UID**, so no added identity EEPROM is
expected. Its factory ROM loader supports I2C and USART; ROM I2C has fixed
7-bit address **0x64**, independent of application address switches. Initial
commissioning therefore permits exactly one new board responding at that default
at a time. Other supported boards at nonconflicting addresses remain on the same
bus, with no requirement to disconnect or electrically separate them. This
avoids needing an automatic selector for initial commissioning. A recovery case
that would put another board at the same loader address still needs the
documented boot/selection procedure to avoid collision. Read and verify the
UID-to-runtime-address binding during commissioning and the actual target UID before later updates or
recovery writes. A shared-address ACK does not establish single-target access.
Preserve SWD/reset access as a recovery option. The six-wire deployment link
uses the ROM I2C route with local boot/reset controls; no automatic ESP-controlled
SWD wiring is added. GPIO, ADC/timer and boot/debug pins have been assigned in
the study; memory/storage behavior and actual JLC availability still need
qualification for the exact part.

Use a marked RUN/RECOVERY jumper or DIP switch plus reset access on each output
board as the agreed service-access direction. For C011, this uses BOOT0 plus
reset to enter the factory system-memory loader without working application code.
The loader itself is read-only and cannot be overwritten through normal flash
program/erase; entry can still be blocked by boot/protection settings. Initial
commissioning must establish and verify `NBOOT_SEL=0`, `NBOOT1=1`, `BOOT_LOCK=0`
and external-reset capability. Do not enable incompatible irreversible locks
such as RDP2 in the supported update path. Review BOOT0's shared PA14/SWCLK
function, switch bias/series protection and default states. Any option-byte
changes still need power-loss/recovery analysis against `MOT-STOR-001`; factory
ROM availability alone does not prove recoverability or persistence conformance.

Provide watchdog supervision and a documented progress signal/response for every
MCU under draft `MOT-ENG-010`. Start with an internal hardware watchdog where
adequate; no dedicated external WDI wire is selected. Healthy progress must cover
the actual critical tasks. Output-MCU expiry returns local actuation to off;
ESP expiry invokes autonomous modules' existing communication-failure policies
and higher-priority inhibits. The C011 ROM loader refreshes an already active
hardware IWDG, so service-mode supervision needs separate assessment.

For international use, assess nominal 100-240 V / 50-60 Hz using common PCB
designs with appropriate regional components and wiring. The current IRM-05
family already specifies universal input, but detectors, surge/triac ratings,
fuses, connectors, spacing and polarity assumptions need separate review. A
functional single-pole cutoff must not be represented as service isolation for
reversible mains connections. Qualification ranges remain undeclared.

Retain the initial 300 W / 120 V target. Investigation of higher-current variants
is deferred to [issue #30](https://github.com/altendky/motley/issues/30), including
same-PCB substitutions, cooling and full-path bottlenecks. It does not block the
initial schematic. No higher rating or inductive-load qualification is added here.

## Concrete exploratory choices and consequences

The revised CAD uses STM32C011F6P6, AP2112 local regulation, a RUN/RECOVERY
BOOT0 shunt and reset/SWD access. PB6/PB7 serve ROM/runtime I2C, PA6 receives
SYNC, PA7 commands heat and PA2 commands cutoff. PA0/PA3 read TMCS1123B5 VOUT
and its output reference; PA1 observes the isolated outlet detector. A 32 KB
redundant-image/configuration layout is only a sizing proposal: firmware fit,
verified storage commits and option-byte power-loss safety are unresolved.

VO3053-X007T replaces the zero-cross driver, with a 430 ohm pulse gate resistor
and 1 nF transistor filter. ACPL-K370 observes outlet voltage after the cutoff,
using separate LOW 90–132 V and HIGH 180–264 V resistor variants to manage
threshold, leakage and heat. TMCS1123B5AQDVGR carries load current in series
after the relay. ACPL-K376 and a SN74LVC1G17 buffer provide the shared reference;
ESP GPIO1 observes it without perturbing GPIO4 boot strapping. Detector gap
timing, electrical fanout and the complete international mains path remain
unqualified. These component ranges do not qualify a universal-input board.

The output placement grows to 100×90 mm; carrier remains 100×85 mm and the
sensor design is unchanged. All components are front-side, with no routing.
Native CAD and both PDFs now represent this direction under the existing
MOT-PROC-001 exploratory exception. Product requirements stay draft; this
decision does not constitute electrical safety, firmware, thermal, EMC or
manufacturing approval. See the
[pin/default review](../../hardware/controller/intelligent-output-review.md)
and [verification record](../../hardware/controller/verification.md).

## Supersession

This replaces ADR-0011's direct four-pin output-control interface while
preserving its single-output board partition. It replaces ADR-0017's LP Qwiic
switched-sensor power source with main 3.3 V; the HP/sensor topology and the
sensor-board design remain unchanged.

## Evidence

- [ST RM0490, device electronic signature and boot/option-byte sections](https://www.st.com/resource/en/reference_manual/rm0490-stm32c0-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)
- [ST factory-loader immutability](https://community.st.com/stm32-mcus-60/faq-stm32-boot-process-37)
- [ST C0 protection lifecycle](https://wiki.st.com/stm32mcu/wiki/Security:RDP_for_STM32C0)
- [ST C011 CMSIS header, UID_BASE](https://github.com/STMicroelectronics/cmsis-device-c0/blob/main/Include/stm32c011xx.h)
- [ST AN2606 Rev 71, C011 system-loader configuration](https://www.st.com/resource/en/application_note/an2606-.pdf)
- [ST AN4221, I2C loader commands](https://www.st.com/resource/en/application_note/an4221-i2c-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf)
- [ST STM32C011 datasheet](https://www.st.com/resource/en/datasheet/stm32c011d6.pdf)
- [MEAN WELL IRM-05 datasheet](https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.pdf)

Document research establishes candidate features, not functioning hardware or a
tested ESP programmer. Proposed selection and architecture are engineering
inferences from those features and the draft requirements.
