#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import common
import lanes
import verify

V2_ARTIFACTS = common.FACTORY / "artifacts"
V2_STATE = common.FACTORY / "v2"


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def packet_sha256(packets: list[dict[str, Any]]) -> str:
    return _digest({"packets": packets})


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


def stage_bundle(packet: dict[str, Any], lane: Path) -> dict[str, Any]:
    _extracted, hashes = verify._validate_bundle_inputs(packet, lane)
    artifact_key = str(packet.get("artifact_key") or packet["attempt_id"])
    output = lane / ".factory-output" / artifact_key
    if output.exists():
        manifest = output / ".factory-artifact.json"
        if manifest.is_file():
            metadata = json.loads(manifest.read_text())
            bundle_sha256 = metadata.get("bundle_sha256")
            if isinstance(bundle_sha256, str) and common.payload_tree_digest(output) == bundle_sha256:
                return {"artifact_dir": str(output), "bundle_sha256": bundle_sha256}
        raise RuntimeError(f"immutable staged bundle already exists: {output}")
    output.mkdir(parents=True)
    for relative in sorted(hashes):
        source = lane / relative
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    (output / "packet.json").write_text(
        json.dumps(common.packet_identity(packet), sort_keys=True, indent=2) + "\n"
    )
    bundle_sha256 = common.payload_tree_digest(output)
    (output / ".factory-artifact.json").write_text(
        json.dumps({"bundle_sha256": bundle_sha256, "hashes": hashes}, sort_keys=True, indent=2) + "\n"
    )
    return {"artifact_dir": str(output), "bundle_sha256": bundle_sha256}


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
    return metadata.get("bundle_sha256") == bundle_sha256 and common.payload_tree_digest(root) == bundle_sha256


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
    try:
        shutil.copytree(source, temporary)
        if common.payload_tree_digest(temporary) != bundle_sha256:
            raise RuntimeError("copied artifact payload hash mismatch")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"artifact_sha256": bundle_sha256, "artifact_dir": str(destination)}


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
    temporary = lane / f".factory-v2-attempt-{os.getpid()}.tmp"
    temporary.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n")
    os.replace(temporary, lane / ".factory-v2-attempt.json")
    return lane


def validate_attempt_lane(
    packets: list[dict[str, Any]],
    *,
    lane_index: int,
    attempt_id: str,
) -> Path:
    lane = lanes.lane_dir(lane_index)
    try:
        manifest = json.loads((lane / ".factory-v2-attempt.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("attempt lane manifest is missing or corrupt") from exc
    if manifest.get("attempt_id") != attempt_id or manifest.get("packet_sha256") != packet_sha256(packets):
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


def _verify_worker(packet: dict[str, Any], lane: Path, translation: dict[str, Any], deadline: float) -> dict[str, Any]:
    payload = json.dumps({
        "packet": packet,
        "lane": str(lane),
        "translation": translation,
        "statics_baseline": None,
        "rounds": 0,
        "deadline": deadline,
        "wave_id": f"v2-{packet['attempt_id']}",
        "packet_id": packet["attempt_id"],
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
        return {"status": "infra-error", "phase": "verify-worker", "detail": completed.stdout + completed.stderr}
    response = json.loads(completed.stdout)
    if not isinstance(response, dict) or not isinstance(response.get("result"), dict):
        return {"status": "infra-error", "phase": "verify-worker", "detail": completed.stdout}
    return response["result"]


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
    work_ids = sorted(str(routine["work_id"]) for routine in packet["routines"])
    try:
        lane = validate_attempt_lane([packet], lane_index=lane_index, attempt_id=attempt_id)
        raw = _verify_worker(packet, lane, translation_from_reply(packet, reply), time.monotonic() + deadline_seconds)
    except (OSError, RuntimeError, TypeError, ValueError, json.JSONDecodeError, common.PhaseTimeout, common.WaveDeadlineExpired) as exc:
        raw = {"status": "infra-error", "phase": "verify-attempt", "detail": f"{type(exc).__name__}: {exc}"}
    normalized = verify.verdict_v1(raw, work_ids)
    if normalized["status"] != "green":
        return {"outcome": "diagnostic", "verdict": normalized, "detail": str(raw.get("detail") or "")}
    artifact = store_artifact(stage_bundle(packet, lanes.lane_dir(lane_index)))
    return {"outcome": "productive", "verdict": normalized, **artifact}


def verify_lane_attempt(
    packet: dict[str, Any],
    *,
    lane_index: int,
    deadline_seconds: int,
) -> dict[str, Any]:
    work_ids = sorted(str(routine["work_id"]) for routine in packet["routines"])
    try:
        raw = verify.verify_packet(packet, lanes.lane_dir(lane_index), True, deadline=time.monotonic() + deadline_seconds)
    except (OSError, RuntimeError, TypeError, ValueError, common.PhaseTimeout, common.WaveDeadlineExpired) as exc:
        raw = {"status": "infra-error", "phase": "verify-lane", "detail": f"{type(exc).__name__}: {exc}"}
    normalized = verify.verdict_v1(raw, work_ids)
    if normalized["status"] != "green":
        return {"outcome": "diagnostic", "verdict": normalized, "detail": str(raw.get("detail") or "")}
    artifact = store_artifact(stage_bundle(packet, lanes.lane_dir(lane_index)))
    return {"outcome": "productive", "verdict": normalized, **artifact}


def verify_lane_packets(
    packets: list[dict[str, Any]],
    *,
    lane_index: int,
    deadline_seconds: int,
) -> dict[str, Any]:
    outcomes = [
        verify_lane_attempt(packet, lane_index=lane_index, deadline_seconds=deadline_seconds)
        for packet in packets
    ]
    failures = [outcome for outcome in outcomes if outcome.get("outcome") != "productive"]
    if failures:
        return {"outcome": "diagnostic", "verdict": failures[0]["verdict"], "detail": json.dumps(failures, sort_keys=True)}
    artifact = store_group_artifact(outcomes)
    return {
        "outcome": "productive",
        "verdict": {
            "status": "green",
            "phase": "group",
            "failure_class": None,
            "scope": "routine",
            "retry_action": "accept",
            "work_ids": sorted(routine["work_id"] for packet in packets for routine in packet["routines"]),
            "summary": "green",
            "evidence": {},
            "fingerprint": _digest({"packets": [packet["attempt_id"] for packet in packets]}),
        },
        **artifact,
    }


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
        records.append({"artifact_sha256": root.name, "identity": identity, "metadata": metadata, "path": str(root)})
    return records
