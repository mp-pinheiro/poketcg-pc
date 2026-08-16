"""Shared paths, packet state store, and metrics for the port factory.

Contracts (all relative to the repo root):
- Queue:    .factory/queue/<id>.json         one packet, atomic writes
- Bundles:  .factory/bundles/<id>/           green artifacts at repo-relative paths
- Cache:    .factory/oracle-cache/           shared PyBoy reference cache
- Metrics:  .factory/metrics.jsonl           one JSON object per finished packet
- Events:   .factory/events.jsonl            one JSON object per wave phase transition
- Blocked:  .factory/blocked.toml            routines the frontier must not re-offer
- Issues:  .factory/issues-cache.json         authoritative Forgejo snapshot

Packet states: pending -> translated -> verifying -> repair -> green -> landed,
with terminal side exits escalated / parked / rejected-format.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import signal
import subprocess
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FACTORY = ROOT / ".factory"
QUEUE = FACTORY / "queue"
BUNDLES = FACTORY / "bundles"
CACHE = FACTORY / "oracle-cache"
METRICS = FACTORY / "metrics.jsonl"
EVENTS = FACTORY / "events.jsonl"
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
PROCESS_TERM_GRACE_S = 0.5
_append_lock = threading.Lock()

SCHEMA = 2
STATES = (
    "pending", "translating", "translated", "verifying", "repair",
    "retry-ready", "recovering", "green", "integrating", "blocked",
    "landed", "superseded",
)
HISTORICAL_STATES = frozenset({"landed", "superseded"})
ACTIVE_CLAIM_STATES = frozenset(set(STATES) - HISTORICAL_STATES)
STATE_TRANSITIONS = {
    "pending": ACTIVE_CLAIM_STATES - {"pending", "landed", "superseded"},
    "translating": {"pending", "translated", "repair", "retry-ready", "recovering", "blocked"},
    "translated": {"pending", "verifying", "repair", "retry-ready", "recovering", "blocked"},
    "verifying": {"pending", "green", "repair", "retry-ready", "recovering", "blocked"},
    "repair": {"pending", "translating", "verifying", "retry-ready", "recovering", "blocked"},
    "retry-ready": {"pending", "translating", "recovering", "blocked", "superseded"},
    "recovering": {"pending", "translated", "verifying", "repair", "retry-ready", "green", "blocked"},
    "green": {"pending", "integrating", "repair", "retry-ready", "superseded"},
    "integrating": {"pending", "landed", "repair", "retry-ready", "recovering"},
    "blocked": {"pending", "retry-ready", "recovering", "superseded"},
    "landed": set(),
    "superseded": set(),
}



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


def _process_groups(root_pid: int) -> set[int]:
    groups = {root_pid}
    pending = [root_pid]
    seen: set[int] = set()
    while pending:
        pid = pending.pop()
        if pid in seen:
            continue
        seen.add(pid)
        try:
            groups.add(os.getpgid(pid))
        except ProcessLookupError:
            continue
        try:
            children = Path(f"/proc/{pid}/task/{pid}/children").read_text()
        except OSError:
            continue
        pending.extend(int(child) for child in children.split())
    return groups


def _signal_groups(groups: set[int], sig: signal.Signals) -> None:
    for group in groups:
        try:
            os.killpg(group, sig)
        except ProcessLookupError:
            pass


def _stop_process_tree(process: subprocess.Popen) -> None:
    groups = _process_groups(process.pid)
    _signal_groups(groups, signal.SIGTERM)
    try:
        process.wait(timeout=PROCESS_TERM_GRACE_S)
    except subprocess.TimeoutExpired:
        pass
    _signal_groups(groups, signal.SIGKILL)
    process.wait()


def run_bounded(command: list[str], *, cwd: Path, cap: float,
                deadline: float | None = None, check: bool = False,
                output_limit: int = 1_048_576,
                input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    if cap <= 0:
        raise ValueError("cap must be positive")
    if output_limit <= 0:
        raise ValueError("output_limit must be positive")
    if deadline is not None and deadline <= time.monotonic():
        raise WaveDeadlineExpired("wave deadline expired before command")
    effective = cap if deadline is None else min(cap, deadline - time.monotonic())
    if effective <= 0:
        raise WaveDeadlineExpired("wave deadline expired before command")
    with (
        tempfile.TemporaryFile() as stdin,
        tempfile.TemporaryFile() as stdout,
        tempfile.TemporaryFile() as stderr,
    ):
        if input_text is not None:
            stdin.write(input_text.encode())
            stdin.seek(0)
        process = subprocess.Popen(
            command, cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr,
            start_new_session=True,
        )
        try:
            process.wait(timeout=effective)
        except subprocess.TimeoutExpired:
            _stop_process_tree(process)
            if deadline is not None and time.monotonic() >= deadline:
                raise WaveDeadlineExpired("wave deadline expired during command")
            raise PhaseTimeout(command, cap)
        except BaseException:
            _stop_process_tree(process)
            raise
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
            "work_id": work_id,
            "issue_number": int(issue["number"]),
            "title": issue.get("title", ""),
            "state": state,
            "labels": sorted(labels),
            "url": issue.get("url") or "",
        }
    return records


def packet_path(packet_id: str) -> Path:
    return QUEUE / f"{packet_id}.json"


def load_packet(packet_id: str | Path) -> dict:
    path = packet_id if isinstance(packet_id, Path) else packet_path(packet_id)
    if not path.is_absolute():
        path = packet_path(str(path))
    packet = read_json(path)
    if packet.get("schema") == SCHEMA:
        validate_packet(packet)
        if path.stem != packet["attempt_id"]:
            raise ValueError(
                f"packet filename {path.name} does not match attempt_id "
                f"{packet['attempt_id']}"
            )
    return packet

def cohort_id(work_ids: list[str] | tuple[str, ...] | set[str]) -> str:
    canonical = sorted(set(work_ids))
    if not canonical or any(not isinstance(work_id, str) or not work_id for work_id in canonical):
        raise ValueError("cohort requires non-empty canonical work IDs")
    return hashlib.sha256("\0".join(canonical).encode()).hexdigest()


def new_attempt_id() -> str:
    return str(uuid.uuid4())


def legacy_attempt_id(packet_id: str, raw: bytes | str) -> str:
    payload = raw if isinstance(raw, bytes) else raw.encode()
    digest = hashlib.sha256(payload).hexdigest()
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"poketcg:legacy:{packet_id}:{digest}"))


def _ensure_packet_schema(packet: dict) -> dict:
    if not isinstance(packet, dict):
        raise ValueError("packet must be an object")
    routines = packet.get("routines")
    if not isinstance(routines, list) or not routines:
        raise ValueError("packet requires a non-empty routines list")
    work_ids = [routine.get("work_id") for routine in routines]
    if any(not isinstance(work_id, str) or not work_id for work_id in work_ids):
        raise ValueError("packet routines require canonical work IDs")
    attempt = packet.get("attempt_id") or packet.get("id")
    if not isinstance(attempt, str) or not attempt:
        raise ValueError("packet requires attempt_id")
    packet.setdefault("schema", SCHEMA)
    if packet["schema"] != SCHEMA:
        raise ValueError(f"unsupported packet schema {packet['schema']!r}")
    packet.setdefault("id", attempt)
    if packet["id"] != attempt or packet.get("attempt_id") != attempt:
        raise ValueError("packet id and attempt_id must match")
    expected_cohort = cohort_id(work_ids)
    if packet.get("cohort_id") != expected_cohort:
        raise ValueError("packet cohort_id does not match its routines")
    for key in ("basename", "file", "base_commit"):
        if not isinstance(packet.get(key), str) or not packet[key]:
            raise ValueError(f"packet requires non-empty {key}")
    state = packet.get("state")
    if state not in STATES:
        raise ValueError(f"unknown packet state {state!r}")
    packet.setdefault("failure_history", [])
    if not isinstance(packet["failure_history"], list):
        raise ValueError("failure_history must be a list")
    return packet


def validate_packet(packet: dict) -> dict:
    """Validate schema-2 packet identity and return the same packet."""
    return _ensure_packet_schema(packet)


def claim_index(packets: list[dict] | None = None) -> dict[str, dict]:
    """Return canonical work ownership for every active packet."""
    packets = list_packets() if packets is None else packets
    claims: dict[str, dict] = {}
    for packet in packets:
        if packet.get("state") in HISTORICAL_STATES:
            continue
        schema = packet.get("schema")
        owner_id = packet.get("attempt_id") or packet.get("id")
        if not isinstance(owner_id, str) or not owner_id:
            raise ValueError("packet requires id")
        if schema == SCHEMA:
            validate_packet(packet)
        routines = packet.get("routines")
        if not isinstance(routines, list):
            raise ValueError(f"packet {owner_id} has no routines")
        for routine in routines:
            work_id = routine.get("work_id")
            if not isinstance(work_id, str) or not work_id:
                raise ValueError(f"packet {owner_id} routine lacks work ID")
            owner = claims.get(work_id)
            if owner is not None and owner["attempt_id"] != owner_id:
                raise RuntimeError(
                    f"work ID {work_id} claimed by packets "
                    f"{owner['attempt_id']} and {owner_id}"
                )
            claims[work_id] = {
                "attempt_id": owner_id,
                "packet_id": packet.get("id", owner_id),
                "state": packet.get("state"),
            }
    return claims


def packet_identity(packet: dict) -> dict:
    """Return persisted identity shared by queue and bundle consumers."""
    if packet.get("schema") != SCHEMA:
        return {
            "id": packet["id"],
            "basename": packet["basename"],
            "file": packet["file"],
            "routines": [
                {
                    "name": routine["name"],
                    "work_id": routine["work_id"],
                    "issue_number": routine["issue_number"],
                }
                for routine in packet.get("routines", [])
            ],
        }
    validate_packet(packet)
    return {
        "schema": SCHEMA,
        "attempt_id": packet["attempt_id"],
        "cohort_id": packet["cohort_id"],
        "id": packet["id"],
        "basename": packet["basename"],
        "file": packet["file"],
        "base_commit": packet["base_commit"],
        "routines": [
            {
                "name": routine["name"],
                "work_id": routine["work_id"],
                "issue_number": routine["issue_number"],
            }
            for routine in packet["routines"]
        ],
    }


def save_packet(packet: dict) -> None:
    validate_packet(packet)
    write_json(packet_path(packet["attempt_id"]), packet)


def set_state(packet: dict, state: str, reason: str | None = None) -> None:
    validate_packet(packet)
    if state not in STATES:
        raise ValueError(f"unknown packet state {state}")
    previous = packet["state"]
    if state != previous and state not in STATE_TRANSITIONS[previous]:
        raise ValueError(f"illegal packet transition {previous} -> {state}")
    if reason and not reason.startswith("supervisor-"):
        history = packet.setdefault("failure_history", [])
        history.append({
            "phase": state,
            "status": state,
            "failure_class": (
                "dependency" if state == "blocked" else
                "harness" if state in {"repair", "recovering"} else
                "translation" if state == "retry-ready" else
                "infrastructure"
            ),
            "fingerprint": hashlib.sha256(reason.encode()).hexdigest()[:16],
            "detail": reason[:1000],
            "model": packet.get("model"),
            "timestamp": int(time.time()),
        })
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


def _append_jsonl(path: Path, entry: dict) -> None:
    entry = dict(entry)
    entry.setdefault("ts", int(time.time()))
    line = json.dumps(entry, sort_keys=True) + "\n"
    with _append_lock:
        FACTORY.mkdir(exist_ok=True)
        with path.open("a") as stream:
            stream.write(line)


def record_metric(entry: dict) -> None:
    _append_jsonl(METRICS, entry)


def record_event(entry: dict) -> None:
    """Also called from verify_worker.py, a separate process: string values
    are truncated to 300 chars so each line stays under Linux's O_APPEND
    atomic-write guarantee for concurrent writers."""
    _append_jsonl(EVENTS, {
        key: (value[:300] if isinstance(value, str) else value)
        for key, value in entry.items()
    })


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
