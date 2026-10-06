#!/usr/bin/env python3
"""Syntax-check one Extended overlay basename without touching ninja state.

Replays the compile command CMake recorded for the overlay's home and probe
translation units with `-fsyntax-only`, so several ports can check their own
files at once against one configured build directory.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.profiles import get_profile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("basenames", nargs="+")
    parser.add_argument("--profile", default="extended")
    parser.add_argument("--build", type=Path,
                        default=Path(os.environ.get("POKETCG_BUILD", "build-ext-cmake")))
    args = parser.parse_args()
    profile = get_profile(args.profile, ROOT)
    build = args.build if args.build.is_absolute() else ROOT / args.build
    commands_path = build / "compile_commands.json"
    if not commands_path.is_file():
        raise SystemExit(f"{commands_path} missing; configure the Extended build first")
    commands = json.loads(commands_path.read_text())
    wanted = set()
    sources = {path.resolve() for path in profile.home_sources(ROOT) + profile.probe_sources(ROOT)}
    for basename in args.basenames:
        wanted.update(path for path in sources if path.stem == basename)
    if not wanted:
        raise SystemExit(f"no translation units for {args.basenames}")
    failures = 0
    for entry in commands:
        file = Path(entry["file"]).resolve()
        if file not in wanted:
            continue
        argv = shlex.split(entry["command"]) if "command" in entry else list(entry["arguments"])
        cleaned = []
        skip = False
        for token in argv:
            if skip:
                skip = False
                continue
            if token == "-o":
                skip = True
                continue
            if token in ("-c", "-MD", "-MMD") or token.startswith(("-MF", "-MT")):
                if token in ("-MF", "-MT"):
                    skip = True
                continue
            cleaned.append(token)
        cleaned.append("-fsyntax-only")
        result = subprocess.run(cleaned, cwd=entry.get("directory", str(build)), text=True,
                                capture_output=True, check=False)
        status = "ok" if result.returncode == 0 else "FAIL"
        print(f"{status} {file.relative_to(ROOT)}")
        if result.returncode != 0:
            failures += 1
            sys.stdout.write(result.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
