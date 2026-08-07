"""Scene-level oracle for the gb-recompiled Game Boy binary."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_BINARY = Path.home() / ".local/share/gbrecompiled/poketcg/poketcg"
REGENERATE_RECIPE = "just oracleb-regenerate"


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

    def run(self, *, input_file: str | os.PathLike | None = None,
            frame_limit: int = 30,
            save_state: str | os.PathLike | None = None) -> Result:
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
            command = [str(self.binary), "--headless", "--no-audio",
                       "--save-dir", str(saves), "--ignore-rtc-persistence"]
            if input_file is not None:
                command += ["--input", str(input_file)]
            command += ["--limit-frames", str(frame_limit), "--dump-state", str(dump)]
            if save_state is not None:
                command += ["--save-state-file", str(Path(save_state).resolve())]
            try:
                completed = subprocess.run(command, capture_output=True, text=True,
                                           timeout=self.timeout, check=False)
            except subprocess.TimeoutExpired as exc:
                raise OracleError(f"gb-recompiled scene timed out after {self.timeout}s") from exc
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise OracleError(f"gb-recompiled scene failed ({completed.returncode}): {detail}")
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
        return Result(*(state[key] for key in required[:11]), state=state)

    def __enter__(self) -> "Oracle":
        return self

    def __exit__(self, *_exc) -> None:
        return None
