#!/usr/bin/env python3
"""Find the defects per-routine verification cannot see.

Each class is a shape the PyBoy oracle passes by construction, because it only
ever calls one routine with a synthesized environment:

  loops      a scene loop flattened to a single pass, so the game never iterates
  banks      a `ld a, BANK(X)` the C never performs, so a read hits the wrong bank
  jumps      a `jp hl` the port answers with an address instead of dispatching it
  backedges  the asm loops and the C has no loop at all
  stubs      a substantial asm routine whose C body does nothing
  cuts       a completion pc that stops the oracle at a routine the subject
             calls, so the contract ends where the stub ended

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


ASM_CALL = re.compile(r"^\s*(?:call|farcall)\b", re.IGNORECASE)


def asm_shapes() -> tuple[set[str], dict[str, int], dict[str, int]]:
    """Routines whose asm branches backwards, plus per-routine instruction and call counts."""
    looping: set[str] = set()
    sizes: dict[str, int] = {}
    asm_calls: dict[str, int] = {}

    def close(name: str | None, labels: dict[str, int], branches: list[tuple[int, str]],
              count: int, calls: int) -> None:
        if name is None:
            return
        sizes[name] = max(sizes.get(name, 0), count)
        asm_calls[name] = max(asm_calls.get(name, 0), calls)
        for position, target in branches:
            if target.startswith(".") and labels.get(target, position) < position:
                looping.add(name)
                return

    for path in sorted(ASM_ROOT.rglob("*.asm")):
        current, labels, branches, count, step, calls = None, {}, [], 0, 0, 0
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split(";", 1)[0]
            label = LABEL.match(line)
            if label:
                close(current, labels, branches, count, calls)
                current, labels, branches, count, step, calls = label.group(1), {}, [], 0, 0, 0
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
            if ASM_CALL.match(line):
                calls += 1
            if INSTRUCTION.match(line):
                count += 1
        close(current, labels, branches, count, calls)
    return looping, sizes, asm_calls


def audit_backedges(bodies: dict[str, tuple[str, str]],
                    looping: set[str]) -> list[dict[str, Any]]:
    return [
        {"routine": name, "file": bodies[name][0]}
        for name in sorted(looping)
        if name in bodies
        and not any(keyword in bodies[name][1] for keyword in LOOP_KEYWORDS)
    ]


CALLEE = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
NOT_A_CALL = frozenset(("if", "while", "for", "switch", "sizeof", "return"))


def audit_stubs(bodies: dict[str, tuple[str, str]],
                sizes: dict[str, int],
                asm_calls: dict[str, int]) -> list[dict[str, Any]]:
    rows = []
    for name, (filename, body) in sorted(bodies.items()):
        asm_instructions = sizes.get(name, 0)
        statements = sum(1 for line in body.splitlines() if line.strip().endswith(";"))
        if asm_instructions < 8 or statements > 1:
            continue
        callees = {c for c in CALLEE.findall(body) if c not in NOT_A_CALL}
        rows.append({"routine": name, "file": filename,
                     "asm_instructions": asm_instructions,
                     "c_statements": statements,
                     "asm_calls": asm_calls.get(name, 0),
                     "c_calls": len(callees),
                     "dropped_calls": max(0, asm_calls.get(name, 0) - len(callees))})
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


SYM_LINE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(\S+)$")
COMPLETION_BLOCK = re.compile(
    r"# >>> factory-completion (\w+)\n(.*?)# <<< factory-completion", re.S)
COMPLETION_PC = re.compile(r'"pc":\s*(0x[0-9A-Fa-f]+)(?:[^}]*?"bank":\s*(\d+))?', re.S)
ASM_CALL_TARGET = re.compile(r"^\s+(?:call|farcall|bank1call|callfar)\s+(?:\w+,\s*)?(\w+)")


def symbol_entries() -> dict[str, tuple[int, int]]:
    """Top-level symbol -> (bank, address). Dotted local labels are branch targets."""
    entries: dict[str, tuple[int, int]] = {}
    for line in (ROOT / "poketcg" / "poketcg.sym").read_text().splitlines():
        match = SYM_LINE.match(line.strip())
        if match and "." not in match.group(3):
            entries[match.group(3)] = (int(match.group(1), 16), int(match.group(2), 16))
    return entries


def asm_call_targets() -> dict[str, set[str]]:
    """Routine -> the routines it calls, from the asm rather than the port."""
    targets: dict[str, set[str]] = {}
    for path in sorted(ASM_ROOT.rglob("*.asm")):
        current = None
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split(";", 1)[0]
            label = LABEL.match(line)
            if label:
                current = label.group(1)
                continue
            if current is None:
                continue
            call = ASM_CALL_TARGET.match(line)
            if call:
                targets.setdefault(current, set()).add(call.group(1))
    return targets


def audit_cuts() -> list[dict[str, Any]]:
    """Completion overrides that stop the oracle inside a routine the subject calls.

    A `pre-ret` pc outside the subject's own span is legitimate when the asm
    tail-jumps: the routine really does complete at the jump target. It is a
    defect when the pc is the entry of a routine the subject `call`s, because
    the oracle then stops on the first such call and the contract covers only
    what runs before it -- which is exactly where a stub ends. Four routines in
    the duel entry chain were pinned this way (StartDuel at SetupDuel,
    StartDuel_VSAIOpp and GameEvent_Duel at LoadPlayerDeck), and each stub
    passed for the life of the port.
    """
    entries = symbol_entries()
    by_site = {(bank, address): name for name, (bank, address) in entries.items()}
    targets = asm_call_targets()
    rows = []
    for path in sorted((ROOT / "tests" / "cases").glob("*.py")):
        text = path.read_text()
        for name, body in COMPLETION_BLOCK.findall(text):
            found = COMPLETION_PC.search(body)
            if not found or name not in entries:
                continue
            # `entry` mode stops both lanes at that routine's entry on purpose
            # (src/trace.h trace_set_stop), which is the answer to a cut rather
            # than an instance of one.
            if '"mode": "entry"' in body:
                continue
            pc = int(found.group(1), 16)
            bank, address = entries[name]
            # A block may omit `bank`, in which case the routine's own bank is
            # the only candidate; skipping those hid Duel_Init's cut entirely.
            declared = int(found.group(2)) if found.group(2) else bank
            landing = (by_site.get((declared, pc)) or by_site.get((bank, pc))
                       or by_site.get((0, pc)))
            if landing is None or landing == name or pc == address:
                continue
            direct = targets.get(name, set())
            # A cut can hide one level down: GameEvent_Duel `bank1call`s
            # StartDuel_VSAIOpp and its pc lands in LoadPlayerDeck, which only
            # the callee calls.
            reachable = set(direct)
            for callee in direct:
                reachable |= targets.get(callee, set())
            if landing not in reachable:  # a tail jump, not a call
                continue
            rows.append({"routine": name, "file": path.name, "pc": f"{pc:04X}",
                         "cuts_at": landing,
                         "depth": 1 if landing in direct else 2})
    return rows


def audit_truncated() -> list[dict[str, Any]]:
    """Bodies that stop partway: every later asm callee missing, all earlier ones present.

    `GiveBoosterPack` ported the eleven statements up to `PlaySong` and stopped,
    with a comment declaring the rest unmeasurable. It was, at that routine's own
    boundary -- it passed 4/4 with the tail deleted. Only a caller running past
    the cut could see it, which is how `ScriptCommand_GiveBoosterPacks` failed on
    `wAnotherBoosterPack`. No case matrix detects this class, so match its shape
    directly: an unbroken prefix of the asm's call sequence present, and an
    unbroken suffix absent. Interleaved gaps are a different thing (a branch the
    body folded, a helper it inlined) and are not reported.
    """
    sequences: dict[str, list[str]] = {}
    for path in sorted(ASM_ROOT.rglob("*.asm")):
        current = None
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split(";", 1)[0]
            label = LABEL.match(line)
            if label:
                current = label.group(1)
                continue
            if current is None:
                continue
            # `call Other.label` is a jump into another routine's local label,
            # which the port factors into its own static rather than calling the
            # parent -- ScriptCommand_JumpIfNPCLoaded reaches
            # ScriptCommand_JumpIfEventTrue.pass_try_jump and the port models it
            # as script_jump_event_pass. Recording the parent name reads as a
            # missing call that was never a call.
            call = re.match(
                r"^\s+(?:call|farcall|bank1call|callfar)\s+(?:\w+,\s*)?([\w.]+)",
                line)
            if call and "." not in call.group(1):
                sequences.setdefault(current, []).append(call.group(1))

    bodies = c_bodies()
    rom_symbols = set(symbol_entries())
    rows: list[dict[str, Any]] = []
    for name, (file, body) in sorted(bodies.items()):
        calls = [c for c in sequences.get(name, []) if c in bodies and c != name]
        if len(calls) < 2:
            continue
        # The asm parser cannot see local labels, so a `.helper`'s calls land on
        # its parent. The port decomposes those into its own functions -- either
        # `Parent_Helper` (LoadTilemap_InitAndDecompressBGMap) or a file-local
        # static (print_text_body) -- and a routine whose callees all sit in one
        # reads as truncated when it is not. Expand through anything called that
        # is not a ROM symbol, since only port-local decomposition can be absent
        # from the sym file.
        reach, seen = body, {name}
        pending = [name]
        while pending:
            for helper, (_, other) in bodies.items():
                if helper in seen or helper in rom_symbols:
                    continue
                if not re.search(r"\b%s\s*\(" % re.escape(helper), reach):
                    continue
                seen.add(helper)
                reach += other
                pending.append(helper)
            pending.pop(0)
        present = [re.search(r"\b%s\s*\(" % re.escape(c), reach) is not None
                   for c in calls]
        if all(present) or not present[0]:
            continue
        cut = present.index(False)
        if any(present[cut:]):
            continue
        rows.append({"routine": name, "file": file, "kept": cut,
                     "dropped": len(calls) - cut, "missing": calls[cut:]})
    rows.sort(key=lambda r: (-r["dropped"], r["routine"]))
    return rows


def audit_overrides() -> list[dict[str, Any]]:
    """Probe adapters that overwrite a real result register with a constant.

    `PokemonTrader_TradeCardsEffect` copied all seven registers out of its
    result struct and then assigned `s->f = 0x70u` over the top, so its exit
    flags were unverifiable for the port's life -- no case matrix can catch a
    hole in the harness that reads it. A constant is legitimate only when the
    adapter never copied a result at all, which is why the copy has to be seen
    first.
    """
    rows: list[dict[str, Any]] = []
    for path in sorted((ROOT / "src" / "probe").glob("*.c")):
        routine, copied = None, False
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            begun = re.match(r"static void adapt_(\w+)\(ProbeState", line)
            if begun:
                routine, copied = begun.group(1), False
                continue
            if routine is None:
                continue
            if re.search(r"s->\w+ = result\.", line):
                copied = True
            constant = re.match(r"\ts->(\w+) = 0x[0-9A-Fa-f]+u;", line)
            if constant and copied:
                rows.append({"routine": routine, "register": constant.group(1),
                             "file": f"src/probe/{path.name}", "line": number})
            if line.startswith("}"):
                routine = None
    return rows


def counts() -> dict[str, int]:
    """Only the exact classes. The worklists are not ratcheted; see the docstring."""
    bodies = c_bodies()
    banks, jumps = asm_routines()
    return {
        "loops": len(audit_loops(bodies)),
        "banks": len(audit_banks(bodies, banks)),
        "jumps": len(audit_jumps(bodies, jumps)),
        "overrides": len(audit_overrides()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", choices=("loops", "banks", "jumps", "overrides",
                                          "backedges", "stubs", "cuts",
                                          "truncated", "all"))
    args = parser.parse_args(argv)

    bodies = c_bodies()
    if args.audit == "all":
        print(json.dumps(counts(), indent=2, sort_keys=True))
        return 0
    if args.audit == "truncated":
        rows = audit_truncated()
    elif args.audit == "overrides":
        rows = audit_overrides()
    elif args.audit == "cuts":
        rows = audit_cuts()
    elif args.audit in ("backedges", "stubs"):
        looping, sizes, asm_calls = asm_shapes()
        rows = (audit_backedges(bodies, looping) if args.audit == "backedges"
                else audit_stubs(bodies, sizes, asm_calls))
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
