# ADR-0014: Integrated controller and switched sensor supply

- **Status:** Accepted; represented in exploratory unrouted CAD, not qualified for fabrication
- **Date:** 2026-11-12
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`; preserve `MOT-PLAT-004`; support draft `MOT-SENS-005`
- **Related ADRs:** [ADR-0011](0011-single-output-modules-and-sensor-core.md), [ADR-0012](0012-automatic-usb-power-and-panel-port.md), [ADR-0013](0013-usb-c-internal-feather-connection.md)
- **Affected components:** Controller/AC-input board, USB interface, sensor supply and inter-board power interface

## Context

The developer selected a directly integrated ESP32-C6-WROOM-1-N8 in place of
the Feather daughterboard, then accepted a separate GPIO-switchable 3.3 V
sensor supply. The existing unrouted CAD and PDFs still show the Feather and
manual JP1. This records planning under the existing `MOT-PROC-001` exploratory
exception; no maintained hardware implementation, firmware changes, purchases
or physical verification are claimed.

## Decision drivers

- Reduce unnecessary controller parts and internal USB connections.
- Preserve JLCPCB Economic assembly eligibility for the selected module.
- Preserve USB development and automatic RECOM priority with USB backup.
- Separate sensor regulator loading from the ESP regulator and permit sensor
  power cycling without rebooting the controller.
- Retain USB-only sensor bench operation within the host's available current.
- Preserve RECOM-only relay/optotriac driver power and the three-board partition.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Feather plus internal USB interconnect | Replaceable tested controller board | Unneeded battery circuitry, sockets and USB adaptation |
| Integrated C6-MINI | Compact module | JLCPCB C5736265 is Standard-only and requires X-ray inspection |
| Integrated C6-WROOM-N8 | Economic assembly listed, extra flash, accessible edge connections | More board area than MINI; custom board bring-up |
| Shared controller/sensor regulator | Fewest parts | Sensor load shares controller regulator; no independent supply reset |
| Separate enabled sensor LDO from selected 5 V | Low incremental cost; independent supply control; USB bench use | Thermal/current and I2C back-power analysis required |

## Decision

Use **ESP32-C6-WROOM-1-N8**, JLCPCB **C5366877**, as the preliminary integrated
controller module. Preserve power-up/reset/boot circuitry, USB serial/JTAG,
appropriate I2C pull-ups, decoupling and recovery access. Omit the Feather
battery connector, charger, fuel gauge, battery changeover, sockets and
internal USB plug connection. A simple status LED and reset/boot buttons are
preferred service controls. Follow the WROOM reference circuit and antenna
keepout; the Feather schematic is a reference rather than a drop-in copy.

Preserve TPS2116 automatic priority selection: healthy RECOM `+5V_SYS` wins over
raw host USB VBUS; USB is an optional backup, with automatic return to RECOM.
Call the future selected rail `+5V_SELECTED`. Retain independent raw-host-VBUS
qualification for USB data attachment, including ROM flashing. The external
interface is a USB-C sink with separate CC pull-downs and suitable protection.
There is no internal USB-C source port, TUSB320 source controller or
carrier-to-Feather cable. Exact enclosure port mounting remains open.

Feed **two parallel regulators** from `+5V_SELECTED`:

- A main 3.3 V regulator supplies the ESP and always-on controller logic.
- A separate **AP2112K-3.3TRG1**, JLCPCB **C51118**, is the preliminary sensor
  regulator, with input/output capacitors and an enable pull-down. An ESP GPIO
  controls its active-high EN input; exact GPIO and startup sequencing remain
  to be selected. Use a distinct future `+3V3_SENS` net. Its output discharge
  supports power cycling, subject to checking actual off voltage and delay.

The sensor supply therefore normally draws from the RECOM 5 V supply through
the selector, and can operate from USB-only power within its current budget.
It does not draw from the ESP's 3.3 V regulator. Grounds remain common on the
isolated low-voltage side; separate regulation is not galvanic isolation.
Relay/optotriac drivers stay on raw RECOM ahead of the selector, so USB-only
power cannot energize their supply.

Regulator placement on the controller or mux board is not fixed. If it resides
on the mux board, carry selected 5 V and EN to that board and define the revised
interconnect explicitly. Decide mux/pull-up power domains and prevent I2C,
reset or other signals from back-powering an off sensor rail. Gate bus activity
and wait for supply/startup readiness under draft `MOT-SENS-005`; that draft
requirement is not treated as approved implemented firmware.

## Consequences

The separate rail adds an estimated **$0.30-0.70 in parts** per controller,
using the observed AP2112 price near $0.17; assembly fees are separate. Reusing
the exact regulator elsewhere may avoid another distinct feeder setup. These
are planning prices, not a final BOM or quote.

The 600 mA device rating is not a continuous-current budget at 5 V input in an
enclosure. Calculate `(VIN - 3.3 V) * IOUT`, package/board temperature rise,
cable drop and startup/inrush. Initially retain no more than one sensor heater
at a time. Check the entire selected supply, host current entitlement and
controller radio peaks; a dedicated regulator does not add 5 V source capacity.
Do not imply that all sensor shorts are isolated from the controller's shared
upstream source. Hardware tests must establish rail-off behavior, recovery,
source failover, heater loading and ROM/application USB operation.

## Supersession

Supersedes ADR-0012's Feather-specific implementation and ADR-0013's internal
USB-C source-port/cable architecture. Preserve their automatic power-priority,
upstream backfeed prevention, USB attachment and RECOM-only driver obligations.
ADR-0011's three designs/four physical boards remain; its controller board now
has an integrated module in the plan. Existing native CAD remains historical
until revised. Superseded by: None.

## References

- [WROOM datasheet and reference circuit](https://documentation.espressif.com/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf)
- [JLCPCB WROOM-N8: Economic and Standard](https://jlcpcb.com/partdetail/Espressif-ESP32_C6_WROOM1/C5366877)
- [JLCPCB MINI-N4: Standard only](https://jlcpcb.com/partdetail/ESP32-C6-MINI-1-N4/C5736265)
- [JLCPCB AP2112K-3.3TRG1](https://jlcpcb.com/partdetail/C51118)
- [Diodes AP2112 datasheet](https://www.diodes.com/datasheet/download/AP2112.pdf)
- [Feather reference schematic](https://github.com/adafruit/Adafruit-ESP32-C6-Feather-PCB/blob/main/Adafruit%20Feather%20ESP32-C6.sch)
