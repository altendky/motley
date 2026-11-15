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
| [motley-carrier-back.svg](motley-carrier-back.svg) | `../../motley-carrier.kicad_pcb` | Controller/AC input, back copper viewed from the top |
| [motley-carrier-in1.svg](motley-carrier-in1.svg) | `../../motley-carrier.kicad_pcb` | Inner 1, low-voltage ground |
| [motley-carrier-in2.svg](motley-carrier-in2.svg) | `../../motley-carrier.kicad_pcb` | Inner 2, separate supplies and USB ground-reference corridor |
| [motley-ac-output.svg](motley-ac-output.svg) | `../../motley-ac-output.kicad_pcb` | Single AC output, front |
| [motley-ac-output-back.svg](motley-ac-output-back.svg) | `../../motley-ac-output.kicad_pcb` | Back copper viewed from the top, with front reference outlines |
| [motley-ac-output-in1.svg](motley-ac-output-in1.svg) | `../../motley-ac-output.kicad_pcb` | Inner 1, low-voltage ground |
| [motley-ac-output-in2.svg](motley-ac-output-in2.svg) | `../../motley-ac-output.kicad_pcb` | Inner 2, separate local 3.3 V, logic 5 V and actuator 5 V regions |
| [motley-sensors.svg](motley-sensors.svg) | `../../motley-sensors.kicad_pcb` | Sensor mux/connectors, front |
| [motley-sensors-back.svg](motley-sensors-back.svg) | `../../motley-sensors.kicad_pcb` | Sensor mux/connectors, back copper viewed from the top |
| [motley-sensors-in1.svg](motley-sensors-in1.svg) | `../../motley-sensors.kicad_pcb` | Inner 1, ground with cut corridors excluded |
| [motley-sensors-in2.svg](motley-sensors-in2.svg) | `../../motley-sensors.kicad_pcb` | Inner 2, sensor supply with cut corridors excluded |

The exporter uses the KiCad version pinned in `mise.toml`, an isolated default
theme, fixed layers/options, stable titles and descriptions, and LF line endings.
It removes export timestamps rather than retaining previous dates or inventing
a date. Front copper is salmon, back copper blue, inner 1 green, inner 2 tan,
mask openings/pads gray and labels dark. Plotting uses temporary board/project copies, so KiCad cannot change
checkout display settings. Saved copper zones are plotted without refilling or modifying CAD.
The view list and palette live in `scripts/board_images.py`. Matching outputs are
left untouched even in write mode. Reproducibility assumes the same pinned tools;
a KiCad upgrade requires reviewing and regenerating the derivatives.

All copper layers are viewed from the top; inner views retain front reference
outlines for context. They plot actual saved layer copper, not front-side mask
openings. Supply regions on inner 2 share a display colour but remain distinct
electrical nets; the carrier USB reference region there is GND. Ground and power
planes are confined to the isolated low-voltage regions, not mains or PE.
Plated mains pad/via rings also appear in an inner layer's colour; that does
not connect them to the surrounding low-voltage ground or supply planes.

Freshness verifies correspondence to the saved board, not electrical correctness,
routing completion, fabrication readiness or mains safety. Transient PDF/PNG
review exports remain in the ignored `hardware/controller/review/` directory.
