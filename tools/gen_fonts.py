#!/usr/bin/env python3
"""Build 8x8 alternate font banks in the ROM text layouts."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_BANK_BASE = 0xF0
FULL_WIDTH_FILES = (
    ("0_0_katakana.1bpp", 640),
    ("0_1_hiragana.1bpp", 768),
    ("0_2_digits_kanji1.1bpp", 1280),
    ("1_kanji2.1bpp", 2048),
    ("2_kanji3.1bpp", 2048),
    ("3.1bpp", 2048),
    ("4.1bpp", 1000),
)
HALF_WIDTH_FILE = "half_width.1bpp"
FULL_BLOB = sum(size for _, size in FULL_WIDTH_FILES)
BANK_BYTES = FULL_BLOB + 768
FULL_LATIN_BASE = (3 << 8) * 8 + 0x50 * 8
FONT_SPECS = (
    (1, "Public Pixel", "public-pixel-8.hex", "PublicPixel.ttf", "public-pixel-LICENSE.txt"),
    (2, "Unscii-8", "unscii-8.hex", None, "unscii-LICENSE.txt"),
    (3, "Pixel Operator 8", "pixel-operator-8.hex", "PixelOperator8.ttf", "pixel-operator-LICENSE.txt"),
)
HALF_SOURCE = "tom-thumb.bdf"
HALF_LICENSE = "tom-thumb-LICENSE.txt"
HALF_BASELINE_ROW = 6
CHARMAP_LINE = re.compile(r'^\s*charmap\s+(".*"),\s*\$([0-9A-Fa-f]+)')
FULLWIDTH_LINE = re.compile(r'^\s*fwcharmap\s+TX_FULLWIDTH3,\s+(".*"),\s*\$([0-9A-Fa-f]+)')


def decode_text(value: str) -> str:
    value = value[1:-1]
    return value.replace(r"\\", "\\").replace(r"\{", "{").replace(r"\}", "}").replace(r'\"', '"')


def load_charmaps(path: Path) -> tuple[dict[int, int], dict[int, int]]:
    half: dict[int, int] = {}
    full: dict[int, int] = {}
    in_half = True
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("NEWCHARMAP"):
            in_half = False
            continue
        match = CHARMAP_LINE.match(line)
        if match and in_half:
            text = decode_text(match[1])
            if len(text) == 1:
                half[int(match[2], 16)] = ord(text)
            continue
        match = FULLWIDTH_LINE.match(line)
        if match:
            text = decode_text(match[1])
            if len(text) == 1:
                full[int(match[2], 16)] = ord(text)
    if not half or not full:
        raise ValueError(f"charmap parse found no entries: {path}")
    return half, full


def load_hex(path: Path) -> dict[int, bytes]:
    glyphs: dict[int, bytes] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        codepoint, bitmap = line.split(":", 1)
        data = bytes.fromhex(bitmap)
        if len(data) == 8:
            glyphs[int(codepoint, 16)] = data
    if not glyphs:
        raise ValueError(f"no 8x8 glyphs found: {path}")
    return glyphs


def source_layout(root: Path) -> tuple[bytearray, bytearray]:
    font_root = root / "poketcg" / "src" / "gfx" / "fonts"
    full = bytearray()
    for name, size in FULL_WIDTH_FILES:
        data = (font_root / "full_width" / name).read_bytes()
        if len(data) != size:
            raise ValueError(f"unexpected size for {name}: {len(data)} != {size}")
        full.extend(data)
    half = bytearray((font_root / HALF_WIDTH_FILE).read_bytes())
    if len(half) != 768:
        raise ValueError(f"unexpected half-width font size: {len(half)}")
    return full, half


def load_bdf(path: Path) -> dict[int, bytes]:
    glyphs: dict[int, bytes] = {}
    codepoint = -1
    box = (0, 0, 0, 0)
    rows: list[int] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        fields = raw.split()
        if not fields:
            continue
        if fields[0] == "ENCODING":
            codepoint = int(fields[1])
        elif fields[0] == "BBX":
            box = tuple(int(value) for value in fields[1:5])
        elif fields[0] == "BITMAP":
            rows = []
        elif fields[0] == "ENDCHAR":
            if rows is not None and codepoint >= 0:
                glyphs[codepoint] = half_glyph(rows, box)
            rows = None
        elif rows is not None:
            value = int(fields[0], 16)
            bits = 4 * len(fields[0])
            rows.append(value >> (bits - 8) if bits > 8 else value << (8 - bits))
    if not glyphs:
        raise ValueError(f"no BDF glyphs found: {path}")
    return glyphs


def half_glyph(rows: list[int], box: tuple[int, int, int, int]) -> bytes:
    width, height, x_offset, y_offset = box
    cell = bytearray(8)
    for index, value in enumerate(rows):
        row = HALF_BASELINE_ROW - (y_offset + height - 1 - index)
        if not 0 <= row < 8:
            continue
        for bit in range(width):
            column = x_offset + bit
            if value & (0x80 >> bit) and 0 <= column < 3:
                cell[row] |= 0x80 >> column
    return bytes(cell)


def spaced_glyph(glyph: bytes) -> bytes:
    mask = 0
    for row in glyph:
        mask |= row
    if not mask:
        return glyph
    columns = [column for column in range(8) if mask & (0x80 >> column)]
    left, right = columns[0], columns[-1]
    width = right - left + 1
    rows = []
    for row in glyph:
        bits = [(row >> (7 - column)) & 1 for column in range(left, right + 1)]
        if width == 8:
            bits = bits[:3] + [bits[3] | bits[4]] + bits[5:]
        rows.append(bits)
    width = len(rows[0])
    start = 0 if width == 7 else 1 + (6 - width) // 2
    return bytes(
        sum(bit << (7 - start - index) for index, bit in enumerate(bits))
        for bits in rows
    )


def build_font(root: Path, spec: tuple[int, str, str, str | None, str]) -> dict[str, object]:
    font_id, name, bitmap_name, source_name, license_name = spec
    full, half = source_layout(root)
    glyphs = load_hex(root / "third_party" / "fonts" / bitmap_name)
    half_glyphs = load_bdf(root / "third_party" / "fonts" / HALF_SOURCE)
    half_map, full_map = load_charmaps(root / "poketcg" / "src" / "constants" / "charmaps.asm")
    full_used = 0
    full_fallback: list[int] = []
    for slot, codepoint in sorted(full_map.items()):
        glyph = glyphs.get(codepoint)
        offset = FULL_LATIN_BASE + slot * 8
        if glyph is None or offset + 8 > len(full):
            full_fallback.append(slot)
            continue
        full[offset:offset + 8] = spaced_glyph(glyph)
        full_used += 1
    half_used = 0
    half_fallback: list[int] = []
    for code, codepoint in sorted(half_map.items()):
        glyph = half_glyphs.get(codepoint)
        if not 0x20 <= code <= 0x7F:
            continue
        offset = (code - 0x20) * 8
        if glyph is None:
            half_fallback.append(code)
            continue
        half[offset:offset + 8] = glyph
        half_used += 1
    if not full_used and not half_used:
        raise ValueError(f"{name}: no glyphs resolved, font bank would be empty")
    data = bytes(full + half)
    if len(data) != BANK_BYTES:
        raise ValueError(f"unexpected {name} bank size: {len(data)}")
    source_paths = [root / "third_party" / "fonts" / bitmap_name]
    if source_name:
        source_paths.append(root / "third_party" / "fonts" / source_name)
    source_paths.append(root / "third_party" / "fonts" / license_name)
    source_paths.append(root / "third_party" / "fonts" / HALF_SOURCE)
    source_paths.append(root / "third_party" / "fonts" / HALF_LICENSE)
    return {
        "id": font_id,
        "name": name,
        "bank": FONT_BANK_BASE + font_id - 1,
        "data": data,
        "sha256": hashlib.sha256(data).hexdigest(),
        "full_used": full_used,
        "full_fallback": full_fallback,
        "half_used": half_used,
        "half_fallback": half_fallback,
        "source_files": [
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in source_paths
        ],
    }


def build_fonts(root: Path = ROOT) -> list[dict[str, object]]:
    return [build_font(root, spec) for spec in FONT_SPECS]


def source_manifest(root: Path = ROOT) -> list[dict[str, object]]:
    return [
        {
            "id": font["id"],
            "name": font["name"],
            "bank": font["bank"],
            "sha256": font["sha256"],
            "source_files": font["source_files"],
        }
        for font in build_fonts(root)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    fonts = build_fonts(args.root.resolve())
    for font in fonts:
        print(
            f"gen_fonts: {font['name']} bank={font['bank']:02X} "
            f"full_width={font['full_used']}+{len(font['full_fallback'])}fallback "
            f"half_width={font['half_used']}+{len(font['half_fallback'])}fallback"
        )
        if args.verify:
            print(f"gen_fonts:   full_width fallback slots: {[hex(v) for v in font['full_fallback']]}")
            print(f"gen_fonts:   half_width fallback codes: {[hex(v) for v in font['half_fallback']]}")
    print(f"gen_fonts: checked {len(fonts)} alternate fonts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
