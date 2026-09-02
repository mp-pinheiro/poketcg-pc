#!/usr/bin/env python3
"""Find the defects per-routine verification cannot see.

Each class is a shape the PyBoy oracle passes by construction, because it only
ever calls one routine with a synthesized environment:

  loops      a scene loop flattened to a single pass, so the game never iterates
  banks      a `ld a, BANK(X)` the C never performs, so a read hits the wrong bank
  jumps      a `jp hl` the port answers with an address instead of dispatching it
  backedges  the asm loops and the C has no loop at all
  stubs      a substantial asm routine whose C body does nothing

`loops`, `banks` and `jumps` are exact and ratcheted by tas_progress.py: they
may fall and never rise.

`backedges` and `stubs` are ranked worklists, not gates, in the same sense as
the branch-count screen in docs/port-contract.md: a necessary condition, not a
verdict. Both have legitimate rows. A back-edge is absent from the C when the
asm loop was hardware (DisableLCD waiting on rLY, deleted by the Phase 1
transform) or arithmetic a C operator expresses directly. A one-statement body
is correct when it delegates to the routine it wraps. Triage against the asm
before touching anything, and order the work by whether the ROM executes the
routine on the TAS.
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

LOCAL_LABEL = re.compile(r"^(\.\w+)\s*$")
BRANCH = re.compile(r"^\s+(?:jr|jp)\s+(?:(?:nz|z|nc|c),\s*)?([A-Za-z_.][\w.]*)\s*$")
INSTRUCTION = re.compile(r"^\s+[a-z][a-z0-9_.]*\b")
LOOP_KEYWORDS = ("for (", "for(", "while (", "while(", "do {", "goto ")


def asm_shapes() -> tuple[set[str], dict[str, int]]:
    """Routines whose asm branches backwards, and every routine's instruction count."""
    looping: set[str] = set()
    sizes: dict[str, int] = {}

    def close(name: str | None, labels: dict[str, int], branches: list[tuple[int, str]],
              count: int) -> None:
        if name is None:
            return
        sizes[name] = max(sizes.get(name, 0), count)
        for position, target in branches:
            if target.startswith(".") and labels.get(target, position) < position:
                looping.add(name)
                return

    for path in sorted(ASM_ROOT.rglob("*.asm")):
        current, labels, branches, count, step = None, {}, [], 0, 0
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split(";", 1)[0]
            label = LABEL.match(line)
            if label:
                close(current, labels, branches, count)
                current, labels, branches, count, step = label.group(1), {}, [], 0, 0
                continue
            if current is None:
                continue
            step += 1
            local = LOCAL_LABEL.match(line.strip()) if line.strip().startswith(".") else None
            if local:
                labels.setdefault(local.group(1), step)
                continue
            branch = BRANCH.match(line)
            if branch:
                branches.append((step, branch.group(1)))
            if INSTRUCTION.match(line):
                count += 1
        close(current, labels, branches, count)
    return looping, sizes


def audit_backedges(bodies: dict[str, tuple[str, str]],
                    looping: set[str]) -> list[dict[str, Any]]:
    return [
        {"routine": name, "file": bodies[name][0]}
        for name in sorted(looping)
        if name in bodies
        and not any(keyword in bodies[name][1] for keyword in LOOP_KEYWORDS)
    ]


def audit_stubs(bodies: dict[str, tuple[str, str]],
                sizes: dict[str, int]) -> list[dict[str, Any]]:
    rows = []
    for name, (filename, body) in sorted(bodies.items()):
        asm_instructions = sizes.get(name, 0)
        statements = sum(1 for line in body.splitlines() if line.strip().endswith(";"))
        if asm_instructions >= 8 and statements <= 1:
            rows.append({"routine": name, "file": filename,
                         "asm_instructions": asm_instructions,
                         "c_statements": statements})
    return rows


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
    """Only the exact classes. The worklists are not ratcheted; see the docstring."""
    bodies = c_bodies()
    banks, jumps = asm_routines()
    return {
        "loops": len(audit_loops(bodies)),
        "banks": len(audit_banks(bodies, banks)),
        "jumps": len(audit_jumps(bodies, jumps)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", choices=("loops", "banks", "jumps",
                                          "backedges", "stubs", "all"))
    args = parser.parse_args(argv)

    bodies = c_bodies()
    if args.audit == "all":
        print(json.dumps(counts(), indent=2, sort_keys=True))
        return 0
    if args.audit in ("backedges", "stubs"):
        looping, sizes = asm_shapes()
        rows = (audit_backedges(bodies, looping) if args.audit == "backedges"
                else audit_stubs(bodies, sizes))
    else:
        banks, jumps = asm_routines()
        rows = {
            "loops": lambda: audit_loops(bodies),
            "banks": lambda: audit_banks(bodies, banks),
            "jumps": lambda: audit_jumps(bodies, jumps),
        }[args.audit]()
    print(json.dumps({"count": len(rows), "rows": rows}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
