#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import forgejo
import ledger

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / ".factory" / "v2"
CACHE_PATH = CACHE_DIR / "cache.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS issue_cache (
    number INTEGER PRIMARY KEY,
    fingerprint TEXT NOT NULL,
    updated_at TEXT,
    payload TEXT NOT NULL,
    dependencies TEXT NOT NULL,
    comments_cursor TEXT
) STRICT;
CREATE TABLE IF NOT EXISTS comment_cache (
    issue_number INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    updated_at TEXT,
    payload TEXT NOT NULL,
    PRIMARY KEY(issue_number, comment_id)
) STRICT;
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) STRICT;
"""


def open_cache(path: Path = CACHE_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.executescript(SCHEMA)
    return connection


def _managed(issue: dict[str, Any]) -> bool:
    return ledger.work_marker(issue) is not None or ledger.control_marker(issue) is not None


def _cursor(value: str | None) -> str | None:
    parsed = forgejo.parse_time(value)
    if parsed is None:
        return None
    return (parsed - timedelta(minutes=5)).isoformat()


def refresh(
    client: forgejo.ForgejoClient,
    *,
    path: Path = CACHE_PATH,
    full: bool = False,
) -> dict[str, Any]:
    snapshot = client.stable_snapshot()
    connection = open_cache(path)
    changed = 0
    comments_read = 0
    try:
        connection.execute("BEGIN IMMEDIATE")
        listed_numbers = {issue["number"] for issue in snapshot["issues"]}
        connection.execute(
            "DELETE FROM issue_cache WHERE number NOT IN ("
            + ",".join("?" for _ in listed_numbers)
            + ")" if listed_numbers else "DELETE FROM issue_cache",
            tuple(sorted(listed_numbers)),
        )
        if listed_numbers:
            connection.execute(
                "DELETE FROM comment_cache WHERE issue_number NOT IN ("
                + ",".join("?" for _ in listed_numbers)
                + ")",
                tuple(sorted(listed_numbers)),
            )
        for issue in snapshot["issues"]:
            if not _managed(issue):
                continue
            number = int(issue["number"])
            fingerprint = forgejo.issue_fingerprint(issue)
            row = connection.execute(
                "SELECT fingerprint, comments_cursor FROM issue_cache WHERE number = ?",
                (number,),
            ).fetchone()
            needs_refresh = full or row is None or row[0] != fingerprint
            if needs_refresh:
                since = None if full or row is None else _cursor(row[1])
                comments = client.comments_since(number, since)
                dependencies = client.dependencies(number)
                for comment in comments:
                    connection.execute(
                        """INSERT INTO comment_cache(issue_number, comment_id, updated_at, payload)
                           VALUES(?, ?, ?, ?)
                           ON CONFLICT(issue_number, comment_id) DO UPDATE SET
                           updated_at = excluded.updated_at, payload = excluded.payload""",
                        (
                            number,
                            int(comment["id"]),
                            comment.get("updated_at"),
                            forgejo.canonical_json(comment),
                        ),
                    )
                latest = max(
                    (str(comment.get("updated_at") or comment.get("created_at") or "") for comment in comments),
                    default=row[1] if row else None,
                )
                connection.execute(
                    """INSERT INTO issue_cache(number, fingerprint, updated_at, payload, dependencies, comments_cursor)
                       VALUES(?, ?, ?, ?, ?, ?)
                       ON CONFLICT(number) DO UPDATE SET
                       fingerprint = excluded.fingerprint,
                       updated_at = excluded.updated_at,
                       payload = excluded.payload,
                       dependencies = excluded.dependencies,
                       comments_cursor = excluded.comments_cursor""",
                    (
                        number,
                        fingerprint,
                        issue.get("updated_at"),
                        forgejo.canonical_json(issue),
                        forgejo.canonical_json(dependencies),
                        latest,
                    ),
                )
                changed += 1
                comments_read += len(comments)
            elif row is not None:
                connection.execute(
                    "UPDATE issue_cache SET payload = ?, updated_at = ? WHERE number = ?",
                    (forgejo.canonical_json(issue), issue.get("updated_at"), number),
                )
        connection.execute(
            "INSERT INTO metadata(key, value) VALUES('snapshot_sha256', ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (str(snapshot["sha256"]),),
        )
        connection.execute(
            "INSERT INTO metadata(key, value) VALUES('refreshed_at', ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (datetime.now(UTC).isoformat(),),
        )
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()
    return {
        "snapshot_sha256": snapshot["sha256"],
        "issues": len(snapshot["issues"]),
        "changed": changed,
        "comments_read": comments_read,
    }


def load(path: Path = CACHE_PATH) -> dict[str, Any]:
    connection = open_cache(path)
    try:
        rows = connection.execute(
            "SELECT number, payload, dependencies FROM issue_cache ORDER BY number"
        ).fetchall()
        issues: list[dict[str, Any]] = []
        comments: dict[int, list[dict[str, Any]]] = {}
        dependencies: dict[int, list[dict[str, Any]]] = {}
        for number, payload, raw_dependencies in rows:
            issues.append(json.loads(payload))
            dependencies[int(number)] = json.loads(raw_dependencies)
            comments[int(number)] = [
                json.loads(raw)
                for raw, in connection.execute(
                    "SELECT payload FROM comment_cache WHERE issue_number = ? ORDER BY comment_id",
                    (number,),
                )
            ]
        metadata = {
            key: value
            for key, value in connection.execute("SELECT key, value FROM metadata")
        }
        return {
            "issues": issues,
            "comments": comments,
            "dependencies": dependencies,
            "snapshot_sha256": metadata.get("snapshot_sha256"),
            "refreshed_at": metadata.get("refreshed_at"),
        }
    finally:
        connection.close()
