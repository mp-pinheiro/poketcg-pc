#!/usr/bin/env python3
"""Count the composition defects per-routine verification cannot see.

Each class is a shape the PyBoy oracle passes by construction, because it only
ever calls one routine with a synthesized environment:

  loops  a scene loop flattened to a single pass, so the game never iterates it
  banks  a `ld a, BANK(X)` the C body never performs, so a read hits the wrong bank
  jumps  a `jp hl` the port answers with an address instead of dispatching it

The counts are ratcheted by tools/completion/tas_progress.py; they may fall and
never rise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ASM_ROOT = ROOT / "poketcg" / "src"
HOME = ROOT / "src" / "home"

LABEL = re.compile(r"^([A-Za-z_]\w*):{1,2}")
BANK_LOAD = re.compile(r"^\s+ld\s+a,\s*BANK\((\w+)\)")
JP_HL = re.compile(r"^\s+jp\s+hl\s*$")
DEFINITION = re.compile(r"^[A-Za-z_][\w \*]*?\b(\w+)\s*\([^;]*?\)\s*$")

# Dispatchers that answer a computed jump. A body naming one has modelled it.
DISPATCHERS = (
    "ScriptEntryEnter", "DispatchIndirect", "LookupOpcode", "LookupAddress",
    "CallDoFrameFunction", "switch (",
)
# ExecuteReceivedIRCommands is the IR link's command loop, whose physical layer
# docs/vision.md Phase 7 deletes outright rather than porting. EnterScript and
# CallMapScriptPointerIfExists return the target on purpose: their own oracle
# cases are captured at the entry (completion mode `pre-ret`), so the consumer
# that actually runs past it dispatches -- HandleOverworldMode, Func_c17a and
# HandleMoveModeAPress each call ScriptEntryEnter.
JUMP_EXEMPT = frozenset({
    "ExecuteReceivedIRCommands",
    "EnterScript",
    "CallMapScriptPointerIfExists",
})


def c_bodies() -> dict[str, tuple[str, str]]:
    bodies: dict[str, tuple[str, str]] = {}
    for path in sorted(HOME.glob("*.c")):
        lines = path.read_text(errors="replace").splitlines()
        for index, line in enumerate(lines):
            match = DEFINITION.match(line)
            if not match or index + 1 >= len(lines) or not lines[index + 1].startswith("{"):
                continue
            depth, collected = 0, []
            for cursor in range(index + 1, len(lines)):
                depth += lines[cursor].count("{") - lines[cursor].count("}")
                collected.append(lines[cursor])
                if depth == 0:
                    break
            bodies[match.group(1)] = (path.name, "\n".join(collected))
    return bodies


def asm_routines() -> tuple[dict[str, list[str]], dict[str, str]]:
    banks: dict[str, list[str]] = {}
    jumps: dict[str, str] = {}
    for path in sorted(ASM_ROOT.rglob("*.asm")):
        current = None
        for line in path.read_text(errors="replace").splitlines():
            label = LABEL.match(line)
            if label:
                current = label.group(1)
                continue
            if current is None:
                continue
            bank = BANK_LOAD.match(line)
            if bank:
                banks.setdefault(current, []).append(bank.group(1))
            if JP_HL.match(line):
                jumps.setdefault(current, path.name)
    return banks, jumps


def audit_loops(bodies: dict[str, tuple[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for name, (filename, body) in sorted(bodies.items()):
        if "for (;;) {" not in body:
            continue
        lines = [line.rstrip() for line in body.splitlines() if line.strip()]
        for index, line in enumerate(lines[:-2]):
            if (re.match(r"^\t\treturn[; ]", line)
                    and lines[index + 1].strip() == "}"
                    and lines[index + 2].strip() == "}"):
                rows.append({"routine": name, "file": filename})
                break
    return rows


def audit_banks(bodies: dict[str, tuple[str, str]],
                banks: dict[str, list[str]]) -> list[dict[str, Any]]:
    return [
        {"routine": name, "file": bodies[name][0], "targets": sorted(set(targets))}
        for name, targets in sorted(banks.items())
        if name in bodies and "BankswitchROM" not in bodies[name][1]
    ]


def audit_jumps(bodies: dict[str, tuple[str, str]],
                jumps: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for name, filename in sorted(jumps.items()):
        if name in JUMP_EXEMPT or name not in bodies:
            continue
        if any(marker in bodies[name][1] for marker in DISPATCHERS):
            continue
        rows.append({"routine": name, "file": filename})
    return rows


def counts() -> dict[str, int]:
    bodies = c_bodies()
    banks, jumps = asm_routines()
    return {
        "loops": len(audit_loops(bodies)),
        "banks": len(audit_banks(bodies, banks)),
        "jumps": len(audit_jumps(bodies, jumps)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", choices=("loops", "banks", "jumps", "all"))
    args = parser.parse_args(argv)

    bodies = c_bodies()
    banks, jumps = asm_routines()
    if args.audit == "all":
        print(json.dumps(counts(), indent=2, sort_keys=True))
        return 0
    rows = {
        "loops": lambda: audit_loops(bodies),
        "banks": lambda: audit_banks(bodies, banks),
        "jumps": lambda: audit_jumps(bodies, jumps),
    }[args.audit]()
    print(json.dumps({"count": len(rows), "rows": rows}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
