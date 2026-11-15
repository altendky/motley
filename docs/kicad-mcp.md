# KiCad MCP integration and workflow evaluation

This is an exploratory development-tool integration, requested on 2026-11-15
under the `MOT-PROC-001` exception in [.rqml/plan.md](../.rqml/plan.md).
The maintained native traceability and deterministic export checks remain the
authority for repository invariants. MCP availability does not establish
electrical correctness or manufacturing readiness.

## Installation and startup

The single root [mise configuration](../mise.toml) installs
[mixelpixx/KiCAD-MCP-Server v2.9.0](https://github.com/mixelpixx/KiCAD-MCP-Server/tree/v2.9.0)
from a checksum-pinned source archive. Its upstream commit is
`9dd467c2ba8df09a23490cc0b463f3942e908cae`. The installed server reports version
2.9.0. This packaging currently supports Linux x86-64, matching our pinned
KiCad AppImage; other platforms need a separately verified interpreter bridge.

```sh
mise install --locked
mise exec -- node scripts/check_kicad_mcp.mjs
```

The [project MCP entry](../.codex/config.toml) launches
`mise exec -- kicad-mcp` and selects `KICAD_BACKEND=swig`. The startup check opens
its own stdio MCP connection, lists the exposed tools and checks the Python
backend with `DISPLAY` and `WAYLAND_DISPLAY` removed. It does not open or edit
a design. It also verifies the locked Python distribution versions, actual
module locations and an in-memory PDF render. This check runs in the
Repository checks CI job.

The upstream npm package name does not provide this release's runnable CLI.
Mise therefore builds the source archive using its bundled `package-lock.json`,
with dependency lifecycle scripts disabled, then runs the TypeScript build.
All resulting Node dependencies and Python packages live inside the mise tool
installation. The wrapper uses KiCad's bundled Python 3.11.2 and `pcbnew`
10.0.8; the project's Python 3.14 cannot load those compiled bindings.

The AppImage replaces `PYTHONPATH`, so the Python wrapper selects a private
`PYTHONUSERBASE` inside the MCP installation. Hash-locked packages are installed
there without modifying the KiCad bundle, host Python or normal user packages.
An installation-private `sitecustomize.py` puts those locked packages ahead of
the AppImage's older HTTP libraries. The pinned AppImage also omits the glibc
2.36 `libutil` compatibility stub; loading a newer host copy breaks PyMuPDF.
The mise installer downloads a checksum-verified official Debian libc6 package,
extracts only `libutil.so.1` and its copyright file into the tool root, and
preloads that private stub in the MCP Python process. It does not replace the
host's glibc or alter the KiCad installation. The URL and SHA-256 are recorded
in [the compatibility installer](../scripts/install-kicad-mcp-compat.py).
The installer checks the release's root `requirements.txt` against the copied
[lock input](../.mise/locks/http-kicad-mcp/2.9.0/requirements.in) before syncing
the [resolved hash lock](../.mise/locks/http-kicad-mcp/2.9.0/requirements.txt).

## CI caching

The existing pinned mise action caches its installed-tool directory, including
the MCP's built `dist`, `node_modules` and private Python packages. The three
full-install jobs restore the same cache; Repository checks saves it, while
the report and firmware jobs are restore-only. The lockfile dry-run job does
not install or cache tools.

The cache key includes the action's normal configuration/platform identity
plus a hash of the installer, launchers and dependency locks. A changed recipe
therefore cannot reuse an older completed installation. Cache misses run the
same locked mise installation; no additional npm/uv archive cache is required.
This describes the configured cache behavior, not a measured hosted warm run.

## Workflow coverage

The evaluation uses disposable copies of `hardware/controller/`; original
board and schematic files are not experiment targets. Record observed results
separately from upstream capability claims. In particular, compare native
UUIDs, hierarchy/instances, `Requirements` fields, pad/net assignments and group
membership after edits, and run our own traceability checks on the copies.

The server initialized and exposed 250 tools without a display, with its SWIG
backend reporting `realtime=false`. The 2026-11-15 evaluation used the native
designs from commit `62c833eef7e817568925fd1b691a24711fc974c0` and recorded 43
successful tool calls across six initial runs. Neither display variable was
present. Representative preservation and rendering checks were repeated after
the final dependency/renderer integration.

| Existing work | Observed result | Boundary |
| --- | --- | --- |
| Read components, fields, pads and board state | Passed on the output design | File-backed state; not live editor synchronization |
| Edit schematic custom properties | Added, read and removed a hidden temporary field while retaining `Requirements` | Tested edits, not every schematic transformation |
| Edit a reused sensor sheet | Shared R10 retained all eight instance paths and references | New hierarchy construction was not tested |
| Move and reopen footprints | Moved R200 by 0.5 mm, saved/reloaded, restored/reloaded | Identity and group membership retained |
| Route editing | Added a 1 mm GND trace, queried its persisted UUID and deleted it | Full autorouting was not exercised |
| Copper fill | Refilled six zones headlessly | Design constraints still need normal review |
| Placement suggestions | Scoped dry-run completed | Its overlap score worsened from 6 to 9 in this short probe; no placement-quality claim |
| Checks | ERC/DRC completed and matched direct CLI reports | Existing findings below remain unresolved |
| Exports | Schematic PDF, board PDF/SVG, four-layer Gerbers/drills, positions, BOM and STEP | Raw BOM needs purchasing filters/custom formatting |
| Previews | Board and schematic PNGs produced nonblank images | Final runtime verifies PyMuPDF without relying on host converters |

After the reversible edits, both disposable test trees returned all 20 native
schematic/PCB files byte-identically to their baselines. UUIDs, properties,
hierarchy, pad/net assignments, groups and routing were also compared
structurally. Our native traceability checker passed on the copy: 20 files,
257 footprints. All 140 original files under `hardware/controller/` remained
unchanged. This is bounded preservation evidence for the operations tested.

Direct pinned KiCad CLI checks on a pristine copy agreed with the MCP:

- ERC reported two existing `pin_to_pin` errors.
- DRC with schematic parity reported zero errors and 53 warnings: 48 footprint
  field mismatches and five footprint/symbol mismatches. Zone refill retained
  those counts.
- The CLI commands returned zero without the option that makes violations
  nonzero. Process/tool success therefore did not mean a clean design.

The raw BOM grouped all 76 output-board footprints into 57 rows, including
mechanical/access features, and did not retain the requested `Requirements`
column. Position export produced 61 rows. Keep the quotation workflow's
reference filtering and matched BOM/CPL accounting; do not substitute these
raw files directly. JLCPCB sourcing/API tools were not exercised here, and this
integration does not replace the existing full-assembly quotation workflow.

### Previously desktop-dependent operations

Earlier work used native **Place Off-Board Footprints** and **Tools →
Multi-Channel → Repeat Layout**, recorded in the
[hardware verification history](../hardware/controller/verification.md).
The pinned server has no dedicated native wrapper for either operation.

It provides `suggest_placement`, `hierarchical_place`, grouping and batch
movement. These are alternative placement mechanisms, not proof of executing
KiCad's native repeat-layout command. Generic GUI-driver tools can invoke
menus, but still require a running KiCad window/helper plugin; complete native
dialog automation has not been verified here. Experimental IPC also requires
a running KiCad editor. Neither is required for the SWIG file backend.

### Checks and exports to retain

- `scripts/hardware_trace.py` remains responsible for requirement fields,
  repeated-sheet identity and schematic/PCB reconciliation. The MCP has no
  RQML-specific integration.
- `scripts/board_images.py` remains responsible for committed SVG palettes,
  metadata normalization, exact views and freshness. Generic MCP SVG exports
  are not byte-compatible substitutes for that workflow.
- ERC/DRC and connectivity comparisons remain separate from MCP success flags.
  A successful edit or export does not establish a valid circuit or layout.

## Updating the pinned tool

Review a new upstream release and its archive checksum, Node lockfile and root
Python requirements. Update the mise declaration and copied input together,
then regenerate the Python hash lock with the command in its header. Refresh
`mise.lock` using the normal documented lock workflow and reinstall the tool
through mise. Installer/launcher changes at the same upstream version require
`mise install --locked --force http:kicad-mcp` locally; CI recipe hashes prevent
restoring the previous installation. Repeat startup and disposable-copy
preservation checks before relying on changed tools.
