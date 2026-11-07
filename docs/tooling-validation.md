# RQML setup verification

The PR configures mise, RQML CLI/MCP and the repository Codex plugin with an empty
draft specification. Product goals, requirements, acceptance criteria, decisions,
verification artifacts and trace links are intentionally deferred.
`PLANNING_SESSION.md` is unchanged historical material.

## Tool versions

- mise 2026.11.2 on Linux x64.
- Node 24.21.0; RQML CLI 0.11.0; MCP 0.8.0; core 0.9.0.
- Schema package 0.2.2, supplying document schema 2.2.0.
- Codex CLI 0.166.0; upstream RQML plugin pinned to
  `4b0272e7d13eebcbdf638b0abdf4018b2f3c505a`.

## Dependency installation

`mise install --locked` previously installed both pinned RQML tools successfully.
The move from npm preserved the same 99 package names, versions and integrity
hashes across the two mise dependency graphs. No local `node_modules/` is needed.

The exact `fast-xml-parser@4.5.7` trust-policy exception follows a review of the
registry publisher history, tarball integrity and all 45 packaged files against
the upstream tag. See [tooling](tooling.md) for its rationale and the remaining
provenance limitation. The exception does not cover other versions.

## Empty-spec checks

Observed on 2026-11-07 on Linux x64, against the final empty scaffold:

| Check | Result |
| --- | --- |
| `mise install --locked node npm:@rqml/cli npm:@rqml/mcp` | Exit 0; all three pinned tools already installed |
| `mise run requirements:validate` | Exit 0; valid schema 2.2.0 and references |
| `mise run requirements:lint` | Exit 0; no strict lint findings |
| `mise run requirements:check` | Exit 0; strict check passes with no coverage/drift findings |
| MCP `rqml_validate` with a path input | Valid schema 2.2.0; no diagnostics |
| MCP `rqml_status` with a path input | Draft document; zero requirements, zero edges, no coverage findings |
| MCP `rqml_check` with strict strictness and a path input | Pass; valid document, no coverage/drift findings |

Passing the empty specification demonstrates tool operation and the absence of
authored obligations; it establishes no product implementation or test coverage.

Tested content SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `requirements.rqml` | `0a3a4ef31135e79285edbf612f168f13d3465b06847271c5609c2e5436cb4fd1` |
| `mise.toml` | `17e3011c8134877e625381fda5b26ea229f52cb6e82194754816147fab364e34` |
| `mise.lock` | `594b29b016d9a212ed529422368fd5590644e603405c17e0a73533aba2a5b4e5` |
| `.codex/config.toml` | `ab27cacf1bc97a78e45996ea5ba142457d0c14a50334d3bd3bf2d2762ecb21e5` |

## Host integration boundaries

The existing project MCP configuration has completed initialization, advertised
13 tools and served read-only calls in Codex. The RQML SessionStart hook has fired
in this conversation. Those startup observations predate the empty-spec reset;
the read-only empty-spec MCP calls above succeeded through that connection.

The MCP launcher invokes mise directly; Codex does not require a special launcher.
Plugin hooks separately need `rqml` on the host process PATH and normal hook trust.
An available MCP server alone does not establish hook activation in every host.
Only Linux x64 execution has been verified; other platforms have lock targets.

Earlier product drafts and disposable tooling trials are excluded from the
current setup documentation. Their earlier commits remain in Git history; no
fixture code or invented implementation/test links are retained in the spec.
