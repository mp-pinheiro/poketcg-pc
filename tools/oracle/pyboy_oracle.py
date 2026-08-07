"""Per-function oracle: run one home-bank routine on PyBoy and capture the exit state.

PyBoy 2.7.0 has no run-to-return API, so a call frame is synthesized: push a
sentinel return address, point PC at the routine, and hook the sentinel. Four
details are load-bearing and were each confirmed against PyBoy 2.7.0:

1. $FF50 must be written before invoking. PyBoy always maps a boot ROM, and the
   CGB boot ROM shadows $0200-$08FF, which covers most of these routines
   (UpdateRNGSources sits at $089B).
2. The sentinel and spin addresses must live in $C000-$CFFF. mb.breakpoint_add
   pokes ram.internal_ram0 directly, which is only correct for WRAM bank 0.
3. There are no individual H/L registers on PyBoyRegisterFile, only HL.
4. The F setter masks with $F0, and pyboy.mb is not reachable on the compiled
   wheel, so everything here goes through the public PyBoy surface.

The callback fires with PC still at the sentinel; it captures state and parks PC
on a `jr -2` spin so the remainder of the frame cannot disturb the snapshot.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from pyboy import PyBoy

SENTINEL = 0xCFF0  # return address pushed for the routine under test
SPIN = 0xCFF4  # `jr -2`, parked here once the snapshot is taken
STACK_TOP = 0xCF00  # frame grows down from here

# Cases must not use this window: it holds the synthesized frame and its stack.
RESERVED = range(0xCE00, 0xD000)

WRAM_BASE, WRAM_END = 0xC000, 0xE000
HRAM_BASE, HRAM_END = 0xFF80, 0x10000
SRAM_BASE, SRAM_END = 0xA000, 0xC000
VRAM_BASE, VRAM_END = 0x8000, 0xA000
OAM_BASE, OAM_END = 0xFE00, 0xFEA0

MAX_FRAMES = 240  # a home-bank leaf that has not returned by now never will


def _read_bank(pb: PyBoy, bank: int, base: int, end: int) -> bytes:
    """One whole 8 KiB banked region (SRAM $A000-$BFFF or CGB VRAM $8000-$9FFF).

    PyBoy's banked reader bounds the slice with `stop < 0x2000` while its writer uses
    `stop <= 0x2000` (pyboy/pyboy.py PyBoyMemoryView.__getitem, both the
    `start < 0xA000` and `start < 0xC000` branches), so a full base-end slice raises.
    Read all but the last byte as a slice and fetch the final byte on its own.
    """
    body = pb.memory[bank, base:end - 1]
    return bytes(body) + bytes([pb.memory[bank, end - 1]])


@dataclass
class Result:
    a: int
    f: int
    b: int
    c: int
    d: int
    e: int
    hl: int
    sp: int
    pc: int
    wram: bytes = field(repr=False)
    hram: bytes = field(repr=False)
    sram: bytes = field(repr=False)
    sram_banks: tuple[bytes, ...] = field(repr=False)
    vram: bytes = field(repr=False)
    vram_banks: tuple[bytes, ...] = field(repr=False)
    oam: bytes = field(repr=False)

    def mem(self, addr: int, n: int = 1, *, bank: int | None = None) -> bytes:
        if VRAM_BASE <= addr and addr + n <= VRAM_END:
            off = addr - VRAM_BASE
            src = self.vram_banks[bank] if bank is not None else self.vram
            return src[off:off + n]
        if WRAM_BASE <= addr and addr + n <= WRAM_END:
            off = addr - WRAM_BASE
            return self.wram[off:off + n]
        if OAM_BASE <= addr and addr + n <= OAM_END:
            off = addr - OAM_BASE
            return self.oam[off:off + n]
        if HRAM_BASE <= addr and addr + n <= HRAM_END:
            off = addr - HRAM_BASE
            return self.hram[off:off + n]
        if SRAM_BASE <= addr and addr + n <= SRAM_END:
            off = addr - SRAM_BASE
            if bank is not None:
                return self.sram_banks[bank][off:off + n]
            return self.sram[off:off + n]
        raise ValueError(
            f"address ${addr:04X}+{n} is outside the captured VRAM/WRAM/OAM/HRAM/SRAM snapshot")


class OracleError(RuntimeError):
    pass


class Oracle:
    def __init__(self, rom: str | os.PathLike, symbols: str | os.PathLike | None = None):
        rom = str(rom)
        if symbols is None:
            guess = Path(rom).with_suffix(".sym")
            if not guess.exists():
                raise OracleError(f"no symbol file next to {rom} (expected {guess})")
            symbols = guess
        self.pyboy = PyBoy(
            rom,
            window="null",
            sound_emulated=False,
            symbols=str(symbols),
            no_input=True,
            log_level="CRITICAL",
        )
        self._hit: Result | None = None

    def close(self) -> None:
        self.pyboy.stop(save=False)

    def __enter__(self) -> "Oracle":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()

    def _capture(self, _ctx) -> None:
        pb = self.pyboy
        rf = pb.register_file
        pb.memory[0x0000] = 0x0A
        self._hit = Result(
            a=rf.A, f=rf.F, b=rf.B, c=rf.C, d=rf.D, e=rf.E,
            hl=rf.HL, sp=rf.SP, pc=rf.PC,
            wram=bytes(pb.memory[WRAM_BASE:WRAM_END]),
            hram=bytes(pb.memory[HRAM_BASE:HRAM_END]),
            sram=bytes(pb.memory[SRAM_BASE:SRAM_END]),
            sram_banks=tuple(_read_bank(pb, bank, SRAM_BASE, SRAM_END) for bank in range(4)),
            vram=bytes(pb.memory[VRAM_BASE:VRAM_END]),
            vram_banks=tuple(_read_bank(pb, bank, VRAM_BASE, VRAM_END) for bank in range(2)),
            oam=bytes(pb.memory[OAM_BASE:OAM_END]),
        )
        rf.PC = SPIN

    def _arm(self) -> None:
        # The hook is keyed on the opcode saved at registration time, and firing
        # removes the breakpoint. Re-arming from a known byte keeps that key stable.
        try:
            self.pyboy.hook_deregister(0, SENTINEL)
        except ValueError:
            pass
        self.pyboy.memory[SENTINEL] = 0x00
        self.pyboy.hook_register(0, SENTINEL, self._capture, None)

    def _reset_ram(self) -> None:
        pb = self.pyboy
        pb.memory[WRAM_BASE:WRAM_END] = [0] * (WRAM_END - WRAM_BASE)
        pb.memory[HRAM_BASE:HRAM_END] = [0] * (HRAM_END - HRAM_BASE)
        pb.memory[0xFF0F] = 0  # IF
        pb.memory[0xFF50] = 0x11  # unmap the boot ROM
        # One Oracle instance serves the whole run; the banked setter writes
        # rambanks[bank, x] directly (bypassing RAMG), so every bank is cleared
        # here regardless of which one is selected, matching mem_reset() on the C side.
        for bank in range(4):
            pb.memory[bank, SRAM_BASE:SRAM_END] = 0
        for bank in range(2):
            pb.memory[bank, VRAM_BASE:VRAM_END] = 0
        pb.memory[OAM_BASE:OAM_END] = [0] * (OAM_END - OAM_BASE)
        pb.memory[0xFF4F] = 0  # VBK: VRAM bank 0
        # Writes below $8000 are MBC commands, not memory writes, so a routine that
        # walks the whole address space (a 64 KiB copy) leaves the cartridge banked
        # somewhere else. Restore MBC5 power-on state so cases cannot leak into
        # each other; this matches mem_reset() on the C side.
        pb.memory[0x0000] = 0x00  # SRAM disable
        pb.memory[0x2000] = 0x01  # ROM bank low
        pb.memory[0x3000] = 0x00  # ROM bank high
        pb.memory[0x4000] = 0x00  # SRAM bank

    def call(self, symbol: str, *, a: int = 0, f: int = 0, b: int = 0, c: int = 0,
             d: int = 0, e: int = 0, hl: int = 0,
             wram: dict[int, bytes] | None = None,
             sram: dict[int, dict[int, bytes]] | None = None,
             ramg: bool | None = None) -> Result:
        pb = self.pyboy
        fn_bank, addr = pb.symbol_lookup(symbol)

        self._reset_ram()
        for at, data in (wram or {}).items():
            if any(x in RESERVED for x in range(at, at + len(data))):
                raise OracleError(
                    f"${at:04X}+{len(data)} overlaps the synthesized call frame "
                    f"(${RESERVED.start:04X}-${RESERVED.stop - 1:04X})")
            for i, byte in enumerate(data):
                pb.memory[at + i] = byte

        for bank, spans in (sram or {}).items():
            pb.memory[0x0000] = 0x0A
            pb.memory[0x4000] = bank & 0xFF
            for at, data in spans.items():
                for i, byte in enumerate(data):
                    pb.memory[at + i] = byte

        # Seeding SRAM enables the latch as a side effect, so a case that needs to
        # enter with non-zero SRAM and RAM disabled -- the only way a routine's own
        # EnableSRAM becomes observable -- forces it back here, after every seed.
        if ramg is not None:
            pb.memory[0x0000] = 0x0A if ramg else 0x00

        # Banked (non-home) routines run out of the $4000-$7FFF window; select the ROM
        # bank exactly as a farcall would, after _reset_ram's power-on bank=1 and before
        # jumping in. Home-bank (0) routines already sit in the always-mapped $0000-$3FFF.
        if fn_bank != 0:
            pb.memory[0x2000] = fn_bank & 0xFF
            pb.memory[0x3000] = (fn_bank >> 8) & 1
        pb.memory[SPIN] = 0x18  # jr
        pb.memory[SPIN + 1] = 0xFE  # -2
        pb.memory[STACK_TOP - 2] = SENTINEL & 0xFF
        pb.memory[STACK_TOP - 1] = SENTINEL >> 8

        rf = pb.register_file
        rf.SP = STACK_TOP - 2
        rf.PC = addr
        rf.A, rf.F, rf.B, rf.C, rf.D, rf.E, rf.HL = a, f, b, c, d, e, hl

        self._hit = None
        self._arm()
        for _ in range(MAX_FRAMES):
            pb.tick(1, False, False)
            if self._hit is not None:
                return self._hit
        raise OracleError(f"{symbol} did not return within {MAX_FRAMES} frames")
