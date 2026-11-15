# Four-layer ground and power-plane study

Date: 2026-11-14. Starting source: merged PR #33, commit
`296edee5de4194e0dd0b33d40a5abc8ae7c81cd9`. The developer requested four layers
with ground and power planes on all three designs. [ADR-0021](../../.rqml/adr/0021-four-layer-ground-and-power-planes.md)
records the decision before native changes. This continues the `MOT-PROC-001`
exploratory exception; `MOT-HW-003` governs native source/annotation identity
and `MOT-CI-004` governs deterministic review derivatives. Electrical product
obligations remain draft design inputs and are not closed by this revision.

## Construction and preserved design

| Layer | Role |
| --- | --- |
| F.Cu | Front assembly and signal/local power copper, 0.035 mm outer copper |
| In1.Cu | Isolated low-voltage ground, 0.0152 mm inner copper |
| In2.Cu | Separate low-voltage supply regions, plus a carrier USB ground corridor, 0.0152 mm inner copper |
| B.Cu | Signal/local return copper, 0.035 mm outer copper |

The native stackup uses the published nominal-1.6-mm **JLC04161H-7628**
dimensions: 0.2104 mm outer-to-inner prepreg with Er 4.4 and a 1.065 mm core
with Er 4.6. These are the dimensions in [JLCPCB's stackup table](https://jlcpcb.com/impedance).
KiCad retains its 0.01 mm default mask model on each side and generic loss
tangent; the summed model is 1.6062 mm while the declared board thickness is
nominal 1.6 mm. Coatings, loss, manufacturing tolerances and the final order
remain unqualified; no controlled-impedance acceptance is claimed.

Carrier/output/sensor outlines stay 95 x 80, 90 x 65 and 80 x 40 mm respectively.
All 99 / 76 / 82 footprints retain their identities, selections, property text,
pad geometry/nets and placement. All components, exposed handling grounds and
probe access stay on the front. The schematic hierarchy and circuit choices
are unchanged. Ordinary through vias span the new inner layers; no blind,
buried, microvia or filled/capped via-in-pad process is introduced.

## Plane partition and isolation

The carrier has In1 GND plus In2 controller 3.3 V, switched sensor 3.3 V, raw
actuator 5 V and selected logic 5 V regions. USB VBUS and individual post-link
Qwiic supplies retain local routes. The output uses In1 GND plus In2 local
3.3 V, selected logic 5 V and raw actuator 5 V regions. The sensor uses In1
GND and In2 switched sensor 3.3 V. Different supply names remain separate nets;
source-selection, switching, link resistors, decoupling and protection are not
bypassed to make larger pours.

Existing deliberately sized outer mains/neutral/PE conductors remain. Inner
LV copper stays out of those domains, with no mains or PE planes and no
logic-GND/PE bond. Geometric separation is reviewed by projecting actual
copper from all four layers, independently of native same-layer DRC. The
provisional 5 mm mains/LV and functional mains spacing remain geometric study
rules, not working-voltage or insulation ratings. Antenna keepouts include
both the carrier board area and the embedded module area on all four layers.
Placement-only Repeat Layout areas keep their original settings.

## USB reference

The carrier's long back-side USB pair is adjacent to In2, so a continuous
GND corridor on that layer takes priority over power regions beneath the pair.
In1 supplies the reference beneath front-side USB segments. Actual filled
reference copper, antipads and transitions are inspected; adding an inner
layer or drawing a ground-zone outline alone is not treated as evidence.
The pair's existing geometry is retained. Stackup/impedance, the provisional
panel-harness pinout, shield termination, retention and actual link operation
still need final review and qualification.

## Sensor cuts and actual plane feeds

The five-, six- and seven-port cuts remain at 50 / 60 / 70 mm from the board's
left edge. Each 1 mm kerf plus +/-0.25 mm allowance excludes pads, vias and
pours across all four copper layers. The two new inner zones therefore each
have four separated pieces, linked electrically through deliberate existing
outer conductors and real plated connections. Three new ordinary 0.6/0.3 mm
sensor-power vias feed the removable tail regions. There are no inner power
bridges across the cutting corridors.

Independent connectivity checks clip actual filled polygons at cut minus
0.75 mm. Disconnected polygon islands are separate nodes; only plated THT pads
and vias join layers. A shared zone UUID or net label cannot electrically
bridge layers in this model. All retained pads and ground/power returns must
remain connected after each cut. Cutting, burr removal, exposed copper/edge
insulation, mechanical strength and operation of the cut board remain
qualification work.

## Observed structural checks

| Final native candidate | Footprints | Track segments | Through vias | Filled zone objects | Physical/silk violations | Opens | Inherited parity findings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Carrier | 99 | 853 | 106 | 8 | 0 | 0 | 49 |
| Single output | 76 | 742 | 67 | 6 | 0 | 0 | 53 |
| Sensor mux | 82 | 1,287 | 135 | 4 | 0 | 0 | 70 |

The native KiCad 10.0.8 commands use `pcb drc --all-track-errors
--schematic-parity --exit-code-violations --format json`. They exit **5** for
the inherited parity sets, not zero. Field/placeholder footprint findings are
compared with the preceding sources, and project constraints, severities and
exclusions are unchanged. All three boards have zero drilled-via intersections
with SMD lands; same-net annular-only overlaps are considered separately.

The output board's earlier two CUT_EN opens are now connected on outer layers
using three ordinary 0.6/0.3 mm vias. All four previous drill/land intersections
are repaired, including the two mains-side vias. Existing via sizes, drilled
holes and attached conductor widths are preserved. A nearby CURRENT_REF via
moves within the MCU area to make the ordinary CUT_EN escape possible; neither
inner plane carries a CUT_EN signal route. The current-sensing circuit and
component/pad placements are unchanged.

The carrier's original 955 segment/via objects remain intact, with two raw-5-V
capacitor fanout tracks and two ordinary vias added. Its In1 ground has one
filled island with 35 plated anchors. In2 raw 5 V has three anchors, selected
5 V six, switched sensor 3.3 V two and the USB ground corridor eight. Controller
3.3 V includes a main region and six small via-anchored pockets, connected
through preserved outer routing. These are connected pieces, not a claim of
one uninterrupted supply sheet across the other rail regions.

Independent carrier reference review finds no missing data-route centerline
samples outside physical signal-pad/via antipads. The former 5.8 mm long-run
reference interruption is gone. A wider reference-band review still finds
tiny transition fringes and one connector-local edge nick beside J21's CC1
antipad, approximately 0.0099 mm2. This is explicitly retained as local
entry/impedance qualification work, not hidden by a blanket reference claim.

On the sensor board, all original 82 footprint blocks, 1,287 segments, 132 vias
and nine groups are unchanged as native syntax trees. Only three power-feed
vias are added. Each new plane has four actual filled pieces; every piece has
same-net plated feeds (GND: 34/5/5/2, power: 5/1/1/1). All three four-layer cut
graphs remain connected, with 167/184/201 retained netted pads and no pad, via
or pour in a cutting corridor. The eight Repeat Layout areas are unchanged.

The library's ESP32-C6 antenna keepout already lists every copper layer, so no
library edit is needed. The copied board footprint's embedded guard now covers
the four enabled layers, matching the library's intended behavior; all other
carrier footprint geometry and fields are preserved.

All independent full-board copper graphs pass, with no disconnected netted
pads or floating filled-plane pieces. All seven wide current paths on each
mains board remain connected. The output's projected domain gap is
5.160952 mm. Its pre-existing HV-side H2 mount is assessed on that side: a
7 mm metal disc clears LV by 8.500 mm, its nearest HV gate copper by 3.033 mm
and the heatsink reserve by 2.5 mm. It does not contact copper, but it does
**not** have 5 mm clearance to every HV conductor. The output's LV-side mounts
clear HV by at least 10.392 mm. These are provisional geometric envelopes;
actual mounting hardware and accessible-metal insulation need qualification.

Only the three PCB files change among 39 native sources. All 36 other native
files, including every schematic, library, project and rule file, remain
byte-identical to the starting revision. Existing outer power-feed routes
remain: some single-anchor local pours supplement that distribution rather
than replacing an entire supply route with an uninterrupted plane.

| Reviewed PCB source | SHA-256 |
| --- | --- |
| motley-carrier.kicad_pcb | `21ee2ad14c3c3eb52687763fe2f693497801f05ee8a13c70fb6d5a451521a7a5` |
| motley-ac-output.kicad_pcb | `c867a18748758c4fd4db703631ccc073a43bcd584fb3cd7c21cc19c3dc6dbb86` |
| motley-sensors.kicad_pcb | `7403e3817df2ddda53f357df8558a458d98a0d4cf3e51dbe487e8d45ef2d095d` |
