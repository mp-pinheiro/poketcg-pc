POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
wGotHeads = 0xCC0A
ARENA_SUBSTATUS2 = 0xC200 + 0xE8  # player page, duelvar $E8
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480

CONTRACT = {
    "CheckSandAttackOrSmokescreenSubstatus": ("a", "b", "c", "d", "e", "f", "hl"),
    "CountTurnDuelistPokemonWithActivePkmnPower": ("a", "b", "c", "d", "e", "f", "hl"),
    "CountPokemonWithActivePkmnPowerInBothPlayAreas": ("a", "b", "c", "d", "e", "f", "hl"),
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
    # Count id $01 across arena ($C2BB) and bench ($C2BC+): MUK = $C3, DODRIO = $C5.
    "CountTurnDuelistPokemonWithActivePkmnPower": [
        # Arena only, no status: 1 found.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
        # Arena + two bench slots: 3 found.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             wPlayerDeck: b"\x01",
                             0xC2BC: b"\x00\x00\xff"},
         "read": {0xCE7C: 1}},
        # Arena asleep (status $01): skipped.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x01",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
        # Arena paralyzed (status $08): skipped too.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x08",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
        # No match: 0 found, no carry.
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
    ],
    "CountPokemonWithActivePkmnPowerInBothPlayAreas": [
        # Player arena has 1; opponent arena has 1 (opponent deck $C480): total 2.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             0xC3BB: b"\x00",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff",
                             0xC480: b"\x01", 0xC3BC: b"\xff"}},
        # Player only: total 1. Opponent bench terminated.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC3BB: b"\xff",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff",
                             0xC480: b"\x01", 0xC3BC: b"\xff"},
         "read": {0xCE7C: 1}},
        # Neither: 0. Both benches terminated.
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\xff", 0xC3BB: b"\xff",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff",
                             0xC480: b"\x01", 0xC3BC: b"\xff"},
         "read": {0xCE7C: 1}},
    ],
}
