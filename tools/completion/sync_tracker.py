#!/usr/bin/env python3
"""Check or apply the manifest projection to the Forgejo tracker."""

from __future__ import annotations

import argparse
import json
import base64
import re
import os
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "tools" / "completion" / "requirements.toml"
REPO = "fairfruit/poketcg-pc"
ID_RE = re.compile(r"(?:ID|Stable ID|Completion obligation):\s*`?([A-Za-z0-9:._-]+)")


class TrackerError(RuntimeError):
    pass


def load_manifest() -> dict[str, Any]:
    try:
        with MANIFEST_PATH.open("rb") as stream:
            manifest = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise TrackerError(f"cannot load requirements manifest: {exc}") from exc
    if manifest.get("manifest", {}).get("schema") != 2:
        raise TrackerError("requirements manifest schema is not 2")
    return manifest


def issue_body(number: int, repo: str) -> str:
    try:
        result = subprocess.run(
            ["fj", "issue", "view", f"{repo}#{number}", "body"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise TrackerError(f"cannot read issue #{number}: {exc}") from exc
    if result.returncode:
        raise TrackerError(f"cannot read issue #{number}: {(result.stderr or result.stdout).strip()}")
    return result.stdout


def desired_body(req: dict[str, Any]) -> str:
    fields = ", ".join(req["state_fields"])
    deps = ", ".join(req["deps"]) or "none"
    return "\n".join([
        f"# Completion obligation: `{req['id']}`",
        "",
        f"- Source anchor: `{req['anchor']}`",
        f"- Milestone: `{req['milestone']}`",
        f"- Dependencies: {deps}",
        f"- Check: `{req['command']}`",
        f"- Terminal event: `{req['terminal_event']}`",
        f"- Minimum frames/events: `{req['min_frames']}` / `{req['min_events']}`",
        f"- Compared state fields: `{fields}`",
        f"- Artifact schema: `{req['artifact_schema']}`",
        "",
        (
            "Remote lifecycle is derived from revision-keyed evidence; tracker state "
            "does not contribute evidence."
        ),
        "",
    ])


def current_id(body: str) -> str | None:
    match = ID_RE.search(body)
    return match.group(1) if match else None

def issue_labels(body: str) -> set[str]:
    lines = body.splitlines()
    labels: set[str] = set()
    for line in lines[2:]:
        value = line.strip()
        if not value or value.startswith(">"):
            break
        labels.add(value)
    return labels


def desired_labels(lifecycle: str, milestone: str) -> set[str]:
    label_lifecycle = "ready" if lifecycle == "complete" else lifecycle
    return {"completion/v2", f"milestone/{milestone}", f"lifecycle/{label_lifecycle}"}

def issue_lifecycle(body: str) -> str:
    lines = body.splitlines()
    if len(lines) > 1 and "Closed" in lines[1]:
        return "closed"
    return "open"

def configured_secret(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    path = Path.home() / ".zsh_secrets"
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            normalized = line.removeprefix("export ").strip()
            if normalized.startswith(f"{name}="):
                return normalized.split("=", 1)[1].strip().strip("\"'")
    except OSError:
        return ""
    return ""


def forgejo_token() -> str:
    value = configured_secret("FJ_FORGEJO_TOKEN") or configured_secret("POKETCG_FORGEJO_TOKEN")
    if not value:
        token_path = Path(os.environ.get(
            "POKETCG_FORGEJO_TOKEN_FILE",
            str(Path.home() / ".config/yfrit-forgejo/api/poketcg-issues.token"),
        ))
        try:
            value = token_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise TrackerError(f"Forgejo API token is unavailable: {exc}") from exc
    value = value.removeprefix("Authorization:").strip()
    if value.casefold().startswith(("token ", "bearer ")):
        value = value.split(" ", 1)[1]
    if not value:
        raise TrackerError("Forgejo API token is empty")
    return value


def reopen_issue(repo: str, issue: int) -> None:
    owner, name = repo.split("/", 1)
    token = forgejo_token()
    username = configured_secret("FJ_FORGEJO_USER") or "mpp"
    authorization = base64.b64encode(f"{username}:{token}".encode()).decode()
    request = urllib.request.Request(
        f"https://forgejo.yfrit.com/api/v1/repos/{owner}/{name}/issues/{issue}",
        data=b'{"state":"open"}',
        method="PATCH",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {authorization}",
            "CF-Access-Client-Id": configured_secret("FJ_CF_ACCESS_CLIENT_ID"),
            "CF-Access-Client-Secret": configured_secret("FJ_CF_ACCESS_CLIENT_SECRET"),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status < 200 or response.status >= 300:
                raise TrackerError(f"issue #{issue} reopen returned HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        raise TrackerError(f"issue #{issue} reopen returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise TrackerError(f"issue #{issue} reopen failed: {exc.reason}") from exc


def desired_lifecycle(req_id: str, evidence: dict[str, Any]) -> str:
    status = evidence.get(req_id, {}).get("status")
    if status == "pass":
        return "complete"
    if status in {"failing", "stale", "unsupported"}:
        return "failing"
    return "ready"


def evidence_status() -> dict[str, Any]:
    command = [sys.executable, str(ROOT / "tools/completion/completion.py"), "status", "--json"]
    try:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=180, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise TrackerError(f"cannot read completion status: {exc}") from exc
    if result.returncode:
        raise TrackerError("completion status failed")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise TrackerError(f"completion status is not JSON: {exc}") from exc


def run_apply(
    issue: int, repo: str, body: str, lifecycle: str, milestone: str,
    old_labels: set[str], current_status: str = "open",
) -> None:
    target = f"{repo}#{issue}"
    result = subprocess.run(
        ["fj", "issue", "edit", target, "body", body],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode:
        raise TrackerError(f"issue #{issue} body update failed: {(result.stderr or result.stdout).strip()}")
    labels = desired_labels(lifecycle, milestone)
    for label in sorted(old_labels - labels):
        result = subprocess.run(
            ["fj", "issue", "edit", target, "labels", "--rm", label],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode:
            raise TrackerError(f"issue #{issue} label removal failed: {(result.stderr or result.stdout).strip()}")
    for label in sorted(labels - old_labels):
        result = subprocess.run(
            ["fj", "issue", "edit", target, "labels", "--add", label],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode:
            raise TrackerError(f"issue #{issue} label update failed: {(result.stderr or result.stdout).strip()}")
    if lifecycle == "complete":
        result = subprocess.run(
            ["fj", "issue", "close", target],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode:
            raise TrackerError(f"issue #{issue} close failed: {(result.stderr or result.stdout).strip()}")
    if lifecycle != "complete" and current_status == "closed":
        reopen_issue(repo, issue)

def restore_snapshot(path: Path) -> None:
    try:
        snapshot = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TrackerError(f"cannot read tracker snapshot: {exc}") from exc
    repo = snapshot.get("repo")
    issues = snapshot.get("issues")
    if not isinstance(repo, str) or not isinstance(issues, dict):
        raise TrackerError("tracker snapshot is malformed")
    for issue_text, saved in issues.items():
        if not isinstance(saved, dict) or not isinstance(saved.get("body"), str):
            raise TrackerError(f"tracker snapshot issue {issue_text} is malformed")
        issue = int(issue_text)
        current = issue_body(issue, repo)
        target = f"{repo}#{issue}"
        result = subprocess.run(
            ["fj", "issue", "edit", target, "body", saved["body"]],
            cwd=ROOT, capture_output=True, text=True, timeout=60, check=False,
        )
        if result.returncode:
            raise TrackerError(f"issue #{issue} body restore failed")
        current_labels = issue_labels(current)
        desired = set(saved.get("labels", []))
        for label in sorted(current_labels - desired):
            subprocess.run(
                ["fj", "issue", "edit", target, "labels", "--rm", label],
                cwd=ROOT, capture_output=True, text=True, timeout=60, check=False,
            )
        for label in sorted(desired - current_labels):
            subprocess.run(
                ["fj", "issue", "edit", target, "labels", "--add", label],
                cwd=ROOT, capture_output=True, text=True, timeout=60, check=False,
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--restore", type=Path)
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args(argv)
    if args.restore:
        try:
            restore_snapshot(args.restore)
        except (TrackerError, OSError, ValueError) as exc:
            print(json.dumps({"schema": 1, "status": "FAIL", "reason": str(exc)}, sort_keys=True))
            return 2
        print(json.dumps({"schema": 1, "status": "PASS", "mode": "restore"}, sort_keys=True))
        return 0
    try:
        manifest = load_manifest()
        repo = manifest.get("tracker", {}).get("repo", REPO)
        evidence = evidence_status()
        requirements = manifest.get("requirement", [])
        drift: list[dict[str, Any]] = []
        observations: list[dict[str, Any]] = []
        for req in requirements:
            if not isinstance(req, dict) or not isinstance(req.get("id"), str):
                continue
            issue = req.get("tracker_issue", 0)
            if not isinstance(issue, int) or issue <= 0:
                drift.append({"id": req["id"], "status": "missing-remote-identity"})
                continue
            body = issue_body(issue, repo)
            actual = current_id(body)
            expected = req["id"]
            lifecycle = desired_lifecycle(expected, evidence.get("requirements", {}))
            current_lifecycle = issue_lifecycle(body)
            labels = issue_labels(body)
            expected_labels = desired_labels(lifecycle, req["milestone"])
            expected_body = desired_body(req)
            body_drift = actual != expected or any(
                marker not in body for marker in expected_body.splitlines() if marker
            )
            label_drift = labels != expected_labels
            lifecycle_drift = (
                (lifecycle == "complete" and current_lifecycle != "closed")
                or (lifecycle != "complete" and current_lifecycle == "closed")
            )
            if body_drift or label_drift or lifecycle_drift:
                drift.append({
                    "id": expected,
                    "issue": issue,
                    "status": "projection-drift",
                    "actual_id": actual,
                    "desired_lifecycle": lifecycle,
                    "actual_lifecycle": current_lifecycle,
                    "label_drift": label_drift,
                    "lifecycle_drift": lifecycle_drift,
                })
            observations.append({
                "issue": issue,
                "body": body,
                "labels": sorted(labels),
                "request": req,
                "lifecycle": lifecycle,
                "current_lifecycle": current_lifecycle,
                "needs_update": body_drift or label_drift or lifecycle_drift,
            })
        snapshot_path = args.snapshot
        if args.apply and snapshot_path is None:
            snapshot_path = ROOT / "build" / "completion" / "tracker-backup.json"
        if snapshot_path is not None:
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_text(json.dumps({
                "schema": 1,
                "repo": repo,
                "issues": {
                    str(item["issue"]): {
                        "body": item["body"],
                        "labels": item["labels"],
                        "lifecycle": issue_lifecycle(item["body"]),
                    }
                    for item in observations
                },
            }, sort_keys=True, separators=(",", ":")) + "\n")
        applied = []
        if args.apply:
            for item in observations:
                if item["needs_update"]:
                    req = item["request"]
                    run_apply(
                        item["issue"], repo, desired_body(req), item["lifecycle"],
                        req["milestone"], set(item["labels"]),
                        item["current_lifecycle"],
                    )
                    applied.append(item["issue"])
        report = {
            "schema": 1,
            "repo": repo,
            "mode": "apply" if args.apply else "check",
            "drift": drift,
            "applied": applied,
            "snapshot": str(snapshot_path.relative_to(ROOT)) if snapshot_path and snapshot_path.is_relative_to(ROOT) else str(snapshot_path) if snapshot_path else None,
            "status": "PASS" if not drift else "DRIFT",
        }
        print(json.dumps(report, sort_keys=True))
        return 0 if not drift else 2
    except (TrackerError, OSError, ValueError) as exc:
        print(json.dumps({"schema": 1, "status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
