# ADR-0019: Compiler-aware caches with fresh firmware outputs

- **Status:** Accepted
- **Date:** 2026-11-13
- **Classification:** discretionary_design_choice
- **Related requirements:** `MOT-BUILD-001`, `MOT-BUILD-002`, `MOT-CI-001`, `MOT-CI-002`, `MOT-PLAT-001`
- **Related ADRs:** [ADR-0006](0006-full-commit-build-identity.md), [ADR-0009](0009-matter-device-information-foundation.md)
- **Affected components:** SDK container runner, GitHub Actions firmware job

## Context

Cold hosted firmware builds take approximately 21 minutes. The runner explicitly
disables ccache and the CI job preserves neither compiler results nor component
downloads. The pinned SDK includes ccache 4.9.1; the pinned CHIP CMake integration
forwards IDF's ccache launcher into its GN build.

The developer requested compiler-aware caching and deferral of the separate
firmware/schematic pinout requirement. Existing approved build requirements
already govern this optimization; no new product requirements are introduced.

## Decision drivers

- Reduce repeated SDK and Matter compilation across commits.
- Preserve fresh CI output directories, locked dependencies, offline compilation,
  read-only owned sources, per-commit identity and complete artifact verification.
- Measure cache hits without assuming a particular speedup.

## Options considered

| Option | Benefits | Costs |
| --- | --- | --- |
| IDF-native ccache plus component-manager download cache | Compiler-aware reuse; both systems validate their own inputs | Requires persistent container mounts and GitHub cache transport |
| Restore the entire build directory | Can skip more generation work | Conflicts with the fresh-output requirement and complicates stale configuration/provenance |
| Reuse a finished firmware bundle | Avoids compilation | Does not establish the current checkout's embedded identity or execution evidence |

## Decision

Enable IDF's native ccache integration and give ccache and the component manager
explicit writable cache directories. Keep ccache's correctness defaults and
bound its size. An environment-selected external cache directory lets CI restore
these caches separately from its fresh build directory. Local builds may keep
their caches inside the designated output directory.

Use the existing pinned GitHub cache action only to transport those native
caches. Partition by SDK/toolchain identity and architecture; prefer matching
dependency/configuration inputs while allowing ccache to validate compatible
older compiler entries. Save evolving compiler snapshots under distinct commit
keys. Successful main builds seed default-branch caches that PR and Mergify queue
builds can restore; one PR's private cache is not assumed visible to another.

Always configure, build, link, generate a new receipt and run all existing
verification. Do not cache staged sources, CMake/Ninja output, sdkconfig, receipts
or bundles. Expose compiler statistics and build-phase timings. Invoke the same
build-runner script directly in CI so successful build output is visible rather
than hidden by pre-commit's normal success-output capture; retain the local hook.

## Consequences

Warm builds still pull the pinned container, configure, link and verify. Private
ESP-Matter precompiled-header work may remain uncacheable under strict defaults.
Changing commit identity should rebuild the application/description files while
allowing unchanged SDK objects to be reused. Qualify this with fresh output
directories and different commit identities, not only a same-commit rerun.

GitHub cache eviction or a miss must leave a working cold-build path. Cache
transport and timing improvements remain unmeasured until observed; no speedup
or equivalence claim follows from enabling a cache alone.

## Supersession

Supersedes: None. Superseded by: None.
