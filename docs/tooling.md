# Requirements with RQML

## Scope and installation

This branch evaluates RQML as the requirements and traceability layer. The current
agent discusses behavior, maintains the specification, edits implementation and
runs verification. A source-navigation companion remains a separate decision.

`@rqml/cli` 0.11.0 is an exact local development dependency. The lockfile resolves
core 0.9.0 and schema package 0.2.2, whose document schema is 2.2.0. Run `npm ci`,
then invoke `npm run rqml -- <command>`. No global CLI, model API, MCP server or
agent-host hooks are needed for the trial. Installation uses published package
contents with dependency lifecycle scripts disabled.

The only normative source is `requirements.rqml`; no parallel hand-maintained
Markdown requirements are introduced. Native `overview`, `show`, `impact` and
`matrix` commands provide readable and JSON views. IDs are separate attributes,
so ordinary title changes do not rename the requirement or its acceptance criteria.

The twelve requirements and fourteen acceptance scenarios preserve PR #2's
intent. Whitespace is normalized; one scenario's tool-specific phrase changes
from a clean OpenLore report to a clean RQML report. Scenario titles are retained
as XML comments, while native criterion IDs identify their acceptance obligations.
Four declared goals carry the original domain purpose/scope. No implementation
or verification edges are present in the project baseline.

## Agent loop

1. Discuss the change and update the affected requirement and acceptance text,
   retaining its IDs. Record unresolved questions explicitly.
2. Use `show` for the requirement and its direct trace neighborhood. Use `impact`
   for transitive declared relationships, then include all applicable engineering
   constraints. A shared goal may return siblings; another domain's constraints
   can be absent unless explicitly related.
3. Follow implementation/test locators, inspect the actual C++ symbols and callers,
   and use matrix JSON to identify other requirements linked to the same file.
   Match the underlying file as well as exact fragment strings, because C++ drift
   baselines are whole-file. CLI `impact` accepts declared artifact IDs, not an
   external code locator as the starting node.
4. Identify preserved behavior, make the focused patch, and explain any necessary
   expansion or redesign. Keep requirements independent of the current realization.
5. Inspect link and implementation changes before recording/repointing links or
   refreshing baselines. Run relevant checks; separately validate the specification
   and report coverage/drift results.
6. Record actual execution evidence against requirement and source/test content,
   including commands, outcomes and remaining gaps. A link, baseline refresh and
   passing behavioral test are different facts.

An implementation link uses `rqml link <id> path/to/file.cpp#symbol --spec
requirements.rqml`. A test relationship adds `--type verifiedBy`. `--update`
replaces an existing edge locator; `--refresh <edge-id>` accepts changed content
for an implementation edge after review. These operations do not execute tests.

## State retention

| Location | Treatment |
| --- | --- |
| `requirements.rqml` | Authoritative requirements, criteria and declared trace graph |
| `.rqml/baseline.json`, when created | Version-controlled reviewed implementation content hashes |
| `.rqml/adr/` and `.rqml/plan.md`, when created | Version-controlled authored decisions and plan |
| `docs/tooling-validation.md` | Observed tool behavior and comparison limits |
| `node_modules/` | Ignored tools and local npm cache |

No baseline exists until real implementation links are recorded. Do not ignore
the whole `.rqml/` directory or regenerate reviewed baselines as if they were a
cache. Keep the reason for an intentional baseline refresh with the change.

## Validation and gate semantics

- `requirements:validate` checks XML/schema and referential integrity.
- `requirements:lint` applies strict semantic lint rules.
- `requirements:check` runs the strict deterministic coverage/drift check.

The initial strict gate fails with exit 2 for missing implementation and test
relationships. Standard check can exit 0 while reporting those gaps for draft
requirements. Neither result is a claim that firmware works. Keep the strict gate
as a visible completion target rather than adding fictional links or silently
using standard mode as an acceptance gate.

All requirements start in RQML's draft lifecycle. A later status transition must
reflect actual review; it is not execution evidence. No RQML host plugin or
approval gate is installed, and routine work proceeds from agreed requirements
through conversation with the current agent.

## Observed limits

- C++ `#symbol` locators are navigation hints. File existence and file hashes are
  checked; the symbol is not parsed or verified. Even a nonexistent function name
  can pass the gate when its file exists. An unrelated edit in that file can mark
  several implementation links changed.
- Changing requirement and acceptance prose does not itself invalidate recorded
  implementation baselines. Such edits require explicit review of realization,
  preservation constraints and previous verification even when check stays green.
- Drift baselines cover implementation edges. `verifiedBy` relationships are not
  content-hashed by this version, and changing or deleting a linked test file can
  leave strict check passing. Independently verify test targets and execution.
- Impact follows declared graph relationships, not recovered C++ source
  dependencies. Matrix coverage labels describe relationships, not executed tests.
- Schema/lint/check do not establish semantic consistency, safety, complete impact
  or correct behavior. A source move needs explicit link repair; a requirement
  revision needs explicit reconsideration of its prior evidence.

## References

- [RQML project and agent loop](https://github.com/rqml-org/rqml)
- [CLI documentation](https://rqml.org/docs/tooling/cli/)
- [Core API and model](https://rqml.org/docs/tooling/core/)
- [OpenLore alternative, PR #2](https://github.com/altendky/motley/pull/2)

The comparison follows the requirements-driven agent development research in the
sibling Tome repository. This project records the relevant procedure and findings
here; that local research checkout is not a runtime dependency.
