#!/usr/bin/env python3
"""Seed an Extended case module from a vanilla one by relocating RAM addresses.

Every numeric WRAM/SRAM address in the vanilla cases is expressed as the
nearest preceding vanilla symbol plus an offset, then re-emitted at that
symbol's Extended address. Routines the Extended asm no longer has are
dropped; routines whose asm changed are kept as a starting point and listed
so the port can rewrite them against the Extended ROM.
"""

from __future__ import annotations

import argparse
import bisect
import importlib.util
import pprint
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from profile_audit import routines_by_basename

from tools.profiles import get_profile, symbol_table

RAM_RANGES = ((0xA000, 0xC000), (0xC000, 0xE000))
ADDRESS_FIELDS = ("wram", "read", "expect")
BANKED_FIELDS = ("sram", "sread")
PAIRS = (("hl",), ("d", "e"), ("b", "c"))

POISON_PAIRS = frozenset({0xDDEE, 0xBBCC, 0x1234})
REGISTER_MAX_OFFSET = 0x80

class Relocator:
    def __init__(self, source: dict[str, tuple[int, int]], target: dict[str, tuple[int, int]]):
        self.target = target
        self.unmapped: set[int] = set()
        self.by_region: dict[tuple[int, int], tuple[list[int], list[str]]] = {}
        for region in RAM_RANGES:
            entries = sorted(
                (address, name)
                for name, (bank, address) in source.items()
                if region[0] <= address < region[1] and "." not in name and name in target
            )
            self.by_region[region] = ([address for address, _ in entries], [name for _, name in entries])

    def region(self, address: int) -> tuple[int, int] | None:
        for region in RAM_RANGES:
            if region[0] <= address < region[1]:
                return region
        return None

    def relocate(self, address: int, bank: int | None = None, max_offset: int | None = None) -> int:
        region = self.region(address)
        if region is None:
            return address
        addresses, names = self.by_region[region]
        index = bisect.bisect_right(addresses, address) - 1
        while index >= 0:
            name = names[index]
            if bank is None or region[0] != 0xA000 or self.target[name][0] == bank:
                break
            index -= 1
        if index < 0:
            self.unmapped.add(address)
            return address
        offset = address - addresses[index]
        if max_offset is not None and offset > max_offset:
            return address
        return self.target[names[index]][1] + offset

    def relocate_register(self, value: int) -> int:
        if value in POISON_PAIRS:
            return value
        return self.relocate(value, max_offset=REGISTER_MAX_OFFSET)


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(f"transpose_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relocate_case(case: dict[str, Any], relocator: Relocator) -> dict[str, Any]:
    result = dict(case)
    for field in ADDRESS_FIELDS:
        value = case.get(field)
        if isinstance(value, dict):
            result[field] = {relocator.relocate(int(address)): payload for address, payload in value.items()}
    for field in BANKED_FIELDS:
        value = case.get(field)
        if isinstance(value, dict):
            result[field] = {
                int(bank): {relocator.relocate(int(address), int(bank)): payload for address, payload in spans.items()}
                for bank, spans in value.items()
            }
    for pair in PAIRS:
        if pair == ("hl",):
            if "hl" in case:
                result["hl"] = relocator.relocate_register(int(case["hl"]))
            continue
        high, low = pair
        if high in case and low in case:
            value = (int(case[high]) << 8) | int(case[low])
            moved = relocator.relocate_register(value)
            if moved != value:
                result[high] = moved >> 8
                result[low] = moved & 0xFF
    setup = case.get("setup")
    if isinstance(setup, list):
        result["setup"] = [
            {key: (relocator.relocate(int(value)) if key == "hl" else value) for key, value in step.items()}
            if isinstance(step, dict) else step
            for step in setup
        ]
    return result


class HexPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, bool):
            return repr(obj), True, False
        if isinstance(obj, int) and obj >= 0x100:
            return f"0x{obj:04X}", True, False
        if isinstance(obj, int) and 0 <= obj <= 0xFF:
            return f"0x{obj:02X}", True, False
        return super().format(obj, context, maxlevels, level)


def render(basename: str, contract: dict[str, Any], cases: dict[str, list[dict[str, Any]]],
           mutations: dict[str, Any], overlay_source: str) -> str:
    printer = HexPrinter(indent=4, width=96, sort_dicts=False)
    lines = [
        f'"""Extended oracle-diff cases for {basename}, seeded from tests/cases/{basename}.py."""',
        "",
        "CONTRACT = {",
    ]
    for name, fields in contract.items():
        lines.append(f"    {name!r}: {printer.pformat(fields)},")
    lines.append("}")
    lines.append("")
    lines.append("CASES = {")
    for name, entries in cases.items():
        lines.append(f"    {name!r}: [")
        for entry in entries:
            body = printer.pformat(entry).replace("\n", "\n        ")
            lines.append(f"        {body},")
        lines.append("    ],")
    lines.append("}")
    lines.append("")
    lines.append("MUTATIONS = {")
    for name, mutation in mutations.items():
        row = dict(mutation)
        row["source"] = overlay_source
        body = printer.pformat(row).replace("\n", "\n    ")
        lines.append(f"    {name!r}: {body},")
    lines.append("}")
    lines.append("")
    lines.append("from tests.cases._schema_migration import legacy_to_schema")
    lines.append("SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("basename")
    parser.add_argument("--profile", default="extended")
    parser.add_argument("--force", action="store_true", help="overwrite an existing overlay module")
    args = parser.parse_args()
    vanilla = get_profile("vanilla", ROOT)
    target = get_profile(args.profile, ROOT)
    source_path = ROOT / "tests" / "cases" / f"{args.basename}.py"
    if not source_path.is_file():
        raise SystemExit(f"no vanilla case module {source_path}")
    output = target.case_path(ROOT) / f"{args.basename}.py"
    if output.exists() and not args.force:
        raise SystemExit(f"{output} exists; pass --force to overwrite")
    module = load_module(source_path)
    vanilla_all = routines_by_basename(vanilla.source_path(ROOT) / "src")
    target_all = routines_by_basename(target.source_path(ROOT) / "src")
    vanilla_bodies = {name: body for routines in vanilla_all.values() for name, body in routines.items()}
    target_bodies = {name: body for routines in target_all.values() for name, body in routines.items()}
    relocator = Relocator(symbol_table(vanilla, ROOT), symbol_table(target, ROOT))
    contract: dict[str, Any] = {}
    cases: dict[str, list[dict[str, Any]]] = {}
    mutations: dict[str, Any] = {}
    dropped, changed = [], []
    for name, entries in module.CASES.items():
        asm_name = name.split(".")[0]
        if asm_name in vanilla_bodies and asm_name not in target_bodies:
            dropped.append(name)
            continue
        if asm_name in target_bodies and vanilla_bodies.get(asm_name) != target_bodies[asm_name]:
            changed.append(name)
        contract[name] = module.CONTRACT[name]
        cases[name] = [relocate_case(entry, relocator) for entry in entries]
        if name in getattr(module, "MUTATIONS", {}):
            mutations[name] = module.MUTATIONS[name]
    overlay_root = target.overlay_root or "src/home"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(args.basename, contract, cases, mutations,
                             f"{overlay_root}/home/{args.basename}.c"))
    print(f"wrote {output.relative_to(ROOT)}: routines={len(cases)} changed={len(changed)} dropped={len(dropped)}")
    for name in changed:
        print(f"  changed {name}")
    for name in dropped:
        print(f"  dropped {name}")
    for address in sorted(relocator.unmapped):
        print(f"  unmapped 0x{address:04X}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
