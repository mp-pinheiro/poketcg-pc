#!/usr/bin/env python3
"""Run the revision-pinned completion constituents and publish one attestation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "site" / "data" / "gate.json"
HISTORY_PATH = ROOT / "site" / "data" / "history.jsonl"
COMPLETION = ROOT / "tools" / "completion" / "completion.py"
PINS = ROOT / "tools" / "completion" / "bizhawk_pins.toml"


class GateError(RuntimeError):
    pass


def atomic_write(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def command_output(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=15, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GateError(f"cannot inspect revision: {exc}") from exc
    if result.returncode or not result.stdout.strip():
        raise GateError((result.stderr or result.stdout).strip() or "revision command failed")
    return result.stdout.strip()


def revision() -> str:
    try:
        return command_output(["jj", "log", "-r", "@-", "--no-graph", "-T", "commit_id"])
    except GateError:
        return command_output(["git", "rev-parse", "HEAD"])


def ensure_clean() -> None:
    try:
        result = subprocess.run(
            ["jj", "diff", "--name-only"], cwd=ROOT, capture_output=True, text=True,
            timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GateError(f"cannot inspect working tree: {exc}") from exc
    if result.returncode != 0:
        raise GateError("working tree status failed")
    if result.stdout.strip():
        raise GateError("release gate requires a clean working tree")


def source_tree_digest() -> str:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, timeout=30, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GateError(f"cannot enumerate committed source tree: {exc}") from exc
    if result.returncode:
        raise GateError("cannot enumerate committed source tree")
    digest = hashlib.sha256()
    for raw_path in sorted(filter(None, result.stdout.split(b"\0"))):
        path = ROOT / os.fsdecode(raw_path)
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise GateError(f"cannot read committed path {path}: {exc}") from exc
        digest.update(raw_path)
        digest.update(b"\0")
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
    except OSError:
        return "missing"
    return digest.hexdigest()


def external_identity(args: argparse.Namespace) -> dict[str, str]:
    values = {
        "baseline": str(ROOT / "tools/completion/baseline.toml"),
        "requirements": str(ROOT / "tools/completion/requirements.toml"),
        "bizhawk_pins": str(PINS),
        "rom": str(args.rom or ROOT / "poketcg/poketcg.gbc"),
        "symbols": str(args.symbols or ROOT / "poketcg/poketcg.sym"),
        "binary": str(args.binary or ROOT / "build/poketcg"),
        "data_pack": str(args.data_pack or ROOT / "build/completion/data-pack.bin"),
    }
    return {name: file_digest(Path(path)) for name, path in values.items()}


def content_key(revision_id: str, tree: str, external: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for name, value in (("revision", revision_id), ("tree", tree), *sorted(external.items())):
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\0")
    return digest.hexdigest()[:32]


def run_constituent(
    name: str, command: list[str], log_path: Path, timeout: float,
) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False
        )
        output = completed.stdout + ("\n" + completed.stderr if completed.stderr else "")
        log_path.write_text(output, encoding="utf-8")
        status = "PASS" if completed.returncode == 0 else "FAIL"
        return {
            "status": status,
            "returncode": completed.returncode,
            "duration": round(time.monotonic() - started, 3),
            "log": str(log_path.relative_to(ROOT)),
        }
    except subprocess.TimeoutExpired as exc:
        log_path.write_text(str(exc), encoding="utf-8")
        return {
            "status": "TIMEOUT",
            "returncode": None,
            "duration": round(time.monotonic() - started, 3),
            "log": str(log_path.relative_to(ROOT)),
        }
    except OSError as exc:
        log_path.write_text(str(exc), encoding="utf-8")
        return {
            "status": "UNAVAILABLE",
            "returncode": None,
            "duration": round(time.monotonic() - started, 3),
            "log": str(log_path.relative_to(ROOT)),
        }


def parse_json_log(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    decoder = json.JSONDecoder()
    for index in range(len(text)):
        if text[index] != "{":
            continue
        try:
            value, end = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if end and isinstance(value, dict):
            return value
    return None


def all_release_conditions(
    audit_report: dict[str, Any] | None,
    constituents: dict[str, dict[str, Any]],
) -> bool:
    if not audit_report or audit_report.get("complete") is not True:
        return False
    counts = audit_report.get("counts", {})
    if counts.get("unclassified_bytes") != 0:
        return False
    if counts.get("orphan_registrations") != 0:
        return False
    final = counts.get("final_routines", {})
    if final.get("count") != final.get("total"):
        return False
    production = counts.get("production_integration", {})
    if production.get("roots") != production.get("root_total"):
        return False
    if production.get("uncovered_required_edges") != 0:
        return False
    requirements = counts.get("requirements", {})
    if requirements.get("passing") != requirements.get("total"):
        return False
    milestones = counts.get("milestone_gates", {})
    if milestones.get("passing") != milestones.get("total"):
        return False
    trusted = counts.get("trusted_oracle_evidence", {})
    if trusted.get("count") != trusted.get("total"):
        return False
    return all(item.get("status") == "PASS" for item in constituents.values())


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--rom", type=Path)
    result.add_argument("--symbols", type=Path)
    result.add_argument("--binary", type=Path)
    result.add_argument("--data-pack", type=Path)
    result.add_argument("--timeout", type=float, default=180.0)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        ensure_clean()
        revision_id = revision()
        tree = source_tree_digest()
        external = external_identity(args)
        key = content_key(revision_id, tree, external)
        run_base = ROOT / "build" / "completion" / "runs" / key
        run_base.mkdir(parents=True, exist_ok=True)
        run_dir = run_base / f"{int(time.time())}-{os.getpid()}"
        run_dir.mkdir()
        constituents: dict[str, dict[str, Any]] = {}
        package_command = [
            sys.executable, str(ROOT / "tools/completion/package_smoke.py"),
            "--package", str(run_dir / "package"),
        ]
        if args.binary:
            package_command.extend(["--binary", str(args.binary)])
        if args.data_pack:
            package_command.extend(["--pack", str(args.data_pack)])
        commands = {
            "completion-audit": [sys.executable, str(COMPLETION), "audit"],
            "completion-cfg": ["just", "completion-cfg-audit"],
            "lane-health": ["just", "completion-lanes-health"],
            "bizhawk-health": ["just", "completion-bizhawk-health"],
            "package-smoke": package_command,
        }
        for name, command in commands.items():
            constituents[name] = run_constituent(
                name, command, run_dir / f"{name}.log", args.timeout
            )
        audit_report = parse_json_log(run_dir / "completion-audit.log")
        summary = {
            "schema": 3,
            "revision": revision_id,
            "source_tree_sha256": tree,
            "content_key": key,
            "external": external,
            "constituents": constituents,
            "audit": audit_report or {},
        }
        complete = all_release_conditions(audit_report, constituents)
        canonical = dict(summary)
        canonical["complete"] = complete
        attestation_material = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        attestation_digest = hashlib.sha256(attestation_material.encode()).hexdigest()
        (run_dir / "attestation.json").write_text(attestation_material + "\n", encoding="utf-8")
        pointer = {
            "schema": 3,
            "complete": complete,
            "content_key": key,
            "attestation_sha256": attestation_digest,
            "run_dir": str(run_dir.relative_to(ROOT)),
            "revision": revision_id,
            "constituents": constituents,
            "counts": (audit_report or {}).get("counts", {}),
        }
        atomic_write(GATE_PATH, json.dumps(pointer, sort_keys=True, separators=(",", ":")) + "\n")
        history = dict(pointer)
        history["timestamp"] = int(time.time())
        with HISTORY_PATH.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(history, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        print(json.dumps({
            "status": "PASS" if complete else "INCOMPLETE",
            "complete": complete,
            "content_key": key,
            "attestation_sha256": attestation_digest,
            "run_dir": str(run_dir.relative_to(ROOT)),
        }, sort_keys=True))
        return 0 if complete else 2
    except GateError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
