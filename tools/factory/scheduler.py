#!/usr/bin/env python3
"""Bounded, transactional scheduling ticks for the port factory."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Any

import common
import state

ATTEMPT_NAMESPACE = uuid.UUID("6753bc9f-a650-56b3-9be8-9047ae543b79")
RECOVERY_MODELS = {
    0: "default",
    1: "default",
    2: "slow",
    3: "agent",
    4: "competing-agent",
}
ATTEMPT_OUTCOMES = frozenset({
    "productive", "salvage", "diagnostic", "blocked", "provider-failure",
    "infrastructure-failure", "external-stop",
})

WORK_OUTCOMES = frozenset({
    "unblocked", "diagnostic", "blocked", "provider-failure",
    "infrastructure-failure", "external-stop",
})

def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def _metadata(connection: sqlite3.Connection, key: str, default: str = "") -> str:
    row = connection.execute(
        "SELECT value FROM metadata WHERE key = ?", (key,),
    ).fetchone()
    return row[0] if row else default


def _basename(source: str | None, snapshot: dict | None = None) -> str:
    if snapshot and isinstance(snapshot.get("basename"), str):
        return snapshot["basename"]
    return Path(source).stem if source else "unknown"


def _owned_paths(basename: str) -> list[str]:
    return common.port_owned_paths(basename)


def _work_rows_for_attempt(
    connection: sqlite3.Connection,
    attempt_id: str,
) -> list[dict[str, Any]]:
    rows = connection.execute(
        """SELECT work_id, source, name, line, size, eligibility, recovery_tier,
                  diagnostic_count, repeated_fingerprint_count,
                  last_failure_fingerprint, not_before, stop_kind
           FROM work WHERE current_attempt_id = ? ORDER BY work_id""",
        (attempt_id,),
    ).fetchall()
    keys = (
        "work_id", "source", "name", "line", "size", "eligibility",
        "recovery_tier", "diagnostic_count", "repeated_fingerprint_count",
        "last_failure_fingerprint", "not_before", "stop_kind",
    )
    return [dict(zip(keys, row, strict=True)) for row in rows]


def _action_descriptor(connection: sqlite3.Connection, action_id: str) -> dict[str, Any]:
    row = connection.execute(
        """SELECT kind, phase, status, input_digest, lease_owner, lease_token,
                  lease_deadline, not_before, created_at, updated_at
           FROM action WHERE action_id = ?""",
        (action_id,),
    ).fetchone()
    if row is None:
        raise KeyError(action_id)
    keys = (
        "kind", "phase", "status", "input_digest", "lease_owner", "lease_token",
        "lease_deadline", "not_before", "created_at", "updated_at",
    )
    descriptor = {"action_id": action_id, **dict(zip(keys, row, strict=True))}
    attempts = []
    for attempt_row in connection.execute(
        """SELECT a.attempt_id, aa.role, a.state, a.generation, a.model,
                  a.snapshot_json, a.owned_paths_json, a.packet_sha256,
                  a.bundle_sha256, a.not_before, a.parent_attempt_id
           FROM action_attempt aa
           JOIN attempt a ON a.attempt_id = aa.attempt_id
           WHERE aa.action_id = ? ORDER BY a.attempt_id""",
        (action_id,),
    ):
        (
            attempt_id, role, attempt_state, generation, model, snapshot_json,
            owned_paths_json, packet_sha256, bundle_sha256, not_before,
            parent_attempt_id,
        ) = attempt_row
        work = _work_rows_for_attempt(connection, attempt_id)
        tier = max((item["recovery_tier"] for item in work), default=generation)
        failures = [
            {
                "phase": failure[0],
                "status": failure[1],
                "failure_class": failure[2],
                "fingerprint": failure[3],
                "detail": failure[4],
                "model": failure[5],
                "observed_at": failure[6],
            }
            for failure in connection.execute(
                """WITH RECURSIVE ancestry(attempt_id) AS (
                       SELECT ?
                       UNION ALL
                       SELECT a.parent_attempt_id
                       FROM attempt a JOIN ancestry x
                         ON a.attempt_id = x.attempt_id
                       WHERE a.parent_attempt_id IS NOT NULL
                   )
                   SELECT phase, status, failure_class, fingerprint, detail,
                          model, observed_at
                   FROM failure WHERE attempt_id IN (SELECT attempt_id FROM ancestry)
                   ORDER BY observed_at, failure_id""",
                (attempt_id,),
            )
        ]
        attempts.append({
            "attempt_id": attempt_id,
            "role": role,
            "state": attempt_state,
            "generation": generation,
            "parent_attempt_id": parent_attempt_id,
            "recovery_tier": tier,
            "model": model or RECOVERY_MODELS.get(min(tier, 4), "default"),
            "snapshot": json.loads(snapshot_json),
            "owned_paths": json.loads(owned_paths_json),
            "packet_sha256": packet_sha256,
            "bundle_sha256": bundle_sha256,
            "not_before": not_before,
            "work": work,
            "failures": failures,
        })
    descriptor["attempts"] = attempts
    direct_work = []
    for work_id, role in connection.execute(
        """SELECT work_id, role FROM action_work
           WHERE action_id = ? ORDER BY work_id""",
        (action_id,),
    ):
        row = connection.execute(
            """SELECT source, name, line, size, canonical_state, eligibility,
                      recovery_tier, diagnostic_count, repeated_fingerprint_count,
                      last_failure_fingerprint, not_before, stop_kind
               FROM work WHERE work_id = ?""",
            (work_id,),
        ).fetchone()
        keys = (
            "source", "name", "line", "size", "canonical_state", "eligibility",
            "recovery_tier", "diagnostic_count", "repeated_fingerprint_count",
            "last_failure_fingerprint", "not_before", "stop_kind",
        )
        blockers = [
            {
                "kind": blocker[0],
                "blocked_on_work_id": blocker[1],
                "reason": blocker[2],
                "unblock": blocker[3],
                "source": blocker[4],
            }
            for blocker in connection.execute(
                """SELECT kind, blocked_on_work_id, reason, unblock, source
                   FROM blocker WHERE work_id = ? AND active = 1
                   ORDER BY kind, blocked_on_work_id, source""",
                (work_id,),
            )
        ]
        direct_work.append({
            "work_id": work_id,
            "role": role,
            **dict(zip(keys, row, strict=True)),
            "blockers": blockers,
        })
    descriptor["work"] = direct_work
    return descriptor


def action_descriptor(
    connection: sqlite3.Connection,
    action_id: str,
) -> dict[str, Any]:
    return _action_descriptor(connection, action_id)




def snapshot(connection: sqlite3.Connection, *, now: int | None = None) -> dict[str, Any]:
    now = int(time.time()) if now is None else now
    eligibility = dict(connection.execute(
        "SELECT eligibility, COUNT(*) FROM work GROUP BY eligibility ORDER BY eligibility"
    ))
    actions = dict(connection.execute(
        "SELECT status, COUNT(*) FROM action GROUP BY status ORDER BY status"
    ))
    runnable_fresh = connection.execute(
        """SELECT COUNT(*) FROM work
           WHERE eligibility = 'fresh-ready' AND current_attempt_id IS NULL
             AND not_before <= ?""",
        (now,),
    ).fetchone()[0]
    runnable_recovery = connection.execute(
        """SELECT COUNT(DISTINCT a.attempt_id)
           FROM attempt a JOIN work w ON w.current_attempt_id = a.attempt_id
           WHERE w.eligibility = 'retry-ready' AND w.not_before <= ?
             AND a.not_before <= ? AND a.owner_action_id IS NULL
             AND a.identity_valid = 1
             AND a.state IN ('pending','retry-ready','recovering','repair','failed','stopped')""",
        (now, now),
    ).fetchone()[0]
    return {
        "schema": state.SCHEMA_VERSION,
        "now": now,
        "eligibility": eligibility,
        "actions": actions,
        "runnable": {"fresh": runnable_fresh, "recovery": runnable_recovery},
        "source_digest": _metadata(connection, "source_digest"),
        "source_revision": _metadata(connection, "source_revision"),
    }


def _action_members_valid(connection: sqlite3.Connection, action_id: str) -> bool:
    attempts = connection.execute(
        """SELECT a.attempt_id, a.owner_action_id
           FROM action_attempt aa JOIN attempt a ON a.attempt_id = aa.attempt_id
           WHERE aa.action_id = ?""",
        (action_id,),
    ).fetchall()
    if any(owner not in {None, action_id} for _, owner in attempts):
        return False
    for attempt_id, _ in attempts:
        count = connection.execute(
            """SELECT COUNT(*) FROM action_work aw
               JOIN work w ON w.work_id = aw.work_id
               WHERE aw.action_id = ? AND w.current_attempt_id = ?""",
            (action_id, attempt_id),
        ).fetchone()[0]
        expected = connection.execute(
            "SELECT COUNT(*) FROM attempt_work WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()[0]
        if count != expected:
            return False
    return True


def _existing_action(connection: sqlite3.Connection, now: int) -> dict[str, Any] | None:
    rows = connection.execute(
        """SELECT action_id FROM action
           WHERE recoverable = 1 AND status IN ('planned','recovering','expired')
             AND not_before <= ? ORDER BY created_at, action_id""",
        (now,),
    ).fetchall()
    for action_id, in rows:
        if _action_members_valid(connection, action_id):
            return _action_descriptor(connection, action_id)
        connection.execute(
            """UPDATE action SET phase = 'abandoned', status = 'abandoned',
               result_json = ?, updated_at = ? WHERE action_id = ?""",
            (json.dumps({"reason": "action-membership-drift"}, sort_keys=True), now, action_id),
        )
        connection.execute(
            "UPDATE attempt SET owner_action_id = NULL WHERE owner_action_id = ?",
            (action_id,),
        )
    return None


def _fresh_groups(
    connection: sqlite3.Connection,
    *,
    now: int,
    max_routines: int,
    max_bytes: int,
) -> list[list[dict[str, Any]]]:
    rows = connection.execute(
        """SELECT work_id, source, name, line, size, recovery_tier,
                  diagnostic_count, repeated_fingerprint_count,
                  last_failure_fingerprint, not_before
           FROM work WHERE eligibility = 'fresh-ready'
             AND current_attempt_id IS NULL AND not_before <= ?
           ORDER BY source, line, work_id""",
        (now,),
    ).fetchall()
    keys = (
        "work_id", "source", "name", "line", "size", "recovery_tier",
        "diagnostic_count", "repeated_fingerprint_count",
        "last_failure_fingerprint", "not_before",
    )
    by_basename: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        work = dict(zip(keys, row, strict=True))
        by_basename[_basename(work["source"])].append(work)
    groups = []
    for basename in sorted(by_basename):
        chunk = []
        size = 0
        for work in by_basename[basename]:
            if chunk and (len(chunk) >= max_routines or size + work["size"] > max_bytes):
                groups.append(chunk)
                chunk = []
                size = 0
            chunk.append(work)
            size += work["size"]
        if chunk:
            groups.append(chunk)
    return groups


def _recovery_candidates(
    connection: sqlite3.Connection,
    *,
    now: int,
) -> list[dict[str, Any]]:
    rows = connection.execute(
        """SELECT DISTINCT a.attempt_id, a.state, a.generation, a.not_before,
                  a.updated_at, a.snapshot_json
           FROM attempt a JOIN work w ON w.current_attempt_id = a.attempt_id
           WHERE w.eligibility = 'retry-ready' AND w.not_before <= ?
             AND a.not_before <= ? AND a.owner_action_id IS NULL
             AND a.identity_valid = 1
             AND a.state IN ('pending','retry-ready','recovering','repair','failed','stopped')
           ORDER BY a.not_before, a.updated_at, a.attempt_id""",
        (now, now),
    ).fetchall()
    candidates = []
    for attempt_id, attempt_state, generation, not_before, updated_at, snapshot_json in rows:
        work = _work_rows_for_attempt(connection, attempt_id)
        if not work:
            continue
        packet = json.loads(snapshot_json)
        candidates.append({
            "attempt_id": attempt_id,
            "state": attempt_state,
            "generation": generation,
            "not_before": not_before,
            "updated_at": updated_at,
            "basename": _basename(work[0]["source"], packet),
            "work": work,
        })
    return candidates


def _integration_candidates(
    connection: sqlite3.Connection,
    *,
    now: int,
    limit: int,
) -> list[dict[str, Any]]:
    rows = connection.execute(
        """SELECT DISTINCT a.attempt_id, a.updated_at, a.snapshot_json
           FROM attempt a JOIN work w ON w.current_attempt_id = a.attempt_id
           WHERE w.eligibility = 'green-integrating'
             AND w.not_before <= ? AND a.not_before <= ?
             AND a.owner_action_id IS NULL AND a.identity_valid = 1
             AND a.state IN ('green','integrating')
           ORDER BY a.updated_at, a.attempt_id""",
        (now, now),
    ).fetchall()
    selected = []
    basenames = set()
    for attempt_id, updated_at, snapshot_json in rows:
        work = _work_rows_for_attempt(connection, attempt_id)
        if not work:
            continue
        basename = _basename(work[0]["source"], json.loads(snapshot_json))
        if basename in basenames:
            continue
        basenames.add(basename)
        selected.append({
            "attempt_id": attempt_id,
            "updated_at": updated_at,
            "basename": basename,
            "work": work,
        })
        if len(selected) >= limit:
            break
    return selected


def _action_payload(kind: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "kind": kind,
        "entries": [
            {
                "attempt_id": entry.get("attempt_id"),
                "role": entry["role"],
                "work": [
                    {
                        key: work.get(key) for key in (
                            "work_id", "eligibility", "recovery_tier",
                            "diagnostic_count", "repeated_fingerprint_count",
                            "last_failure_fingerprint", "not_before",
                        )
                    }
                    for work in entry["work"]
                ],
                "updated_at": entry.get("updated_at"),
            }
            for entry in entries
        ],
    }


def _insert_action(
    connection: sqlite3.Connection,
    *,
    action_id: str,
    kind: str,
    entries: list[dict[str, Any]],
    now: int,
) -> tuple[str, bool]:
    payload = _action_payload(kind, entries)
    input_digest = _digest(payload)
    idempotency_key = f"{kind}:{input_digest}"
    existing = connection.execute(
        "SELECT action_id FROM action WHERE idempotency_key = ?",
        (idempotency_key,),
    ).fetchone()
    if existing:
        return existing[0], False
    connection.execute(
        """INSERT INTO action(
            action_id, kind, idempotency_key, phase, status, recoverable,
            input_digest, frontier_digest, not_before, created_at, updated_at
        ) VALUES(?, ?, ?, 'planned', 'planned', 1, ?, ?, 0, ?, ?)""",
        (action_id, kind, idempotency_key, input_digest, input_digest, now, now),
    )
    return action_id, True


def _insert_fresh_attempt(
    connection: sqlite3.Connection,
    *,
    action_id: str,
    work: list[dict[str, Any]],
    revision: str,
    inventory_hash: str,
    now: int,
    kind: str = "fresh",
) -> dict[str, Any]:
    work_ids = sorted(item["work_id"] for item in work)
    attempt_id = str(uuid.uuid5(
        ATTEMPT_NAMESPACE, f"{action_id}\0{'|'.join(work_ids)}",
    ))
    cohort_id = common.cohort_id(work_ids)
    source = work[0]["source"]
    basename = _basename(source)
    snapshot = {
        "schema": 1,
        "attempt_id": attempt_id,
        "cohort_id": cohort_id,
        "kind": kind,
        "base_revision": revision,
        "inventory_hash": inventory_hash,
        "basename": basename,
        "file": source,
        "routines": [
            {key: item[key] for key in ("work_id", "source", "name", "line", "size")}
            for item in work
        ],
    }
    snapshot_json = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    packet_hash = hashlib.sha256(snapshot_json.encode()).hexdigest()
    owned_paths = _owned_paths(basename)
    connection.execute(
        """INSERT INTO attempt(
            attempt_id, cohort_id, kind, generation, base_revision, inventory_hash,
            snapshot_json, owned_paths_json, state, not_before, packet_sha256,
            identity_valid, created_at, updated_at
        ) VALUES(?, ?, ?, 0, ?, ?, ?, ?, 'pending', 0, ?, 1, ?, ?)""",
        (
            attempt_id, cohort_id, kind, revision, inventory_hash, snapshot_json,
            json.dumps(owned_paths, sort_keys=True), packet_hash, now, now,
        ),
    )
    for item in work:
        connection.execute(
            "INSERT INTO attempt_work(attempt_id, work_id) VALUES(?, ?)",
            (attempt_id, item["work_id"]),
        )
        connection.execute(
            """UPDATE work SET current_attempt_id = ?, eligibility = 'retry-ready'
               WHERE work_id = ? AND current_attempt_id IS NULL""",
            (attempt_id, item["work_id"]),
        )
    return {
        "attempt_id": attempt_id,
        "role": "fresh",
        "work": work,
        "updated_at": now,
        "basename": basename,
    }


def _insert_retry_attempt(
    connection: sqlite3.Connection,
    *,
    action_id: str,
    parent_attempt_id: str,
    work: list[dict[str, Any]],
    revision: str,
    inventory_hash: str,
    now: int,
) -> dict[str, Any]:
    work_ids = sorted(item["work_id"] for item in work)
    parent = connection.execute(
        "SELECT generation FROM attempt WHERE attempt_id = ?",
        (parent_attempt_id,),
    ).fetchone()
    if parent is None:
        raise KeyError(parent_attempt_id)
    attempt_id = str(uuid.uuid5(
        ATTEMPT_NAMESPACE,
        f"retry\0{action_id}\0{parent_attempt_id}\0{'|'.join(work_ids)}",
    ))
    cohort_id = common.cohort_id(work_ids)
    source = work[0]["source"]
    basename = _basename(source)
    snapshot = {
        "schema": 1,
        "attempt_id": attempt_id,
        "cohort_id": cohort_id,
        "kind": "recovery",
        "parent_attempt_id": parent_attempt_id,
        "base_revision": revision,
        "inventory_hash": inventory_hash,
        "basename": basename,
        "file": source,
        "routines": [
            {key: item[key] for key in ("work_id", "source", "name", "line", "size")}
            for item in work
        ],
    }
    snapshot_json = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    packet_hash = hashlib.sha256(snapshot_json.encode()).hexdigest()
    connection.execute(
        """INSERT INTO attempt(
            attempt_id, cohort_id, kind, parent_attempt_id, generation,
            base_revision, inventory_hash, snapshot_json, owned_paths_json,
            state, not_before, packet_sha256, identity_valid, created_at, updated_at
        ) VALUES(?, ?, 'recovery', ?, ?, ?, ?, ?, ?, 'pending', 0, ?, 1, ?, ?)""",
        (
            attempt_id, cohort_id, parent_attempt_id, parent[0] + 1,
            revision, inventory_hash, snapshot_json,
            json.dumps(_owned_paths(basename), sort_keys=True),
            packet_hash, now, now,
        ),
    )
    for item in work:
        connection.execute(
            "INSERT INTO attempt_work(attempt_id, work_id) VALUES(?, ?)",
            (attempt_id, item["work_id"]),
        )
        connection.execute(
            """UPDATE work SET current_attempt_id = ?, eligibility = 'retry-ready'
               WHERE work_id = ? AND current_attempt_id = ?""",
            (attempt_id, item["work_id"], parent_attempt_id),
        )
    connection.execute(
        """UPDATE attempt SET state = 'superseded', updated_at = ?
           WHERE attempt_id = ?""",
        (now, parent_attempt_id),
    )
    return {
        "attempt_id": attempt_id,
        "role": "recovery",
        "work": work,
        "updated_at": now,
        "basename": basename,
    }




def _bind_action_entries(
    connection: sqlite3.Connection,
    action_id: str,
    entries: list[dict[str, Any]],
) -> None:
    for entry in entries:
        attempt_id = entry.get("attempt_id")
        if attempt_id:
            connection.execute(
                "INSERT INTO action_attempt(action_id, attempt_id, role) VALUES(?, ?, ?)",
                (action_id, attempt_id, entry["role"]),
            )
        for work in entry["work"]:
            connection.execute(
                "INSERT OR IGNORE INTO action_work(action_id, work_id, role) VALUES(?, ?, ?)",
                (action_id, work["work_id"], entry["role"]),
            )


def _recovery_lane_cost(entry: dict[str, Any]) -> int:
    tier = max(
        (int(work.get("recovery_tier", 0)) for work in entry["work"]),
        default=0,
    )
    return 2 if tier >= 4 else 1


def _select_mixed_wave(
    connection: sqlite3.Connection,
    *,
    lanes_count: int,
    now: int,
    max_routines: int,
    max_bytes: int,
) -> tuple[list[list[dict[str, Any]]], list[dict[str, Any]]]:
    fresh = _fresh_groups(
        connection, now=now, max_routines=max_routines, max_bytes=max_bytes,
    )
    recovery = _recovery_candidates(connection, now=now)
    if not fresh:
        fresh_slots, recovery_slots = 0, lanes_count
    elif not recovery:
        fresh_slots, recovery_slots = lanes_count, 0
    elif lanes_count == 1:
        tick = int(_metadata(connection, "scheduler_tick", "0"))
        fresh_slots, recovery_slots = ((0, 1) if tick % 5 == 4 else (1, 0))
    else:
        recovery_slots = max(1, lanes_count // 5)
        fresh_slots = lanes_count - recovery_slots
    selected_fresh = fresh[:fresh_slots]
    basenames = {_basename(group[0]["source"]) for group in selected_fresh}
    selected_recovery = []
    recovery_used = 0
    for entry in recovery:
        cost = _recovery_lane_cost(entry)
        if entry["basename"] in basenames or recovery_used + cost > recovery_slots:
            continue
        selected_recovery.append(entry)
        basenames.add(entry["basename"])
        recovery_used += cost
        if recovery_used >= recovery_slots:
            break
    spare = lanes_count - len(selected_fresh) - recovery_used
    if spare and len(selected_fresh) < len(fresh):
        for group in fresh[len(selected_fresh):]:
            basename = _basename(group[0]["source"])
            if basename in basenames:
                continue
            selected_fresh.append(group)
            basenames.add(basename)
            spare -= 1
            if not spare:
                break
    if spare and len(selected_recovery) < len(recovery):
        chosen = {entry["attempt_id"] for entry in selected_recovery}
        for entry in recovery:
            cost = _recovery_lane_cost(entry)
            if (
                entry["attempt_id"] in chosen
                or entry["basename"] in basenames
                or cost > spare
            ):
                continue
            selected_recovery.append(entry)
            basenames.add(entry["basename"])
            spare -= cost
            if not spare:
                break
    return selected_fresh, selected_recovery


def _strong_components(graph: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    result: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = index
        low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in sorted(graph.get(node, set())):
            if target not in graph:
                continue
            if target not in indices:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in on_stack:
                low[node] = min(low[node], indices[target])
        if low[node] != indices[node]:
            return
        component = []
        while True:
            target = stack.pop()
            on_stack.remove(target)
            component.append(target)
            if target == node:
                break
        result.append(sorted(component))

    for node in sorted(graph):
        if node not in indices:
            visit(node)
    return sorted(result)


def _blocked_entries(
    connection: sqlite3.Connection,
    limit: int,
    *,
    cycles_only: bool = False,
) -> tuple[str, list[dict[str, Any]]]:
    blocked = {
        work_id for work_id, in connection.execute(
            "SELECT work_id FROM work WHERE eligibility = 'blocked' AND stop_kind IS NULL"
        )
    }
    graph = {work_id: set() for work_id in blocked}
    dependencies = {work_id: set() for work_id in blocked}
    for work_id, blocked_on in connection.execute(
        """SELECT work_id, blocked_on_work_id FROM blocker
           WHERE active = 1 AND kind = 'dependency'"""
    ):
        if work_id in dependencies:
            dependencies[work_id].add(blocked_on)
        if work_id in graph and blocked_on in blocked:
            graph[work_id].add(blocked_on)
    cycles = []
    for component in _strong_components(graph):
        members = set(component)
        cyclic = len(component) > 1 or component[0] in graph.get(component[0], set())
        closed = all(dependencies[node] <= members for node in component)
        if cyclic and closed:
            cycles.append(component)
    selected_ids = cycles[0] if cycles else []
    kind = "dependency-scc"
    if not selected_ids and cycles_only:
        return kind, []
    if not selected_ids:
        selected_ids = [
            work_id for work_id, in connection.execute(
                """SELECT DISTINCT w.work_id FROM work w
                   LEFT JOIN blocker b ON b.work_id = w.work_id AND b.active = 1
                   WHERE w.eligibility = 'blocked' AND w.stop_kind IS NULL
                     AND (b.kind IS NULL OR b.kind != 'dependency')
                   ORDER BY w.not_before, w.work_id LIMIT ?""",
                (limit,),
            )
        ]
        kind = "blocker-review"
    entries = []
    for work_id in selected_ids:
        row = connection.execute(
            """SELECT work_id, source, name, line, size, eligibility, recovery_tier,
                      diagnostic_count, repeated_fingerprint_count,
                      last_failure_fingerprint, not_before, stop_kind
               FROM work WHERE work_id = ?""",
            (work_id,),
        ).fetchone()
        keys = (
            "work_id", "source", "name", "line", "size", "eligibility",
            "recovery_tier", "diagnostic_count", "repeated_fingerprint_count",
            "last_failure_fingerprint", "not_before", "stop_kind",
        )
        entries.append({"role": kind, "work": [dict(zip(keys, row, strict=True))]})
    return kind, entries

def _plan_blocked_action(
    connection: sqlite3.Connection,
    *,
    kind: str,
    entries: list[dict[str, Any]],
    now: int,
) -> dict[str, Any]:
    action_id = str(uuid.uuid4())
    action_id, created = _insert_action(
        connection, action_id=action_id, kind=kind, entries=entries, now=now,
    )
    if not created:
        return {"status": "stalled", "reason": f"{kind}-no-new-evidence"}
    bound_entries = entries
    if kind == "dependency-scc":
        work = [entry["work"][0] for entry in entries]
        connection.executemany(
            """UPDATE work SET recovery_tier = MAX(recovery_tier, 3),
                               eligibility = 'retry-ready'
               WHERE work_id = ?""",
            [(item["work_id"],) for item in work],
        )
        dependency_attempt = _insert_fresh_attempt(
            connection, action_id=action_id, work=work,
            revision=_metadata(connection, "source_revision"),
            inventory_hash=_metadata(connection, "source_digest"),
            now=now, kind="dependency-scc",
        )
        dependency_attempt["role"] = "dependency-scc"
        bound_entries = [dependency_attempt]
    _bind_action_entries(connection, action_id, bound_entries)
    return {
        "status": "planned",
        "action": _action_descriptor(connection, action_id),
        "reused": False,
    }


def plan_tick(
    connection: sqlite3.Connection,
    *,
    lanes_count: int = 10,
    now: int | None = None,
    max_routines: int = 3,
    max_bytes: int = 140,
    integration_batch: int = 3,
) -> dict[str, Any]:
    if lanes_count <= 0 or max_routines <= 0 or max_bytes <= 0 or integration_batch <= 0:
        raise ValueError("scheduler limits must be positive")
    now = int(time.time()) if now is None else now
    with state.immediate(connection):
        state.recover_expired_in_transaction(connection, now)
        existing = _existing_action(connection, now)
        if existing:
            return {"status": "planned", "action": existing, "reused": True}
        gate_rows = connection.execute(
            """SELECT work_id, source, name, line, size, eligibility, recovery_tier,
                      diagnostic_count, repeated_fingerprint_count,
                      last_failure_fingerprint, not_before, stop_kind
               FROM work
               WHERE eligibility = 'green-integrating'
                 AND current_attempt_id IS NULL AND not_before <= ?
               ORDER BY work_id LIMIT ?""",
            (now, integration_batch),
        ).fetchall()
        if gate_rows:
            keys = (
                "work_id", "source", "name", "line", "size", "eligibility",
                "recovery_tier", "diagnostic_count",
                "repeated_fingerprint_count", "last_failure_fingerprint",
                "not_before", "stop_kind",
            )
            entries = [
                {
                    "role": "gate-refresh",
                    "work": [dict(zip(keys, row, strict=True))],
                    "updated_at": None,
                }
                for row in gate_rows
            ]
            action_id = str(uuid.uuid4())
            action_id, created = _insert_action(
                connection, action_id=action_id, kind="gate-refresh",
                entries=entries, now=now,
            )
            if created:
                _bind_action_entries(connection, action_id, entries)
                return {
                    "status": "planned",
                    "action": _action_descriptor(connection, action_id),
                    "reused": False,
                }
            return {"status": "stalled", "reason": "gate-refresh-no-new-evidence"}
        integration = _integration_candidates(
            connection, now=now, limit=integration_batch,
        )
        if integration:
            entries = [{**entry, "role": "integration"} for entry in integration]
            action_id = str(uuid.uuid4())
            action_id, created = _insert_action(
                connection, action_id=action_id, kind="integration",
                entries=entries, now=now,
            )
            if created:
                _bind_action_entries(connection, action_id, entries)
                return {
                    "status": "planned",
                    "action": _action_descriptor(connection, action_id),
                    "reused": False,
                }
            return {"status": "stalled", "reason": "integration-no-new-evidence"}
        projection_rows = connection.execute(
            """SELECT projection_key, source_hash, desired_json, attempts, not_before
               FROM projection_backlog
               WHERE backend = 'forgejo' AND not_before <= ?
               ORDER BY projection_key""",
            (now,),
        ).fetchall()
        if projection_rows:
            entries = [{
                "role": "projection",
                "work": [],
                "updated_at": _digest(projection_rows),
            }]
            action_id = str(uuid.uuid4())
            action_id, created = _insert_action(
                connection, action_id=action_id, kind="projection-reconcile",
                entries=entries, now=now,
            )
            if created:
                _bind_action_entries(connection, action_id, entries)
                return {
                    "status": "planned",
                    "action": _action_descriptor(connection, action_id),
                    "reused": False,
                }
            return {
                "status": "stalled",
                "reason": "projection-no-new-evidence",
            }
        kind, entries = _blocked_entries(
            connection, lanes_count, cycles_only=True,
        )
        if entries:
            return _plan_blocked_action(
                connection, kind=kind, entries=entries, now=now,
            )
        fresh_groups, recovery = _select_mixed_wave(
            connection, lanes_count=lanes_count, now=now,
            max_routines=max_routines, max_bytes=max_bytes,
        )
        if fresh_groups or recovery:
            action_id = str(uuid.uuid4())
            provisional = [
                {"role": "fresh", "work": group, "updated_at": None}
                for group in fresh_groups
            ] + [
                {**entry, "role": "recovery"} for entry in recovery
            ]
            wave_kind = (
                "worker-wave" if fresh_groups and recovery
                else "fresh-wave" if fresh_groups
                else "retry-wave"
            )
            action_id, created = _insert_action(
                connection, action_id=action_id, kind=wave_kind,
                entries=provisional, now=now,
            )
            if not created:
                return {"status": "stalled", "reason": f"{wave_kind}-no-new-evidence"}
            revision = _metadata(connection, "source_revision")
            inventory_hash = _metadata(connection, "source_digest")
            entries = [
                _insert_fresh_attempt(
                    connection, action_id=action_id, work=group,
                    revision=revision, inventory_hash=inventory_hash, now=now,
                )
                for group in fresh_groups
            ] + [
                _insert_retry_attempt(
                    connection, action_id=action_id,
                    parent_attempt_id=entry["attempt_id"],
                    work=entry["work"], revision=revision,
                    inventory_hash=inventory_hash, now=now,
                )
                for entry in provisional[len(fresh_groups):]
            ]
            _bind_action_entries(connection, action_id, entries)
            tick = int(_metadata(connection, "scheduler_tick", "0")) + 1
            connection.execute(
                """INSERT INTO metadata(key, value) VALUES('scheduler_tick', ?)
                   ON CONFLICT(key) DO UPDATE SET value = excluded.value""",
                (str(tick),),
            )
            return {
                "status": "planned",
                "action": _action_descriptor(connection, action_id),
                "reused": False,
                "capacity": {
                    "lanes": lanes_count,
                    "fresh_lanes": len(fresh_groups),
                    "recovery_lanes": sum(
                        _recovery_lane_cost(entry) for entry in recovery
                    ),
                    "recovery_attempts": len(recovery),
                },
            }
        kind, entries = _blocked_entries(connection, lanes_count)
        if entries:
            return _plan_blocked_action(
                connection, kind=kind, entries=entries, now=now,
            )
        counts = dict(connection.execute(
            "SELECT eligibility, COUNT(*) FROM work GROUP BY eligibility"
        ))
        return {
            "status": "blocked",
            "reason": "no-runnable-action",
            "eligibility": counts,
        }


def plan_recovery_tick(
    connection: sqlite3.Connection,
    *,
    now: int | None = None,
) -> dict[str, Any] | None:
    """Return retained journal work without planning from authority metadata."""
    now = int(time.time()) if now is None else now
    with state.immediate(connection):
        state.recover_expired_in_transaction(connection, now)
        action = _existing_action(connection, now)
    if action is None:
        return None
    return {"status": "planned", "action": action, "reused": True}


def has_publication_work(
    connection: sqlite3.Connection,
    *,
    now: int | None = None,
) -> bool:
    now = int(time.time()) if now is None else now
    return bool(connection.execute(
        """SELECT 1 FROM work
           WHERE eligibility = 'green-integrating' AND not_before <= ?
           LIMIT 1""",
        (now,),
    ).fetchone())


def acquire_recovery_tick(
    connection: sqlite3.Connection,
    *,
    lease_owner: str,
    lease_seconds: int,
    now: int | None = None,
) -> dict[str, Any] | None:
    """Lease retained journal work without planning against stale metadata."""
    now = int(time.time()) if now is None else now
    planned = plan_recovery_tick(connection, now=now)
    if planned is None:
        return None
    action_id = planned["action"]["action_id"]
    try:
        lease = state.claim_action(
            connection, action_id, lease_owner=lease_owner,
            lease_seconds=lease_seconds, now=now,
        )
    except state.LeaseConflict as exc:
        return {"status": "busy", "reason": str(exc), "action_id": action_id}
    return {
        **planned,
        "status": "leased",
        "lease": lease,
        "action": _action_descriptor(connection, action_id),
    }


def acquire_tick(
    connection: sqlite3.Connection,
    *,
    lease_owner: str,
    lease_seconds: int,
    lanes_count: int = 10,
    now: int | None = None,
    **limits: Any,
) -> dict[str, Any]:
    now = int(time.time()) if now is None else now
    planned = plan_tick(
        connection, lanes_count=lanes_count, now=now, **limits,
    )
    if planned.get("status") != "planned":
        return planned
    action_id = planned["action"]["action_id"]
    try:
        lease = state.claim_action(
            connection, action_id, lease_owner=lease_owner,
            lease_seconds=lease_seconds, now=now,
        )
    except state.LeaseConflict as exc:
        return {"status": "busy", "reason": str(exc), "action_id": action_id}
    return {
        **planned,
        "status": "leased",
        "lease": lease,
        "action": _action_descriptor(connection, action_id),
    }


def _failure_fingerprint(result: dict[str, Any]) -> str:
    fingerprint = result.get("fingerprint")
    if isinstance(fingerprint, str) and len(fingerprint) == 64:
        return fingerprint
    return _digest({
        "failure_class": result.get("failure_class") or "unknown",
        "detail": result.get("detail") or "",
        "phase": result.get("phase") or "worker",
        "status": result.get("outcome") or "diagnostic",
    })


def _advance_diagnostic(
    connection: sqlite3.Connection,
    work_id: str,
    fingerprint: str,
) -> tuple[bool, bool]:
    row = connection.execute(
        """SELECT recovery_tier, diagnostic_count, repeated_fingerprint_count,
                  last_failure_fingerprint FROM work WHERE work_id = ?""",
        (work_id,),
    ).fetchone()
    if row is None:
        raise KeyError(work_id)
    tier, diagnostics, repeats, previous = row
    novel = previous != fingerprint
    advance = False
    if tier < 3:
        if novel:
            diagnostics += 1
            repeats = 0
            advance = diagnostics >= 2
        else:
            repeats += 1
            advance = repeats >= 1
    elif tier == 3:
        if novel:
            diagnostics += 1
            repeats = 0
        else:
            repeats += 1
            advance = repeats >= 1
    else:
        diagnostics += int(novel)
        repeats = 0 if novel else repeats + 1
    if advance:
        tier = min(tier + 1, 4)
        diagnostics = 0
        repeats = 0
    connection.execute(
        """UPDATE work SET recovery_tier = ?, diagnostic_count = ?,
                  repeated_fingerprint_count = ?, last_failure_fingerprint = ?,
                  eligibility = 'retry-ready', stop_kind = NULL WHERE work_id = ?""",
        (tier, diagnostics, repeats, fingerprint, work_id),
    )
    return novel, advance


def _require_published_bundle(
    attempt_id: str,
    snapshot: dict[str, Any],
    work_ids: list[str],
    bundle_hash: Any,
) -> None:
    if not isinstance(bundle_hash, str) or len(bundle_hash) != 64:
        raise ValueError(f"productive attempt {attempt_id} has no bundle hash")
    bundle = common.BUNDLES / attempt_id
    manifest_path = bundle / "packet.json"
    if not bundle.is_dir() or not manifest_path.is_file():
        raise RuntimeError(f"productive attempt {attempt_id} bundle is not published")
    if common.payload_tree_digest(bundle) != bundle_hash:
        raise RuntimeError(f"productive attempt {attempt_id} bundle hash mismatch")
    manifest = json.loads(manifest_path.read_text())
    required_keys = {
        "schema", "attempt_id", "cohort_id", "id", "basename", "file",
        "base_commit", "routines",
    }
    manifest_work = [
        routine.get("work_id") for routine in manifest.get("routines", [])
        if isinstance(routine, dict)
    ]
    expected_base = snapshot.get("base_revision") or snapshot.get("base_commit")
    if (
        set(manifest) != required_keys
        or manifest.get("schema") != common.SCHEMA
        or manifest.get("attempt_id") != attempt_id
        or manifest.get("id") != attempt_id
        or manifest.get("cohort_id") != common.cohort_id(work_ids)
        or sorted(manifest_work) != sorted(work_ids)
        or (expected_base and manifest.get("base_commit") != expected_base)
        or (snapshot.get("basename") and manifest.get("basename") != snapshot["basename"])
        or (snapshot.get("file") and manifest.get("file") != snapshot["file"])
    ):
        raise RuntimeError(f"productive attempt {attempt_id} identity mismatch")


def _record_attempt_result(
    connection: sqlite3.Connection,
    *,
    action_id: str,
    attempt_id: str,
    result: dict[str, Any],
    now: int,
) -> tuple[int, int, int]:
    outcome = result.get("outcome")
    if outcome not in ATTEMPT_OUTCOMES:
        raise ValueError(f"invalid attempt outcome for {attempt_id}: {outcome}")
    work_ids = [
        work_id for work_id, in connection.execute(
            "SELECT work_id FROM attempt_work WHERE attempt_id = ? ORDER BY work_id",
            (attempt_id,),
        )
    ]
    productive = diagnostic = churn = 0
    if outcome == "salvage":
        children = result.get("children")
        if not isinstance(children, list):
            raise TypeError("salvage result requires children")
        for child in children:
            if child.get("state") == "green":
                _require_published_bundle(
                    child["attempt_id"], child["snapshot"],
                    child.get("work_ids") or [], child.get("bundle_sha256"),
                )
        state.create_salvage_children_in_transaction(
            connection, attempt_id, children, now=now,
        )
        failure = result.get("failure") or {}
        fingerprint = _failure_fingerprint(failure)
        detail = str(failure.get("detail") or "salvaged partial attempt")
        connection.execute(
            """INSERT INTO failure(
                attempt_id, action_id, phase, status, failure_class, fingerprint,
                detail, model, observed_at
            ) VALUES(?, ?, ?, 'failed', ?, ?, ?, ?, ?)""",
            (
                attempt_id, action_id, str(failure.get("phase") or "verification"),
                str(failure.get("failure_class") or "partial"), fingerprint,
                detail, failure.get("model"), now,
            ),
        )
        for child in children:
            child_work = child.get("work_ids") or []
            if child.get("state") == "green":
                productive += len(child_work)
                continue
            for work_id in child_work:
                novel, advanced = _advance_diagnostic(
                    connection, work_id, fingerprint,
                )
                diagnostic += int(novel or advanced)
                churn += int(not novel and not advanced)
    elif outcome == "productive":
        bundle_hash = result.get("bundle_sha256")
        snapshot_json = connection.execute(
            "SELECT snapshot_json FROM attempt WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        if snapshot_json is None:
            raise KeyError(attempt_id)
        _require_published_bundle(
            attempt_id, json.loads(snapshot_json[0]), work_ids, bundle_hash,
        )
        connection.execute(
            """UPDATE attempt SET state = 'green', bundle_sha256 = ?, updated_at = ?
               WHERE attempt_id = ?""",
            (bundle_hash, now, attempt_id),
        )
        for work_id in work_ids:
            connection.execute(
                """UPDATE work SET eligibility = 'green-integrating', not_before = 0,
                          diagnostic_count = 0, repeated_fingerprint_count = 0,
                          stop_kind = NULL WHERE work_id = ?""",
                (work_id,),
            )
        productive = len(work_ids)
    elif outcome == "diagnostic":
        fingerprint = _failure_fingerprint(result)
        detail = str(result.get("detail") or "diagnostic failure")
        connection.execute(
            """INSERT INTO failure(
                attempt_id, action_id, phase, status, failure_class, fingerprint,
                detail, model, observed_at
            ) VALUES(?, ?, ?, 'failed', ?, ?, ?, ?, ?)""",
            (
                attempt_id, action_id, str(result.get("phase") or "worker"),
                str(result.get("failure_class") or "unknown"), fingerprint,
                detail, result.get("model"), now,
            ),
        )
        connection.execute(
            "UPDATE attempt SET state = 'retry-ready', updated_at = ? WHERE attempt_id = ?",
            (now, attempt_id),
        )
        for work_id in work_ids:
            novel, advanced = _advance_diagnostic(connection, work_id, fingerprint)
            diagnostic += int(novel or advanced)
            churn += int(not novel and not advanced)
    elif outcome == "provider-failure":
        retry_after = result.get("retry_after", 60)
        if not isinstance(retry_after, int) or not 1 <= retry_after <= 3600:
            raise ValueError("provider retry_after must be between 1 and 3600 seconds")
        not_before = now + retry_after
        connection.execute(
            """UPDATE attempt SET state = 'retry-ready', not_before = ?, updated_at = ?
               WHERE attempt_id = ?""",
            (not_before, now, attempt_id),
        )
        connection.executemany(
            """UPDATE work SET eligibility = 'retry-ready', not_before = ?
               WHERE work_id = ?""",
            [(not_before, work_id) for work_id in work_ids],
        )
        diagnostic = 1
    elif outcome == "infrastructure-failure":
        connection.execute(
            "UPDATE attempt SET state = 'retry-ready', updated_at = ? WHERE attempt_id = ?",
            (now, attempt_id),
        )
        connection.executemany(
            "UPDATE work SET eligibility = 'retry-ready' WHERE work_id = ?",
            [(work_id,) for work_id in work_ids],
        )
        diagnostic = 1
    elif outcome == "blocked":
        blocked_on = result.get("blocked_on") or []
        if not isinstance(blocked_on, list) or not all(isinstance(value, str) for value in blocked_on):
            raise ValueError("blocked_on must be a list of work IDs")
        known = {
            work_id for work_id, in connection.execute(
                f"SELECT work_id FROM work WHERE work_id IN ({','.join('?' for _ in blocked_on)})",
                blocked_on,
            )
        } if blocked_on else set()
        if known != set(blocked_on):
            raise ValueError(f"unknown blocked_on work IDs: {sorted(set(blocked_on) - known)}")
        connection.execute(
            "UPDATE attempt SET state = 'blocked', updated_at = ? WHERE attempt_id = ?",
            (now, attempt_id),
        )
        detail = str(result.get("detail") or "dependency blocked")
        for work_id in work_ids:
            connection.execute(
                "UPDATE work SET eligibility = 'blocked' WHERE work_id = ?",
                (work_id,),
            )
            for dependency in sorted(known):
                connection.execute(
                    """INSERT OR IGNORE INTO blocker(
                        work_id, kind, blocked_on_work_id, reason, unblock, source, active
                    ) VALUES(?, 'dependency', ?, ?, ?, 'worker', 1)""",
                    (work_id, dependency, detail, f"complete {dependency}"),
                )
        diagnostic = 1
    else:
        stop_kind = str(result.get("stop_kind") or "external")
        connection.execute(
            "UPDATE attempt SET state = 'stopped', updated_at = ? WHERE attempt_id = ?",
            (now, attempt_id),
        )
        connection.executemany(
            """UPDATE work SET eligibility = 'external-stop', stop_kind = ?
               WHERE work_id = ?""",
            [(stop_kind, work_id) for work_id in work_ids],
        )
        diagnostic = 1
    return productive, diagnostic, churn


def _record_work_result(
    connection: sqlite3.Connection,
    *,
    action_id: str,
    work_id: str,
    result: dict[str, Any],
    now: int,
) -> tuple[int, int, int]:
    outcome = result.get("outcome")
    if outcome not in WORK_OUTCOMES:
        raise ValueError(f"invalid work outcome for {work_id}: {outcome}")
    current_attempt = connection.execute(
        "SELECT current_attempt_id FROM work WHERE work_id = ?",
        (work_id,),
    ).fetchone()
    if current_attempt is None:
        raise KeyError(work_id)
    attempt_id = current_attempt[0]
    if outcome == "unblocked":
        eligibility = "retry-ready" if attempt_id else "fresh-ready"
        connection.execute(
            """UPDATE work SET eligibility = ?, not_before = 0, stop_kind = NULL
               WHERE work_id = ?""",
            (eligibility, work_id),
        )
        connection.execute(
            "UPDATE blocker SET active = 0 WHERE work_id = ?",
            (work_id,),
        )
        return 1, 0, 0
    if outcome == "diagnostic":
        fingerprint = _failure_fingerprint(result)
        detail = str(result.get("detail") or "blocker diagnostic")
        connection.execute(
            """INSERT INTO failure(
                attempt_id, work_id, action_id, phase, status, failure_class,
                fingerprint, detail, model, observed_at
            ) VALUES(?, ?, ?, ?, 'failed', ?, ?, ?, ?, ?)""",
            (
                attempt_id, work_id, action_id,
                str(result.get("phase") or "blocker-analysis"),
                str(result.get("failure_class") or "unknown"),
                fingerprint, detail, result.get("model"), now,
            ),
        )
        novel, advanced = _advance_diagnostic(connection, work_id, fingerprint)
        return 0, int(novel or advanced), int(not novel and not advanced)
    if outcome == "provider-failure":
        retry_after = result.get("retry_after", 60)
        if not isinstance(retry_after, int) or not 1 <= retry_after <= 3600:
            raise ValueError("provider retry_after must be between 1 and 3600 seconds")
        connection.execute(
            "UPDATE work SET not_before = ? WHERE work_id = ?",
            (now + retry_after, work_id),
        )
        return 0, 1, 0
    if outcome == "infrastructure-failure":
        return 0, 1, 0
    if outcome == "blocked":
        blocked_on = result.get("blocked_on") or []
        if not isinstance(blocked_on, list) or not all(isinstance(value, str) for value in blocked_on):
            raise ValueError("blocked_on must be a list of work IDs")
        known = {
            dependency for dependency, in connection.execute(
                f"SELECT work_id FROM work WHERE work_id IN ({','.join('?' for _ in blocked_on)})",
                blocked_on,
            )
        } if blocked_on else set()
        if known != set(blocked_on):
            raise ValueError(f"unknown blocked_on work IDs: {sorted(set(blocked_on) - known)}")
        detail = str(result.get("detail") or "dependency blocked")
        connection.execute(
            "UPDATE work SET eligibility = 'blocked' WHERE work_id = ?",
            (work_id,),
        )
        for dependency in sorted(known):
            connection.execute(
                """INSERT OR IGNORE INTO blocker(
                    work_id, kind, blocked_on_work_id, reason, unblock, source, active
                ) VALUES(?, 'dependency', ?, ?, ?, 'blocker-analysis', 1)""",
                (work_id, dependency, detail, f"complete {dependency}"),
            )
        return 0, 1, 0
    stop_kind = str(result.get("stop_kind") or "external")
    connection.execute(
        """UPDATE work SET eligibility = 'external-stop', stop_kind = ?
           WHERE work_id = ?""",
        (stop_kind, work_id),
    )
    return 0, 1, 0


def accept_tick(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    result: dict[str, Any],
    now: int | None = None,
) -> dict[str, Any]:
    now = int(time.time()) if now is None else now
    if not isinstance(result, dict):
        raise TypeError("action result must be an object")
    with state.immediate(connection):
        state.require_lease(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, now=now,
        )
        expected = {
            attempt_id for attempt_id, in connection.execute(
                "SELECT attempt_id FROM action_attempt WHERE action_id = ?",
                (action_id,),
            )
        }
        attempt_results = result.get("attempts") or {}
        if not isinstance(attempt_results, dict):
            raise TypeError("attempt results must be an object")
        if set(attempt_results) != expected:
            raise ValueError(
                f"attempt result membership mismatch: expected={sorted(expected)} "
                f"actual={sorted(attempt_results)}"
            )
        expected_work = {
            work_id for work_id, in connection.execute(
                "SELECT work_id FROM action_work WHERE action_id = ?",
                (action_id,),
            )
        }
        work_results = result.get("work") or {}
        if not isinstance(work_results, dict):
            raise TypeError("work results must be an object")
        if expected and work_results:
            raise ValueError("attempt actions cannot also return direct work results")
        if not expected and set(work_results) != expected_work:
            raise ValueError(
                f"work result membership mismatch: expected={sorted(expected_work)} "
                f"actual={sorted(work_results)}"
            )
        productive = diagnostic = churn = 0
        for attempt_id in sorted(expected):
            counts = _record_attempt_result(
                connection, action_id=action_id, attempt_id=attempt_id,
                result=attempt_results[attempt_id], now=now,
            )
            productive += counts[0]
            diagnostic += counts[1]
            churn += counts[2]
        for work_id in sorted(work_results):
            counts = _record_work_result(
                connection, action_id=action_id, work_id=work_id,
                result=work_results[work_id], now=now,
            )
            productive += counts[0]
            diagnostic += counts[1]
            churn += counts[2]
        liveness = "productive" if productive else "diagnostic" if diagnostic else "churn"
        accepted = {
            **result,
            "liveness": liveness,
            "productive_work": productive,
            "diagnostic_work": diagnostic,
            "churn_work": churn,
        }
        state.finish_action_in_transaction(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, result=accepted, success=True, now=now,
        )
    return accepted


