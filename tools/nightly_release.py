from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.completion.revision import DERIVED_PATHS


def source_changed(root: Path, previous: str, current: str) -> bool:
    command = [
        "git", "diff", "--quiet", "--no-ext-diff", previous, current, "--", ".",
        *(f":(exclude){path}" for path in sorted(DERIVED_PATHS)),
    ]
    result = subprocess.run(command, cwd=root, capture_output=True, check=False)
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    raise RuntimeError(result.stderr.decode(errors="replace").strip() or "git diff failed")


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: nightly_release.py FROM_REF TO_REF", file=sys.stderr)
        return 2
    try:
        changed = source_changed(ROOT, sys.argv[1], sys.argv[2])
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print("changed" if changed else "unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
