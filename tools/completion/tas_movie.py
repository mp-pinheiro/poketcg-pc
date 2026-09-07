#!/usr/bin/env python3
"""Convert a BizHawk .bk2 movie into the port's per-frame input encoding."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# scenario.boot_input's JOYP nibble order: low nibble dpad, high nibble buttons.
BK2_TO_MASK = {
    "A": 0x10, "B": 0x20, "Select": 0x40, "Start": 0x80,
    "Right": 0x01, "Left": 0x02, "Up": 0x04, "Down": 0x08,
}


class MovieError(RuntimeError):
    pass


def open_movie(path: Path) -> zipfile.ZipFile:
    """TASVideos serves the .bk2 wrapped in an outer zip, so unwrap once if the
    archive holds a single nested .bk2 rather than the movie members."""
    archive = zipfile.ZipFile(path)
    names = archive.namelist()
    if "Input Log.txt" in names:
        return archive
    nested = [name for name in names if name.lower().endswith(".bk2")]
    if len(nested) != 1:
        raise MovieError(f"{path} is not a bk2 movie: {names}")
    inner = ROOT / "build" / "completion" / "tas" / "inner.bk2"
    inner.parent.mkdir(parents=True, exist_ok=True)
    inner.write_bytes(archive.read(nested[0]))
    return zipfile.ZipFile(inner)


def header(archive: zipfile.ZipFile) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in archive.read("Header.txt").decode(errors="replace").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            fields[parts[0]] = parts[1].strip()
    return fields


def masks(archive: zipfile.ZipFile) -> list[int]:
    lines = archive.read("Input Log.txt").decode(errors="replace").splitlines()
    # Newer BizHawk writes an [Input] section header before LogKey.
    header_index = next(
        (index for index, line in enumerate(lines) if line.startswith("LogKey:")), None)
    if header_index is None:
        raise MovieError("input log has no LogKey header")
    columns = [name for name in lines[header_index][len("LogKey:"):].split("|") if name]
    if columns and columns[0] == "#":
        columns = columns[1:]
    out: list[int] = []
    for line in lines[header_index + 1:]:
        if not line.startswith("|"):
            continue
        # Frame rows are |<one char per column>|; a dot means unpressed and the
        # pressed character is the button's own initial.
        body = line.strip("|")
        if len(body) < len(columns):
            continue
        mask = 0
        for index, name in enumerate(columns):
            if body[index] != "." and name in BK2_TO_MASK:
                mask |= BK2_TO_MASK[name]
        out.append(mask)
    if not out:
        raise MovieError("input log has no frame rows")
    return out


def frame_mode(archive: zipfile.ZipFile) -> str:
    """BizHawk's Gambatte frame clock, from the movie's SyncSettings:
    EqualLengthFrames=true (the 1.x default) is 35,112 samples per frame,
    false (the 2.x default) ends a frame at V-Blank. refstream.Core replays
    each the way it was recorded (`frame_mode`)."""
    try:
        settings = json.loads(archive.read("SyncSettings.json").decode("utf-8"))
    except KeyError:
        return "equal"
    equal = settings.get("o", settings).get("EqualLengthFrames")
    return "equal" if equal else "vblank"


def gba_cgb(archive: zipfile.ZipFile) -> bool:
    """BizHawk's GBACGB sync setting: GBA initial CPU registers and the AGB
    boot ROM. It changes the state the game starts from, so a movie recorded
    with it only replays with gambatte's GBA_FLAG."""
    try:
        settings = json.loads(archive.read("SyncSettings.json").decode("utf-8"))
    except KeyError:
        return False
    return bool(settings.get("o", settings).get("GBACGB"))


def convert(path: Path, rom: Path) -> dict[str, Any]:
    archive = open_movie(path)
    fields = header(archive)
    timeline = masks(archive)
    rom_sha1 = hashlib.sha1(rom.read_bytes()).hexdigest()
    movie_sha1 = fields.get("SHA1", "").lower()
    return {
        "schema": 1,
        "format": "tas-movie-v1",
        "frames": len(timeline),
        "frame_mode": frame_mode(archive),
        "gba_cgb": gba_cgb(archive),
        "boot_rom_sha1": fields.get("GBC_Firmware_World", "").lower() or None,
        "core": fields.get("Core"),
        "platform": fields.get("Platform"),
        "cgb_mode": fields.get("IsCGBMode"),
        "movie_rom_sha1": movie_sha1,
        "local_rom_sha1": rom_sha1,
        "rom_matches": movie_sha1 == rom_sha1,
        "author": fields.get("Author"),
        "masks": timeline,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("movie")
    parser.add_argument("--rom", default="poketcg/poketcg.gbc")
    parser.add_argument("--input-out", help="per-frame mask file for --input")
    parser.add_argument("--json")
    args = parser.parse_args(argv)
    movie = Path(args.movie)
    rom = Path(args.rom) if Path(args.rom).is_absolute() else ROOT / args.rom
    try:
        record = convert(movie, rom)
    except (MovieError, OSError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2
    if args.input_out:
        Path(args.input_out).write_text(
            ",".join(str(value) for value in record["masks"]) + "\n")
    summary = {key: value for key, value in record.items() if key != "masks"}
    if args.json:
        Path(args.json).write_text(json.dumps(record, separators=(",", ":")) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if record["rom_matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
