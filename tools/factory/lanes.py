"""Factory lane provisioning: plain directory copies, no VCS, disposable.

A lane is /tmp/poketcg-factory/lane-<n>/ holding an rsync of the buildable
tree, a read-only ``poketcg`` symlink into the repo checkout, and a private
``build/`` configured once with ``-DPORT_FILES=""`` (full tree, barrier
semantics).  Refreshing a lane never touches its build dir, so steady-state
rebuilds stay incremental.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

from common import LANE_BASE, ROOT, run_bounded

RSYNC_EXCLUDES = (
    ".jj", ".git", ".factory", ".github", ".claude", ".entire", ".pi", ".omp",
    "build", "build-*", "poketcg", "site", "docs", "__pycache__",
    "tools/oracle/.venv", "tools/oracle/gbref/build",
)


def lane_dir(index: int) -> Path:
    return LANE_BASE / f"lane-{index}"


def ensure(index: int, deadline: float | None = None) -> Path:
    """Create or refresh lane <index> from the current repo tree.

    The lane keeps its build dir, so restoring a file rsync had previously
    overwritten leaves ninja's object from that earlier packet newer than the
    restored source: the lane relinks a routine that no longer exists and every
    later packet in it fails to build. rsync cannot fix this - once content
    matches the repo again it transfers nothing - so every file surgery is
    allowed to write is stamped after the sync.
    """
    lane = lane_dir(index)
    lane.mkdir(parents=True, exist_ok=True)
    command = ["rsync", "-a", "--checksum", "--no-times", "--delete"]
    for pattern in RSYNC_EXCLUDES:
        command += ["--exclude", pattern]
    command += [f"{ROOT}/", f"{lane}/"]
    run_bounded(command, cwd=ROOT, cap=300, deadline=deadline, check=True)
    stamp = time.time()
    for folder in ("src/home", "src/probe", "tests/cases"):
        for path in (lane / folder).glob("*"):
            if path.is_file():
                os.utime(path, (stamp, stamp))
    link = lane / "poketcg"
    if not link.is_symlink():
        if link.exists():
            raise RuntimeError(f"{link} exists and is not a symlink")
        link.symlink_to(ROOT / "poketcg")
    (lane / "build").mkdir(exist_ok=True)
    return lane


def configure(lane: Path, deadline: float | None = None) -> subprocess.CompletedProcess[str]:
    """Configure the lane build once; later builds are plain ninja."""
    return run_bounded(
        ["cmake", "-G", "Ninja", "-B", "build", "-DCMAKE_BUILD_TYPE=Debug",
         "-DPORT_FILES="],
        cwd=lane, cap=120, deadline=deadline, check=False,
    )


def build(lane: Path, deadline: float | None = None) -> subprocess.CompletedProcess[str]:
    if not (lane / "build" / "build.ninja").exists():
        configured = configure(lane, deadline)
        if configured.returncode != 0:
            return configured
    return run_bounded(
        ["ninja", "-C", "build", "-j2"], cwd=lane, cap=600,
        deadline=deadline, check=False,
    )
