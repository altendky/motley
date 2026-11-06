# Motley

Configurable ESP32-C6 firmware for Home Assistant through Matter over Thread.
The first application is an externally powered controller with remote wired
temperature and humidity sensor heads.

This branch evaluates **RQML** as an alternative to the
[OpenLore/OpenSpec setup in PR #2](https://github.com/altendky/motley/pull/2).
It starts from the same planning-only `main` and preserves the same 12 requirements
and 14 acceptance scenarios. It does not layer RQML over OpenLore or select a
source-navigation companion.

## Current direction

- Adafruit ESP32-C6 Feather with modern C++, ESP-IDF and Espressif `esp-matter`.
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
historical snapshot, not the current specification.

## Requirements

The authoritative [requirements.rqml](requirements.rqml) uses schema 2.2.0 and
native IDs for requirements and acceptance criteria. Four packages contain:

| Domain | Requirement IDs |
| --- | --- |
| Controller and integration | `MOT-PLAT-001` through `MOT-PLAT-003` |
| Ports, sensor heads and readings | `MOT-SENS-001` through `MOT-SENS-004` |
| C++ and verification constraints | `MOT-ENG-001` through `MOT-ENG-003` |
| Conditional heater output | `MOT-OUT-001` and `MOT-OUT-002` |

All firmware requirements are unimplemented and unverified. Scenario criteria are
acceptance intent, not executed tests. Four explicit domain goals organize the
declared graph; they do not provide source dependencies or implementation evidence.

## Local tools

Use Node satisfying `package.json` and npm. Firmware will use ESP-IDF's CMake build.

```sh
npm ci
npm run requirements:validate
npm run requirements:lint
npm run rqml -- show MOT-SENS-004 --spec requirements.rqml
npm run rqml -- impact MOT-SENS-004 --spec requirements.rqml --json
npm run rqml -- matrix requirements.rqml --json
```

`npm run requirements:check` runs the strict coverage/drift gate. It currently
**exits 2**, reporting 12 unimplemented and 12 unverified requirements. Validation
and lint pass. That distinction is intentional: no placeholder implementation or
test links are added to make coverage appear complete.

RQML links C++ files and detects file drift, but it does not validate `#function`
fragments or discover C++ dependencies. Requirement edits do not automatically
invalidate old implementation baselines, and `verifiedBy` links do not establish
test freshness or execution. See [tooling](docs/tooling.md) and the
[comparison and validation record](docs/tooling-validation.md).

## Codex integration

`.codex/config.toml` enables the locally pinned RQML MCP server. The repository
marketplace in `.agents/plugins/marketplace.json` also selects a pinned revision
of the upstream RQML Codex plugin for its skills and hooks. Its bundled MCP
launcher is disabled so the local, locked server is the only RQML server.

From the repository root, run `npm ci`, then `npm run codex`. This puts the RQML CLI
on PATH for the plugin hooks. Codex must be installed separately. Reload/restart
Codex after changing repository configuration, and use its plugin and MCP views
to confirm the integration is loaded. Project configuration requires a trusted
project; hooks additionally require the normal host trust review.

The plugin is cached by Codex outside the repository. It uses standard checking
by default; the project's separate strict check remains an unmet completion gate.
See [tooling](docs/tooling.md) for setup and verification details.

## Next implementation step

Select and record a compatible SDK set, establish the ESP32-C6 firmware build,
and prove one SHT45 reading through the multiplexer reaches Home Assistant and
recovers after a power cycle. Cable qualification and heater output acceptance
remain separate hardware checks.

Before implementation, resolve measurement freshness limits, unavailable-reading
representation, configuration persistence and endpoint allocation. For heater
control, resolve accessory selection and manual versus local temperature control.
