#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Exercise native annotation failures and stable repeated/multi-unit identity."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import hardware_trace as trace


class HardwareTraceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write("requirements.rqml", '''<rqml><requirements>
          <req id="REQ-A"/><req id="REQ-B"/></requirements><trace>
          <edge from="top.kicad_sch" to="REQ-A" type="implements"/>
          <edge from="leaf.kicad_sch" to="REQ-A" type="dependsOn"/>
          <edge from="top.kicad_pcb" to="REQ-A" type="implements"/>
          </trace></rqml>''')
        self.write("top.kicad_sch", '''(kicad_sch (uuid "root")
          (sheet (uuid "left") (property "Sheetfile" "leaf.kicad_sch")
            (property "Requirements" "REQ-A"))
          (sheet (uuid "right") (property "Sheetfile" "leaf.kicad_sch")
            (property "Requirements" "REQ-A")))''')
        self.write("leaf.kicad_sch", '''(kicad_sch (uuid "leaf")
          (symbol (uuid "part") (unit 1) (on_board yes)
            (property "Reference" "R1") (property "Requirements" "REQ-A REQ-B")))''')
        self.write("top.kicad_pcb", '''(kicad_pcb
          (footprint "fixture" (uuid "fp-left") (path "/root/left/part")
            (property "Reference" "R99") (property "Requirements" "REQ-B REQ-A"))
          (footprint "fixture" (uuid "fp-right") (path "/root/right/part")
            (property "Reference" "R2") (property "Requirements" "REQ-A REQ-B")))''')

    def write(self, name, text):
        (self.root / name).write_text(text)

    def replace(self, name, old, new):
        path = self.root / name
        self.assertIn(old, path.read_text())
        path.write_text(path.read_text().replace(old, new))

    def report(self):
        return trace.check(self.root, (Path("top.kicad_sch"),))

    def fails(self, expected):
        result = self.report()
        self.assertFalse(result["ok"])
        self.assertIn(expected, "\n".join(result["errors"]))

    def test_repeated_sheet_paths_match_independent_of_reference_and_field_order(self):
        result = self.report()
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(len(result["components"]), 2)
        self.assertEqual(result["files"], ["leaf.kicad_sch", "top.kicad_pcb", "top.kicad_sch"])
        self.assertEqual({item["source_path"] for item in result["components"]},
                         {"/root/left/part", "/root/right/part"})

    def test_unknown_requirement_is_rejected(self):
        self.replace("leaf.kicad_sch", "REQ-A REQ-B", "REQ-A REQ-UNKNOWN")
        self.fails("unknown requirements REQ-UNKNOWN")

    def test_declared_project_instance_path_must_exist(self):
        self.replace("leaf.kicad_sch", '(property "Reference" "R1")', '''(property "Reference" "R1")
            (instances (project "top"
              (path "/root/left" (reference "R10"))
              (path "/root/right" (reference "R11"))))''')
        self.assertTrue(self.report()["ok"], self.report()["errors"])
        self.replace("leaf.kicad_sch", '"/root/right"', '"/root/stale-instance"')
        self.fails("missing/duplicate declared instance path")

    def test_dangling_uuid_path_is_rejected(self):
        self.replace("top.kicad_pcb", "/root/right/part", "/root/right/deleted-part")
        self.fails("missing/dangling schematic path")

    def test_field_mismatch_is_rejected(self):
        self.replace("top.kicad_pcb", '"REQ-B REQ-A"', '"REQ-A"')
        self.fails("Requirements differ from schematic path")

    def test_missing_leaf_link_is_not_inferred_from_root_link(self):
        self.replace("requirements.rqml", '<edge from="leaf.kicad_sch" to="REQ-A" type="dependsOn"/>', "")
        self.fails("leaf.kicad_sch: no explicit RQML file relationship")

    def test_missing_symbol_and_sheet_fields_are_rejected(self):
        for filename in ["leaf.kicad_sch", "top.kicad_sch"]:
            original = (self.root / filename).read_text()
            with self.subTest(filename=filename):
                (self.root / filename).write_text(original.replace('(property "Requirements" "REQ-A REQ-B")', "").replace('(property "Requirements" "REQ-A")', ""))
                self.fails("missing Requirements field")
            (self.root / filename).write_text(original)

    def test_duplicate_footprint_cannot_replace_missing_repeated_instance(self):
        self.replace("top.kicad_pcb", "/root/right/part", "/root/left/part")
        self.fails("duplicate footprint for schematic component")

    def test_duplicate_source_uuid_is_rejected(self):
        path = self.root / "leaf.kicad_sch"
        text = path.read_text()
        path.write_text(text[:-1] + text[text.index("(symbol"):text.rindex(")")] + ")")
        self.fails("duplicate source UUID")

    def test_multi_unit_part_accepts_either_unit_path_and_requires_matching_fields(self):
        self.write("leaf.kicad_sch", '''(kicad_sch (uuid "leaf")
          (symbol (uuid "unit-one") (unit 1) (property "Reference" "K1")
            (property "Requirements" "REQ-A REQ-B"))
          (symbol (uuid "unit-two") (unit 2) (property "Reference" "K1")
            (property "Requirements" "REQ-A REQ-B")))''')
        self.replace("top.kicad_pcb", "/root/left/part", "/root/left/unit-two")
        self.replace("top.kicad_pcb", "/root/right/part", "/root/right/unit-one")
        self.assertTrue(self.report()["ok"], self.report()["errors"])
        self.replace("leaf.kicad_sch", '(unit 2) (property "Reference" "K1")\n            (property "Requirements" "REQ-A REQ-B")', '(unit 2) (property "Reference" "K1")\n            (property "Requirements" "REQ-A")')
        self.fails("inconsistent multi-unit Requirements")

    def test_board_only_mechanics_need_annotation_but_no_source_symbol(self):
        path = self.root / "top.kicad_pcb"
        text = path.read_text()
        path.write_text(text[:-1] + '''(footprint "mount" (uuid "mount")
          (attr board_only exclude_from_bom) (property "Reference" "H1")
          (property "Requirements" "REQ-A")))''')
        self.assertTrue(self.report()["ok"], self.report()["errors"])
        self.replace("top.kicad_pcb", "board_only ", "")
        self.fails("missing/dangling schematic path")

    def test_virtual_flags_are_not_required_to_have_footprints(self):
        path = self.root / "leaf.kicad_sch"
        path.write_text(path.read_text()[:-1] + '''(symbol (uuid "virtual")
          (property "Reference" "#FLG01")))''')
        self.assertTrue(self.report()["ok"], self.report()["errors"])

    def test_hierarchy_cycle_and_missing_file_fail(self):
        self.replace("top.kicad_sch", "leaf.kicad_sch", "top.kicad_sch")
        self.fails("cyclic schematic hierarchy")
        self.replace("top.kicad_sch", '"top.kicad_sch"', '"missing.kicad_sch"')
        self.fails("No such file")

    def test_native_string_escapes_and_malformed_structure(self):
        self.assertEqual(trace.parse('(text "quote \\" (nested) \\\\ end")'),
                         ["text", 'quote " (nested) \\ end'])
        for text in ["(x", ")", '(text "unfinished)', "(x)(y)"]:
            with self.subTest(text=text), self.assertRaises(trace.TraceError):
                trace.parse(text)

    def test_cli_json_reports_failure_without_kicad_or_exported_netlist(self):
        from contextlib import redirect_stdout
        import io
        output = io.StringIO()
        with redirect_stdout(output):
            status = trace.main(["--root", str(self.root), "--design", "top.kicad_sch", "--json"])
        self.assertEqual(status, 0)
        self.assertTrue(json.loads(output.getvalue())["ok"])
        self.replace("leaf.kicad_sch", "REQ-A REQ-B", "BOGUS")
        output = io.StringIO()
        with redirect_stdout(output):
            status = trace.main(["--root", str(self.root), "--design", "top.kicad_sch", "--json"])
        self.assertEqual(status, 1)
        self.assertFalse(json.loads(output.getvalue())["ok"])


if __name__ == "__main__":
    unittest.main()
