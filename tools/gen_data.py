#!/usr/bin/env python3
"""Extract selected linked-ROM sections into generated C arrays."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path

SCHEMA = (
    {"name": "decks", "section": "Decks", "ctype": "uint8_t", "symbol": "DeckPointers"},
    {"name": "cards", "section": "Cards", "ctype": "uint8_t", "symbol": "CardPointers"},
    {"name": "text_1", "section": "Text 1", "ctype": "uint8_t", "symbol": "TextOffsets"},
    {"name": "text_2", "section": "Text 2", "ctype": "uint8_t", "symbol": "AcidCheckText"},
    {"name": "text_3", "section": "Text 3", "ctype": "uint8_t", "symbol": "YouDoNotOwnAllCardsNeededToBuildThisDeckText"},
    {"name": "text_4", "section": "Text 4", "ctype": "uint8_t", "symbol": "Mail3Part1Text"},
    {"name": "text_5", "section": "Text 5", "ctype": "uint8_t", "symbol": "ChrisFightingClubDeclinedDuelText"},
    {"name": "text_6", "section": "Text 6", "ctype": "uint8_t", "symbol": "RonaldChallengeCup2Missed2Text"},
    {"name": "text_7", "section": "Text 7", "ctype": "uint8_t", "symbol": "Text05db"},
    {"name": "text_8", "section": "Text 8", "ctype": "uint8_t", "symbol": "Text0684"},
    {"name": "text_9", "section": "Text 9", "ctype": "uint8_t", "symbol": "Text073f"},
    {"name": "text_10", "section": "Text 10", "ctype": "uint8_t", "symbol": "KakunaDescription"},
    {"name": "text_11", "section": "Text 11", "ctype": "uint8_t", "symbol": "HorseaDescription"},
    {"name": "text_12", "section": "Text 12", "ctype": "uint8_t", "symbol": "DamageSwapDescription"},
    {"name": "text_13", "section": "Text 13", "ctype": "uint8_t", "symbol": "ScoopUpDescription"},
    {"name": "gfx_1", "section": "Gfx 1", "ctype": "uint8_t", "symbol": "Fonts"},
    {"name": "gfx_3", "section": "Gfx 3", "ctype": "uint8_t", "symbol": "WaterClubTilemap"},
    {"name": "gfx_4", "section": "Gfx 4", "ctype": "uint8_t", "symbol": "OverworldMapTiles"},
    {"name": "gfx_5", "section": "Gfx 5", "ctype": "uint8_t", "symbol": "LightningClubTilesetGfx"},
    {"name": "gfx_6", "section": "Gfx 6", "ctype": "uint8_t", "symbol": "CardPopGfx"},
)

# Static tables embedded in code sections are declared explicitly so the
# production resolver never reads unclassified code bytes from the ROM.
NATIVE_DATA_SPANS = (
    ("input_name_question_data", 6, 0x675E, 0x29),
    ("input_name_background_data", 6, 0x68BC, 0x05),
    ("input_name_char_underbar", 6, 0x68F2, 0x16),
    ("input_name_cursor_tile", 6, 0x6A77, 0x10),
    ("input_name_keyboard", 6, 0x6BAF, 0x14A),
    ("input_name_transition_1", 6, 0x6CF9, 0x66),
    ("input_name_transition_2", 6, 0x6D5F, 0x2A),
    ("naming_default_player_name", 4, 0x68EB, 0x10),
    ("input_name_deck_underbar", 6, 0x6E83, 0x16),
    ("input_name_deck_keyboard", 6, 0x7019, 0xC1),
)

SECTION_RE = re.compile(
    r'^\s*SECTION:\s*\$([0-9A-Fa-f]{4})-\$([0-9A-Fa-f]{4})\s+\(\$[0-9A-Fa-f]{4}\s+bytes\)\s+\["([^"]+)"\]$'
)
BANK_RE = re.compile(r'^\s*(ROM0|ROMX) bank #([0-9]+):\s*$')
SYM_RE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")
TEXTID_RE = re.compile(r"^[0-9A-Fa-f]{1,4}\s+\S+\s*$")
ARRAY_RE = re.compile(r"^static const (\w+) (\w+)\[\] = \{$")


@dataclass(frozen=True)
class Section:
    name: str
    bank: int
    start: int
    end: int


def parse_map(path: Path) -> dict[str, Section]:
    sections: dict[str, Section] = {}
    bank: int | None = None
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        header = BANK_RE.match(line)
        if header:
            bank = int(header[2]) if header[1] == "ROMX" else 0
            continue
        match = SECTION_RE.match(line)
        if not match or bank is None:
            continue
        section = Section(match[3], bank, int(match[1], 16), int(match[2], 16))
        if section.name in sections:
            raise ValueError(f"{path}:{lineno}: duplicate section {section.name!r}")
        if section.bank >= 0:
            sections[section.name] = section
    return sections


def parse_symbols(path: Path) -> dict[str, tuple[int, int]]:
    symbols: dict[str, tuple[int, int]] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        match = SYM_RE.match(line)
        if not match:
            if line and not line.startswith(";") and not TEXTID_RE.match(line):
                continue
            continue
        symbols[match[3]] = (int(match[1], 16), int(match[2], 16))
    return symbols


def rom_offset(bank: int, address: int) -> int:
    if address < 0x4000:
        if bank != 0:
            raise ValueError(f"bank {bank} has non-bank address ${address:04X}")
        return address
    if not 0x4000 <= address <= 0x7FFF:
        raise ValueError(f"ROM address out of range: ${address:04X}")
    return 0x4000 * bank + address - 0x4000


def resolve(entry: dict[str, str], sections: dict[str, Section], symbols: dict[str, tuple[int, int]]) -> Section:
    try:
        section = sections[entry["section"]]
    except KeyError as exc:
        raise ValueError(f"schema section not found: {entry['section']}") from exc
    symbol_name = entry.get("symbol")
    if symbol_name:
        try:
            bank, address = symbols[symbol_name]
        except KeyError as exc:
            raise ValueError(f"schema symbol not found: {symbol_name}") from exc
        if (bank, address) != (section.bank, section.start):
            raise ValueError(
                f"symbol {symbol_name} is {bank:02X}:${address:04X}, "
                f"not {section.name} start {section.bank:02X}:${section.start:04X}"
            )
    return section


def slices(schema: tuple[dict[str, str], ...], sections: dict[str, Section], symbols: dict[str, tuple[int, int]], rom: bytes) -> list[tuple[dict[str, str], Section, bytes]]:
    result = []
    for entry in schema:
        section = resolve(entry, sections, symbols)
        start = rom_offset(section.bank, section.start)
        end = start + section.end - section.start + 1
        if end > len(rom):
            raise ValueError(f"section {section.name} exceeds ROM: {start:#x}-{end:#x}")
        result.append((entry, section, rom[start:end]))
    return result

def sparse_items(
    rom: bytes,
) -> list[tuple[dict[str, str], Section, bytes]]:
    inventory_path = Path("site/data/inventory.json")
    try:
        inventory = json.loads(inventory_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load source span inventory: {exc}") from exc
    spans = inventory.get("spans")
    if not isinstance(spans, list):
        raise ValueError("source inventory has no spans")
    result = []
    for index, span in enumerate(spans):
        if not isinstance(span, dict) or span.get("kind") != "data":
            continue
        if span.get("bank_type") not in {"ROM0", "ROMX"}:
            raise ValueError(f"non-ROM data span: {span}")
        bank = span.get("bank")
        address = span.get("address")
        length = span.get("length")
        if not all(isinstance(value, int) for value in (bank, address, length)):
            raise ValueError(f"invalid source data span: {span}")
        start = rom_offset(bank, address)
        end = start + length
        if length < 1 or end > len(rom):
            raise ValueError(f"source data span exceeds ROM: {span}")
        name = f"inventory_span_{index:05d}"
        section = Section(f"inventory-span-{index:05d}", bank, address, address + length - 1)
        entry = {"name": name, "section": section.name, "ctype": "uint8_t"}
        result.append((entry, section, rom[start:end]))
    for name, bank, address, length in NATIVE_DATA_SPANS:
        start = rom_offset(bank, address)
        end = start + length
        if length < 1 or end > len(rom):
            raise ValueError(f"native data span exceeds ROM: {name}")
        section = Section(f"native-{name}", bank, address, address + length - 1)
        entry = {"name": name, "section": section.name, "ctype": "uint8_t"}
        result.append((entry, section, rom[start:end]))
    if not result:
        raise ValueError("source inventory has no declared data spans")
    return result


def render(items: list[tuple[dict[str, str], Section, bytes]], rom_name: str) -> str:
    lines = [f"/* Generated from {rom_name} by tools/gen_data.py. Do not edit. */", "#ifndef POKETCG_GENERATED_DATA_H", "#define POKETCG_GENERATED_DATA_H", "", "#include <stdint.h>", ""]
    for entry, section, data in items:
        lines.append(f"static const {entry['ctype']} poketcg_{entry['name']}[] = {{")
        for offset in range(0, len(data), 16):
            lines.append("    " + ", ".join(f"0x{byte:02X}" for byte in data[offset:offset + 16]) + ",")
        lines.extend(["};", ""])
    lines.append("#endif")
    return "\n".join(lines)


def parse_generated(text: str, items: list[tuple[dict[str, str], Section, bytes]]) -> dict[str, bytes]:
    lines = text.splitlines()
    arrays: dict[str, bytes] = {}
    index = 0
    while index < len(lines):
        match = ARRAY_RE.match(lines[index])
        if not match:
            index += 1
            continue
        values: list[int] = []
        index += 1
        while index < len(lines) and lines[index] != "};":
            for token in lines[index].strip().rstrip(",").split(","):
                token = token.strip()
                if token:
                    values.append(int(token, 0))
            index += 1
        arrays[match[2]] = bytes(values)
        index += 1
    expected = {f"poketcg_{entry['name']}" for entry, _, _ in items}
    if set(arrays) != expected:
        raise ValueError(f"generated arrays differ from schema: {sorted(set(arrays) ^ expected)}")
    return arrays


def verify(items: list[tuple[dict[str, str], Section, bytes]], arrays: dict[str, bytes], rom: bytes) -> tuple[int, int]:
    total = 0
    for entry, section, _ in items:
        start = rom_offset(section.bank, section.start)
        expected = rom[start:start + section.end - section.start + 1]
        actual = arrays[f"poketcg_{entry['name']}"]
        if len(actual) != len(expected):
            raise ValueError(f"section {section.name}: size {len(actual)} != {len(expected)}")
        for offset, (left, right) in enumerate(zip(actual, expected)):
            if left != right:
                raise ValueError(f"section {section.name}: first differing offset {offset:#x} (ROM {right:#04x}, generated {left:#04x})")
        total += len(expected)
    return len(items), total

PACK_MAGIC = b"PTCGDAT1"
PACK_HEADER = struct.Struct("<8sII")
PACK_RECORD = struct.Struct("<IHHII")


def write_sparse_pack(
    items: list[tuple[dict[str, str], Section, bytes]],
    rom: bytes,
    pack_path: Path,
    manifest_path: Path,
    rom_path: Path,
    map_path: Path,
    sym_path: Path,
) -> tuple[int, int]:
    payload = bytearray(PACK_HEADER.pack(PACK_MAGIC, 1, len(items)))
    payload.extend(b"\0" * PACK_RECORD.size * len(items))
    spans = []
    for entry, section, data in items:
        if section.name.casefold() == "romheader" or section.name.casefold().startswith(
            ("start", "game loop", "duel core", "menus", "overworld", "ai logic")
        ):
            raise ValueError(f"refusing executable section in sparse pack: {section.name}")
        pack_offset = len(payload)
        payload.extend(data)
        spans.append({
            "name": entry["name"],
            "section": section.name,
            "kind": "data",
            "bank": section.bank,
            "address": section.start,
            "length": len(data),
            "pack_offset": pack_offset,
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    records = bytearray()
    for span in spans:
        records.extend(PACK_RECORD.pack(
            span["bank"], span["address"], span["length"], span["pack_offset"], 0
        ))
    table_end = PACK_HEADER.size + len(records)
    payload[PACK_HEADER.size:table_end] = records
    pack_path.parent.mkdir(parents=True, exist_ok=True)
    pack_path.write_bytes(payload)
    manifest = {
        "schema": 1,
        "format": "poketcg-sparse-data-v1",
        "rom_sha256": hashlib.sha256(rom).hexdigest(),
        "map_sha256": hashlib.sha256(map_path.read_bytes()).hexdigest(),
        "symbol_sha256": hashlib.sha256(sym_path.read_bytes()).hexdigest(),
        "pack_sha256": hashlib.sha256(payload).hexdigest(),
        "pack_size": len(payload),
        "rom_source": str(rom_path),
        "spans": spans,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
    )
    return len(spans), len(payload)


def verify_sparse_pack(
    pack_path: Path,
    manifest_path: Path,
    rom: bytes,
    sections: dict[str, Section],
) -> tuple[int, int]:
    try:
        payload = pack_path.read_bytes()
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read sparse pack: {exc}") from exc
    if not isinstance(manifest, dict) or manifest.get("schema") != 1:
        raise ValueError("sparse pack manifest schema is invalid")
    if manifest.get("rom_sha256") != hashlib.sha256(rom).hexdigest():
        raise ValueError("sparse pack ROM identity differs from source")
    if manifest.get("pack_size") != len(payload):
        raise ValueError("sparse pack size differs from manifest")
    if hashlib.sha256(payload).hexdigest() != manifest.get("pack_sha256"):
        raise ValueError("sparse pack hash differs from manifest")
    if len(payload) < PACK_HEADER.size:
        raise ValueError("sparse pack is truncated")
    magic, version, count = PACK_HEADER.unpack(payload[:PACK_HEADER.size])
    if magic != PACK_MAGIC or version != 1:
        raise ValueError("sparse pack header is invalid")
    table_end = PACK_HEADER.size + count * PACK_RECORD.size
    if table_end > len(payload):
        raise ValueError("sparse pack record table is truncated")
    spans = manifest.get("spans")
    if not isinstance(spans, list) or count != len(spans):
        raise ValueError("sparse pack span count is invalid")
    total = 0
    expected_offset = table_end
    for index, span in enumerate(spans):
        if not isinstance(span, dict) or span.get("kind") != "data":
            raise ValueError("sparse pack contains a non-data span")
        section = sections.get(span.get("section"))
        label = span.get("section")
        if section is not None:
            expected_bank = section.bank
            expected_address = section.start
            expected_length = section.end - section.start + 1
            start = rom_offset(expected_bank, expected_address)
        else:
            expected_bank = span.get("bank")
            expected_address = span.get("address")
            expected_length = span.get("length")
            if not all(isinstance(value, int) for value in (
                expected_bank, expected_address, expected_length,
            )):
                raise ValueError(f"sparse pack span is invalid: {label}")
            start = rom_offset(expected_bank, expected_address)
        bank, address, length, pack_offset, _flags = PACK_RECORD.unpack_from(
            payload, PACK_HEADER.size + index * PACK_RECORD.size
        )
        if (span.get("bank"), span.get("address"), span.get("length")) != (
            bank, address, expected_length
        ):
            raise ValueError(f"sparse pack record differs: {label}")
        if pack_offset != expected_offset or span.get("pack_offset") != pack_offset:
            raise ValueError(f"sparse pack offsets are not contiguous: {label}")
        actual = payload[pack_offset:pack_offset + length]
        expected = rom[start:start + length]
        if len(actual) != length:
            raise ValueError(f"sparse pack data is truncated: {label}")
        if actual != expected or hashlib.sha256(actual).hexdigest() != span.get("sha256"):
            raise ValueError(f"sparse pack first mismatch: {label}")
        expected_offset += length
        total += length
    if expected_offset != len(payload):
        raise ValueError("sparse pack has trailing bytes")
    return len(spans), total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, default=Path("poketcg/poketcg.gbc"))
    parser.add_argument("--map", type=Path, default=Path("poketcg/poketcg.map"))
    parser.add_argument("--sym", type=Path, default=Path("poketcg/poketcg.sym"))
    parser.add_argument("--out", type=Path, default=Path("include/generated/data.h"))
    parser.add_argument("--verify", action="store_true")
    # --check validates the artifact already on disk instead of a freshly rendered
    # string, so a corrupted or stale include/generated/data.h is actually caught.
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sparse-pack", action="store_true")
    parser.add_argument("--pack-check", action="store_true")
    parser.add_argument("--pack", type=Path, default=Path("build/completion/data-pack.bin"))
    parser.add_argument(
        "--pack-manifest",
        type=Path,
        default=Path("build/completion/data-pack.json"),
    )
    args = parser.parse_args()
    for path in (args.rom, args.map, args.sym):
        if not path.exists():
            raise SystemExit(f"input not found: {path} (run `just bootstrap`)")
    sections = parse_map(args.map)
    symbols = parse_symbols(args.sym)
    rom = args.rom.read_bytes()
    items = sparse_items(rom) if args.sparse_pack else slices(SCHEMA, sections, symbols, rom)
    if args.sparse_pack and args.pack_check:
        parser.error("--sparse-pack and --pack-check are mutually exclusive")
    if args.sparse_pack or args.pack_check:
        if args.check:
            parser.error("--check validates the C header, not a sparse pack")
        if args.pack_check:
            count, total = verify_sparse_pack(args.pack, args.pack_manifest, rom, sections)
            print(f"gen_data: checked sparse pack {args.pack} -- {count} sections, {total} bytes")
        else:
            count, total = write_sparse_pack(
                items, rom, args.pack, args.pack_manifest,
                args.rom, args.map, args.sym,
            )
            print(f"gen_data: wrote sparse pack {args.pack} -- {count} sections, {total} bytes")
            if args.verify:
                verify_sparse_pack(args.pack, args.pack_manifest, rom, sections)
                print("gen_data: verified sparse pack")
        return 0
    if args.check:
        if not args.out.exists():
            raise SystemExit(f"nothing to check: {args.out} does not exist")
        arrays = parse_generated(args.out.read_text(), items)
        count, total = verify(items, arrays, rom)
        print(f"gen_data: checked {args.out} -- {count} sections, {total} bytes")
        return 0
    text = render(items, args.rom.name)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text)
    print(f"gen_data: wrote {args.out} ({len(items)} sections, {sum(len(data) for _, _, data in items)} bytes)")
    if args.verify:
        arrays = parse_generated(text, items)
        print(f"gen_data: checksum {zlib.crc32(b''.join(data for _, _, data in items)):08x}")
        count, total = verify(items, arrays, rom)
        print(f"gen_data: verified {count} sections, {total} bytes")
        perturbed = bytearray(rom)
        first_entry, first_section, _ = items[0]
        first_offset = rom_offset(first_section.bank, first_section.start)
        perturbed[first_offset] ^= 1
        try:
            verify(items, arrays, bytes(perturbed))
        except ValueError as error:
            print(f"gen_data: perturbation caught: {error}")
        else:
            raise ValueError(f"perturbation was not detected in {first_section.name}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"gen_data: error: {error}", file=sys.stderr)
        raise SystemExit(1)
