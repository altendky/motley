# ADR-0007: Abbreviated labels in size-limited standard fields

- **Status:** Accepted
- **Date:** 2026-11-07
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-BUILD-002`, `MOT-CI-002`
- **Related ADRs:** [ADR-0006](0006-full-commit-build-identity.md)
- **Affected components:** SDK version label, build verifier, receipt

## Context

The developer clarified that full hashes must remain present and available,
while size-limited standard fields may abbreviate them. The SDK version field
holds 32 bytes including its terminator; it cannot hold the full identity.

## Decision drivers

- Keep full identity accessible in firmware and build evidence.
- Make generic SDK image inspection useful within the existing field size.

## Options considered

| Option | Benefit | Cost |
| --- | --- | --- |
| Abbreviated standard label plus full custom identity | Standard tooling shows commit context; full identity remains verified | Standard labels can share a prefix |
| Neutral standard label plus full custom identity | Preserves full identity | Standard tooling shows no commit context |

## Decision

Use `g<12-character-prefix>-clean|dirty` only for the constrained SDK application
version field. Verify that label against the full identity and record it as
`sdk_project_version` in the receipt's inspection metadata.

Carry forward ADR-0006's full custom descriptor and verification. Receipts,
displayed build identities, and artifact names continue using the full hash.
An abbreviated SDK label alone never establishes build identity.

## Consequences

SDK tooling provides a useful short label while the complete commit and working
tree state remain accessible in the image, ELF, and receipt. No task behavior or
artifact publication policy changes. Existing receipts require rebuilding when
their standard-label inspection metadata no longer matches.

## Supersession

Supersedes: ADR-0006. Superseded by: None.
