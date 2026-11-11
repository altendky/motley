# Firmware build

The ESP32-C6 target implements the build obligations of `MOT-BUILD-001` and the
Matter foundation in [requirements.rqml](../requirements.rqml).
[ADR-0009](../.rqml/adr/0009-matter-device-information-foundation.md) advances
the completed idle-only bootstrap to Matter startup. Hardware acceptance is
tracked separately in [the development procedure](matter-development.md).

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
inputs into a staging project under the output directory. An online SDK
reconfigure acquires the exact managed components in the committed
[dependency lock](../firmware/dependencies.lock). Compilation then mounts that
staging project read-only with networking disabled. Generated configuration and
artifacts stay in the output directory. The original repository is never
mounted writable into the SDK container.

Each build regenerates `sdkconfig` from the declared defaults. A cached or
manually edited output `sdkconfig` cannot override them; put reviewed setting
changes in the firmware inputs. Reverification preserves the original config.

Ordinary builds reject changes to the committed lock or staged owned sources.
Dependency content hashes, executable modes, and file counts are recorded per
component and checked for changes during compilation and reverification.
The bundle includes the exact lock and `dependency-content.json`; the receipt
also records the upstream identities declared in `toolchain.toml`.

To intentionally resolve a new candidate dependency set:

```sh
mise exec -- uv run scripts/firmware.py --build-dir /path/to/update-output --update-dependencies
```

This produces a candidate `/path/to/update-output/dependencies.lock` without
changing repository inputs or publishing a successful build. Review its
compatibility and changes, copy the accepted lock into `firmware/`, and rebuild
normally. A lock pins transitive ranges as well as the direct exact release.

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
debug string cannot satisfy the check. Matter's 64-character version field
uses the full identity when it fits, otherwise the shortened SDK label. The
full identity remains in the custom descriptor and boot log. The SDK's 32-byte standard version field
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
was observed for the prior bootstrap in PR #14; the Matter revision still needs
its own hosted run.

Build verification establishes cross-compilation and inspectable artifacts.
Board boot, radio operation, commissioning, controller presentation, and power
cycle/reset behavior require hardware evidence. It does not establish
application fault or watchdog supervision.
