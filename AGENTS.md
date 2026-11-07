# Motley development with RQML

Read `README.md` for repository state and tool setup. `requirements.rqml` is the
maintained specification and currently contains only an empty draft scaffold.
Develop product requirements and architectural decisions through discussion;
do not populate them merely to demonstrate the tools or satisfy a gate.
`PLANNING_SESSION.md` is historical research, not approved specification content.
Mise supplies development tools, not firmware.

## Working from requirements

- Discuss intent before implementation, then maintain the affected requirements.
  The agent operates RQML and edits XML; the user need not maintain its artifacts.
- Preserve requirement and acceptance-criterion IDs through prose, title,
  location and design changes. IDs identify obligations, not source files.
- Before changing an existing artifact, use MCP `rqml_show` and `rqml_impact`
  with the path to `requirements.rqml`. CLI equivalents are `mise run rqml --
  show <id> --spec requirements.rqml` and `mise run rqml -- impact <id> --spec
  requirements.rqml --json`. Use path inputs, not the complete XML per request.
- Assess applicable constraints and actual source consumers independently of
  the declared graph. RQML does not recover C++ call/include dependencies or
  establish complete constraint applicability.
- Follow declared code/test locators. Use matrix JSON to find requirements
  sharing a source file, including locators with different fragments; CLI
  `impact` does not start from an external source locator.
- Identify preserved behavior before editing shared code. Explain a larger
  redesign when needed while preserving agreed requirements.
- Record significant architectural decisions as ADRs under `.rqml/adr/` and
  implementation plans in `.rqml/plan.md` when those stages are reached.

## Links and verification evidence

- Record real implementation links with `rqml link <id> path#symbol --spec
  requirements.rqml`; use `--type verifiedBy` for real test links. For C++, verify
  the symbol and its relevance manually: `#symbol` is only a navigation hint.
- Inspect changes before replacing a link with `--update` or accepting changed
  implementation content with `--refresh <edge-id>`. A hash refresh does not
  execute tests or prove correctness.
- Requirement or acceptance edits require reconsidering implementation and prior
  verification even when RQML reports no drift. Keep intended behavior separate
  from current mappings; never rewrite intent merely to match observed code.
- Independently check test-target existence, inspect changed tests and run
  appropriate checks. Verification links and drift reports do not replace
  checking test targets and observing their execution.
- Record commands, results, applicable requirement content and tested source/test
  hashes or commit. Link review, structural checks and execution are distinct.
- Run `mise run requirements:validate` and `mise run requirements:lint` after spec
  edits, and `mise run requirements:check` for strict coverage/drift. Report exit
  codes and gaps. An empty scaffold passing is not evidence of product coverage.
  Keep future unimplemented requirements visible without fabricated links or a
  weakened gate.

## State and integrations

Keep `requirements.rqml` and authored `.rqml/` state under version control,
including `.rqml/baseline.json` when real implementation links create it. Never
treat reviewed baselines as caches or refresh them without reviewing the change.

Run `mise install`, then open Codex normally at the repository root.
The MCP entry invokes mise itself. Upstream plugin hooks separately require the
RQML CLI on Codex's PATH, for example through mise shell activation. The plugin's
bundled MCP launcher is disabled to avoid duplicating the pinned project server.
Hook activation requires the host's normal trust review. Upstream hooks use
standard strictness; `requirements:check` remains the explicit strict completion
check. No source-navigation companion is configured. Read `docs/tooling.md` for
integration details and traceability boundaries.
