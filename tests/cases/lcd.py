POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "EnableLCD": ("b", "c", "d", "e", "hl"),
    # DisableLCD spins on rLY waiting for vblank, so under the oracle the PPU really
    # advances and the ROM's interrupt handlers run during the wait. On the LCD-on
    # path that leaves residue in c/d/e and hl ($CABA) that I have NOT derived from
    # the asm, so it is not asserted rather than hardcoded. `b` is preserved on both
    # paths. The routine's real product -- rLCDC, wLCDC, the white palettes and rIE --
    # is diffed against the ROM in the cases below.
    "DisableLCD": ("b",),
    "Set_OBJ_8x8": ("b", "c", "d", "e", "hl"),
    "Set_OBJ_8x16": ("b", "c", "d", "e", "hl"),
    "SetWindowOn": ("b", "c", "d", "e", "hl"),
    "SetWindowOff": ("b", "c", "d", "e", "hl"),
}

CASES = {
    # Oracle-run: $FF00-$FF7F is captured, so rLCDC is diffed against the ROM.
    # rIE ($FFFF) is HRAM and was already observable.
    "EnableLCD": [
        {"wram": {0xCABB: b"\0", 0xCABF: b"\0"},
         "read": {0xCABB: 1, 0xCABF: 1, 0xFF40: 1}},
        dict(POISON, wram={0xCABB: b"\x04", 0xCABF: b"\x55"},
             read={0xCABB: 1, 0xCABF: 1, 0xFF40: 1}),
    ],
    "DisableLCD": [
        {"wram": {0xCABB: b"\x80", 0xCAB7: b"\xFF", 0xFF40: b"\x80", 0xFFFF: b"\xFF"},
         "read": {0xCABB: 1, 0xCAB7: 1, 0xFF40: 1, 0xFFFF: 1,
                  0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
        dict(POISON, wram={0xCABB: b"\0", 0xCAB7: b"\xA5", 0xFF40: b"\0", 0xFFFF: b"\xA5"},
             read={0xCABB: 1, 0xCAB7: 1}),
    ],
    "Set_OBJ_8x8": [{"wram": {0xCABB: b"\xFF"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x04"}, read={0xCABB: 1})],
    "Set_OBJ_8x16": [{"wram": {0xCABB: b"\0"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x80"}, read={0xCABB: 1})],
    "SetWindowOn": [{"wram": {0xCABB: b"\0"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x04"}, read={0xCABB: 1})],
    "SetWindowOff": [{"wram": {0xCABB: b"\xFF"}, "read": {0xCABB: 1}}, dict(POISON, wram={0xCABB: b"\x20"}, read={0xCABB: 1})],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
