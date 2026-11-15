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

## KiCad

On Linux x86-64, `mise install` installs KiCad 10.0.8 from the official full
AppImage distributed by [KiCad's MIT mirror](https://www.kicad.org/download/linux/).
The archive checksum is pinned in configuration and `mise.lock`. Mise extracts
the AppImage once, including symbols, footprints and 3D models; launches need no
FUSE mount. Use the mise environment to select it instead of a system KiCad:

```sh
mise exec -- kicad-cli version
mise exec -- kicad hardware/controller/motley-carrier.kicad_pro
mise exec -- eeschema hardware/controller/motley-carrier.kicad_sch
mise exec -- pcbnew hardware/controller/motley-carrier.kicad_pcb
```

The KiCad tool is skipped on other platforms; install the same release using
[KiCad's platform packages](https://www.kicad.org/download/). Other mise tools
remain available there. Initial installation needs about 4 GB for the extracted
application and libraries, plus the download/archive.

For later major upgrades, inspect release notes and capture connectivity and
geometry before changing native sources. KiCad 10 provides
[native upgrade commands](https://docs.kicad.org/10.0/en/cli/cli.html):

```sh
for sheet in hardware/controller/*.kicad_sch; do
  mise exec -- kicad-cli sch upgrade "$sheet"
done
for board in hardware/controller/*.kicad_pcb; do
  mise exec -- kicad-cli pcb upgrade "$board"
done
for library in hardware/controller/*.kicad_sym; do
  mise exec -- kicad-cli sym upgrade "$library"
done
mise exec -- kicad-cli fp upgrade hardware/controller/Motley.pretty
```

Schematic upgrade handles only the named sheet; enumerate children explicitly.
Review stock-library/model variables as well as serializer changes. There is no
CLI project-file upgrade command; do not hand-increment `.kicad_pro` schemas.
Compare fresh netlists, ERC/DRC and native trace checks before refreshing reviewed
RQML baselines. The KiCad 10 migration evidence is in the
[hardware verification record](../hardware/controller/verification.md).

## Generated board SVGs

Versioned per-board views live in
[`hardware/controller/generated/board-images/`](../hardware/controller/generated/board-images/README.md).
They are derivatives of the native KiCad boards, with fixed layers/colours,
isolated KiCad preferences and stable metadata without export timestamps
(`MOT-CI-004`). Use the pinned tool environment:

```sh
mise exec -- uv run scripts/board_images.py --write
mise exec -- uv run scripts/board_images.py --check
```

The first command regenerates changed/missing SVGs; the second fails on
missing/stale/unexpected views without modifying them. Commit matching native
board and image changes together. Pre-commit always runs the freshness check,
including when a commit only deletes an SVG. CI's existing **Repository
checks** job runs it through `pre-commit --all-files`, and failure blocks the
aggregate check. It uses the KiCad installation already provided by mise.
SVG freshness does not establish circuit correctness or fabrication readiness.

## Human-readable requirements report

Every PR and push to `main` has an independent **Requirements report** CI job
(`MOT-CI-003`). It validates the checked-out specification and generates the
standard RQML Markdown overview, including draft requirements, lifecycle status,
statements and acceptance criteria. The job runs alongside the firmware build,
so the report can be downloaded without waiting for firmware success.

Download the `requirements-<commit>-run<run-id>-a<attempt>` artifact from the
workflow run's artifacts. It contains `requirements.md`; the commit is the
checked-out GitHub event SHA, including the test-merge commit on PR runs.
Generation, empty-output or upload failures fail this job and the aggregate
`all` check. Retention uses the repository's normal artifact settings.

Generate the same Markdown locally; redirect stdout to save it to a chosen file:

```sh
mise exec -- rqml overview requirements.rqml
```

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

Native KiCad traceability is checked without requiring KiCad or generated
netlists in the repository check environment:

```sh
uv run scripts/hardware_trace.py
uv run scripts/hardware_trace.py --json
uv run scripts/test_hardware_trace.py
```

The hidden `Requirements` field contains space-separated requirement IDs on
schematic symbols/sheet symbols and PCB footprints. The checker traverses all
three root designs and their included sheets, validates IDs and explicit RQML
file relationships, and reconciles fields using root/sheet/symbol UUID paths.
Repeated sheets and multi-unit components retain their native identities;
board-only mechanics are explicitly distinguished from circuit components.

`MOT-HW-003` implementation links provide whole-file drift checking for native
annotation sources. Other `dependsOn` links and component fields identify
design inputs, including draft electrical requirements; they do not establish
those requirements' implementation or verification. RQML does not interpret
KiCad UUID fragments or automatically scan source comments. The native checker
tests annotation integrity only, not circuit correctness, PCB routing or ESD.

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
