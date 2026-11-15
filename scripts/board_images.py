#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Generate/check derivative board SVGs (MOT-CI-004); never edit native CAD."""

import argparse
from dataclasses import dataclass
from html import escape
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("hardware/controller/generated/board-images")
REGENERATE = "mise exec -- uv run scripts/board_images.py --write"


@dataclass(frozen=True)
class View:
    filename: str
    board: str
    layers: str
    title: str


VIEWS = (
    View("motley-carrier.svg", "motley-carrier",
         "F.Cu,F.Mask,F.SilkS,Dwgs.User,Edge.Cuts", "Controller and AC input - top"),
    View("motley-carrier-back.svg", "motley-carrier",
         "B.Cu,B.Mask,F.SilkS,Dwgs.User,Edge.Cuts", "Controller and AC input - back copper, viewed from top"),
    View("motley-ac-output.svg", "motley-ac-output",
         "F.Cu,F.Mask,F.SilkS,Dwgs.User,Edge.Cuts", "AC output - top"),
    View("motley-ac-output-back.svg", "motley-ac-output",
         "B.Cu,B.Mask,F.SilkS,Dwgs.User,Edge.Cuts", "AC output - back copper, viewed from top"),
    View("motley-sensors.svg", "motley-sensors",
         "F.Cu,F.Mask,F.SilkS,Dwgs.User,Edge.Cuts", "Sensor mux and connectors - top"),
    View("motley-sensors-back.svg", "motley-sensors",
         "B.Cu,B.Mask,F.SilkS,Dwgs.User,Edge.Cuts", "Sensor mux and connectors - back copper, viewed from top"),
)


class ExportError(Exception):
    pass


def normalize_svg(source: str, view: View) -> bytes:
    """Replace volatile metadata/palette, preserving KiCad's vector geometry."""
    # KiCad also uses <desc> inside stroked-text groups for reference labels.
    # Change document metadata only; keep those per-item descriptions intact.
    header, separator, body = source.partition("<g")
    for tag, value in (
        ("title", view.title),
        ("desc", f"Generated from hardware/controller/{view.board}.kicad_pcb "
         "by scripts/board_images.py. Do not edit this derivative."),
    ):
        header, count = re.subn(
            rf"<{tag}>.*?</{tag}>", f"<{tag}>{escape(value)}</{tag}>",
            header, flags=re.DOTALL,
        )
        if count != 1:
            raise ExportError(f"{view.filename}: expected exactly one SVG {tag}")
    source = header + separator + body
    # Highlight mask openings as pads. Colours are review presentation only.
    for colour in ("#D864FF", "#02FFEE"):
        source = source.replace(
            f"fill:{colour}; fill-opacity:0.4000",
            "fill:#A8AFBA; fill-opacity:1.0000",
        ).replace(colour, "#A8AFBA")
    for before, after in {
        "#C83434": "#E9AFA5", "#4D7FC4": "#AAC6EB", "#F2EDA1": "#20252B",
        "#D0D2CD": "#20252B", "#C2C2C2": "#65717E",
    }.items():
        source = source.replace(before, after)
    source = "\n".join(line.rstrip() for line in source.splitlines()).rstrip() + "\n"
    try:
        svg = ET.fromstring(source)
    except ET.ParseError as exc:
        raise ExportError(f"{view.filename}: invalid SVG: {exc}") from exc
    if svg.tag != "{http://www.w3.org/2000/svg}svg":
        raise ExportError(f"{view.filename}: exporter did not produce an SVG")
    return source.encode("utf-8")


def export_environment(config: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update(KICAD_CONFIG_HOME=str(config / "kicad"),
               XDG_CONFIG_HOME=str(config), LC_ALL="C", TZ="UTC")
    return env


def run_kicad(arguments: list[str], env: dict[str, str]) -> str:
    try:
        result = subprocess.run(
            ["kicad-cli", *arguments], env=env, text=True, encoding="utf-8",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
        )
    except FileNotFoundError as exc:
        raise ExportError("kicad-cli is unavailable; run mise install and use mise exec") from exc
    except subprocess.CalledProcessError as exc:
        raise ExportError(f"KiCad failed (exit {exc.returncode}):\n{exc.stdout}") from exc
    return result.stdout.strip()


def render_views(root: Path, work: Path) -> dict[str, bytes]:
    env = export_environment(work / "config")
    with (root / "mise.toml").open("rb") as source:
        version = tomllib.load(source)["tools"]["http:kicad"]["version"]
    actual = run_kicad(["version"], env)
    if actual != version:
        raise ExportError(f"KiCad {version} is required, found {actual!r}; run mise install")
    # KiCad can save .kicad_prl display settings even during CLI plotting.
    # Plot copies, retaining project text variables but protecting the checkout.
    inputs = work / "inputs"
    inputs.mkdir()
    for board in sorted({view.board for view in VIEWS}):
        for suffix in (".kicad_pcb", ".kicad_pro"):
            source = root / "hardware/controller" / f"{board}{suffix}"
            if source.exists() or suffix == ".kicad_pcb":
                shutil.copyfile(source, inputs / source.name)
    rendered = {}
    for view in VIEWS:
        target = work / view.filename
        run_kicad([
            "pcb", "export", "svg", str(inputs / f"{view.board}.kicad_pcb"),
            "--output", str(target), "--layers", view.layers,
            "--theme", "_builtin_default", "--mode-single", "--page-size-mode", "2",
            "--exclude-drawing-sheet", "--drill-shape-opt", "2", "--scale", "1",
        ], env)
        rendered[view.filename] = normalize_svg(target.read_text(encoding="utf-8"), view)
    return rendered


def synchronize(output: Path, rendered: dict[str, bytes], write: bool,
                fail_on_change: bool = False) -> list[str]:
    """Check exact derivatives; explicit writes retain already matching files."""
    issues = [f"unexpected SVG: {p.name}" for p in sorted(output.glob("*.svg"))
              if p.name not in rendered]
    for name, content in rendered.items():
        path = output / name
        existing = path.read_bytes() if path.exists() else None
        if existing == content:
            continue
        if write:
            output.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            print(f"Updated {path}")
            if fail_on_change:
                # pre-commit's diff cannot always see a recreated untracked SVG.
                issues.append(f"regenerated SVG: {name}")
        else:
            issues.append(f"{'missing' if existing is None else 'stale'} SVG: {name}")
    return issues


def unindexed_images(root: Path, names: dict[str, bytes]) -> list[str]:
    """A recreated untracked file must not make a staged deletion pass on retry."""
    missing = []
    for name in names:
        try:
            indexed = subprocess.run(
                ["git", "-C", str(root), "cat-file", "-s", f":{(OUTPUT / name).as_posix()}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            )
        except FileNotFoundError as exc:
            raise ExportError("git is required for the pre-commit formatter") from exc
        # Intent-to-add entries have an empty blob and are not a committed SVG.
        if indexed.returncode or indexed.stdout.strip() == "0":
            missing.append(name)
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check freshness without modifying files (default)")
    mode.add_argument("--write", action="store_true", help="regenerate the committed SVG derivatives")
    mode.add_argument("--fix", action="store_true", help="regenerate and fail if changed, for pre-commit")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        with tempfile.TemporaryDirectory(prefix="motley-board-images-") as temporary:
            rendered = render_views(root, Path(temporary))
        issues = synchronize(root / OUTPUT, rendered, args.write or args.fix,
                             fail_on_change=args.fix)
        if args.fix:
            issues.extend(f"SVG must be staged with git add: {name}"
                          for name in unindexed_images(root, rendered))
    except (ExportError, OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        print(f"Board SVG export failed: {exc}", file=sys.stderr)
        return 1
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        if args.fix:
            print("Review and stage regenerated SVGs, then rerun pre-commit.\n"
                  "Remove unexpected SVGs explicitly.", file=sys.stderr)
        else:
            print(f"Regenerate with: {REGENERATE}\nRemove unexpected SVGs explicitly.", file=sys.stderr)
        return 1
    print(f"Board SVG derivatives: {len(rendered)} views; {'updated' if args.write else 'current'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
