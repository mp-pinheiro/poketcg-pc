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
    revisions = _run(
        root,
        [
            "jj",
            "log",
            "-r",
            "ancestors(@-, 256)",
            "--no-graph",
            "-T",
            "commit_id ++ \"\\n\"",
        ],
    ).splitlines()
    if not revisions:
        raise RuntimeError("no committed revisions")
    for revision in revisions:
        changed = _run(
            root,
            [
                "jj",
                "diff",
                "--name-only",
                "--from",
                f"{revision}-",
                "--to",
                revision,
            ],
        ).splitlines()
        if any(path not in DERIVED_PATHS for path in changed):
            return revision
    return revisions[-1]


def current_source_revision(root: Path) -> str:
    try:
        return _jj_source_revision(root)
    except (OSError, RuntimeError, subprocess.SubprocessError):
        try:
            return _run(root, ["git", "rev-parse", "HEAD"])
        except (OSError, RuntimeError, subprocess.SubprocessError):
            return "unknown"
