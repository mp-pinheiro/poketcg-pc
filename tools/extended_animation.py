#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from profiles import get_profile

ROOT = Path(__file__).resolve().parent.parent
CONST_FILES = (
    "src/constants/attack_animation_constants.asm",
    "src/constants/sfx_constants.asm",
    "src/constants/music_constants.asm",
)
CONST_RE = re.compile(r"^\s*(?:const|DEF)\s+([A-Za-z_][A-Za-z0-9_]*)")


def constants(source: Path) -> set[str]:
    found: set[str] = set()
    for relative in CONST_FILES:
        path = source / relative
        if not path.is_file():
            continue
        for line in path.read_text(errors="replace").splitlines():
            match = CONST_RE.match(line)
            if match:
                found.add(match.group(1))
    return found


def manifest(root: Path) -> dict[str, object]:
    vanilla = get_profile("vanilla", root).source_path(root)
    extended = get_profile("extended", root).source_path(root)
    added = sorted(constants(extended) - constants(vanilla))
    return {
        "schema": 1,
        "profile": "extended",
        "entries": [
            {"name": name, "scenario": f"tests/profiles/extended/scenes/{name}.json"}
            for name in added
        ],
    }


def gate(path: Path, root: Path) -> None:
    document = json.loads(path.read_text())
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("Extended animation manifest has no entries")
    failures = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not isinstance(entry.get("scenario"), str):
            failures.append("malformed entry")
            continue
        scenario = root / entry["scenario"]
        if not scenario.is_file():
            failures.append(f"{entry['name']}: missing scenario")
            continue
        result = json.loads(scenario.read_text())
        if result.get("status") != "pass":
            failures.append(f"{entry['name']}: scenario is not passing")
    if failures:
        for failure in failures:
            print(failure)
        raise SystemExit("Extended animation manifest gate failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "build-extended" / "completion" / "extended-animation-manifest.json")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest(ROOT), sort_keys=True, separators=(",", ":")) + "\n")
        print(f"extended-animation: wrote {args.manifest}")
        return 0
    gate(args.manifest, ROOT)
    print("extended-animation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
