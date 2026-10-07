#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.gen_constants import evaluate

SYM_RE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")
EVENT_RE = re.compile(r"^\s*event_def\s+\$([0-9A-Fa-f]+)\s*,\s*%([01]{8})\s*;\s*(EVENT_\w+)")
TEXT_LINE_RE = re.compile(r'^\s*(?:text|line|cont|para)\s+"([^"]*)"')
DROPPED_EVENTS = {"EVENT_CONSOLE", "EVENT_GIFT_CENTER_MENU_CHOICE"}
NEW_EVENTS = {"EVENT_MAN1_REQUESTED_CARD_ID_HI"}
SPLIT_SUFFIX = "_LO"
EVENT_VARS_SIZE = 0x40
SRAM_BASE = 0xA000
NUM_BUILT_DECKS = 4


def symbols(path: Path) -> dict[str, tuple[int, int]]:
    table: dict[str, tuple[int, int]] = {}
    for line in path.read_text(errors="replace").splitlines():
        match = SYM_RE.match(line.strip())
        if match and "." not in match.group(3):
            table.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return table


def sram(table: dict[str, tuple[int, int]], bank: int) -> dict[str, int]:
    return {name: address for name, (sym_bank, address) in table.items()
            if sym_bank == bank and SRAM_BASE <= address < 0xC000 and name.startswith("s")}


def need(table: dict[str, int], name: str, profile: str) -> int:
    if name not in table:
        raise SystemExit(f"gen_save_import: {profile} symbol {name} is missing")
    return table[name]


def check_same_block(vanilla: dict[str, int], extended: dict[str, int], start: int, end: int,
                     what: str) -> list[tuple[int, int]]:
    cleared = []
    ordered = sorted(set(vanilla.values()) | {end})
    for name, address in vanilla.items():
        if not start <= address < end:
            continue
        if name not in extended:
            size = min(a for a in ordered if a > address) - address
            cleared.append((address, size))
        elif extended[name] != address:
            raise SystemExit(f"gen_save_import: {what} field {name} moved")
    for name, address in extended.items():
        if start <= address < end and vanilla.get(name) != address:
            raise SystemExit(f"gen_save_import: {what} field {name} has no vanilla source")
    return sorted(set(cleared))


def deck_stride(table: dict[str, int], prefix: str, count: int, profile: str) -> int:
    first = need(table, f"{prefix}1", profile)
    stride = need(table, f"{prefix}2", profile) - first
    for index in range(1, count + 1):
        if need(table, f"{prefix}{index}", profile) != first + (index - 1) * stride:
            raise SystemExit(f"gen_save_import: {profile} {prefix}{index} breaks the deck stride")
        if need(table, f"{prefix}{index}Cards", profile) - need(table, f"{prefix}{index}Name", profile) != 0x18:
            raise SystemExit(f"gen_save_import: {profile} {prefix}{index} name is not 24 bytes")
    return stride


def saved_deck_count(table: dict[str, int]) -> int:
    numbers = sorted(int(m.group(1)) for name in table if (m := re.fullmatch(r"sSavedDeck(\d+)", name)))
    if numbers != list(range(1, len(numbers) + 1)):
        raise SystemExit("gen_save_import: saved deck slots are not contiguous")
    return len(numbers)


def general_skips(vanilla: dict[str, int], extended: dict[str, int]) -> tuple[int, list[int]]:
    v_start = need(vanilla, "sGeneralSaveDataHeaderEnd", "vanilla")
    e_start = need(extended, "sGeneralSaveDataHeaderEnd", "extended")
    v_size = need(vanilla, "sEventVars", "vanilla") + EVENT_VARS_SIZE - v_start
    e_size = need(extended, "sEventVars", "extended") + EVENT_VARS_SIZE - e_start
    fields = sorted((address, name) for name, address in vanilla.items()
                    if v_start <= address < v_start + v_size)
    boundaries = [address for address, _name in fields] + [v_start + v_size]
    skips: list[int] = []
    for index, (address, name) in enumerate(fields):
        if name not in extended:
            skips.extend(range(address - v_start, boundaries[index + 1] - v_start))
    for address, name in fields:
        if name not in extended:
            continue
        offset = address - v_start
        expected = offset - sum(1 for skip in skips if skip < offset)
        if extended[name] - e_start != expected:
            raise SystemExit(f"gen_save_import: general save field {name} does not follow the stream copy")
    for name, address in extended.items():
        if e_start <= address < e_start + e_size and name not in vanilla:
            raise SystemExit(f"gen_save_import: general save field {name} has no vanilla source")
    if v_size - len(skips) != e_size:
        raise SystemExit("gen_save_import: general save payload sizes disagree")
    return v_size, skips


def event_masks(disasm: Path) -> dict[str, tuple[int, int]]:
    for path in sorted((disasm / "src").rglob("*.asm")):
        text = path.read_text(errors="replace")
        if "EventVarMasks:" not in text:
            continue
        table: dict[str, tuple[int, int]] = {}
        for line in text.split("EventVarMasks:", 1)[1].splitlines()[1:]:
            match = EVENT_RE.match(line)
            if match:
                table[match.group(3)] = (int(match.group(1), 16), int(match.group(2), 2))
            elif table and line.strip() and not line.strip().startswith(("table_width", "assert", ";")):
                break
        if table:
            return table
    raise SystemExit(f"gen_save_import: no EventVarMasks table under {disasm}")


def contiguous(mask: int) -> bool:
    shifted = mask >> ((mask & -mask).bit_length() - 1)
    return mask != 0 and shifted & (shifted + 1) == 0


def event_pairs(vanilla: dict[str, tuple[int, int]],
                extended: dict[str, tuple[int, int]]) -> list[tuple[int, int, int, int]]:
    pairs = []
    covered: set[str] = set()
    for name, (v_offset, v_mask) in vanilla.items():
        if name in DROPPED_EVENTS:
            continue
        target_name = name if name in extended else f"{name}{SPLIT_SUFFIX}"
        if target_name not in extended:
            raise SystemExit(f"gen_save_import: vanilla {name} has no Extended counterpart")
        e_offset, e_mask = extended[target_name]
        if not contiguous(v_mask) or not contiguous(e_mask) or v_mask.bit_count() > e_mask.bit_count():
            raise SystemExit(f"gen_save_import: {name} does not fit {target_name}")
        if v_offset >= EVENT_VARS_SIZE or e_offset >= EVENT_VARS_SIZE:
            raise SystemExit(f"gen_save_import: {name} lies outside the event variables")
        pairs.append((v_offset, v_mask, e_offset, e_mask))
        covered.add(target_name)
    missing = sorted(set(extended) - covered - NEW_EVENTS)
    if missing:
        raise SystemExit(f"gen_save_import: Extended events with no vanilla source: {', '.join(missing)}")
    return pairs


def game_event_map(vanilla_disasm: Path, extended_disasm: Path) -> list[int]:
    source = (vanilla_disasm / "src" / "constants" / "misc_constants.asm").read_text()
    names = sorted(set(re.findall(r"\bconst\s+(GAME_EVENT_\w+)", source)))
    vanilla = evaluate(vanilla_disasm, names)
    extended = evaluate(extended_disasm, names)
    fallback = extended["GAME_EVENT_OVERWORLD"]
    table = [fallback] * (max(vanilla.values()) + 1)
    for name, value in vanilla.items():
        table[value] = extended.get(name, fallback)
    return table


def menu_items(disasm: Path, label: str) -> list[str]:
    for path in sorted((disasm / "src" / "text").glob("*.asm")):
        lines = path.read_text(errors="replace").splitlines()
        for index, line in enumerate(lines):
            if line.strip() == f"{label}:":
                items = []
                for item in lines[index + 1:]:
                    if item.strip() == "done":
                        return items
                    match = TEXT_LINE_RE.match(item)
                    if match:
                        items.append(match.group(1))
    raise SystemExit(f"gen_save_import: {label} is missing under {disasm}")


def item_map(vanilla: list[str], extended: list[str]) -> list[int]:
    return [extended.index(item) if item in extended else 0 for item in vanilla]


def array(name: str, values: list[int]) -> list[str]:
    body = ", ".join(f"0x{value:02X}u" for value in values)
    return [f"static const uint8_t {name}[] = {{{body}}};"]


def render(vanilla: dict[str, int], extended: dict[str, int], disasms: tuple[Path, Path]) -> str:
    collection = need(vanilla, "sCardCollection", "vanilla")
    if collection != need(extended, "sCardCollection", "extended"):
        raise SystemExit("gen_save_import: the card collection moved")
    header_cleared = check_same_block(vanilla, extended, SRAM_BASE, collection, "SRAM header")
    shared_start = need(vanilla, "sDebugDuelMode", "vanilla")
    shared_end = need(vanilla, "sChallengeMachineEnd", "vanilla")
    if (need(extended, "sDebugDuelMode", "extended"), need(extended, "sChallengeMachineEnd", "extended")) != (
            shared_start, shared_end):
        raise SystemExit("gen_save_import: the challenge machine block moved")
    if check_same_block(vanilla, extended, shared_start, shared_end, "challenge machine"):
        raise SystemExit("gen_save_import: the challenge machine block lost a field")
    built_stride = deck_stride(vanilla, "sDeck", NUM_BUILT_DECKS, "vanilla")
    saved_count = saved_deck_count(vanilla)
    if deck_stride(vanilla, "sSavedDeck", saved_count, "vanilla") != built_stride:
        raise SystemExit("gen_save_import: vanilla built and saved decks differ in size")
    deck_stride(extended, "sDeck", NUM_BUILT_DECKS, "extended")
    deck_stride(extended, "sSavedDeck", saved_deck_count(extended), "extended")
    trailer = ("sCurrentlySelectedDeck", "sUnnamedDeckCounter", "sHasPromotionalCards", "sb704",
               "sCardAndDeckSaveDataEnd")
    v_trailer = [need(vanilla, name, "vanilla") - need(vanilla, trailer[0], "vanilla") for name in trailer]
    e_trailer = [need(extended, name, "extended") - need(extended, trailer[0], "extended") for name in trailer]
    if v_trailer != e_trailer:
        raise SystemExit("gen_save_import: the deck trailer fields moved")
    payload_size, skips = general_skips(vanilla, extended)
    vanilla_disasm, extended_disasm = disasms
    pairs = event_pairs(event_masks(vanilla_disasm), event_masks(extended_disasm))
    lines = [
        "#ifndef POKETCG_GENERATED_SAVE_IMPORT_LAYOUT_H",
        "#define POKETCG_GENERATED_SAVE_IMPORT_LAYOUT_H",
        "",
        "#include <stdint.h>",
        "",
        f"#define VANILLA_CARD_COLLECTION_ADDR 0x{collection:04X}u",
        f"#define VANILLA_CARD_COLLECTION_SIZE 0x{need(vanilla, 'sDeck1', 'vanilla') - collection:03X}u",
        f"#define VANILLA_BUILT_DECKS_ADDR 0x{need(vanilla, 'sDeck1', 'vanilla'):04X}u",
        f"#define VANILLA_SAVED_DECKS_ADDR 0x{need(vanilla, 'sSavedDeck1', 'vanilla'):04X}u",
        f"#define VANILLA_DECK_STRUCT_SIZE 0x{built_stride:02X}u",
        f"#define VANILLA_NUM_BUILT_DECKS {NUM_BUILT_DECKS}u",
        f"#define VANILLA_NUM_SAVED_DECKS {saved_count}u",
        f"#define VANILLA_DECK_TRAILER_ADDR 0x{need(vanilla, trailer[0], 'vanilla'):04X}u",
        f"#define VANILLA_DECK_TRAILER_SIZE {v_trailer[-1]}u",
        f"#define VANILLA_GENERAL_HEADER_ADDR 0x{need(vanilla, 'sGeneralSaveData', 'vanilla'):04X}u",
        f"#define VANILLA_GENERAL_PAYLOAD_ADDR 0x{need(vanilla, 'sGeneralSaveDataHeaderEnd', 'vanilla'):04X}u",
        f"#define VANILLA_GENERAL_PAYLOAD_SIZE 0x{payload_size:02X}u",
        f"#define VANILLA_EVENT_VARS_ADDR 0x{need(vanilla, 'sEventVars', 'vanilla'):04X}u",
        f"#define SAVE_IMPORT_EVENT_VARS_SIZE 0x{EVENT_VARS_SIZE:02X}u",
        f"#define SAVE_IMPORT_SHARED_BLOCK_ADDR 0x{shared_start:04X}u",
        f"#define SAVE_IMPORT_SHARED_BLOCK_SIZE 0x{shared_end - shared_start:02X}u",
        "",
        "typedef struct {",
        "\tuint16_t address;",
        "\tuint8_t size;",
        "} SaveImportSpan;",
        "",
        "typedef struct {",
        "\tuint8_t vanilla_offset;",
        "\tuint8_t vanilla_mask;",
        "\tuint8_t extended_offset;",
        "\tuint8_t extended_mask;",
        "} SaveImportEvent;",
        "",
        "static const SaveImportSpan kSaveImportHeaderCleared[] = {",
        *[f"\t{{0x{address:04X}u, {size}u}}," for address, size in header_cleared],
        "};",
        *array("kSaveImportGeneralSkips", skips),
        "static const SaveImportEvent kSaveImportEvents[] = {",
        *[f"\t{{0x{a:02X}u, 0x{b:02X}u, 0x{c:02X}u, 0x{d:02X}u}}," for a, b, c, d in pairs],
        "};",
        *array("kSaveImportGameEvents", game_event_map(vanilla_disasm, extended_disasm)),
        *array("kSaveImportPcMenuItems", item_map(menu_items(vanilla_disasm, "PCMenuOptionsText"),
                                                  menu_items(extended_disasm, "PCMenuOptionsText"))),
        "",
        "#endif",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the vanilla-to-Extended save import layout.")
    parser.add_argument("--vanilla-sym", type=Path, required=True)
    parser.add_argument("--extended-sym", type=Path, required=True)
    parser.add_argument("--vanilla-disasm", type=Path, required=True)
    parser.add_argument("--extended-disasm", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    vanilla = sram(symbols(args.vanilla_sym), 0)
    extended = sram(symbols(args.extended_sym), 0)
    text = render(vanilla, extended, (args.vanilla_disasm, args.extended_disasm))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if not args.out.is_file() or args.out.read_text() != text:
        args.out.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
