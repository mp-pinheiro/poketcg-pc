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

import io
import os
import sys
import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from pyboy import PyBoy

# The deep stack lives in the unallocated $D69C-$DD7F gap in pret's WRAM map.
# It used to occupy $CF30-$CFFF, hiding live deck/card scratch symbols from the
# oracle. Measured stack low-water over the 31 largest routines was 86 bytes
# below entry SP; this window provides 143 bytes below STACK_TOP.
#
# PyBoy can hook execution only in fixed WRAM, not $D000-$DFFF. Keep the tiny
# sentinel/spin stub at its original fixed-WRAM address for immediate capture;
# only the stack moves. The stub overlaps six bytes of wNamingScreenBuffer, but
# every deck/card blocker symbol through $CFD2 remains case-addressable.
SENTINEL = 0xCFF0
SPIN = 0xCFF4
STACK_TOP = 0xDCC0

RESERVED = (range(0xCFF0, 0xCFF6), range(0xDC30, 0xDD00))


def _reserved_overlap(address: int, size: int) -> range | None:
    return next((region for region in RESERVED
                 if address < region.stop and address + size > region.start), None)

WRAM_BASE, WRAM_END = 0xC000, 0xE000
HRAM_BASE, HRAM_END = 0xFF80, 0x10000
SRAM_BASE, SRAM_END = 0xA000, 0xC000
VRAM_BASE, VRAM_END = 0x8000, 0xA000
OAM_BASE, OAM_END = 0xFE00, 0xFEA0
IO_BASE, IO_END = 0xFF00, 0xFF80

MAX_FRAMES = 240  # a home-bank leaf that has not returned by now never will

# Frames bound emulated time, not wall clock, and the two come apart when a
# frame never finishes: `mb.tick` spins on `while not lcd.frame_done` while
# `PyBoy._tick` re-enters it per breakpoint, and `PyBoy.tick` holds
# `cython.nogil` throughout, so neither the frame loop below nor a Python
# signal handler ever regains control. Seven such processes were once left
# pinned to a core for 12 CPU-hours after their driver died.
#
# Two guards. The loop checks a deadline between frames, which is graceful: the
# routine fails as a timeout and the run continues to the next case. The
# watchdog thread covers the case the loop cannot see, a single frame that
# never returns; it runs precisely because `nogil` released the GIL, and it
# hard-exits rather than raising, because there is no thread left to raise on.
#
# The budget is per allotted frame (measured cost is ~10 ms/frame, so 0.25 s is
# 25x headroom) with a floor for short cases, and stays under the 1800 s cap
# `tools/factory/common.py:run_bounded` puts on the whole diff command.
WALL_FLOOR = float(os.environ.get("POKETCG_ORACLE_WALL_FLOOR", "120"))
WALL_PER_FRAME = 0.25
WATCHDOG_GRACE = 30.0

_watchdog_deadline = 0.0
_watchdog_armed_at = 0.0
_watchdog_symbol = ""
_watchdog_running = False


def _watchdog_loop() -> None:
    while True:
        time.sleep(1.0)
        deadline = _watchdog_deadline
        if deadline and time.monotonic() > deadline:
            # Shaped for verify.py's TIMEOUT_MARK so the verdict names the spinner.
            sys.stderr.write(
                f"OracleError: {_watchdog_symbol} did not return within "
                f"{deadline - _watchdog_armed_at:.0f}s of wall clock; the PyBoy "
                f"frame is wedged and holds nogil, so the process is exiting\n")
            sys.stderr.flush()
            os._exit(3)


def _arm_watchdog(symbol: str, cap: float) -> None:
    global _watchdog_deadline, _watchdog_symbol, _watchdog_running, _watchdog_armed_at
    if not _watchdog_running:
        threading.Thread(target=_watchdog_loop, name="oracle-watchdog",
                         daemon=True).start()
        _watchdog_running = True
    _watchdog_symbol = symbol
    _watchdog_armed_at = time.monotonic()
    _watchdog_deadline = _watchdog_armed_at + cap + WATCHDOG_GRACE


def _disarm_watchdog() -> None:
    global _watchdog_deadline
    _watchdog_deadline = 0.0


# hKeysHeld bit order (src/constants/hardware.inc): bit0 A, 1 B, 2 SELECT, 3 START,
# 4 RIGHT, 5 LEFT, 6 UP, 7 DOWN.
BUTTONS = ("a", "b", "select", "start", "right", "left", "up", "down")



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
    io: bytes = field(repr=False)

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
        if IO_BASE <= addr and addr + n <= IO_END:
            off = addr - IO_BASE
            data = bytearray(self.io[off:off + n])
            for i in range(n):
                io_addr = addr + i
                if io_addr == 0xFF02:
                    data[i] |= 0x7C
                elif io_addr == 0xFF0F:
                    data[i] |= 0xE0
                elif io_addr == 0xFF56:
                    data[i] = 0x3E | (data[i] & 0x01)
            return bytes(data)
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
        self._armed_addr: int | None = None
        self._armed_bank: int = 0
        self._key_timeline: list[int] = [0]
        self._baseline = io.BytesIO()
        self._reset_ram()
        self.pyboy.save_state(self._baseline)

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
            io=bytes(pb.memory[IO_BASE:IO_END]),
        )
        rf.PC = SPIN

    def _disarm(self) -> None:
        if self._armed_addr is not None:
            try:
                self.pyboy.hook_deregister(self._armed_bank, self._armed_addr)
            except (ValueError, KeyError):
                pass
        self._armed_addr = None
        self._armed_bank = 0

    def _arm(self, addr: int, bank: int = 0) -> None:
        # PyBoy keys ROM hooks on (bank, address). A hook in the switchable
        # $4000-$7FFF window only fires while that bank is mapped, so a pre-ret
        # completion pc in banked ROM must name the routine's own bank.
        self._disarm()
        self.pyboy.hook_register(bank, addr, self._capture, None)
        self._armed_addr = addr
        self._armed_bank = bank

    def _reset_ram(self) -> None:
        pb = self.pyboy
        pb.memory[WRAM_BASE:WRAM_END] = [0] * (WRAM_END - WRAM_BASE)
        pb.memory[HRAM_BASE:HRAM_END] = [0] * (HRAM_END - HRAM_BASE)
        pb.memory[0xFF0F] = 0  # IF
        pb.memory[0xFFFF] = 0x00
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

    _VBLANK_HALT = 0x0270
    _VBLANK_NOP = 0x0271
    _WVBLANK_COUNTER = 0xCAB8

    def _service_vblank(self, _ctx) -> None:
        pb = self.pyboy
        pb.memory[self._WVBLANK_COUNTER] = (pb.memory[self._WVBLANK_COUNTER] + 1) & 0xFF
        self.pyboy.register_file.PC = self._VBLANK_NOP

    def _apply_keys(self, old: int, new: int) -> None:
        """Emit only the button edges that actually changed between two frames."""
        pb = self.pyboy
        for bit, button in enumerate(BUTTONS):
            was, now = old & (1 << bit), new & (1 << bit)
            if was == now:
                continue
            if now:
                pb.button_press(button)
            else:
                pb.button_release(button)

    def _run(self, symbol: str, regs: dict, stop_pc: int | None = None,
             stack: Sequence[int] | None = None, cycle: bool = False,
             hbank_rom: int | None = None, frames: int | None = None,
             post_call_byte: int | None = None) -> Result:
        """Drive one routine to its requested completion point."""
        pb = self.pyboy
        fn_bank, addr = pb.symbol_lookup(symbol)

        if fn_bank != 0:
            pb.memory[0x2000] = fn_bank & 0xFF
            pb.memory[0x3000] = (fn_bank >> 8) & 1
            pb.memory[0xFF80] = fn_bank & 0xFF
        # A routine that re-reads hBankROM as data cannot be tested against its
        # own symbol bank, so let the case name the value without disturbing the
        # $4000-$7FFF paging above.
        if hbank_rom is not None:
            pb.memory[0xFF80] = hbank_rom & 0xFF
        pb.memory[SPIN] = 0x18  # jr
        pb.memory[SPIN + 1] = 0xFE  # -2
        words = list(stack or ())
        if len(words) > 4:
            raise OracleError("stack declares more than 4 caller-pushed words")
        pb.memory[STACK_TOP - 2] = SENTINEL & 0xFF
        pb.memory[STACK_TOP - 1] = SENTINEL >> 8
        if post_call_byte is not None:
            pb.memory[SENTINEL] = post_call_byte
        # Caller-pushed saves sit below the return address, in push order, so
        # the routine's first `pop` reads the last word and its `ret` still
        # finds the sentinel underneath. STACK_TOP-2 stays the sentinel slot.
        for index, word in enumerate(words):
            base = STACK_TOP - 4 - 2 * index
            pb.memory[base] = word & 0xFF
            pb.memory[base + 1] = (word >> 8) & 0xFF

        rf = pb.register_file
        rf.SP = STACK_TOP - 2 - 2 * len(words)
        rf.PC = addr
        rf.A = regs.get("a", 0)
        rf.F = regs.get("f", 0)
        rf.B = regs.get("b", 0)
        rf.C = regs.get("c", 0)
        rf.D = regs.get("d", 0)
        rf.E = regs.get("e", 0)
        rf.HL = regs.get("hl", 0)

        self._hit = None
        if stop_pc is None:
            self._arm(SENTINEL + 1 if post_call_byte is not None else SENTINEL)
        else:
            # Home bank ($0000-$3FFF) is always mapped; a banked stop pc must be
            # hooked against the routine's own bank.
            self._arm(stop_pc, 0 if stop_pc < 0x4000 else fn_bank)
        try:
            pb.hook_deregister(0, self._VBLANK_HALT)
        except (ValueError, KeyError):
            pass
        pb.hook_register(0, self._VBLANK_HALT, self._service_vblank, None)
        # One tick is one frame, so this is the frame boundary the reference
        # advances its timeline on (tools/oracle/gbref/runner.c). Cycle modulo the
        # entry count, and only for the routine under test -- runner.c holds entry
        # 0 across every setup call and starts cycling afterwards.
        timeline = self._key_timeline if cycle else [0]
        index, current = 0, timeline[0]
        # MAX_FRAMES's "a home-bank leaf that has not returned by now never will"
        # assumption does not hold for routines that run a card's real effect
        # command: EstimateDamage_VersusDefendingCard needs millions of
        # instructions. A case that declares a large `cycle_budget` is asking for
        # that time, so honour it here instead of failing at a fixed 240.
        budget = frames or MAX_FRAMES
        cap = max(WALL_FLOOR, WALL_PER_FRAME * budget)
        deadline = time.monotonic() + cap
        _arm_watchdog(symbol, cap)
        try:
            for _ in range(budget):
                pb.tick(1, False, False)
                if self._hit is not None:
                    return self._hit
                if time.monotonic() > deadline:
                    raise OracleError(
                        f"{symbol} did not return within {cap:.0f}s of wall clock "
                        f"({budget} frames allotted)")
                if len(timeline) > 1:
                    index = (index + 1) % len(timeline)
                    if timeline[index] != current:
                        self._apply_keys(current, timeline[index])
                        current = timeline[index]
            raise OracleError(
                f"{symbol} did not return within {budget} frames")
        finally:
            _disarm_watchdog()
            try:
                pb.hook_deregister(0, self._VBLANK_HALT)
            except (ValueError, KeyError):
                pass

    def call(self, symbol: str, *, a: int = 0, f: int = 0, b: int = 0, c: int = 0,
             d: int = 0, e: int = 0, hl: int = 0,
             wram: dict[int, bytes] | None = None,
             sram: dict[int, dict[int, bytes]] | None = None,
             ramg: bool | None = None,
             setup: list[dict] | None = None,
             keys: int | Sequence[int] = 0,
             stop_pc: int | None = None,
             stack: Sequence[int] | None = None,
             hbank_rom: int | None = None,
             frames: int | None = None,
             post_call_byte: int | None = None) -> Result:
        pb = self.pyboy
        self._baseline.seek(0)
        pb.load_state(self._baseline)

        # Release every button before pressing the held ones, so a case's `keys`
        # never inherits state left by a previous call. `no_input=True` (set in
        # __init__) only skips the window plugin in `_handle_events`; these API
        # events still reach `mb.buttonevent` on the next tick.
        for button in BUTTONS:
            pb.button_release(button)
        # A schema-2 case may declare `keys` as a cycled per-frame timeline. The
        # run starts on entry 0, exactly as runner.c does; _run cycles the rest.
        self._key_timeline = ([int(k) for k in keys] or [0]) \
            if isinstance(keys, (list, tuple)) else [int(keys)]
        for bit, button in enumerate(BUTTONS):
            if self._key_timeline[0] & (1 << bit):
                pb.button_press(button)

        self._reset_ram()
        for at, data in (wram or {}).items():
            overlap = _reserved_overlap(at, len(data))
            if overlap is not None:
                raise OracleError(
                    f"${at:04X}+{len(data)} overlaps the synthesized call frame "
                    f"(${overlap.start:04X}-${overlap.stop - 1:04X})")
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

        # Some routines need warm state that a single call cannot build -- the text
        # engine's tile cache is a linked list only SetupText makes acyclic. Each
        # setup routine runs to completion here, after every seed, and whatever it
        # leaves in RAM is the entry state for the routine under test.
        for pre in setup or []:
            self._run(pre["fn"], pre)

        # Banked (non-home) routines run out of the $4000-$7FFF window; select the ROM
        # bank exactly as a farcall would, after _reset_ram's power-on bank=1 and before
        # jumping in. Home-bank (0) routines already sit in the always-mapped $0000-$3FFF.
        return self._run(
            symbol,
            {"a": a, "f": f, "b": b, "c": c, "d": d, "e": e, "hl": hl},
            stop_pc,
            stack,
            cycle=True,
            hbank_rom=hbank_rom,
            frames=frames,
            post_call_byte=post_call_byte,
        )
