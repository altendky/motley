# ADR-0012: Automatic USB power selection and enclosure port

- **Status:** Superseded in part by ADR-0013, then ADR-0014 (integrated controller); not implemented
- **Date:** 2026-11-12
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`; preserve `MOT-PLAT-004`'s USB development interface
- **Related ADRs:** [ADR-0011](0011-single-output-modules-and-sensor-core.md)
- **Affected components:** Feather/AC-input carrier, USB harness, enclosure USB opening, future schematic and placement exports

## Context

The developer wants to plug in USB while mains remains the preferred supply,
with USB optionally powering the controller when mains is absent. Automatic
operation is preferred if its cost is reasonable. The enclosure needs a panel
or bulkhead USB port. The Feather's USB header pin shares its connector's VBUS;
D+/D- are not exposed on its daughterboard headers. The existing JP1 drawing
requires a manual disconnection before connecting a USB host.

This records an architectural plan under the existing `MOT-PROC-001`
exploratory exception. It does not change firmware, approve a maintained
hardware requirement, qualify USB/mains safety, or authorize fabrication.
The current native CAD and PDFs still show JP1 until a later CAD revision.

## Decision drivers

- Keep healthy RECOM power preferred even when USB voltage is slightly higher.
- Use USB as an optional backup without jumpers or firmware-dependent switching.
- Prevent power from flowing into the upstream computer or inactive RECOM output.
- Preserve serial/JTAG flashing and the agreed USB development interface.
- Keep the Feather unmodified and replaceable.
- Mechanically support external cable insertion at the enclosure wall.
- Keep USB-only operation separate from the RECOM-powered output-driver rail.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Retain JP1 | Lowest parts count | Opening the enclosure and remembering the USB procedure; no automatic backup |
| Accessible manual switch | Easier to operate | Still permits the wrong setting and may interrupt controller power |
| Modify the Feather USB power path | Could reduce internal connectors | Requires board surgery and compromises simple module replacement |
| Carrier power mux with panel USB and internal Feather cable | Automatic preference/backup; unmodified Feather; independent port placement | Two internal connections, additional USB circuitry and qualification |

## Decision

Plan the carrier-based automatic arrangement. The following are preliminary
component selections, not a qualified BOM:

1. Use **TPS2116** in automatic priority mode: RECOM `+5V_SYS` to VIN1,
   upstream host `USB_VBUS_RAW` to VIN2, MODE tied to VIN1, and a resistor
   divider to PR1 defining acceptable RECOM voltage. Its output is a separate
   `FEATHER_5V_SELECTED` rail. USB can be absent; when both are healthy VIN1
   wins, when VIN1 falls below the threshold VIN2 is used if available, and
   recovering VIN1 takes priority again. Set the threshold from worst-case
   supply, divider and IC tolerances; the PR1 reference spans 0.92-1.08 V.
   No exact divider, threshold or uninterrupted-transfer claim is selected yet.
2. Keep relay and optotriac drivers on raw RECOM `+5V_SYS`, ahead of the mux.
   Supply the Feather, its 3.3 V sensor rail and associated USB logic from the
   selected supply. USB-only operation cannot energize the output-driver rail.
   Remove the old direct JP1 feed when implementing; it must not bypass the mux.
3. Bring an enclosure **USB-C female bulkhead** into a carrier USB-C sink
   receptacle. The budget candidate is **Adafruit 6069**, C-female to C-male,
   round nut mount, nominal 300 mm cable. The published mounting description
   allows 12-18 mm holes and panels up to 13 mm thick; final hole, nut access,
   cable bend and wall dimensions need the drawing/sample. No ingress rating
   is claimed. Distributor metadata describes it as unshielded; verify the
   actual cable's data, shield and CC connectivity before fixing the layout.
4. Put the upstream Type-C sink termination at the carrier: separate Rd
   resistors on CC1 and CC2, provisionally 5.1 kOhm each, with appropriate
   ESD protection. Do not connect upstream CC through to the Feather. Treat
   the bulkhead as a passive extension pending all-orientation tests; a
   purchasable extension is not evidence of USB-IF compliance. Do not substitute
   the Adafruit 4053 C-female-to-A-male host-port extension without checking its
   CC role. No PD or voltage above 5 V is requested.
5. Use a short internal data-capable USB-A-to-C cable, provisionally
   **Adafruit 4472, 152 mm**, from a carrier-only USB-A receptacle to the
   Feather USB-C port. The carrier socket carries selected VBUS, GND and USB
   data; it is an internal device interconnect, not a general host socket.
   It must remain inaccessible for unrelated devices. Its cable provides the
   conventional A-to-C plug termination; this does not grant extra host current.
   The exact active-lifecycle USB-A receptacle remains to be selected.
6. Qualify attachment using **raw upstream VBUS**, not selected VBUS, because
   the Feather remains powered when USB is absent. Reserve a hardware data
   disconnect, preliminarily **TS3USB221E**, powered from main 3.3 V, with one
   pair selected and the other pair unused. Default OE to disconnected; only
   enable D+/D- when raw host VBUS is valid. Select the VBUS detector/level
   translation and sequencing before schematic implementation. Preserve ROM
   download/JTAG operation without relying on application firmware to gate
   its USB pull-up. This is signal disconnection, not galvanic USB isolation.

The intended system states are:

| RECOM | Upstream USB | Feather power | Upstream data path | Output-driver power |
| --- | --- | --- | --- | --- |
| Healthy | Absent | RECOM | Disconnected | RECOM |
| Healthy | Present | RECOM | Enabled after supplies are valid | RECOM |
| Unavailable | Present | USB, within available current | Enabled after supplies are valid | Off |
| Unavailable | Absent | Off | Disconnected | Off |

USB current advertisement, pre-enumeration/suspend behavior, inrush and the
Feather/radio/probe budget remain design obligations. TPS2116's 2.5 A rating
does not negotiate or limit USB current. Sensor heater use must not assume the
computer can supply the full controller supply rating. Choose required current
limiting or load restrictions after checking descriptors and actual peaks.

## Consequences

The three-board-design/four-physical-board partition remains unchanged.
The carrier gains a small low-voltage USB/power group and two internal sockets.
Keep both cable runs in the low-voltage region, provide harness retention and
separation from mains and heatsinks, and reserve plug/bend space without fixing
an enclosure yet. Shield-to-enclosure/ground treatment needs an EMI/ESD design;
do not casually bond USB ground to protective earth. The bulkhead cap, if kept,
does not establish enclosure waterproofing.

Planning cost is approximately **$11-14 per controller**, before assembly,
shipping, taxes or tariffs. On 2026-11-12 the checked single-unit prices were
$4.50 for 6069, $2.95 for 4472, $1.05 for TPS2116DRLR, $0.80 for GCT
USB4105-GF-A, and $0.96 for TS3USB221ERSER: $10.26 subtotal. Allow another
$1-3 for the internal A socket, detection/control, capacitors, resistors and
additional port protection. These allowances are not a priced final BOM.
The earlier $4-7 estimate did not include the panel bulkhead or the data gate.
The screw-ear SparkFun CAB-15455 is a $14.95 alternative bulkhead cable; its
6-inch lead, 18 mm M3 screw spacing and enclosure fit may justify it if nut
mounting is undesirable. Adafruit 4218 is a larger shielded 30 cm alternative,
listed at $12.44 by Mouser.

Before implementation, validate the bulkhead's CC/data mapping and mechanical
fit, choose the remaining parts and limit USB-only loads. After implementation,
check all source/attach states, source failover and recovery, USB voltage in
both directions, enumeration/flashing in ROM and application, supply dips,
current/inrush, cable orientation, ESD/layout and mains separation. Clean ERC
or a block diagram does not establish those results.

## Supersession

Replaces the manual JP1 arrangement as the future planning direction, while
leaving existing native CAD explicitly pending. Does not change ADR-0011's
partition or claim its hardware implemented. Superseded by: None.

## References

- [TPS2116 datasheet](https://www.ti.com/lit/ds/symlink/tps2116.pdf)
- [Feather power guidance](https://learn.adafruit.com/adafruit-esp32-c6-feather/power-management)
  and [schematic](https://github.com/adafruit/Adafruit-ESP32-C6-Feather-PCB/blob/main/Adafruit%20Feather%20ESP32-C6.sch)
- [Adafruit 6069](https://www.adafruit.com/product/6069),
  [Mouser 485-6069](https://www.mouser.com/en/ProductDetail/Adafruit/6069?qs=7%2F6SraaimPTSDPWnRvsZeg%3D%3D),
  [DigiKey shielding metadata](https://www.digikey.com/en/products/detail/adafruit-industries-llc/6069/25897275)
- [Adafruit 4472](https://www.adafruit.com/product/4472),
  [Mouser 485-4472](https://www.mouser.com/en/ProductDetail/Adafruit/4472?qs=CUBnOrq4ZJxdyof1rGiiGQ%3D%3D)
- [Mouser TPS2116DRLR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS2116DRLR?qs=aP1CjGhiNiGo3XAyXcVPaQ%3D%3D)
- [Mouser USB4105-GF-A](https://www.mouser.com/en/ProductDetail/GCT/USB4105-GF-A?qs=KUoIvG%2F9IlY%2FMLlBMpStpA%3D%3D)
- [TS3USB221E datasheet](https://www.ti.com/lit/ds/symlink/ts3usb221e.pdf),
  [Mouser TS3USB221ERSER](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TS3USB221ERSER?qs=OaSNdy%2FNfzkaIRVJErYydw%3D%3D)
- [ST AN4879: host VBUS sensing for self-powered USB](https://www.st.com/content/st_com/en/technical-documents/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics_asset/chunk-003-topic-an4879-vbus-sensing-detection.html)
- [SparkFun CAB-15455](https://www.sparkfun.com/panel-mount-usb-c-extension-cable-6.html)
  and [Mouser Adafruit 4218](https://www.mouser.com/en/ProductDetail/Adafruit/4218?qs=PzGy0jfpSMv4n1zZIh57VA%3D%3D)
