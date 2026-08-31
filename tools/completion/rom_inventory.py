#!/usr/bin/env python3
"""Build a complete physical-ROM span inventory from map and symbols."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT / "poketcg" / "poketcg.gbc"
DEFAULT_MAP = ROOT / "poketcg" / "poketcg.map"
DEFAULT_SYMBOLS = ROOT / "poketcg" / "poketcg.sym"
DEFAULT_OUTPUT = ROOT / "build" / "completion" / "rom-inventory.json"
ROM_SIZE = 0x100000
BANK_SIZE = 0x4000

BANK_RE = re.compile(r"^(ROM0|ROMX|SRAM|WRAM0|WRAM|HRAM|VRAM|OAM) bank #(\d+):$")
SECTION_RE = re.compile(
    r'^\tSECTION: \$([0-9a-fA-F]{4})-\$([0-9a-fA-F]{4}) '
    r'\(\$([0-9a-fA-F]{4}) bytes\) \["(.*)"\]$'
)
SYMBOL_RE = re.compile(r"^([0-9a-fA-F]{2}):([0-9a-fA-F]{4})\s+(\S+)$")
ROM_TYPES = {"ROM0", "ROMX"}
DATA_HINTS = (
    "audio", "anim", "booster", "card", "deck", "gfx", "graphic", "pal",
    "text", "sgb", "table", "data", "map objects", "map data", "copyright",
)


@dataclass(frozen=True)
class Section:
    bank_type: str
    bank: int
    start: int
    end: int
    name: str

    @property
    def length(self) -> int:
        return self.end - self.start + 1

    @property
    def offset(self) -> int:
        if self.bank_type == "ROM0":
            return self.start
        return self.bank * BANK_SIZE + (self.start - BANK_SIZE)


def fail(message: str) -> None:
    raise ValueError(message)


def parse_map(path: Path) -> list[Section]:
    if not path.is_file():
        fail(f"missing map: {path}")
    current: tuple[str, int] | None = None
    sections: list[Section] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        bank_match = BANK_RE.fullmatch(raw)
        if bank_match:
            current = (bank_match.group(1), int(bank_match.group(2)))
            continue
        section_match = SECTION_RE.fullmatch(raw)
        if not section_match or current is None or current[0] not in ROM_TYPES:
            continue
        start = int(section_match.group(1), 16)
        end = int(section_match.group(2), 16)
        declared = int(section_match.group(3), 16)
        if end < start or end - start + 1 != declared:
            fail(f"invalid section extent in {path}: {raw}")
        section = Section(current[0], current[1], start, end, section_match.group(4))
        if section.offset < 0 or section.offset + section.length > ROM_SIZE:
            fail(f"section outside ROM: {section.name}")
        sections.append(section)
    if not sections:
        fail(f"no ROM sections in map: {path}")
    return sections


def parse_symbols(path: Path) -> list[tuple[int, int, str]]:
    if not path.is_file():
        fail(f"missing symbols: {path}")
    symbols: list[tuple[int, int, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = SYMBOL_RE.fullmatch(raw)
        if not match:
            continue
        bank = int(match.group(1), 16)
        address = int(match.group(2), 16)
        name = match.group(3)
        offset = address if bank == 0 else bank * BANK_SIZE + address - BANK_SIZE
        if 0 <= offset < ROM_SIZE:
            symbols.append((bank, address, name))
    if not symbols:
        fail(f"no symbols in: {path}")
    return symbols


def section_kind(name: str) -> str:
    lowered = name.casefold()
    if lowered == "romheader":
        return "header/metadata"
    if any(hint in lowered for hint in DATA_HINTS):
        return "data"
    if lowered.startswith("rst") or lowered in {
        "vblank", "lcdc", "timer", "serial", "joypad", "start",
        "audio callback", "game loop", "duel core", "menus common",
        "menus 1", "menus 2", "menus 3", "menus 4", "overworld scripting",
        "overworld map", "save", "map scripts", "sprite animations",
        "scenes", "challenge machine", "ai logic 1", "ai logic 2",
        "effect commands", "animation commands", "ir communications core",
        "sprite animations vblank", "starter deck", "link functions",
        "promotional card", "booster pack menu", "input name",
        "auto deck machines", "bank 7", "duel animations", "start menu",
        "intro sequence", "credits sequence", "effect functions",
        "unused save validation",
    }:
        return "code"
    return "unclassified"


def symbol_offset(bank: int, address: int) -> int:
    if bank == 0:
        return address
    return bank * BANK_SIZE + (address - BANK_SIZE)


def section_spans(
    section: Section, symbols: list[tuple[int, int, str]],
) -> list[dict[str, object]]:
    section_end = section.offset + section.length
    expected_bank = section.bank if section.bank_type == "ROMX" else 0
    address_names: dict[int, str] = {}
    for bank, address, name in symbols:
        offset = symbol_offset(bank, address)
        if (
            bank == expected_bank
            and section.offset <= offset < section_end
            and "." not in name
        ):
            address_names.setdefault(offset, name)
    addresses = sorted(address_names.items())
    kind = section_kind(section.name)
    spans: list[dict[str, object]] = []
    cursor = section.offset
    for index, (offset, name) in enumerate(addresses):
        if offset > cursor:
            spans.append({
                "kind": "unclassified",
                "source": "mapped-gap",
                "bank_type": section.bank_type,
                "bank": section.bank,
                "address": section.start + cursor - section.offset,
                "length": offset - cursor,
                "offset": cursor,
                "section": section.name,
            })
        end = addresses[index + 1][0] if index + 1 < len(addresses) else section_end
        spans.append({
            "kind": kind,
            "source": "mapped-symbol",
            "bank_type": section.bank_type,
            "bank": section.bank,
            "address": section.start + offset - section.offset,
            "length": end - offset,
            "offset": offset,
            "section": section.name,
            "symbol": name,
        })
        cursor = end
    if cursor < section_end:
        spans.append({
            "kind": "unclassified",
            "source": "mapped-gap",
            "bank_type": section.bank_type,
            "bank": section.bank,
            "address": section.start + cursor - section.offset,
            "length": section_end - cursor,
            "offset": cursor,
            "section": section.name,
        })
    return spans


def add_padding(spans: list[dict[str, object]], cursor: int, end: int) -> None:
    if cursor >= end:
        return
    spans.append({
        "kind": "padding",
        "source": "unmapped",
        "bank_type": None,
        "bank": None,
        "address": None,
        "length": end - cursor,
        "offset": cursor,
        "section": None,
    })


def merge_adjacent(spans: list[dict[str, object]]) -> list[dict[str, object]]:
    merged: list[dict[str, object]] = []
    for span in spans:
        if (
            merged
            and span["source"] == "unmapped"
            and merged[-1]["source"] == "unmapped"
            and merged[-1]["kind"] == span["kind"]
            and merged[-1]["offset"] + merged[-1]["length"] == span["offset"]
        ):
            merged[-1]["length"] += span["length"]
            continue
        merged.append(span)
    return merged


def build(rom: Path, map_path: Path, symbols_path: Path) -> dict[str, object]:
    if not rom.is_file():
        fail(f"missing ROM: {rom}")
    actual_size = rom.stat().st_size
    if actual_size != ROM_SIZE:
        fail(f"ROM size {actual_size}, expected {ROM_SIZE}")
    sections = parse_map(map_path)
    symbols = parse_symbols(symbols_path)
    mapped = sorted(
        (
            span
            for section in sections
            for span in section_spans(section, symbols)
        ),
        key=lambda item: int(item["offset"]),
    )
    spans: list[dict[str, object]] = []
    cursor = 0
    for span in mapped:
        offset = int(span["offset"])
        length = int(span["length"])
        if offset < cursor:
            fail(f"overlapping mapped spans at 0x{offset:06x}")
        add_padding(spans, cursor, offset)
        spans.append(span)
        cursor = offset + length
    add_padding(spans, cursor, ROM_SIZE)
    spans = merge_adjacent(spans)
    covered = 0
    totals: dict[str, int] = {}
    for span in spans:
        length = int(span["length"])
        covered += length
        kind = str(span["kind"])
        totals[kind] = totals.get(kind, 0) + length
    if covered != ROM_SIZE:
        fail(f"physical span union {covered}, expected {ROM_SIZE}")
    raw_rom = rom.read_bytes()
    return {
        "schema": 2,
        "rom_size": ROM_SIZE,
        "rom_sha256": hashlib.sha256(raw_rom).hexdigest(),
        "map_sha256": hashlib.sha256(map_path.read_bytes()).hexdigest(),
        "symbol_sha256": hashlib.sha256(symbols_path.read_bytes()).hexdigest(),
        "mapped_sections": len(sections),
        "symbols": len(symbols),
        "mapped_bytes": sum(section.length for section in sections),
        "unclassified_bytes": totals.get("unclassified", 0),
        "spans": spans,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--map", dest="map_path", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--symbols", type=Path, default=DEFAULT_SYMBOLS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        result = build(args.rom, args.map_path, args.symbols)
    except (OSError, ValueError) as exc:
        print(f"rom-inventory: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "rom_bytes": result["rom_size"],
        "mapped_bytes": result["mapped_bytes"],
        "unclassified_bytes": result["unclassified_bytes"],
        "spans": len(result["spans"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
