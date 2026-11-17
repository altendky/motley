# Development-build budget basis

Updated 2026-11-15 using actual JLCPCB quotation API results for that date's
routed four-layer designs and matched BOM/CPL files. JLC charges below are
quoted; the remaining parts and wiring are estimates. One finished controller
uses one carrier, one sensor mux and two identical output boards. No cart
addition, order or payment was made.

The 2026-11-16 exact-part integration has a
[new actual JLC quotation](jlcpcb-quote-2026-11-16-exact-parts.md): $285.26 /
$312.08 / $419.13 for the three scenarios' fabrication and partial assembly.
New mains terminals, output-bus connectors, R25 and all new LOW passives are
included. A refreshed base hand-fitting basket is
[$25.67 per finished controller](hardware-exact-selections.md#retail-hand-fitting-basket),
excluding additional optical stock omissions and off-board hardware. The
complete-controller figures below retain the older
quotation and completion allowances; they need reconciliation against the new
factory selections before claiming a current finished-controller budget.

## Batch costs

All amounts are USD, before shipping and tax. The budget uses the upper
remaining-parts/wiring allowance, then rounds the combined batch estimate to
the nearest $25. These remain approximate budgets.

| Finished controllers | JLC fabrication and partial assembly, quoted | Remaining parts/wiring, upper estimate | Combined upper estimate before $25 rounding | README batch budget | Per two-output controller, from README budget |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | $259.18 | $81.48 | $340.66 | $350 | $350 |
| 2 | $273.59 | $178.03 | $451.62 | $450 | $225 |
| 5 | $356.19 | $456.25 | $812.44 | $800 | $160 |

Per-controller figures divide the rounded README batch budget by the number
finished, including the cost of paid-for spares.

The budget includes boards, partial factory assembly, hand-fitted components,
output heatsinks/interfaces, captive mains cord/strain relief, two outlets per
controller, panel USB and consumed internal wiring. It excludes sensor
probes/extensions, enclosure and mounting hardware, tools/labor, shipping,
tax/tariffs, and whole-spool/container purchases beyond consumed allowances.
Spare factory assemblies are not fully hand-completed. The selected
[7Semi ES-12289 probe](https://7semi.com/7semi-sht45-digital-humidity-and-temperature-sensor-probe/)
was listed at $13; probe count need not equal the eight available ports.

## Quantities and JLC quotes

JLC's current Economic settings allow two or five assemblies from five
fabricated boards, and ten from ten. Arbitrary smaller assembly counts require
Standard service. The minimum case here is the smallest supported Economic
arrangement, not a comparison against all-hand assembly or every service.

| Finished controllers | Fabricated: carrier / mux / output | Factory assembled: carrier / mux / output | Carrier job | Mux job | Output job |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | 5 / 5 / 5 | 2 / 2 / 2 | $122.31 | $47.19 | $89.68 |
| 2 | 5 / 5 / 5 | 2 / 2 / 5 | $122.31 | $47.19 | $104.09 |
| 5 | 5 / 5 / 10 | 5 / 5 / 10 | $154.38 | $63.12 | $138.69 |

Each job price includes fabrication, selected components and assembly fees.
The minimum case buys one spare carrier and mux assembly; the two-controller
case buys one spare output assembly. Required hand-fitted parts are budgeted
only for the finished controllers.

| Board | Detected outline | Five bare PCBs | Ten bare PCBs |
| --- | --- | ---: | ---: |
| Carrier | 95 × 80 mm | $8 | Not requested |
| Single output | 90 × 65 mm | $8 | $14 |
| Sensor mux | L-shaped, 80 × 40 mm overall | $8 | Not requested |

Settings: four layers, 1.6 mm FR4, green mask, leaded HASL, 1 oz outer and
0.5 oz inner copper, front assembly, normal lead time, one design per job.
Fabrication subtotals are $24, $24 and $30 and are already included above.

The returned assembly fees included $8.24 setup, $1.55 stencil, $3.09 per
chargeable Extended component type, placement and through-hole soldering.
The latter was $3.61 setup per job plus approximately $0.26–$1.63 soldering,
depending on job and quantity. Actual component purchases include JLC's
attrition/minimum quantities; many small passives require at least twenty.
These charges are retained rather than replacing them with exact-fit BOM sums.

## Factory coverage and remaining parts

Only exact approved quotation codes that were matched, selected, in stock and
eligible for Economic assembly were retained. Automatic generic substitutions
for the mains/pulse resistors were deselected. Stock was rechecked at each
quantity; the larger case therefore has more hand-fitted parts.

| Finished controllers | Factory-fitted positions per carrier / output / mux | Additional optical parts to hand-fit due to stock |
| ---: | --- | --- |
| 1 | 77 / 47 / 74 | None |
| 2 | 77 / 46 / 74 | Output U31, ACPL-K370-500E |
| 5 | 76 / 45 / 74 | Carrier U40, ACPL-K376-000E; output U2, VO3053-X007T, and U31 |

The carrier also needs its fuse/clips, mains terminals, selected deployment
headers, R25 and R80–R83. Each output needs its fuse/clips, mains/deployment
connections, Omron cutoff relay, snubber capacitor/resistor and covered shunts,
recovery header/shunt, R104 and R310–R313. The sensor board has no additional
purchased board components in these matches. Test loops and mechanical/access
features remain outside purchased-component counts.

The factory quote includes some through-hole components, including the carrier's
MEAN WELL supply, output triac and mux deployment headers. They are excluded
from the hand-completion subtotal. A generic manual-parts export cannot simply
be added to the factory quote.

Completion allowances count three fuse cartridges and six clips, fourteen
unselected HV/pulse-rated resistors, two heatsinks/clips, four six-pin and two
five-pin cable housings, and 34 LV crimp contacts per controller. They also
include six covered shunts: four snubber links and two recovery links. Outlet
handoff terminals do not include the two receptacles or six insulated quick
disconnects. Panel USB pricing includes its cable-side housing/contacts.

## Price references and unresolved selections

The completion model uses quantity price breaks across the required finished
units. Representative current retail checks for stock omissions are:

| Part | Observed unit price | Source |
| --- | ---: | --- |
| Omron G6DN-1A-L-DC5 | $2.38; $2.36 at ten | [Mouser](https://www.mouser.com/en/ProductDetail/Omron-Electronics/G6DN-1A-L-DC5?qs=Mv7BduZupUhZB902RCoZGQ%3D%3D) |
| ACPL-K370-500E | $5.16; $3.78 at ten | [Mouser](https://www.mouser.com/ProductDetail/Broadcom-Avago/ACPL-K370-500E?qs=WpC4P%252BDU3FkkR3M3Qiegkg%3D%3D) |
| ACPL-K376-000E | $7.38; limited stock | [Mouser](https://www.mouser.com/en/ProductDetail/Broadcom-Avago/ACPL-K376-000E?qs=WpC4P%252BDU3FnO2YOR%2FlQ05Q%3D%3D) |
| VO3053-X007T | $1.16; $0.813 at ten | [DigiKey](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VO3053-X007T/2355056) |
| RC0603FR-07226KL (R25) | $0.10, cut tape MOQ one | [DigiKey](https://www.digikey.com/en/products/detail/yageo/RC0603FR-07226KL/727066) |

Other priced candidates include the
[HSE-B20350-NP heatsink](https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/HSE-B20350-NP/7319885),
[HSC-03 clip](https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/HSC-03/13282949),
[Qualtek 738W-X2-03 outlets](https://www.mouser.com/en/ProductDetail/Qualtek/738W-X2-03?qs=HFfMDpzxxd1SmutvsrmPJA%3D%3D)
and [Adafruit 6153 panel USB cable](https://www.adafruit.com/product/6153).
These off-board checks retain November 13 pricing where not refreshed.

The native mains terminal footprints use 7.50 mm pitch; the priced Same Sky
7.62 mm alternative is an allowance, not a drop-in selection. HV/pulse
resistors carry $0.50–$1 allowances each pending exact selection. Snubber
parts, covered links, cord/bushing fit, outlet contact tooling, thermal fit and
USB robustness/pinout still need qualification. Board pricing does not resolve
these choices. Retail stock, shipping and purchases larger than consumed wire,
grease or contact quantities can increase cash outlay.

## Input identity

Quotes used the current native designs at commit
`a7726ebd99365fd315ce48e93537fb303a74a925`, exported with pinned KiCad 10.0.8.
All 257 footprints were reconciled: 223 purchased-component positions and 34
mechanical/access features. Matching CPL locations/rotations and front-only
assembly were checked against native placements. Native PCB SHA-256 values:

| Board | SHA-256 |
| --- | --- |
| Carrier | `21ee2ad14c3c3eb52687763fe2f693497801f05ee8a13c70fb6d5a451521a7a5` |
| Output | `c867a18748758c4fd4db703631ccc073a43bcd584fb3cd7c21cc19c3dc6dbb86` |
| Mux | `7403e3817df2ddda53f357df8558a458d98a0d4cf3e51dbe487e8d45ef2d095d` |

Generated exports, API requests/responses and reference-level completion
reconciliation remain temporary quotation evidence. The reusable workflow is
in the [quote skill](../.agents/skills/jlcpcb-quote/SKILL.md). See the
[hardware guide](../hardware/controller/README.md) for design limitations;
successful exports and quotes do not establish manufacturing readiness.
