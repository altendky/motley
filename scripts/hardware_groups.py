#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Check functional allocation of native KiCad components; no cost calculation.

Run directly from any directory. Allocation is explicit in FunctionalGroup
properties, never inferred from sheet names, reference ranges or placement.
"""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import tomllib

sys.dont_write_bytecode = True
from hardware_trace import DESIGNS, TraceError, children, parse, properties, value

CATALOG = Path("hardware/controller/functional-groups.toml")
GROUP_ID = re.compile(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*")


def load_catalog(path: Path) -> dict:
    catalog = tomllib.loads(path.read_text())
    if set(catalog) != {"version", "groups"} or type(catalog["version"]) is not int or catalog["version"] != 1:
        raise TraceError("group catalog must contain version = 1 and groups")
    groups = catalog["groups"]
    if not isinstance(groups, dict) or not groups:
        raise TraceError("group catalog must define at least one group")
    for name, entry in groups.items():
        if not GROUP_ID.fullmatch(name) or not isinstance(entry, dict) or set(entry) != {"description", "boards"}:
            raise TraceError(f"invalid group catalog entry {name!r}")
        description, boards = entry["description"], entry["boards"]
        if not isinstance(description, str) or not description.strip():
            raise TraceError(f"group {name}: missing description")
        if (not isinstance(boards, list) or not boards
                or any(not isinstance(board, str) or not GROUP_ID.fullmatch(board) for board in boards)
                or len(boards) != len(set(boards))):
            raise TraceError(f"group {name}: boards must be a nonempty unique list of board names")
    return groups


def check(root: Path, designs: tuple[Path, ...] = DESIGNS,
          catalog: Path = CATALOG) -> dict:
    root = root.resolve()
    errors: list[str] = []
    rows: list[dict] = []
    files: set[str] = set()
    try:
        known = load_catalog(root / catalog)
    except (OSError, ValueError) as exc:
        return dict(ok=False, errors=[f"{catalog}: {exc}"], components=[], files=[])

    def load(path: Path, kind: str):
        path = path.resolve()
        relative = str(path.relative_to(root))
        node = parse(path.read_text())
        if node[0] != kind:
            raise TraceError(f"{relative}: expected {kind}")
        files.add(relative)
        return node

    def allocation(item, board: str, where: str) -> str:
        group = properties(item).get("FunctionalGroup", "")
        if not group.strip():
            errors.append(f"{where}: missing or empty FunctionalGroup")
        elif not GROUP_ID.fullmatch(group):
            errors.append(f"{where}: expected exactly one FunctionalGroup identifier, got {group!r}")
        elif group not in known:
            errors.append(f"{where}: unknown FunctionalGroup {group!r}")
        elif board not in known[group]["boards"]:
            errors.append(f"{where}: FunctionalGroup {group!r} is not allowed on board {board}")
        return group

    for design in designs:
        board = design.stem
        try:
            symbols: dict[str, dict] = {}
            components: dict[tuple[str, str], list[str]] = defaultdict(list)

            def walk(path: Path, scope: str, ancestors: tuple[Path, ...]) -> None:
                path = path.resolve()
                if path in ancestors:
                    raise TraceError(f"{path.relative_to(root)}: cyclic schematic hierarchy")
                node = load(path, "kicad_sch")
                if not scope:
                    uid = value(node, "uuid")
                    if not uid:
                        raise TraceError(f"{path.relative_to(root)}: missing root UUID")
                    scope = "/" + uid
                seen: set[str] = set()
                for item in children(node, "symbol") + children(node, "sheet"):
                    uid = value(item, "uuid")
                    if not uid or uid in seen:
                        raise TraceError(f"{path.relative_to(root)}: missing/duplicate source UUID {uid!r}")
                    seen.add(uid)
                    try:
                        props = properties(item)
                    except TraceError as exc:
                        raise TraceError(f"{path.relative_to(root)} {item[0]} {uid}: {exc}") from exc
                    if item[0] == "sheet":
                        filename = props.get("Sheetfile", "")
                        if not filename:
                            raise TraceError(f"{path.relative_to(root)}: sheet {uid} lacks Sheetfile")
                        walk(path.parent / filename, scope + "/" + uid, ancestors + (path,))
                        continue
                    reference = props.get("Reference", "")
                    if reference.startswith("#"):
                        continue
                    if not reference:
                        raise TraceError(f"{path.relative_to(root)}: symbol {uid} lacks Reference")
                    instances = children(item, "instances")
                    if instances:
                        entries = [entry for instance in instances
                                   for project in children(instance, "project")
                                   if len(project) > 1 and project[1] == board
                                   for entry in children(project, "path")
                                   if len(entry) > 1 and entry[1] == scope]
                        if len(entries) != 1:
                            raise TraceError(f"{path.relative_to(root)} {reference}: missing/duplicate declared instance path {scope}")
                        reference = value(entries[0], "reference", reference)
                    target = scope + "/" + uid
                    if target in symbols:
                        raise TraceError(f"duplicate source instance path {target}")
                    where = f"{path.relative_to(root)} {reference} ({target})"
                    symbols[target] = dict(reference=reference, unit=value(item, "unit", "1"),
                                           group=allocation(item, board, where),
                                           on_board=value(item, "on_board", "yes") != "no")
                    components[scope, reference].append(target)

            walk(root / design, "", ())
            component_for = {}
            for key, targets in components.items():
                units = [symbols[target]["unit"] for target in targets]
                if len(units) != len(set(units)):
                    errors.append(f"{design} {key}: duplicate units of physical component")
                if len({symbols[target]["group"] for target in targets}) != 1:
                    errors.append(f"{design} {key}: inconsistent multi-unit FunctionalGroup")
                if len({symbols[target]["on_board"] for target in targets}) != 1:
                    errors.append(f"{design} {key}: inconsistent multi-unit on_board attribute")
                component_for.update((target, key) for target in targets)

            pcb_path = design.with_suffix(".kicad_pcb")
            pcb = load(root / pcb_path, "kicad_pcb")
            matched = set()
            seen_footprints = set()
            for footprint in children(pcb, "footprint"):
                uid = value(footprint, "uuid")
                try:
                    props = properties(footprint)
                except TraceError as exc:
                    raise TraceError(f"{pcb_path} footprint {uid}: {exc}") from exc
                reference = props.get("Reference", "")
                where = f"{pcb_path} {reference}"
                if not uid or uid in seen_footprints:
                    raise TraceError(f"{where}: missing/duplicate footprint UUID {uid!r}")
                seen_footprints.add(uid)
                group = allocation(footprint, board, where)
                target = value(footprint, "path")
                board_only = any("board_only" in attr[1:] for attr in children(footprint, "attr"))
                if board_only and not target:
                    pass
                elif target not in symbols:
                    errors.append(f"{where}: missing/dangling schematic path {target!r}")
                else:
                    source = symbols[target]
                    key = component_for[target]
                    if key in matched:
                        errors.append(f"{where}: duplicate footprint for schematic component {target}")
                    matched.add(key)
                    if not source["on_board"]:
                        errors.append(f"{where}: footprint refers to on_board=no symbol")
                    if group != source["group"]:
                        errors.append(f"{where}: FunctionalGroup differs from schematic path {target}")
                rows.append(dict(board=board, reference=reference, group=group,
                                 source_path=target or None, footprint_uuid=uid))

            for key, targets in components.items():
                if key in matched:
                    continue
                source = symbols[targets[0]]
                if source["on_board"]:
                    errors.append(f"{design} {key}: component has no PCB footprint")
                else:
                    rows.append(dict(board=board, reference=source["reference"],
                                     group=source["group"], source_path=targets[0],
                                     footprint_uuid=None))
        except (OSError, ValueError, IndexError) as exc:
            errors.append(f"{design}: {exc}")
    rows.sort(key=lambda row: (row["board"], row["group"], row["reference"], row["source_path"] or ""))
    return dict(ok=not errors, errors=errors, components=rows, files=sorted(files))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--design", type=Path, action="append", help="Root schematic; repeat for several boards")
    parser.add_argument("--json", action="store_true", help="Include per-component allocations")
    args = parser.parse_args(argv)
    report = check(args.root, tuple(args.design) if args.design else DESIGNS, args.catalog)
    if args.json:
        print(json.dumps(report, indent=2))
    elif report["ok"]:
        print(f"Functional allocation: {len(report['components'])} components; pass")
        for (board, group), count in sorted(Counter((row["board"], row["group"]) for row in report["components"]).items()):
            print(f"  {board}: {group}: {count}")
        print("Allocation integrity only; functional ownership still requires review. No prices are calculated.")
    else:
        print("Functional allocation check failed:", file=sys.stderr)
        for error in report["errors"]:
            print(f"  {error}", file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
