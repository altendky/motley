# ADR-0001: Portable core and explicit environment adapters

- **Status:** Proposed
- **Date:** 2026-11-07
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-ENG-004`, `MOT-ENG-005` in [requirements.rqml](../../requirements.rqml)
- **Related ADRs:** None
- **Affected components:** Application core, runtime coordination, sensor adapters, Matter adapter, storage adapter, clock adapter, host tests, firmware build

## Context

The developer agreed that Motley needs a portable C++ core testable on a host,
with clock, sensor, storage, and Matter I/O supplied outside that core. The
requirements now express that direction; their detailed acceptance criteria
remain draft. No firmware or host test target exists yet.

The software design can progress while exact sensor counts, wiring, and heater
hardware remain open. Product behavior still needs requirements before it is
implemented.

## Decision drivers

- Exercise application decisions with controlled inputs on a development host.
- Share the implementation used by host tests and controller firmware.
- Keep platform scheduling, driver lifetimes, and SDK types at the integration
  boundary.
- Keep requested work distinct from the observed result of performing it.
- Establish useful boundaries without selecting an event framework or generic
  plugin system before their need is understood.

## Options considered

| Option | Benefits | Costs and fit |
| --- | --- | --- |
| Pure C++ core, explicit inputs and requested work, adapters coordinated by a runtime | Host execution needs ordinary C++ tools; decisions and failures are directly inspectable | Requires explicit result routing and ownership; target integration still needs separate verification |
| Core calls injected I/O interfaces | Familiar object interfaces; fake implementations can support host tests | Production calls still execute I/O from inside core decisions; conflicts with the explicit boundary in `MOT-ENG-005` |
| Application logic coupled to ESP-IDF/Matter, tested through an SDK host environment | Less initial separation from examples and platform APIs | Makes core testing depend on the firmware environment and does not meet the agreed independent-host boundary |

## Decision

Propose a core that consumes explicit observations and operation results,
updates application-owned state, and produces requested work as data. Time is
an input; requesting a later wake-up does not read a clock or start a timer
inside the core.

A small runtime connects those requests to concrete adapters and delivers their
results back to the core. Adapters own access to clocks, sensor buses, storage,
and Matter. The runtime handles platform execution and scheduling; the core
owns application decisions. A successful SDK call is interpreted according to
that API's contract, rather than automatically treated as observed controller
or physical-device success.

```mermaid
flowchart LR
    tests[Host tests] -->|Explicit inputs| core[Portable C++ core]
    core -->|State and requested work| tests
    core -->|Requested work| runtime[Runtime coordination]
    runtime -->|Time, observations, results| core
    runtime -->|Operations| adapters[Clock, sensor, storage, Matter adapters]
    adapters -->|Operation results| runtime
```

Build the core sources as an ordinary host C++ library and include those same
sources in the firmware build. The proposed host build uses CMake independently
of ESP-IDF. Select the C++ language level, test framework, and firmware dependency
delivery in subsequent tooling work.

This does not prescribe one universal event variant, an asynchronous framework,
an abstract class per adapter, or a final source-tree layout. Define concrete
types and interfaces as approved product scenarios establish their needs.

## Consequences

The core can be tested using explicit time and supplied success/failure results.
Tests can inspect requested work without a device, filesystem, or network.
Firmware integration reuses that implementation.

The runtime must define result correlation, ownership, and scheduling once the
relevant behaviors are specified. Those contracts are additional work, not
provided automatically by separating the core. Host tests cannot establish
sensor communication, radio behavior, commissioning, persistence across real
resets, or heater switching behavior.

The firmware and host compilers must support the selected language features.
The first shared-source build will establish that compatibility. No such build
or product test has been executed.

## Supersession

Supersedes: None. Superseded by: None.
