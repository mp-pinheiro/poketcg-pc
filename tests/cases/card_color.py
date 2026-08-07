"""Oracle-diff cases for poketcg/src/home/card_color.asm.

The three color routines (GetArenaCardColor, GetPlayAreaCardColor, HandleEnergyBurn) are
not registered: their Shift-Pokemon-Power path calls CheckIsIncapableOfUsingPkmnPower
(substatus.asm:502), which cascades through CountPokemonWithActivePkmnPowerInBothPlayAreas
+ SwapTurn + the full play-area traversal -- unported duel engine.
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
}


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
}
