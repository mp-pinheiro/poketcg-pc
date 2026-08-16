#!/usr/bin/env python3
"""Transactional factory state and read-only legacy migration audit."""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sqlite3
import uuid
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import common

SCHEMA_VERSION = 2
ACTION_NAMESPACE = uuid.UUID("a8cf2bbb-e5ee-5a2d-84af-1d9c28587762")
INPUT_FILES = (
    common.ROOT / "site/data/inventory.json",
    common.ROOT / "site/data/gate.json",
    common.ROOT / "tools/progress/scope.toml",
    common.ROOT / "tools/oracle/artifacts.json",
    common.ROOT / "tests/routines.py",
    common.METRICS,
    common.EVENTS,
    common.BLOCKED,
    common.FACTORY / "supervisor.json",
    common.FACTORY / "integration.json",
    common.FACTORY / "forgejo-sync.json",
)
INPUT_TREES = (
    common.QUEUE,
    common.BUNDLES,
    common.FACTORY / "recovery-groups",
    common.FACTORY / "escalations",
)
HISTORICAL = frozenset({"landed", "superseded"})
ATTEMPT_STATES = frozenset({
    "pending", "leased", "translating", "translated", "verifying", "repair",
    "retry-ready", "recovering", "green", "integrating", "blocked", "landed",
    "superseded", "failed", "stopped",
})
RETRY_STATES = frozenset({
    "translating", "translated", "verifying", "repair", "retry-ready", "recovering",
    "failed", "stopped",
})

SCHEMA_SQL = """
CREATE TABLE metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) STRICT;
CREATE TABLE source_input (
    path TEXT PRIMARY KEY,
    sha256 TEXT NOT NULL CHECK(length(sha256) = 64),
    size INTEGER NOT NULL CHECK(size >= 0)
) STRICT;
CREATE TABLE work (
    work_id TEXT PRIMARY KEY CHECK(work_id LIKE 'port:v1:%'),
    source TEXT,
    name TEXT NOT NULL,
    line INTEGER,
    size INTEGER NOT NULL CHECK(size >= 0),
    canonical_state TEXT NOT NULL,
    eligibility TEXT NOT NULL,
    current_attempt_id TEXT,
    recovery_tier INTEGER NOT NULL DEFAULT 0 CHECK(recovery_tier BETWEEN 0 AND 5),
    diagnostic_count INTEGER NOT NULL DEFAULT 0 CHECK(diagnostic_count >= 0),
    repeated_fingerprint_count INTEGER NOT NULL DEFAULT 0
        CHECK(repeated_fingerprint_count >= 0),
    last_failure_fingerprint TEXT
        CHECK(last_failure_fingerprint IS NULL OR length(last_failure_fingerprint) = 64),
    not_before INTEGER NOT NULL DEFAULT 0 CHECK(not_before >= 0),
    stop_kind TEXT,
    FOREIGN KEY(work_id, current_attempt_id)
        REFERENCES attempt_work(work_id, attempt_id)
        DEFERRABLE INITIALLY DEFERRED
) STRICT;
CREATE TABLE action (
    action_id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    phase TEXT NOT NULL,
    status TEXT NOT NULL,
    recoverable INTEGER NOT NULL DEFAULT 1 CHECK(recoverable IN (0, 1)),
    input_digest TEXT NOT NULL CHECK(length(input_digest) = 64),
    frontier_digest TEXT,
    lease_owner TEXT,
    lease_token TEXT,
    lease_deadline INTEGER,
    heartbeat_at INTEGER,
    not_before INTEGER NOT NULL DEFAULT 0,
    result_json TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    CHECK(not_before >= 0),
    CHECK(
        (lease_owner IS NULL AND lease_token IS NULL AND lease_deadline IS NULL)
        OR
        (lease_owner IS NOT NULL AND lease_token IS NOT NULL AND lease_deadline IS NOT NULL)
    )
) STRICT;
CREATE TABLE attempt (
    attempt_id TEXT PRIMARY KEY,
    legacy_packet_id TEXT,
    cohort_id TEXT NOT NULL CHECK(length(cohort_id) = 64),
    kind TEXT NOT NULL,
    parent_attempt_id TEXT REFERENCES attempt(attempt_id),
    generation INTEGER NOT NULL CHECK(generation >= 0),
    base_revision TEXT,
    inventory_hash TEXT,
    snapshot_json TEXT NOT NULL CHECK(json_valid(snapshot_json)),
    owned_paths_json TEXT NOT NULL CHECK(json_valid(owned_paths_json)),
    state TEXT NOT NULL CHECK(state IN (
        'pending', 'leased', 'translating', 'translated', 'verifying', 'repair',
        'retry-ready', 'recovering', 'green', 'integrating', 'blocked', 'landed',
        'superseded', 'failed', 'stopped'
    )),
    model TEXT,
    not_before INTEGER NOT NULL DEFAULT 0 CHECK(not_before >= 0),
    owner_action_id TEXT REFERENCES action(action_id),
    packet_sha256 TEXT NOT NULL CHECK(length(packet_sha256) = 64),
    bundle_sha256 TEXT,
    identity_valid INTEGER NOT NULL CHECK(identity_valid IN (0, 1)),
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY(owner_action_id, attempt_id)
        REFERENCES action_attempt(action_id, attempt_id)
        DEFERRABLE INITIALLY DEFERRED
) STRICT;
CREATE TABLE attempt_work (
    attempt_id TEXT NOT NULL REFERENCES attempt(attempt_id),
    work_id TEXT NOT NULL REFERENCES work(work_id),
    PRIMARY KEY(attempt_id, work_id),
    UNIQUE(work_id, attempt_id)
) STRICT;
CREATE TABLE failure (
    failure_id INTEGER PRIMARY KEY,
    attempt_id TEXT REFERENCES attempt(attempt_id),
    work_id TEXT REFERENCES work(work_id),
    action_id TEXT REFERENCES action(action_id),
    phase TEXT NOT NULL,
    status TEXT NOT NULL,
    failure_class TEXT NOT NULL,
    fingerprint TEXT NOT NULL CHECK(length(fingerprint) = 64),
    detail TEXT NOT NULL,
    model TEXT,
    observed_at INTEGER NOT NULL,
    CHECK(attempt_id IS NOT NULL OR work_id IS NOT NULL OR action_id IS NOT NULL)
) STRICT;
CREATE TABLE action_attempt (
    action_id TEXT NOT NULL REFERENCES action(action_id),
    attempt_id TEXT NOT NULL REFERENCES attempt(attempt_id),
    role TEXT NOT NULL,
    PRIMARY KEY(action_id, attempt_id)
) STRICT;
CREATE TABLE action_work (
    action_id TEXT NOT NULL REFERENCES action(action_id),
    work_id TEXT NOT NULL REFERENCES work(work_id),
    role TEXT NOT NULL,
    PRIMARY KEY(action_id, work_id)
) STRICT;
CREATE TABLE integration (
    action_id TEXT PRIMARY KEY REFERENCES action(action_id),
    phase TEXT NOT NULL CHECK(phase IN (
        'prepared', 'applied', 'source-committed', 'gate-passed',
        'progress-committed', 'pushed', 'finalized', 'failed'
    )),
    baseline_revision TEXT,
    candidate_tree TEXT,
    candidate_commit TEXT,
    gate_hash TEXT,
    progress_hash TEXT,
    remote_revision TEXT,
    updated_at INTEGER NOT NULL
) STRICT;
CREATE TABLE blocker (
    work_id TEXT NOT NULL REFERENCES work(work_id),
    kind TEXT NOT NULL,
    blocked_on_work_id TEXT REFERENCES work(work_id),
    reason TEXT NOT NULL,
    unblock TEXT NOT NULL,
    source TEXT NOT NULL,
    active INTEGER NOT NULL CHECK(active IN (0, 1)),
    PRIMARY KEY(work_id, kind, blocked_on_work_id, source)
) STRICT;
CREATE TABLE projection_backlog (
    backend TEXT NOT NULL,
    projection_key TEXT NOT NULL,
    source_hash TEXT,
    desired_json TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0 CHECK(attempts >= 0),
    not_before INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY(backend, projection_key)
) STRICT;
CREATE TRIGGER work_identity_immutable
BEFORE UPDATE OF work_id, source, name, line, size
ON work BEGIN SELECT RAISE(ABORT, 'work identity is immutable'); END;
CREATE TRIGGER action_identity_immutable
BEFORE UPDATE OF action_id, kind, idempotency_key, recoverable, input_digest,
                 frontier_digest, created_at
ON action BEGIN SELECT RAISE(ABORT, 'action identity is immutable'); END;
CREATE TRIGGER attempt_identity_immutable
BEFORE UPDATE OF attempt_id, legacy_packet_id, cohort_id, kind, parent_attempt_id,
                 generation, base_revision, inventory_hash, snapshot_json,
                 owned_paths_json, packet_sha256
ON attempt BEGIN SELECT RAISE(ABORT, 'attempt identity is immutable'); END;
CREATE TRIGGER attempt_work_immutable_update
BEFORE UPDATE ON attempt_work BEGIN SELECT RAISE(ABORT, 'attempt membership is immutable'); END;
CREATE TRIGGER attempt_work_immutable_delete
BEFORE DELETE ON attempt_work BEGIN SELECT RAISE(ABORT, 'attempt membership is immutable'); END;
CREATE TRIGGER action_work_immutable_update
BEFORE UPDATE ON action_work BEGIN SELECT RAISE(ABORT, 'action work is immutable'); END;
CREATE TRIGGER action_work_immutable_delete
BEFORE DELETE ON action_work BEGIN SELECT RAISE(ABORT, 'action work is immutable'); END;
CREATE TRIGGER failure_append_only_update
BEFORE UPDATE ON failure BEGIN SELECT RAISE(ABORT, 'failure evidence is append-only'); END;
CREATE TRIGGER failure_append_only_delete
BEFORE DELETE ON failure BEGIN SELECT RAISE(ABORT, 'failure evidence is append-only'); END;
"""


def open_state(path: Path = common.STATE_DB) -> sqlite3.Connection:
    """Open the durable authority. Callers own explicit transactions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=30, isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")
    mode = connection.execute("PRAGMA journal_mode = WAL").fetchone()[0]
    if str(mode).lower() != "wal":
        connection.close()
        raise RuntimeError(f"state database refused WAL mode: {mode}")
    return connection


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_SQL)
    connection.execute(
        "INSERT INTO metadata(key, value) VALUES('schema_version', ?)",
        (str(SCHEMA_VERSION),),
    )


class LeaseConflict(RuntimeError):
    pass


class LeaseLost(RuntimeError):
    pass


@contextlib.contextmanager
def immediate(connection: sqlite3.Connection):
    if connection.in_transaction:
        raise RuntimeError("nested state transaction")
    connection.execute("BEGIN IMMEDIATE")
    try:
        yield
    except BaseException:
        connection.execute("ROLLBACK")
        raise
    else:
        connection.execute("COMMIT")


def recover_expired_in_transaction(
    connection: sqlite3.Connection,
    now: int,
) -> list[str]:
    rows = connection.execute(
        """SELECT action_id FROM action
           WHERE lease_deadline IS NOT NULL
             AND lease_deadline <= ?
             AND status IN ('leased', 'running')""",
        (now,),
    ).fetchall()
    action_ids = sorted(row[0] for row in rows)
    for action_id in action_ids:
        connection.execute(
            "UPDATE attempt SET owner_action_id = NULL WHERE owner_action_id = ?",
            (action_id,),
        )
        connection.execute(
            """UPDATE action
               SET phase = 'recovering', status = 'expired',
                   lease_owner = NULL, lease_token = NULL, lease_deadline = NULL,
                   heartbeat_at = NULL, updated_at = ?
               WHERE action_id = ?""",
            (now, action_id),
        )
    return action_ids


def recover_expired_actions(
    connection: sqlite3.Connection,
    *,
    now: int,
) -> list[str]:
    with immediate(connection):
        return recover_expired_in_transaction(connection, now)


def claim_action(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_seconds: int,
    now: int,
) -> dict[str, Any]:
    if not lease_owner:
        raise ValueError("lease owner must be nonempty")
    if lease_seconds <= 0:
        raise ValueError("lease duration must be positive")
    with immediate(connection):
        recovered = recover_expired_in_transaction(connection, now)
        row = connection.execute(
            """SELECT status, recoverable, not_before, lease_owner, lease_token, lease_deadline
               FROM action WHERE action_id = ?""",
            (action_id,),
        ).fetchone()
        if row is None:
            raise KeyError(action_id)
        status, recoverable, not_before, owner, _token, deadline = row
        if not recoverable:
            raise LeaseConflict(f"action {action_id} is retained evidence, not runnable")
        if status not in {"planned", "recovering", "expired"}:
            raise LeaseConflict(
                f"action {action_id} is {status}; owner={owner} deadline={deadline}"
            )
        if not_before > now:
            raise LeaseConflict(f"action {action_id} is deferred until {not_before}")
        conflicts = connection.execute(
            """SELECT attempt_id, owner_action_id FROM attempt
               WHERE attempt_id IN (
                   SELECT attempt_id FROM action_attempt WHERE action_id = ?
               )
                 AND owner_action_id IS NOT NULL
                 AND owner_action_id != ?""",
            (action_id, action_id),
        ).fetchall()
        if conflicts:
            detail = ", ".join(f"{attempt}:{current}" for attempt, current in conflicts)
            raise LeaseConflict(f"action attempt ownership conflict: {detail}")
        lease_token = str(uuid.uuid4())
        lease_deadline = now + lease_seconds
        connection.execute(
            """UPDATE action
               SET phase = 'leased', status = 'leased', lease_owner = ?,
                   lease_token = ?, lease_deadline = ?, heartbeat_at = ?, updated_at = ?
               WHERE action_id = ?""",
            (lease_owner, lease_token, lease_deadline, now, now, action_id),
        )
        connection.execute(
            """UPDATE attempt SET owner_action_id = ?
               WHERE attempt_id IN (
                   SELECT attempt_id FROM action_attempt WHERE action_id = ?
               )""",
            (action_id, action_id),
        )
    return {
        "action_id": action_id,
        "lease_owner": lease_owner,
        "lease_token": lease_token,
        "lease_deadline": lease_deadline,
        "recovered_action_ids": recovered,
    }


def heartbeat_action(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    lease_seconds: int,
    now: int,
) -> int:
    if lease_seconds <= 0:
        raise ValueError("lease duration must be positive")
    deadline = now + lease_seconds
    with immediate(connection):
        cursor = connection.execute(
            """UPDATE action
               SET phase = 'running', status = 'running', lease_deadline = ?,
                   heartbeat_at = ?, updated_at = ?
               WHERE action_id = ? AND lease_owner = ? AND lease_token = ?
                 AND lease_deadline > ?
                 AND status IN ('leased', 'running')""",
            (deadline, now, now, action_id, lease_owner, lease_token, now),
        )
        if cursor.rowcount != 1:
            raise LeaseLost(f"lease lost for action {action_id}")
    return deadline


def require_lease(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    now: int,
) -> None:
    row = connection.execute(
        """SELECT 1 FROM action
           WHERE action_id = ? AND lease_owner = ? AND lease_token = ?
             AND lease_deadline > ?
             AND status IN ('leased', 'running')""",
        (action_id, lease_owner, lease_token, now),
    ).fetchone()
    if row is None:
        raise LeaseLost(f"lease lost for action {action_id}")


def finish_action_in_transaction(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    result: dict[str, Any],
    success: bool,
    now: int,
) -> None:
    require_lease(
        connection, action_id, lease_owner=lease_owner,
        lease_token=lease_token, now=now,
    )
    phase = "completed" if success else "failed"
    connection.execute(
        "UPDATE attempt SET owner_action_id = NULL WHERE owner_action_id = ?",
        (action_id,),
    )
    connection.execute(
        """UPDATE action
           SET phase = ?, status = ?, result_json = ?,
               lease_owner = NULL, lease_token = NULL, lease_deadline = NULL,
               heartbeat_at = NULL, updated_at = ?
           WHERE action_id = ?""",
        (phase, phase, json.dumps(result, sort_keys=True), now, action_id),
    )

INTEGRATION_TRANSITIONS = {
    "prepared": "applied",
    "applied": "source-committed",
    "source-committed": "gate-passed",
    "gate-passed": "progress-committed",
    "progress-committed": "pushed",
}


def prepare_integration(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    baseline_revision: str,
    now: int,
) -> dict[str, Any]:
    """Create or resume the publication journal owned by one leased action."""
    with immediate(connection):
        require_lease(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, now=now,
        )
        kind = connection.execute(
            "SELECT kind FROM action WHERE action_id = ?", (action_id,),
        ).fetchone()
        if kind is None or kind[0] not in {"integration", "gate-refresh"}:
            raise ValueError(f"action {action_id} is not a publication action")
        existing = connection.execute(
            """SELECT phase, baseline_revision, candidate_tree, candidate_commit,
                      gate_hash, progress_hash, remote_revision, updated_at
               FROM integration WHERE action_id = ?""",
            (action_id,),
        ).fetchone()
        if existing is None:
            connection.execute(
                """INSERT INTO integration(
                    action_id, phase, baseline_revision, updated_at
                ) VALUES(?, 'prepared', ?, ?)""",
                (action_id, baseline_revision, now),
            )
            connection.execute(
                """UPDATE attempt SET state = 'integrating', updated_at = ?
                   WHERE attempt_id IN (
                       SELECT attempt_id FROM action_attempt WHERE action_id = ?
                   ) AND state = 'green'""",
                (now, action_id),
            )
        elif existing[1] != baseline_revision:
            raise ValueError("integration baseline identity mismatch")
    return integration_status(connection, action_id)


def integration_status(
    connection: sqlite3.Connection,
    action_id: str,
) -> dict[str, Any]:
    row = connection.execute(
        """SELECT phase, baseline_revision, candidate_tree, candidate_commit,
                  gate_hash, progress_hash, remote_revision, updated_at
           FROM integration WHERE action_id = ?""",
        (action_id,),
    ).fetchone()
    if row is None:
        raise KeyError(action_id)
    keys = (
        "phase", "baseline_revision", "candidate_tree", "candidate_commit",
        "gate_hash", "progress_hash", "remote_revision", "updated_at",
    )
    return {"action_id": action_id, **dict(zip(keys, row, strict=True))}


def advance_integration(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    expected_phase: str,
    values: dict[str, str | None] | None,
    now: int,
) -> dict[str, Any]:
    next_phase = INTEGRATION_TRANSITIONS.get(expected_phase)
    if next_phase is None:
        raise ValueError(f"integration phase {expected_phase!r} cannot advance")
    allowed = {
        "candidate_tree", "candidate_commit", "gate_hash", "progress_hash",
        "remote_revision",
    }
    updates = values or {}
    if not set(updates) <= allowed:
        raise ValueError(f"unknown integration fields: {sorted(set(updates) - allowed)}")
    with immediate(connection):
        require_lease(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, now=now,
        )
        assignments = ["phase = ?", "updated_at = ?"]
        parameters: list[Any] = [next_phase, now]
        for key in sorted(updates):
            assignments.append(f"{key} = ?")
            parameters.append(updates[key])
        parameters.extend([action_id, expected_phase])
        cursor = connection.execute(
            f"""UPDATE integration SET {', '.join(assignments)}
                WHERE action_id = ? AND phase = ?""",
            parameters,
        )
        if cursor.rowcount != 1:
            raise ValueError(
                f"integration {action_id} is not in phase {expected_phase}"
            )
    return integration_status(connection, action_id)


def finalize_integration(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    remote_revision: str,
    now: int,
) -> dict[str, Any]:
    """Atomically mark published attempts, work, journal, and action complete."""
    with immediate(connection):
        require_lease(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, now=now,
        )
        phase = connection.execute(
            "SELECT phase FROM integration WHERE action_id = ?", (action_id,),
        ).fetchone()
        if phase is None or phase[0] != "pushed":
            raise ValueError(f"integration {action_id} is not pushed")
        attempt_ids = [
            row[0] for row in connection.execute(
                "SELECT attempt_id FROM action_attempt WHERE action_id = ?",
                (action_id,),
            )
        ]
        work_ids = [
            row[0] for row in connection.execute(
                "SELECT work_id FROM action_work WHERE action_id = ?",
                (action_id,),
            )
        ]
        connection.executemany(
            "UPDATE attempt SET state = 'landed', updated_at = ? WHERE attempt_id = ?",
            [(now, attempt_id) for attempt_id in attempt_ids],
        )
        connection.executemany(
            """UPDATE work SET canonical_state = 'complete', eligibility = 'complete',
                               not_before = 0, stop_kind = NULL
               WHERE work_id = ?""",
            [(work_id,) for work_id in work_ids],
        )
        connection.execute(
            """UPDATE integration SET phase = 'finalized', remote_revision = ?,
                                      updated_at = ?
               WHERE action_id = ?""",
            (remote_revision, now, action_id),
        )
        connection.execute(
            """INSERT INTO metadata(key, value) VALUES('source_revision', ?)
               ON CONFLICT(key) DO UPDATE SET value = excluded.value""",
            (remote_revision,),
        )
        connection.execute(
            """INSERT INTO projection_backlog(
                   backend, projection_key, source_hash, desired_json,
                   attempts, not_before
               ) VALUES('forgejo', ?, ?, ?, 0, 0)
               ON CONFLICT(backend, projection_key) DO UPDATE SET
                   source_hash = excluded.source_hash,
                   desired_json = excluded.desired_json,
                   not_before = 0""",
            (
                remote_revision, remote_revision,
                json.dumps(
                    {"kind": "full-reconcile", "revision": remote_revision},
                    sort_keys=True,
                ),
            ),
        )
        result = {
            "outcome": "productive",
            "published_revision": remote_revision,
            "attempt_ids": sorted(attempt_ids),
            "work_ids": sorted(work_ids),
        }
        finish_action_in_transaction(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, result=result, success=True, now=now,
        )
    return result


def finish_projection_action(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    now: int,
) -> dict[str, Any]:
    """Clear reconciled projection backlog and finish its leased action."""
    with immediate(connection):
        require_lease(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, now=now,
        )
        kind = connection.execute(
            "SELECT kind FROM action WHERE action_id = ?", (action_id,),
        ).fetchone()
        if kind is None or kind[0] != "projection-reconcile":
            raise ValueError(f"action {action_id} is not a projection action")
        count = connection.execute(
            "SELECT COUNT(*) FROM projection_backlog WHERE backend = 'forgejo'"
        ).fetchone()[0]
        connection.execute(
            "DELETE FROM projection_backlog WHERE backend = 'forgejo'"
        )
        result = {"outcome": "productive", "projection_rows": count}
        finish_action_in_transaction(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, result=result, success=True, now=now,
        )
    return result




def create_salvage_children_in_transaction(
    connection: sqlite3.Connection,
    parent_attempt_id: str,
    children: list[dict[str, Any]],
    *,
    now: int,
) -> list[str]:
    """Replace one attempt with immutable child attempts that exactly partition it."""
    parent = connection.execute(
        """SELECT generation, base_revision, inventory_hash, owned_paths_json,
                  model, state
           FROM attempt WHERE attempt_id = ?""",
        (parent_attempt_id,),
    ).fetchone()
    if parent is None:
        raise KeyError(parent_attempt_id)
    if parent[5] in {"landed", "superseded"}:
        raise ValueError(f"attempt {parent_attempt_id} is already terminal")
    parent_work = {
        row[0] for row in connection.execute(
            "SELECT work_id FROM attempt_work WHERE attempt_id = ?",
            (parent_attempt_id,),
        )
    }
    child_work = [
        {str(work_id) for work_id in child.get("work_ids", [])}
        for child in children
    ]
    if not children or any(not work_ids for work_ids in child_work):
        raise ValueError("salvage children must be non-empty")
    flattened = [work_id for work_ids in child_work for work_id in work_ids]
    if len(flattened) != len(set(flattened)) or set(flattened) != parent_work:
        raise ValueError("salvage children must exactly partition parent work")
    created: list[str] = []
    for child, work_ids in zip(children, child_work, strict=True):
        attempt_id = str(child["attempt_id"])
        try:
            uuid.UUID(attempt_id)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"invalid child attempt ID {attempt_id!r}") from exc
        snapshot = child.get("snapshot")
        if not isinstance(snapshot, dict):
            raise TypeError("salvage child snapshot must be an object")
        snapshot_work = {
            routine.get("work_id")
            for routine in snapshot.get("routines", [])
            if isinstance(routine, dict)
        }
        if snapshot_work != work_ids:
            raise ValueError(
                f"child {attempt_id} snapshot membership does not match work_ids"
            )
        cohort_id = common.cohort_id(work_ids)
        if snapshot.get("attempt_id") != attempt_id:
            raise ValueError(f"child {attempt_id} snapshot identity mismatch")
        if snapshot.get("cohort_id") != cohort_id:
            raise ValueError(f"child {attempt_id} cohort identity mismatch")
        child_state = str(child.get("state", "retry-ready"))
        if child_state not in {"green", "retry-ready", "blocked"}:
            raise ValueError(f"invalid salvage child state {child_state!r}")
        snapshot_json = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
        packet_hash = hashlib.sha256(snapshot_json.encode()).hexdigest()
        bundle_hash = child.get("bundle_sha256")
        if child_state == "green" and (
            not isinstance(bundle_hash, str) or len(bundle_hash) != 64
        ):
            raise ValueError("green salvage child requires bundle_sha256")
        connection.execute(
            """INSERT INTO attempt(
                   attempt_id, cohort_id, kind, parent_attempt_id, generation,
                   base_revision, inventory_hash, snapshot_json, owned_paths_json,
                   state, model, not_before, packet_sha256, bundle_sha256,
                   identity_valid, created_at, updated_at
               ) VALUES(?, ?, 'salvage-child', ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, 1, ?, ?)""",
            (
                attempt_id, cohort_id, parent_attempt_id, parent[0] + 1,
                parent[1], parent[2], snapshot_json, parent[3], child_state,
                child.get("model") or parent[4], packet_hash, bundle_hash,
                now, now,
            ),
        )
        for work_id in sorted(work_ids):
            connection.execute(
                "INSERT INTO attempt_work(attempt_id, work_id) VALUES(?, ?)",
                (attempt_id, work_id),
            )
            eligibility = (
                "green-integrating" if child_state == "green" else child_state
            )
            connection.execute(
                """UPDATE work SET current_attempt_id = ?, eligibility = ?,
                                  not_before = 0
                   WHERE work_id = ?""",
                (attempt_id, eligibility, work_id),
            )
        created.append(attempt_id)
    connection.execute(
        "UPDATE attempt SET state = 'superseded', updated_at = ? WHERE attempt_id = ?",
        (now, parent_attempt_id),
    )
    return created



def finish_action(
    connection: sqlite3.Connection,
    action_id: str,
    *,
    lease_owner: str,
    lease_token: str,
    result: dict[str, Any],
    success: bool,
    now: int,
) -> None:
    with immediate(connection):
        finish_action_in_transaction(
            connection, action_id, lease_owner=lease_owner,
            lease_token=lease_token, result=result, success=success, now=now,
        )


def _relative(path: Path) -> str:
    return path.relative_to(common.ROOT).as_posix()


def _input_paths() -> list[Path]:
    paths = {path for path in INPUT_FILES if path.is_file()}
    for root in INPUT_TREES:
        if root.is_dir():
            paths.update(path for path in root.rglob("*") if path.is_file())
    return sorted(paths, key=_relative)


def _capture_inputs() -> dict[str, bytes]:
    return {_relative(path): path.read_bytes() for path in _input_paths()}


def _input_rows(blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "size": len(blob)}
        for path, blob in sorted(blobs.items())
    ]


def _source_digest(rows: list[dict[str, Any]], revision: str | None) -> str:
    digest = hashlib.sha256()
    digest.update((revision or "revision-unavailable").encode())
    digest.update(b"\0")
    for row in rows:
        digest.update(row["path"].encode())
        digest.update(b"\0")
        digest.update(row["sha256"].encode())
        digest.update(b"\0")
        digest.update(str(row["size"]).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def _json_blob(blobs: dict[str, bytes], path: str) -> dict | None:
    raw = blobs.get(path)
    if raw is None:
        return None
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain one JSON object")
    return value


def _load_progress_projection() -> tuple[Any, dict, dict | None, str | None, str]:
    path = common.ROOT / "tools/progress/report.py"
    spec = importlib.util.spec_from_file_location("factory_state_progress", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load progress projection")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        inventory = module.load_inventory()
        routines, _ = module.load_routines()
        gate = module.load_gate()
        report = module.compute(inventory, routines, gate)
        revision = module.current_revision()
    return module, report, gate, revision, captured.getvalue().strip()


def _cohort(work_ids: list[str]) -> str:
    return common.cohort_id(work_ids)


def _failure_fingerprint(row: dict) -> str:
    existing = row.get("fingerprint")
    if isinstance(existing, str) and len(existing) == 64:
        return existing
    payload = "\0".join(str(row.get(key, "")) for key in (
        "phase", "status", "failure_class", "detail", "reason",
    ))
    return hashlib.sha256(payload.encode()).hexdigest()


def _mapped_state(raw: Any) -> str:
    state = str(raw or "pending")
    aliases = {
        "escalated": "retry-ready",
        "rejected-format": "retry-ready",
        "parked": "blocked",
        "reset-stale": "pending",
        "reset-infra": "pending",
    }
    state = aliases.get(state, state)
    return state if state in ATTEMPT_STATES else "stopped"


def _bundle_digests(rows: list[dict[str, Any]]) -> dict[str, str]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    prefix = ".factory/bundles/"
    for row in rows:
        if not row["path"].startswith(prefix):
            continue
        remainder = row["path"][len(prefix):]
        attempt_id, separator, relative = remainder.partition("/")
        if separator:
            grouped[attempt_id].append({**row, "relative": relative})
    result = {}
    for attempt_id, files in grouped.items():
        digest = hashlib.sha256()
        for row in sorted(files, key=lambda item: item["relative"]):
            digest.update(row["relative"].encode())
            digest.update(b"\0")
            digest.update(row["sha256"].encode())
            digest.update(b"\0")
            digest.update(str(row["size"]).encode())
            digest.update(b"\n")
        result[attempt_id] = digest.hexdigest()
    return result


def _attempt_kind(packet: dict, generation: int) -> str:
    if packet.get("kind") == "dependency-group" or packet.get("group_id"):
        return "dependency-group"
    if packet.get("parent_attempt_id") or generation > 0 or packet.get("rounds", 0):
        return "recovery"
    return "fresh"



def _owned_paths(packet: dict) -> list[str]:
    explicit = packet.get("owned_paths")
    if isinstance(explicit, list) and all(isinstance(path, str) for path in explicit):
        return sorted(set(explicit))
    source = packet.get("file")
    basename = packet.get("basename")
    if not isinstance(source, str) or not isinstance(basename, str):
        return []
    c_source = str(Path(source).with_suffix(".c"))
    h_source = str(Path(source).with_suffix(".h"))
    return sorted({
        c_source,
        h_source,
        f"src/probe/{basename}.c",
        f"tests/cases/{basename}.py",
    })

def _packet_work_ids(packet: dict) -> list[str]:
    work_ids = []
    for routine in packet.get("routines", []):
        work_id = routine.get("work_id") if isinstance(routine, dict) else None
        if not work_id and isinstance(routine, dict):
            source = routine.get("file")
            name = routine.get("name")
            if source and name:
                work_id = f"port:v1:{source}:{name}"
        if isinstance(work_id, str):
            work_ids.append(work_id)
    return work_ids


def _import_attempts(
    connection: sqlite3.Connection,
    blobs: dict[str, bytes],
    input_rows: list[dict[str, Any]],
    known_work: set[str],
) -> dict[str, Any]:
    bundle_digests = _bundle_digests(input_rows)
    records = []
    invalid = []
    raw_to_attempt: dict[str, str] = {}
    used_attempt_ids: set[str] = set()
    retired: set[str] = set()
    queue_prefix = ".factory/queue/"
    for path, blob in sorted(blobs.items()):
        if not path.startswith(queue_prefix) or not path.endswith(".json"):
            continue
        try:
            packet = json.loads(blob)
            if not isinstance(packet, dict):
                raise TypeError("packet is not an object")
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            invalid.append({"path": path, "active": True, "errors": [str(exc)]})
            continue
        packet_hash = hashlib.sha256(blob).hexdigest()
        raw_id = str(packet.get("attempt_id") or packet.get("id") or Path(path).stem)
        candidate = raw_id
        try:
            uuid.UUID(candidate)
        except ValueError:
            candidate = common.legacy_attempt_id(raw_id, packet_hash)
        if candidate in used_attempt_ids:
            candidate = str(uuid.uuid5(ACTION_NAMESPACE, f"{path}\0{packet_hash}"))
        used_attempt_ids.add(candidate)
        raw_to_attempt[raw_id] = candidate
        raw_to_attempt[str(packet.get("id") or raw_id)] = candidate
        legacy_packet_id = packet.get("legacy_packet_id")
        if legacy_packet_id:
            raw_to_attempt[str(legacy_packet_id)] = candidate
        work_ids = _packet_work_ids(packet)
        unknown = sorted(set(work_ids) - known_work)
        retired.update(unknown)
        errors = []
        try:
            common.validate_packet(packet)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(str(exc))
        if len(work_ids) != len(set(work_ids)):
            errors.append("duplicate work IDs inside packet")
        if not work_ids:
            errors.append("packet has no recoverable work IDs")
        state = _mapped_state(packet.get("state"))
        active = state not in HISTORICAL
        identity_valid = not errors and not unknown
        if errors or unknown:
            invalid.append({
                "path": path,
                "attempt_id": candidate,
                "active": active,
                "errors": errors,
                "unknown_work_ids": unknown,
            })
        generation = packet.get("attempt_generation", packet.get("generation", 0))
        generation = generation if isinstance(generation, int) and generation >= 0 else 0
        cohort = packet.get("cohort_id")
        if not isinstance(cohort, str) or len(cohort) != 64:
            cohort = _cohort(work_ids)
        records.append({
            "path": path,
            "packet": packet,
            "attempt_id": candidate,
            "raw_id": raw_id,
            "work_ids": sorted(set(work_ids) & known_work),
            "unknown_work_ids": unknown,
            "state": state,
            "active": active,
            "identity_valid": identity_valid,
            "generation": generation,
            "cohort_id": cohort,
            "packet_hash": packet_hash,
            "bundle_hash": bundle_digests.get(raw_id) or bundle_digests.get(candidate),
        })
    known_attempts = {record["attempt_id"] for record in records}
    for record in records:
        packet = record["packet"]
        parent = packet.get("parent_attempt_id")
        parent = raw_to_attempt.get(str(parent), str(parent)) if parent else None
        if parent not in known_attempts:
            parent = None
        created = packet.get("created_at", packet.get("updated_at", 0))
        updated = packet.get("updated_at", created)
        created = int(created) if isinstance(created, (int, float)) else 0
        updated = int(updated) if isinstance(updated, (int, float)) else created
        connection.execute(
            """INSERT INTO attempt(
                attempt_id, legacy_packet_id, cohort_id, kind, parent_attempt_id,
                generation, base_revision, inventory_hash, snapshot_json,
                owned_paths_json, state, model, not_before, packet_sha256,
                bundle_sha256, identity_valid, created_at, updated_at
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record["attempt_id"], record["raw_id"], record["cohort_id"],
                _attempt_kind(packet, record["generation"]), parent,
                record["generation"], packet.get("base_commit"),
                packet.get("inventory_hash"),
                json.dumps(packet, sort_keys=True, separators=(",", ":")),
                json.dumps(_owned_paths(packet), sort_keys=True),
                record["state"], packet.get("model"),
                int(packet.get("not_before", 0) or 0), record["packet_hash"],
                record["bundle_hash"], int(record["identity_valid"]), created, updated,
            ),
        )
        for work_id in record["work_ids"]:
            connection.execute(
                "INSERT INTO attempt_work(attempt_id, work_id) VALUES(?, ?)",
                (record["attempt_id"], work_id),
            )
        history = packet.get("failure_history", [])
        if not isinstance(history, list):
            history = []
        inserted_history = False
        for failure in history:
            if not isinstance(failure, dict):
                continue
            inserted_history = True
            detail = str(failure.get("detail") or failure.get("reason") or "legacy failure")
            connection.execute(
                """INSERT INTO failure(
                    attempt_id, phase, status, failure_class, fingerprint, detail,
                    model, observed_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record["attempt_id"], str(failure.get("phase") or "legacy"),
                    str(failure.get("status") or "failed"),
                    str(failure.get("failure_class") or "unknown"),
                    _failure_fingerprint(failure), detail, failure.get("model"),
                    int(failure.get("observed_at", failure.get("at", updated)) or updated),
                ),
            )
        has_legacy_failure = (
            record["state"] in RETRY_STATES
            or record["state"] == "blocked"
            or packet.get("reason")
            or packet.get("failure_class")
            or packet.get("rounds")
        )
        if has_legacy_failure and not inserted_history:
            detail = json.dumps({
                "generation": record["generation"],
                "reason": packet.get("reason"),
                "rounds": packet.get("rounds", 0),
                "state": record["state"],
            }, sort_keys=True)
            evidence = {
                "phase": "legacy-current-state",
                "status": record["state"],
                "failure_class": packet.get("failure_class") or "unknown",
                "detail": detail,
            }
            connection.execute(
                """INSERT INTO failure(
                    attempt_id, phase, status, failure_class, fingerprint, detail,
                    model, observed_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record["attempt_id"], evidence["phase"], evidence["status"],
                    evidence["failure_class"], _failure_fingerprint(evidence), detail,
                    packet.get("model"), updated,
                ),
            )
    unmatched_bundles = sorted(set(bundle_digests) - set(raw_to_attempt) - known_attempts)
    return {
        "records": records,
        "raw_to_attempt": raw_to_attempt,
        "invalid": sorted(invalid, key=lambda item: item["path"]),
        "retired_work_ids": sorted(retired),
        "bundle_digests": bundle_digests,
        "unmatched_bundles": unmatched_bundles,
    }


def _import_metric_failures(
    connection: sqlite3.Connection,
    blobs: dict[str, bytes],
    attempts: dict[str, Any],
) -> dict[str, Any]:
    raw = blobs.get(".factory/metrics.jsonl")
    if raw is None:
        return {"imported": 0, "unmatched_ids": [], "malformed_lines": []}
    unmatched = set()
    malformed = []
    imported = 0
    by_attempt = {record["attempt_id"]: record for record in attempts["records"]}
    for line_number, line in enumerate(raw.decode(errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            metric = json.loads(line)
            if not isinstance(metric, dict):
                raise TypeError("metric is not an object")
        except (json.JSONDecodeError, TypeError) as exc:
            malformed.append({"line": line_number, "error": str(exc)})
            continue
        verdict = str(metric.get("verdict") or "unknown")
        if verdict in {"green", "landed", "complete"}:
            continue
        raw_id = str(metric.get("attempt_id") or metric.get("id") or "")
        attempt_id = attempts["raw_to_attempt"].get(raw_id, raw_id)
        if not raw_id or attempt_id not in by_attempt:
            unmatched.add(raw_id or f"line:{line_number}")
            continue
        detail = json.dumps({
            "reason": metric.get("reason"),
            "rounds": metric.get("rounds"),
            "verdict": verdict,
            "wall_s": metric.get("wall_s"),
        }, sort_keys=True)
        evidence = {
            "phase": "legacy-metric",
            "status": verdict,
            "failure_class": metric.get("failure_class") or "unknown",
            "detail": detail,
        }
        connection.execute(
            """INSERT INTO failure(
                attempt_id, phase, status, failure_class, fingerprint, detail,
                model, observed_at
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                attempt_id, evidence["phase"], evidence["status"],
                evidence["failure_class"], _failure_fingerprint(evidence), detail,
                metric.get("model"), int(metric.get("ts", 0) or 0),
            ),
        )
        imported += 1
    return {
        "imported": imported,
        "unmatched_ids": sorted(unmatched),
        "malformed_lines": malformed,
    }


def _set_work_ownership(
    connection: sqlite3.Connection,
    work_records: list[dict],
    attempts: dict[str, Any],
) -> dict[str, Any]:
    valid_owners: dict[str, list[dict]] = defaultdict(list)
    invalid_owners: dict[str, list[str]] = defaultdict(list)
    for record in attempts["records"]:
        if not record["active"]:
            continue
        target = valid_owners if record["identity_valid"] else invalid_owners
        for work_id in record["work_ids"]:
            if record["identity_valid"]:
                target[work_id].append(record)
            else:
                target[work_id].append(record["attempt_id"])
    duplicates = {
        work_id: sorted(record["attempt_id"] for record in owners)
        for work_id, owners in valid_owners.items() if len(owners) > 1
    }
    falsely_completed = []
    partition: dict[str, list[str]] = defaultdict(list)
    resolution = []
    by_work = {row["work_id"]: row for row in work_records if row.get("work_id")}
    for work_id, row in sorted(by_work.items()):
        canonical = row.get("state", "unknown")
        owners = valid_owners.get(work_id, [])
        invalid = invalid_owners.get(work_id, [])
        owner = owners[0] if len(owners) == 1 and not invalid else None
        if canonical in {"complete", "excluded"}:
            eligibility = canonical
            if owners or invalid:
                falsely_completed.append(work_id)
                owner = None
        elif invalid or len(owners) > 1:
            eligibility = "external-stop"
            resolution.append({
                "work_id": work_id,
                "reason": "invalid-or-ambiguous-active-owner",
                "attempt_ids": sorted([record["attempt_id"] for record in owners] + invalid),
            })
        elif canonical == "blocked":
            eligibility = "blocked"
            owner = None
        elif owner:
            state = owner["state"]
            packet = owner["packet"]
            if state in {"green", "integrating"}:
                eligibility = "green-integrating"
            elif state == "blocked":
                eligibility = "blocked"
            elif state == "pending" and owner["generation"] == 0 and not packet.get("rounds"):
                eligibility = "fresh-ready"
            else:
                eligibility = "retry-ready"
        elif canonical in {"ready", "awaiting-gate"}:
            eligibility = "fresh-ready"
        elif canonical == "failing":
            eligibility = "retry-ready"
        else:
            eligibility = "external-stop"
            resolution.append({"work_id": work_id, "reason": f"unknown-canonical-state:{canonical}"})
        recovery_tier = 0
        diagnostic_count = 0
        repeated_count = 0
        last_fingerprint = None
        not_before = 0
        if owner and eligibility == "retry-ready":
            recovery_tier = min(owner["generation"], 4)
            fingerprints = [
                failure[0]
                for failure in connection.execute(
                    """SELECT fingerprint FROM failure
                       WHERE attempt_id = ? ORDER BY observed_at, failure_id""",
                    (owner["attempt_id"],),
                )
            ]
            diagnostic_count = len(fingerprints)
            if fingerprints:
                last_fingerprint = fingerprints[-1]
                repeated_count = fingerprints.count(last_fingerprint)
            not_before = int(owner["packet"].get("not_before", 0) or 0)
        connection.execute(
            """UPDATE work SET eligibility = ?, current_attempt_id = ?,
                      recovery_tier = ?, diagnostic_count = ?,
                      repeated_fingerprint_count = ?,
                      last_failure_fingerprint = ?, not_before = ?
               WHERE work_id = ?""",
            (
                eligibility, owner["attempt_id"] if owner else None,
                recovery_tier, diagnostic_count, repeated_count,
                last_fingerprint, not_before, work_id,
            ),
        )
        partition[eligibility].append(work_id)
    return {
        "partition": {key: sorted(value) for key, value in sorted(partition.items())},
        "duplicate_owner_candidates": duplicates,
        "invalid_owner_candidates": {
            key: sorted(value) for key, value in sorted(invalid_owners.items())
        },
        "falsely_completed_work_ids": sorted(falsely_completed),
        "resolution_plan": resolution,
    }


def _import_blockers(connection: sqlite3.Connection, work_records: list[dict]) -> list[dict]:
    by_name: dict[str, list[str]] = defaultdict(list)
    for row in work_records:
        if row.get("work_id"):
            by_name[row["name"]].append(row["work_id"])
    unresolved = []
    for row in work_records:
        work_id = row.get("work_id")
        if not work_id:
            continue
        operational = row.get("operational_blocker")
        if operational:
            connection.execute(
                """INSERT OR IGNORE INTO blocker(
                    work_id, kind, blocked_on_work_id, reason, unblock, source, active
                ) VALUES(?, 'operational', NULL, ?, ?, 'blocked.toml', 1)""",
                (work_id, operational["reason"], operational["unblock"]),
            )
        for name in row.get("blockers") or []:
            targets = by_name.get(name, [])
            if len(targets) != 1:
                unresolved.append({"work_id": work_id, "blocker": name, "matches": targets})
                continue
            connection.execute(
                """INSERT OR IGNORE INTO blocker(
                    work_id, kind, blocked_on_work_id, reason, unblock, source, active
                ) VALUES(?, 'dependency', ?, ?, ?, 'progress', 1)""",
                (work_id, targets[0], f"depends on {name}", f"complete {name}"),
            )
    return unresolved


def _stable_action_id(journal: dict, source_digest: str) -> str:
    candidate = journal.get("action_id") or journal.get("transaction_id")
    if candidate:
        try:
            return str(uuid.UUID(str(candidate)))
        except ValueError:
            pass
    return str(uuid.uuid5(ACTION_NAMESPACE, f"{source_digest}\0{json.dumps(journal, sort_keys=True)}"))


def _import_legacy_action(
    connection: sqlite3.Connection,
    journal: dict | None,
    attempts: dict[str, Any],
    source_digest: str,
    revision: str | None,
) -> dict | None:
    if not journal:
        return None
    action_id = _stable_action_id(journal, source_digest)
    old_phase = str(journal.get("phase") or "unknown")
    packet_ids = [str(value) for value in journal.get("packet_ids", [])]
    by_attempt = {record["attempt_id"]: record for record in attempts["records"]}
    resolved = []
    missing = []
    for packet_id in packet_ids:
        attempt_id = attempts["raw_to_attempt"].get(packet_id, packet_id)
        if attempt_id in by_attempt:
            resolved.append(attempt_id)
        else:
            missing.append(packet_id)
    expected_base = journal.get("base_commit")
    base_mismatches = [
        attempt_id for attempt_id in resolved
        if expected_base and by_attempt[attempt_id]["packet"].get("base_commit") != expected_base
    ]
    state_mismatches = [
        {"attempt_id": attempt_id, "state": by_attempt[attempt_id]["state"]}
        for attempt_id in resolved if by_attempt[attempt_id]["state"] != "translating"
    ]
    expected_hashes = journal.get("packet_hashes") if isinstance(journal.get("packet_hashes"), dict) else {}
    hash_mismatches = [
        attempt_id for attempt_id in resolved
        if expected_hashes.get(attempt_id) != by_attempt[attempt_id]["packet_hash"]
    ] if expected_hashes else []
    disposition = "recovering" if old_phase in {"planned", "running"} else "expired"
    result = {
        "source": ".factory/supervisor.json",
        "action_id": action_id,
        "old_phase": old_phase,
        "planned_phase": "recovering",
        "planned_status": "expired",
        "disposition": disposition,
        "packet_ids": packet_ids,
        "resolved_attempt_ids": sorted(resolved),
        "missing_packet_ids": sorted(missing),
        "packet_state_mismatches": state_mismatches,
        "packet_base_mismatches": sorted(base_mismatches),
        "packet_hash_validation": "compared" if expected_hashes else "missing-from-legacy-journal",
        "packet_hash_mismatches": sorted(hash_mismatches),
        "journal_base": expected_base,
        "current_revision": revision,
    }
    now = int(journal.get("started_at", journal.get("updated_at", 0)) or 0)
    connection.execute(
        """INSERT INTO action(
            action_id, kind, idempotency_key, phase, status, recoverable,
            input_digest, frontier_digest, not_before, result_json, created_at, updated_at
        ) VALUES(?, ?, ?, 'recovering', 'expired', 0, ?, ?, 0, ?, ?, ?)""",
        (
            action_id, str(journal.get("kind") or "legacy"),
            f"legacy-supervisor:{source_digest}", source_digest,
            journal.get("frontier_digest"), json.dumps(result, sort_keys=True), now, now,
        ),
    )
    for attempt_id in sorted(set(resolved)):
        connection.execute(
            "INSERT INTO action_attempt(action_id, attempt_id, role) VALUES(?, ?, 'legacy-member')",
            (action_id, attempt_id),
        )
        for work_id, in connection.execute(
            "SELECT work_id FROM attempt_work WHERE attempt_id = ?",
            (attempt_id,),
        ):
            connection.execute(
                """INSERT OR IGNORE INTO action_work(action_id, work_id, role)
                   VALUES(?, ?, 'legacy-member')""",
                (action_id, work_id),
            )
    return result


def _import_integration(
    connection: sqlite3.Connection,
    journal: dict | None,
    attempts: dict[str, Any],
    source_digest: str,
) -> dict | None:
    if not journal:
        return None
    action_id = _stable_action_id(journal, source_digest)
    exists = connection.execute(
        "SELECT 1 FROM action WHERE action_id = ?", (action_id,),
    ).fetchone()
    now = int(journal.get("updated_at", journal.get("started_at", 0)) or 0)
    if not exists:
        connection.execute(
            """INSERT INTO action(
                action_id, kind, idempotency_key, phase, status, recoverable,
                input_digest, not_before, created_at, updated_at
            ) VALUES(?, 'integration', ?, 'recovering', 'expired', 0, ?, 0, ?, ?)""",
            (action_id, f"legacy-integration:{source_digest}", source_digest, now, now),
        )
    old_phase = str(journal.get("phase") or "failed")
    phase = old_phase if old_phase in {
        "prepared", "applied", "source-committed", "gate-passed",
        "progress-committed", "pushed", "finalized",
    } else "failed"
    connection.execute(
        """INSERT INTO integration(
            action_id, phase, baseline_revision, candidate_tree, candidate_commit,
            gate_hash, progress_hash, remote_revision, updated_at
        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            action_id, phase, journal.get("baseline"), journal.get("candidate_tree"),
            journal.get("candidate_commit"), journal.get("gate_hash"),
            journal.get("progress_hash"), journal.get("remote_revision"), now,
        ),
    )
    return {
        "source": ".factory/integration.json",
        "action_id": action_id,
        "old_phase": old_phase,
        "planned_phase": phase,
        "packet_ids": sorted(str(value) for value in journal.get("packet_ids", [])),
    }


def _import_projection_backlog(connection: sqlite3.Connection, marker: dict | None) -> int:
    if not marker:
        return 0
    connection.execute(
        """INSERT INTO projection_backlog(
            backend, projection_key, source_hash, desired_json, attempts, not_before
        ) VALUES('forgejo', 'legacy-residual', NULL, ?, 0, ?)""",
        (json.dumps(marker, sort_keys=True), int(marker.get("not_before", 0) or 0)),
    )
    return 1


def _database_counts(connection: sqlite3.Connection) -> dict[str, int]:
    tables = (
        "metadata", "source_input", "work", "attempt", "attempt_work", "failure",
        "action", "action_attempt", "action_work", "integration", "blocker",
        "projection_backlog",
    )
    return {
        table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in tables
    }


def audit_legacy(*, destination: Path | None = None) -> dict[str, Any]:
    """Build and audit the proposed authority, optionally publishing it atomically."""
    if destination is not None and destination.exists():
        raise FileExistsError(f"transactional state already exists: {destination}")
    state_exists_before = common.STATE_DB.exists()
    blobs = _capture_inputs()
    rows = _input_rows(blobs)
    report_module, report, gate, revision, projection_log = _load_progress_projection()
    source_digest = _source_digest(rows, revision)
    connection = sqlite3.connect(":memory:", isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")
    create_schema(connection)
    connection.execute("BEGIN IMMEDIATE")
    try:
        connection.execute(
            "INSERT INTO metadata(key, value) VALUES('source_digest', ?)",
            (source_digest,),
        )
        connection.execute(
            "INSERT INTO metadata(key, value) VALUES('source_revision', ?)",
            (revision or "",),
        )
        for row in rows:
            connection.execute(
                "INSERT INTO source_input(path, sha256, size) VALUES(?, ?, ?)",
                (row["path"], row["sha256"], row["size"]),
            )
        work_records = [row for row in report.get("work_records", []) if row.get("work_id")]
        for row in sorted(work_records, key=lambda item: item["work_id"]):
            connection.execute(
                """INSERT INTO work(
                    work_id, source, name, line, size, canonical_state, eligibility
                ) VALUES(?, ?, ?, ?, ?, ?, 'unclassified')""",
                (
                    row["work_id"], row.get("source"), row["name"], row.get("line"),
                    int(row.get("size", 0)), str(row.get("state") or "unknown"),
                ),
            )
        known_work = {row["work_id"] for row in work_records}
        attempts = _import_attempts(connection, blobs, rows, known_work)
        metric_evidence = _import_metric_failures(connection, blobs, attempts)
        ownership = _set_work_ownership(connection, work_records, attempts)
        unresolved_blockers = _import_blockers(connection, work_records)
        legacy_action = _import_legacy_action(
            connection, _json_blob(blobs, ".factory/supervisor.json"), attempts,
            source_digest, revision,
        )
        legacy_integration = _import_integration(
            connection, _json_blob(blobs, ".factory/integration.json"), attempts,
            source_digest,
        )
        projection_rows = _import_projection_backlog(
            connection, _json_blob(blobs, ".factory/forgejo-sync.json"),
        )
        connection.execute("COMMIT")
    except Exception:
        connection.execute("ROLLBACK")
        connection.close()
        raise

    gate_status = report_module.gate_is_trusted(gate, revision=revision)
    inventory = (gate or {}).get("inventory") if isinstance(gate, dict) else None
    gate_green = bool(
        gate_status and isinstance(inventory, dict)
        and not inventory.get("failures", 0)
        and not inventory.get("primary_missing", 0)
    )
    gate_reason = (
        "green" if gate_green else "gate-failures" if gate_status
        else "missing-or-stale-gate"
    )
    partition = ownership["partition"]
    managed_unfinished = sorted(
        row["work_id"] for row in work_records
        if row.get("state") not in {"complete", "excluded"}
    )
    allowed = {"fresh-ready", "retry-ready", "blocked", "green-integrating", "external-stop"}
    projected_unfinished = sorted(
        work_id for key, values in partition.items() if key in allowed for work_id in values
    )
    residual = sorted(set(managed_unfinished) ^ set(projected_unfinished))
    repeated = sorted(
        work_id for work_id, count in Counter(projected_unfinished).items() if count != 1
    )
    foreign_keys = [list(row) for row in connection.execute("PRAGMA foreign_key_check")]
    integrity = [row[0] for row in connection.execute("PRAGMA integrity_check")]
    counts = _database_counts(connection)
    temporary_state = None
    if destination is not None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary_state = destination.with_name(
            f".{destination.name}.migrate-{os.getpid()}-{uuid.uuid4().hex}"
        )
        target = sqlite3.connect(temporary_state)
        try:
            connection.backup(target)
        finally:
            target.close()
    connection.close()

    after_blobs = _capture_inputs()
    before_rows = {row["path"]: row for row in rows}
    after_rows = {row["path"]: row for row in _input_rows(after_blobs)}
    drift = sorted(
        path for path in set(before_rows) | set(after_rows)
        if before_rows.get(path) != after_rows.get(path)
    )
    active_invalid = [row for row in attempts["invalid"] if row.get("active")]
    ok = not any((
        drift,
        foreign_keys,
        metric_evidence["malformed_lines"],
        integrity != ["ok"],
        residual,
        repeated,
        ownership["duplicate_owner_candidates"],
        ownership["falsely_completed_work_ids"],
        active_invalid,
        common.STATE_DB.exists() != state_exists_before,
    ))
    if destination is not None:
        if not ok:
            if temporary_state is not None and temporary_state.exists():
                temporary_state.unlink()
            raise RuntimeError("legacy state audit failed; transactional state not published")
        if temporary_state is None:
            raise RuntimeError("migration did not produce a database image")
        with temporary_state.open("rb") as descriptor:
            os.fsync(descriptor.fileno())
        os.replace(temporary_state, destination)
        directory_fd = os.open(destination.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    return {
        "schema_version": SCHEMA_VERSION,
        "ok": ok,
        "source_digest": source_digest,
        "source_revision": revision,
        "inputs": rows,
        "input_drift": drift,
        "database_created": destination is not None,
        "state_path_exists": common.STATE_DB.exists(),
        "would_create_state_path": _relative(common.STATE_DB),
        "projection_log": projection_log,
        "inventory": {
            "pret_commit": report.get("pret_commit"),
            "work_records": len(work_records),
            "managed": sum(not row.get("excluded") for row in work_records),
            "managed_unfinished": len(managed_unfinished),
            "measures": report.get("measures", {}),
        },
        "gate": {"current": bool(gate_status), "green": gate_green, "reason": gate_reason},
        "rows": counts,
        "partition_counts": {key: len(value) for key, value in sorted(partition.items())},
        "unfinished_partition_counts": {
            key: len(partition.get(key, [])) for key in sorted(allowed)
        },
        "residual_work_ids": residual,
        "repeated_partition_work_ids": repeated,
        "invalid_packet_identities": attempts["invalid"],
        "active_invalid_packet_identities": active_invalid,
        "duplicate_owner_candidates": ownership["duplicate_owner_candidates"],
        "invalid_owner_candidates": ownership["invalid_owner_candidates"],
        "falsely_completed_work_ids": ownership["falsely_completed_work_ids"],
        "resolution_plan": ownership["resolution_plan"],
        "retired_work_ids": attempts["retired_work_ids"],
        "unmatched_bundle_attempt_ids": attempts["unmatched_bundles"],
        "metric_evidence": metric_evidence,
        "unresolved_blockers": unresolved_blockers,
        "legacy_action": legacy_action,
        "legacy_integration": legacy_integration,
        "projection_backlog_rows": projection_rows,
        "foreign_key_check": foreign_keys,
        "integrity_check": integrity,
    }
