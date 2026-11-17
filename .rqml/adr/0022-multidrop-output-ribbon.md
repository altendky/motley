# ADR-0022: Continuous multi-drop output ribbon with optional second headers

- **Status:** Accepted design direction; parts, wiring limits and CAD integration pending
- **Date:** 2026-11-17
- **Classification:** discretionary_design_choice
- **Related requirements:** draft `MOT-AC-009`, `MOT-HW-015`; approved `MOT-PROC-001`, `MOT-HW-003/013`, `MOT-CI-004`
- **Related ADRs:** ADR-0020, ADR-0021
- **Affected components:** controller/output bus headers, low-voltage harness, output connector population, placement and routing

## Context

The developer selected a continuous ribbon harness as the primary output-bus
topology, replacing the proposed baseline of separate cables through two fitted
headers on every output. Current CAD still has PH6 connections and only one bus
header on each output; neither the 2.54 mm conversion nor a second output header
is implemented yet. Issues #59 and #62 track connector mistake-proofing and
the multi-drop harness work.

## Decision drivers

- Reduce the number of mating contacts traversed by downstream supply current.
- Keep downstream wiring intact when an individual board is unplugged.
- Retain optional separate-cable chaining without buying a second header for
  the default output-board assembly.
- Preserve separate logic and actuator 5 V rails, common low-voltage ground,
  the shared communications bus and line-reference signal.

## Options considered

| Option | Benefits | Costs and limitations |
| --- | --- | --- |
| Separate cables and two fitted headers per output | Individually replaceable cables and flexible spacing | Downstream power traverses intermediate mating contacts and PCB connections; unplugging an intermediate cable breaks the chain |
| Continuous ribbon with one fitted header per output | Continuous downstream conductors; fewer fitted connectors; individual boards are taps | Harness socket spacing is fixed; cable construction and strain relief need explicit specifications |
| Continuous ribbon plus a second DNP header per output | Same primary harness with an optional cable-chaining population | Extra footprint, routing, allocation and exposed-pad review remain necessary |

## Decision

Use one continuous low-voltage ribbon cable from a controller bus header,
with one IDC socket at each output-board position. Specify sockets explicitly
suitable for mid-cable termination. Conductors remain continuous through each
tap; downstream power does not pass through the tapped board's mating contacts
or PCB traces. Each board still has its own contact path to the ribbon.

Use keyed/shrouded 2x3, 2.54 mm board headers, subject to exact-part review.
Provide two electrically identical parallel header footprints on each output
board: one populated and the second DNP by default. Either footprint may serve
the same bus role when deliberately populated. A second fitted header permits
separate-cable chaining as an optional population; the primary build uses the
continuous harness. Connect a given harness to one controller bus socket.

Define pin 1 to wire 1 at every socket and the remaining conductors in order.
Review and freeze the numbered signal mapping for the chosen ribbon/header
pair before CAD integration. Preserve all six functions: low-voltage GND,
selected logic 5 V, raw mains-derived actuator 5 V, SDA, SCL and LINE_SYNC.
The two 5 V rails remain separate. Mains and PE use their separate distribution.

Keep pull-ups centrally owned and treat all taps as one shared electrical bus.
Board identity and runtime addressing do not depend on harness position.
The existing one-new-default-address-board commissioning restriction remains.

## Consequences

This removes intermediate board connections from the downstream conductor path;
it does not eliminate wire resistance, tap-contact failures, cable damage or
shared-bus faults. A shorted tap may still affect the bus. Reduced connector
count is a design rationale, not measured reliability evidence.

Select exact cable gauge, conductor spacing/insulation, IDC socket and strain
relief together. Check total current, shared-ground and supply voltage drops,
temperature, I2C capacitance/rise time, SYNC fanout and allowed total length/tap
spacing. The sixteen-output preference does not establish that the present
1 A supply supports sixteen active boards. Do not silently reduce the target
or claim a new wiring rating.

Apply poka-yoke to the new mating pair and cable construction, including
incompatible USB connections. Keep pin-net, DNP/BOM, native identities,
allocation and generated-image checks when integrating the two footprints.
Physical cable assembly and qualification remain open.

## Supersession

No accepted ADR is superseded. This selects the harness topology within
ADR-0020's shared internal bus; its power domains, commissioning architecture,
isolation boundary and local output control remain applicable.
