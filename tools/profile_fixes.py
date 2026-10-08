#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.profiles import Profile, get_profile

REVERT_KEYS = ("routine", "source", "before", "after", "case", "index")
KINDS = {"code", "unfixed", "data", "removed"}


def fixes_path(profile: Profile) -> Path:
    return ROOT / "profiles" / profile.name / "fixes.toml"


def receipt_namespace(profile: Profile) -> Path:
    value = profile.evidence.get("fix_receipt_namespace")
    if not isinstance(value, str) or not value:
        raise SystemExit(f"profile {profile.name} has no evidence.fix_receipt_namespace")
    return ROOT / value


def scoreboard_path(profile: Profile) -> Path:
    return profile.build_path(ROOT) / "completion" / "scoreboard.json"


def sections(source: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    heading = None
    for line in source.read_text().splitlines():
        if line.startswith("### "):
            heading = line[4:].strip()
            result[heading] = ""
        elif line.startswith("## "):
            heading = None
        elif heading is not None:
            result[heading] += line + "\n"
    return result


def case_routines(profile: Profile) -> set[str]:
    names: set[str] = set()
    previous = os.environ.get("POKETCG_PROFILE")
    os.environ["POKETCG_PROFILE"] = profile.name
    try:
        for path in profile.case_modules(ROOT):
            spec = importlib.util.spec_from_file_location(f"fix_cases_{profile.name}_{path.stem}", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            names.update(name for name, entries in getattr(module, "CASES", {}).items() if entries)
    finally:
        if previous is None:
            os.environ.pop("POKETCG_PROFILE", None)
        else:
            os.environ["POKETCG_PROFILE"] = previous
    return names


def scoreboard_status(path: Path) -> dict[str, str]:
    document = json.loads(path.read_text())
    status: dict[str, str] = {}
    for group in document.get("groups", {}).values():
        for name, record in group.get("routines", {}).items():
            status[name] = record.get("status", "")
    return status


def revert_receipt(profile: Profile, revert: dict) -> Path:
    canonical = json.dumps({key: revert.get(key) for key in REVERT_KEYS}, sort_keys=True)
    return receipt_namespace(profile) / f"{revert.get('routine')}-{hashlib.sha256(canonical.encode()).hexdigest()[:12]}.json"


def revert_proven(profile: Profile, revert: dict) -> bool:
    path = revert_receipt(profile, revert)
    return path.is_file() and json.loads(path.read_text()).get("status") == "RED"


def prove(profile: Profile, revert: dict, build: Path) -> str:
    mutation = {"source": revert["source"], "source_symbol": revert["routine"],
                "before": revert["before"], "after": revert["after"]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(mutation, handle)
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "run_mutation.py"), revert["routine"], revert["case"],
             "--build", str(build), "--index", str(revert["index"]), "--mutation", handle.name,
             "--receipt", str(revert_receipt(profile, revert))],
            cwd=ROOT, capture_output=True, text=True, check=False)
    finally:
        Path(handle.name).unlink()
    lines = [line for line in (result.stdout + result.stderr).splitlines() if line.startswith("MUTATION_")]
    return lines[-1] if lines else f"MUTATION_EXECUTION_FAILED: rc={result.returncode}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a profile's fixes manifest, cases, scoreboard and revert receipts.")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--scoreboard", type=Path)
    parser.add_argument("--prove", action="store_true",
                        help="run every revert without a current receipt through tools/run_mutation.py")
    parser.add_argument("--build", type=Path, help="ninja build dir whose probe --prove rebuilds (default: the profile's)")
    args = parser.parse_args()
    profile = get_profile(args.profile, ROOT)
    document = tomllib.loads(fixes_path(profile).read_text())
    rows = document.get("fixes")
    if not isinstance(rows, list):
        raise SystemExit(f"{profile.title} fixes manifest has no fixes")
    source = ROOT / str(document.get("source", ""))
    if not source.is_file():
        raise SystemExit(f"{profile.title} fixes manifest names a missing source document: {source}")
    documented = sections(source)
    scoreboard = args.scoreboard or scoreboard_path(profile)
    build = args.build or profile.build_path(ROOT)
    failures: list[str] = []
    actual = [row.get("heading") for row in rows if isinstance(row, dict)]
    failures += [f"missing heading: {name}" for name in sorted(set(documented) - set(actual))]
    failures += [f"unknown heading: {name}" for name in sorted(set(actual) - set(documented))]
    failures += [f"duplicate heading: {name}" for name in sorted({n for n in actual if actual.count(n) > 1})]
    functions = set(json.loads(profile.artifact_path("inventory", ROOT).read_text())["functions"])
    if not scoreboard.is_file():
        failures.append(f"no scoreboard at {scoreboard.relative_to(ROOT)}: run tools/extended_scoreboard.py")
        status: dict[str, str] = {}
    else:
        status = scoreboard_status(scoreboard)
    tested = case_routines(profile)
    counts = {kind: 0 for kind in KINDS}
    for row in rows:
        heading, kind, routines = row.get("heading"), row.get("kind"), row.get("routines", [])
        if kind not in KINDS:
            failures.append(f"{heading}: kind {kind!r} is not one of {sorted(KINDS)}")
            continue
        counts[kind] += 1
        if kind in ("code", "unfixed"):
            if not routines:
                failures.append(f"{heading}: a {kind} row names no routine")
            for routine in routines:
                if routine not in functions:
                    failures.append(f"{heading}: {routine} is not a {profile.title} function")
                elif routine not in tested:
                    failures.append(f"{heading}: {routine} has no {profile.title} oracle cases")
                elif status.get(routine) != "pass":
                    failures.append(f"{heading}: {routine} is {status.get(routine, 'not scored')} in the scoreboard")
        if kind == "unfixed" and "**Fix:** TODO" not in documented.get(heading, ""):
            failures.append(f"{heading}: upstream documents a fix, so the row must be code")
        if kind == "code":
            reverts = row.get("reverts", [])
            for routine in routines:
                if not any(revert.get("routine") == routine for revert in reverts):
                    failures.append(f"{heading}: {routine} has no revert")
            for revert in reverts:
                missing = [key for key in REVERT_KEYS if key not in revert]
                if missing:
                    failures.append(f"{heading}: revert lacks {', '.join(missing)}")
                    continue
                if args.prove and not revert_proven(profile, revert):
                    print(f"{heading}: {revert['routine']}: {prove(profile, revert, build)}")
                if not revert_proven(profile, revert):
                    failures.append(f"{heading}: {revert['routine']} revert has no RED receipt "
                                    f"({revert_receipt(profile, revert).relative_to(ROOT)})")
        elif kind == "removed":
            basenames = row.get("basenames", [])
            if not basenames:
                failures.append(f"{heading}: a removed row names no basename")
            missing = [name for name in basenames if name not in profile.removed_basenames]
            if missing:
                failures.append(f"{heading}: {', '.join(missing)} not removed from the profile")
    if counts["data"]:
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_data.py"), "--profile", profile.name,
                                 "--pack-check"], cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            failures.append(f"data fixes: the {profile.title} pack check failed: {result.stdout.strip()[-200:]}")
    if failures:
        for failure in failures:
            print(failure)
        print(f"profile-fixes: FAIL profile={profile.name} rows={len(rows)} failures={len(failures)}")
        return 1
    print(f"profile-fixes: PASS profile={profile.name} rows={len(rows)} code={counts['code']} "
          f"unfixed={counts['unfixed']} data={counts['data']} removed={counts['removed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
