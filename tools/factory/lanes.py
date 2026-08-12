"""Factory lane provisioning: plain directory copies, no VCS, disposable.

A lane is /tmp/poketcg-factory/lane-<n>/ holding an rsync of the buildable
tree, a read-only ``poketcg`` symlink into the repo checkout, and a private
``build/`` configured once with ``-DPORT_FILES=""`` (full tree, barrier
semantics).  Refreshing a lane never touches its build dir, so steady-state
rebuilds stay incremental.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from common import LANE_BASE, ROOT

RSYNC_EXCLUDES = (
    ".jj", ".git", ".factory", ".github", ".claude", ".entire", ".pi", ".omp",
    "build", "build-*", "poketcg", "site", "docs", "__pycache__",
    "tools/oracle/.venv", "tools/oracle/gbref/build",
)


def lane_dir(index: int) -> Path:
    return LANE_BASE / f"lane-{index}"


def ensure(index: int) -> Path:
    """Create or refresh lane <index> from the current repo tree."""
    lane = lane_dir(index)
    lane.mkdir(parents=True, exist_ok=True)
    command = ["rsync", "-a", "--delete"]
    for pattern in RSYNC_EXCLUDES:
        command += ["--exclude", pattern]
    command += [f"{ROOT}/", f"{lane}/"]
    subprocess.run(command, check=True, capture_output=True, text=True)
    link = lane / "poketcg"
    if not link.is_symlink():
        if link.exists():
            raise RuntimeError(f"{link} exists and is not a symlink")
        link.symlink_to(ROOT / "poketcg")
    (lane / "build").mkdir(exist_ok=True)
    return lane


def configure(lane: Path) -> subprocess.CompletedProcess[str]:
    """Configure the lane build once; later builds are plain ninja."""
    return subprocess.run(
        ["cmake", "-G", "Ninja", "-B", "build", "-DCMAKE_BUILD_TYPE=Debug",
         "-DPORT_FILES="],
        cwd=lane, capture_output=True, text=True, check=False,
    )


def build(lane: Path) -> subprocess.CompletedProcess[str]:
    if not (lane / "build" / "build.ninja").exists():
        configured = configure(lane)
        if configured.returncode != 0:
            return configured
    return subprocess.run(
        ["ninja", "-C", "build", "-j2"], cwd=lane, capture_output=True, text=True,
        check=False,
    )
