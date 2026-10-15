from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.completion.evidence import canonical_digest, requirements_contract
from tools.completion.revision import DERIVED_PATHS
from tools.oracle.release_gate import documentation_only_path

REQUIREMENTS_PATH = "tools/completion/requirements.toml"


def git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace").strip() or "git failed")
    return result.stdout


def documentation_only(root: Path, previous: str, current: str) -> bool:
    changed = git(root, "diff", "--name-only", "--no-renames", "-z", previous, current, "--")
    paths = [path.decode("utf-8") for path in changed.split(b"\0") if path]
    for path in paths:
        if path in DERIVED_PATHS or documentation_only_path(path):
            continue
        if path != REQUIREMENTS_PATH:
            return False
        if git(root, "diff", "--summary", "--no-renames", previous, current, "--", path):
            return False
        before = tomllib.loads(git(root, "show", f"{previous}:{path}").decode("utf-8"))
        after = tomllib.loads(git(root, "show", f"{current}:{path}").decode("utf-8"))
        if canonical_digest(requirements_contract(before)) != canonical_digest(requirements_contract(after)):
            return False
    return True


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: ci_scope.py FROM_REF TO_REF", file=sys.stderr)
        return 2
    try:
        docs = documentation_only(ROOT, sys.argv[1], sys.argv[2])
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print("docs" if docs else "full")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
