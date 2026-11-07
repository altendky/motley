# RQML tooling

## Scope

This setup supplies requirements tooling and an empty specification. It does not
select product behavior, architecture, hardware or an implementation plan.
`requirements.rqml` contains only document metadata and an empty requirements
section. Add artifacts after discussing their intent; no example obligation is
included as a placeholder.

## Installation and locked state

Use mise 2026.11.2 or newer. `mise.toml` pins Node 24.21.0,
`npm:@rqml/cli` 0.11.0 and `npm:@rqml/mcp` 0.8.0. Review the project configuration,
run `mise trust`, then `mise install --locked`.

Mise installs tools outside the checkout. Its embedded aube installer replays the
dependency graphs in `mise.lock` and `.mise/locks/` with dependency lifecycle
scripts disabled. Commit sidecars with the lockfile; `mise lock --sidecars` lists
them. Core is 0.9.0, schema package is 0.2.2, and document schema is 2.2.0.

Both RQML tools declare an exact `fast-xml-parser@4.5.7` trust-policy exception.
Aube flags this v4 release because the earlier-published v5.9.1 used a trusted
publisher, while v4.5.7 used the existing human publisher. The reviewed tarball's
SHA-512 matches the previous npm lock and all 45 packaged files match upstream
commit `49a12f10e9a44da765f045ca0c60e8d9e5be5aa0` (tag `v4.5.7`). It contains the
[comment/CDATA security backport](https://github.com/NaturalIntelligence/fast-xml-parser/commit/e561c2188607a108a9a8d9b6428902a28aad8fb0)
and has no installation lifecycle scripts. This review supports only that exact
exception and does not supply the missing provenance.

The lock includes Linux x64/ARM64, macOS x64/ARM64 and Windows x64 tool targets.
Only Linux x64 execution has been verified. To deliberately update a tool and its
dependency graph, review the changes produced by a command such as:

```sh
MISE_LOCKED=0 mise lock --bump --platform linux-x64,linux-arm64,macos-x64,macos-arm64,windows-x64 -- npm:@rqml/cli
mise install --locked
```

## Codex MCP and plugin

`.codex/config.toml` registers `mise exec -- rqml-mcp` as the project stdio server.
Install tools before opening Codex normally at the repository root. The launcher
has no machine-specific paths and passes protocol stdout through without task
banners. Mise can try to install missing tools during startup.

The local marketplace is explicitly registered as `motley` with source `.`;
that source resolves from the launch directory. The marketplace pins the upstream
`rqml-codex` plugin to commit `4b0272e7d13eebcbdf638b0abdf4018b2f3c505a`.
`rqml@motley` supplies authoring, initialization, status, design, plan, check and
review skills plus upstream hooks. Codex caches the plugin outside this repo.

The plugin's unpinned npx MCP launcher is disabled through plugin-scoped policy.
The pinned project server supplies the tools. The project neither installs Codex
nor requires a Codex wrapper. Plugin hooks separately look up `rqml` on Codex's
PATH; mise shell activation can supply it. Missing CLI causes those hooks to
fail open even when the independently launched MCP server works.

Project configuration and hooks require the host's normal trust review. Confirm
loaded tools and hooks after changing configuration. Upstream hooks use standard
strictness; the project's explicit completion check is strict. No approval-mode
overrides, user trust state or source-navigation companion are committed.

## Requirements workflow

1. Discuss intent and author the relevant goals, requirements and acceptance
   criteria. Preserve stable IDs when revising existing obligations.
2. Record significant design decisions in `.rqml/adr/` and a staged plan in
   `.rqml/plan.md` when needed. Do not create product decisions as tool examples.
3. Read existing artifacts with `show` and inspect declared relationships with
   `impact`. Review applicable constraints and actual source dependencies too.
4. Implement agreed behavior, then record real code/test traces using `rqml link`;
   review changes before repointing links or refreshing baselines.
5. Run appropriate behavioral tests, validate/lint the specification, and run the
   strict coverage/drift gate. Record commands, results and tested content.

`mise run rqml -- overview requirements.rqml` provides a readable document view.
`mise run rqml -- matrix requirements.rqml --json` reports coverage relationships.

## Checks and evidence

- `mise run requirements:validate` checks schema and referential integrity.
- `mise run requirements:lint` applies strict semantic lint rules.
- `mise run requirements:check` runs the strict coverage/drift gate.

All three pass for the empty scaffold. There are no authored obligations to
assess; this establishes no product completeness or firmware correctness.
Authored requirements without real implementation/test links will produce
coverage findings. Keep the strict gate rather than inventing links.

Version-control authored `.rqml/` state, including reviewed implementation
baselines when real links create them. No baseline is needed for the empty spec.

## Known limits of the pinned tools

- C++ `#symbol` locators are navigation hints; the tool checks files, not symbols.
  Implementation drift hashes whole files, so one edit can affect several links.
- Requirement/acceptance edits do not invalidate implementation baselines; review
  their realization and previous verification independently.
- `verifiedBy` files are not content-baselined or checked for drift by this version.
  Verify test targets and execution independently.
- Impact traverses declared relationships, not recovered C++ call/include graphs.
  Coverage labels indicate links, not observed passing tests.
- Passing validation, lint or trace checks does not establish semantic
  consistency, complete impact analysis or correct behavior.

## References

- [RQML project](https://github.com/rqml-org/rqml)
- [Pinned Codex plugin](https://github.com/rqml-org/rqml-codex/tree/4b0272e7d13eebcbdf638b0abdf4018b2f3c505a)
- [Mise npm dependency locking](https://mise.jdx.dev/dev-tools/backends/npm#dependency-locking)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
