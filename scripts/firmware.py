#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Acquire locked Matter dependencies, build offline, and verify firmware artifacts."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import struct
import subprocess
import sys
import tomllib

sys.dont_write_bytecode = True
from build_metadata import artifact_name, ci_context, digest, display_version, file_identity, sdk_project_version, source_snapshot, validate_output

ROOT = Path(__file__).resolve().parent.parent
FIRMWARE = ROOT / "firmware"
ARTIFACTS = (
    "motley.elf",
    "motley.bin",
    "bootloader/bootloader.bin",
    "partition_table/partition-table.bin",
)
REPORTS = ("motley-image-info.txt", "bootloader-image-info.txt", "compiler-version.txt", "size-report.txt", "verification.json",
           "dependencies.lock", "dependency-content.json")
BUNDLE_FILES = (*ARTIFACTS, "flash_args", "flasher_args.json", "motley.map", *REPORTS)
IDENTITY_MARKER = b"MOTLEY_BUILD_IDENTITY_V1:"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_sdk(image: str, build_dir: Path, *command: str, capture: bool = False,
            log: Path | None = None, acquire: bool = False):
    arguments = ["docker", "run", "--rm"]
    if not acquire:
        arguments.extend(["--network", "none"])
    if hasattr(os, "getuid"):
        arguments.extend(["--user", f"{os.getuid()}:{os.getgid()}"])
    if not acquire:
        # The writable /build parent must not expose a second writable source path.
        arguments.extend(["--mount", f"type=bind,source={build_dir / 'project'},target=/build/project,readonly"])
    arguments.extend([
        "--mount", f"type=bind,source={build_dir / 'project'},target=/project" + ("" if acquire else ",readonly"),
        "--mount", f"type=bind,source={build_dir},target=/build",
        "--workdir", "/project",
        "--env", "IDF_CCACHE_ENABLE=0",
        "--env", "IDF_COMPONENT_CACHE_PATH=/build/component-cache",
        image,
        *command,
    ])
    if log is None:
        return subprocess.run(arguments, check=True, text=True, capture_output=capture)
    with log.open("w") as output:
        process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end="")
            output.write(line)
        code = process.wait()
    if code:
        raise subprocess.CalledProcessError(code, arguments)
    return subprocess.CompletedProcess(arguments, code)


def stage_project(build_dir: Path) -> None:
    """Copy owned inputs without ever giving the SDK a writable repository mount."""
    project = build_dir / "project"
    if project.is_symlink() or (FIRMWARE / "managed_components").exists():
        raise ValueError("Staged project must be local; managed dependencies belong only in build output")
    project.mkdir(exist_ok=True)
    for path in project.iterdir():
        if path.name == "managed_components" and path.is_dir() and not path.is_symlink():
            continue
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
    shutil.copytree(FIRMWARE, project, dirs_exist_ok=True)


def check_staged_sources(build_dir: Path) -> None:
    project = build_dir / "project"
    def inputs(root):
        return {p.relative_to(root).as_posix(): file_identity(p) for p in root.rglob("*")
                if (p.is_file() or p.is_symlink()) and p.relative_to(root).parts[0] != "managed_components"}
    if inputs(FIRMWARE) != inputs(project):
        raise ValueError("Staged firmware sources differ from declared inputs")


def dependency_content(build_dir: Path) -> dict:
    """Fingerprint actual dependency bytes/modes as well as recording the solver lock."""
    managed = build_dir / "project" / "managed_components"
    if not managed.is_dir() or managed.is_symlink():
        raise ValueError("Missing managed dependencies")
    result = {}
    for component in sorted(managed.iterdir()):
        if not component.is_dir() or component.is_symlink():
            raise ValueError("Unexpected managed dependency entry")
        paths = sorted(component.rglob("*"))
        if any(p.is_symlink() for p in paths):
            raise ValueError("Symlinked managed dependencies are not supported")
        files = {p.relative_to(component).as_posix(): file_identity(p) for p in paths if p.is_file()}
        result[component.name] = {"files": len(files), "content_sha256": digest(files)}
    if not result:
        raise ValueError("Empty managed dependencies")
    return result


def check_dependency_lock(build_dir: Path) -> None:
    if (build_dir / "dependencies.lock").read_bytes() != (FIRMWARE / "dependencies.lock").read_bytes():
        raise ValueError("Dependency resolution changed the committed lock; review an explicit dependency update")


def report(path: Path, content: str, write: bool) -> None:
    if write:
        path.write_text(content)
    elif path.read_text() != content:
        raise ValueError(f"Stored inspection report differs: {path.name}")


def verify_flash_args(build_dir: Path, flashing: dict) -> None:
    tokens = shlex.split((build_dir / "flash_args").read_text())
    options, files = {}, {}
    for key, value in zip(tokens[::2], tokens[1::2], strict=True):
        if key.startswith("--"):
            if key not in ("--flash-mode", "--flash-freq", "--flash-size") or key in options:
                raise ValueError("Invalid or duplicate flash option")
            options[key] = value
        else:
            offset = int(key, 0)
            if offset in files or Path(value).is_absolute() or ".." in Path(value).parts:
                raise ValueError("Invalid flash image path or duplicate offset")
            files[offset] = value
    declared = flashing["write_flash_args"]
    expected_options = dict(zip(declared[::2], declared[1::2], strict=True))
    expected_files = {int(offset, 0): name for offset, name in flashing["flash_files"].items()}
    if options != expected_options or files != expected_files:
        raise ValueError("Flash arguments do not match verified flashing metadata")


def verify_embedded_identity(elf: bytes, image: bytes, version: str) -> None:
    """Check allocated application-description bytes, not incidental debug strings."""
    if len(elf) < 52 or elf[:6] != b"\x7fELF\x01\x01":
        raise ValueError("Expected a 32-bit little-endian ELF for identity inspection")
    section_offset = struct.unpack_from("<I", elf, 32)[0]
    entry_size, count, names_index = struct.unpack_from("<HHH", elf, 46)
    if entry_size < 40 or not count or names_index >= count or section_offset + count * entry_size > len(elf):
        raise ValueError("Invalid ELF section table")
    def section(index):
        return struct.unpack_from("<10I", elf, section_offset + index * entry_size)
    def contents(header):
        offset, size = header[4:6]
        if offset + size > len(elf):
            raise ValueError("ELF section extends beyond file")
        return elf[offset:offset + size]
    names = contents(section(names_index))
    descriptions = []
    for index in range(count):
        header = section(index)
        name_offset = header[0]
        if name_offset >= len(names):
            raise ValueError("Invalid ELF section name")
        name = names[name_offset:].split(b"\0", 1)[0]
        if name == b".flash.appdesc" and header[1] == 1 and header[2] & 2:
            descriptions.append(contents(header))
    if len(descriptions) != 1:
        raise ValueError("Expected one allocated ELF application description")
    if len(image) < 32 or image[0] != 0xE9 or image[1] == 0:
        raise ValueError("Invalid application image segment header")
    segment_size = struct.unpack_from("<I", image, 28)[0]
    if 32 + segment_size > len(image):
        raise ValueError("Application image segment extends beyond file")
    expected = IDENTITY_MARKER + version.encode("ascii") + b"\0"
    for name, description in (("ELF", descriptions[0]), ("image", image[32:32 + segment_size])):
        if (description[:4] != struct.pack("<I", 0xABCD5432)
                or description[256:256 + len(expected)] != expected
                or description.count(IDENTITY_MARKER) != 1):
            raise ValueError(f"{name} full build identity is missing, truncated, duplicated, or mismatched")


def verify_artifacts(build_dir: Path, toolchain: dict, version: str,
                     write_reports: bool = True) -> dict:
    check_staged_sources(build_dir)
    check_dependency_lock(build_dir)
    dependencies = dependency_content(build_dir)
    report(build_dir / "dependency-content.json", json.dumps(dependencies, indent=2) + "\n", write_reports)
    for name in ARTIFACTS:
        path = build_dir / name
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"Missing or empty build artifact: {name}")

    header = (build_dir / "motley.elf").read_bytes()[:20]
    if (len(header) != 20 or header[:4] != b"\x7fELF"
            or header[5] != 1 or struct.unpack_from("<H", header, 18)[0] != 243):
        raise ValueError("Application ELF is not a little-endian RISC-V ELF")

    description = json.loads((build_dir / "project_description.json").read_text())
    if description["target"] != toolchain["target"]:
        raise ValueError("Generated project target does not match toolchain.toml")
    expected_sdk_version = sdk_project_version(version)
    if description["project_version"] != expected_sdk_version:
        raise ValueError("Generated project version does not match the constrained SDK label")
    verify_embedded_identity((build_dir / "motley.elf").read_bytes(),
                             (build_dir / "motley.bin").read_bytes(), version)

    database = json.loads((build_dir / "compile_commands.json").read_text())
    owned = [entry for entry in database if entry["file"] == "/project/main/app_main.cpp"]
    if len(owned) != 1:
        raise ValueError("Expected exactly one owned application compile command")
    arguments = owned[0].get("arguments") or shlex.split(owned[0]["command"])
    for prefix, expected in (
        ("-std=", "-std=c++23"),
        (("-fexceptions", "-fno-exceptions"), "-fno-exceptions"),
        (("-frtti", "-fno-rtti"), "-fno-rtti"),
    ):
        matches = [arg for arg in arguments if arg.startswith(prefix)]
        if not matches or matches[-1] != expected:
            raise ValueError(f"Effective compiler option is not {expected}")

    configuration = (build_dir / "sdkconfig").read_text().splitlines()
    for option in ("CONFIG_COMPILER_CXX_EXCEPTIONS", "CONFIG_COMPILER_CXX_RTTI",
                   "CONFIG_ENABLE_WIFI_STATION", "CONFIG_ENABLE_OTA_REQUESTOR"):
        if f"# {option} is not set" not in configuration:
            raise ValueError(f"{option} must be disabled in the generated configuration")
    for option in ("CONFIG_OPENTHREAD_ENABLED", "CONFIG_BT_NIMBLE_ENABLED",
                   "CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG", "CONFIG_PARTITION_TABLE_CUSTOM"):
        if f"{option}=y" not in configuration:
            raise ValueError(f"{option} must be enabled in the generated configuration")

    for name in ("motley.bin", "bootloader/bootloader.bin"):
        result = run_sdk(
            toolchain["image"], build_dir,
            "python", "-m", "esptool", "--chip", toolchain["target"],
            "image-info", f"/build/{name}", capture=True,
        )
        if name == "motley.bin":
            embedded = re.search(r"^App version:\s+(.+)$", result.stdout, re.MULTILINE)
            if not embedded or embedded.group(1).strip() != expected_sdk_version:
                raise ValueError("Application image version does not match the constrained SDK label")
        if not re.search(r"^Checksum:.*\(valid\)$", result.stdout, re.MULTILINE):
            raise ValueError(f"Invalid image checksum: {name}")
        if not re.search(r"^Validation hash:.*\(valid\)$", result.stdout, re.MULTILINE):
            raise ValueError(f"Invalid image validation hash: {name}")
        report(build_dir / f"{Path(name).stem}-image-info.txt", result.stdout, write_reports)

    compiler = run_sdk(toolchain["image"], build_dir,
                       description["c_compiler"].removesuffix("gcc") + "g++", "--version", capture=True)
    report(build_dir / "compiler-version.txt", compiler.stdout, write_reports)
    flashing = json.loads((build_dir / "flasher_args.json").read_text())
    if flashing["extra_esptool_args"]["chip"] != toolchain["target"]:
        raise ValueError("Flashing metadata target differs")
    if set(flashing["flash_files"].values()) != set(ARTIFACTS[1:]):
        raise ValueError("Flashing metadata does not reference the bundled images")
    verify_flash_args(build_dir, flashing)
    checks = {"target": "passed", "compiler_settings": "passed", "elf": "passed",
              "image_checksums": "passed", "embedded_version": "passed", "flashing_paths": "passed",
              "hardware_execution": "not tested"}
    report(build_dir / "verification.json", json.dumps(checks, indent=2) + "\n", write_reports)
    for name in BUNDLE_FILES:
        if not (build_dir / name).is_file() or (build_dir / name).stat().st_size == 0:
            raise ValueError(f"Missing or empty bundle file: {name}")

    return {
        "target": description["target"],
        "sdk_version": description["git_revision"],
        "sdk_project_version": description["project_version"],
        "container_image": toolchain["image"],
        "matter_upstream": toolchain.get("matter_upstream"),
        "compiler_version": compiler.stdout.strip(),
        "owned_compile_arguments": arguments,
        "sdkconfig_sha256": sha256(build_dir / "sdkconfig"),
        "dependencies": dependencies,
        "artifacts": {name: {"sha256": sha256(build_dir / name), "size": (build_dir / name).stat().st_size}
                      for name in BUNDLE_FILES},
        "checks": checks,
    }


def check_receipt(previous: dict, source: dict, inspection: dict) -> None:
    if previous.get("schema_version") != 3:
        raise ValueError("Unsupported or missing receipt schema; rebuild required")
    if previous["source"] != source or previous["inspection"] != inspection:
        raise ValueError("Existing build receipt does not match current inputs/artifacts; rebuild required")
    if previous["version"] != display_version(source):
        raise ValueError("Receipt version does not match source identity")


def create_bundle(build_dir: Path, receipt: dict) -> None:
    staging = build_dir / "bundle.tmp"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    for name in (*BUNDLE_FILES, "build-receipt.json"):
        source = build_dir / name
        if name != "build-receipt.json" and sha256(source) != receipt["inspection"]["artifacts"][name]["sha256"]:
            raise ValueError(f"Artifact changed before packaging: {name}")
        destination = staging / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    staging.rename(build_dir / "bundle")


def check_bundle(build_dir: Path, receipt: dict) -> None:
    bundle = build_dir / "bundle"
    if (bundle / "build-receipt.json").read_bytes() != (build_dir / "build-receipt.json").read_bytes():
        raise ValueError("Bundled receipt differs from original")
    for name, identity in receipt["inspection"]["artifacts"].items():
        if sha256(bundle / name) != identity["sha256"]:
            raise ValueError(f"Bundled artifact differs from receipt: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-dir", type=Path,
        default=Path(os.environ.get("MOTLEY_BUILD_DIR", ROOT / "build" / "firmware")),
    )
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--update-dependencies", action="store_true",
                        help="Resolve a candidate lock in build output for review; do not build or modify repository inputs")
    options = parser.parse_args()
    if options.verify_only and options.update_dependencies:
        parser.error("Choose either verification or dependency update")
    build_dir = options.build_dir.resolve()
    try:
        validate_output(ROOT, build_dir)
    except ValueError as error:
        parser.error(str(error))
    receipt_path = build_dir / "build-receipt.json"
    try:
        source = source_snapshot(ROOT, build_dir)
        toolchain = tomllib.loads((FIRMWARE / "toolchain.toml").read_text())
        if not re.fullmatch(r"[^@\s]+@sha256:[0-9a-f]{64}", toolchain["image"]):
            raise ValueError("The SDK image must be pinned by SHA-256 digest")
        version = display_version(source)
        if options.verify_only:
            previous = json.loads(receipt_path.read_text())
            inspection = verify_artifacts(build_dir, toolchain, version, write_reports=False)
            check_receipt(previous, source, inspection)
            check_bundle(build_dir, previous)
            receipt = previous
        else:
            context = ci_context(ROOT, source)
            started = datetime.now(timezone.utc).isoformat()
            build_dir.mkdir(parents=True, exist_ok=True)
            receipt_path.unlink(missing_ok=True)
            bundle = build_dir / "bundle"
            if bundle.is_symlink():
                bundle.unlink()
            elif bundle.exists():
                shutil.rmtree(bundle)
            stage_project(build_dir)
            # Defaults are declared inputs; a previous menuconfig must not override them.
            for name in ("sdkconfig", "sdkconfig.old"):
                (build_dir / name).unlink(missing_ok=True)
            if (FIRMWARE / "dependencies.lock").is_file():
                shutil.copy2(FIRMWARE / "dependencies.lock", build_dir / "dependencies.lock")
            if options.update_dependencies:
                (build_dir / "dependencies.lock").unlink(missing_ok=True)
            configure = ("idf.py", "-B", "/build", "-D", "SDKCONFIG=/build/sdkconfig",
                         "-D", f"IDF_TARGET={toolchain['target']}",
                         "-D", f"MOTLEY_BUILD_VERSION={version}")
            run_sdk(toolchain["image"], build_dir, *configure, "reconfigure",
                    acquire=True, log=build_dir / "dependencies.log")
            check_staged_sources(build_dir)
            if options.update_dependencies:
                if source != source_snapshot(ROOT, build_dir):
                    raise ValueError("Build inputs or checkout changed during dependency resolution")
                print(f"Review candidate dependency lock: {build_dir / 'dependencies.lock'}")
                return 0
            check_dependency_lock(build_dir)
            dependencies = dependency_content(build_dir)
            run_sdk(
                toolchain["image"], build_dir, *configure, "build",
                log=build_dir / "build.log",
            )
            size = run_sdk(toolchain["image"], build_dir, "idf.py", "-B", "/build", "size", capture=True)
            (build_dir / "size-report.txt").write_text(size.stdout)
            inspection = verify_artifacts(build_dir, toolchain, version)
            if dependencies != inspection["dependencies"]:
                raise ValueError("Dependency content changed during compilation")
            receipt = {"schema_version": 3, "version": version, "source": source,
                       "execution": {"started_at_utc": started, "context": context},
                       "inspection": inspection, "artifact_name": artifact_name(toolchain["target"], source, context)}
        if source != source_snapshot(ROOT, build_dir):
            raise ValueError("Build inputs or checkout changed during execution; rebuild required")
        if not options.verify_only:
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
            create_bundle(build_dir, receipt)
            check_bundle(build_dir, receipt)
            if os.environ.get("GITHUB_ACTIONS") == "true" and os.environ.get("GITHUB_OUTPUT"):
                with Path(os.environ["GITHUB_OUTPUT"]).open("a") as output:
                    output.write(f"artifact_name={receipt['artifact_name']}\n")
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Firmware check failed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr, file=sys.stderr)
        if not options.verify_only and build_dir.is_dir():
            receipt_path.unlink(missing_ok=True)
            if (build_dir / "bundle").is_dir():
                shutil.rmtree(build_dir / "bundle")
            (build_dir / "failure.json").write_text(json.dumps({"status": "failed", "error": str(error)}) + "\n")
        return 1
    print(f"Verified {toolchain['target']} {version} firmware artifacts in {build_dir / 'bundle'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
