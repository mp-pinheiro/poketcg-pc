#!/usr/bin/env python3
"""Reject acceptance escape hatches that let a stub pass the oracle.

Two mechanisms let a routine "PASS" without its C body ever being compared to
the ROM's, and both were found hiding one-line stubs on the duel's attack path
(PlayAttackAnimation_DealAttackDamage, HandleBetweenTurnKnockOuts, AIDoAction's
turn dispatch, _AIProcessHandTrainerCards):

- a case whose `completion` is `pre-ret` or `entry`, which stops the reference
  at an arbitrary program counter before the routine's own `ret`;
- a case whose `evidence` is not `primary`, which never runs the reference.

A third symptom is visible from the C alone: a factory body with no calls and
no bus access while the disassembly's body is more than a return.

Every routine relying on one of these must be declared in tests/hatches.py with
a kind. `never-returns` (a loop the asm never leaves), `hardware-only` (IR,
printer, serial) and `link-only` are facts about the ROM. `unaudited` is debt:
it passes the routine stage so the grind can proceed, and the release stage
ratchets it: the count may only fall below tools/oracle/hatch_ratchet.json,
which `--write-ratchet` lowers, so a landing that adds no debt is not blocked
by the debt it inherited. An undeclared hatch fails both stages, so a new stub
cannot be introduced.

`--list` prints the debt as a work queue: asm body size first, whether a
recorded reference session reaches the routine, and the declared kind.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))

from audit_oracle_cases import load_modules

HATCH_KINDS = {"never-returns", "hardware-only", "link-only", "unaudited"}
RELEASE_BLOCKING = {"unaudited"}
RATCHET = ROOT / "tools" / "oracle" / "hatch_ratchet.json"
LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?\s*(;.*)?$")
FACTORY = re.compile(r"^/\* >>> factory (\w+) \*/\n(.*?)\n/\* <<< factory \1 \*/", re.DOTALL | re.MULTILINE)
CALL = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
NOT_CALLS = {"void", "return", "if", "while", "for", "switch", "sizeof", "uint8_t", "uint16_t", "uint32_t", "int"}
TRIVIAL_ASM = 3  # `ld a, X / scf / ret` and shorter are real empty bodies


def load_hatches() -> dict[str, dict[str, str]]:
    spec = importlib.util.spec_from_file_location("hatches", ROOT / "tests" / "hatches.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(getattr(module, "HATCHES", {}))


def asm_bodies() -> dict[str, tuple[int, str, int]]:
    """Routine -> (instruction count, file, line) from the disassembly, counting
    up to the next global label. A body that is only a straight-line `ret`
    stops there; anything with a branch is counted whole."""
    bodies: dict[str, tuple[int, str, int]] = {}
    for path in glob.glob(str(ROOT / "poketcg" / "src" / "**" / "*.asm"), recursive=True):
        lines = Path(path).read_text(errors="replace").split("\n")
        for index, line in enumerate(lines):
            match = LABEL.match(line)
            if not match:
                continue
            count = 0
            branched = False
            cursor = index + 1
            while cursor < len(lines):
                text = lines[cursor]
                if LABEL.match(text):
                    break
                bare = text.split(";")[0].strip()
                if bare and not bare.startswith("."):
                    count += 1
                    mnemonic = bare.split()[0]
                    if mnemonic in ("jr", "jp", "call", "farcall", "bank1call", "rst"):
                        branched = True
                    if mnemonic in ("ret", "reti") and not branched and count <= TRIVIAL_ASM:
                        break
                cursor += 1
            bodies.setdefault(match.group(1), (count, path.split("/src/", 1)[-1], index + 1))
    return bodies


def hollow_bodies() -> dict[str, str]:
    """C factory blocks with no calls and no bus access -> file name."""
    hollow: dict[str, str] = {}
    for path in sorted(glob.glob(str(ROOT / "src" / "home" / "*.c"))):
        text = Path(path).read_text()
        for match in FACTORY.finditer(text):
            name, body = match.group(1), match.group(2)
            if name == "statics":
                continue
            calls = [c for c in CALL.findall(body) if c not in NOT_CALLS and c != name]
            if calls or "gb_write" in body or "gb_read" in body or "=" in body.replace("==", "").replace("!=", "").replace("<=", "").replace(">=", ""):
                continue
            hollow[name] = Path(path).name
    return hollow


def hatched_routines() -> dict[str, set[str]]:
    """Routine -> the hatch mechanisms its cases use."""
    uses: dict[str, set[str]] = {}
    for _path, module in load_modules():
        for fn, records in getattr(module, "SCHEMA2_CASES", {}).items():
            for record in records:
                if not isinstance(record, dict):
                    continue
                mode = (record.get("completion") or {}).get("mode", "return")
                if mode in ("pre-ret", "entry"):
                    uses.setdefault(fn, set()).add(mode)
                if record.get("evidence", "primary") != "primary":
                    uses.setdefault(fn, set()).add(record.get("evidence"))
    return uses


def session_reach() -> dict[str, int]:
    """Routine -> first reference ordinal in the most recent verified session
    trace, when one exists; used only to order the queue."""
    reach: dict[str, int] = {}
    for path in sorted(glob.glob(str(ROOT / "build" / "completion" / "tas" / "ref-*.json"))):
        try:
            data = json.loads(Path(path).read_text())
        except (OSError, json.JSONDecodeError):
            continue
        for row in data.get("calls", []):
            name, first = row.get("routine"), row.get("first_ordinal")
            if isinstance(name, str) and isinstance(first, int):
                reach[name] = min(first, reach.get(name, first))
    return reach


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("routine", "release"), default="routine")
    parser.add_argument("--list", action="store_true", help="print the declared debt as a work queue")
    parser.add_argument("--write-ratchet", action="store_true",
                        help="lower the release ceiling to the current unaudited count")
    args = parser.parse_args()

    hatches = load_hatches()
    uses = hatched_routines()
    bodies = asm_bodies()
    hollow = {fn: f for fn, f in hollow_bodies().items() if bodies.get(fn, (0,))[0] > TRIVIAL_ASM}
    failures = 0

    for fn, entry in sorted(hatches.items()):
        if not isinstance(entry, dict) or entry.get("kind") not in HATCH_KINDS or not str(entry.get("reason", "")).strip():
            print(f"HATCH {fn}: requires kind in {sorted(HATCH_KINDS)} and a reason")
            failures += 1
            continue
        if fn not in uses and fn not in hollow:
            print(f"HATCH {fn}: declared but no case uses a hatch and the body is not hollow; delete the entry")
            failures += 1

    for fn, mechanisms in sorted(uses.items()):
        if fn not in hatches:
            print(f"HATCH {fn}: {'/'.join(sorted(mechanisms))} case without a declared hatch in tests/hatches.py")
            failures += 1
    for fn, file in sorted(hollow.items()):
        if fn not in hatches:
            count, asm_file, line = bodies[fn]
            print(f"HOLLOW {fn}: {file} body has no calls or bus access; {asm_file}:{line} is {count} instructions")
            failures += 1

    unaudited = sum(1 for entry in hatches.values() if isinstance(entry, dict) and entry.get("kind") in RELEASE_BLOCKING)
    ceiling = json.loads(RATCHET.read_text())["unaudited"] if RATCHET.exists() else unaudited
    if args.stage == "release" and unaudited > ceiling:
        print(f"HATCH unaudited={unaudited} exceeds the ratchet ceiling {ceiling}: a landing added debt")
        failures += 1
    if args.write_ratchet and not failures and unaudited < ceiling:
        RATCHET.write_text(json.dumps({"unaudited": unaudited}, indent=2) + "\n")
        print(f"HATCH ratchet {ceiling} -> {unaudited}")

    if args.list:
        reach = session_reach()
        rows = []
        for fn, entry in hatches.items():
            count, asm_file, line = bodies.get(fn, (0, "?", 0))
            rows.append((reach.get(fn, 1 << 30), -count, fn, entry["kind"], count, f"{asm_file}:{line}",
                         "hollow" if fn in hollow else "/".join(sorted(uses.get(fn, ())))))
        rows.sort()
        for first, _neg, fn, kind, count, source, how in rows:
            reached = f"ordinal {first}" if first != 1 << 30 else "unreached"
            print(f"{kind:14s} {count:4d} instr  {reached:16s} {how:14s} {fn:44s} {source}")
        print(f"{len(rows)} hatched routines, {sum(1 for r in rows if r[3] in RELEASE_BLOCKING)} unaudited")

    if failures:
        print(f"HATCH_AUDIT failed: {failures}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
