# RQML tooling

Tool definitions and locking policy live in [mise.toml](../mise.toml).
Keep `mise.lock` and its `.mise/locks/` dependency graphs together when updating
tools. See [AGENTS.md](../AGENTS.md) for the requirements workflow.

## Setup and checks

```sh
mise trust
mise install
mise exec -- pre-commit install
mise exec -- pre-commit run --all-files
```

Pre-commit validates and strictly lints specification changes. Standard
consistency/drift checking and a separate mapped-implementation approval gate
run on every commit, including changes outside the specification. During
incremental development, unimplemented and unverified requirements are permitted
backlog. Invalid specifications, missing/changed linked implementation, and
implementation mapped to unapproved requirements still fail their checks.

Inspect the backlog explicitly:

```sh
mise exec -- rqml status --spec requirements.rqml --json
mise exec -- rqml matrix requirements.rqml
```

Standard human check output does not list every nonblocking coverage finding.
Strict completeness assessment remains available with
`mise exec -- rqml check requirements.rqml --strictness strict`; it is separate
from the normal incremental-development gate. See
[ADR-0008](../.rqml/adr/0008-requirements-first-incremental-gate.md).

The separately invoked [firmware build](firmware-build.md) uses the pinned
ESP-IDF container and also runs as a CI job.

## Codex integration

Open Codex at the repository root: the local marketplace source resolves from
that directory. The MCP server is configured in
[.codex/config.toml](../.codex/config.toml), and the plugin source is declared in
[the marketplace](../.agents/plugins/marketplace.json). The plugin's bundled MCP
server is disabled so only the project server supplies RQML tools.

MCP and plugin hooks have separate launch paths. The MCP server invokes mise
itself. Hooks look up `rqml` on Codex's PATH, so they need the mise environment,
for example through shell activation. An available MCP server does not establish
that hooks are active; hooks can fail open when the CLI is missing.

Project configuration and hooks use the host's normal trust review. Confirm
tools and hooks in the host after configuration changes. The project does not
require a special Codex launcher.

## Traceability boundaries

- Impact follows declared relationships. Inspect actual source dependencies and
  applicable constraints as well.
- Start meaningful maintained implementation from agreed requirements. Review
  the actual diff for unlinked behavior or configuration; RQML does not discover
  source code absent from its trace graph. Helpers and tests can support broader
  requirements. Record scoped exceptions or experiments explicitly.
- A code or test link records a relationship. Verify its target and relevance,
  and run the appropriate tests.
- Revisit implementation and verification when requirement intent changes.
  A clean drift report does not establish continued satisfaction.
- Passing checks on an empty specification establishes no product coverage.
  Structural validation and trace coverage do not prove correct behavior.
