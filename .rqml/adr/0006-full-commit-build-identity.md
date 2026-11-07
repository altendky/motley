# ADR-0006: Full commit identity in firmware and artifacts

- **Status:** Superseded by ADR-0007
- **Date:** 2026-11-07
- **Classification:** required_by_spec
- **Related requirements:** `MOT-BUILD-002`, `MOT-CI-002`
- **Related ADRs:** [ADR-0005](0005-build-provenance-and-artifacts.md)
- **Affected components:** Build identity, firmware metadata, artifact names, verifier

## Context

The developer explicitly requires full commit hashes everywhere. The pinned
SDK's application-description version field is only 32 bytes including its
terminator. A full Git hash plus clean/dirty suffix cannot fit there.

## Decision drivers

- Preserve every commit-hash character in human and machine identities.
- Embed inspectable identity without runtime work or dynamic allocation.
- Verify the final ELF and flash image, including retention through linking.

## Options considered

| Option | Benefits | Costs |
| --- | --- | --- |
| SDK custom application-description constant | Full identity in ELF and flash image; supported retained read-only section; no runtime work | Requires a generated header and explicit linker retention |
| Put full identity only in the receipt | No firmware changes | Does not meet the embedded full-identity requirement |
| Truncate to the SDK version field | Fits the existing field | Violates the explicit full-hash requirement |

## Decision

Use `g<full-commit-hash>-clean|dirty` in receipts, output, artifact names, and a
constant `motley_build_identity` in the SDK's `.rodata_custom_desc` section.
Generate its initializer through CMake and retain its C-linkage symbol with the
component's propagated linker `--undefined` option. The task still only blocks.

Set the SDK's constrained version field to the neutral `see-build-identity`
label. It contains no abbreviated hash. The verifier separately checks that
label and a single exact, NUL-terminated `MOTLEY_BUILD_IDENTITY_V1:` record in
both the ELF and application image. Missing, abbreviated, mismatched, duplicate,
or unterminated identity records fail verification. The receipt format advances
to version 3; older receipts require rebuilding.

All remaining provenance and publication decisions in ADR-0005 carry forward.
Its earlier abbreviated examples are historical evidence, not current policy.

## Consequences

Generic SDK image-info shows the neutral version label. The full identity is
available in the custom record and verified receipt. Ordinary string inspection
also exposes it. This consumes a small fixed amount of flash with no application
runtime behavior. Physical board execution and hosted CI remain separate checks.

## Supersession

Supersedes: ADR-0005. Superseded by: [ADR-0007](0007-size-limited-version-label.md).
