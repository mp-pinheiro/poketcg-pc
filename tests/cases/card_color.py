"""Oracle-diff cases for poketcg/src/home/card_color.asm.

GetPlayAreaCardColor and HandleEnergyBurn are Wave 2 scope (need
GetArenaCardColor's own play-area-location generalization plus
CountPokemonWithActivePkmnPowerInBothPlayAreas' full traversal already
covered by substatus). GetArenaCardColor -- the a=PLAY_AREA_ARENA(0)
specialization -- ports cleanly now that CheckIsIncapableOfUsingPkmnPower
(substatus.asm:502) has landed with no remaining unported dependency.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB   # DUELVARS_ARENA_CARD ($BB); bench1 at +1, etc.
wChangedWeakness = 0xC2E9   # DUELVARS_ARENA_CARD_CHANGED_WEAKNESS
wChangedResistance = 0xC2EA
CONTRACT = {
    "GetCardWeakness": ("a", "b", "c", "d", "e"),
    "GetArenaCardWeakness": ("a", "b", "c", "d", "e"),
    "GetPlayAreaCardWeakness": ("a", "b", "c", "d", "e"),
    "GetCardResistance": ("a", "b", "c", "d", "e"),
    "GetArenaCardResistance": ("a", "b", "c", "d", "e"),
    "GetPlayAreaCardResistance": ("a", "b", "c", "d", "e"),
    "GetArenaCardColor": ("a", "b", "c", "d", "e"),
}

wChangedType = 0xC2D4       # DUELVARS_ARENA_CARD_CHANGED_TYPE
wArenaCardStatus = 0xC2F0   # DUELVARS_ARENA_CARD_STATUS
wBench = 0xC2BC             # DUELVARS_BENCH
RECYCLE = 0xE4              # a real TYPE_TRAINER card (ai_trainer_card_logic.asm)


def arena(cardid, idx=0):
    return {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: bytes((idx,)),
            wPlayerDeck + idx: bytes((cardid,))}


CASES = {
    "GetCardWeakness": [
        {"a": wPlayerArenaCard & 0xFF, "wram": arena(8)},
        {"a": wPlayerArenaCard & 0xFF, "wram": arena(0x40, idx=3)},
        dict(POISON, a=wPlayerArenaCard & 0xFF, wram=arena(0xE4, idx=5)),
    ],
    "GetArenaCardWeakness": [
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wChangedWeakness: b"\x30"}},
        {"wram": {**arena(8), wChangedWeakness: b"\x00"}},
        dict(POISON, wram={**arena(0x40, idx=2), wChangedWeakness: b"\x00"}),
    ],
    "GetPlayAreaCardWeakness": [
        {"a": 0, "wram": {**arena(8), wChangedWeakness: b"\x00"}},
        {"a": 1, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)),
                          wPlayerArenaCard + 1: bytes((4,)), wPlayerDeck + 4: bytes((0x80,))}},
        dict(POISON, a=2, wram={hWhoseTurn: bytes((PLAYER_TURN,)),
                                wPlayerArenaCard + 2: bytes((1,)), wPlayerDeck + 1: bytes((8,))}),
    ],
    "GetCardResistance": [
        {"a": wPlayerArenaCard & 0xFF, "wram": arena(8)},
        {"a": wPlayerArenaCard & 0xFF, "wram": arena(0x40, idx=3)},
        dict(POISON, a=wPlayerArenaCard & 0xFF, wram=arena(0xE4, idx=5)),
    ],
    "GetArenaCardResistance": [
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wChangedResistance: b"\x10"}},
        {"wram": {**arena(8), wChangedResistance: b"\x00"}},
        dict(POISON, wram={**arena(0x40, idx=2), wChangedResistance: b"\x00"}),
    ],
    "GetPlayAreaCardResistance": [
        {"a": 0, "wram": {**arena(8), wChangedResistance: b"\x00"}},
        {"a": 1, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)),
                          wPlayerArenaCard + 1: bytes((4,)), wPlayerDeck + 4: bytes((0x80,))}},
        dict(POISON, a=2, wram={hWhoseTurn: bytes((PLAYER_TURN,)),
                                wPlayerArenaCard + 2: bytes((1,)), wPlayerDeck + 1: bytes((8,))}),
    ],
    "GetArenaCardColor": [
        # Regular path, no Shift active: card's own type.
        {"wram": {**arena(8), wChangedType: b"\x00"}},
        # Regular path, Trainer card: reported as COLORLESS.
        {"wram": {**arena(RECYCLE), wChangedType: b"\x00"}},
        # Shift active but incapable (arena status paralyzed): falls back to
        # the regular (card-type) path despite the changed-type flag.
        {"wram": {**arena(8), wChangedType: b"\x80", wArenaCardStatus: b"\x01"}},
        # Shift active and capable (no status, no Muk on either side):
        # returns the changed type's low nibble directly.
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wChangedType: b"\x83",
                  wArenaCardStatus: b"\x00", wPlayerArenaCard: b"\xff",
                  wBench: b"\xff", 0xC3BB: b"\xff", 0xC3BC: b"\xff"}},
        dict(POISON, wram={**arena(0x40, idx=3), wChangedType: b"\x00"}),
    ],
}
