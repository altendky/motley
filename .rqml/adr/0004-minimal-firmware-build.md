# ADR-0004: Minimal firmware build in a pinned SDK container

- **Status:** Accepted
- **Date:** 2026-11-07
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-BUILD-001` in [requirements.rqml](../../requirements.rqml)
- **Related ADRs:** [ADR-0002](0002-build-dependencies-and-code-tooling.md)
- **Affected components:** Firmware entry point, SDK build configuration, build runner, artifact verification, pre-commit, CI

## Context

The developer requested a basic do-nothing task to establish a build before
designing functionality. `MOT-BUILD-001` is approved for this narrow milestone.
The broader engineering requirements and proposed architecture remain separate.

## Decision drivers

- Produce an inspectable ESP32-C6 cross-build without connected hardware.
- Use a repeatable SDK environment with a single authoritative image pin.
- Keep generated configuration and artifacts outside the firmware sources.
- Keep the bootstrap application inert and its resource use small.
- Reuse the same build check locally and in CI.

## Options considered

| Option | Benefits | Costs and fit |
| --- | --- | --- |
| Official ESP-IDF container pinned by digest | Supplies matched SDK/compiler/Python/build tools; straightforward CI reuse | Requires Docker and an initial image download |
| Native SDK installation | Direct access to SDK tools and future flashing | Requires separately installing and validating the matched host environment |
| Start with Matter integration | Exercises the future protocol dependency graph immediately | Adds dependencies and behavior beyond the requested first build |

## Decision

Build a separate `firmware/` ESP-IDF project using the official SDK image pinned
in `firmware/toolchain.toml`. That file owns the image selection and chip target.
A small standalone Python runner invokes the image, builds, and verifies
artifacts. Pre-commit exposes it as an explicitly invoked firmware-build check,
and CI invokes that same check.

Reuse the SDK's existing application main task and suspend it. Add no separate
application task, polling loop, sensor access, or protocol initialization.
Compile the owned component in C++23 mode with exceptions and RTTI disabled.
Use SDK defaults for unspecified board settings; a successful chip-target build
does not validate a particular board's flash configuration or peripherals.

Mount firmware sources read-only and put generated `sdkconfig`, compiler
database, and artifacts in a separate writable output directory. Record the
actual target, compiler settings, SDK identification, source/configuration
hashes, and artifact hashes in a build receipt. The runner checks SDK-generated
images with the SDK's own inspection tools.

No managed component manifest or lockfile is needed while the project has no
managed dependencies. Add esp-matter as a separate verified stage later.

## Consequences

The first checkpoint validates the SDK/C++/artifact path. A blocking entry point
is inspected structurally; no board execution is claimed. The image pin fixes
the build environment, while generated build receipts describe observed output.

The source layout and runner are small enough to extend as real functionality
is specified. Hardware boot, commissioning, application watchdog supervision,
memory-fault handling, and portable-core behavior remain pending. The suspended
task is not registered as a watchdog progress source.

## Supersession

Supersedes: None. Superseded by: None.
