#!/usr/bin/env python3
"""Replace bank-switched ROM address literals in C with generated rom.h labels.

Every `0x4000`-`0x7FFF` literal is resolved against the vanilla symbol table:
inside a factory block in the block's own bank (or the bank named by an
enclosing `rom_ptr(<bank>u, ...)` or a `/* bank N */` note), and in a
`#define` by the define's name or by the address being unique across banks.
A literal that names a global label becomes `<Label>_ADDR`; one that falls
inside a label's span becomes `(<Label>_ADDR + 0xNNu)`, so the same C compiles
against either profile's `rom.h`. Vanilla object code is unchanged because the
macros expand to the same numbers. Unresolved literals are reported, never
guessed.
"""

from __future__ import annotations

import argparse
import bisect
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.profiles import get_profile, symbol_table

LITERAL_RE = re.compile(r"\b0[xX]([0-7][0-9A-Fa-f]{3})[uU]?\b")
FACTORY_RE = re.compile(r"/\* >>> factory (\w+) \*/\n(.*?)/\* <<< factory \1 \*/", re.DOTALL)
COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
ROM_PTR_RE = re.compile(r"rom_ptr\(\s*(\d+)[uU]?\s*,")
BANK_COMMENT_RE = re.compile(r"/\*\s*bank\s+(\d+)\s*\*/")
DEFINE_RE = re.compile(r"^#define\s+(\w+)\s+0[xX][4-7][0-9A-Fa-f]{3}[uU]?\b")
INCLUDE_RE = re.compile(r'^#include "generated/[a-z]+\.h"\n', re.MULTILINE)
MAX_OFFSET = 0x100
MASK_LINE_RE = re.compile(r"0x3FFF|~0x8000|<<\s*14|mbc5_write|rRTC|0x4000u\s*\)\s*;")
SELF_DEFINE_RE = re.compile(r"^#define (\w+) \1[ \t]*\n", re.MULTILINE)


class Resolver:
    def __init__(self, labels: dict[str, tuple[int, int]], preferred: set[str]):
        self.labels = labels
        self.preferred = preferred
        self.index: dict[tuple[int, int], list[str]] = defaultdict(list)
        for name, (bank, address) in labels.items():
            if 0x0150 <= address < 0x8000 and "." not in name:
                self.index[(bank, address)].append(name)
        self.tables: dict[int, list[int]] = defaultdict(list)
        for bank, address in self.index:
            self.tables[bank].append(address)
        for addresses in self.tables.values():
            addresses.sort()

    def choose(self, names: list[str]) -> str:
        for name in names:
            if name in self.preferred:
                return name
        return names[0]

    def exact(self, bank: int, address: int) -> str | None:
        names = self.index.get((bank, address))
        return f"{self.choose(names)}_ADDR" if names else None

    def offset(self, bank: int, address: int) -> str | None:
        addresses = self.tables.get(bank, [])
        position = bisect.bisect_right(addresses, address) - 1
        if position < 0:
            return None
        base = addresses[position]
        if address - base > MAX_OFFSET:
            return None
        label = self.choose(self.index[(bank, base)])
        if label not in self.preferred:
            return None
        return f"({label}_ADDR + 0x{address - base:02X}u)"

    def banks_at(self, address: int) -> list[int]:
        return sorted({bank for (bank, candidate) in self.index if candidate == address})

    def by_define(self, define: str, address: int) -> str | None:
        banks = self.banks_at(address)
        wanted = re.sub(r"_(ADDR|BANK)$", "", define).replace("_", "").lower()
        matches = sorted(
            {name for bank in banks for name in self.index[(bank, address)]
             if name.replace("_", "").lower() == wanted}
        )
        if len(matches) == 1:
            return f"{matches[0]}_ADDR"
        base = re.sub(r"_(START_SCRIPT|ADDR|BANK)$", "", define)
        located = self.labels.get(base)
        if located is not None and base in self.preferred and 0 <= address - located[1] <= MAX_OFFSET:
            return f"({base}_ADDR + 0x{address - located[1]:02X}u)"
        return None


def masked(text: str) -> str:
    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    return STRING_RE.sub(blank, COMMENT_RE.sub(blank, text))


def relocate(text: str, resolver: Resolver) -> tuple[str, list[str]]:
    code = masked(text)
    spans: list[tuple[int, int, int | None]] = []
    bank_votes: dict[int, int] = defaultdict(int)
    for block in FACTORY_RE.finditer(text):
        bank = resolver.labels.get(block.group(1), (0, 0))[0]
        spans.append((block.start(), block.end(), bank or None))
        if bank:
            bank_votes[bank] += 1
    file_bank = max(bank_votes, key=bank_votes.get) if bank_votes else None
    edits: list[tuple[int, int, str]] = []
    unresolved: list[str] = []
    for literal in LITERAL_RE.finditer(code):
        address = int(literal.group(1), 16)
        position = literal.start()
        line_start = code.rfind("\n", 0, position) + 1
        line_end = code.find("\n", position)
        if line_end < 0:
            line_end = len(code)
        line = code[line_start:line_end]
        raw_line = text[line_start:line_end]
        if MASK_LINE_RE.search(raw_line):
            continue
        bank = None
        for start, end, block_bank in spans:
            if start <= position < end:
                bank = block_bank
                break
        pointer = ROM_PTR_RE.search(line)
        if pointer is not None and pointer.end() <= position - line_start:
            bank = int(pointer.group(1))
        comment = BANK_COMMENT_RE.search(raw_line)
        if comment is not None:
            bank = int(comment.group(1))
        define = DEFINE_RE.match(raw_line)
        replacement = None
        if address < 0x4000:
            if address >= 0x0150:
                replacement = resolver.exact(0, address)
            if replacement is None:
                continue
        elif bank is not None:
            replacement = resolver.exact(bank, address) or resolver.offset(bank, address)
        elif define is not None:
            replacement = resolver.by_define(define.group(1), address)
            if replacement is None and file_bank is not None:
                replacement = resolver.exact(file_bank, address) or resolver.offset(file_bank, address)
        elif file_bank is not None:
            replacement = resolver.exact(file_bank, address) or resolver.offset(file_bank, address)
        if replacement is None:
            where = f"bank {bank}" if bank is not None else "no bank context"
            unresolved.append(f"0x{address:04X} ({where}) {raw_line.strip()[:80]}")
            continue
        edits.append((literal.start(), literal.end(), replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    text = SELF_DEFINE_RE.sub("", text)
    if edits and '#include "generated/rom.h"' not in text:
        match = INCLUDE_RE.search(text)
        if match is not None:
            text = text[:match.start()] + '#include "generated/rom.h"\n' + text[match.start():]
        else:
            text = '#include "generated/rom.h"\n' + text
    return text, unresolved


MACRO_RE = re.compile(r"\(([A-Za-z_]\w*)_ADDR \+ 0x([0-9A-Fa-f]{2})u\)|\b([A-Za-z_]\w*)_ADDR\b")


def baseline_macros(path: Path) -> set[str]:
    shown = subprocess.run(["jj", "file", "show", "-r", "@-", str(path.relative_to(ROOT))],
                           cwd=ROOT, text=True, capture_output=True, check=False)
    if shown.returncode != 0:
        return set()
    return {match.group(1) or match.group(3) for match in MACRO_RE.finditer(shown.stdout)}


def revert_foreign(text: str, resolver: Resolver, keep: set[str], all_new: bool = False) -> tuple[str, int]:
    code = masked(text)
    spans: list[tuple[int, int, int | None]] = []
    bank_votes: dict[int, int] = defaultdict(int)
    for block in FACTORY_RE.finditer(text):
        bank = resolver.labels.get(block.group(1), (0, 0))[0]
        spans.append((block.start(), block.end(), bank or None))
        if bank:
            bank_votes[bank] += 1
    file_bank = max(bank_votes, key=bank_votes.get) if bank_votes else None
    edits: list[tuple[int, int, str]] = []
    for match in MACRO_RE.finditer(code):
        label = match.group(1) or match.group(3)
        located = resolver.labels.get(label)
        if located is None or not 0x4000 <= located[1] < 0x8000:
            continue
        label_bank, label_address = located
        position = match.start()
        line_start = code.rfind("\n", 0, position) + 1
        line_end = code.find("\n", position)
        if line_end < 0:
            line_end = len(code)
        line = code[line_start:line_end]
        raw_line = text[line_start:line_end]
        context = None
        for start, end, block_bank in spans:
            if start <= position < end:
                context = block_bank
                break
        pointer = ROM_PTR_RE.search(line)
        if pointer is not None and pointer.end() <= position - line_start:
            context = int(pointer.group(1))
        comment = BANK_COMMENT_RE.search(raw_line)
        if comment is not None:
            context = int(comment.group(1))
        if label in keep or f"{label}_BANK" in raw_line:
            continue
        define = re.match(r"^#define\s+(\w+)\s", raw_line)
        if define is not None:
            wanted = re.sub(r"_(START_SCRIPT|ADDR|BANK)$", "", define.group(1)).replace("_", "").lower()
            if label.replace("_", "").lower() == wanted:
                continue
        if context is None:
            context = file_bank
        if context == label_bank and not all_new:
            continue
        offset = int(match.group(2), 16) if match.group(2) else 0
        literal = f"0x{label_address + offset:04X}u"
        edits.append((match.start(), match.end(), literal))
    for start, end, literal in sorted(edits, reverse=True):
        text = text[:start] + literal + text[end:]
    return text, len(edits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, help="C files (default: src/home/*.c)")
    parser.add_argument("--check", action="store_true", help="report only; do not rewrite")
    parser.add_argument("--revert-foreign", action="store_true",
                        help="turn rom.h macros whose label bank disagrees with their context back into literals")
    parser.add_argument("--revert-new", action="store_true",
                        help="turn every rom.h macro absent from the @- revision back into a literal")
    args = parser.parse_args()
    resolver = Resolver(symbol_table(get_profile("vanilla", ROOT), ROOT),
                        set(symbol_table(get_profile("extended", ROOT), ROOT)))
    paths = [path if path.is_absolute() else (ROOT / path) for path in args.paths] or sorted(
        (ROOT / "src" / "home").glob("*.c"))
    total_edits = 0
    total_unresolved = 0
    if args.revert_foreign or args.revert_new:
        reverted = 0
        for path in paths:
            original = path.read_text()
            text, count = revert_foreign(original, resolver, baseline_macros(path), args.revert_new)
            if count:
                print(f"{path.relative_to(ROOT)}: reverted={count}")
                reverted += count
                if not args.check:
                    path.write_text(text)
        print(f"reverted={reverted}")
        return 0
    for path in paths:
        original = path.read_text()
        text, unresolved = relocate(original, resolver)
        edits = text.count("_ADDR") - original.count("_ADDR")
        total_edits += edits
        total_unresolved += len(unresolved)
        if text != original and not args.check:
            path.write_text(text)
        if edits or unresolved:
            print(f"{path.relative_to(ROOT)}: relocated={edits} unresolved={len(unresolved)}")
        for entry in unresolved:
            print(f"  {entry}")
    print(f"relocated={total_edits} unresolved={total_unresolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
