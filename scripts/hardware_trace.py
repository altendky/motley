#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Check native KiCad requirement annotations, not electrical correctness.

RQML checks file drift independently. Component UUID fragments remain navigation
hints to RQML; this checker reconciles native hierarchical symbol/footprint paths.
"""

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

type Node = list[str | Node]
TOKEN = re.compile(r'\s*(\(|\)|"(?:\\.|[^"\\])*"|[^()\s"]+)')
DESIGNS = tuple(Path("hardware/controller") / f"{name}.kicad_sch" for name in
                ("motley-carrier", "motley-ac-output", "motley-sensors"))


class TraceError(ValueError):
    """A malformed or unresolved native trace target."""


def parse(text: str) -> Node:
    """Read KiCad's list/string structure without depending on KiCad or exports."""
    stack: list[Node] = []
    roots: list[Node] = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if not match:
            if text[position:].strip():
                raise TraceError(f"invalid S-expression at character {position}")
            break
        token = match[1]
        position = match.end()
        if token == "(":
            node: Node = []
            (stack[-1] if stack else roots).append(node)
            stack.append(node)
        elif token == ")":
            if not stack:
                raise TraceError("unmatched closing parenthesis")
            stack.pop()
        else:
            if not stack:
                raise TraceError("atom outside root expression")
            if token.startswith('"'):
                token = re.sub(r"\\(.)", lambda m: {"n": "\n", "r": "\r", "t": "\t"}.get(m[1], m[1]), token[1:-1])
            stack[-1].append(token)
    if stack or len(roots) != 1:
        raise TraceError("expected one balanced root expression")
    return roots[0]


def children(node: Node, key: str) -> list[Node]:
    return [item for item in node if isinstance(item, list) and item and item[0] == key]


def value(node: Node, key: str, default: str = "") -> str:
    found = children(node, key)
    return str(found[0][1]) if found and len(found[0]) > 1 else default


def properties(node: Node) -> dict[str, str]:
    found = children(node, "property")
    names = [str(item[1]) for item in found]
    if len(names) != len(set(names)):
        raise TraceError("duplicate property name")
    return {str(item[1]): str(item[2]) for item in found}


def check(root: Path, designs: tuple[Path, ...] = DESIGNS,
          spec: Path = Path("requirements.rqml")) -> dict:
    root = root.resolve()
    document = ET.parse(root / spec).getroot()
    known = {item.attrib["id"] for item in document.findall(".//{*}req")}
    links: set[Path] = set()
    for edge in document.findall(".//{*}edge"):
        for side, other in (("from", "to"), ("to", "from")):
            uri = edge.get(side, "")
            if edge.get(other) not in known or not uri:
                continue
            parsed = urlsplit(uri)
            if not parsed.scheme or parsed.scheme == "file":
                links.add((root / unquote(parsed.path)).resolve())
    files: set[Path] = set()
    errors: list[str] = []
    rows: list[dict] = []

    def display(path: Path) -> str:
        return str(path.relative_to(root))

    def load(path: Path, kind: str) -> Node:
        path = path.resolve()
        display(path)  # Native sources outside the governed repository are unsupported.
        files.add(path)
        node = parse(path.read_text())
        if not node or node[0] != kind:
            raise TraceError(f"{display(path)}: expected {kind}")
        return node

    def requirements(node: Node, where: str) -> frozenset[str]:
        ids = properties(node).get("Requirements", "").split()
        if not ids:
            errors.append(f"{where}: missing Requirements field")
        if len(ids) != len(set(ids)):
            errors.append(f"{where}: duplicate requirement identifier")
        unknown = set(ids) - known
        if unknown:
            errors.append(f"{where}: unknown requirements {', '.join(sorted(unknown))}")
        return frozenset(ids)

    for design in designs:
        try:
            schematic = (root / design).resolve()
            project = schematic.stem
            symbols: dict[str, dict] = {}
            groups: dict[tuple[str, str], list[str]] = defaultdict(list)
            seen_files: dict[Path, Node] = {}

            def walk(path: Path, scope: str, ancestors: tuple[Path, ...]) -> None:
                path = path.resolve()
                if path in ancestors:
                    raise TraceError(f"{display(path)}: cyclic schematic hierarchy")
                if path not in seen_files:
                    seen_files[path] = load(path, "kicad_sch")
                node = seen_files[path]
                if not scope:
                    scope = "/" + value(node, "uuid")
                    if scope == "/":
                        raise TraceError(f"{display(path)}: missing root UUID")
                uuids: set[str] = set()
                for item in children(node, "symbol") + children(node, "sheet"):
                    uid = value(item, "uuid")
                    if not uid or uid in uuids:
                        raise TraceError(f"{display(path)}: missing/duplicate source UUID {uid}")
                    uuids.add(uid)
                    props = properties(item)
                    if item[0] == "sheet":
                        requirements(item, f"{display(path)} sheet {uid}")
                        filename = props.get("Sheetfile", "")
                        if not filename:
                            raise TraceError(f"{display(path)}: sheet {uid} lacks Sheetfile")
                        walk(path.parent / filename, scope + "/" + uid, ancestors + (path,))
                        continue
                    reference = props.get("Reference", "")
                    if reference.startswith("#") or value(item, "on_board", "yes") == "no":
                        continue
                    # Instance reference is used only to associate multi-unit symbols,
                    # never to bind a footprint. Repeated sheets have distinct scopes.
                    for instances in children(item, "instances"):
                        for instance in children(instances, "project"):
                            if len(instance) > 1 and instance[1] == project:
                                entries = [entry for entry in children(instance, "path")
                                           if len(entry) > 1 and entry[1] == scope]
                                if len(entries) != 1:
                                    raise TraceError(f"{display(path)} {uid}: missing/duplicate declared instance path {scope}")
                                reference = value(entries[0], "reference", reference)
                    target = scope + "/" + uid
                    if target in symbols:
                        raise TraceError(f"duplicate source instance path {target}")
                    ids = requirements(item, f"{display(path)} {reference}")
                    symbols[target] = dict(file=display(path), reference=reference,
                                           requirements=ids, unit=value(item, "unit", "1"))
                    groups[scope, reference].append(target)

            walk(schematic, "", ())
            group_for: dict[str, tuple[str, str]] = {}
            for key, targets in groups.items():
                units = [symbols[target]["unit"] for target in targets]
                fields = {symbols[target]["requirements"] for target in targets}
                if len(units) != len(set(units)) or len(fields) != 1:
                    raise TraceError(f"{key}: duplicate units or inconsistent multi-unit Requirements")
                group_for.update((target, key) for target in targets)
            boardfile = schematic.with_suffix(".kicad_pcb")
            board = load(boardfile, "kicad_pcb")
            matched: set[tuple[str, str]] = set()
            footprint_ids: set[str] = set()
            for footprint in children(board, "footprint"):
                props = properties(footprint)
                reference = props.get("Reference", "")
                uid = value(footprint, "uuid")
                if not uid or uid in footprint_ids:
                    raise TraceError(f"{display(boardfile)}: missing/duplicate footprint UUID {uid}")
                footprint_ids.add(uid)
                where = f"{display(boardfile)} {reference}"
                ids = requirements(footprint, where)
                target = value(footprint, "path")
                board_only = any("board_only" in attr[1:] for attr in children(footprint, "attr"))
                if board_only and not target:
                    source = None
                elif target not in symbols:
                    errors.append(f"{where}: missing/dangling schematic path {target!r}")
                    continue
                else:
                    source = symbols[target]
                    group = group_for[target]
                    if group in matched:
                        errors.append(f"{where}: duplicate footprint for schematic component {target}")
                    matched.add(group)
                    if ids != source["requirements"]:
                        errors.append(f"{where}: Requirements differ from schematic path {target}")
                rows.append(dict(board=display(boardfile), reference=reference,
                                 footprint_uuid=uid, source_path=target or None,
                                 source_file=source["file"] if source else None,
                                 requirements=sorted(ids)))
            for group in groups.keys() - matched:
                errors.append(f"{display(schematic)}: component {group} has no PCB footprint")
        except (OSError, ValueError, IndexError) as exc:
            errors.append(f"{design}: {exc}")
    for path in sorted(files):
        if path not in links:
            errors.append(f"{display(path)}: no explicit RQML file relationship")
    return dict(ok=not errors, scope="Annotation integrity only; no electrical or hardware acceptance claim",
                files=[display(path) for path in sorted(files)], components=rows, errors=errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", type=Path, default=Path("requirements.rqml"))
    parser.add_argument("--design", type=Path, action="append", help="Root schematic; repeat for several boards")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = check(args.root, tuple(args.design) if args.design else DESIGNS, args.spec)
    except (OSError, ValueError, ET.ParseError) as exc:
        report = dict(ok=False, errors=[str(exc)])
    if args.json:
        print(json.dumps(report, indent=2))
    elif report["ok"]:
        print(f"Hardware annotations: {len(report['files'])} files, {len(report['components'])} footprints; pass")
        print(report["scope"])
    else:
        print("Hardware annotation check failed:", file=sys.stderr)
        for error in report["errors"]:
            print(f"  {error}", file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
