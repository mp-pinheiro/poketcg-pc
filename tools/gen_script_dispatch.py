#!/usr/bin/env python3
"""Generate the native overworld-script opcode dispatch table."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

_TABLE = "const ProbeEntry probe_entries_scripting[] = {"
_ROW = re.compile(r'\{\s*"([A-Za-z0-9_]+)"\s*,\s*adapt_\1\s*\}')
_OPCODE = re.compile(r"\bdw\s+(ScriptCommand_[A-Za-z0-9_]+)")


def render(probe_path: Path, table_path: Path) -> str:
    probe = probe_path.read_text()
    table_at = probe.index(_TABLE)
    definitions = probe[:table_at]
    adapters = set(_ROW.findall(probe[table_at:]))
    opcodes = _OPCODE.findall(table_path.read_text())
    if len(opcodes) != 104:
        raise SystemExit(f"unexpected script table length: {len(opcodes)}")
    missing = sorted(set(opcodes) - adapters)
    if missing:
        print(f"script adapters unavailable: {missing}")
    definitions = definitions.replace(
        '#include "probe.h"',
        '#include "home/script_dispatch.h"',
    ).replace("ProbeState", "ScriptDispatchState")
    rows = ["static const ScriptDispatchFn kScriptDispatchTable[] = {"]
    rows.extend(
        f"\tadapt_{name}," if name in adapters else "\tNULL,"
        for name in opcodes
    )
    rows.append("};")
    lookup = """

ScriptDispatchFn ScriptDispatchLookupOpcode(uint8_t opcode)
{
	if (opcode >= (uint8_t)(sizeof(kScriptDispatchTable) / sizeof(kScriptDispatchTable[0])))
		return NULL;
	return kScriptDispatchTable[opcode];
}
"""
    return definitions.rstrip() + "\n\n" + "\n".join(rows) + lookup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--table", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    content = render(args.probe, args.table)
    if not args.output.is_file() or args.output.read_text() != content:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
