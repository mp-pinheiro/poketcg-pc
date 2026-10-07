#!/usr/bin/env python3
"""Rewrite vanilla ROM code pointers seeded into a profile's case modules.

Case modules seeded from tests/cases/ get their RAM addresses relocated, but the
values seeded into function-pointer variables (wDoFrameFunction, menu and card
list handlers, the interrupt trampolines) are still vanilla ROM addresses. The
profile's ROM has other code there, so the oracle and the port both run the
wrong thing. Every such value that is a vanilla label address is replaced by
the profile's address of the same label; values that already name a profile
label, and values with no vanilla label, are left alone and reported.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.profiles import get_profile

POINTER_VARIABLES = (
    "wDoFrameFunction", "wMenuUpdateFunc", "wListFunctionPointer", "wCardListHandlerFunction",
    "wCardListUpdateFunction", "wDeckConfigurationMenuHandlerFunction", "wLoadNPCFunction",
    "wScreenAnimUpdatePtr", "wPrintSortNumberInCardListPtr",
)
TRAMPOLINES = ("wLCDCFunctionTrampoline", "wVBlankFunctionTrampoline")
SYMBOL_RE = re.compile(r"^([0-9a-fA-F]{2}):([0-9a-fA-F]{4}) (\S+)$")


def symbols(path: Path) -> dict[str, tuple[int, int]]:
    table: dict[str, tuple[int, int]] = {}
    for line in path.read_text().splitlines():
        match = SYMBOL_RE.match(line.strip())
        if match and "." not in match.group(3):
            table.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return table


def code_labels(table: dict[str, tuple[int, int]]) -> dict[int, list[str]]:
    by_address: dict[int, list[str]] = {}
    for name, (bank, address) in table.items():
        if address < 0x8000 and not name.startswith(("w", "h", "s", "v")):
            by_address.setdefault(address, []).append(name)
    return by_address


def pointer_slots(table: dict[str, tuple[int, int]]) -> dict[int, str]:
    slots = {table[name][1]: name for name in POINTER_VARIABLES if name in table}
    slots.update({table[name][1] + 1: name for name in TRAMPOLINES if name in table})
    return slots


def relocate(text: str, slots: dict[int, str], vanilla: dict[int, list[str]],
             profile: dict[str, tuple[int, int]], profile_labels: dict[int, list[str]],
             report: list[str], origin: str) -> str:
    tree = ast.parse(text)
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not (isinstance(key, ast.Constant) and key.value == "wram" and isinstance(value, ast.Dict)):
                continue
            for seed_key, seed_value in zip(value.keys, value.values):
                if not (isinstance(seed_key, ast.Constant) and isinstance(seed_key.value, int)
                        and isinstance(seed_value, ast.Constant) and isinstance(seed_value.value, bytes)):
                    continue
                start = seed_key.value
                payload = bytearray(seed_value.value)
                changed = False
                for slot, variable in slots.items():
                    offset = slot - start
                    if not 0 <= offset <= len(payload) - 2:
                        continue
                    pointer = payload[offset] | payload[offset + 1] << 8
                    if pointer == 0 or pointer in profile_labels:
                        continue
                    names = [name for name in vanilla.get(pointer, []) if name in profile]
                    where = f"{origin}:{seed_value.lineno}"
                    if len(names) != 1:
                        report.append(f"{where}: {variable} ${pointer:04X} has no unique profile label "
                                      f"(vanilla {vanilla.get(pointer, [])})")
                        continue
                    target = profile[names[0]][1]
                    payload[offset] = target & 0xFF
                    payload[offset + 1] = target >> 8
                    changed = True
                    report.append(f"{where}: {variable} ${pointer:04X} -> ${target:04X} ({names[0]})")
                if changed:
                    begin = offsets[seed_value.lineno - 1] + seed_value.col_offset
                    end = offsets[seed_value.end_lineno - 1] + seed_value.end_col_offset
                    edits.append((begin, end, repr(bytes(payload))))
    for begin, end, replacement in sorted(edits, reverse=True):
        text = text[:begin] + replacement + text[end:]
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile", default="extended")
    parser.add_argument("--check", action="store_true", help="report without rewriting; exit 1 if anything would change")
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()
    profile = get_profile(args.profile, ROOT)
    vanilla_profile = get_profile("vanilla", ROOT)
    if profile.name == vanilla_profile.name:
        raise SystemExit("relocate_case_pointers: the vanilla profile has nothing to relocate")
    profile_table = symbols(profile.sym_path(ROOT))
    vanilla_table = symbols(vanilla_profile.sym_path(ROOT))
    slots = pointer_slots(profile_table)
    vanilla_labels = code_labels(vanilla_table)
    profile_labels = code_labels(profile_table)
    files = args.files or sorted(profile.case_path(ROOT).glob("*.py"))
    report: list[str] = []
    pending = 0
    for path in files:
        text = path.read_text()
        relocated = relocate(text, slots, vanilla_labels, profile_table, profile_labels, report,
                             str(path.relative_to(ROOT)) if path.is_absolute() else str(path))
        if relocated != text:
            pending += 1
            if not args.check:
                compile(relocated, str(path), "exec")
                path.write_text(relocated)
    for line in report:
        print(line)
    print(f"relocate-case-pointers: {len(report)} pointer seeds, {pending} files "
          f"{'would change' if args.check else 'rewritten'}")
    return 1 if args.check and pending else 0


if __name__ == "__main__":
    raise SystemExit(main())
