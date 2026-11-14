# ADR-0015: Native hardware traceability and low-voltage handling access

- Status: Accepted traceability approach; ESD and access circuits are exploratory
- Date: 2026-11-12
- Classification: derived_from_requirements
- Related requirements: MOT-HW-001, MOT-HW-002, MOT-HW-003, MOT-HW-004, MOT-HW-005, MOT-HW-006, MOT-SENS-005
- Related ADRs: ADR-0011, ADR-0014
- Affected components: all three KiCad projects, shared sheets, review tools

## Context

The developer requested explicit RQML connections into native schematics and
PCBs, consideration of ESD at external interfaces, a finger touch reference
on each board, and inexpensive clip probe access. Existing electrical hardware
requirements remain draft; the user accepted file links plus native fields as
the traceability approach. No hardware immunity or live-handling qualification
has occurred. The three boards remain an unrouted design experiment.

## Decision drivers

Preserve stable requirement IDs, repeated sensor sheets and board groupings.
Separate applicability from implementation and measured verification. Avoid
new PE-to-logic-ground bonds, unwanted default-state paths, costly mandatory
test contacts, and unsupported system-ESD claims.

## Options considered

1. Notes or reference-designator lists only: easy to read but weak identity and
   no machine-checked agreement with PCB fields.
2. Native requirement fields and RQML file links: portable KiCad text, searchable
   IDs, stable source UUID/instance mapping and whole-file drift checking.
3. A KiCad/RQML plugin with component-aware hashes/navigation: more machinery;
   not supported by the pinned RQML CLI and not needed for this first integration.

## Decision

Use hidden space-separated `Requirements` fields on symbols, sheet symbols and
matching PCB footprints. Link every annotated native source, including included
leaf sheets, to MOT-HW-003. Those links implement annotation traceability only;
other requirement fields and `dependsOn` file relationships record design
inputs without claiming completion of draft electrical obligations. A small
native-file checker verifies known IDs, recursive source coverage and agreement
using root/sheet/symbol UUID paths, including repeated and multi-unit parts.

Within the scoped MOT-PROC-001 drawing experiment, add connector-side
bidirectional low-voltage signal clamps where appropriate, with separate
6 V-standoff protection for 5 V rails. In particular, unidirectional clamps
from HEAT/CUT connector pins to local GND are unsuitable: their forward path
would defeat the blocking diodes during ground-first loss. Retain USB's
low-capacitance protection; separately document its panel CC/shield limitations.
Do not connect ordinary logic TVSs from mains contacts to LV GND or add an
unselected mains MOV under this ESD change.

Provide exposed local-LV-GND touch copper, explicitly identified as floating
circuit ground rather than earth, with no intentional PE bond. Provide bare
two-hole same-net test footprints accepting optional hand-formed wire loops.
No purchased test-point contact is required. Put all new handling/probe access
in LV regions and retain sensor-board access after every supported cut.

## Consequences

File-level drift includes placement/format changes; a KiCad UUID fragment is
only a navigation hint to RQML. Annotation checks do not prove electrical
correctness. ESD clamp voltage, current coordination, partial-power effects,
return paths, routing and system tests remain explicit qualification work.
Touch copper equalizes potentials but does not make an exposed energized
mains assembly safe to handle. Clip placement and optional wire geometry need
physical confirmation; routing and fabrication remain outside this study.

## Supersession

No previous ADR is superseded. This adds traceability and exploratory service
access while retaining the accepted partition and integrated-controller design.
