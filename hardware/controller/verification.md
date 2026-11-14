# Modular controller study verification

Date: 2026-11-13. Tools: KiCad CLI and pcbnew 9.0.8; pypdf for combined PDFs.

Scope: structural verification of the exploratory exception described in
[README.md](README.md), governed by `MOT-PROC-001` and
[ADR-0011](../../.rqml/adr/0011-single-output-modules-and-sensor-core.md).
No hardware, firmware-control, mains, thermal, ingress, sensor-accuracy or actual
trimming tests occurred. No product implementation or verification is claimed.

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

## Current checked source SHA-256 identities

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
