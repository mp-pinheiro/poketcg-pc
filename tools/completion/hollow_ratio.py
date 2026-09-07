#!/usr/bin/env python3
"""Routines whose C body is far smaller than the asm it ports.

The oracle proves a routine on its cases; a body that returns a constant
passes cases that never leave the empty state. The AI decision routines that
stopped the ai-duel-02 session were all of that shape: `AIDecideEvolution`
was `return 0xff` for 290 asm lines, `GetAIScoreOfAttack` scored every attack
0x50 for 500. This lists every factory block whose asm-instructions-to-C-
statements ratio is out of range, most suspicious first: the proactive queue
behind the session loop.

    python3 tools/completion/hollow_ratio.py [--min-asm 25] [--ratio 6]
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import audit_hatches

BLOCK = re.compile(r"/\* >>> factory (\w+) \*/\n(.*?)/\* <<< factory \1 \*/", re.DOTALL)


def c_statements(body: str) -> int:
    count = 0
    for line in body.split("\n"):
        text = line.strip()
        if not text or text.startswith(("/*", "*", "//")):
            continue
        if ";" in text or text.endswith("{"):
            count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--min-asm", type=int, default=25, help="ignore routines with fewer asm instructions")
    parser.add_argument("--ratio", type=float, default=6.0, help="report when asm instructions exceed C statements by this factor")
    args = parser.parse_args(argv)
    bodies = audit_hatches.asm_bodies()
    rows = []
    for path in glob.glob(str(ROOT / "src" / "home" / "*.c")):
        text = Path(path).read_text()
        for match in BLOCK.finditer(text):
            name = match.group(1)
            if name not in bodies:
                continue
            asm_count = bodies[name][0]
            statements = c_statements(match.group(2))
            if asm_count >= args.min_asm and statements * args.ratio < asm_count:
                rows.append((asm_count / max(1, statements), asm_count, statements, name, bodies[name][1]))
    rows.sort(reverse=True)
    print(f"{'asm':>5} {'c':>4} {'ratio':>6}  routine")
    for ratio, asm_count, statements, name, source in rows:
        print(f"{asm_count:5d} {statements:4d} {ratio:6.1f}  {name:44s} {source}")
    print(f"HOLLOW_RATIO suspects={len(rows)} min_asm={args.min_asm} ratio={args.ratio:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
