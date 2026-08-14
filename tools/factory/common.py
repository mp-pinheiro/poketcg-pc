"""Shared paths, packet state store, and metrics for the port factory.

Contracts (all relative to the repo root):
- Queue:    .factory/queue/<id>.json         one packet, atomic writes
- Bundles:  .factory/bundles/<id>/           green artifacts at repo-relative paths
- Cache:    .factory/oracle-cache/           shared PyBoy reference cache
- Metrics:  .factory/metrics.jsonl           one JSON object per finished packet
- Blocked:  .factory/blocked.toml            routines the frontier must not re-offer
- Issues:  .factory/issues-cache.json         authoritative Forgejo snapshot

Packet states: pending -> translated -> verifying -> repair -> green -> landed,
with terminal side exits escalated / parked / rejected-format.
"""

from __future__ import annotations

import json
import fcntl
import os
import re
import signal
import subprocess
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FACTORY = ROOT / ".factory"
QUEUE = FACTORY / "queue"
BUNDLES = FACTORY / "bundles"
CACHE = FACTORY / "oracle-cache"
METRICS = FACTORY / "metrics.jsonl"
BLOCKED = FACTORY / "blocked.toml"
ISSUES_CACHE = FACTORY / "issues-cache.json"
ISSUES_SCHEMA = 2
ISSUES_BACKEND = "forgejo"
ISSUES_REPOSITORY = "mpp/poketcg-pc"
LANE_BASE = Path("/tmp/poketcg-factory")
ORACLE_PROJECT = ROOT / "tools" / "oracle"
ORACLE_PYTHON = [
    "uv", "run", "--project", str(ORACLE_PROJECT), "--frozen",
    "--python", "3.12.3", "python",
]
RUNNER = ROOT / "tools/oracle/gbref/build/gbref_runner"
WAVE_LOCK = FACTORY / "wave.lock"

_metrics_lock = threading.Lock()

STATES = (
    "pending", "translating", "translated", "verifying", "repair", "green", "landed",
    "escalated", "parked", "rejected-format",
)



class WaveDeadlineExpired(TimeoutError):
    pass


class PhaseTimeout(TimeoutError):
    def __init__(self, command: list[str], cap: float):
        self.command = command
        self.cap = cap
        super().__init__(f"phase timed out after {cap:.3f}s: {' '.join(command)}")


def _bounded_output(stream: tempfile._TemporaryFileWrapper, output_limit: int) -> str:
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(max(0, size - output_limit))
    data = stream.read()
    text = data.decode(errors="replace")
    return ("[... output truncated ...]\n" + text) if size > output_limit else text


def run_bounded(command: list[str], *, cwd: Path, cap: float,
                deadline: float | None = None, check: bool = False,
                output_limit: int = 1_048_576) -> subprocess.CompletedProcess[str]:
    if cap <= 0:
        raise ValueError("cap must be positive")
    if output_limit <= 0:
        raise ValueError("output_limit must be positive")
    if deadline is not None and deadline <= time.monotonic():
        raise WaveDeadlineExpired("wave deadline expired before command")
    effective = cap if deadline is None else min(cap, deadline - time.monotonic())
    if effective <= 0:
        raise WaveDeadlineExpired("wave deadline expired before command")
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(
            command, cwd=cwd, stdout=stdout, stderr=stderr,
            start_new_session=True,
        )
        try:
            process.wait(timeout=effective)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            if deadline is not None and time.monotonic() >= deadline:
                raise WaveDeadlineExpired("wave deadline expired during command")
            raise PhaseTimeout(command, cap)
        result = subprocess.CompletedProcess(
            command, process.returncode,
            _bounded_output(stdout, output_limit),
            _bounded_output(stderr, output_limit),
        )
    if check and result.returncode:
        raise subprocess.CalledProcessError(
            result.returncode, command, output=result.stdout, stderr=result.stderr,
        )
    return result


@contextmanager
def wave_lock(metadata: dict):
    FACTORY.mkdir(parents=True, exist_ok=True)
    descriptor = WAVE_LOCK.open("a+")
    try:
        try:
            fcntl.flock(descriptor.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            descriptor.seek(0)
            live = descriptor.read().strip()
            raise RuntimeError(f"factory wave lock is held: {live}")
        descriptor.seek(0)
        descriptor.truncate()
        descriptor.write(json.dumps(metadata, sort_keys=True))
        descriptor.flush()
        os.fsync(descriptor.fileno())
        yield
    finally:
        fcntl.flock(descriptor.fileno(), fcntl.LOCK_UN)
        descriptor.close()

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
    """Return authoritative Forgejo records keyed by canonical work ID."""
    if not ISSUES_CACHE.exists():
        if required:
            raise RuntimeError(
                f"Forgejo issue cache missing: {ISSUES_CACHE}; "
                "run issues.py fetch"
            )
        return {}
    data = json.loads(ISSUES_CACHE.read_text())
    if (
        data.get("schema") != ISSUES_SCHEMA
        or data.get("backend") != ISSUES_BACKEND
        or data.get("repository") != ISSUES_REPOSITORY
        or not isinstance(data.get("issues"), list)
    ):
        raise RuntimeError(
            f"invalid Forgejo issue cache: {ISSUES_CACHE}; run issues.py fetch"
        )
    records: dict[str, dict] = {}
    for issue in data["issues"]:
        body = issue.get("body") or ""
        matches = list(re.finditer(
            r"<!--\s*poketcg-port-work:v1\s*(\{.*?\})\s*-->",
            body, re.DOTALL,
        ))
        if "poketcg-port-work:v1" in body and len(matches) != 1:
            raise RuntimeError(
                f"issue #{issue.get('number')} has malformed work markers"
            )
        if not matches:
            continue
        payload = json.loads(matches[0].group(1))
        work_id = payload.get("work_id") if isinstance(payload, dict) else None
        if (
            not isinstance(work_id, str)
            or not work_id.startswith("port:v1:")
            or set(payload) != {"work_id"}
            or work_id in records
        ):
            raise RuntimeError(f"duplicate or malformed cached work ID: {work_id}")
        state = str(issue.get("state", "")).lower()
        if state not in {"open", "closed"}:
            raise RuntimeError(
                f"issue #{issue.get('number')} has invalid state: {state}"
            )
        labels = issue.get("labels") or []
        if not all(isinstance(label, str) for label in labels):
            raise RuntimeError(
                f"issue #{issue.get('number')} has non-normalized labels"
            )
        records[work_id] = {
            "issue_number": int(issue["number"]),
            "title": issue.get("title", ""),
            "state": state,
            "labels": sorted(labels),
            "url": issue.get("url") or "",
        }
    return records

def packet_identity(packet: dict) -> dict:
    """Return the persisted identity shared by queue and bundle consumers."""
    required_packet = ("id", "basename", "file", "routines")
    missing_packet = [key for key in required_packet if key not in packet]
    if missing_packet:
        raise ValueError(
            f"packet identity missing fields: {', '.join(missing_packet)}"
        )
    routines = []
    for index, routine in enumerate(packet["routines"]):
        missing = [
            key for key in ("name", "work_id", "issue_number")
            if key not in routine
        ]
        if missing:
            raise ValueError(
                f"packet identity routine {index} missing fields: "
                + ", ".join(missing)
            )
        routines.append({
            "name": routine["name"],
            "work_id": routine["work_id"],
            "issue_number": routine["issue_number"],
        })
    return {
        "id": packet["id"],
        "basename": packet["basename"],
        "file": packet["file"],
        "routines": routines,
    }


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
