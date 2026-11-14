# ADR-0011: Single-output modules and sensor core behind connectors

- **Status:** Accepted for the exploratory hardware study
- **Date:** 2026-11-12
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`; draft `MOT-SENS-005` remains future firmware work
- **Related ADRs:** [ADR-0010](0010-three-board-controller-study.md)
- **Affected components:** AC-output module, carrier interfaces, sensor-board outline, combined review PDFs

## Context

The developer clarified that each AC-output board should contain one output,
with two identical boards used in the current controller. The sensor board's
length should follow its connector row, with the mux and supporting circuitry
fully behind that row. A core spanning two or more connector positions is
acceptable; an unwanted socket can be omitted or removed. This revises the
physical partition and sensor geometry in ADR-0010.

## Decision drivers

- Reuse one AC-output design for each controlled outlet.
- Keep the complete sensor core behind the connector row rather than extending
  the board length beside it.
- Preserve optional removal of the highest-numbered sensor connector tail.
- Preserve the existing circuit and its separate mains/low-voltage interfaces.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Two outputs on one board | Fewer physical modules and interconnects | Does not match the requested per-output modularity |
| One output per identical board | Reusable module and independent outlet placement | Two physical output boards and separate feeds |
| Narrow sensor core behind one socket | Can trim to a one-position board | Considerably deeper core and tighter component arrangement |
| Compact core behind two positions | Shorter overall connector-controlled length and compact depth | Core remains when an unwanted socket is omitted; tail trimming retains at least the core width |

## Decision

Use three board designs and four physical boards in the current unit: one
Feather/AC-input carrier, two identical single-channel AC-output modules, and
one mux/sensor board. Each output module instantiates the existing shared heater
sheet once and has a four-pin low-voltage interface (GND, 5V, heat enable, cutoff
enable) plus a separate fused-line/neutral/PE feed. The carrier exposes separate
control and mains feed connections for the two module copies.

Move the sensor core fully behind the connector row. The row's connector pitch,
outer connector envelopes and end margins determine overall board length. Keep
the mux, support parts, upstream interface and mechanical pins behind the first
two connector positions; trim only the remaining connector tail. Do not promise
a one-position cut-down board or remove required core circuitry to achieve it.
Omitting or removing an unwanted socket does not require removing its PCB area.

Keep separate project roots/netlists for the three designs and one canonical
heater sheet and sensor-port sheet. The assembly record maps both physical
output copies to the single output project. Review PDFs show each design once,
with the required output quantity stated explicitly.

## Consequences

The controller has four physical boards but still only three distinct designs
for manufacturing setup. Output-board assembly quantity is twice the controller
quantity. Prototype minimum quantities and assembly setup must be quoted against
that arrangement rather than four unique designs. All boards remain unrouted;
the earlier mains, thermal, mechanical, sensor-cable and post-trim qualification
limitations remain. No product requirements or verification traces are added.

## Supersession

Supersedes ADR-0010's two-channel output-board partition, three-physical-board
count and one-position sensor trimming assumption. Its other scoped-experiment
and interface/isolation decisions remain applicable. Superseded in part by
[ADR-0016](0016-flexible-sensor-core-aspect-ratio.md): the common sensor area is
not constrained to the first two connector positions.
