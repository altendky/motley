#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Exercise functional allocation failures and physical component identity."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import hardware_groups as groups


class HardwareGroupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.catalog = Path("functional-groups.toml")
        self.write(str(self.catalog), '''version = 1
[groups."output.control"]
description = "Local controller and its supporting interface circuitry."
boards = ["top"]
[groups."diagnostics.access"]
description = "Physical probing and service access."
boards = ["top"]
[groups."mechanical.mounting"]
description = "Board mounting features."
boards = ["top"]
''')
        self.write("top.kicad_sch", '''(kicad_sch (uuid "root")
          (sheet (uuid "left") (property "Sheetfile" "leaf.kicad_sch"))
          (sheet (uuid "right") (property "Sheetfile" "leaf.kicad_sch")))''')
        self.write("leaf.kicad_sch", '''(kicad_sch (uuid "leaf")
          (symbol (uuid "part") (unit 1) (on_board yes) (in_bom yes)
            (property "Reference" "R1")
            (property "FunctionalGroup" "output.control")
            (instances (project "top"
              (path "/root/left" (reference "R10"))
              (path "/root/right" (reference "R11"))))))''')
        self.write("top.kicad_pcb", '''(kicad_pcb
          (footprint "fixture" (uuid "fp-left") (path "/root/left/part")
            (property "Reference" "R90")
            (property "FunctionalGroup" "output.control"))
          (footprint "fixture" (uuid "fp-right") (path "/root/right/part")
            (property "Reference" "R91")
            (property "FunctionalGroup" "output.control")))''')

    def write(self, name, text):
        (self.root / name).write_text(text)

    def replace(self, name, old, new):
        path = self.root / name
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def append(self, name, text):
        path = self.root / name
        contents = path.read_text().rstrip()
        self.assertTrue(contents.endswith(")"))
        path.write_text(contents[:-1] + text + ")")

    def report(self):
        return groups.check(self.root, (Path("top.kicad_sch"),), self.catalog)

    def passes(self):
        result = self.report()
        self.assertTrue(result["ok"], result["errors"])
        return result

    def fails(self, *expected):
        result = self.report()
        self.assertFalse(result["ok"], result)
        diagnostics = "\n".join(result["errors"])
        self.assertTrue(diagnostics)
        for text in expected:
            self.assertIn(text, diagnostics)
        return result

    def test_repeated_sheet_instances_are_distinct_and_references_do_not_bind(self):
        result = self.passes()
        self.assertEqual(len(result["components"]), 2)
        self.assertEqual({row["source_path"] for row in result["components"]},
                         {"/root/left/part", "/root/right/part"})
        self.assertEqual({row["footprint_uuid"] for row in result["components"]},
                         {"fp-left", "fp-right"})
        self.assertEqual({row["group"] for row in result["components"]},
                         {"output.control"})
        self.assertEqual({row["board"] for row in result["components"]}, {"top"})

    def test_instance_path_must_resolve(self):
        self.replace("leaf.kicad_sch", '"/root/right"', '"/root/stale"')
        self.fails("instance")

    def test_source_and_board_allocations_must_agree(self):
        self.replace("top.kicad_pcb", '"output.control"', '"diagnostics.access"')
        self.fails("FunctionalGroup")

    def test_missing_empty_multiple_and_unknown_groups_fail(self):
        field = '(property "FunctionalGroup" "output.control")'
        for filename in ("leaf.kicad_sch", "top.kicad_pcb"):
            original = (self.root / filename).read_text()
            for replacement in ("", '(property "FunctionalGroup" "")',
                                '(property "FunctionalGroup" "output.control diagnostics.access")',
                                '(property "FunctionalGroup" "unknown.feature")'):
                with self.subTest(filename=filename, replacement=replacement):
                    self.write(filename, original.replace(field, replacement))
                    self.fails("FunctionalGroup")
                self.write(filename, original)

    def test_duplicate_field_is_not_silently_last_value_wins(self):
        for filename in ("leaf.kicad_sch", "top.kicad_pcb"):
            original = (self.root / filename).read_text()
            with self.subTest(filename=filename):
                self.replace(filename, '(property "FunctionalGroup" "output.control")',
                             '(property "FunctionalGroup" "output.control")\n'
                             '(property "FunctionalGroup" "diagnostics.access")')
                self.fails("duplicate", filename,
                           "part" if filename == "leaf.kicad_sch" else "fp-left")
            self.write(filename, original)

    def test_catalog_board_scope_is_enforced(self):
        self.replace(str(self.catalog), 'boards = ["top"]', 'boards = ["another-board"]')
        self.fails("top")

    def test_multi_unit_component_is_counted_once_per_sheet_instance(self):
        self.write("leaf.kicad_sch", '''(kicad_sch (uuid "leaf")
          (symbol (uuid "unit-one") (unit 1) (property "Reference" "K1")
            (property "FunctionalGroup" "output.control"))
          (symbol (uuid "unit-two") (unit 2) (property "Reference" "K1")
            (property "FunctionalGroup" "output.control")))''')
        self.replace("top.kicad_pcb", "/root/left/part", "/root/left/unit-two")
        self.replace("top.kicad_pcb", "/root/right/part", "/root/right/unit-one")
        self.assertEqual(len(self.passes()["components"]), 2)
        self.replace("leaf.kicad_sch", '(unit 2) (property "Reference" "K1")\n'
                     '            (property "FunctionalGroup" "output.control")',
                     '(unit 2) (property "Reference" "K1")\n'
                     '            (property "FunctionalGroup" "diagnostics.access")')
        self.fails("multi-unit")

    def test_duplicate_unit_number_cannot_hide_a_physical_component(self):
        self.append("leaf.kicad_sch", '''(symbol (uuid "duplicate-unit") (unit 1)
          (property "Reference" "R10")
          (property "FunctionalGroup" "output.control")
          (instances (project "top"
            (path "/root/left" (reference "R10"))
            (path "/root/right" (reference "R11")))))''')
        self.fails("unit")

    def test_dnp_and_bom_excluded_components_still_require_allocation(self):
        original = (self.root / "leaf.kicad_sch").read_text()
        for attributes in ("(dnp yes) (in_bom yes)", "(in_bom no)"):
            with self.subTest(attributes=attributes):
                self.write("leaf.kicad_sch", original.replace("(in_bom yes)", attributes))
                self.assertEqual(len(self.passes()["components"]), 2)
                self.replace("leaf.kicad_sch", '(property "FunctionalGroup" "output.control")', "")
                self.fails("FunctionalGroup")
            self.write("leaf.kicad_sch", original)

    def test_bom_only_symbols_are_allocated_without_footprints(self):
        self.replace("leaf.kicad_sch", "(on_board yes)", "(on_board no)")
        self.write("top.kicad_pcb", "(kicad_pcb)")
        result = self.passes()
        self.assertEqual(len(result["components"]), 2)
        self.assertTrue(all(row["footprint_uuid"] is None for row in result["components"]))
        self.replace("leaf.kicad_sch", '(property "FunctionalGroup" "output.control")', "")
        self.fails("FunctionalGroup")

    def test_board_only_mounting_features_are_allocated(self):
        self.append("top.kicad_pcb", '''(footprint "mount" (uuid "mount")
          (attr board_only exclude_from_bom) (property "Reference" "H1")
          (property "FunctionalGroup" "mechanical.mounting"))''')
        result = self.passes()
        self.assertEqual(len(result["components"]), 3)
        mount = next(row for row in result["components"] if row["footprint_uuid"] == "mount")
        self.assertIsNone(mount["source_path"])
        self.assertEqual(mount["group"], "mechanical.mounting")
        self.replace("top.kicad_pcb", '(property "FunctionalGroup" "mechanical.mounting")', "")
        self.fails("FunctionalGroup")

    def test_unmarked_orphan_footprints_do_not_become_board_only(self):
        self.append("top.kicad_pcb", '''(footprint "orphan" (uuid "orphan")
          (property "Reference" "H1")
          (property "FunctionalGroup" "mechanical.mounting"))''')
        self.fails("path")

    def test_virtual_power_symbols_and_library_definitions_are_not_components(self):
        self.append("leaf.kicad_sch", '''(symbol (uuid "flag")
          (property "Reference" "#FLG01"))
          (lib_symbols (symbol "Device:R"
            (property "Reference" "R")
            (symbol "R_0_1" (rectangle (start 0 0) (end 1 1)))))''')
        self.assertEqual(len(self.passes()["components"]), 2)

    def test_duplicate_footprint_does_not_replace_missing_instance(self):
        self.replace("top.kicad_pcb", "/root/right/part", "/root/left/part")
        self.fails("duplicate")

    def test_dangling_source_path_fails(self):
        self.replace("top.kicad_pcb", "/root/right/part", "/root/right/deleted")
        self.fails("path")

    def test_component_with_no_footprint_fails(self):
        self.write("top.kicad_pcb", "(kicad_pcb)")
        self.fails("footprint")

    def test_duplicate_native_uuids_fail(self):
        self.replace("top.kicad_pcb", '"fp-right"', '"fp-left"')
        self.fails("UUID")

    def test_hierarchy_cycle_missing_file_and_malformed_native_fail(self):
        original = (self.root / "top.kicad_sch").read_text()
        for replacement in ("top.kicad_sch", "missing.kicad_sch"):
            with self.subTest(replacement=replacement):
                self.write("top.kicad_sch", original.replace("leaf.kicad_sch", replacement))
                self.fails()
        self.write("top.kicad_sch", original)
        self.write("leaf.kicad_sch", "(kicad_sch (symbol")
        self.fails()

    def test_missing_or_invalid_catalog_fails(self):
        original = (self.root / self.catalog).read_text()
        for text in ('version = 99\n[groups]\n',
                     'version = 1\n[groups]\n',
                     'version = 1\n[groups."output.control"]\nboards = "top"\n',
                     '[groups."output.control"\n'):
            with self.subTest(text=text):
                self.write(str(self.catalog), text)
                self.fails()
        self.write(str(self.catalog), original)
        (self.root / self.catalog).unlink()
        self.fails()

    def test_checker_and_json_cli_never_rewrite_inputs(self):
        before = {p: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        self.passes()
        output = io.StringIO()
        with redirect_stdout(output):
            status = groups.main(["--root", str(self.root), "--catalog", str(self.catalog),
                                  "--design", "top.kicad_sch", "--json"])
        self.assertEqual(status, 0)
        self.assertTrue(json.loads(output.getvalue())["ok"])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.iterdir() if p.is_file()})
        self.replace("leaf.kicad_sch", '"output.control"', '"unknown.feature"')
        invalid = {p: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        output = io.StringIO()
        with redirect_stdout(output):
            status = groups.main(["--root", str(self.root), "--catalog", str(self.catalog),
                                  "--design", "top.kicad_sch", "--json"])
        self.assertEqual(status, 1)
        self.assertFalse(json.loads(output.getvalue())["ok"])
        self.assertEqual(invalid, {p: p.read_bytes() for p in self.root.iterdir() if p.is_file()})


if __name__ == "__main__":
    unittest.main()
