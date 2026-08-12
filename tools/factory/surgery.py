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


class SurgeryError(ValueError):
    pass


def _span(text: str, open_mark: str, close_mark: str) -> tuple[int, int] | None:
    start = text.find(open_mark)
    if start < 0:
        return None
    end = text.find(close_mark, start)
    if end < 0:
        raise SurgeryError(f"unterminated marker {open_mark!r}")
    end = text.index("\n", end + len(close_mark)) + 1 if "\n" in text[end:] else len(text)
    return start, end


def _replace_span(text: str, open_mark: str, close_mark: str, replacement: str,
                  insert_at: int) -> str:
    span = _span(text, open_mark, close_mark)
    if span:
        return text[:span[0]] + replacement + text[span[1]:]
    return text[:insert_at] + replacement + text[insert_at:]


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
    elif "legacy_to_schema" not in paths["cases"].read_text():
        raise SurgeryError(
            f"{paths['cases']} hand-writes SCHEMA2_CASES; factory appends are "
            f"not supported for pre-migration modules — escalate")


ADAPTER_NAME = re.compile(r"\badapt_[A-Za-z0-9_]+\b")

INCLUDE_LINE = re.compile(r'^\s*#include\s+"([^"]+)"', re.MULTILINE)


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
                cut = text[:span[0]] + text[span[1]:]
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
                cases_text = cases_text[:span[0]] + cases_text[span[1]:]
    compile(cases_text, str(paths["cases"]), "exec")
    paths["c"].write_text(c_text)
    paths["h"].write_text(h_text)
    paths["probe"].write_text(probe_text)
    paths["cases"].write_text(cases_text)



def apply(root: Path, packet: dict, translation: dict) -> list[Path]:
    """Write parsed blocks into the packet's four files under ``root``."""
    basename = packet["basename"]
    paths = quad_paths(root, basename)
    ensure_skeletons(root, packet)
    changed: set[Path] = set()

    # --- statics into the .c, right after the skeleton includes -------------
    # Merged, never replaced: repair rounds may emit partial statics and must
    # not lose earlier defines/includes.
    c_text = paths["c"].read_text()
    statics = translation.get("statics")
    if statics:
        open_s, close_s = "/* >>> factory statics */", "/* <<< factory statics */"
        span = _span(c_text, open_s, close_s)
        existing_lines: list[str] = []
        if span:
            body = c_text[span[0]:span[1]].splitlines()[1:-1]
            existing_lines = [l for l in body if l.strip() != close_s]
        merged = list(existing_lines)
        for line in statics.rstrip().splitlines():
            if line.strip() and line not in merged:
                merged.append(line)
            elif not line.strip() and (not merged or merged[-1].strip()):
                merged.append(line)
        block = open_s + "\n" + "\n".join(merged) + "\n" + close_s + "\n"
        include_end = 0
        for match in re.finditer(r"^#include .*$", c_text, flags=re.MULTILINE):
            include_end = match.end()
        insert_at = c_text.index("\n", include_end) + 1 if include_end else 0
        c_text = _replace_span(c_text, open_s, close_s, block, insert_at)

    h_text = paths["h"].read_text()
    probe_text = paths["probe"].read_text()
    cases_text = paths["cases"].read_text()

    for routine in packet["routines"]:
        fn = routine["name"]
        if fn not in translation["routines"]:
            continue
        blocks = translation["routines"][fn]
        open_c = f"/* >>> factory {fn} */"
        close_c = f"/* <<< factory {fn} */"

        c_block = f"\n{open_c}\n{blocks['C'].rstrip()}\n{close_c}\n"
        c_text = _replace_span(c_text, open_c, close_c, c_block, len(c_text))

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
        probe_block = f"{open_c}\n{adapter}\n{close_c}\n\n"
        probe_text = _replace_span(probe_text, open_c, close_c, probe_block, table_at)
        # regenerate this routine's table row before the sentinel
        row = f'\t{{ "{fn}", {adapter_name} }},\n'
        probe_text = re.sub(
            rf'^\t{{ "{re.escape(fn)}", adapt_[A-Za-z0-9_]+ }},\n',
            "", probe_text, flags=re.MULTILINE)
        sentinel = probe_text.find("\t{ NULL, NULL },")
        if sentinel < 0:
            raise SurgeryError(f"{paths['probe']} has no NULL sentinel row")
        probe_text = probe_text[:sentinel] + row + probe_text[sentinel:]

        open_py = f"# >>> factory {fn}"
        close_py = f"# <<< factory {fn}"
        cases_block = f"{open_py}\n{blocks['CASES'].rstrip()}\n{close_py}\n\n"
        tail_at = cases_text.find("SCHEMA2_CASES = legacy_to_schema")
        if tail_at < 0:
            raise SurgeryError(f"{paths['cases']} lost its legacy_to_schema tail")
        # the import line sits directly above the assignment; insert above it
        import_at = cases_text.rfind("from tests.cases._schema_migration", 0, tail_at)
        insert_at = import_at if import_at >= 0 else tail_at
        cases_text = _replace_span(cases_text, open_py, close_py, cases_block, insert_at)

        open_mut = f"# >>> factory-mutation {fn}"
        close_mut = f"# <<< factory-mutation {fn}"
        mut_block = f"{open_mut}\n{blocks['MUTATION'].rstrip()}\n{close_mut}\n"
        cases_text = _replace_span(cases_text, open_mut, close_mut, mut_block,
                                   len(cases_text))

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
