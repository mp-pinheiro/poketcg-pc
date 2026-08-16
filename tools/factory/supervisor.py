#!/usr/bin/env python3
"""Bounded, crash-resumable control plane for the autonomous port factory."""
from __future__ import annotations

import argparse
import contextlib
import copy
import fcntl
import importlib.util
import io
import json
import sqlite3
import subprocess
import sys
import time
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import integrate
import scheduler
import state
import workers

ROOT = common.ROOT
LOCK_PATH = common.FACTORY / "supervisor.lock"


@contextmanager
def supervisor_lock() -> Iterator[None]:
    common.FACTORY.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("a+") as descriptor:
        fcntl.flock(descriptor.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(descriptor.fileno(), fcntl.LOCK_UN)


def _revision() -> str | None:
    for command in (
        ("jj", "log", "--no-graph", "-r", "main", "-T", "commit_id"),
        ("git", "rev-parse", "HEAD"),
    ):
        try:
            result = subprocess.run(
                command, cwd=ROOT, text=True, capture_output=True,
                timeout=5, check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return None

def _required_revision() -> str:
    revision = _revision()
    if revision is None:
        raise RuntimeError("cannot resolve current repository revision")
    return revision


def _load_report() -> dict[str, Any]:
    path = ROOT / "tools" / "progress" / "report.py"
    spec = importlib.util.spec_from_file_location("factory_live_progress", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load progress report module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with contextlib.redirect_stdout(io.StringIO()):
        inventory = module.load_inventory()
        routines, _ = module.load_routines()
        gate = module.load_gate()
        report = module.compute(inventory, routines, gate)
    report["gate"] = gate
    return report


def gate_record_status(
    gate: dict[str, Any] | None,
    *,
    revision: str | None = None,
) -> dict[str, Any]:
    """Classify gate freshness separately from its routine verdicts."""
    if not isinstance(gate, dict) or gate.get("schema") != 1:
        return {"current": False, "green": False, "reason": "missing-or-malformed-gate"}
    inventory = gate.get("inventory")
    routines = gate.get("routines")
    if (
        not gate.get("complete")
        or not isinstance(inventory, dict)
        or not isinstance(routines, dict)
        or not routines
    ):
        return {"current": False, "green": False, "reason": "incomplete-gate"}
    count = inventory.get("routines")
    if not isinstance(count, int) or count <= 0 or len(routines) != count:
        return {"current": False, "green": False, "reason": "invalid-gate-inventory"}
    if any(
        not isinstance(row, dict) or row.get("status") not in {"pass", "fail"}
        for row in routines.values()
    ):
        return {"current": False, "green": False, "reason": "invalid-gate-routines"}
    recorded = gate.get("commit")
    tested = revision or _revision()
    if not recorded or not tested:
        return {"current": False, "green": False, "reason": "gate-revision-unavailable"}
    current = recorded == tested
    if not current:
        path = ROOT / "tools" / "progress" / "report.py"
        spec = importlib.util.spec_from_file_location("factory_gate_freshness", path)
        if spec is None or spec.loader is None:
            return {"current": False, "green": False, "reason": "stale-gate"}
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        current = not module.gate_inputs_changed(recorded, tested)
    green = (
        current
        and not inventory.get("failures", 0)
        and not inventory.get("primary_missing", 0)
    )
    return {
        "current": current,
        "green": green,
        "reason": "green" if green else "gate-failures" if current else "stale-gate",
    }


def completion_status(
    report: dict[str, Any],
    *,
    revision: str | None = None,
) -> dict[str, Any]:
    measures = report.get("measures") if isinstance(report, dict) else None
    gate = report.get("gate") if isinstance(report, dict) else None
    gate_status = gate_record_status(
        gate if isinstance(gate, dict) else None, revision=revision,
    )
    required = (
        "verified_code", "verified_code/total",
        "verified_functions", "verified_functions/total",
    )
    valid = isinstance(measures, dict) and all(
        isinstance(measures.get(key), int) for key in required
    )
    exact = bool(
        valid
        and measures["verified_code"] == measures["verified_code/total"]
        and measures["verified_functions"] == measures["verified_functions/total"]
    )
    complete = bool(gate_status["current"] and gate_status["green"] and exact)
    reason = (
        "complete" if complete
        else gate_status["reason"] if not gate_status["current"]
        else "verified-totals-incomplete" if not exact
        else "gate-not-green"
    )
    return {
        "complete": complete,
        "gate": gate_status,
        "exact_totals": exact,
        "measures": measures or {},
        "reason": reason,
    }


def _open_state():
    if not common.STATE_DB.is_file():
        raise RuntimeError(
            "transactional state is absent; run driver.py migrate-recovery-state --apply"
        )
    return state.open_state()


def snapshot() -> dict[str, Any]:
    report = _load_report()
    completion = completion_status(report, revision=_revision())
    if not common.STATE_DB.is_file():
        return {
            "schema": 2,
            "state": "migration-required",
            "completion": completion,
            "categories": {},
        }
    connection = _open_state()
    try:
        durable = scheduler.snapshot(connection)
        active = connection.execute(
            """SELECT action_id, kind, phase, status, lease_owner, lease_deadline
               FROM action WHERE status IN ('planned','leased','running','recovering','expired')
               ORDER BY created_at, action_id"""
        ).fetchall()
    finally:
        connection.close()
    categories = durable["eligibility"]
    return {
        "schema": 2,
        "state": "complete" if completion["complete"] else "incomplete",
        "completion": completion,
        "categories": categories,
        "durable": durable,
        "active_actions": [
            {
                "action_id": row[0], "kind": row[1], "phase": row[2],
                "status": row[3], "lease_owner": row[4], "lease_deadline": row[5],
            }
            for row in active
        ],
    }


def _adopt_orphaned_supervisor_action(
    connection: sqlite3.Connection,
    *,
    lease_owner: str,
    now: int,
) -> None:
    if lease_owner != "supervise":
        return
    rows = connection.execute(
        """SELECT action_id, lease_owner FROM action
           WHERE status IN ('leased', 'running')
             AND lease_owner LIKE 'supervise-%'
             AND lease_deadline > ?
           ORDER BY created_at, action_id""",
        (now,),
    ).fetchall()
    for action_id, previous_owner in rows:
        _, _, pid_text = previous_owner.partition("-")
        if not pid_text.isdigit() or Path(f"/proc/{pid_text}").exists():
            continue
        with state.immediate(connection):
            connection.execute(
                """UPDATE action SET lease_owner = ?, updated_at = ?
                   WHERE action_id = ? AND lease_owner = ?
                     AND status IN ('leased', 'running')""",
                (lease_owner, now, action_id, previous_owner),
            )
        return


def _resume_owned_action(
    connection,
    *,
    lease_owner: str,
    lease_seconds: int,
    now: int,
) -> dict[str, Any] | None:
    row = connection.execute(
        """SELECT action_id, lease_token FROM action
           WHERE status IN ('leased','running') AND lease_owner = ?
             AND lease_deadline > ? ORDER BY created_at, action_id LIMIT 1""",
        (lease_owner, now),
    ).fetchone()
    if row is None:
        return None
    action_id, lease_token = row
    deadline = state.heartbeat_action(
        connection, action_id, lease_owner=lease_owner,
        lease_token=lease_token, lease_seconds=lease_seconds, now=now,
    )
    return {
        "status": "leased",
        "reused": True,
        "lease": {
            "action_id": action_id,
            "lease_owner": lease_owner,
            "lease_token": lease_token,
            "lease_deadline": deadline,
        },
        "action": scheduler.action_descriptor(connection, action_id),
    }


def next_action(
    *,
    lease_owner: str = "orchestrator",
    lease_seconds: int = 7200,
    lanes_count: int = 10,
) -> dict[str, Any]:
    completion = completion_status(_load_report(), revision=_revision())
    if completion["complete"]:
        return {"status": "complete", "message": "PORT COMPLETE", "completion": completion}
    connection = _open_state()
    try:
        _adopt_orphaned_supervisor_action(
            connection, lease_owner=lease_owner, now=int(time.time()),
        )
        resumed = _resume_owned_action(
            connection, lease_owner=lease_owner,
            lease_seconds=lease_seconds, now=int(time.time()),
        )
        if resumed is not None:
            return resumed
        recovered = scheduler.acquire_recovery_tick(
            connection, lease_owner=lease_owner, lease_seconds=lease_seconds,
        )
        if recovered is not None:
            return recovered
        if scheduler.has_publication_work(connection):
            return scheduler.acquire_tick(
                connection, lease_owner=lease_owner,
                lease_seconds=lease_seconds, lanes_count=lanes_count,
            )
        state.align_source_revision(connection, _required_revision())
        return scheduler.acquire_tick(
            connection, lease_owner=lease_owner, lease_seconds=lease_seconds,
            lanes_count=lanes_count,
        )
    finally:
        connection.close()


def accept_action(payload: dict[str, Any]) -> dict[str, Any]:
    connection = _open_state()
    try:
        action = scheduler.action_descriptor(connection, payload["action_id"])
        attempts = {
            attempt["attempt_id"]: attempt for attempt in action["attempts"]
        }
        attempt_results = payload.get("result", {}).get("attempts") or {}
        for attempt_id, result in attempt_results.items():
            attempt = attempts.get(attempt_id)
            if attempt is None:
                raise ValueError(f"result contains unknown attempt {attempt_id}")
            workers.publish_result(attempt, result)
        return scheduler.accept_tick(
            connection, payload["action_id"],
            lease_owner=payload["lease_owner"],
            lease_token=payload["lease_token"], result=payload["result"],
        )
    finally:
        connection.close()


def integrate_action(payload: dict[str, Any], *, push: bool = True) -> dict[str, Any]:
    connection = _open_state()
    try:
        return integrate.integrate_leased_action(
            connection, payload["action_id"],
            lease_owner=payload["lease_owner"],
            lease_token=payload["lease_token"], push=push,
        )
    finally:
        connection.close()


def reconcile_action(payload: dict[str, Any]) -> dict[str, Any]:
    connection = _open_state()
    try:
        integrate.run(
            ["just", "issues-sync-apply"],
            check_message="Forgejo reconciliation failed",
        )
        integrate.run(
            ["just", "issues-verify"],
            check_message="Forgejo projection verification failed",
        )
        return state.finish_projection_action(
            connection, payload["action_id"],
            lease_owner=payload["lease_owner"],
            lease_token=payload["lease_token"], now=int(time.time()),
        )
    finally:
        connection.close()



def _callback_values(
    callback: Callable[[list[dict[str, Any]]], Any],
    requests: list[dict[str, Any]],
) -> dict[str, Any]:
    if not requests:
        return {}
    returned = callback(copy.deepcopy(requests))
    if isinstance(returned, dict):
        values = returned
    elif isinstance(returned, list) and len(returned) == len(requests):
        values = {
            request.get(
                "request_id",
                request.get("attempt_id", request.get("work_id")),
            ): value
            for request, value in zip(requests, returned, strict=True)
        }
    else:
        raise TypeError("callback must return a keyed mapping or one value per request")
    expected = {
        request.get(
            "request_id",
            request.get("attempt_id", request.get("work_id")),
        )
        for request in requests
    }
    if set(values) != expected:
        raise ValueError(
            f"callback membership mismatch: expected={sorted(expected)} "
            f"actual={sorted(values)}"
        )
    return values

def _callback_values_parallel(
    callback: Callable[[list[dict[str, Any]]], Any],
    requests: list[dict[str, Any]],
    *,
    width: int,
) -> dict[str, Any]:
    def invoke(request: dict[str, Any]) -> tuple[str, Any]:
        values = _callback_values(callback, [request])
        return next(iter(values.items()))

    values = {}
    with ThreadPoolExecutor(max_workers=max(1, min(width, len(requests)))) as pool:
        for request_id, value in pool.map(invoke, requests):
            values[request_id] = value
    return values




def _worker_result(
    action: dict[str, Any],
    translate_many: Callable[[list[dict[str, Any]]], Any],
    recover_many: Callable[[list[dict[str, Any]]], Any],
    analyze_failure: Callable[[list[dict[str, Any]]], Any],
    *,
    lanes_count: int,
    verify_width: int,
) -> dict[str, Any]:
    attempts = {
        attempt["attempt_id"]: attempt for attempt in action.get("attempts", [])
    }
    lane_indices = list(range(lanes_count))
    translation = workers.translation_assignments(
        action, lane_indices=lane_indices,
    )
    def invoke_translation(assignment: dict[str, Any]) -> Any:
        return next(iter(_callback_values(translate_many, [assignment]).values()))

    def verify_translation(
        assignment: dict[str, Any],
        reply: str,
    ) -> tuple[str, dict[str, Any]]:
        attempt_id = assignment["attempt_id"]
        return attempt_id, workers.verify_reply(
            assignment["attempt"], reply,
            lane_index=assignment["lane_index"],
            deadline_seconds=assignment["deadline_seconds"],
            packet=assignment["packet"],
            lane=Path(assignment["lane"]),
        )

    results: dict[str, dict[str, Any]] = {}
    with (
        ThreadPoolExecutor(max_workers=max(1, len(translation))) as translators,
        ThreadPoolExecutor(max_workers=max(1, verify_width)) as verifiers,
    ):
        translation_futures = {
            translators.submit(invoke_translation, assignment): assignment
            for assignment in translation
        }
        verification_futures = {}
        for future in as_completed(translation_futures):
            assignment = translation_futures[future]
            reply = future.result()
            if (
                isinstance(reply, dict)
                and reply.get("outcome") in {
                    "provider-failure", "infrastructure-failure",
                }
            ):
                results[assignment["attempt_id"]] = reply
                continue
            if not isinstance(reply, str):
                raise TypeError(
                    f"translation reply for {assignment['attempt_id']} must be text"
                )
            verification = verifiers.submit(
                verify_translation, assignment, reply,
            )
            verification_futures[verification] = assignment["attempt_id"]
        for future in as_completed(verification_futures):
            attempt_id, result = future.result()
            results[attempt_id] = result

    used_lanes = len(translation)
    analysis_requests = workers.recovery_analysis_requests(action)
    analysis_replies = _callback_values_parallel(
        analyze_failure, analysis_requests, width=verify_width,
    )
    analyses = {
        attempt_id: workers.parse_recovery_analysis(reply)
        for attempt_id, reply in analysis_replies.items()
    }
    agent_assignments = workers.agent_assignments(
        action,
        lane_indices=lane_indices[used_lanes:],
        analyses=analyses,
    )
    if agent_assignments:
        def invoke_agent(assignment: dict[str, Any]) -> Any:
            return next(iter(_callback_values(recover_many, [assignment]).values()))

        def verify_agent(
            assignment: dict[str, Any],
        ) -> tuple[str, dict[str, Any]]:
            return assignment["attempt_id"], workers.verify_agent_lane(assignment)

        variant_results: dict[str, list[dict[str, Any]]] = {}
        central_before = workers.central_owned_snapshot(agent_assignments)
        try:
            with (
                ThreadPoolExecutor(
                    max_workers=max(1, len(agent_assignments)),
                ) as agents,
                ThreadPoolExecutor(max_workers=max(1, verify_width)) as verifiers,
            ):
                agent_futures = {
                    agents.submit(invoke_agent, assignment): assignment
                    for assignment in agent_assignments
                }
                verification_futures = {}
                for future in as_completed(agent_futures):
                    assignment = agent_futures[future]
                    returned = future.result()
                    if (
                        isinstance(returned, dict)
                        and returned.get("outcome") in {
                            "provider-failure", "infrastructure-failure",
                        }
                    ):
                        variant_results.setdefault(
                            assignment["attempt_id"], [],
                        ).append(returned)
                        continue
                    verification = verifiers.submit(verify_agent, assignment)
                    verification_futures[verification] = assignment["attempt_id"]
                for future in as_completed(verification_futures):
                    attempt_id, result = future.result()
                    variant_results.setdefault(attempt_id, []).append(result)
        except Exception as dispatch_error:
            try:
                workers.assert_central_owned_unchanged(
                    agent_assignments, central_before,
                )
            except Exception as isolation_error:
                raise ExceptionGroup(
                    "recovery dispatch and isolation both failed",
                    [dispatch_error, isolation_error],
                ) from None
            raise
        workers.assert_central_owned_unchanged(agent_assignments, central_before)
        for attempt_id, competing in variant_results.items():
            results[attempt_id] = workers.first_green(competing)

    reviews = workers.failure_review_requests(action, results)
    review_replies = _callback_values_parallel(
        analyze_failure, reviews, width=verify_width,
    )
    parsed_reviews = {
        attempt_id: workers.parse_failure_review(reply, attempt_id)
        for attempt_id, reply in review_replies.items()
    }
    if parsed_reviews:
        results = workers.merge_failure_reviews(action, results, parsed_reviews)
    if set(results) != set(attempts):
        raise ValueError(
            f"worker result mismatch: expected={sorted(attempts)} "
            f"actual={sorted(results)}"
        )
    return {"attempts": results, "work": {}}


def supervise(
    translate_many: Callable[[list[dict[str, Any]]], Any],
    recover_many: Callable[[list[dict[str, Any]]], Any],
    analyze_failure: Callable[[list[dict[str, Any]]], Any],
    *,
    lanes_count: int = 10,
    verify_width: int = 6,
) -> dict[str, Any]:
    """Run journaled actions until the authoritative completion predicate holds."""
    lease_owner = "supervise"
    with supervisor_lock():
        while True:
            planned = next_action(
                lease_owner=lease_owner,
                lease_seconds=7200,
                lanes_count=lanes_count,
            )
            if planned["status"] == "complete":
                return planned
            if planned["status"] != "leased":
                raise RuntimeError(json.dumps(planned, sort_keys=True))
            action = planned["action"]
            payload = {
                "action_id": action["action_id"],
                "lease_owner": planned["lease"]["lease_owner"],
                "lease_token": planned["lease"]["lease_token"],
            }
            kind = action["kind"]
            if kind in {
                "worker-wave", "fresh-wave", "retry-wave", "dependency-scc",
            }:
                payload["result"] = _worker_result(
                    action, translate_many, recover_many, analyze_failure,
                    lanes_count=lanes_count, verify_width=verify_width,
                )
                accept_action(payload)
            elif kind == "blocker-review":
                requests = workers.blocker_requests(action)
                replies = _callback_values(analyze_failure, requests)
                payload["result"] = {
                    "attempts": {},
                    "work": {
                        work_id: workers.parse_blocker_result(reply, work_id)
                        for work_id, reply in replies.items()
                    },
                }
                accept_action(payload)
            elif kind in {"integration", "gate-refresh"}:
                integrate_action(payload, push=True)
            elif kind == "projection-reconcile":
                reconcile_action(payload)
            else:
                raise RuntimeError(f"unsupported supervisor action: {kind}")



def preview_next(*, lanes_count: int = 10) -> dict[str, Any]:
    """Plan against an in-memory authority copy without leasing or mutation."""
    completion = completion_status(_load_report(), revision=_revision())
    if completion["complete"]:
        return {
            "status": "complete",
            "message": "PORT COMPLETE",
            "completion": completion,
        }
    source = _open_state()
    copy = sqlite3.connect(":memory:", isolation_level=None)
    copy.row_factory = sqlite3.Row
    try:
        source.backup(copy)
        planned = scheduler.plan_recovery_tick(copy)
        if planned is None:
            if scheduler.has_publication_work(copy):
                planned = scheduler.plan_tick(copy, lanes_count=lanes_count)
            else:
                state.align_source_revision(copy, _required_revision())
                planned = scheduler.plan_tick(copy, lanes_count=lanes_count)
        return {
            **planned,
            "dry_run": True,
            "completion": completion,
        }
    finally:
        copy.close()
        source.close()


def session_loop(
    *,
    lease_owner: str,
    lease_seconds: int,
    lanes_count: int,
) -> int:
    """Hold the supervisor lock while serving one bounded action at a time."""
    with supervisor_lock():
        print(json.dumps({
            "status": "ready",
            "lease_owner": lease_owner,
            "lease_seconds": lease_seconds,
            "lanes": lanes_count,
        }, sort_keys=True), flush=True)
        for line in sys.stdin:
            try:
                request = json.loads(line)
                if not isinstance(request, dict):
                    raise TypeError("session request must be an object")
                command = request.get("command")
                if command == "close":
                    print(json.dumps({"status": "closed"}), flush=True)
                    return 0
                if command == "status":
                    value = snapshot()
                elif command == "next":
                    value = next_action(
                        lease_owner=lease_owner,
                        lease_seconds=lease_seconds,
                        lanes_count=lanes_count,
                    )
                elif command == "accept":
                    value = accept_action(request["payload"])
                elif command == "integrate":
                    value = integrate_action(
                        request["payload"],
                        push=bool(request.get("push", True)),
                    )
                elif command == "reconcile":
                    value = reconcile_action(request["payload"])
                else:
                    raise ValueError(f"unknown session command: {command!r}")
                response = {"status": "ok", "value": value}
            except (
                KeyError, OSError, RuntimeError, TypeError, ValueError,
                sqlite3.Error, subprocess.SubprocessError,
            ) as exc:
                response = {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "detail": str(exc),
                }
            print(json.dumps(response, sort_keys=True), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    status_parser = sub.add_parser("status")
    status_parser.add_argument("--json", action="store_true")
    next_parser = sub.add_parser("next")
    next_parser.add_argument("--json", action="store_true")
    next_parser.add_argument("--dry-run", action="store_true")
    next_parser.add_argument("--lease-owner", default="orchestrator")
    next_parser.add_argument("--lease-seconds", type=int, default=7200)
    next_parser.add_argument("--lanes", type=int, default=10)
    sub.add_parser("reconcile")
    sub.add_parser("accept")
    integrate_parser = sub.add_parser("integrate")
    integrate_parser.add_argument("--no-push", action="store_true")
    session_parser = sub.add_parser("session")
    session_parser.add_argument("--lease-owner", default="orchestrator")
    session_parser.add_argument("--lease-seconds", type=int, default=7200)
    session_parser.add_argument("--lanes", type=int, default=10)
    args = parser.parse_args()
    if args.command == "session":
        return session_loop(
            lease_owner=args.lease_owner,
            lease_seconds=args.lease_seconds,
            lanes_count=args.lanes,
        )
    with supervisor_lock():
        if args.command == "status":
            value = snapshot()
        elif args.command == "next":
            value = (
                preview_next(lanes_count=args.lanes)
                if args.dry_run
                else next_action(
                    lease_owner=args.lease_owner,
                    lease_seconds=args.lease_seconds,
                    lanes_count=args.lanes,
                )
            )
        else:
            payload = json.load(sys.stdin)
            if args.command == "accept":
                value = accept_action(payload)
            elif args.command == "integrate":
                value = integrate_action(payload, push=not args.no_push)
            else:
                value = reconcile_action(payload)
    json_output = bool(getattr(args, "json", False))
    print(json.dumps(
        value, sort_keys=json_output, indent=None if json_output else 2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
