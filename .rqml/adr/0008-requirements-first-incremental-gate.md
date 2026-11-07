# ADR-0008: Requirements-first development with nonblocking backlog coverage

- **Status:** Accepted
- **Date:** 2026-11-07
- **Classification:** derived_from_requirements
- **Related requirements:** `MOT-PROC-001`, `MOT-PROC-002`
- **Related ADRs:** None
- **Affected components:** Agent workflow, pre-commit, requirements status reporting

## Context

The developer permits unfinished requirements and wants to favor requirements
before maintained implementation while learning where exceptions are useful.
The previous strict coverage gate rejected the accepted unfinished backlog.

## Decision drivers

- Keep unfinished intent visible without requiring all work immediately.
- Preserve specification validity, implementation drift, and approval checks.
- Review implementation absent from the declared trace graph.

## Options considered

| Option | Benefit | Cost |
| --- | --- | --- |
| Standard consistency check plus approval gate and source review | Uses supported checks, allows backlog, retains integrity/approval enforcement | Unlinked implementation needs explicit review |
| Strict coverage gate | Requires complete forward coverage | Rejects the permitted backlog |
| Custom source coverage scanner | Could flag unlinked files | Needs a deliberate scope and exception model; file coverage does not establish behavioral traceability |

## Decision

Run `rqml check` at standard strictness and separately run unconditional
`rqml gate --spec requirements.rqml`. Preserve schema validation and strict
semantic lint. Report backlog using status/matrix; standard human check output
does not list all nonblocking coverage gaps. Keep strict coverage available as
an explicit assessment rather than the normal completion gate.

Default to agreed requirements before meaningful maintained implementation.
Review actual source/configuration changes against intended behavior and trace
mappings, and record real links. Ordinary helpers and tests can support an
existing requirement. Record the reason and scope of an exception or temporary
experiment instead of silently adding a maintained feature.

The approval gate inspects declared implementation edges. Neither it nor the
consistency check discovers arbitrary unlinked code. No automatic reverse
coverage guarantee or custom scanner is introduced.

## Consequences

Unfinished requirements remain visible and normal checks can pass. Integrity
and mapped approval failures still block. This policy supports incremental
development; it does not establish a release-completion policy or prove all
implementation behavior has a suitable requirement.

## Supersession

Supersedes: None. Superseded by: None.
