#!/usr/bin/env python3
"""Re-derive `<Label>_ADDR + 0xNN` ROM offsets in Extended overlays.

relocate_rom_literals.py turns a vanilla ROM literal that falls inside a
label's span into `<Label>_ADDR + 0xNNu`. The label relocates with the
profile; the offset does not, so when the Extended routine laid its code out
differently the expression points at the wrong byte. For every such
expression in an overlay this tool finds the vanilla label (global or local)
sitting exactly at `vanilla(Label) + NN`, looks the same label up in the
Extended table, and rewrites the offset to the Extended distance (or to the
global label itself). Offsets with no vanilla label at their target cannot be
derived and are reported for a hand port.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.profiles import get_profile, symbol_table

OFFSET_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)_ADDR \+ (0x[0-9A-Fa-f]+|[0-9]+)u?\b")
COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--check", action="store_true", help="report only, write nothing")
    args = parser.parse_args()
    vanilla = symbol_table(get_profile("vanilla", ROOT), ROOT)
    extended = symbol_table(get_profile("extended", ROOT), ROOT)
    at_vanilla: dict[tuple[int, int], list[str]] = defaultdict(list)
    for name, (bank, address) in vanilla.items():
        at_vanilla[(bank, address)].append(name)
    at_extended: dict[tuple[int, int], list[str]] = defaultdict(list)
    extended_locals: dict[tuple[int, int], set[str]] = defaultdict(set)
    for name, (bank, address) in extended.items():
        if "." in name:
            extended_locals[(bank, address)].add(name.split(".")[0])
        else:
            at_extended[(bank, address)].append(name)
    paths = [path.resolve() for path in args.paths] or sorted((ROOT / "src" / "profiles" / "extended").rglob("*.[ch]"))
    total = fixed = manual = 0
    for path in paths:
        text = path.read_text()
        code = COMMENT_RE.sub(lambda match: " " * len(match.group(0)), text)
        edits: list[tuple[int, int, str]] = []
        for match in OFFSET_RE.finditer(code):
            label, offset_text = match.group(1), match.group(2)
            if label not in vanilla or label not in extended:
                continue
            bank, address = vanilla[label]
            if address >= 0x8000:
                continue
            total += 1
            offset = int(offset_text, 0)
            target = address + offset
            candidates = [name for name in at_vanilla.get((bank, target), ()) if name in extended]
            candidates.sort(key=lambda name: (not name.startswith(label + "."), "." in name, name))
            if not candidates:
                line = text.count("\n", 0, match.start()) + 1
                if label in extended_locals.get((extended[label][0], extended[label][1] + offset), set()):
                    continue
                already = at_extended.get((extended[label][0], extended[label][1] + offset), [])
                direct = at_extended.get((bank, target), [])
                if direct and not already and "src/profiles/" in str(path):
                    replacement = f"{direct[0]}_ADDR"
                    fixed += 1
                    print(f"{path.relative_to(ROOT)}:{line}: {match.group(0)} -> {replacement} (Extended label at the literal value)")
                    edits.append((match.start(), match.end(), replacement))
                    continue
                manual += 1
                print(f"{path.relative_to(ROOT)}:{line}: {label}_ADDR + {offset_text}: no label at "
                      f"{bank:02x}:{target:04x} (hand port)")
                continue
            chosen = candidates[0]
            ext_bank, ext_target = extended[chosen]
            if ext_bank != extended[label][0]:
                manual += 1
                print(f"{path.relative_to(ROOT)}: {label}_ADDR + {offset_text}: {chosen} changed bank in Extended (hand port)")
                continue
            if "." not in chosen:
                replacement = f"{chosen}_ADDR"
            elif chosen.count(".") == 1:
                replacement = f"{chosen.replace('.', '__')}_ADDR"
            else:
                new_offset = ext_target - extended[label][1]
                if new_offset == offset:
                    continue
                if new_offset < 0:
                    manual += 1
                    print(f"{path.relative_to(ROOT)}: {label}_ADDR + {offset_text}: {chosen} precedes {label} in Extended (hand port)")
                    continue
                replacement = f"{label}_ADDR + 0x{new_offset:02X}u"
            if replacement == match.group(0):
                continue
            fixed += 1
            line = text.count("\n", 0, match.start()) + 1
            print(f"{path.relative_to(ROOT)}:{line}: {match.group(0)} -> {replacement} ({chosen})")
            edits.append((match.start(), match.end(), replacement))
        if edits and not args.check:
            for start, end, replacement in sorted(edits, reverse=True):
                text = text[:start] + replacement + text[end:]
            path.write_text(text)
    print(f"offsets={total} rewritten={fixed} hand_port={manual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
