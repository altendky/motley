# ESD, touch reference and probe-access study

Review: 2026-11-14. Governing design inputs: MOT-HW-001/002/004/005/006/009/010;
native annotation integrity: approved MOT-HW-003 and ADR-0015. Electrical
requirements remain drafts. This is an unrouted prototype, not a system ESD
rating, a fabrication release or permission to handle exposed live mains.
The [intelligent-output review](intelligent-output-review.md) records current
pin/default/power dispositions and the full fresh XML inventory. This revision
adds local STM32C011 output logic, VO3053-X007T phase control and isolated
TMCS1123B5/ACPL-K370 feedback, with an ACPL-K376/buffer reference on the carrier.
Those circuits and their default, timing, power and insulation limits remain
unqualified; no firmware behavior or system immunity is established.

## Current component choices and budget

| Function | Candidate | Normal-voltage / integration limits | Complete unit quantity |
| --- | --- | --- | ---: |
| 3.3 V signal/rail clamps | Nexperia PESD5V0S2BT,215, JLC C49338, SOT-23 | Two bidirectional branches, pins 1/2 to protected nets, 3 to local GND; 5 V standoff | 36 |
| Raw/selected/logic 5 V and USB VBUS clamps | onsemi ESD5Z6.0T1G, JLC C82323, SOD-523 | 6 V standoff; pin 1 K to rail, pin 2 A to local GND | 7 |
| Sensor data series impedance | 100 ohm 0805, 1%, R30-R45 | Between connector-side TVS and mux-side 2k2 pull-up/data net | 16 |
| Touch reference | Bare 8 mm exposed copper to local LV GND | No purchased part; top/front side on every board | 4 |
| Optional wire loops | Bare two-hole same-net footprints, 2.54 mm pitch / 0.8 mm drill | Both holes are pin 1; hand-form a U-loop if wanted | 26 |
| Optional diagnostic posts | Bare single 1 mm plated hole | Sensor SDA/SCL/RESET; hand-fit a post or compatible single-pin loop | 3 |

Current quantities come from fresh root XML: carrier 14 dual/3 single clamps,
one output 2 dual/2 single, sensors 18 dual/0 single. One carrier, two outputs and
one sensor board therefore use 36 dual and 7 single clamps. The optional loops
reconcile as 6 carrier + 2x9 output + 2 sensor = 26; three sensor posts and four
top/front touch pads remain. Sensor data series resistors are unchanged.

**Historical budget, 2026-11-13 revision:** dual TVSs were $0.0827, singles
$0.0424 and generic 0805 series resistors approximately $0.0034 at the recorded
JLC low-quantity snapshot. The earlier 34-dual/5-single population produced
approximately $3.08 protection parts plus $0.23 Economic joints, or $3.31 per
two-output unit, including eight carrier Qwiic TVSs. That is not an estimate
for the current population; the added bus/SYNC/logic-power protection has not
been requoted. Sockets, DIP switch, bus pulls, power links, attrition, tax,
shipping and unchanged setup were excluded. Bare touch/probe features require
no purchased contact or paid assembly joint unless optional wire is fitted;
board-area effects depend on final placement.

Both TVS types were Extended in that historical quote. One newly loaded type
was $3.07 per assembly job. Three separately assembled designs could add $6.14 carrier,
$6.14 output job (building both copies together), and $3.07 sensor job:
**$15.35 across those three jobs**, not per unit, at those rates. Confirm a fresh quote and
existing parts-library/setup treatment before ordering. Hand assembly remains
possible; no order has been placed.
[Dual TVS](https://jlcpcb.com/partdetail/C49338),
[single TVS](https://jlcpcb.com/partdetail/C82323),
[JLC assembly charges](https://jlcpcb.com/help/article/pcb-assembly-price).

Placement correction, 2026-11-13: all fitted sensor parts, including D60/D61,
are now on the front. The bare touch copper needs no assembly pass and was
subsequently moved to the top/front side at the developer's request.
This removes the earlier layout's two-sided component-assembly requirement;
the Economic budget above had omitted that tier effect. The common area is
now 49 mm wide behind five connector positions following the chaining/address
extension, within the same 80 x 44 mm envelope. Supported trimming retains five
through eight connectors. Assembly
eligibility and the complete final quote still need confirmation from production
files; the board remains unrouted.

## Connector/contact dispositions

| Connector(s) | Contact disposition | Remaining limits |
| --- | --- | --- |
| Sensor J2-J9, four contacts each | GND is the return; 3V3_SENS has a bidirectional clamp; SDA/SCL each have a bidirectional clamp on the cable side of their 100 ohm resistor. Both original 2k2 pull-ups stay on the mux side. One channel of each supply array is unused/NC. | Protection stays within its removable connector section. Complete cable/probe capacitance, actual remote pull-ups, common-mode discharge and probe-head immunity need tests. |
| Sensor J12/J13 and carrier J13, five contacts | GND return; switched 3V3, SDA, SCL and mux RESET protected by shared upstream dual arrays. Sensor pair passes all five signals through, including shared reset. | These internal links are included for modular handling exposure. PB-02 reset-pull/off-domain behavior remains open; shared chains add capacitance/load and require final entry/return placement review. |
| Carrier J23/J25 HP and J24/J26 LP Qwiic, four contacts each | Standard GND/3.3V/SDA/SCL. D40/D42/D44/D46 protect data pairs; D41/D43/D45/D47 protect each connector-side power contact, with second branch NC. R44/R46 feed HP from switched +3V3_SENS; R45/R47 feed LP from main +3V3. HP 10k pulls remain switched; LP 4k7 pulls now use main +3V3. | Four sockets, two independent buses, with duplicates parallel on each. One host and supply; no external power into carrier sockets. Open power links do not isolate signals. Added capacitance, reset/off-domain behavior and complete cable loading require qualification. |
| Sensor J10/J11 Qwiic upstream, four contacts | Standard GND/3.3V/SDA/SCL; both power contacts share one node before R50 = 0. Existing D60/D61 protect local upstream nets; local pull-ups are configurable through R55/R56. | Disconnect deployment links to another host/supply for standalone bench use. Removing R50 disconnects the pair from local power, not the external contacts from each other and not SDA/SCL. No automatic source or host selection or unpowered-board isolation. |
| Sensor SW1 address DIP, six contacts | Internal configuration, local 3.3 V on pins 1/2/3 and defined address inputs on 6/5/4 with separate 10k pull-downs. | No separate TVS added to these internal low-voltage switch nodes; enclosure access and handling scope remain unqualified. Change addresses unpowered. |
| Carrier J15/J18 and each output J14, six contacts | GND, selected logic 5 V, SDA, SCL, LINE_SYNC, raw 5 V. Carrier D34 protects SDA/SCL, D35 SYNC (second branch NC), D36 raw 5 V and D37 selected 5 V. Output D110 protects SDA/SCL, D112 SYNC (second branch NC), D111 raw 5 V and D113 logic 5 V. Signal arrays remain bidirectional; supply arrays have 6 V standoff. | Local HEAT_EN/CUT_EN no longer cross this connector. Shared I2C/SYNC and dual supplies introduce partial-contact/back-power paths that the older two-command analysis does not qualify. Hot leakage, missing GND, capacitance/edge timing, current/inrush and transient actuation remain open. |
| Output J21 SWD/service, SW20 recovery, SW21 reset | Local 3.3 V reference, GND, SWDIO, SWCLK/BOOT0 and NRST; defined reset/boot biases are recorded in the intelligent-output review. | No additional connector-local TVS was added here. Service exposure, debugger-powered/unpowered states, shunt handling and whether local protection is needed remain explicit decisions. |
| Carrier J22, four contacts | GND return; RX/TX and 3.3 V protected by two dual arrays; remaining channel NC. | External adapter power, missing-ground behavior and injection into an unpowered MCU still need an explicit supported procedure and tests. |
| USB J21 VBUS and D+/D- | Existing USBLC6-2 protects the data path; D38 adds 6 V-standoff VBUS protection. D38 and TP7 actually join J21 pin 1, including the existing power-selector input, bleed and VBUS qualifier. | Keep low-capacitance protection on USB data. Normal host current/inrush/transfer budgets and fast-pulse coordination remain open. |
| USB J21 provisional CC1/CC2 contacts | Remain NC on the carrier; the selected panel assembly contains its sink resistors. No active carrier CC input is exposed through these contacts. | Actual panel/harness mapping and resistor location must be confirmed. The external female CC contacts' discharge path is not qualified by these NC markers or the data-line protector. Select any additional protection at the verified panel interface. |
| USB shell/shield | No shield is provided by the provisional unshielded harness; no new bond is invented. | The user's preference for a robust shielded assembly, shell termination and panel retention remains unsatisfied. Enclosure/return design and testing are required. |
| Carrier J1/J16/J19; output J17/J10, three mains contacts each | PE remains separate from logic GND and continuous where required; no ordinary logic TVS is connected from L/N/PE to LV GND. | Mains transient protection, insulation, fuse coordination, enclosure/access and surge/ESD exposure remain a separate engineering task. No arbitrary MOV was added. |
| Output J20 snubber contacts/shunts | Internal mains configuration; existing two-cap assembly and unplug/discharge procedure retained. | Covered shunts are not a qualified touch barrier. No LV ESD device or test clip is added here. |

## Why these topologies

PESD5V0S2BT has 45 pF maximum capacitance per line and 100 nA maximum leakage
at 5 V/25 C. Its specified clamping voltage can reach 10 V at 1 A and 14 V
at 12 A. The component's IEC discharge rating does not prove a complete board
or enclosure rating. Its **bidirectional** signal branches avoid a normal
forward-diode return from a floating output-board GND into another LOW signal.
D101/D102 remain in the local MCU-to-driver paths, while the external interface
is now I2C/SYNC. The earlier two-command missing-ground calculation does not
establish safety of this new interface. Temperature, injection and transient
paths still need qualification. Do not substitute a steering/unidirectional
array without repeating the complete interface analysis.
[Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/PESD5V0S2BT.pdf).

The 5 V-standoff array is deliberately not placed across raw 5 V or USB VBUS:
normal tolerance can exceed 5.0 V. ESD5Z6.0T1G instead has 6 V standoff and
6.8 V minimum breakdown at 25 C. Its pulse clamp is also above ordinary IC
absolute voltage limits (12.4 V typical at 5 A; 20.5 V maximum at 8.8 A using
the specified waveform), so it is not a guarantee of downstream survival or
continuous-overvoltage regulation.
[onsemi datasheet](https://www.onsemi.com/pdf/datasheet/esd5z2.5t1-d.pdf).

Each sensor line gains up to 45 pF at its cable-side TVS. With the previously
estimated 1.50k effective pull-up, that contribution alone adds about 57 ns
to a 30%-70% rise time. Actual total capacitance includes the mux, upstream
protection, all selected wiring and the probe; no cable length is newly rated.
At the illustrative 1.93 mA LOW current, 100 ohm adds about 0.193 V. A remote
0.4 V LOW would then be about 0.593 V at the mux before other losses, below
0.99 V at a nominal 3.3 V input. This is a scenario, not a full tolerance
budget. The resistor does not mathematically guarantee the mux's injection
limit with the TVS at its maximum residual clamp voltage. Pulse coordination,
signal LOW margin, local capacitance and actual layout require tests.

Route connector-to-clamp-to-circuit with a short discharge path and a broad,
low-inductance return that avoids sensitive shared ground paths. Current
placements reserve groups only: no tracks, vias or pours have been added.
Return and shell/enclosure geometry cannot be qualified from this placement.
The expanded mux common area puts J10 roughly 20-26 mm from D60/D61. Shared
upstream protection is still a candidate, not necessarily a short entry clamp;
final routing may need protection local to the new connector. No immunity claim
is inferred from the shared net names or clean physical DRC.
[TI protection-layout guidance](https://www.ti.com/lit/an/slva680a/slva680a.pdf).

## Touch and clip access

`LV GND` silk marks each touch area. These pads equalize finger/board potential
with the **local isolated/floating circuit ground**. They are not an earth
connection or a guaranteed ESD discharge accessory, and add no PE-to-GND bond.
They do not make touching exposed energized mains circuitry safe. Every board's
pad is on top/front, including sensor TP1 in its fixed core. The placement
export shows all touch points in its three front views. Use appropriate ESD handling controls for
assembly; no ordinary small resistor has been presented as an 8 kV-rated
finger-discharge network.

| Board | Touch | Optional probe points |
| --- | --- | --- |
| Carrier | TP1, LV GND | TP2 GND, TP3 raw mains-derived 5 V, TP4 selected 5 V, TP5 main 3.3 V, TP6 sensor 3.3 V, TP7 raw USB VBUS |
| Each output | TP1, LV GND | TP2 GND, TP3 raw 5 V, TP4 HEAT_EN, TP5 CUT_EN; TP20 local 3.3 V, TP21 LINE_SYNC, TP22 CURRENT_V, TP23 CURRENT_REF, TP24 OUT_VOLT_N |
| Sensor fixed core | TP1, top/front LV GND | TP2 GND and TP3 sensor 3.3 V accept two-hole loops; TP4 SDA, TP5 SCL and TP6 RESET use single-hole posts |

Wire/contact geometry and clip clearance are provisional. A purchased
[Adafruit 3825 mini-loop pack](https://www.adafruit.com/product/3825) was
$9.95/100 at the checked snapshot, about $0.10 per used loop, but its stated
approximately 1 mm mounting hole is larger than the 0.8 mm two-hole wire-loop
pattern. Do not treat those as interchangeable without selecting a compatible
footprint; the present default is hand-formed wire. Use appropriately rated
test equipment without defeating mains isolation through an earth-grounded
instrument lead. No intentional mains test loop has been added.

## Verification boundary

Fresh ERC, XML netlists, physical pad/net/path/field parity and unrouted DRC
are recorded in `verification.md`. Repeated sensor sections and every planned
cut retain the core touch/probe points. The TVS columns were moved inward
0.2 mm to retain at least 0.375 mm pad-to-worst-cut-edge clearance under the
stated 1 mm kerf and +/-0.25 mm cut positioning assumption. This remains a
geometry check, not a qualified cutting process.

System ESD levels, waveforms, pass criteria, powered/unpowered/partial-contact
states, actual enclosure/cable return paths, leakage/temperature corners and
post-discharge functional checks remain to be agreed and physically tested.
No component rating or annotation test is linked as that hardware evidence.
