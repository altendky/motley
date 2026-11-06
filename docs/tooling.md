# Requirements and OpenLore

## Scope

OpenLore is the primary tool being evaluated for requirement-to-code navigation.
OpenSpec supplies the requirement format and structural validation. The current
agent discusses intent, edits requirements and code, and runs verification.
There is no additional model service in this workflow.

The setup uses OpenLore 3.5.0 and OpenSpec 1.16.0 as exact local development
dependencies. `package-lock.json` records the resolved dependency tree. Install
with `npm ci`; do not substitute a moving `npx openlore` version. Node must satisfy
the range in `package.json`.

No global installation, agent-client registration, daemon or Git hook is needed.
The repository's `AGENTS.md` directs agents to the local CLI. Automatic upstream
installation is deliberately not used because it also configures agents and
hooks. MCP registration can be evaluated separately later.

## Working loop

1. Update the affected requirements from agreed intent. Preserve the `MOT-*` ID
   even when changing the prose, heading or file. Review the resulting requirement
   diff and retain unresolved choices explicitly.
2. Run `npm run lore:analyze` when source analysis is missing or stale. Retrieve
   task context with `npm run lore -- orient --task '<focused task>' --json`.
3. Follow explicit requirement anchors into implementation and tests. Inspect
   callers and shared dependencies, identifying other behavior to preserve.
4. Make the focused patch, explaining any necessary expansion of scope.
5. Run relevant build, test and hardware checks. Update real implementation
   anchors, run `npm run specs:validate`, refresh source/specification indexes and run
   `npm run lore:mapping` after link edits.
6. Report the requirement diff, retrieved evidence, expected and actual impact,
   preserved behavior, check results and remaining uncertainty.

For example, an implemented requirement can contain this requirement-scoped line:

```markdown
- **Implementation**: `read_temperature::main/drivers/sht45.cpp`
```

This is syntax only, not an existing Motley symbol. The bold `Implementation`
marker is required by the installed parser; a plain `Implementation:` line is
ignored. Multiple requirements may refer to shared code. Keep
unimplemented requirements unlinked; do not link them to this example or to an
entire application merely to improve a coverage number.

The firmware requirements currently have no implementation anchors because no
firmware exists. An empty mapping is expected and is not completion evidence.
Scenario bullets are acceptance intent, not executable tests.

## Authored and derived state

| Location | Treatment |
| --- | --- |
| `openspec/specs/`, `openspec/config.yaml` | Authored, version-controlled requirements and context |
| `openspec/decisions/` when created | Authored, version-controlled lasting decisions |
| `.openlore/config.json` | Version-controlled analysis configuration |
| `.openlore/memory/notes.json` when created | Authored memory; retain and review changes |
| `.openlore/decisions/` when created | Retain pending decision content and transition history; transitions alone are not approval evidence |
| `.openlore/analysis/` | Ignored, rebuildable indexes and reports |
| Cache, logs, telemetry and session ledger | Ignored runtime artifacts |
| `node_modules/` | Ignored dependencies and npm cache |

Do not ignore or delete the whole `.openlore/` directory. Inspect generated
changes to its configuration before including them in a future commit; fields
such as `lastRun` can be operational metadata rather than a deliberate setting.

## Dependency and configuration details

The normal upstream dependency set is installed because packages marked optional
are needed for useful CLI behavior: without `protobufjs` the CLI fails at startup,
and without LanceDB it skips the function, text and specification indexes. The
initial attempt to omit optional dependencies was therefore abandoned.

`apache-arrow` 18.1.0 is also an explicit development dependency to satisfy the
peer range declared by the installed LanceDB 0.40.0. OpenLore's optional Arrow
21.x dependency resolves inside OpenLore and is not visible to the hoisted
LanceDB package; without the explicit compatible peer, index building fails.

The native parser packages declare conflicting tree-sitter peer ranges. The
repository uses npm's `legacy-peer-deps` resolution and the lockfile, then checks
actual parser/extractor behavior. This is a compatibility exception, not evidence
that every upstream grammar is compatible. Dependency lifecycle scripts are
disabled; the trial uses published prebuilt binaries. Another platform may need
an explicitly reviewed native build if those binaries do not load.

OpenLore's project-type enum has no C/C++ value. Configuration uses `unknown`
rather than calling the firmware a Node application because of its tooling
manifest. Source files are still detected by language. Build output, downloaded
components and SDK directories are excluded from the project graph.

Analysis uses `--no-embed`: keyword retrieval is sufficient for this initial
trial. No embedding provider or model generation is configured. Specification
commands disable OpenSpec usage telemetry for these invocations.

Automatic index bootstrapping is disabled; refresh explicitly with
`npm run lore:analyze`. In this requirements-only repository, specification search
works and `orient` can return matching specifications without application functions.
An earlier analysis with no indexed symbols returned `index-absent`; later
documentation produced a signature-only index. Neither is firmware evidence.
Use `npm run lore -- search '<task>' --specs --json` to retrieve requirements now.
This also avoids repeated background builds that cannot produce a function index
of real application functions from documents alone.

## Limits and acceptance

The C/C++ fixture established a sharper limit than the language-support summary:
`mapping refresh` resolves anchors through an exported-symbol inventory whose
extractor does not cover C/C++. A real C++ symbol with a correctly formatted
anchor is reported as `not-assessed`, with boundary `language-not-extracted`.
Function navigation and keyword requirement search work, but automatic
requirement-to-function coverage and reverse links are not established. Preserve
authored anchors and verify them manually; do not clear this state by accepting
a new baseline or changing the requirement to match the tool. This gap requires
an upstream fix or a separately evaluated integration before relying on automatic
C/C++ traceability.

OpenLore can parse C and C++ and identify functions and calls. Its C++ type
inference is lightweight, and its cross-file import resolver does not provide
compiler-level C/C++ include or translation-unit analysis. SDK callbacks, virtual
dispatch, macros, templates and conditional compilation need additional source
inspection and real builds. No compile-database-aware integration is configured.

A successful mapping says a link resolved. A clean drift report says a structural
check found no discrepancy under its model. Neither proves behavior, complete
impact analysis, a passing test or a safe output circuit.

Keep a verification record separate from links. Identify the command, result,
tested commit or working-content hashes, and what was not checked. Report stale,
inferred and unknown relationships explicitly.

Stable identity through arbitrary prose changes, anchor repair after moves and
renames, repeated focused changes, and deliberate behavior-breaking changes still
need the broader evaluation described by the research. This setup does not claim
to have completed that evaluation.

## References

- [Requirements-driven development research](../../tome/research/requirements-driven-agent-development.md)
  describes the intended workflow; the sibling path is a local research reference.
- [Inspected OpenLore source revision](https://github.com/clay-good/OpenLore/tree/41faf5181510f955a3a3c6235644d36a277b9b9b)
  underlies that research. The installed npm artifact is independently pinned by
  version and integrity in the lockfile; it is not assumed identical to this tree.
- [Language support](https://github.com/clay-good/OpenLore/blob/41faf5181510f955a3a3c6235644d36a277b9b9b/docs/language-support.md),
  [configuration](https://github.com/clay-good/OpenLore/blob/41faf5181510f955a3a3c6235644d36a277b9b9b/docs/configuration.md),
  and [installation behavior](https://github.com/clay-good/OpenLore/blob/41faf5181510f955a3a3c6235644d36a277b9b9b/docs/install.md).
