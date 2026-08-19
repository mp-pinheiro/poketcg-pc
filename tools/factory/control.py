#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import subprocess
import tempfile
import threading
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import cache
import common
import forecast
import forgejo
import integrate
import ledger
import migration
import packet as packet_builder
import prompt
import scheduler
import surgery
import workers

ROOT = Path(__file__).resolve().parents[2]
V2_ROOT = ROOT / ".factory" / "v2"
PROMPTS = V2_ROOT / "prompts"


class ControlError(RuntimeError):
    pass


@dataclass
class ReducedSnapshot:
    raw: dict[str, Any]
    control_issue: dict[str, Any] | None
    control: ledger.ControlView | None
    issues_by_work: dict[str, dict[str, Any]]
    views_by_work: dict[str, ledger.WorkView]
    packets_by_work: dict[str, dict[str, Any]]
    factory_snapshot: scheduler.FactorySnapshot


def response(
    operation: str,
    status: str,
    *,
    run_id: str | None = None,
    snapshot_sha256: str | None = None,
    data: object | None = None,
    error: tuple[str, str, str | None] | None = None,
) -> dict[str, Any]:
    return {
        "schema": 1,
        "op": operation,
        "status": status,
        "run_id": run_id,
        "snapshot_sha256": snapshot_sha256,
        "data": data,
        "error": (
            {"class": error[0], "detail": error[1], "retry_at": error[2]}
            if error else None
        ),
    }


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False,
    ) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, sort_keys=True, separators=(",", ":"))
        stream.write("\n")
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


OWNED_PATH_PREFIXES = (
    "src/home/", "src/probe/", "tests/cases/", "tools/oracle/mutation_receipts/",
)


def owned_dirty_paths(summary: str) -> list[str]:
    paths: set[str] = set()
    for line in summary.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        path = parts[1].strip().strip('"')
        if path.startswith(OWNED_PATH_PREFIXES):
            paths.add(path)
    return sorted(paths)


def dirty_port_paths(cwd: Path = ROOT) -> list[str]:
    for command in (
        ["jj", "diff", "--summary"],
        ["git", "status", "--porcelain", "--untracked-files=no"],
    ):
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
        if result.returncode == 0:
            return owned_dirty_paths(result.stdout)
    return []



def current_revision(cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "main", "-T", "commit_id"],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    revision = result.stdout.strip()
    if result.returncode != 0 or len(revision) != 40:
        raise ControlError("cannot resolve local jj main revision")
    return revision


def gate_record() -> dict[str, Any]:
    path = ROOT / "site" / "data" / "gate.json"
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ControlError("current gate record is unavailable") from exc
    if not isinstance(value, dict):
        raise ControlError("current gate record is invalid")
    return value


def authorized_authors(client: forgejo.ForgejoClient) -> set[str]:
    configured = os.environ.get("POKETCG_FACTORY_AUTHORS", "")
    values = {value.strip() for value in configured.split(",") if value.strip()}
    values.add(client.owner)
    return values


def priority(issue: dict[str, Any]) -> str:
    labels = set(issue.get("labels") or [])
    for value in ("urgent", "high", "normal", "low"):
        if f"priority/{value}" in labels:
            return value
    return "normal"


def _inventory_by_work() -> dict[str, dict[str, Any]]:
    functions, _inventory = packet_builder.compute_functions()
    values: dict[str, dict[str, Any]] = {}
    for function in functions:
        work_id = function.get("work_id")
        if isinstance(work_id, str):
            values[work_id] = function
    return values


def _paths_for_function(function: dict[str, Any]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    source = str(function.get("file") or "")
    basename = Path(source).stem
    if not basename:
        return (), ()
    paths = surgery.quad_paths(ROOT, basename)
    return (basename,), tuple(sorted(path.relative_to(ROOT).as_posix() for path in paths.values()))


def _factory_work(
    issue: dict[str, Any],
    marker: dict[str, Any],
    view: ledger.WorkView,
    inventory: dict[str, dict[str, Any]],
) -> scheduler.FactoryWork:
    work_id = view.work_id
    members = marker.get("members") if work_id.startswith("cohort:") else [work_id]
    if not isinstance(members, list):
        members = [work_id]
    records = [inventory[member] for member in members if member in inventory]
    if work_id.startswith("port:") and len(records) != 1:
        raise ControlError(f"inventory has no unique record for {work_id}")
    if work_id.startswith("cohort:") and len(records) != len(members):
        raise ControlError(f"cohort {work_id} has missing inventory members")
    basenames: set[str] = set()
    owned_paths: set[str] = set()
    for record in records:
        record_basenames, record_paths = _paths_for_function(record)
        basenames.update(record_basenames)
        owned_paths.update(record_paths)
    source = str(records[0].get("file") if records else issue.get("title") or work_id)
    size = sum(int(record.get("size") or 0) for record in records)
    tier = max((int(record.get("tier") or 1) for record in records), default=4)
    ready_at = view.canonical_event.created_at if view.canonical_event else forgejo.parse_time(issue.get("updated_at"))
    return scheduler.FactoryWork(
        issue_number=int(issue["number"]),
        work_id=work_id,
        source=source,
        basenames=tuple(sorted(basenames)) or (f"issue-{issue['number']}",),
        owned_paths=tuple(sorted(owned_paths)),
        size=size,
        tier=tier,
        priority=priority(issue),
        state=view.state,
        dependencies=tuple(sorted(view.blockers)),
        ready_at=ready_at,
        retry_at=view.retry_at,
        p50_seconds=420.0 if tier == 1 and not work_id.startswith("cohort:") else 900.0,
        cohort=work_id.startswith("cohort:"),
        recovery_tier=scheduler.recovery_tier(view.diagnostic_count, view.repeat_fingerprints),
        infra_failures=view.infra_failures,
        escalated=view.escalated,
    )


def reduced_snapshot(
    client: forgejo.ForgejoClient,
    *,
    full: bool = False,
) -> ReducedSnapshot:
    cache.refresh(client, full=full)
    raw = cache.load()
    inventory = _inventory_by_work()
    authors = authorized_authors(client)
    control_issue: dict[str, Any] | None = None
    control: ledger.ControlView | None = None
    issues_by_work: dict[str, dict[str, Any]] = {}
    views_by_work: dict[str, ledger.WorkView] = {}
    packets_by_work: dict[str, dict[str, Any]] = {}
    for issue in raw["issues"]:
        number = int(issue["number"])
        if ledger.control_marker(issue) is not None:
            if control_issue is not None:
                raise ControlError("multiple factory control issues exist")
            control_issue = issue
            control = ledger.reduce_control(
                issue,
                raw["comments"].get(number, []),
                now=datetime.now(UTC),
            )
            continue
        marker = ledger.work_marker(issue)
        if marker is None:
            continue
        view = ledger.reduce_work(
            issue,
            raw["comments"].get(number, []),
            raw["dependencies"].get(number, []),
            now=datetime.now(UTC),
            authorized_authors=authors,
            artifact_exists=workers.artifact_exists,
        )
        if view.work_id in issues_by_work:
            raise ControlError(f"duplicate v2 work ID {view.work_id}")
        issues_by_work[view.work_id] = issue
        views_by_work[view.work_id] = view
        packets_by_work[view.work_id] = marker
    cohort_members = {
        member
        for work_id, marker in packets_by_work.items()
        if work_id.startswith("cohort:")
        for member in marker.get("members") or []
    }
    works = tuple(
        _factory_work(issues_by_work[work_id], packets_by_work[work_id], view, inventory)
        for work_id, view in sorted(views_by_work.items())
        if work_id not in cohort_members
    )
    states = {work_id: view.as_dict() for work_id, view in views_by_work.items()}
    snapshot_sha256 = forgejo.sha256({
        "remote": raw.get("snapshot_sha256"),
        "states": states,
        "control": control.as_dict() if control else None,
    })
    active = frozenset(
        work_id
        for work_id, view in views_by_work.items()
        if view.state == "running" and work_id not in cohort_members
    )
    integrating = tuple(sorted(
        issue["number"]
        for work_id, issue in issues_by_work.items()
        if work_id not in cohort_members
        and views_by_work[work_id].state == "integrating"
        and views_by_work[work_id].productive_result_comment_id is not None
    ))
    factory = scheduler.FactorySnapshot(
        sha256=snapshot_sha256,
        works=works,
        active_work_ids=active,
        control_active=bool(control and control.active),
        integration_ready=integrating,
        complete=bool(views_by_work) and all(view.terminal for view in views_by_work.values()),
    )
    return ReducedSnapshot(
        raw=raw,
        control_issue=control_issue,
        control=control,
        issues_by_work=issues_by_work,
        views_by_work=views_by_work,
        packets_by_work=packets_by_work,
        factory_snapshot=factory,
    )


def _require_run(state: ReducedSnapshot, request: dict[str, Any]) -> ledger.ControlView:
    run_id = request.get("run_id")
    claim_comment_id = request.get("run_claim_comment_id")
    if state.control is None or state.control_issue is None:
        raise ControlError("factory control issue is missing")
    if not state.control.active:
        raise ControlError("factory run lease is not active")
    if run_id != state.control.run_id or claim_comment_id != state.control.claim_comment_id:
        raise ControlError("request does not hold the factory run lease")
    return state.control


def _packets_for_claim(
    work: scheduler.FactoryWork,
    marker: dict[str, Any],
    attempt_id: str,
    revision: str,
    issue_numbers: dict[str, int],
) -> list[dict[str, Any]]:
    if work.cohort:
        members = marker.get("members")
        if not isinstance(members, list) or not all(isinstance(member, str) for member in members):
            raise ControlError("cohort marker has no valid members")
        packets = packet_builder.build_scc_packets(set(members), issue_numbers=issue_numbers)
    else:
        packets = packet_builder.build_packets_for_work_ids(
            {work.work_id},
            issue_numbers=issue_numbers,
        )
    for index, packet in enumerate(packets):
        packet["attempt_id"] = attempt_id
        packet["id"] = attempt_id
        packet["artifact_key"] = attempt_id if len(packets) == 1 else f"{attempt_id}-{index}"
        packet["base_commit"] = revision
        packet["state"] = "pending"
        packet["not_before"] = 0
        common.validate_packet(packet)
    return packets


def _store_prompt(
    *,
    packet_sha256: str,
    attempt_id: str,
    work: scheduler.FactoryWork,
    packets: list[dict[str, Any]],
    prompt_text: str,
    lane_index: int,
    lane_root: str,
    lane_capability: str,
) -> Path:
    path = PROMPTS / f"{packet_sha256}.json"
    value = {
        "schema": 1,
        "attempt_id": attempt_id,
        "work_id": work.work_id,
        "issue_number": work.issue_number,
        "packets": packets,
        "prompt": prompt_text,
        "lane_index": lane_index,
        "lane_root": lane_root,
        "lane_capability": lane_capability,
        "owned_paths": list(work.owned_paths),
    }
    if path.exists():
        existing = json.loads(path.read_text())
        if existing != value:
            raise ControlError(f"prompt artifact identity conflict: {path}")
    else:
        atomic_json(path, value)
    return path


def _load_prompt(packet_sha256: str) -> dict[str, Any]:
    if not isinstance(packet_sha256, str) or len(packet_sha256) != 64:
        raise ControlError("packet_sha256 must be a SHA-256")
    path = PROMPTS / f"{packet_sha256}.json"
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ControlError("prompt artifact is missing or corrupt") from exc
    return value


def gate_matches_revision(gate: dict[str, Any], revision: str) -> bool:
    return bool(packet_builder.report_module().gate_is_trusted(gate, revision=revision))


def preflight(client: forgejo.ForgejoClient) -> dict[str, Any]:
    snapshot = client.stable_snapshot()
    first_issue = snapshot["issues"][0] if snapshot["issues"] else None
    if first_issue is not None:
        client.dependencies(int(first_issue["number"]))
    revision = current_revision()
    gate = gate_record()
    if not gate_matches_revision(gate, revision):
        raise ControlError("gate does not prove the current main revision")
    dirty = dirty_port_paths()
    if dirty:
        raise ControlError(f"central checkout has uncommitted port files: {dirty[:8]}")
    return {
        "repository": client.repository,
        "issue_snapshot_sha256": snapshot["sha256"],
        "issues": len(snapshot["issues"]),
        "revision": revision,
        "gate_commit": gate.get("commit"),
        "gate_complete": bool(gate.get("complete")),
    }


def status(client: forgejo.ForgejoClient, *, full: bool = False) -> dict[str, Any]:
    state = reduced_snapshot(client, full=full)
    counts: dict[str, int] = {}
    for view in state.views_by_work.values():
        counts[view.state] = counts.get(view.state, 0) + 1
    return {
        "snapshot_sha256": state.factory_snapshot.sha256,
        "control": state.control.as_dict() if state.control else None,
        "counts": counts,
        "works": len(state.views_by_work),
    }


def frontier(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client, full=bool(request.get("full")))
    capacity = scheduler.Capacity(
        job_slots=int(request.get("job_slots", 16)),
        verifier_slots=int(request.get("verifier_slots", 8)),
        active_jobs=int(request.get("active_jobs", 0)),
        provider_throttled=bool(request.get("provider_throttled", False)),
        verifier_queue_p95=float(request.get("verifier_queue_p95", 0.0)),
        verifier_soft_deadline=float(request.get("verifier_soft_deadline", 300.0)),
        healthy_completions=int(request.get("healthy_completions", 0)),
    )
    factory_plan = scheduler.plan(state.factory_snapshot, capacity)
    return response(
        "frontier",
        "complete" if factory_plan.complete else "waiting" if factory_plan.waiting_until else "ok",
        run_id=state.control.run_id if state.control else None,
        snapshot_sha256=state.factory_snapshot.sha256,
        data=factory_plan.as_dict(),
    )


SOFT_DEADLINE_SECONDS = {"smol": 420, "task": 900}
HARD_DEADLINE_SECONDS = {"smol": 1440, "task": 3600}
VERIFY_ALLOWANCE_SECONDS = 600


def _soft_deadline(route: str) -> int:
    return SOFT_DEADLINE_SECONDS.get(route, SOFT_DEADLINE_SECONDS["task"])


def _hard_deadline(route: str) -> int:
    return HARD_DEADLINE_SECONDS.get(route, HARD_DEADLINE_SECONDS["task"])


def _lease_seconds(request: dict[str, Any]) -> int:
    """A lease must outlive the deadline it authorizes, or the work is claimed twice."""
    floor = _hard_deadline(str(request.get("model_route", "smol"))) + VERIFY_ALLOWANCE_SECONDS
    requested = request.get("lease_seconds")
    seconds = int(requested) if isinstance(requested, int) else floor
    return min(max(seconds, floor), 7200)


def claim(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client)
    control = _require_run(state, request)
    work_id = request.get("work_id")
    if not isinstance(work_id, str) or work_id not in state.views_by_work:
        raise ControlError("claim references an unknown work ID")
    view = state.views_by_work[work_id]
    work = next(item for item in state.factory_snapshot.works if item.work_id == work_id)
    if view.state not in {"ready", "recovery"}:
        raise ControlError(f"{work_id} is not claimable: {view.state}")
    if view.canonical_event is None:
        raise ControlError(f"{work_id} has no migrated event")
    dirty = dirty_port_paths()
    if dirty:
        raise ControlError(f"central checkout has uncommitted port files: {dirty[:8]}")
    revision = current_revision()
    seed = forgejo.sha256({
        "work_id": work_id,
        "parent": view.canonical_event.event.event_id,
        "intent": view.intent_sha256,
        "revision": revision,
    })
    attempt_id = seed
    member_work_ids = state.packets_by_work[work_id].get("members") if work.cohort else [work_id]
    if not isinstance(member_work_ids, list):
        raise ControlError("cohort marker has invalid members")
    issue_numbers = {
        member: int(state.issues_by_work[member]["number"])
        for member in member_work_ids
    }
    packets = _packets_for_claim(
        work,
        state.packets_by_work[work_id],
        attempt_id,
        revision,
        issue_numbers,
    )
    packet_sha256 = forgejo.sha256({"packets": packets, "intent": view.intent_sha256})
    prompt_text = "\n\n".join(prompt.render(packet) for packet in packets)
    lane_index = int(seed[:8], 16) % 100000
    lane = workers.prepare_attempt_lane(
        packets,
        lane_index=lane_index,
        attempt_id=attempt_id,
        owned_paths=list(work.owned_paths),
    )
    lane_capability = secrets.token_hex(32)
    prompt_text = "\n".join((
        f"FACTORY_LANE_ROOT={lane}",
        f"FACTORY_LANE_CAPABILITY={lane_capability}",
        "",
        prompt_text,
    ))
    _store_prompt(
        packet_sha256=packet_sha256,
        attempt_id=attempt_id,
        work=work,
        packets=packets,
        prompt_text=prompt_text,
        lane_index=lane_index,
        lane_root=str(lane),
        lane_capability=lane_capability,
    )
    event = ledger.FactoryEvent.create(
        kind="claim",
        run_id=control.run_id or "",
        work_id=work_id,
        attempt_id=attempt_id,
        parent_comment_id=view.canonical_event.comment_id,
        parent_event_sha256=view.canonical_event.event.event_sha256,
        base_revision=revision,
        intent_sha256=view.intent_sha256 or "",
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "lease_seconds": _lease_seconds(request),
            "packet_sha256": packet_sha256,
            "model_route": request.get("model_route", "smol"),
            "owned_paths_sha256": forgejo.sha256(list(work.owned_paths)),
        },
    )
    comment = client.append_event(work.issue_number, event.comment_body(), event.event_id)
    winner = ledger.elect_lease(
        client.comments(work.issue_number),
        work_id=work_id,
        now=datetime.now(UTC),
    )
    if winner is None or winner.comment_id != comment["id"]:
        return response(
            "claim",
            "conflict",
            run_id=control.run_id,
            snapshot_sha256=state.factory_snapshot.sha256,
            error=("lease", "another claim won this work", None),
        )
    return response(
        "claim",
        "ok",
        run_id=control.run_id,
        snapshot_sha256=state.factory_snapshot.sha256,
        data={
            "issue_number": work.issue_number,
            "work_id": work_id,
            "attempt_id": attempt_id,
            "claim_comment_id": comment["id"],
            "packet_sha256": packet_sha256,
            "model_route": event.payload["model_route"],
            "lane_index": lane_index,
            "lane_capability": lane_capability,
            "owned_paths": list(work.owned_paths),
            "soft_deadline_seconds": _soft_deadline(str(event.payload["model_route"])),
            "hard_deadline_seconds": _hard_deadline(str(event.payload["model_route"])),
            "prompt": prompt_text,
        },
    )


def record(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client)
    control = _require_run(state, request)
    work_id = request.get("work_id")
    packet_sha256 = request.get("packet_sha256")
    claim_comment_id = request.get("claim_comment_id")
    if not isinstance(work_id, str) or not isinstance(packet_sha256, str) or not isinstance(claim_comment_id, int):
        raise ControlError("record needs work_id, packet_sha256, and claim_comment_id")
    view = state.views_by_work.get(work_id)
    if view is None or view.claim_comment_id != claim_comment_id:
        raise ControlError("record does not own the current work claim")
    prompt_artifact = _load_prompt(packet_sha256)
    if prompt_artifact.get("work_id") != work_id:
        raise ControlError("record prompt artifact work ID mismatch")
    packets = prompt_artifact.get("packets")
    if not isinstance(packets, list) or not packets:
        raise ControlError("record prompt artifact has no packets")
    deadline = int(request.get("deadline_seconds", 900))
    lane_index = int(prompt_artifact["lane_index"])
    workers.validate_attempt_lane(
        packets,
        lane_index=lane_index,
        attempt_id=str(prompt_artifact["attempt_id"]),
    )
    if isinstance(request.get("reply"), dict):
        if len(packets) != 1:
            raise ControlError("structured reply cannot verify a multi-packet cohort")
        result = workers.verify_attempt(
            packets[0], request["reply"], lane_index=lane_index, deadline_seconds=deadline,
        )
    else:
        result = workers.verify_lane_packets(
            packets, lane_index=lane_index, deadline_seconds=deadline,
        )
    outcome = str(result.get("outcome") or "diagnostic")
    verdict = result.get("verdict")
    if not isinstance(verdict, dict):
        raise ControlError("verifier returned no normalized verdict")
    artifact_sha256 = result.get("artifact_sha256") if outcome == "productive" else None
    if artifact_sha256 is not None and not workers.artifact_exists(artifact_sha256):
        raise ControlError("verifier returned a missing artifact")
    parent = view.canonical_event
    if parent is None:
        raise ControlError("record work has no canonical parent event")
    event = ledger.FactoryEvent.create(
        kind="attempt-result",
        run_id=control.run_id or "",
        work_id=work_id,
        attempt_id=str(prompt_artifact["attempt_id"]),
        parent_comment_id=parent.comment_id,
        parent_event_sha256=parent.event.event_sha256,
        base_revision=parent.event.base_revision,
        intent_sha256=view.intent_sha256 or "",
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "claim_comment_id": claim_comment_id,
            "outcome": outcome,
            "verdict": verdict,
            "artifact_sha256": artifact_sha256,
            "next_wake_at": request.get("next_wake_at"),
        },
    )
    comment = client.append_event(state.issues_by_work[work_id]["number"], event.comment_body(), event.event_id)
    escalation: dict[str, Any] | None = None
    if outcome == "diagnostic":
        pressure = scheduler.recovery_tier(
            view.diagnostic_count + 1,
            view.repeat_fingerprints + (1 if verdict.get("fingerprint") == view.last_fingerprint else 0),
        )
        if pressure >= scheduler.ESCALATION_DIAGNOSTICS:
            escalation = _escalate_work(
                client,
                state=state,
                view=view,
                run_id=control.run_id or "",
                diagnostic_count=view.diagnostic_count + 1,
                fingerprint=verdict.get("fingerprint"),
                parent_comment_id=int(comment["id"]),
                parent_event_sha256=event.event_sha256,
            )
    return response(
        "record",
        "ok",
        run_id=control.run_id,
        snapshot_sha256=state.factory_snapshot.sha256,
        data={
            "event_comment_id": comment["id"],
            "outcome": outcome,
            "artifact_sha256": artifact_sha256,
            "verdict": verdict,
            "escalation": escalation,
        },
    )


def _escalate_work(
    client: forgejo.ForgejoClient,
    *,
    state: ReducedSnapshot,
    view: ledger.WorkView,
    run_id: str,
    diagnostic_count: int,
    fingerprint: Any,
    parent_comment_id: int,
    parent_event_sha256: str,
) -> dict[str, Any]:
    issue = state.issues_by_work[view.work_id]
    event = ledger.FactoryEvent.create(
        kind="block",
        run_id=run_id,
        work_id=view.work_id,
        attempt_id=None,
        parent_comment_id=parent_comment_id,
        parent_event_sha256=parent_event_sha256,
        base_revision=view.base_revision or current_revision(),
        intent_sha256=view.intent_sha256 or "",
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "reason": "recovery-exhausted",
            "unblock": (
                f"{diagnostic_count} diagnostics"
                + (f", verdict fingerprint {fingerprint}" if isinstance(fingerprint, str) else "")
                + "; fix the cause, then post /factory unblock"
            ),
            "dependency_issue_numbers": [],
        },
    )
    comment = client.append_event(int(issue["number"]), event.comment_body(), event.event_id)
    labels = _projected_labels(issue, "blocked")
    if "attention/human" not in labels:
        labels = sorted([*labels, "attention/human"])
    client.set_projection(int(issue["number"]), labels=labels, state="open")
    return {
        "issue_number": int(issue["number"]),
        "event_comment_id": int(comment["id"]),
        "reason": "recovery-exhausted",
        "diagnostic_count": diagnostic_count,
    }


def _artifact_attempt_ids(record: dict[str, Any]) -> set[str]:
    identity = record.get("identity")
    if isinstance(identity, dict) and isinstance(identity.get("attempt_id"), str):
        return {identity["attempt_id"]}
    metadata = record.get("metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("members"), list):
        return set()
    records = {item["artifact_sha256"]: item for item in workers.artifact_records()}
    return {
        attempt_id
        for member in metadata["members"]
        if isinstance(member, str)
        for attempt_id in _artifact_attempt_ids(records.get(member, {}))
    }


def reconcile_artifacts(
    client: forgejo.ForgejoClient,
    state: ReducedSnapshot,
    *,
    run_id: str,
    run_claim_comment_id: int,
) -> dict[str, list[str]]:
    _require_run(state, {
        "run_id": run_id,
        "run_claim_comment_id": run_claim_comment_id,
    })
    records = workers.artifact_records()
    referenced = {
        event.event.payload["artifact_sha256"]
        for comments in state.raw["comments"].values()
        for comment in comments
        if (event := ledger.parse_event_comment(comment)) is not None
        and event.event.kind == "attempt-result"
        and isinstance(event.event.payload.get("artifact_sha256"), str)
    }
    grouped_members = {
        member
        for record in records
        if isinstance(record.get("metadata"), dict)
        for member in record["metadata"].get("members") or []
        if isinstance(member, str)
    }
    adopted: list[str] = []
    missing: list[str] = []
    for work_id, view in state.views_by_work.items():
        if view.state != "integrating" or not view.artifact_sha256:
            continue
        if workers.artifact_exists(view.artifact_sha256):
            continue
        parent = view.canonical_event
        if parent is None or view.productive_result_comment_id is None:
            continue
        event = ledger.FactoryEvent.create(
            kind="artifact-missing",
            run_id=run_id,
            work_id=work_id,
            attempt_id=parent.event.attempt_id,
            parent_comment_id=parent.comment_id,
            parent_event_sha256=parent.event.event_sha256,
            base_revision=parent.event.base_revision,
            intent_sha256=view.intent_sha256 or "",
            emitted_at=datetime.now(UTC).isoformat(),
            payload={
                "attempt_result_comment_id": view.productive_result_comment_id,
                "artifact_sha256": view.artifact_sha256,
                "reason": "artifact missing during reconciliation",
            },
        )
        client.append_event(
            int(state.issues_by_work[work_id]["number"]),
            event.comment_body(),
            event.event_id,
        )
        missing.append(work_id)
    for artifact in records:
        artifact_sha256 = artifact["artifact_sha256"]
        if artifact_sha256 in referenced or artifact_sha256 in grouped_members:
            continue
        attempts = _artifact_attempt_ids(artifact)
        if len(attempts) != 1:
            continue
        attempt_id = next(iter(attempts))
        for work_id, view in state.views_by_work.items():
            if view.state != "running" or view.claim_comment_id is None:
                continue
            claim = next(
                (item for item in view.chain if item.comment_id == view.claim_comment_id),
                None,
            )
            if claim is None or claim.event.attempt_id != attempt_id:
                continue
            parent = view.canonical_event
            if parent is None:
                continue
            event = ledger.FactoryEvent.create(
                kind="attempt-result",
                run_id=run_id,
                work_id=work_id,
                attempt_id=attempt_id,
                parent_comment_id=parent.comment_id,
                parent_event_sha256=parent.event.event_sha256,
                base_revision=parent.event.base_revision,
                intent_sha256=view.intent_sha256 or "",
                emitted_at=datetime.now(UTC).isoformat(),
                payload={
                    "claim_comment_id": view.claim_comment_id,
                    "outcome": "productive",
                    "verdict": {
                        "status": "green",
                        "phase": "artifact-reconcile",
                        "failure_class": None,
                        "scope": "routine",
                        "retry_action": "accept",
                        "work_ids": [work_id],
                        "summary": "recovered artifact",
                        "evidence": {},
                        "fingerprint": forgejo.sha256({"artifact": artifact_sha256, "work": work_id}),
                    },
                    "artifact_sha256": artifact_sha256,
                    "next_wake_at": None,
                },
            )
            client.append_event(
                int(state.issues_by_work[work_id]["number"]),
                event.comment_body(),
                event.event_id,
            )
            adopted.append(work_id)
            break
    return {"adopted": adopted, "missing": missing}


def reconcile_policy(
    client: forgejo.ForgejoClient,
    state: ReducedSnapshot,
    *,
    run_id: str,
) -> dict[str, list[str]]:
    """Make the ledger agree with `.factory/blocked.toml`, in both directions."""
    inventory = _inventory_by_work()
    blocked: list[str] = []
    cleared: list[str] = []
    for work_id, view in sorted(state.views_by_work.items()):
        if view.terminal or view.state in {"running", "integrating"}:
            continue
        record = inventory.get(work_id) or {}
        veto = record.get("operational_blocker")
        policy_blocked = view.state == "blocked" and not view.blockers and not view.escalated
        parent = view.canonical_event
        if parent is None:
            continue
        if veto and view.state != "blocked":
            event = ledger.FactoryEvent.create(
                kind="block",
                run_id=run_id,
                work_id=work_id,
                attempt_id=None,
                parent_comment_id=parent.comment_id,
                parent_event_sha256=parent.event.event_sha256,
                base_revision=parent.event.base_revision,
                intent_sha256=view.intent_sha256 or "",
                emitted_at=datetime.now(UTC).isoformat(),
                payload={
                    "reason": "operational-blocker",
                    "unblock": str(veto.get("unblock") or "clear the operational blocker"),
                    "dependency_issue_numbers": [],
                },
            )
            issue = state.issues_by_work[work_id]
            client.append_event(int(issue["number"]), event.comment_body(), event.event_id)
            labels = _projected_labels(issue, "blocked")
            if "attention/human" not in labels:
                labels = sorted([*labels, "attention/human"])
            client.set_projection(int(issue["number"]), labels=labels, state="open")
            blocked.append(work_id)
        elif policy_blocked and not veto:
            event = ledger.FactoryEvent.create(
                kind="unblock",
                run_id=run_id,
                work_id=work_id,
                attempt_id=None,
                parent_comment_id=parent.comment_id,
                parent_event_sha256=parent.event.event_sha256,
                base_revision=parent.event.base_revision,
                intent_sha256=view.intent_sha256 or "",
                emitted_at=datetime.now(UTC).isoformat(),
                payload={
                    "block_comment_id": parent.comment_id,
                    "reason": "operational blocker cleared",
                },
            )
            issue = state.issues_by_work[work_id]
            client.append_event(int(issue["number"]), event.comment_body(), event.event_id)
            cleared.append(work_id)
    return {"blocked": blocked, "cleared": cleared}


def reconcile(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client, full=bool(request.get("full", False)))
    artifacts = {"adopted": [], "missing": []}
    policy: dict[str, list[str]] = {"blocked": [], "cleared": []}
    if bool(request.get("adopt", False)):
        run_id = request.get("run_id")
        run_claim_comment_id = request.get("run_claim_comment_id")
        if not isinstance(run_id, str) or not isinstance(run_claim_comment_id, int):
            raise ControlError("artifact adoption needs the active factory run lease")
        artifacts = reconcile_artifacts(
            client,
            state,
            run_id=run_id,
            run_claim_comment_id=run_claim_comment_id,
        )
        policy = reconcile_policy(client, state, run_id=run_id)
    return response(
        "reconcile",
        "ok",
        run_id=state.control.run_id if state.control else None,
        snapshot_sha256=state.factory_snapshot.sha256,
        data={**status(client, full=False), "artifacts": artifacts, "policy": policy},
    )


def _control_intent(issue: dict[str, Any]) -> str:
    marker = ledger.control_marker(issue)
    if marker is None:
        raise ControlError("factory control issue is missing its marker")
    return forgejo.sha256(marker)


def run_claim(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client)
    if state.control_issue is None or state.control is None:
        raise ControlError("factory control issue is missing")
    if state.control.active:
        return response(
            "run-claim",
            "conflict",
            run_id=state.control.run_id,
            snapshot_sha256=state.factory_snapshot.sha256,
            error=("lease", "another factory run is active", state.control.claim_expires_at.isoformat() if state.control.claim_expires_at else None),
        )
    run_id = request.get("run_id") if isinstance(request.get("run_id"), str) else secrets.token_hex(16)
    parent = state.control.chain[-1] if state.control.chain else None
    event = ledger.FactoryEvent.create(
        kind="run-claim",
        run_id=run_id,
        work_id=None,
        attempt_id=None,
        parent_comment_id=parent.comment_id if parent else None,
        parent_event_sha256=parent.event.event_sha256 if parent else None,
        base_revision=current_revision(),
        intent_sha256=_control_intent(state.control_issue),
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "runner_instance": str(request.get("runner_instance") or os.getpid()),
            "lease_seconds": int(request.get("lease_seconds", 600)),
        },
    )
    comment = client.append_event(
        int(state.control_issue["number"]),
        event.comment_body(),
        event.event_id,
    )
    winner = ledger.elect_lease(
        client.comments(int(state.control_issue["number"])),
        work_id=None,
        now=datetime.now(UTC),
        control=True,
    )
    if winner is None or winner.comment_id != comment["id"]:
        return response(
            "run-claim",
            "conflict",
            run_id=run_id,
            snapshot_sha256=state.factory_snapshot.sha256,
            error=("lease", "another run won the control lease", None),
        )
    return response(
        "run-claim",
        "ok",
        run_id=run_id,
        snapshot_sha256=state.factory_snapshot.sha256,
        data={"run_claim_comment_id": comment["id"], "lease_seconds": event.payload["lease_seconds"]},
    )


def run_heartbeat(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client)
    control = _require_run(state, request)
    parent = state.control.chain[-1] if state.control and state.control.chain else None
    if parent is None or state.control_issue is None:
        raise ControlError("factory control chain is missing")
    event = ledger.FactoryEvent.create(
        kind="run-heartbeat",
        run_id=control.run_id or "",
        work_id=None,
        attempt_id=None,
        parent_comment_id=parent.comment_id,
        parent_event_sha256=parent.event.event_sha256,
        base_revision=current_revision(),
        intent_sha256=_control_intent(state.control_issue),
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "claim_comment_id": control.claim_comment_id,
            "lease_seconds": int(request.get("lease_seconds", 600)),
            "phase": str(request.get("phase", "running")),
        },
    )
    comment = client.append_event(int(state.control_issue["number"]), event.comment_body(), event.event_id)
    return response(
        "run-heartbeat",
        "ok",
        run_id=control.run_id,
        snapshot_sha256=state.factory_snapshot.sha256,
        data={"event_comment_id": comment["id"]},
    )


def run_release(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client)
    control = _require_run(state, request)
    parent = state.control.chain[-1] if state.control and state.control.chain else None
    if parent is None or state.control_issue is None:
        raise ControlError("factory control chain is missing")
    event = ledger.FactoryEvent.create(
        kind="run-release",
        run_id=control.run_id or "",
        work_id=None,
        attempt_id=None,
        parent_comment_id=parent.comment_id,
        parent_event_sha256=parent.event.event_sha256,
        base_revision=current_revision(),
        intent_sha256=_control_intent(state.control_issue),
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "claim_comment_id": control.claim_comment_id,
            "reason": str(request.get("reason", "released")),
        },
    )
    comment = client.append_event(int(state.control_issue["number"]), event.comment_body(), event.event_id)
    return response(
        "run-release",
        "ok",
        run_id=control.run_id,
        snapshot_sha256=state.factory_snapshot.sha256,
        data={"event_comment_id": comment["id"]},
    )


def _append_control_event(
    client: forgejo.ForgejoClient,
    state: ReducedSnapshot,
    *,
    kind: str,
    run_id: str,
    claim_comment_id: int,
    payload: dict[str, Any],
    base_revision: str,
) -> dict[str, Any]:
    if state.control_issue is None:
        raise ControlError("factory control issue is missing")
    comments = client.comments(int(state.control_issue["number"]))
    current = ledger.reduce_control(
        state.control_issue,
        comments,
        now=datetime.now(UTC),
    )
    if current.run_id != run_id or current.claim_comment_id != claim_comment_id:
        raise ControlError("factory run lease changed during control operation")
    parent = current.chain[-1] if current.chain else None
    if parent is None:
        raise ControlError("factory control event chain is missing")
    event = ledger.FactoryEvent.create(
        kind=kind,
        run_id=run_id,
        work_id=None,
        attempt_id=None,
        parent_comment_id=parent.comment_id,
        parent_event_sha256=parent.event.event_sha256,
        base_revision=base_revision,
        intent_sha256=_control_intent(state.control_issue),
        emitted_at=datetime.now(UTC).isoformat(),
        payload=payload,
    )
    return client.append_event(
        int(state.control_issue["number"]),
        event.comment_body(),
        event.event_id,
    )


def _projected_labels(issue: dict[str, Any], state: str) -> list[str]:
    labels = {
        label for label in issue.get("labels") or []
        if not label.startswith("port/") and not label.startswith("attention/")
    }
    labels.add(f"port/{state}")
    return sorted(labels)


def _landing_event(
    client: forgejo.ForgejoClient,
    *,
    issue: dict[str, Any],
    work_id: str,
    result: integrate.IntegrationResult,
    source_attempt_result_comment_id: int | None = None,
    source_attempt_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    comments = client.comments(int(issue["number"]))
    dependencies = client.dependencies(int(issue["number"]))
    commands = [
        command
        for comment in comments
        if (command := ledger.command_from_comment(comment, authorized_authors=authorized_authors(client))) is not None
    ]
    view = ledger.reduce_work(
        issue,
        comments,
        dependencies,
        now=datetime.now(UTC),
        authorized_authors=authorized_authors(client),
        artifact_exists=workers.artifact_exists,
    )
    parent = view.canonical_event
    result_comment_id = source_attempt_result_comment_id or view.productive_result_comment_id
    attempt_id = source_attempt_id or (parent.event.attempt_id if parent else None)
    if parent is None or result_comment_id is None:
        raise ControlError(f"{work_id} has no productive result to land")
    current_intent = ledger.intent_sha256(issue, dependencies, commands)
    if view.intent_sha256 != current_intent:
        raise ControlError(f"{work_id} intent changed before landing")
    event = ledger.FactoryEvent.create(
        kind="landed",
        run_id=parent.event.run_id,
        work_id=work_id,
        attempt_id=attempt_id,
        parent_comment_id=parent.comment_id,
        parent_event_sha256=parent.event.event_sha256,
        base_revision=result.source_revision,
        intent_sha256=current_intent,
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "batch_id": result.publication_revision,
            "attempt_result_comment_id": result_comment_id,
            "source_revision": result.source_revision,
            "publication_revision": result.publication_revision,
            "gate_sha256": result.gate_sha256,
            "progress_sha256": result.progress_sha256,
        },
    )
    comment = client.append_event(int(issue["number"]), event.comment_body(), event.event_id)
    return client.issue(int(issue["number"])), int(comment["id"])

def _sync_root_after_push(publication_revision: str) -> None:
    dirty = subprocess.run(
        ["jj", "diff", "--summary"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if dirty.returncode != 0 or dirty.stdout.strip():
        raise ControlError("factory root is dirty after integration push")
    fetched = subprocess.run(
        ["jj", "git", "fetch", "--remote", "origin"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if fetched.returncode != 0:
        raise ControlError("cannot fetch pushed factory revision into root")
    remote = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "main@origin", "-T", "commit_id"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    ).stdout.strip()
    if remote != publication_revision:
        raise ControlError("fetched origin main differs from pushed publication")
    rebased = subprocess.run(
        ["jj", "rebase", "-d", "main@origin"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if rebased.returncode != 0 or current_revision() != publication_revision:
        raise ControlError("cannot synchronize factory root to publication revision")


def _project_landing(
    client: forgejo.ForgejoClient,
    *,
    issue: dict[str, Any],
    work_id: str,
    result: integrate.IntegrationResult,
    run_id: str,
    source_attempt_result_comment_id: int | None = None,
    source_attempt_id: str | None = None,
) -> int:
    landed_issue, landed_comment_id = _landing_event(
        client,
        issue=issue,
        work_id=work_id,
        result=result,
        source_attempt_result_comment_id=source_attempt_result_comment_id,
        source_attempt_id=source_attempt_id,
    )
    projected = client.set_projection(
        int(landed_issue["number"]),
        labels=_projected_labels(landed_issue, "done"),
        state="closed",
    )
    landed_comments = client.comments(int(landed_issue["number"]))
    landed = next(item for item in landed_comments if item["id"] == landed_comment_id)
    event = ledger.parse_event_comment(landed)
    if event is None:
        raise ControlError("landed event was not readable")
    projection = ledger.FactoryEvent.create(
        kind="projection-repaired",
        run_id=run_id,
        work_id=work_id,
        attempt_id=event.event.attempt_id,
        parent_comment_id=event.comment_id,
        parent_event_sha256=event.event.event_sha256,
        base_revision=result.publication_revision,
        intent_sha256=event.event.intent_sha256,
        emitted_at=datetime.now(UTC).isoformat(),
        payload={
            "target_event_id": event.event.event_id,
            "labels": _projected_labels(projected, "done"),
            "issue_state": "closed",
            "readback_sha256": forgejo.issue_fingerprint(projected),
        },
    )
    comment = client.append_event(
        int(landed_issue["number"]),
        projection.comment_body(),
        projection.event_id,
    )
    return int(comment["id"])


def integrate_batch(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client, full=True)
    control = _require_run(state, request)
    numbers = request.get("issue_numbers")
    if numbers is None:
        numbers = list(state.factory_snapshot.integration_ready)
    if not isinstance(numbers, list) or not numbers or not all(isinstance(number, int) for number in numbers):
        raise ControlError("integration needs non-empty issue_numbers")
    by_number = {int(issue["number"]): work_id for work_id, issue in state.issues_by_work.items()}
    work_ids = [by_number.get(number) for number in sorted(set(numbers))]
    if any(work_id is None for work_id in work_ids):
        raise ControlError("integration references an unknown issue")
    artifacts: list[str] = []
    result_comment_ids: list[int] = []
    for work_id in work_ids:
        view = state.views_by_work[str(work_id)]
        if view.state != "integrating" or not view.artifact_sha256 or not view.productive_result_comment_id:
            raise ControlError(f"{work_id} is not ready for integration")
        artifacts.append(view.artifact_sha256)
        result_comment_ids.append(view.productive_result_comment_id)
    expected_remote = current_revision()
    _append_control_event(
        client,
        state,
        kind="integration-start",
        run_id=control.run_id or "",
        claim_comment_id=control.claim_comment_id or 0,
        payload={
            "batch_id": forgejo.sha256({"artifacts": sorted(artifacts), "remote": expected_remote}),
            "attempt_result_comment_ids": sorted(result_comment_ids),
            "artifact_sha256s": sorted(set(artifacts)),
            "expected_remote_revision": expected_remote,
        },
        base_revision=expected_remote,
    )
    lock = threading.RLock()
    stopped = threading.Event()
    heartbeat_error: list[BaseException] = []

    def append_phase(name: str, data: dict) -> None:
        with lock:
            fresh = reduced_snapshot(client)
            _append_control_event(
                client,
                fresh,
                kind="integration-phase",
                run_id=control.run_id or "",
                claim_comment_id=control.claim_comment_id or 0,
                payload={
                    "batch_id": forgejo.sha256({"artifacts": sorted(artifacts), "remote": expected_remote}),
                    "phase": name,
                    "input_sha256": forgejo.sha256(data),
                    "output_sha256": forgejo.sha256(data),
                    "source_revision": data.get("source_revision"),
                    "publication_revision": data.get("publication_revision"),
                },
                base_revision=str(data.get("publication_revision") or data.get("source_revision") or expected_remote),
            )

    def heartbeat_loop() -> None:
        while not stopped.wait(120):
            try:
                with lock:
                    fresh = reduced_snapshot(client)
                    _append_control_event(
                        client,
                        fresh,
                        kind="run-heartbeat",
                        run_id=control.run_id or "",
                        claim_comment_id=control.claim_comment_id or 0,
                        payload={
                            "claim_comment_id": control.claim_comment_id,
                            "lease_seconds": 600,
                            "phase": "integration",
                        },
                        base_revision=expected_remote,
                    )
            except (ControlError, forgejo.ForgejoError, ledger.LedgerError, OSError, ValueError) as exc:
                heartbeat_error.append(exc)
                return

    prospective_done = {str(work_id) for work_id in work_ids}
    for work_id in work_ids:
        if str(work_id).startswith("cohort:"):
            prospective_done.update(state.packets_by_work[str(work_id)].get("members") or [])
    prospective = forecast_status(client, {
        "completed_work_ids": sorted(prospective_done),
        "trials": int(request.get("forecast_trials", 20000)),
    })
    forecast_payload = prospective.get("data")
    if not isinstance(forecast_payload, dict):
        raise ControlError("prospective factory forecast is invalid")
    factory_state_payload = {
        "schema": 1,
        "snapshot_sha256": state.factory_snapshot.sha256,
        "counts": {
            name: sum(view.state == name for view in state.views_by_work.values())
            for name in ("ready", "running", "blocked", "recovery", "integrating", "paused", "done", "excluded")
        },
        "planned_landing_work_ids": sorted(prospective_done),
    }
    thread = threading.Thread(target=heartbeat_loop, daemon=True)
    thread.start()
    try:
        result = integrate.integrate_v2(
            sorted(set(artifacts)),
            expected_remote_revision=expected_remote,
            phase=append_phase,
            forecast_payload=forecast_payload,
            factory_state_payload=factory_state_payload,
        )
    finally:
        stopped.set()
        thread.join()
    if heartbeat_error:
        raise ControlError(f"integration lease heartbeat failed: {heartbeat_error[0]}")
    _sync_root_after_push(result.publication_revision)
    projections: list[int] = []
    for work_id in work_ids:
        source_view = state.views_by_work[str(work_id)]
        projections.append(_project_landing(
            client,
            issue=state.issues_by_work[str(work_id)],
            work_id=str(work_id),
            result=result,
            run_id=control.run_id or "",
        ))
        if not str(work_id).startswith("cohort:"):
            continue
        marker = state.packets_by_work[str(work_id)]
        members = marker.get("members") or []
        if not isinstance(members, list):
            raise ControlError("cohort marker has invalid members")
        names = {member.rsplit(":", 1)[-1] for member in members}
        if not names <= set(result.routine_names):
            raise ControlError("cohort integration artifact omitted member routines")
        parent = source_view.canonical_event
        if parent is None or source_view.productive_result_comment_id is None:
            raise ControlError("cohort has no productive result evidence")
        for member in members:
            if state.views_by_work[member].terminal:
                continue
            projections.append(_project_landing(
                client,
                issue=state.issues_by_work[member],
                work_id=member,
                result=result,
                run_id=control.run_id or "",
                source_attempt_result_comment_id=source_view.productive_result_comment_id,
                source_attempt_id=parent.event.attempt_id,
            ))
    append_phase("projections-stable", {"projection_comment_ids": projections, **result.as_dict()})
    return response(
        "integrate",
        "ok",
        run_id=control.run_id,
        snapshot_sha256=state.factory_snapshot.sha256,
        data=result.as_dict(),
    )
def _remote_main_revision() -> str:
    result = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/main"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    fields = result.stdout.split()
    if result.returncode != 0 or not fields or len(fields[0]) != 40:
        raise ControlError("cannot resolve remote main revision")
    return fields[0]


def _unaccepted_artifacts(state: ReducedSnapshot) -> list[str]:
    referenced: set[str] = set()
    for comments in state.raw["comments"].values():
        for comment in comments:
            event = ledger.parse_event_comment(comment)
            if event is None or event.event.kind != "attempt-result":
                continue
            artifact = event.event.payload.get("artifact_sha256")
            if isinstance(artifact, str):
                referenced.add(artifact)
    records = {record["artifact_sha256"]: record for record in workers.artifact_records()}
    expanded = set(referenced)
    for artifact in list(referenced):
        metadata = records.get(artifact, {}).get("metadata")
        if isinstance(metadata, dict) and isinstance(metadata.get("members"), list):
            expanded.update(member for member in metadata["members"] if isinstance(member, str))
    return sorted(set(records) - expanded)


def complete_factory(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client, full=True)
    control = _require_run(state, request)
    unfinished = sorted(
        work_id for work_id, view in state.views_by_work.items()
        if not view.terminal
    )
    if unfinished:
        return response(
            "complete",
            "waiting",
            run_id=control.run_id,
            snapshot_sha256=state.factory_snapshot.sha256,
            data={"unfinished": unfinished[:100], "count": len(unfinished)},
        )
    artifacts = _unaccepted_artifacts(state)
    if artifacts:
        return response(
            "complete",
            "waiting",
            run_id=control.run_id,
            snapshot_sha256=state.factory_snapshot.sha256,
            data={"unaccepted_artifacts": artifacts},
        )
    revision = current_revision()
    remote = _remote_main_revision()
    gate = gate_record()
    if remote != revision or not gate_matches_revision(gate, revision) or not gate.get("complete"):
        raise ControlError("remote main and current gate do not converge")
    first = client.stable_snapshot()
    second = client.stable_snapshot()
    if first["sha256"] != second["sha256"]:
        raise ControlError("Forgejo projection did not stabilize")
    gate_sha256 = forgejo.sha256(gate)
    _append_control_event(
        client,
        state,
        kind="port-complete",
        run_id=control.run_id or "",
        claim_comment_id=control.claim_comment_id or 0,
        payload={
            "remote_revision": remote,
            "publication_revision": revision,
            "gate_sha256": gate_sha256,
            "projection_sha256": second["sha256"],
        },
        base_revision=revision,
    )
    released = run_release(client, {
        "run_id": control.run_id,
        "run_claim_comment_id": control.claim_comment_id,
        "reason": "complete",
    })
    if released["status"] != "ok":
        raise ControlError("cannot release completed factory run")
    return response(
        "complete",
        "complete",
        run_id=control.run_id,
        snapshot_sha256=second["sha256"],
        data={"status": "complete", "message": "PORT COMPLETE"},
    )




def forecast_status(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    state = reduced_snapshot(client, full=bool(request.get("full", False)))
    completed_override = {
        value for value in request.get("completed_work_ids", [])
        if isinstance(value, str)
    }
    number_to_work = {
        work.issue_number: work.work_id
        for work in state.factory_snapshot.works
    }
    nodes = [
        forecast.Node(
            work_id=work.work_id,
            tier=work.tier,
            size=work.size,
            basenames=work.basenames,
            dependencies=tuple(
                number_to_work[number]
                for number in work.dependencies
                if number in number_to_work
            ),
            state="done" if work.work_id in completed_override else work.state,
            priority=work.priority,
        )
        for work in state.factory_snapshot.works
    ]
    external = [
        work.work_id
        for work in state.factory_snapshot.works
        if work.work_id not in completed_override
        and (
            work.state == "paused"
            or state.views_by_work[work.work_id].quarantined
            or any(number not in number_to_work for number in work.dependencies)
        )
    ]
    samples: list[forecast.Sample] = []
    for work in state.factory_snapshot.works:
        view = state.views_by_work[work.work_id]
        samples.extend(forecast.samples_from_chain(
            [
                {"kind": item.event.kind, "emitted_at": item.event.emitted_at}
                for item in view.chain
            ],
            tier=work.tier,
            size=work.size,
        ))
    confidence = "high" if len(samples) >= 30 else "low"
    if not samples:
        samples = forecast.provisional_history(
            ROOT / "site" / "data" / "history.jsonl",
            now=datetime.now(UTC),
        )
    if external:
        return response(
            "forecast",
            "ok",
            run_id=state.control.run_id if state.control else None,
            snapshot_sha256=state.factory_snapshot.sha256,
            data={
                "unconditional_eta": None,
                "conditional_on": external,
                "samples": len(samples),
                "confidence": "low",
            },
        )
    result = forecast.forecast_dates(
        forecast.monte_carlo(
            nodes,
            samples,
            lanes=int(request.get("lanes", 16)),
            trials=int(request.get("trials", 20000)),
            seed=state.factory_snapshot.sha256,
        ),
        started_at=datetime.now(UTC),
    )
    result["confidence"] = confidence
    result["unconditional_eta"] = result["p85_at"]
    return response(
        "forecast",
        "ok",
        run_id=state.control.run_id if state.control else None,
        snapshot_sha256=state.factory_snapshot.sha256,
        data=result,
    )


def migrate_factory(client: forgejo.ForgejoClient, request: dict[str, Any]) -> dict[str, Any]:
    snapshot = client.stable_snapshot()
    revision = current_revision()
    gate = gate_record()
    plan = migration.build_plan(snapshot, revision=revision, gate=gate)
    if not bool(request.get("apply", False)):
        return response(
            "migrate",
            "ok",
            snapshot_sha256=snapshot["sha256"],
            data={
                "plan_sha256": plan["plan_sha256"],
                "counts": plan["counts"],
                "actions": len(plan["actions"]),
                "unmarked_port_like": plan["unmarked_port_like"],
                "ignored_superseded": plan["ignored_superseded"],
            },
        )
    preflight(client)
    if migration.PLAN_PATH.is_file():
        try:
            saved = json.loads(migration.PLAN_PATH.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise ControlError("saved migration plan is corrupt") from exc
        if saved.get("gate_commit") != gate.get("commit"):
            raise ControlError("saved migration plan no longer matches the current gate")
        plan = saved
    else:
        migration.atomic_json(migration.PLAN_PATH, plan)
    limit = request.get("limit")
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ControlError("migrate limit must be a positive integer")
    workers = request.get("workers", 8)
    if not isinstance(workers, int) or not 1 <= workers <= 16:
        raise ControlError("migrate workers must be 1..16")
    result = migration.apply_plan(
        client, plan, gate=gate, limit=limit, workers=workers,
    )
    return response(
        "migrate",
        "ok",
        snapshot_sha256=snapshot["sha256"],
        data=result,
    )


def dispatch(operation: str, request: dict[str, Any], client: forgejo.ForgejoClient) -> dict[str, Any]:
    if operation == "preflight":
        return response("preflight", "ok", data=preflight(client))
    if operation == "status":
        value = status(client, full=bool(request.get("full", False)))
        return response("status", "ok", run_id=(value.get("control") or {}).get("run_id"), snapshot_sha256=value["snapshot_sha256"], data=value)
    if operation == "reconcile":
        return reconcile(client, request)
    if operation == "frontier":
        return frontier(client, request)
    if operation == "run-claim":
        return run_claim(client, request)
    if operation == "run-heartbeat":
        return run_heartbeat(client, request)
    if operation == "run-release":
        return run_release(client, request)
    if operation == "claim":
        return claim(client, request)
    if operation == "record":
        return record(client, request)
    if operation == "integrate":
        return integrate_batch(client, request)
    if operation == "forecast":
        return forecast_status(client, request)
    if operation == "migrate":
        return migrate_factory(client, request)
    if operation == "complete":
        return complete_factory(client, request)
    raise ControlError(f"unsupported operation {operation}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("preflight", "status", "reconcile", "frontier", "run-claim", "run-heartbeat", "run-release", "claim", "record", "integrate", "forecast", "migrate", "complete"))
    parser.add_argument("--request", default="{}")
    args = parser.parse_args()
    try:
        request = json.loads(args.request)
        if not isinstance(request, dict):
            raise ControlError("request must be a JSON object")
        value = dispatch(args.operation, request, forgejo.ForgejoClient())
    except (forgejo.ForgejoUnavailable, forgejo.ForgejoConflict) as exc:
        retry_at = (datetime.now(UTC) + timedelta(seconds=60)).isoformat()
        value = response(
            args.operation,
            "waiting",
            data={"waiting_until": retry_at, "waiting_reason": "forgejo-unavailable"},
            error=(type(exc).__name__, str(exc), retry_at),
        )
    except (ControlError, forgejo.ForgejoError, ledger.LedgerError, ValueError, OSError, json.JSONDecodeError) as exc:
        value = response(args.operation, "stop", error=(type(exc).__name__, str(exc), None))
    print(json.dumps(value, sort_keys=True))
    return 0 if value["status"] != "stop" else 2


if __name__ == "__main__":
    raise SystemExit(main())
