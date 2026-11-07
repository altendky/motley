# ADR-0002: Native firmware tools and an independent C++ host build

- **Status:** Proposed
- **Date:** 2026-11-07
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-ENG-004`, `MOT-ENG-005`, `MOT-ENG-006`, `MOT-ENG-007` in [requirements.rqml](../../requirements.rqml)
- **Related ADRs:** [ADR-0001](0001-portable-core-and-adapters.md), [ADR-0003](0003-bounded-memory-and-fault-supervision.md)
- **Affected components:** Build configuration, dependency declarations, host tests, firmware build, code analysis, pre-commit, CI

## Context

Motley needs a firmware build for ESP32-C6 and a separate host build of its
portable C++ core. Project tooling should make dependencies and build settings
reviewable, while using the SDK's supported firmware integration.

The repository already uses Mise, pre-commit, and GitHub Actions. No firmware
SDK, host product test suite, or C++ project dependencies have been installed
for Motley. A temporary host compatibility probe has run; its limited evidence
is recorded below.

## Decision drivers

- Build the same core sources for a host and the controller.
- Keep routine core tests independent of firmware SDK installation.
- Use a supported Matter/Thread firmware dependency route.
- Give each dependency and tool selection one authoritative declaration.
- Check owned C++ code with two compilers, executable tests, and analysis.
- Keep project checks in pre-commit and reuse them in CI.

## Options considered

| Option | Benefits | Costs and fit |
| --- | --- | --- |
| Native ESP-IDF with managed esp-matter; ordinary CMake host project | Uses the documented product-application route and keeps host testing independent | Two build environments need explicit boundaries and coordinated core settings |
| Full esp-matter SDK checkout with an independent host project | Provides source customization, examples, and additional SDK host tools | Larger source/tool setup; justified when those capabilities are required |
| PlatformIO as the outer project manager | Offers a common project interface and environment configuration | Its supported package set and integration need separate validation; adds another owner around the chosen SDK workflow |
| Conan or vcpkg for portable C++ dependencies, alongside the IDF component manager | Provides package/version/profile management for a growing C++ dependency set | Adds another package system and host/target integration; the initial host test dependency does not yet justify it |

The alternatives are not declared incompatible. Their additional integration
has not been validated for Motley.

## Decision

Propose the following starting stack:

| Responsibility | Tool or approach | Authoritative configuration |
| --- | --- | --- |
| Owned C++ language level | Explicit C++23 for the core and owned adapters | CMake targets and owned firmware-component build settings |
| Firmware SDK | Native ESP-IDF plus the managed esp-matter component | Selected SDK release and component manifest/lock |
| Target compiler, firmware CMake/Ninja, and SDK Python environment | Espressif's tools for that SDK release | SDK tool manifest and installation metadata |
| Host build | CMake with Ninja | CMake targets and shared `CMakePresets.json` |
| Host test execution | CTest with Catch2 | Test targets and pinned test dependency |
| Firmware component dependencies | IDF Component Manager | `idf_component.yml` and generated `dependencies.lock` |
| Initial host-only dependency acquisition | CMake FetchContent with a fixed source archive and SHA-256 | CMake dependency declaration |
| General development tools | Mise | `mise.toml`, `mise.lock`, and associated lock graphs |
| Formatting | clang-format on owned C++ | `.clang-format` and a pinned tool version |
| Static analysis | clang-tidy on the core's host compilation database first | `.clang-tidy`, compiler database, and a pinned tool version |
| Runtime diagnostics | Host AddressSanitizer and UndefinedBehaviorSanitizer build | Host CMake preset/target options |
| Repository checks | Pre-commit, invoked by GitHub Actions | `.pre-commit-config.yaml` and CI workflows |

Select one published esp-matter release and its documented compatible ESP-IDF
and connectedhomeip combination. The managed package is the first delivery route
to validate. Exact selections belong in executable configuration and locks;
this record does not maintain a second list of version pins.

Use the SDK's matching RISC-V cross-compiler for firmware. A host GCC installation
does not substitute for it. Explicitly install the SDK-recommended firmware
CMake/Ninja versions instead of assuming the general host versions are the
SDK-tested set. Configure and build the host without activating the firmware
SDK. Keep host and firmware build directories and compilation databases separate.

Use an SDK-owned Python virtual environment for SDK packages, and validate the
bootstrap interpreter against the selected SDK's complete constrained package
set. The virtual environment isolates packages but does not select a different
Python interpreter automatically. The SDK's release constraints can be downloaded
separately from its source; record the actual constraints/package-resolution
evidence when validating the environment. An SDK source revision alone does not
establish that this Python package resolution is frozen.

C++23 is a deliberate project baseline, not a request to inherit the SDK's
language default. The evaluated SDK release defaults to a newer language mode.
Inspect actual compile commands for owned sources: declaring an "at least
C++23" CMake feature alone need not lower an existing newer default. Validate
the intended library features on both real compiler/library combinations.

The developer agreed to Rust-style typed results for recoverable operational
failures. `MOT-ENG-006` captures that policy, with detailed acceptance criteria
still draft. Use `std::expected<T, E>` or `std::expected<void, E>` at
application-owned boundaries, with typed errors and `[[nodiscard]]` on those
functions. Diagnose unacknowledged discarded results as build errors.

Use domain-appropriate error enums; `std::variant` can carry alternatives with
different payloads when needed. Handle or propagate results explicitly. The
standard chaining operations can support composition without introducing a
project-specific error framework or a macro-based propagation convention.
SDK-imposed callback and C signatures remain in adapters, where their results
are translated to application-owned types.

The developer subsequently agreed to exceptions-disabled production code and
dependency compatibility checks, captured in `MOT-ENG-007`; its detailed
acceptance criteria remain draft. Compile owned production sources without
exception handling in both the firmware and host core builds. Host test
frameworks may use exceptions internally, with no unwinding through the core.

The inspected ESP-IDF configuration defaults to exceptions disabled, and the
identified Matter revision has a compatible default. Prefer small RAII adapters
around SDK error-code APIs. The optional `esp-idf-cxx` I2C wrapper explicitly
requires exceptions and is not suitable for this production policy. Check the
actual resolved dependency configuration and used failure paths during the
firmware build; source defaults do not establish the final flags or behavior.

Disabling exceptions does not make allocating standard containers report
failures through an application result type. The inspected IDF configuration
aborts on libstdc++ paths that would throw. The developer has agreed to bounded
memory with static/stack preference and hard failures for memory faults;
`MOT-ENG-008`, `MOT-ENG-009`, and proposed ADR-0003 carry that direction forward.
RTTI is intended to be disabled by default for owned production code. Revisit
that preference if a concrete library or design need appears; it is not a
blanket dependency ban. Exact memory budgets and panic/watchdog/reset
configuration remain open. The broader tooling stack in this record remains
proposed.

Catch2 is a host test dependency; it is not proposed as a firmware dependency.
Fetch it from a fixed, hash-checked source archive initially. Move to a package
manager if the portable dependency graph, binary reuse, or distribution needs
justify one. Configure missing dependencies explicitly; do not silently use an
unrelated system installation instead of the pinned source.

Apply warnings and analysis to owned targets. Do not impose owned-code warning
policies on third-party SDK sources. Formatting checks cover owned files only.
Host presets should support a GCC build, a Clang build, and a sanitized Clang
build. Select the initial compiler versions and CI platform when implementing
these configurations.

Expose the project checks through pre-commit. Lightweight formatting checks can
run on changed files; build/test and analysis hooks need their configured host
environment. Firmware compilation needs a prepared SDK environment and can use
an explicitly invoked hook in CI. CI should exercise those same checks, retain
the existing aggregate job, and report build/test results independently of RQML
trace coverage. A pinned container is an optional reproducible build environment;
Docker is not required for the ordinary core build by this proposal.

## Consequences

The SDK owns its firmware toolchain and component resolution; CMake owns the
portable build; Mise owns general tools. There is no single additional C++
project manager in the initial proposal.

The initial dependency graph stays small. Source-archive pins need explicit
updates and cache handling; FetchContent does not supply a general dependency
solver/lockfile. IDF's lockfile covers its component graph, not the separate
host test dependency. Upgrade automation must follow those distinct declarations.

The proposed source layout is a `core/` library with `tests/`, and a separate
`firmware/` IDF project that incorporates the same core sources. Add `cmake/`
helpers only when needed. This layout has not been created. Avoid coupling the
root host configure step to an SDK environment check.

The missing firmware SDK, actual target feature checks, Catch2 integration,
clang-tidy availability, and complete clean-build workflow still need validation.
Firmware clang-tidy is a separate integration: Espressif's current path uses its
Clang toolchain and is not assumed to be a drop-in check on a GCC firmware build.

### Evidence and limits

On 2026-11-07, a temporary CMake/Ninja probe compiled and ran with host GCC and
Clang in explicit C++23 mode. It exercised `std::expected`, `std::span`,
`std::variant`, and `std::vector`, with owned-target warning checks enabled.
Configure, build, and CTest execution exited 0 for both compilers.

Checked temporary source SHA-256:
`9b928208eae448d77180677955702ec8190d082d0c6f42fffd634ef02a2eed39`.
Checked temporary CMake configuration SHA-256:
`1aa9573c836f19f2d7fe029be9920b1e5c2fbebd517208e898340f521cfe6548`.

The Clang AddressSanitizer/UndefinedBehaviorSanitizer build compiled, but its
first test execution failed because LeakSanitizer could not run under the
sandbox's process-inspection restrictions. The same instrumented executable
passed through CTest outside the sandbox, exit 0, without disabling leak checks.

This checks local tool/library availability only. It is not a product test,
target cross-build, Catch2 test, allocation-failure test, or implementation of
`MOT-ENG-004` or `MOT-ENG-005`; no implementation or verification traces are added.
The probe used the host's current exception/RTTI defaults and does not establish
agreement with the future firmware error policy.

### Primary references

- [Espressif setup and SDK delivery routes](https://docs.espressif.com/projects/esp-matter/en/latest/esp32c6/developing.html)
- [Published managed esp-matter component compatibility](https://components.espressif.com/components/espressif/esp_matter/versions/1.6.1/readme)
- [ESP-IDF C++ configuration](https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32c6/api-guides/cplusplus.html)
- [SDK exception-disabled failure behavior](https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32c6/api-reference/kconfig-reference.html#config-compiler-cxx-exceptions)
- [Inspected Matter compiler configuration](https://github.com/project-chip/connectedhomeip/blob/b1902b39ac/build/config/compiler/BUILD.gn#L645-L659)
- [Optional I2C wrapper's exception requirement](https://github.com/espressif/esp-idf-cxx/blob/main/include/i2c_cxx.hpp#L9-L10)
- [Catch2 exception-disabled limitations](https://github.com/catchorg/Catch2/blob/devel/docs/configuration.md#disabling-exceptions)
- [Evaluated SDK language defaults](https://github.com/espressif/esp-idf/blob/v6.0.2/tools/cmake/build.cmake)
- [SDK tool and environment management](https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32c6/api-guides/tools/idf-tools.html)
- [Evaluated SDK tool selections](https://github.com/espressif/esp-idf/blob/v6.0.2/tools/tools.json)
- [Component-manager lockfile rules](https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/dependencies_lock.html)
- [CMake shared and local presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
- [CMake FetchContent](https://cmake.org/cmake/help/latest/module/FetchContent.html)
- [Catch2 CMake/CTest integration](https://github.com/catchorg/Catch2/blob/devel/docs/cmake-integration.md)
- [Standard expected result type](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p0323r12.html) and [chaining operations](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2505r5.html)
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) and [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
- [ESP-IDF clang-tidy integration](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/tools/idf-clang-tidy.html)

## Supersession

Supersedes: None. Superseded by: None.
