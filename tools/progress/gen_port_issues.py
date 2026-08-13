#!/usr/bin/env python3
"""Compatibility entry point for the managed routine issue reconciler.

The old title/group generator is intentionally gone.  Use
``tools/factory/issues.py plan`` for normal reconciliation or the explicit
``migrate`` command for legacy adoption.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ISSUES = ROOT / "tools" / "factory" / "issues.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--migrate", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="retain compatibility; plan is always read-only")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tier", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--dir")
    args = parser.parse_args()
    if args.tier is not None or args.dir:
        parser.error(
            "--tier/--dir are retired; issue identity is one routine per work ID"
        )
    command = "migrate" if args.migrate else "plan"
    argv = [sys.executable, str(ISSUES), command]
    if args.json or args.dry_run:
        argv.append("--json")
    result = subprocess.run(argv, cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
