#!/usr/bin/env python3
"""Generate production effect dispatch from the canonical probe adapters."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_TABLE = "const ProbeEntry probe_entries_effect_functions[] = {"
_ROW = re.compile(r'\{\s*"([A-Za-z0-9_]+)"\s*,\s*adapt_\1\s*\}')


def render(probe_path: Path, inventory_path: Path) -> str:
    probe = probe_path.read_text()
    table_at = probe.index(_TABLE)
    definitions = probe[:table_at]
    names = _ROW.findall(probe[table_at:])
    if len(names) != len(set(names)):
        raise SystemExit("effect adapter names are duplicated")

    inventory = json.loads(inventory_path.read_text())["functions"]
    missing = sorted(name for name in names if name not in inventory)
    if missing:
        raise SystemExit(f"effect adapters missing from inventory: {missing}")
    addresses = {name: int(inventory[name]["addr"]) for name in names}
    by_address: dict[int, list[str]] = {}
    for name, address in addresses.items():
        by_address.setdefault(address, []).append(name)
    collisions = {address: values for address, values in by_address.items() if len(values) > 1}
    if collisions:
        raise SystemExit(f"effect adapter address collisions: {collisions}")

    definitions = definitions.replace(
        '#include "probe.h"',
        '#include "home/effect_dispatch.h"\n\n#include <string.h>',
    ).replace("ProbeState", "EffectDispatchState")
    rows = ["static const EffectDispatchEntry kEffectDispatchEntries[] = {"]
    for name in sorted(names, key=lambda item: (addresses[item], item)):
        rows.append(f'\t{{ "{name}", 0x{addresses[name]:04X}u, adapt_{name} }},')
    rows.append("};")
    lookup = r'''

EffectDispatchFn EffectDispatchLookupName(const char *name)
{
	for (uint16_t i = 0u; i < (uint16_t)(sizeof(kEffectDispatchEntries) / sizeof(kEffectDispatchEntries[0])); i++)
		if (strcmp(kEffectDispatchEntries[i].name, name) == 0)
			return kEffectDispatchEntries[i].function;
	return NULL;
}

EffectDispatchFn EffectDispatchLookupAddress(uint16_t address)
{
	uint16_t low = 0u;
	uint16_t high = (uint16_t)(sizeof(kEffectDispatchEntries) / sizeof(kEffectDispatchEntries[0]));
	while (low < high) {
		uint16_t middle = (uint16_t)(low + (uint16_t)((high - low) / 2u));
		if (kEffectDispatchEntries[middle].address < address)
			low = (uint16_t)(middle + 1u);
		else
			high = middle;
	}
	if (low < (uint16_t)(sizeof(kEffectDispatchEntries) / sizeof(kEffectDispatchEntries[0])) &&
	    kEffectDispatchEntries[low].address == address)
		return kEffectDispatchEntries[low].function;
	return NULL;
}
'''
    return definitions.rstrip() + "\n\n" + "\n".join(rows) + lookup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    content = render(args.probe, args.inventory)
    if not args.output.is_file() or args.output.read_text() != content:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
