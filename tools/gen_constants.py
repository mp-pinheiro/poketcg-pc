#!/usr/bin/env python3
"""Emit generated/constants.h and generated/text_ids.h for the selected profile.

Every integer constant defined under the disassembly's constants/ (via `const`,
`shift_const`, `DEF ... EQU`, `DEF ... RB/RW`) is evaluated by rgbasm against
that checkout, and every `textpointer` label in text/text_offsets.asm gets its
ordinal, so shared C can name constants and text ids without carrying a
per-profile literal.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.profiles import get_profile

NAME_RE = re.compile(
    r"^\s*(?:(?:shift_)?const\s+([A-Za-z_]\w*)|DEF\s+([A-Za-z_]\w*)\s+(?:EQU|RB|RW)\b|([A-Za-z_]\w*)\s+EQU\b)",
    re.MULTILINE | re.IGNORECASE,
)
PRINT_RE = re.compile(r"^([A-Za-z_]\w*)=(-?\d+)$")
STRING_FORMAT_ERROR = "Formatting string as type 'd'"
DENYLIST = frozenset({"NULL", "TRUE", "FALSE", "EOF"})


def constant_names(disasm: Path) -> list[str]:
    names: set[str] = set()
    for path in sorted((disasm / "src" / "constants").glob("*.asm")):
        for match in NAME_RE.finditer(path.read_text(encoding="utf-8", errors="replace")):
            name = match.group(1) or match.group(2) or match.group(3)
            if name and name not in DENYLIST:
                names.add(name)
    return sorted(names)


def evaluate(disasm: Path, names: list[str]) -> dict[str, int]:
    lines = ['INCLUDE "macros.asm"', 'INCLUDE "constants.asm"']
    for name in names:
        lines += [f"IF DEF({name})", f'PRINTLN "{name}={{d:{name}}}"', "ENDC"]
    with tempfile.TemporaryDirectory(prefix="gen-constants-") as directory:
        source = Path(directory) / "probe.asm"
        source.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result = subprocess.run(
            ["rgbasm", "-I", str(disasm / "src"), "-o", str(Path(directory) / "probe.o"), str(source)],
            capture_output=True, text=True, check=False,
        )
    unexpected = [line for line in result.stderr.splitlines()
                  if line.startswith("error:") and STRING_FORMAT_ERROR not in line]
    if unexpected:
        raise SystemExit("rgbasm failed:\n" + "\n".join(unexpected[:20]))
    values: dict[str, int] = {}
    for line in result.stdout.splitlines():
        match = PRINT_RE.match(line)
        if match:
            values[match.group(1)] = int(match.group(2))
    return values


def text_ids(disasm: Path) -> dict[str, int]:
    ids: dict[str, int] = {}
    ordinal = 0
    for line in (disasm / "src" / "text" / "text_offsets.asm").read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*const_def\s+(\d+)", line)
        if match:
            ordinal = int(match.group(1))
            continue
        match = re.match(r"\s*textpointer\s+(\w+)", line)
        if match:
            ids[match.group(1)] = ordinal
            ordinal += 1
    return ids


def literal(value: int) -> str:
    if value < 0:
        return f"(-{abs(value)})"
    return f"0x{value:X}u"


def render(guard: str, values: dict[str, int]) -> str:
    lines = [f"#ifndef {guard}", f"#define {guard}", ""]
    for name in sorted(values):
        lines.append(f"#define {name} {literal(values[name])}")
    lines += ["", "#endif", ""]
    return "\n".join(lines)


def write_header(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    profile = get_profile(args.profile, ROOT)
    disasm = profile.source_path(ROOT)
    values = evaluate(disasm, constant_names(disasm))
    write_header(args.out / "constants.h", render("POKETCG_GENERATED_CONSTANTS_H", values))
    ids = text_ids(disasm)
    write_header(args.out / "text_ids.h", render("POKETCG_GENERATED_TEXT_IDS_H", ids))
    print(f"gen_constants: constants.h {len(values)} names, text_ids.h {len(ids)} names")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
