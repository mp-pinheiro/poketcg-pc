#!/usr/bin/env python3
"""Render translation prompts from packets and parse tagged-block replies.

Reply grammar (parsed, never trusted):

    ===STATICS                     optional, once: file-scope helpers/defines,
                                   extra #include lines first
    ===C <Fn>                      one C function definition
    ===H <Fn>                      prototype line(s)
    ===PROBE <Fn>                  one adapter function (adapt_<Fn'>)
    ===CASES <Fn>                  CONTRACT["<Fn>"] = {...} and CASES["<Fn>"] = [...]
    ===MUTATION <Fn>               MUTATIONS["<Fn>"] = {...}

Every routine in the packet needs all five routine blocks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, estimate_tokens, load_packet  # noqa: E402

CONTRACT_DOC = ROOT / "docs" / "factory-contract.md"
BLOCK = re.compile(r"^===(STATICS|C|H|PROBE|CASES|MUTATION)(?:\s+(\S+))?\s*$")
REQUIRED = ("C", "H", "PROBE", "CASES", "MUTATION")


class FormatError(ValueError):
    pass


def example_quad(basename: str) -> str:
    parts = []
    for rel in (f"src/home/{basename}.c", f"src/home/{basename}.h",
                f"src/probe/{basename}.c", f"tests/cases/{basename}.py"):
        path = ROOT / rel
        parts.append(f"--- {rel} ---\n{path.read_text()}")
    return "\n".join(parts)


def render(packet: dict, feedback: str | None = None,
           targets: list[str] | None = None) -> str:
    wanted = set(targets) if targets else {r["name"] for r in packet["routines"]}
    doc = CONTRACT_DOC.read_text()
    lines: list[str] = [doc, ""]
    lines.append("# COMPLETED EXAMPLE (a real, verified port; copy its conventions exactly)")
    lines.append(example_quad(packet["example"]))
    lines.append("")
    lines.append("# YOUR TASK")
    lines.append(f"Port the following routines from poketcg/{packet['file']} "
                 f"into basename `{packet['basename']}`.")
    if packet.get("existing"):
        existing = packet["existing"]
        lines.append("")
        lines.append(f"The target files already exist (append mode). Existing "
                     f"src/home/{packet['basename']}.h:")
        lines.append("```c\n" + existing["header"].strip() + "\n```")
        lines.append(f"Already-ported routines in this file: "
                     f"{', '.join(existing['contract_keys']) or 'none'}. "
                     f"Do NOT re-emit them.")
    if packet["constants"]:
        lines.append("")
        lines.append("Constant values from the pret tree (define locally with "
                     "`#define NAME 0x..u` when the C body needs them):")
        for name, value in packet["constants"].items():
            lines.append(f"- {name} EQU {value}")
    if packet.get("symbols"):
        lines.append("")
        lines.append("RAM symbol addresses (C code uses the bare macro names from the "
                     "generated headers; Python CASES use these NUMERIC addresses — "
                     "define module-level constants like `wFoo = 0x1234` at need, "
                     "never a C `_ADDR` macro name):")
        for name, addr in packet["symbols"].items():
            lines.append(f"- {name} = {addr}")
    lines.append("")
    verified = [r["name"] for r in packet["routines"] if r["name"] not in wanted]
    if verified:
        lines.append(f"Already verified in a previous round (do NOT re-emit): "
                     f"{', '.join(verified)}.")
        lines.append("")
    for routine in [r for r in packet["routines"] if r["name"] in wanted]:
        lines.append(f"## Routine `{routine['name']}` "
                     f"(poketcg/{packet['file']}:{routine['line']}, "
                     f"{routine['size']} bytes, {routine['refs']} callsites)")
        if routine.get("fallthrough"):
            lines.append(f"FALLTHROUGH: the body falls through into "
                         f"`{routine['fallthrough']}` — the C body must end by "
                         f"calling it (or returning its result).")
        callees = [c for c in routine["callees"] if c["c"]]
        if callees:
            lines.append("Ported callees (already available, include their header):")
            for callee in callees:
                lines.append(f"- `{callee['c']}`  // home/{callee['header']}, "
                             f"pret `{callee['name']}`")
        missing = [c["name"] for c in routine["callees"] if not c["c"]]
        if missing:
            lines.append(f"Callees with no C prototype found (bus data labels or "
                         f"scope-excluded): {', '.join(missing)}. Data labels are "
                         f"read through gb_read8 at their symbol address; they are "
                         f"not C calls.")
        lines.append("```asm")
        lines.append(routine["asm"])
        lines.append("```")
        lines.append("")
    lines.append("# OUTPUT FORMAT — MANDATORY")
    lines.append(
        "Reply with tagged blocks ONLY, no prose, no markdown fences. Grammar:\n"
        "===STATICS            (optional, once) file-scope statics/defines; extra\n"
        "                      #include lines first\n"
        "===C <RoutineName>    the C function for that routine\n"
        "===H <RoutineName>    its prototype line(s) for the header\n"
        "===PROBE <RoutineName> its adapter: static void adapt_<Name>(ProbeState *s)\n"
        "===CASES <RoutineName> exactly two statements:\n"
        '                      CONTRACT["<RoutineName>"] = {"compare": (...), "preserve": (...)}\n'
        '                      CASES["<RoutineName>"] = [ ...cases... ]\n'
        "===MUTATION <RoutineName> exactly one statement:\n"
        '                      MUTATIONS["<RoutineName>"] = {"source_symbol": ..., "before": ...,\n'
        '                      "after": ..., "case_ids": [...]}  # before/after are exact C\n'
        "                      substrings; before MUST occur exactly once in the file\n"
        f"Emit all five routine blocks for every routine: "
        f"{', '.join(r['name'] for r in packet['routines'] if r['name'] in wanted)}."
    )
    if feedback:
        lines.append("")
        lines.append("# PREVIOUS ATTEMPT FAILED — FIX AND RE-EMIT THE LISTED ROUTINES' BLOCKS")
        lines.append(feedback)
    return "\n".join(lines)


def parse(reply: str, packet: dict, targets: list[str] | None = None) -> dict:
    """-> {"statics": str|None, "routines": {fn: {kind: text}}}. Raises FormatError."""
    wanted_names = targets or [r["name"] for r in packet["routines"]]
    text = reply.replace("\r\n", "\n")
    # tolerate a fenced reply
    text = re.sub(r"^```[a-z]*\n|```\s*$", "", text.strip(), flags=re.MULTILINE)
    blocks: list[tuple[str, str | None, list[str]]] = []
    current: tuple[str, str | None, list[str]] | None = None
    for line in text.split("\n"):
        match = BLOCK.match(line.strip())
        if match:
            current = (match.group(1), match.group(2), [])
            blocks.append(current)
        elif current is not None:
            current[2].append(line)
    if not blocks:
        raise FormatError("no ===BLOCK headers found in reply")
    statics: str | None = None
    routines: dict[str, dict[str, str]] = {}
    for kind, name, body_lines in blocks:
        body = "\n".join(body_lines).strip()
        if kind == "STATICS":
            statics = body if statics is None else statics + "\n" + body
            continue
        if not name:
            raise FormatError(f"block ==={kind} is missing its routine name")
        routines.setdefault(name, {})[kind] = body
    all_names = {r["name"] for r in packet["routines"]}
    for fn in wanted_names:
        got = routines.get(fn, {})
        missing = [kind for kind in REQUIRED if not got.get(kind)]
        if missing:
            raise FormatError(f"routine {fn}: missing or empty blocks {missing}")
        if f'CONTRACT["{fn}"]' not in got["CASES"] or f'CASES["{fn}"]' not in got["CASES"]:
            raise FormatError(f"routine {fn}: CASES block must assign CONTRACT[\"{fn}\"] and CASES[\"{fn}\"]")
        if f'MUTATIONS["{fn}"]' not in got["MUTATION"]:
            raise FormatError(f"routine {fn}: MUTATION block must assign MUTATIONS[\"{fn}\"]")
    unknown = set(routines) - all_names
    if unknown:
        raise FormatError(f"blocks for unknown routines: {sorted(unknown)}")
    # keep only the requested routines: verified ones stay at their lane state
    routines = {fn: blocks_ for fn, blocks_ in routines.items() if fn in set(wanted_names)}
    return {"statics": statics, "routines": routines}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    packet = load_packet(args.packet)
    text = render(packet)
    if args.dry_run:
        print(f"prompt tokens (est.): {estimate_tokens(text)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
