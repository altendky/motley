# Motley

This repository has RQML requirements tooling configured. Product requirements,
acceptance criteria and architectural decisions will be developed separately.

`requirements.rqml` is an intentionally empty draft: it contains no product
goals, requirements, acceptance criteria, verification artifacts or trace links.
`PLANNING_SESSION.md` preserves historical research; it is not an approved
requirements or architecture document.

## Development tools

Install [mise](https://mise.jdx.dev/). Tool versions and lock settings live in
[`mise.toml`](mise.toml); dependency graphs live in `mise.lock` and `.mise/locks/`.

From the repository root:

```sh
mise trust
mise install
mise run requirements:validate
mise run requirements:lint
mise run requirements:check
mise run rqml -- overview requirements.rqml
```

Validation, strict lint and the strict coverage/drift check pass for the empty
scaffold. That verifies tool operation; it establishes no product coverage or
firmware correctness. Once requirements are authored, missing implementation and
verification links remain visible through the same strict check.

## Codex integration

Open Codex normally at the repository root after installing the tools.
The MCP server is configured in [`.codex/config.toml`](.codex/config.toml).
The project does not install Codex or require a special Codex launcher.

The repository marketplace pins the upstream RQML Codex plugin for skills and
hooks. Its unpinned bundled MCP server is disabled to avoid a duplicate server.
Plugin hooks separately require `rqml` on Codex's PATH, for example through mise
shell activation. Project and hook trust use the host's normal review process.
Confirm loaded tools and hooks in the host after configuration changes.

See [tooling](docs/tooling.md) for integration details and traceability boundaries.
