# Hardware candidates

Status: preliminary consideration record, updated 2026-11-10. These are parts
and arrangements being explored for the sensor controller and two heater
outputs, not a complete bill of materials or an approved hardware design.
Prices and stock below are snapshots from the discussion, before shipping,
tax, tariffs, and assembly overage; check them again before ordering.

The current working plan includes two grounded single AC outlets with insulated
female quick-disconnect terminals. Both a detachable mains cord and a permanently
attached cord remain in play. The custom carrier board, sensor connections,
power supply, protection, and thermal design still need development.

## Controller and sensor candidates

| Function | Candidate | Position in the discussion |
| --- | --- | --- |
| Controller | [Adafruit ESP32-C6 Feather, 5933](https://www.adafruit.com/product/5933) | Working controller target; also considered as a socketed daughterboard on a custom carrier. Mouser price discussed: $14.95. |
| Air temperature and humidity | [Adafruit SHT45 breakout, 5665](https://www.adafruit.com/product/5665) | Favored candidate; sensor count and measurement locations remain open. |
| Glass temperature | Sensor part not yet selected | Measurement discussed for heater monitoring and limiting; placement and attachment remain open. |

Four temperature measurements and perhaps two humidity measurements were an
initial exploration. They are not fixed channel counts. Sensor exposure,
condensation, contamination, air exchange, and thermal coupling need assessment
in the intended tank arrangement.

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
| Custom carrier with TCA9548APWR | Eight JST-SH connectors in a row, Feather sockets, and two AC stages on one board. Schematic, layout, enclosure fit, and mains separation are not yet designed. |

[Adafruit 4528](https://www.adafruit.com/product/4528) is a Grove-to-STEMMA-QT
adapter cable considered for a Grove hub. Its mapping and the final sensor cable
assembly need checking together.

The following parts were used to explore JLCPCB assembly pricing. Quantities
are per carrier board; all remain preliminary.

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

The intended assembly uses four-conductor separable stranded ribbon and
individual crimp contacts inserted into JST-SH housings. It is not FFC/FPC
flat-flex cable. Each contact is crimped individually.

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

| Function | Preliminary part | Quantity per board | Package and sourcing snapshot |
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

## Fabrication and cost context

Hand soldering SMT is acceptable to the user. A custom carrier can therefore
use SMT parts even when through-hole alternatives exist. JLCPCB assembly is
another option; the through-hole triacs, relays, and daughterboard sockets need
the appropriate assembly process or manual installation.

At the discussed price tiers, the mux, eight horizontal SH sockets, two triacs,
two optotriacs, two relays, and two Feather socket strips total approximately
$8.70 per board for a two-board batch, or $8.01 per board for a five-board
batch. These are component-price calculations, not purchasable complete boards:
relay stock was unavailable and the supporting parts remain incomplete.

An earlier planning allowance of roughly $60–100 for two populated carriers
before shipping/tax excluded Feather modules, heatsinks, and enclosures and was
not a vendor quote. PCB dimensions, complete BOM, placement files, assembly
fees, and shipping are needed for a meaningful final comparison. See
[JLCPCB's assembly pricing](https://jlcpcb.com/help/article/pcb-assembly-price).
