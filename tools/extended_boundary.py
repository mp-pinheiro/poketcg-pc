#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from profiles import get_profile

ROOT = Path(__file__).resolve().parent.parent
BOUNDARY_IDS = (0x00FE, 0x00FF, 0x0100, 0x01FF)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def patch_fixture(source: Path) -> None:
    pointers = source / "src" / "data" / "card_pointers.asm"
    lines = pointers.read_text().splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith("\tdab "))
    end = next(index for index in range(start, len(lines)) if lines[index] == "\tdwb NULL, $0")
    entries = lines[start:end]
    if not entries:
        raise SystemExit("Extended CardPointers has no card entries")
    while len(entries) < 0x1FF:
        entries.append(entries[-1])
    for card_id in BOUNDARY_IDS:
        entries[card_id - 1] = entries[0]
    pointers.write_text("\n".join(lines[:start] + entries + lines[end:]) + "\n")
    constants = source / "src" / "constants" / "card_constants.asm"
    text = constants.read_text()
    marker = "DEF NUM_CARDS EQU const_value - 1"
    if marker not in text:
        raise SystemExit("Extended NUM_CARDS definition not found")
    constants.write_text(text.replace(marker, "DEF NUM_CARDS EQU $1ff", 1))


def build_fixture(root: Path) -> dict[str, object]:
    profile = get_profile("extended", root)
    with tempfile.TemporaryDirectory(prefix="poketcg-extended-boundary-") as directory:
        source = Path(directory) / profile.checkout
        shutil.copytree(profile.source_path(root), source)
        patch_fixture(source)
        rgbasm = shutil.which("rgbasm")
        if rgbasm is None:
            raise SystemExit("RGBDS 1.0.0 is required for the Extended boundary fixture")
        rgbds = str(Path(rgbasm).parent) + "/"
        subprocess.run(["make", "-C", str(source), "clean"], check=True)
        subprocess.run(["make", "-C", str(source), "DEBUG=1", f"RGBDS={rgbds}"], check=True)
        rom = source / profile.rom_name
        if not rom.is_file():
            raise SystemExit(f"boundary fixture ROM missing: {rom}")
        result = {
            "schema": 1,
            "profile": profile.name,
            "source_commit": profile.source_commit,
            "rom_sha256": sha256(rom),
            "card_ids": list(BOUNDARY_IDS),
            "catalog_card_count": 0xE4,
            "fixture_card_count": 0x1FF,
            "storage": {
                "collection_bytes": 0x200,
                "deck_entries": 60,
                "deck_entry_bytes": 2,
                "deck_compressed_bytes": 68,
            },
        }
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "build-extended" / "completion" / "extended-boundary.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build_fixture(ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.check and args.output.is_file():
        previous = json.loads(args.output.read_text())
        if previous != result:
            raise SystemExit("Extended boundary fixture changed")
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(f"extended-boundary: PASS rom_sha256={result['rom_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
