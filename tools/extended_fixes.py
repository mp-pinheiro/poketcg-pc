#!/usr/bin/env python3
"""Check that every fix Extended documents is ported and tested.

Every `### ` heading of poketcg-extended/bugs_and_glitches.md must have one
row in profiles/extended/fixes.toml. A `code` row names the Extended routines
the fix changed: each must be an Extended function, have oracle cases in the
Extended case modules, and pass in the scoreboard. A `data` row is a fix to
text, graphics or map data, which the native port reads from the
ROM-derived data pack, so the pack check is its evidence. A `removed` row
belongs to a feature the profile removed (Card Pop!).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.profiles import get_profile

SOURCE = ROOT / "poketcg-extended" / "bugs_and_glitches.md"
FIXES = ROOT / "profiles" / "extended" / "fixes.toml"
SCOREBOARD = ROOT / "build-extended" / "completion" / "scoreboard.json"
KINDS = {"code", "data", "removed"}


def headings() -> set[str]:
    return {line[4:].strip() for line in SOURCE.read_text().splitlines() if line.startswith("### ")}


def case_routines(profile) -> set[str]:
    names: set[str] = set()
    for path in profile.case_modules(ROOT):
        spec = importlib.util.spec_from_file_location(f"fix_cases_{path.stem}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        names.update(name for name, entries in getattr(module, "CASES", {}).items() if entries)
    return names


def scoreboard_status(path: Path) -> dict[str, str]:
    document = json.loads(path.read_text())
    status: dict[str, str] = {}
    for group in document.get("groups", {}).values():
        for name, record in group.get("routines", {}).items():
            status[name] = record.get("status", "")
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixes", type=Path, default=FIXES)
    parser.add_argument("--scoreboard", type=Path, default=SCOREBOARD)
    args = parser.parse_args()
    profile = get_profile("extended", ROOT)
    document = tomllib.loads(args.fixes.read_text())
    rows = document.get("fixes")
    if not isinstance(rows, list):
        raise SystemExit("Extended fixes manifest has no fixes")
    failures: list[str] = []
    expected = headings()
    actual = [row.get("heading") for row in rows if isinstance(row, dict)]
    failures += [f"missing heading: {name}" for name in sorted(expected - set(actual))]
    failures += [f"unknown heading: {name}" for name in sorted(set(actual) - expected)]
    failures += [f"duplicate heading: {name}" for name in sorted({n for n in actual if actual.count(n) > 1})]
    functions = set(json.loads(profile.artifact_path("inventory", ROOT).read_text())["functions"])
    if not args.scoreboard.is_file():
        failures.append(f"no scoreboard at {args.scoreboard.relative_to(ROOT)}: run tools/extended_scoreboard.py")
        status: dict[str, str] = {}
    else:
        status = scoreboard_status(args.scoreboard)
    tested = case_routines(profile)
    counts = {kind: 0 for kind in KINDS}
    for row in rows:
        heading, kind, routines = row.get("heading"), row.get("kind"), row.get("routines", [])
        if kind not in KINDS:
            failures.append(f"{heading}: kind {kind!r} is not one of {sorted(KINDS)}")
            continue
        counts[kind] += 1
        if kind == "code":
            if not routines:
                failures.append(f"{heading}: a code fix names no routine")
            for routine in routines:
                if routine not in functions:
                    failures.append(f"{heading}: {routine} is not an Extended function")
                elif routine not in tested:
                    failures.append(f"{heading}: {routine} has no Extended oracle cases")
                elif status.get(routine) != "pass":
                    failures.append(f"{heading}: {routine} is {status.get(routine, 'not scored')} in the scoreboard")
        elif kind == "removed":
            removed = set(profile.removed_basenames)
            if "card_pop" not in removed:
                failures.append(f"{heading}: the feature is not removed from the profile")
    if counts["data"]:
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_data.py"), "--profile", "extended",
                                 "--pack-check"], cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            failures.append(f"data fixes: the Extended pack check failed: {result.stdout.strip()[-200:]}")
    if failures:
        for failure in failures:
            print(failure)
        print(f"extended-fixes: FAIL rows={len(rows)} failures={len(failures)}")
        return 1
    print(f"extended-fixes: PASS rows={len(rows)} code={counts['code']} data={counts['data']} removed={counts['removed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
