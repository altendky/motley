# RQML tooling

Tool definitions and locking policy live in [mise.toml](../mise.toml).
Keep `mise.lock` and its `.mise/locks/` dependency graphs together when updating
tools. See the [README](../README.md) for setup and [AGENTS.md](../AGENTS.md) for
the requirements workflow.

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
- A code or test link records a relationship. Verify its target and relevance,
  and run the appropriate tests.
- Revisit implementation and verification when requirement intent changes.
  A clean drift report does not establish continued satisfaction.
- Passing checks on an empty specification establishes no product coverage.
  Structural validation and trace coverage do not prove correct behavior.
