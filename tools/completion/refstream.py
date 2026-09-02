#!/usr/bin/env python3
"""Anchored Gambatte reference stream: per-DoFrame state, byte writers, routine trace."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import re
import struct
import sys
from bisect import bisect_right
from collections.abc import Callable
from pathlib import Path
from typing import Any, Self

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SYM_PATH = ROOT / "poketcg" / "poketcg.sym"
HARDWARE_INC = ROOT / "poketcg" / "src" / "constants" / "hardware.inc"
STREAM_ROOT = ROOT / "build" / "completion" / "refstream"
STREAM_FORMAT = "refstream-v2"

WIDTH = 160
HEIGHT = 144
SAMPLES_PER_FRAME = 35112
MAX_SLICES_PER_FRAME = 240

# DoFrame ($053F) + 4 pushes + `ld hl, wDoFrameFunction` + three calls: the
# instruction before `ld a, [wDebugPauseAllowed]`, which is where the native
# port reaches frame_boundary_reach() (src/home/frames.c). Sampling the
# reference on PPU frame boundaries instead reports ~40 bytes of wOAM
# sampling-phase noise that is not port divergence.
DOFRAME_ANCHOR = 0x0552

# gambatte_getregs fills a 10-int array; PC is index 0 and L is index 9.
REG_PC = 0

# libgambatte/include/inputgetter.h button bits, identical to hKeysHeld.
GAMBATTE_BUTTONS = {
    "A": 0x01, "B": 0x02, "SELECT": 0x04, "START": 0x08,
    "RIGHT": 0x10, "LEFT": 0x20, "UP": 0x40, "DOWN": 0x80,
}

FIELD_WINDOWS = {
    "wram": (0xC000, 0x2000),
    "hram": (0xFF80, 0x80),
    "io": (0xFF00, 0x80),
    "oam": (0xFE00, 0xA0),
    "sram_bank_0": (0xA000, 0x2000),
    "sram_bank_1": (0xA000, 0x2000),
    "sram_bank_2": (0xA000, 0x2000),
    "sram_bank_3": (0xA000, 0x2000),
    "save": (0xA000, 0x8000),
}
SRAM_FIELD_BANK = {f"sram_bank_{bank}": bank for bank in range(4)}

RECORD_DOMAINS = (
    ("wram", 0x2000),
    ("hram", 0x80),
    ("io", 0x80),
    ("oam", 0xA0),
    ("palette_ram", 0x80),
)
RECORD_STRIDE = sum(length for _, length in RECORD_DOMAINS)
RECORD_OFFSETS: dict[str, tuple[int, int]] = {}
_cursor = 0
for _name, _length in RECORD_DOMAINS:
    RECORD_OFFSETS[_name] = (_cursor, _length)
    _cursor += _length

SYM_RE = re.compile(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(\S+)$")
HARDWARE_RE = re.compile(r"^\s*def\s+(r[A-Za-z0-9_]+)\s+equ\s+\$([0-9A-Fa-f]{4})\s*$")


class RefstreamError(RuntimeError):
    pass


def load_labels(path: Path = SYM_PATH) -> list[tuple[int, int, str]]:
    if not path.is_file():
        raise RefstreamError(f"missing symbol table {path}")
    labels = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = SYM_RE.match(line.split(";")[0].strip())
        if match:
            labels.append((int(match.group(1), 16), int(match.group(2), 16), match.group(3)))
    if not labels:
        raise RefstreamError(f"{path} has no parseable labels")
    return labels


def load_hardware_registers(path: Path = HARDWARE_INC) -> dict[int, str]:
    if not path.is_file():
        return {}
    registers: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = HARDWARE_RE.match(line)
        if match:
            registers.setdefault(int(match.group(2), 16), match.group(1))
    return registers


_field_tables: dict[str, list[tuple[int, str]]] | None = None


def field_symbol_tables() -> dict[str, list[tuple[int, str]]]:
    """field -> sorted [(field_offset, symbol)] for every field with symbols."""
    global _field_tables
    if _field_tables is not None:
        return _field_tables
    labels = load_labels()
    tables: dict[str, dict[int, str]] = {field: {} for field in FIELD_WINDOWS}
    for bank, address, name in labels:
        for field, (base, length) in FIELD_WINDOWS.items():
            if not base <= address < base + min(length, 0x2000 if field == "save" else length):
                continue
            if field in SRAM_FIELD_BANK and bank != SRAM_FIELD_BANK[field]:
                continue
            offset = address - base
            if field == "save":
                offset += bank * 0x2000
            tables[field].setdefault(offset, name)
    registers = load_hardware_registers()
    io_base = FIELD_WINDOWS["io"][0]
    for address, name in registers.items():
        if io_base <= address < io_base + FIELD_WINDOWS["io"][1]:
            tables["io"].setdefault(address - io_base, name)
    _field_tables = {
        field: sorted(entries.items()) for field, entries in tables.items() if entries
    }
    return _field_tables


def resolve_region(field: str, offset: int) -> tuple[str, int]:
    """(symbol, field offset of its base) for one differing byte."""
    table = field_symbol_tables().get(field)
    base = FIELD_WINDOWS.get(field, (0, 0))[0]
    if not table:
        return f"${base + offset:04X}", offset
    index = bisect_right(table, (offset, "\uffff")) - 1
    if index < 0:
        return f"${base + offset:04X}", offset
    return table[index][1], table[index][0]


def group_by_symbol(
    field: str, offsets: list[int], *, offsets_per_region: int = 8
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, int], list[int]] = {}
    for offset in offsets:
        grouped.setdefault(resolve_region(field, offset), []).append(offset)
    base = FIELD_WINDOWS.get(field, (0, 0))[0]
    rows = [
        {
            "field": field,
            "symbol": symbol,
            "address": f"0x{base + symbol_offset:04X}",
            "field_offset": symbol_offset,
            "count": len(hits),
            "offsets": hits[:offsets_per_region],
        }
        for (symbol, symbol_offset), hits in grouped.items()
    ]
    rows.sort(key=lambda row: (-row["count"], row["field_offset"]))
    return rows


def _library() -> tuple[ctypes.CDLL, dict[str, Any]]:
    sys.path.insert(0, str(ROOT / "tools" / "completion"))
    import gambatte_runner

    pins = gambatte_runner.load_pins()
    library = gambatte_runner.configure_library(
        gambatte_runner.resolve(pins["core"]["path"])
    )
    library.gambatte_getaddrbank.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
    library.gambatte_getaddrbank.restype = ctypes.c_uint
    library.gambatte_setwritecallback.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.gambatte_newstatelen.argtypes = [ctypes.c_void_p]
    library.gambatte_newstatelen.restype = ctypes.c_int
    return library, pins


INPUT_GETTER = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_void_p)
EXEC_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.c_ulonglong)
MEMORY_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_longlong)


def native_mask_to_gambatte(mask: int) -> int:
    """scenario.boot_input JOYP nibble order -> gambatte bits, matching
    shell_hkeys_from_input (src/shell.c)."""
    return ((mask << 4) | (mask >> 4)) & 0xFF


class Core:
    def __init__(self, masks: list[int]) -> None:
        self.library, self.pins = _library()
        import gambatte_runner

        rom_path = gambatte_runner.resolve(self.pins["rom"]["path"])
        rom = rom_path.read_bytes()
        self._rom_buffer = (ctypes.c_ubyte * len(rom)).from_buffer_copy(rom)
        self.rom_size = len(rom)
        self._framebuffer = (ctypes.c_uint32 * (WIDTH * HEIGHT))()
        self._sound = (ctypes.c_int16 * ((SAMPLES_PER_FRAME + 2064) * 2))()
        self._registers = (ctypes.c_int * 10)()
        self._masks = masks
        self.frame = 0
        self.ordinal = 0
        self._user_exec: Callable[[int, int], None] | None = None
        self._keepalive: list[Any] = []
        self.core = self.library.gambatte_create()
        if not self.core:
            raise RefstreamError("gambatte_create returned null")
        if self.library.gambatte_loadbuf(self.core, self._rom_buffer, len(rom), 1 | 16 | 32) != 0:
            raise RefstreamError("gambatte_loadbuf failed")
        getter = INPUT_GETTER(self._input)
        self._keepalive.append(getter)
        self.library.gambatte_setinputgetter(
            self.core, ctypes.cast(getter, ctypes.c_void_p), None
        )
        identity = (ctypes.c_int * 32768)()
        for index in range(32768):
            identity[index] = index
        self.library.gambatte_setcgbpalette(self.core, identity)
        self._keepalive.append(identity)
        self.library.gambatte_settimemode(self.core, True)
        self.library.gambatte_settime(self.core, 0)

    def _input(self, _context: int) -> int:
        """The reference reads JOYP inside ReadJoypad, before the DoFrame
        anchor fires, so ordinal k is the mask the native port applies on the
        frame whose boundary is anchor k."""
        if 0 <= self.ordinal < len(self._masks):
            return native_mask_to_gambatte(self._masks[self.ordinal])
        return 0

    def _exec(self, address: int, cycle: int) -> None:
        if address == DOFRAME_ANCHOR:
            self.ordinal += 1
        if self._user_exec is not None:
            self._user_exec(address, cycle)

    def install_exec(self, callback: Callable[[int, int], None] | None = None) -> None:
        self._user_exec = callback
        holder = EXEC_CALLBACK(self._exec)
        self._keepalive.append(holder)
        self.library.gambatte_setexeccallback(
            self.core, ctypes.cast(holder, ctypes.c_void_p)
        )

    def on_write(self, callback: Callable[[int, int], None]) -> None:
        holder = MEMORY_CALLBACK(callback)
        self._keepalive.append(holder)
        self.library.gambatte_setwritecallback(
            self.core, ctypes.cast(holder, ctypes.c_void_p)
        )

    def step_frame(self) -> None:
        for _ in range(MAX_SLICES_PER_FRAME):
            emitted = ctypes.c_uint(SAMPLES_PER_FRAME)
            rendered = self.library.gambatte_runfor(
                self.core, self._framebuffer, WIDTH, self._sound, ctypes.byref(emitted)
            )
            if rendered >= 0:
                return
        raise RefstreamError(f"no rendered frame after {MAX_SLICES_PER_FRAME} slices")

    def run(self, frames: int, *, stop: Callable[[], bool] | None = None) -> int:
        for index in range(frames):
            self.frame = index
            if stop is not None and stop():
                return index
            self.step_frame()
        return frames

    def area(self, name: str) -> bytes:
        import gambatte_runner

        return gambatte_runner.memory_area(self.library, self.core, name)

    def hram_block(self) -> bytes:
        """gambatte's HRAM area stops at $FFFE; the native g_hram is
        $FF80-$FFFF, so IE has to come off the bus."""
        read = self.library.gambatte_cpuread
        core = self.core
        return bytes(read(core, address) for address in range(0xFF80, 0x10000))

    def io_block(self) -> bytes:
        read = self.library.gambatte_cpuread
        core = self.core
        return bytes(read(core, address) for address in range(0xFF00, 0xFF80))

    def palette_block(self) -> bytes:
        background = self.area("BG Palette RGB")
        objects = self.area("OBJ Palette RGB")
        return _pack_palette(background) + _pack_palette(objects)

    def pc(self) -> int:
        self.library.gambatte_getregs(self.core, self._registers)
        return self._registers[REG_PC] & 0xFFFF

    def bank_of(self, address: int) -> int:
        return int(self.library.gambatte_getaddrbank(self.core, address))

    def close(self) -> None:
        if self.core:
            self.library.gambatte_destroy(self.core)
            self.core = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def _pack_palette(rgb: bytes) -> bytes:
    """32 RGB32 entries -> the native g_pal 64-byte little-endian 15-bit half."""
    packed = bytearray()
    for index in range(0, min(len(rgb), 128), 4):
        red, green, blue = rgb[index + 2], rgb[index + 1], rgb[index]
        value = (red * 31 + 127) // 255 | ((green * 31 + 127) // 255) << 5 | ((blue * 31 + 127) // 255) << 10
        packed += struct.pack("<H", value)
    packed += b"\x00" * (0x40 - len(packed))
    return bytes(packed[:0x40])


def scenario_masks(scenario: str, frames: int) -> list[int]:
    sys.path.insert(0, str(ROOT / "tools" / "completion"))
    import scenario as scenario_module

    if scenario in {"boot-title", "boot-title-negative"}:
        return scenario_module.boot_input(frames)
    return [0] * frames


def stream_key(pins: dict[str, Any], masks: list[int], frames: int) -> str:
    digest = hashlib.sha256()
    digest.update(pins["rom"]["sha256"].encode())
    digest.update(pins["core"]["sha256"].encode())
    digest.update(bytes(mask & 0xFF for mask in masks))
    digest.update(struct.pack("<I", frames))
    digest.update(STREAM_FORMAT.encode())
    return digest.hexdigest()[:24]


def routine_entry_addresses() -> tuple[set[int], dict[tuple[int, int], str]]:
    """(candidate entry addresses, (bank, address) -> routine).

    An address is only that routine's entry when the mapped bank matches:
    216 entry addresses collide across banks in 16-bit space, and a hot
    address in the currently mapped bank frequently coincides with some other
    bank's routine entry. Attributing on the address alone reports duel
    routines running during the title screen."""
    from tests import routines

    names = set(routines.ALL)
    by_bank_address: dict[tuple[int, int], str] = {}
    candidates: set[int] = set()
    for bank, address, name in load_labels():
        if name not in names:
            continue
        by_bank_address[(0 if address < 0x4000 else bank, address)] = name
        candidates.add(address)
    return candidates, by_bank_address


def label_resolver() -> Callable[[int, int], tuple[str, int] | None]:
    per_bank: dict[int, list[tuple[int, str]]] = {}
    for bank, address, name in load_labels():
        per_bank.setdefault(bank, []).append((address, name))
    for entries in per_bank.values():
        entries.sort()

    def resolve(bank: int, pc: int) -> tuple[str, int] | None:
        candidates = per_bank.get(0 if pc < 0x4000 else bank, [])
        index = bisect_right(candidates, (pc, "\uffff")) - 1
        if index < 0:
            return None
        return candidates[index][1], pc - candidates[index][0]

    return resolve


def routine_of_label(label: str) -> str:
    from tests import routines

    names = set(routines.ALL)
    root = label.split(".", 1)[0]
    return root if root in names else label


def build(scenario: str, frames: int, anchors: int) -> dict[str, Any]:
    masks = scenario_masks(scenario, frames)
    with Core(masks) as core:
        key = stream_key(core.pins, masks, frames)
        directory = STREAM_ROOT / key
        meta_path = directory / "meta.json"
        if meta_path.is_file():
            existing = json.loads(meta_path.read_text())
            if existing.get("key") == key and existing.get("anchor_hits", 0) >= min(anchors, frames):
                existing["cached"] = True
                return existing
        records = bytearray()
        ordinals = bytearray()
        hits = 0

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal hits
            if address != DOFRAME_ANCHOR or hits >= anchors:
                return
            wram = core.area("WRAM")
            records.extend(wram[: RECORD_OFFSETS["wram"][1]])
            records.extend(core.hram_block())
            records.extend(core.io_block())
            records.extend(core.area("OAM")[: RECORD_OFFSETS["oam"][1]])
            records.extend(core.palette_block())
            ordinals.extend(struct.pack("<II", core.frame, wram[0xAB8]))
            hits += 1

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: hits >= anchors)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "anchors.bin").write_bytes(bytes(records))
        (directory / "ordinals.bin").write_bytes(bytes(ordinals))
        (directory / "labels.json").write_text(
            json.dumps(
                {
                    "labels": [
                        {"bank": bank, "address": address, "name": name}
                        for bank, address, name in load_labels()
                    ]
                },
                separators=(",", ":"),
            )
        )
        meta = {
            "schema": 1,
            "format": STREAM_FORMAT,
            "scenario": scenario,
            "frames": frames,
            "anchor_hits": hits,
            "key": key,
            "anchor": f"0x{DOFRAME_ANCHOR:04X}",
            "stride": RECORD_STRIDE,
            "domain_offsets": {
                name: {"offset": offset, "length": length}
                for name, (offset, length) in RECORD_OFFSETS.items()
            },
            "rom_sha256": core.pins["rom"]["sha256"],
            "core_sha256": core.pins["core"]["sha256"],
            "directory": str(directory.relative_to(ROOT)),
            "cached": False,
        }
        meta_path.write_text(json.dumps(meta, sort_keys=True, separators=(",", ":")) + "\n")
        return meta


class Stream:
    """Reader for a built stream directory, indexed by DoFrame ordinal."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.meta = json.loads((directory / "meta.json").read_text())
        self._records = (directory / "anchors.bin").read_bytes()
        self._ordinals = (directory / "ordinals.bin").read_bytes()
        self.stride = int(self.meta["stride"])
        self.count = len(self._records) // self.stride

    def domain(self, ordinal: int, name: str) -> bytes:
        if not 0 <= ordinal < self.count:
            raise IndexError(f"ordinal {ordinal} outside 0..{self.count - 1}")
        offset, length = RECORD_OFFSETS[name]
        start = ordinal * self.stride + offset
        return self._records[start : start + length]

    def ordinal_info(self, ordinal: int) -> tuple[int, int]:
        return struct.unpack_from("<II", self._ordinals, ordinal * 8)


def open_stream(scenario: str, frames: int, anchors: int) -> Stream:
    meta = build(scenario, frames, anchors)
    return Stream(ROOT / meta["directory"])


def writers(scenario: str, frames: int, addresses: list[int]) -> list[dict[str, Any]]:
    masks = scenario_masks(scenario, frames)
    resolve = label_resolver()
    watched = set(addresses)
    tally: dict[int, dict[tuple[str, int, int, int], dict[str, Any]]] = {
        address: {} for address in addresses
    }
    with Core(masks) as core:

        def on_write(address: int, _cycle: int) -> None:
            if address not in watched:
                return
            pc = core.pc()
            label = resolve(core.bank_of(pc), pc)
            name, label_offset = label if label else (f"${pc:04X}", 0)
            bank = core.bank_of(pc)
            record = tally[address].setdefault(
                (name, label_offset, pc, bank),
                {
                    "label": name,
                    "label_offset": label_offset,
                    "pc": f"0x{pc:04X}",
                    "bank": bank,
                    "routine": routine_of_label(name),
                    "count": 0,
                    "first_ordinal": core.ordinal,
                },
            )
            record["count"] += 1

        core.on_write(on_write)
        core.install_exec()
        core.run(frames)
    result = []
    for address in addresses:
        rows = sorted(tally[address].values(), key=lambda row: -row["count"])
        result.append({"address": f"0x{address:04X}", "writers": rows})
    return result


def routine_trace(
    scenario: str, frames: int, wanted: set[str] | None
) -> dict[str, Any]:
    masks = scenario_masks(scenario, frames)
    candidates, by_bank_address = routine_entry_addresses()
    events: list[tuple[int, str]] = []
    with Core(masks) as core:

        def on_exec(address: int, _cycle: int) -> None:
            if address not in candidates:
                return
            bank = 0 if address < 0x4000 else core.bank_of(address)
            name = by_bank_address.get((bank, address))
            if name is None:
                return
            if wanted is None or name in wanted:
                events.append((core.ordinal, name))

        core.install_exec(on_exec)
        core.run(frames)
    per_routine: dict[str, int] = {}
    for _ordinal, name in events:
        per_routine[name] = per_routine.get(name, 0) + 1
    return {
        "scenario": scenario,
        "frames": frames,
        "events": len(events),
        "distinct_routines": len(per_routine),
        "calls": sorted(
            ({"routine": name, "count": count} for name, count in per_routine.items()),
            key=lambda row: (-row["count"], row["routine"]),
        ),
        "first_events": [
            {"ordinal": ordinal, "routine": name} for ordinal, name in events[:16]
        ],
    }


def parse_addresses(text: str) -> list[int]:
    values = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        values.append(int(part, 16) if part.lower().startswith("0x") else int(part, 0))
    if not values:
        raise RefstreamError("no addresses given")
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    build_parser = subcommands.add_parser("build")
    build_parser.add_argument("scenario")
    build_parser.add_argument("--frames", type=int, default=2400)
    build_parser.add_argument("--anchors", type=int, default=2100)

    writers_parser = subcommands.add_parser("writers")
    writers_parser.add_argument("scenario")
    writers_parser.add_argument("--frames", type=int, default=2400)
    writers_parser.add_argument("--address", required=True)

    trace_parser = subcommands.add_parser("trace")
    trace_parser.add_argument("scenario")
    trace_parser.add_argument("--frames", type=int, default=2000)
    trace_parser.add_argument("--routines")

    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            payload: Any = build(args.scenario, args.frames, args.anchors)
        elif args.command == "writers":
            payload = writers(args.scenario, args.frames, parse_addresses(args.address))
        else:
            wanted = set(args.routines.split(",")) if args.routines else None
            payload = routine_trace(args.scenario, args.frames, wanted)
    except (RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
