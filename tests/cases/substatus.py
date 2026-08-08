POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
wGotHeads = 0xCC0A
ARENA_SUBSTATUS2 = 0xC200 + 0xE8  # player page, duelvar $E8

CONTRACT = {
    "CheckSandAttackOrSmokescreenSubstatus": ("a", "b", "c", "d", "e", "f", "hl"),
}

CASES = {
    "CheckSandAttackOrSmokescreenSubstatus": [
        # No substatus: a = 0, Z set, de untouched.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x00"}},
        # Sand attack, got tails: carry set, a = 0, de = $00DE.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x02", wGotHeads: b"\x00"}},
        # Sand attack, got heads: a = heads, no carry, de = $00DE.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x02", wGotHeads: b"\x01"}},
        # Smokescreen, got tails: carry set, de = $00DF.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x01", wGotHeads: b"\x00"}},
        # Smokescreen, got heads: a = heads, de = $00DF.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x01", wGotHeads: b"\x01"}},
        # Unrelated substatus value: a = it, no carry, de untouched.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x03"}},
        # Poisoned: opponent's turn reads the $C3 page.
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC300 + 0xE8: b"\x00"}),
    ],
}
