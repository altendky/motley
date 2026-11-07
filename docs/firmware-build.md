# Minimal firmware build

This implements the build-only milestone `MOT-BUILD-001` in
[requirements.rqml](../requirements.rqml), using [ADR-0004](../.rqml/adr/0004-minimal-firmware-build.md).
The SDK's existing application task suspends without doing application work.

## Prerequisites and command

Install the project tools as described in [tooling](tooling.md). A running Docker
daemon with Linux-container support is also required. The official SDK image
and chip target are declared in [toolchain.toml](../firmware/toolchain.toml);
Docker downloads the pinned image when it is not cached.

From the repository root:

```sh
mise exec -- pre-commit run --hook-stage manual firmware-build --all-files
```

By default, outputs go to `build/firmware/`. To keep them elsewhere, set
`MOTLEY_BUILD_DIR` to an output directory before running that command. Use a
fresh output directory for clean-build verification. The runner mounts firmware
sources read-only; generated configuration and artifacts stay in the output
directory. Compilation inside the container has networking disabled.

The same hook runs in the firmware CI job. It is a manual-stage hook so ordinary
repository checks do not require downloading the SDK image.

Metadata and artifact failure fixtures run without Docker:

```sh
mise exec -- uv run scripts/test_firmware.py
```

## Outputs and evidence

The build produces `motley.elf`, `motley.bin`, `bootloader/bootloader.bin`, and
`partition_table/partition-table.bin`. The runner checks target metadata,
effective owned-source C++23/exceptions/RTTI settings, the RISC-V ELF header,
and image inspection with the SDK's esptool. The build also prints a size report.

`bundle/` contains those outputs, `flash_args`, `flasher_args.json`, the linker
map, compiler/image/size reports, `verification.json`, and `build-receipt.json`.
The flash metadata uses relative paths matching the bundle layout. These remain
SDK-default flash settings until verified against the actual board.

The schema-versioned receipt records actual commit/tree/parents, attached branch
or null, staged/unstaged/untracked state, actual input hashes and fingerprint,
UTC start time, SDK/compiler/container/configuration identity, effective compiler
arguments, and output names/sizes/hashes. It records hardware testing as pending.
Build identities use `g<full-commit-hash>-clean|dirty`, including artifact
names and console output. The ELF and application image retain that complete
identity in an SDK custom application-description record. Verification checks
the allocated ELF section and the corresponding image bytes, so an incidental
debug string cannot satisfy the check. The SDK's 32-byte standard version field
uses `g<12-character-prefix>-clean|dirty`; the verifier checks that label against
the full identity and records it separately as `sdk_project_version` in the
receipt. A short standard label alone does not identify a build. See
[ADR-0007](../.rqml/adr/0007-size-limited-version-label.md). Receipt schema version
3 requires a rebuild of earlier receipts.

Cleanliness is measured before generation across the repository, including
nonignored untracked files and excluding only the designated output directory.
Build input fingerprints cover firmware files and the runner/metadata module,
including executable modes. Symlinked build inputs are rejected. Builds fail
if inputs or checkout state change during execution. Unrelated documentation
changes can mark a build dirty without changing its executable-input fingerprint.

GitHub context records the event commit separately from actual HEAD, checkout
ref/kind, PR head/base repositories/branches/commits, exact-base inclusion, and
workflow/run/attempt/job/URL. PR test merges require matching checkout and parent
evidence; a PR-head build is identified independently of whether it already
contains the base. Missing context or history remains null/unknown. The workflow
uses full-history checkouts. Merge-queue metadata is supported if that event is
supplied; no new queue trigger is configured.

Rechecking requires the original receipt and matching source/checkout,
configuration, SDK, inspection reports, and artifacts, including bundled copies.
It preserves original timestamps and CI context. To recheck existing outputs:

```sh
mise exec -- uv run scripts/firmware.py --build-dir /path/to/output --verify-only
```

CI uploads `bundle/` only after successful build and verification. Artifact names
include target, full commit hash, clean/dirty state, checkout kind/PR number, and run
ID/attempt. Missing bundle files and upload failures fail the firmware job and
its aggregate check. Failed-run logs and failure status use a separate diagnostics
artifact. Retention follows repository settings. Hosted upload/download execution
remains pending until observed in CI.

This establishes a cross-build and inspectable artifacts. Board boot, actual
flash settings, task execution, Matter integration, and application fault or
watchdog behavior remain hardware/integration work. The minimal target uses
ESP-IDF directly; it has no managed-component manifest or lockfile yet.
