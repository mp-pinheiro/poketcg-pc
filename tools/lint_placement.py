#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.factory_blocks import code_mask, default_roots, tree_paths
from tools.profiles import load_catalog

INTEGER = r"(?:0[xX][0-9A-Fa-f]+|\d+)[uU]?"
RULES = (
    ("literal ROM bank select", re.compile(rf"\bBankswitchROM\s*\(\s*(?:\(\s*uint8_t\s*\)\s*)?{INTEGER}\s*\)")),
    ("literal ROM bank select", re.compile(rf"\bgb_write8\s*\(\s*0[xX]2000[uU]?\s*,\s*(?:\(\s*uint8_t\s*\)\s*)?{INTEGER}\s*\)")),
    ("literal ROM bank select", re.compile(rf"\bhBankROM\s*=\s*(?:\(\s*uint8_t\s*\)\s*)?{INTEGER}\s*;")),
    ("literal ROM bank select", re.compile(rf"\bBankpushROM\s*\(\s*{INTEGER}\s*\)")),
    ("literal ROM bank", re.compile(rf"\b(?:rom_ptr|GetFarByte|GetFarWord|rom_ptr_product)\s*\(\s*(?:\(\s*uint8_t\s*\)\s*)?{INTEGER}\s*,")),
)
OFFSET = re.compile(rf"\b([A-Za-z_]\w*?)_ADDR\s*\+\s*\(?\s*(?:\(\s*uint16_t\s*\)\s*)?({INTEGER})")
START_SCRIPT = re.compile(r"^\s*#\s*define\s+\w+_START_SCRIPT\b")
BANK_DEFINE = re.compile(rf"^\s*#\s*define\s+([A-Za-z_]\w*BANK\w*|BANK_\w*)\s+\(?\s*{INTEGER}")


def rom_labels() -> set[str]:
    labels: set[str] = set()
    _, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
    for profile in profiles.values():
        path = profile.sym_path(ROOT)
        if not path.is_file():
            continue
        for line in path.read_text(errors="replace").splitlines():
            match = re.match(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(\S+)", line.strip())
            if match and int(match.group(2), 16) < 0x8000:
                labels.add(match.group(3).replace(".", "__"))
    return labels


def lint(paths: list[Path]) -> list[str]:
    labels = rom_labels()
    failures = []
    for path in paths:
        text = path.read_text(errors="replace")
        masked = code_mask(text).split("\n")
        masked_text = "\n".join(masked)
        for number, line in enumerate(masked, 1):
            for rule, pattern in RULES:
                for match in pattern.finditer(line):
                    failures.append(f"{path.relative_to(ROOT)}:{number}: {rule}: {match.group(0).strip()}")
            bank_define = BANK_DEFINE.match(line)
            if bank_define:
                name = re.escape(bank_define.group(1))
                uses = re.compile(
                    rf"\b(?:BankswitchROM|BankpushROM|rom_ptr|GetFarByte|GetFarWord|rom_ptr_product)\s*\(\s*{name}\b|"
                    rf"\b(?:g_rom_bank|bank)\s*(?:=|==)\s*{name}\b|"
                    rf"\b\w+\s*=\s*\(uint8_t\)\s*\(\s*{name}\s*\+|"
                    rf"\bbank\s*=\s*\(uint8_t\)\s*\(\s*bank\s*\+\s*{name}\b"
                )
                if uses.search(masked_text):
                    failures.append(f"{path.relative_to(ROOT)}:{number}: literal ROM bank macro: {line.strip()}")
            if START_SCRIPT.match(line):
                continue
            for match in OFFSET.finditer(line):
                if match.group(1) in labels:
                    failures.append(f"{path.relative_to(ROOT)}:{number}: ROM label offset: {match.group(0).strip()}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject ROM placement constants in C: literal bank selects and offsets from ROM labels.")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = [path.resolve() for path in tree_paths(args.paths or default_roots())]
    failures = lint(paths)
    for failure in failures:
        print(failure)
    print(f"lint-placement: files={len(paths)} failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
