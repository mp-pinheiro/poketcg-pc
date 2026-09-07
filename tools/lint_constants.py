#!/usr/bin/env python3
"""Gate against hand-typed constants that disagree with the disassembly.

Every ported routine names the asm's constants in local ``#define`` lines, and
each one is a byte typed from memory. The oracle only catches a wrong value
when a case happens to observe it, so a bad TX_SYMBOL index, energy flag, deck
id or data-table address can sit under a green diff for weeks and surface as a
TAS divergence a hundred seconds of bisection later. This lint closes that hole
mechanically: a ``#define`` whose name is an asm symbol must carry the asm's
value.

Three sources of truth, matched by exact name only (no case folding, no
snake-case guessing -- ``ChallengeHallNPCs`` and ``ChallengeHallNPCS`` are
different labels):

  * rgbasm.  ``macros.asm`` + ``constants.asm`` are assembled with one
    ``PRINTLN`` per candidate name, so ``const_def`` chains, ``EQU``
    expressions and shifted flags resolve exactly as the ROM build resolves
    them. Names the assembler cannot print as integers (string equates) are
    skipped.
  * ``text/text_offsets.asm``.  A ``NameText`` define is a text id: the
    ``textpointer`` ordinal, starting at ``const_def 1``.
  * ``poketcg.sym``.  A define named exactly like a ROM label is that label's
    address (the low 16 bits; a ``bank << 16 | address`` form is accepted).

A negative asm value (``MENU_CANCEL`` is ``-1``) matches its 8- or 16-bit
two's complement. Everything else is a mismatch and fails the build.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DISASM = REPO_ROOT / "poketcg"
DEFAULT_SOURCES = ("src/home", "src/probe")

DEFINE_RE = re.compile(
    r"^#define\s+([A-Za-z_]\w*)\s+\(?\s*(-?0[xX][0-9A-Fa-f]+|-?\d+)\s*[uUlL]{0,2}\s*\)?\s*(?://.*|/\*.*)?$"
)
SYM_RE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+([A-Za-z_][\w.]*)\s*$")
PRINT_RE = re.compile(r"^([A-Za-z_]\w*)=(-?\d+)$")
STRING_FORMAT_ERROR = "Formatting string as type 'd'"


def collect_defines(roots: list[Path]) -> dict[str, list[tuple[Path, int, int]]]:
    defines: dict[str, list[tuple[Path, int, int]]] = defaultdict(list)
    for root in roots:
        paths = [root] if root.is_file() else sorted(list(root.rglob("*.c")) + list(root.rglob("*.h")))
        for path in paths:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = DEFINE_RE.match(line)
                if match:
                    defines[match.group(1)].append((path, number, int(match.group(2), 0)))
    return defines


def asm_values(names: list[str]) -> dict[str, int]:
    """Resolve names through rgbasm; names without an integer value are absent."""
    lines = ['INCLUDE "macros.asm"', 'INCLUDE "constants.asm"']
    for name in names:
        lines += [f"IF DEF({name})", f'PRINTLN "{name}={{d:{name}}}"', "ENDC"]
    with tempfile.TemporaryDirectory(prefix="lint-constants-") as directory:
        source = Path(directory) / "probe.asm"
        source.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result = subprocess.run(
            ["rgbasm", "-I", str(DISASM / "src"), "-o", str(Path(directory) / "probe.o"), str(source)],
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


def text_ids() -> dict[str, int]:
    ids: dict[str, int] = {}
    ordinal = 0
    for line in (DISASM / "src" / "text" / "text_offsets.asm").read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*const_def\s+(\d+)", line)
        if match:
            ordinal = int(match.group(1))
            continue
        match = re.match(r"\s*textpointer\s+(\w+)", line)
        if match:
            ids[match.group(1)] = ordinal
            ordinal += 1
    return ids


def rom_labels() -> dict[str, tuple[int, int]]:
    labels: dict[str, tuple[int, int]] = {}
    for line in (DISASM / "poketcg.sym").read_text(encoding="utf-8").splitlines():
        match = SYM_RE.match(line)
        if match and "." not in match.group(3):
            labels.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return labels


def matches(c_value: int, asm_value: int) -> bool:
    if c_value == asm_value:
        return True
    if asm_value < 0:
        return c_value in (asm_value & 0xFF, asm_value & 0xFFFF)
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=DEFAULT_SOURCES,
                        help="source files or directories to lint")
    args = parser.parse_args(argv)
    roots = [REPO_ROOT / path for path in args.paths]
    defines = collect_defines(roots)
    names = sorted(defines)
    constants = asm_values(names)
    ids = text_ids()
    labels = rom_labels()

    failures: list[str] = []
    checked = 0
    for name in names:
        expected: int | None = None
        source = ""
        if name in constants:
            expected, source = constants[name], "constants.asm"
        elif name in ids:
            expected, source = ids[name], "text_offsets.asm"
        elif name in labels:
            bank, address = labels[name]
            expected, source = address, f"poketcg.sym bank {bank:02x}"
        if expected is None:
            continue
        for path, number, value in defines[name]:
            checked += 1
            ok = matches(value, expected)
            if not ok and source.startswith("poketcg.sym"):
                ok = value == ((labels[name][0] << 16) | labels[name][1])
            if not ok:
                failures.append(
                    f"{path.relative_to(REPO_ROOT)}:{number}: {name} is 0x{value:X}, "
                    f"{source} says 0x{expected & 0xFFFFFFFF:X} ({expected})"
                )
    for failure in failures:
        print(failure)
    print(f"lint-constants: {checked} defines checked against the disassembly, "
          f"{len(failures)} mismatched", file=sys.stderr if failures else sys.stdout)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
