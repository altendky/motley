# Motley plan

## Reviewed uv dependency update, 2026-11-21

Reviewed `598e342fd533cfaf3855848ae1cc1b66d4ee2886` and the `MOT-HW-003`
show/impact results before refreshing its two tooling baselines. The update
changes only uv 0.13.8 to 0.13.9 in `mise.toml` and the corresponding release
asset URLs and checksums for all five existing `mise.lock` platforms, retaining
their provenance settings. KiCad pins, native hardware, traceability checks and
requirements remain unchanged. This maintains the approved tooling relationship,
with no requirement-intent change or new implementation coverage.

Used `rqml link --refresh` for `E-IMPL-MOT-HW-003-21` and
`E-IMPL-MOT-HW-003-22` only. Standard RQML consistency and the mapped-implementation
approval gate both exited 0 after the refresh.
`mise exec -- pre-commit run --all-files` exited 0, including hardware trace,
firmware metadata, generated SVG and RQML checks. Reviewed SHA-256 values are
`f72986a4096e8245f7339d9c58292c10f8fef214f90c2093ed7085e990cdef17`
for `mise.toml` and
`f32e0653f13de516ac345d752545c6b2aa574eae8d468fa4fa10e9b27bb3adb9`
for `mise.lock`; other source/test inputs remain at the reviewed commit above.
These local checks do not claim a new firmware build or additional platform
execution evidence.

## Multi-drop output ribbon, 2026-11-17

**Readiness:** READY for the reviewed native integration. Kinghelm
KH-2.54PH180-2X3P-L8.9 / C5157626 passed actual Economic assembly matching;
HARTING 09185065813 and 3M 3801/06 form a dimensionally matched prototype
harness pending sample termination/mating. Pin order is logic 5 V, SDA, GND,
SCL, raw actuator 5 V, LINE_SYNC. ADR-0022 records the selected topology and
draft `MOT-HW-016` its interface contract. Continue the existing exploratory
exception; electrical requirements remain draft. Sixteen outputs remains a
soft exploration target, not a qualified population. Issues #59/#62 remain open.

- [x] **Goal:** Select and document the complete multi-drop interconnect.
  **Requirements:** `MOT-AC-009`, `MOT-HW-015`; ADR-0022 and existing six-signal
  power domains. **Files:** `docs/hardware-exact-selections.md`,
  `docs/ac-output-module.md`, `hardware/controller/README.md`. Check exact
  keyed/shrouded 2x3/2.54 mm headers, mid-cable IDC sockets, matching ribbon
  gauge/spacing/insulation and strain relief; establish manufacturer fit and
  actual factory-installation eligibility separately. Specify pin 1 to wire 1
  everywhere; freeze the numbered pin map after ribbon-coupling review.
  **Verification:** review drawings, mating exclusions, contact/wire limits,
  chain current/voltage drop, I2C loading and SYNC fanout; state supported
  lengths/counts or explicit qualification gaps. Do not assume the present
  supply qualifies the preferred sixteen-output capacity.
  **Decision:** keep the existing S2BT protection; use central LP pull-ups
  R42/R43 = 2k2 for calculated two-output rise-time margin, and add one raw
  actuator 5 V bypass capacitor per output tap. Nominal 50 mm spacing needs
  strain-relief/service allowance; 1 m is a conservative screening assumption,
  not a cable rating. Twisted cable and lever terminals remain alternatives;
  they are not required for the initial internal ribbon.
- [x] **Goal:** Integrate the reviewed connector population into native CAD.
  **Requirements:** `MOT-HW-003/013/015`, `MOT-AC-009`, `MOT-CI-004`.
  **Files:** carrier/output root schematics and PCBs, any required local
  footprints/library tables, native review inventories and generated SVGs.
  Convert controller/output bus connectors to the selected interface; add a
  second parallel output header DNP by default. Preserve separate logic/raw
  5 V, all six bus functions, local defaults/protection, mains isolation,
  front assembly and the 100 mm dimension discussion target. Preserve source
  identities wherever possible and allocate both fitted and DNP footprints.
  **Verification:** fresh XML pin-net comparison, DNP/BOM inspection, native
  ERC/DRC and filled-copper/drill/isolation review; render revised SVGs.
- [x] **Goal:** Record observed evidence and remaining wiring limits.
  **Requirements:** `MOT-HW-003/013/015`, `MOT-AC-009`, `MOT-CI-004`.
  **Files:** `hardware/controller/verification.md`, changed design notes and
  issue #62. Run `mise exec -- pre-commit run --all-files` and standard RQML.
  Use `rqml link` for real new native-file applicability relationships and
  implementation links for approved annotation/allocation obligations; refresh
  changed baselines only after review. Keep draft electrical design inputs
  distinct from completed implementation/physical verification. Retain old
  quotes as dated snapshots rather than prices for changed exports.

**Result:** exact source/pin/DNP/BOM comparisons and independent native reviews
pass; both changed boards have zero DRC violations/opens, connected actual
copper and passing drill/plane/isolation screens. One documented 21.96 mm
CUT_EN bridge uses output In2 without adding vias. Eight SVGs regenerate;
sensor sources/views are unchanged. Full pre-commit and standard RQML pass,
exit 0. Reviewed annotation/allocation baselines were refreshed; no draft
electrical requirement was approved or given fabricated verification coverage.
Physical harness and product qualification remain open. See the current
hardware verification and harness records for hashes, assumptions and limits.

## Optional USB header and CC pull-downs, 2026-11-17

**Readiness:** READY for the user's requested normally-unpopulated 0.1-inch
USB interface and DNP CC pull-downs. `MOT-HW-014` records this real design input;
continue the existing exploratory exception with electrical requirements draft.
Approved `MOT-HW-003/013` and `MOT-CI-004` govern trace fields, allocation and
derivatives. Preserve the default USB behavior, power qualification and mains
isolation; keep the existing carrier outline and other boards unchanged.

- [x] Add a labelled six-position 2.54 mm header and separate 5k1/1% CC1/CC2
  pull-down footprints, all DNP. Three copper solder selectors default to PH
  and select VBUS/D+/D- together for the alternate interface. No new purchased
  default components or duplicate pull-downs on the Adafruit assembly.
- [x] Place/reroute only the affected USB area, retaining a continuous LV ground
  reference and disconnected inactive USB branches. Preserve existing UUIDs,
  groups and pin maps except the intentional selector interface; verify the
  contracted default electrical behavior and separate ALT behavior.
- [x] Run native ERC/DRC, actual copper/plane/isolation/drill checks and default/
  ALT connectivity review. Update pin/ESD notes, derivative SVGs and quote-input
  provenance; independently review before refreshing baselines, then run full
  pre-commit and standard RQML. Physical USB/hot-plug qualification remains open.

**Result:** default/ALT connectivity and independent native review pass; native
DRC has zero violations/opens. Full pre-commit and standard RQML pass (exit 0).
The reference centerline screen passes; neighboring header antipads clip parts
of the wider ±0.3 mm margin. Record this limitation and source identities in
`hardware/controller/verification.md`; no USB impedance or operating acceptance
is inferred.

## Assembly-ready exact-part integration, 2026-11-16

**Readiness:** READY for the user's authorization to confirm factory assembly,
integrate exact footprints and obtain updated prices. Continue the exploratory
hardware exception under `MOT-PROC-001`; approved `MOT-HW-003/013` and
`MOT-CI-004` govern native identities, allocations and derivatives. Preserve
electrical connectivity, front assembly, four-layer isolation and dimensions
below the 100 mm discussion target. Keep the retained relay and LOW default;
do not silently claim optional HIGH qualification or completed protection tests.

- [x] Confirm actual PCBA matching for the proposed exact mains terminals,
  holders and headers; distinguish selected factory parts from hand installation.
  Review sensible alternatives and existing fuse/jumper limitations.
- [x] Integrate manufacturer-derived footprints, source fields and corrected
  placement/routing, retaining source UUIDs, pad-net identities and functional
  allocations. Check access, covered component envelopes and hole sizes.
- [x] Compare fresh netlists, native DRC/ERC, copper connectivity, isolation,
  drills and wide mains paths. Inspect revised views and regenerate derivatives;
  independently review before refreshing affected RQML baselines. Run full
  pre-commit and standard RQML; record limits and tested hashes.
- [x] Export revised BOM/CPL/Gerbers and obtain quotation-only JLC pricing.
  Reconcile actual factory-selected references, hand-fitted items and attrition
  for the one/two/five-controller scenarios without double counting parts.

Verification: both boards have zero physical DRC violations/opens; independent
filled-copper, isolation, drill and wide-path audits pass, as do source/pin-net
invariants, full pre-commit and standard RQML. Eight changed SVGs are current;
sensor sources/views are unchanged. Actual Economic prices are $285.26 /
$312.08 / $419.13, with manual positions and stock omissions separated in
`docs/jlcpcb-quote-2026-11-16-exact-parts.md`. This is a checked exploratory
integration and quotation, not electrical/thermal or fabrication qualification.

## Exact mechanical/electrical purchasing selections, 2026-11-16

**Readiness:** SELECTED exact parts for the user's sourcing request.
Continue the existing exploratory hardware exception and approved
`MOT-HW-003/013` annotation/allocation obligations. Preserve circuit behavior,
source identities, front assembly, isolation and the 100 mm board target.

- [x] Inspect the twelve unresolved positions, existing ancillary selections and
  manufacturer drawings. Select actual mains terminals, fuse holder/cartridge
  assemblies, LV harness headers and configuration links; prioritize technical
  fit and current acquisition over retaining an unverified generic footprint.
- [x] Record exact MPNs, source codes and dimensional/electrical evidence.
  Apply confirmed existing-part metadata; preserve accepted current parts and
  keep unfinished qualifications explicit. Fuse and connector drawings expose
  real footprint/access changes, so record their complete integration plan in
  `docs/hardware-exact-selections.md` for the separate manufacturing-cleanup
  work item.
- [x] Independently verify that this pass changes only the documented R25/K1
  identities/relay assignment and J20's discovered LOW-only constraint, with
  unchanged wiring/geometry/SVGs. Refresh reviewed RQML baselines and run full
  pre-commit. Preserve the preceding quote as a dated snapshot rather than a
  price claim for the selected future connector/holder integration.

Verification: independent parsed native-tree comparison passes; all twelve
SVGs are byte-current. Full pre-commit, including annotation/allocation and
standard RQML checks, passes (exit 0). Reviewed native hashes are recorded in
`hardware/controller/verification.md`. Mechanical integration and physical
qualification remain explicit follow-up work.

## JLC-sourceable AC passive revision, 2026-11-16

**Readiness:** VERIFIED the user's authorized update of the circuit and
board from the completed passive review. Continue the existing `MOT-PROC-001`
exploratory hardware exception: electrical requirements remain draft inputs,
not product qualification claims. Approved `MOT-HW-003`, `MOT-HW-013` and
`MOT-CI-004` govern native identity, allocation and generated views. The reviewed
component/value changes are implementation details, not a new architecture.

- [x] **Goal:** Update heater, feedback and line-reference schematics with
  stocked pulse-rated passives, explicit source fields and common-PCB LOW/HIGH
  assembly choices. **Inputs:** `MOT-HW-001/002/003`, `MOT-AC-001/002/003/008/013/014`,
  `hardware/controller/ac-passive-review.md`. Preserve source UUIDs and groups;
  add meaningful annotations for new symbols and retain the off-default path.
- [x] **Goal:** Synchronize output/carrier footprints, repair affected routing
  and preserve external connectors, front assembly, four-layer LV planes and
  the existing isolation boundary. Keep dimensions at most 100 mm. Verify
  changed pad nets against fresh KiCad XML netlists, native DRC/parity,
  connectivity, drills, mains netclasses and unchanged unrelated circuits.
- [x] **Goal:** Refresh affected review/SVG and pin/default inventories,
  record calculations/actual limits separately from qualified behavior, inspect
  changed source before refreshing the existing native `MOT-HW-003` baselines,
  and run allocation/trace checks plus full pre-commit and standard RQML.

Verification: the current section in `hardware/controller/verification.md`
records tested source hashes and observed native/graph checks. Both changed
boards have zero physical/silk violations, opens and drilled-via/SMT-land
intersections; inherited parity/ERC findings remain explicit. All 263 footprints
pass annotation/allocation, full pre-commit and standard RQML pass (exit 0), and
eight derivative SVGs are refreshed. Sensor sources/views are unchanged.
Ignored PDFs are earlier snapshots; assembly eligibility, revised pricing and
physical electrical qualification remain unclaimed.

## Functional component allocation, 2026-11-15

**Readiness:** READY for the developer's accepted grouping proposal, narrowed
to attribution and checks without pricing or a mise task wrapper. `MOT-HW-013`
records the agreed obligation. Preserve `MOT-HW-003` UUID/requirement identity,
`MOT-CI-004` deterministic images and `MOT-PROC-002` backlog-tolerant gates.
The hidden field/catalog names and native parser reuse are implementation
details; no electrical architecture or new ADR is needed.

- [x] Add a versioned functional-group catalog and hidden `FunctionalGroup`
  properties to physical schematic components and PCB footprints. Include
  DNP/excluded-BOM parts, test/touch access and board-only mechanics; preserve
  multi-unit consistency and repeated-sheet identity. Review shared support
  ownership explicitly. Verify native trees differ only by that property.
- [x] Add executable PEP 723 uv scripts for read-only allocation checking and
  regression fixtures. Reject missing/empty/duplicate/unknown/board-inappropriate
  groups and inconsistent multi-unit/source/PCB allocation, with per-instance
  inventory and no prices or external services. Exercise BOM-only symbols too.
- [x] Add pre-commit checks (also executed by existing CI), document direct
  commands and maintenance boundaries, export a real grouped BOM, run trace,
  SVG freshness, fixtures and full pre-commit. Record implementation/test links
  for `MOT-HW-013` and refresh only reviewed affected baselines.

Verification: direct `./scripts/hardware_groups.py` passes for 257 components
in 17 catalog groups. Direct `./scripts/test_hardware_groups.py` passes all 20
fixtures. KiCad 10 BOM export retains valid `FunctionalGroup` fields on all
three roots (88/62/74 BOM quantities; BOM-excluded access and board-only features
remain covered by the 257-component native inventory). All 20 native files were
compared against the starting tree with only the new field removed; no other
structural differences exist. Native requirement annotation checks pass, all
12 SVGs remain byte-current, independent ownership/checker review has no blocking
findings, and full pre-commit including RQML passes (exit 0).

Executed source SHA-256: checker
`26d21622470568f2c8feaba8a258c8deb9fcc3b1aece390099d06f37996d5874`,
fixtures `55965e04dbf3d634ada4e4e7384710c930852d795fe0d52f6d03f97a6627aba6`,
catalog `e3465d8b19788e28359e699bc38d58da3bc128e311511ed5ccdc24bf83251c62`.
No hosted run of the new hooks is claimed before this change is pushed.

## Four-layer ground/power-plane revision, 2026-11-14

**Readiness:** READY for the developer's explicit four-layer/plane request.
ADR-0021 records the stackup and power/reference partition before native edits.
Continue the `MOT-PROC-001` exploratory exception; `MOT-HW-003` governs native
identity/drift and `MOT-CI-004` governs reproducible SVG derivatives. Draft
electrical constraints remain design inputs, not product acceptance claims.

- [x] **Goal:** Convert carrier/output/sensor candidates to four enabled copper
  layers and an explicit nominal-1.6-mm standard stackup. **Files:** three PCBs
  and only necessary project/rule changes. Preserve all 257 identities, local
  pad nets/geometry, front assembly, outlines, external circuits and selected
  mains paths. Extend antenna and sensor kerf copper keepouts to all layers.
- [x] **Goal:** Add connected In1 GND and distinct In2 power regions without
  merging raw/selected/switched/post-link rails. Preserve a continuous actual
  In2 GND reference beneath back-side carrier USB with nearby return ties.
  **Inputs:** ADR-0021, `MOT-HW-004/005/006/009/010/011/012`, `MOT-SENS-005`.
  Inspect filled copper and vertical connections; repair output CUT_EN opens
  and drill/land intersections without changing circuits or load-path widths.
- [x] **Goal:** Independently verify four-layer identity, actual full-board and
  retained-cut connectivity, projected mains isolation, antenna/mount reserves,
  plane rail separation, reference coverage and drilled vias. **Inputs:**
  `MOT-HW-003/004/005/006/007/008`, `MOT-AC-014`. Native DRC must distinguish
  physical/silk/open and inherited parity findings; no diagnostic suppression.
- [x] **Goal:** Add inner-plane SVGs, update current design/review/evidence and
  placement exports, inspect changed source consumers/trace links and refresh
  only reviewed baselines. Run annotation/fixture/freshness checks, full
  pre-commit and standard RQML.

Delivery uses the signed-commit/PR/queue workflow, followed by observing the
merge and updating the ordinary main checkout.

All three converted boards have zero native physical/silk violations, zero
opens and zero drill/land intersections. The output's two preceding CUT_EN
gaps are now closed without inner signal routing. Independent four-layer
connectivity, plane feeds, sensor cuts and current/isolation checks pass.
The former long USB reference gap is gone; local antipad/impedance and physical
manufacturing qualifications remain open. Twelve SVGs and both layout/copper
review PDFs are refreshed. Native annotations, 15 trace fixtures, 11 SVG
fixtures and full pre-commit pass; source identity and execution evidence are
recorded separately from product qualification.

## Carrier and sensor packing/routing study, 2026-11-14

**Readiness:** READY for the developer's request to pack and route both remaining
boards. Extend the `MOT-PROC-001` exploratory CAD exception; approved `MOT-HW-003`
governs native annotation/source identity and `MOT-CI-004` governs SVG freshness.
Electrical obligations remain draft design inputs, not completed qualification.
Use `MOT-HW-004/005/006/007/008/009/010/011/012`, `MOT-SENS-005`, `MOT-PLAT-004`
and the preserved AC/power interfaces as applicable constraints. No schematic,
component selection, firmware or AC-output-board changes are planned.

- [x] Pack the controller/AC-input board below its 100 x 85 mm starting envelope.
  Preserve all footprint identities/nets, front assembly, antenna/cable/metal
  reserve, USB data path, source-selection/regulator groups, accessible service
  interfaces and mains/LV separation. Route mains distribution deliberately,
  then local USB/power and remaining LV. Use explicit provisional isolation and
  conductor rules; do not mistake DRC for a current/insulation/EMI rating.
- [x] Pack the 80 x 44 mm sensor L-shaped board by reducing depth, retaining
  its connector-controlled 80 mm length, common circuit and five/six/seven-port
  cut-down options. Preserve connector orientation, front assembly/top access,
  all upstream interfaces, switch addressing and removable pulls. Route full
  board and independently inspect connectivity after each proposed tail cut;
  keep pads/vias/pours out of kerfs and deliberate trace crossings separated.
- [x] For both candidates, verify exact component UUID/property/pad-net parity,
  mounting/reserve/courtyard geometry, copper DRC, open connections and via/drill
  placement. Aim for zero open nets; prefer a slightly less aggressive packing
  over trapping pins. Record every unresolved routing/DFM finding explicitly.
- [x] Integrate only reviewed board/project/rule changes, regenerate derived
  SVGs and review artifacts, update dimensions and verification evidence, inspect
  source consumers/trace links, refresh only reviewed annotation baselines, and
  run native annotations/fixtures, full pre-commit and standard RQML.

The carrier is 95 x 80 mm and the sensor L is 80 x 40 mm; all 99 / 82 footprint
identities, local pad nets/geometry, front assembly and access are preserved.
Both have zero physical/silk violations, zero opens and zero drill/land hits.
Inherited parity findings remain 49 / 70 (native DRC exit 5). All three sensor
cut graphs and the carrier wide-current/isolation/mount/reserve checks pass.
Six committed SVG views and the placement PDF are refreshed. Native annotations,
15 trace fixtures, 11 SVG fixtures, full pre-commit and standard RQML pass.
USB reference/impedance, RF/enclosure, mains/current/thermal and physical cutting
qualification remain open; the separate output-board routing gaps are unchanged.

## Formatter-style SVG regeneration, 2026-11-14

**Readiness:** READY for the developer's correction to `MOT-CI-004`: local
pre-commit updates derivatives like a formatter; CI retains a read-only check.
Preserve deterministic rendering, isolated temporary CAD copies and unchanged
file handling. Existing requirement/acceptance IDs remain stable.

- [x] Add a formatter mode that regenerates expected images and returns failure
  when it creates or changes any, including a regenerated untracked/deleted SVG.
  Keep manual `--write` and read-only `--check` behavior. Add regression fixtures.
- [x] Switch the local hook to formatter mode. Have CI explicitly run `--check`
  and skip only the formatter hook during its aggregate pre-commit run; preserve
  all existing jobs and other gates. Update source/derivative documentation.
- [x] Exercise real stale and missing SVG correction, hook retry success and
  read-only stale rejection, source/image integrity, fixtures, full pre-commit,
  and standard RQML. Review and refresh only affected trace baselines.

Eleven fixtures and real pre-commit correction/retry tests pass. Scratch-index
tests prove a recreated SVG remains blocked after a staged deletion or intent-
to-add until actually staged. Full pre-commit, explicit read-only freshness and
standard RQML pass (exit 0); CAD and existing SVG bytes remain unchanged.

## Reproducible generated board SVGs, 2026-11-14

**Readiness:** READY for the developer's explicit request, recorded as
`MOT-CI-004`. Keep the native KiCad files authoritative and place the four
configured SVG views in `hardware/controller/generated/board-images/`.
Use a stable title without a timestamp, fixed plot settings and an isolated
default theme. Compare freshly rendered bytes; never retain old image metadata
as a generation input. This is tooling within the existing CI architecture,
with no hardware circuit or routing change.

- [x] Implement a dependency-free `scripts/board_images.py` with explicit write
  and read-only check modes, pinned KiCad validation, normalization and useful
  missing/stale/export-failure diagnostics. Regenerate all views before writing;
  preserve already matching files. Add meaningful failure/determinism fixtures.
- [x] Generate and version the four SVGs in the derivative directory with source
  and command documentation. Add pre-commit freshness and fixture hooks; the
  existing CI Repository checks job already runs these with pinned KiCad.
- [x] Verify repeat generation, independence from local configuration and working
  directory, real stale/missing failure, source immutability, fixtures, full and
  new-file pre-commit, and standard RQML. Review/record implementation and test
  links for `MOT-CI-004`; preserve existing annotation and backlog gates.

All eight fixtures and eight real export/failure cases pass. Full pre-commit
and explicit new-file checks pass (exit 0), including SVG freshness, native
annotations and RQML gates. Check mode preserves source/output bytes and mtimes;
write mode preserves already matching derivatives. The existing output-board
routing/DFM gaps remain separate from this completed tooling capability.

## Output-board packing follow-up, 2026-11-14

**Readiness:** READY for the developer's request to pack the first routed
placement more tightly. Continue the `MOT-PROC-001` exploratory exception and
`MOT-HW-003` annotation integrity; preserve the circuit, 76 footprint identities,
front-side assembly/access, 35 x 29 mm heatsink reserve, LV left/mains right and
both AC connectors at bottom right. Try about 90 x 65 mm, without treating that
trial as a required result or weakening the existing provisional separation.
The preferred maximum remains 100 mm per dimension (`MOT-HW-007/008`).

- [x] **Goal:** Pack the recovery, MCU, driver, sensing and probe groups around
  the isolation boundary and reduce idle margins. **Inputs:** `MOT-HW-003/004/
  005/006/007/008`, `MOT-AC-014`, existing routing review. **Files:** output PCB
  and current review notes. Check package courtyards, mount/heatsink reserves and
  source identity before replacing the previous routed snapshot.
- [ ] **Goal:** Rework routing for the packed placement using the same scoped
  routing approach and provisional geometric rules; preserve load-path widths,
  LV-only ground and the all-layer barrier. Check actual copper, zero open nets,
  source/pad identity and independent review; report any remaining limitation.
- [x] **Goal:** Refresh placement/copper PDFs and current source/check evidence,
  retain the preceding routed trial as historical evidence, and run native trace,
  fixtures, full pre-commit and standard RQML. Refresh only reviewed changed
  annotation baselines. Carrier/sensor sources and schematic circuits stay intact.

The packed placement is 90 x 65 mm, 22% below the preceding 100 x 75 mm trial.
Independent review preserves all 76 footprint identities and pad nets, front
assembly, heatsink/mounting reserves, seven wide mains paths and a 5.16 mm
projected copper gap. The bounded routing pass stops with two `CUT_EN`
connections open; the zero-open-net goal above remains pending. Four actual
via-drill/land intersections also remain DFM work. Ordinary 0.6/0.3 mm LV vias
are now permitted by two project minima; clearance rules and mains vias remain
unchanged. The routing review and verification record distinguish these gaps
from passing native physical DRC and annotation checks.

## Output-board placement and routing experiment, 2026-11-14

**Readiness:** READY for a bounded exploratory pass requested by the developer:
LV on the left, mains on the right, AC input/output together at bottom right.
This extends the scoped `MOT-PROC-001` CAD exception to trial copper routing;
approved `MOT-HW-003` governs native annotations. Electrical requirements remain
draft; these are provisional geometric rules, not an insulation/current rating
or manufacturing release. Preserve the schematic circuit, existing source UUIDs,
front-side assembly/touch/probe access and the 100 mm outline target. Carrier
and sensor sources stay unchanged. Two copper layers are permitted; front-only
assembly does not mean a single copper layer.

- [x] **Goal:** Compact output placement with the agreed connector edges and
  an explicit isolation corridor, heatsink reserve and service access.
  **Inputs:** `MOT-HW-003/004/005/006/007/008`, `MOT-AC-014`, ADR-0020.
  **Files:** output PCB/project, provisional routing rules and review notes.
  Inspect exact isolation-crossing package limits before selecting geometric
  rules; record unresolved package/insulation and thermal limitations.
- [x] **Goal:** Route the mains load path deliberately and make one bounded
  local routing pass over logic/sensing. Preserve schematic connectivity and
  avoid mains copper in the LV region. Review ground returns, protection entry
  paths and current/reference ADC routing. Do not substitute circuit components
  or pursue manufacturing optimization in this pass.
- [x] **Goal:** Run net/pad/UUID/annotation reconciliation, ERC and actual copper
  DRC; inspect rendered copper/placement and refresh review PDFs. Record routed
  versus unresolved connections and every remaining finding without suppressing
  diagnostic categories. Run hardware trace/fixtures, full pre-commit and standard
  RQML; refresh only inspected changed annotation baselines. Report study scope
  and remaining qualification gaps separately from structural results.

The result is 100 x 75 mm, with 525 segments, 34 vias and two LV-only ground
zones. KiCad reports zero physical/copper violations and zero unconnected items;
exit 5 remains solely for 53 inherited parity findings. Independent review
confirms source/pad identity, all seven load/neutral/PE paths through wide trunks
and short package fanouts, front-only assembly and at least 5.16 mm all-layer
horizontal copper separation. Existing output ERC findings remain unchanged.
Trace annotations, all 15 fixtures, full pre-commit and standard RQML pass
(exit 0); the new rules/review files receive an explicit scoped pre-commit run.
Only three native files differ: output PCB/project and the new rules file;
35 other native sources remain byte-identical. Source/PDF identities, mechanical
limitations and pending qualification are recorded in the hardware verification
and output-routing review documents. No firmware or product qualification is
claimed, and no further routing optimization is part of this bounded pass.

## Intelligent-output exploratory schematic and placement revision, 2026-11-14

**Readiness:** Exploratory schematic and movable placement updated at the
developer's request after the requirements discussion. This continues the scoped exploratory CAD
exception under approved `MOT-PROC-001`, with approved `MOT-HW-003` governing
native traceability. Draft electrical inputs remain design inputs, not claims
of complete maintained-product implementation or qualification. Preserve the
three-design partition, two physical output copies, single-sided assembly,
top-side touch/probe access, 100 mm outline target and absence of routing.
The sensor native design is outside the electrical revision.

- [x] **Goal:** Set concrete provisional circuit interfaces before native edits.
  **Inputs:** draft `MOT-AC-001` through `MOT-AC-015`, `MOT-ENG-010`,
  `MOT-STOR-001`, applicable `MOT-HW-*`, proposed ADR-0020. Check actual MCU
  pins, boot modes and storage geometry; choose shared reference, independent
  voltage/current feedback and random-phase optotriac with stated limits.
  **Files:** ADR-0020, output proposal and design review notes. Firmware fit,
  option-byte persistence, detector timing/leakage/heat and mains qualification
  remain explicit open work; higher-current exploration stays in issue #30.
- [x] **Goal:** Revise the controller/output schematics and movable placement.
  **Files:** controller/output native sheets, new control/sensing sheets and
  required library/PCB sources. Replace direct two-channel GPIO links with
  runtime I2C and shared line reference. Separate selected logic power from raw
  actuator power for USB commissioning; retain both controller Qwiic buses and
  review LP power/pull-up domain changes. Add local MCU/regulator, hardware
  recovery, safe bias, watchdog documentation and feedback; keep the Omron
  cutoff, configured snubber and initial 300 W target. Record genuine design-input
  and annotation links using RQML; do not invent product implementation coverage.
- [x] **Goal:** Verify and publish updated review artifacts.
  **Files:** native sources, pin/ESD/verification notes and both combined PDFs.
  **Verification:** fresh netlists and all pad/net/UUID/value/field reconciliation,
  changed-circuit/default/power-domain reviews, ERC/DRC, front-only placement,
  outline and zero-routing checks, unchanged sensor comparison, hardware trace
  checker/fixtures and full pre-commit/RQML. Refresh only reviewed changed native
  annotation baselines. Export and render both PDFs and inspect changed pages.
  Record source hashes, execution results and unresolved electrical limits;
  no purchasing, assembly or energization is part of this experiment.

The structural audit reconciles 247 components / 706 symbol pins and all 257
footprints, including connector/power maps and unchanged sensor sources. All
boards remain front-only and unrouted, with zero physical DRC findings; expected
unrouted/parity findings and the existing PS1 / manufacturer-directed TMCS ERC
findings remain visible. Both combined PDFs were regenerated and rendered for
review: 24 schematic pages and three placement pages. Annotation checks, all 15
trace fixtures, full pre-commit and standard RQML pass (exit 0). Native source
manifest SHA-256: `c9d850e7fb61cad55d144be6fe9e33a76b4b4a5bdf651cc5ca09022f772af6ce`; checked specification:
`ea0a8782859f70d9940ea8996993b5fc8a60fc169862d6c5c1d71987a106d0fc`. Individual source/PDF hashes and open qualification gaps are in
`hardware/controller/verification.md` and `intelligent-output-review.md`.
Coverage backlog remains 36 unimplemented / 43 unverified requirements; no
electrical product completion, firmware fit, recovery execution, watchdog tests,
qualified sixteen-board fanout or mains/thermal/EMC approval is claimed.

## Manual recovery, per-MCU watchdogs and deferred current study, 2026-11-14

**Readiness:** READY for the requested specification/design clarification;
electrical CAD and firmware implementation remain pending. Preserve global
identity tracking and mixed-bus commissioning of one new default-address board.

- [x] **Goal:** Record easy hardware recovery under `MOT-AC-011`, using a marked
  RUN/RECOVERY DIP/jumper plus reset access. **Files:** specification, output
  proposal and proposed ADR-0020. Verify candidate ST ROM immutability, pin/boot
  options and lock limitations; preserve the `MOT-STOR-001` assessment of option
  writes rather than claiming ROM availability proves safe recovery.
- [x] **Goal:** Require watchdog health signals and responses on every MCU in
  draft `MOT-ENG-010`, including progress-based refresh, bounded hardware expiry,
  local off states and the main-ESP/communication-fallback distinction.
  **Files:** specification, output proposal and proposed ADR-0020. Record real
  goal/dependency links without claiming firmware or hardware implementation.
- [x] **Goal:** Create and verify
  [issue #30](https://github.com/altendky/motley/issues/30) for higher-current
  plausibility. **Files:** candidate design inputs and plan notes. Retain the
  initial 300 W target; remove higher-current investigation as a prerequisite
  for initial CAD work. The issue records bottleneck, same-PCB variant and
  incremental-cost questions without selecting a higher rating.
- [ ] **Goal:** Select exact recovery controls, MCU pins and verified boot/reset
  options; define watchdog activation, progress signals, expiry limits and reset
  responses for the ESP and output MCU. **Inputs:** `MOT-AC-011/012/015`,
  `MOT-ENG-010`, `MOT-HW-001/002`, `MOT-STOR-001`, proposed ADR-0020.
  **Files:** later affected native CAD, MCU firmware and verification records.
  **Verification:** corrupt-app jumper/reset recovery, identity-checked loader
  writes with other normal-address boards present, option/power-loss behavior,
  critical-task stall and interrupt-alive watchdog injection, local actuator
  shutdown and configured fallback after ESP loss. Record actual traces then.

Specification validation, strict lint, standard RQML and full pre-commit pass
(exit 0); the untracked ADR and final plan bookkeeping are checked explicitly.
Independent read-only review found no material blockers and confirmed the ROM,
boot-lock and watchdog distinctions. Checked specification SHA-256:
`9ea1a0cc08ed972281cc950a90f80c64b96867a21c8b9495a2c7568406118736`.
There are 47 requirements, with 36 unimplemented and 43 unverified. No CAD,
firmware or reviewed implementation baseline changes and no watchdog/recovery
hardware execution are claimed.

## Output identity and single-board commissioning clarification, 2026-11-14

**Readiness:** READY for this specification/design clarification; electrical CAD
remains pending. The developer requires global identity-based tracking of output
configuration, faults and updates, permits one new board at the selected default
address at a time for initial commissioning, and requests explicit factory/default
address reservations. Already commissioned boards and other boards at
nonconflicting addresses may remain on the same bus; no separate runtime path is
required for them.
No firmware or CAD implementation is added.

- [x] **Goal:** Strengthen draft `MOT-AC-012`, preserve its IDs and add acceptance
  for identity-keyed persistent records, address reuse and explicit replacement
  rebinding. Extend `MOT-AC-011` with shared-bus, single-default-target
  commissioning and UID-checked update/recovery. **Files:** `requirements.rqml`;
  assess `MOT-STOR-001` as a
  dependency without weakening its storage obligations.
- [x] **Goal:** Record mandatory address-plan obligations in draft `MOT-AC-015`
  and connect real goal/dependency edges through RQML. **Files:** specification,
  `docs/ac-output-module.md`, proposed ADR-0020. Research NXP reserved ranges,
  ST C011 loader `0x64`, TI mux range and Sensirion probe addresses. Distinguish
  per-bus conflicts, protocol reservations and unselected application defaults.
- [ ] **Goal:** Implement only after the remaining hardware/interface choices
  are agreed. **Inputs:** `MOT-AC-009/011/012/015`, `MOT-STOR-001`, proposed
  ADR-0020. Select the runtime pool and exact service wiring/loader, verify UID
  readout without a working application, and define identity validation,
  persistence and explicit replacement-role rebinding. **Verification:** later
  exercise factory-blank, corrupt/recovery, address-change, address-reuse,
  ESP-restart and reserved/conflicting-address cases. Include commissioning one
  new default-address board while other boards remain connected at distinct
  addresses; an ACK alone cannot prove that only one device responds at the
  default. Record actual code/tests only then.

Discussion-stage verification: schema validation, strict lint, standard RQML and
full `mise exec -- pre-commit run --all-files` pass (exit 0). The proposed ADR and
final plan bookkeeping are also checked explicitly because the ADR is untracked.
Checked specification SHA-256:
`d0b2f17a1651a7251b5f6de6cc5c47aa100f985508b2a1666dbccfeaa406c3ac`.
There are 46 requirements, with 35 unimplemented and 42 unverified. No
implementation baselines or hardware coverage are changed; no commissioning,
identity or address-allocation code has been executed.

## Intelligent-output requirements and architecture discussion, 2026-11-14

**Readiness:** READY for requirements/design discussion; NOT READY for maintained
electrical CAD implementation. The developer made sixteen outputs negotiable for
cost/difficulty, requested ESP programming including initial commissioning,
preferred stable identity and international AC support, and asked to assess
inexpensive higher-load variants. Inductive-load discussion remains deferred.
These clarify draft `MOT-AC-009` and add draft `MOT-AC-011/012/013/014`; they do
not approve the complete electrical specification or select new hardware.

- [x] **Goal:** Preserve these preferences and the initial 300 W / 120 V target.
  **Files:** `requirements.rqml`, `docs/ac-output-module.md`. Preserve existing
  IDs and record real goal/dependency edges through RQML. Review changed criteria
  rather than treating a priority change as a coverage-only edit.
- [x] **Goal:** Describe the recommended responsibility split and open choices.
  **Files:** proposed ADR-0020 and the output-module proposal. Inspect ST factory
  UID/loader documentation; identify fixed-ROM-address and boot-option issues.
  No firmware, CAD, PDFs or implementation baselines are changed by this work.
- [ ] **Goal:** Select programming and runtime interconnects under
  `MOT-AC-007/009/011/012`, `MOT-STOR-001` and `MOT-HW-001/002/004`.
  **Files:** ADR-0020 and output-module proposal; update requirement parameters
  only after agreement. Compare shared-bus commissioning of one new default-address
  board, recovery selection and ESP-driven SWD, including blank and corrupt targets,
  option bytes, pin availability, storage erase geometry and incremental cost.
  Define bus topology, addressing, wiring length, supported count, power budget
  and sync distribution; assess the ESP LP-I2C block before selecting it.
- [ ] **Goal:** Bound electrical choices under `MOT-AC-001/002/003/004/005/008/010/013/014`.
  **Files:** requirement parameters, architecture and candidate record. Select
  feedback/line-reference circuits and meaningful timing/current thresholds;
  review universal-input variants and the initial 300 W thermal/current path
  before fixing footprints. Higher-current plausibility is deferred to issue #30;
  do not add general inductive-load promises.
- [ ] **Goal:** After agreement, revise and verify native CAD and review PDFs.
  **Files:** affected controller/output sheets, PCBs, libraries, verification
  record and reviews. Follow the requirements-first workflow and native hardware
  traceability; link actual implementation only after it exists. Verify netlist
  parity, pin/default/ESD/insulation reviews, placement, ERC/DRC and the 100 mm
  target, preserving the sensor design and unrouted status unless scope changes.

Discussion-stage verification: schema validation, strict lint, standard RQML and
full repository pre-commit pass (exit 0); the new untracked ADR also passes an
explicit scoped pre-commit run. Independent read-only review found no blockers
and confirmed the loader/address/boot-option limitations. Checked specification
SHA-256: `fd4cb98ba78e2868c53676fbff53af4499ca19203f5c385037e20ad77da0e7c6`.
There are 45 requirements, with 34 unimplemented and 41 unverified; no electrical
implementation or verification coverage is claimed. Hardware/ESP-loader execution
and product qualification remain unperformed.

## KiCad tool pin and native format migration, 2026-11-14

**Readiness:** READY for the developer's request to manage KiCad through mise
and apply native format upgrades. This is tooling maintenance supporting approved
`MOT-HW-003`, under `MOT-PROC-001/002`; the existing electrical study remains an
exploratory exception. Preserve connectivity, UUID identities, requirement fields,
placement, outlines and unrouted status. No product requirement or architectural
decision changes are needed. Shared tooling documentation also retains
`MOT-CI-003`'s report instructions.

- [x] **Goal:** Pin stable KiCad using an official distribution and mise's HTTP
  backend, with a locked checksum. **Files:** `mise.toml`, `mise.lock`,
  `docs/tooling.md` and any necessary launcher/install helper. Explicitly document
  platform support. Record real supporting tool links to `MOT-HW-003`.
- [x] **Goal:** Upgrade native sources using KiCad's own serializers, including
  every child schematic and local library. **Files:** `hardware/controller/`,
  including library tables, README and verification notes. Capture pre-migration
  netlists and structural inventories; inspect native changes and library paths.
  Do not manually bump project schemas or alter electrical design.
- [x] **Goal:** Verify preservation. **Verification:** compare before/after
  connectivity and native identities/geometry, run fresh ERC/DRC, hardware trace
  checker and fixtures, and full `mise exec -- pre-commit run --all-files` plus
  standard RQML. Record commands, results and source hashes; refresh only reviewed
  changed trace baselines. Retain honest coverage and unrouted-board limitations.
  KiCad 10.0.8 installs and runs through mise; all 25 native upgrades exit 0.
  Fresh netlists preserve 193 components / 134 nets and all pin connectivity;
  parsed native comparisons preserve the 203 footprint placements, pad geometry,
  outlines and groups. Native source/test hashes, serializer UUID repairs and
  identical before/after KiCad 10 ERC/DRC findings are recorded in
  `hardware/controller/verification.md`. Four referenced stock STEP models are
  absent from the official bundle; existing symbol/metadata parity differences
  remain documented. Hardware trace and all 15 fixtures, ShellCheck, full
  pre-commit, the new launcher's scoped pre-commit and standard RQML pass
  (exit 0). The first full pre-commit attempt failed only on a protected Mergify
  schema cache; after granting that cache access the full run passed. Reviewed
  implementation baselines were refreshed, and 13 tool/library support links
  were added. Backlog remains 37 unverified / 30 unimplemented requirements,
  with zero unapproved implementations, dangling references or lint findings.

## Human-readable requirements CI artifact, 2026-11-13

**Readiness:** READY for the developer's explicit request to generate the standard
Markdown report and retain it in CI. `MOT-CI-003` records that agreed behavior;
`MOT-PROC-001/002` govern specification-first implementation and honest coverage.
Existing `MOT-CI-001/002` firmware build/publication and `MOT-HW-003` documentation
trace obligations remain intact. The artifact uses the pinned CLI's overview
without a custom renderer. This is an implementation detail requiring no ADR.
The deferred pinout requirement remains separate.

- [x] **Goal:** Generate and retain the checked-out specification's Markdown.
  **Files:** `.github/workflows/ci.yml`, `docs/tooling.md`, `requirements.rqml`.
  Add a small independent report job, validate and render with the pinned CLI,
  reject empty output, upload a commit/run/attempt-named artifact and include the
  job in `all`. Record real implementation links to the job and documentation;
  refresh reviewed shared workflow and documentation baselines.
- [x] **Goal:** Verify report content and publication. **Verification:** Generate
  the report locally, reconcile requirement and acceptance IDs/content with XML,
  inspect Markdown, check empty-file failure, run actionlint and full pre-commit
  including standard RQML. Observe the hosted report job and download its artifact
  using `gh`; compare the downloaded Markdown to the checked-out specification's
  generated report. Record results and actual source/test hashes or commit.
  Local pinned `rqml validate` and `rqml overview requirements.rqml` exit zero;
  ElementTree reconciliation confirms all 41 requirement headers, statuses and
  statements plus all 110 acceptance IDs and given/when/then texts. The generated
  report is 97,017 bytes; `test -s` accepts it and rejects an empty fixture.
  Spec/report SHA-256 values are
  `9e31caca94fa6e56d89423e56617e39cb7b7f72a95d1ff13d696446a1c5d279b` /
  `e54605d6a14bea226abde8b3ebe09850f92808de7639367f01f3a4b969ade956`.
  Actionlint and full pre-commit pass (exit 0). Hosted report job 132332900904
  in run 43557288744 passed in 11 seconds for implementation commit
  `53eb585dd1da5e332258f1d4225ced0230826a85`. Artifact 14098723188 was published
  for test-merge `2e01cc04e1a37bcd7d8b6c937be327af67583f63` while firmware was
  still running. `gh run download` retrieved its Markdown; `gh api` retrieved the
  exact test-merge specification. A fresh pinned overview of that source and
  `cmp` against both the artifact and local report succeeded (exit 0), with the
  source/report hashes above unchanged. This verifies generation, real upload,
  download and report content; unrelated firmware execution remains separate.

## Compiler-aware firmware CI caching, 2026-11-13

**Readiness:** READY under approved `MOT-BUILD-001/002`, `MOT-CI-001/002`
and `MOT-PLAT-001`. ADR-0019 preserves fresh CI outputs and existing identity,
dependency and artifact checks. The separate pinout requirement is deferred.

- [x] **Goal:** Reuse native compiler results and component downloads. **Files:**
  `scripts/firmware.py`, `.github/workflows/ci.yml`, `docs/firmware-build.md`.
  Add explicit cache mounts, bounded IDF ccache, compatible GitHub restore/save
  keys, cache statistics and phase timings; keep build outputs fresh and sources
  read-only/offline during compilation. Refresh reviewed existing implementation
  edges for the runner and workflow; do not claim new requirement coverage.
  Implementation and 33 runner fixtures pass, including a regression preventing
  a symlinked cache root from creating a writable alias of staged sources.
  Actionlint and full pre-commit pass. The actual registry package compiles Matter
  through IDF/CMake with no PCH commands in this configuration; all 1,921 compiler
  calls in the cold run were cacheable. The upstream GN/PCH paths considered in
  ADR-0019 are not the active package build path.
- [x] **Goal:** Establish correctness and measure useful reuse. **Files:**
  `scripts/test_firmware.py` and temporary build evidence. **Verification:**
  runner fixtures, fresh-output cold/warm SDK builds sharing only native caches,
  different commit identity and changed-source/configuration cases, observed
  ccache statistics, full `mise exec -- pre-commit run --all-files` and standard
  RQML. Retain accurate gaps for unexecuted hosted or dependency-change cases.
  Cold `26f239ed600d05b154ca0c754ca8eed988177d26` and warm
  `eab21032052afbdd9c913b6dd0816ee6caa80628` detached study checkouts used the
  modified runner and were correctly identified as dirty. Both had executable
  input fingerprint `35947a54d22fe3c8b83c54d5c7c63a52d583f61f9755cfe68cc40afbf2bb873b`.
  Cold/warm complete runner times were 683.3/151.7 seconds, compilation/linking
  609.6/87.7 seconds, and warm hits 1,916 of 1,921 (99.7%). Both full artifact,
  dependency and embedded-identity checks passed. A third fresh-output run changed
  the application log string and main-task stack default (8192 to 9216); its
  application image contained the new marker, generated sdkconfig held 9216,
  input fingerprint changed to
  `6e4681b956269b8f8802f3b74e5e78ffdf26336b9a6926efb3bd51f42c01fe16`,
  and all artifact checks passed (171.4 seconds, 1,915/1,921 cache hits).
  SDK lock-change runs remain unexecuted; existing lock-mutation rejection
  fixtures pass. Hosted evidence follows below. Temporary receipts and logs live under the owned
  `firmware-cache-study` evidence directory, not in the repository.
  `mise exec -- uv run scripts/test_firmware.py` passed (exit 0, 33 tests) with
  runner SHA-256 `016aadd40f1a8acf3eaa6e6b863c8ec731aee27a7efe99f728d84cda92681faf`
  and fixture SHA-256 `9bcd5228330a16fc00c119ff1fa0c100ad395c9fae4cedfbf700258351bf3824`.
  The SDK study invoked that runner with `MOTLEY_CACHE_DIR=<study>/native-cache`
  and distinct `--build-dir` outputs; full runner exits were zero.
- [x] **Goal:** Qualify hosted disk headroom and isolate SDK pull time.
  **Requirements:** `MOT-CI-001/002`, preserving `MOT-BUILD-001/002` and
  `MOT-PLAT-001`. **Files:** `.github/workflows/ci.yml`, build documentation.
  Hosted run 43549461704 failed with the runner annotation `No space left on
  device`, without build logs or diagnostics artifacts. The local pinned image
  reports 9,606,072,451 bytes for image size. Free only the unused preinstalled host
  Android and .NET SDKs on this disposable firmware runner, print free space,
  and explicitly time the pinned registry pull. Keep Docker archive caching
  unimplemented unless measurement establishes a benefit. Refresh only the two
  reviewed workflow baselines; verify actionlint, full pre-commit/standard RQML,
  and the hosted job's free-space, pull, build and cache-save results.
  Follow-up commit `c4dc76d72ecb47e8a3d3f4b7605a9aa8652a6968` passed full
  pre-commit and hosted run 43550224452, including aggregate `all`. The SDK
  built clean PR test-merge `cfa9598c9c810ab2256114d1d3fe08a1dd76f4dd` and
  passed complete artifact checks. Cleanup raised reported free disk space
  15 GB to 32 GB (63 s); the pull then left 18 GB free. The hosted Docker
  daemon reports image size 5,274,582,696 bytes, distinct from the local report;
  the earlier local value must not be treated as portable unpacked size.
  Pull/configure/cold-compile/verification times were 193.17/43.0/1689.2/7.1 s.
  GitHub saved both caches: compiler 241,472,642 bytes, downloads 22,295,147 bytes.
  All 1,921 cold compiler calls missed. Later hosted warm-cache observations
  belong in the PR validation notes; no warm hosted speedup is inferred here.

## Controller AC/DC module substitution, 2026-11-13

**Readiness:** READY for the developer-approved exploratory substitution of
RECOM RAC05-05SK with MEAN WELL IRM-05-5; retain the Omron G6DN-1A-L DC5.
This is a component implementation detail, not a change to the isolated 5 V,
1 A architecture, so no new ADR or electrical requirement is introduced.
The scoped `MOT-PROC-001` study exception applies. Approved `MOT-HW-003`
governs native trace integrity; draft `MOT-HW-001/004/005/007/008` continue to
govern pin review, access, isolation inputs and the 100 mm size target.

- [x] Replace the power-sheet symbol and carrier footprint with the stock
  IRM-05 family, explicitly remap N/L/-V/+V pins and remove the obsolete NC.
  Preserve stable component/sheet identities and requirements fields.
- [x] Fit the larger module within the existing carrier outline, moving only
  interfering placement groups as needed. Retain front-side parts/touches,
  mains-priority/USB-backup behavior, raw-mains-only output-driver power and
  zero routing. Update current part records and pin/source inventories.
- [x] Independently reconcile every affected pin/net and unchanged circuitry,
  run ERC, physical DRC and native trace checks, regenerate both PDFs and
  inspect changed pages. Refresh only reviewed changed implementation edges;
  run full pre-commit and standard RQML. Record remaining physical/thermal,
  ripple, fuse/inrush and electrical qualification work without claiming tests.
  Independent pad/net and UUID/path checks pass; output/sensor designs remain
  byte-identical. Carrier ERC is clear; physical DRC is zero with the expected
  212 unrouted items and two existing parity warnings. Native annotations and
  all 15 trace fixtures pass. Both PDFs are refreshed and visually reviewed.
  Full pre-commit passed; scoped formatting removed whitespace from the new
  supply symbol, after which its reviewed hash/source inventory was refreshed.
  Ripple, inrush/transfer and thermal/mains qualification remain future work.

## Temporary JLC quotation-only export package, 2026-11-13

**Readiness:** READY for the user-requested preliminary export under the
existing `MOT-PROC-001` exploratory exception. No routing, maintained export
capability, CAD changes, purchases or uploads are introduced by this task.

- [x] Generate separate Gerber/drill ZIPs and BOM/CPL CSVs from each current
  board using a shared origin for copper, drills and positions. Mark exports
  UNROUTED / QUOTATION ONLY and preserve source hashes. Keep generated files
  under ignored `hardware/controller/review/`, with temporary builders outside
  the repository, consistent with the earlier temporary-CSV instruction.
- [x] Match exact known components to catalog IDs, identify quote-only generic
  passive candidates, and keep unresolved/hand-fit items and cost gaps explicit.
  Exclude bare touch/probe/mechanical features from purchased-part assembly.
  State one carrier, one mux and two identical output boards per complete unit.
- [x] Reconcile every fitted component across upload/review/exclusion records,
  match CPL designators/units/sides/positions with BOM and plotted origin, inspect
  actual generated geometry and validate ZIP/CSV parsing. Record assumptions,
  production limitations and observed checks; run repository/RQML checks.
  Generated three Economic top-side SMT quotation jobs: 65 carrier, 16 output
  and 72 mux placements, with matching catalog IDs; 32 non-SMT component records
  per complete unit remain separately priced/hand-fit. Independent review
  reconciled all 608 front-copper pad flashes and 119 drill centers to native
  coordinates, all component dispositions, closed profiles and source hashes.
  CSV/ZIP checks and geometry inspection pass. Full pre-commit, including
  standard RQML, passes (exit 0); existing backlog remains 25 unverified and
  19 unimplemented requirements. No JLC upload, price confirmation, production
  centroid/rotation validation or routing was performed.

## Multiple-mux addressing and chaining, 2026-11-13

**Readiness:** READY for the user-accepted exploratory CAD extension under
`MOT-PROC-001`. Update draft MOT-HW-009/010 and record MOT-HW-011/012 plus future
MOT-SENS-006; ADR-0018 records the design. MOT-HW-001/003/004 and MOT-SENS-005
continue to apply. No firmware implementation or hardware qualification here.

- [x] Specify two carrier Qwiic sockets per bus, two upstream Qwiic and two
  five-pin connectors per mux, three locally biased address switches and
  independent upstream pull-up disconnects. Preserve reset pass-through.
- [x] Update native schematics and sync only affected carrier/sensor PCB groups;
  keep all components/touches on top, no routing, and each board within the
  100 mm target. Reassess sensor common-area width and cut-down variants.
- [x] Reconcile every new pin/contact and existing connectivity, all eight
  address configurations, retained-board geometry, native requirements fields,
  ERC/physical DRC, source hashes and trace links. Regenerate and visually inspect
  both PDFs. Native checks pass for 17 files/203 footprints and 15 fixtures;
  all address/pull configurations pass independent structural checks. ERC is
  clear and physical DRC is zero, retaining expected unrouted/parity findings.
  Full pre-commit/RQML passes; scoped checks cover new untracked files too.
  Only the five reviewed changed native implementation baselines were refreshed.
- [ ] Later implement and test global mux deselection, discovery/configuration,
  shared-reset recovery and sensor-heater scheduling. Qualify combined pull-up,
  capacitance, current/drop, rail-off, ESD and actual deployment/bench chains.

## Optional Qwiic controller and mux bench access, 2026-11-13

**Readiness:** READY for the explicitly requested exploratory CAD extension
under `MOT-PROC-001`. Draft `MOT-HW-009/010` capture the interface request;
ADR-0017 records power/pull-up and supported bench-use choices. Existing
`MOT-HW-001/002/004` and `MOT-SENS-005` remain electrical design inputs;
approved `MOT-HW-003` governs annotations, not electrical qualification.

- [x] Record two independent carrier Qwiic ports, an additional mux upstream
  Qwiic input and retention of the five-pin deployment/reset connection.
- [x] Add a carrier bench sheet: main GPIO19 SDA/18 SCL, LP GPIO6 SDA/7 SCL,
  switched sensor-rail power on both, local 10k/4k7 pull-up pairs respectively,
  removable 0-ohm power links and local bidirectional connector TVSs. Extend
  sensor root with Qwiic/power link; retain local mux pulls/reset and five pins.
- [x] Synchronize only carrier/sensor boards, keep all parts/touch points on
  top, original outlines, sensor three-through-eight-port cuts and zero routing.
- [x] Reconcile pins, power/default/ESD dispositions, native fields/UUIDs and
  netlist parity; inspect changed source, ERC and physical DRC. Regenerate and
  inspect both PDFs, update documentation/source hashes and real trace edges.
  Native checker and all 15 fixtures pass; full and changed-file pre-commit
  pass, including standard RQML and implementation approval checks. ERC is
  clear; physical DRC is zero with expected unrouted/parity findings. Reviewed
  baselines were refreshed only for the five changed linked native sources.
- [ ] Later qualify complete cable rise/LOW margin, LP/reset/off-domain states,
  regulator/USB/combined current budgets, ESD and bench connection procedures.
  No firmware driver or physical hardware test is implemented by this study.

## Top-side handling touch points, 2026-11-13

**Readiness:** READY for the requested top-side touch-pad correction under the
existing `MOT-PROC-001` exploratory exception. Update draft `MOT-HW-005` to
capture top/front access; approved `MOT-HW-003` governs native trace integrity.

- [x] Move sensor TP1 and its LV-GND marking to the front, preserving 8 mm
  exposed copper and space for a finger. Adjust nearby new TVS placements only
  as needed. Keep the outline, three-through-eight-port cuts and zero routing.
- [x] Verify every board's touch point is on top, with unchanged pad nets,
  UUIDs and requirement fields. Run physical DRC and native annotation checks;
  refresh and inspect the placement PDF without the obsolete back-view page.
  update source hashes, the reviewed PCB baseline and documentation.
- [x] Run full and changed-file pre-commit/RQML checks. No physical handling/ESD
  test claimed.

## Sensor front-only component assembly, 2026-11-13

**Readiness:** READY for the user-requested placement correction under the
existing `MOT-PROC-001` exploratory exception and ADR-0016. Preserve circuit,
UUIDs, native requirement fields and zero routing. `MOT-HW-003` governs native
trace integrity; draft `MOT-HW-004/005/006` remain design inputs. Honor the
100 mm size target recorded in draft `MOT-HW-007/008`.

- [x] Move D60/D61 to the front and widen the fixed common area behind three
  connector positions, preserving the 80 x 44 mm envelope and all other parts.
  Keep the bare back-side touch pad; it needs no component assembly.
- [x] Remove the obsolete two-port cut marking and verify retained components
  for every supported three-through-eight-port variant, including kerf allowance.
- [x] Compare native pad nets, UUIDs, fields and unchanged footprint placement
  against a pre-edit snapshot. Run native trace checks and physical DRC; export
  and inspect both PDFs. Refresh only the inspected changed PCB trace baseline
  and current source hashes. Update layout/cost documentation.
- [x] Run complete and changed-file pre-commit checks, including standard RQML.

## Preferred board-size envelope, 2026-11-13

**Readiness:** READY to record the developer's 100 mm target and early-discussion
trigger as draft `MOT-HW-007/008`, under `MOT-PROC-001`. No CAD resize, routing
or automated size gate is introduced by this documentation change.

- [x] **Specify:** distinguish the preferred maximum of 100 mm for each overall
  board dimension from the obligation to discuss an anticipated overrun before
  proceeding. Exactly 100 mm meets the target; larger boards may be agreed.
- [x] **Record scope:** apply to each individual full board outline, including
  the sensor common area, without imposing its aspect ratio or a panel size.
  Current study outlines (100 x 85, 100 x 50 and 80 x 44 mm) meet the target.
- [ ] **Future layout review:** compare proposed full outline dimensions with
  the target during placement and routing planning. Raise expected overruns
  immediately with dimensions, reasons and alternatives; record the agreed
  decision before proceeding with enlargement. Recheck after outline changes.

Files: `requirements.rqml`, this plan, `hardware/controller/README.md` and
`docs/hardware-candidates.md`. Verification: RQML validation/lint/standard check
and repository pre-commit; these check document integrity, not future layout
compliance. Record goal relationships only; no implementation or verification
coverage is claimed for these draft requirements.

## Sensor common-area geometry clarification, 2026-11-13

**Readiness:** READY to record the developer's clarified placement intent under
the existing `MOT-PROC-001` exploratory exception. ADR-0016 supersedes the
two-position core restriction in ADR-0011. No native CAD changes in this stage.

- [x] Record that the connector row sets full board length while the common
  circuitry can trade width along the row against depth behind it; no fixed
  connector count constrains the common area. Update README and candidate record.
- [x] Revisit the common area and place D60/D61 on the front. The corrected
  29 mm-wide leg spans three positions, with the same depth and 80 x 44 mm
  envelope; cuts retain three through eight ports. All other footprint positions
  are preserved. Physical DRC and native field/net checks pass, zero routing is
  retained, and both PDFs were regenerated and inspected. Geometry remains a
  snapshot, not a fixed common-area aspect ratio.

## Native traceability, ESD and service access, 2026-11-12

**Readiness:** READY to implement the user-accepted MOT-HW-003 traceability
approach and exploratory drawing changes under MOT-PROC-001; NOT READY for ESD
or handling qualification. MOT-HW-004/005/006 capture the requested ESD, touch
and economical probe obligations as drafts. ADR-0015 records the boundary.

- [x] **Specify/design:** retain existing requirement IDs; record the native
  traceability requirement and three electrical/access drafts. Read existing
  bias/default/sensor requirements and impacts. User acceptance covers native
  file links plus component/sheet fields, not electrical compliance.
- [x] **Implement traceability:** annotate physical schematic symbols/sheets
  and PCB footprints; add a native UUID/path-based consistency checker and
  negative-case tests. Record real MOT-HW-003 implementation/verification links
  only after observing the checks; use design-input relationships for drafts.
- [x] **ESD/access study:** assess every connector and unused contact, select
  normal-voltage-compatible clamps, preserve command blocking/default states,
  add marked LV-GND touch pads and optional wire-loop test footprints. Keep
  three outlines, sensor cut retention and zero routing; no mains clip points.
- [x] **Verify/export:** ERC, fresh netlists, all-pad field/net/path parity,
  DRC and repeated-placement/cut checks; regenerate both PDFs and visually
  inspect changed pages. Update all-pin/ESD records and source hashes. Run
  checker tests and complete repository checks with exact protected-file grants.
  Native checker: 16 files/173 footprints; 15 fixture tests pass. ERC is clear
  and physical DRC is zero on all three designs, with intentional unrouted
  counts 164/56/150 and the same 2/5/0 footprint warnings. Both PDFs now contain
  20 schematic and four placement pages, including a sensor back view. The
  all-pin inventory is current at 163 components/463 logical pins. Complete
  pre-commit passes; reviewed native/process baseline changes were refreshed
  only after inspecting source and observing the structural checks. Electrical
  qualifications remain open; the traceability test does not establish them.
- [ ] **Qualify later:** ESD exposure levels/pass criteria, residual currents,
  powered-off/partial-contact states, actual clip/touch mechanics and final
  ground/return/shield layout. No test links may imply these have been executed.

## Pin bias and hardware-default review, 2026-11-12

**Readiness:** READY for requirements/design review; NOT READY to claim
defined hardware defaults. Draft `MOT-HW-001` requires a disposition for every
component pin/contact; draft `MOT-HW-002` requires the declared defaults when
drivers are high impedance or absent. The developer requested requirements
planning and an audit of the existing study, not corrective schematic edits.

- [x] **Specify:** record the two requirements and `GOAL-MOT-HARDWARE` in
  `requirements.rqml`, with explicit startup/reset/bootloader/brownout/off,
  internal pulls, partial power, leakage/loading/coupling and removable-contact
  acceptance criteria. Add only real goal links; no implementation/test traces.
- [x] **Audit:** inspect controller, USB/power, output and mux/sensor circuits;
  reconcile all 96 components / 322 symbol pins with dispositions in
  `hardware/controller/pin-bias-review.md`. Record source hashes and distinguish
  paths present from qualified limits. Preserve native CAD and both PDFs.
- [x] **Incremental cost investigation:** identify the missing-ground return
  through the other command's pull-down. Record two blocking diodes per output
  board (four total), resistor substitutions and optional local filters as a
  candidate, approximately $0.10-$0.20 additional components plus $0.01-$0.04
  Economic joint charges per complete unit. Separate any $3.07 new Extended
  type/batch fee. Actual parts, ON-drive/leakage/transient margins and live
  contact sequences remain unqualified; no corrective CAD edits made.
- [x] **Authorized study correction:** the developer accepted the incremental
  protection cost and requested implementation. Extend the existing scoped
  `MOT-PROC-001` exploratory exception to the output blocking/filter/bias
  circuitry, its drive-margin corrections, CUT2 GPIO7-to-GPIO0 and sensor EN
  GPIO20-to-GPIO11 substitutions, board synchronization and both PDFs. Preserve
  the mains stage, snubber, interfaces, three outlines and zero routing. This
  does not approve the full draft `MOT-HW-001/002` wording or claim hardware
  qualification; sensor bus off-domain pulls and physical tests remain open.
  The prototype retains MMBT3904s, uses Basic C81598 blocking diodes, local
  10k/100n B-E networks and 470/150 ohm base resistors. Added parts/joints total
  approximately $0.1304 per complete two-output unit at the recorded prices,
  before attrition/tax/shipping. Existing placements/outlines, mains/snubber
  connectivity and zero routing are preserved; evidence is in the CAD review.
- [ ] **Review:** agree the exact requirement wording and live-unplug/contact
  sequencing scope. The requirements remain draft until developer acceptance.
- [ ] **Remaining design/qualification:** qualify the implemented GPIO11 EN
  and output blocking/bias/filter corrections; resolve PB-02 sensor-domain
  reset pulls, unused input/strap policies and external service/power
  states. Choose actual transistor variants and a bounded disturbance envelope.
  Use guaranteed limits/calculations and receiving-board bias that survives
  disconnection. Record any significant architectural decision separately.
- [ ] **Implement after design agreement:** update the affected schematic,
  board, notes, audit dispositions and both PDFs; map maintained implementation
  only after requirement approval and review. Re-run ERC/netlist/pad parity,
  unrouted DRC, source-diff checks and visual PDF review. No baseline refresh
  or hardware-acceptance claim follows automatically from these checks.
- [ ] **Qualify:** test the agreed startup/reset/ROM/brownout/off and connector/
  jumper states on hardware, including bounded disturbance injection, receiver
  levels, unintended opto/coil drive and rail back-power. Record tested source
  identities, timing/release limits and results; link actual verification only.

## Latest exploratory hardware direction, 2026-11-12

**Readiness:** READY for planning; NOT READY for fabrication. The accepted
[ADR-0014](adr/0014-integrated-controller-and-switched-sensor-supply.md)
supersedes the Feather/internal USB direction in the historical sections below.
Under the existing `MOT-PROC-001` exploratory exception, use WROOM-N8 directly
on the controller board, retain RECOM-priority/USB-backup selection and
RECOM-only output drivers, and feed separate controller and enabled sensor
3.3 V regulators in parallel from selected 5 V. Preserve `MOT-PLAT-004` USB
serial behavior and draft `MOT-SENS-005` startup-readiness intent. Native CAD
and both review PDFs now represent this integrated direction as an unrouted
study, including automatic source selection and host-qualified USB data.
No firmware changes, product implementation traces or baseline refreshes
belong to this exploratory drawing update.

- [x] Record integrated WROOM-N8 (C5366877, Economic assembly listed), omission
  of Feather battery/accessory circuitry, and the separate switched AP2112
  sensor regulator (C51118). Files: ADR-0014, candidate record, CAD README.
- [x] Provisionally select Adafruit 6153 panel USB-C female to six-pin JST-PH
  pigtail; record its built-in CC pull-downs and unshielded 175 mm harness in
  `docs/hardware-candidates.md`; represent its mating header in CAD/PDFs with
  actual harness pin order explicitly pending sample verification/repinning.
- [ ] Revisit the unsatisfied preference for a more robust shielded USB
  assembly, including defined shield/shell termination, data-pair construction,
  strain relief and panel retention. Qualify the provisional harness pinout,
  both plug orientations and USB operation during heater switching; confirm
  sample panel fit before final enclosure/harness selection.
- [x] Make the new schematic inputs concrete for review: WROOM-N8 with local
  Espressif symbol/footprint, reset/boot/UART recovery, TPS2116 priority divider,
  main and sensor AP2112 regulators, sensor EN (now GPIO11 after the bias
  correction) and existing
  five-pin sensor interface. Power the mux/pull-ups from switched 3V3_SENS;
  fit mux R2/R3 at 4k7. Draw TS3USB221ERSER data gating with an independent
  TLV3011BIDBVR raw-VBUS qualifier and USBLC6-2SC6 ESD starting circuit.
- [x] Revise the exploratory controller/interface CAD and grouped placement;
  preserve the single-output module and cuttable sensor geometry. Files:
  controller/sensor sources, local libraries, README, verification record and
  both combined PDFs. Verify ERC, pin/net maps, zero routing, DRC, PDF renders
  and source hashes. These checks do not establish maintained-product coverage.
- [ ] Complete regulator/load/thermal budgets, source-transfer and USB
  current/inrush/suspend analysis, actual harness pin mapping and protection
  qualification. Validate sensor off-state back-power paths and GPIO startup
  sequencing before promoting the exploratory circuit to a buildable design.
- [ ] Qualify source selection and sensor off/on/startup under mains-only,
  USB-only, both and neither; measure heater/radio peaks, voltage drop and
  temperatures, check absence of back-power, then verify ROM flashing and USB
  serial/commissioning on actual hardware. Later sensing firmware must enable
  the rail and meet startup conditions before I2C, under agreed requirements.

Drawing verification is recorded in `hardware/controller/verification.md`.
Independent pin/net review and schematic-to-pad review passed after correcting
the fitted mux pull-up value labels. All three ERC reports have zero findings;
the unrouted carrier/sensor boards have no physical DRC violations. Current
source hashes accompany the checks. The output module and its mains/power
sheet are unchanged. No physical hardware or firmware acceptance follows;
the product backlog remains 13 unverified and seven unimplemented requirements.

## Readiness

### Next milestone: commissionable Matter device and firmware information

**IMPLEMENTING:** the developer approved this milestone on 2026-11-09.
`MOT-PLAT-001`, `MOT-PLAT-004`, and `MOT-INFO-001` are approved;
ADR-0009 records dependency delivery, identity, serial UI, and the explicit
transition from idle-only startup. `MOT-BUILD-001` retains its build/compiler
obligations while application behavior advances to the approved milestone.
The developer confirmed Home Assistant and a working Thread border router are
available. Dependency resolution succeeded with the exact managed release and
its complete lock. SDK compilation and image inspection passed; radio tests,
commissioning, and physical reset verification remain pending.

The development interface is agreed: use USB serial for commissioning-code
output and an explicit factory-reset request. Physical/deployed setup controls
will be defined and implemented in
[deferred issue #15](https://github.com/altendky/motley/issues/15).

- [x] Research the compatible SDK route and standard firmware information path.
- [x] Draft `MOT-PLAT-001`, `MOT-PLAT-004`, and `MOT-INFO-001` with acceptance
  criteria and declared dependencies; propose ADR-0009.
- [x] Review the exact milestone: commission over Thread, read device/firmware
  identity in Home Assistant and through Matter, retain commissioning across a
  power cycle, and deliberately reset for recommissioning.
- [x] Select and pin the dependency delivery/resolution scheme. Candidate
  managed component compatibility matches the current IDF pin; account for the
  runner's read-only sources and offline compile phase. Record generated locks
  and actual resolved inputs rather than treating published compatibility as
  build evidence.
- [x] Resolve the idle-only bootstrap transition, truthful prototype identity
  fields, numeric software version, board/flash configuration, setup-code
  output and explicit reset command details over USB serial before coding those
  behaviors. No physical control is required for this development milestone.
- [ ] Prove the standard firmware string can use the full build identity through
  the supported SDK configuration interface. Verify the transmitted value, not
  only generated configuration or an abbreviated SDK label.
- [ ] Build and test the smallest valid information-focused device model. A
  root-only prototype is a research candidate; Home Assistant source suggests
  registry support but actual controller acceptance and device-model suitability
  remain open. Do not invent sensor readings to populate an endpoint.
- [ ] Exercise actual commissioning with the available Home Assistant/Thread
  environment; independently read Basic Information, compare the firmware
  identity with its receipt, power-cycle and reread, then reset/recommission.
- [ ] Preserve C++23/exceptions/RTTI settings, CI artifacts, full firmware
  identity, and existing accepted behavior through reviewed traces and tests.

`MOT-PLAT-001` retains the historical compatible-stack obligation and its first
acceptance ID. The old board-specific draft is not treated as hardware approval.
Historical `MOT-PLAT-002` and `MOT-PLAT-003` remain reserved for their broader
integration/scope obligations; this foundation does not restore sensing scope.
Implementation traces follow inspected source; hardware acceptance remains
unverified until observed on the target and Home Assistant.

Milestone exclusions for now: sensor measurements, heater/output control, OTA,
extended runtime diagnostics, and product-certification claims.

### Matter integration evidence, 2026-11-09

The source/configuration review preserves C++23, disabled exceptions/RTTI,
full-hash identity, immutable reverification, and separate success/failure
artifacts. The new dependency lock fixes all six registry components and IDF.
Actual managed-component content identities are recorded with each build.
Only endpoint zero is created; capacity three is reserved because the managed
package compiles bridge helpers whose array bounds require spare capacity.
This does not create sensor, bridge, or actuator endpoints.

`mise exec -- uv run scripts/test_firmware.py`: 29 tests passed, exit 0.
They include altered staged inputs, changed locks/dependency content, read-only
mount policy, cached bootstrap configuration removal, and effective Matter
transport/console rejection alongside the existing provenance/artifact fixtures.
A real container probe confirmed `EROFS` when opening both `/project/main/app_main.cpp`
and its `/build/project/main/app_main.cpp` alias for writing; no bytes were changed.
Review identified the writable alias and cached configuration risks before these
fixes. A second review found no further substantive issue.

`mise exec -- pre-commit run --all-files` and explicit checks on the new files
passed, exit 0. The initial sandboxed run encountered read-only tracked agent
configuration and unavailable schema networking; the normal host run passed.
RQML standard checking passes with no drift, dangling refs, premature mappings,
or unimplemented approved requirements. Six engineering requirements remain
unimplemented; twelve requirements have no verification edge. A test edge is
partial evidence and does not establish every acceptance criterion.

The initial SDK compilation exposed example-only Thread configuration macros
and an invalid bridge-helper array bound at capacity one. The corrected
configuration uses explicit native-radio/host/queue settings and capacity three.
The corrected SDK compilation/link and artifact inspection passed, producing
a 1,933,088-byte application (`0x1d7f20`) with 52% of its application partition
free. The static size report records 187,592 bytes of DIRAM used; this is not a
runtime heap/stack budget assessment. Packaging was correctly rejected because
concurrent planning/trace edits changed the checkout during this build. A final
stable-checkout run produces the identified receipt and bundle; rechecking must
use that same checkout state. Upstream Kconfig warnings and an SDK submodule
Git-ownership diagnostic remain visible in the logs.
The firmware has not been flashed or commissioned. The USB board has not yet
appeared on this host; hardware/controller criteria remain unverified.

Reviewed source SHA-256 identities:

| Input | SHA-256 |
| --- | --- |
| `firmware/main/app_main.cpp` | `2b62468f4668d5ffee6c5e5854aa82b3569149d17d40e743b1b979a0799d0578` |
| `firmware/sdkconfig.defaults` | `d12cbc5e07616ffd4e7cf89aeaaaf029c0c4b329e6fcf0f98033c5f20398e55a` |
| `firmware/dependencies.lock` | `483e8cb9c13c9827bba5df97ef44e5e1fb8d495a5ed67def85a77f700ab7e7a2` |
| `scripts/firmware.py` | `e10907a2acfb4df1c71af15f446515ab1d3941b7913f32be4ce1ec2e6c56c8f9` |
| `scripts/test_firmware.py` | `67f928516fb488208809a80e6e254b357ab12dc3442f5a09547f4506fc76a312` |

Older bootstrap trace notes retain their historical observations; ADR-0009 and
this section describe the current behavior and evidence. Reviewed baseline
refreshes accept changed content; they do not execute tests or prove hardware
behavior. The old completed stages below remain historical evidence.

### Requirements-first workflow

**IMPLEMENTED:** the developer permits unfinished requirements and prefers agreed
requirements before maintained implementation, with scoped exceptions while
learning the workflow. `MOT-PROC-001` and `MOT-PROC-002` capture that policy;
ADR-0008 records the supported gate configuration and its review boundaries.

- [x] Update `AGENTS.md` and `docs/tooling.md` with the default review/mapping
  workflow and explicit exceptions; preserve the visible backlog.
- [x] Use standard consistency checking plus an unconditional mapped-approval
  gate in `.pre-commit-config.yaml`, retaining schema validation and strict lint.
- [x] Verify allowed unfinished coverage and rejected drift, invalid specs, and
  premature mapped implementation using disposable fixtures; record evidence,
  trace real policy/configuration artifacts, and run full pre-commit checks.

Policy verification on 2026-11-07 used the pinned RQML CLI, version 0.11.0.
Disposable fixture runner exited 0 after observing:

- Both draft and approved unimplemented/unverified requirements: standard
  `rqml check` exit 0 and approval gate exit 0; optional strict check exit 2.
- Approved linked implementation: standard check exit 0; changing or removing
  that implementation: standard check exit 2.
- Implementation mapped to a draft requirement: standard check exit 0, separate
  `rqml gate --spec <fixture>` exit 2.
- Invalid specification: standard check exit 1.

Fixture setup was corrected for the CLI's empty-trace append handling and the
document-validation exit code before the successful run. Fixtures were removed;
the temporary verification script and log remain available for review. Script
SHA-256: `996d3b9c11a66c7932b07db3422dd1b6e7959eeaf1cdc0ff6bf3bdf3f9b4162a`.
Tested `.pre-commit-config.yaml` SHA-256:
`45293898abe2b170d9c3b0aea4db6384797d965dc94e061824ccba7333883fba`.
Reviewed `AGENTS.md` SHA-256:
`fe72cb1bbb9d9155d13dba8585dddd86e66b232b60f9b8146c148f200a21525d`.

The current nine files under `firmware/` and `scripts/` all have implementation
or verification mappings to the relevant build/CI requirements. This inventory
supports source review; it is not a behavioral reverse-coverage guarantee.
The new approval hook examines the entire declared mapping, not just changed
paths. Unlinked implementation remains a review responsibility.

`mise exec -- pre-commit run --all-files` passed, exit 0, including metadata tests,
schema validation, strict semantic lint, standard consistency, and approval gate.
RQML standard check also passed with no drift or premature implementation.
Coverage gaps remain visible through status/matrix, including pending hosted CI
verification and six draft engineering requirements. Prior strict failures below
are historical evidence under the previous completeness policy.

**COMPLETE: minimal cross-build milestone (`MOT-BUILD-001`).**

The developer requested an idle-task build before functional design.
`MOT-BUILD-001` is approved and ADR-0004 records its implementation approach.
The application behavior below remains planning work beyond this bootstrap.

`MOT-ENG-004` and `MOT-ENG-005` capture the agreed portable-core direction;
`MOT-ENG-006` captures the agreed typed-result policy for recoverable failures.
`MOT-ENG-007` captures exceptions-disabled production code and dependency
compatibility checks. `MOT-ENG-008` and `MOT-ENG-009` capture bounded memory
and hard-failure handling for detected memory faults.
Their detailed acceptance criteria are draft. The approved bootstrap does not
claim to implement or verify those broader requirements.

The proposed scope, artifact boundaries, and open decisions are in
[the project planning brief](../docs/project-planning.md).

## Build identity and artifact stage

### Size-limited standard-field clarification

The developer permits abbreviated hashes in constrained standard fields when
the full hash remains present and available. ADR-0007 supersedes ADR-0006's
neutral SDK label; the verified full custom descriptor is preserved.

- [x] Restore a useful abbreviated SDK version label and inspect it against
  full identity; keep receipt identity, artifact names, and output full-length.
- [x] Test constrained labels and shared prefixes, build, reverify, refresh
  reviewed traces, and run required pre-commit checks.

Verification on 2026-11-07: 23 tests passed, exit 0, including the SDK field's
31-character payload bound and shared-prefix labels remaining distinguishable
through full identities. The SDK build check passed, exit 0, using an incremental
cache copied from the prior successful build. `--verify-only` passed, exit 0,
before this documentation/trace update and preserved receipt SHA-256
`a4b64feca91e5971655ff121a3a652ee2640144ab4dcd7253990a36c20c71205`.
The SDK label is `g3b28ebbba0f8-dirty`; full identity
`g3b28ebbba0f809f309db964c0e7e08506eeccc66-dirty` remains verified in both ELF
and image, and remains the receipt/artifact identity.

Input fingerprint: `f8747e121d9d3b002f5600ee9e4e0f3d4c634c558a71f3d54609ac415da8c7ac`.
Test source SHA-256: `e1f3f3e54d07a55bc05cb45f73547a37e303b54284be07ee175ec8dd2a91fe9d`.
Implementation hashes are preserved in the reviewed trace baselines and receipt.
RQML standard check passes; full pre-commit retains the same strict coverage gaps
for pending hosted CI verification and the six draft engineering requirements.

### Full-hash correction

The developer requires full commit hashes throughout build identities and
artifact names. `MOT-BUILD-002` and `MOT-CI-002` retain their IDs with corrected
acceptance. ADR-0006 supersedes ADR-0005's abbreviated identity design.

- [x] Use the complete Git hash in all build identities and artifact names.
- [x] Embed a retained custom description containing full hash/cleanliness;
  keep the SDK's size-limited version field neutral, with no abbreviated hash.
- [x] Test hashes sharing a prefix and reject truncated/missing/malformed records;
  run the SDK build and reverification against ELF and binary output.
- [x] Record current evidence, review affected trace links, and run pre-commit.

Full-hash verification on 2026-11-07 supersedes the abbreviated-identity evidence
below. `mise exec -- uv run scripts/test_firmware.py` passed 23 tests, exit 0.
The SDK build check passed, exit 0, after correcting a generated-header template
path exposed by SDK component scanning. The allocated ELF descriptor and
application image both contain
`g3b28ebbba0f809f309db964c0e7e08506eeccc66-dirty` without truncation. The linker
map retains `motley_build_identity` as a 73-byte custom descriptor. `app_main`
still only suspends. SDK version metadata uses `see-build-identity`.

`mise exec -- uv run scripts/firmware.py --build-dir <output> --verify-only`
passed, exit 0, before this documentation/trace update, preserving the version-3
receipt SHA-256 `267f39369eba36455f108b3b6f49468e08511560b376f576e38e69620591e967`.
Input fingerprint:
`2ebe172a6ba59a840235ec56b7663978c7002b0ce53fe15409d6565ca6913d47`.
Application image: 126,304 bytes, SHA-256
`0f9d18971bbaae2afd269a6758ec2ceb7a4e24bc66ecd0b5bbc94d1b56fe5703`.
Test source SHA-256:
`191563cd15615043d934a17d1b9bdced391497d7b83587fed471684ba54b82c8`.
The receipt and refreshed implementation baselines record current input hashes.
Hosted CI and hardware verification remain pending. The known strict coverage
gaps below are preserved; no verification links are fabricated for them.

**IMPLEMENTED AND LOCALLY VERIFIED; hosted CI execution pending.** The developer
approved the proposed identity fields and artifact set. ADR-0005 records the
design. `MOT-BUILD-001` behavior and existing draft engineering requirements are
preserved.

- [x] Implement metadata snapshot, CI checkout classification, immutable
  receipts, embedded version, and curated bundle (`MOT-BUILD-002`).
  Files: `scripts/build_metadata.py`, `scripts/firmware.py`,
  `firmware/CMakeLists.txt`, `docs/firmware-build.md`.
- [x] Maintain the same local/CI firmware check and add verified bundle and
  failed-diagnostic uploads (`MOT-CI-001`, `MOT-CI-002`).
  Files: `.github/workflows/ci.yml`, `.pre-commit-config.yaml`.
- [x] Run meaningful metadata/provenance failure fixtures, fresh cross-build,
  image-version and bundle inspection, and receipt reverification.
  Files: `scripts/test_firmware.py`; command: `mise exec -- uv run scripts/test_firmware.py`.
- [x] Record reviewed implementation/verification links and hashes and run full
  pre-commit checks. Preserve the known strict-coverage findings below.
- [ ] Observe a hosted CI build, aggregate failure handling, artifact upload,
  and download before recording verification links for `MOT-CI-001` and
  `MOT-CI-002`. No service execution evidence is claimed by local checks.

### Identity/artifact verification, 2026-11-07

- `mise exec -- uv run scripts/test_firmware.py`: exit 0, 20 tests. Fixtures
  cover actual Git identity/branch state, staged/unstaged/untracked/ignored/output
  handling, input fingerprints, ancestor/missing-object results, fork PR context,
  PR head versus merge/queue evidence, bad compiler/configuration/image identity,
  malformed or mismatched flash arguments, bundle corruption/missing files,
  source changes invalidating prior success, and immutable receipt reverification.
  Temporary Git clones reuse the existing full local history; no commits created.
- `MOTLEY_BUILD_DIR=<fresh-output-directory> mise exec -- pre-commit run --hook-stage manual firmware-build --all-files`:
  exit 0 from an empty output directory using the pinned SDK. The embedded and
  inspected version is `g3b28ebbba0f8-dirty`, branch `planning/project`.
- `mise exec -- uv run scripts/firmware.py --build-dir <same-output-directory> --verify-only`:
  exit 0; original receipt SHA-256 remained
  `c4971a5dd2c9febc75584fc01c390cb3bd21f34878f943b1430d4edb8f374b9a`.
  This check ran against the checkout snapshot recorded in that receipt, before
  this subsequent documentation update.
- Versioned receipt input fingerprint:
  `102904451bf821fd3d7c9400e3c78000b66be108e454aaa4e5de75f4980b6b3a`.
  Application image: 126,224 bytes, SHA-256
  `ee532153c3aca79d98826b6fa7682205733ea482163421c798f70b9c7900f48a`.
  The receipt contains every bundled file's size/hash and all tested input hashes.
- Read-only review found unvalidated plain-text flash arguments. The final
  verifier checks their options and offset/path mappings against JSON metadata;
  negative fixtures and the final actual SDK build exercise this fix.
- Local workflow syntax validation passed. The upload action is pinned to a
  reviewed published revision. Hosted upload/download and hardware execution
  remain untested; no verification edges were fabricated for those outcomes.
- RQML standard check passes with no drift, changed context, premature
  implementations, or missing approved implementations. Full pre-commit exits 1
  because inner strict `rqml-check` exits 2: `MOT-CI-001` and `MOT-CI-002` have no
  verification edge, and `MOT-ENG-004` through `MOT-ENG-009` still lack implementation
  and verification. Other observed hooks pass.

| Tested artifact | SHA-256 |
| --- | --- |
| `scripts/firmware.py` | `f709e7057ce967168b3aba55a201bffe98756c314676816411d8b1bfc9255255` |
| `scripts/build_metadata.py` | `ea0b850eb050d9fd4f885f9e977bf2afe404a8f311e73f0910f73bd7d786e21e` |
| `scripts/test_firmware.py` | `180d31fbdb00d1abce0a86ced7a274a629f807f7ff7428ae2082e6ef33ce9edb` |
| `.github/workflows/ci.yml` | `23920c809f31146e629c5206f3fd84df15c047f42487f0517f93e48983c6e888` |

## Completed bootstrap stage

- [x] Specify and approve the requested idle-task build as `MOT-BUILD-001`.
- [x] Record the pinned SDK-container approach in ADR-0004.
- [x] Create the minimal firmware target.
  - Goal: an ESP32-C6 C++ application whose existing SDK main task suspends.
  - Requirements: `MOT-BUILD-001`; apply the agreed engineering direction without
    claiming completion of the draft core/fault requirements.
  - Files: `firmware/CMakeLists.txt`, `firmware/main/CMakeLists.txt`,
    `firmware/main/app_main.cpp`, `firmware/sdkconfig.defaults`,
    `firmware/toolchain.toml`.
- [x] Add a repeatable build and artifact check.
  - Files: `scripts/firmware.py`, `.pre-commit-config.yaml`,
    `.github/workflows/ci.yml`, `docs/firmware-build.md`.
  - Verification: a clean `firmware-build` pre-commit manual hook, effective
    C++ flags, target metadata, ELF/image inspection, SDK size report, and
    rejection of invalid/missing artifacts.
  - Record real `implements` links to the firmware/build configuration and
    `verifiedBy` to the artifact verification function after observing execution.
- [x] Run a clean build, inspect outputs, review the diff, and record evidence.
  - Command: `MOTLEY_BUILD_DIR=<fresh-output-directory> mise exec -- pre-commit run --hook-stage manual firmware-build --all-files`.
  - Finish with full pre-commit checks and report remaining draft-requirement
    coverage gaps. Hardware execution remains untested until a board is used.

## Planning work

- [x] Inspect the maintained specification and distinguish it from historical
  planning research.
- [x] Document proposed ownership of requirements, architectural decisions,
  implementation plans, explanations, and executable configuration.
- [x] Agree the first application direction: temperature/humidity measurements
  exposed to Home Assistant through Matter over Thread.
- [x] Recover the original Codex hardware and engineering discussion and
  distinguish user choices, tentative counts, agent proposals, and later
  tooling-only specification cleanup in the planning brief.
- [x] Agree host-testability and an explicit core/environment boundary as
  requirements; draft `MOT-ENG-004` and `MOT-ENG-005` with acceptance criteria.
- [x] Propose the supporting core/adapters architecture in ADR-0001.

## Active software planning

- [x] Develop a concrete code/build/dependency/test-tooling proposal in ADR-0002
  and check basic host C++23 compiler and sanitizer availability.
- [x] Agree typed results for recoverable failures, with `std::expected`, typed
  errors, `[[nodiscard]]`, and diagnostics for unacknowledged discarded results;
  draft `MOT-ENG-006` and update the tooling rationale.
- [x] Agree exceptions-disabled production code, compatible dependency use,
  and separation from host test-framework exceptions; draft `MOT-ENG-007`.
- [x] Agree static/stack preference, limited bounded allocation, and hard
  failures for detected memory faults; draft `MOT-ENG-008` and `MOT-ENG-009`.
- [x] Verify documented ESP32-C6 watchdog availability and propose memory/fault
  supervision in ADR-0003, keeping reset policy and timeouts undecided.
- [x] Record RTTI disabled as the intended default, revisitable for a concrete
  library or design need.
- [ ] Settle ADR-0002's remaining tooling choices, then turn them into
  executable configuration.
- [ ] Define numerical memory budgets and settle ADR-0003's fatal diagnostics,
  panic/reset behavior, watchdog progress criteria, and timing from bounded work.
- [ ] Review the precise statements and acceptance criteria of `MOT-ENG-004`,
  `MOT-ENG-005`, `MOT-ENG-006`, `MOT-ENG-007`, `MOT-ENG-008`, and `MOT-ENG-009`,
  then record their lifecycle approval when agreed.
- [ ] Settle ADR-0001, including application-core, runtime, and adapter
  responsibilities.
- [ ] Select the firmware dependency route and compatible SDK release set.
  Native ESP-IDF with the managed esp-matter component is the initial candidate;
  compare full-source delivery when required tooling or modifications warrant it.
- [ ] Select the host C++ language level, build/test tools, dependency locking,
  and compiler checks against that SDK set.
- [ ] Record the tooling decision and an executable first implementation stage
  with real build/test commands once these choices are settled.
- [ ] Add architecture and developer setup documentation when there is an
  implemented architecture and exercised setup to describe.

The current discussion prioritizes code and project tooling. Configuration and
measurement-state behavior are subsequent requirements work, not the next
tool-selection decision. ADR-0002 proposes tool ownership and build structure;
it is not an accepted implementation plan.

## Deferred and remaining planning

- [ ] Specify the first core behavior and its success/failure scenarios before
  implementing it. Sensing/configuration behavior is the candidate; heater
  regulation remains a separate scope decision.
- [ ] Discuss the physical application and hardware before fixing sensors,
  channel counts, or the controller board.
- [ ] Agree the first device's success/failure scenarios and exclusions.
- [ ] Draft its goals and focused requirements with acceptance criteria;
  review them with the developer and record approval only when given.
- [ ] Agree the engineering constraints that apply across the first milestone.
- [ ] Evaluate the firmware and host-test toolchain against that scope, including
  dependency management, reproducibility, and actual host prerequisites.
- [ ] Record significant design choices as ADRs tied to the relevant requirements.
- [ ] Replace this readiness outline with scoped implementation stages once the
  specification and design are sufficient.

## Verification state

The engineering requirements remain unimplemented and unverified. The separate
minimal-build requirement has real implementation links and an executed artifact
verification link. No hardware or host product behavior tests have run. Preserve
the missing draft engineering implementation/test findings; do not add placeholder
links to satisfy the strict completion check.

### Minimal build evidence, 2026-11-07

- `MOTLEY_BUILD_DIR=<fresh-output-directory> mise exec -- pre-commit run --hook-stage manual firmware-build --all-files`: exit 0. Built from an empty output directory with the SDK pin in `firmware/toolchain.toml`.
- `mise exec -- uv run scripts/firmware.py --build-dir <same-output-directory> --verify-only`: exit 0. The original receipt matched current source, verifier, SDK, compiler/configuration metadata, and artifact hashes.
- `AC-MOT-BUILD-001-01`: produced application ELF (3,120,416 bytes), application image (126,224 bytes), bootloader image (22,192 bytes), and partition table (3,072 bytes). ELF size includes debug information.
- `AC-MOT-BUILD-001-02`: reviewed `app_main`: it loops only on `vTaskSuspend(nullptr)` in the SDK-created application task. Effective owned-source flags select C++23, exceptions off, and RTTI off; generated SDK configuration also disables exceptions and RTTI. SDK headers use GNU extensions, so this platform stub uses `-Wall -Wextra -Werror` without `-Wpedantic`; the portable-core diagnostics remain a later decision.
- `AC-MOT-BUILD-001-03`: executed `scripts/firmware.py#verify_artifacts`; checked target metadata, compile command, SDK configuration, little-endian RISC-V ELF, and both images through SDK esptool inspection. Application image inspection identified ESP32-C6 and valid checksum/hash.
- Disposable negative fixtures: eight checks exited 0 after confirming rejection of missing/empty images, invalid ELF, wrong target, wrong C++ mode, enabled exceptions, enabled RTTI, and invalid SDK configuration. A separate CLI fixture confirmed stale source provenance exits 1 and preserves the original receipt. Fixtures were removed.
- Initial attempts exposed an unsupported IDF parallelism option, GNU extensions in SDK headers under pedantic diagnostics, and a different SDK metadata key. These were corrected before the clean successful run.
- Read-only review found a stale-provenance risk in `--verify-only`; it now requires a matching original receipt and never rewrites it. Build input changes during execution also cause failure.
- Added the same hook to CI and validated its workflow syntax locally. The hosted CI job has not been run here. Board boot and task execution remain untested.
- Final RQML standard check: pass, with no drift, context changes, or uncovered approved requirements. Strict check: fail only for missing implementation/verification of `MOT-ENG-004` through `MOT-ENG-009`.
- Final `mise exec -- pre-commit run --all-files`: exit 1; all other hooks passed, and inner `rqml-check` exited 2 for those six draft coverage gaps. A separate run covering all untracked files had the same result; their formatting/JSON/TOML checks passed.

Tested source/configuration hashes are preserved in the reviewed
`.rqml/baseline.json` implementation-link entries. The verifier's SHA-256 at
execution was `3cd273013e04a50811ce848b4c630b36006df43543dd6b0dabbcf13be5ac3df4`.
The generated receipt additionally records the effective compiler command,
SDK identity, input hashes, generated configuration hash, and output hashes.

| Output | SHA-256 |
| --- | --- |
| Application ELF | `0a1ca7ec3e7b22b5bab79b62782e5f7763ea5e0b3dbd9b53ff4bd8143da18e7c` |
| Application image | `059c73f5b0d4baee786f28b8edef54cbc240741a2c18d8309e7d9ee4d690304a` |
| Bootloader image | `0d1631ac50989e6eca3b3c30979514a7f3ea26b8a28d259a11a5b2468925b084` |
| Partition table | `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820` |

### Earlier planning-only checks

Structural verification on 2026-11-07 covered `MOT-ENG-004`, `MOT-ENG-005`,
`MOT-ENG-006`, `MOT-ENG-007`, `MOT-ENG-008`, `MOT-ENG-009`, their acceptance
criteria, and their declared goal links. Checked specification SHA-256:
`2c15226333fb990c7d140680090a80754bef9113cfaece6de4949a5974a2c33e`.
There are no tested implementation or product-test hashes to record.

ADR-0002 records a separate temporary tooling probe: host GCC/Clang configure,
build, and CTest runs exited 0. The sanitized Clang run initially exited 8 at
CTest because LeakSanitizer was blocked by sandbox process-inspection limits;
the same instrumented build passed outside the sandbox, exit 0. This is tooling
availability evidence, not product verification or requirement implementation.

| Check | Observed result |
| --- | --- |
| RQML MCP validation with the specification path | Valid; no diagnostics |
| Pre-commit RQML validation and strict lint hooks | Exit 0 |
| RQML MCP check, standard strictness | Pass; missing implementation and verification remain reported |
| RQML MCP check, strict strictness | Fail: the current engineering requirements lack implementation and verification links |
| `mise exec -- pre-commit run --all-files` | Exit 1; inner strict `rqml-check` exits 2 for missing implementation and verification links; other hooks pass |
| Pre-commit on the changed planning documents and specification | Exit 1 for the same strict coverage findings; formatting, validation, and lint pass |

## Implementation-plan entry criteria

Each implementation stage will identify its goal, approved requirement IDs,
relevant ADRs, files to create or change, verification commands, and real trace
edges to record after implementation. Do not invent IDs, file layouts, commands,
or completed verification to fill those fields before the decisions are made.

Plan build and host-test evidence separately from physical-device verification.
Keep hardware-dependent acceptance pending until exercised. Preserve completed
stages when updating the implementation plan.

## Exploratory three-board CAD revision, 2026-11-12

**Readiness:** READY for the scoped unrouted drawing experiment; NOT READY for
routing, fabrication or mains use. [ADR-0010](adr/0010-three-board-controller-study.md)
records the developer's partition. `MOT-PROC-001` governs the exception; draft
`MOT-SENS-005` is not implemented or approved by CAD work. Firmware stages above
are unchanged. No product implementation or verification edges will be added for
this experiment.

- [x] Record three physical boards: Feather/AC input and supply, both AC outputs,
  and mux with the trimmable L-shaped sensor-connector bank.
- [x] Split the schematic and unrouted PCB into per-board projects under
  `hardware/controller/`, preserving `heater-channel.kicad_sch` and
  `sensor-port.kicad_sch` as canonical shared definitions. Add explicit matching
  low-voltage and mains inter-board connections.
- [x] Arrange the L-shaped sensor board with fixed mux/interface core, same-edge
  connectors and seven cutting lanes; preserve per-port placement areas. Keep
  all routing absent. Document future routing and trimming qualifications.
- [x] Verify per-board ERC, netlists, schematic parity, footprint pad/net mapping,
  original circuit reconstruction through the interfaces, shared instance
  isolation, repeated geometry, board outlines and core/port retention for all
  seven cuts. Export and visually inspect schematic/placement PDFs.
- [x] Update `hardware/controller/README.md`, `verification.md` and
  `docs/hardware-candidates.md`; run `mise exec -- pre-commit run --all-files`,
  explicit checks of untracked hardware files, and standard RQML check. Record
  actual results and unresolved provisional footprint/mains/thermal limitations.

Execution evidence is in [hardware verification](../hardware/controller/verification.md).
All per-board ERC and geometry/connectivity checks passed; DRC retains only the
documented unrouted connections and twelve existing footprint-assignment warnings.
Standard RQML and pre-commit on all 26 changed/new files passed. The required
aggregate all-files run was attempted but cannot complete the end-of-file fixer
on protected unrelated configuration in this sandbox; its broader write request
was rejected automatically. The other initially restricted hooks passed in
scoped reruns. No product verification or fabrication readiness is inferred.

## Exploratory output-module and sensor-length revision, 2026-11-12

**Readiness:** READY for the unrouted drawing experiment; NOT READY for routing,
fabrication or mains use. [ADR-0011](adr/0011-single-output-modules-and-sensor-core.md)
records the developer's clarification. `MOT-PROC-001` governs the same exception;
firmware requirements, source and traces remain unchanged. Earlier completed
stages above describe the preceding CAD revision.

- [x] Record three designs / four physical boards: one carrier, two copies of a
  single-output module, and one sensor board with its core behind the row.
- [x] Revise carrier and AC-output schematics/PCBs, preserving the canonical
  heater circuit. Give each module copy a four-signal control connection and
  separate mains feed from the carrier. Verify two-copy assembly reconstruction.
- [x] Shorten the L-board to connector-controlled length; retain a compact core
  behind the first two positions and verify all remaining tail-cut variants.
- [x] Regenerate both combined PDFs from all three designs; verify page counts,
  bookmarks, circuit/placement rendering, per-board ERC/DRC and zero routing.
- [x] Update README, candidate record and current verification evidence; run
  applicable pre-commit and standard RQML checks. Preserve known qualification
  gaps and the existing aggregate-hook sandbox limitation explicitly.

Current evidence: one 100 x 85 mm carrier, two copies of the same 100 x 50 mm
single-output module, and an 80 x 44 mm sensor board. The mux/core fits entirely
behind the first two positions; six tail cuts preserve two through seven port
positions. Both independent assembly audits reconstruct all 70 original parts,
228 pin entries and 75 net groups. ERC passes; DRC retains only unrouted nets and
seven provisional footprint warnings across three designs. Combined schematic
and placement PDFs have 16 and three pages respectively, with board bookmarks.
Standard RQML and pre-commit on all 27 changed/new files pass; the existing
aggregate formatter sandbox limitation is unchanged.

## Exploratory manual snubber configuration, 2026-11-12

**Readiness:** READY for the requested placeholder; NOT READY for fabrication
or mains use. This is an implementation detail within the existing
`MOT-PROC-001` exploratory exception, not a new maintained hardware capability
or a change to ADR-0011's board partition. No product traces will be added.

- [x] Fit the provisional 100 Ohm / 10 nF X2 snubber parts and insert a 2x2
  header in series with that branch on the canonical output module. Tie pins
  1/3 to the capacitor side and 2/4 to triac A1. Two closed-top shunts across
  1-2 and 3-4 enable the branch; rotating both across 1-3 and 2-4 disables it
  while covering every pin. Default assembly is ON. Record two shunts per
  module as assembly accessories, with no extra GPIO or interface change.
- [x] Update the unrouted output placement, assembly/orientation labels,
  README and candidate record. Keep header geometry, compatible short pin
  length, shunt fit, voltage/transient ratings and mains spacing unqualified.
  Configuration is only changed unplugged and discharged; coverage does not
  establish a touch-safe rating.
- [x] Verify ERC, every footprint pad/net and DNP state, ON/OFF connectivity,
  preservation of the rest of the circuit, zero routing and physical DRC.
  Refresh both combined PDFs, render changed pages, update verification
  evidence and run applicable pre-commit plus standard RQML checks.

## Historical automatic USB power and enclosure-port plan, 2026-11-12

Superseded by ADR-0014 and the integrated-controller drawing update above.

**Readiness:** READY for planning under the `MOT-PROC-001` exploratory exception;
NOT READY for schematic implementation until the remaining electrical/harness
choices below are resolved. [ADR-0012](adr/0012-automatic-usb-power-and-panel-port.md)
records the original planning direction; [ADR-0013](adr/0013-usb-c-internal-feather-connection.md)
replaces its internal A connection with USB-C and withdraws the old cost total.
Preserve
`MOT-PLAT-004`'s development USB serial interface; no firmware or product traces
are added by this plan. At that stage the CAD/PDFs still contained manual JP1.

- [x] Record RECOM priority, optional USB backup, return-to-RECOM behavior,
  unmodified Feather, panel USB-C and separate RECOM-only output-driver power.
- [x] Research panel/harness candidates, power mux and host-VBUS data gating;
  record checked prices, mounting assumptions and validation gaps in ADR-0012
  and `docs/hardware-candidates.md`. Update the CAD README's future-plan note.
- [ ] **Resolve design inputs.** Confirm the Adafruit 6069's data/CC mapping in
  every plug orientation, exact mounting drawing/sample, shielding and cable
  bend space. Select a short data-capable C-to-C cable, carrier USB-C source
  receptacle and source CC/attachment/VBUS switching/current protection;
  no intermediate USB-A is permitted. Power source attachment logic from
  selected 5 V independently of the Feather regulator to avoid startup deadlock.
  Select host-VBUS detector/level translation, port protection and
  USB-current restrictions/limiting. Select PR1 divider from worst-case RECOM,
  Feather minimum voltage and TPS2116 reference tolerances; evaluate slow-ramp
  chatter and any needed hysteresis. Files: candidate record and a superseding
  ADR if the accepted architecture changes. Verification: supplier drawings,
  circuit calculations and actual sample continuity/fit; do not infer testing.
- [ ] **Revise the unrouted CAD.** Once the design inputs are sufficient, replace
  the direct JP1 feed in `hardware/controller/controller.kicad_sch` with raw
  RECOM/raw USB inputs and selected Feather power; add the USB data gate and
  carrier connectors. Keep output drivers on raw RECOM. Update the carrier PCB
  with a movable USB group and plug/harness clearance, without routing. Update
  README and verification evidence. Verification: ERC, all pin/net/footprint and
  source-path audits, source-state truth table, no bypass/backfeed paths, zero
  routing, DRC and preservation of other board sources. No hardware product
  trace edges until maintained requirements and actual implementations exist.
- [ ] **Refresh review artifacts.** Export both combined PDFs, render changed
  schematic/placement pages and inspect labels, connector roles and power
  boundaries. Run `mise exec -- pre-commit run --all-files`, explicit checks of
  changed/untracked files and standard RQML consistency. Record actual results
  and the existing protected-config limitation if it persists.
- [ ] **Qualify hardware later.** Measure source preference/failover/recovery,
  output dips and upstream/inactive-source leakage; test mains-only, USB-only,
  both, neither, USB insertion/removal and slow RECOM brownout. Test C-to-C and
  A-to-C host cables in all orientations, USB suspend/inrush/current limits,
  application serial and ROM flashing/JTAG. Verify data stays disconnected
  without raw host VBUS. Check EMI/ESD, enclosure retention and mains separation.
  These are future hardware acceptance checks, not completed CAD verification.

Planning verification: independent read-only review found no blocking issue;
all 20 native CAD hashes match the preceding snubber revision. Standard RQML
passes with the unchanged backlog of 13 unverified and seven unimplemented
requirements. Pre-commit on all 28 changed/new files passed, exit 0. The required
aggregate run exited 1 only because the end-of-file fixer cannot open protected
`.agents/plugins/marketplace.json` and `.codex/config.toml` for writing; every
other aggregate hook passed, including Mergify, firmware metadata and RQML
checks. No broader configuration-write retry was made after the earlier
automatic approval rejection. No purchases, CAD edits or physical tests were
performed for this plan.

Correction: the completed initial research above included the now-rejected
A-to-C connection. Reprice the C-to-C cable and Type-C source support before
reusing a complete USB cost estimate. Adafruit 6370 is a 100 mm / $6.95
packaging candidate, not the final cable selection. CAD and PDFs are unchanged.
Correction checks: all 29 changed/new files passed pre-commit, exit 0; standard
RQML passed with the same backlog. All 20 native CAD hashes still match. The
aggregate run again exited 1 solely for the two protected formatter inputs;
all other hooks passed. Source-side CC logic must start independently of the
Feather's 3.3 V output; independent review confirmed that bootstrap constraint.

## Exploratory KiCad MCP integration, 2026-11-15

**Readiness:** READY for the user-requested tool installation and evaluation.
Under `MOT-PROC-001`, this is a scoped development-tool experiment: pin and
install mixelpixx's KiCAD MCP Server through mise, register it for this project,
and evaluate existing CAD workflows on disposable copies. It does not establish
validated CAD transformations or replace the maintained traceability/export
checks. Preserve `MOT-HW-003`, `MOT-CI-003`, `MOT-CI-004` and `MOT-PROC-002`.

- [x] Add the pinned server to the single root mise tool group and register
  the project MCP entry, with the Python runtime appropriate to the pinned
  KiCad build. Verify CI caches the installed server and its built dependencies.
- [x] Initialize the installed server and exercise schematic properties,
  placement, routing/zone operations, checks and representative exports on
  disposable native copies. Compare UUIDs, requirement fields, hierarchy and
  connectivity; confirm the checkout's CAD remains unchanged.
- [x] Record observed headless capabilities, operations requiring a KiCad
  window, untested functions and failures. Distinguish alternative placement
  algorithms from native Place Off-Board Footprints and Repeat Layout.
- [x] Review mapped configuration/documentation changes, refresh only reviewed
  changed RQML edges, and run native trace/SVG checks and full pre-commit.

Delivery is a pull request for review; do not land it as part of this work.

Evaluation evidence is summarized in `docs/kicad-mcp.md`: 250 exposed tools,
headless property/placement/routing/fill/check/export probes, unchanged native
identity and byte-for-byte restoration after reversible edits. Final-runtime
property/shared-sheet/placement and PNG probes passed after the private Python
dependency and renderer compatibility fixes. The original 140 controller files
remain unchanged. Native annotation and canonical SVG checks pass; existing
ERC/DRC findings match direct CLI output and are not resolved by this experiment.
Full pre-commit passes, exit 0; standard RQML and mapped-implementation approval
pass with the existing backlog of 43 unverified and 36 unimplemented requirements.
