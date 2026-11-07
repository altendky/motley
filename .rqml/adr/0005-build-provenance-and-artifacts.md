# ADR-0005: Checkout-aware build receipts and CI artifact bundles

- **Status:** Superseded by ADR-0006
- **Date:** 2026-11-07
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-BUILD-002`, `MOT-CI-001`, `MOT-CI-002`
- **Related ADRs:** [ADR-0004](0004-minimal-firmware-build.md)
- **Affected components:** Host build runner, firmware version, CI uploads, build documentation

## Context

The developer approved retaining firmware artifacts with commit/cleanliness
identity, branch context, and explicit PR head versus merged-result provenance.
The original SDK container has no Git checkout, so the host must supply identity.

## Decision drivers

- Identify the actual built source, including local modifications.
- Preserve CI event context separately from actual checkout evidence.
- Keep successful provenance immutable during reverification.
- Make downloaded artifacts inspectable and retain failed diagnostics separately.

## Options considered

| Option | Benefits | Costs |
| --- | --- | --- |
| Host Git snapshot plus versioned receipt and compact embedded version | Works locally and in CI; retains full contextual evidence without expanding firmware metadata | Requires explicit snapshot comparison and receipt validation |
| Derive identity only from CI variables | Small implementation | Does not describe local builds or a checkout overridden by workflow configuration |
| Let the SDK derive Git version | Uses SDK defaults | Container source mount has no Git metadata and cannot establish host cleanliness |

## Decision

Collect actual commit/tree/parents/attached branch and staged, unstaged, and
untracked state before generating outputs. Exclude only the designated output
directory; reject an output directory equal to or containing the repository,
inside firmware sources, or containing build-runner sources. Fingerprint actual
firmware and runner inputs, including file paths and executable modes. Snapshot
again before publication and fail on input or checkout changes.

Pass `g<12-hex-commit>-clean|dirty` to the SDK as the application version.
Inspect the generated image version. Keep full hashes and contextual fields in
schema-versioned `build-receipt.json`, including hashes and sizes of every
published file except the receipt itself. Validate the receipt against current
inputs and artifacts during `--verify-only`; preserve original time and CI data.

Extract an allowlist of CI fields rather than dumping the complete environment
or event. Classify PR head only when actual HEAD matches the event head. Classify
a PR test merge only with the merge ref, matching event SHA, and matching base/head
parents. Record mismatches as unknown. Record exact-base ancestry independently;
missing history or objects produce unknown, never a guessed false result.
Use full-history checkouts in CI. Merge-queue context is identified from its
event/head evidence; no queue provider or workflow trigger is added here.

Build a curated `bundle/` preserving relative flash paths. CI uploads it only
after successful verification, errors on missing files, and includes run/attempt
in artifact names. Upload logs/failure status separately after failure. Use the
repository's configured artifact retention default; no new retention duration
is selected. No publishing or release deployment is introduced.

## Consequences

The receipt is the authoritative detailed provenance; branch names are context
and full commit hashes remain the source identity. Two dirty checkouts can share
a display version but have different input fingerprints. Cleanliness covers
the repository while input fingerprints cover executable build inputs; an
unrelated documentation edit can therefore mark a build dirty.

CI upload semantics and actual hosted execution still need observed hosted-run
evidence. Local fixtures and cross-builds cannot establish that service outcome.
The idle task and earlier engineering drafts retain their existing scope.

## Supersession

Supersedes: None. Superseded by: [ADR-0006](0006-full-commit-build-identity.md).
