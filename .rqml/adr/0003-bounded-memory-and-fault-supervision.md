# ADR-0003: Bounded memory and fatal-fault supervision

- **Status:** Proposed
- **Date:** 2026-11-07
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-ENG-006`, `MOT-ENG-007`, `MOT-ENG-008`, `MOT-ENG-009` in [requirements.rqml](../../requirements.rqml)
- **Related ADRs:** [ADR-0001](0001-portable-core-and-adapters.md), [ADR-0002](0002-build-dependencies-and-code-tooling.md)
- **Affected components:** Core data structures, runtime, task stacks, SDK configuration, diagnostics, fault supervision, host and target verification

## Context

The developer prefers static/stack storage and very limited memory use, and
accepts hard failures for memory faults. Motley handles bounded device work;
arbitrarily sized data-processing workloads are outside the discussed purpose.
`MOT-ENG-008` and `MOT-ENG-009` express the memory and fatal-failure direction,
with detailed acceptance criteria still draft.

The developer also asked about hardware watchdogs. Their availability is
documented for ESP32-C6. This record proposes how to use fault and progress
supervision; it does not establish approved watchdog timings or a reset policy.

## Decision drivers

- Make resource use understandable for each supported configuration.
- Prefer predictable ownership and bounded storage.
- Preserve typed results for ordinary operational and capacity failures.
- Avoid continuing normal execution after a detected memory-integrity fault.
- Account for SDK memory needs without claiming whole-firmware zero-heap use.
- Supervise application progress independently of external sensor/network
  availability.

## Options considered

| Option | Benefits | Costs and fit |
| --- | --- | --- |
| Bounded owned storage, justified limited allocation, fatal memory-fault path, hardware watchdog supervision | Fits the agreed resource and failure direction; gives distinct responses to detected faults and hangs | Needs explicit budgets, progress definitions, and target fault tests |
| General runtime allocation with recovery attempted throughout | Can accommodate more dynamic workloads | Adds recovery complexity that is not justified by the current device scope |
| Require zero heap allocation across the entire SDK and application | Strong whole-program restriction | Compatibility is unproven and goes beyond the stated preference; not proposed |
| Rely on watchdog timeout for all fatal faults | Simple common recovery trigger | Delays handling of already detected faults and does not establish memory-fault detection |

## Decision

Propose fixed-capacity C++ containers and explicitly owned static storage for
predictable, long-lived application data. Use bounded automatic storage for
small temporary values. Large buffers do not belong on a task stack merely to
avoid the heap. No raw C arrays or manual ownership are implied by this design.

Allow dynamic allocation where justified, with capacity and lifetime stated.
Prefer establishing predictable capacities during initialization. Do not
interpret initialization-time allocation or reserving a vector as proof that
every later path is allocation-free. Assess the complete selected firmware's
static storage, task stacks, heap usage, and SDK contribution before fixing
numerical budgets.

Validate ordinary capacity limits before they become memory faults, returning
the relevant typed error. Detected corruption, stack faults, and unexpected
memory exhaustion enter fatal handling. Keep the fatal path small and avoid
depending on fresh allocation for diagnostics. Detailed diagnostic retention,
panic configuration, reset behavior, and repeated-fault handling remain open.

Propose an explicit panic/reboot configuration for detected fatal faults and
hardware-backed watchdog supervision for loss of progress. The runtime owns
supervision; the core receives explicit time and results as described in
ADR-0001. Define progress around completion of bounded application work,
including correctly handled operational failures. An unconditional timer feed
or a requirement for successful network access would not establish this policy.

### Platform evidence

ESP32-C6 provides hardware watchdogs used by IDF's interrupt and task watchdogs.
The task watchdog normally warns and continues; panic/reset behavior needs
explicit configuration. The interrupt watchdog includes a later reset stage
if panic handling cannot execute. OpenOCD affects watchdog operation, so target
verification needs a suitable run without debugger interference.
[Watchdog guide](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32c6/api-reference/system/wdts.html).

Detected memory/stack checks and CPU faults can enter IDF's panic handler,
whose response is configurable. These mechanisms do not guarantee detection
of every memory error.
[Fatal-error guide](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32c6/api-guides/fatal-errors.html).

## Consequences

Memory limits become inputs to configuration and implementation review, rather
than assumptions based on a small initial device. Static/stack preference does
not remove the need to measure stack margins and account for SDK allocations.

Hard-failure acceptance avoids requiring general allocation recovery. It does
not select a watchdog timeout, guarantee diagnostic output from a corrupted
system, or establish recovery from persistent faults. Panic behavior and
watchdog supervision require separate fault-injection and stalled-progress
tests on the selected firmware. No such hardware tests have run.

Reset behavior for any future heater output belongs to its own requirements
and hardware validation; restarting the controller alone does not establish
the output's electrical state.

## Supersession

Supersedes: None. Superseded by: None.
