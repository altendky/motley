---
name: jlcpcb-quote
description: Prepare current Motley KiCad exports and obtain JLCPCB prices through its web API, separating fabrication, confirmed assembly and unquoted costs.
---

# JLCPCB quotes

Use quotation-only API operations. Do not add to a cart, order, pay or purchase
component inventory. These are undocumented frontend APIs; verify current
contracts and responses. Read [the API reference](references/api.md) for the
verified fabrication and assembly workflow.

## Inputs

- Export each current `hardware/controller/motley-*.kicad_pcb` separately with
  pinned KiCad, saved copper fills, enabled copper layers, mask, silkscreen,
  outline and drills. Preserve native source hashes and use disposable copies
  for export origins. Check detected dimensions/layers against the native board.
- Generate matching BOM/CPL pairs from current placements. Account for every
  footprint as factory candidate, manual/unmatched, DNP or mechanical/access
  feature. Verify exact manufacturer/package/variant for catalogue codes;
  reject unapproved automatic matches, especially mains/pulse-rated parts.
- One complete controller currently uses one carrier, one sensor mux and two
  identical output boards. Recheck fabrication/assembly minimums and stock for
  each scenario. Quote spare factory assemblies but hand-complete only the
  requested finished units.

## Authentication and evidence

Fabrication pricing works anonymously; saved assembly jobs, matching and final
pricing require authentication. Reuse an authorized session. If interactive
login/verification is needed, let the user complete it, then continue API calls
in that session. Keep the browser client open across tasks when requested;
handle local task failures without disconnecting it. Do not extract cookies,
tokens or passwords into agent-visible output or quote artifacts.

Retain requests, responses, date, settings, input hashes and confirmed selected
references. Check API `code`, quantities, stock and actual fee breakdowns before
claiming a populated-board quote; catalogue prices alone are insufficient.

## Report

Separate quoted PCB/assembly charges, missing or hand-fitted parts and off-board
allowances. Reconcile manual parts against actual factory selections to avoid
double counting THT parts JLC will fit. Include attrition/minimum purchases,
spares, unresolved matches and shipping/tax exclusions. A fuse may need a
cartridge plus two clips; an outlet handoff terminal excludes the receptacle.

Round only after summing unrounded amounts. Preserve useful aggregate evidence
with the cost documentation; keep generated quote files temporary. Export and
quote acceptance do not establish manufacturing readiness.
