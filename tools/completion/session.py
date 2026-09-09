#!/usr/bin/env python3
"""Verify a session against the ROM, one DoFrame at a time.

A session is one byte of input per DoFrame, in InputFrame order (src/input.h).
It comes from one of two places:

  derive   the reference plays a frame-indexed movie (the TAS) and the byte its
           own ReadJoypad saw at every DoFrame is logged. No human, and the
           session reaches wherever the ROM reaches on that movie.
  play     `just play --record-input` logs what a human played.

Verification is the same either way. The reference replays the session on the
DoFrame axis once and caches a CRC-32 per ordinal of the masked game state
(WRAM, HRAM, OAM, VRAM); the port writes the same digest stream through
--digest-out; the first ordinal whose digests differ is exact, found in one
native run. Only then does a targeted reference capture at that ordinal name
the bytes, their RAM symbols and the routine that last wrote them.

Ordinals are 1-based on both sides: native, frame_boundary_doframe_ordinal
after the increment; reference, the count of $0552 anchor hits.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import struct
import subprocess
import sys
import tempfile
import zlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import scenario as scenario_module

SESSIONS = ROOT / "tests" / "sessions"
CACHE = ROOT / "build" / "completion" / "sessions"
RATCHET_PATH = ROOT / "tools" / "completion" / "session_ratchet.json"
NATIVE_TIMEOUT = 1800
DIGEST_FORMAT = "session-digest-v7"
# wram, hram, oam, vram, audio; then the reference's real time at the anchor
# in 2 MiHz units (emitted samples of completed slices plus the exec
# callback's in-slice offset), wVBlankCounter and wTimerCounter.
REFERENCE_RECORD = struct.Struct("<5IQBB")
NATIVE_RECORD = struct.Struct("<5I")
# One per timer sync point reached: the interval it fell in (anchors completed
# so far), its real time and wTimerCounter, which is how the port learns at
# which tick of the interval game code observed timer-ISR state. The sync
# points are every routine through which game code reaches that state: the
# home/sound.asm driver wrappers (StopMusic and PlaySFX_InvalidChoice fall
# into PlaySong/PlaySFX, so one entry each) and the play-time counter's
# readers and writers. The port calls frame_boundary_timer_sync at the same
# entries (src/home/frames.h). Keyed by (bank, address); home routines are
# bank-independent.
CALL_RECORD = struct.Struct("<IQB")
TIMER_SYNC = {
    (None, 0x377F): "SetupSound", (None, 0x3785): "PlaySong",
    (None, 0x378A): "AssertSongFinished", (None, 0x378F): "AssertSFXFinished",
    (None, 0x3796): "PlaySFX", (None, 0x379B): "PauseSong", (None, 0x37A0): "ResumeSong",
    (None, 0x383D): "ExecuteGameEvent",           # map.asm:26, enables the counter
    (3, 0x41B1): "Func_c1b1",                     # overworld.asm:230, zeroes it
    (4, 0x41CD): "PrintPlayTime",                 # print_stats.asm:115, reads it
    (4, 0x52FD): "CopyGeneralSaveDataToSRAM",     # save.asm .loop_bytes `ld a, [hli]`: saves it
}
TIMER_SYNC_ADDRESSES = {address: bank for bank, address in TIMER_SYNC}
# A sync point inside a copy loop fires once per byte; only the read of the
# play-time counter's first byte is the sync (the port syncs at that read).
TIMER_SYNC_HL = {0x52FD: 0xCAC5}
# The game's own writes to wVBlankCounter, the only places VBlank-ISR timing
# is observable mid-interval: `ld [wVBlankCounter], a` in DuelMainInterface
# (core.asm:291) and AIMakeDecision (core.asm:6255). One record per write:
# the interval, the real time, the counter before the write and the value
# written. The port calls frame_boundary_vblank_sync at the same writes.
VBLANK_SYNC = {(1, 0x427D): "DuelMainInterface", (1, 0x67EE): "AIMakeDecision"}
VBLANK_SYNC_ADDRESSES = {address: bank for bank, address in VBLANK_SYNC}
VBLANK_RECORD = struct.Struct("<IQBB")
# The first four gate `confirmed`; audio is SECTION "WRAM Audio" on its own,
# reported but not gated: the sound driver runs from the timer ISR, which the
# lag track schedules around the game's driver calls, but the reference APU
# registers it writes are hardware the port does not model byte-for-byte.
REGIONS = ("wram", "hram", "oam", "vram", "audio")
GATED = 4
REGION_LENGTHS = {"wram": 0x2000, "hram": 0x80, "oam": 0xA0, "vram": 0x4000, "audio": 0x165}
REGION_BASES = {"wram": 0xC000, "hram": 0xFF80, "oam": 0xFE00, "vram": 0x8000, "audio": 0xDD80}

# The lag track replays the ROM's own timer and VBlank ISR counts per DoFrame,
# so the play-time clock and both ISR counters are compared. The sound
# driver's SECTION "WRAM Audio" ($DD80-$DEE4, wram.asm:2992-3289) is carved
# out of the gated wram digest and digested as the ungated `audio` region: its
# ISR *count* per DoFrame is exact, but the port batches those ticks at the
# frame boundary while the ROM interleaves them with game code, so a sound
# requested between two ticks starts one update apart. Reported, not gated.
TIMING_PHASE: dict[str, list[tuple[int, int]]] = {"wram": [(0xDD80 - 0xC000, 0xDEE5 - 0xC000)]}
# Ledger entries whose justification is the frame axis, compared on this one:
#   hram $FF8D hDPadRepeat   -- HandleDPadRepeat runs once per anchor on both lanes
#   wram $CAB8 wVBlankCounter, $CAC3 wTimerCounter -- ISR counts replayed exactly
#   wram $CABA-$CABC wRNG1/wRNG2/wRNGCounter -- a software LFSR advanced by game
#     code only (random.asm), so with the same DoFrames and input it must match;
#     every shuffle and coin flip rides on it
#   wram $CAC0-$CAC1 wVBlankOAMCopyToggle -- consumed by the same ISR count
COMPARE_DESPITE_LEDGER = {"hram": [(0x0D, 0x0E)],
                          "wram": [(0xAB8, 0xAB9), (0xABA, 0xABD), (0xAC0, 0xAC2), (0xAC3, 0xAC4)]}


class SessionError(RuntimeError):
    pass


def session_dir(name: str) -> Path:
    return SESSIONS / name


def load_session(name: str) -> tuple[list[int], dict[str, Any]]:
    directory = session_dir(name)
    input_path = directory / "input.txt"
    meta_path = directory / "session.json"
    if not input_path.is_file():
        raise SessionError(f"no session input at {input_path.relative_to(ROOT)}")
    masks = refstream.load_masks(input_path)
    meta = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
    pokes_path = directory / "pokes.txt"
    meta["pokes"] = refstream.load_pokes(pokes_path) if pokes_path.is_file() else {}
    return masks, meta


def reference_frames(masks: list[int], meta: dict[str, Any]) -> int:
    """PPU frames to give the reference. A derived session knows its movie's
    length; a recording gets twice its DoFrames, DoFrames being the sparser
    axis (refstream.py: 78,207 movie frames hold 55,080 DoFrames)."""
    return int(meta.get("reference_frames") or len(masks) * 2 + 400)


def read_ratchet() -> dict[str, dict[str, int]]:
    if not RATCHET_PATH.is_file():
        return {}
    return json.loads(RATCHET_PATH.read_text())


def write_ratchet(ratchet: dict[str, dict[str, int]]) -> None:
    RATCHET_PATH.write_text(json.dumps(ratchet, indent=2, sort_keys=True) + "\n")


def mask_ranges() -> dict[str, list[tuple[int, int]]]:
    ranges: dict[str, list[tuple[int, int]]] = {region: [] for region in REGIONS}
    for region in ("wram", "hram", "oam"):
        ranges[region] += [tuple(r) for r in scenario_module.COMPARATOR_EXCLUDED_RANGES.get(region, ())]
    for region, extra in TIMING_PHASE.items():
        ranges[region] += extra
    for region, keep in COMPARE_DESPITE_LEDGER.items():
        table = bytearray(REGION_LENGTHS[region])
        for start, end in ranges[region]:
            for index in range(max(0, start), min(len(table), end)):
                table[index] = 1
        for start, end in keep:
            for index in range(max(0, start), min(len(table), end)):
                table[index] = 0
        ranges[region] = runs(table)
    return ranges


def runs(table: bytearray) -> list[tuple[int, int]]:
    out = []
    start = None
    for index, flag in enumerate(table):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            out.append((start, index))
            start = None
    if start is not None:
        out.append((start, len(table)))
    return out


def mask_text() -> str:
    lines = ["# masked before digesting, on both lanes; regenerated by session.py"]
    for region, spans in mask_ranges().items():
        for start, end in spans:
            lines.append(f"{region} 0x{start:04X} 0x{end:04X}")
    return "\n".join(lines) + "\n"


def mask_tables() -> dict[str, bytes]:
    tables = {}
    for region, spans in mask_ranges().items():
        table = bytearray(REGION_LENGTHS[region])
        for start, end in spans:
            for index in range(max(0, start), min(len(table), end)):
                table[index] = 1
        tables[region] = bytes(table)
    return tables


def masked(data: bytes, table: bytes) -> bytes:
    if not any(table):
        return data
    out = bytearray(data)
    for index, flag in enumerate(table):
        if flag:
            out[index] = 0
    return bytes(out)


def reference_regions(core: refstream.Core) -> dict[str, bytes]:
    wram = core.area("WRAM")[:0x2000]
    return {
        "wram": wram,
        "hram": core.hram_block(),
        "oam": core.area("OAM")[:0xA0],
        "vram": core.area("VRAM")[:0x4000],
        "audio": wram[0x1D80:0x1EE5],
    }


def native_regions(dump: dict[str, Any]) -> dict[str, bytes]:
    wram = bytes(dump["wram"])
    return {
        "wram": wram,
        "hram": bytes(dump["hram"]),
        "oam": bytes(dump["oam"]),
        "vram": bytes(dump["vram_bank_0"]) + bytes(dump["vram_bank_1"]),
        "audio": wram[0x1D80:0x1EE5],
    }


def digest(regions: dict[str, bytes], tables: dict[str, bytes]) -> tuple[int, ...]:
    return tuple(zlib.crc32(masked(regions[r], tables[r])) & 0xFFFFFFFF for r in REGIONS)


def stream_key(masks: list[int], frames: int, axis: str, pokes: refstream.Pokes | None = None) -> str:
    import gambatte_runner

    pins = gambatte_runner.load_pins()
    h = hashlib.sha256()
    h.update(DIGEST_FORMAT.encode())
    h.update(axis.encode())
    h.update(struct.pack("<I", frames))
    h.update(bytes(m & 0xFF for m in masks))
    h.update(refstream.pokes_text(pokes).encode())
    h.update(mask_text().encode())
    # The lag track in the stream directory is shaped by the sync points, so
    # a change to them rebuilds the reference rather than replaying against
    # a schedule the port no longer follows.
    h.update(repr(sorted(TIMER_SYNC.items(), key=repr)).encode())
    h.update(repr(sorted(TIMER_SYNC_HL.items())).encode())
    h.update(repr(sorted(VBLANK_SYNC.items())).encode())
    h.update(pins["rom"]["sha256"].encode())
    h.update(pins["core"]["sha256"].encode())
    h.update(str(pins["boot"].get("sha1", pins["boot"]["mode"])).encode())
    return h.hexdigest()[:24]


def build_reference(name: str, masks: list[int], frames: int, *, axis: str = "ordinal",
                    record_input: bool = False, frame_mode: str = "vblank", gba: bool = False,
                    pokes: refstream.Pokes | None = None) -> dict[str, Any]:
    """One reference replay: a digest record per DoFrame anchor, cached by
    input. With `record_input` the byte ReadJoypad saw at each anchor is
    returned as well, in InputFrame order, which is how a movie becomes a
    session."""
    profile = axis if frame_mode == "vblank" else f"{axis}:{frame_mode}"
    if gba:
        profile += ":gba"
    key = stream_key(masks, frames, profile, pokes)
    directory = CACHE / name / key
    meta_path = directory / "meta.json"
    if meta_path.is_file() and not record_input:
        meta = json.loads(meta_path.read_text())
        if meta.get("format") == DIGEST_FORMAT:
            meta["cached"] = True
            return meta
    tables = mask_tables()
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    records = bytearray()
    calls = bytearray()
    vblank_writes = bytearray()
    inputs = bytearray()
    with refstream.Core(padded, gba=gba, pokes=pokes) as core:
        core.input_axis = axis
        core.frame_mode = frame_mode
        read = core.library.gambatte_cpuread
        registers = (ctypes.c_int * 10)()
        hits = 0

        def on_exec(address: int, cycle: int) -> None:
            nonlocal hits
            if address in TIMER_SYNC_ADDRESSES:
                bank = TIMER_SYNC_ADDRESSES[address]
                if bank is None or core.bank_of(address) == bank:
                    wanted_hl = TIMER_SYNC_HL.get(address)
                    if wanted_hl is not None:
                        core.library.gambatte_getregs(core.core, registers)
                        if (((registers[8] & 0xFF) << 8) | (registers[9] & 0xFF)) != wanted_hl:
                            return
                    calls.extend(CALL_RECORD.pack(hits, core.samples + cycle, read(core.core, 0xCAC3)))
                return
            if address in VBLANK_SYNC_ADDRESSES:
                if core.bank_of(address) == VBLANK_SYNC_ADDRESSES[address]:
                    core.library.gambatte_getregs(core.core, registers)
                    vblank_writes.extend(VBLANK_RECORD.pack(hits, core.samples + cycle,
                                                            read(core.core, 0xCAB8), registers[2] & 0xFF))
                return
            if address != refstream.DOFRAME_ANCHOR:
                return
            hits += 1
            regions = reference_regions(core)
            crcs = digest(regions, tables)
            records.extend(REFERENCE_RECORD.pack(*crcs, core.samples + cycle, regions["wram"][0xAB8],
                                                 regions["wram"][0xAC3]))
            if record_input:
                held = read(core.core, 0xFF90)
                inputs.append(((held << 4) | (held >> 4)) & 0xFF)

        core.install_exec(on_exec)
        directory.mkdir(parents=True, exist_ok=True)
        for stale in directory.glob("checkpoint-*"):
            stale.unlink()
        core.checkpoint_dir = directory
        core.run(frames)
    (directory / "digests.bin").write_bytes(bytes(records))
    (directory / "calls.bin").write_bytes(bytes(calls))
    (directory / "vblank-writes.bin").write_bytes(bytes(vblank_writes))
    (directory / "lag.txt").write_text(lag_track(bytes(records), bytes(calls), bytes(vblank_writes)))
    meta = {
        "schema": 1, "format": DIGEST_FORMAT, "name": name, "axis": axis, "key": key,
        "frames": frames, "anchors": hits, "record": REFERENCE_RECORD.size,
        "directory": str(directory.relative_to(ROOT)), "cached": False,
    }
    if record_input:
        meta["inputs"] = list(inputs)
    meta_path.write_text(json.dumps({k: v for k, v in meta.items() if k != "inputs"},
                                    sort_keys=True) + "\n")
    return meta


def load_reference(meta: dict[str, Any]) -> bytes:
    return (ROOT / meta["directory"] / "digests.bin").read_bytes()


TICK_CYCLES = 17408  # SetupTimer: TAC_16KHZ with TMA=-68 (time.asm:69-85)
TICK_TIME = TICK_CYCLES // 2  # in the record's 2 MiHz units


def unwrap(delta_mod: int, expected: float, modulus: int = 256) -> int:
    """The byte counter's delta closest to the cycle-derived expectation."""
    base = delta_mod % modulus
    candidates = [base + modulus * m for m in range(-1, 4)]
    return max(0, min(candidates, key=lambda c: abs(c - expected)))


def lag_track(records: bytes, calls: bytes = b"", vblank_writes: bytes = b"") -> str:
    """One line per DoFrame: `<cycles> <timer ISRs> <VBlank ISRs>` the ROM
    spent between the previous anchor and this one, then one number per
    timer sync point reached in that interval: the timer ISRs that had fired
    before it; then, after a `v`, one number per game write to wVBlankCounter
    in the interval: the VBlank ISRs that had fired before it. The port
    replays the schedule (src/runtime.c timer_sync, vblank_sync): the ISR
    counts come from the ROM's own wTimerCounter and wVBlankCounter, unwrapped
    by the real time and followed through the game's own resets of the VBlank
    counter, so the port's interrupt handlers run exactly as often as the
    ROM's did and the game observes each count at the same point.
    Line 1 carries the boot's absolute counts."""
    count = len(records) // REFERENCE_RECORD.size
    by_interval: dict[int, list[tuple[int, int]]] = {}
    for index in range(len(calls) // CALL_RECORD.size):
        interval, time, counter = CALL_RECORD.unpack_from(calls, index * CALL_RECORD.size)
        by_interval.setdefault(interval, []).append((time, counter))
    writes_by_interval: dict[int, list[tuple[int, int, int]]] = {}
    for index in range(len(vblank_writes) // VBLANK_RECORD.size):
        interval, time, before, written = VBLANK_RECORD.unpack_from(vblank_writes, index * VBLANK_RECORD.size)
        writes_by_interval.setdefault(interval, []).append((time, before, written))
    lines = []
    prev = (0, 0, 0)  # time, vblanks, ticks at the interval's start
    for index in range(count):
        row = REFERENCE_RECORD.unpack_from(records, index * REFERENCE_RECORD.size)
        time, vblanks, ticks = row[5], row[6], row[7]
        cycles = 2 * (time - prev[0])
        if index == 0:
            dt, dv = ticks, vblanks
            offsets_v: list[int] = []
        else:
            dt = unwrap(ticks - prev[2], cycles / TICK_CYCLES)
            # VBlank ISRs, segment by segment between the game's own writes.
            dv = 0
            offsets_v = []
            cursor_time, cursor_value = prev[0], prev[1]
            for write_time, before, written in writes_by_interval.get(index, ()):
                dv += unwrap(before - cursor_value, 2 * (write_time - cursor_time) / 70224)
                offsets_v.append(dv)
                cursor_time, cursor_value = write_time, written
            dv += unwrap(vblanks - cursor_value, 2 * (time - cursor_time) / 70224)
        offsets = [
            min(dt, unwrap(counter - prev[2], (call_time - prev[0]) / TICK_TIME))
            for call_time, counter in by_interval.get(index, ())
        ]
        fields = [max(1, cycles), dt, dv, *offsets]
        if offsets_v:
            fields += ["v", *offsets_v]
        lines.append(" ".join(str(n) for n in fields))
        prev = (time, vblanks, ticks)
    return "\n".join(lines) + "\n"


def run_native(directory: Path, input_path: Path, n: int, *, lag_path: Path,
               digest_out: Path | None = None, mask_path: Path | None = None,
               dump_ordinals: list[int] | None = None) -> tuple[Path, str]:
    state_path = directory / "state.json"
    command = [
        str(scenario_module.BINARY), "--headless",
        "--data-pack", str(scenario_module.PACK),
        "--frames", "0",
        "--stop-ordinal", str(n),
        "--input-ordinal", str(input_path),
        "--lag-track", str(lag_path),
        "--dump-state", str(state_path),
    ]
    pokes_path = input_path.with_name("pokes.txt")
    if pokes_path.is_file():
        command += ["--poke-ordinal", str(pokes_path)]
    if digest_out:
        command += ["--digest-out", str(digest_out)]
        if mask_path:
            command += ["--digest-mask", str(mask_path)]
    if dump_ordinals:
        command += ["--dump-state-ordinals", ",".join(str(v) for v in dump_ordinals)]
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                timeout=NATIVE_TIMEOUT, check=False)
    except subprocess.TimeoutExpired as exc:
        text = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else str(exc.stderr or "")
        return state_path, f"HANG no exit within {NATIVE_TIMEOUT}s\n{text}"
    if result.returncode != 0:
        return state_path, result.stderr.strip()[-2000:] or f"exit {result.returncode}"
    return state_path, ""


def first_divergence(reference: bytes, native: bytes) -> tuple[int | None, int, list[str], int | None]:
    """(first gated divergent ordinal, native ordinals, gated regions that
    differ there, first ordinal the ungated audio region differs)."""
    ref_count = len(reference) // REFERENCE_RECORD.size
    nat_count = len(native) // NATIVE_RECORD.size
    audio_first = None
    for index in range(min(ref_count, nat_count)):
        ref = REFERENCE_RECORD.unpack_from(reference, index * REFERENCE_RECORD.size)
        nat = NATIVE_RECORD.unpack_from(native, index * NATIVE_RECORD.size)
        if audio_first is None and ref[GATED] != nat[GATED]:
            audio_first = index + 1
        if ref[:GATED] != nat[:GATED]:
            return index + 1, nat_count, [REGIONS[i] for i in range(GATED) if ref[i] != nat[i]], audio_first
    return None, nat_count, [], audio_first


def checkpoint_directory(name: str, masks: list[int], frames: int,
                         pokes: refstream.Pokes | None) -> Path:
    """The cached stream's directory, where the build left its savestates. A
    stream built before savestates existed gets them from one replay here."""
    directory = ROOT / build_reference(name, masks, frames, pokes=pokes)["directory"]
    if not any(directory.glob("checkpoint-*.bin")):
        padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
        with refstream.Core(padded, pokes=pokes) as core:
            core.input_axis = "ordinal"
            core.install_exec(None)
            core.checkpoint_dir = directory
            core.run(frames, stop=lambda: core.ordinal >= len(masks))
    return directory


def reference_capture(name: str, masks: list[int], frames: int, ordinal: int,
                      pokes: refstream.Pokes | None = None, *, sram: bool = False) -> dict[str, bytes]:
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    captured: dict[str, bytes] = {}
    with refstream.Core(padded, pokes=pokes) as core:
        core.input_axis = "ordinal"
        hits = core.seek(checkpoint_directory(name, masks, frames, pokes), ordinal)

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal hits
            if address != refstream.DOFRAME_ANCHOR:
                return
            hits += 1
            if hits == ordinal:
                captured.update(reference_regions(core))
                if sram:
                    captured["sram"] = core.area("CartRAM")

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: hits >= ordinal)
    if not captured:
        raise SessionError(f"reference never reached ordinal {ordinal}")
    return captured


FIXTURES = ROOT / "tests" / "fixtures"


# Interrupt-context and driver routines: entered from the timer or serial ISR
# with the driver mid-note, so a standalone call from a live state never
# returns (Music1_note wedged PyBoy for its whole wall budget). The audio digest
# compares the driver's effect per anchor instead.
SWEEP_SKIP_PREFIXES = ("Music", "Sound", "SFX", "Sfx", "Audio", "Timer", "Serial", "VBlank",
                       "Func_fc26c", "PlaySong", "PlaySFX", "PauseSong", "ResumeSong")
SWEEP_BUDGETS = {"instruction_budget": 10_000_000, "cycle_budget": 40_000_000}


def sweep_entries(name: str, *, after: int, until: int | None, limit: int) -> tuple[list[dict[str, Any]], int]:
    """One reference replay: the first entry (registers, SP, WRAM, HRAM, VRAM
    bank 0) of every ported, comparable routine in the session window."""
    sys.path.insert(0, str(ROOT / "tests"))
    sys.path.insert(0, str(ROOT))
    import test_leaves  # noqa: E402
    cases, contracts = test_leaves.load_cases()
    special = {fn for fn, rows in cases.items()
               if any(row.get("_completion", {}).get("mode", "return") != "return"
                      or not row.get("oracle", True)
                      or row.get("stack") or row.get("post_call_byte") is not None
                      or (isinstance(row.get("keys"), list) and len(row["keys"]) > 1) for row in rows)}
    setups = {fn: rows[0]["setup"] for fn, rows in cases.items() if rows and rows[0].get("setup")}
    masks, meta = load_session(name)
    frames = reference_frames(masks, meta)
    until = until or len(masks)
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    candidates, by_bank_address = refstream.routine_entry_addresses()
    entries: dict[str, dict[str, Any]] = {}
    with refstream.Core(padded, pokes=meta["pokes"]) as core:
        core.input_axis = "ordinal"
        if after > 0:
            core.seek(checkpoint_directory(name, masks, frames, meta["pokes"]), after)
        registers = (ctypes.c_int * 10)()

        def on_exec(address: int, _cycle: int) -> None:
            if address not in candidates or core.ordinal < after:
                return
            bank = 0 if address < 0x4000 else core.bank_of(address)
            label = by_bank_address.get((bank, address))
            if (label is None or label in entries or label not in contracts or label in special
                    or label.startswith(SWEEP_SKIP_PREFIXES)):
                return
            core.library.gambatte_getregs(core.core, registers)
            regions = reference_regions(core)
            entries[label] = {
                "session": name, "ordinal": core.ordinal, "entry": label, "bank": bank,
                "fields": list(contracts[label]), "setup": setups.get(label),
                "regs": {"a": registers[2] & 0xFF, "b": registers[3] & 0xFF, "c": registers[4] & 0xFF,
                         "d": registers[5] & 0xFF, "e": registers[6] & 0xFF, "f": registers[7] & 0xF0,
                         "hl": ((registers[8] & 0xFF) << 8) | (registers[9] & 0xFF)},
                "sp": registers[1] & 0xFFFF,
                "wram": regions["wram"].hex(), "hram": regions["hram"].hex(),
                "vram0": regions["vram"][:0x2000].hex(),
            }

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: core.ordinal >= until or (limit and len(entries) >= limit))
    return sorted(entries.values(), key=lambda e: e["ordinal"]), until


def sweep_worker(entries_path: Path, start: int, out_path: Path) -> int:
    """Oracle-diff entries[start:] in this process, one JSON line each,
    flushed as it goes: a routine that wedges PyBoy takes the process with it,
    and the parent reads how far it got."""
    import importlib
    sys.path.insert(0, str(ROOT / "tests"))
    sys.path.insert(0, str(ROOT))
    import test_leaves  # noqa: E402
    from pyboy_oracle import Oracle  # noqa: E402
    fixtures = importlib.import_module("tests.cases._fixtures")
    entries = json.loads(entries_path.read_text())
    rom = os.environ.get("POKETCG_ROM", str(ROOT / "poketcg" / "poketcg.gbc"))
    os.environ.setdefault("POKETCG_ROM", rom)
    probe = scenario_module.BINARY.with_name("poketcg_probe")
    with Oracle(rom) as oracle, out_path.open("a") as out:
        for index in range(start, len(entries)):
            entry = entries[index]
            label = entry["entry"]
            fixture = fixtures.Fixture.from_capture(entry)
            case = dict(fixture.case(bank=entry["bank"] or None), **entry["regs"], **SWEEP_BUDGETS)
            if entry.get("setup"):
                case["setup"] = entry["setup"]
            try:
                bad = test_leaves.direct_case(oracle, probe, label, tuple(entry["fields"]), case, auto_observe=True)
                status = "fail" if bad else "ok"
            except Exception as exc:  # noqa: BLE001 - a lane that could not run is a row, not a crash
                bad = [f"{type(exc).__name__}: {str(exc)[:160]}"]
                status = "error"
            # A memory mismatch is game state the port computed differently; a
            # register-only one is an exit value no caller may read. Rank them.
            memory = any(m.lstrip().startswith(("$", "vram", "sram")) for m in bad)
            out.write(json.dumps({"index": index, "ordinal": entry["ordinal"], "routine": label,
                                  "bank": entry["bank"], "status": status, "memory": memory,
                                  "mismatches": bad[:12]}) + "\n")
            out.flush()
    return 0


def sweep(name: str, *, after: int = 0, until: int | None = None, limit: int = 0,
          json_path: Path | None = None) -> int:
    """Every ported routine the reference enters in a session, oracle-diffed at
    its first entry there, in one pass and without a model in the loop.

    The verify loop finds one divergence per iteration: the first byte the
    native trajectory gets wrong. A sweep asks a different question of the same
    recording -- for each routine the ROM ran, does the port run it the same
    from that live state? -- so it also reaches routines the native trajectory
    never got to, and a divergence deep in a duel turn is named directly rather
    than through the scratch bytes the loop reports first. The reference is
    replayed once (from its checkpoints), each entry becomes a fixture case in
    memory, `tests/test_leaves.direct_case` widens the observation to every
    byte the reference wrote (auto-observe), and rows come out in session
    order. Routines whose committed cases need long `keys` timelines or a
    completion override are skipped: their entries are not comparable from a
    bare seed. The oracle runs in worker processes so a wedged PyBoy frame
    costs one routine, marked `wedged`, not the sweep. Runs under the oracle
    environment (`just session-sweep`)."""
    entries, until = sweep_entries(name, after=after, until=until, limit=limit)
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix=f"sweep-{name}-") as tmp:
        entries_path = Path(tmp) / "entries.json"
        entries_path.write_text(json.dumps(entries))
        results_path = Path(tmp) / "results.jsonl"
        start = 0
        env = dict(os.environ, POKETCG_ORACLE_WALL_FLOOR=os.environ.get("POKETCG_ORACLE_WALL_FLOOR", "30"))
        while start < len(entries):
            results_path.write_text("")
            proc = subprocess.run([sys.executable, __file__, "sweep-worker", str(entries_path),
                                   "--start", str(start), "--out", str(results_path)],
                                  cwd=ROOT, env=env, capture_output=True, text=True)
            done = [json.loads(line) for line in results_path.read_text().splitlines() if line.strip()]
            rows.extend(done)
            next_index = done[-1]["index"] + 1 if done else start
            if proc.returncode != 0 or next_index < len(entries) and not done and next_index == start:
                if next_index < len(entries):
                    entry = entries[next_index]
                    rows.append({"index": next_index, "ordinal": entry["ordinal"], "routine": entry["entry"],
                                 "bank": entry["bank"], "status": "wedged",
                                 "mismatches": [(proc.stderr or "").strip().splitlines()[-1][:160]
                                                if proc.stderr else "worker died"]})
                    next_index += 1
            if next_index <= start:
                break
            start = next_index
    rows.sort(key=lambda r: (not r.get("memory", False), r["ordinal"]))
    failing = sum(r["status"] == "fail" for r in rows)
    for row in rows:
        if row["status"] != "ok":
            kind = "memory" if row.get("memory") else "registers"
            print(f"ROW ordinal={row['ordinal']} routine={row['routine']} status={row['status']} {kind} "
                  + " | ".join(m[:100] for m in row["mismatches"][:3]))
    print(f"SWEEP {name} after={after} until={until} routines={len(rows)} failing={failing} "
          f"errors={sum(r['status'] == 'error' for r in rows)} wedged={sum(r['status'] == 'wedged' for r in rows)}")
    report = {"schema": 1, "format": "session-sweep-v1", "name": name, "after": after, "until": until, "rows": rows}
    # One tracker copy per window, so a bounded re-sweep refreshes the routines
    # it entered without forgetting the rows of the full sweep.
    for path in (json_path, TRACKER_DIR / f"sweep-{name}-{after}-{until if until is not None else 'end'}.json"):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(report, indent=1))
    return 0 if failing == 0 else 1


def capture(name: str, routine: str, *, after: int = 0, nth: int = 1, out: Path | None = None,
            sram: bool = False) -> int:
    """The reference's live state at `routine`'s `nth` entry (at or after DoFrame
    `after`) while it replays session `name`, written as a case fixture
    (tests/cases/_fixtures.py): registers, SP, WRAM, HRAM and VRAM bank 0.
    The printed return chain names the caller, so a routine the turn enters
    from several places can be captured at the wanted one."""
    masks, meta = load_session(name)
    frames = len(masks) * 2 + 400
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    candidates, by_bank_address = refstream.routine_entry_addresses()
    targets = {address for (bank, address), label in by_bank_address.items() if label == routine}
    if not targets:
        raise SessionError(f"{routine} is not a ported routine with a symbol")
    banks = {address: bank for (bank, address), label in by_bank_address.items() if label == routine}
    captured: dict[str, Any] = {}
    entries = 0
    with refstream.Core(padded, pokes=meta["pokes"]) as core:
        core.input_axis = "ordinal"
        if after > 0:
            core.seek(checkpoint_directory(name, masks, frames, meta["pokes"]), after)
        read = core.library.gambatte_cpuread
        registers = (ctypes.c_int * 10)()

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal entries
            if captured or address not in targets or core.ordinal < after:
                return
            bank = 0 if address < 0x4000 else core.bank_of(address)
            if bank != banks[address]:
                return
            entries += 1
            if entries < nth:
                return
            core.library.gambatte_getregs(core.core, registers)
            regions = reference_regions(core)
            captured.update({
                "session": name, "ordinal": core.ordinal, "entry": routine,
                "regs": {"a": registers[2] & 0xFF, "b": registers[3] & 0xFF, "c": registers[4] & 0xFF,
                         "d": registers[5] & 0xFF, "e": registers[6] & 0xFF, "f": registers[7] & 0xF0,
                         "hl": ((registers[8] & 0xFF) << 8) | (registers[9] & 0xFF)},
                "sp": registers[1] & 0xFFFF,
                "wram": regions["wram"].hex(), "hram": regions["hram"].hex(),
                "vram0": regions["vram"][:0x2000].hex(),
                "rom_bank": core.bank_of(0x4000),
            })
            if sram:
                captured["sram"] = core.area("CartRAM").hex()

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: bool(captured))
    if not captured:
        raise SessionError(f"{routine} entry {nth} was never reached in session {name} after ordinal {after} "
                           f"({entries} entries)")
    path = out or FIXTURES / f"{name}-{routine}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(captured))
    regs = captured["regs"]
    wram = bytes.fromhex(captured["wram"])
    sp = captured["sp"]
    chain = [wram[sp - 0xC000 + i] | (wram[sp - 0xC000 + i + 1] << 8) for i in range(0, 8, 2)
             if 0xC000 <= sp + i + 1 < 0xE000]
    print(f"FIXTURE {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path} ordinal={captured['ordinal']} "
          f"a={regs['a']:02x} f={regs['f']:02x} bc={regs['b']:02x}{regs['c']:02x} de={regs['d']:02x}{regs['e']:02x} "
          f"hl={regs['hl']:04x} sp={sp:04x} stack={' '.join(f'{v:04x}' for v in chain)}")
    return 0


def lag_between(reference: bytes, ordinal: int) -> dict[str, int]:
    """Reference PPU frames and VBlanks between anchors ordinal-1 and ordinal.
    More than one PPU frame is a lag frame the port has to model as a service
    pass (frame_boundary_consume_services) at whatever the game was doing."""
    this = REFERENCE_RECORD.unpack_from(reference, (ordinal - 1) * REFERENCE_RECORD.size)
    if ordinal < 2:
        return {"frames": round(2 * this[5] / 70224, 2), "vblanks": this[6]}
    prev = REFERENCE_RECORD.unpack_from(reference, (ordinal - 2) * REFERENCE_RECORD.size)
    return {"frames": round(2 * (this[5] - prev[5]) / 70224, 2), "vblanks": (this[6] - prev[6]) & 0xFF}


def region_field(region: str, offset: int) -> tuple[str, int]:
    if region == "vram":
        return ("vram_bank_1", offset - 0x2000) if offset >= 0x2000 else ("vram_bank_0", offset)
    return region, offset


def attribute(name: str, masks: list[int], frames: int, ordinal: int,
              native: dict[str, bytes], reference: dict[str, bytes],
              pokes: refstream.Pokes | None = None) -> list[dict[str, Any]]:
    tables = mask_tables()
    picked: list[tuple[str, int, int, int, str]] = []
    seen: set[str] = set()
    for region in REGIONS[:GATED]:
        table = tables[region]
        nat, ref = native[region], reference[region]
        for offset in range(min(len(nat), len(ref))):
            if table[offset] or nat[offset] == ref[offset]:
                continue
            field, field_offset = region_field(region, offset)
            symbol, _base = refstream.resolve_region(field, field_offset)
            if symbol in seen:
                continue
            seen.add(symbol)
            picked.append((field, field_offset, nat[offset], ref[offset], symbol))
    picked = picked[:16]
    addresses = sorted({refstream.FIELD_WINDOWS[f][0] + o for f, o, _n, _r, _s in picked})
    # The last writer before the divergence is almost always inside the
    # preceding stride, so watch the tail from a checkpoint first and fall
    # back to a boot replay only for a byte nothing in that tail wrote.
    writers: dict[int, Any] = {}
    if addresses:
        checkpoints = checkpoint_directory(name, masks, frames, pokes)
        writers = {
            int(entry["address"], 16): entry
            for entry in refstream.writers(f"session:{name}", frames, addresses, events=True,
                                           masks=masks, axis="ordinal", ordinals=ordinal, pokes=pokes,
                                           checkpoints=checkpoints, window=refstream.Core.CHECKPOINT_STRIDE)
        }
        unwritten = [a for a in addresses if refstream.writer_before(writers.get(a), ordinal) is None]
        if unwritten:
            for entry in refstream.writers(f"session:{name}", frames, unwritten, events=True,
                                           masks=masks, axis="ordinal", ordinals=ordinal, pokes=pokes):
                writers[int(entry["address"], 16)] = entry
    out = []
    for field, offset, got, want, symbol in picked:
        address = refstream.FIELD_WINDOWS[field][0] + offset
        entry = writers.get(address)
        # A write during DoFrame K carries core.ordinal K-1 (the anchor for K
        # has not fired yet), so "before ordinal K" is exactly the set whose
        # last element produced the value the reference holds at anchor K.
        prior = refstream.writer_before(entry, ordinal) if entry else None
        out.append({
            "field": field, "offset": offset, "address": f"0x{address:04X}",
            "symbol": symbol, "native": got, "reference": want,
            "writer": prior["routine"] if prior else "",
            "writer_label": prior["label"] if prior else "",
        })
    return out


def verify(name: str, *, write: bool, json_path: Path | None) -> int:
    masks, meta = load_session(name)
    n = len(masks)
    frames = reference_frames(masks, meta)
    report: dict[str, Any] = {"schema": 2, "format": "session-verify-v2", "name": name,
                              "ordinals": n, "goal": meta.get("goal", "")}
    pokes = meta["pokes"]
    ref_meta = build_reference(name, masks, frames, pokes=pokes)
    reference = load_reference(ref_meta)
    ref_count = len(reference) // REFERENCE_RECORD.size
    if ref_count < n:
        report.update(status="ref-short", confirmed=0, reference_ordinals=ref_count)
        print(f"SESSION {name} status=ref-short confirmed=0 ordinals={n} reference={ref_count}")
        emit(report, json_path)
        return 4
    with tempfile.TemporaryDirectory(prefix=f"session-{name}-") as tmp:
        directory = Path(tmp)
        mask_path = directory / "mask.txt"
        mask_path.write_text(mask_text())
        digest_path = directory / "native.bin"
        lag_path = ROOT / ref_meta["directory"] / "lag.txt"
        _state, failure = run_native(directory, session_dir(name) / "input.txt", n,
                                     lag_path=lag_path, digest_out=digest_path, mask_path=mask_path)
        native = digest_path.read_bytes() if digest_path.is_file() else b""
        ordinal, reached, regions, audio_first = first_divergence(reference, native)
        # A session may declare a ceiling: the last ordinal the ROM's own
        # route is defined C code. tas-5530s takes the Duel Escape glitch at
        # 48438 (an out-of-table jump into attack animation data, executed as
        # instructions); no port follows arbitrary code execution, so the
        # session is clean once it matches through the ceiling.
        ceiling = meta.get("ceiling")
        if ceiling is not None and (ordinal is None or ordinal > ceiling) and reached >= ceiling:
            status, confirmed = "clean", ceiling
            if ordinal is not None:
                print(f"CEILING {name} ordinal={ceiling}: {meta.get('ceiling_reason', '')}")
                ordinal = None
        elif ordinal is None and reached < n:
            status, confirmed = "native-short", reached
        elif ordinal is None:
            status, confirmed = "clean", n
        else:
            status, confirmed = "diverged", ordinal - 1
        report.update(status=status, confirmed=confirmed, reached=reached, native_failure=failure,
                      reference=ref_meta["directory"], audio_first_divergence=audio_first)
        print(f"SESSION {name} status={status} confirmed={confirmed} ordinals={n} "
              f"audio_first_divergence={audio_first if audio_first is not None else 'none'}")
        if status == "diverged":
            lag = lag_between(reference, ordinal)
            report["divergence"] = {"ordinal": ordinal, "regions": regions, "lag": lag}
            print(f"WINDOW ordinal={ordinal} regions={','.join(regions)} "
                  f"reference_frames={lag['frames']} reference_vblanks={lag['vblanks']}")
            capture_dir = directory / "capture"
            capture_dir.mkdir()
            state_path, cap_failure = run_native(capture_dir, session_dir(name) / "input.txt",
                                                 ordinal, lag_path=lag_path, dump_ordinals=[ordinal])
            dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
            if not dump_path.is_file():
                raise SessionError(f"no native dump at ordinal {ordinal}: {cap_failure[-300:]}")
            native_state = native_regions(json.loads(dump_path.read_text()))
            reference_state = reference_capture(name, masks, frames, ordinal, pokes)
            details = attribute(name, masks, frames, ordinal, native_state, reference_state, pokes)
            report["divergence"]["rows"] = details
            for row in details[:8]:
                print(f"DIVERGE ordinal={ordinal} field={row['field']} address={row['address']} "
                      f"symbol={row['symbol']} native={row['native']} reference={row['reference']} "
                      f"writer={row['writer']}")
        if status == "native-short" and failure:
            for line in failure.strip().splitlines()[-3:]:
                print(f"NATIVE {line}")
    ratchet = read_ratchet()
    previous = ratchet.get(name, {}).get("confirmed_ordinal")
    exit_code = {"clean": 0, "diverged": 1, "native-short": 1}[status]
    if previous is not None and confirmed < previous and not write:
        print(f"REGRESSION {name} key=confirmed_ordinal was={previous} now={confirmed}")
        report["regression"] = {"was": previous, "now": confirmed}
        exit_code = 3
    elif previous is None or confirmed > previous or write:
        ratchet[name] = {"confirmed_ordinal": confirmed}
        write_ratchet(ratchet)
    emit(report, json_path)
    return exit_code


def derive(name: str, movie: Path, goal: str) -> int:
    """The reference plays a frame-indexed movie; the byte each DoFrame read
    becomes the session. Then the session is replayed on the DoFrame axis and
    its digests must equal the movie run's: the ROM reads JOYP only inside
    ReadJoypad, so both axes are one execution."""
    movie_masks = refstream.load_masks(movie)
    profile = refstream.movie_profile(movie)
    frame_mode = profile["frame_mode"]
    frames = len(movie_masks) + 400
    movie_run = build_reference(f"{name}-movie", movie_masks, frames, axis="frame",
                                record_input=True, frame_mode=frame_mode, gba=profile["gba"])
    inputs = movie_run["inputs"]
    directory = session_dir(name)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "input.txt").write_text("\n".join(str(b) for b in inputs) + "\n")
    meta = {
        "schema": 1, "name": name, "goal": goal, "ordinals": len(inputs),
        "derived_from": str(movie.relative_to(ROOT) if movie.is_absolute() else movie),
        "movie_frames": len(movie_masks), "movie_frame_mode": frame_mode, "movie_gba": profile["gba"],
        "reference_frames": frames,
        "recorded": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    session_run = build_reference(name, inputs, frames, axis="ordinal")
    movie_digests = load_reference(movie_run)
    session_digests = load_reference(session_run)
    mismatch = None
    for index in range(min(len(movie_digests), len(session_digests)) // REFERENCE_RECORD.size):
        a = REFERENCE_RECORD.unpack_from(movie_digests, index * REFERENCE_RECORD.size)[:GATED]
        b = REFERENCE_RECORD.unpack_from(session_digests, index * REFERENCE_RECORD.size)[:GATED]
        if a != b:
            mismatch = index + 1
            break
    meta["axis_match"] = mismatch is None and session_run["anchors"] == movie_run["anchors"]
    meta["axis_mismatch_ordinal"] = mismatch
    (directory / "session.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(f"DERIVED {name} ordinals={len(inputs)} movie_frames={len(movie_masks)} "
          f"axis_match={meta['axis_match']}"
          + (f" mismatch_ordinal={mismatch}" if mismatch else ""))
    return 0 if meta["axis_match"] else 1


TRACKER_DIR = ROOT / "build" / "completion" / "tracker"


def emit(report: dict[str, Any], json_path: Path | None) -> None:
    """The report goes to the caller's path and to the tracker's copy, which
    `tools/completion/tracker.py sync` projects onto the issue tracker."""
    for path in (json_path, TRACKER_DIR / f"verify-{report['name']}.json"):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def session_names() -> list[str]:
    if not SESSIONS.is_dir():
        return []
    return sorted(p.name for p in SESSIONS.iterdir() if (p / "input.txt").is_file())


def lowest_confirmed() -> str:
    names = session_names()
    if not names:
        raise SessionError("no sessions under tests/sessions")
    ratchet = read_ratchet()
    return min(names, key=lambda name: (ratchet.get(name, {}).get("confirmed_ordinal", -1), name))


def diff(name: str, ordinal: int) -> int:
    """Every gated byte the two lanes disagree on at one DoFrame ordinal, by
    symbol: the whole picture behind a verify's first eight DIVERGE rows."""
    masks, meta = load_session(name)
    frames = reference_frames(masks, meta)
    ref_meta = build_reference(name, masks, frames, pokes=meta["pokes"])
    lag_path = ROOT / ref_meta["directory"] / "lag.txt"
    with tempfile.TemporaryDirectory(prefix=f"session-{name}-") as tmp:
        state_path, failure = run_native(Path(tmp), session_dir(name) / "input.txt", ordinal,
                                         lag_path=lag_path, dump_ordinals=[ordinal])
        dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
        if not dump_path.is_file():
            raise SessionError(f"no native dump at ordinal {ordinal}: {failure[-300:]}")
        dump = json.loads(dump_path.read_text())
        native = native_regions(dump)
        native["sram"] = b"".join(bytes(dump[f"sram_bank_{bank}"]) for bank in range(4))
    reference = reference_capture(name, masks, frames, ordinal, meta["pokes"], sram=True)
    tables = mask_tables()
    rows = 0
    # SRAM is not digested (a save is compared through the checksum the game
    # keeps in WRAM); it is diffed here so a checksum row names its byte.
    for region in (*REGIONS[:GATED], "sram"):
        table = tables[region] if region in tables else bytes(len(native["sram"]))
        nat, ref = native[region], reference[region]
        offset = 0
        while offset < min(len(nat), len(ref)):
            if table[offset] or nat[offset] == ref[offset]:
                offset += 1
                continue
            end = offset
            while end < min(len(nat), len(ref)) and not table[end] and nat[end] != ref[end]:
                end += 1
            if region == "sram":
                bank, in_bank = divmod(offset, 0x2000)
                symbol, _base = refstream.resolve_region(f"sram_bank_{bank}", in_bank)
                print(f"DIFF ordinal={ordinal} field=sram_bank_{bank} address=0x{0xA000 + in_bank:04X} symbol={symbol} "
                      f"native={nat[offset:end].hex()} reference={ref[offset:end].hex()}")
                rows += 1
                offset = end
                continue
            field, field_offset = region_field(region, offset)
            symbol, _base = refstream.resolve_region(field, field_offset)
            address = refstream.FIELD_WINDOWS[field][0] + field_offset
            print(f"DIFF ordinal={ordinal} field={field} address=0x{address:04X} symbol={symbol} "
                  f"native={nat[offset:end].hex()} reference={ref[offset:end].hex()}")
            rows += 1
            offset = end
    print(f"DIFF {name} ordinal={ordinal} runs={rows}")
    return 0 if rows == 0 else 1


# Routines that say nothing about where a DoFrame interval went: bank
# switches, the sound driver, text plumbing and the card-data loaders that
# every AI evaluation calls dozens of times.
ROUTINE_NOISE = (
    "Bank", "Music", "SFX", "TimerHandler", "SoundTimerHandler", "IncrementPlayTime",
    "SerialTimerHandler", "ReadJoypad", "SaveButtonsHeld", "HandleDPadRepeat",
    "FlushPalettesIfRequested", "NoOp", "HtimesL", "GetTurnDuelistVariable",
    "GetNonTurnDuelistVariable", "GetCardPointer", "GetCardIDFromDeckIndex", "_GetCardIDFromDeckIndex",
    "LoadCardDataTo", "CopyText", "GetText", "InitText", "ProcessText", "PlaceNextTextTile",
    "BCCoordToBGMap0Address", "DECoordToBGMap0Address", "WriteByteToBGMap0", "HblankWriteByteToBGMap0",
    "SafeCopyData", "JPHblankCopy", "CaseHalfWidthLetter", "ClassifyTextCharacterPair",
    "ProcessSpecialTextCharacter", "TerminateHalfWidthText", "GenerateTextTile", "Func_22ca",
    "Func_2325", "Func_235e", "ConvertSpecialTrainerCardToPokemon", "SwapTurn",
    "CopyAttackDataAndDamage", "GetCardType", "CountCardIDInLocation", "TranslateColorToWR",
    "GetArenaCard", "GetCardWeakness", "GetCardResistance", "GetPlayAreaCardColor",
    "CheckIsIncapableOfUsingPkmnPower", "CountPokemonWithActivePkmnPower", "CountTurnDuelistPokemonWithActivePkmnPower",
    "ApplyAttached", "HandleDamageReduction", "HandleDoubleDamageSubstatus", "HandleNoDamageOrEffectSubstatus",
    "CheckIfEnoughParticularAttachedEnergy", "GetPlayAreaCardAttachedEnergies", "HandleEnergyBurn",
    "CheckEnergyNeededForAttack", "CheckLoadedAttackFlag", "ConvertColorToEnergyCardID", "CheckMatchingCommand",
    "TryExecuteEffectCommandFunction", "CalculateDamage_", "EstimateDamage_", "FindLastCardInHand",
    "CreateHandCardList", "ConvertHPToDamageCounters",
)


def routines(name: str, ordinal: int, *, everything: bool) -> int:
    """The reference's routine entries between DoFrame anchors `ordinal` and
    `ordinal + 1`, in order, runs collapsed: the interval a verify diverged in,
    read as the routines it ran. The noise list keeps the AI's decision
    routines visible; --all prints every entry."""
    masks, meta = load_session(name)
    frames = reference_frames(masks, meta)
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    candidates, by_bank_address = refstream.routine_entry_addresses()
    sequence: list[str] = []
    with refstream.Core(padded, pokes=meta["pokes"]) as core:
        core.input_axis = "ordinal"
        core.seek(checkpoint_directory(name, masks, frames, meta["pokes"]), ordinal)

        def on_exec(address: int, _cycle: int) -> None:
            if address not in candidates or core.ordinal != ordinal:
                return
            bank = 0 if address < 0x4000 else core.bank_of(address)
            label = by_bank_address.get((bank, address))
            if label and (everything or not label.startswith(ROUTINE_NOISE)):
                sequence.append(label)

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: core.ordinal > ordinal)
    out: list[str] = []
    for label in sequence:
        if out and out[-1].split("x")[0] == label:
            head, _, count = out[-1].partition("x")
            out[-1] = f"{head}x{int(count or 1) + 1}"
        else:
            out.append(label)
    print(f"ROUTINES {name} ordinal={ordinal} entries={len(sequence)} shown={len(out)}")
    for index, label in enumerate(out):
        print(f"  {index:4d} {label}")
    return 0


def status() -> int:
    ratchet = read_ratchet()
    print(f"{'session':<24} {'ordinals':>8} {'confirmed':>9}  goal")
    for name in session_names():
        masks, meta = load_session(name)
        confirmed = ratchet.get(name, {}).get("confirmed_ordinal", "-")
        print(f"{name:<24} {len(masks):>8} {confirmed!s:>9}  {meta.get('goal', '')}")
    return 0


def record_meta(name: str, goal: str) -> int:
    masks, meta = load_session(name)
    meta.update({
        "schema": 1, "name": name, "goal": goal or meta.get("goal", ""),
        "ordinals": len(masks),
        "recorded": datetime.now(UTC).isoformat(timespec="seconds"),
    })
    (session_dir(name) / "session.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(f"SESSION {name} ordinals={len(masks)} goal={meta['goal']!r}")
    return 0


# The ROM's duel loop dispatches per turn holder (core.asm HandleTurn reads
# DUELVARS_DUELIST_TYPE) and AIDoAction keys on the global wOpponentDeckID
# (home/ai.asm), so with the player's duelist type set to AI the ROM plays
# both sides of a duel by itself. The poke lands at the first anchor after
# StartDuel_VSAIOpp/InitVariablesToBeginDuel have run and before
# ChooseInitialArenaAndBenchPokemon reads the type (practice-win: 23,226 and
# 23,840). Text boxes still wait for a press, so the tail mashes A.
AI_DUEL = {
    "wPlayerDuelistType": 0xC2F1, "wOpponentDuelistType": 0xC3F1,
    "wDuelType": 0xCC09, "wOpponentDeckID": 0xCC0E, "wIsPracticeDuel": 0xCC13,
    "wDuelInitialPrizes": 0xCC08, "wRNG1": 0xCACA, "wRNG2": 0xCACB,
}
DUELIST_TYPE_AI_OPP = 0x80
WRAM = {"wDuelTurns": 0x0C06, "wDuelFinished": 0x0C07}
AI_DUEL_MAX_ORDINALS = 80_000


def ai_duel(name: str, *, base: str, at: int, deck: int, seed: int | None, prizes: int | None,
            period: int, tail: int, goal: str) -> int:
    """Branch `base` at DoFrame `at` into an AI-versus-AI duel and record the
    session the reference plays: the base's input through `at`, the pokes,
    then A every `period` DoFrames until wDuelFinished is set plus `tail`
    more, so the result screen and the post-duel script are in the session."""
    base_masks, base_meta = load_session(base)
    if not 1 <= at <= len(base_masks):
        raise SessionError(f"--at must be within {base}'s {len(base_masks)} ordinals")
    if not 0 <= deck <= 0x7F:
        raise SessionError("deck id must be 0..127")
    pokes: refstream.Pokes = {k: list(v) for k, v in base_meta["pokes"].items() if k < at}
    kind = DUELIST_TYPE_AI_OPP | deck
    writes = [(AI_DUEL["wPlayerDuelistType"], kind), (AI_DUEL["wOpponentDuelistType"], kind),
              (AI_DUEL["wDuelType"], kind), (AI_DUEL["wOpponentDeckID"], deck),
              (AI_DUEL["wIsPracticeDuel"], 0)]
    if prizes is not None:
        writes.append((AI_DUEL["wDuelInitialPrizes"], prizes))
    if seed is not None:
        writes += [(AI_DUEL["wRNG1"], seed & 0xFF), (AI_DUEL["wRNG2"], (seed >> 8) & 0xFF)]
    pokes.setdefault(at, []).extend(writes)
    prefix = base_masks[:at]
    mash = [0x10 if (i % period) < 4 else 0 for i in range(AI_DUEL_MAX_ORDINALS - at)]
    masks = prefix + mash
    finished_at: int | None = None
    turns = 0
    end = len(masks)
    with refstream.Core(masks, pokes=pokes) as core:
        core.input_axis = "ordinal"
        core.install_exec(None)

        def stop() -> bool:
            nonlocal finished_at, turns, end
            if core.ordinal <= at:
                return False
            wram = core.area("WRAM")
            turns = wram[WRAM["wDuelTurns"]]
            if finished_at is None and wram[WRAM["wDuelFinished"]] != 0:
                finished_at = core.ordinal
                end = min(len(masks), finished_at + tail)
            return core.ordinal >= end

        core.run(len(masks) * 2 + 400, stop=stop)
    if finished_at is None:
        raise SessionError(f"the duel did not finish within {AI_DUEL_MAX_ORDINALS} ordinals "
                           f"(turns={turns}); the AI or the mash period stalled")
    directory = session_dir(name)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "input.txt").write_text("\n".join(str(m) for m in masks[:end]) + "\n")
    (directory / "pokes.txt").write_text(refstream.pokes_text(pokes))
    meta = {
        "schema": 1, "name": name, "ordinals": end,
        "goal": goal or f"AI-versus-AI duel, deck id {deck}, branched from {base} at {at}",
        "derived_from": base, "branch_ordinal": at, "ai_deck": deck, "seed": seed,
        "prizes": prizes, "duel_finished_ordinal": finished_at, "duel_turns": turns,
        "recorded": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    (directory / "session.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(f"SESSION {name} ordinals={end} duel_finished={finished_at} turns={turns} "
          f"deck={deck} seed={seed} prizes={prizes}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("name", nargs="?", default="")
    verify_parser.add_argument("--write-ratchet", action="store_true",
                               help="accept a lower confirmed ordinal")
    verify_parser.add_argument("--json")
    sub.add_parser("status")
    sweep_parser = sub.add_parser("sweep", help="oracle-diff every ported routine at its first entry in a session")
    sweep_parser.add_argument("name")
    sweep_parser.add_argument("--after", type=int, default=0, help="first DoFrame ordinal to capture from")
    sweep_parser.add_argument("--until", type=int, help="last DoFrame ordinal to capture through")
    sweep_parser.add_argument("--limit", type=int, default=0, help="stop after this many routines")
    sweep_parser.add_argument("--json", type=Path)
    worker_parser = sub.add_parser("sweep-worker", help=argparse.SUPPRESS)
    worker_parser.add_argument("entries", type=Path)
    worker_parser.add_argument("--start", type=int, default=0)
    worker_parser.add_argument("--out", type=Path, required=True)
    diff_parser = sub.add_parser("diff", help="all gated bytes the lanes disagree on at one ordinal")
    diff_parser.add_argument("name")
    diff_parser.add_argument("ordinal", type=int)
    routines_parser = sub.add_parser("routines", help="the reference's routine entries within one DoFrame interval")
    routines_parser.add_argument("name")
    routines_parser.add_argument("ordinal", type=int)
    routines_parser.add_argument("--all", action="store_true", help="include the plumbing routines")
    meta_parser = sub.add_parser("meta")
    meta_parser.add_argument("name")
    meta_parser.add_argument("--goal", default="")
    derive_parser = sub.add_parser("derive")
    derive_parser.add_argument("name")
    derive_parser.add_argument("--movie", required=True, type=Path,
                               help="per-rendered-frame mask file, e.g. build/completion/tas/input.txt")
    derive_parser.add_argument("--goal", default="")
    capture_parser = sub.add_parser("capture", help="write a case fixture from the reference's state at a routine's entry")
    capture_parser.add_argument("name")
    capture_parser.add_argument("--routine", required=True)
    capture_parser.add_argument("--after", type=int, default=0, help="first DoFrame ordinal to consider")
    capture_parser.add_argument("--nth", type=int, default=1, help="capture the nth entry at or after --after")
    capture_parser.add_argument("--out", type=Path)
    capture_parser.add_argument("--sram", action="store_true",
                                help="also capture the four SRAM banks, for a routine that reads save data")
    duel_parser = sub.add_parser("ai-duel", help="branch a session into an AI-versus-AI duel")
    duel_parser.add_argument("name")
    duel_parser.add_argument("--from", dest="base", default="practice-win")
    duel_parser.add_argument("--at", type=int, default=23227,
                             help="DoFrame ordinal to poke at: after StartDuel_VSAIOpp, before the first turn")
    duel_parser.add_argument("--deck", type=int, required=True,
                             help="*_DECK_ID whose AI plays both sides (0 is Sam's scripted practice AI)")
    duel_parser.add_argument("--seed", type=int, help="wRNG1/wRNG2 at the branch")
    duel_parser.add_argument("--prizes", type=int, choices=range(1, 7))
    duel_parser.add_argument("--period", type=int, default=24, help="DoFrames between A presses")
    duel_parser.add_argument("--tail", type=int, default=1500, help="DoFrames kept after wDuelFinished")
    duel_parser.add_argument("--goal", default="")
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            return status()
        if args.command == "diff":
            return diff(args.name, args.ordinal)
        if args.command == "sweep":
            return sweep(args.name, after=args.after, until=args.until, limit=args.limit,
                         json_path=args.json)
        if args.command == "sweep-worker":
            return sweep_worker(args.entries, args.start, args.out)
        if args.command == "routines":
            return routines(args.name, args.ordinal, everything=args.all)
        if args.command == "meta":
            return record_meta(args.name, args.goal)
        if args.command == "derive":
            movie = args.movie if args.movie.is_absolute() else ROOT / args.movie
            return derive(args.name, movie, args.goal or f"derived from {args.movie}")
        if args.command == "capture":
            return capture(args.name, args.routine, after=args.after, nth=args.nth, out=args.out, sram=args.sram)
        if args.command == "ai-duel":
            return ai_duel(args.name, base=args.base, at=args.at, deck=args.deck, seed=args.seed,
                           prizes=args.prizes, period=args.period, tail=args.tail, goal=args.goal)
        name = args.name or lowest_confirmed()
        return verify(name, write=args.write_ratchet,
                      json_path=Path(args.json) if args.json else None)
    except (SessionError, refstream.RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
