#!/usr/bin/env python3
"""The only writer of port files: deterministic skeletons + marked fragments.

Every model contribution lands inside marker pairs so repair rounds replace
their own previous output idempotently:

    C/H/probe:  /* >>> factory <Fn> */ ... /* <<< factory <Fn> */
    cases:      # >>> factory <Fn> ... # <<< factory <Fn>
    mutation:   # >>> factory-mutation <Fn> ... # <<< factory-mutation <Fn>
    statics:    /* >>> factory statics */ ... /* <<< factory statics */

The probe entry table row is regenerated from the adapter name, inserted
before the ``{ NULL, NULL }`` sentinel.  Writes are refused outside the
packet's four files.
"""

from __future__ import annotations
import re
from pathlib import Path

import common


class SurgeryError(ValueError):
    pass


def _span(text: str, open_mark: str, close_mark: str) -> tuple[int, int] | None:
    open_match = re.search(rf"(?m)^{re.escape(open_mark)}[ \t]*$", text)
    if open_match is None:
        return None
    close_match = re.search(
        rf"(?m)^{re.escape(close_mark)}[ \t]*$",
        text[open_match.end():],
    )
    if close_match is None:
        raise SurgeryError(f"unterminated marker {open_mark!r}")
    end = open_match.end() + close_match.end()
    if end < len(text) and text[end] == "\n":
        end += 1
    return open_match.start(), end


def _cut(text: str, span: tuple[int, int]) -> str:
    """Delete a marker span and the separator blank line it leaves behind.

    apply() writes one blank line before each block, so cutting the span
    alone leaves that blank line stacked on the previous block's: every
    remove/apply cycle would grow the file by one line and a repair round
    would never be a fixed point.
    """
    before, after = text[:span[0]], text[span[1]:]
    if before.endswith("\n\n") and (not after or after.startswith("\n")):
        before = before[:-1]
    return before + after


def _replace_span(text: str, open_mark: str, close_mark: str, replacement: str,
                  insert_at: int, *, lead: str = "", trail: str = "") -> str:
    """Replace a marker block in place, or insert it padded at ``insert_at``.

    ``lead``/``trail`` separate a newly inserted block from its neighbours.
    They must not reach the in-place branch: the separators are already in the
    file there, so re-applying a routine would add one blank line per verify
    round and every repair would produce a different artifact hash.
    """
    span = _span(text, open_mark, close_mark)
    if span:
        return text[:span[0]] + replacement + text[span[1]:]
    return text[:insert_at] + lead + replacement + trail + text[insert_at:]


def _guard_name(basename: str) -> str:
    return f"POKETCG_HOME_{re.sub(r'[^A-Za-z0-9]', '_', basename).upper()}_H"


def c_skeleton(basename: str) -> str:
    return (f'#include "home/{basename}.h"\n\n'
            f'#include "generated/hram.h"\n'
            f'#include "generated/wram.h"\n'
            f'#include "mem.h"\n')


def h_skeleton(basename: str) -> str:
    guard = _guard_name(basename)
    return (f"#ifndef {guard}\n#define {guard}\n\n#include <stdint.h>\n\n"
            f"#endif /* {guard} */\n")


def probe_skeleton(basename: str) -> str:
    return (f'#include "home/{basename}.h"\n'
            f'#include "generated/hram.h"\n'
            f'#include "generated/wram.h"\n'
            f'#include "probe.h"\n\n'
            f"const ProbeEntry probe_entries_{basename}[] = {{\n"
            f"\t{{ NULL, NULL }},\n"
            f"}};\n")


def cases_skeleton(basename: str, pret_file: str) -> str:
    return (f'"""Oracle-diff cases for poketcg/{pret_file}."""\n\n'
            'POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,\n'
            '          "d": 0xDD, "e": 0xEE, "hl": 0x1234}\n\n'
            "CONTRACT = {}\n"
            "CASES = {}\n\n"
            "from tests.cases._schema_migration import legacy_to_schema\n"
            "SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)\n\n"
            "MUTATIONS = {}\n")


def quad_paths(root: Path, basename: str) -> dict[str, Path]:
    return {
        "c": root / "src" / "home" / f"{basename}.c",
        "h": root / "src" / "home" / f"{basename}.h",
        "probe": root / "src" / "probe" / f"{basename}.c",
        "cases": root / "tests" / "cases" / f"{basename}.py",
    }

def ensure_skeletons(root: Path, packet: dict) -> None:
    paths = quad_paths(root, packet["basename"])
    if not paths["c"].exists():
        paths["c"].write_text(c_skeleton(packet["basename"]))
    if not paths["h"].exists():
        paths["h"].write_text(h_skeleton(packet["basename"]))
    if not paths["probe"].exists():
        paths["probe"].write_text(probe_skeleton(packet["basename"]))
    if not paths["cases"].exists():
        paths["cases"].write_text(cases_skeleton(packet["basename"], packet["file"]))
    elif common.classify_case_module(paths["cases"]) != "legacy-appendable":
        raise SurgeryError(
            f"{paths['cases']} hand-writes SCHEMA2_CASES; factory appends are "
            f"not supported for pre-migration modules — escalate")


ADAPTER_NAME = re.compile(r"\badapt_[A-Za-z0-9_]+\b")

DEFINE_NAME = re.compile(r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\b")

# Pre-migration probe files vary: `{NULL, NULL},` and `{ NULL, NULL },` both
# occur across landed basenames. Matching either keeps factory appends working
# on legacy files without reformatting code this packet does not own.
SENTINEL_ROW = re.compile(r"^[ \t]*\{\s*NULL\s*,\s*NULL\s*\},[ \t]*$", re.MULTILINE)

CASES_STATICS_OPEN = "# >>> factory-cases-statics"
CASES_STATICS_CLOSE = "# <<< factory-cases-statics"

INCLUDE_LINE = re.compile(r'^\s*#include\s+"([^"]+)"', re.MULTILINE)

LEGACY_SCHEMA2_ASSIGNMENT = re.compile(
    r"(?ms)^[ \t]*SCHEMA2_CASES[ \t]*=[ \t]*legacy_to_schema"
    r"[ \t\r\n]*\([ \t\r\n]*CASES[ \t\r\n]*,[ \t\r\n]*CONTRACT"
    r"[ \t\r\n]*\)[ \t]*(?:\#[^\r\n]*)?$"
)


def _legacy_tail_at(text: str, path: Path | None = None) -> int:
    if path is not None and common.classify_case_module(path) != "legacy-appendable":
        raise SurgeryError("cases module has no appendable legacy_to_schema tail")
    match = LEGACY_SCHEMA2_ASSIGNMENT.search(text)
    if match is None:
        raise SurgeryError("cases module has no appendable legacy_to_schema tail")
    return match.start()


def check_includes(root: Path, text: str) -> None:
    """Reject #include paths that do not resolve in this tree."""
    for header in INCLUDE_LINE.findall(text):
        if header in ("mem.h", "probe.h"):
            continue
        if (root / "src" / header).exists() or (root / "include" / header).exists():
            continue
        raise SurgeryError(
            f'#include "{header}" does not exist in this tree; the only valid '
            f'quoted includes are home/<basename>.h (ported callees), '
            f'generated/wram.h, generated/hram.h, generated/sram.h, mem.h. '
            f'#define needed constants locally instead')


def remove(root: Path, packet: dict, fns: list[str]) -> None:
    """Delete the marked fragments of ``fns`` from the packet's four files."""
    paths = quad_paths(root, packet["basename"])
    c_text = paths["c"].read_text()
    h_text = paths["h"].read_text()
    probe_text = paths["probe"].read_text()
    cases_text = paths["cases"].read_text()
    for fn in fns:
        open_c, close_c = f"/* >>> factory {fn} */", f"/* <<< factory {fn} */"
        for text_name, text in (("c", c_text), ("h", h_text), ("probe", probe_text)):
            span = _span(text, open_c, close_c)
            if span:
                cut = _cut(text, span)
                if text_name == "c":
                    c_text = cut
                elif text_name == "h":
                    h_text = cut
                else:
                    probe_text = cut
        probe_text = re.sub(
            rf'^\t{{ "{re.escape(fn)}", adapt_[A-Za-z0-9_]+ }},\n',
            "", probe_text, flags=re.MULTILINE)
        for open_py, close_py in ((f"# >>> factory {fn}", f"# <<< factory {fn}"),
                                  (f"# >>> factory-mutation {fn}",
                                   f"# <<< factory-mutation {fn}")):
            span = _span(cases_text, open_py, close_py)
            if span:
                cases_text = _cut(cases_text, span)
    compile(cases_text, str(paths["cases"]), "exec")
    paths["c"].write_text(c_text)
    paths["h"].write_text(h_text)
    paths["probe"].write_text(probe_text)
    paths["cases"].write_text(cases_text)


def _block_body(text: str, open_mark: str, close_mark: str, fn: str, kind: str) -> str:
    span = _span(text, open_mark, close_mark)
    if span is None:
        raise SurgeryError(f"{fn}: bundle is missing its {kind} block "
                           f"({open_mark!r} not found)")
    lines = text[span[0]:span[1]].splitlines()
    return "\n".join(lines[1:-1])


def extract(root: Path, packet: dict) -> dict:
    """Inverse of apply(): read this packet's marked fragments back out of a
    tree. Returns the same shape apply() consumes: {"statics": str|None,
    "routines": {fn: {"C","H","PROBE","CASES","MUTATION"}}}.

    Statics are extracted whole (the lane's already-merged block, a superset
    of whatever the destination already has) rather than omitted: apply()'s
    statics merge is line-deduplicating, so re-applying the full merged text
    to a fresh destination adds only genuinely new lines and never
    duplicates — the mechanism that lets two lanes' packets for the same
    basename compose instead of one clobbering the other's #define/#include.
    """
    basename = packet["basename"]
    paths = quad_paths(root, basename)
    c_text = paths["c"].read_text()
    h_text = paths["h"].read_text()
    probe_text = paths["probe"].read_text()
    cases_text = paths["cases"].read_text()

    statics_span = _span(c_text, "/* >>> factory statics */", "/* <<< factory statics */")
    statics = None
    if statics_span:
        lines = c_text[statics_span[0]:statics_span[1]].splitlines()
        statics = "\n".join(lines[1:-1])

    # Module-level helpers/addresses shared by a basename's cases, the Python
    # analogue of the C statics block. Without this, a helper defined outside
    # the per-routine markers is silently dropped on transplant and the cases
    # module dies with NameError at land time.
    cases_statics = None
    cs_span = _span(cases_text, CASES_STATICS_OPEN, CASES_STATICS_CLOSE)
    if cs_span:
        lines = cases_text[cs_span[0]:cs_span[1]].splitlines()
        cases_statics = "\n".join(lines[1:-1])

    routines: dict[str, dict[str, str]] = {}
    for routine in packet["routines"]:
        fn = routine["name"]
        open_c, close_c = f"/* >>> factory {fn} */", f"/* <<< factory {fn} */"
        open_py, close_py = f"# >>> factory {fn}", f"# <<< factory {fn}"
        open_mut = f"# >>> factory-mutation {fn}"
        close_mut = f"# <<< factory-mutation {fn}"
        open_comp = f"# >>> factory-completion {fn}"
        close_comp = f"# <<< factory-completion {fn}"
        routines[fn] = {
            "C": _block_body(c_text, open_c, close_c, fn, "C"),
            "H": _block_body(h_text, open_c, close_c, fn, "H"),
            "PROBE": _block_body(probe_text, open_c, close_c, fn, "PROBE"),
            "CASES": _block_body(cases_text, open_py, close_py, fn, "CASES"),
            "MUTATION": _block_body(cases_text, open_mut, close_mut, fn, "MUTATION"),
        }
        # Optional: a schema-2 completion override, applied after
        # SCHEMA2_CASES exists. Needed by routines whose asm tail never
        # reaches either oracle's fixed completion address (e.g. a computed
        # `ld sp, hl` unwind); absent for almost every routine.
        if _span(cases_text, open_comp, close_comp):
            routines[fn]["COMPLETION"] = _block_body(
                cases_text, open_comp, close_comp, fn, "COMPLETION")
    return {"statics": statics, "cases_statics": cases_statics, "routines": routines}


CONDITIONAL = re.compile(r"\s*#\s*(if|ifdef|ifndef|else|elif|endif)\b")
TYPEDEF_NAME = re.compile(
    r"^\}\s*([A-Za-z_]\w*)\s*;"                        # } Name;
    r"|^typedef\b[^{]*?\(\s*\*\s*([A-Za-z_]\w*)\s*\)"  # typedef ret (*Name)(args);
    r"|^typedef\s+[^{(]*?\b([A-Za-z_]\w*)\s*;\s*$")    # typedef base Name;


def _stanzas(lines: list[str]) -> list[list[str]]:
    out: list[list[str]] = []
    cur: list[str] = []
    for line in lines:
        if line.strip():
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _typedef_names(stanza: list[str]) -> list[str]:
    names = []
    for line in stanza:
        m = TYPEDEF_NAME.match(line)
        if m:
            names.append(m.group(1) or m.group(2) or m.group(3))
    return names


def _define_value(line: str) -> object:
    """Comparable value of a ``#define`` line.

    Numeric when parseable, so ``0x0Fu``/``0x0fu``/``15u`` compare equal —
    C's own redefinition rule is token-based, but two spellings of one value
    are a formatting difference, not the constant conflict worth blocking on.
    Falls back to the normalised text for non-numeric bodies (expressions,
    string literals), which then compare exactly.
    """
    body = line.split(None, 2)
    text = body[2].strip() if len(body) > 2 else ""
    token = text.split("/*")[0].strip().rstrip("uUlL")
    try:
        return int(token, 0)
    except ValueError:
        return " ".join(text.split())


def _merge_statics(basename: str, existing: list[str], new: list[str],
                  referenced: set[str] | None = None) -> list[str]:
    """Merge statics at stanza (blank-line-delimited block) granularity.

    Line-level dedup corrupts multi-line constructs: a second packet's
    ``#endif`` or ``} Name;`` matches an already-present line and is dropped,
    orphaning the rest of its construct. Stanzas dedup whole or not at all.
    Rejected outright, with feedback the model can act on:
    - preprocessor conditionals (their halves interleave across merges),
    - a #define name re-emitted with a different value,
    - a typedef name re-emitted with a different body.

    ``referenced`` is the set of identifiers the packet's routines touch. A
    #define whose value disagrees with an existing one but that no routine
    references is a speculative zombie: drop it and keep the canonical value
    already in the tree. A conflicting define a routine *does* use stays a
    hard error — that is a real disagreement the model must resolve.
"""
    for line in new:
        if CONDITIONAL.match(line):
            raise SurgeryError(
                f"{basename}: preprocessor conditionals are not allowed in "
                f"STATICS ({line.strip()!r}) — emit plain #define lines; the "
                f"merge dedups identical ones")
    old_stanzas = _stanzas(existing)
    seen = {"\n".join(s) for s in old_stanzas}
    defined: dict[str, str] = {}
    typedefs: dict[str, str] = {}
    for stanza in old_stanzas:
        for line in stanza:
            m = DEFINE_NAME.match(line)
            if m:
                defined[m.group(1)] = line
        for name in _typedef_names(stanza):
            typedefs[name] = "\n".join(stanza)
    merged = list(old_stanzas)
    for stanza in _stanzas(new):
        key = "\n".join(stanza)
        if key in seen:
            continue
        kept: list[str] = []
        for line in stanza:
            m = DEFINE_NAME.match(line)
            if m:
                name = m.group(1)
                prior = defined.get(name)
                if prior is not None:
                    if _define_value(prior) == _define_value(line):
                        continue  # same value, possibly different spelling
                    if referenced is not None and name not in referenced:
                        continue
                    raise SurgeryError(
                        f"{basename}: conflicting #define {name}: {prior!r} "
                        f"already merged, new packet emits {line!r} — reuse "
                        f"the existing constant instead of redefining it")
                defined[name] = line
            kept.append(line)
        for name in _typedef_names(stanza):
            prior = typedefs.get(name)
            if prior is not None and prior != key:
                raise SurgeryError(
                    f"{basename}: conflicting typedef {name}: a different "
                    f"definition is already merged — reuse the existing type "
                    f"or rename yours")
            typedefs[name] = key
        seen.add(key)
        if kept:
            merged.append(kept)
    out: list[str] = []
    for stanza in merged:
        if out:
            out.append("")
        out.extend(stanza)
    return out


def read_statics(root: Path, basename: str) -> list[str]:
    """Current statics body lines of the basename's .c under ``root``
    (empty when the file or block does not exist yet)."""
    path = quad_paths(root, basename)["c"]
    if not path.exists():
        return []
    span = _span(path.read_text(),
                 "/* >>> factory statics */", "/* <<< factory statics */")
    if span is None:
        return []
    body = path.read_text()[span[0]:span[1]].splitlines()[1:-1]
    return body


def apply(root: Path, packet: dict, translation: dict,
          statics_baseline: list[str] | None = None) -> list[Path]:
    """Write parsed blocks into the packet's four files under ``root``.

    ``statics_baseline`` — pre-run foreign statics content. When given, the
    statics block is rebuilt as baseline + this translation's statics, so a
    repair round may revise its OWN earlier lines freely while conflicts
    against other packets' landed content still reject. Without it (the
    integrate/land path), the current block is the merge base: cross-packet
    append-only semantics.
    """
    basename = packet["basename"]
    paths = quad_paths(root, basename)
    ensure_skeletons(root, packet)
    changed: set[Path] = set()
    referenced: set[str] = set()
    for blocks in translation.get("routines", {}).values():
        for key in ("C", "H", "PROBE", "CASES", "MUTATION", "COMPLETION"):
            referenced.update(re.findall(r"\b[A-Za-z_]\w*\b", blocks.get(key) or ""))

    # --- statics into the .c, right after the skeleton includes -------------
    c_text = paths["c"].read_text()
    statics = translation.get("statics")
    if statics:
        open_s, close_s = "/* >>> factory statics */", "/* <<< factory statics */"
        span = _span(c_text, open_s, close_s)
        if statics_baseline is not None:
            existing_lines = list(statics_baseline)
        else:
            existing_lines = []
            if span:
                body = c_text[span[0]:span[1]].splitlines()[1:-1]
                existing_lines = [l for l in body if l.strip() != close_s]
        merged = _merge_statics(basename, existing_lines,
                                statics.rstrip().splitlines(), referenced)
        block = open_s + "\n" + "\n".join(merged) + "\n" + close_s + "\n"
        include_end = 0
        for match in re.finditer(r"^#include .*$", c_text, flags=re.MULTILINE):
            include_end = match.end()
        insert_at = c_text.index("\n", include_end) + 1 if include_end else 0
        c_text = _replace_span(c_text, open_s, close_s, block, insert_at)

    h_text = paths["h"].read_text()
    probe_text = paths["probe"].read_text()
    cases_text = paths["cases"].read_text()

    cases_statics = translation.get("cases_statics")
    if cases_statics:
        cs_span = _span(cases_text, CASES_STATICS_OPEN, CASES_STATICS_CLOSE)
        existing_cs: list[str] = []
        if cs_span:
            body = cases_text[cs_span[0]:cs_span[1]].splitlines()[1:-1]
            existing_cs = [l for l in body if l.strip() != CASES_STATICS_CLOSE]
        merged_cs = _merge_statics(basename, existing_cs,
                                   cases_statics.rstrip().splitlines())
        cs_block = (CASES_STATICS_OPEN + "\n" + "\n".join(merged_cs) + "\n"
                    + CASES_STATICS_CLOSE + "\n")
        # ahead of the routine blocks, which anchor on the migration import
        tail_at = _legacy_tail_at(cases_text, paths["cases"])
        anchor = cases_text.rfind("from tests.cases._schema_migration", 0, tail_at)
        cases_text = _replace_span(cases_text, CASES_STATICS_OPEN,
                                   CASES_STATICS_CLOSE, cs_block,
                                   anchor if anchor >= 0 else tail_at,
                                   trail="\n")

    for routine in packet["routines"]:
        fn = routine["name"]
        if fn not in translation["routines"]:
            continue
        blocks = translation["routines"][fn]
        open_c = f"/* >>> factory {fn} */"
        close_c = f"/* <<< factory {fn} */"

        c_block = f"{open_c}\n{blocks['C'].rstrip()}\n{close_c}\n"
        c_text = _replace_span(c_text, open_c, close_c, c_block, len(c_text),
                               lead="\n")

        h_block = f"{open_c}\n{blocks['H'].rstrip()}\n{close_c}\n"
        endif_at = h_text.rfind("#endif")
        if endif_at < 0:
            raise SurgeryError(f"{paths['h']} has no #endif anchor")
        h_text = _replace_span(h_text, open_c, close_c, h_block, endif_at)

        adapter = blocks["PROBE"].rstrip()
        names = ADAPTER_NAME.findall(adapter)
        if not names:
            raise SurgeryError(f"{fn}: PROBE block defines no adapt_* function")
        adapter_name = names[0]
        table_at = probe_text.find("const ProbeEntry probe_entries_")
        if table_at < 0:
            raise SurgeryError(f"{paths['probe']} has no probe_entries table")
        probe_block = f"{open_c}\n{adapter}\n{close_c}\n"
        probe_text = _replace_span(probe_text, open_c, close_c, probe_block,
                                   table_at, trail="\n")
        # regenerate this routine's table row before the sentinel
        row = f'\t{{ "{fn}", {adapter_name} }},\n'
        probe_text = re.sub(
            rf'^\t{{ "{re.escape(fn)}", adapt_[A-Za-z0-9_]+ }},\n',
            "", probe_text, flags=re.MULTILINE)
        match = SENTINEL_ROW.search(probe_text)
        if match is None:
            raise SurgeryError(f"{paths['probe']} has no NULL sentinel row")
        sentinel = match.start()
        probe_text = probe_text[:sentinel] + row + probe_text[sentinel:]

        open_py = f"# >>> factory {fn}"
        close_py = f"# <<< factory {fn}"
        cases_block = f"{open_py}\n{blocks['CASES'].rstrip()}\n{close_py}\n"
        tail_at = _legacy_tail_at(cases_text, paths["cases"])
        import_at = cases_text.rfind("from tests.cases._schema_migration", 0, tail_at)
        insert_at = import_at if import_at >= 0 else tail_at
        cases_text = _replace_span(cases_text, open_py, close_py, cases_block,
                                   insert_at, trail="\n")

        open_mut = f"# >>> factory-mutation {fn}"
        close_mut = f"# <<< factory-mutation {fn}"
        mut_block = f"{open_mut}\n{blocks['MUTATION'].rstrip()}\n{close_mut}\n"
        cases_text = _replace_span(cases_text, open_mut, close_mut, mut_block,
                                   len(cases_text))

        if blocks.get("COMPLETION"):
            open_comp = f"# >>> factory-completion {fn}"
            close_comp = f"# <<< factory-completion {fn}"
            comp_block = (f"{open_comp}\n{blocks['COMPLETION'].rstrip()}\n"
                          f"{close_comp}\n")
            # appended at end so it runs after SCHEMA2_CASES is assigned
            cases_text = _replace_span(cases_text, open_comp, close_comp,
                                       comp_block, len(cases_text))

    check_includes(root, c_text)
    check_includes(root, probe_text)

    try:
        compile(cases_text, str(paths["cases"]), "exec")
    except SyntaxError as exc:
        raise SurgeryError(f"cases module is not valid Python: {exc}") from exc

    for key, text in (("c", c_text), ("h", h_text), ("probe", probe_text),
                      ("cases", cases_text)):
        path = paths[key]
        if path.read_text() != text:
            path.write_text(text)
            changed.add(path)
    return sorted(changed)
