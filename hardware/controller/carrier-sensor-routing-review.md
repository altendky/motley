# Carrier and sensor packing/routing study

Historical two-layer snapshot. The current [four-layer review](four-layer-review.md)
records the later ground/power-plane conversion and its observed checks.

Date: 2026-11-14. Starting source: merged PR #32, commit
`a579741eda4976dab7317129edab4154e4f28dbd`. The developer requested packing and
routing the two remaining boards. This continues the `MOT-PROC-001` exploratory
CAD exception; approved `MOT-HW-003` governs source/annotation identity and
`MOT-CI-004` governs derivative SVG freshness. Electrical requirements remain
draft design inputs. The AC-output board and all schematic circuits stay intact.

## Placement

| Board | Previous envelope | Packed envelope | Area change |
| --- | --- | --- | --- |
| Controller / AC input | 100 x 85 mm rectangle | 95 x 80 mm rectangle | 8,500 to 7,600 mm2, 10.6% smaller |
| Sensor mux | 80 x 44 mm L | 80 x 40 mm L | 2,714 to 2,518 mm2 of board material, 7.2% smaller; bounding rectangle 9.1% smaller |

The carrier retains 99 footprints, with the controller/USB/regulators on the
left and mains distribution on the right. The supply body's actual
45.7 x 25.4 x 21.5 mm envelope limits packing. The sensor board retains 82
footprints, its 80 mm connector row, 18 mm deep port bank and 49 mm wide common
leg. All eight right-angle sensor connectors face the same wall at 10 mm pitch.
The common circuitry remains behind the first five connector positions.
Both designs retain front assembly, top-side ground touch and clip access,
native identities/properties, pad nets and movable functional groups.
Moving groups now requires reviewing and reworking their copper connections.

## Routing choices and boundaries

The carrier uses deliberately routed 3 mm shared mains trunks and 2 mm outlet
branches, with 0.8 mm supply branches and 0.4 mm detector branches. These are
geometric study choices for the nominal two-output load, not current or
fault-energy ratings. Provisional rules require 5 mm mains/LV copper separation
and 0.6 mm functional spacing within the mains domain. Ground remains separate
from PE. The two-layer LV routes use ordinary small vias and ground pours;
two copper layers do not require back-side component assembly.

The sensor layout retains the five-, six- and seven-port cut positions at
50, 60 and 70 mm from the left edge. A 1 mm kerf plus 0.25 mm positioning
allowance on each side reserves a 1.5 mm corridor. Pads, vias and pours must
stay out of those corridors; downstream power, return and signal traces must
cross them deliberately. Connectivity checks must clip actual filled copper
at the retained edge of each corridor, including separate ground islands.
Keeping the components alone is insufficient: an otherwise connected route
can detour through material that will be removed.

The bounded routing method combines explicit high-current and USB routing
with local automatic LV routing and manual cleanup. Temporary router exchange
files omit KiCad Repeat Layout placement areas that its DSN exporter incorrectly
turns into copper obstacles. Native placement/reuse areas remain present.
Router output is checked against native geometry and connectivity before use.

## Observed checks

The carrier has 851 track segments, 104 vias and two LV-only GND pours. All
seven shared 3 mm / branch 2 mm load paths are geometrically connected. An
independent all-layer copper projection finds no violation of the provisional
5 mm mains/LV separation. Four provisional 7 mm mounting-metal discs retain
at least 5 mm clearance from mains copper and avoid component courtyards;
the antenna component reserve is clear. Actual insulation, mounting and
current capability remain unqualified.

| Native KiCad 10.0.8 check | Carrier | Sensors |
| --- | ---: | ---: |
| Physical/copper violations | 0 | 0 |
| Open connections | 0 | 0 |
| Silkscreen warnings | 0 | 0 |
| Schematic-parity findings | 49 | 70 |

Both DRC commands use `--all-track-errors --schematic-parity
--exit-code-violations --format json` and exit **5**, not zero, because of the
inherited parity findings. A final carrier label-only pass removed 73 silk
warnings without changing copper or component placement. Its 47 field and two provisional footprint
assignment findings exactly match the baseline by type, description and
footprint identity. No severity or exclusion was changed to hide findings.

The sensor candidate has 1,287 track segments, 132 ordinary vias and two GND
pours, with the native placement/reuse areas retained. KiCad reports zero
physical/silkscreen violations and zero open connections. Its 70 schematic-
parity findings are exactly the same description/datasheet mismatches as the
unrouted baseline, compared by type, text and item identity. They are retained
to preserve component fields, rather than silently repaired or excluded.

Independent clipping of filled copper at the worst retained edge of each cut
finds every required net connected: 167, 184 and 201 retained netted pads for
five, six and seven ports respectively. No pad, via or pour intersects any
kerf corridor. The graph treats disconnected islands separately and does not
join copper simply because it shares a net name. The first trial exposed two
signal detours through removable material; both were corrected before these
checks. Cut-down hardware operation remains untested.

The sensor's GND SMD pads, touch contact, TP2 loop and deployment-header ground
pins use solid zone connections to avoid isolated/starved thermal connections.
Other through-hole pads retain their thermal settings. These choices need
soldering/profile review. Seventeen same-net via-annulus/land overlaps remain,
but no drilled hole intersects an SMD land; they are distinct from the unresolved
drill/land intersections on the separate output board.

Both independent and parent audits preserve every footprint UUID, schematic
identity, selection, property string, local pad geometry/UUID/net and front-side
assembly. Neither board has a via drill intersecting an SMD land. The carrier
has six same-net annulus-only overlaps. The two initially found carrier drill
intersections were repaired before the final audited sources below. Thirty-four
other native files, including every schematic and all output-board sources,
remain byte-identical to the starting revision.

| Reviewed source | SHA-256 |
| --- | --- |
| motley-carrier.kicad_pcb | `67584fe431810bb080f64fd173dc7f4a9c5a547f1323b4982612dcc9f7cc5568` |
| motley-carrier.kicad_pro | `c92f5ac677f1923e7a4c7107235e32a4d688f0b2c30dd1eb05a2f784138fa2b2` |
| motley-carrier.kicad_dru | `fea85fb31efc1a7c56c69e3faedc91b4a311641d485dfd2da4bb3de50c3a2776` |
| motley-sensors.kicad_pcb | `9a91785ea8714a23174925a3b4f73af596818d83efa630fed96c77859b75cea4` |
| motley-sensors.kicad_pro | `06be9ce8a56f4c5dcb4ce3a6d73b081dae3ce0e24bf9ce00c75e6842b970f365` |

## Qualification still needed

The antenna reserve remains a copper exclusion with separately reviewed
component clearance, not a qualified RF layout. FR-4 remains beneath the module antenna; antenna overhang
or an appropriate board cutout and the final enclosure need review before
manufacture. See Espressif's [ESP32-C6 placement guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html).

The long USB data pair has a 19.05 mm parallel back-copper corridor, two
transitions per signal and an inline ESD protector. The opposite front GND
plane has interruptions, including an approximately 5.8 mm gap. A same-layer
ground rail and local return vias were added, but they do not establish an
equivalent continuous reference or controlled impedance. Pair geometry and
return paths still need review with the selected stackup and panel harness;
this illustrative board has no qualified 90-ohm geometry. The provisional panel harness pin order, shield
termination and mechanical retention remain unresolved as recorded in the
main hardware README.

Clearance checks do not select insulation category, material CTI, creepage,
surge/fuse coordination or enclosed-temperature/current ratings. The supply
dimensions/pin assignment were checked against the [MEAN WELL IRM-05
datasheet](https://www.meanwell.com/Upload/PDF/IRM-05/IRM-05-SPEC.PDF); they do
not qualify the complete assembly. Mounting hardware, wire entry, soldering,
connector/harness ratings, EMC and actual device operation remain open.
Cut edges require a qualified cutting process, deburring, inspection and
continuity/short checks; exposed copper and environmental protection still need
physical evaluation. These routed studies are not manufacturing releases.

The separate output-board study retains its previously documented two open
`CUT_EN` connections and four via-drill/land intersections. This change does
not repair or hide those findings.
