#!/usr/bin/env python3
"""Check the Extended three-palette presentation surfaces.

Each surface in profiles/extended/presentation.toml names the Extended
routines that draw it and the reference sessions that show it. A routine must
be an Extended function with oracle cases that pass in the scoreboard; a
session must be recorded and verified to its full length in the Extended
ratchet, which compares framebuffer, palette RAM, OAM and state with the
reference on every DoFrame.
"""
from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.profile_fixes import case_routines, scoreboard_path, scoreboard_status
from tools.profiles import get_profile

CONTRACT = ROOT / "profiles" / "extended" / "presentation.toml"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--scoreboard", type=Path)
    args = parser.parse_args()
    profile = get_profile("extended", ROOT)
    args.scoreboard = args.scoreboard or scoreboard_path(profile)
    contract = tomllib.loads(args.contract.read_text())
    surfaces = contract.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise SystemExit("Extended presentation contract has no surfaces")
    namespace = ROOT / contract["session_namespace"]
    ratchet = ROOT / contract["ratchet"]
    records = json.loads(ratchet.read_text()) if ratchet.is_file() else {}
    functions = set(json.loads(profile.artifact_path("inventory", ROOT).read_text())["functions"])
    tested = case_routines(profile)
    if args.scoreboard.is_file():
        status = scoreboard_status(args.scoreboard)
    else:
        status = {}
        print(f"no scoreboard at {args.scoreboard.relative_to(ROOT)}: run tools/extended_scoreboard.py")
    failures = 0
    for surface in surfaces:
        name = surface.get("name")
        problems: list[str] = []
        for routine in surface.get("routines", []):
            if routine not in functions:
                problems.append(f"{routine} is not an Extended function")
            elif routine not in tested:
                problems.append(f"{routine} has no Extended oracle cases")
            elif status.get(routine) != "pass":
                problems.append(f"{routine} is {status.get(routine, 'not scored')} in the scoreboard")
        for session in surface.get("sessions", []):
            meta_path = namespace / session / "session.json"
            if not meta_path.is_file():
                problems.append(f"session {session} is not recorded")
                continue
            length = int(json.loads(meta_path.read_text()).get("ordinals", 0))
            confirmed = int(records.get(session, {}).get("confirmed_ordinal", -1))
            if length < 1 or confirmed != length:
                problems.append(f"session {session} ratchet {confirmed} != length {length}")
        if not surface.get("routines") or not surface.get("sessions"):
            problems.append("a surface needs routines and sessions")
        for problem in problems:
            print(f"extended-presentation: FAIL {name}: {problem}")
        if not problems:
            print(f"extended-presentation: PASS {name} routines={len(surface['routines'])} "
                  f"sessions={','.join(surface['sessions'])}")
        failures += len(problems)
    if failures or not status:
        print(f"extended-presentation: FAIL surfaces={len(surfaces)} failures={failures}")
        return 1
    print(f"extended-presentation: PASS surfaces={len(surfaces)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
