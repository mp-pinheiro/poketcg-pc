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
    "GetCardWeakness": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetArenaCardWeakness": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetPlayAreaCardWeakness": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetCardResistance": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetArenaCardResistance": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetPlayAreaCardResistance": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetArenaCardColor": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "GetPlayAreaCardColor": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "HandleEnergyBurn": {"compare": (), "preserve": ()},
}

wChangedType = 0xC2D4       # DUELVARS_ARENA_CARD_CHANGED_TYPE
wArenaCardStatus = 0xC2F0   # DUELVARS_ARENA_CARD_STATUS
wBench = 0xC2BC             # DUELVARS_BENCH
CHARIZARD = 0x32
wAttachedEnergies_ADDR = 0xCC1B
wTotalAttachedEnergies_ADDR = 0xCC23
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
    "GetPlayAreaCardColor": [
        {"a": 0, "wram": {**arena(8), wChangedType: b"\x00"}},
        {"a": 1, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard + 1: bytes((3,)),
                          wPlayerDeck + 3: bytes((0x40,)), wChangedType + 1: b"\x00"}},
        {"a": 0, "wram": {**arena(RECYCLE), wChangedType: b"\x00"}},
        {"a": 0, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wChangedType: b"\x83",
                          wArenaCardStatus: b"\x00", wPlayerArenaCard: b"\xff",
                          wBench: b"\xff", 0xC3BB: b"\xff", 0xC3BC: b"\xff"}},
        {"a": 0, "wram": {**arena(8), wChangedType: b"\x80", wArenaCardStatus: b"\x01"}},
        dict(POISON, a=0, wram={**arena(0x40, idx=3), wChangedType: b"\x00"}),
    ],
    "HandleEnergyBurn": [
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: bytes((0,)),
                  wPlayerDeck + 0: bytes((0x08,))}},
        dict(POISON, wram={hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: bytes((2,)),
                           wPlayerDeck + 2: bytes((CHARIZARD,)),
                           wArenaCardStatus: b"\x01"}),
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: bytes((5,)),
                  wPlayerDeck + 5: bytes((CHARIZARD,)),
                  wChangedType: b"\x00", wArenaCardStatus: b"\x00",
                  wBench: b"\xff", 0xC3BB: b"\xff", 0xC3BC: b"\xff",
                  wAttachedEnergies_ADDR: b"\x01\x02\x03\x04\x05\x06",
                  wTotalAttachedEnergies_ADDR: b"\x07"},
         "read": {wAttachedEnergies_ADDR: 6}},
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: bytes((7,)),
                  wPlayerDeck + 7: bytes((CHARIZARD,)),
                  wChangedType: b"\x00", wArenaCardStatus: b"\x00",
                  wBench: b"\xff", 0xC3BB: b"\xff", 0xC3BC: b"\xff",
                  wAttachedEnergies_ADDR: b"\x02\x03\x01\x00\x00\x00",
                  wTotalAttachedEnergies_ADDR: b"\x06"},
         "read": {wAttachedEnergies_ADDR: 6}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GetArenaCardColor": {
        "source_symbol": "GetArenaCardColor",
        "before": "\treturn GetPlayAreaCardColor(0);",
        "after": "\treturn GetPlayAreaCardColor(1);",
        "case_ids": ["GetArenaCardColor-3", "GetArenaCardColor-0", "GetArenaCardColor-1", "GetArenaCardColor-2", "GetArenaCardColor-4"],
    },
}
MUTATIONS["GetPlayAreaCardColor"] = {
    "source_symbol": "GetPlayAreaCardColor",
    "before": "\treturn type == TYPE_TRAINER ? COLORLESS : type;",
    "after": "\treturn type != TYPE_TRAINER ? COLORLESS : type;",
    "case_ids": ["GetPlayAreaCardColor-0"],
}
MUTATIONS["GetPlayAreaCardWeakness"] = {
    "source_symbol": "GetPlayAreaCardWeakness",
    "before": "\treturn card_weakness_of((uint8_t)(a + DUELVARS_ARENA_CARD));",
    "after": "\treturn card_weakness_of((uint8_t)(a - DUELVARS_ARENA_CARD));",
    "case_ids": ["GetPlayAreaCardWeakness-1"],
}
MUTATIONS["HandleEnergyBurn"] = {
    "source_symbol": "HandleEnergyBurn",
    "before": "\tif (card_id != CHARIZARD)",
    "after": "\tif (card_id == CHARIZARD)",
    "case_ids": ["HandleEnergyBurn-2"],
}
MUTATIONS["GetArenaCardResistance"] = {
    "source_symbol": "GetArenaCardResistance",
    "before": "\tuint8_t changed = turn_duel_var(DUELVARS_ARENA_CARD_CHANGED_RESISTANCE);\n\tif (changed != 0)",
    "after": "\tuint8_t changed = turn_duel_var(DUELVARS_ARENA_CARD_CHANGED_RESISTANCE);\n\tif (changed == 0)",
    "case_ids": ["GetArenaCardResistance-0"],
}
MUTATIONS["GetArenaCardWeakness"] = {
    "source_symbol": "GetArenaCardWeakness",
    "before": "\tuint8_t changed = turn_duel_var(DUELVARS_ARENA_CARD_CHANGED_WEAKNESS);\n\tif (changed != 0)",
    "after": "\tuint8_t changed = turn_duel_var(DUELVARS_ARENA_CARD_CHANGED_WEAKNESS);\n\tif (changed == 0)",
    "case_ids": ["GetArenaCardWeakness-0"],
}
MUTATIONS["GetCardResistance"] = {
    "source_symbol": "GetCardResistance",
    "before": "\treturn card_resistance_of(a);",
    "after": "\treturn (card_resistance_of(a)) ^ 1u;",
    "case_ids": ["GetCardResistance-0"],
}
MUTATIONS["GetCardWeakness"] = {
    "source_symbol": "GetCardWeakness",
    "before": "\treturn card_weakness_of(a);",
    "after": "\treturn (card_weakness_of(a)) ^ 1u;",
    "case_ids": ["GetCardWeakness-0"],
}
MUTATIONS["GetPlayAreaCardResistance"] = {
    "source_symbol": "GetPlayAreaCardResistance",
    "before": "\t\treturn GetArenaCardResistance();",
    "after": "\t\treturn (GetArenaCardResistance()) ^ 1u;",
    "case_ids": ["GetPlayAreaCardResistance-0"],
}
