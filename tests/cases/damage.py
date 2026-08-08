"""Oracle-diff cases for poketcg/src/home/damage.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDamage = 0xCCB9

CONTRACT = {
    "AddToDamage": ("b", "c", "d", "e", "hl"),
    "SubtractFromDamage": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "AddToDamage": [
        {"a": 0, "wram": {wDamage: b"\x00\x00"}},
        {"a": 0x40, "wram": {wDamage: b"\xC0\x00"}},
        {"a": 0x10, "wram": {wDamage: b"\x05\x01"}},
        dict(POISON, a=0xFF, wram={wDamage: b"\x01\x80"}),
    ],
    "SubtractFromDamage": [
        {"a": 0, "wram": {wDamage: b"\x00\x00"}},
        {"a": 0x40, "wram": {wDamage: b"\xC0\x00"}},
        # Low-byte borrow into the high byte.
        {"a": 0x10, "wram": {wDamage: b"\x05\x01"}},
        # High byte itself would go negative: wraps like real hardware.
        {"a": 0x01, "wram": {wDamage: b"\x00\x00"}},
        dict(POISON, a=0xFF, wram={wDamage: b"\x01\x80"}),
    ],
}
