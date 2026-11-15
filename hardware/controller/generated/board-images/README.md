# Generated board images

These versioned SVGs are **generated derivatives**, not design sources. Edit the
native boards in `hardware/controller/`, then regenerate from the repository root:

```sh
mise exec -- uv run scripts/board_images.py --write
```

Check freshness without changing any CAD or images:

```sh
mise exec -- uv run scripts/board_images.py --check
```

Local pre-commit always runs a `--fix` formatter, including deletion-only commits.
It regenerates missing, changed or stale expected SVGs and fails after updates;
review and stage the regenerated files, then retry. Matching files stay untouched.
Recreated or new SVGs keep failing until added to the Git index.
CI's **Repository checks** job explicitly runs the read-only `--check` and skips
only the formatter hook during its remaining pre-commit checks. Unexpected SVGs
and exporter errors fail in both modes. Commit the images together with their
matching native board changes. Do not hand-edit these SVGs.

| Derivative | Native source | View |
| --- | --- | --- |
| [motley-carrier.svg](motley-carrier.svg) | `../../motley-carrier.kicad_pcb` | Controller/AC input, front |
| [motley-ac-output.svg](motley-ac-output.svg) | `../../motley-ac-output.kicad_pcb` | Single AC output, front |
| [motley-ac-output-back.svg](motley-ac-output-back.svg) | `../../motley-ac-output.kicad_pcb` | Back copper viewed from the top, with front reference outlines |
| [motley-sensors.svg](motley-sensors.svg) | `../../motley-sensors.kicad_pcb` | Sensor mux/connectors, front |

The exporter uses the KiCad version pinned in `mise.toml`, an isolated default
theme, fixed layers/options, stable titles and descriptions, and LF line endings.
It removes export timestamps rather than retaining previous dates or inventing
a date. Front copper is salmon, back copper blue, mask openings/pads gray and
labels dark. Plotting uses temporary board/project copies, so KiCad cannot change
checkout display settings. Saved copper zones are plotted without refilling or modifying CAD.
The view list and palette live in `scripts/board_images.py`. Matching outputs are
left untouched even in write mode. Reproducibility assumes the same pinned tools;
a KiCad upgrade requires reviewing and regenerating the derivatives.

Freshness verifies correspondence to the saved board, not electrical correctness,
routing completion, fabrication readiness or mains safety. Transient PDF/PNG
review exports remain in the ignored `hardware/controller/review/` directory.
