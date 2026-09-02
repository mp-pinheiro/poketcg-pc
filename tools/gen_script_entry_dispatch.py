#!/usr/bin/env python3
"""Generate the script entry address table from poketcg.sym plus the ROM.

Two sites reach a script by a computed jump, and both need the target resolved
ahead of time because deciding at run time would mean reading ROM code as data,
which the product data pack does not carry.

EnterScript (engine/overworld/overworld.asm:122-127) ends in `jp hl` with hl
taken from wNextScript. Every `Script_*` label that opens with the
`start_script` macro is a lone `rst $20` and is interpreted by RST20; the rest
are ordinary routines needing a C body.

CallMapScriptPointerIfExists (engine/overworld/scripting.asm:98-101) ends in
`jp hl` with hl read out of the MapScripts table, whose targets are named in
data/map_scripts.asm and are all ordinary routines.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

OPCODE_RST_20 = 0xE7
SYM_LINE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")
DECL = re.compile(r"^[A-Za-z_][\w ]*\**\s*\b(\w+)\s*\(\s*void\s*\)\s*;", re.MULTILINE)
MAP_SCRIPT_TARGET = re.compile(r"^\tdw\s+(\w+)\s*$", re.MULTILINE)


def symbol_table(sym_path: Path) -> dict[str, tuple[int, int]]:
    table: dict[str, tuple[int, int]] = {}
    for line in sym_path.read_text().splitlines():
        match = SYM_LINE.match(line)
        if match:
            table.setdefault(
                match.group(3), (int(match.group(1), 16), int(match.group(2), 16))
            )
    return table


# data/map_scripts.asm:1-12 gives each map eight pointers, in slot order:
# 0 NPC data, 2 after-NPCs, 4 objects, 6 pressed A, 8 load map, a after duel,
# c moved player, e close text box. Slots 0 and 4 are data tables that
# Func_c943 and HandleMoveModeAPress walk; only the rest are jumped to.
MAP_SCRIPT_DATA_SLOTS = (0, 2)


def map_script_code_targets(map_scripts: Path) -> set[str]:
    pointers = MAP_SCRIPT_TARGET.findall(map_scripts.read_text())
    if len(pointers) % 8:
        raise SystemExit(
            f"{map_scripts} holds {len(pointers)} pointers, not a multiple of 8"
        )
    return {
        name for index, name in enumerate(pointers)
        if name != "NULL" and index % 8 not in MAP_SCRIPT_DATA_SLOTS
    }

def script_entries(sym_path: Path, rom_path: Path, map_scripts: Path
                   ) -> dict[int, tuple[int, int, list[str]]]:
    rom = rom_path.read_bytes()
    table = symbol_table(sym_path)

    def first_byte(name: str) -> int:
        bank, offset = table[name]
        physical = bank * 0x4000 + (offset - 0x4000 if offset >= 0x4000 else offset)
        if physical >= len(rom):
            raise SystemExit(f"{name} at {bank:02X}:{offset:04X} is past the ROM")
        return rom[physical]

    wanted = {
        name for name in table
        if name.startswith("Script_") and "." not in name
    }
    # A local label inside a script is a `jp hl` destination only when it opens
    # with the start_script macro; SetNextScript targets those re-entry points
    # (e.g. Script_EnterLabFirstTime.ows_d779). The rest are bytecode-jump
    # targets, reached by a command writing wScriptPointer, never by a jump.
    wanted |= {
        name for name in table
        if name.startswith("Script_") and "." in name
        and first_byte(name) == OPCODE_RST_20
    }
    wanted |= map_script_code_targets(map_scripts)
    unresolved = sorted(name for name in wanted if name not in table)
    if unresolved:
        raise SystemExit(f"script entry targets missing from poketcg.sym: {unresolved}")

    found: dict[int, tuple[int, int, list[str]]] = {}
    for name in sorted(wanted):
        bank, offset = table[name]
        physical = bank * 0x4000 + (offset - 0x4000 if offset >= 0x4000 else offset)
        if physical >= len(rom):
            raise SystemExit(f"{name} at {bank:02X}:{offset:04X} is past the ROM")
        entry = found.setdefault(offset, (bank, rom[physical], []))
        if entry[0] != bank:
            raise SystemExit(
                f"${offset:04X} is claimed by bank {entry[0]:02X} and {bank:02X}; "
                "the table keys on the 16-bit address a `jp hl` carries"
            )
        entry[2].append(name)
    return found


PROTOTYPE = re.compile(
    r"^(?P<ret>[A-Za-z_][\w ]*\**)\s+(?P<name>\w+)\s*\((?P<args>[^)]*)\)\s*;",
    re.MULTILINE,
)


def ported_symbols(home: Path) -> dict[str, tuple[str, str, str]]:
    """name -> (header, return type, argument list) for every declared routine."""
    owners: dict[str, tuple[str, str, str]] = {}
    for header in sorted(home.glob("*.h")):
        text = header.read_text()
        for match in PROTOTYPE.finditer(text):
            owners.setdefault(
                match.group("name"),
                (header.name, match.group("ret").strip(), match.group("args").strip()),
            )
    return owners


def struct_members(header_text: str, type_name: str) -> set[str]:
    match = re.search(
        r"typedef struct \{(?P<body>[^}]*)\}\s*%s\s*;" % re.escape(type_name),
        header_text,
    )
    if match is None:
        return set()
    return set(re.findall(r"\b(\w+)\s*;", match.group("body")))


THUNK_PARAMETERS = ("b", "c", "d", "e", "hl")


def thunk(name: str, owner: tuple[str, str, str], header_text: str) -> str:
    _header, ret, args = owner
    declared = [] if not args or args == "void" else [
        parameter.split()[-1].lstrip("*") for parameter in args.split(",")
    ]
    unknown = [p for p in declared if p not in THUNK_PARAMETERS]
    if unknown:
        raise SystemExit(
            f"{name} takes {unknown}, which a `jp hl` entry cannot supply; "
            "only b, c, d, e and hl are live at the jump"
        )
    call_args = ", ".join(declared)
    lines = [f"static uint8_t enter_{name}({', '.join(
        ('uint16_t hl' if p == 'hl' else f'uint8_t {p}') for p in THUNK_PARAMETERS
    )})", "{"]
    lines += [f"\t(void){p};" for p in THUNK_PARAMETERS if p not in declared]
    members = struct_members(header_text, ret) if ret != "void" else set()
    if ret == "void":
        lines += [f"\t{name}({call_args});", "\treturn 0u;"]
    elif "f" in members:
        lines.append(f"\treturn {name}({call_args}).f;")
    elif "carry" in members:
        lines.append(f"\treturn {name}({call_args}).carry ? 0x10u : 0u;")
    else:
        lines += [f"\t(void){name}({call_args});", "\treturn 0u;"]
    lines.append("}\n")
    return "\n".join(lines)


def render(sym_path: Path, rom_path: Path, home: Path, map_scripts: Path) -> str:
    entries = script_entries(sym_path, rom_path, map_scripts)
    owners = ported_symbols(home)
    header_text = {p.name: p.read_text() for p in home.glob("*.h")}

    rows, thunks = [], []
    headers = {"scripting.h"}
    for offset in sorted(entries):
        bank, opcode, names = entries[offset]
        ported = sorted(name for name in names if name in owners)
        name = ported[0] if ported else sorted(names)[0]
        if opcode == OPCODE_RST_20:
            rows.append(f'\t{{ 0x{offset:04X}u, "{name}", SCRIPT_ENTRY_BYTECODE, 0x{bank:02X}u, NULL }},')
        elif ported:
            owner = owners[name]
            headers.add(owner[0])
            thunks.append(thunk(name, owner, header_text[owner[0]]))
            rows.append(f'\t{{ 0x{offset:04X}u, "{name}", SCRIPT_ENTRY_ROUTINE, 0x{bank:02X}u, enter_{name} }},')
        else:
            rows.append(f'\t{{ 0x{offset:04X}u, "{name}", SCRIPT_ENTRY_UNPORTED, 0x{bank:02X}u, NULL }},')

    include_lines = "\n".join(f'#include "home/{header}"' for header in sorted(headers))
    body = "\n".join(thunks)
    table = "\n".join(rows)
    return f'''/* Generated by tools/gen_script_entry_dispatch.py. Do not edit. */
#include "home/script_entry_dispatch.h"

#include <stdio.h>
#include <stdlib.h>

#include "generated/hram.h"
#include "home/switch_rom.h"
#include "mem.h"

{include_lines}

{body}
static const ScriptEntryRow kScriptEntries[] = {{
{table}
}};

#define SCRIPT_ENTRY_COUNT \\
\t((uint16_t)(sizeof(kScriptEntries) / sizeof(kScriptEntries[0])))

const ScriptEntryRow *ScriptEntryLookup(uint16_t address)
{{
\tuint16_t low = 0u;
\tuint16_t high = SCRIPT_ENTRY_COUNT;

\twhile (low < high) {{
\t\tuint16_t middle = (uint16_t)(low + (uint16_t)((high - low) / 2u));

\t\tif (kScriptEntries[middle].address < address)
\t\t\tlow = (uint16_t)(middle + 1u);
\t\telse
\t\t\thigh = middle;
\t}}
\tif (low < SCRIPT_ENTRY_COUNT && kScriptEntries[low].address == address)
\t\treturn &kScriptEntries[low];
\treturn NULL;
}}

uint8_t ScriptEntryEnter(uint16_t target)
{{
\tconst ScriptEntryRow *row;
\tuint8_t saved_bank;
\tuint8_t flags;

\t/* Every shipped script entry is in ROM, so a RAM target only happens under
\t * a probe case that stubs the jump destination. RAM is readable through the
\t * bus, unlike ROM code, so decode the stub: `ret` ($C9) returns to
\t * EnterScript's caller and `rst $20` ($E7) enters the interpreter, exactly
\t * as the CPU would. */
\tif (target >= 0xC000u) {{
\t\tuint8_t opcode = gb_read8(target);

\t\tif (opcode == 0xC9u)
\t\t\treturn 0u;
\t\tif (opcode == 0xE7u)
\t\t\treturn RST20(0u, 0u, 0u, 0u, 0u, 0u, (uint16_t)(target + 1u)).f;
\t\tfprintf(stderr, "script entry ram opcode=$%02X target=$%04X\\n",
\t\t        (unsigned)opcode, (unsigned)target);
\t\tabort();
\t}}
\trow = ScriptEntryLookup(target);
\tif (row == NULL) {{
\t\tfprintf(stderr, "script entry miss target=$%04X\\n", (unsigned)target);
\t\tabort();
\t}}
\tif (row->kind == SCRIPT_ENTRY_UNPORTED) {{
\t\tfprintf(stderr, "script entry unported name=%s target=$%04X\\n",
\t\t        row->name, (unsigned)target);
\t\tabort();
\t}}

\tsaved_bank = hBankROM;
\tBankswitchROM(row->bank);
\tif (row->kind == SCRIPT_ENTRY_BYTECODE)
\t\tflags = RST20(0u, 0u, 0u, 0u, 0u, 0u, (uint16_t)(target + 1u)).f;
\telse
\t\tflags = row->function(0u, 0u, 0u, 0u, target);
\tBankswitchROM(saved_bank);
\treturn flags;
}}
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sym", type=Path, required=True)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--home", type=Path, required=True)
    parser.add_argument("--map-scripts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    content = render(args.sym, args.rom, args.home, args.map_scripts)
    if not args.output.is_file() or args.output.read_text() != content:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
