# Optional output control

## Purpose

Capture constraints for the discussed optional on/off control of an approximately
25 W, 120 V AC heater. Relay accessory selection, wiring, automatic regulation and
implementation remain pending. This specification does not require a heater in
the first sensor-only prototype.

## Requirements

### Requirement: MOT-OUT-001 — External switching hardware

When heater control is enabled, Motley SHALL control an appropriately rated
external switching accessory through its low-voltage interface. The controller
board SHALL NOT directly switch or carry the heater's mains supply.

#### Scenario: Selecting a heater output

- **WHEN** heater switching is added to a controller configuration
- **THEN** the switching accessory and its electrical ratings are identified
- **AND** the controller's GPIO drives only the accessory's low-voltage interface

### Requirement: MOT-OUT-002 — Defined de-energized state

An enabled heater output SHALL initialize to off and remain off until its
configuration is valid and an explicit control action enables it. If automatic
temperature regulation is implemented, its output SHALL turn off when the
controlling measurement is invalid or stale. Software control SHALL NOT replace
independent thermal protection.

#### Scenario: Controller restart

- **WHEN** the controller powers up or resets
- **THEN** the heater output is off before normal control begins
- **AND** output initialization and reset behavior are verified on the chosen hardware

#### Scenario: Feedback failure during automatic regulation

- **WHEN** an enabled automatic controller loses valid temperature feedback
- **THEN** it requests the heater output off
- **AND** the failure is observable
