#!/usr/bin/env python3
"""Replace local `#define NAME <literal>` lines with the generated profile headers.

A define whose name and value match the vanilla `generated/constants.h` or
`generated/text_ids.h` entry is deleted and the file gains the matching
`#include "generated/..."`, so the same C compiles against each profile's
constant values. Defines whose value differs from the generated one are kept
and reported.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DEFINE_RE = re.compile(
    r"^#define\s+([A-Za-z_]\w*)\s+\(?\s*(-?0[xX][0-9A-Fa-f]+|-?\d+)\s*[uUlL]{0,2}\s*\)?\s*(?://.*|/\*.*\*/)?\s*$"
)
GENERATED_RE = re.compile(r"^#define (\w+) (.*)$")
INCLUDE_RE = re.compile(r'^#include ["<].*[">]\s*$', re.MULTILINE)
GENERATED_INCLUDE_RE = re.compile(r'^#include "generated/\w+\.h"\s*$', re.MULTILINE)


def load_generated(path: Path) -> dict[str, int]:
    values: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = GENERATED_RE.match(line)
        if match:
            text = match.group(2).strip().strip("()").rstrip("uU")
            values[match.group(1)] = int(text, 0)
    return values


def rewrite(text: str, tables: dict[str, dict[str, int]]) -> tuple[str, list[str], set[str]]:
    lines = text.split("\n")
    kept: list[str] = []
    mismatched: list[str] = []
    needed: set[str] = set()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = DEFINE_RE.match(line)
        if match:
            name, value = match.group(1), int(match.group(2), 0)
            owner = next((header for header, table in tables.items() if name in table), None)
            if owner is not None:
                if tables[owner][name] == value:
                    needed.add(owner)
                    guard = kept and kept[-1].strip() == f"#ifndef {name}"
                    if guard and index + 1 < len(lines) and lines[index + 1].strip() == "#endif":
                        kept.pop()
                        index += 2
                    else:
                        index += 1
                    continue
                mismatched.append(f"{name} is 0x{value:X}, generated says 0x{tables[owner][name]:X}")
        kept.append(line)
        index += 1
    result = "\n".join(kept)
    for header in sorted(needed):
        include = f'#include "generated/{header}"'
        if include in result:
            continue
        anchors = list(GENERATED_INCLUDE_RE.finditer(result)) or list(INCLUDE_RE.finditer(result))
        if anchors:
            position = anchors[0].start()
            result = result[:position] + include + "\n" + result[position:]
        else:
            result = include + "\n" + result
    return result, mismatched, needed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generated", type=Path, required=True,
                        help="directory holding the vanilla constants.h and text_ids.h")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    tables = {
        "constants.h": load_generated(args.generated / "constants.h"),
        "text_ids.h": load_generated(args.generated / "text_ids.h"),
    }
    paths = [path if path.is_absolute() else ROOT / path for path in args.paths] or (
        sorted((ROOT / "src" / "home").glob("*.c")) + sorted((ROOT / "src" / "home").glob("*.h"))
        + sorted((ROOT / "src" / "probe").glob("*.c")))
    total = 0
    for path in paths:
        original = path.read_text(encoding="utf-8")
        text, mismatched, needed = rewrite(original, tables)
        removed = original.count("\n") - text.count("\n") + (1 if needed else 0) * 0
        if text != original:
            total += removed
            if not args.check:
                path.write_text(text, encoding="utf-8")
            print(f"{path.relative_to(ROOT)}: removed={removed} includes={sorted(needed)}")
        for entry in mismatched:
            print(f"  keep {path.relative_to(ROOT)}: {entry}")
    print(f"removed={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
