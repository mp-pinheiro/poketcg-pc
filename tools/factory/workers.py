#!/usr/bin/env python3
"""Disposable translation and agent-recovery adapters for leased actions."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import common
import lanes
import packet as packet_builder
import prompt as prompt_mod
import surgery
import verify


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()

def detail_digest(result: dict[str, Any]) -> str:
    payload = f"{result.get('status')}\n{result.get('detail') or ''}"
    return hashlib.sha1(payload.encode(), usedforsecurity=False).hexdigest()[:10]


def _apply_and_verify(
    packet: dict[str, Any],
    lane: Path,
    translation: dict[str, Any],
    statics_baseline: list[str] | None,
    rounds: int,
    deadline: float,
    wave_id: str,
    packet_id: str,
) -> dict[str, Any]:
    payload = json.dumps({
        "packet": packet,
        "lane": str(lane),
        "translation": translation,
        "statics_baseline": statics_baseline,
        "rounds": rounds,
        "deadline": deadline,
        "wave_id": wave_id,
        "packet_id": packet_id,
    })
    completed = common.run_bounded(
        [sys.executable, str(Path(__file__).with_name("verify_worker.py"))],
        cwd=common.ROOT,
        cap=max(0.001, deadline - time.monotonic()),
        deadline=deadline,
        check=True,
        input_text=payload,
    )
    response = json.loads(completed.stdout)
    if not isinstance(response, dict):
        raise TypeError("verification worker returned a non-object")
    if response.get("deadline"):
        raise common.WaveDeadlineExpired(str(response["deadline"]))
    result = response.get("result")
    baseline = response.get("statics_baseline")
    if not isinstance(result, dict) or not isinstance(result.get("status"), str):
        raise TypeError("verification worker returned an invalid verdict")
    if not isinstance(baseline, list):
        raise TypeError("verification worker returned an invalid statics baseline")
    result["_statics_baseline"] = baseline
    return result

def central_owned_snapshot(
    assignments: list[dict[str, Any]],
) -> dict[str, str | None]:
    relative_paths = {
        relative
        for assignment in assignments
        for relative in assignment["attempt"]["owned_paths"]
    }
    snapshot: dict[str, str | None] = {}
    for relative in sorted(relative_paths):
        if Path(relative).is_absolute():
            raise ValueError(f"attempt owned path must be relative: {relative}")
        path = common.ROOT / relative
        snapshot[relative] = (
            hashlib.sha256(path.read_bytes()).hexdigest()
            if path.is_file() else None
        )
    return snapshot


def assert_central_owned_unchanged(
    assignments: list[dict[str, Any]],
    expected: dict[str, str | None],
) -> None:
    actual = central_owned_snapshot(assignments)
    if actual != expected:
        changed = sorted(
            path for path in expected | actual
            if expected.get(path) != actual.get(path)
        )
        raise RuntimeError(
            "recovery agent modified orchestrator paths: " + ", ".join(changed)
        )


def materialize_packet(attempt: dict[str, Any]) -> dict[str, Any]:
    expected = {row["work_id"] for row in attempt["work"]}
    snapshot = attempt.get("snapshot") or {}
    routines = snapshot.get("routines") if isinstance(snapshot, dict) else None
    if (
        isinstance(routines, list)
        and routines
        and all(isinstance(row, dict) and row.get("asm") for row in routines)
    ):
        result = copy.deepcopy(snapshot)
    else:
        kind = "dependency-group" if attempt.get("role") == "dependency-scc" else "translation"
        packets = packet_builder.build_packets_for_work_ids(expected, kind=kind)
        if len(packets) != 1:
            raise RuntimeError(
                f"attempt {attempt['attempt_id']} materialized as {len(packets)} packets"
            )
        result = packets[0]
    actual = {row.get("work_id") for row in result.get("routines", [])}
    if actual != expected:
        raise RuntimeError(
            f"attempt membership mismatch: expected={sorted(expected)} actual={sorted(actual)}"
        )
    result["schema"] = common.SCHEMA
    result["attempt_id"] = attempt["attempt_id"]
    result["id"] = attempt["attempt_id"]
    result["cohort_id"] = common.cohort_id(expected)
    result["parent_attempt_id"] = snapshot.get("parent_attempt_id")
    result["attempt_generation"] = attempt.get("recovery_tier", attempt.get("generation", 0))
    result["base_commit"] = snapshot.get("base_revision") or snapshot.get("base_commit") \
        or result.get("base_commit")
    result["state"] = "pending"
    result["not_before"] = 0
    result["failure_history"] = list(attempt.get("failures") or [])
    result["updated_at"] = int(time.time())
    common.validate_packet(result)
    return result


def _failure_feedback(attempt: dict[str, Any]) -> str | None:
    failures = attempt.get("failures") or []
    if not failures:
        return None
    rows = []
    for failure in failures[-8:]:
        rows.append(
            f"[{failure.get('failure_class', 'unknown')}] "
            f"{failure.get('detail', 'failure')}"
        )
    return "Previous independent verifier evidence:\n" + "\n".join(rows)


def translation_requests(action: dict[str, Any]) -> list[dict[str, Any]]:
    requests = []
    for attempt in action.get("attempts", []):
        tier = int(attempt.get("recovery_tier", 0))
        if tier >= 4:
            continue
        packet = materialize_packet(attempt)
        requests.append({
            "attempt_id": attempt["attempt_id"],
            "model": "slow" if tier >= 2 else "default",
            "prompt": prompt_mod.render(packet, feedback=_failure_feedback(attempt)),
            "deadline_seconds": 900 if tier >= 2 else 420,
            "packet_sha256": _digest(packet),
            "packet": packet,
        })
    return requests


def translation_assignments(
    action: dict[str, Any],
    *,
    lane_indices: list[int],
    deadline_seconds: int = 120,
) -> list[dict[str, Any]]:
    requests = translation_requests(action)
    if len(lane_indices) < len(requests):
        raise ValueError(
            f"need {len(requests)} translation lanes, received {len(lane_indices)}"
        )
    attempts = {
        attempt["attempt_id"]: attempt for attempt in action.get("attempts", [])
    }
    assignments = []
    for lane_index, request in zip(lane_indices, requests, strict=False):
        attempt = attempts[request["attempt_id"]]
        packet = request["packet"]
        lane = lanes.ensure(
            lane_index,
            deadline=time.monotonic() + request["deadline_seconds"],
            packet=packet,
        )
        assignments.append({
            **request,
            "attempt": attempt,
            "packet": packet,
            "lane": str(lane),
            "lane_index": lane_index,
        })
    return assignments




def recovery_analysis_requests(action: dict[str, Any]) -> list[dict[str, Any]]:
    requests = []
    for attempt in action.get("attempts", []):
        if int(attempt.get("recovery_tier", 0)) < 4:
            continue
        requests.append({
            "attempt_id": attempt["attempt_id"],
            "model": "slow",
            "prompt": (
                "Independently analyze this repeatedly failing port attempt. Do not "
                "edit files. Return one JSON object with `root_cause`, `repair`, and "
                "`constraints`. Ground the repair in the supplied failure history and "
                "owned paths. "
                f"Evidence: {json.dumps(attempt, sort_keys=True)}"
            ),
        })
    return requests


def parse_recovery_analysis(reply: str) -> dict[str, Any]:
    start = reply.find("{")
    end = reply.rfind("}")
    if start < 0 or end < start:
        raise ValueError("recovery analysis returned no JSON object")
    try:
        value = json.loads(reply[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid recovery analysis JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise TypeError("recovery analysis must be a JSON object")
    for field in ("root_cause", "repair"):
        content = value.get(field)
        if isinstance(content, (dict, list)) and content:
            value[field] = json.dumps(content, sort_keys=True)
        elif not isinstance(content, str) or not content.strip():
            raise TypeError(f"recovery analysis requires nonempty {field}")
    constraints = value.get("constraints")
    if isinstance(constraints, dict) and constraints:
        value["constraints"] = json.dumps(constraints, sort_keys=True)
    elif not isinstance(constraints, (str, list)):
        raise TypeError("recovery analysis requires constraints")
    return value


def _agent_prompt(
    attempt: dict[str, Any],
    lane: Path,
    variant: int,
    packet: dict[str, Any],
    analysis: dict[str, Any] | None,
) -> str:
    failures = attempt.get("failures") or []
    assignment = {
        "attempt_id": attempt["attempt_id"],
        "variant": variant,
        "lane": str(lane),
        "owned_paths": [
            str(lane / relative) for relative in attempt["owned_paths"]
        ],
        "work_ids": sorted(row["work_id"] for row in attempt["work"]),
        "routines": [row["name"] for row in packet["routines"]],
        "failure_history": failures,
        "analysis": analysis,
        "verifier": (
            "python3 tools/factory/workers.py verify-agent "
            f"--assignment .recovery-assignment-{attempt['attempt_id']}.json"
        ),
    }
    assignment_path = lane / f".recovery-assignment-{attempt['attempt_id']}.json"
    assignment_path.write_text(json.dumps(
        {"attempt": attempt, "packet": packet, "analysis": analysis},
        sort_keys=True,
    ))
    return (
        "You are a disposable recovery editor in an isolated, credential-free lane.\n"
        f"Read {assignment_path.name} first; its packet contains the assembly for every routine.\n"
        f"Assignment: {json.dumps(assignment, sort_keys=True)}\n"
        "Edit only the absolute owned_paths; the process cwd is not the lane. "
        "Never resolve an owned path relative to cwd. Do not use git, jj, network, "
        "credentials, or files outside the lane. "
        "Implement every assigned routine completely; preserve factory markers and the existing "
        "case contract. Do not run the verifier or project-wide tests; the orchestrator verifies "
        "your lane after you return. Return a concise list of changed paths and any unresolved "
        "technical blocker."
    )


def agent_assignments(
    action: dict[str, Any],
    *,
    lane_indices: list[int],
    analyses: dict[str, dict[str, Any]] | None = None,
    deadline_seconds: int = 900,
) -> list[dict[str, Any]]:
    attempts = [
        attempt for attempt in action.get("attempts", [])
        if int(attempt.get("recovery_tier", 0)) >= 4
    ]
    required = sum(
        2 if int(attempt.get("recovery_tier", 0)) >= 4 else 1
        for attempt in attempts
    )
    if len(lane_indices) < required:
        raise ValueError(f"agent recovery needs {required} lane indices")
    analyses = analyses or {}
    expected_analyses = {
        attempt["attempt_id"] for attempt in attempts
        if int(attempt.get("recovery_tier", 0)) >= 4
    }
    if set(analyses) != expected_analyses:
        raise ValueError(
            f"recovery analysis membership mismatch: expected={sorted(expected_analyses)} "
            f"actual={sorted(analyses)}"
        )
    assignments = []
    lane_iter = iter(lane_indices)
    deadline = time.monotonic() + deadline_seconds
    for attempt in attempts:
        packet = materialize_packet(attempt)
        effective_attempt = copy.deepcopy(attempt)
        effective_attempt["owned_paths"] = common.port_owned_paths(packet["basename"])
        variants = 2 if int(attempt.get("recovery_tier", 0)) >= 4 else 1
        for variant in range(1, variants + 1):
            lane_index = next(lane_iter)
            lane = lanes.ensure(lane_index, deadline=deadline, packet=packet)
            environment = lanes.recovery_environment(lane)
            lanes.assert_recovery_environment(lane, environment)
            assignments.append({
                "attempt_id": attempt["attempt_id"],
                "request_id": f"{attempt['attempt_id']}:{variant}",
                "attempt": effective_attempt,
                "packet": packet,
                "variant": variant,
                "lane_index": lane_index,
                "lane": str(lane),
                "prompt": _agent_prompt(
                    effective_attempt, lane, variant, packet,
                    analyses.get(attempt["attempt_id"]),
                ),
                "owned_paths": [
                    str(lane / relative)
                    for relative in effective_attempt["owned_paths"]
                ],
                "environment_verified": True,
            })
    return assignments




def stage_bundle(packet: dict[str, Any], lane: Path) -> dict[str, Any]:
    _extracted, hashes = verify._validate_bundle_inputs(packet, lane)
    artifact_key = str(packet.get("artifact_key") or packet["attempt_id"])
    output = lane / ".factory-output" / artifact_key
    if output.exists():
        existing = common.payload_tree_digest(output)
        manifest = output / ".factory-artifact.json"
        if manifest.is_file():
            metadata = json.loads(manifest.read_text())
            expected = metadata.get("bundle_sha256")
            if expected and existing == expected:
                return {"artifact_dir": str(output), "bundle_sha256": existing}
        raise RuntimeError(f"immutable staged bundle already exists: {output}")
    output.mkdir(parents=True)
    for relative in sorted(hashes):
        source = lane / relative
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    identity = common.packet_identity(packet)
    (output / "packet.json").write_text(
        json.dumps(identity, sort_keys=True, indent=2) + "\n"
    )
    bundle_hash = common.payload_tree_digest(output)
    artifact = {"hashes": hashes, "bundle_sha256": bundle_hash}
    (output / ".factory-artifact.json").write_text(
        json.dumps(artifact, sort_keys=True, indent=2) + "\n"
    )
    return {"artifact_dir": str(output), "bundle_sha256": bundle_hash}


def publish_artifact(
    attempt: dict[str, Any],
    result: dict[str, Any],
) -> Path:
    """Atomically accept one verified lane artifact into the canonical bundle store."""
    source = Path(str(result.get("artifact_dir") or ""))
    bundle_hash = result.get("bundle_sha256")
    if not source.is_dir() or not isinstance(bundle_hash, str) or len(bundle_hash) != 64:
        raise ValueError("productive result requires a staged artifact and bundle hash")
    packet = materialize_packet(attempt)
    expected_identity = common.packet_identity(packet)
    manifest = source / "packet.json"
    if not manifest.is_file() or json.loads(manifest.read_text()) != expected_identity:
        raise RuntimeError("staged artifact packet identity mismatch")
    if common.payload_tree_digest(source) != bundle_hash:
        raise RuntimeError("staged artifact payload hash mismatch")
    destination = common.BUNDLES / attempt["attempt_id"]
    common.BUNDLES.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if (
            common.payload_tree_digest(destination) == bundle_hash
            and json.loads((destination / "packet.json").read_text()) == expected_identity
        ):
            return destination
        raise RuntimeError(f"canonical bundle identity conflict: {destination}")
    temporary = common.BUNDLES / f".accept-{attempt['attempt_id']}-{os.getpid()}"
    if temporary.exists():
        raise RuntimeError(f"artifact acceptance staging path exists: {temporary}")
    try:
        shutil.copytree(source, temporary)
        artifact_manifest = temporary / ".factory-artifact.json"
        if artifact_manifest.exists():
            artifact_manifest.unlink()
        if common.payload_tree_digest(temporary) != bundle_hash:
            raise RuntimeError("copied artifact payload hash mismatch")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return destination


def publish_result(
    attempt: dict[str, Any],
    result: dict[str, Any],
) -> list[Path]:
    """Publish every productive artifact before the state transaction accepts it."""
    if result.get("outcome") == "productive":
        return [publish_artifact(attempt, result)]
    if result.get("outcome") != "salvage":
        return []
    published = []
    for child in result.get("children", []):
        if child.get("state") != "green":
            continue
        snapshot = child.get("snapshot")
        if not isinstance(snapshot, dict):
            raise TypeError("green salvage child requires a snapshot")
        child_attempt = {
            "attempt_id": child["attempt_id"],
            "snapshot": snapshot,
            "work": [
                {
                    "work_id": routine["work_id"],
                    "source": routine["work_id"].split(":", 2)[1],
                    "name": routine["name"],
                }
                for routine in snapshot["routines"]
            ],
        }
        published.append(publish_artifact(child_attempt, child))
    return published




def _child_packet(
    parent: dict[str, Any],
    routine_names: set[str],
) -> dict[str, Any]:
    child = copy.deepcopy(parent)
    child_id = common.new_attempt_id()
    child["attempt_id"] = child_id
    child["id"] = child_id
    child["parent_attempt_id"] = parent["attempt_id"]
    child["attempt_generation"] = int(parent.get("attempt_generation", 0)) + 1
    child["routines"] = [
        routine for routine in parent["routines"]
        if routine["name"] in routine_names
    ]
    child["cohort_id"] = common.cohort_id({
        routine["work_id"] for routine in child["routines"]
    })
    child["state"] = "pending"
    child["not_before"] = 0
    child["updated_at"] = int(time.time())
    common.validate_packet(child)
    return child


def salvage_children(
    packet: dict[str, Any],
    lane: Path,
    verdict: dict[str, Any],
    *,
    deadline: float,
) -> dict[str, Any] | None:
    names = {routine["name"] for routine in packet["routines"]}
    reported = verdict.get("failing") or (
        [verdict["routine"]] if verdict.get("routine") else []
    )
    failing = {str(name) for name in reported if name in names}
    keep = names - failing
    if not failing or not keep:
        return None
    surgery.remove(lane, packet, sorted(failing))
    kept_packet = _child_packet(packet, keep)
    kept_verdict = verify.verify_packet(
        kept_packet, lane, True, deadline=deadline,
    )
    if kept_verdict.get("status") != "green":
        return None
    failed_packet = _child_packet(packet, failing)
    artifact = stage_bundle(kept_packet, lane)
    return {
        "outcome": "salvage",
        "children": [
            {
                "attempt_id": kept_packet["attempt_id"],
                "work_ids": sorted(
                    routine["work_id"] for routine in kept_packet["routines"]
                ),
                "snapshot": kept_packet,
                "state": "green",
                **artifact,
            },
            {
                "attempt_id": failed_packet["attempt_id"],
                "work_ids": sorted(
                    routine["work_id"] for routine in failed_packet["routines"]
                ),
                "snapshot": failed_packet,
                "state": "retry-ready",
            },
        ],
        "failure": _diagnostic(packet, verdict),
    }




def _diagnostic(packet: dict[str, Any], verdict: dict[str, Any]) -> dict[str, Any]:
    failure_class = str(verdict.get("failure_class") or verdict.get("status") or "unknown")
    detail = str(verdict.get("detail") or verdict.get("output") or verdict)
    return {
        "outcome": "diagnostic",
        "phase": "verification",
        "failure_class": failure_class,
        "detail": detail[-12000:],
        "fingerprint": _digest({
            "failure_class": failure_class,
            "detail": detail[-12000:],
        }),
    }


def verify_reply(
    attempt: dict[str, Any],
    reply: str,
    *,
    lane_index: int,
    deadline_seconds: int = 900,
    packet: dict[str, Any] | None = None,
    lane: Path | None = None,
    translate: Callable[[str], str] | None = None,
    max_rounds: int = 3,
) -> dict[str, Any]:
    packet = packet or materialize_packet(attempt)
    deadline = time.monotonic() + deadline_seconds
    lane = lane or lanes.ensure(lane_index, deadline=deadline, packet=packet)
    wave_id = f"action-{attempt['attempt_id']}"
    started = time.monotonic()
    rounds = 0
    last_digest: str | None = None
    statics_baseline: list[str] | None = None
    current = reply
    while True:
        common.record_event({
            "event": "verify-start", "wave_id": wave_id,
            "elapsed_s": round(time.monotonic() - started, 3),
            "packet_id": attempt["attempt_id"], "round": rounds,
        })
        round_started = time.monotonic()
        try:
            translation = prompt_mod.parse(current, packet)
        except prompt_mod.FormatError as exc:
            verdict = {
                "status": "format", "failure_class": "schema", "detail": str(exc),
            }
        else:
            verdict = _apply_and_verify(
                packet, lane, translation, statics_baseline, rounds, deadline,
                wave_id, attempt["attempt_id"],
            )
            statics_baseline = verdict.pop("_statics_baseline", None)
        digest = detail_digest(verdict)
        common.record_event({
            "event": "verify-finished", "wave_id": wave_id,
            "elapsed_s": round(time.monotonic() - started, 3),
            "packet_id": attempt["attempt_id"], "round": rounds,
            "status": verdict.get("status"), "digest": digest,
            "wall_s": round(time.monotonic() - round_started, 2),
        })
        if verdict.get("status") == "green":
            artifact = stage_bundle(packet, lane)
            return {"outcome": "productive", **artifact}
        repeated = digest == last_digest
        if (
            translate is None
            or rounds >= max_rounds
            or repeated
            or time.monotonic() >= deadline
        ):
            break
        last_digest = digest
        rounds += 1
        failing = verdict.get("failing") or (
            [verdict["routine"]] if verdict.get("routine") else None
        )
        feedback = f"{verdict.get('status')}:\n{verdict.get('detail') or ''}"
        current = translate(prompt_mod.render(packet, feedback, failing))
    salvage = salvage_children(packet, lane, verdict, deadline=deadline)
    return salvage or _diagnostic(packet, verdict)


def verify_agent_lane(
    assignment: dict[str, Any],
    *,
    deadline_seconds: int = 900,
) -> dict[str, Any]:
    attempt = assignment["attempt"]
    packet = assignment.get("packet") or materialize_packet(attempt)
    lane = Path(assignment["lane"])
    try:
        lanes.assert_recovery_environment(lane, lanes.recovery_environment(lane))
        deadline = time.monotonic() + deadline_seconds
        verdict = verify.verify_packet(
            packet, lane, True, deadline=deadline,
        )
        if verdict.get("status") != "green":
            salvage = salvage_children(packet, lane, verdict, deadline=deadline)
            return salvage or _diagnostic(packet, verdict)
        artifact = stage_bundle(packet, lane)
    except (OSError, RuntimeError, ValueError) as exc:
        return _diagnostic(packet, {
            "status": "bundle",
            "failure_class": "bundle",
            "detail": f"{type(exc).__name__}: {exc}",
        })
    return {"outcome": "productive", **artifact}


def failure_review_requests(
    action: dict[str, Any],
    results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    requests = []
    for attempt in action.get("attempts", []):
        attempt_id = attempt["attempt_id"]
        result = results.get(attempt_id)
        if (
            int(attempt.get("recovery_tier", 0)) != 2
            or not isinstance(result, dict)
            or result.get("outcome") != "diagnostic"
        ):
            continue
        requests.append({
            "attempt_id": attempt_id,
            "model": "slow",
            "prompt": (
                "Independently classify this failed port attempt. Do not edit files. "
                "Return one JSON object with `failure_scope` equal to `routine` or "
                "`shared-harness`, a stable `failure_class`, a concrete `detail`, and "
                "`failing_work_ids` containing only supplied canonical work IDs. "
                f"Evidence: {json.dumps({'attempt': attempt, 'result': result}, sort_keys=True)}"
            ),
        })
    return requests


def merge_failure_reviews(
    action: dict[str, Any],
    results: dict[str, dict[str, Any]],
    reviews: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    expected = {
        request["attempt_id"]
        for request in failure_review_requests(action, results)
    }
    if set(reviews) != expected:
        raise ValueError(
            f"failure review membership mismatch: expected={sorted(expected)} "
            f"actual={sorted(reviews)}"
        )
    merged = copy.deepcopy(results)
    attempts = {
        attempt["attempt_id"]: attempt for attempt in action.get("attempts", [])
    }
    for attempt_id, review in reviews.items():
        scope = review.get("failure_scope")
        if scope not in {"routine", "shared-harness"}:
            raise ValueError(f"invalid failure scope for {attempt_id}: {scope}")
        allowed = {
            work["work_id"] for work in attempts[attempt_id].get("work", [])
        }
        failing = set(review.get("failing_work_ids") or [])
        if not failing <= allowed:
            raise ValueError(
                f"unknown failing work IDs for {attempt_id}: {sorted(failing - allowed)}"
            )
        failure_class = str(
            review.get("failure_class")
            or merged[attempt_id].get("failure_class")
            or "unknown"
        )
        detail = str(review.get("detail") or merged[attempt_id].get("detail") or "")
        merged[attempt_id].update({
            "failure_scope": scope,
            "failure_class": f"{scope}:{failure_class}",
            "detail": detail,
            "failing_work_ids": sorted(failing),
            "phase": "failure-review",
            "fingerprint": _digest({
                "failure_scope": scope,
                "failure_class": failure_class,
                "detail": detail,
            }),
        })
    return merged


def blocker_requests(action: dict[str, Any]) -> list[dict[str, Any]]:
    requests = []
    for work in action.get("work", []):
        requests.append({
            "work_id": work["work_id"],
            "model": "slow",
            "prompt": (
                "Independently analyze this port blocker from the supplied evidence. "
                "Do not edit files. Return one JSON object only. Allowed outcomes: "
                "`unblocked` when the blocker evidence is stale; `blocked` with "
                "`blocked_on` canonical work IDs and `detail`; or `diagnostic` with "
                "`failure_class` and `detail` when a code or harness repair is required. "
                f"Evidence: {json.dumps(work, sort_keys=True)}"
            ),
        })
    return requests


def parse_failure_review(text: str, attempt_id: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"failure review for {attempt_id} returned no JSON object")
    result = json.loads(text[start:end + 1])
    if result.get("failure_scope") not in {"routine", "shared-harness"}:
        raise ValueError(f"invalid failure scope for {attempt_id}")
    if not isinstance(result.get("failure_class"), str):
        raise TypeError(f"failure review for {attempt_id} requires failure_class")
    if not isinstance(result.get("detail"), str):
        raise TypeError(f"failure review for {attempt_id} requires detail")
    result.setdefault("failing_work_ids", [])
    return result


def parse_blocker_result(text: str, work_id: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"blocker analysis for {work_id} returned no JSON object")
    result = json.loads(text[start:end + 1])
    outcome = result.get("outcome")
    if outcome not in {
        "unblocked", "blocked", "diagnostic", "provider-failure",
        "infrastructure-failure", "external-stop",
    }:
        raise ValueError(f"invalid blocker outcome for {work_id}: {outcome!r}")
    if outcome == "blocked":
        blocked_on = result.get("blocked_on")
        if not isinstance(blocked_on, list) or not all(
            isinstance(value, str) and value.startswith("port:v1:")
            for value in blocked_on
        ):
            raise ValueError("blocked outcome requires canonical blocked_on work IDs")
    if outcome == "diagnostic":
        result.setdefault("phase", "blocker-analysis")
        result.setdefault("failure_class", "blocker")
        result.setdefault("detail", "blocker requires repair")
        result["fingerprint"] = _digest({
            "work_id": work_id,
            "failure_class": result["failure_class"],
            "detail": result["detail"],
        })
    return result


def first_green(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Select the first verified repair, or retain both independent failures."""
    for result in results:
        if result.get("outcome") == "productive" or (
            result.get("outcome") == "salvage"
            and any(
                child.get("state") == "green"
                for child in result.get("children", [])
            )
        ):
            return result
    if not results:
        raise ValueError("competing recovery returned no results")
    for transient in ("provider-failure", "infrastructure-failure"):
        transient_results = [
            result for result in results if result.get("outcome") == transient
        ]
        if transient_results:
            retry_after = max(
                (int(result.get("retry_after", 0)) for result in transient_results),
                default=0,
            )
            return {
                "outcome": transient,
                "failure_class": transient.removesuffix("-failure"),
                "detail": json.dumps(results, sort_keys=True),
                "retry_after": retry_after,
                "phase": "competing-recovery",
            }
    if len(results) == 1:
        return results[0]
    evidence = [
        {
            "outcome": result.get("outcome"),
            "failure_class": result.get("failure_class"),
            "detail": result.get("detail"),
            "fingerprint": result.get("fingerprint"),
        }
        for result in results
    ]
    return {
        "outcome": "diagnostic",
        "phase": "independent-agent-recovery",
        "failure_class": "independent-agent-failures",
        "detail": json.dumps(evidence, sort_keys=True),
        "fingerprint": _digest(evidence),
    }


V2_ARTIFACTS = common.FACTORY / "artifacts"


def translation_from_reply(packet: dict[str, Any], reply: dict[str, Any]) -> dict[str, Any]:
    expected = {"attempt_id", "statics", "c", "header", "probe", "cases", "mutation"}
    if set(reply) != expected:
        raise ValueError(f"translation reply fields differ: {sorted(set(reply) ^ expected)}")
    attempt_id = packet.get("attempt_id") or packet.get("id")
    if reply["attempt_id"] != attempt_id:
        raise ValueError("translation reply attempt_id does not match packet")
    routines = packet.get("routines") or []
    if len(routines) != 1:
        raise ValueError("structured translation replies require exactly one routine")
    if not all(isinstance(reply[name], str) for name in expected - {"attempt_id"}):
        raise TypeError("translation reply code fields must be strings")
    name = routines[0]["name"]
    return {
        "statics": reply["statics"] or None,
        "routines": {
            name: {
                "C": reply["c"],
                "H": reply["header"],
                "PROBE": reply["probe"],
                "CASES": reply["cases"],
                "MUTATION": reply["mutation"],
            },
        },
    }


def artifact_exists(bundle_sha256: str) -> bool:
    if not isinstance(bundle_sha256, str) or len(bundle_sha256) != 64:
        return False
    root = V2_ARTIFACTS / bundle_sha256
    manifest = root / ".factory-artifact.json"
    if not root.is_dir() or not manifest.is_file():
        return False
    try:
        metadata = json.loads(manifest.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    if metadata.get("kind") == "group":
        members = metadata.get("members")
        return (
            isinstance(members, list)
            and members == sorted(set(members))
            and all(isinstance(member, str) and artifact_exists(member) for member in members)
            and _digest({"kind": "group", "members": members}) == bundle_sha256
        )
    return (
        metadata.get("bundle_sha256") == bundle_sha256
        and common.payload_tree_digest(root) == bundle_sha256
    )


def store_artifact(staged: dict[str, Any]) -> dict[str, Any]:
    source = Path(str(staged.get("artifact_dir") or ""))
    bundle_sha256 = staged.get("bundle_sha256")
    if not source.is_dir() or not isinstance(bundle_sha256, str) or len(bundle_sha256) != 64:
        raise ValueError("staged artifact requires a source directory and bundle SHA-256")
    if common.payload_tree_digest(source) != bundle_sha256:
        raise RuntimeError("staged artifact payload hash mismatch")
    V2_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    destination = V2_ARTIFACTS / bundle_sha256
    if destination.exists():
        if artifact_exists(bundle_sha256):
            return {"artifact_sha256": bundle_sha256, "artifact_dir": str(destination)}
        raise RuntimeError(f"artifact identity conflict: {destination}")
    temporary = V2_ARTIFACTS / f".stage-{bundle_sha256}-{os.getpid()}"
    if temporary.exists():
        raise RuntimeError(f"artifact staging path exists: {temporary}")
    try:
        shutil.copytree(source, temporary)
        if common.payload_tree_digest(temporary) != bundle_sha256:
            raise RuntimeError("copied artifact payload hash mismatch")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"artifact_sha256": bundle_sha256, "artifact_dir": str(destination)}


def verify_attempt(
    packet: dict[str, Any],
    reply: dict[str, Any],
    *,
    lane_index: int,
    deadline_seconds: int,
) -> dict[str, Any]:
    attempt_id = packet.get("attempt_id") or packet.get("id")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ValueError("packet requires attempt_id")
    deadline = time.monotonic() + deadline_seconds
    work_ids = sorted(str(routine["work_id"]) for routine in packet["routines"])
    try:
        translation = translation_from_reply(packet, reply)
        lane = validate_attempt_lane(
            [packet],
            lane_index=lane_index,
            attempt_id=attempt_id,
        )
        payload = json.dumps({
            "packet": packet,
            "lane": str(lane),
            "translation": translation,
            "statics_baseline": None,
            "rounds": 0,
            "deadline": deadline,
            "wave_id": f"v2-{attempt_id}",
            "packet_id": attempt_id,
        })
        completed = common.run_bounded(
            [sys.executable, str(Path(__file__).with_name("verify_worker.py"))],
            cwd=common.ROOT,
            cap=max(0.001, deadline - time.monotonic()),
            deadline=deadline,
            check=False,
            input_text=payload,
        )
        if completed.returncode != 0:
            raw = {
                "status": "infra-error",
                "phase": "verify-worker",
                "detail": completed.stdout + completed.stderr,
            }
        else:
            response = json.loads(completed.stdout)
            if not isinstance(response, dict) or not isinstance(response.get("result"), dict):
                raw = {
                    "status": "infra-error",
                    "phase": "verify-worker",
                    "detail": completed.stdout,
                }
            else:
                raw = response["result"]
    except (OSError, RuntimeError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raw = {
            "status": "infra-error",
            "phase": "verify-attempt",
            "detail": f"{type(exc).__name__}: {exc}",
        }
    normalized = verify.verdict_v1(raw, work_ids)
    if normalized["status"] != "green":
        return {
            "outcome": "diagnostic",
            "verdict": normalized,
            "detail": str(raw.get("detail") or ""),
        }
    lane = lanes.lane_dir(lane_index)
    staged = stage_bundle(packet, lane)
    artifact = store_artifact(staged)
    return {
        "outcome": "productive",
        "verdict": normalized,
        **artifact,
    }


def verify_lane_attempt(
    packet: dict[str, Any],
    *,
    lane_index: int,
    deadline_seconds: int,
) -> dict[str, Any]:
    deadline = time.monotonic() + deadline_seconds
    work_ids = sorted(str(routine["work_id"]) for routine in packet["routines"])
    lane = lanes.lane_dir(lane_index)
    try:
        raw = verify.verify_packet(packet, lane, True, deadline=deadline)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        raw = {
            "status": "infra-error",
            "phase": "verify-lane",
            "detail": f"{type(exc).__name__}: {exc}",
        }
    normalized = verify.verdict_v1(raw, work_ids)
    if normalized["status"] != "green":
        return {
            "outcome": "diagnostic",
            "verdict": normalized,
            "detail": str(raw.get("detail") or ""),
        }
    staged = stage_bundle(packet, lane)
    artifact = store_artifact(staged)
    return {
        "outcome": "productive",
        "verdict": normalized,
        **artifact,
    }


def store_group_artifact(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    members = sorted({
        str(artifact["artifact_sha256"])
        for artifact in artifacts
        if isinstance(artifact.get("artifact_sha256"), str)
    })
    if not members or len(members) != len(artifacts) or not all(artifact_exists(member) for member in members):
        raise ValueError("group artifact members are missing or invalid")
    group_sha256 = _digest({"kind": "group", "members": members})
    destination = V2_ARTIFACTS / group_sha256
    if destination.exists():
        if artifact_exists(group_sha256):
            return {"artifact_sha256": group_sha256, "artifact_dir": str(destination)}
        raise RuntimeError(f"group artifact identity conflict: {destination}")
    temporary = V2_ARTIFACTS / f".group-{group_sha256}-{os.getpid()}"
    try:
        temporary.mkdir(parents=True)
        (temporary / "members").mkdir()
        for member in members:
            shutil.copytree(V2_ARTIFACTS / member, temporary / "members" / member)
        (temporary / ".factory-artifact.json").write_text(
            json.dumps({"kind": "group", "members": members, "bundle_sha256": group_sha256}, sort_keys=True) + "\n"
        )
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"artifact_sha256": group_sha256, "artifact_dir": str(destination)}


def verify_lane_packets(
    packets: list[dict[str, Any]],
    *,
    lane_index: int,
    deadline_seconds: int,
) -> dict[str, Any]:
    outcomes = [
        verify_lane_attempt(
            packet,
            lane_index=lane_index,
            deadline_seconds=deadline_seconds,
        )
        for packet in packets
    ]
    failures = [outcome for outcome in outcomes if outcome.get("outcome") != "productive"]
    if failures:
        return {
            "outcome": "diagnostic",
            "verdict": failures[0]["verdict"],
            "detail": json.dumps(failures, sort_keys=True),
        }
    artifact = store_group_artifact(outcomes)
    return {
        "outcome": "productive",
        "verdict": {
            "status": "green",
            "phase": "group",
            "failure_class": None,
            "scope": "routine",
            "retry_action": "accept",
            "work_ids": sorted(
                routine["work_id"] for packet in packets for routine in packet["routines"]
            ),
            "summary": "green",
            "evidence": {},
            "fingerprint": _digest({"packets": [packet["attempt_id"] for packet in packets]}),
        },
        **artifact,
    }


V2_STATE = common.FACTORY / "v2"


def packet_sha256(packets: list[dict[str, Any]]) -> str:
    return _digest({"packets": packets})


def prepare_attempt_lane(
    packets: list[dict[str, Any]],
    *,
    lane_index: int,
    attempt_id: str,
    owned_paths: list[str],
) -> Path:
    if not packets:
        raise ValueError("attempt lane requires packets")
    lane = lanes.ensure(lane_index, packet=packets[0])
    manifest = {
        "schema": 1,
        "attempt_id": attempt_id,
        "packet_sha256": packet_sha256(packets),
        "owned_paths": sorted(owned_paths),
        "packets": [
            {
                "basename": packet["basename"],
                "work_ids": sorted(routine["work_id"] for routine in packet["routines"]),
            }
            for packet in packets
        ],
    }
    path = lane / ".factory-v2-attempt.json"
    temporary = lane / f".factory-v2-attempt-{os.getpid()}.tmp"
    temporary.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n")
    os.replace(temporary, path)
    return lane


def validate_attempt_lane(
    packets: list[dict[str, Any]],
    *,
    lane_index: int,
    attempt_id: str,
) -> Path:
    lane = lanes.lane_dir(lane_index)
    path = lane / ".factory-v2-attempt.json"
    try:
        manifest = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("attempt lane manifest is missing or corrupt") from exc
    if (
        manifest.get("attempt_id") != attempt_id
        or manifest.get("packet_sha256") != packet_sha256(packets)
    ):
        raise RuntimeError("attempt lane manifest does not match packet identity")
    return lane


def quarantine_lane(*, lane_index: int, attempt_id: str) -> Path:
    lane = lanes.lane_dir(lane_index)
    destination = V2_STATE / "quarantine" / attempt_id
    if not lane.exists():
        raise RuntimeError("cannot quarantine a missing lane")
    if destination.exists():
        raise RuntimeError(f"quarantine destination exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(lane, destination)
    except OSError:
        shutil.copytree(lane, destination)
        shutil.rmtree(lane)
    return destination


def artifact_records() -> list[dict[str, Any]]:
    if not V2_ARTIFACTS.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for root in sorted(path for path in V2_ARTIFACTS.iterdir() if path.is_dir() and not path.name.startswith(".")):
        if not artifact_exists(root.name):
            continue
        packet = root / "packet.json"
        manifest = root / ".factory-artifact.json"
        try:
            metadata = json.loads(manifest.read_text())
            identity = json.loads(packet.read_text()) if packet.is_file() else None
        except (OSError, json.JSONDecodeError):
            continue
        records.append({
            "artifact_sha256": root.name,
            "identity": identity,
            "metadata": metadata,
            "path": str(root),
        })
    return records

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("prepare")
    reply_parser = sub.add_parser("verify-reply")
    reply_parser.add_argument("--lane", type=int, required=True)
    reply_parser.add_argument("--deadline", type=int, default=900)
    agent_parser = sub.add_parser("verify-agent")
    agent_parser.add_argument("--assignment", type=Path, required=True)
    agent_parser.add_argument("--deadline", type=int, default=900)
    args = parser.parse_args()
    if args.command == "prepare":
        action = json.load(sys.stdin)
        print(json.dumps({"requests": translation_requests(action)}, sort_keys=True))
        return 0
    if args.command == "verify-reply":
        payload = json.load(sys.stdin)
        result = verify_reply(
            payload["attempt"], payload["reply"], lane_index=args.lane,
            deadline_seconds=args.deadline,
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    assignment = json.loads(args.assignment.read_text())
    assignment["lane"] = str(Path.cwd())
    result = verify_agent_lane(assignment, deadline_seconds=args.deadline)
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("outcome") == "productive" else 1


if __name__ == "__main__":
    raise SystemExit(main())
