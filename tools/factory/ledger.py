#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from forgejo import canonical_json, parse_time, sha256

EVENT_BEGIN = "<!-- poketcg-factory-event:v1"
EVENT_END = "-->"
WORK_V2_BEGIN = "<!-- poketcg-port-work:v2"
COHORT_BEGIN = "<!-- poketcg-port-cohort:v1"
AUXILIARY_BEGIN = "<!-- poketcg-factory-work:v1"
CONTROL_BEGIN = "<!-- poketcg-factory-control:v1"
EVENT_RE = re.compile(r"<!--\s*poketcg-factory-event:v1\s*(\{.*?\})\s*-->", re.DOTALL)
MARKER_RE = re.compile(r"<!--\s*([^\s]+)\s*(\{.*?\})\s*-->", re.DOTALL)
COMMAND_RE = re.compile(r"^/factory\s+([a-z-]+)(?:\s+(.*))?$", re.IGNORECASE)
ROUTINE_ID_RE = re.compile(r"^port:v1:[^:\s]+:[^:\s]+$")
COHORT_ID_RE = re.compile(r"^cohort:v1:[0-9a-f]{64}$")
ISSUE_ID_RE = re.compile(r"^issue:v1:[1-9][0-9]*$")

EVENT_KINDS = frozenset({
    "migrated", "run-claim", "run-heartbeat", "run-release", "claim",
    "heartbeat", "attempt-result", "attempt-invalidated", "artifact-missing", "diagnosis", "block",
    "unblock", "integration-start", "integration-phase", "landed",
    "projection-repaired", "capacity-change", "telemetry", "forecast",
    "port-complete", "stale-base",
})
WORK_EVENT_KINDS = EVENT_KINDS - {
    "run-claim", "run-heartbeat", "run-release", "capacity-change", "telemetry",
    "forecast", "port-complete", "integration-start", "integration-phase",
}
CONTROL_EVENT_KINDS = EVENT_KINDS - WORK_EVENT_KINDS


class LedgerError(ValueError):
    pass

@dataclass(frozen=True)
class FactoryEvent:
    event_id: str
    kind: str
    run_id: str
    work_id: str | None
    attempt_id: str | None
    parent_comment_id: int | None
    parent_event_sha256: str | None
    base_revision: str
    intent_sha256: str
    emitted_at: str
    payload: dict[str, Any]

    @staticmethod
    def create(
        *,
        kind: str,
        run_id: str,
        work_id: str | None,
        attempt_id: str | None,
        parent_comment_id: int | None,
        parent_event_sha256: str | None,
        base_revision: str,
        intent_sha256: str,
        emitted_at: str,
        payload: dict[str, Any],
    ) -> FactoryEvent:
        value = {
            "kind": kind,
            "run_id": run_id,
            "work_id": work_id,
            "attempt_id": attempt_id,
            "parent_comment_id": parent_comment_id,
            "parent_event_sha256": parent_event_sha256,
            "base_revision": base_revision,
            "intent_sha256": intent_sha256,
            "emitted_at": emitted_at,
            "payload": payload,
        }
        return FactoryEvent(event_id=sha256(value), **value)

    @property
    def event_sha256(self) -> str:
        return sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "kind": self.kind,
            "run_id": self.run_id,
            "work_id": self.work_id,
            "attempt_id": self.attempt_id,
            "parent_comment_id": self.parent_comment_id,
            "parent_event_sha256": self.parent_event_sha256,
            "base_revision": self.base_revision,
            "intent_sha256": self.intent_sha256,
            "emitted_at": self.emitted_at,
            "payload": self.payload,
        }

    def comment_body(self) -> str:
        return f"{EVENT_BEGIN}\n{canonical_json(self.as_dict())}\n{EVENT_END}\n"


@dataclass(frozen=True)
class EventComment:
    comment_id: int
    created_at: datetime
    author: str
    event: FactoryEvent


@dataclass(frozen=True)
class FactoryCommand:
    comment_id: int
    author: str
    command: str
    argument: str
    created_at: datetime


@dataclass
class WorkView:
    issue_number: int
    work_id: str
    state: str = "ready"
    chain: list[EventComment] = field(default_factory=list)
    ignored: list[str] = field(default_factory=list)
    commands: list[FactoryCommand] = field(default_factory=list)
    claim_comment_id: int | None = None
    claim_expires_at: datetime | None = None
    productive_result_comment_id: int | None = None
    artifact_sha256: str | None = None
    retry_at: datetime | None = None
    base_revision: str | None = None
    intent_sha256: str | None = None
    diagnosis: dict[str, Any] | None = None
    blockers: list[int] = field(default_factory=list)
    quarantined: bool = False
    quarantine_reason: str | None = None
    diagnostic_count: int = 0
    infra_failures: int = 0
    repeat_fingerprints: int = 0
    last_fingerprint: str | None = None
    escalated: bool = False
    invalidated_result_comment_ids: list[int] = field(default_factory=list)

    @property
    def canonical_event(self) -> EventComment | None:
        return self.chain[-1] if self.chain else None

    @property
    def terminal(self) -> bool:
        return self.state in {"done", "excluded"}

    def as_dict(self) -> dict[str, Any]:
        return {
            "issue_number": self.issue_number,
            "work_id": self.work_id,
            "state": self.state,
            "claim_comment_id": self.claim_comment_id,
            "claim_expires_at": self.claim_expires_at.isoformat() if self.claim_expires_at else None,
            "productive_result_comment_id": self.productive_result_comment_id,
            "artifact_sha256": self.artifact_sha256,
            "retry_at": self.retry_at.isoformat() if self.retry_at else None,
            "base_revision": self.base_revision,
            "intent_sha256": self.intent_sha256,
            "blockers": self.blockers,
            "quarantined": self.quarantined,
            "quarantine_reason": self.quarantine_reason,
            "diagnostic_count": self.diagnostic_count,
            "infra_failures": self.infra_failures,
            "repeat_fingerprints": self.repeat_fingerprints,
            "escalated": self.escalated,
            "invalidated_result_comment_ids": self.invalidated_result_comment_ids,
            "canonical_event_id": self.canonical_event.event.event_id if self.canonical_event else None,
            "canonical_comment_id": self.canonical_event.comment_id if self.canonical_event else None,
            "ignored": self.ignored,
        }


@dataclass
class ControlView:
    issue_number: int
    run_id: str | None = None
    claim_comment_id: int | None = None
    claim_expires_at: datetime | None = None
    phase: str | None = None
    chain: list[EventComment] = field(default_factory=list)
    ignored: list[str] = field(default_factory=list)
    completed: bool = False

    @property
    def active(self) -> bool:
        return self.claim_comment_id is not None and self.claim_expires_at is not None

    def as_dict(self) -> dict[str, Any]:
        return {
            "issue_number": self.issue_number,
            "run_id": self.run_id,
            "claim_comment_id": self.claim_comment_id,
            "claim_expires_at": self.claim_expires_at.isoformat() if self.claim_expires_at else None,
            "phase": self.phase,
            "completed": self.completed,
            "canonical_event_id": self.chain[-1].event.event_id if self.chain else None,
            "canonical_comment_id": self.chain[-1].comment_id if self.chain else None,
            "ignored": self.ignored,
        }


def _is_work_id(value: str | None) -> bool:
    return bool(value and (ROUTINE_ID_RE.fullmatch(value) or COHORT_ID_RE.fullmatch(value) or ISSUE_ID_RE.fullmatch(value)))


def _marker(body: str, begin: str) -> dict[str, Any] | None:
    found: list[dict[str, Any]] = []
    for prefix, raw in MARKER_RE.findall(body):
        if f"<!-- {prefix}" != begin:
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"invalid {begin} marker JSON") from exc
        if not isinstance(value, dict):
            raise LedgerError(f"{begin} marker is not an object")
        found.append(value)
    if len(found) > 1:
        raise LedgerError(f"duplicate {begin} markers")
    return found[0] if found else None


def work_marker(issue: dict[str, Any]) -> dict[str, Any] | None:
    body = str(issue.get("body") or "")
    routine = _marker(body, WORK_V2_BEGIN)
    cohort = _marker(body, COHORT_BEGIN)
    auxiliary = _marker(body, AUXILIARY_BEGIN)
    values = [value for value in (routine, cohort, auxiliary) if value is not None]
    if len(values) > 1:
        raise LedgerError(f"issue #{issue.get('number')} has multiple factory work markers")
    if not values:
        return None
    marker = values[0]
    work_id = marker.get("work_id")
    if not isinstance(work_id, str) or not _is_work_id(work_id):
        raise LedgerError(f"issue #{issue.get('number')} has invalid factory work ID")
    if cohort is not None:
        members = marker.get("members")
        if not isinstance(members, list) or not members or members != sorted(set(members)):
            raise LedgerError(f"cohort #{issue.get('number')} has invalid members")
        if not all(isinstance(member, str) and ROUTINE_ID_RE.fullmatch(member) for member in members):
            raise LedgerError(f"cohort #{issue.get('number')} has invalid member work IDs")
        expected = hashlib.sha256("\0".join(members).encode()).hexdigest()
        if work_id != f"cohort:v1:{expected}":
            raise LedgerError(f"cohort #{issue.get('number')} has mismatched membership hash")
    if auxiliary is not None and marker.get("kind") not in {"injected", "incident"}:
        raise LedgerError(f"auxiliary issue #{issue.get('number')} has invalid kind")
    return marker


def control_marker(issue: dict[str, Any]) -> dict[str, Any] | None:
    return _marker(str(issue.get("body") or ""), CONTROL_BEGIN)


def _require_exact_keys(value: dict[str, Any], allowed: set[str], context: str) -> None:
    unknown = set(value) - allowed
    if unknown:
        raise LedgerError(f"{context} has unknown fields: {sorted(unknown)}")


def _require_string(value: dict[str, Any], key: str, *, allow_empty: bool = False) -> str:
    item = value.get(key)
    if not isinstance(item, str) or (not allow_empty and not item):
        raise LedgerError(f"event {key} must be a non-empty string")
    return item


def _require_id(value: Any, context: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or value <= 0:
        raise LedgerError(f"{context} must be a positive integer or null")
    return value


def _validate_payload(kind: str, payload: dict[str, Any]) -> None:
    required: dict[str, set[str]] = {
        "migrated": {"state", "source_revision", "publication_revision", "gate_sha256", "legacy_history_sha256", "landed_at", "exclusion_reason"},
        "run-claim": {"runner_instance", "lease_seconds"},
        "run-heartbeat": {"claim_comment_id", "lease_seconds", "phase"},
        "run-release": {"claim_comment_id", "reason"},
        "claim": {"lease_seconds", "packet_sha256", "model_route", "owned_paths_sha256"},
        "heartbeat": {"claim_comment_id", "lease_seconds", "phase"},
        "attempt-result": {"claim_comment_id", "outcome", "verdict", "artifact_sha256", "next_wake_at"},
        "attempt-invalidated": {"attempt_result_comment_ids", "reason", "evidence_sha256"},
        "artifact-missing": {"attempt_result_comment_id", "artifact_sha256", "reason"},
        "diagnosis": {"failure_scope", "failure_class", "affected_work_ids", "repair", "constraints", "confidence", "next_action"},
        "block": {"reason", "unblock", "dependency_issue_numbers"},
        "unblock": {"block_comment_id", "reason"},
        "integration-start": {"batch_id", "attempt_result_comment_ids", "artifact_sha256s", "expected_remote_revision"},
        "integration-phase": {"batch_id", "phase", "input_sha256", "output_sha256", "source_revision", "publication_revision"},
        "landed": {"batch_id", "attempt_result_comment_id", "source_revision", "publication_revision", "gate_sha256", "progress_sha256"},
        "projection-repaired": {"target_event_id", "labels", "issue_state", "readback_sha256"},
        "capacity-change": {"previous", "current", "reason"},
        "telemetry": {"records"},
        "forecast": {"snapshot_sha256", "p50", "p85", "p95", "confidence"},
        "port-complete": {"remote_revision", "publication_revision", "gate_sha256", "projection_sha256"},
        "stale-base": {"reason", "new_base_revision"},
    }
    allowed = required.get(kind)
    if allowed is None:
        raise LedgerError(f"unknown event kind {kind!r}")
    if kind == "claim" and set(payload) == allowed | {"agent_name", "model_id"}:
        pass
    else:
        _require_exact_keys(payload, allowed, f"{kind} payload")
    if kind in {"run-claim", "claim"}:
        seconds = payload.get("lease_seconds")
        if not isinstance(seconds, int) or not 1 <= seconds <= 7200:
            raise LedgerError(f"{kind} lease_seconds must be 1..7200")
    if kind == "claim" and "agent_name" in payload:
        if payload["agent_name"] is not None and not isinstance(payload["agent_name"], str):
            raise LedgerError("claim agent_name must be string or null")
        if payload["model_id"] is not None and not isinstance(payload["model_id"], str):
            raise LedgerError("claim model_id must be string or null")
        if payload["agent_name"] is None or payload["model_id"] is None:
            raise LedgerError("V2 generator claims require agent_name and model_id")
    if kind in {"run-heartbeat", "heartbeat", "run-release"}:
        _require_id(payload.get("claim_comment_id"), f"{kind}.claim_comment_id")
    if kind == "attempt-result":
        _require_id(payload.get("claim_comment_id"), "attempt-result.claim_comment_id")
        if payload.get("outcome") not in {"productive", "diagnostic", "provider-failure", "infrastructure-failure", "blocked", "stopped"}:
            raise LedgerError("attempt-result has invalid outcome")
        if not isinstance(payload.get("verdict"), dict):
            raise LedgerError("attempt-result verdict must be an object")
        artifact = payload.get("artifact_sha256")
        if payload.get("outcome") == "productive" and (not isinstance(artifact, str) or len(artifact) != 64):
            raise LedgerError("productive attempt-result needs artifact_sha256")
        if payload["verdict"].get("schema") == 2:
            expected_verdict = {"schema", "status", "phase", "failure_class", "scope", "retry_action", "work_ids", "summary", "witness", "phase_seconds", "fingerprint"}
            _require_exact_keys(payload["verdict"], expected_verdict, "VerdictV2")
            if payload["verdict"].get("status") not in {"green", "red"}:
                raise LedgerError("VerdictV2 status must be green or red")
            if not isinstance(payload["verdict"].get("work_ids"), list) or not isinstance(payload["verdict"].get("witness"), dict) or not isinstance(payload["verdict"].get("phase_seconds"), dict):
                raise LedgerError("VerdictV2 has invalid evidence fields")
            if not isinstance(payload["verdict"].get("fingerprint"), str) or not re.fullmatch(r"[0-9a-f]{64}", payload["verdict"]["fingerprint"]):
                raise LedgerError("VerdictV2 fingerprint must be a SHA-256")
    if kind == "attempt-invalidated":
        values = payload.get("attempt_result_comment_ids")
        if not isinstance(values, list) or not values or values != sorted(set(values)) or not all(isinstance(value, int) and value > 0 for value in values):
            raise LedgerError("attempt-invalidated IDs must be a non-empty sorted unique list")
        _require_string(payload, "reason")
        evidence = payload.get("evidence_sha256")
        if not isinstance(evidence, str) or not re.fullmatch(r"[0-9a-f]{64}", evidence):
            raise LedgerError("attempt-invalidated evidence_sha256 must be a SHA-256")
    if kind == "diagnosis":
        if payload.get("failure_scope") not in {"routine", "shared-harness", "dependency", "infrastructure"}:
            raise LedgerError("diagnosis has invalid failure scope")
        confidence = payload.get("confidence")
        if not isinstance(confidence, (float, int)) or not 0 <= confidence <= 1:
            raise LedgerError("diagnosis confidence must be 0..1")
        affected = payload.get("affected_work_ids")
        if not isinstance(affected, list) or affected != sorted(set(affected)) or not all(_is_work_id(row) for row in affected):
            raise LedgerError("diagnosis affected_work_ids must be sorted factory IDs")
    if kind == "block":
        dependencies = payload.get("dependency_issue_numbers")
        if not isinstance(dependencies, list) or dependencies != sorted(set(dependencies)) or not all(isinstance(value, int) and value > 0 for value in dependencies):
            raise LedgerError("block dependency_issue_numbers must be sorted issue numbers")
    if kind == "integration-start":
        values = payload.get("attempt_result_comment_ids")
        if not isinstance(values, list) or values != sorted(set(values)) or not all(isinstance(value, int) and value > 0 for value in values):
            raise LedgerError("integration attempt-result IDs must be sorted")
    if kind == "landed":
        _require_id(payload.get("attempt_result_comment_id"), "landed.attempt_result_comment_id")
    if kind == "projection-repaired" and payload.get("issue_state") not in {"open", "closed"}:
        raise LedgerError("projection-repaired has invalid issue state")


def parse_event_comment(comment: dict[str, Any]) -> EventComment | None:
    body = str(comment.get("body") or "")
    matches = EVENT_RE.findall(body)
    if not matches:
        return None
    if len(matches) != 1:
        raise LedgerError(f"comment #{comment.get('id')} has duplicate event markers")
    try:
        value = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise LedgerError(f"comment #{comment.get('id')} has invalid event JSON") from exc
    if not isinstance(value, dict):
        raise LedgerError("factory event is not an object")
    fields = {
        "event_id", "kind", "run_id", "work_id", "attempt_id", "parent_comment_id",
        "parent_event_sha256", "base_revision", "intent_sha256", "emitted_at", "payload",
    }
    _require_exact_keys(value, fields, "factory event")
    event_id = _require_string(value, "event_id")
    kind = _require_string(value, "kind")
    if kind not in EVENT_KINDS:
        raise LedgerError(f"unknown factory event kind {kind!r}")
    work_id = value.get("work_id")
    if work_id is not None and not _is_work_id(work_id):
        raise LedgerError("factory event has invalid work_id")
    if kind in WORK_EVENT_KINDS and work_id is None:
        raise LedgerError(f"work event {kind} has null work_id")
    if kind in CONTROL_EVENT_KINDS and work_id is not None:
        raise LedgerError(f"control event {kind} has work_id")
    payload = value.get("payload")
    if not isinstance(payload, dict):
        raise LedgerError("factory event payload is not an object")
    _validate_payload(kind, payload)
    event = FactoryEvent(
        event_id=event_id,
        kind=kind,
        run_id=_require_string(value, "run_id"),
        work_id=work_id,
        attempt_id=value.get("attempt_id") if isinstance(value.get("attempt_id"), str) else None,
        parent_comment_id=_require_id(value.get("parent_comment_id"), "parent_comment_id"),
        parent_event_sha256=value.get("parent_event_sha256") if isinstance(value.get("parent_event_sha256"), str) else None,
        base_revision=_require_string(value, "base_revision"),
        intent_sha256=_require_string(value, "intent_sha256"),
        emitted_at=_require_string(value, "emitted_at"),
        payload=payload,
    )
    expected = sha256({key: item for key, item in event.as_dict().items() if key != "event_id"})
    if event.event_id != expected:
        raise LedgerError(f"comment #{comment.get('id')} event ID does not match payload")
    created = parse_time(str(comment.get("created_at") or ""))
    if created is None:
        raise LedgerError(f"comment #{comment.get('id')} has invalid created_at")
    identifier = comment.get("id")
    if not isinstance(identifier, int) or identifier <= 0:
        raise LedgerError("factory event comment has invalid ID")
    return EventComment(
        comment_id=identifier,
        created_at=created,
        author=str(comment.get("author") or ""),
        event=event,
    )


def command_from_comment(comment: dict[str, Any], *, authorized_authors: set[str]) -> FactoryCommand | None:
    author = str(comment.get("author") or "")
    if author not in authorized_authors:
        return None
    match = COMMAND_RE.fullmatch(str(comment.get("body") or "").strip())
    if not match:
        return None
    command, argument = match.group(1).lower(), (match.group(2) or "").strip()
    allowed = {"pause", "resume", "priority", "retry", "help", "depend", "undepend", "inject"}
    if command not in allowed:
        raise LedgerError(f"unknown authorized factory command {command!r}")
    created = parse_time(str(comment.get("created_at") or ""))
    identifier = comment.get("id")
    if created is None or not isinstance(identifier, int) or identifier <= 0:
        raise LedgerError("factory command has invalid comment metadata")
    return FactoryCommand(identifier, author, command, argument, created)


def intent_sha256(issue: dict[str, Any], dependencies: Iterable[dict[str, Any]], commands: Iterable[FactoryCommand]) -> str:
    marker = work_marker(issue)
    if marker is None:
        raise LedgerError(f"issue #{issue.get('number')} has no factory work marker")
    generated = str(issue.get("body") or "")
    begin = "<!-- poketcg-port-generated:begin -->"
    end = "<!-- poketcg-port-generated:end -->"
    generated_block = ""
    if begin in generated and end in generated:
        start = generated.index(begin)
        finish = generated.index(end, start) + len(end)
        generated_block = generated[start:finish]
    command_values = [
        {"id": command.comment_id, "command": command.command, "argument": command.argument}
        for command in sorted(commands, key=lambda command: command.comment_id)
        if command.command in {"pause", "resume", "retry", "help", "depend", "undepend", "inject"}
    ]
    return sha256({
        "marker": marker,
        "generated": generated_block,
        "dependencies": sorted(int(row["number"]) for row in dependencies),
        "closed": issue.get("state") == "closed",
        "commands": command_values,
    })


def _canonical_chain(
    comments: Iterable[dict[str, Any]],
    *,
    work_id: str | None,
    allowed_kinds: set[str],
) -> tuple[list[EventComment], list[str]]:
    valid: list[EventComment] = []
    ignored: list[str] = []
    for comment in comments:
        try:
            parsed = parse_event_comment(comment)
        except LedgerError as exc:
            ignored.append(f"comment #{comment.get('id')}: {exc}")
            continue
        if parsed is None:
            continue
        if parsed.event.work_id != work_id or parsed.event.kind not in allowed_kinds:
            continue
        valid.append(parsed)
    children: dict[int | None, list[EventComment]] = {}
    for item in valid:
        children.setdefault(item.event.parent_comment_id, []).append(item)
    for values in children.values():
        values.sort(key=lambda item: item.comment_id)
    chain: list[EventComment] = []
    parent_id: int | None = None
    parent_hash: str | None = None
    while candidates := children.get(parent_id):
        selected: EventComment | None = None
        for candidate in candidates:
            expected_hash = candidate.event.parent_event_sha256
            if parent_id is None:
                if expected_hash is None:
                    selected = candidate
                    break
            elif expected_hash == parent_hash:
                selected = candidate
                break
            else:
                ignored.append(f"comment #{candidate.comment_id}: parent hash mismatch")
        if selected is None:
            break
        chain.append(selected)
        for losing in candidates:
            if losing.comment_id != selected.comment_id:
                ignored.append(f"comment #{losing.comment_id}: losing concurrent branch")
        parent_id = selected.comment_id
        parent_hash = selected.event.event_sha256
    reachable = {item.comment_id for item in chain}
    for item in valid:
        if item.comment_id not in reachable and not any(message.startswith(f"comment #{item.comment_id}:") for message in ignored):
            ignored.append(f"comment #{item.comment_id}: orphaned event branch")
    return chain, ignored


def _lease_expiry(comment: EventComment, seconds: int) -> datetime:
    return comment.created_at + timedelta(seconds=seconds)


def _active_claim(chain: list[EventComment], now: datetime) -> tuple[int | None, datetime | None]:
    claim_id: int | None = None
    expiry: datetime | None = None
    for item in chain:
        event = item.event
        if event.kind in {"claim", "run-claim"}:
            claim_id = item.comment_id
            expiry = _lease_expiry(item, int(event.payload["lease_seconds"]))
        elif event.kind in {"heartbeat", "run-heartbeat"} and claim_id == event.payload["claim_comment_id"]:
            expiry = _lease_expiry(item, int(event.payload["lease_seconds"]))
        elif event.kind in {"attempt-result", "run-release", "landed"}:
            claim_id = None
            expiry = None
    if expiry is not None and expiry <= now:
        return None, None
    return claim_id, expiry


def _verdict_fingerprint(payload: dict[str, Any]) -> str | None:
    verdict = payload.get("verdict")
    if not isinstance(verdict, dict):
        return None
    fingerprint = verdict.get("fingerprint")
    return fingerprint if isinstance(fingerprint, str) and fingerprint else None


def reduce_work(
    issue: dict[str, Any],
    comments: Iterable[dict[str, Any]],
    dependencies: Iterable[dict[str, Any]],
    *,
    now: datetime,
    authorized_authors: set[str],
    artifact_exists: Callable[[str], bool] | None = None,
) -> WorkView:
    marker = work_marker(issue)
    if marker is None:
        raise LedgerError(f"issue #{issue.get('number')} is not factory managed")
    work_id = str(marker["work_id"])
    commands: list[FactoryCommand] = []
    for comment in comments:
        command = command_from_comment(comment, authorized_authors=authorized_authors)
        if command is not None:
            commands.append(command)
    commands.sort(key=lambda command: command.comment_id)
    dependencies = list(dependencies)
    current_intent = intent_sha256(issue, dependencies, commands)
    chain, ignored = _canonical_chain(comments, work_id=work_id, allowed_kinds=set(WORK_EVENT_KINDS))
    result_by_comment = {
        item.comment_id: item
        for item in chain
        if item.event.kind == "attempt-result"
    }
    invalidated: set[int] = set()
    for item in chain:
        if item.event.kind != "attempt-invalidated":
            continue
        for target_id in item.event.payload["attempt_result_comment_ids"]:
            target = result_by_comment.get(target_id)
            if target is None:
                raise LedgerError(f"attempt-invalidated targets non-canonical result #{target_id}")
            if target.event.payload["outcome"] != "diagnostic" or target.event.payload["artifact_sha256"] is not None:
                raise LedgerError(f"attempt-invalidated target #{target_id} is not a diagnostic without artifact")
            if any(
                descendant.event.kind == "landed"
                and descendant.event.payload["attempt_result_comment_id"] == target_id
                for descendant in chain
            ):
                raise LedgerError(f"attempt-invalidated target #{target_id} already landed")
            invalidated.add(target_id)
    view = WorkView(issue_number=int(issue["number"]), work_id=work_id, chain=chain, ignored=ignored, commands=commands, blockers=sorted(int(row["number"]) for row in dependencies), invalidated_result_comment_ids=sorted(invalidated))
    latest_pause = max((command.comment_id for command in commands if command.command == "pause"), default=0)
    latest_resume = max((command.comment_id for command in commands if command.command == "resume"), default=0)
    pause_active = latest_pause > latest_resume
    for item in chain:
        event = item.event
        view.base_revision = event.base_revision
        view.intent_sha256 = event.intent_sha256
        if event.kind == "migrated":
            state = event.payload["state"]
            if state in {"done", "complete"}:
                view.state = "done"
            elif state == "excluded":
                view.state = "excluded"
            elif state == "blocked":
                view.state = "blocked"
            elif state in {"recovery", "failing"}:
                view.state = "recovery"
        elif event.kind == "attempt-result" and item.comment_id not in invalidated:
            outcome = event.payload["outcome"]
            if outcome == "productive":
                view.state = "integrating"
                view.productive_result_comment_id = item.comment_id
                view.artifact_sha256 = str(event.payload["artifact_sha256"])
                view.diagnostic_count = 0
                view.repeat_fingerprints = 0
                view.last_fingerprint = None
                if artifact_exists is not None and not artifact_exists(view.artifact_sha256):
                    view.state = "recovery"
                    view.quarantined = True
                    view.quarantine_reason = "accepted artifact is missing"
            elif outcome == "provider-failure":
                view.state = "recovery"
                view.retry_at = parse_time(event.payload.get("next_wake_at"))
            elif outcome in {"diagnostic", "infrastructure-failure", "stopped"}:
                view.state = "recovery"
                if outcome == "diagnostic":
                    view.diagnostic_count += 1
                    fingerprint = _verdict_fingerprint(event.payload)
                    if fingerprint is not None and fingerprint == view.last_fingerprint:
                        view.repeat_fingerprints += 1
                    else:
                        view.repeat_fingerprints = 0
                    view.last_fingerprint = fingerprint
                else:
                    view.infra_failures += 1
            elif outcome == "blocked":
                view.state = "blocked"
        elif event.kind == "artifact-missing":
            view.state = "recovery"
            view.artifact_sha256 = None
        elif event.kind == "block":
            view.state = "blocked"
            view.escalated = event.payload.get("reason") == "recovery-exhausted"
        elif event.kind == "unblock":
            view.state = "recovery" if view.productive_result_comment_id is None else "integrating"
            view.escalated = False
            view.diagnostic_count = 0
            view.repeat_fingerprints = 0
            view.last_fingerprint = None
        elif event.kind == "diagnosis":
            view.diagnosis = dict(event.payload)
        elif event.kind == "integration-start":
            view.state = "integrating"
        elif event.kind == "landed":
            view.state = "done"
            view.productive_result_comment_id = None
    claim_id, expires = _active_claim(chain, now)
    view.claim_comment_id = claim_id
    view.claim_expires_at = expires
    if view.terminal:
        return view
    if view.intent_sha256 is not None and view.intent_sha256 != current_intent:
        view.state = "recovery"
        view.quarantined = True
        view.quarantine_reason = "canonical event intent differs from current issue intent"
        return view
    if pause_active:
        view.state = "paused"
        return view
    if claim_id is not None:
        view.state = "running"
        return view
    if view.blockers:
        view.state = "blocked"
    if view.retry_at is not None and view.retry_at > now:
        view.state = "recovery"
    return view


def reduce_control(
    issue: dict[str, Any],
    comments: Iterable[dict[str, Any]],
    *,
    now: datetime,
) -> ControlView:
    marker = control_marker(issue)
    if marker is None:
        raise LedgerError(f"issue #{issue.get('number')} is not the factory control issue")
    repository = marker.get("repository")
    if not isinstance(repository, str) or not repository:
        raise LedgerError("factory control marker has no repository")
    chain, ignored = _canonical_chain(comments, work_id=None, allowed_kinds=set(CONTROL_EVENT_KINDS))
    view = ControlView(issue_number=int(issue["number"]), chain=chain, ignored=ignored)
    for item in chain:
        event = item.event
        if event.kind == "run-claim":
            view.run_id = event.run_id
            view.claim_comment_id = item.comment_id
            view.claim_expires_at = _lease_expiry(item, int(event.payload["lease_seconds"]))
            view.phase = "running"
            view.completed = False
        elif event.kind == "run-heartbeat" and view.claim_comment_id == event.payload["claim_comment_id"]:
            view.claim_expires_at = _lease_expiry(item, int(event.payload["lease_seconds"]))
            view.phase = str(event.payload["phase"])
        elif event.kind == "integration-start":
            view.phase = "integration"
        elif event.kind == "integration-phase":
            view.phase = str(event.payload["phase"])
        elif event.kind == "port-complete":
            view.completed = True
            view.phase = "complete"
        elif event.kind == "run-release" and view.claim_comment_id == event.payload["claim_comment_id"]:
            view.claim_comment_id = None
            view.claim_expires_at = None
            view.phase = str(event.payload["reason"])
    if view.claim_expires_at is not None and view.claim_expires_at <= now:
        view.claim_comment_id = None
        view.claim_expires_at = None
        if not view.completed:
            view.phase = "expired"
    return view


def elect_lease(
    comments: Iterable[dict[str, Any]],
    *,
    work_id: str | None,
    now: datetime,
    control: bool = False,
) -> EventComment | None:
    allowed = set(CONTROL_EVENT_KINDS) if control else set(WORK_EVENT_KINDS)
    chain, _ignored = _canonical_chain(comments, work_id=work_id, allowed_kinds=allowed)
    claim_id, _expires = _active_claim(chain, now)
    if claim_id is None:
        return None
    return next(item for item in chain if item.comment_id == claim_id)
