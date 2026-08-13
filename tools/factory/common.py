"""Shared paths, packet state store, and metrics for the port factory.

Contracts (all relative to the repo root):
- Queue:    .factory/queue/<id>.json         one packet, atomic writes
- Bundles:  .factory/bundles/<id>/           green artifacts at repo-relative paths
- Cache:    .factory/oracle-cache/           shared PyBoy reference cache
- Metrics:  .factory/metrics.jsonl           one JSON object per finished packet
- Blocked:  .factory/blocked.toml            routines the frontier must not re-offer

Packet states: pending -> translated -> verifying -> repair -> green -> landed,
with terminal side exits escalated / parked / rejected-format.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FACTORY = ROOT / ".factory"
QUEUE = FACTORY / "queue"
BUNDLES = FACTORY / "bundles"
CACHE = FACTORY / "oracle-cache"
METRICS = FACTORY / "metrics.jsonl"
BLOCKED = FACTORY / "blocked.toml"
ISSUES_CACHE = FACTORY / "issues-cache.json"
LANE_BASE = Path("/tmp/poketcg-factory")
PBENV = Path("/tmp/pbenv/bin/python")
RUNNER = ROOT / "tools/oracle/gbref/build/gbref_runner"

_metrics_lock = threading.Lock()

STATES = (
    "pending", "translated", "verifying", "repair", "green", "landed",
    "escalated", "parked", "rejected-format",
)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.stem}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(data, stream, indent=1, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())

def issue_records(*, required: bool = False) -> dict[str, dict]:
    """Return cached marker records keyed by canonical work ID."""
    if not ISSUES_CACHE.exists():
        if required:
            raise RuntimeError(
                f"managed issue cache missing: {ISSUES_CACHE}; run issues.py fetch"
            )
        return {}
    data = json.loads(ISSUES_CACHE.read_text())
    records: dict[str, dict] = {}
    for issue in data.get("issues", []):
        body = issue.get("body") or ""
        marker = re.search(
            r"<!--\s*poketcg-port-work:v1\s*(\{.*?\})\s*-->",
            body, re.DOTALL,
        )
        if not marker:
            continue
        payload = json.loads(marker.group(1))
        work_id = payload.get("work_id")
        if not isinstance(work_id, str) or work_id in records:
            raise RuntimeError(f"duplicate or malformed cached work ID: {work_id}")
        records[work_id] = {
            "issue_number": int(issue["number"]),
            "title": issue.get("title", ""),
            "state": str(issue.get("state", "open")).lower(),
        }
    return records


def issues_are_migrated() -> bool:
    if not ISSUES_CACHE.exists():
        return False
    data = json.loads(ISSUES_CACHE.read_text())
    return bool(data.get("migration_complete"))


def packet_path(packet_id: str) -> Path:
    return QUEUE / f"{packet_id}.json"


def load_packet(packet_id: str) -> dict:
    return read_json(packet_path(packet_id))


def save_packet(packet: dict) -> None:
    write_json(packet_path(packet["id"]), packet)


def set_state(packet: dict, state: str, reason: str | None = None) -> None:
    if state not in STATES:
        raise ValueError(f"unknown packet state {state}")
    packet["state"] = state
    packet["reason"] = reason
    packet["updated_at"] = int(time.time())
    save_packet(packet)


def list_packets(states: tuple[str, ...] | None = None) -> list[dict]:
    packets = []
    if not QUEUE.is_dir():
        return packets
    for path in sorted(QUEUE.glob("*.json")):
        packet = read_json(path)
        if states is None or packet.get("state") in states:
            packets.append(packet)
    return packets


def record_metric(entry: dict) -> None:
    entry = dict(entry)
    entry.setdefault("ts", int(time.time()))
    with _metrics_lock:
        FACTORY.mkdir(exist_ok=True)
        with METRICS.open("a") as stream:
            stream.write(json.dumps(entry, sort_keys=True) + "\n")


def blocked_routines() -> set[str]:
    """Names listed in .factory/blocked.toml under [[blocked]] name=... entries."""
    if not BLOCKED.exists():
        return set()
    import tomllib

    with BLOCKED.open("rb") as stream:
        data = tomllib.load(stream)
    return {entry["name"] for entry in data.get("blocked", [])}


def block_routine(name: str, reason: str, unblock: str) -> None:
    if name in blocked_routines():
        return
    FACTORY.mkdir(exist_ok=True)
    with BLOCKED.open("a") as stream:
        stream.write(
            f'\n[[blocked]]\nname = "{name}"\nreason = "{reason}"\nunblock = "{unblock}"\n'
        )


def estimate_tokens(text: str) -> int:
    return len(text) // 4
