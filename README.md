# Motley

Configurable ESP32-C6 firmware for Home Assistant through Matter over Thread.
The first application is an externally powered controller with remote wired
temperature and humidity sensor heads.

The project is at requirements and tooling setup. Firmware, SDK checkout and
hardware acceptance are not implemented yet.

## Current direction

- Adafruit ESP32-C6 Feather with C++, ESP-IDF and Espressif `esp-matter`.
- Initially four temperature measurements and two humidity measurements, with
  independently configurable locations.
- Adafruit PCA9548 eight-channel STEMMA QT multiplexer and SHT45 breakouts as the
  starting hardware; each identical sensor can have its own port.
- Approximately six feet of four-wire cable per remote branch, subject to testing
  the actual cable and electrical configuration.
- Optional on/off control of an external accessory for a roughly 25 W, 120 V AC
  heater. Switching hardware and any local regulation are not yet selected.
- Safety, correctness, explicit errors, RAII and standard containers before
  optimization. Unavoidable SDK pointer interfaces stay in adapters.

Thread router operation, long battery life and the earlier Velux controller are
future work. The original [planning session](PLANNING_SESSION.md) remains a
historical snapshot; its initial scope, pin table and SDK advice are not the
current specification.

## Requirements

| Domain | Maintained requirements |
| --- | --- |
| Controller and integration | [Platform](openspec/specs/platform/spec.md) |
| Ports, sensor heads and readings | [Wired sensing](openspec/specs/sensing/spec.md) |
| C++ and verification constraints | [Engineering](openspec/specs/engineering/spec.md) |
| Conditional heater output | [Optional output control](openspec/specs/output-control/spec.md) |

These describe intended behavior. All firmware requirements are unimplemented;
there are no production implementation anchors or passing hardware tests yet.
`MOT-*` IDs are retained as requirements evolve.

## Local development tools

Use Node satisfying `package.json` and npm. The npm manifest is development
tooling; firmware will use the ESP-IDF CMake build.

```sh
npm ci
npm run specs:validate
npm run lore:analyze
npm run lore:mapping
npm run lore -- search 'measurement freshness' --specs --json
```

OpenLore 3.5.0 supplies local structural analysis and mapping. OpenSpec 1.16.0
validates the authored requirements. The current agent maintains both documents
and implementation; these commands require no model API key. See
[tooling and limitations](docs/tooling.md) for dependency choices, state retention
and verification.

Once firmware symbols exist, use `npm run lore -- orient --task '<task>' --json`
to retrieve implementation context. The requirements-only repository has no
firmware functions yet; specification search and mapping inspection are usable now.

The C/C++ trial found a current OpenLore limitation: source navigation works,
but requirement-to-function anchors are reported as `not-assessed`. Such links
must be checked manually until that support is added. See the
[validation record](docs/tooling-validation.md) for observed results and gaps.

## Next implementation step

Select and record a compatible SDK set, establish the ESP32-C6 firmware build,
and prove one SHT45 reading through the multiplexer reaches Home Assistant and
recovers after a power cycle. Expand to the configured measurement locations
after that path works. Cable qualification and heater output acceptance remain
separate hardware checks.

Before implementing them, resolve measurement freshness limits, the Matter
representation of unavailable readings, configuration persistence and endpoint
allocation. For heater control, resolve accessory selection and whether initial
operation is manual switching or local temperature regulation.
