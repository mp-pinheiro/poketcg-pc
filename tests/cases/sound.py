"""Oracle-diff cases for poketcg/src/home/sound.asm's tile-plane converters.

Func_37c5 processes exactly 768 source bytes (8x6x8x2) and touches roughly
3266 bytes of destination (de sweeps ~3072 bytes, plus the +$c0/+$c2 write
offsets ahead of it), so every case reads a wide `sread` window. Destinations
sit in SRAM (the real caller, engine/link/printer.asm, targets sGfxBuffer2 =
$a800) so there is no reserved-WRAM collision to worry about. Source `hl`
points into the default-active ROM bank 1 ($4000-$7fff); the routine never
bank-switches itself, so both sides read the same real ROM bytes there.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

SREAD_LEN = 3280

CONTRACT = {
    "Func_37c5": ("a", "d", "e", "hl"),
    "Func_37a5": ("a", "f", "d", "e", "hl"),
}

CASES = {
    "Func_37c5": [
        # All-zero: carry_in clear (f=0), a=0.
        {"hl": 0x4000, "d": 0xA8, "e": 0x00, "ramg": True,
         "sread": {0: {0xA800: SREAD_LEN}}},
        # Same source/dest, carry_in SET this time -- proves the entry carry
        # (undocumented but real, threaded with no reset anywhere in the
        # routine) actually reaches the computed tile data.
        {"hl": 0x4000, "d": 0xAC, "e": 0x00, "f": 0x10, "ramg": True,
         "sread": {0: {0xAC00: SREAD_LEN}}},
        # Different source region and a nonzero starting accumulator.
        {"hl": 0x4200, "d": 0xB0, "e": 0x00, "a": 0x5A, "ramg": True,
         "sread": {0: {0xB000: SREAD_LEN}}},
        dict(POISON, hl=0x4100, d=0xA8, e=0x00, ramg=True,
             sread={0: {0xA800: SREAD_LEN}}),
    ],
    "Func_37a5": [
        # hl's top 3 bits select the CardGraphics bank offset (0 here); the
        # low bits get <<3'd and normalized into $4000-$7fff for Func_37c5.
        {"hl": 0x02A7, "d": 0xA8, "e": 0x00, "ramg": True,
         "sread": {0: {0xA800: SREAD_LEN}}},
        {"hl": 0x1800, "d": 0xA0, "e": 0x00, "ramg": True,
         "sread": {0: {0xA000: SREAD_LEN}}},
        dict(POISON, hl=0x1234, d=0xA8, e=0x00, ramg=True,
             sread={0: {0xA800: SREAD_LEN}}),
    ],
}
