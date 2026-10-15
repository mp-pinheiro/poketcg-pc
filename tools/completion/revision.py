from __future__ import annotations

import subprocess
from pathlib import Path

DERIVED_PATHS = frozenset({
    "site/data/gate.json",
    "site/data/history.jsonl",
    "site/data/progress.json",
})


def _run(root: Path, command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=root,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "revision command failed")
    return result.stdout.strip()


def _jj_source_revision(root: Path) -> str:
    revision = _run(
        root,
        ["jj", "--ignore-working-copy", "log", "-r", "@-", "--no-graph", "-T", "commit_id"],
    )
    while True:
        parents = _run(
            root,
            ["jj", "--ignore-working-copy", "log", "-r", revision, "--no-graph",
             "-T", 'parents.map(|p| p.commit_id()).join("\\n")'],
        ).splitlines()
        if not parents:
            return revision
        parent = parents[0]
        changed = _run(
            root,
            ["jj", "--ignore-working-copy", "diff", "--name-only",
             "--from", parent, "--to", revision],
        ).splitlines()
        if any(path not in DERIVED_PATHS for path in changed):
            return revision
        revision = parent


def _git_source_revision(root: Path) -> str:
    offset = 0
    while True:
        revisions = _run(
            root, ["git", "rev-list", "--first-parent", "--parents",
                   "--max-count=256", f"--skip={offset}", "HEAD"],
        ).splitlines()
        if not revisions:
            raise RuntimeError("no committed source revision")
        for row in revisions:
            revision, *parents = row.split()
            command = (
                ["git", "diff", "--name-only", parents[0], revision]
                if parents else ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "--root", revision]
            )
            changed = _run(root, command).splitlines()
            if not parents or any(path not in DERIVED_PATHS for path in changed):
                return revision
        offset += len(revisions)


def current_source_revision(root: Path) -> str:
    for resolve in (_jj_source_revision, _git_source_revision):
        try:
            return resolve(root)
        except (OSError, RuntimeError, subprocess.SubprocessError):
            continue
    return "unknown"
