# Modular controller study verification

## Formatter-style SVG pre-commit, 2026-11-14

The developer requested formatter behavior for the local hook. `MOT-CI-004`
retains its identifiers with updated local-formatting and read-only CI criteria.
Pre-commit uses `--fix`; CI explicitly uses `--check` and skips only the formatter
during its remaining pre-commit run. Manual `--write` remains unchanged.

Eleven unit fixtures pass (exit 0), including regeneration/restaging and index
checks. Real pre-commit runs on deliberately stale/missing SVGs regenerate their
exact original bytes and fail (exit 1); retries with matching tracked files pass
(exit 0). Read-only stale checking fails without writing. Native CAD and local
settings remain byte/mtime identical. A separate scratch Git index confirms
staged deletion is regenerated, retry without adding remains blocked, intent-to-
add remains blocked, and adding the regenerated file permits the hook to pass.
No commits or signing were needed in that disposable fixture repository.

Independent review found no remaining blockers. Current SVG bytes are unchanged
from commit `54f0fed`; only tooling, requirements and documentation change.
Full pre-commit passes, including actionlint, all unit/trace fixtures, formatter,
standard RQML and mapped-implementation approval (exit 0). Explicit read-only
freshness passes (exit 0), and standard RQML reports no drift. Product backlog
remains 36 unimplemented and 43 unverified requirements.

| Tested source | SHA-256 |
| --- | --- |
| scripts/board_images.py | `bc14b4d6b2d1911085114241486515a618371cb9532f43fc978d31c01b5a926a` |
| scripts/test_board_images.py | `71a000c150f77b5cf7709cf1703e9d70b88e7691df68f49f4487259a53f72481` |

## Original generated SVG checks before formatter update, 2026-11-14

Approved `MOT-CI-004` records the developer's request for versioned derivative
SVGs with normalized timestamps and pre-commit/CI freshness checks. Four views
now live under `generated/board-images/` with a derivative/source README. The
exporter uses pinned KiCad 10.0.8, fixed plot options, an isolated default theme
and temporary PCB/project copies. Document titles/descriptions and whitespace
are normalized without changing vector geometry or stroked-text descriptions.
Native CAD bytes remain identical to the preceding packed-layout revision.

`mise exec -- uv run scripts/test_board_images.py` passes eight fixtures,
exit 0. Real checks from another working directory with hostile user preferences
pass; repeated `--write` preserves both bytes and modification times of matching
images. Altered SVG, missing SVG, extra SVG and a changed native reference each
fail with exit 1; explicit regeneration repairs the missing output. Restored
inputs pass. Before/after snapshots confirm checks leave all source and output
files untouched, including local project settings. Independent review confirms
temporary PCB/project inputs suffice for the current embedded geometry/fonts.

The freshness hook always runs, including deletion-only commits. CI's existing
Repository checks job installs pinned KiCad and runs `pre-commit --all-files`;
the existing aggregate dependency propagates failure. CI wiring is reviewed;
execution evidence here is local. Full pre-commit and explicit new-file checks
pass (exit 0), including native traceability, the SVG fixtures/freshness check,
schema/strict lint, standard RQML and mapped-implementation approval.

| Tested source | SHA-256 |
| --- | --- |
| scripts/board_images.py | `d9cc3a88f0987bf8a587551758cf372602a15aa9ee4a1837a34ad685d7e3e423` |
| scripts/test_board_images.py | `6430901a19d60d3fe0ecc3f30fe3db78f813e1acde8ae3687d6685d8c8fb51f3` |

SVG freshness is independent of the outstanding routing/DFM findings below and
does not close electrical product obligations. Generated SVGs and their matching
native board revision must be committed together.

## Packed output-board placement, 2026-11-14

The developer requested tighter placement after reviewing the 100 x 75 mm
routing study below. The output board is now **90 x 65 mm**, 22% less area;
LV remains left, mains right and both AC connections at bottom right. This
continues the `MOT-PROC-001` exploratory exception and approved `MOT-HW-003`
annotation obligation. The circuit, component selection and schematic are intact.

Independent native review confirms all 76 footprint identities/properties/pad
nets, front assembly and touch access, the full 35 x 29 mm heatsink reserve,
provisional 7 mm mounting-head envelopes and all seven wide mains paths.
Projected all-layer copper separation remains 5.16 mm. There are 686 segments,
64 vias and two LV-only GND zones. Sixteen LV vias use ordinary 0.6/0.3 mm
geometry; two project minima now permit it. All other project settings, custom
clearances and actual mains-via dimensions are unchanged from the preceding
trial. Thirty-six other native sources are byte-identical to that trial.

Final KiCad 10.0.8 DRC reports **zero physical/copper violations**, **two open
connections on CUT_EN**, and the inherited 53 parity findings (48 metadata,
five provisional footprint assignments), exit 5. U20 pin 9 and the TP5 island
remain unrouted. Independent same-net via review also finds four drill/land
intersections at C203.1, R202.2, U2.6 and U30.1; C202.1 has annular-copper overlap
only. These unfinished routing/DFM items are not waived by passing native
physical DRC. No diagnostic categories or exclusions were changed. The
[routing review](output-routing-review.md) records details and qualification gaps.

Native annotations pass 20 files / 257 footprints, and all 15 trace fixtures
pass (exit 0). Only the inspected output PCB/project annotation baselines were
refreshed through RQML. Full pre-commit passes, including schema/strict lint,
standard RQML and mapped-implementation approval (exit 0). The requirement
backlog remains 36 unimplemented and 43 unverified; this experiment does not
close product obligations.

| Checked source | SHA-256 |
| --- | --- |
| motley-ac-output.kicad_pcb | `44bf7c4621ace38860c8fdbcf6450d458834e2b7a1688047b18e82640f5b2d2d` |
| motley-ac-output.kicad_pro | `9be71d93c7bcf868baec769ec3d00992bc36f52f8a91d60a855ad7316cdb9140` |
| motley-ac-output.kicad_dru | `96fbf97d53dacc811fd5c0d1542a214558497cec2d228871cffe12618eccd064` |
| requirements.rqml | `3f25c134ce1e7451bd3f61dece1e330ed50579e0c59da8c5b26fd40001638adc` |

The placement PDF retains three pages/bookmarks and a component-only output
view. The separate copper PDF has two pages. Changed pages were rendered and
inspected, including the merged placement page and both copper views. The
component-only view supplies legible black reference labels alongside the
colour copper plots. The 24-page schematic PDF remains
current because its native sources are unchanged.

| Review PDF | Bytes | SHA-256 |
| --- | ---: | --- |
| motley-controller-placement.pdf | 364384 | `4f3583f359a4162b2e19e61f2e522cdd7ac154812f43b931cf0a7b6626d84f0d` |
| motley-ac-output-routing.pdf | 265261 | `115b8cd938ab5b70f9eb249f27f3e6f898a79a26fc28a0a6cccea8bbd9800f97` |

## Earlier 100 x 75 mm output routing study, 2026-11-14

The developer authorized a bounded output-board routing experiment with LV on
the left, mains on the right and AC input/output together at bottom right.
This extends the `MOT-PROC-001` exploratory exception. The
[routing review](output-routing-review.md) records provisional geometric rules,
method, primary package references and remaining limits. The schematic circuit
is unchanged; no product requirement is marked completed by these checks.

The output PCB is 100 x 75 mm, with 525 track segments, 34 vias and two LV GND
zones. All 76 footprint UUIDs, values, requirement fields and pad nets match
the preceding source. All components/touch/probe points remain on the front.
Independent review confirms all seven load/neutral/PE paths using at least
0.8 mm tracks and 1.8 mm / 0.8 mm drilled mains vias, including the short
package neckdowns; 36 segments are 2 mm wide. Thin detector/gate branches are
not required for load continuity. The heatsink reservation intersects only Q102.
Both ground zones are confined to LV, and an all-layer X-envelope comparison
establishes a conservative geometric gap of 5.16 mm. Screw/washer/clip metal,
thermal/fault-current performance and insulation qualification remain open.

Final KiCad 10.0.8 `pcb drc --format json --schematic-parity
--exit-code-violations` reports zero physical/copper violations and zero
unconnected items. Its exit 5 is solely for 53 inherited parity findings:
48 metadata differences and five provisional footprint-assignment differences.
Output `sch erc --format json --exit-code-violations` retains the two documented
TMCS unused-output grounding findings (exit 5). No diagnostic severities or DRC
exclusions were changed. Native trace checking passes 20 files / 257 footprints,
and all 15 trace fixtures pass (both exit 0). Full pre-commit passes, including
schema/strict lint, standard RQML and mapped-implementation approval (exit 0).
Backlog remains 36 unimplemented and 43 unverified requirements.

Only the output PCB/project and new custom-rule source differ; 35 other native
sources, including every schematic and both other boards, remain byte-identical
to commit `81cddc5701fa41644adf3978fc8b2d633878a257`. Two new configuration
annotation links and two draft design-input links were recorded through RQML;
only the inspected output-board annotation baseline was refreshed.

| Checked source | SHA-256 |
| --- | --- |
| motley-ac-output.kicad_pcb | `abbd14535fb0327723b48450a3997225a2664651cf3b79bc09403149e1ec7910` |
| motley-ac-output.kicad_pro | `05afeeff4d0dca29df741b54bdd8b867ad572b455271cc1f30c12fc3ed0207ca` |
| motley-ac-output.kicad_dru | `96fbf97d53dacc811fd5c0d1542a214558497cec2d228871cffe12618eccd064` |
| requirements.rqml | `3f25c134ce1e7451bd3f61dece1e330ed50579e0c59da8c5b26fd40001638adc` |

The combined placement PDF has three pages/bookmarks; a component-only output
view omits copper for legibility. The separate routing PDF has two pages,
front/back viewed from the top. All changed pages were rendered and inspected;
light plot annotations were darkened in the copper review copy. The unchanged
24-page schematic PDF remains current. Current PDF identities:

| Review PDF | Bytes | SHA-256 |
| --- | ---: | --- |
| motley-controller-placement.pdf | 366118 | `fe70af2b06d7ee84d807acf21ecc370851002723694f724a5433330cce973600` |
| motley-ac-output-routing.pdf | 254550 | `5f49930b169f84e9363a43708682df2ac168b5e83ecf88b88cda68d07d3ad70f` |

## Intelligent-output revision, 2026-11-14

This revision follows the developer's request to update the schematic and board
after the architecture discussion. It continues the `MOT-PROC-001` exploratory
CAD exception; approved `MOT-HW-003` governs annotation integrity. Electrical
requirements remain draft. [ADR-0020](../../.rqml/adr/0020-intelligent-output-module-proposal.md)
records the selected study direction, and the
[pin/default review](intelligent-output-review.md) records every current
component/pin disposition, including remaining qualification gaps.

The carrier now supplies six-wire output interfaces with separate selected
logic power and raw actuator power, LP I2C and buffered line timing. Each output
has a STM32C011F6P6 with local regulation/recovery, a VO3053-X007T random-phase
driver, ACPL-K370 voltage observation and TMCS1123B5 current/reference ADC
signals. The MCU can be powered from USB while actuators remain on the raw
mains-derived supply. This is a circuit connection, not completed commissioning,
watchdog, fault-detection or power-loss-safe update firmware.

| Unique design | Components / symbol pins | PCB footprints / reconciled numbered pads | Outline |
| --- | ---: | ---: | --- |
| Carrier | 95 / 291 | 99 / 319 | 100×85 mm |
| Single AC output | 72 / 191 | 76 / 204 | 100×90 mm |
| Sensor mux | 80 / 224 | 82 / 246 | 80×44 mm, L-shaped |

All 247 schematic components, 706 symbol pins and 257 footprints were enumerated.
One carrier, two outputs and one sensor board comprise 319 components, 897
symbol pins and 333 footprints. Counts include DNP and bare test features;
power flags and mechanical-only holes are not schematic components. Existing
symbol/sheet/footprint UUID identities remain intact. Obsolete instances belonging
to the retired monolithic project were removed so standalone KiCad projects
retain their current references. All sensor sheets and the sensor PCB are
byte-identical to the pre-revision snapshot. Project settings are unchanged;
default-only `.kicad_pro` serialization emitted by checks was discarded.

Independent fresh XML/native inspection reconciles all pad nets, component
values and `Requirements` fields, verifies the series relay/current-sensor/outlet
path, both connector pin maps, MCU functions, LP/HP power domains, default
pull-downs and fitted/DNP snubber/region options. All assembly footprints and
touch pads are on the front. Outlines remain within 100 mm; there are zero
tracks, vias or copper pours. Placement groups remain movable. There is no
clearance qualification simply because the unrouted geometry passes DRC.

KiCad CLI 10.0.8 ERC reports the existing carrier PS1 stock-symbol mismatch
warning (exit 5), two output open-collector-to-power-output findings (exit 5),
and no sensor findings (exit 0). Both output findings are the TMCS1123 ALERT/OC
pins deliberately grounded as TI directs when unused. Their electrical pin
types and connections are retained; no new global severity suppression was
introduced. KiCad DRC reports zero physical violations on all three boards.
The intentional unrouted items are 238/147/175 and parity findings are 49/53/70
for carrier/output/sensors respectively (all DRC exits 5). Parity comprises
47/48/70 metadata differences and 2/5/0 footprint-assignment differences;
independent reconciliation checks actual pin-net/value/requirement consistency.
The inherited blank mains footprint assignments remain provisional.

The new Broadcom SSO8, TI DVG10 and Vishay option-7 land patterns follow their
manufacturer package drawings and remain study footprints. The Vishay pattern
has 9.53 mm pad-column spacing with 1.52×1.78 mm pads; the former generic SMDIP
assignment did not match option 7. Package drills/copper/paste tolerances,
assembly rules and all mains isolation geometry still need final qualification.

The combined schematic has 24 pages (carrier 7, output 5, sensors 12); the
placement PDF has three pages. Both retain the three design bookmarks and
stable review paths. Rendered changed schematic pages and both changed
placements were inspected; no routing or manufacturing files are generated.

`uv run scripts/hardware_trace.py` passes 20 annotated files and 257
footprints; `uv run scripts/test_hardware_trace.py` passes all 15 fixtures.
Both exit 0. Full `mise exec -- pre-commit run --all-files` passes (exit 0),
including RQML validation, strict lint, standard consistency/drift and the
mapped-implementation approval gate. Standard RQML passes with zero drift,
dangling references or premature implementations; backlog remains 36
unimplemented and 43 unverified requirements. Seven new native annotation
links and nineteen draft design-input relationships were recorded. Only
reviewed changed MOT-HW-003 source baselines were refreshed after inspection
and observed checks; electrical product requirements were not self-approved.

Checked specification SHA-256: `ea0a8782859f70d9940ea8996993b5fc8a60fc169862d6c5c1d71987a106d0fc`.
The sorted 37-file native manifest uses one UTF-8 line per source:
`<sha256>  hardware/controller/<path>\n`; manifest SHA-256:
`c9d850e7fb61cad55d144be6fe9e33a76b4b4a5bdf651cc5ca09022f772af6ce`. The individual source identities are below.

| Review artifact | Pages / design bookmarks | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| motley-controller.pdf | 24 / 3 | 1262406 | `812161efe4d9868a625034ee66352d1a6a07119eec9b0c40f05e684f048b48d6` |
| motley-controller-placement.pdf | 3 / 3 | 374730 | `6d1d34bb8a63d0da7c923c238ea8ab2e420815ee4d69d505959b18516553dcd3` |

| Native source in hardware/controller | SHA-256 |
| --- | --- |
| Motley.kicad_sym | `d9d6ca992a29e81e175f22a552f8037b1ccb1a66c59547328a992aa2fa835ef7` |
| Motley.pretty/ACPL_K37x_SSO8_Study.kicad_mod | `c57159dff22577fd6172392067cd1699a87c76798f3c92270c4541ff89bc8dc9` |
| Motley.pretty/ESP32-C6-WROOM-1.kicad_mod | `568d88bd414795e7fee4fea1d61174a9d6d23ba423ae406e2bc2714e1afe86d8` |
| Motley.pretty/Mechanical_Pin_PTH_Study.kicad_mod | `ad0353acad0927d098dd80da87b866cc53b4edfe5d556dca7dbe43f464af4c2e` |
| Motley.pretty/Relay_G6DN_1A_L_DC5_Study.kicad_mod | `a14222197bff677d00e25ed0438f4dde523effc991f1c7062ecd6404135d94ee` |
| Motley.pretty/TMCS1123_DVG10_Study.kicad_mod | `bda118ef04ae4147e97b9d21ea8b6837f01e37087b90307fc735f685b80a6d4d` |
| Motley.pretty/TouchGround_8mm.kicad_mod | `a4f1bceba6230a1cf6ab3a760d1e9f0644200b8ccd8a630eb2ef7ad6eae7a01e` |
| Motley.pretty/VO3053_Option7_Study.kicad_mod | `e26ffb5473b2371e8e2f2c261b1750df94ee7d9b4587fc2b6b6117b9ac7f4a9a` |
| Motley.pretty/WireLoop_P2.54.kicad_mod | `5e996c3e0f85643e4c05bb1f5be4595ae655e9e0e4784fea24bb30c001ce2f24` |
| Motley.pretty/WirePost_1mm.kicad_mod | `9e02ddc7191c62da1f43e54aaf771540dcca8549262ac5bb448101201ffebab6` |
| MotleyPower.kicad_sym | `bf28a07f77bd20c7c8371bdf4ba95a4375b76814ade88128ead2ada544763a77` |
| OutputStudy.kicad_sym | `96a6df360fc81ca8e7046ab59c3d13d4b7c463f1fe5541e99537afe40049b77e` |
| carrier-access.kicad_sch | `dbe47a24ad12d904e34c7cf2341076cdd1da339988a6937e4a414a8fa4eaee6f` |
| controller.kicad_sch | `7c032913cc82a5f5d96be21f257bcb2a53b0cc2b1c8d64ab1e979fb1be8897f2` |
| fp-lib-table | `f0f5afca0c428d0f7597f0c641acdcb8c96b46196be6e57898d4ab6b0d60019f` |
| heater-channel.kicad_sch | `5b98aaeb02cb063978511e033c108e442a1ec0cf1449027e181a7d142d948dde` |
| line-reference.kicad_sch | `965c8ad358ab401b95b5e3d77e89f900adbc1ddd2d68fa544ea83e860944ac1f` |
| motley-ac-output.kicad_pcb | `87f13d10a94d2772ba8939c93f4052f6c7ed514e8ebde44d099c8e90cfbab93f` |
| motley-ac-output.kicad_pro | `e7f1284a2a56f64884d80ee2d9c7f5cd17d4b8881d7d1fb9b48631d5caa094e5` |
| motley-ac-output.kicad_sch | `3791fcf357078839c2231731bad698f74fad84b23b21d8a9bd42048df777991c` |
| motley-carrier.kicad_pcb | `3da00dbcfd5c6912e2c08bed98404128813633da536bc64515d99df10d5744b5` |
| motley-carrier.kicad_pro | `31bbd4990d03d0c164afeed26713d3cc113a59b6d10c1993abb459209e5e807f` |
| motley-carrier.kicad_sch | `d4a4cf29ee0bfc62cd36710af7ee206b1c27c2485a8f5c5e79b20e3627161087` |
| motley-sensors.kicad_pcb | `af74c2913611de4850fb9a778f3831dd866d297b93d7b107bcc8880e75bf403f` |
| motley-sensors.kicad_pro | `ce8f50b8cfd251904732c6868ff9ba98d9a917059801e3d7280df4472ba5f527` |
| motley-sensors.kicad_sch | `094068119528af7bceffbec44416b2534b57b864b613df85b36ff5c96c10bab7` |
| mux.kicad_sch | `6dd91ad68cb5755d44177572707d2621f7c347350751870c1b6f85a4f307207a` |
| output-access.kicad_sch | `693d926250d33eeab33842e2c29704d05205c0cead5adc9c3cef90c45c72f1cf` |
| output-control.kicad_sch | `969a97dbf4979b3c6dcc47d9dc87960af91b085fc622198849520e8c17d29c41` |
| output-feedback.kicad_sch | `001c93a0b98a8cadf061cbf20304d7ab1f16e0711b5ace13f13acbc8a906ce4f` |
| power.kicad_sch | `6cd9d8044a37ad4dca0260642186068023377936b5f91a0adc924ea6faf951da` |
| qwiic-bench.kicad_sch | `539bb81c6afaa753bd1886c222bd9d1d134cf11d903e3b06898473c89dd65f3e` |
| sensor-access.kicad_sch | `9f07f41b2d45bd4808527aef9496c8bb2c8ae9149a504d833aa5382612ebcf72` |
| sensor-port.kicad_sch | `b652997cbde8b72b54122874582927edd8dfbaf3e050c52e4004383da2b02f9e` |
| sensor-ports.kicad_sch | `8fa5f00bb87bd6688f1db4c40904b14a3071bf15ba2798e3dfd40507f9360db0` |
| sym-lib-table | `b7863c50299d29f52a8e1614e53dfafbb27d175b6c5195e0857b4121f8898dcb` |
| usb-power.kicad_sch | `76084cdecf17fc2dd15f87dd98dcfc0f4edc6bcc5416a53331f6f5b3a2a6fafd` |

Earlier dated sections describe their own historical snapshots.

## Historical verification records

Date: 2026-11-13. Tools: KiCad CLI and pcbnew 9.0.8; pypdf for combined PDFs.

Scope: structural verification of the exploratory exception described in
[README.md](README.md), governed by `MOT-PROC-001` and
[ADR-0011](../../.rqml/adr/0011-single-output-modules-and-sensor-core.md).
No hardware, firmware-control, mains, thermal, ingress, sensor-accuracy or actual
trimming tests occurred. No product implementation or verification is claimed.

## KiCad 10 native format migration, 2026-11-14

The developer requested KiCad in mise and migration to its newer native formats.
`mise.toml` and `mise.lock` now pin the official full Linux x86-64 AppImage at
10.0.8; the installation extracts once and installed launchers dispatch through
upstream `AppRun`. Other platforms skip this tool and need their native KiCad
10.0.8 package. This maintenance supports approved `MOT-HW-003` and preserves
the existing `MOT-PROC-001` exploratory electrical-design exception.

KiCad's own `sch upgrade`, `pcb upgrade`, `sym upgrade` and `fp upgrade` commands
all exited 0. Every child sheet was upgraded individually: 14 schematics, three
boards, two symbol libraries and six footprints. Schematics now use format
20260306, boards/footprints 20260206 and symbol libraries 20251024. The three
`.kicad_pro` files remain byte-identical; the CLI has no project upgrade command.
The serializer rewrote indentation/order and explicit defaults, moved hidden
field syntax, converted PCB nets from numeric IDs to names and converted legacy
footprint timestamps/reference/value text into the current representation.
KiCad repaired three pre-existing duplicate UUIDs (one controller wire and two
output-root symbol pins) and supplied missing pin/graphic UUIDs. Symbol, sheet
and footprint identities used for traceability remain intact.

Project stock-symbol tables now use `KICAD10_SYMBOL_DIR` and `.kicad_symdir`
directories. Footprint/model references use the corresponding KiCad 10 variables.
The project footprint table explicitly includes its used MountingHole library,
so a fresh configuration does not depend on a previously initialized global
table. All referenced stock symbol and footprint library paths resolve.
Four of the 27 unique stock STEP paths are absent from the full distribution:
IRM-05-xx THT, Littelfuse 111 clips, Texas UQFN-10 1.5x2mm and MetzConnect
RT13703HBWC. The shipped stock footprints still reference those same missing
model names; no substitute geometry was invented. This limits 3D visualization,
not the preserved PCB geometry or connectivity.

Fresh KiCad 9 and 10 XML netlists have identical component references, values,
footprints, hierarchical identities, requirement fields and pin-to-net mappings:
82/31/80 components and 60/23/51 nets for carrier/output/sensors. Comparison
normalizes the empty-datasheet marker and KiCad 10's pinfunction export suffix;
pin numbers and electrical types remain unchanged. Parsed native comparison
confirms all 203 footprint identities, placements, pad geometry/nets, outlines,
groups and rule-area geometry are preserved, with no added routing. Schematic
differences outside default/empty fields are serializer precision normalization
and the duplicate-UUID repairs described above.

Fresh `sch erc --format json --exit-code-violations` on KiCad 10 reports one
carrier warning (PS1 IRM-05-5 differs from the new stock symbol), exit 5; output
and sensor ERC each report zero findings, exit 0. `pcb drc --format json
--schematic-parity --exit-code-violations` reports zero physical violations and
the unchanged 212/56/175 unrouted items, exit 5. Its parity findings are
41/34/70: respectively 39/29/70 metadata-field differences and 2/5/0 footprint
assignment differences. Repeating the exact KiCad 10 checks against a preserved
copy of the original KiCad 9 sources, with only updated library tables, produces
identical ERC, physical DRC, unrouted and parity findings. They are existing
design/library differences exposed by the new tool, not conversion regressions.

`uv run scripts/hardware_trace.py` passes 17 annotated files / 203 footprints;
`uv run scripts/test_hardware_trace.py` passes all 15 fixtures (both exit 0).
ShellCheck passes the installed launcher source. RQML tool/library links record
support for native traceability, not implementation of draft electrical goals.
Full `mise exec -- pre-commit run --all-files`, the new launcher's scoped
pre-commit run and `rqml check requirements.rqml --strictness standard` pass,
exit 0. Reviewed implementation baselines were refreshed after inspection and
the observed checks. Coverage backlog remains 37 unverified and 30 unimplemented
requirements; zero unapproved implementations, dangling references or lint
findings are reported.

The checked native set comprises 30 files: the 25 migrated native design/library
files, three unchanged projects and two library tables. Its manifest is sorted
by repository-relative path, one UTF-8 line per file in the form
`<sha256>  <path>\n`; the manifest SHA-256 is
`60e47a45136cba561cec38af5a36c74ce1b132274fec6f36523ff8ffc3bd041e`.
Trace checker/test source SHA-256 values are respectively
`e2c6e9bcd1e4b5a9bd78d61fd2353052598c9430390aa377efeb3fca9f8ea55e` and
`45613bac1cd0d50c1d31ad593479c3a0a81e6a6b11271a55cfc970de59efc80f`.

## Current MEAN WELL supply substitution, 2026-11-13

The developer selected MEAN WELL IRM-05-5 in place of RECOM RAC05-05SK and
explicitly retained Omron G6DN-1A-L DC5. This component implementation detail
extends the existing MOT-PROC-001 exploratory exception; it does not approve
the draft electrical requirements or change the isolated 5 V / 1 A architecture.
MOT-HW-003 still governs native annotation integrity. Earlier sections and
dated JLC quote packages describe their preceding source snapshots.

PS1 now uses the stock IRM-05-5 symbol and IRM-05-xx THT footprint, with
JLC C48603696 recorded in both native fields. Independent fresh-netlist review
confirms pins 1 neutral, 2 fused line, 3 secondary GND and 4 raw 5 V; the
obsolete RECOM NC pin/marker/net is removed. The priority-sense node is renamed
MAINS_PRIORITY_SENSE without changing its connectivity or component values.
USB remains optional backup; heater drivers still use raw mains-derived 5 V.

The larger module is at (132, 56) mm, rotated 180 degrees: AC pins are on the
right at (132, 56)/(132, 45.25), secondary GND/+5 V on the left at
(93.5, 45.25)/(93.5, 53.25). Stock drills are 1.5 mm and the body spans
x89.9-135.6/y41.8-67.2 mm. It fits the unchanged 100 x 85 mm outline.
C1/C2, D30/D40-D43, R44/R45 and H2 move to clear it; drawing labels and J13's
reference move for legibility. All other footprint positions are preserved.
The original module UUID, schematic path, requirements field and placement
group are retained. Independent comparison checks all numbered pads against
fresh XML, including repeated module grounds, and finds no unintended net
changes. Output/sensor PCBs and heater circuitry are byte-identical to the
pre-substitution snapshot. The Omron selection and its driver are unchanged.

Carrier ERC reports zero violations (exit 0). Physical DRC reports zero
violations, with 212 intentional unrouted items and the same two existing
footprint parity warnings (exit 5 with --exit-code-violations). All footprints
and touch points remain on the front, with zero tracks/vias/copper pours and
the original antenna rule area. Native trace checks pass 17 files and 203
footprints. The pin inventory is now 193 components / 549 symbol pins across
the three unique designs, or 224 / 622 with two output boards.

Both combined PDFs are regenerated: 21 schematic pages and three placement
pages. The changed carrier root, power and USB sheets and carrier placement
are rendered and visually reviewed. The optional PDF bookkeeping helper is
absent on this host; actual KiCad export, pypdf merge and Poppler rendering
succeeded. Current native source hashes are recorded below and in the pin
review. Only the four inspected changed MOT-HW-003 implementation baselines
were refreshed after the observed structural review. All 15 trace fixtures
pass. Full repository pre-commit passed; the scoped run additionally removed
whitespace from the new symbol, so its source hash and reviewed baseline were
refreshed before repeating the affected checks.

Ripple/overshoot, startup/source transfer, inrush/fuse coordination, actual
stock revision, enclosed-temperature derating and final mains routing remain
unqualified. The 200 mVpp ripple, larger height and approximately 2.04 W
full-load loss are recorded in the component candidate record. No hardware,
manufacturing, safety or immunity test is claimed by these structural checks.

## Addressed mux and chain interfaces before supply substitution, 2026-11-13

The developer accepted ADR-0018: switch-selectable mux addresses, two upstream
Qwiic and two five-pin deployment connectors on each mux, and two Qwiic sockets
per controller bus. Draft MOT-HW-009/010 were refined; MOT-HW-011/012 and future
MOT-SENS-006 record address bias, pull-up configuration and global sensor
visibility. No firmware is implemented by this exploratory CAD extension.

Carrier J23/J25 share HP data and J24/J26 share LP data; all four power contacts
have individual removable 0-ohm links and local TVSs. Sensor J10/J11 share
connector-side power before R50. J12/J13 pass all five signals, including
shared reset. Single-host/supply/no-loop procedures remain required; no source
ORing, signal isolation or per-socket current limiter is added.

SW1 is a preliminary CTS 219-3MSTR/C3012353 choice using the stock CTS-family
gull-wing footprint. Actual exported nets confirm pairs 1-6, 2-5 and 3-4:
pins 1/2/3 to local 3.3 V, 6/5/4 to A0/A1/A2, each with its own 10k pull-down.
Independent assertions check all eight states, 0x70 through 0x77. Address draw
is nominally 0-0.99 mA total; the 1 uA address-leakage term alone produces
10 mV across a 10k OFF pull-down versus nominal 0.99 V VIL at 3.3 V. This
supports a DC bias assessment, not transient or dry-contact qualification.
CTS specifies dry-circuit life at 0.1 mA/5 V; the exact 3.3 V point and actuator
height/assembly remain to qualify. MSTR switches ship ON; configure unpowered.

R55/R56 separately feed unchanged R2/R3 = 4k7. Assertions cover all four
fitted/removed link combinations, separate floating feed nodes and unchanged
reset bias. With links removed, suitable external bus pull-ups must remain.
All eight muxes retaining 4k7 pulls, a carrier 10k and one selected 2k2 branch
would give about 444 ohm nominal and 7.4 mA at zero LOW, before probe-added
pulls; this is a reason to configure aggregate pulls, not a valid LOW-margin
claim. Firmware must deselect previous muxes and track active heater pulses.

Independent before/after review confirms every existing footprint UUID,
orientation, position and source path. Old carrier footprints remain unchanged;
sensor changes to old pad nets are limited to the intended address/pull-feed
and equivalent named Qwiic power nets. Fresh XML matches all numbered pads:
273 carrier, 226 sensor and 79 output. Output, sensor port and access circuits
are otherwise unchanged. Every footprint and 8 mm GND touch pad is front-side.
The mux fixed leg widened 29 to 49 mm behind five positions, retaining the
same 80 x 44 mm envelope. All 26 common-core footprints survive every marked
five-through-eight-port variant; rightmost core copper x87.4 mm is inside the
worst first cut edge x89.25 mm. Physical cutting remains unqualified.

| Project | Schematic components / symbol pins | Total footprints | ERC | Physical DRC | Unrouted | Existing parity warnings |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| Carrier | 82 / 253 | 86 | Exit 0 | 0 | 212 | 2 |
| Output design | 31 / 73 | 35 | Exit 0 | 0 | 56 | 5 |
| Sensor | 80 / 224 | 82 | Exit 0 | 0 | 175 | 0 |

DRC exits 5 for intentional unrouted connections and seven existing footprint
warnings. No tracks, vias or copper pours were added. The native checker passes
17 files / 203 footprints and all 15 fixture tests pass. The pin inventory is
193 components / 550 symbol pins, or 224 / 623 with two output boards.
Both PDFs contain 21 schematic and three placement pages; changed roots, mux,
carrier bench leaf and placements are rendered for visual review. Schematic
switch/library configuration and 30 current native source hashes are included
in this review. The new upstream connector's roughly 20-26 mm shared-clamp
path remains a routing concern and may require local ESD devices. No electrical,
physical chain, ESD, cable/load or firmware qualification is asserted.

Full repository and scoped changed-file pre-commit pass (exit 0), including
native trace/test hooks, RQML schema validation, strict lint, standard drift and
mapped-implementation approval. Baselines were refreshed only for the five
inspected changed linked native sources after review and observed checks.
RQML retains 25 unverified and 19 unimplemented requirements as backlog; no
approved requirement is unimplemented, and no implementation is mapped to an
unapproved requirement. MOT-SENS-006 has no fabricated firmware or test link.

## Optional Qwiic bench interfaces before chain extension

Draft MOT-HW-009/010 and ADR-0017 record the requested optional interfaces.
The existing five-pin deployment/reset link J13/J12 is unchanged. Added
carrier J23 exposes HP GPIO19 SDA/18 SCL, J24 exposes LP GPIO6 SDA/7 SCL, and
sensor J11 exposes the mux upstream bus. The carrier has a new dedicated
Qwiic schematic leaf. Every new socket has standard GND/3.3 V/SDA/SCL order.

Both carrier ports source the same switched sensor rail through R44/R45 = 0;
main local pulls are 10k and LP local pulls 4k7. Four new bidirectional dual
TVSs protect the carrier connector data/power contacts. Sensor R50 = 0 links
its bench input power to its existing rail; nearby D60/D61, local upstream
pulls and reset bias remain. Standalone mux bench use requires J12 unplugged,
one controlling host and one supply. No source ORing or I/O isolation was added.

Independent before/after review checks all numbered pads against fresh XML,
existing footprint UUIDs/source paths, unchanged deployment contacts and reset
bias, and strict native object changes after normalizing net-code numbering.
Only the intended GPIO6/7 assignments and additions change connectivity.
All old carrier footprint positions are retained; only sensor D60 moves to
(58, 74) mm. All 18 common-core footprints survive three-through-eight-port
variants with the existing cutting allowance. Every footprint/touch pad is
front-side; outlines remain 100 x 85, 100 x 50 and 80 x 44 mm. No tracks,
vias or copper pours were added. Output and repeated sensor circuits are
byte-for-byte unchanged from the pre-Qwiic snapshot.

| Project | Schematic components / symbol pins | Total footprints | ERC | Physical DRC | Unrouted | Existing parity warnings |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| Carrier | 74 / 229 | 78 | Exit 0 | 0 | 192 | 2 |
| Output design | 31 / 73 | 35 | Exit 0 | 0 | 56 | 5 |
| Sensor | 72 / 199 | 74 | Exit 0 | 0 | 155 | 0 |

DRC exits 5 only for intentional unrouted connections and the seven existing
footprint warnings. Native annotation checks pass for 17 files and 187
footprints, with all 15 fixture tests passing. The complete pin inventory is
177 components / 501 symbol pins, or 208 / 574 with two output boards. Both
PDFs are regenerated: 21 schematic pages and three placement pages. Changed
roots, MCU pin labels, the new bench sheet and carrier/sensor placements are
rendered for visual review. The bench root box was moved clear of mains J16.
Current source identities below cover 30 native files. No firmware, physical
I2C, handling, heater scheduling, load, hot-plug or ESD test is claimed.

Full and changed-file pre-commit checks pass (exit 0), including validation,
strict lint, standard RQML drift/approval and native trace/test hooks. Only the
five inspected changed native baselines were refreshed; the new Qwiic leaf has
its own real annotation-integrity link and draft electrical design-input links.
RQML reports 22 unverified and 16 unimplemented requirements, with no approved
requirement unimplemented or premature implementation. These are backlog gaps,
not hardware acceptance evidence.

## Top-side touch access correction before Qwiic additions

Draft MOT-HW-005 now explicitly calls for the touch point on the top/front
side. Sensor TP1 moved from the back to the front at (63.5, 66) mm, retaining
its 8 mm exposed GND copper, and its LV-GND silk moved above it. D61 moved to
(63, 74) mm to make room; D60/D61 references moved to their right for clarity.
The carrier and output touch points were already on top. Every design's TP1
was independently checked for front-side placement, 8 mm size and GND net.
There are now no back-side footprints on the sensor board.

The before/after identity audit preserves pad-number/net mappings, UUIDs,
source paths and requirement fields. Native text review finds only TP1, D61,
D60 reference text, the LV-GND marking and removal of the obsolete back-view
title from its group. Other native objects are unchanged. The outline remains
80 x 44 mm and all 16 fixed-core footprints survive every supported
three-through-eight-port variant with the existing cutting allowance.

Fresh ERC exits 0; physical DRC has zero violations for all boards. DRC exits
5 only for the same unrouted counts 164/56/150 and existing parity warnings
2/5/0. No routing was added. Native annotations pass for 16 files and 173
footprints. Both PDFs were regenerated: 20 schematic pages and three front
placement pages. The changed sensor view was rendered and visually inspected;
the obsolete back-view page/export was removed. Current native hashes and only
the inspected sensor PCB trace baseline were refreshed. Physical finger access,
ESD immunity and the other electrical qualification gaps remain untested.

Complete and changed-file pre-commit checks pass (exit 0), including standard
RQML consistency/drift, approval and native annotation checks.

## Sensor component-assembly correction before top-side touch revision

D60 and D61 moved from the back to front at (62, 78) and (62, 72) mm. Every
fitted sensor component is now on the front; the only back footprint is the
bare TP1 touch pad, excluded from BOM and placement files. No second component
assembly side is needed. The fixed leg widened from 19 to 29 mm behind three
connector positions; the overall outline remains 80 x 44 mm. Five marked cuts
retain three through seven ports, or leave the full eight-port board intact.

Before/after checks preserve every footprint UUID, source path, Requirements
field and pad-number/net mapping. All other footprint positions, orientations
and sides are unchanged. A UUID-based native-text comparison finds exactly
two footprint changes, three outline segment changes, one updated note, and
removal of only the obsolete two-port cut line/label. All other objects match.
The 16 fixed-core footprints and all eight seven-footprint port groups were
included in retained-pad checks for each three-through-eight-port variant,
with 1 mm kerf and +/-0.25 mm positioning allowance. This remains geometric
evidence, not qualification of cutting or routing.

Fresh ERC exits 0 for all three designs. Physical DRC violations remain zero;
DRC exits 5 for the same intentional 164/56/150 unrouted connections and 2/5/0
existing parity warnings. No tracks, vias or copper pours were added. The
native annotation checker passes for 16 files and 173 footprints. Both PDFs
were regenerated (20 schematic and four placement pages); the changed sensor
front and back views were rendered and visually inspected. The bare touch
point remains visible in the back view. Current source hashes below were
refreshed, and only the inspected sensor PCB's MOT-HW-003 baseline was refreshed.
The PDF artifact-marker utility remains unavailable; actual native exports and
the established PDF merge/render tools succeeded.

Complete and changed-file pre-commit checks pass (exit 0), including standard
RQML consistency/drift, mapped-implementation approval and native trace checks.
The new size-target requirements remain draft backlog, with no fabricated
implementation or hardware verification links.

## Native traceability, ESD and access revision before assembly correction

The developer requested native RQML connections, external-interface ESD review,
board touch-ground points and inexpensive clip probe access. ADR-0015 records
the accepted annotation approach and exploratory hardware boundary. Approved
MOT-HW-003 now has real native/tooling implementation links and structural
verification targets. Draft MOT-HW-004/005/006 record ESD, touch and probe design
inputs; their fields and `dependsOn` links do not claim hardware acceptance.

| Project | Schematic components | Mechanical footprints | ERC | Physical DRC violations | Unrouted | Existing parity warnings |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `motley-carrier` | 62 | 4 | Exit 0, zero findings | 0 | 164 | 2 |
| `motley-ac-output` | 31 | 4 | Exit 0, zero findings | 0 | 56 | 5 |
| `motley-sensors` | 70 | 2 | Exit 0, zero findings | 0 | 150 | 0 |

All DRC commands exit 5 for the intentional unrouted connections and unchanged
seven footprint-parity warnings; no exclusions/rules were weakened. All boards
still have zero tracks, vias or copper pours. Initial new placements produced
real courtyard, mask/short and silk findings; moving only new parts, packing
the existing 16 port pull-ups in repeated columns, and moving dense references
to the review drawing layer resolved them. Actual LV-GND silk labels remain
on the boards. Back-side fields are mirrored appropriately. Only the sensor
pull-ups among the pre-existing component bodies changed position; existing
reference identities, footprint IDs, groups, outlines and cuts are preserved.
Sensor placement areas now cover the full 18 mm connector-arm depth.

Independent before/after analysis removes the new shunt/test-point nodes and
collapses the 16 new 100 ohm series resistors to recover every original
component-pin net group. All physical schematic pads match fresh XML:
carrier 217, one output 79, sensor 211. Source paths, Requirements fields,
DNP and repeated/multi-unit correspondence agree. Both holes of each loop
are pad 1 on one net. Whole-unit totals are 26 dual bidirectional TVSs, five
single 6 V TVSs, 16 series resistors, 16 bare two-hole probe loops, three bare
single posts and four bare touch pads. The all-pin inventory reconciles
163 components/463 logical pins across the designs, or 194/536 when building
two output boards. Of those physical components, 23 are bare-PCB access
features with no purchased part; the remaining BOM count is 171.

Every rail clamp has K1 on the intended 5 V/VBUS rail and A2 on local GND;
5 V-standoff dual arrays are used only on 3.3 V/control nets. All port TVSs
are connector-side of their 100 ohm resistors; the 2k2 pulls remain mux-side.
Output bidirectional clamps do not introduce the low-voltage forward return
that would defeat D101/D102. ERC identified a same-name local/global USB VBUS
scope error: the new clamp/probe were initially on a separate net. Converting
the existing USB_VBUS_RAW labels to global resolved it. Fresh XML explicitly
confirms D38 K1 and TP7 join J21.1, D20.5, C21.1, R23.1, R25.1 and U20.6.
No separate orphan VBUS net remains.

Cut review moved the two diode columns inward from +/-2.4 to +/-2.2 mm.
Actual diode pads now retain at least 0.375 mm to the worst-position cut edge
with the documented kerf/position assumption; resistor pads retain 0.425 mm.
Core touch/probe points survive every cut. New plated test holes do not
intersect SMD footprint bodies on either side. Geometric access-to-mains
pad bounds are at least 31.787 mm on the carrier and 7.946 mm on an output;
output touch-pad distance is 15.16 mm. These are placement observations, not
qualified mains clearances or proof that a particular clip fits safely.

The native-only checker traverses 16 schematic/PCB files and reconciles all
173 design footprints, using full hierarchical source UUID paths. Its 15
positive/negative fixture tests exercise repeated sheets, multi-unit devices,
unknown IDs, missing source links, inconsistent fields and dangling/duplicate
paths. Commands are `uv run scripts/hardware_trace.py` and
`uv run scripts/test_hardware_trace.py`; neither requires KiCad or generated
netlists. Annotation integrity is the only verification they claim.

Both PDFs are regenerated: 20 schematic pages (carrier 1-5, output 6-8, sensor
9-20) and four placement pages (three front views plus a mirrored sensor back
view for its bare touch pad). Changed roots, USB sheet, three new
access sheets, shared port and all placements are rendered for visual review.
Rotated TVS/resistor reference/value fields were made horizontal for clarity.
The PDF skill artifact-marker utility is still absent on this host; native
KiCad exports and the established pypdf helper produce the actual PDFs.

The [ESD/access review](esd-access-review.md) contains per-connector/contact
dispositions, supplier snapshots, the approximately $2.61/unit added fitted
protection estimate, separate loading fees and handling/probe limits. No
hardware was energized or subjected to ESD. Residual clamp/current coordination,
temperature and power/contact states, PB-02 back-power, panel CC/shield mapping,
ground-return routing and physical immunity/access remain qualification work.

Complete `pre-commit run --all-files` passes (exit 0), including the new native
checker/fixture hooks, firmware metadata tests and existing validation, strict
lint, standard drift and approval gates. Command-scoped write access to the
two protected configuration files was used for their ordinary formatter
checks. The actual process diff preserves every prior gate and adds the two
hardware hooks. Reviewed baseline refreshes cover only those process changes
and inspected native annotation/layout refinements after structural checking;
no firmware baseline or electrical-verification evidence was fabricated.
RQML remains backlog-tolerant, with 18 unverified and 12 unimplemented
requirements; no approved requirement is unimplemented. A separate scoped
formatter/check run covers the new untracked native/tooling/document files.

## Historical receiver-local protection and GPIO correction

The developer accepted the low incremental cost and authorized this prototype
change. Under the existing `MOT-PROC-001` exploratory exception, the output
sheet now fits D101/D102 1N4148W blocking diodes, C102/C103 100n B-E filters,
10k B-E pull-downs and 470/150 ohm base resistors. CUT2 is GPIO0 instead of
GPIO7; sensor EN is GPIO11 instead of GPIO20, with R22 changed to 10k.
The [pin-bias review](pin-bias-review.md) records the calculations, added
per-unit parts/joint estimate of $0.1304 and remaining qualification limits.
The two hardware requirements remain draft; no product trace or baseline
refresh is claimed. No firmware or physical hardware was changed/tested.

| Project | Schematic parts | Mechanical footprints | ERC | Physical DRC violations | Unrouted | Existing parity warnings |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `motley-carrier` | 46 | 4 | Exit 0, zero findings | 0 | 128 | 2 |
| `motley-ac-output` | 24 | 4 | Exit 0, zero findings | 0 | 42 | 5 |
| `motley-sensors` | 30 | 2 | Exit 0, zero findings | 0 | 80 | 0 |

DRC exits 5 for each intentionally unrouted board; all seven parity warnings
remain the same blank schematic-footprint assignments. Initial placement of
the new capacitors produced three silkscreen warnings; moving only C102 and
the new capacitor reference fields removed them. No exclusions were added.
The first board-sync helper incorrectly assumed one stamp per physical part;
it stopped on K1's two schematic units. Selecting its existing coil-unit path
corrected the helper, and the successful run preserved that canonical path.

Independent before/after review re-exported the saved preceding schematics.
Collapsing the two added diode edges and removing the two added capacitors
recovers every original output component-pin net group, including mains and
snubber connectivity. Reversing only the two GPIO substitutions recovers all
original carrier net groups. Every carrier/output physical schematic pad
(180/65) matches fresh netlists, including values, DNP and paths. D101/D102
pin 2 anodes face J14.3/.4; pin 1 cathodes feed R102/R106. Capacitors and
pull-downs connect directly across each local base/emitter.

All 50 existing carrier and 24 existing output footprints preserve position,
angle, UUID, footprint ID and parent group. The four new footprints belong to
`01_HEATER_1`; board outlines and group identities remain unchanged. All boards
retain zero tracks, vias or copper pours. Only five native CAD files changed:
controller/USB-power/heater sheets and carrier/output PCBs. Sensor CAD, shared
libraries, mains supply, snubber parts and interface pin orders are preserved.
The all-pin inventory now reconciles 100 components and 330 logical pins;
the physical two-output build has 124 components and 393 logical pin instances.

Fresh ERC, XML export, DRC and both PDF exports use the commands below with
session-local XDG paths. Combined PDFs retain 17 schematic pages and three
placement pages/bookmarks. Changed controller, power and heater pages plus
both changed placement pages were rendered for visual review. A new heater
note initially extended below the page frame and was moved into clear space
before final export. The PDF skill's artifact-marker utility remains
unavailable on this host; native KiCad export and the established pypdf helper
produce the actual review PDFs.

Loaded GPIO VOH/current, actual NPN manufacturer, cold diode drop, hot leakage,
noise/contact transients, all relevant reset/ROM/brownout waveforms and actuator
release/commutation remain hardware qualification work. PB-02 sensor-domain
reset-pull injection, unused-pin and external service-power findings remain
open. Structural checks do not establish those electrical behaviors.

`pre-commit run --all-files` and a separate run over all eleven changed
maintained/native source paths pass (exit 0), including standard RQML drift
and mapped-implementation approval gates. `rqml validate` and the independent
connectivity/pad/placement review pass (exit 0). The requirement note for
`MOT-SENS-005` now distinguishes the historical Feather mapping from GPIO11
on the integrated study; its obligation, status and IDs are unchanged. RQML
backlog remains 15 unverified and nine unimplemented requirements. Current
source identities below record the checked circuit; no baseline refresh or
hardware test link was added.

## Historical integrated-controller and switched-sensor revision

The developer requested the accepted integrated-controller direction in the
schematic, grouped board study and both PDFs. This revises the exploratory
exception under `MOT-PROC-001` and ADR-0014; it adds no firmware, product traces
or reviewed-baseline refresh. It is not a fabrication release.

| Project | Schematic parts | Mechanical footprints | ERC | Physical DRC violations | Unrouted | Parity warnings |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `motley-carrier` | 46 | 4 | Exit 0, zero findings | 0 | 128 | 2 |
| `motley-ac-output` | 20 | 4 | Exit 0, zero findings | 0 | 36 | 5 |
| `motley-sensors` | 30 | 2 | Exit 0, zero findings | 0 | 80 | 0 |

All three DRC commands exit 5 because these boards are intentionally unrouted.
The seven parity warnings are the existing blank schematic footprint fields
with board-only study assignments. No new exclusions or physical violations
are hidden. All boards contain zero tracks, vias and copper pours.

Independent source and exported-netlist review checked WROOM pins, reset/boot
and native USB polarity, both AP2112 regulators, TPS2116 pins and priority
configuration, TS3USB221E RSE package pins/channel/enable and TLV3011B comparator
polarity/POR behavior. A fitted pull-up value-label mismatch was corrected:
mux R2/R3 are actually 4k7 and not DNP in schematic and PCB.

An independent schematic-to-board audit checked all 180 carrier pads and 117
sensor-board pads, values and DNP flags against fresh XML netlists. All nine
WROOM pad-29 lands and pins 1/28 are GND. Raw RECOM remains the output-driver
supply; the selected 5 V output feeds both regulators; switched 3V3 powers the
whole mux/pull-up/sensor domain. J13/J12 retain the five-wire pin correspondence.
The USB mating header's signal order is explicitly project-defined pending
actual cable verification/repinning, not a manufacturer-qualified pinout.

The 100 x 85 mm controller outline and seven existing mains/supply component
positions, angles and UUIDs are preserved. U10 is at (62, 56.05) mm; H1 moves
to (44, 64) mm clear of the antenna reservation. Six unlocked native groups
separate controller, regulators, USB/selection, interfaces, AC input and mounts.
The sensor outline, port/core placement, all positions, angles, footprint IDs
and UUIDs are preserved. AC-output schematic, PCB, project, shared heater sheet
and the original mains-supply sheet are byte-identical to the preceding snapshot.

Commands remain the ERC/netlist/DRC/export commands documented below, using
session-local XDG configuration/cache paths. The temporary update helper had
an interpreter/pcbnew failure before writing; using the installed system
Python with KiCad bindings completed successfully. The WROOM library is pinned
to Espressif tag 3.0.1 with attribution/license retained locally; its only
adaptations are the library path and omission of an unavailable 3D model.

Both combined review PDFs were regenerated with three board bookmarks:
the schematic has 17 pages (controller 1-4, output 5-6, sensors 7-17), and the
placement PDF has three pages in the same order. Changed controller, USB/power,
sensor root/mux/shared-port and placement pages were rendered and visually
reviewed. The output module is still shown once and built twice. The PDF
skill's artifact-marker utility remains absent from this host; native KiCad
exports and the pypdf merge helper produced the review files.

USB current entitlement/inrush/suspend/transfer, harness pinout and mechanical
fit, shielding/shell termination/strain relief, regulator thermal capacity,
sensor off-state back-power and startup, ROM flashing and heater-switching EMI
remain open physical/electrical qualifications. No hardware was energized.

Standard RQML passes (exit 0), with no drift; the unchanged product backlog is
13 unverified and seven unimplemented requirements. The initial aggregate pre-commit
run exited 1 only because the end-of-file formatter could not open protected
`.agents/plugins/marketplace.json` and `.codex/config.toml` for writing.
All other hooks, including Mergify schema validation, firmware metadata tests
and both RQML gates, pass using writable session caches and network access.
Pre-commit on all 19 files changed by this update passes (exit 0). Its first
pass normalized the vendor license's final newline; the subsequent run is
clean. `git diff --check` passes, and all 23 recorded native source hashes
match the final files. No requirements or baseline content changed.

After the developer authorized requesting command-scoped write access to those
two configuration files, the complete `pre-commit run --all-files` passed
(exit 0), including every formatting, schema, firmware-metadata and RQML hook.
SHA-256 checks before and after confirm both configuration files were unchanged.
No formatter wrapper or repository exclusion was needed.

## Pre-intelligent-output checked source SHA-256 identities

| File | SHA-256 |
| --- | --- |
| `Motley.kicad_sym` | `e557a1de158ea9264df70cc5a8d7471576b9f40f7d6d8ba468c7652cd32a8367` |
| `Motley.pretty/ESP32-C6-WROOM-1.kicad_mod` | `5714c18133f1fcfaab88beddf92bcba0a4f37726f0f2404bd1e6ff7005934b15` |
| `Motley.pretty/Mechanical_Pin_PTH_Study.kicad_mod` | `f54ac1d1b04da3e525a552b15dc9589ddfac2b462b33ca2334a3d2665cac1b3e` |
| `Motley.pretty/Relay_G6DN_1A_L_DC5_Study.kicad_mod` | `21014fe1eb67b2dd9b7a64feea7bde100896bada291868d180b482a4793c3422` |
| `Motley.pretty/TouchGround_8mm.kicad_mod` | `87a41340e670c19887619da49b37fd0c87ddb3c8321462fae2d1748636b80149` |
| `Motley.pretty/WireLoop_P2.54.kicad_mod` | `e187fa4a7795c2ccfab4c438ead377fe4535129bee00f00a980a776ff0052bff` |
| `Motley.pretty/WirePost_1mm.kicad_mod` | `6e2e4600edccd3cac271d7a7e6a5a3381976f8831ad356b3cdd1c0ea7e5cf949` |
| `MotleyPower.kicad_sym` | `bb5dd2e24a42f15357ed9ce591cfa0a2b7825bbeff566270b977f35307f9d909` |
| `carrier-access.kicad_sch` | `d2975adc9f3ed7c2a1c331dab80b92d1335d8d95739fd4ec4cdc3ce22391e30b` |
| `controller.kicad_sch` | `73ad913970aaefdf7064b3c9dbf60e966d87927a17b64032b4971dea2a7c5c68` |
| `fp-lib-table` | `a5c48b258c5ef02214d292e07da18c5b0f2f0cffa773c8bb6dbd3c11b66e83e3` |
| `heater-channel.kicad_sch` | `a5e21f6c13f875cd1bafa127c820390dec9b6fb2c8c6a4f6351ef77532a2ca4c` |
| `motley-ac-output.kicad_pcb` | `4077efa09ecd78d1ebf3540ecd91999b5e94b0189125c69a015ce0322819447e` |
| `motley-ac-output.kicad_pro` | `e7f1284a2a56f64884d80ee2d9c7f5cd17d4b8881d7d1fb9b48631d5caa094e5` |
| `motley-ac-output.kicad_sch` | `a4b5362bec1d6d4618e0e1472f6e661e4edd6c1539982e938381e89d79c244d6` |
| `motley-carrier.kicad_pcb` | `164c14fe6d68409f88af1e43bfc27f96c7f0646b2f1676e9d1a0cfd3948f56da` |
| `motley-carrier.kicad_pro` | `31bbd4990d03d0c164afeed26713d3cc113a59b6d10c1993abb459209e5e807f` |
| `motley-carrier.kicad_sch` | `f8dac93b03c1891baf500a1f4f34ab9bd08301a25445c19373f6971c411d77d1` |
| `motley-sensors.kicad_pcb` | `01febb2380997c044b24faadc1214fdddabcc0d3caf6fc9a8082da2970716d35` |
| `motley-sensors.kicad_pro` | `ce8f50b8cfd251904732c6868ff9ba98d9a917059801e3d7280df4472ba5f527` |
| `motley-sensors.kicad_sch` | `9101d48a3edf78b480238c01cc1077844c0b2112728f11fbe50ca54b6e861257` |
| `mux.kicad_sch` | `95cad4a7e2b2de0fdb53f34afd9a9c5cbf2f3564efa499a6f3a48bfb01e6e47e` |
| `output-access.kicad_sch` | `bb3ae7d4c430cd54ea1f08a0c0b0d27f438aa3f653ab54c3ddf6c6e66c5e5cb4` |
| `power.kicad_sch` | `7d28e1aa3cb93cc1e64c3bd6dff164347795f66de0d59ac172272e7ce5a0bf6b` |
| `qwiic-bench.kicad_sch` | `7fb17c0ee7b63ad16440a31e12084ee211d8b876341c104258a17ca054eed457` |
| `sensor-access.kicad_sch` | `6aad7b16b91da885ea0939c474ca10f280e96e0b30cf052018afdbc436d40790` |
| `sensor-port.kicad_sch` | `ceaffb60fd391ac18a4592e845581049851a5bfae359873efe42c2160d1072e5` |
| `sensor-ports.kicad_sch` | `f6116bc20fe6297a3d46ca7931911f46a905f4e08deb4c41a356a99363aec671` |
| `sym-lib-table` | `786e986bca637e3f7e6d679adce07df1cfbaa1c744d39fc80148da961bcf599b` |
| `usb-power.kicad_sch` | `23ac8b24e12196fa678ff7587a1341882022814e03f54bffd8ceec622e474109` |

## Historical single-output-module revision with snubber placeholder

There are three designs and four physical boards: one carrier, two identical
single-output modules, and one sensor board. References repeat between physical
output copies because they are the same design, not two schematic instances.

| Project | Quantity | Schematic parts per board | Mechanical footprints | ERC | Physical DRC violations | Unrouted connections | Parity warnings |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| `motley-carrier` | 1 | 12 | 4 | Exit 0; zero findings | 0 | 32 | 2 |
| `motley-ac-output` | 2 | 20 | 4 | Exit 0; zero findings | 0 | 36 | 5 |
| `motley-sensors` | 1 | 30 | 2 | Exit 0; zero findings | 0 | 80 | 0 |

Each DRC exits 5 for the intentionally unrouted design. Seven warnings across
the three designs are the documented board-only assignments for blank schematic
footprint fields; the physical pair of output boards repeats five of these.
There are no other violations/parity findings or new exclusions. These default
rules do not qualify mains, creepage, current or thermal design.

Commands executed for each project basename:

```sh
kicad-cli sch erc hardware/controller/PROJECT.kicad_sch \
  --format json --output hardware/controller/review/PROJECT-erc.json \
  --exit-code-violations
kicad-cli sch export netlist hardware/controller/PROJECT.kicad_sch \
  --format kicadxml --output hardware/controller/review/PROJECT-netlist.xml
kicad-cli pcb drc hardware/controller/PROJECT.kicad_pcb \
  --format json --output hardware/controller/review/PROJECT-drc.json \
  --exit-code-violations --schematic-parity
```

Native files were saved/reloaded and independently reviewed:

- Instantiating the output netlist twice and joining the five interfaces in the
  README reconstructs **all 70 original physical component references, all 228
  original pin entries and all 75 original net groups** with the J20 ON shunts
  fitted. The only original value/DNP changes are the explicitly fitted R108
  and C101 on each copy; all other values, footprint fields and exclusion
  states match. The present unit has 82 physical schematic components,
  including ten interface-connector instances and two J20 headers. Four
  closed-top shunts are separate assembly accessories. Both the main audit
  and an independent read-only review passed.
- J20 pins 1/3 share C101 pad 2; pins 2/4 share triac A1. The bare-board netlist
  intentionally leaves the two sides separate. Explicitly modeling OFF shunts
  (1-3 and 2-4) disconnects only each C101 pad 2 from the prior A1 net; modeling
  ON shunts (1-2 and 3-4) restores the original circuit. Neither state bypasses
  the series RC parts. One ON shunt alone would still enable the branch.
  J20 and its assembly notes/envelopes belong to the heater group. The stock
  footprint and closed-cap drawings do not qualify pin length, fit, touch
  protection, transients or mains spacing. Default assembly is ON; configuration
  changes require unplugging and discharging.
- Carrier J15/J18 preserve the original separate GPIO heat/cutoff commands.
  Output J14 uses generic `HEAT_EN`/`CUT_EN`. Carrier J16/J19 provide independent
  module feeds; PE, neutral, fused line and low-voltage GND remain distinct.
- Every connected physical pad matches its own netlist, including duplicated
  fuse-pad numbers. Per-board root/sheet/symbol UUIDs, values and DNP states
  match; the module relay uses its canonical coil-unit UUID. All previous
  component UUIDs, footprint assignments and positions/angles are retained.
  Only the canonical heater sheet and AC-output PCB changed among native CAD
  sources for the snubber revision; the carrier, sensor and other native files
  are byte-identical to the saved preceding revision.
- The carrier is 100 x 85 mm; one output module is 100 x 50 mm. The sensor board
  is an 80 x 44 mm closed L with an 18 mm arm and 19 mm fixed leg. Its core's
  complete footprint bounds are within local x1.205..18.425 mm and
  y19.075..41.795 mm, fully behind the first two connector positions. Row centers
  are x5+10*i mm; the row and end margins control total length.
- Six trial cuts at local x20,30,40,50,60,70 retain two through seven connector
  positions. All retain the core, its interface and mechanical pins, and exactly
  the desired connectors/pull-ups. With 1 mm kerf and +/-0.25 mm placement
  tolerance, minimum courtyard margin is 0.325 mm; minimum copper-to-board-edge
  clearance over all variants is 0.725 mm, with 0.85 mm at the connector cut
  edge. Routing crossings, actual cutting, edge treatment and trimmed operation
  remain unverified. Unwanted sockets may be omitted or removed.
- One heater placement area and eight sensor placement areas remain; functional
  groups are unlocked. Carrier signal headers clear the provisional antenna
  reserve. Only the Feather itself intersects it. Mounts clear component
  courtyards. The sensor mechanical pads are isolated, board-only 1 mm plated
  holes with 1.8 mm pads; actual pin fit is unqualified.
- Every board has **zero tracks, vias and copper pours**. Rule/placement areas
  are not copper zones. No routing or manufacturing export occurred.

## Combined PDF refresh

All per-design schematic and placement exports exited 0. The combined files keep
their original paths under ignored `review/`:

- `motley-controller.pdf`: **16 pages**, carrier 1-3, output design 4-5, sensor
  design 6-16. The one-output module is shown once and explicitly marked to build
  twice; the physical unit still has two controlled outlets.
- `motley-controller-placement.pdf`: **three pages**, in the same design order.
  Both PDFs have three board bookmarks. All pages were rendered for the prior
  module/core review. The changed heater schematic and output-placement pages
  were rendered and visually checked again for this snubber revision, including
  the combined schematic's page 5. Native CAD is unchanged by PDF merging.
  Page numbering inside each KiCad sheet is per project. The PDF skill's
  artifact-marker utility is absent from this host; native KiCad exports and
  the existing pypdf merge helper produced the review files.

## Repository checks

Standard RQML check passes, exit 0; the specification, baseline, firmware and
product traces are unchanged. The backlog remains 13 requirements without
verification and seven without implementation. Pre-commit checking all 27
changed/new files passed, exit 0; all applicable hooks passed, including the
standard consistency and mapped-implementation gates. Unrelated hooks skipped.

The required aggregate `pre-commit run --all-files` was repeated for this change
and exited 1 because
the end-of-file formatter could not open protected `.agents`/`.codex` config
files for writing. Automatic approval rejected broader write access to unrelated
configuration in the earlier attempt. This run's Mergify schema download also
initially failed DNS resolution; a network-enabled scoped rerun passed, exit 0.
Firmware metadata tests and both RQML gates passed in the aggregate run.
The safe current checks target
all changed/new files with a session-local uv cache; protected files are neither
modified nor bypassed. This aggregate limitation remains, without implying a
failure in the changed CAD.

## Historical pre-integration checked source SHA-256 identities

| File | SHA-256 |
| --- | --- |
| `Motley.kicad_sym` | `d7d3de9c4849084bac53422ea74ec1fc0d5eaf00d4e87cd52b59b457f8669160` |
| `Motley.pretty/Mechanical_Pin_PTH_Study.kicad_mod` | `f54ac1d1b04da3e525a552b15dc9589ddfac2b462b33ca2334a3d2665cac1b3e` |
| `Motley.pretty/Relay_G6DN_1A_L_DC5_Study.kicad_mod` | `21014fe1eb67b2dd9b7a64feea7bde100896bada291868d180b482a4793c3422` |
| `controller.kicad_sch` | `e24b70b4a23ea493ed4d1c8a6dcd4c409368885be41619de19fd60acb503965a` |
| `fp-lib-table` | `60c8deae579abd86dd18acc7567330b6840d4e9f13c322ec42273cad0642988f` |
| `heater-channel.kicad_sch` | `0c01a5432da9adf4cf307cb08910d25298508557e74806f64b06d99c44e24aa2` |
| `motley-ac-output.kicad_pcb` | `91a9141419390273b0fb26c989c830c97a4bc26ab15de4364a697f64109da393` |
| `motley-ac-output.kicad_pro` | `e7f1284a2a56f64884d80ee2d9c7f5cd17d4b8881d7d1fb9b48631d5caa094e5` |
| `motley-ac-output.kicad_sch` | `abb19c40445baf6a5fa8fe1bba5f7cd9aa27805763bb9dcc5ccc68f74c786b57` |
| `motley-carrier.kicad_pcb` | `615c36fdadbe553fb1391730023ee02780d3149c3585ecc8f16bcebf61b19a8e` |
| `motley-carrier.kicad_pro` | `31bbd4990d03d0c164afeed26713d3cc113a59b6d10c1993abb459209e5e807f` |
| `motley-carrier.kicad_sch` | `636055b0da51584bded75a7627c0f6c9ba391f77b90c2c380f4bc133903a5f6b` |
| `motley-sensors.kicad_pcb` | `83fd265316a6f5d7d3e05538c14715bcbf3657f1a781a038af446c9c89de357f` |
| `motley-sensors.kicad_pro` | `ce8f50b8cfd251904732c6868ff9ba98d9a917059801e3d7280df4472ba5f527` |
| `motley-sensors.kicad_sch` | `b1c377ac2bdf0bc45e3e244821c50459753879d02da7183b46843144b5378a0e` |
| `mux.kicad_sch` | `e8788639b8f5c06a1a0a5763da8642bc607f6604c2b71065bc8ae60c2599c669` |
| `power.kicad_sch` | `4d9e4c73138f694809309369f6c5e170cd5ceea8d551bd92cc38e6c9e1550b14` |
| `sensor-port.kicad_sch` | `c3f3b28d6fe1a7493a2ca42ae75bb0e8c15a61795a3e27afe1e99a4ba4aaba11` |
| `sensor-ports.kicad_sch` | `128baefa50dd758ca67f8ddb13812902bd42a8ebfc184a76dcab0765a6db61df` |
| `sym-lib-table` | `3563da0f7f84c1d0bfa17a222ab3f0a9a992453a6cdf2161cda68a6546de35f1` |

## Historical combined-board checks, 2026-11-11

The following source paths, counts and hashes refer to the retired combined
study and are retained as execution history. They are not current board results.


Date: 2026-11-11. Tool: KiCad CLI 9.0.8.

Scope: structural verification of the design experiment described in
[README.md](README.md), under the recorded `MOT-PROC-001` exception. No hardware,
firmware-control, mains, thermal, ingress, or sensor-accuracy testing occurred.
The sensing goal and sensor power-readiness requirement remain draft and are
not claimed implemented or verified by this schematic.

### Executed schematic checks

- `kicad-cli sch erc hardware/controller/motley-controller.kicad_sch --format json --output hardware/controller/review/erc.json --exit-code-violations`:
  exit 0, **zero errors and zero warnings**, with no ERC exclusions.
- `kicad-cli sch export netlist hardware/controller/motley-controller.kicad_sch --format kicadxml --output hardware/controller/review/netlist.xml`:
  exit 0. Independent netlist review found no miswires in the reviewed pin maps
  and circuit topology; this is not a component qualification or simulation.
- `kicad-cli sch export pdf hardware/controller/motley-controller.kicad_sch --output hardware/controller/review/motley-controller.pdf`:
  exit 0, six pages. Rendered to PNG for visual review and adjusted for readable
  labels, connected heater circuits, and non-overlapping notes.

Independent review checked all 28 Feather pads against the manufacturer's
Eagle design and KiCad footprint; both 3.3 V pads; GPIO assignments; the open
run-power jumper; all TCA9548A pins, address straps and reset; eight separately
paired sensor channels and QT signal order; actual DNP flags; both mains paths;
all NPN and flyback diode pin polarities; triac gate/shunt networks; the split
relay units combining into one physical component per channel; optional series
RC branches; supply pin map; and absence of mains-neutral/PE bonds to LV ground.

The exact part descriptions for the adapted triac and optotriac symbols were
corrected after review. Electrical connections were preserved and ERC/export
were rerun on the source identities below. Final layout review covers all six
rendered pages. No test evidence is inferred from a clean ERC report.

#### Circuit drawing revision

The power, controller, and sensor-port sheets were redrawn after review to use
explicit wires within their circuits. The mains input now visibly feeds F1 and
the RECOM input; C1/C2 visibly parallel the secondary output. Feather I2C/reset,
run-power, mux address straps, and sensor-port pull-ups are wired directly.
Inter-sheet net labels and power/ground connections remain labeled.

Before and after KiCad XML netlists were compared as exact sets of component-pin
net groups, ignoring virtual ERC power-flag symbols. Every physical component-pin
connection group, component value, and footprint matched. Net names for internal
signals may acquire their sheet path when represented as local labels. ERC and
exports were rerun: exit 0, zero ERC errors/warnings. The three changed PDF pages
were rendered and visually reviewed; the other three sheets were unchanged.

### Repository checks

`mise exec -- pre-commit run --all-files`: exit 0. Formatting, configuration,
firmware metadata tests, RQML schema validation, strict lint, standard
consistency/drift checking, and mapped-implementation approval checks passed.
The manual firmware-build hook was not run for this schematic experiment.
The RQML backlog remains 13 requirements without verification and seven without
implementation; no coverage or product-completion claim is made for these files.

Explicit pre-commit checking of all newly created schematic/project/library
files and review notes also passed, exit 0. These files were not yet tracked,
so the all-files run alone would not have covered their formatting.

### Executed placement checks

- Reloaded the saved native PCB through KiCad 9's `pcbnew` API and checked all
  **228 component-pin net entries** against the exported schematic XML,
  including duplicate-number fuse pads. All matched. The board contains
  **70 schematic components, four mechanical mounting holes, 75 nets, and six
  unlocked groups**, with no tracks or vias. Values, DNP state, and schematic
  UUID paths were preserved. The schematic circuit was not changed.
- `kicad-cli pcb drc hardware/controller/motley-controller.kicad_pcb --format json --output hardware/controller/review/drc.json --exit-code-violations --schematic-parity`:
  **exit 5**, with **159 unconnected items** and **12 footprint-symbol mismatch
  warnings**. All twelve warnings are the explicitly documented board-only
  assignments for blank schematic footprint fields; there are no other
  schematic-parity findings. The remaining `violations` list is empty after
  fixing copper-to-edge spacing and reference-label collisions.
  No DRC exclusions were added. The project contains ordinary KiCad default
  rules, not qualified mains spacing, creepage, current, or thermal rules;
  this result does not qualify the board for routing or manufacture.
- `kicad-cli pcb export pdf hardware/controller/motley-controller.kicad_pcb --output hardware/controller/review/motley-controller-placement.pdf --layers F.Cu,F.SilkS,Dwgs.User,Edge.Cuts --mode-single --black-and-white`:
  exit 0. Rendered the single-page placement to PNG and visually reviewed the
  component groups, references, edge orientations, heatsink outlines, and
  planning annotations. The PDF omits the interactive ratsnest, which remains
  available in PCB Editor.

The provisional G6DN footprint uses Omron's package pin spacing; its pad/drill
choices still need qualification. Heatsink outlines, antenna reserve, mounting
holes, and isolation guide are placement assumptions. KiCad expanded the
project file with its default PCB settings during board verification.

#### Compact placement revision

The outline is now **150 x 105 mm**, compared with the initial 180 x 120 mm:
27.08% less area. KiCad 9.0.8's native **Place Off-Board Footprints** command was
executed through PCB Editor on four temporary regional boards. It placed 34
footprints: 16 sensor resistors, four mux supporting components, and seven
small driver components per heater. Large components were fixed anchors;
temporary heater-region obstacles reserved the mains side. Only target
footprint positions and orientations were merged back by UUID. Manual edits
then corrected connector pitch, snubber/relay spacing, mounting-hole clearance,
and reference-label placement. No routing command was executed.

Before/after comparison verified identical footprint UUIDs, schematic paths,
values, library IDs, DNP flags, and complete pad-number/net-name mappings for
all 74 footprints, as well as unchanged membership of all six functional
groups. The board still has 75 nets and zero tracks or vias. Both heatsink
reservations remain unobstructed by the component courtyards. These geometric
checks do not qualify mains or thermal spacing.

The DRC, PDF export, and rendered visual review above were repeated for this
revision. The expected unrouted and board-only footprint-assignment findings
remain; final counts and source identity below describe the compact board.

#### Shared schematic and native repeat revision

The root now instantiates `heater-channel.kicad_sch` twice; the sensor wrapper
instantiates `sensor-port.kicad_sch` eight times. Per-instance annotation retains
all original references. The old separate heater definitions were removed.
Heater controls and sensor signal pairs cross explicit hierarchical interfaces;
the triac A1 label is local, so the two heater outputs remain separate.

Old and new XML netlists were compared as exact sets of physical `(reference,
pin)` groups: all **75 groups and 228 entries** match, as do all **70 component
values, schematic footprint fields, DNP states, and exclusion flags**. An
independent read-only review confirmed the result, the four separate command
nets, and all sixteen separate sensor signal nets. Only the two internal triac
net names changed to their instance-qualified local names.

KiCad 9.0.8's native **Tools → Multi-Channel → Repeat Layout** was executed for
`HEATER_1 → HEATER_2` and `SENSOR_PORT_0 → SENSOR_PORT_1…7`. Target matching
reported OK. Before applying each pass, the native dialog was checked with
placement copying on, routing and other-item copying off, target grouping off,
and locked-item override off. The saved board was reloaded and all 17 heater
target transforms were checked against a `(0, 35 mm)` translation, and all 21
sensor target transforms against an 8 mm horizontal pitch, including rotation.
Component UUIDs, values, footprint library IDs, DNP states, pad mappings, all
six footprint-group memberships, and study drawings were preserved. Ten native
placement areas and the updated schematic-instance paths are retained.

Final ERC: **exit 0, zero errors/warnings across 14 instantiated sheets**.
Final board DRC: **exit 5**, solely for the existing **159 unconnected items**
and **12 provisional footprint-assignment warnings**; the remaining physical
violation list is empty. There are zero tracks/vias and no copper pours.
The two PDFs were regenerated. Root, wrapper, shared port, both heater
instances, last-port annotation, and the repeated placement were rendered and
visually reviewed. No mains, thermal, or hardware-operation qualification is
inferred from these checks.

### Checked source SHA-256 identities

| File | SHA-256 |
| --- | --- |
| `motley-controller.kicad_sch` | `c4bd2aa903ff23dcb248a8fc5dd68b903df101c201f1feeb766a56ff6c320f25` |
| `power.kicad_sch` | `de7fbefc2d4368ffd7d038ab9b16defb32a5e2962a7a66815061660e0491424c` |
| `controller.kicad_sch` | `fcc3f6394b922f3b23f4d72568d64f0ee6af66125f0c9838bf00b06c20f5d144` |
| `sensor-ports.kicad_sch` | `ea055dcabfdd8dde5071eeea680af52c9e451e6d49946140acbbb36951fbd93b` |
| `sensor-port.kicad_sch` | `fae60a81ff1f05a45ee5c84c4028a5ef8bc0ece4e74936e67c17743b381ed520` |
| `heater-channel.kicad_sch` | `aa08587173c315a453825c64431faa0427db3865846a4cfd63afff75ee0629e7` |
| `Motley.kicad_sym` | `d7d3de9c4849084bac53422ea74ec1fc0d5eaf00d4e87cd52b59b457f8669160` |
| `motley-controller.kicad_pro` | `e92c295de7c4b82ed4a5051ed96bcb53a711be8b31e874ab1ff77ba506433b33` |
| `sym-lib-table` | `3563da0f7f84c1d0bfa17a222ab3f0a9a992453a6cdf2161cda68a6546de35f1` |
| `motley-controller.kicad_pcb` | `98fd14cf881e3f141959eaf290461b672769ba8b37017b349c8f92e95efe01c2` |
| `Motley.pretty/Relay_G6DN_1A_L_DC5_Study.kicad_mod` | `21014fe1eb67b2dd9b7a64feea7bde100896bada291868d180b482a4793c3422` |
| `fp-lib-table` | `60c8deae579abd86dd18acc7567330b6840d4e9f13c322ec42273cad0642988f` |

### Remaining release work

See the README's open questions. In particular, USB source isolation, 3.3 V
power/thermal headroom, sensor termination and exposure, fuse and surge/EMI
coordination, low-current relay behavior, exact footprints, enclosure geometry,
and mains separation remain unresolved. Product requirements and a reviewed
hardware design must precede promotion of this experiment to a maintained
fabrication target. An unrouted PCB placement was generated; no manufacturing
files were generated.
