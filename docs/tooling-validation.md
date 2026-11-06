# Initial tooling validation

Observed on 2026-11-06 with Node 26.13.0 and npm 12.2.1 on Linux x86-64.
OpenLore 3.5.0 and OpenSpec 1.16.0 were installed locally. This record concerns
tooling and requirements only; it is not firmware or hardware acceptance.

The base commit was `6ee995ecdebdfbb1baac7b95bdce67baae57205e`. All new setup
files were uncommitted working-tree content. The historical planning document
was unchanged, and no new commit was created.

## Observed checks

| Check | Result |
| --- | --- |
| Clean `npm ci --no-audit --no-fund --loglevel=error` using the lockfile and repository npm settings | Passed; 324 packages installed |
| `npm run specs:validate` | All four specifications passed strict validation |
| `npm run lore:analyze` | Built local text and specification indexes without an embedding provider |
| `npm run lore:mapping` | Recognized 12 requirements, all unmapped, with no ambiguous or stale anchors |
| `npm run lore -- search 'measurement freshness' --specs --limit 1 --json` | First result was `MOT-SENS-004 — Measurement validity` |
| `npm run lore -- orient --task 'remote sensor measurement freshness' --json` | Returned matching requirements and no application functions, as expected |
| C/C++ extraction in a disposable fixture | Three functions extracted, including one C function and a C++ call across source files |
| C++ fixture orientation | Returned `read_temperature`, `apply_calibration`, and their caller/callee relationship |
| Explicit C++ requirement anchor | Parsed the correctly formatted anchor, but reported `not-assessed` / `language-not-extracted` |
| Git ignore policy | Analysis is ignored; authored configuration, memory and decision paths are not |

The fixture contained `src/sensor.cpp` with `read_temperature()` calling
`apply_calibration(2500)`, `src/calibration.cpp` defining that function, a shared
declaration header, and `src/status.c` defining `sensor_status(void)`. A separate
requirement used `- **Implementation**:` with the backtick-quoted anchor
`read_temperature::src/sensor.cpp`. No Motley implementation was created to make
this trial pass. The fixture was removed after its results were recorded.

The mapping limitation is material: the source-navigation call graph and the
requirement mapper use different symbol inventories. A successful C++ navigation
query does not establish automatic traceability. The project keeps authored
requirements and records this gap rather than treating it as coverage.

## Tested content

SHA-256 values identify the tested lockfile and requirement content. The config
hash identifies the explicit setup used for the final checks.

| File | SHA-256 |
| --- | --- |
| `package-lock.json` | `df19f860d10da3321cad2d50b30b66670ec6dc1464238b0e992f16d497944d24` |
| `openspec/specs/engineering/spec.md` | `da657336558040ae7521e7bcb3048a0dfb31e03d88459192697b9269d29a8e71` |
| `openspec/specs/output-control/spec.md` | `fff2dbb86f3783943d49cfb03031ddd6be4de7add555e8db842f7c6411fbf29d` |
| `openspec/specs/platform/spec.md` | `475193cccdc74c5286dfc0217350662b0e01c60fc5d30190894edf8557047d0d` |
| `openspec/specs/sensing/spec.md` | `f08e7a141b5be80011f85e0c837c8b140b4a36a34f8990e6a34f6d1d79eb2768` |
| `.openlore/config.json` | `3bdd6dce5da576f1b97f3df06e1686dd658d2ccfca71b32df16583b6e7c0a79c` |

## Remaining work

No firmware build, physical sensor read, cable qualification, Home Assistant
commissioning, reboot recovery or heater test has run. Stable OpenLore identity
through requirement rewrites, anchor relocation and repeated-change behavior
remain to be evaluated. Automatic C/C++ requirement mapping needs additional
support before it can be relied on.
