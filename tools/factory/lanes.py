"""Factory lane provisioning: private, disposable checkout copies.

Lanes contain source and only the pinned derived/oracle inputs their worker
needs.  They never link writable paths back into the controller checkout.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
import time
from collections.abc import Iterator
from pathlib import Path

try:
    from tools.factory.common import (
        LANE_BASE,
        ROOT,
        LockBusy,
        file_lock,
        locks_dir,
        run_bounded,
    )
except ModuleNotFoundError:
    from common import LANE_BASE, ROOT, LockBusy, file_lock, locks_dir, run_bounded

RSYNC_EXCLUDES = (
    ".jj",
    ".git",
    ".factory",
    ".github",
    ".claude",
    ".entire",
    ".pi",
    ".omp",
    ".env",
    ".env.*",
    ".config",
    ".gitconfig",
    ".git-credentials",
    ".ssh",
    ".netrc",
    ".credentials",
    "credentials",
    "secrets",
    ".recovery-home",
    "build",
    "build-*",
    "poketcg",
    "site",
    "docs",
    "__pycache__",
    "tools/git-credential-forgejo",
    "tools/oracle/.venv",
    "tools/oracle/gbref/build",
)

PURGED_LANE_PATHS = (
    ".git",
    ".jj",
    "tools/git-credential-forgejo",
    ".env",
    ".gitconfig",
    ".git-credentials",
    ".ssh",
    ".netrc",
    ".credentials",
    "credentials",
    "secrets",
    ".recovery-home",
)

PRIVATE_INPUTS = (
    "docs/vision.md",
    "tools/completion/baseline.toml",
    "tools/completion/requirements.toml",
    "tools/completion/gambatte_pins.toml",
    "tools/completion/session_ratchet.json",
    "tools/progress/scope.toml",
    "site/data/inventory.json",
    "site/data/coverage.json",
    "site/data/progress.json",
    "poketcg/poketcg.gbc",
    "poketcg/poketcg.map",
    "poketcg/poketcg.sym",
    "poketcg/rom.sha1",
    "tools/oracle/gbref/build/gbref_runner",
)

PRIVATE_TREES = (
    "build/completion/evidence",
    "build/completion/gambatte",
    "poketcg/src",
)


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _materialize_private_inputs(root: Path, lane: Path) -> None:
    for relative in ("docs", "site", "poketcg"):
        _remove_path(lane / relative)
    for relative in PRIVATE_INPUTS:
        source = root / relative
        if not source.is_file():
            continue
        destination = lane / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for relative in PRIVATE_TREES:
        source = root / relative
        if not source.is_dir():
            continue
        destination = lane / relative
        _remove_path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
    try:
        commit = subprocess.run(
            ["git", "-C", str(root / "poketcg"), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except OSError:
        commit = None
    if commit is not None and commit.returncode == 0 and commit.stdout.strip():
        target = lane / "poketcg" / ".pret-commit"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(commit.stdout.strip() + "\n", encoding="utf-8")


def _purge_forbidden_lane_paths(lane: Path) -> None:
    for relative in PURGED_LANE_PATHS:
        path = lane / relative
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


_AUTH_ENV_PARTS = (
    "AUTH",
    "CREDENTIAL",
    "FORGEJO",
    "CLOUDFLARE",
    "CF_ACCESS",
    "TOKEN",
    "PASSWORD",
    "SECRET",
    "API_KEY",
    "ACCESS_KEY",
    "GIT_CONFIG",
    "SSH_AUTH",
)


def _is_auth_environment_key(key: str) -> bool:
    upper = key.upper()
    return any(part in upper for part in _AUTH_ENV_PARTS)


def recovery_environment(lane: Path) -> dict[str, str]:
    """Return an environment safe to pass to a credential-free recovery agent."""
    home = lane / ".recovery-home"
    home.mkdir(parents=True, exist_ok=True)
    if any(home.iterdir()):
        raise RuntimeError(f"recovery HOME is not empty: {home}")
    environment = {
        key: value
        for key, value in os.environ.items()
        if not _is_auth_environment_key(key)
    }
    environment["HOME"] = str(home)
    assert_recovery_environment(lane, environment)
    return environment


def assert_recovery_environment(
    lane: Path,
    environment: dict[str, str],
) -> None:
    """Reject a lane or environment that could expose repository credentials."""
    forbidden_paths = (
        lane / ".git",
        lane / ".jj",
        lane / "tools" / "git-credential-forgejo",
        lane / ".env",
        lane / ".gitconfig",
        lane / ".git-credentials",
        lane / ".ssh",
        lane / ".netrc",
        lane / ".credentials",
        lane / "credentials",
        lane / "secrets",
    )
    present = [str(path) for path in forbidden_paths if path.exists()]
    if present:
        raise RuntimeError(
            "recovery lane contains forbidden paths: " + ", ".join(present)
        )
    leaked = sorted(key for key in environment if _is_auth_environment_key(key))
    if leaked:
        raise RuntimeError(
            "recovery environment contains auth variables: " + ", ".join(leaked)
        )
    home = Path(environment.get("HOME", ""))
    if home != lane / ".recovery-home" or not home.is_dir():
        raise RuntimeError("recovery environment HOME is not lane-local")
    if any(home.iterdir()):
        raise RuntimeError(f"recovery HOME is not empty: {home}")


def lane_dir(index: int) -> Path:
    return LANE_BASE / f"lane-{index}"


LANE_SLOT_BASE = 700
LANE_SLOT_COUNT = 64


@contextlib.contextmanager
def claim(timeout: float = 900.0) -> Iterator[int]:
    """Reserve one lane index for the caller's lifetime.

    The lock is held on <lane>.lock, not on the lane directory, so a claim
    costs nothing and a crashed holder releases it automatically. Slots start
    at 700 to reuse the already-warm build directories in /tmp.

    Every concurrent orchestrator draws from this one registry: a lane index
    derived from position in a wave collides across sessions, and two rsyncs
    into one lane can green an artifact built from another attempt's tree.
    """
    deadline = time.monotonic() + max(0.0, timeout)
    while True:
        for index in range(LANE_SLOT_BASE, LANE_SLOT_BASE + LANE_SLOT_COUNT):
            with contextlib.ExitStack() as stack:
                try:
                    stack.enter_context(
                        file_lock(LANE_BASE / f"lane-{index}.lock", blocking=False)
                    )
                except LockBusy:
                    continue
                yield index
                return
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"no free factory lane in {LANE_SLOT_BASE}.."
                f"{LANE_SLOT_BASE + LANE_SLOT_COUNT - 1}"
            )
        time.sleep(1.0)


def _restore_packet_receipts(
    lane: Path, packet: dict | None, *, root: Path = ROOT
) -> None:
    if packet is None:
        return
    expected = {
        routine["work_id"]: routine["name"] for routine in packet.get("routines", [])
    }
    if not expected:
        return
    destination = lane / "tools" / "oracle" / "mutation_receipts"
    for metadata_path in sorted((root / ".factory" / "bundles").glob("*/packet.json")):
        try:
            metadata = json.loads(metadata_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if metadata.get("basename") != packet.get("basename") or metadata.get(
            "file"
        ) != packet.get("file"):
            continue
        routines = {
            routine.get("work_id"): routine.get("name")
            for routine in metadata.get("routines", [])
        }
        matches = expected.keys() & routines.keys()
        for work_id in matches:
            source = (
                metadata_path.parent
                / "tools"
                / "oracle"
                / "mutation_receipts"
                / f"{expected[work_id]}.json"
            )
            if source.is_file():
                destination.mkdir(parents=True, exist_ok=True)
                target = destination / source.name
                if not target.exists():
                    shutil.copy2(source, target)


def ensure(
    index: int,
    deadline: float | None = None,
    packet: dict | None = None,
    *,
    root: Path = ROOT,
) -> Path:
    """Create or refresh lane <index> from an explicit controller root."""
    root = root.resolve()
    lane = lane_dir(index)
    lane.mkdir(parents=True, exist_ok=True)
    with file_lock(locks_dir(root) / "tree.lock", exclusive=False, timeout=1800):
        _purge_forbidden_lane_paths(lane)
        command = ["rsync", "-a", "--checksum", "--no-times", "--delete"]
        for pattern in RSYNC_EXCLUDES:
            command += ["--exclude", pattern]
        command += [f"{root}/", f"{lane}/"]
        run_bounded(command, cwd=root, cap=300, deadline=deadline, check=True)
        _materialize_private_inputs(root, lane)
        _restore_packet_receipts(lane, packet, root=root)
        stamp = time.time()
        for folder in ("src/home", "src/probe", "tests/cases"):
            for path in (lane / folder).glob("*"):
                if path.is_file():
                    os.utime(path, (stamp, stamp))
    (lane / "build").mkdir(exist_ok=True)
    return lane


def configure(
    lane: Path, deadline: float | None = None
) -> subprocess.CompletedProcess[str]:
    """Configure the lane build once; later builds are plain ninja."""
    return run_bounded(
        [
            "cmake",
            "-G",
            "Ninja",
            "-B",
            "build",
            "-DCMAKE_BUILD_TYPE=Debug",
            "-DPORT_FILES=",
        ],
        cwd=lane,
        cap=120,
        deadline=deadline,
        check=False,
        env={"POKETCG_PORTS": "", "CMAKE_BUILD_PARALLEL_LEVEL": "2"},
    )


def build(
    lane: Path, deadline: float | None = None
) -> subprocess.CompletedProcess[str]:
    if not (lane / "build" / "build.ninja").exists():
        configured = configure(lane, deadline)
        if configured.returncode != 0:
            return configured
    return run_bounded(
        ["ninja", "-C", "build", "-j2"],
        cwd=lane,
        cap=600,
        deadline=deadline,
        check=False,
        env={"POKETCG_PORTS": "", "CMAKE_BUILD_PARALLEL_LEVEL": "2"},
    )
