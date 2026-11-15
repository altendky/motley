# ADR-0021: Four-layer controller boards with ground and power planes

- **Status:** Accepted for the developer-authorized exploratory CAD revision; product qualification pending
- **Date:** 2026-11-14
- **Classification:** discretionary_design_choice
- **Related requirements:** approved `MOT-PROC-001`, `MOT-HW-003`, `MOT-CI-004`; draft `MOT-HW-004/005/006/007/008/009/010/011/012`, `MOT-SENS-005`, `MOT-AC-014`
- **Related ADRs:** ADR-0011, ADR-0014, ADR-0015, ADR-0016, ADR-0020
- **Affected components:** carrier, single-output and sensor-mux PCB stackups, copper distribution and derivative review images

## Context

The developer selected four copper layers with ground and power planes after
comparing the extra fabrication cost with two layers. The current routed
studies have front-only assembly and fixed outlines below 100 mm. The carrier
USB pair has gaps in its opposite-layer ground reference. The output study
also retains two CUT_EN opens and four via-drill/SMD-land intersections.
Adding inner copper must preserve isolated power domains and supported sensor
cuts rather than bypassing switches, source selection or power-link resistors.

This is a layout/stackup choice within the recorded `MOT-PROC-001` exploratory
exception. It does not introduce a new product behavior or approve the draft
electrical requirements. Existing requirement identities and schematic circuits
remain unchanged; `MOT-HW-003` continues to govern native source identity.

## Decision drivers

- Improve low-voltage supply distribution and signal return paths at a modest
  fabrication premium, while retaining front-only component assembly.
- Preserve mains/LV separation on every layer, protective-earth continuity,
  antenna exclusions, rail switching/source selection and connector protection.
- Retain the packed outlines and sensor five/six/seven-port cut-down geometry.
- Make the actual inner copper visible and reviewable in committed derivatives.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Retain two layers | Existing routed study; lowest bare-board cost | Supply/return routing competes with signals; fragmented USB reference remains |
| Four layers with ground and split power | Adjacent references and broader supply copper; front assembly unchanged | Extra fabrication cost; plane islands, keepouts and power-domain boundaries require review |
| Four layers with two ground layers | Simple references on both outer sides | Does not provide the requested internal power distribution without additional partitions |

## Decision

Convert all three PCB designs to four layers while preserving their footprints,
native identities, pad nets, circuits, outlines and front-side access. Use:

| Layer | Role |
| --- | --- |
| F.Cu | Components, signals and necessary local power/ground copper |
| In1.Cu | Low-voltage GND reference plane, excluded from mains, antenna and cutting reserves |
| In2.Cu | Distinct low-voltage supply-plane regions; an explicit GND reference corridor beneath the carrier's existing back-side USB route |
| B.Cu | Signals and necessary local power/return copper |

Use the JLCPCB standard **JLC04161H-7628 / 1.6 mm nominal** construction as
the documented study stackup: outer copper 0.035 mm, outer-to-inner 7628
prepreg 0.2104 mm (Er 4.4), inner copper 0.0152 mm, and core dielectric
1.065 mm (Er 4.6). The material-layer total is 1.5862 mm before surface
coatings; retain the nominal 1.6 mm board specification. The [published
stackup](https://jlcpcb.com/impedance) identifies these dimensions. Manufacturing
tolerances, exact order options and controlled-impedance acceptance remain open.

Keep raw actuator 5 V, selected logic 5 V, controller 3.3 V and switched sensor
3.3 V distinct on the carrier. Keep local output 3.3 V, selected logic 5 V and
raw actuator 5 V distinct on output boards. The sensor's main power plane uses
3V3_SENS. Existing post-link Qwiic supply nets remain local, separate nets.
Use practical plane regions with actual via/through-hole connections; do not
label an unconnected copper island as implemented power distribution.

Retain the existing deliberately sized outer mains conductors. No mains or PE
plane is added. Inner LV copper must pass an independent projected all-layer
5 mm mains separation check as well as native DRC. Extend antenna/kerf copper
exclusions to all enabled layers; preserve placement-only Repeat Layout areas.
The carrier back USB route must see actual continuous In2 GND below its
route/transition corridor, with return stitching. The added In1 plane alone
does not solve a back-side reference gap. This revision does not claim a
qualified 90-ohm differential pair.

For sensor variants, clip actual filled copper at the worst retained edge of
each kerf and verify all retained netted pads. Split polygon islands explicitly;
only plated through pads and vias may connect layers in that graph. Keep
pads/vias/pours outside every kerf and retain separated outer trace crossings.

Resolve the output board's two opens and drill/land intersections during the
associated routing revision where practical, preserving the mains load path
and package fanouts. Do not substitute components or change schematic pinouts.

## Consequences

The board editor, project stackup and saved copper fills must agree. Ordinary
through vias remain sufficient; no blind/buried vias or filled/capped via-in-pad
process is selected. Add deterministic In1/In2 SVG views and retain front/back
views. Review per-net plane connections, isolated islands, current paths, USB
references, trims, antenna and mounting envelopes before refreshing baselines.

Native DRC/parity results, exact source hashes and actual execution evidence
remain separate from RQML structural gates. Firmware, electrical/thermal/EMC,
cutting-process, enclosure and mains qualification remain outside this revision.

## Supersession

No system-architecture ADR is superseded. This replaces the earlier two-layer
stackup assumptions in the current routing studies while preserving their
circuit, modular partition and exploratory-status decisions.
