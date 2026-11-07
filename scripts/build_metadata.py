"""Host-side source and CI provenance for the firmware build runner."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, errors="surrogateescape",
    ).strip("\n")


def validate_output(root: Path, output: Path) -> None:
    if root.is_relative_to(output):
        raise ValueError("Build output must not equal or contain the repository")
    if output.is_relative_to(root / "firmware") or (root / "scripts").is_relative_to(output):
        raise ValueError("Build output must not overlap firmware or build-runner sources")
    if output.is_relative_to(root / "scripts"):
        raise ValueError("Build output must not be inside build-runner sources")
    if output.is_relative_to(root):
        relative = output.relative_to(root).as_posix()
        if git(root, "ls-files", "--", f":(top,literal){relative}"):
            raise ValueError("Build output must not contain tracked repository files")


def file_identity(path: Path) -> dict:
    if path.is_symlink():
        return {"symlink": os.readlink(path)}
    if not path.is_file():
        raise ValueError(f"Expected a regular build input: {path}")
    return {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "executable": bool(path.stat().st_mode & 0o111),
    }


def input_files(root: Path) -> dict:
    paths = [path for path in (root / "firmware").rglob("*") if path.is_file() or path.is_symlink()]
    paths += [root / "scripts" / name for name in ("firmware.py", "build_metadata.py")]
    # Do not silently omit a symlink target from the input fingerprint/container mount.
    if any(path.is_symlink() for path in paths):
        raise ValueError("Symlinked firmware/build-runner inputs are not supported")
    return {path.relative_to(root).as_posix(): file_identity(path) for path in sorted(paths)}


def source_snapshot(root: Path, output: Path) -> dict:
    validate_output(root, output)
    paths = ["."]
    if output.is_relative_to(root):
        paths.append(f":(top,literal,exclude){output.relative_to(root).as_posix()}")
    records = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all",
                  "--ignore-submodules=none", "--", *paths).split("\0")
    changes = []
    iterator = iter(records)
    for record in iterator:
        if not record:
            continue
        item = {"index": record[0], "worktree": record[1], "path": record[3:]}
        if record[0] in "RC" or record[1] in "RC":
            item["original_path"] = next(iterator)
        if record[:2] == "??":
            item["content"] = file_identity(root / item["path"])
        changes.append(item)
    branch = subprocess.run(
        ["git", "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"],
        capture_output=True, text=True,
    )
    if branch.returncode not in (0, 1):
        raise ValueError("Could not determine checkout branch")
    inputs = input_files(root)
    return {
        "commit": git(root, "rev-parse", "HEAD"),
        "tree": git(root, "rev-parse", "HEAD^{tree}"),
        "parents": git(root, "show", "-s", "--format=%P", "HEAD").split(),
        "branch": branch.stdout.strip() or None,
        "working_tree": {
            "state": "dirty" if changes else "clean",
            "staged": any(c["index"] not in (" ", "?") for c in changes),
            "unstaged": any(c["worktree"] not in (" ", "?") for c in changes),
            "untracked": any(c["index"] == "?" for c in changes),
            "changes": changes,
            "index_diff_sha256": hashlib.sha256(git(root, "diff", "--cached", "--no-ext-diff", "--binary", "--", *paths).encode(errors="surrogateescape")).hexdigest(),
            "worktree_diff_sha256": hashlib.sha256(git(root, "diff", "--no-ext-diff", "--binary", "--", *paths).encode(errors="surrogateescape")).hexdigest(),
        },
        "inputs": inputs,
        "input_fingerprint": digest(inputs),
    }


def is_ancestor(root: Path, base: str | None, commit: str) -> bool | None:
    if not base or not re.fullmatch(r"[0-9a-f]{40,64}", base):
        return None
    # An incomplete graph cannot establish a negative result reliably.
    if git(root, "rev-parse", "--is-shallow-repository") != "false":
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", base, commit],
        capture_output=True,
    )
    return {0: True, 1: False}.get(result.returncode)


def classify_checkout(source: dict, event_name: str | None, checkout_ref: str | None,
                      event_commit: str | None, pr: dict | None, merge_group: dict | None) -> str:
    commit = source["commit"]
    if pr:
        head, base = pr["head"]["commit"], pr["base"]["commit"]
        if head and commit == head:
            return "pr-head"
        if (head and base and head != base and checkout_ref == f"refs/pull/{pr['number']}/merge"
                and commit == event_commit and source["parents"] == [base, head]):
            return "pr-merge"
        return "unknown"
    if event_name == "merge_group":
        return "merge-queue" if merge_group and merge_group["head_commit"] == commit else "unknown"
    if event_name and event_name.startswith("pull_request"):
        return "unknown"
    return "branch" if source["branch"] else "detached"


def ci_context(root: Path, source: dict, env: dict | None = None, event: dict | None = None) -> dict:
    env = os.environ if env is None else env
    enabled = env.get("GITHUB_ACTIONS") == "true"
    if event is None:
        event = json.loads(Path(env["GITHUB_EVENT_PATH"]).read_text()) if enabled and env.get("GITHUB_EVENT_PATH") else {}
    name = env.get("GITHUB_EVENT_NAME") if enabled else None
    checkout_ref = env.get("GITHUB_REF") if enabled else None
    event_commit = env.get("GITHUB_SHA") if enabled else None
    pr_data = event.get("pull_request") if enabled else None
    pr = None
    if pr_data:
        def endpoint(side):
            value = pr_data.get(side) or {}
            return {"repository": (value.get("repo") or {}).get("full_name"),
                    "branch": value.get("ref"), "commit": value.get("sha")}
        pr = {"number": pr_data.get("number", event.get("number")),
              "url": pr_data.get("html_url"), "head": endpoint("head"), "base": endpoint("base")}
    group_data = event.get("merge_group") if enabled else None
    group = None if not group_data else {
        "head_commit": group_data.get("head_sha"), "head_ref": group_data.get("head_ref"),
        "base_commit": group_data.get("base_sha"), "base_ref": group_data.get("base_ref"),
    }
    base = pr["base"]["commit"] if pr else group["base_commit"] if group else None
    run_id, repo = env.get("GITHUB_RUN_ID"), env.get("GITHUB_REPOSITORY")
    return {
        "provider": "github-actions" if enabled else "local",
        "event": name, "event_commit": event_commit, "checkout_ref": checkout_ref,
        "checkout_kind": classify_checkout(source, name, checkout_ref, event_commit, pr, group),
        "pull_request": pr, "merge_group": group,
        "base_included": is_ancestor(root, base, source["commit"]) if base else None,
        "workflow": env.get("GITHUB_WORKFLOW") if enabled else None,
        "workflow_ref": env.get("GITHUB_WORKFLOW_REF") if enabled else None,
        "workflow_commit": env.get("GITHUB_WORKFLOW_SHA") if enabled else None,
        "repository": repo if enabled else None,
        "run_id": run_id if enabled else None,
        "run_attempt": env.get("GITHUB_RUN_ATTEMPT") if enabled else None,
        "job": env.get("GITHUB_JOB") if enabled else None,
        "run_url": f"{env.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{run_id}" if enabled and repo and run_id else None,
    }


def display_version(source: dict) -> str:
    commit = source["commit"]
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit):
        raise ValueError("Build identity requires a full Git commit hash")
    return f"g{commit}-{source['working_tree']['state']}"


def sdk_project_version(version: str) -> str:
    match = re.fullmatch(r"g([0-9a-f]{40}|[0-9a-f]{64})-(clean|dirty)", version)
    if not match:
        raise ValueError("SDK label requires a full build identity")
    return f"g{match[1][:12]}-{match[2]}"


def artifact_name(target: str, source: dict, context: dict) -> str:
    pr = context["pull_request"]
    kind = context["checkout_kind"]
    checkout = f"pr{pr['number']}-{kind}" if pr else kind
    name = f"motley-{target}-{display_version(source)}-{checkout}"
    if context["provider"] == "github-actions":
        name += f"-run{context['run_id']}-a{context['run_attempt']}"
    return re.sub(r"[^A-Za-z0-9._-]", "-", name)
