# Motley plan

## Readiness

### Requirements-first workflow

**IMPLEMENTED:** the developer permits unfinished requirements and prefers agreed
requirements before maintained implementation, with scoped exceptions while
learning the workflow. `MOT-PROC-001` and `MOT-PROC-002` capture that policy;
ADR-0008 records the supported gate configuration and its review boundaries.

- [x] Update `AGENTS.md` and `docs/tooling.md` with the default review/mapping
  workflow and explicit exceptions; preserve the visible backlog.
- [x] Use standard consistency checking plus an unconditional mapped-approval
  gate in `.pre-commit-config.yaml`, retaining schema validation and strict lint.
- [x] Verify allowed unfinished coverage and rejected drift, invalid specs, and
  premature mapped implementation using disposable fixtures; record evidence,
  trace real policy/configuration artifacts, and run full pre-commit checks.

Policy verification on 2026-11-07 used the pinned RQML CLI, version 0.11.0.
Disposable fixture runner exited 0 after observing:

- Both draft and approved unimplemented/unverified requirements: standard
  `rqml check` exit 0 and approval gate exit 0; optional strict check exit 2.
- Approved linked implementation: standard check exit 0; changing or removing
  that implementation: standard check exit 2.
- Implementation mapped to a draft requirement: standard check exit 0, separate
  `rqml gate --spec <fixture>` exit 2.
- Invalid specification: standard check exit 1.

Fixture setup was corrected for the CLI's empty-trace append handling and the
document-validation exit code before the successful run. Fixtures were removed;
the temporary verification script and log remain available for review. Script
SHA-256: `996d3b9c11a66c7932b07db3422dd1b6e7959eeaf1cdc0ff6bf3bdf3f9b4162a`.
Tested `.pre-commit-config.yaml` SHA-256:
`45293898abe2b170d9c3b0aea4db6384797d965dc94e061824ccba7333883fba`.
Reviewed `AGENTS.md` SHA-256:
`fe72cb1bbb9d9155d13dba8585dddd86e66b232b60f9b8146c148f200a21525d`.

The current nine files under `firmware/` and `scripts/` all have implementation
or verification mappings to the relevant build/CI requirements. This inventory
supports source review; it is not a behavioral reverse-coverage guarantee.
The new approval hook examines the entire declared mapping, not just changed
paths. Unlinked implementation remains a review responsibility.

`mise exec -- pre-commit run --all-files` passed, exit 0, including metadata tests,
schema validation, strict semantic lint, standard consistency, and approval gate.
RQML standard check also passed with no drift or premature implementation.
Coverage gaps remain visible through status/matrix, including pending hosted CI
verification and six draft engineering requirements. Prior strict failures below
are historical evidence under the previous completeness policy.

**COMPLETE: minimal cross-build milestone (`MOT-BUILD-001`).**

The developer requested an idle-task build before functional design.
`MOT-BUILD-001` is approved and ADR-0004 records its implementation approach.
The application behavior below remains planning work beyond this bootstrap.

`MOT-ENG-004` and `MOT-ENG-005` capture the agreed portable-core direction;
`MOT-ENG-006` captures the agreed typed-result policy for recoverable failures.
`MOT-ENG-007` captures exceptions-disabled production code and dependency
compatibility checks. `MOT-ENG-008` and `MOT-ENG-009` capture bounded memory
and hard-failure handling for detected memory faults.
Their detailed acceptance criteria are draft. The approved bootstrap does not
claim to implement or verify those broader requirements.

The proposed scope, artifact boundaries, and open decisions are in
[the project planning brief](../docs/project-planning.md).

## Build identity and artifact stage

### Size-limited standard-field clarification

The developer permits abbreviated hashes in constrained standard fields when
the full hash remains present and available. ADR-0007 supersedes ADR-0006's
neutral SDK label; the verified full custom descriptor is preserved.

- [x] Restore a useful abbreviated SDK version label and inspect it against
  full identity; keep receipt identity, artifact names, and output full-length.
- [x] Test constrained labels and shared prefixes, build, reverify, refresh
  reviewed traces, and run required pre-commit checks.

Verification on 2026-11-07: 23 tests passed, exit 0, including the SDK field's
31-character payload bound and shared-prefix labels remaining distinguishable
through full identities. The SDK build check passed, exit 0, using an incremental
cache copied from the prior successful build. `--verify-only` passed, exit 0,
before this documentation/trace update and preserved receipt SHA-256
`a4b64feca91e5971655ff121a3a652ee2640144ab4dcd7253990a36c20c71205`.
The SDK label is `g3b28ebbba0f8-dirty`; full identity
`g3b28ebbba0f809f309db964c0e7e08506eeccc66-dirty` remains verified in both ELF
and image, and remains the receipt/artifact identity.

Input fingerprint: `f8747e121d9d3b002f5600ee9e4e0f3d4c634c558a71f3d54609ac415da8c7ac`.
Test source SHA-256: `e1f3f3e54d07a55bc05cb45f73547a37e303b54284be07ee175ec8dd2a91fe9d`.
Implementation hashes are preserved in the reviewed trace baselines and receipt.
RQML standard check passes; full pre-commit retains the same strict coverage gaps
for pending hosted CI verification and the six draft engineering requirements.

### Full-hash correction

The developer requires full commit hashes throughout build identities and
artifact names. `MOT-BUILD-002` and `MOT-CI-002` retain their IDs with corrected
acceptance. ADR-0006 supersedes ADR-0005's abbreviated identity design.

- [x] Use the complete Git hash in all build identities and artifact names.
- [x] Embed a retained custom description containing full hash/cleanliness;
  keep the SDK's size-limited version field neutral, with no abbreviated hash.
- [x] Test hashes sharing a prefix and reject truncated/missing/malformed records;
  run the SDK build and reverification against ELF and binary output.
- [x] Record current evidence, review affected trace links, and run pre-commit.

Full-hash verification on 2026-11-07 supersedes the abbreviated-identity evidence
below. `mise exec -- uv run scripts/test_firmware.py` passed 23 tests, exit 0.
The SDK build check passed, exit 0, after correcting a generated-header template
path exposed by SDK component scanning. The allocated ELF descriptor and
application image both contain
`g3b28ebbba0f809f309db964c0e7e08506eeccc66-dirty` without truncation. The linker
map retains `motley_build_identity` as a 73-byte custom descriptor. `app_main`
still only suspends. SDK version metadata uses `see-build-identity`.

`mise exec -- uv run scripts/firmware.py --build-dir <output> --verify-only`
passed, exit 0, before this documentation/trace update, preserving the version-3
receipt SHA-256 `267f39369eba36455f108b3b6f49468e08511560b376f576e38e69620591e967`.
Input fingerprint:
`2ebe172a6ba59a840235ec56b7663978c7002b0ce53fe15409d6565ca6913d47`.
Application image: 126,304 bytes, SHA-256
`0f9d18971bbaae2afd269a6758ec2ceb7a4e24bc66ecd0b5bbc94d1b56fe5703`.
Test source SHA-256:
`191563cd15615043d934a17d1b9bdced391497d7b83587fed471684ba54b82c8`.
The receipt and refreshed implementation baselines record current input hashes.
Hosted CI and hardware verification remain pending. The known strict coverage
gaps below are preserved; no verification links are fabricated for them.

**IMPLEMENTED AND LOCALLY VERIFIED; hosted CI execution pending.** The developer
approved the proposed identity fields and artifact set. ADR-0005 records the
design. `MOT-BUILD-001` behavior and existing draft engineering requirements are
preserved.

- [x] Implement metadata snapshot, CI checkout classification, immutable
  receipts, embedded version, and curated bundle (`MOT-BUILD-002`).
  Files: `scripts/build_metadata.py`, `scripts/firmware.py`,
  `firmware/CMakeLists.txt`, `docs/firmware-build.md`.
- [x] Maintain the same local/CI firmware check and add verified bundle and
  failed-diagnostic uploads (`MOT-CI-001`, `MOT-CI-002`).
  Files: `.github/workflows/ci.yml`, `.pre-commit-config.yaml`.
- [x] Run meaningful metadata/provenance failure fixtures, fresh cross-build,
  image-version and bundle inspection, and receipt reverification.
  Files: `scripts/test_firmware.py`; command: `mise exec -- uv run scripts/test_firmware.py`.
- [x] Record reviewed implementation/verification links and hashes and run full
  pre-commit checks. Preserve the known strict-coverage findings below.
- [ ] Observe a hosted CI build, aggregate failure handling, artifact upload,
  and download before recording verification links for `MOT-CI-001` and
  `MOT-CI-002`. No service execution evidence is claimed by local checks.

### Identity/artifact verification, 2026-11-07

- `mise exec -- uv run scripts/test_firmware.py`: exit 0, 20 tests. Fixtures
  cover actual Git identity/branch state, staged/unstaged/untracked/ignored/output
  handling, input fingerprints, ancestor/missing-object results, fork PR context,
  PR head versus merge/queue evidence, bad compiler/configuration/image identity,
  malformed or mismatched flash arguments, bundle corruption/missing files,
  source changes invalidating prior success, and immutable receipt reverification.
  Temporary Git clones reuse the existing full local history; no commits created.
- `MOTLEY_BUILD_DIR=<fresh-output-directory> mise exec -- pre-commit run --hook-stage manual firmware-build --all-files`:
  exit 0 from an empty output directory using the pinned SDK. The embedded and
  inspected version is `g3b28ebbba0f8-dirty`, branch `planning/project`.
- `mise exec -- uv run scripts/firmware.py --build-dir <same-output-directory> --verify-only`:
  exit 0; original receipt SHA-256 remained
  `c4971a5dd2c9febc75584fc01c390cb3bd21f34878f943b1430d4edb8f374b9a`.
  This check ran against the checkout snapshot recorded in that receipt, before
  this subsequent documentation update.
- Versioned receipt input fingerprint:
  `102904451bf821fd3d7c9400e3c78000b66be108e454aaa4e5de75f4980b6b3a`.
  Application image: 126,224 bytes, SHA-256
  `ee532153c3aca79d98826b6fa7682205733ea482163421c798f70b9c7900f48a`.
  The receipt contains every bundled file's size/hash and all tested input hashes.
- Read-only review found unvalidated plain-text flash arguments. The final
  verifier checks their options and offset/path mappings against JSON metadata;
  negative fixtures and the final actual SDK build exercise this fix.
- Local workflow syntax validation passed. The upload action is pinned to a
  reviewed published revision. Hosted upload/download and hardware execution
  remain untested; no verification edges were fabricated for those outcomes.
- RQML standard check passes with no drift, changed context, premature
  implementations, or missing approved implementations. Full pre-commit exits 1
  because inner strict `rqml-check` exits 2: `MOT-CI-001` and `MOT-CI-002` have no
  verification edge, and `MOT-ENG-004` through `MOT-ENG-009` still lack implementation
  and verification. Other observed hooks pass.

| Tested artifact | SHA-256 |
| --- | --- |
| `scripts/firmware.py` | `f709e7057ce967168b3aba55a201bffe98756c314676816411d8b1bfc9255255` |
| `scripts/build_metadata.py` | `ea0b850eb050d9fd4f885f9e977bf2afe404a8f311e73f0910f73bd7d786e21e` |
| `scripts/test_firmware.py` | `180d31fbdb00d1abce0a86ced7a274a629f807f7ff7428ae2082e6ef33ce9edb` |
| `.github/workflows/ci.yml` | `23920c809f31146e629c5206f3fd84df15c047f42487f0517f93e48983c6e888` |

## Completed bootstrap stage

- [x] Specify and approve the requested idle-task build as `MOT-BUILD-001`.
- [x] Record the pinned SDK-container approach in ADR-0004.
- [x] Create the minimal firmware target.
  - Goal: an ESP32-C6 C++ application whose existing SDK main task suspends.
  - Requirements: `MOT-BUILD-001`; apply the agreed engineering direction without
    claiming completion of the draft core/fault requirements.
  - Files: `firmware/CMakeLists.txt`, `firmware/main/CMakeLists.txt`,
    `firmware/main/app_main.cpp`, `firmware/sdkconfig.defaults`,
    `firmware/toolchain.toml`.
- [x] Add a repeatable build and artifact check.
  - Files: `scripts/firmware.py`, `.pre-commit-config.yaml`,
    `.github/workflows/ci.yml`, `docs/firmware-build.md`.
  - Verification: a clean `firmware-build` pre-commit manual hook, effective
    C++ flags, target metadata, ELF/image inspection, SDK size report, and
    rejection of invalid/missing artifacts.
  - Record real `implements` links to the firmware/build configuration and
    `verifiedBy` to the artifact verification function after observing execution.
- [x] Run a clean build, inspect outputs, review the diff, and record evidence.
  - Command: `MOTLEY_BUILD_DIR=<fresh-output-directory> mise exec -- pre-commit run --hook-stage manual firmware-build --all-files`.
  - Finish with full pre-commit checks and report remaining draft-requirement
    coverage gaps. Hardware execution remains untested until a board is used.

## Planning work

- [x] Inspect the maintained specification and distinguish it from historical
  planning research.
- [x] Document proposed ownership of requirements, architectural decisions,
  implementation plans, explanations, and executable configuration.
- [x] Agree the first application direction: temperature/humidity measurements
  exposed to Home Assistant through Matter over Thread.
- [x] Recover the original Codex hardware and engineering discussion and
  distinguish user choices, tentative counts, agent proposals, and later
  tooling-only specification cleanup in the planning brief.
- [x] Agree host-testability and an explicit core/environment boundary as
  requirements; draft `MOT-ENG-004` and `MOT-ENG-005` with acceptance criteria.
- [x] Propose the supporting core/adapters architecture in ADR-0001.

## Active software planning

- [x] Develop a concrete code/build/dependency/test-tooling proposal in ADR-0002
  and check basic host C++23 compiler and sanitizer availability.
- [x] Agree typed results for recoverable failures, with `std::expected`, typed
  errors, `[[nodiscard]]`, and diagnostics for unacknowledged discarded results;
  draft `MOT-ENG-006` and update the tooling rationale.
- [x] Agree exceptions-disabled production code, compatible dependency use,
  and separation from host test-framework exceptions; draft `MOT-ENG-007`.
- [x] Agree static/stack preference, limited bounded allocation, and hard
  failures for detected memory faults; draft `MOT-ENG-008` and `MOT-ENG-009`.
- [x] Verify documented ESP32-C6 watchdog availability and propose memory/fault
  supervision in ADR-0003, keeping reset policy and timeouts undecided.
- [x] Record RTTI disabled as the intended default, revisitable for a concrete
  library or design need.
- [ ] Settle ADR-0002's remaining tooling choices, then turn them into
  executable configuration.
- [ ] Define numerical memory budgets and settle ADR-0003's fatal diagnostics,
  panic/reset behavior, watchdog progress criteria, and timing from bounded work.
- [ ] Review the precise statements and acceptance criteria of `MOT-ENG-004`,
  `MOT-ENG-005`, `MOT-ENG-006`, `MOT-ENG-007`, `MOT-ENG-008`, and `MOT-ENG-009`,
  then record their lifecycle approval when agreed.
- [ ] Settle ADR-0001, including application-core, runtime, and adapter
  responsibilities.
- [ ] Select the firmware dependency route and compatible SDK release set.
  Native ESP-IDF with the managed esp-matter component is the initial candidate;
  compare full-source delivery when required tooling or modifications warrant it.
- [ ] Select the host C++ language level, build/test tools, dependency locking,
  and compiler checks against that SDK set.
- [ ] Record the tooling decision and an executable first implementation stage
  with real build/test commands once these choices are settled.
- [ ] Add architecture and developer setup documentation when there is an
  implemented architecture and exercised setup to describe.

The current discussion prioritizes code and project tooling. Configuration and
measurement-state behavior are subsequent requirements work, not the next
tool-selection decision. ADR-0002 proposes tool ownership and build structure;
it is not an accepted implementation plan.

## Deferred and remaining planning

- [ ] Specify the first core behavior and its success/failure scenarios before
  implementing it. Sensing/configuration behavior is the candidate; heater
  regulation remains a separate scope decision.
- [ ] Discuss the physical application and hardware before fixing sensors,
  channel counts, or the controller board.
- [ ] Agree the first device's success/failure scenarios and exclusions.
- [ ] Draft its goals and focused requirements with acceptance criteria;
  review them with the developer and record approval only when given.
- [ ] Agree the engineering constraints that apply across the first milestone.
- [ ] Evaluate the firmware and host-test toolchain against that scope, including
  dependency management, reproducibility, and actual host prerequisites.
- [ ] Record significant design choices as ADRs tied to the relevant requirements.
- [ ] Replace this readiness outline with scoped implementation stages once the
  specification and design are sufficient.

## Verification state

The engineering requirements remain unimplemented and unverified. The separate
minimal-build requirement has real implementation links and an executed artifact
verification link. No hardware or host product behavior tests have run. Preserve
the missing draft engineering implementation/test findings; do not add placeholder
links to satisfy the strict completion check.

### Minimal build evidence, 2026-11-07

- `MOTLEY_BUILD_DIR=<fresh-output-directory> mise exec -- pre-commit run --hook-stage manual firmware-build --all-files`: exit 0. Built from an empty output directory with the SDK pin in `firmware/toolchain.toml`.
- `mise exec -- uv run scripts/firmware.py --build-dir <same-output-directory> --verify-only`: exit 0. The original receipt matched current source, verifier, SDK, compiler/configuration metadata, and artifact hashes.
- `AC-MOT-BUILD-001-01`: produced application ELF (3,120,416 bytes), application image (126,224 bytes), bootloader image (22,192 bytes), and partition table (3,072 bytes). ELF size includes debug information.
- `AC-MOT-BUILD-001-02`: reviewed `app_main`: it loops only on `vTaskSuspend(nullptr)` in the SDK-created application task. Effective owned-source flags select C++23, exceptions off, and RTTI off; generated SDK configuration also disables exceptions and RTTI. SDK headers use GNU extensions, so this platform stub uses `-Wall -Wextra -Werror` without `-Wpedantic`; the portable-core diagnostics remain a later decision.
- `AC-MOT-BUILD-001-03`: executed `scripts/firmware.py#verify_artifacts`; checked target metadata, compile command, SDK configuration, little-endian RISC-V ELF, and both images through SDK esptool inspection. Application image inspection identified ESP32-C6 and valid checksum/hash.
- Disposable negative fixtures: eight checks exited 0 after confirming rejection of missing/empty images, invalid ELF, wrong target, wrong C++ mode, enabled exceptions, enabled RTTI, and invalid SDK configuration. A separate CLI fixture confirmed stale source provenance exits 1 and preserves the original receipt. Fixtures were removed.
- Initial attempts exposed an unsupported IDF parallelism option, GNU extensions in SDK headers under pedantic diagnostics, and a different SDK metadata key. These were corrected before the clean successful run.
- Read-only review found a stale-provenance risk in `--verify-only`; it now requires a matching original receipt and never rewrites it. Build input changes during execution also cause failure.
- Added the same hook to CI and validated its workflow syntax locally. The hosted CI job has not been run here. Board boot and task execution remain untested.
- Final RQML standard check: pass, with no drift, context changes, or uncovered approved requirements. Strict check: fail only for missing implementation/verification of `MOT-ENG-004` through `MOT-ENG-009`.
- Final `mise exec -- pre-commit run --all-files`: exit 1; all other hooks passed, and inner `rqml-check` exited 2 for those six draft coverage gaps. A separate run covering all untracked files had the same result; their formatting/JSON/TOML checks passed.

Tested source/configuration hashes are preserved in the reviewed
`.rqml/baseline.json` implementation-link entries. The verifier's SHA-256 at
execution was `3cd273013e04a50811ce848b4c630b36006df43543dd6b0dabbcf13be5ac3df4`.
The generated receipt additionally records the effective compiler command,
SDK identity, input hashes, generated configuration hash, and output hashes.

| Output | SHA-256 |
| --- | --- |
| Application ELF | `0a1ca7ec3e7b22b5bab79b62782e5f7763ea5e0b3dbd9b53ff4bd8143da18e7c` |
| Application image | `059c73f5b0d4baee786f28b8edef54cbc240741a2c18d8309e7d9ee4d690304a` |
| Bootloader image | `0d1631ac50989e6eca3b3c30979514a7f3ea26b8a28d259a11a5b2468925b084` |
| Partition table | `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820` |

### Earlier planning-only checks

Structural verification on 2026-11-07 covered `MOT-ENG-004`, `MOT-ENG-005`,
`MOT-ENG-006`, `MOT-ENG-007`, `MOT-ENG-008`, `MOT-ENG-009`, their acceptance
criteria, and their declared goal links. Checked specification SHA-256:
`2c15226333fb990c7d140680090a80754bef9113cfaece6de4949a5974a2c33e`.
There are no tested implementation or product-test hashes to record.

ADR-0002 records a separate temporary tooling probe: host GCC/Clang configure,
build, and CTest runs exited 0. The sanitized Clang run initially exited 8 at
CTest because LeakSanitizer was blocked by sandbox process-inspection limits;
the same instrumented build passed outside the sandbox, exit 0. This is tooling
availability evidence, not product verification or requirement implementation.

| Check | Observed result |
| --- | --- |
| RQML MCP validation with the specification path | Valid; no diagnostics |
| Pre-commit RQML validation and strict lint hooks | Exit 0 |
| RQML MCP check, standard strictness | Pass; missing implementation and verification remain reported |
| RQML MCP check, strict strictness | Fail: the current engineering requirements lack implementation and verification links |
| `mise exec -- pre-commit run --all-files` | Exit 1; inner strict `rqml-check` exits 2 for missing implementation and verification links; other hooks pass |
| Pre-commit on the changed planning documents and specification | Exit 1 for the same strict coverage findings; formatting, validation, and lint pass |

## Implementation-plan entry criteria

Each implementation stage will identify its goal, approved requirement IDs,
relevant ADRs, files to create or change, verification commands, and real trace
edges to record after implementation. Do not invent IDs, file layouts, commands,
or completed verification to fill those fields before the decisions are made.

Plan build and host-test evidence separately from physical-device verification.
Keep hardware-dependent acceptance pending until exercised. Preserve completed
stages when updating the implementation plan.
