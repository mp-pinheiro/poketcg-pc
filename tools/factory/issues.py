#!/usr/bin/env python3
"""Batch-close GitHub port issues whose routines have all landed.

Issues are a reporting mirror, not a dispatcher: nothing here assigns,
claims, or creates.  ``sync`` parses each open ``port``-labeled issue's
routine table, checks every routine against the derived registry, and closes
fully-landed issues with a one-line comment.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "tests"))

ROW = re.compile(r"^\|\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\|\s*\d+b\s*\|")


def routine_table(body: str) -> list[str]:
    names = []
    for line in body.splitlines():
        match = ROW.match(line.strip())
        if match and match.group(1) not in ("routine",):
            names.append(match.group(1))
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from routines import ALL  # noqa: E402 - derived registry
    registered = set(ALL)
    listing = subprocess.run(
        ["gh", "issue", "list", "--label", "port", "--state", "open",
         "--limit", "200", "--json", "number,title,body"],
        text=True, capture_output=True, check=True)
    issues = json.loads(listing.stdout)
    commit = subprocess.run(["jj", "log", "--no-graph", "-r", "main", "-T",
                             "commit_id.short()"], text=True,
                            capture_output=True).stdout.strip()
    closed = 0
    for issue in issues:
        names = routine_table(issue.get("body") or "")
        if not names:
            continue
        missing = [n for n in names if n not in registered]
        if missing:
            continue
        message = (f"All {len(names)} routines landed and gate-verified "
                   f"(registry at {commit}). Closed by the factory issue sync.")
        print(f"close #{issue['number']} {issue['title']}")
        if not args.dry_run:
            subprocess.run(["gh", "issue", "close", str(issue["number"]),
                            "--comment", message], check=True,
                           capture_output=True, text=True)
        closed += 1
    print(f"{'would close' if args.dry_run else 'closed'}: {closed}/{len(issues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
