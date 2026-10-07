#!/usr/bin/env python3
"""Reject raw WRAM, SRAM and HRAM address literals in tests/cases modules; spell them with tests/cases/_symbols.py."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "cases"
EXEMPT = {"_symbols.py", "_schema_migration.py"}
RANGES = ((0xC000, 0xE000), (0xA000, 0xC000), (0xFF80, 0xFFFF))


def in_ram(value: int) -> bool:
    return any(low <= value < high for low, high in RANGES)


def is_data_argument(node: ast.Constant, parents: dict[int, ast.AST]) -> bool:
    call = parents.get(id(node))
    return isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "data" \
        and len(call.args) == 1 and call.args[0] is node and not call.keywords


def violations(path: Path) -> list[tuple[int, int]]:
    tree = ast.parse(path.read_text(), filename=str(path))
    parents = {id(child): node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) is int and in_ram(node.value) \
                and not is_data_argument(node, parents):
            found.append((node.lineno, node.value))
    return sorted(found)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="modules to check (default: tests/cases/*.py)")
    args = parser.parse_args()
    paths = args.paths or sorted(p for p in CASES.glob("*.py") if p.name not in EXEMPT)
    total = 0
    for path in paths:
        for line, value in violations(path):
            total += 1
            shown = path.resolve().relative_to(ROOT) if path.resolve().is_relative_to(ROOT) else path
            print(f"{shown}:{line}: raw address literal 0x{value:04X}; use sym(), a _symbols constant or data()")
    if total:
        print(f"lint-case-literals: {total} raw address literals in {len(paths)} modules")
        return 1
    print(f"lint-case-literals: {len(paths)} modules clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
