#!/usr/bin/env python3

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "poketcg-extended" / "bugs_and_glitches.md"
FIXES = ROOT / "profiles" / "extended" / "fixes.toml"


def headings() -> set[str]:
    return {line[4:] for line in SOURCE.read_text().splitlines() if line.startswith("### ")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixes", type=Path, default=FIXES)
    args = parser.parse_args()
    document = tomllib.loads(args.fixes.read_text())
    rows = document.get("fixes")
    if not isinstance(rows, list):
        raise SystemExit("Extended fixes manifest has no fixes")
    expected = headings()
    actual = {row.get("heading") for row in rows if isinstance(row, dict)}
    failures = [f"missing heading: {name}" for name in sorted(expected - actual)]
    failures.extend(f"duplicate heading: {name}" for name in sorted(name for name in actual if name and sum(row.get("heading") == name for row in rows) > 1))
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print(f"extended-fixes: PASS rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
