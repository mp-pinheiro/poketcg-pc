"""Live duel states captured from the reference for fixture-backed cases.

`practice-win-attack-entry.json` is tools/completion/pilot.py session
`practice-win` at DoFrame 35383, the entry of PlayAttackAnimation_DealAttackDamage:
Goldeen's Horn Attack on Sam's Machop in turn 1 of the practice duel. Whole
WRAM, HRAM and VRAM bank 0 are seeded so a routine runs exactly as the game
does, and `keys` taps A through every text box it opens. The observations
cover both duelists' variables, the damage/effect working area and the
redrawn BG map.
"""
import json
from pathlib import Path

_ATTACK = json.load(open(Path(__file__).resolve().parent.parent / "fixtures" / "practice-win-attack-entry.json"))
_ATTACK_WRAM = bytes.fromhex(_ATTACK["wram"])
_ATTACK_HRAM = bytes.fromhex(_ATTACK["hram"])
_ATTACK_VRAM = bytes.fromhex(_ATTACK["vram0"])
ATTACK_REGS = _ATTACK["regs"]

# wIE ($CAB7) mirrors rIE, which each reference lane arms for itself.
# Frame counters advanced inside key waits: wVBlankCounter ($CAB8),
# wCursorBlinkCounter ($CD0F) and wCheckMenuCursorBlinkCounter ($CEA3), and
# wFlushPaletteFlags ($CABF) and wVBlankOAMCopyToggle ($CAC0), which the
# VBlank ISR consumes. The PyBoy lane
# skips the VBlank halt, so its waits run many DoFrames per tick and these can
# never agree with the native lane: timing phase, unseeded and uncompared. $CFF0-$CFF5 and $DC30-$DCFF are the oracle's synthesized call
# frame (tools/oracle/pyboy_oracle.py RESERVED); $DD80+ is the sound driver's.
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCD0F, 0xCEA3)
_SPANS = ((0xC000, 0xCFF0), (0xD000, 0xDC30), (0xDD00, 0xDD80))


def attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    """The attack-entry state with `changes` ({"C3C8": bytes} hex addresses)
    patched in, as a case body. `vram=False` leaves VRAM unseeded and
    uncompared, for a routine that returns mid-frame: the gbref lane's PPU
    answers $FF to a VRAM read during mode 3. `bank` seeds hBankROM for a
    banked routine: the reference leaves the routine's own bank selected at
    its `ret` and the probe's bank guard restores the entry value, so seeding
    the routine's bank is the one value both lanes exit with. A home routine
    keeps the captured value; PyBoy needs the shadow consistent with the
    mapped bank or the first bank restore maps garbage."""
    wram = bytearray(_ATTACK_WRAM)
    hram = bytearray(_ATTACK_HRAM)
    for addr, data in changes.items():
        address = int(addr, 16)
        if address >= 0xFF80:
            hram[address - 0xFF80:address - 0xFF80 + len(data)] = data
        else:
            wram[address - 0xC000:address - 0xC000 + len(data)] = data
    spans = {}
    for start, end in _SPANS:
        cursor = start
        for hole in sorted(_HOLES):
            if start <= hole < end:
                spans[cursor] = bytes(wram[cursor - 0xC000:hole - 0xC000])
                cursor = hole + 1
        spans[cursor] = bytes(wram[cursor - 0xC000:end - 0xC000])
    if bank is not None:
        hram[0] = bank
    # $FFB8-$FFFE is the unused HRAM tail (hram.asm `ds $38`); the gbref
    # runner's setup calls run on a stack up there.
    spans[0xFF80] = bytes(hram[:0x38])
    if vram:
        spans[0x8000] = _ATTACK_VRAM
    # rLCDC from the game's own wLCDC mirror: the gbref lane runs a real PPU,
    # and with the LCD off its first `halt` would wait for a VBlank forever.
    spans[0xFF40] = bytes([_ATTACK_WRAM[0xCABB - 0xC000]])
    # The game's own SP: the gbref lane otherwise parks the stack at $FFFE, and
    # this call depth plus real interrupt frames would grow it down through
    # hKeysHeld and the rest of HRAM.
    case = {"wram": spans, "entry_sp": _ATTACK["sp"],
            "read": {0xC200: 0x200, 0xCC00: 0x100},
            "keys": [0x00, 0x01], "instruction_budget": 40000000, "cycle_budget": 160000000}
    if vram:
        case["vread"] = {0: {0x9800: 0x400}}
    return case
