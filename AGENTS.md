# Motley development

Read `README.md` for the current scope. Maintained requirements live in
`openspec/specs/`; `PLANNING_SESSION.md` is historical research and contains
superseded scope and technical assumptions.

## Requirements and changes

- Discuss intent through ordinary conversation, then maintain the relevant
  requirements. Do not require the user to operate a tool-specific stage menu.
- Preserve each `MOT-*` requirement ID across amendments, moves and title changes.
  These IDs are a project convention, not a guarantee supplied by OpenLore.
- Before changing implemented behavior, use
  `npm run lore -- orient --task '<focused task>' --json`, follow the relevant
  requirement links, and inspect source consumers. If the index is absent or
  stale, run `npm run lore:analyze` first.
- Identify requirements whose behavior shared code must preserve. Use ordinary
  source inspection and build information to supplement incomplete graph edges,
  especially C++ callbacks, virtual dispatch, macros and Kconfig branches.
- Keep patches scoped to the agreed behavior. Maintain exact implementation
  anchors only where real symbols exist, in a requirement-scoped
  `- **Implementation**:` entry with backtick-quoted
  `symbolName::path/to/file.cpp` or `path/to/file.cpp#symbolName`. Never invent a
  link to mark a requirement covered. OpenLore 3.5.0 reports C/C++ anchors as
  `not-assessed`; verify those manually against source, and do not claim automatic
  reverse requirement links or function coverage from this version.
- After changes, validate specs with `npm run specs:validate`, refresh source
  analysis after source or specification changes, and run `npm run lore:mapping`
  after link edits.
- Run checks appropriate to the actual change. Report requirement changes,
  expected and actual impact, preservation constraints, verification results and
  remaining gaps. A mapping or clean graph is not evidence of a passing test.
- Preserve agreed requirements when observations about implementation disagree;
  report the disagreement instead of rewriting intent to match the code.

## Firmware

Follow `openspec/specs/engineering/spec.md`: safety and correctness take priority
over optimization. Keep unavoidable C SDK pointer interfaces in small adapters.
Treat hardware acceptance and Home Assistant reporting as separate from host
tests and successful local SDK calls.

## Tool state

Use the pinned local CLI through npm. See `docs/tooling.md` for scope, known
limitations and the authored-state policy. No automatic installer, global agent
configuration or Git hooks are needed for this workflow. Do not delete all of
`.openlore/` to rebuild indexes; its authored memory and decisions are durable.
