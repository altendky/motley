# Hardware candidates

Status: preliminary consideration record, updated 2026-11-13. These are parts
and arrangements being explored for the sensor controller and two heater
outputs, not a complete bill of materials or an approved hardware design.
Prices and stock below are snapshots from the discussion, before shipping,
tax, tariffs, and assembly overage; check them again before ordering.

The current working plan includes two grounded single AC outlets with insulated
female quick-disconnect terminals. Both a detachable mains cord and a permanently
attached cord remain in play. The MEAN WELL IRM-05-5 is the provisional controller
power supply. Plan for three PCB designs and four physical boards: one integrated
ESP32-C6 controller with AC input and supply, two identical single-output AC modules, and one mux
with sensor connectors on an L-shaped board. The row controls full board length;
the mux/common circuitry fits behind it with a flexible width/depth aspect ratio,
not a fixed connector-count width. The current placement uses the first five
positions, but future placement can spread wider. Tail trimming must preserve
the entire common area. An unwanted socket can be omitted. See
[ADR-0016](../.rqml/adr/0016-flexible-sensor-core-aspect-ratio.md).
Ordinary
pins/plated holes are the provisional low-voltage interconnect approach;
castellations are not planned. Routing, protection, enclosure fit and thermal
qualification remain open. Native CAD now shows the integrated controller;
[ADR-0014](../.rqml/adr/0014-integrated-controller-and-switched-sensor-supply.md)
records the accepted integrated-controller and separate sensor-regulator plan.
See the [three-board study](../hardware/controller/README.md)
and [partition decision](../.rqml/adr/0011-single-output-modules-and-sensor-core.md).

For each individual board, **100 mm in either overall outline dimension is a
strong target maximum**, inclusive of exactly 100 mm. If a larger dimension is
anticipated, discuss the size and tradeoffs with the developer before proceeding
with the enlargement. This permits agreed exceptions; it is not a hard limit or
a manufacturing-panel constraint. Draft `MOT-HW-007/008` capture this direction.
All current trial outlines meet the target.

## Controller and sensor candidates

| Function | Candidate | Position in the discussion |
| --- | --- | --- |
| Controller | [Espressif ESP32-C6-WROOM-1-N8 / JLCPCB C5366877](https://jlcpcb.com/partdetail/Espressif-ESP32_C6_WROOM1/C5366877) | Preliminary integrated-controller choice; JLCPCB lists Economic and Standard assembly. N8 has 8 MB flash; reference N4/N8 price difference was about $0.28. Custom support circuitry and bring-up pending. |
| Earlier development controller | [Adafruit ESP32-C6 Feather, 5933](https://www.adafruit.com/product/5933) | $14.95 reference board; replaced in current native CAD by WROOM-N8. Its battery charger, fuel gauge and daughterboard sockets are omitted from the integrated study. |
| Air temperature and humidity | [7Semi SHT45 probe, ES-12289](https://7semi.com/7semi-sht45-digital-humidity-and-temperature-sensor-probe/) | Provisional choice accepted on 2026-11-11: standard non-membrane stainless tube, 6 mm diameter × 50 mm, 1 m PVC cable, direct I2C at 3.3 V. Listed at $13 each; sensor count and locations remain open. |
| Glass temperature | Sensor part not yet selected | Measurement discussed for heater monitoring and limiting; placement and attachment remain open. |

Four temperature measurements and perhaps two humidity measurements were an
initial exploration. They are not fixed channel counts. Sensor exposure,
condensation, contamination, air exchange, and thermal coupling need assessment
in the intended tank arrangement.

Plan for the standard ventilated, non-membrane ES-12289 rather than the optional
membrane version or the larger ES-13513. Its internal PCB coating, cable-entry
sealing, and whole-probe ingress rating have not been established; do not treat
it as a waterproof or washable assembly. The earlier
[Adafruit SHT45 breakout, 5665](https://www.adafruit.com/product/5665) and a custom
sensor PCB remain alternatives, not the current purchase plan.

The target air conditions discussed are approximately 85 °F and 80% RH.
SHT45 has a specified 0–100% RH measurement range; its recommended normal range
is 20–80% RH, and sustained high humidity can introduce reversible creep.
Periodic built-in heater cycles are acceptable to the developer; their schedule
and cooling interval need validation in the actual probe. See the
[SHT4x datasheet](https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf)
and [heater application note](https://sensirion.com/media/documents/A88858C9/629626D4/Application_Note_Creep_Mitigation_SHT4x.pdf).

An [exploratory KiCad controller schematic](../hardware/controller/README.md)
makes the current component choices reviewable; it is not a fabrication release.

## Multiplexer and carrier alternatives

The user prefers external sensor connectors arranged on one side or in one row.
The separate multiplexer boards below remain reference alternatives while a
custom carrier is explored.

| Candidate | Form and acquisition considerations |
| --- | --- |
| [Adafruit PCA9548 multiplexer, 5626](https://www.adafruit.com/product/5626) | Earlier working candidate. Connectors distributed around the board are inconvenient for this enclosure. |
| [Seeed Grove eight-channel hub, 103020293](https://www.seeedstudio.com/Grove-8-Channel-I2C-Hub-TCA9548A-p-4398.html) | Eight top-entry Grove outputs in a row on a long narrow board. Seeed listed $6.99, but Mouser marked its listing obsolete/restricted. No official successor was identified; lifecycle remains unresolved. Grove-to-QT adaptation would be needed. |
| [DFRobot DFR0576](https://www.dfrobot.com/product-1780.html) | Top-facing output pin headers; different connection system from JST-SH. Mouser price discussed: $6.90. |
| [Arduino Modulino Hub, ABX00100](https://docs.arduino.cc/resources/datasheets/ABX00100-datasheet.pdf) | Eight multiplexer channels; four vertical and four horizontal QT connectors, so only a partial improvement in connector arrangement. |
| Custom sensor board with TCA9548APWR | Current plan: L-shaped board with mux/interface behind the connector row, flexible common-area aspect ratio and eight JST-SH connectors controlling full length. The common area now spans five positions and includes selectable address DIP, two upstream Qwiic sockets and two five-pin deployment headers. All fitted parts are on the front; marked cuts retain five through eight ports. Separate integrated-controller/AC-input and single-output designs remain. Unrouted; enclosure fit, routing and mains separation remain unqualified. |

[Adafruit 4528](https://www.adafruit.com/product/4528) is a Grove-to-STEMMA-QT
adapter cable considered for a Grove hub. Its mapping and the final sensor cable
assembly need checking together.

The following parts were used to explore JLCPCB assembly pricing. Quantities
are per complete controller across the three boards; all remain preliminary.

| Function | Part | Quantity | JLCPCB catalog ID | Price snapshot per part |
| --- | --- | ---: | --- | ---: |
| Multiplexer | [TI TCA9548APWR](https://jlcpcb.com/partdetail/TexasInstruments-TCA9548APWR/C130026) | 1 | C130026 | $0.8214 at 1–9 |
| Horizontal sensor socket | [JST SM04B-SRSS-TB(LF)(SN)](https://jlcpcb.com/partdetail/JST-SM04B_SRSS_TB_LF_SN/C160404) | 8 | C160404 | $0.2147 at 1–49 |
| Vertical sensor socket alternative | JST BM04B-SRSS-TB(LF)(SN) | Instead of horizontal sockets | C160390 | $0.3680 at 1–49 |
| Feather socket | [Kinghelm KH-2.54FH-1X12P-H8.5](https://jlcpcb.com/partdetail/ShenzhenKinghelmElec-KH_254FH_1X12P_H85/C2905419) | 1 | C2905419 | $0.1775 at 1–49 |
| Feather socket | [Kinghelm KH-2.54FH-1X16P-H8.5](https://jlcpcb.com/partdetail/3175195-KH_2_54FH_1X16P_H85/C2905421) | 1 | C2905421 | $0.1756 at 1–49 |

Header height, pin lengths, board spacing, antenna clearance, and USB access
need mechanical checking against the Feather and enclosure.

## Sensor cable and termination candidates

### Additional controller and mux Qwiic access

The current study provides carrier J23/J25 for HP I2C (GPIO19 SDA/18 SCL),
J24/J26 for LP I2C (GPIO6 SDA/7 SCL), sensor J10/J11 parallel upstream Qwiic,
and J12/J13 parallel five-pin deployment/reset. Duplicate sockets share a bus,
not an extra controller. Both carrier pairs source the switched sensor rail
through individual R44-R47 = 0; the mux Qwiic pair shares R50 = 0 before the
local rail. Power links do not isolate data or select between external supplies.
Use one host and supply, with no wiring loops. Main local pulls remain 10k;
LP local pulls remain 4k7, one pair per bus. Mux 4k7 upstream pulls now have
separate removable R55/R56 links for aggregate bus configuration.

Select mux addresses with a provisional [CTS 219-3MSTR / JLC C3012353](https://jlcpcb.com/partdetail/CTS_ElectronicComponents-2193MSTR/C3012353)
three-position SMT DIP switch and three local 10k pull-downs. OFF=0, ON=1;
address=0x70+A0+2*A1+4*A2. This suffix ships ON, so set the desired unique
address unpowered. JLC lists Economic/Standard assembly and Extended status;
observed LCSC price was $1.2892 at one or $1.0543 at ten, not a JLC quote.
CTS specifies dry-circuit life at 0.1 mA/5 V; nominal 0.33 mA/3.3 V use is a
reasonable preliminary signal-level fit, not a separately qualified point.
The stock CTS-family gull-wing land pattern is close to the drawing; exact
actuator height, assembly process and footprint qualification remain open.
[CTS datasheet](https://www.ctscorp.com/Files/DataSheets/Switches/DIP-Switches/CTS-Switches-DIP-219-Series-Datasheet.pdf).

The addressing/chaining expansion adds three Qwiic sockets, one five-pin
header, four TVS arrays, seven 0805 resistors and one DIP relative to the prior
bench-access revision. Allow roughly $2-3 additional parts/joints per complete
unit using earlier price snapshots, before attrition/shipping and any new DIP
loading fee. This is not a production quote. Earlier three-socket bench access
was approximately $1.07/unit before those extras.

Eight distinct addresses are possible per bus; this is not an electrical
rating for eight loaded boards. Configure pulls and aggregate cable capacitance,
reset loading and current/drop for the actual topology. Only one downstream
branch may expose identical-address sensors on a bus at once; firmware must
clear the previous mux before enabling another. Heater pulses continue after
channel deselection, so preserve the one-active-heater schedule across the
connected system. Five-pin chains share reset; Qwiic-only chains omit it.
[ADR-0018](../.rqml/adr/0018-addressed-mux-chains.md) and the
[interface/power record](../hardware/controller/README.md#multiple-mux-boards-and-addressing)
record these choices. Firmware and physical qualification remain future work.

### Probe wiring

For the selected probe, start with its factory 1 m lead and extend as needed;
the extension and controller termination are not yet selected. Prefer extension
joints outside the condensing area and check supply drop with the heater on.
Earlier custom-cable research below covers four-conductor separable stranded
ribbon and individual crimp contacts inserted into JST-SH housings. It is not
FFC/FPC flat-flex cable. Each contact is crimped individually.

| Item | Candidate or constraint |
| --- | --- |
| Connector family | JST-SH, 1.0 mm pitch, four positions; used by STEMMA QT/Qwiic. Verify signal order at both ends. |
| Female cable housing | JST SHR-04V-S-B |
| Crimp contact | JST SSH-003T-P0.2-H; specified for 28–32 AWG and 0.4–0.8 mm insulated wire diameter. |
| Cable currently described in tool research | Owner-reported four-conductor, 28 AWG stranded copper, thin-wall PVC, approximately 0.7 mm insulated diameter and 1.0 mm conductor spacing. Supplier part number and measured dimensions are not recorded here. |
| Earlier gauge alternative | 30 AWG was acceptable in discussion, provided the complete wire construction fits the contact. |
| Earlier commercial ribbon lead | Molex FEP 1000570251, four conductors, 28 AWG, 1.27 mm spacing, approximately 0.74 ± 0.08 mm insulation diameter; the upper tolerance exceeds the SH contact's 0.8 mm limit. Not a confirmed fit. |
| BNTECHGO silicone ribbon on Amazon | The 28 AWG version discussed was too thick for SH contacts. The 30 AWG version's approximately 0.8 ± 0.1 mm diameter was borderline, not a confirmed substitute. |
| Adafruit 3889 | Four-conductor 30 AWG silicone ribbon lead; discussed as a fixed 1 m option, not continuous bulk ribbon for a 6 ft run. |

Primary contact reference: [JST SH specification](https://www.jst.com/wp-content/uploads/2025/06/eSH.pdf).
The cable supplier, exact wire construction, crimp validation, and sourcing
for repeat purchases remain open. No particular ribbon splice was selected.

Approximately 6 ft sensor runs and a 10 kHz I2C clock are explored starting
points. Only one downstream multiplexer channel would be enabled for a
transaction. Inactive bundled cables can still couple capacitively; one-channel
operation does not establish a cable length rating. Pull-ups, total bus
capacitance, rise time, supply drop, and noise margin need checking on the
actual mux, sensor, cable, and bundle. No numerical maximum cable length is
established by this record.

Tool research lives in Tome rather than this project's hardware selection:

- [JST-SH crimping tools](../../tome/research/jst-sh-crimping-tools.md): Engineer
  PAD-02 is the current preference, with PAD-11 dies supplying SH capability.
- [Ribbon stripping tools](../../tome/research/ribbon-wire-strippers.md): Knipex
  12 40 200 EvoStrip is the current preference; short stripping on the exact
  ribbon still needs physical validation.
- [Existing tools](../../tome/property/tools.md): Klein VDV200-010 frame with
  VDV205-035 insulated-terminal and VDV205-036 non-insulated/open-barrel dies.

## AC heater stage candidates

The current exploration is two independently controlled 120 VAC resistive
heater channels, each capable of at least 300 W. At 300 W per channel, nominal
current is 2.5 A each and 5 A combined. Earlier 25–30 W heaters remain relevant
as small loads; they do not define the desired output capacity.

Each proposed channel has a zero-cross optotriac driving a power triac for
frequent modulation, plus a normally open mechanical relay in series for an
additional cutoff. The relay stays energized through normal modulation.
Normal relay changes would occur with the triac off, while the relay must still
interrupt full load if the triac fails short. A modulation window around
10 seconds is an initial thermal-control idea, not a settled timing requirement.

| Function | Preliminary part | Quantity per complete two-output controller | Package and sourcing snapshot |
| --- | --- | ---: | --- |
| Power triac | [ST BTA08-600SWRG](https://www.st.com/resource/en/datasheet/cd00002266.pdf) | 2 | Insulated-tab TO-220 through-hole; 8 A / 600 V device. JLC C153058, $0.6824 at 1–9. Current rating alone does not establish enclosed-board load capability. |
| Zero-cross optotriac | [Lite-On MOC3063S-TA1](https://jlcpcb.com/partdetail/LiteOn-MOC3063STA1/C77950) | 2 | SMT six-pin package; MOC3063-family candidate. JLC C77950, $0.2101 at 1–49. |
| Series cutoff relay | [Omron G6DN-1A-L DC5](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf) | 2 | Through-hole, normally open, 5 A / 250 VAC resistive rating; 5 V, approximately 36 mA coil. Mouser price discussed: $2.38. JLC C6624853 listed $2.0110 at 1–9 but had zero available stock. |
| Small transistor driver lead | MMBT3904 | Circuit-dependent | JLC C20526 was priced as a possible driver component, not selected for a finished circuit. |
| Flyback diode lead | 1N4148W | Circuit-dependent | JLC C81598 was considered for relay-coil suppression; suitability and circuit remain to be finalized. |
| Triac heatsink | [Same Sky HSE-B20350-NP](https://eu.mouser.com/ProductDetail/Same-Sky/HSE-B20350-NP?qs=5aG0NVq1C4zCQ307rYtYwQ%3D%3D), with more compact alternatives below | 2 | Initial candidate: 35 × 29 × 12 mm, TO-220, Mouser 490-HSE-B20350-NP. Natural-convection performance is load-dependent; the headline 12.1 °C/W applies at a 75 °C rise. |
| Heatsink retaining clip | [Same Sky HSC-03](https://www.sameskydevices.com/product/resource/hsc-03.pdf) for the HSE-B20350-NP | 2 | Matching clip, Mouser 490-HSC-03. The developer accepted clip retention; the exact clip follows the eventual heatsink selection. |
| Thermal interface | Thin layer of non-electrically-conductive thermal grease | 2 interfaces | Preferred interface with mechanical clip pressure; exact compound not selected. Adhesive retention is not the current preference. |

The triac discussion estimated roughly 0.2 W dissipation at a 30 W heater and
roughly 2.2 W at 300 W. Those are preliminary electrical estimates, not enclosure
temperature measurements. Heatsink mounting, ambient temperature, ventilation,
and component temperatures need validation.

Manual snubber configuration placeholder, 2026-11-12: each output module fits
the provisional 100 Ohm / 10 nF X2 series RC branch and a 2x2 header J20. Pins
1/3 are the capacitor side and 2/4 are triac A1. Two closed-top shunts across
1-2 and 3-4 enable the branch (default); across 1-3 and 2-4 disable it while
covering all four pins. Rotate both shunts and configure only unplugged and
discharged. No automatic control, extra GPIO or interface signal is selected.
The developer accepted this as a placeholder, with the arrangement still open
to replacement.

The [Harwin M7685-05](https://www.harwin.com/products/M7685-05) is a closed-top,
red, gold-contact, 10 mm-high shunt candidate: two per module / four per unit.
[DigiKey](https://www.digikey.com/en/products/detail/harwin-inc/M7685-05/3727987)
listed $0.49 each; allow roughly $1-1.50 per module for two caps and a header,
excluding assembly/shipping/tax/tariffs. The [Harwin jumper specification](https://www.harwin.com/api/download?document=https%3A%2F%2Fcontent.harwin.com%2Fm%2F79934dbb6c4e2144%2Foriginal%2FC003-C003XX-Component-Specification-M7XXX-Series-2-54mm-pitch-Jumper-Sockets.pdf)
gives 3 A and 250 V DC / AC peak working ratings for this family. Those figures
do not qualify mains transients, PCB spacing or touch protection. The cap's
maximum mating pin length is 5.6 mm; the earlier M20-9990245's 6.1 mm pins are
incompatible. No exact short-pin header has been selected; the KiCad stock
2x2 pattern remains a packaging placeholder. No matching insulating blank cap
was found in the bounded search. The estimated 0.45 mA RMS at 120 V / 60 Hz
does not eliminate pulse-current review: a full 170 V step through 100 Ohm
would initially give approximately 1.7 A, with a 1 microsecond RC time constant.

The [HSE-B20350-NP datasheet](https://www.mouser.com/datasheet/2/1628/hse_b20350_np-3510330.pdf)
gives 28.43 °C rise at 2 W and 40.12 °C at 3 W in natural convection.
Interpolation at 2.2 W gives approximately 31 °C heatsink rise above local air,
before adding the mounting interface and junction-to-case temperature rises.
Internal mounting with passive ventilation is plausible, not qualified; both
channels and the other enclosure heat sources must be included in testing.

For a narrower board layout, the [Boyd/Aavid 534202B02853G](https://www.mouser.com/datasheet/2/2/Aavid_04102019_534202B02853_Aavid_Thermalloy_11631-1568321.pdf)
is a compact alternative under consideration: vertical mounting, approximately
25.4 × 12.7 mm footprint and 29.97 mm height, with a device clip and Shur-Lock
board tabs. Its published 13.4 °C/W rating is at a 75 °C rise in natural
convection, not a constant resistance established at our 2.2 W dissipation.
[Boyd lists the dimensions](https://cn.boydcorp.com/thermal/air-cooling/heat-sinks.html),
and [Mouser lists the part](https://eu.mouser.com/c/thermal-management/heat-sinks/?designed+for=TO-220&mounting+style=Through+Hole&pg=2).
Its approximate body footprint is 68% smaller than the initial heatsink, at the
cost of about 18 mm more height. Exact board clearance, clip fit to the selected
insulated TO-220 package, price, and low-power thermal performance need checking
before selection.

The developer clarified that the Boyd stamped/folded alternative is not the
desired upgrade: extruded construction is preferred. The 534202B02853G remains
a packaging reference, not a cooling improvement over the original Same Sky
(13.4 versus 12.1 °C/W, both quoted at a 75 °C rise).

### Extruded heatsink shortlist

Research snapshot: 2026-11-10. These remain candidates, not qualified selections.
Clips with thermal grease remain preferred; screw-mounted alternatives are
identified explicitly. Listed body dimensions exclude any additional space
needed for the triac, clip operation, leads, fasteners, and electrical clearance.
Prices below are quantity-one USD snapshots before shipping, tax, and tariffs.

Packaging preference clarified after this shortlist: the developer expects to
favor more board area and less height above the PCB; no enclosure or numerical
height limit has been selected. Favor low-profile extrusions in further
selection. The original HSE-B20350-NP with HSC-03 clip therefore remains a
stronger packaging candidate than the tall alternatives below.

| Candidate | Body size (mm) | Device and board attachment | Cooling evidence | Sourcing snapshot |
| --- | --- | --- | --- | --- |
| [Ohmite WA-T220-101E](https://www.ohmite.com/catalog/w-series-heatsink/WA-T220-101E) | Approximately 18.3 × 16 footprint, 30.5 high | Integrated spring clip and solderable PCB feet | Manufacturer quotes 12 °C/W in natural convection at **10 W**; that is not a 2.2 W rating. Low-load curve and final assembly need assessment. | [DigiKey](https://www.digikey.com/en/products/detail/ohmite/WA-T220-101E/2202817) listed $3.34 and over 37,000 in stock. [Mouser](https://www.mouser.com/ProductDetail/Ohmite/WA-T220-101E?qs=TVIBDWOgMcXN3XlHAuYPZQ%3D%3D), 588-WA-T220-101E, marked restricted availability; do not treat it as a confirmed Mouser purchase option. |
| [Wakefield 693-25](https://wakefieldthermal.com/content/data_sheets/690%20%281%29.pdf) | Approximately 25 × 22.1 footprint, 35.05 high, excluding PCB pins | Integrated TO-220 holding clip and solderable PCB retaining pin | Visual reading of the page-two natural-convection graph for 25 mm / one device suggests approximately **39 °C rise at 2.2 W**; this is an approximate graph reading, not tabulated data or a measurement. | [Mouser](https://www.mouser.com/en/ProductDetail/Wakefield-Thermal/693-25?qs=vLWxofP3U2xs2JVhTO%252B%2F7Q%3D%3D), 567-693-25, listed $8.34, 197 in stock, minimum one. |
| [Same Sky HSE-B254-04H](https://www.sameskydevices.com/product/resource/hse-bx-04h.pdf) | 16.5 × 16 footprint, 25.4 high; excludes 4 mm pins below the body | Component #6-32 threaded mounting hole; two PCB placement pins. No matching clip established. | Published natural-convection rises: 33.54 °C at 2 W and 49.96 °C at 3 W; interpolate approximately **37 °C at 2.2 W**. | [Mouser](https://www.mouser.com/en/c/thermal-management/heat-sinks/?designed+for=TO-218%2C+TO-220), 490-HSE-B254-04H, listed $1.37, over 2,300 in stock, minimum one. |
| [Same Sky HSE-B381-04H](https://www.sameskydevices.com/product/thermal-management/heat-sinks/board-level-heat-sinks/extruded-heat-sinks/hse-b381-04h) | 16.5 × 16 footprint, 38.1 high; excludes 4 mm pins below the body | Taller version of the same screw-mounted profile, with two PCB placement pins | Published natural-convection rises: 26.70 °C at 2 W and 41.68 °C at 3 W; interpolate approximately **30 °C at 2.2 W**. | [Mouser](https://www.mouser.com/en/c/thermal-management/heat-sinks/?designed+for=TO-218%2C+TO-220), 490-HSE-B381-04H, listed $1.47, 529 in stock, minimum one. |

The Ohmite is a compact clip-mounted mechanical alternative if extra height and
sourcing outside Mouser are acceptable. The Wakefield retains a Mouser clip option, with
an estimated temperature rise higher than the original baseline. The two
small Same Sky profiles supply quantified thermal alternatives if screw
attachment is acceptable. The original HSE-B20350-NP remains the baseline with
approximately 31 °C rise at 2.2 W; none of these comparisons establishes final
enclosure temperatures.

The Same Sky HSE-BX-04H mechanical drawing was visually inspected: its cut
length is the mounted height, and its two solder pins project below that end.
The catalog's length/width/height fields alone do not identify board footprint.
The heatsink body footprint is approximately 74% smaller than the original
35 × 29 mm heatsink; the populated assembly needs additional device and
clearance allowance.

Primary evidence: [Ohmite W-series datasheet](https://www.mouser.com/datasheet/3/132/1/sink_w.pdf),
[Wakefield 690-series datasheet](https://wakefieldthermal.com/content/data_sheets/690%20%281%29.pdf),
and [Same Sky HSE-BX-04H datasheet](https://www.sameskydevices.com/product/resource/hse-bx-04h.pdf).

### Electrical isolation and remaining stage questions

The BTA08-600SWRG's internal ceramic insulation separates its mounting tab from
the live terminals; ST rates the insulated tab at 2500 V RMS. The thermal grease
is not the electrical isolation barrier. This differs from the non-insulated
BTB08 package. Clip and heatsink clearance from live leads and PCB conductors
still need design review; the tab rating alone does not establish an accessible
heatsink's safety classification. See the linked ST triac datasheet.

The G6DN relay's suitability for repeated cold/dry switching remains open.
Gold-plated/twin-contact features do not by themselves prove that contact
resistance stays satisfactory without normal load-switching cleaning action.
The selected load, duty profile, coil drive, and failure interruption need review.

The user does not want a separate protection temperature sensor. The additional
relay supplies a second cutoff actuator; it does not independently protect
against a shared sensor or controller failure. Triacs can fail short and relay
contacts can weld closed. A normal-current heater stuck on need not blow its
fuse. Fault handling and the scope of independent cutoff control remain open.

Supporting resistors, optocoupler input drive, relay drivers, isolated low-voltage
power supply, mains-rated wiring/connectors, fusing, transient protection,
clearances, enclosure, and final schematic are incomplete.

### AC control, feedback and bus investigation

Discussion direction, 2026-11-13; hardware selection and circuit changes remain
pending. Investigate both leading-edge phase-angle control for compatible lamps
and zero-cross, whole-cycle burst-fire/time-proportional control for heaters.
The current BTA08 power triac remains a candidate for both. The existing
MOC3063 zero-cross optotriac cannot provide phase-angle triggering; compare a
non-zero-cross driver plus isolated mains timing. Gate drive, lamp inrush and
EMI filtering need review before changing the circuit. See
[ST AN5114](https://www.st.com/resource/en/application_note/an5114-controlling-a-triac-with-a-phototriac-stmicroelectronics.pdf).

The feedback objective is to compare actual conduction with commanded
conduction, including unexpected delivery while commanded off. Investigate
per-output voltage detection and current sampling, with true RMS as a useful
extension. Compare sensed conduction timing with the line reference; do not
treat a slow averaged reading as proof of correct phase-angle firing. Resolve
snubber leakage thresholds, minimum detectable load, absent-load/latching
limitations, and detection before versus after the cutoff contact. Zero current
alone cannot distinguish an unplugged load from a non-firing output stage.

Bus connectivity is now a hardware-selection consideration, without selecting
I2C or committing to bus-controlled firing. Candidate approaches:

| Approach | Evidence and selection questions |
| --- | --- |
| Allegro ACS37800 | [Manufacturer datasheet](https://www.allegromicro.com/-/media/files/datasheets/acs37800-datasheet.pdf): I2C variants, configurable addresses, integrated isolated Hall current sensing, RMS voltage/current, power and configurable zero-cross/fault outputs. Check current range/noise at small and dimmed loads, 1 kHz bandwidth and phase-cut measurement error, update latency, voltage-sensing isolation and complete circuit cost. |
| ADI ADE7953 | [Manufacturer information](https://www.analog.com/en/products/ade7953.html): I2C/SPI/UART, RMS, waveform and power measurements. Requires external sensing circuitry and an explicitly engineered isolation/power boundary. Its fixed I2C address needs consideration for repeated output modules. |
| Isolated current sensor plus ADC/controller | Compare a Hall sensor or CT with local conversion and bus readout. A local controller could also generate line-synchronous gate timing and enforce a command timeout. Quantify the added parts, firmware and failure modes against dedicated metering ICs. |

These are research leads, not qualified parts or purchase selections. Keep
measurement readout separate from firing control: an I2C sensor or ordinary
GPIO expander does not itself supply synchronized phase-angle timing. Compare
central timing with locally timed output modules, including startup defaults,
lost or stale commands and whether a cutoff path remains usable with a stalled
bus. Preserve the device-local temperature-control direction.

An open alternative is one normally open cutoff relay in the common controlled
load feed, replacing the individual output relays. This could reduce repeated
hardware and deliberately remove all heater/lamp power after a fault; it also
loses independent cutoff and makes one relay a shared failure point. Keep the
controller supply branch ahead of any proposed load cutoff so the controller
can remain powered to diagnose and report a trip. Review whether input and
per-channel feedback still identify the failing stage after a global cutoff.

At two 300 W loads and 120 VAC, nominal combined load current is 5 A. The
existing [G6DN](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf)
is rated for 5 A carry/switching; a common relay would need selection for the
combined load, inrush and intended expansion rather than simply relocating
that part. No relay topology change is selected; the current schematic and
per-channel relays remain as drawn.

## AC outlets and terminals

| Item | Current working position | Price snapshot |
| --- | --- | ---: |
| [Qualtek 738W-X2/03](https://www.mouser.com/en/ProductDetail/Qualtek/738W-X2-03?qs=HFfMDpzxxd1SmutvsrmPJA%3D%3D) | Plan for two single grounded NEMA 5-15R snap-in outlets, no lid. 15 A / 125 VAC component rating. | $1.33 each at Mouser; $2.66 for two |
| Insulated female quick-disconnect terminals | Working connection approach; exact part and internal wire gauge still to be selected. Six terminals for the two outlets, plus any required by the input arrangement and other components. | Not priced |

The outlet [drawing](https://www.qualtekusa.com/images/AC_Receptacles/pdfs/738wx203.pdf)
specifies a 26 × 22 mm cutout, 0.8–2.0 mm panel thickness, and approximately
4.8 mm wide, 0.6 mm thick tabs. The terminals support soldering as well as the
cataloged .187 inch quick-disconnect connection. Match female-terminal tab
thickness capability, wire range, insulation, and crimp tooling before ordering.

Conventional pre-insulated closed-barrel terminals are the intended category
for the existing Klein VDV205-035 die. A fully insulated connector containing
an open crimp barrel may require different tooling. PAD-12S/PAD-13S cover some
open-barrel quick-disconnect contacts, depending on the exact part.

Soldering remains technically possible but is not the current wiring plan.
Grounded outlets preserve compatibility with future grounded heaters. Protective
earth would pass continuously to the outlets; the proposed switching acts on
the hot conductor, not protective earth. Enclosure protection needs its own
assessment.

Styles considered but set aside for this arrangement include the covered
Altech PMRBA ($11.78 at Mouser), the large round flange of the Leviton 5279-C
(approximately $20), and duplex outlets. The user prefers individual placement,
no cover, and compact mounting. Leviton 5258-SS short-strap singles were another
screw-mounted alternative (Gordon price discussed: $7.77), before returning to
the smaller snap-in Qualtek.

## Both power entry options remain open

| Arrangement | Candidate parts | Benefits and unresolved details |
| --- | --- | --- |
| Detachable cord | [Qualtek 719W-00/03 fused IEC C14 inlet](https://www.mouser.com/en/ProductDetail/Qualtek/719W-00-03?qs=HFfMDpzxxd0cIbY2W7udQg%3D%3D), $2.27 at Mouser, plus NEMA 5-15P-to-C13 cord | Screw-mounted inlet, 10 A / 250 VAC rating, .187 inch quick-disconnect tabs, integrated fuse holder. Cord and actual fuse are not selected. |
| Permanently attached cord | [Qualtek 311007-01](https://www.mouser.com/en/ProductDetail/Qualtek/311007-01?qs=Hvek%2Fj8XCASvHrBoncML4w%3D%3D), approximately $6, plus [Heyco 1150 / SR 5N-4](https://www.mouser.com/en/ProductDetail/Heyco/1150?qs=lnCxUF7NcEva7gG44r6ZVQ%3D%3D), $0.10 at Mouser | Grounded NEMA 5-15P plug, 2 m, 18/3 SVT, 10 A / 125 VAC cord with free wire ends. Bushing supplies enclosure strain relief; separate fuse holder needed. |

The [Heyco bushing specification](https://www.heyco.com/wp-content/uploads/wpallimport/files/Original-Strain-Relief-Round-1.pdf)
lists 18/3 SVT around 6.5 mm diameter and a maximum 1.6 mm mounting panel.
The [Qualtek cord drawing](https://www.qualtekusa.com/images/Power%20Cords/PDF%20Files/31100701.pdf)
does not specify jacket diameter, so the exact cord/bushing fit and shaped
panel cutout remain to be confirmed. A thicker panel would need a different
bushing variant or a suitable mounting detail.

Other input references considered were the plain screw-mounted C14
Qualtek 703W-00/03 (approximately $1.08, separate fuse holder needed) and
snap-in fused C14 Qualtek 723W-X2/03 (approximately $2.72). A threaded Heyco
cord grip, such as M4336, is an alternative to the snap-in bushing if adjustable
grip or different panel mounting becomes useful. These do not replace the
two open arrangements above.

## Controller power supply

Plan provisionally for one **MEAN WELL IRM-05-5** encapsulated, isolated,
through-hole AC/DC module per controller, supplying 5 V at 1 A (5 W). It powers
both heater channels' relay coils and the controller/sensors. This is a component choice
for planning; the power budget and final circuit are not yet validated.

| Candidate | Position in the discussion | Body size, L × W × H | Price/source snapshot |
| --- | --- | --- | --- |
| [MEAN WELL IRM-05-5 / JLC C48603696](https://jlcpcb.com/partdetail/50875454-MW_PCB_AC_DC_5W_IRM_055/C48603696) | Selected provisionally on 2026-11-13; 5 V, 1 A; Economic/Standard wave assembly | 45.7 × 25.4 × 21.5 mm | JLC $4.9277 each, MOQ 1; 2,682 orderable in the live 2026-11-13 check |
| [RECOM RAC05-05SK](https://www.mouser.com/en/ProductDetail/RECOM-Power/RAC05-05SK?qs=BZBei1rCqCAuA5d34muF0w%3D%3D) | Previous choice retained as a compact alternative; 5 V, 1 A | 25.4 × 25.4 × 16.5 mm | Mouser $12.27 for one, in-stock snapshot 2026-11-11; exact JLC C5199917 had no stock on 2026-11-13 |

The developer accepted the MEAN WELL substitution and explicitly retained the
Omron G6DN-1A-L DC5 cutoff relays. Native PS1 now uses the stock IRM-05 symbol
and footprint: pin 1 neutral, 2 fused line, 3 secondary GND and 4 raw 5 V.
This is a four-pin replacement, not a renaming of the five-pin RECOM pattern.
The larger body is accommodated by rearranging the carrier study within its
existing 100 x 85 mm outline. Both output boards remain unchanged.

The [MEAN WELL datasheet](https://www.meanwell.eu/Upload/PDF/IRM-05/IRM-05-SPEC.PDF)
documents safety approvals, Class II construction, 200 mVpp maximum ripple and
71% typical full-load efficiency for the 5 V version. Its 2025 revision lists
4.2 kVAC input/output withstand, while the JLC catalogue says 3 kV: confirm
the stocked revision before relying on the higher value. Nominal 5 V at +2.5%
plus a conservative full 0.2 V ripple allowance is 5.325 V, below the power
selector's 5.5 V recommended ceiling; this arithmetic is not a transient or
overvoltage-protection qualification. Check ripple, startup/transfer, inrush,
fuse coordination and enclosed-temperature derating in hardware. At full
5 W output, 71% efficiency implies about 2.04 W loss; actual load is lower.
The module requires non-condensing conditions. Earlier JLC quote exports
and cost tables describe the preceding CAD/supply selection and are historical.

The proposed supply takeoff is from fused mains ahead of the heater switching
stages, so the controller remains powered while heating is disabled. Its 5 V
rail feeds the relay drivers directly and the controller through automatic
source selection. The selected 5 V rail feeds separate controller and sensor
3.3 V regulators in parallel. The two selected relay coils together draw approximately
72 mA at 5 V. Allow for radio peaks, sensors, optotriac drive, decoupling, and
enclosure temperature when confirming supply capacity and derating.

The current plan uses WROOM-N8 directly on the controller board, automatic
onboard mains-supply priority / optional USB backup, and one external USB-C sink interface.
There is no internal USB-C source port or Feather cable. Retain independent
raw-host-VBUS data qualification and mains-supply-only output-driver power. The
unrouted exploratory CAD now represents this direction, including the USB
harness and separate regulator circuits; it is not a fabrication release.
See [ADR-0014](../.rqml/adr/0014-integrated-controller-and-switched-sensor-supply.md).

### Separate switched sensor supply

Plan a separate [Diodes AP2112K-3.3TRG1 / JLCPCB C51118](https://jlcpcb.com/partdetail/C51118)
from selected 5 V to `+3V3_SENS`, in parallel with the ESP's main 3.3 V
regulator. The mains supply normally powers it; USB can supply it during bench operation
within the host current budget. The drawing places the regulator on the
controller with GPIO11 controlling active-high EN and a local 10k pull-down.
This replaces GPIO20/100k after the pin-bias review found its reset pull-up
could enable the regulator. Sensor SDA/SCL/reset startup pulls remain an open
off-domain issue; changing EN alone does not qualify rail-off behavior.
The mux and its pull-ups share this switched rail, retaining the five-pin
sensor-board interface. The grounds are
common. This is separate regulation, not galvanic isolation.

The [AP2112 datasheet](https://www.diodes.com/datasheet/download/AP2112.pdf)
documents enable control, output discharge and the required input/output
capacitors. The observed regulator price was about $0.17; allow $0.30-0.70
incremental parts per board including capacitors/resistor, before assembly.
An additional Extended part type can add a batch loading fee; using the same
regulator elsewhere may avoid another distinct setup.

Keep the preliminary one-sensor-heater-at-a-time schedule. Qualify regulator
thermal dissipation, sensor startup and cable drop, shared 5 V/USB current,
and I2C/reset back-power paths before promising power-cycle recovery. The 600 mA
headline rating is not the enclosed-board continuous current budget. SDA, SCL
and mux reset must remain high impedance without internal pull-ups while the
sensor rail is off; actual back-power and startup behavior remain unverified.

### Receiver-local output-command protection

The developer accepted this inexpensive prototype correction on 2026-11-12.
Each output board now has two **ST(Semtech) 1N4148W, JLC C81598** blocking
diodes, one in each command: anode toward the controller/J14, cathode toward
the transistor base resistor. Keep both 10k base-emitter pull-downs and 100n
base-emitter filters on the receiving board, after the diodes. R102 is 470 ohm
for the opto driver; R106 is 150 ohm for the coil driver. Retain the existing
MMBT3904s and coil flyback diode. CUT2 moves from GPIO7/MTDO to GPIO0; sensor EN
moves from GPIO20 to GPIO11. No extra GPIO or inter-board contact is added.

Four diodes and four capacitors per complete two-output unit add $0.1048 in
components at the recorded JLC low-quantity prices ($0.0124 and $0.0138 each),
plus $0.0256 in Economic solder-joint charges. These are Basic parts, so this
choice introduces no Extended-type loading fee. Resistor substitutions add
no placements. This estimate excludes attrition, tax/shipping, unchanged setup
and any final manufacturer change to the existing generic transistor.
[Diode listing](https://jlcpcb.com/partdetail/C81598),
[capacitor listing](https://jlcpcb.com/partdetail/C49678),
[assembly charges](https://jlcpcb.com/help/article/pcb-assembly-price).

This blocks the identified return through the other LOW command when ground
opens first; it is not a completed live-unplug qualification. The source-backed
drive scenarios and remaining loaded-VOH, cold-drop, hot-leakage, transient and
release-time checks are in [the pin-bias review](../hardware/controller/pin-bias-review.md).

### ESD and low-cost handling access

The current unrouted study provisionally fits Nexperia
[PESD5V0S2BT,215 / C49338](https://jlcpcb.com/partdetail/C49338) dual
bidirectional clamps for 3.3 V signals/rails and onsemi
[ESD5Z6.0T1G / C82323](https://jlcpcb.com/partdetail/C82323) 6 V-standoff
single clamps for raw 5 V and USB VBUS. There are 34 duals, five singles and
16 sensor-data 100 ohm series resistors per complete two-output unit.
Bidirectional command clamps preserve the missing-ground blocking function;
ordinary unidirectional signal clamps would not be a suitable substitution.

Allow approximately $3.31/unit for those protection parts and Economic joints,
including eight carrier Qwiic TVSs but excluding sockets, DIP and bus pulls.
Two new Extended types can add loading fees: approximately $15.35 across
separate carrier, output and sensor assembly jobs, not per unit. Bare ground
touch pads and probe footprints add no purchased contacts. Sixteen positions
accept optional hand-formed two-hole wire loops; three sensor diagnostic
positions accept single-hole posts. The default includes no fitted loop part.

See [ESD and access review](../hardware/controller/esd-access-review.md) for
all connector/contact dispositions, standoff/clamp limits, prices, per-board
probe maps and pending panel CC/shield, physical handling and system-immunity
qualification. Touch points reference isolated local LV GND, not earth.
Mains protection and PE continuity remain separate; no logic TVS to mains or
new PE-to-GND bond is introduced. Native requirement fields and RQML file
relationships now make this study inspectable through its governing inputs.

### USB power and enclosure interface candidates

#### Current integrated-controller panel port

Provisionally use one [Adafruit 6153](https://www.adafruit.com/product/6153)
USB-C female panel-mount pigtail per controller, accepted for now on
2026-11-12. The observed price is $2.95. It uses a round nut mount
(manufacturer hole range 11-13.5 mm, panel thickness up to 7 mm) and a six-pin
JST-PH internal connector carrying VBUS, GND, D+/D-, CC1 and CC2.
[DigiKey's listing](https://www.digikey.com/en/products/detail/adafruit-industries-llc/6153/26249970)
specifies 175 mm overall length and unshielded individual wires.

**Unresolved preference: a more robust USB assembly with a shielded internal
cable and a defined shield/shell connection.** Accepting 6153 for the prototype
does not satisfy or withdraw that preference. Revisit shielding, data-pair
construction, cable retention/strain relief and panel retention before settling
the enclosure and final harness. No ingress or USB compliance rating is assumed.

Adafruit documents separate built-in 5.1 kohm pull-downs on CC1 and CC2;
omit duplicate carrier-board pull-downs when using this assembly. Those
resistors indicate a sink; they do not establish the product page's claimed
2 A entitlement. The host's available current still limits USB-only operation.
The carrier needs a matching six-position JST-PH header and the existing
planned USB protection, raw-host-VBUS qualification and power selection.
Before relying on the harness, check its pinout/CC resistance, both external
plug orientations, ROM flashing and USB serial while the heater outputs switch.
Confirm the actual panel fit and internal connector passage on a sample before
fixing the cutout. Native CAD and PDFs now include a mating six-pin JST-PH
header; its project-defined pin order (VBUS, GND, D+, D-, CC1, CC2) remains a
placeholder pending actual harness verification/repinning. It is not a verified
drop-in cable pinout.

The exploratory USB/power drawing uses TPS2116DRLR, a TS3USB221ERSER data
switch and USBLC6-2SC6 protection. A newly concrete, unpriced
[TLV3011BIDBVR](https://www.ti.com/lit/ds/symlink/tlv3012.pdf) comparator candidate
qualifies raw VBUS independently of firmware: its reference versus a
226k/100k divider enables the active-low switch at approximately 4.05 V.
The B variant's fail-safe inputs and POR behavior matter. A 47k pull-up defaults
to data disconnect. Main and sensor AP2112 regulators share selected 5 V.
These parts and starting values are represented for review, not qualified for
USB current, inrush, suspend, sequencing, assembly availability or thermal use.

#### Historical Feather interface candidates

Historical Feather arrangement, superseded by ADR-0014: the component leads and
price snapshots below remain research references, not the current BOM. The
integrated controller retains a single external USB-C sink and host-VBUS
qualification; internal source-port circuitry/cables below are no longer needed.

The earlier preliminary topology was panel USB-C extension -> carrier sink USB-C socket
-> carrier data gate / power selection -> internal USB-C source socket -> short C-to-C
cable -> Feather USB-C port. RECOM feeds TPS2116 VIN1; raw host VBUS feeds VIN2;
its selected output powers the Feather. Output drivers stay on raw RECOM so
USB-only bench operation leaves their 5 V rail off. Remove the direct JP1 path
when implementing. No new output/sensor-board interface signal is planned.
Power internal source-port attachment logic from selected 5 V or its own
regulator, not the Feather's 3.3 V, which depends on that port already being on.

| Function | Preliminary candidate | Quantity per controller | Checked one-off price / remaining qualification |
| --- | --- | ---: | --- |
| Panel USB-C female / internal C male | [Adafruit 6069 / Mouser 485-6069](https://www.mouser.com/en/ProductDetail/Adafruit/6069?qs=7%2F6SraaimPTSDPWnRvsZeg%3D%3D) | 1 | $4.50; compact round nut mount, nominal 300 mm lead. [Manufacturer](https://www.adafruit.com/product/6069) describes 12-18 mm hole range and up to 13 mm panel. Verify exact cutout/sample, CC/data in all orientations, shielding and retention. No waterproof or USB-IF compliance claim. |
| Automatic priority power mux | [TI TPS2116DRLR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS2116DRLR?qs=aP1CjGhiNiGo3XAyXcVPaQ%3D%3D) | 1 | $1.05; VIN1 preferred, VIN2 optional backup, automatic recovery to VIN1. Select worst-case PR1 divider; 2.5 A device rating does not establish USB current entitlement. |
| Carrier upstream USB-C receptacle | [GCT USB4105-GF-A](https://www.mouser.com/en/ProductDetail/GCT/USB4105-GF-A?qs=KUoIvG%2F9IlY%2FMLlBMpStpA%3D%3D) | 1 | $0.80; USB 2.0, SMT with through-hole shell stakes. Independent sink Rd on each CC pin; ESD/protection and footprint still to qualify. |
| Hardware USB data disconnect | [TI TS3USB221ERSER](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TS3USB221ERSER?qs=OaSNdy%2FNfzkaIRVJErYydw%3D%3D) | 1 | $0.96; candidate with OE and powered-off leakage support. Enable one selected pair only when raw host VBUS is valid; detector/level translation is not selected. |
| Internal carrier-to-Feather cable | Short data-capable C-to-C cable, exact part pending; [Adafruit 6370](https://www.adafruit.com/product/6370) is a packaging candidate | 1 | 6370 is $6.95, 100 mm, right-angle, with manufacturer-confirmed power/data/CC wiring. Check reach and plug direction; seek a suitable lower-cost option before selecting. The A-to-C 4472 is rejected. |
| Carrier internal USB-C source interface | USB-C receptacle, source CC/attachment logic and controlled VBUS with discharge/current protection | 1 | Exact parts/cost pending; TUSB320LAI is a research candidate. Do not copy the input port's sink Rd termination or simply rename the A socket. External and internal CC remain independent. |
| Supporting components | Host detector/level translation, decoupling, divider resistors and additional port protection | Circuit-dependent | Reprice after selecting Type-C source support; not a final BOM. Avoid selecting last-time-buy USB connectors. |

The previous **$11-14** estimate used the rejected intermediate A socket and
A-to-C cable; it is no longer the current total. Reprice the C-to-C cable and
source-side Type-C support before giving a new complete budget. The $4.50
bulkhead, $1.05 mux, $0.80 input receptacle and $0.96 data-switch snapshots
remain component leads. A screw-ear
[SparkFun CAB-15455](https://www.sparkfun.com/panel-mount-usb-c-extension-cable-6.html)
is an alternative: $14.95, 152 mm lead, 18 mm M3 mounting pitch. The larger
[Adafruit 4218](https://www.mouser.com/en/ProductDetail/Adafruit/4218?qs=PzGy0jfpSMv4n1zZIh57VA%3D%3D)
is a shielded 30 cm round alternative at $12.44. Those choices increase the
total by their difference from the $4.50 panel cable; they are not added ports.

The panel candidate's linked PDF drawing returned 404 during this research;
do not treat the broad mounting description as a production cutout. Retain
sample/drawing checks before enclosure design. Distributor metadata describes
6069 as unshielded; do not assume its cap or body provides an ingress/EMI rating.
Both cable routes stay on the low-voltage side, with retention clear of mains
wiring and heatsinks. The no-cover preference for AC outlets does not select
or require a cover on this USB port; its supplied cap is optional.

A self-powered Feather needs raw-host-VBUS-qualified USB attachment, not just
power isolation: selected 5 V remains live without a host. Plan the data gate
to prevent presenting the Feather's pull-up to an unpowered/disconnected host;
check ROM flashing/JTAG as well as application serial. See [ST VBUS guidance](https://www.st.com/content/st_com/en/technical-documents/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics_asset/chunk-003-topic-an4879-vbus-sensing-detection.html)
and [TI TS3USB221E](https://www.ti.com/lit/ds/symlink/ts3usb221e.pdf).
TPS2116 failover tolerances, chatter/dips, USB current advertisement, inrush and
suspend behavior remain unqualified. USB-only radio/probe/heater scheduling
must fit available host current; the mux is neither a PD negotiator nor a USB
current limiter. No firmware behavior or hardware tests are claimed by this plan.

### Other power-supply references

The Amazon example discussed was an HLK-PM03, a 3.3 V module; the related
HLK-PM01 supplies 5 V at 600 mA. These illustrate the same module approach but
are not the selected supply. Manufacturer references:
[RECOM RAC05-K datasheet](https://recom-power.com/pdf/Powerline_AC-DC/RAC05-K.pdf),
[Mean Well IRM-05 datasheet](https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.pdf),
and [Hi-Link 3 W module specifications](https://hilinkpower.com/Uploads/ProductClass/4gvpx3a5es1vz.pdf).

## Fabrication and cost context

Hand soldering SMT is acceptable to the user. A custom carrier can therefore
use SMT parts even when through-hole alternatives exist. JLCPCB assembly is
another option; the through-hole triacs, relays, and daughterboard sockets need
the appropriate assembly process or manual installation.

At the discussed price tiers, the mux, eight horizontal SH sockets, two triacs,
two optotriacs, two relays, and two Feather socket strips total approximately
$8.70 per board for a two-board batch, or $8.01 per board for a five-board
batch. These are component-price calculations per complete controller, now
distributed across three boards, not purchasable complete assemblies:
relay stock was unavailable and the supporting parts remain incomplete.

An earlier planning allowance of roughly $60–100 for two populated carriers
before shipping/tax excluded Feather modules, heatsinks, and enclosures and was
not a vendor quote. PCB dimensions, complete BOM, placement files, assembly
fees, and shipping are needed for a meaningful final comparison. See
[JLCPCB's assembly pricing](https://jlcpcb.com/help/article/pcb-assembly-price).

### Three-board manufacturing comparison, 2026-11-12

A direct anonymous query to [JLCPCB's calculator](https://cart.jlcpcb.com/quote)
returned $4 for five 100 x 100 mm boards, $4 for five 50 x 100 mm boards and
$11.30 for five 150 x 100 mm boards. Settings: two layers, green solder mask,
1.6 mm FR4, 1 oz copper and leaded HASL, no special processes, before shipping
and taxes. Both smaller sizes also showed an eligible $2 promotional amount;
eligibility for a combined final order has not been checked.

The published Economic assembly setup/stencil amounts were $8.18 + $1.53 per
separate job. Two jobs therefore add $9.71 fixed overhead compared with one;
three add $19.42 compared with one. Duplicated Extended-part loading fees,
minimum quantities/overage, interconnects and shipping can change that comparison.
There are still three distinct designs: buy twice as many identical output
modules as carriers/sensor boards for the current two-outlet unit. The current
trial outlines are 100 x 85 mm for the carrier, 100 x 50 mm for each output
module, and 80 x 44 mm overall for the L-board. These are exploratory placements, not
quoted final Gerbers or a reason to reduce necessary mains/thermal allowances.
