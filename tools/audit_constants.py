#!/usr/bin/env python3
"""Check locally #define'd constants in ported C against pret ground truth.

The port defines constants locally (`#define needed constants locally instead`
- see surgery.check_includes), so a wrong value is invisible to the compiler
and, crucially, invisible to the oracle whenever the routine's cases never
seed the affected address. That combination produced live-wrong constants in
gate-green code: `DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA` as 0x02 (real 0xef)
and `TYPE_TRAINER` as 0x08 (real 0x10), each read by landed routines.

A name is reported only when pret defines it numerically AND the C value
differs AND the macro is actually referenced outside its own #define lines.
Dead duplicates are reported separately: harmless today, but they shadow each
other and are what the wrong values hid behind.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "factory"))

from packet import load_constants  # noqa: E402

DEFINE = re.compile(r"^#define\s+([A-Za-z_]\w*)\s+(.+?)\s*$")


def c_value(text: str) -> int | None:
    token = text.strip().split("/*")[0].strip().rstrip("uUlL")
    try:
        return int(token, 0)
    except ValueError:
        return None


def pret_value(text: str) -> int | None:
    token = text.strip()
    if token.startswith("$"):
        token = "0x" + token[1:]
    try:
        return int(token, 0)
    except ValueError:
        return None


def audit(paths: list[Path]) -> tuple[list[str], list[str]]:
    truth = load_constants()
    wrong: list[str] = []
    shadowed: list[str] = []
    for path in sorted(paths):
        text = path.read_text()
        lines = text.splitlines()
        defines: dict[str, list[tuple[int, int | None]]] = {}
        for number, line in enumerate(lines, 1):
            match = DEFINE.match(line)
            if match:
                defines.setdefault(match.group(1), []).append(
                    (number, c_value(match.group(2))))
        for name, entries in defines.items():
            # last definition wins in C
            effective = entries[-1][1]
            uses = sum(1 for line in lines
                       if re.search(rf"\b{re.escape(name)}\b", line)
                       and not DEFINE.match(line))
            if len(entries) > 1:
                values = {v for _, v in entries}
                kind = "same value" if len(values) == 1 else "CONFLICTING"
                shadowed.append(
                    f"{path.relative_to(ROOT)}: {name} defined {len(entries)}x "
                    f"({kind}), uses={uses}, effective={effective:#04x}"
                    if effective is not None else
                    f"{path.relative_to(ROOT)}: {name} defined {len(entries)}x, uses={uses}")
            expected = pret_value(truth.get(name, ""))
            if expected is None or effective is None or not uses:
                continue
            if effective != expected:
                wrong.append(
                    f"{path.relative_to(ROOT)}:{entries[-1][0]}: {name} = "
                    f"{effective:#04x} but pret says {expected:#04x} "
                    f"({uses} live use{'s' if uses != 1 else ''})")
    return wrong, shadowed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shadowed", action="store_true",
                        help="also list duplicate definitions")
    args = parser.parse_args()
    wrong, shadowed = audit(list((ROOT / "src" / "home").glob("*.c")))
    for line in wrong:
        print(f"WRONG {line}")
    if args.shadowed:
        for line in shadowed:
            print(f"SHADOW {line}")
    print(f"CONSTANTS wrong={len(wrong)} shadowed={len(shadowed)}")
    return 1 if wrong else 0


if __name__ == "__main__":
    raise SystemExit(main())
