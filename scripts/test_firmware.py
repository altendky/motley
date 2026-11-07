#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Exercise source identity, PR provenance, and artifact failure handling."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
import build_metadata as metadata
import firmware


def identity_fixture(version: str, extra: bytes = b"") -> tuple[bytes, bytes]:
    description = struct.pack("<I", 0xABCD5432) + bytes(252)
    description += firmware.IDENTITY_MARKER + version.encode() + b"\0" + extra
    names = b"\0.shstrtab\0.flash.appdesc\0"
    elf = bytearray(52 + 3 * 40)
    elf[:6] = b"\x7fELF\x01\x01"
    struct.pack_into("<H", elf, 18, 243)
    struct.pack_into("<I", elf, 32, 52)
    struct.pack_into("<HHH", elf, 46, 40, 3, 1)
    struct.pack_into("<10I", elf, 52 + 40, 1, 3, 0, 0, len(elf), len(names), 0, 0, 1, 0)
    struct.pack_into("<10I", elf, 52 + 80, names.index(b".flash.appdesc"), 1, 2, 0,
                     len(elf) + len(names), len(description), 0, 0, 4, 0)
    elf.extend(names + description)
    image = bytearray(32)
    image[0:2] = b"\xe9\x01"
    struct.pack_into("<I", image, 28, len(description))
    image.extend(description)
    return bytes(elf), bytes(image)


class GitIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(firmware.ROOT), str(self.root)],
                       check=True, capture_output=True)
        self.git("checkout", "--detach", "HEAD")
        self.output = self.root / "build" / "firmware"
        (self.root / "firmware").mkdir(exist_ok=True)
        (self.root / "scripts").mkdir(exist_ok=True)
        # Inputs may be absent from the bootstrap commit used by the local clone.
        for name in ("firmware.py", "build_metadata.py"):
            (self.root / "scripts" / name).write_text("# fixture\n")
        (self.root / "firmware" / "input.cpp").write_text("// fixture\n")
        self.git("add", "firmware", "scripts")
        # Use the existing signed commit's tree for clean-state cases, without creating commits.

    def git(self, *args):
        return metadata.git(self.root, *args)

    def snapshot(self):
        return metadata.source_snapshot(self.root, self.output)

    def test_real_commit_tree_parents_and_detached_branch(self):
        snapshot = self.snapshot()
        self.assertEqual(snapshot["commit"], self.git("rev-parse", "HEAD"))
        self.assertEqual(snapshot["tree"], self.git("rev-parse", "HEAD^{tree}"))
        self.assertIsNone(snapshot["branch"])
        self.git("checkout", "-b", "identity-fixture")
        self.assertEqual(self.snapshot()["branch"], "identity-fixture")

    def test_staged_unstaged_untracked_and_input_fingerprints(self):
        first = self.snapshot()
        self.assertTrue(first["working_tree"]["staged"])
        source = self.root / "firmware" / "input.cpp"
        source.write_text("// changed\n")
        second = self.snapshot()
        self.assertTrue(second["working_tree"]["unstaged"])
        self.assertNotEqual(first["input_fingerprint"], second["input_fingerprint"])
        (self.root / "untracked.txt").write_text("one\n")
        third = self.snapshot()
        self.assertTrue(third["working_tree"]["untracked"])
        (self.root / "untracked.txt").write_text("two\n")
        self.assertNotEqual(third, self.snapshot())

    def test_clean_output_and_ignored_files(self):
        # Read the existing commit only: restore and remove the fixture's untracked inputs.
        self.git("reset", "--hard", "HEAD")
        self.git("clean", "-fd")
        (self.root / "firmware").mkdir(exist_ok=True)
        (self.root / "scripts").mkdir(exist_ok=True)
        # Input gathering is independent of repository-wide cleanliness.
        with patch.object(metadata, "input_files", return_value={}):
            self.assertEqual(self.snapshot()["working_tree"]["state"], "clean")
            self.output.mkdir(parents=True)
            (self.output / "generated.txt").write_text("output\n")
            self.assertEqual(self.snapshot()["working_tree"]["state"], "clean")
            with (self.root / ".git" / "info" / "exclude").open("a") as exclude:
                exclude.write("\nignored.fixture\n")
            (self.root / "ignored.fixture").write_text("ignored\n")
            self.assertEqual(self.snapshot()["working_tree"]["state"], "clean")

    def test_output_cannot_hide_repository_or_tracked_files(self):
        for output in (self.root, self.root.parent, self.root / "firmware",
                       self.root / "scripts", self.root / ".github"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                metadata.validate_output(self.root, output)

    def test_symlinked_inputs_are_rejected(self):
        (self.root / "firmware" / "link.cpp").symlink_to("input.cpp")
        with self.assertRaisesRegex(ValueError, "Symlinked"):
            self.snapshot()

    def test_ancestry_true_false_and_missing_object(self):
        head = self.git("rev-parse", "HEAD")
        parent = self.git("rev-parse", "HEAD^")
        self.assertTrue(metadata.is_ancestor(self.root, parent, head))
        self.assertFalse(metadata.is_ancestor(self.root, head, parent))
        self.assertIsNone(metadata.is_ancestor(self.root, "0" * 40, head))


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.base, self.head, self.merge = "a" * 40, "b" * 40, "c" * 40
        self.source = {"commit": self.merge, "parents": [self.base, self.head], "branch": None,
                       "working_tree": {"state": "clean"}}
        self.pr = {"number": 42, "head": {"commit": self.head}, "base": {"commit": self.base}}

    def classify(self, source=None, **overrides):
        args = dict(source=source or self.source, event_name="pull_request",
                    checkout_ref="refs/pull/42/merge", event_commit=self.merge,
                    pr=self.pr, merge_group=None)
        args.update(overrides)
        return metadata.classify_checkout(**args)

    def test_merge_requires_actual_checkout_and_matching_parents(self):
        self.assertEqual(self.classify(), "pr-merge")
        for overrides in ({"event_commit": self.head}, {"checkout_ref": "refs/heads/main"},
                          {"source": {**self.source, "parents": [self.head, self.base]}}):
            with self.subTest(overrides=overrides):
                self.assertEqual(self.classify(**overrides), "unknown")

    def test_pr_head_is_independent_of_base_inclusion(self):
        source = {**self.source, "commit": self.head, "parents": [self.base]}
        self.assertEqual(self.classify(source=source), "pr-head")

    def test_missing_pr_context_and_merge_queue(self):
        self.assertEqual(self.classify(pr=None), "unknown")
        self.assertEqual(self.classify(pr=None, event_name="merge_group",
                                      merge_group={"head_commit": self.merge}), "merge-queue")
        self.assertEqual(self.classify(pr=None, event_name="merge_group",
                                      merge_group={"head_commit": self.head}), "unknown")

    def test_fork_pr_context_and_event_commit_preserved(self):
        event = {"pull_request": {"number": 42, "html_url": "https://example.test/pr/42",
                 "head": {"sha": self.head, "ref": "topic", "repo": {"full_name": "fork/motley"}},
                 "base": {"sha": self.base, "ref": "main", "repo": {"full_name": "owner/motley"}}}}
        env = {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request",
               "GITHUB_SHA": self.merge, "GITHUB_REF": "refs/pull/42/merge",
               "GITHUB_REPOSITORY": "owner/motley", "GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "2"}
        with patch.object(metadata, "is_ancestor", return_value=True):
            context = metadata.ci_context(Path("unused"), self.source, env, event)
        self.assertEqual(context["pull_request"]["head"]["repository"], "fork/motley")
        self.assertEqual(context["event_commit"], self.merge)
        self.assertTrue(context["base_included"])
        self.assertEqual(context["run_url"], "https://github.com/owner/motley/actions/runs/123")
        name = metadata.artifact_name("esp32c6", self.source, context)
        self.assertIn("pr42-pr-merge-run123-a2", name)

    def test_local_context_ignores_github_variables_without_provider(self):
        context = metadata.ci_context(Path("unused"), self.source, {"GITHUB_SHA": self.head}, {})
        self.assertEqual(context["provider"], "local")
        self.assertIsNone(context["event_commit"])
        self.assertEqual(context["checkout_kind"], "detached")

    def test_full_hashes_with_shared_prefix_remain_distinct(self):
        context = metadata.ci_context(Path("unused"), self.source, {}, {})
        for length in (40, 64):
            first = {**self.source, "commit": "a" * length}
            second = {**self.source, "commit": "a" * (length - 1) + "b"}
            self.assertEqual(metadata.display_version(first), "g" + first["commit"] + "-clean")
            self.assertLessEqual(len(metadata.sdk_project_version(metadata.display_version(first)).encode()), 31)
            self.assertEqual(metadata.sdk_project_version(metadata.display_version(first)),
                             metadata.sdk_project_version(metadata.display_version(second)))
            self.assertIn(second["commit"], metadata.artifact_name("esp32c6", second, context))
            self.assertNotEqual(metadata.display_version(first), metadata.display_version(second))
        with self.assertRaisesRegex(ValueError, "full Git commit"):
            metadata.display_version({**self.source, "commit": "a" * 12})


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name)
        self.version = "g" + "1" * 40 + "-dirty"
        for name in firmware.BUNDLE_FILES:
            path = self.output / name
            path.parent.mkdir(exist_ok=True)
            path.write_text("fixture\n")
        elf, image = identity_fixture(self.version)
        (self.output / "motley.elf").write_bytes(elf)
        (self.output / "motley.bin").write_bytes(image)
        self.description = {"target": "esp32c6", "project_version": metadata.sdk_project_version(self.version),
                            "git_revision": "fixture-sdk", "c_compiler": "/sdk/gcc"}
        (self.output / "project_description.json").write_text(json.dumps(self.description))
        self.command = "g++ -std=c++23 -fno-exceptions -fno-rtti"
        self.write_database()
        (self.output / "sdkconfig").write_text("# CONFIG_COMPILER_CXX_EXCEPTIONS is not set\n# CONFIG_COMPILER_CXX_RTTI is not set\n")
        flashing = {"extra_esptool_args": {"chip": "esp32c6"},
                    "write_flash_args": ["--flash-mode", "dio", "--flash-size", "2MB", "--flash-freq", "80m"],
                    "flash_files": dict(zip(("0x0", "0x8000", "0x10000"), firmware.ARTIFACTS[1:]))}
        (self.output / "flasher_args.json").write_text(json.dumps(flashing))
        self.flash_args = "--flash-mode dio --flash-freq 80m --flash-size 2MB\n0x0 motley.bin\n0x8000 bootloader/bootloader.bin\n0x10000 partition_table/partition-table.bin\n"
        (self.output / "flash_args").write_text(self.flash_args)

    def write_database(self):
        (self.output / "compile_commands.json").write_text(json.dumps([
            {"file": "/project/main/app_main.cpp", "command": self.command}]))

    def inspect(self, **options):
        stdout = f"App version: {metadata.sdk_project_version(self.version)}\nChecksum: 0x00 (valid)\nValidation hash: 0000 (valid)\n"
        with patch.object(firmware, "run_sdk", return_value=subprocess.CompletedProcess([], 0, stdout)):
            return firmware.verify_artifacts(self.output, {"target": "esp32c6", "image": "fixture"}, self.version, **options)

    def test_image_identity_and_missing_artifact_failures(self):
        self.inspect()
        (self.output / "motley.bin").unlink()
        with self.assertRaisesRegex(ValueError, "Missing or empty"):
            self.inspect()

    def test_effective_flags_target_version_and_config_rejected(self):
        for flag in ("-std=c++20", "-fexceptions", "-frtti"):
            self.command = f"g++ -std=c++23 -fno-exceptions -fno-rtti {flag}"
            self.write_database()
            with self.subTest(flag=flag), self.assertRaisesRegex(ValueError, "Effective compiler"):
                self.inspect()
        self.command = "g++ -std=c++23 -fno-exceptions -fno-rtti"; self.write_database()
        for key, value, message in (("target", "esp32", "target"), ("project_version", "wrong", "version")):
            (self.output / "project_description.json").write_text(json.dumps({**self.description, key: value}))
            with self.assertRaisesRegex(ValueError, message): self.inspect()
        (self.output / "project_description.json").write_text(json.dumps(self.description))
        (self.output / "sdkconfig").write_text("CONFIG_COMPILER_CXX_RTTI=y\n")
        with self.assertRaisesRegex(ValueError, "must be disabled"): self.inspect()

    def test_embedded_version_and_checksum_failures(self):
        for stdout in ("App version: wrong\n", f"App version: {metadata.sdk_project_version(self.version)}\nChecksum: 0 (invalid)\n"):
            with patch.object(firmware, "run_sdk", return_value=subprocess.CompletedProcess([], 0, stdout)):
                with self.assertRaises(ValueError):
                    firmware.verify_artifacts(self.output, {"target": "esp32c6", "image": "fixture"}, self.version)

    def test_receipt_preserves_context_and_rejects_stale_inputs(self):
        inspection = self.inspect()
        source = {"commit": "1" * 40, "working_tree": {"state": "clean"}}
        receipt = {"schema_version": 3, "version": metadata.display_version(source),
                   "source": source, "inspection": inspection,
                   "execution": {"started_at_utc": "original", "context": {"run_id": "original"}}}
        before = json.dumps(receipt, sort_keys=True)
        firmware.check_receipt(receipt, source, inspection)
        self.assertEqual(json.dumps(receipt, sort_keys=True), before)
        with self.assertRaisesRegex(ValueError, "does not match"):
            firmware.check_receipt(receipt, {**source, "commit": "2" * 40}, inspection)

    def test_bundle_keeps_flash_layout_and_detects_corruption(self):
        inspection = self.inspect()
        receipt = {"inspection": inspection}
        (self.output / "build-receipt.json").write_text(json.dumps(receipt))
        firmware.create_bundle(self.output, receipt)
        firmware.check_bundle(self.output, receipt)
        flash = json.loads((self.output / "bundle" / "flasher_args.json").read_text())
        self.assertTrue(all((self.output / "bundle" / name).is_file() for name in flash["flash_files"].values()))
        (self.output / "bundle" / "motley.bin").write_text("corrupted")
        with self.assertRaisesRegex(ValueError, "Bundled artifact differs"):
            firmware.check_bundle(self.output, receipt)

    def test_missing_map_and_changed_packaging_input_fail(self):
        inspection = self.inspect()
        (self.output / "motley.map").unlink()
        with self.assertRaisesRegex(ValueError, "Missing or empty bundle"):
            self.inspect()
        (self.output / "build-receipt.json").write_text("{}")
        (self.output / "motley.bin").write_text("changed")
        with self.assertRaisesRegex(ValueError, "changed before packaging"):
            firmware.create_bundle(self.output, {"inspection": inspection})

    def test_malformed_flash_options_paths_and_offsets_fail(self):
        for content in ("fixture", self.flash_args.replace("motley.bin", "/build/motley.bin"),
                        self.flash_args.replace("0x8000", "0x9000"),
                        self.flash_args.replace("80m", "40m"),
                        self.flash_args + "0x10000 motley.bin\n",
                        self.flash_args.replace("--flash-mode", "--unknown")):
            (self.output / "flash_args").write_text(content)
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.inspect()

    def test_full_identity_rejects_truncation_wrong_state_and_duplicates(self):
        for value in ("g" + "1" * 12 + "-dirty", self.version.replace("dirty", "clean"),
                      self.version[:-1], "g" + "2" * 40 + "-dirty"):
            elf, image = identity_fixture(value)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "full build identity"):
                firmware.verify_embedded_identity(elf, image, self.version)
        elf, image = identity_fixture(self.version, firmware.IDENTITY_MARKER + self.version.encode() + b"\0")
        with self.assertRaisesRegex(ValueError, "duplicated"):
            firmware.verify_embedded_identity(elf, image, self.version)

    def test_debug_only_identity_and_image_mismatch_fail(self):
        elf, image = identity_fixture(self.version)
        debug_only = bytearray(elf)
        struct.pack_into("<I", debug_only, 52 + 80 + 8, 0)
        with self.assertRaisesRegex(ValueError, "allocated"):
            firmware.verify_embedded_identity(bytes(debug_only), image, self.version)
        _, wrong_image = identity_fixture(self.version.replace("dirty", "clean"))
        with self.assertRaisesRegex(ValueError, "image full build identity"):
            firmware.verify_embedded_identity(elf, wrong_image, self.version)
        with self.assertRaisesRegex(ValueError, "Invalid ELF section"):
            firmware.verify_embedded_identity(elf[:60], image, self.version)


class RunnerTests(unittest.TestCase):
    def test_source_change_during_build_invalidates_previous_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            (root / "firmware").mkdir()
            (root / "firmware" / "toolchain.toml").write_text('image = "sdk@sha256:' + 'a' * 64 + '"\ntarget = "esp32c6"\n')
            output = root / "output"
            output.mkdir()
            (output / "bundle").mkdir()
            (output / "bundle" / "stale.bin").write_text("stale")
            (output / "build-receipt.json").write_text("stale")
            source = {"commit": "1" * 40, "working_tree": {"state": "dirty"}}
            changed = {**source, "commit": "2" * 40}
            with (patch.object(firmware, "ROOT", root), patch.object(firmware, "FIRMWARE", root / "firmware"),
                  patch.object(firmware, "source_snapshot", side_effect=[source, changed]),
                  patch.object(firmware, "ci_context", return_value={"provider": "local", "pull_request": None, "checkout_kind": "branch"}),
                  patch.object(firmware, "run_sdk", return_value=subprocess.CompletedProcess([], 0, "size")),
                  patch.object(firmware, "verify_artifacts", return_value={}),
                  patch.object(sys, "argv", ["firmware.py", "--build-dir", str(output)]),
                  redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO())):
                self.assertEqual(firmware.main(), 1)
            self.assertFalse((output / "bundle").exists())
            self.assertFalse((output / "build-receipt.json").exists())
            self.assertEqual(json.loads((output / "failure.json").read_text())["status"], "failed")

    def test_verify_only_never_relabels_original_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            (root / "firmware").mkdir()
            (root / "firmware" / "toolchain.toml").write_text('image = "sdk@sha256:' + 'a' * 64 + '"\ntarget = "esp32c6"\n')
            output = root / "output"; output.mkdir()
            source = {"commit": "1" * 40, "working_tree": {"state": "clean"}}
            receipt = {"schema_version": 3, "version": metadata.display_version(source),
                       "source": source, "inspection": {}, "execution": {"time": "original", "run": "original"}}
            path = output / "build-receipt.json"; path.write_text(json.dumps(receipt))
            before = path.read_bytes()
            with (patch.object(firmware, "ROOT", root), patch.object(firmware, "FIRMWARE", root / "firmware"),
                  patch.object(firmware, "source_snapshot", return_value=source),
                  patch.object(firmware, "ci_context", side_effect=AssertionError("Must preserve original context")),
                  patch.object(firmware, "verify_artifacts", return_value={}),
                  patch.object(firmware, "check_bundle"),
                  patch.object(sys, "argv", ["firmware.py", "--build-dir", str(output), "--verify-only"]),
                  redirect_stdout(io.StringIO())):
                self.assertEqual(firmware.main(), 0)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
