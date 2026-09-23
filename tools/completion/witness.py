#!/usr/bin/env python3
"""Requirement evidence from recorded sessions on the DoFrame axis.

The reference (Gambatte) and the port replay one session; the masked digest
stream must match at every anchor (session.verify), then sampled anchors are
compared byte for byte across the requirement's representation fields.
"""

from __future__ import annotations

import array
import hashlib
import json
import math
import re
import struct
import tempfile
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import session

ROOT = session.ROOT
FRAME_PIXELS = 160 * 144
EVENT_NAMES = {
    1: "BOOT_STARTED",
    2: "TITLE_READY",
    3: "START_MENU_READY",
    4: "NEW_GAME_ENTERED",
    5: "OVERWORLD_READY",
    6: "CREDITS_REACHED",
    7: "PRINTER_PNG_CLOSED",
    8: "LINK_SESSION_CLOSED",
}
IO_COMPARED = (
    0x00, 0x01, 0x02, 0x06, 0x07,
    0x40, 0x42, 0x43, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4D, 0x4F,
    0x51, 0x52, 0x53, 0x54, 0x55, 0x56,
    0x68, 0x6A, 0x70,
)
IO_BITS = {0x07: 0x07}
APU_FIRST, APU_LAST = 0xFF10, 0xFF3F
APU_TRACE_ORDINALS = 6000
APU_TRACE_CAPACITY = 65536
APU_READBACK = {
    0xFF10: (0x80, 0xFF), 0xFF11: (0x3F, 0xFF), 0xFF12: (0x00, 0xFF), 0xFF13: (0xFF, 0x00),
    0xFF14: (0xBF, 0x40), 0xFF15: (0xFF, 0x00), 0xFF16: (0x3F, 0xFF), 0xFF17: (0x00, 0xFF),
    0xFF18: (0xFF, 0x00), 0xFF19: (0xBF, 0x40), 0xFF1A: (0x7F, 0xFF), 0xFF1B: (0xFF, 0x00),
    0xFF1C: (0x9F, 0xFF), 0xFF1D: (0xFF, 0x00), 0xFF1E: (0xBF, 0x40), 0xFF1F: (0xFF, 0x00),
    0xFF20: (0xFF, 0x00), 0xFF21: (0x00, 0xFF), 0xFF22: (0x00, 0xFF), 0xFF23: (0xBF, 0x40),
    0xFF24: (0x00, 0xFF), 0xFF25: (0x00, 0xFF), 0xFF26: (0x70, 0x80),
}
NR52 = 0xFF26
SERIAL_VECTOR = 0x0058
BOOT_ROM_PCS = ((0x0000, 0x0100), (0x0200, 0x0900))


class WitnessError(RuntimeError):
    pass


WRAM_HEADER = ROOT / "include" / "generated" / "wram.h"


def wram_offset(symbol: str) -> int:
    match = re.search(rf"#define\s+{re.escape(symbol)}_ADDR\s+0x([0-9A-Fa-f]+)u?", WRAM_HEADER.read_text(encoding="utf-8"))
    if match is None:
        raise WitnessError(f"{symbol}_ADDR is absent from {WRAM_HEADER}")
    return int(match.group(1), 16) - 0xC000


DUEL_FINISHED_OFFSET = wram_offset("wDuelFinished")
RNG_OFFSET = wram_offset("wRNG1")


@dataclass(frozen=True)
class Spec:
    sessions: tuple[str, ...]
    fields: tuple[str, ...]
    terminal: str
    event: str | None = None
    samples: int = 24
    checks: tuple[str, ...] = ()


SPECS: dict[str, Spec] = {
    "boot-title": Spec(
        sessions=("boot-menu",),
        fields=(
            "wram", "hram", "vram_bank_0", "vram_bank_1", "oam", "io", "palette_ram",
            "framebuffer", "input_latch", "timer_frame_counters",
        ),
        terminal="NEW_GAME_ENTERED",
        event="NEW_GAME_ENTERED",
    ),
    "ui-corpus": Spec(
        sessions=("boot-deck-machine", "practice-win"),
        fields=("wram", "vram_bank_0", "vram_bank_1", "oam", "palette_ram", "framebuffer"),
        terminal="UI_CORPUS_CLOSED",
    ),
    "raster-effects": Spec(
        sessions=("effect-gastly-lv17-2-board",),
        fields=("framebuffer", "vram_bank_0", "vram_bank_1"),
        terminal="RASTER_EFFECTS_CLOSED",
    ),
    "audio-catalog": Spec(
        sessions=("boot-menu", "seed-deck-machines", "challenge-machine"),
        fields=("apu_state", "apu_trace", "timer_frame_counters"),
        terminal="AUDIO_TRACE_CLOSED",
    ),
    "audio-pcm": Spec(
        sessions=("boot-menu", "seed-deck-machines", "challenge-machine"),
        fields=("apu_trace", "framebuffer"),
        terminal="PCM_WINDOW_CLOSED",
        checks=("pcm",),
    ),
    "script-vm": Spec(
        sessions=("practice-win", "boot-deck-machine", "challenge-machine", "seed-packs"),
        fields=("wram", "mapper_state", "input_latch"),
        terminal="SCRIPT_OPCODE_CLOSED",
        checks=("script_opcodes",),
    ),
    "all-maps-scripts": Spec(
        sessions=("credits-1-explore-1",),
        fields=("wram", "framebuffer", "save", "rng"),
        terminal="CREDITS_REACHED",
        event="CREDITS_REACHED",
    ),
    "link-ir-printer": Spec(
        sessions=("link-duel-a", "link-duel-b"),
        fields=("transport", "wram", "rng", "framebuffer", "input_latch"),
        terminal="LINK_SESSION_CLOSED",
        event="LINK_SESSION_CLOSED",
    ),
    "printer": Spec(
        sessions=("printer-card-list",),
        fields=("printer", "wram", "framebuffer", "input_latch"),
        terminal="PRINTER_PNG_CLOSED",
        event="PRINTER_PNG_CLOSED",
        checks=("pages",),
    ),
    "new-game-to-credits": Spec(
        sessions=("credits-1-explore-1",),
        fields=(
            "wram", "hram", "sram_bank_0", "sram_bank_1", "sram_bank_2", "sram_bank_3",
            "vram_bank_0", "vram_bank_1", "oam", "io", "palette_ram", "mapper_state",
            "input_latch", "timer_frame_counters", "rng", "apu_state", "apu_trace",
            "framebuffer", "save", "transport", "printer",
        ),
        terminal="CREDITS_REACHED",
        event="CREDITS_REACHED",
    ),
    "duel-state": Spec(
        sessions=(
            "practice-win", "ai-duel-02", "ai-duel-03", "ai-duel-0c",
            "effect-clefairy-2", "effect-item-finder", "effect-psyduck-1",
        ),
        fields=("wram", "rng", "input_latch"),
        terminal="DUEL_VECTOR_CLOSED",
    ),
    "seeded-duel": Spec(
        sessions=(
            "effect-clefairy-2", "effect-item-finder", "effect-pokemon-flute",
            "effect-revive", "effect-electabuzz-lv20-2", "effect-psyduck-1",
        ),
        fields=("wram", "rng", "framebuffer", "save"),
        terminal="DUEL_TERMINAL_OUTCOME",
        checks=("duel_finished",),
    ),
}



def apu_readback(address: int, value: int) -> int:
    if address >= 0xFF27 and address <= 0xFF2F:
        return 0xFF
    if address >= 0xFF30:
        return value
    fixed, keep = APU_READBACK[address]
    return fixed | (value & keep)


def in_boot_rom(pc: int) -> bool:
    return any(start <= pc < end for start, end in BOOT_ROM_PCS)


def sample_anchors(count: int, samples: int) -> list[int]:
    chosen = {max(1, round(index * count / samples)) for index in range(1, samples + 1)}
    chosen.add(count)
    return sorted(chosen)


def verify_report(name: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"witness-{name}-") as directory:
        json_path = Path(directory) / "verify.json"
        session.verify(name, write=False, json_path=json_path, publish=False)
        return json.loads(json_path.read_text(encoding="utf-8"))


def reference_pass(
    name: str,
    masks: list[int],
    meta: dict[str, Any],
    frames: int,
    anchors: list[int],
    *,
    want_frames: bool,
    want_apu: bool,
    want_save: bool,
    pcm_sink: Any = None,
) -> dict[str, Any]:
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    count = anchors[-1]
    wanted = set(anchors)
    captured: dict[int, dict[str, Any]] = {}
    stable: dict[int, bool] = {}
    apu_writes: list[tuple[int, int, int]] = []
    anchor_samples: list[int] = []
    link = meta.get("link")
    if link:
        side = int(link["side"])
        members = (name, link["peer"]) if side == 0 else (link["peer"], name)
        cores, pair, _masks = session.linked_pair(members, frames)
        core = cores[side]
    else:
        cores = [refstream.Core(padded, pokes=meta["pokes"], save=meta["save"], printer=meta["printer"])]
        pair = None
        core = cores[0]
    try:
        core.input_axis = "ordinal"
        hits = 0
        received = 0
        received_crc = 0
        last_frame = b""
        pending: int | None = None
        read = core.library.gambatte_cpuread
        handle = core.core

        apu_limit = min(count, APU_TRACE_ORDINALS)

        def on_write(address: int, _cycle: int) -> None:
            if APU_FIRST <= address <= APU_LAST and hits < apu_limit and not in_boot_rom(core.pc()):
                apu_writes.append((hits, address, read(handle, address)))

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal hits, last_frame, pending, received, received_crc
            if address == SERIAL_VECTOR:
                received += 1
                received_crc = zlib.crc32(bytes((read(handle, 0xFF01),)), received_crc)
                return
            if address != refstream.DOFRAME_ANCHOR:
                return
            hits += 1
            anchor_samples.append(core.samples)
            if want_frames:
                frame = bytes(core._framebuffer)
                if pending is not None:
                    stable[pending] = stable.get(pending, False) and frame == captured[pending]["framebuffer"]
                    pending = None
                if hits in wanted:
                    stable[hits] = frame == last_frame
                    pending = hits
                last_frame = frame
            if hits in wanted:
                record = session.reference_regions(core)
                record["io"] = core.io_block()
                record["palette_ram"] = core.palette_block()
                record["mapper_state"] = {
                    "rom_bank": core.bank_of(0x4000),
                    "sram_bank": core.bank_of(0xA000),
                    "vram_bank": record["io"][0x4F] & 1,
                }
                if want_frames:
                    record["framebuffer"] = last_frame
                record["transport"] = {"exchanges": received, "received_crc": received_crc}
                if want_save and hits == count:
                    record["save"] = core.area("CartRAM")[:0x8000]
                if core.printer is not None:
                    record["printer"] = core.printer.snapshot()
                    if hits == count:
                        record["pages"] = list(core.printer.pages)
                captured[hits] = record

        if want_apu:
            core.on_write(on_write)
        if pcm_sink is not None:
            core.pcm_sink = pcm_sink
        core.install_exec(on_exec)
        if pair is not None:
            session.run_linked(pair, lambda: hits > count, frames * refstream.SAMPLES_PER_FRAME)
        else:
            core.run(frames, stop=lambda: hits > count)
        if pending is not None:
            stable[pending] = False
    finally:
        for member in cores:
            member.close()
    if len(captured) != len(wanted):
        raise WitnessError(f"reference reached {len(captured)} of {len(wanted)} anchors for {name}")
    return {"anchors": captured, "stable": stable, "apu_writes": apu_writes, "anchor_samples": anchor_samples}


REFERENCE_PCM_RATE = 2097152
NATIVE_PCM_RATE = 44100
NATIVE_PCM_BLOCK = 1470
PCM_WINDOW_ORDINALS = 4
PCM_WINDOWS = 40
PCM_FFT_SIZE = 2048
PCM_SILENCE_RMS = 100.0
PCM_AGREE_COSINE = 0.7
PCM_MEDIAN_COSINE = 0.8
PCM_AGREE_FRACTION = 0.9
PCM_ENVELOPE_CORRELATION = 0.9


def _fft(values: list[complex]) -> list[complex]:
    size = len(values)
    if size == 1:
        return values
    even = _fft(values[0::2])
    odd = _fft(values[1::2])
    out = [0j] * size
    for k in range(size // 2):
        twiddle = complex(math.cos(-2 * math.pi * k / size), math.sin(-2 * math.pi * k / size)) * odd[k]
        out[k] = even[k] + twiddle
        out[k + size // 2] = even[k] - twiddle
    return out


def _mono(samples: array.array) -> list[float]:
    return [(samples[2 * i] + samples[2 * i + 1]) / 2.0 for i in range(len(samples) // 2)]


def _rms(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))


def _spectrum(values: list[float]) -> list[float]:
    values = values[:PCM_FFT_SIZE]
    mean = sum(values) / len(values) if values else 0.0
    padded = [complex(v - mean) for v in values] + [0j] * (PCM_FFT_SIZE - len(values))
    return [abs(c) for c in _fft(padded)[: PCM_FFT_SIZE // 2]]


def _cosine(left: list[float], right: list[float]) -> float:
    num = sum(a * b for a, b in zip(left, right))
    da = math.sqrt(sum(a * a for a in left))
    db = math.sqrt(sum(b * b for b in right))
    return num / (da * db) if da and db else 0.0


def _correlation(left: list[float], right: list[float]) -> float:
    size = min(len(left), len(right))
    if size < 2:
        return 0.0
    ml = sum(left[:size]) / size
    mr = sum(right[:size]) / size
    num = sum((left[i] - ml) * (right[i] - mr) for i in range(size))
    dl = math.sqrt(sum((left[i] - ml) ** 2 for i in range(size)))
    dr = math.sqrt(sum((right[i] - mr) ** 2 for i in range(size)))
    return num / (dl * dr) if dl and dr else 0.0


def _reference_window(raw: bytes, anchor_samples: list[int], start: int, length: int) -> list[float]:
    begin = anchor_samples[start - 1] if start >= 1 else 0
    end = anchor_samples[start + length - 1]
    frames_in = end - begin
    stereo = array.array("h", raw[begin * 4 : end * 4])
    frames_out = frames_in * NATIVE_PCM_RATE // REFERENCE_PCM_RATE
    out: list[float] = []
    for index in range(frames_out):
        source = index * frames_in // frames_out
        out.append((stereo[2 * source] + stereo[2 * source + 1]) / 2.0)
    return out


def _native_blocks(raw: bytes) -> dict[int, array.array]:
    blocks: dict[int, array.array] = {}
    offset = 0
    stride = 4 + NATIVE_PCM_BLOCK * 2
    while offset + stride <= len(raw):
        tag = struct.unpack_from("<I", raw, offset)[0]
        blocks.setdefault(tag, array.array("h")).extend(array.array("h", raw[offset + 4 : offset + stride]))
        offset += stride
    return blocks


def compare_pcm(reference_raw: bytes, anchor_samples: list[int], native_raw: bytes, count: int) -> dict[str, Any]:
    blocks = _native_blocks(native_raw)
    step = max(1, (count - PCM_WINDOW_ORDINALS) // PCM_WINDOWS)
    cosines: list[float] = []
    reference_rms: list[float] = []
    native_rms: list[float] = []
    silent = 0
    for start in range(1, count - PCM_WINDOW_ORDINALS, step):
        reference = _reference_window(reference_raw, anchor_samples, start, PCM_WINDOW_ORDINALS)
        native_samples = array.array("h")
        for ordinal in range(start, start + PCM_WINDOW_ORDINALS):
            native_samples.extend(blocks.get(ordinal, array.array("h")))
        native = _mono(native_samples)
        left = _rms(reference)
        right = _rms(native)
        reference_rms.append(left)
        native_rms.append(right)
        if left < PCM_SILENCE_RMS and right < PCM_SILENCE_RMS:
            silent += 1
            continue
        cosines.append(_cosine(_spectrum(reference), _spectrum(native)))
    ordered = sorted(cosines)
    median = ordered[len(ordered) // 2] if ordered else 0.0
    agreeing = sum(1 for value in cosines if value >= PCM_AGREE_COSINE) / len(cosines) if cosines else 0.0
    envelope = _correlation(reference_rms, native_rms)
    passed = (
        bool(cosines)
        and median >= PCM_MEDIAN_COSINE
        and agreeing >= PCM_AGREE_FRACTION
        and envelope >= PCM_ENVELOPE_CORRELATION
    )
    return {
        "windows": len(reference_rms),
        "silent_windows": silent,
        "window_ordinals": PCM_WINDOW_ORDINALS,
        "median_cosine": round(median, 4),
        "agreeing_fraction": round(agreeing, 4),
        "envelope_correlation": round(envelope, 4),
        "thresholds": {
            "agree_cosine": PCM_AGREE_COSINE,
            "median_cosine": PCM_MEDIAN_COSINE,
            "agree_fraction": PCM_AGREE_FRACTION,
            "envelope_correlation": PCM_ENVELOPE_CORRELATION,
        },
        "status": "PASS" if passed else "FAIL",
    }


def native_pass(
    name: str,
    count: int,
    anchors: list[int],
    lag_path: Path,
    directory: Path,
    *,
    pcm_out: Path | None = None,
    printer_dir: Path | None = None,
) -> dict[int, dict[str, Any]]:
    state_path, failure, _off = session.run_native(
        directory, session.session_dir(name) / "input.txt", count, lag_path=lag_path,
        dump_ordinals=anchors, pcm_out=pcm_out, printer_dir=printer_dir,
    )
    dumps: dict[int, dict[str, Any]] = {}
    for ordinal in anchors:
        dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
        if not dump_path.is_file():
            raise WitnessError(f"native dump missing at ordinal {ordinal} for {name}: {failure[-300:]}")
        dumps[ordinal] = json.loads(dump_path.read_text(encoding="utf-8"))
    return dumps


def read_png_grey(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise WitnessError(f"{path} is not a PNG")
    offset = 8
    width = height = 0
    idat = b""
    while offset < len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        kind = data[offset + 4 : offset + 8]
        body = data[offset + 8 : offset + 8 + length]
        if kind == b"IHDR":
            width = int.from_bytes(body[:4], "big")
            height = int.from_bytes(body[4:8], "big")
            if body[8] != 8 or body[9] != 0:
                raise WitnessError(f"{path} is not 8-bit greyscale")
        elif kind == b"IDAT":
            idat += body
        offset += 12 + length
    raw = zlib.decompress(idat)
    stride = width + 1
    rows = b"".join(raw[y * stride + 1 : (y + 1) * stride] for y in range(height))
    return width, height, rows


def compare_pages(printer_dir: Path, reference_pages: list[tuple[bytes, int]]) -> dict[str, Any]:
    files = sorted(printer_dir.glob("print-*.png"))
    mismatched: list[int] = []
    detail = ""
    for index, (tiles, palette) in enumerate(reference_pages):
        expected = refstream.render_page(tiles, palette)
        if index >= len(files):
            mismatched.append(index + 1)
            detail = detail or f"native wrote {len(files)} pages, reference printed {len(reference_pages)}"
            continue
        width, height, rows = read_png_grey(files[index])
        if width != 160 or rows != expected:
            mismatched.append(index + 1)
            detail = detail or f"page {index + 1}: {width}x{height} differs from the reference render"
    if len(files) > len(reference_pages):
        mismatched.append(len(reference_pages) + 1)
        detail = detail or f"native wrote {len(files)} pages, reference printed {len(reference_pages)}"
    if not reference_pages:
        detail = detail or "reference printed no page"
    status = "PASS" if reference_pages and not mismatched else "FAIL"
    return {
        "native_pages": len(files),
        "reference_pages": len(reference_pages),
        "mismatched": mismatched,
        "status": status,
        "detail": detail,
    }


def count_diff(left: bytes, right: bytes) -> int:
    if len(left) != len(right):
        return max(len(left), len(right))
    return sum(1 for a, b in zip(left, right) if a != b)


def compare_anchor(
    field: str,
    ordinal: int,
    native: dict[str, Any],
    reference: dict[str, Any],
    stable: bool,
    tables: dict[str, bytes],
    masks: list[int],
) -> int | None:
    if field in {"wram", "hram", "oam"}:
        return count_diff(
            session.masked(bytes(native[field]), tables[field]),
            session.masked(reference[field], tables[field]),
        )
    if field in {"vram_bank_0", "vram_bank_1"}:
        half = 0x2000 if field.endswith("1") else 0
        table = tables["vram"][half : half + 0x2000]
        return count_diff(
            session.masked(bytes(native[field]), table),
            session.masked(reference["vram"][half : half + 0x2000], table),
        )
    if field == "palette_ram":
        return count_diff(bytes(native["palette_ram"]), reference["palette_ram"])
    if field == "io":
        readback = native["io_readback"]
        return sum(
            1
            for offset in IO_COMPARED
            if (readback[offset] & IO_BITS.get(offset, 0xFF))
            != (reference["io"][offset] & IO_BITS.get(offset, 0xFF))
        )
    if field == "framebuffer":
        if not stable:
            return None
        pixels = struct.unpack(f"<{FRAME_PIXELS}I", reference["framebuffer"])
        return sum(1 for a, b in zip(native["framebuffer"], pixels) if (a & 0x7FFF) != (b & 0x7FFF))
    if field == "input_latch":
        mask = masks[ordinal - 1] if ordinal - 1 < len(masks) else 0
        return int(native["input_latch"] != ((mask << 4) | (mask >> 4)) & 0xFF)
    if field == "rng":
        return count_diff(bytes(native["rng"]), reference["wram"][RNG_OFFSET : RNG_OFFSET + 3])
    if field == "transport":
        expected = reference.get("transport") or {"exchanges": 0, "received_crc": 0}
        actual = native.get("transport")
        if not isinstance(actual, dict):
            return 1
        return sum(1 for key in ("exchanges", "received_crc") if actual.get(key) != expected[key])
    if field == "printer":
        expected = reference.get("printer")
        actual = native.get("printer")
        if expected is None:
            return len(actual or []) if isinstance(actual, list) else int(bool(actual and actual.get("attached")))
        if not isinstance(actual, dict):
            return 1
        return sum(
            1 for key in ("attached", "pages", "band_bytes", "status") if actual.get(key) != expected[key]
        ) + count_diff(bytes(actual.get("bands", [])), bytes(expected["bands"]))
    if field == "mapper_state":
        expected = reference["mapper_state"]
        return sum(1 for key, value in expected.items() if native["mapper_state"].get(key) != value)
    if field in {"save", "sram_bank_0", "sram_bank_1", "sram_bank_2", "sram_bank_3"}:
        if "save" not in reference:
            return None
        if field == "save":
            return count_diff(bytes(native["save"]), reference["save"])
        bank = int(field[-1])
        return count_diff(bytes(native[field]), reference["save"][bank * 0x2000 : (bank + 1) * 0x2000])
    if field == "apu_state":
        readback = native["io_readback"]
        return sum(
            1
            for address in range(APU_FIRST, 0xFF30)
            if (readback[address - 0xFF00] & (0xF0 if address == NR52 else 0xFF))
            != (reference["io"][address - 0xFF00] & (0xF0 if address == NR52 else 0xFF))
        )
    return None


def compare_apu_trace(native_dump: dict[str, Any], reference_writes: list[tuple[int, int, int]]) -> dict[str, Any]:
    native_writes = [(int(row["address"]), int(row["value"])) for row in native_dump["apu_trace"]]
    truncated = len(native_writes) >= APU_TRACE_CAPACITY
    if len(native_writes) > len(reference_writes):
        native_writes = native_writes[: len(reference_writes)]
    common = min(len(native_writes), len(reference_writes))
    first = None
    for index in range(common):
        address, value = native_writes[index]
        _ordinal, ref_address, ref_readback = reference_writes[index]
        if address != ref_address:
            first = index
            break
        want = apu_readback(address, value)
        if address == NR52:
            want &= 0xF0
            ref_readback &= 0xF0
        if want != ref_readback:
            first = index
            break
    if first is None and len(native_writes) != len(reference_writes) and not truncated:
        first = common
    return {
        "native_writes": len(native_writes),
        "reference_writes": len(reference_writes),
        "compared": common,
        "native_truncated": truncated,
        "first_mismatch": first,
        "status": "PASS" if first is None else "FAIL",
    }


def event_names(mask: int) -> list[str]:
    return [name for value, name in EVENT_NAMES.items() if mask & (1 << value)]


def witness_session(name: str, spec: Spec) -> dict[str, Any]:
    masks, meta = session.load_session(name)
    count = len(masks)
    frames = session.reference_frames(masks, meta)
    report = verify_report(name)
    row: dict[str, Any] = {
        "name": name,
        "ordinals": count,
        "verify": {
            key: report.get(key)
            for key in ("status", "confirmed", "reached", "schedule_mismatches", "audio_first_divergence")
        },
    }
    if report.get("divergence"):
        row["divergence"] = {key: report["divergence"].get(key) for key in ("ordinal", "regions")}
    if (
        report.get("status") != "clean"
        or report.get("confirmed") != count
        or report.get("schedule_mismatches")
        or report.get("audio_first_divergence") is not None
    ):
        row["status"] = "FAIL"
        return row
    anchors = sample_anchors(count, spec.samples)
    if "duel_finished" in spec.checks:
        finished = meta.get("duel_finished_ordinal")
        if not isinstance(finished, int) or finished < 1 or finished > count:
            row["status"] = "FAIL"
            row["failures"] = [f"session records no duel outcome inside {count} ordinals"]
            return row
        anchors = sorted(set(anchors) | {min(finished + 1, count)})
    fields = set(spec.fields)
    want_frames = "framebuffer" in fields
    want_apu = bool(fields & {"apu_trace", "apu_state"})
    want_save = bool(fields & {"save", "sram_bank_0", "sram_bank_1", "sram_bank_2", "sram_bank_3"})
    want_pcm = "pcm" in spec.checks
    with tempfile.TemporaryDirectory(prefix=f"witness-native-{name}-") as directory:
        lane = Path(directory)
        reference_pcm = b""
        native_pcm = b""
        if want_pcm:
            with (lane / "reference.pcm").open("wb") as sink:
                reference = reference_pass(
                    name, masks, meta, frames, anchors,
                    want_frames=want_frames, want_apu=want_apu, want_save=want_save, pcm_sink=sink,
                )
            reference_pcm = (lane / "reference.pcm").read_bytes()
        else:
            reference = reference_pass(
                name, masks, meta, frames, anchors,
                want_frames=want_frames, want_apu=want_apu, want_save=want_save,
            )
        ref_meta = session.build_reference(name, masks, frames, pokes=meta["pokes"], save=meta["save"],
                                           printer=meta["printer"])
        lag_path = ROOT / ref_meta["directory"] / "lag.txt"
        printer_dir = lane / "printer" if meta["printer"] else None
        native = native_pass(
            name, count, anchors, lag_path, lane,
            pcm_out=(lane / "native.pcm") if want_pcm else None, printer_dir=printer_dir,
        )
        pages = compare_pages(printer_dir, reference["anchors"][count].get("pages", [])) if printer_dir else None
        if want_pcm:
            native_pcm = (lane / "native.pcm").read_bytes()
    tables = session.mask_tables()
    census: dict[str, dict[str, int]] = {}
    failures: list[str] = []
    for field in spec.fields:
        if field in {"timer_frame_counters", "apu_trace"}:
            continue
        compared = 0
        differing = 0
        for ordinal in anchors:
            diff = compare_anchor(
                field, ordinal, native[ordinal], reference["anchors"][ordinal],
                reference["stable"].get(ordinal, False), tables, masks,
            )
            if diff is None:
                continue
            compared += 1
            differing += diff
        census[field] = {"anchors": compared, "differing": differing}
        if compared == 0 or differing:
            failures.append(f"{field}: {differing} differing over {compared} anchors")
    if "pcm" in spec.checks:
        pcm = compare_pcm(reference_pcm, reference["anchor_samples"], native_pcm, count)
        row["pcm"] = pcm
        census["apu_pcm"] = {"anchors": pcm["windows"], "differing": 0 if pcm["status"] == "PASS" else 1}
        if pcm["status"] != "PASS":
            failures.append(
                f"pcm: median cosine {pcm['median_cosine']}, agreeing {pcm['agreeing_fraction']}, "
                f"envelope {pcm['envelope_correlation']}"
            )
    if "script_opcodes" in spec.checks and name == spec.sessions[0]:
        opcodes = script_opcode_coverage()
        row["script_opcodes"] = opcodes
        census["script_opcodes"] = {"anchors": opcodes["handlers"], "differing": len(opcodes["unwitnessed"])}
        if opcodes["status"] != "PASS":
            failures.append(f"script opcodes without a red witness: {len(opcodes['unwitnessed'])}")
    if "duel_finished" in spec.checks:
        finished = min(int(meta["duel_finished_ordinal"]) + 1, count)
        flag = native[finished]["wram"][DUEL_FINISHED_OFFSET]
        row["duel_finished"] = {"ordinal": finished, "flag": flag}
        if not flag:
            failures.append(f"duel outcome flag clear at ordinal {finished}")
    if "pages" in spec.checks:
        if pages is None:
            failures.append("session has no printer on the link")
        else:
            row["pages"] = pages
            census["printer_pages"] = {"anchors": pages["reference_pages"], "differing": len(pages["mismatched"])}
            if pages["status"] != "PASS":
                failures.append(f"printer pages: {pages['detail']}")
    if "timer_frame_counters" in fields:
        census["timer_frame_counters"] = {
            "anchors": count,
            "differing": int(report.get("schedule_mismatches") or 0),
        }
    if "apu_trace" in fields:
        apu = compare_apu_trace(native[count], reference["apu_writes"])
        apu["ordinals"] = min(count, APU_TRACE_ORDINALS)
        row["apu_trace"] = apu
        census["apu_trace"] = {"anchors": apu["reference_writes"], "differing": 0 if apu["status"] == "PASS" else 1}
        if apu["status"] != "PASS":
            failures.append(f"apu_trace: first mismatch at write {apu['first_mismatch']}")
    runtime = native[count].get("runtime", {})
    observed = event_names(int(runtime.get("event_mask", 0)))
    row["events"] = {"count": int(runtime.get("events", 0)), "observed": observed}
    row["frames"] = int(runtime.get("frames", 0))
    if spec.event and spec.event not in observed:
        failures.append(f"native never marked {spec.event}")
    row["anchors"] = anchors
    row["census"] = census
    row["status"] = "PASS" if not failures else "FAIL"
    if failures:
        row["failures"] = failures
    return row


LINK_ONLY_SCRIPT_COMMANDS = frozenset({"ScriptCommand_BattleCenter", "ScriptCommand_GiftCenter"})
COVERAGE_LEDGER = ROOT / "site" / "data" / "coverage.json"
RATCHET = ROOT / "tools" / "completion" / "session_ratchet.json"


RECEIPTS = ROOT / "tools" / "oracle" / "mutation_receipts"


def script_opcode_coverage() -> dict[str, Any]:
    ledger = json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8"))
    ratchet = json.loads(RATCHET.read_text(encoding="utf-8"))
    order = ledger["session_order"]
    clean = set()
    for path in (ROOT / "tests" / "sessions").glob("*/session.json"):
        meta = json.loads(path.read_text(encoding="utf-8"))
        if ratchet.get(path.parent.name, {}).get("confirmed_ordinal") == meta.get("ordinals"):
            clean.add(path.parent.name)
    handlers = {name: row for name, row in ledger["routines"].items() if name.startswith("ScriptCommand_")}
    routed = sorted(
        name for name, row in handlers.items()
        if any(order[index] in clean for index in row.get("sessions", []))
    )
    unwitnessed = []
    for name in handlers:
        receipt = RECEIPTS / f"{name}.json"
        try:
            status = json.loads(receipt.read_text(encoding="utf-8")).get("status")
        except (OSError, json.JSONDecodeError):
            status = None
        if status != "RED":
            unwitnessed.append(name)
    unrouted = sorted(
        name for name in handlers
        if name not in routed and name not in LINK_ONLY_SCRIPT_COMMANDS and not handlers[name].get("excluded")
    )
    return {
        "handlers": len(handlers),
        "witnessed": len(handlers) - len(unwitnessed),
        "unwitnessed": sorted(unwitnessed),
        "routed": len(routed),
        "unrouted": unrouted,
        "unmeasurable": sorted(name for name, row in handlers.items() if row.get("unmeasurable")),
        "link_only": sorted(LINK_ONLY_SCRIPT_COMMANDS & set(handlers)),
        "status": "PASS" if not unwitnessed else "FAIL",
    }


def corpus_entry(name: str) -> dict[str, str]:
    directory = session.session_dir(name)
    entry = {
        "session": name,
        "input": str((directory / "input.txt").relative_to(ROOT)),
        "path": str((directory / "session.json").relative_to(ROOT)),
    }
    for key, file_name in (("pokes", "pokes.txt"), ("save", session.SAVE_FILE)):
        if (directory / file_name).is_file():
            entry[key] = str((directory / file_name).relative_to(ROOT))
    return entry


def corpus_for(sessions: tuple[str, ...]) -> list[dict[str, str]]:
    return [corpus_entry(name) for name in sessions]


def corpus(scenario: str) -> list[dict[str, str]]:
    return corpus_for(SPECS[scenario].sessions)


def run(scenario: str) -> dict[str, Any]:
    spec = SPECS[scenario]
    rows = [witness_session(name, spec) for name in spec.sessions]
    passed = all(row["status"] == "PASS" for row in rows)
    linked = any(session.load_session(name)[1]["printer"] or session.load_session(name)[1]["link"]
                 for name in spec.sessions)
    fragment: dict[str, Any] = {
        "oracles": ["linked-reference" if linked else "gambatte", "native"],
        "state_fields": list(spec.fields),
        "frames": sum(row.get("frames", 0) for row in rows),
        "events": sum(row.get("events", {}).get("count", 0) for row in rows),
        "comparison": {
            "status": "PASS" if passed else "FAIL",
            "axis": "doframe-ordinal",
            "sessions": rows,
        },
        "session_sha256": hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }
    if passed:
        fragment["status"] = "PASS"
        fragment["terminal_event"] = spec.terminal
    else:
        fragment["status"] = "FAIL"
        fragment["failure"] = "SESSION_WITNESS_MISMATCH"
        fragment["detail"] = "; ".join(
            f"{row['name']}: " + "; ".join(row.get("failures") or [json.dumps(row.get("verify"))])
            for row in rows
            if row["status"] != "PASS"
        )
    return fragment


NEGATIVES: dict[str, tuple[str, int, int]] = {
    "boot-title-negative": ("boot-menu", 600, 0x01),
}


def first_mismatch(native: dict[str, bytes], reference: dict[str, bytes]) -> dict[str, Any] | None:
    tables = session.mask_tables()
    for region in session.REGIONS[: session.GATED]:
        table = tables[region]
        left, right = native[region], reference[region]
        for offset in range(min(len(left), len(right))):
            if table[offset] or left[offset] == right[offset]:
                continue
            field, field_offset = session.region_field(region, offset)
            symbol, _base = refstream.resolve_region(field, field_offset)
            return {
                "field": field,
                "offset": field_offset,
                "symbol": symbol,
                "native": left[offset],
                "reference": right[offset],
            }
    return None


def negative(scenario: str, evidence_dir: Path, requirement: str) -> dict[str, Any]:
    name, at, bits = NEGATIVES[scenario]
    masks, meta = session.load_session(name)
    count = len(masks)
    frames = session.reference_frames(masks, meta)
    ref_meta = session.build_reference(name, masks, frames, pokes=meta["pokes"], save=meta["save"])
    reference = session.load_reference(ref_meta)
    lag_path = ROOT / ref_meta["directory"] / "lag.txt"
    perturbed = list(masks)
    for ordinal in range(at - 1, min(count, at + 7)):
        perturbed[ordinal] |= bits
    fragment: dict[str, Any] = {
        "oracles": ["gambatte", "native"],
        "state_fields": ["first_mismatch_region", "first_mismatch_offset", "replay_artifact"],
        "frames": count,
        "events": 0,
        "status": "FAIL",
    }
    with tempfile.TemporaryDirectory(prefix=f"witness-negative-{name}-") as directory:
        lane = Path(directory)
        input_path = lane / "input.txt"
        input_path.write_text("\n".join(str(value) for value in perturbed) + "\n", encoding="utf-8")
        for file_name in ("pokes.txt", session.SAVE_FILE):
            source = session.session_dir(name) / file_name
            if source.is_file():
                (lane / file_name).write_bytes(source.read_bytes())
        mask_path = lane / "mask.txt"
        mask_path.write_text(session.mask_text())
        digest_path = lane / "native.bin"
        _state, failure, _off = session.run_native(
            lane, input_path, count, lag_path=lag_path, digest_out=digest_path, mask_path=mask_path
        )
        native_digests = digest_path.read_bytes() if digest_path.is_file() else b""
        ordinal, reached, regions, _audio = session.first_divergence(reference, native_digests)
        if ordinal is None:
            fragment["failure"] = "NO_MISMATCH_FOUND"
            fragment["detail"] = (
                f"perturbing {name} at ordinal {at} left {reached} ordinals byte-identical: {failure[-200:]}"
            )
            return fragment
        capture = lane / "capture"
        capture.mkdir()
        state_path, capture_failure, _off = session.run_native(
            capture, input_path, ordinal, lag_path=lag_path, dump_ordinals=[ordinal]
        )
        dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
        if not dump_path.is_file():
            raise WitnessError(f"no native dump at ordinal {ordinal}: {capture_failure[-300:]}")
        native_state = session.native_regions(json.loads(dump_path.read_text(encoding="utf-8")))
        digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    reference_state = session.reference_capture(name, masks, frames, ordinal, meta["pokes"], save=meta["save"])
    finding = first_mismatch(native_state, reference_state)
    if finding is None:
        fragment["failure"] = "MISMATCH_UNATTRIBUTED"
        fragment["detail"] = f"digests diverge at ordinal {ordinal} in {regions} but no compared byte differs"
        return fragment
    replay = {
        "schema": "negative-evidence-replay-v1",
        "scenario": scenario,
        "session": name,
        "perturbation": {"ordinal": at, "ordinals": 8, "mask_bits": bits},
        "native_input_sha256": digest,
        "first_mismatch_ordinal": ordinal,
        "regions": regions,
        "finding": finding,
    }
    replay_path = evidence_dir / f"{requirement}.replay.json"
    replay_path.write_text(json.dumps(replay, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    fragment.update(
        {
            "status": "PASS",
            "terminal_event": "FIRST_MISMATCH",
            "events": 1,
            "comparison": {"status": "PASS", "kind": "first-mismatch", "regions": regions},
            "first_mismatch_frame": ordinal,
            "first_mismatch_region": finding["field"],
            "first_mismatch_offset": finding["offset"],
            "first_mismatch_symbol": finding["symbol"],
            "replay_artifact": str(replay_path.relative_to(ROOT)),
        }
    )
    return fragment
