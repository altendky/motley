# Output-board placement and routing study

Date: 2026-11-14. Starting source: merged PR #31, commit
`81cddc5701fa41644adf3978fc8b2d633878a257`. The developer requested a bounded
semi-real placement/routing attempt, then chose LV left, mains right, and AC
input/output together at bottom right. This extends the `MOT-PROC-001`
exploratory CAD exception; it does not approve a manufactured mains device.

## Result and preserved behavior

The output board is **90 x 65 mm**, down from the preceding 100 x 75 mm
routing study: **22% less area**, or 35% below the original 100 x 90 mm study.
The developer requested this further packing pass after reviewing the first
routing attempt. This is a trial placement, not a demonstrated minimum. J14 and J21 are
on the left; J17 mains input and J10 outlet connection sit together along the
bottom-right edge. The 35 x 29 mm heatsink reserve occupies the upper right.
Mounting positions and actual connector wire-entry/retention remain provisional.

The schematic circuit is unchanged. All 76 footprints retain their identities,
values, requirement fields and pad nets; assembly, ground touch and optional
clip points remain on the front. Carrier and sensor native sources are
unchanged. Functional footprint groups remain available, but moving them now
requires copper rework. This pass has 686 track segments, 64 vias and two
LV-only GND zones, one per copper layer; no GND-to-PE bond was introduced.

## Provisional routing rules

| Item | Study choice and boundary |
| --- | --- |
| Stackup assumption | Two external copper layers, illustrative 1.6 mm FR-4 / 1 oz copper; material, CTI, copper tolerance and manufacturing stackup are unselected. |
| Mains/LV copper | 5.0 mm custom geometric clearance rule. Independent all-layer X-envelope review gives a conservative 5.16 mm separation: mains copper starts at x=80.16, LV copper ends at x=75.00. This is not an insulation rating. |
| Functional mains-domain spacing | 0.6 mm geometric rule, distinct from the mains/LV barrier. It accommodates intrinsic TO-220, sensor and jumper pad pitches; working-voltage, surge and creepage qualification remain open. |
| Load, neutral and PE path | Deliberately selected 2.0 mm trunks, short 0.8 mm TO-220 fanouts, and 1.8 mm / 0.8 mm drilled mains crossover vias. Both tabs of each fuse clip are bonded. Via/current/temperature/fault-energy qualification remains open. |
| Gate/detector branches | 0.4-0.5 mm low-current branches; preferred class width 0.6 mm. Gate/snubber loop inductance and dv/dt/EMI remain unmeasured. |
| LV routing | 0.2-0.25 mm signals; mostly 0.8 mm / 0.4 mm drilled vias, with 16 ordinary 0.6 mm / 0.3 mm drilled vias in crowded LV connections; 0.25 mm class clearance. Global minimum width/clearance is 0.2 mm. |
| Ground copper | Front/back LV-only GND outlines stop at x=75. Ground stitching joins islands; service returns use solid connections. Current/reference ADC returns and relay switching noise still need hardware review/tests. |

Class widths are routing preferences, not DRC minimum-current guarantees.
Actual load-trunk widths were inspected independently of the class settings.
The mains/LV rule checks ordinary copper clearance; the explicit all-layer
projection check is separate because same-layer DRC alone does not establish
that barrier through the board.

The relay remains the package limitation. Its PCB coil/contact copper gap is
5.62 mm, compared with about 8 mm for the other three isolating packages. Omron
lists different insulation claims for different approval standards; its
EN61810 table's basic-insulation clearance/creepage figures must not be replaced
by an assumed universal 8 mm reinforced rating. This pass makes no such claim.

## Routing method and observed checks

The load path was routed first with selected conductor widths; local gate and
detector branches followed. LV routing used local Freerouting 2.5.0 in bounded
trials, each limited to at most two minutes and a 2 GB JVM, with optimizer/fanout
disabled and mains classes excluded. Router-only keepouts blocked x>=75 on both layers, and the
existing mains copper was fixed. The router's guard-overlap warnings concern
fixed mains items inside those intentionally blocked regions; they are not
native PCB exclusions. Final KiCad DRC is authoritative for the declared rules.
The routing process ran without network permission and with telemetry disabled.
No board data was uploaded.

The native Freerouting executable hit a serialization bug. The official Java
build completed local bounded trials. Native import retained
the selected wide mains routing; final local connections, fuse-clip bonds,
ground fills/stitches and unused-via cleanup were then completed. Intermediate
bad/partial trials were not treated as final evidence.

Final KiCad 10.0.8 DRC with schematic parity reports **zero physical/copper
violations and two unconnected items**, both on `CUT_EN`: U20 pin 9 and the
TP5 probe island still need connections. This is a packed placement with a
bounded routing attempt, not a fully routed board. Its exit is 5 for those
opens and the 53 inherited schematic-parity findings: 48 metadata-field differences and five
provisional footprint-assignment differences. No diagnostic categories or DRC
exclusions were added to obtain that result. The existing two manufacturer-
directed grounded-output ERC findings remain separate from copper DRC.

Native annotations pass 20 files / 257 footprints, and all 15 trace fixtures
pass (exit 0). Final repository/RQML results and source identities are recorded
in [verification.md](verification.md). Draft electrical product obligations are
not marked implemented or verified by this experiment.

The three-page combined placement PDF is refreshed, and a separate two-page
output routing PDF shows front/back copper. The unchanged schematic PDF remains
current. These are review artifacts, not manufacturing files.

The two project minima now permit ordinary 0.6 mm / 0.3 mm drilled LV vias;
preferred class sizes remain unchanged, as do the actual mains vias and all
clearance rules. [JLCPCB's DRC guide](https://jlcpcb.com/blog/design-rule-check)
describes this size as a standard through via. No microvias or filled/capped
via-in-pad process is selected.

Independent via/pad review identifies four remaining drill/land intersections
at C203.1, R202.2, U2.6 and U30.1. C202.1 has annular-copper overlap only, with
the drill outside the land. These are explicit unfinished DFM details, despite
native DRC allowing same-net overlap. Four additional LV overlaps found during
the repair were moved clear of the lands. The preceding 100 x 75 mm result and
its checks remain historical in [verification.md](verification.md).

## Remaining work before fabrication or energization

Exact mains terminal/fuse/snubber/relay footprint selection, header/shunt mains
ratings, actual heatsink/clip/interface and enclosure geometry remain open.
Insulation category, pollution/material assumptions, creepage/clearance, surge,
fusing/fault interruption, PE implementation, copper/via temperature and
isolation manufacturing rules still need qualification. The current 5 mm rule
does not resolve universal mains compatibility. Detector/gate timing, current
sampling/noise, ESD, hot/partial connection behavior and firmware are also
unverified. Trace length/return cleanup and further placement optimization can
be considered after reviewing this first complete trial.

Mounting centres moved with the packed groups. A provisional 7 mm screw-head/
washer envelope now fits entirely on one side of the isolation corridor at
every mount, and the heatsink reserve intersects only Q102's courtyard. Actual
screw/washer/clip metal and enclosure access remain outside the copper proof.
ADC return quality, gate-loop length and EMI still need electrical review and
measurement; geometric connectivity does not establish their performance.

## Primary package/routing references

- [Vishay VO3053 option-7 package drawing](https://www.vishay.com/docs/83749/vo3052.pdf)
- [Broadcom ACPL-K370/K376 land pattern and isolation](https://docs.broadcom.com/doc/AV02-2153EN)
- [TI TMCS1123 HV land pattern and layout](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf)
- [Omron G6DN dimensions and approvals](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6dn.pdf)
- [Freerouting 2.5.0 CLI](https://github.com/freerouting/freerouting/blob/v2.5.0/docs/command_line_arguments.md)
