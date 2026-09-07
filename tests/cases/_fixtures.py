"""Live game states captured from the reference for fixture-backed cases.

A fixture is `tools/completion/session.py capture NAME --routine R`: the
reference's registers, SP, WRAM, HRAM and VRAM bank 0 at R's entry while it
replays a recorded session. Seeded whole, a routine runs exactly as the game
does, and `keys` taps A through every text box it opens. The observations
cover both duelists' variables, the damage/effect working area and the
redrawn BG map.

`practice-win-attack-entry.json` is session `practice-win` at DoFrame 35383,
the entry of PlayAttackAnimation_DealAttackDamage: Goldeen's Horn Attack on
Sam's Machop in turn 1 of the practice duel.
"""
import json
from pathlib import Path

# Bytes the two reference lanes cannot agree on with the native lane, left
# unseeded and uncompared. wIE ($CAB7) mirrors rIE, which each lane arms for
# itself. wVBlankCounter ($CAB8), wCursorBlinkCounter ($CD0F) and
# wCheckMenuCursorBlinkCounter ($CEA3) count frames spent in key waits, which
# the PyBoy lane runs many DoFrames per tick (it skips the VBlank halt).
# wFlushPaletteFlags ($CABF) and wVBlankOAMCopyToggle ($CAC0) are consumed by
# the VBlank ISR. Do not widen this for a byte the game computes.
# $CFF0-$CFF5 and $DC30-$DCFF are the PyBoy oracle's synthesized call frame
# (tools/oracle/pyboy_oracle.py RESERVED); $DD80+ is the sound driver's.
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCD0F, 0xCEA3)
_SPANS = ((0xC000, 0xCFF0), (0xD000, 0xDC30), (0xDD00, 0xDD80))


class Fixture:
    """One captured state (`session.py capture NAME --routine R`) as a case
    builder: `Fixture("practice-win-attack-entry").case(**{"C3C8": b"\\x00"})`."""

    def __init__(self, name: str):
        data = json.load(open(Path(__file__).resolve().parent.parent / "fixtures" / f"{name}.json"))
        self.name = name
        self.ordinal = data["ordinal"]
        self.entry = data["entry"]
        self.regs = data["regs"]
        self.sp = data["sp"]
        self.wram = bytes.fromhex(data["wram"])
        self.hram = bytes.fromhex(data["hram"])
        self.vram = bytes.fromhex(data["vram0"])

    def case(self, vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
        """The captured state with `changes` ({"C3C8": bytes} hex addresses)
        patched in, as a case body. `vram=False` leaves VRAM unseeded and
        uncompared, for a routine that returns mid-frame: the gbref lane's PPU
        answers $FF to a VRAM read during mode 3. `bank` seeds hBankROM for a
        banked routine: the reference leaves the routine's own bank selected at
        its `ret` and the probe's bank guard restores the entry value, so
        seeding the routine's bank is the one value both lanes exit with. A home
        routine keeps the captured value; PyBoy needs the shadow consistent
        with the mapped bank or the first bank restore maps garbage."""
        wram = bytearray(self.wram)
        hram = bytearray(self.hram)
        for addr, data in changes.items():
            address = int(addr, 16)
            if address >= 0xFF80:
                hram[address - 0xFF80:address - 0xFF80 + len(data)] = data
            else:
                wram[address - 0xC000:address - 0xC000 + len(data)] = data
        if bank is not None:
            hram[0] = bank
        spans = {}
        for start, end in _SPANS:
            cursor = start
            for hole in sorted(_HOLES):
                if start <= hole < end:
                    spans[cursor] = bytes(wram[cursor - 0xC000:hole - 0xC000])
                    cursor = hole + 1
            spans[cursor] = bytes(wram[cursor - 0xC000:end - 0xC000])
        # $FFB8-$FFFE is the unused HRAM tail (hram.asm `ds $38`); the gbref
        # runner's setup calls run on a stack up there.
        spans[0xFF80] = bytes(hram[:0x38])
        if vram:
            spans[0x8000] = self.vram
        # rLCDC from the game's own wLCDC mirror: the gbref lane runs a real PPU,
        # and with the LCD off its first `halt` would wait for a VBlank forever.
        spans[0xFF40] = bytes([self.wram[0xCABB - 0xC000]])
        # The game's own SP: the gbref lane otherwise parks the stack at $FFFE, and
        # a deep call plus real interrupt frames would grow it down through
        # hKeysHeld and the rest of HRAM.
        case = {"wram": spans, "entry_sp": self.sp,
                "read": {0xC200: 0x200, 0xCC00: 0x100},
                "keys": [0x00, 0x01], "instruction_budget": 40000000, "cycle_budget": 160000000}
        if vram:
            case["vread"] = {0: {0x9800: 0x400}}
        return case


ATTACK = Fixture("practice-win-attack-entry")
ATTACK_REGS = ATTACK.regs


def attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ATTACK.case(vram=vram, bank=bank, **changes)
