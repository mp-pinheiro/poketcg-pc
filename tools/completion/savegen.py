#!/usr/bin/env python3
"""Save images for state-seeded sessions.

A session directory holding `save.sav` (the 32 KiB cartridge RAM) starts both
lanes from that save: the reference seeds CartRAM before the first instruction
and the native lane takes `--load-save`. `base` takes the image from the
reference at an ordinal of a recorded session; `edit` changes the collection,
the PC packs, the medal count and event variables against the disassembly's
own layout, then recomputes the general save data's byte count and checksum
(engine/save.asm CopyGeneralSaveDataToSRAM) and refreshes the SRAM2 backups the
game falls back to.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import effects
import session

SAVES = ROOT / "build" / "completion" / "saves"
PRET = ROOT / "poketcg" / "src"
SCRIPTING = PRET / "engine" / "overworld" / "scripting.asm"
SCRIPT_CONSTANTS = PRET / "constants" / "script_constants.asm"
BANK = 0x2000
CARD_COLLECTION = 0xA100
CARD_AND_DECK = (0xA100, 0xB708)
GENERAL = 0xB800
GENERAL_DATA = 0xB808
GENERAL_END = 0xB900
GENERAL_MAGIC = (0x08, 0x00)
MEDAL_COUNT = 0xB808
PC_PACKS = 0xB82D
NUM_PC_PACKS = 15
EVENT_VARS = 0xB87B
EVENT_MASKS = re.compile(r"^\s*event_def\s+\$([0-9a-fA-F]+),\s*%([01]{8})")
CARD_NOT_OWNED = 0x80


class SaveError(RuntimeError):
    pass


def offset(address: int, bank: int = 0) -> int:
    if not 0xA000 <= address < 0xC000:
        raise SaveError(f"0x{address:04X} is not a cartridge RAM address")
    return bank * BANK + (address - 0xA000)


def event_table() -> dict[str, tuple[int, int]]:
    """EVENT_* -> (byte offset in the event variables, bit mask)."""
    names: list[str] = []
    counting = False
    for line in SCRIPT_CONSTANTS.read_text().splitlines():
        text = line.split(";", 1)[0].strip()
        if text == "const_def":
            if names:
                break
            counting = True
        elif counting and text.startswith("const EVENT_"):
            names.append(text.split()[1])
    masks: list[tuple[int, int]] = []
    for line in SCRIPTING.read_text().splitlines():
        match = EVENT_MASKS.match(line)
        if match:
            masks.append((int(match.group(1), 16), int(match.group(2), 2)))
    if len(masks) < len(names):
        raise SaveError(f"{len(masks)} event masks for {len(names)} event names")
    return {name: masks[index] for index, name in enumerate(names)}


def general_checksum(image: bytearray, bank: int) -> tuple[int, int]:
    base = offset(GENERAL, bank)
    count = image[base + 2] | image[base + 3] << 8
    data = offset(GENERAL_DATA, bank)
    total = sum(image[data:data + count]) & 0xFFFF
    return count, total


def validate(image: bytes) -> dict[str, object]:
    working = bytearray(image)
    base = offset(GENERAL)
    count, total = general_checksum(working, 0)
    stored = working[base + 4] | working[base + 5] << 8
    return {
        "magic": (working[base], working[base + 1]) == GENERAL_MAGIC,
        "byte_count": count, "checksum": total, "stored_checksum": stored,
        "checksum_ok": total == stored,
        "medals": working[offset(MEDAL_COUNT)],
        "packs": list(working[offset(PC_PACKS):offset(PC_PACKS) + NUM_PC_PACKS]),
        "owned_cards": sum(1 for value in working[offset(CARD_COLLECTION):offset(CARD_COLLECTION) + 0x100]
                           if value and not value & CARD_NOT_OWNED),
    }


def seal(image: bytearray) -> None:
    """Recompute the general block's checksum and refresh the SRAM2 backups."""
    base = offset(GENERAL)
    count, total = general_checksum(image, 0)
    image[base], image[base + 1] = GENERAL_MAGIC
    image[base + 2], image[base + 3] = count & 0xFF, count >> 8
    image[base + 4], image[base + 5] = total & 0xFF, total >> 8
    image[offset(GENERAL, 2):offset(GENERAL_END, 2)] = image[offset(GENERAL):offset(GENERAL_END)]
    start, end = CARD_AND_DECK
    image[offset(start, 2):offset(end, 2)] = image[offset(start):offset(end)]


def base(name: str, *, source: str, at: int) -> int:
    masks, meta = session.load_session(source)
    if not 1 <= at <= len(masks):
        raise SaveError(f"--at must be within {source}'s {len(masks)} ordinals")
    frames = session.reference_frames(masks, meta)
    captured = session.reference_capture(source, masks, frames, at, meta["pokes"], sram=True, save=meta["save"])
    image = bytes(captured["sram"][:0x8000])
    SAVES.mkdir(parents=True, exist_ok=True)
    out = SAVES / f"{name}.sav"
    out.write_bytes(image)
    report = validate(image)
    print(f"SAVE {name} from={source} ordinal={at} magic={report['magic']} "
          f"checksum_ok={report['checksum_ok']} medals={report['medals']} owned_cards={report['owned_cards']} "
          f"out={out.relative_to(ROOT)}")
    return 0


def edit(path: Path, *, out: Path, cards: list[str], events: list[str], medals: int | None,
         packs: list[str], all_cards: int | None) -> int:
    image = bytearray(path.read_bytes())
    if len(image) != 0x8000:
        raise SaveError(f"{path} is {len(image)} bytes, not 32768")
    card_ids = effects.card_ids()
    if all_cards is not None:
        for card in card_ids.values():
            image[offset(CARD_COLLECTION) + card] = all_cards & 0x7F
    for spec in cards:
        card_name, _, count = spec.partition("=")
        if card_name not in card_ids or not count:
            raise SaveError(f"--card wants CARD=COUNT with a card constant, got {spec}")
        image[offset(CARD_COLLECTION) + card_ids[card_name]] = int(count, 0) & 0x7F
    if medals is not None:
        image[offset(MEDAL_COUNT)] = medals & 0xFF
    for spec in packs:
        slot, _, pack = spec.partition("=")
        if not pack or not 0 <= int(slot, 0) < NUM_PC_PACKS:
            raise SaveError(f"--pack wants SLOT=PACK with a slot in 0..{NUM_PC_PACKS - 1}, got {spec}")
        image[offset(PC_PACKS) + int(slot, 0)] = int(pack, 0) & 0xFF
    table = event_table()
    for spec in events:
        event, _, value = spec.partition("=")
        if event not in table or not value:
            raise SaveError(f"--event wants EVENT_X=VALUE with a script_constants.asm event, got {spec}")
        byte, mask = table[event]
        shift = (mask & -mask).bit_length() - 1
        cell = offset(EVENT_VARS) + byte
        image[cell] = (image[cell] & ~mask & 0xFF) | ((int(value, 0) << shift) & mask)
    seal(image)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(bytes(image))
    report = validate(bytes(image))
    print(f"SAVE {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} medals={report['medals']} "
          f"owned_cards={report['owned_cards']} packs={report['packs']} checksum_ok={report['checksum_ok']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    base_parser = sub.add_parser("base", help="take a save image from the reference at a session ordinal")
    base_parser.add_argument("name")
    base_parser.add_argument("--from", dest="source", required=True)
    base_parser.add_argument("--at", type=int, required=True)
    edit_parser = sub.add_parser("edit", help="edit a save image and reseal it")
    edit_parser.add_argument("save", type=Path)
    edit_parser.add_argument("--out", type=Path, required=True)
    edit_parser.add_argument("--card", action="append", default=[], help="CARD=COUNT")
    edit_parser.add_argument("--all-cards", type=int, help="every card's count")
    edit_parser.add_argument("--event", action="append", default=[], help="EVENT_X=VALUE")
    edit_parser.add_argument("--medals", type=int)
    edit_parser.add_argument("--pack", action="append", default=[], help="SLOT=PACK id in the PC")
    show_parser = sub.add_parser("show", help="validate a save image")
    show_parser.add_argument("save", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "base":
            return base(args.name, source=args.source, at=args.at)
        if args.command == "edit":
            return edit(args.save, out=args.out, cards=args.card, events=args.event, medals=args.medals,
                        packs=args.pack, all_cards=args.all_cards)
        print(json.dumps(validate(args.save.read_bytes()), indent=1))
        return 0
    except (SaveError, session.SessionError, effects.EffectsError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
