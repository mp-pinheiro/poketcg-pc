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

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT


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
    lines: list[str] = [
        "You are a credential-free port generator. The packet below is complete context.",
        "Return one TranslationReplyV2 JSON object and nothing else.",
        "",
    ]
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
    if packet.get("text_ids"):
        lines.append("")
        lines.append("Text IDs (`ldtx hl, X` loads hl with this exact numeric id; "
                     "copy these #define lines verbatim into STATICS, never invent "
                     "TX_*/TEXT_* names):")
        for name, value in packet["text_ids"].items():
            lines.append(f"- #define {name} {value}")
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
        issue = (
            f", managed issue #{routine['issue_number']}"
            if routine.get("issue_number") is not None else
            ", managed issue not yet reconciled"
        )
        lines.append(f"## Routine `{routine['name']}` "
                     f"(poketcg/{packet['file']}:{routine['line']}, "
                     f"{routine['size']} bytes, {routine['refs']} callsites{issue})")
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
        "Return JSON with exactly these fields: schema=2, attempt_id, statics, "
        "cases_statics, routines. Each routine object has exactly name, c, header, "
        "probe, cases, mutation, completion. Preserve packet routine order and "
        "attempt_id. Use null for absent statics/cases_statics/completion. No prose, "
        "markdown, tagged blocks, extra fields, or duplicate routines."
    )
    if feedback:
        lines.append("")
        lines.append("# PREVIOUS ATTEMPT FAILED — FIX AND RE-EMIT THE LISTED ROUTINES' BLOCKS")
        lines.append(feedback)
    return "\n".join(lines)


