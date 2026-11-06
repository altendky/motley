# Motley development with RQML

Read `README.md` for scope. `requirements.rqml` is the maintained requirements
document; `PLANNING_SESSION.md` is historical research with superseded scope and
technical assumptions. The npm manifest supplies development tools, not firmware.

## Working from requirements

- Discuss intent through ordinary conversation, then maintain the affected
  requirements. The agent operates the tools and edits XML; the user does not
  need to operate RQML stages or maintain its artifacts manually.
- Preserve requirement `id` and acceptance-criterion `id` values through prose,
  title, location and design changes. IDs identify obligations, not source files.
- Start a focused change with MCP `rqml_show` and `rqml_impact`, using the path to
  `requirements.rqml`. The CLI equivalents are `npm run rqml -- show <id> --spec
  requirements.rqml` and `npm run rqml -- impact <id> --spec requirements.rqml
  --json`. Use path inputs rather than loading the complete XML into each request.
- Apply all `MOT-ENG-*` constraints to every firmware change, even if the impact
  traversal does not retrieve them. Domain goal links do not establish complete
  constraint applicability or a minimal implementation edit set.
- Follow declared code/test locators and inspect actual source consumers. RQML
  does not recover C++ call/include dependencies. Use the matrix JSON to find
  requirements sharing a source file, including links with different fragments;
  CLI `impact` does not start from an external source locator.
- Identify preserved behavior before editing shared code. Explain a larger
  redesign when needed while preserving the agreed requirements.
- Keep unimplemented requirements visible without fabricated links. Initially
  all firmware requirements are draft, unimplemented and unverified.

## Links, review and execution evidence

- Record real implementation links with `rqml link <id> path#symbol --spec
  requirements.rqml`; use `--type verifiedBy` for real test links. For C++,
  `#symbol` is a navigation hint: verify the symbol and its relevance manually.
- Before replacing a link with `--update` or refreshing an implementation baseline
  with `--refresh <edge-id>`, inspect the change and explain why it still satisfies
  its requirements. A hash refresh does not execute tests or prove correctness.
- A requirement/acceptance edit triggers reconsideration of its realization and
  previous verification even when RQML reports no implementation drift. Keep
  intended behavior separate from current mappings; never rewrite intent merely
  to match observed code.
- Check test-target existence, inspect changed tests and run appropriate checks.
  RQML 0.11.0 does not baseline or detect missing/changed `verifiedBy` files through
  its drift checker. A declared verification link is not an observed passing test.
- Record commands, results, applicable requirement content and tested source/test
  hashes or commit. Distinguish link review, structural checks and execution.
- Run `npm run requirements:validate` and `npm run requirements:lint` after spec
  edits, and `npm run requirements:check` for coverage/drift. Report actual exit
  codes and gaps. The initial strict check intentionally fails with exit 2 because
  no firmware or test links exist; do not hide that by weakening the gate.

## State and integrations

Keep `requirements.rqml` and authored `.rqml/` state under version control,
including `.rqml/baseline.json` when real implementation links create it. Never
treat baselines as disposable caches or refresh them without review.

Codex configuration enables a pinned project MCP server and the RQML plugin from
the repository marketplace. From the root, run `npm ci`, then `npm run codex`
so plugin hooks inherit the local RQML CLI on PATH. Skills come from the plugin;
its bundled MCP launcher is disabled to avoid duplicating the project server.
Hook activation requires the host's normal trust review. The upstream plugin
uses standard check strictness by default; `requirements:check` remains the
explicit strict completion check and still reports missing firmware/test links.
No source-navigation companion is configured. Read `docs/tooling.md` and
`docs/tooling-validation.md` for observed capabilities and gaps.
