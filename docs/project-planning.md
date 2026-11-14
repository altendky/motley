# Project planning

This is a working brief for developing Motley's specification and design.
Agreed planning direction and unresolved proposals are distinguished below;
neither substitutes for reviewed requirements.
The maintained specification is [requirements.rqml](../requirements.rqml).
It contains draft engineering requirements and the approved minimal-build
milestone; product behavior still needs to be specified.

Current component research is recorded in [Hardware candidates](hardware-candidates.md).
It preserves preliminary parts, sourcing snapshots, and open alternatives,
including two AC outlets and both power-entry arrangements, without promoting
them to a complete selection or approved hardware design.

## Where information belongs

| Artifact | Owns | References rather than duplicates |
| --- | --- | --- |
| `requirements.rqml` | Goals, required behavior, binding constraints, acceptance criteria, and real implementation/test traces | Design rationale, procedures, and task sequencing |
| `.rqml/adr/` | Significant architectural choices, alternatives, reasons, and consequences | Requirements and acceptance criteria |
| `.rqml/plan.md` | Readiness, implementation stages, affected files, verification steps, and progress | Specification content and architectural rationale |
| `docs/` | Project orientation, architecture explanations, diagrams, setup, wiring, operation, troubleshooting, and research | Binding obligations and implementation task status |
| Tool configuration and lockfiles | Tool selections, versions, dependency declarations, locking policy, and executable automation | Explanations of when and why to use the tools |

A binding obligation belongs in RQML even when it concerns architecture or
engineering rather than externally visible behavior. An ADR explains a
significant choice; ordinary implementation details need no ADR. Architecture
documentation describes the current system, while ADRs preserve decision history.

The portable-core direction is now agreed. `MOT-ENG-004` captures host
testability and `MOT-ENG-005` captures the explicit environment boundary. Their
detailed acceptance criteria are draft. [ADR-0001](../.rqml/adr/0001-portable-core-and-adapters.md)
proposes the supporting architecture; it does not substitute for those
obligations or establish implementation evidence.

`MOT-ENG-006` captures the agreed typed-result policy for recoverable failures.
`MOT-ENG-007` captures the subsequently agreed exceptions-disabled production
policy. `MOT-ENG-008` and `MOT-ENG-009` capture bounded memory with static/stack
preference and hard failures for detected memory faults. ADR-0002 covers code
tooling and proposed ADR-0003 covers memory/fault supervision. RTTI is intended
to be disabled by default, revisitable for a concrete need. Numerical budgets
and watchdog/reset details remain open.

Keep one authoritative home for each fact. Explanations link to requirement IDs;
plans link to requirements and ADRs. Avoid maintaining additional acceptance
lists in Markdown. Promote settled proposals from this brief into their proper
artifacts and replace the proposal with a reference.

## Requirements structure

Start with one specification and a shallow grouping by capability. Candidate
areas are device behavior, external interfaces and lifecycle, configuration,
and engineering constraints. Add groups only as actual requirements emerge.

A requirement identifies a focused obligation, not a function or source file.
Use acceptance criteria to express relevant cases and boundaries. Decompose a
requirement only when the obligations can be understood and reviewed separately.

Connect requirements to cohesive implementation and test targets once those
targets exist. A requirement may span modules, and a module may serve several
requirements. Do not reproduce the C++ call/include graph or create obligations
for every helper function. Apply project-wide constraints through design and
review as well as declared traces.

## First milestone direction

The agreed direction is a temperature/humidity device exposing measurements to
Home Assistant through Matter over Thread. Exact hardware must be discussed
before selecting sensors or fixing channel counts. Four temperature channels
and two humidity channels were an initial proposal, not an agreed count.
The earlier working target was the Adafruit ESP32-C6 Feather; the current
discussion confirms an Adafruit Feather as hardware to use. The recovered
hardware discussion below is the starting point for further planning.

The application is air temperature/humidity monitoring in a hermit-crab tank.
The working physical arrangement places the controller outside the tank and
sensors inside it. No submerged measurements have been requested. Cables around
6 ft long have been considered; this is a tentative length, not a fixed limit.
Monitoring the ambient environment outside the tank is also under consideration.
The recovered enclosure discussion also requested a glass-temperature sensor
for monitoring and limiting heater control; its role in the first milestone
still needs reconciliation with the air-monitoring scope.

Resolve measurement locations, operating ranges, exposure to moisture or
condensation, wiring, power, and environmental constraints before selecting
parts. Do not assume which measurements share a physical sensor.

Develop reusable pieces through the first useful device. Decide which variation
the first milestone actually needs before designing a general device framework.
The historical skylight application in
[PLANNING_SESSION.md](../PLANNING_SESSION.md) is research material, not the
current specification or an automatically included milestone.

The first milestone needs agreement on:

- The measurements and physical arrangement: sensor types, channel count,
  connections, power, and any relevant environmental constraints.
- How a person commissions the device and observes its measurements through
  the intended controller.
- Expected behavior when a sensor is absent, fails, or recovers, and when the
  network is unavailable or the device restarts.
- Configuration that is essential for this device, and how it is supplied.
- Explicit exclusions and which lifecycle capabilities are needed immediately.

Do not infer timing, accuracy, retry, persistence, or recovery thresholds from
examples or SDK defaults. Establish them when drafting acceptance criteria.

## Recovered planning context

The original Codex discussion on November 5–6, 2026, contains more product
planning than the temporary continuation note preserved. Later discussion on
November 7 requested an empty specification for merging the RQML tooling setup,
followed by deliberate requirements development. Removing those draft
requirements did not establish rejection of the prior product discussion.
Earlier written summaries remain recoverable in Git before commit
`edc760914c93c177a5394f72f05e5328bb0658e1`; they are draft evidence, not approved
requirements.

| Topic | Recovered position | Status |
| --- | --- | --- |
| Controller | Adafruit ESP32-C6 Feather was the working target. | Earlier target; Adafruit Feather reaffirmed in the current discussion; no connected-board verification |
| Integration | Home Assistant through Matter over Thread. | Agreed direction |
| Measurement locations | Temperature and humidity need not share locations or use integrated sensors. Avoid arrangements that depend on special combinations of sensor addresses and placement. | User-stated flexibility goal; exact layout open |
| Counts | Four temperature measurements and perhaps two humidity measurements. | Exploratory; current discussion explicitly leaves counts open |
| Expansion | A clean, expandable arrangement using multiplexed ports; starting in the same Adafruit product family was welcomed, with alternatives still worth knowing. | User-stated direction; exact hardware remains to be settled |
| Multiplexer | Adafruit PCA9548 eight-channel STEMMA QT multiplexer, product 5626. The earlier proposal used a separate cable-connected board, not a stacking FeatherWing. | Historical agent proposal; assembly not verified |
| Sensors | Adafruit SHT45 breakout, product 5665; the user said SHT45 seemed decent. | Favored candidate, not a final selection or purchase record |
| Remote heads | Sensor enclosure with a four-wire cable back to the controller or expansion board; roughly 6 ft was considered. | Discussed arrangement; cable, enclosure, and electrical qualification open |
| Optional output | Possible control of an external accessory for an approximately 25 W, 120 V AC heater. A related enclosure discussion explored independently varying both heaters through Home Assistant, with air and glass-temperature feedback. | Exploratory capability; switching accessory and regulation undecided; not automatically part of the first sensing milestone |
| Language | C/C++ was accepted after considering Rust library maturity. Safety and correctness, managed ownership, avoiding raw pointers, and vectors rather than C arrays were requested. | Project engineering direction to express carefully in requirements and design |
| Deferred priorities | Thread-router operation and long battery life may matter for later Motley uses, but are not first needs. | User-stated scope priorities |
| SDK and builds | ESP-IDF with esp-matter was the leading path; native SDK tooling with CMake/Ninja and a host-testable core was later proposed. | Build/dependency comparison unfinished; no validated firmware stack |
| Architecture | A previous cross-project review suggested a pure core, explicit state/effects, narrow I/O adapters, meaningful types, and abstraction where needed. | Originally an agent synthesis; the host-testable core and environment boundary are now agreed directions captured in `MOT-ENG-004` and `MOT-ENG-005`; ADR-0001 remains proposed |

The earlier draft used `MOT-PLAT-001`–`003`, `MOT-SENS-001`–`004`,
`MOT-ENG-001`–`003`, and `MOT-OUT-001`–`002`. Consult that history when bringing
an obligation back into the specification, preserving its identity where the
intent remains the same. Review the statements and acceptance criteria rather
than restoring the draft wholesale.

Technical claims in the recovered conversation are historical research, not
fresh compatibility verification. The actual sensor assembly and cable still
need validation. A recent check of Sensirion's
[design guide](https://sensirion.com/resource/user_guide/sht/design_in/)
also identifies air exchange, separation from electronics' heat, contamination,
prolonged high humidity, and long-I2C signal integrity as design considerations.
Testing one candidate probe over the intended cable and comparing readings with
a reference instrument in the intended environment would provide initial fit
evidence; it has not been performed.

## Heater modulation and switching endurance

The user's working premise is that the thermal system strongly smooths heater
power pulses with periods on the order of 10 seconds or longer. Slow
time-proportioned on/off control is therefore an option for variable average
power. The final period and acceptable glass/air temperature variation remain
to be established; no thermal test has been performed for Motley.

For continuous modulation at an intermediate duty cycle, one complete on/off
cycle per period gives the following switching budget for each output:

| Modulation period | Complete on/off cycles per 365-day year |
| --- | ---: |
| 10 s | 3,153,600 |
| 60 s | 525,600 |
| 300 s | 105,120 |

These are calculated counts, not lifetime predictions. Multiply by the fraction
of time spent cycling for a different operating profile; a steady fully-on or
fully-off output need not switch each period. Compare the candidate's definition
of an operation with this complete-cycle count.

Mechanical relay evaluation must use electrical endurance at the actual load
and switching conditions, in addition to mechanical endurance. See
[Omron's relay guidance](https://www.ia.omron.com/product/cautions/36/safety_precautions.html).
A zero-cross AC solid-state relay is a candidate for frequent heater cycling;
[Omron's SSR guide](https://www.ia.omron.com/data_pdf/guide/18/ssr_tg_e_9_10.pdf)
discusses repeated heater switching and the absence of contact wear. Exact
load compatibility, operating limits, and the complete switching accessory
remain to be evaluated. Neither a switching technology nor a period is selected.

## Open hardware expansion ideas

Recorded 2026-11-13 for later consideration. These are open proposals, not
selected features, approved requirements, or additions to the current
[controller board study](../hardware/controller/README.md). No bus, connector,
pin assignment, display, or input device is selected here.

| Idea | Questions to investigate |
| --- | --- |
| Bus-controlled output stages | Could an addressed bus replace or supplement individual GPIO command wires, allowing more flexible placement and a much higher output count? Compare shared I/O or PWM expanders with intelligent output modules; consider address selection, discovery/configuration, bus wiring and power, command timing, and fault containment. |
| Bus-friendly AC feedback | Include I2C or another suitable digital readout when comparing voltage/current feedback hardware, so adding outputs does not consume separate controller ADC inputs for every channel. Distinguish measurement readout from line-synchronous triac firing; compare integrated meters with isolated sensors plus a local ADC/controller. See the [AC control investigation](hardware-candidates.md#ac-control-feedback-and-bus-investigation). |
| Shared output cutoff | Consider replacing per-channel cutoff relays with one relay feeding all controlled outlets. Compare shutting down every output on a fault with retaining unaffected channels, combined current and lamp inrush, module independence, and cutoff operation during a control-bus failure. Keep this open; the current circuit retains per-channel relays. |
| More exposed controller interfaces | Which otherwise available buses and GPIO would be useful on expansion headers? Consider SPI, UART, additional I2C access, analog inputs and PWM outputs where supported and available after existing assignments. Review pin multiplexing, boot/debug use, voltage levels and power budgets before choosing pins. |
| Familiar expansion header layout | Would Feather/FeatherWing or another established header arrangement make accessories easier to reuse? Evaluate mechanical fit, actual pin/function compatibility, supply rails, clearance and enclosure access; similar header geometry alone would not establish compatibility. |
| Display or multiple displays | Consider local temperature/humidity, setpoint, output-state and fault indication. Explore one shared display versus multiple displays, their location, interface and connector needs, and whether they belong on a separate board. |
| Local control inputs | Consider buttons, rotary encoders, switches or analog controls for settings and operation. Define intended actions, startup/disconnection behavior, and how local commands interact with network commands and safety limits before selecting hardware. |
| Optional user-interface board | Could displays and controls share an optional panel board, separate from the controller and mains output boards? Consider enclosure placement, mounting, cable/header choice and power; decide what remains usable when the board is absent or disconnected. |

For bus-controlled outputs, preserve the discussed direction that temperature
regulation runs in the device rather than Home Assistant. Decide whether a
single local controller owns all loops or intelligent output modules own their
loops. Network availability must not be required for continued regulation;
loss of the internal control bus or stale commands needs a separate
fault policy. Review output-off defaults, startup, reset, disconnected
connectors and failed expansion modules against `MOT-HW-001` and `MOT-HW-002`
when developing a concrete proposal.

Existing dual-I2C Qwiic access is recorded separately in `MOT-HW-009`; this list
asks what further expansion is worthwhile. Revisit these ideas before fixing
the remaining pin allocation, board routing and enclosure interfaces, comparing
incremental cost and space with the likely benefit. Any anticipated dimension
above the 100 mm board target remains a discussion point under
`MOT-HW-007` and `MOT-HW-008`. Promote an idea into requirements and an ADR only
when its intent and architectural choice have actually been settled.

## Decisions to resolve

| Decision | Question to settle | Destination |
| --- | --- | --- |
| First useful device | Given the agreed sensor-device direction, what physical arrangement, success/failure scenarios, and exclusions define the first deliverable? | Goals, scenarios, and requirements in RQML |
| Engineering constraints | Which portability, testing, resource, and dependency boundaries are binding for Motley? | RQML obligations; ADRs for significant ways of meeting them |
| Build and dependency tooling | Which SDK, build system, component manager, and host-test setup form a compatible, reproducible stack? | ADR; tool/dependency configuration; setup procedures |
| Runtime boundaries | How do domain behavior, sensor access, Matter integration, configuration, and time interact? | ADR where significant; architecture explanation as the design develops |
| Verification scope | Which behavior is established by host tests, target builds, and physical-device integration tests? | Acceptance criteria in RQML; execution steps and results in the plan |

Toolchain evaluation should establish a working target build and host-test path,
not only the availability of installation commands. Prefer project-managed
tools and dependencies where practical; identify actual host prerequisites.
Keep selected versions in configuration rather than copying them into prose.

## Current software and documentation focus

The current approved checkpoint is a commissionable Matter-over-Thread device with
readable device and firmware information, followed by power-cycle/recommissioning
checks. The developer has Home Assistant and a working Thread border router.
Approved `MOT-PLAT-001`, `MOT-PLAT-004`, and `MOT-INFO-001` capture this stage;
[ADR-0009](../.rqml/adr/0009-matter-device-information-foundation.md) records the
integration decision and evidence. Progress and remaining verification are in
[the plan](../.rqml/plan.md). Application sensing and control remain later work.

Use standard Matter Basic Information for declared vendor/product, hardware,
stable-device, and firmware identity. The aim is to show the complete current
commit/cleanliness identity in Home Assistant's normal firmware information.
The SDK's shortened version label remains separate. ADR-0009 selects numeric
software version, prototype identity, board settings and serial commands.
The root-only device model and actual controller presentation remain to be
validated on hardware; see [the development procedure](matter-development.md).

Use a development-style USB serial interface for commissioning-code output and
deliberate factory reset in this milestone. The deployed-device setup/recovery
interface will be defined and implemented in
[deferred issue #15](https://github.com/altendky/motley/issues/15).

The following broader tooling proposals remain open beyond that checkpoint.

Hardware research continues separately in [Hardware candidates](hardware-candidates.md);
it does not change the approved software milestone. The proposed
core/adapters architecture is in
[ADR-0001](../.rqml/adr/0001-portable-core-and-adapters.md). The immediate focus
is code and project tooling:
[ADR-0002](../.rqml/adr/0002-build-dependencies-and-code-tooling.md) proposes
the language baseline, build structure, dependency management, test framework,
analysis, and CI integration. Settle those choices and their failure-handling
implications before turning them into executable configuration. Measurement
identity, validity/freshness, configuration validation, and mapping to external
measurements are subsequent requirements topics, not implemented capabilities.

The requested build-first checkpoint is specified separately as `MOT-BUILD-001`.
[ADR-0004](../.rqml/adr/0004-minimal-firmware-build.md) selects an official
ESP-IDF container for the idle-task target. Its exercised workflow is described
in [firmware-build.md](firmware-build.md). This bootstrap does not settle the
future Matter dependency release set.

The firmware tooling candidate is native ESP-IDF with esp-matter. Espressif
documents both a managed-component route and a full SDK checkout in its
[ESP32-C6 development guide](https://docs.espressif.com/projects/esp-matter/en/latest/esp32c6/developing.html).
Evaluate the managed component first for a product application; use a full
checkout if required tools or source changes justify it. Select a specific
release and its documented compatible SDK set together. Do not combine
instructions from unrelated release branches or copy versions into this brief.

The component manager uses a manifest and generated lockfile; apply its
[locking guidance](https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/dependencies_lock.html)
to the chosen dependency sources. Mise continues to own general development
tools. Actual selections and pins belong in executable configuration.

Routine core tests are proposed to use an ordinary host C++ build. ESP-IDF's
[Linux host target](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c6/api-guides/host-apps.html)
is experimental and supports only part of the SDK; it is a separate option for
platform-related tests. Neither route has been installed or validated here.

As the design settles, keep these documentation responsibilities distinct:

- This brief retains unresolved proposals and planning context.
- ADRs retain significant choices and their consequences.
- Architecture documentation will explain the implemented boundaries and data
  flow, linking to the relevant requirements and ADRs.
- Developer setup documentation will describe exercised host and firmware
  commands and configuration ownership once the toolchain is proven.
- `.rqml/plan.md` tracks the next work and observed verification evidence.

Do not create empty documentation shells or copy SDK setup instructions before
the corresponding project workflow exists.

## Evidence and unresolved work

The engineering requirements remain draft with no implementation or verification
links, and the pure-core ADR remains proposed. The minimal firmware build is a
separate milestone; its status and evidence are tracked in
[the plan](../.rqml/plan.md). Application behavior and its test suite remain
future work.

Draft requirements are proposals until reviewed and approved. Missing
implementation or verification remains visible as incomplete work; do not create
placeholder traces to make coverage appear complete.

Builds and host tests can establish useful evidence before a physical device is
available. They do not establish electrical behavior, real sensor communication,
radio operation, commissioning, or controller interoperability. Record those
as pending hardware verification until exercised.

Current planning tasks and readiness live in [.rqml/plan.md](../.rqml/plan.md).
