#!/usr/bin/env python3
"""Oracle-check every Extended case group in its own process and tabulate results.

A reference run that never returns wedges the PyBoy process, so the full
`tests/test_leaves.py --all` sweep dies at the first such case. Running one
basename per process with a deadline bounds the damage to that basename and
yields a complete per-routine scoreboard for the Extended profile.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

RESULT_RE = re.compile(r"^(PASS|FAIL) (\S+?): (\d+)(?:/(\d+))? cases")


def run_group(group: str, probe: Path, rom: Path, deadline: int) -> dict[str, object]:
    env = dict(os.environ)
    env.update({"POKETCG_PROFILE": "extended", "POKETCG_ROM": str(rom)})
    command = ["uv", "run", "--project", "tools/oracle", "--frozen", "--python", "3.12.3", "python",
               "tests/test_leaves.py", "--group", group, "--oracle-mode", "live",
               "--probe", str(probe), "--rom", str(rom)]
    started = time.time()
    try:
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True,
                                timeout=deadline, check=False)
        output = result.stdout
        status = "done"
    except subprocess.TimeoutExpired as expired:
        output = (expired.stdout or b"").decode(errors="replace") if isinstance(expired.stdout, bytes) else (expired.stdout or "")
        status = "timeout"
    routines: dict[str, dict[str, int]] = {}
    for line in output.splitlines():
        match = RESULT_RE.match(line)
        if match:
            verdict, name, first, second = match.groups()
            total = int(second) if second else int(first)
            routines[name] = {"status": verdict.lower(), "cases": total, "failing": int(first) if second else 0}
    wedged = re.search(r"OracleError: (\S+) did not return", output)
    return {
        "group": group,
        "status": status,
        "seconds": round(time.time() - started, 1),
        "routines": routines,
        "wedged": wedged.group(1) if wedged else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--build", type=Path, default=Path(os.environ.get("POKETCG_BUILD", "build-ext-cmake")))
    parser.add_argument("--output", type=Path, default=ROOT / "build-extended" / "completion" / "scoreboard.json")
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--deadline", type=int, default=900)
    parser.add_argument("groups", nargs="*")
    args = parser.parse_args()
    os.environ["POKETCG_PROFILE"] = "extended"
    from tools.profiles import get_profile
    import routines

    profile = get_profile("extended", ROOT)
    build = args.build if args.build.is_absolute() else ROOT / args.build
    probe = build / profile.probe
    rom = profile.rom_path(ROOT)
    groups = args.groups or sorted(routines.ROUTINES)
    results: dict[str, object] = {}
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for row in pool.map(lambda group: run_group(group, probe, rom, args.deadline), groups):
            results[row["group"]] = row
            passing = sum(1 for entry in row["routines"].values() if entry["status"] == "pass")
            print(f"{row['group']:28s} {row['status']:8s} pass={passing:3d} fail={len(row['routines']) - passing:3d}"
                  f"{' wedged=' + row['wedged'] if row['wedged'] else ''}", flush=True)
    total_pass = sum(1 for row in results.values() for entry in row["routines"].values() if entry["status"] == "pass")
    total = sum(len(row["routines"]) for row in results.values())
    registered = len(routines.ALL)
    summary = {"schema": 1, "build": str(build), "registered": registered, "evaluated": total,
               "passing": total_pass, "groups": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(f"scoreboard: registered={registered} evaluated={total} passing={total_pass}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
