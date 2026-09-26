#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import struct
import subprocess
import zlib
from pathlib import Path

from gen_lz import decompress

ROOT = Path(__file__).resolve().parents[1]
MINT_SOURCE_COMMIT = "1de12603f93ca0dc48dae628735acdd6c334a604"
PORTRAIT_BANK = 0xF6
SINGLE_PORTRAIT_BANK = 0xF7
SPRITE_BANK = 0xF8
PALETTE_BANK = 0xF9
TEXT_BANK = 0xFA
PORTRAIT_TILES = 36
SPRITE_TILES = 20
PALETTE_LABEL = "Palette079"
ATTRIBUTE_TILEMAP = "tilemap0D4.bin"
RGB_LINE = re.compile(r"^\s*rgb\s+(\d+),\s*(\d+),\s*(\d+)")


def source_root(root: Path) -> Path:
    path = root / "poketcg2"
    if not path.is_dir():
        raise ValueError(f"missing pinned poketcg2 checkout: {path} (run `just bootstrap`)")
    try:
        revision = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"], text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot read poketcg2 revision: {exc}") from exc
    if revision != MINT_SOURCE_COMMIT:
        raise ValueError(f"poketcg2 revision {revision} differs from pinned {MINT_SOURCE_COMMIT}")
    return path / "src"


def decode_png(path: Path) -> tuple[int, int, list[int]]:
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    pos = 8
    width = height = depth = color_type = None
    compressed = bytearray()
    while pos < len(raw):
        size = struct.unpack_from(">I", raw, pos)[0]
        kind = raw[pos + 4:pos + 8]
        body = raw[pos + 8:pos + 8 + size]
        pos += size + 12
        if kind == b"IHDR":
            width, height, depth, color_type, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", body
            )
            if compression or filtering or interlace or depth != 2 or color_type != 0:
                raise ValueError(f"unsupported PNG format: {path}")
        elif kind == b"IDAT":
            compressed.extend(body)
        elif kind == b"IEND":
            break
    if width is None or height is None:
        raise ValueError(f"PNG has no IHDR: {path}")
    stride = (width * depth + 7) // 8
    decoded = zlib.decompress(compressed)
    rows: list[list[int]] = []
    previous = bytearray(stride)
    cursor = 0
    for _ in range(height):
        filter_type = decoded[cursor]
        current = bytearray(decoded[cursor + 1:cursor + 1 + stride])
        cursor += stride + 1
        for index in range(stride):
            left = current[index - 1] if index else 0
            above = previous[index]
            upper_left = previous[index - 1] if index else 0
            if filter_type == 1:
                current[index] = (current[index] + left) & 0xFF
            elif filter_type == 2:
                current[index] = (current[index] + above) & 0xFF
            elif filter_type == 3:
                current[index] = (current[index] + (left + above) // 2) & 0xFF
            elif filter_type == 4:
                estimate = left + above - upper_left
                left_distance = abs(estimate - left)
                above_distance = abs(estimate - above)
                upper_left_distance = abs(estimate - upper_left)
                predictor = left if left_distance <= above_distance and left_distance <= upper_left_distance else (
                    above if above_distance <= upper_left_distance else upper_left
                )
                current[index] = (current[index] + predictor) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}: {path}")
        row: list[int] = []
        for byte in current:
            row.extend((byte >> 6, (byte >> 4) & 3, (byte >> 2) & 3, byte & 3))
        rows.append(row[:width])
        previous = current
    return width, height, [pixel for row in rows for pixel in row]


def tile_pixels(path: Path, expected_tiles: int) -> list[list[int]]:
    width, height, pixels = decode_png(path)
    if width % 8 or height % 8:
        raise ValueError(f"Mint image is not tile-aligned: {path}")
    tiles: list[list[int]] = []
    for tile_y in range(height // 8):
        for tile_x in range(width // 8):
            tiles.append([
                3 - pixels[(tile_y * 8 + row) * width + tile_x * 8 + column]
                for row in range(8)
                for column in range(8)
            ])
    if len(tiles) != expected_tiles:
        raise ValueError(f"unexpected tile count for {path}: {len(tiles)}")
    return tiles


def encode_tiles(tiles: list[list[int]]) -> bytes:
    data = bytearray(struct.pack("<H", len(tiles)))
    for tile in tiles:
        for row in range(8):
            low = high = 0
            for column in range(8):
                value = tile[row * 8 + column]
                low |= (value & 1) << (7 - column)
                high |= ((value >> 1) & 1) << (7 - column)
            data.extend((low, high))
    return bytes(data)


def portrait_attributes(source: Path) -> list[int]:
    data = decompress((source / "data" / "maps" / "tiles" / ATTRIBUTE_TILEMAP).read_bytes())
    if len(data) != 72:
        raise ValueError(f"unexpected Mint tilemap size: {len(data)}")
    attributes: list[int] = []
    for row in range(6):
        attributes.extend(value & 0x07 for value in data[row * 12 + 6:row * 12 + 12])
    if max(attributes) > 2:
        raise ValueError(f"Mint tilemap uses palette {max(attributes)}")
    return attributes


def portrait_palettes(source: Path) -> list[list[tuple[int, int, int]]]:
    lines = (source / "data" / "palettes1.asm").read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith(f"{PALETTE_LABEL}::"))
    count = int(lines[start + 1].split()[1])
    colors: list[tuple[int, int, int]] = []
    for line in lines[start + 2:]:
        match = RGB_LINE.match(line)
        if match:
            colors.append((int(match[1]), int(match[2]), int(match[3])))
        if len(colors) == count * 4:
            break
    if len(colors) != count * 4:
        raise ValueError(f"{PALETTE_LABEL}: expected {count * 4} colours, found {len(colors)}")
    return [colors[index:index + 4] for index in range(0, len(colors), 4)]


def player_portrait_backdrop(path: Path) -> tuple[int, int, int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith("PlayerPicPal::"))
    for line in lines[start + 1:]:
        match = RGB_LINE.match(line)
        if match:
            return int(match[1]), int(match[2]), int(match[3])
    raise ValueError(f"PlayerPicPal has no colours: {path}")


def palette_bytes(palette: list[tuple[int, int, int]]) -> bytes:
    data = bytearray()
    for red, green, blue in palette:
        value = red | (green << 5) | (blue << 10)
        data.extend((value & 0xFF, value >> 8))
    return bytes(data)


def single_palette_tiles(tiles: list[list[int]], attributes: list[int]) -> list[list[int]]:
    remap = {0: (0, 1, 2, 3), 1: (0, 0, 2, 3), 2: (0, 0, 1, 3)}
    return [[remap[attribute][value] for value in tile] for tile, attribute in zip(tiles, attributes)]


def text_from_rom(rom: bytes, text_id: int) -> bytes:
    def rom_offset(bank: int, address: int) -> int:
        return address if address < 0x4000 else bank * 0x4000 + address - 0x4000

    entry = rom_offset(0x0D, 0x4000 + text_id * 3)
    low, high, bank_bits = rom[entry:entry + 3]
    bank = 0x0D + (bank_bits << 2) + (high >> 6)
    address = 0x4000 | ((high & 0x3F) << 8) | low
    start = rom_offset(bank, address)
    end = rom.index(0, start) + 1
    return rom[start:end]


def build_texts(rom: bytes) -> dict[int, bytes]:
    replacements = {
        0x05A6: ((b"He, too, has", b"She, too, has"),),
        0x05E3: ((b"with him for", b"with her for"),),
        0x05F1: ((b"handed his cards", b"handed her cards"),),
        0x0657: ((b"make his Pok", b"make her Pok"),),
        0x06A0: ((b"\nhis Energy", b"\nher Energy"),),
    }
    result: dict[int, bytes] = {}
    for text_id, changes in replacements.items():
        data = text_from_rom(rom, text_id)
        for old, new in changes:
            if data.count(old) != 1:
                raise ValueError(f"text {text_id:04X}: expected one {old!r}")
            data = data.replace(old, new)
        result[text_id] = data
    return result


def text_blob(texts: dict[int, bytes]) -> bytes:
    header = bytearray(b"MTXT" + bytes((len(texts),)))
    records = bytearray()
    body = bytearray()
    offset = 5 + len(texts) * 6
    for text_id, data in sorted(texts.items()):
        records.extend(struct.pack("<HHH", text_id, offset, len(data)))
        body.extend(data)
        offset += len(data)
    return bytes(header + records + body)


def source_file(root: Path, path: Path) -> dict[str, str]:
    try:
        relative = path.relative_to(root / "poketcg2")
        label = f"poketcg2@{MINT_SOURCE_COMMIT}/{relative.as_posix()}"
    except ValueError:
        label = path.relative_to(root).as_posix()
    return {"path": label, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def asset(kind_id: int, name: str, data: bytes, bank: int, paths: list[Path], root: Path) -> dict[str, object]:
    return {
        "kind": "mint_asset",
        "id": kind_id,
        "name": name,
        "bank": bank,
        "flags": 0xD0000000 | kind_id,
        "data": data,
        "sha256": hashlib.sha256(data).hexdigest(),
        "source_files": [source_file(root, path) for path in paths],
    }


def build_mint(root: Path, rom: bytes) -> list[dict[str, object]]:
    source = source_root(root)
    portrait_png = source / "gfx" / "duelists" / "mint.png"
    sprite_png = source / "gfx" / "overworld_sprites" / "mint.png"
    tilemap_bin = source / "data" / "maps" / "tiles" / ATTRIBUTE_TILEMAP
    palette_asm = source / "data" / "palettes1.asm"
    backdrop_asm = root / "poketcg" / "src" / "gfx.asm"
    tiles = tile_pixels(portrait_png, PORTRAIT_TILES)
    attributes = portrait_attributes(source)
    palettes = portrait_palettes(source)
    if len(palettes) != 3:
        raise ValueError(f"{PALETTE_LABEL}: expected 3 palettes, found {len(palettes)}")
    backdrop = player_portrait_backdrop(backdrop_asm)
    palette_blob = bytearray((0, len(palettes)))
    for palette in palettes:
        palette_blob.extend(palette_bytes([backdrop] + palette[1:]))
    palette_blob.extend(attributes)
    palette_blob.extend((0, 1))
    palette_blob.extend(palette_bytes([backdrop] + palettes[0][1:]))
    text_paths = [root / "poketcg" / "src" / "text" / name for name in ("text6.asm", "text7.asm", "text8.asm")]
    return [
        asset(1, "Mint portrait", encode_tiles(tiles), PORTRAIT_BANK, [portrait_png], root),
        asset(2, "Mint single-palette portrait", encode_tiles(single_palette_tiles(tiles, attributes)),
              SINGLE_PORTRAIT_BANK, [portrait_png, tilemap_bin], root),
        asset(3, "Mint overworld sprite", encode_tiles(tile_pixels(sprite_png, SPRITE_TILES)), SPRITE_BANK,
              [sprite_png], root),
        asset(4, "Mint portrait palettes", bytes(palette_blob), PALETTE_BANK,
              [palette_asm, tilemap_bin, backdrop_asm], root),
        asset(5, "Mint text variants", text_blob(build_texts(rom)), TEXT_BANK, text_paths, root),
    ]


def build_mint_assets(root: Path, rom: bytes) -> list[dict[str, object]]:
    return build_mint(root.resolve(), rom)
