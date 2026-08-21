"""Shared paths, packet identity, and bounded process execution.

Contracts (all relative to the repo root):
- Artifacts: .factory/artifacts/<sha256>/    immutable verified bundles
- Cache:     .factory/oracle-cache/          shared PyBoy reference cache
- Events:    .factory/events.jsonl           one JSON object per verify phase

A packet is a value: identity is its `attempt_id`, membership is its routine
work IDs, and persistence belongs to the caller. There is no queue directory,
no packet state machine, and no local claim store - Forgejo comments are the
event log and `.factory/state.sqlite3` is gone.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import signal
import subprocess
import tempfile
import threading
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FACTORY = ROOT / ".factory"
CACHE = FACTORY / "oracle-cache"
LANE_BASE = Path("/tmp/poketcg-factory")
ORACLE_PROJECT = ROOT / "tools" / "oracle"
ORACLE_PYTHON = [
    "uv", "run", "--project", str(ORACLE_PROJECT), "--frozen",
    "--python", "3.12.3", "python",
]
RUNNER = ROOT / "tools/oracle/gbref/build/gbref_runner"
PROCESS_TERM_GRACE_S = 0.5
_append_lock = threading.Lock()

SCHEMA = 2
STATES = frozenset({"pending"})



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



def cohort_id(work_ids: list[str] | tuple[str, ...] | set[str]) -> str:
    canonical = sorted(set(work_ids))
    if not canonical or any(not isinstance(work_id, str) or not work_id for work_id in canonical):
        raise ValueError("cohort requires non-empty canonical work IDs")
    return hashlib.sha256("\0".join(canonical).encode()).hexdigest()


def new_attempt_id() -> str:
    return str(uuid.uuid4())

def classify_case_module(path: Path) -> str:
    """Classify whether factory legacy fragments can append to a case module."""
    if not path.is_file():
        return "new"
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except (OSError, SyntaxError):
        return "native-migration-required"

    def targets_schema2(node: ast.Assign | ast.AnnAssign) -> bool:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return any(
            isinstance(target, ast.Name) and target.id == "SCHEMA2_CASES"
            for target in targets
        )

    def is_legacy_projection(value: ast.expr) -> bool:
        return (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "legacy_to_schema"
            and len(value.args) == 2
            and not value.keywords
            and all(
                isinstance(argument, ast.Name) and argument.id == expected
                for argument, expected in zip(value.args, ("CASES", "CONTRACT"))
            )
        )

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and targets_schema2(node):
            return (
                "legacy-appendable"
                if is_legacy_projection(node.value)
                else "native-migration-required"
            )
    return "native-migration-required"


def payload_tree_digest(
    root: Path,
    *,
    ignored: frozenset[str] = frozenset({"packet.json", ".factory-artifact.json"}),
) -> str:
    """Hash immutable artifact payload files independently from metadata."""
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if relative in ignored:
            continue
        data = path.read_bytes()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).hexdigest().encode())
        digest.update(b"\0")
        digest.update(str(len(data)).encode())
        digest.update(b"\n")
    return digest.hexdigest()




def _ensure_packet_schema(packet: dict) -> dict:
    if not isinstance(packet, dict):
        raise TypeError("packet must be an object")
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
        raise TypeError("failure_history must be a list")
    return packet


def validate_packet(packet: dict) -> dict:
    """Validate schema-2 packet identity and return the same packet."""
    return _ensure_packet_schema(packet)


def packet_identity(packet: dict) -> dict:
    """Return persisted identity shared by artifact and integration consumers."""
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
