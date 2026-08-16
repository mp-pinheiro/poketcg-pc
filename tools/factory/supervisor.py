#!/usr/bin/env python3
"""Crash-resumable supervisor for the autonomous port factory.

The supervisor is deliberately a planner: translation and recovery are supplied
by callbacks, while queue ownership, journal identity, and completion remain
local and deterministic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))

import importlib.util
import common  # noqa: E402

ROOT = common.ROOT
JOURNAL = common.FACTORY / "supervisor.json"
LOCK_PATH = common.FACTORY / "supervisor.lock"
JOURNAL_SCHEMA = 1
HISTORICAL = common.HISTORICAL_STATES


def _revision() -> str | None:
    for command in (("git", "rev-parse", "HEAD"),
                    ("jj", "log", "--no-graph", "-r", "main", "-T", "commit_id")):
        try:
            result = subprocess.run(command, cwd=ROOT, text=True,
                                    capture_output=True, timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return None


def _load_report() -> dict:
    path = ROOT / "site" / "data" / "progress.json"
    try:
        spec = importlib.util.spec_from_file_location(
            "factory_progress_report", ROOT / "tools" / "progress" / "report.py")
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load progress report module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        inventory = module.load_inventory()
        routines, _ = module.load_routines()
        return module.compute(inventory, routines, module.load_gate())
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, json.JSONDecodeError):
        if not path.exists():
            raise
        return json.loads(path.read_text())


def gate_record_status(gate: dict | None, *, revision: str | None = None) -> dict:
    """Classify gate freshness separately from its routine verdicts."""
    if not isinstance(gate, dict) or gate.get("schema") != 1:
        return {"current": False, "green": False, "reason": "missing-or-malformed-gate"}
    inventory = gate.get("inventory")
    routines = gate.get("routines")
    if (not gate.get("complete") or not isinstance(inventory, dict)
            or not isinstance(routines, dict) or not routines):
        return {"current": False, "green": False, "reason": "incomplete-gate"}
    count = inventory.get("routines")
    if not isinstance(count, int) or count <= 0 or len(routines) != count:
        return {"current": False, "green": False, "reason": "invalid-gate-inventory"}
    if any(not isinstance(row, dict) or row.get("status") not in {"pass", "fail"}
           for row in routines.values()):
        return {"current": False, "green": False, "reason": "invalid-gate-routines"}
    recorded = gate.get("commit")
    tested = revision or _revision()
    if not recorded or not tested:
        return {"current": False, "green": False, "reason": "gate-revision-unavailable"}
    current = recorded == tested
    if not current:
        path = ROOT / "tools" / "progress" / "report.py"
        spec = importlib.util.spec_from_file_location(
            "progress_report_for_supervisor", path)
        if spec is None or spec.loader is None:
            return {"current": False, "green": False, "reason": "stale-gate"}
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        changed = module.gate_inputs_changed(recorded, tested)
        current = not changed
    green = current and not inventory.get("failures", 0) and not inventory.get("primary_missing", 0)
    return {"current": current, "green": green,
            "reason": "green" if green else ("gate-failures" if current else "stale-gate")}


def completion_status(report: dict, *, revision: str | None = None) -> dict:
    measures = report.get("measures") if isinstance(report, dict) else None
    gate = report.get("gate") if isinstance(report, dict) else None
    status = gate_record_status(gate if isinstance(gate, dict) else None,
                                revision=revision)
    required = ("verified_code", "verified_code/total",
                "verified_functions", "verified_functions/total")
    valid = isinstance(measures, dict) and all(isinstance(measures.get(k), int) for k in required)
    exact = valid and measures["verified_code"] == measures["verified_code/total"] \
        and measures["verified_functions"] == measures["verified_functions/total"]
    complete = bool(status["current"] and status["green"] and exact)
    return {"complete": complete, "gate": status, "exact_totals": bool(exact),
            "measures": measures or {},
            "reason": "complete" if complete else status["reason"] if not status["current"] else
            "verified-totals-incomplete" if not exact else "gate-not-green"}


def _frontier(report: dict, packets: list[dict]) -> list[dict]:
    rows = {r.get("work_id"): r for r in report.get("work_records", []) if r.get("work_id")}
    claims = common.claim_index(packets)
    result = []
    for work_id, row in rows.items():
        if row.get("state") in {"complete", "excluded"}:
            continue
        result.append({"work_id": work_id, "state": row.get("state"),
                       "claim": claims.get(work_id, {}).get("attempt_id")})
    return sorted(result, key=lambda row: row["work_id"])


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def snapshot() -> dict:
    report = _load_report()
    packets = common.list_packets()
    frontier = _frontier(report, packets)
    categories = {"fresh-ready": 0, "retry-ready": 0, "recovering": 0,
                  "dependency-blocked": 0, "harness-repair": 0,
                  "provider-wait": 0, "integrating": 0}
    for packet in packets:
        state = packet.get("state")
        count = len(packet.get("routines", []))
        if state == "retry-ready":
            categories["retry-ready"] += count
        elif state == "recovering":
            categories["recovering"] += count
        elif state == "blocked":
            categories["dependency-blocked"] += count
        elif state == "integrating":
            categories["integrating"] += count
        elif state in {"repair", "verifying", "translated", "translating"}:
            categories["harness-repair"] += count
    categories["fresh-ready"] = sum(
        1 for row in frontier if row.get("state") == "ready" and not row.get("claim"))
    revision = _revision()
    raw_gate = None
    gate_path = ROOT / "site" / "data" / "gate.json"
    if gate_path.exists():
        try:
            raw_gate = json.loads(gate_path.read_text())
        except json.JSONDecodeError:
            raw_gate = None
    completion_report = dict(report)
    if raw_gate is not None:
        completion_report["gate"] = raw_gate
    return {"schema": JOURNAL_SCHEMA, "revision": revision,
            "base_commit": revision, "frontier": frontier,
            "frontier_digest": _digest(frontier), "categories": categories,
            "completion": completion_status(completion_report, revision=revision),
            "packet_ids": sorted(p.get("attempt_id", p.get("id", "")) for p in packets
                                 if p.get("state") not in HISTORICAL),
            "generated_at": int(time.time())}
def _read_journal() -> dict | None:
    if not JOURNAL.exists():
        return None
    data = common.read_json(JOURNAL)
    if data.get("schema") != JOURNAL_SCHEMA:
        raise RuntimeError("STOP-THE-LINE corrupt supervisor journal schema")
    return data

def liveness_tuple(snap: dict) -> tuple:
    measures = snap.get("completion", {}).get("measures", {})
    return (measures.get("verified_code"), measures.get("verified_functions"),
            snap.get("frontier_digest"), snap.get("base_commit"),
            snap.get("revision"))


def _write_journal(data: dict) -> None:
    common.write_json(JOURNAL, data)


@contextmanager
def supervisor_lock() -> Iterator[None]:
    common.FACTORY.mkdir(parents=True, exist_ok=True)
    stream = LOCK_PATH.open("a+")
    try:
        import fcntl
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
        stream.close()


def _action_packet_ids(kind: str, snap: dict) -> list[str]:
    if kind == "integrate-green":
        states = {"green"}
    elif kind == "integration-resume":
        states = {"integrating", "green"}
    else:
        return list(snap["packet_ids"])
    return sorted(
        packet.get("attempt_id", packet.get("id", ""))
        for packet in common.list_packets()
        if packet.get("state") in states
    )


def next_action(*, current: dict | None = None) -> dict:
    snap = current or snapshot()
    journal = _read_journal()
    if journal and journal.get("phase") not in {"done", "failed", "idle"}:
        if journal.get("frontier_digest") != snap["frontier_digest"] or journal.get("base_commit") != snap["base_commit"]:
            return {"kind": "stop-the-line", "reason": "journal-identity-mismatch",
                    "action_id": journal.get("action_id"), "snapshot": snap}
        kind = journal.get("kind", "resume")
        return {"kind": kind, "action_id": journal.get("action_id"),
                "packet_ids": journal.get("packet_ids", []), "resume": True,
                "snapshot": snap}
    if not snap["completion"]["gate"]["current"]:
        kind = "gate-refresh"
    elif journal and journal.get("candidate_commit"):
        kind = "integration-resume"
    elif snap["categories"]["integrating"]:
        kind = "integration-resume"
    elif any(p.get("state") == "green" for p in common.list_packets()):
        kind = "integrate-green"
    elif snap["categories"]["retry-ready"]:
        kind = "retry-wave"
    elif snap["categories"]["fresh-ready"]:
        kind = "fresh-wave"
    elif snap["categories"]["dependency-blocked"]:
        kind = "revalidate-blockers"
    elif snap["completion"]["complete"]:
        kind = "complete"
    else:
        return {"kind": "stop-the-line", "reason": "invariant:no-frontier",
                "residual": snap["frontier"], "snapshot": snap}
    return {"kind": kind, "snapshot": snap,
            "packet_ids": _action_packet_ids(kind, snap)}

def _deterministic_action(action: dict, **_limits: Any) -> dict:
    kind = action["kind"]
    if kind == "gate-refresh":
        subprocess.run(["just", "oracle-release-gate"], cwd=ROOT, check=True)
        subprocess.run(["just", "progress"], cwd=ROOT, check=True)
        return {"status": "complete", "success": True, "kind": kind}
    if kind in {"integrate-green", "integration-resume"}:
        import integrate
        packets = [
            common.load_packet(packet_id)
            for packet_id in action.get("packet_ids", [])
        ]
        result = integrate.integrate(packets, push=True,
                                     group=kind == "integration-resume")
        subprocess.run(["just", "issues-sync-apply"], cwd=ROOT, check=True)
        subprocess.run(["just", "issues-verify"], cwd=ROOT, check=True)
        return {"status": "complete", "success": True, "kind": kind,
                "integration": result}
    if kind == "revalidate-blockers":
        return {"status": "blocked", "success": False, "kind": kind,
                "reason": "revalidation requires an SCC or cleared dependency"}
    raise RuntimeError(f"unsupported deterministic action {kind}")


def start(completion: Callable, *, lanes_count: int = 10,
          verify_width: int = 6, max_actions: int | None = None) -> dict:
    """Run the complete supervisor loop using the harness completion seam."""
    from driver import run_wave

    def wave(action: dict, *, model: str, **limits: Any) -> dict:
        def translate_many(prompts: list[str]) -> list[str]:
            return [completion(prompt, model=model) for prompt in prompts]
        return run_wave(
            action["packet_ids"], translate_many,
            lanes_count=limits["lanes_count"],
            verify_width=limits["verify_width"],
            model=model,
            max_rounds=3,
            max_wall_s=3600,
        )

    def translate_many(action: dict, **limits: Any) -> dict:
        return wave(action, model="default", **limits)

    def recover_many(action: dict, **limits: Any) -> dict:
        return wave(action, model="slow", **limits)

    def analyze_failure(action: dict, result: dict) -> str:
        prompt = (
            "Analyze this factory failure and return concrete repair guidance.\n"
            f"Action: {json.dumps(action, sort_keys=True)}\n"
            f"Result: {json.dumps(result, sort_keys=True)}"
        )
        return completion(prompt, model="slow")

    return supervise(
        translate_many, recover_many, analyze_failure,
        lanes_count=lanes_count, verify_width=verify_width,
        max_actions=max_actions,
    )


def supervise(translate_many: Callable | None, recover_many: Callable | None,
              analyze_failure: Callable | None, *, lanes_count: int = 10,
              verify_width: int = 6, max_actions: int | None = None) -> dict:
    if not any((translate_many, recover_many, analyze_failure)):
        raise TypeError("supervise requires runtime callback seams")
    run_id = str(uuid.uuid4())
    with supervisor_lock():
        actions = 0
        while max_actions is None or actions < max_actions:
            snap = snapshot()
            action = next_action(current=snap)
            if action["kind"] in {"complete", "stop-the-line"}:
                return action
            journal = {"schema": JOURNAL_SCHEMA, "run_id": run_id,
                       "action_id": str(uuid.uuid4()), "kind": action["kind"],
                       "phase": "planned", "frontier_digest": snap["frontier_digest"],
                       "base_commit": snap["base_commit"], "candidate_commit": None,
                       "packet_ids": action.get("packet_ids", []),
                       "attempt_generation": None, "not_before": 0,
                       "started_at": int(time.time()), "result": None}
            _write_journal(journal)
            if action["kind"] in {"gate-refresh", "integrate-green",
                                  "integration-resume", "revalidate-blockers"}:
                callback = _deterministic_action
            else:
                callback = recover_many if action["kind"] in {
                    "retry-wave", "revalidate-blockers"
                } else translate_many
            if callback is None:
                journal["phase"] = "failed"
                journal["result"] = {"reason": "callback-unavailable"}
                _write_journal(journal)
                return {"kind": "stop-the-line", "reason": "callback-unavailable", "action": action}
            journal["phase"] = "running"
            _write_journal(journal)
            try:
                result = callback(
                    action, lanes_count=lanes_count, verify_width=verify_width)
            except Exception as exc:
                result = {
                    "status": "failed",
                    "failure_class": "infrastructure",
                    "detail": f"{type(exc).__name__}: {exc}",
                    "retryable": True,
                }
            successful = isinstance(result, dict) and (
                result.get("success") is True or result.get("status") in {"green", "complete"})
            if not successful and analyze_failure is not None:
                analysis = analyze_failure(action, result)
                if isinstance(result, dict):
                    result = dict(result)
                    result["analysis"] = analysis
            after = snapshot()
            if (not successful and liveness_tuple(snap) == liveness_tuple(after)
                    and result.get("status") == "failed"):
                journal["phase"] = "failed"
                journal["result"] = result
                _write_journal(journal)
                return {
                    "kind": "stop-the-line",
                    "reason": "action-failed-without-progress",
                    "action": action,
                    "result": result,
                }
            if action["kind"] == "revalidate-blockers" and (
                    liveness_tuple(snap) == liveness_tuple(after)):
                journal["phase"] = "failed"
                journal["result"] = {
                    "reason": "dependency-revalidation-unresolved",
                    "residual": after["frontier"],
                }
                _write_journal(journal)
                return {
                    "kind": "stop-the-line",
                    "reason": "dependency-revalidation-unresolved",
                    "snapshot": after,
                }
            journal["phase"] = "idle"
            journal["result"] = result
            journal["liveness"] = liveness_tuple(after)
            if successful and liveness_tuple(snap) == liveness_tuple(after):
                journal["phase"] = "failed"
                journal["result"] = {"reason": "no-progress",
                                     "action": action["kind"],
                                     "packet_ids": action.get("packet_ids", [])}
                _write_journal(journal)
                return {"kind": "stop-the-line", "reason": "no-progress",
                        "action": action, "snapshot": after}
            actions += 1
        return {"kind": "stop-the-line", "reason": "action-limit", "actions": actions}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status")
    status.add_argument("--json", action="store_true")
    nxt = sub.add_parser("next")
    nxt.add_argument("--dry-run", action="store_true")
    nxt.add_argument("--json", action="store_true")
    args = parser.parse_args()
    with supervisor_lock():
        value = snapshot() if args.command == "status" else next_action()
    if args.json or args.command == "next":
        print(json.dumps(value, sort_keys=True))
    else:
        print(json.dumps(value, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
