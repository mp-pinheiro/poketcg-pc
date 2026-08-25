#!/usr/bin/env python3
"""Render translation prompts from packets and parse marker-body replies.

Generator output is deliberately fragment-sized: each block is inserted into
an existing quartet file by the verifier.  The prompt must never imply that a
complete C, header, probe, or cases file should be returned.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT
from verify import POISON, RESERVED


def _marker_body(lines: list[str], open_mark: str, close_mark: str) -> str:
    """Text between two exact marker lines; empty when either is absent."""
    try:
        start = lines.index(open_mark)
        end = lines.index(close_mark, start + 1)
    except ValueError:
        return ""
    return "\n".join(lines[start + 1:end]).rstrip()


def _worked_case_example(basename: str) -> tuple[str, str] | None:
    """Verbatim cases and mutation marker bodies of one landed routine.

    Surgery brackets every factory-written routine with markers, so the text
    lifted here compiled, passed the schema audit and matched the ROM comparator.
    Copying it whole demonstrates the contract shape, the poisoned registers, the
    byte-string seeds and a unique, observable mutation anchor all at once; a
    line-scraped approximation of the same tables demonstrates none of them. The
    smallest qualifying routine wins so prompts gain a correct example without
    bloat.
    """
    directory = ROOT / "tests" / "cases"
    ordered = [basename, *sorted(
        path.stem for path in directory.glob("*.py")
        if not path.stem.startswith("_"))]
    seen: set[str] = set()
    for name in ordered:
        if name in seen:
            continue
        seen.add(name)
        path = directory / (name + ".py")
        if not path.is_file():
            continue
        lines = path.read_text().splitlines()
        best: tuple[int, str, str, str] | None = None
        for line in lines:
            if not line.startswith("# >>> factory ") or "factory-mutation" in line:
                continue
            fn = line[len("# >>> factory "):].strip()
            cases = _marker_body(lines, "# >>> factory " + fn, "# <<< factory " + fn)
            mutation = _marker_body(
                lines, "# >>> factory-mutation " + fn, "# <<< factory-mutation " + fn)
            # Smallest is only useful if it is also instructive: the example has to
            # carry real CASES entries, a poisoned case and a populated contract, or
            # it teaches none of the rules it is here to demonstrate.
            if not mutation or "CASES[" not in cases or "POISON" not in cases:
                continue
            if '"compare": ()' in cases or "'compare': ()" in cases:
                continue
            score = len(cases) + len(mutation)
            if best is None or (score, fn) < (best[0], best[1]):
                best = (score, fn, cases, mutation)
        if best is not None:
            return best[2], best[3]
    return None


def _fragment_example(basename: str) -> str:
    """Return a small, sanitized marker-body example from an existing quartet."""
    home = (ROOT / "src/home" / f"{basename}.c").read_text()
    header = (ROOT / "src/home" / f"{basename}.h").read_text()
    probe = (ROOT / "src/probe" / f"{basename}.c").read_text()
    cases = (ROOT / "tests/cases" / f"{basename}.py").read_text()

    def without_directives(text: str) -> str:
        return "\n".join(line for line in text.splitlines()
                         if not line.lstrip().startswith("#")).strip()

    def first_function(text: str) -> str:
        match = re.search(r"(?m)^[A-Za-z_][^;\n]*\([^;\n]*\)\s*\{", text)
        if not match:
            return without_directives(text)
        depth = 0
        for index in range(match.end() - 1, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    return without_directives(text[match.start():index + 1])
        return without_directives(text[match.start():])

    adapter = re.search(
        r"(?ms)^[A-Za-z_][^;\n]*\badapt_[A-Za-z0-9_]+\s*\([^;\n]*\)\s*\{.*?^}",
        probe,
    )
    case_lines = [
        line.strip() for line in cases.splitlines()
        if re.match(r"^(?:CONTRACT|CASES)\s*\[", line.strip())
    ]
    mutation_lines = [
        line.strip() for line in cases.splitlines()
        if re.match(r"^MUTATIONS\s*\[", line.strip())
    ]
    worked = _worked_case_example(basename)
    if worked is not None:
        case_lines, mutation_lines = [worked[0]], [worked[1]]
    return "\n".join((
        "FRAGMENT EXAMPLE (marker bodies only; never copy a complete file):",
        f"C body:\n{first_function(home)}",
        "Header declarations:\n" + without_directives(header),
        "Probe adapter body:\n" + (adapter.group(0).strip() if adapter else
                                    "static void adapt_Name(ProbeState *s) {}"),
        "Cases assignments:\n" + ("\n".join(case_lines) or
                                   'CONTRACT["Name"] = {};\\nCASES["Name"] = [];'),
        "Mutation assignment:\n" + ("\n".join(mutation_lines) or
                                     'MUTATIONS["Name"] = {};'),
    ))


def example_quad(basename: str) -> str:
    """Compatibility name retained for callers; returns fragments, not files."""
    return _fragment_example(basename)

def render(packet: dict, feedback: str | None = None,
           targets: list[str] | None = None) -> str:
    wanted = set(targets) if targets else {r["name"] for r in packet["routines"]}
    lines: list[str] = [
        "You are a credential-free port generator. The packet below is complete context.",
        "Return one TranslationReplyV2 JSON object and nothing else.",
        "Every value below is a marker BODY inserted into an existing file. "
        "Never return a complete file.",
        "",
    ]
    lines.append(example_quad(packet["example"]))
    lines.append("")
    lines.append("# FRAGMENT RULES — MANDATORY")
    lines.extend((
        "C: exactly one routine definition; no #include, #if, #define, guards, or file wrapper.",
        "header: only typedefs/declarations inserted before the existing guard #endif; "
        "no guard or include lines. A multi-register result struct is typedef'd HERE and "
        "only here — repeating the typedef in the C fragment is a redefinition error.",
        "probe: exactly one static void adapt_<name>(ProbeState *s) definition; "
        "no ProbeEntry, probe table, sentinel, or module wrapper.",
        "cases: only CONTRACT[\"<name>\"] and CASES[\"<name>\"] assignments.",
        "mutation: only MUTATIONS[\"<name>\"] assignment.",
        "statics: the ONLY place an #include or #define may appear. A <label>_ADDR macro "
        "or a g_wram/g_sram accessor needs its generated header here. The only quoted "
        f"includes that resolve are home/<basename>.h (basename `{packet['basename']}` and "
        "any ported callee's header), generated/wram.h, generated/hram.h, "
        "generated/sram.h, and mem.h; anything else fails the tree check. A constant the "
        "asm uses and this packet does not list must be #define'd here from its numeric "
        "value, never assumed to exist.",
        "cases_statics: module-level Python helpers and addresses shared by this "
        "basename's cases; do not repeat CONTRACT/CASES/MUTATIONS/SCHEMA2_CASES tables.",
        "Do not emit file guards, complete modules, prose, markdown, or tagged blocks.",
        "",
    ))
    poison = " ".join(f"{name}=0x{value:02X}" if value <= 0xFF else f"{name}=0x{value:04X}"
                      for name, value in POISON.items())
    lines.append("# CASE RULES — ENFORCED MECHANICALLY BEFORE ANY ORACLE RUN")
    lines.extend((
        "CONTRACT[\"<name>\"] = {\"compare\": (...), \"preserve\": (...)} names registers. "
        "`compare` is every register the oracle observes; `preserve` is the subset of "
        "those that must come back unchanged. `preserve` MUST be a subset of `compare` "
        "— list a preserved register in both, never in `preserve` alone.",
        f"At least one case in CASES[\"<name>\"] must poison four or more registers with "
        f"these exact values: {poison}.",
        f"No case may seed, read, or expect an address in "
        f"${RESERVED.start:04X}-${RESERVED.stop - 1:04X}: that range is the oracle's own "
        f"call frame.",
        "The port has no interrupt handler; the reference ROM does. Its VBlank handler "
        "clears wVBlankOAMCopyToggle ($CAC0), flushes wFlushPaletteFlags ($CABF), and "
        "mirrors hSCX/hSCY/hWX/hWY and wLCDC into the LCD registers, so those bytes "
        "diverge for any routine that enables the LCD, loads a scene, or lets frames "
        "elapse. Never read or expect a byte the VBlank handler mutates, and never "
        "declare a sweeping whole-WRAM or whole-VRAM observation: the comparator then "
        "diffs everything and every unported callee side effect lands as a mismatch. "
        "Observe only the bytes this routine's own asm writes.",
        "EVERY `wram` seed address is implicitly compared. tools/oracle/gbref/"
        "compare_one.py builds the compared bus spans from your declared reads UNION "
        "the addresses of your wram seeds, so a case with an empty compare tuple and "
        "no reads still fails if any byte it seeded ends up different. Seed a WRAM "
        "address only when both the real ROM and the port leave it the same value. "
        "`hram` seeds are not compared unless the case is a snapshot case, so a "
        "control byte that lives in HRAM belongs in `hram`, never in `wram`.",
        "A reference-side BUDGET_EXHAUSTED is a seeding defect, never a budget defect: "
        "raising instruction_budget or cycle_budget cannot fix it. The real ROM spins "
        "when a list it walks has no terminator. A routine that prints text reaches "
        "Func_235e, which walks a glyph cache (key1 $C6xx, key2 $C7xx, next $C8xx, head "
        "index in hffa9 at $FFA9) and cycles forever on an uninitialised chain. Do not "
        "hand-seed those pages: one zeroed byte only survives until the cache interns "
        "its first glyph. Run the game's own initialiser instead, exactly as the landed "
        "case modules do - \"setup\": [{\"fn\": \"SetupText\", \"d\": 0x20, \"e\": 0x40}] - "
        "which zeroes hffa9 and the whole key1 page. GetCardIDFromDeckIndex spins the "
        "same way on an unterminated card list; seed that list so the lookup ends.",
        "The other reference-side hang is WaitForVBlank (poketcg/src/home/lcd.asm:2-16). "
        "It reads wLCDC at $CABB, and if the LCD-enable bit is clear it returns at once; "
        "if that bit is set it halts until a VBlank interrupt bumps wVBlankCounter, "
        "which never happens inside the oracle's synthetic call frame, so the case burns "
        "its whole budget at pc $0271. Any routine reaching DoFrame, "
        "DrawWideTextBox_WaitForInput, or WaitForWideTextBoxInput therefore needs "
        "wram={0xCABB: b\"\\x00\"} to stay bounded, exactly as tests/cases/copy.py seeds "
        "that byte for the opposite branch. Seeding it is safe under the rule above "
        "because both sides leave it identical - unless the routine itself calls "
        "EnableLCD before the wait, in which case pick a case that exits before it.",
        "Memory seeds are byte strings, never ints: wram={0xC500: b\"\\x00\\x01\"}. "
        "`read` and `expect` use the same shape.",
        "MUTATIONS[\"<name>\"][\"case_ids\"] entries must read <name>-<index> with index "
        "below the number of cases you declared, and \"before\" must appear verbatim in "
        "your C fragment.",
        "That \"before\" string must occur EXACTLY ONCE in your C fragment. A string "
        "that appears twice cannot be located unambiguously and is rejected as "
        "\"mutation anchor is not unique\"; extend it with surrounding tokens until it "
        "is unique.",
        "Choose a \"before\" line whose corruption at least one listed case would "
        "actually detect. The mutation test corrupts the routine and REQUIRES the "
        "cases to fail; a mutation on a line no case observes is rejected as "
        "\"corrupted routine still passed\". Seed and expect whatever that line "
        "influences.",
        "A case with oracle=False needs a non-empty why plus one of expect, expect_regs, "
        "expect_sram, expect_vram.",
        "Every routine needs at least one primary schema-2 case. Primary cases run "
        "against the real ROM; scene, intentional-transform, native-stress, and "
        "dependency-blocked cases are supplemental evidence only.",
        "MUTATIONS[\"<name>\"][\"case_ids\"] may select only primary cases as mutation "
        "witnesses; non-primary cases cannot certify the source mutation.",
        "The cases fragment must be valid Python on its own line-by-line: no positional "
        "argument after a keyword argument, no bare C macro names (they do not exist in "
        "Python — use the numeric addresses listed below).",
        "A routine entered mid-frame — a `jp` target whose epilogue pops words its "
        "own caller pushed, or a body that reads sp+N above its own frame — declares "
        "stack=[w0, w1] in every case: caller-pushed words below the synthesized "
        "return address, in push order, four maximum. w0 is the caller's first push, "
        "so the routine's first pop reads the LAST element. Its probe adapter takes "
        "those words from s->stack[0 .. s->stack_count-1] because the native side has "
        "no GB stack, and its C signature accepts them as ordinary parameters. Omit "
        "stack entirely for every routine whose pushes and pops balance.",
        "",
    ))
    lines.append("# YOUR TASK")
    lines.append(f"Port the following routines from poketcg/{packet['file']} "
                 f"into basename `{packet['basename']}`.")
    lines.append(
        f"Case module appendability: {packet.get('case_appendability', 'new')}."
    )
    if packet.get("existing"):
        existing = packet["existing"]
        lines.append("")
        lines.append(
            "Append mode: the existing quartet files and guard remain in place. "
            "Emit only new marker bodies; already-ported routines are not requested."
        )
        lines.append(f"Already-ported routines: "
                     f"{', '.join(existing['contract_keys']) or 'none'}.")
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
        "probe, cases, mutation, completion. Use null for absent "
        "statics/cases_statics/completion. No prose, markdown, tagged blocks, extra "
        "fields, or duplicate routines."
    )
    lines.append(f'attempt_id must be exactly "{packet["attempt_id"]}".')
    lines.append("routines must be exactly, in this order: "
                 + ", ".join(r["name"] for r in packet["routines"]) + ".")
    if feedback:
        lines.append("")
        lines.append("# PREVIOUS ATTEMPT FAILED — FIX AND RE-EMIT THE LISTED ROUTINES' BLOCKS")
        lines.append(feedback)
    return "\n".join(lines)


