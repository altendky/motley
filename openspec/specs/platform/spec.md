# Platform

## Purpose

Define Motley's initial controller and integration scope. These are intended
requirements; firmware implementation and hardware verification are pending.

## Requirements

### Requirement: MOT-PLAT-001 — ESP32-C6 and supported Matter SDK

Motley SHALL initially target the Adafruit ESP32-C6 Feather, using modern C++
with ESP-IDF and Espressif's `esp-matter`. The build SHALL identify a compatible,
pinned ESP-IDF, esp-matter and connectedhomeip combination.

#### Scenario: Reproducing a firmware build

- **WHEN** a developer prepares the documented firmware toolchain
- **THEN** the required SDK revisions and target are explicit
- **AND** the build does not silently select moving upstream branches

### Requirement: MOT-PLAT-002 — Home Assistant integration

Motley SHALL expose configured temperature and humidity measurements to Home
Assistant through Matter over Thread. Each measurement SHALL have a stable
identity across controller restarts with unchanged configuration. Commissioning
state SHALL survive ordinary power cycles.

#### Scenario: Reporting after a power cycle

- **WHEN** a commissioned controller loses power and restarts
- **THEN** it reconnects without requiring a factory reset or recommissioning
- **AND** Home Assistant can read and subscribe to its configured measurements
- **AND** reporting is verified at Home Assistant, rather than inferred solely
  from successful local SDK calls

### Requirement: MOT-PLAT-003 — Initial scope and future capabilities

The initial platform SHALL support an externally powered controller with wired
sensor heads. Thread router operation and long battery life SHALL remain future
capabilities to evaluate, rather than initial acceptance criteria.

#### Scenario: Accepting the first sensor controller

- **WHEN** wired sensing and Home Assistant reporting are demonstrated
- **THEN** initial acceptance does not depend on router operation or a battery
  lifetime target
