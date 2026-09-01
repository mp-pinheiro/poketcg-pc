"""Scene-level oracle for the gb-recompiled Game Boy binary."""

from __future__ import annotations

import json
import struct
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_BINARY = Path.home() / ".local/share/gbrecompiled/poketcg/poketcg"
REGENERATE_RECIPE = "just oracleb-regenerate"

GBSV_HEADER = struct.Struct("<IIQ9I")
GBSV_MAGIC = 0x56534247
PPU_COLOR_FRAMEBUFFER_OFFSET = 23142
PPU_BG_PALETTE_OFFSET = 161384
PPU_OBJ_PALETTE_OFFSET = 161448
PPU_FRAMEBUFFER_SIZE = 160 * 144


def _full_state(save_state: Path, dump: dict) -> dict:
    raw = save_state.read_bytes()
    if len(raw) < GBSV_HEADER.size:
        raise OracleError("gb-recompiled savestate is truncated")
    header = GBSV_HEADER.unpack_from(raw)
    if header[0] != GBSV_MAGIC:
        raise OracleError("gb-recompiled savestate has invalid magic")
    _, version, _, rom_size, eram_size, wram_size, vram_size, oam_size, hram_size, io_size, ppu_size, apu_size = header
    if version != 9:
        raise OracleError(f"unsupported gb-recompiled savestate version {version}")
    region_sizes = (eram_size, wram_size, vram_size, oam_size, hram_size, io_size, ppu_size, apu_size)
    core_size = len(raw) - GBSV_HEADER.size - sum(region_sizes)
    if core_size < 366:
        raise OracleError("gb-recompiled savestate core is truncated")
    cursor = GBSV_HEADER.size + core_size
    regions: dict[str, bytes] = {}
    for name, size in zip(
        ("eram", "wram", "vram", "oam", "hram", "io", "ppu", "apu"), region_sizes
    ):
        end = cursor + size
        if end > len(raw):
            raise OracleError(f"gb-recompiled savestate {name} region is truncated")
        regions[name] = raw[cursor:end]
        cursor = end
    if cursor != len(raw):
        raise OracleError("gb-recompiled savestate has trailing bytes")
    if wram_size < 0x2000 or vram_size != 0x4000 or hram_size < 0x7F or io_size < 0x81:
        raise OracleError("gb-recompiled savestate memory layout is unsupported")
    if ppu_size < PPU_OBJ_PALETTE_OFFSET + 0x40:
        raise OracleError("gb-recompiled savestate PPU state is truncated")

    wram = regions["wram"][:0x2000]
    vram = regions["vram"]
    io = regions["io"][:0x80]
    hram = regions["hram"][:0x7F] + bytes((regions["io"][0x80],))
    ppu = regions["ppu"]
    color_framebuffer = ppu[
        PPU_COLOR_FRAMEBUFFER_OFFSET:
        PPU_COLOR_FRAMEBUFFER_OFFSET + PPU_FRAMEBUFFER_SIZE * 2
    ]
    state = {
        "wram": list(wram),
        "hram": list(hram),
        "sram_bank_0": list(regions["eram"][0x0000:0x2000]),
        "sram_bank_1": list(regions["eram"][0x2000:0x4000]),
        "sram_bank_2": list(regions["eram"][0x4000:0x6000]),
        "sram_bank_3": list(regions["eram"][0x6000:0x8000]),
        "vram_bank_0": list(vram[:0x2000]),
        "vram_bank_1": list(vram[0x2000:0x4000]),
        "oam": list(regions["oam"]),
        "io": list(io),
        "palette_ram": list(
            ppu[PPU_BG_PALETTE_OFFSET:PPU_BG_PALETTE_OFFSET + 0x40]
            + ppu[PPU_OBJ_PALETTE_OFFSET:PPU_OBJ_PALETTE_OFFSET + 0x40]
        ),
        "mapper_state": {
            "rom_bank": struct.unpack_from("<H", raw, GBSV_HEADER.size + 352)[0],
            "sram_bank": raw[GBSV_HEADER.size + 354],
            "vram_bank": raw[GBSV_HEADER.size + 356],
            "sram_enabled": raw[GBSV_HEADER.size + 358],
        },
        "input_latch": raw[GBSV_HEADER.size + 365],
        "timer_frame_counters": {
            "frames": dump.get("completed_frames", 0),
            "cycles": dump.get("cycles", 0),
        },
        "rng": list(wram[0xACA:0xACD]),
        "apu_state": {"raw": list(regions["apu"])},
        "apu_trace": [],
        "framebuffer": list(struct.unpack("<" + "H" * PPU_FRAMEBUFFER_SIZE, color_framebuffer)),
        "save": list(regions["eram"]),
        "transport": [],
        "printer": [],
        "scratch": [0] * 0x100,
    }
    if rom_size <= 0:
        raise OracleError("gb-recompiled savestate has invalid ROM size")
    return state


@dataclass(frozen=True)
class Result:
    a: int
    f: int
    b: int
    c: int
    d: int
    e: int
    h: int
    l: int
    sp: int
    pc: int
    completed_frames: int
    state: dict

    @property
    def hl(self) -> int:
        return (self.h << 8) | self.l

    def mem(self, addr: int, n: int = 1) -> bytes:
        if n < 0 or addr < 0 or addr + n > 0x10000:
            raise ValueError(f"invalid address range ${addr:04X}+{n}")
        if 0xC000 <= addr and addr + n <= 0xE000:
            data = (self.state["wram_bank_0_c000_cfff"] +
                    self.state["wram_bank_1_d000_dfff"])
            off = addr - 0xC000
            return bytes(data[off:off + n])
        if 0xFF80 <= addr and addr + n <= 0x10000:
            data = self.state["hram_ff80_fffe"]
            off = addr - 0xFF80
            if off + n > len(data):
                raise ValueError("address $FFFF is not present in the scene dump")
            return bytes(data[off:off + n])
        if 0xA000 <= addr and addr + n <= 0xA100:
            data = self.state["eram_a000_a0ff"]
            off = addr - 0xA000
            return bytes(data[off:off + n])
        region = "VRAM" if 0x8000 <= addr < 0xA000 else "OAM" if 0xFE00 <= addr < 0xFEA0 else "IO" if 0xFF00 <= addr < 0xFF80 else "SRAM"
        raise ValueError(f"address ${addr:04X}+{n} is outside the captured {region} snapshot")


class OracleError(RuntimeError):
    pass


class Oracle:
    def __init__(self, binary: str | os.PathLike | None = None, *, timeout: float = 30.0):
        configured = binary or os.environ.get("POKETCG_ORACLEB")
        self.binary = Path(configured) if configured else DEFAULT_BINARY
        self.timeout = timeout
        if not self.binary.is_file():
            raise OracleError(
                f"gb-recompiled binary not found at {self.binary}; set POKETCG_ORACLEB "
                f"or regenerate it with {REGENERATE_RECIPE}")

    def run(
        self,
        *,
        input_file: str | os.PathLike | None = None,
        frame_limit: int = 30,
        save_state: str | os.PathLike | None = None,
        audio_trace: str | os.PathLike | None = None,
    ) -> Result:
        """Run one scene. `save_state`, when given, is where the binary's whole-state
        save is kept -- the JSON dump has no VRAM/OAM/IO, so that file is the only
        route to a full comparison. It is only requested when a caller asks for it;
        writing it into the scratch directory would delete it before anyone could read
        it, which is worse than not producing it at all."""
        if frame_limit < 1:
            raise ValueError("frame_limit must be positive")
        with tempfile.TemporaryDirectory(prefix="poketcg-oracleb-") as directory:
            dump = Path(directory) / "state.json"
            # --save-dir isolates battery RAM per run. Without it the binary persists a
            # save next to itself and the NEXT run loads it, so two replays of the same
            # scene start from different state and diverge. That is the documented
            # stale-save footgun, and it made a 10-frame replay non-reproducible here.
            saves = Path(directory) / "saves"
            saves.mkdir()
            command = [str(self.binary), "--headless",
                       "--save-dir", str(saves), "--ignore-rtc-persistence"]
            if input_file is not None:
                command += ["--input", str(input_file)]
            command += ["--limit-frames", str(frame_limit), "--dump-state", str(dump)]
            if audio_trace is not None:
                command.append("--debug-audio-trace")
            if save_state is not None:
                command += ["--save-state-file", str(Path(save_state).resolve())]
            try:
                completed = subprocess.run(
                    command,
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise OracleError(f"gb-recompiled scene timed out after {self.timeout}s") from exc
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise OracleError(f"gb-recompiled scene failed ({completed.returncode}): {detail}")
            if audio_trace is not None:
                trace_source = Path(directory) / "debug_audio_trace.log"
                if not trace_source.is_file():
                    raise OracleError("gb-recompiled audio trace was not produced")
                Path(audio_trace).write_bytes(trace_source.read_bytes())
            try:
                state = json.loads(dump.read_text())
            except (OSError, json.JSONDecodeError) as exc:
                raise OracleError(f"gb-recompiled did not produce valid state JSON: {exc}") from exc
        required = ("a", "f", "b", "c", "d", "e", "h", "l", "sp", "pc",
                    "completed_frames", "wram_bank_0_c000_cfff",
                    "wram_bank_1_d000_dfff", "hram_ff80_fffe", "eram_a000_a0ff")
        missing = [key for key in required if key not in state]
        if missing:
            raise OracleError(f"gb-recompiled state is missing keys: {', '.join(missing)}")
        if save_state is not None:
            state.update(_full_state(Path(save_state), state))
        return Result(*(state[key] for key in required[:11]), state=state)

    def __enter__(self) -> "Oracle":
        return self

    def __exit__(self, *_exc) -> None:
        return None
