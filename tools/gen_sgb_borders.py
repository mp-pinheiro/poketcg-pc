#!/usr/bin/env python3
"""Pack the game's own SGB borders as SNES tiles, map and palettes."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BORDER_BANK_BASE = 0xF3
TILE_BYTES = 0x2000
MAP_BYTES = 0x800
PALETTE_BYTES = 0x80
BORDER_BYTES = TILE_BYTES + MAP_BYTES + PALETTE_BYTES
BORDER_SPECS = (
    (1, "Intro", "border_intro_1.bin", "border_intro_2.bin", "border_intro_3.bin", "border_intro_4.bin"),
    (2, "Medals", "border_medals_1.bin", "border_medals_2.bin", "border_medals_3.bin", "border_medals_5.bin"),
    (3, "Legend", "border_medals_1.bin", "border_medals_2.bin", "border_medals_4.bin", "border_medals_5.bin"),
)


def build_border(root: Path, spec: tuple[int, str, str, str, str, str]) -> dict[str, object]:
    border_id, name, tiles_low, tiles_high, palettes, tile_map = spec
    source = root / "poketcg" / "src" / "data" / "sgb_data"
    paths = [source / tiles_low, source / tiles_high, source / palettes, source / tile_map]
    low, high, pals, layout = (path.read_bytes() for path in paths)
    if len(low) > 0x1000 or len(high) > 0x1000 or len(pals) > PALETTE_BYTES or len(layout) != MAP_BYTES:
        raise ValueError(f"unexpected SGB border source sizes for {name}")
    data = low.ljust(0x1000, b"\0") + high.ljust(0x1000, b"\0") + layout + pals.ljust(PALETTE_BYTES, b"\0")
    return {
        "kind": "sgb_border",
        "id": border_id,
        "name": name,
        "bank": BORDER_BANK_BASE + border_id - 1,
        "flags": 0xE0000000 | border_id,
        "data": data,
        "sha256": hashlib.sha256(data).hexdigest(),
        "source_files": [
            {"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in paths
        ],
    }


def build_borders(root: Path = ROOT) -> list[dict[str, object]]:
    return [build_border(root, spec) for spec in BORDER_SPECS]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    for border in build_borders(args.root.resolve()):
        print(f"gen_sgb_borders: {border['name']} bank={border['bank']:02X} bytes={len(border['data'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
