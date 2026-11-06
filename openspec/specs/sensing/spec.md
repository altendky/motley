# Wired sensing

## Purpose

Provide flexible remote temperature and humidity measurements without requiring
special arrangements of sensor addresses or overlapping measurement locations.
Implementation and physical cable validation are pending.

## Requirements

### Requirement: MOT-SENS-001 — Independent measurement locations

Motley SHALL support an initial configuration with at least four temperature
measurements and two relative-humidity measurements. Configuration SHALL describe
each sensor's location, model and enabled measurements. Temperature and humidity
locations SHALL be independently configurable; a combined sensor MAY provide both.

#### Scenario: Separate temperature and humidity locations

- **WHEN** four temperature locations and two different humidity locations are
  configured
- **THEN** each measurement is associated with its configured location
- **AND** the configuration does not require paired temperature/humidity locations

### Requirement: MOT-SENS-002 — Multiplexed ports

The initial design SHALL support an Adafruit PCA9548 eight-channel STEMMA QT
multiplexer and SHT45 sensor breakouts. Identical fixed-address sensors SHALL be
usable on separate channels. A configured bus path SHALL identify each multiplexer
address and selected channel, allowing later expansion without treating the
sensor's I²C address as its unique identity.

#### Scenario: Two identical sensor addresses

- **WHEN** two SHT45 sensors occupy separate channels of one multiplexer
- **THEN** each is read using its configured bus path
- **AND** channel selection prevents the other sensor from responding to that read

#### Scenario: Describing an expanded bus

- **WHEN** a later design uses parallel or cascaded multiplexers
- **THEN** a sensor can be identified by the complete ordered bus path
- **AND** accepting that configuration still requires electrical and driver validation

### Requirement: MOT-SENS-003 — Remote wired sensor heads

Sensor heads SHALL connect by a four-conductor cable carrying power, ground, SDA
and SCL to the controller or its expansion board. The initial cable validation
target SHALL be approximately six feet per remote branch. Compatibility SHALL be
established for the actual cable, supply, bus timing and installed sensor assembly.

#### Scenario: Qualifying the standard sensor cable

- **WHEN** the proposed six-foot cable and enclosed sensor head are tested
- **THEN** successful and failed reads are observed under representative operation
- **AND** any required timing, pull-up or signal-conditioning constraints are recorded
- **AND** the multiplexer is not assumed to regenerate signals or reset cable limits

### Requirement: MOT-SENS-004 — Measurement validity

Motley SHALL distinguish successful, failed and stale measurements. It SHALL NOT
publish a failed read as a new valid reading. Freshness limits and the external
representation of unavailable measurements SHALL be explicit before acceptance.

#### Scenario: A remote sensor is disconnected

- **WHEN** a previously readable sensor stops responding
- **THEN** its failure and measurement freshness are observable
- **AND** its last value is not presented indefinitely as a fresh measurement
- **AND** other sensor ports continue operating
