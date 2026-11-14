# ADR-0010: Three-board controller study

- **Status:** Superseded in part by ADR-0011
- **Date:** 2026-11-12
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-PROC-001`; draft `MOT-SENS-005` remains future firmware work
- **Related ADRs:** None
- **Affected components:** Controller CAD projects, inter-board connections, sensor connector placement, manufacturing planning

## Context

The developer selected three physical boards: Feather with AC input, AC output,
and multiplexer with sensor connectors. The connector board should have an
L-shaped outline and permit removing the highest-numbered unused ports. Ordinary
through-hole pins are preferred over castellations. The present CAD is an
unrouted placement experiment under the scoped `MOT-PROC-001` exception documented
in `hardware/controller/README.md`; this decision does not approve a mains design
or add maintained product behavior.

## Decision drivers

- Place sensor connectors together at one enclosure wall.
- Separate enclosure placement of the controller, outlets and sensor bank.
- Retain one sensor-board design for configurations with one through eight ports.
- Preserve shared definitions for the two heater circuits and eight sensor ports.
- Keep manufacturing overhead reasonable at prototype quantities.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| One integrated PCB | One assembly setup and fewer interconnects | Couples all connector locations and enclosure geometry |
| Three boards, with both outputs on one board | Independent sensor and power placement; three assembly setups | Additional connectors and separate fabrication/assembly jobs |
| One board per heater channel | Identical interchangeable output modules | Four physical boards and more wiring/supports for the current two-channel unit |

## Decision

Use three board designs and three physical boards per controller:

1. **Feather / AC input:** Feather sockets, run-power jumper, input connection,
   main fuse, RECOM RAC05-05SK and its output capacitors.
2. **AC output:** both branch fuses, zero-cross optotriacs, triacs, series cutoff
   relays, low-voltage drivers, optional snubbers, outlet wiring connections and
   heatsink reservations. Both channels instantiate the shared heater sheet.
3. **Mux / sensor connectors:** TCA9548A, reset pull-up, decoupling, optional
   upstream pull-ups, and eight instances of the shared sensor-port sheet.

The sensor interface carries 3V3, GND, SDA, SCL and GPIO21 mux reset. A separate
low-voltage output interface carries 5V, GND and four heater/relay commands.
Mains distribution to the output board uses a distinct, appropriately rated
connection carrying fused line, neutral and PE. Ordinary signal headers are
placement placeholders for low voltage only. PE continuity and the isolation
between mains and low voltage must survive the split.

The L-board retains the mux and upstream interface in its fixed leg. Remove
highest channels first, retaining ports 0 through N-1 and their pull-ups. Reserve
cutting lanes between port groups; essential core and retained-port paths must
never depend on a discarded section. Routing must account for deliberate copper
crossings to the discarded ports, edge clearance after cutting, kerf and cleanup.
An unrouted placement cannot qualify electrical operation after trimming.

Each physical board has its own schematic root, project, netlist and PCB. Keep
the canonical shared channel sheets and local libraries. Record the system
interconnect map separately rather than treating other boards' components as
missing parts in each PCB's schematic parity check.

## Consequences

Keep all three placement studies unrouted as requested. Board dimensions and
interconnect packaging remain provisional. Prefer fitting within 100 x 100 mm
where practical, but do not trade mains spacing, thermal room or mechanical fit
for a fabrication discount. No buying, panelization, routing, Gerbers or mains
energization is authorized by this architectural decision.

Separate Economic PCBA jobs add setup/stencil overhead. A direct anonymous quote
on 2026-11-12 for five green, two-layer, 1.6 mm, 1 oz, leaded-HASL boards returned
$4 for 100 x 100 mm, $4 for 50 x 100 mm and $11.30 for 150 x 100 mm, before
shipping/taxes; smaller boards also showed an eligible $2 promotional amount.
Those figures are a planning comparison, not an order quote for the final CAD.

## Supersession

Supersedes the experiment's monolithic PCB partition; component choices and
unresolved engineering questions remain. Superseded in part by:
[ADR-0011](0011-single-output-modules-and-sensor-core.md).
