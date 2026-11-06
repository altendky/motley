# Engineering constraints

## Purpose

Keep firmware straightforward, reviewable and correct. These constraints apply
to project-owned application code; SDK boundaries require explicit adaptation.

## Requirements

### Requirement: MOT-ENG-001 — Managed ownership and containers

Application code SHALL use values, references, RAII and standard containers such
as `std::vector`. It SHALL avoid raw pointers, C arrays, manual allocation and
manual resource cleanup. Unavoidable pointer or buffer interfaces imposed by
ESP-IDF and Matter SHALL be isolated in small adapters with explicit ownership,
lifetime and size contracts.

#### Scenario: Adapting an SDK callback

- **WHEN** an SDK API requires a raw context pointer or buffer
- **THEN** the adapter contains that interface and documents its lifetime
- **AND** ordinary application logic operates through managed types

### Requirement: MOT-ENG-002 — Correctness before optimization

Implementation SHALL favor clear control flow, explicit error handling and
defined initialization and failure behavior. Optimization SHALL be justified by
a measured constraint while preserving the agreed behavior. Resource allocation
and synchronization failures SHALL have defined handling.

#### Scenario: A hardware operation fails

- **WHEN** a sensor, bus or output operation returns an error
- **THEN** the caller receives or handles that failure explicitly
- **AND** success is not assumed from a requested operation alone

### Requirement: MOT-ENG-003 — Requirements and verification evidence

Agreed behavior SHALL remain in maintained requirements with stable project IDs.
Implemented requirements SHALL link to specific implementation symbols and relevant
tests where available. Unimplemented requirements SHALL remain visible without
invented implementation links. Mapping, structural analysis and observed test
results SHALL be recorded as distinct evidence.

#### Scenario: Changing a requirement implemented by shared code

- **WHEN** an agreed behavior changes
- **THEN** its implementation links and source consumers are inspected
- **AND** other affected requirements are identified as preservation constraints
- **AND** verification records identify the commands, results and tested content
- **AND** a clean OpenLore report alone is not treated as proof of correctness
