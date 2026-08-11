POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
wDamage = 0xCCB9
wAIMinDamage = 0xCCBA
wAIMaxDamage = 0xCCBB
wPlayerArena = 0xC2BB
wOpponentArena = 0xC3BB
wPlayerBench = 0xC2BC
wOpponentBench = 0xC3BC
wPlayerStatus = 0xC2F0
wOpponentStatus = 0xC3F0
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480

CONTRACT = {
    "CalculateDamage_VersusDefendingPokemon": {
        "compare": ("a", "d", "e", "f", "hl"),
        "preserve": (),
    },
    "CalculateDamage_FromDefendingPokemon": {
        "compare": ("a", "d", "e", "f", "hl"),
        "preserve": (),
    },
}


def state(minimum, maximum, damage, location=0, player_status=0, opponent_status=0):
    return {
        hWhoseTurn: b"\xC2",
        hTempPlayAreaLocation_ff9d: bytes((location,)),
        wDamage: bytes((damage,)),
        wAIMinDamage: bytes((minimum,)),
        wAIMaxDamage: bytes((maximum,)),
        wPlayerArena: b"\x00",
        wOpponentArena: b"\x00",
        wPlayerBench: b"\x00\xFF\xFF\xFF\xFF\xFF",
        wOpponentBench: b"\x00\xFF\xFF\xFF\xFF\xFF",
        wPlayerStatus: bytes((player_status,)),
        wOpponentStatus: bytes((opponent_status,)),
        wPlayerDeck: b"\x00",
        wOpponentDeck: b"\x00",
    }

CASES = {
    "CalculateDamage_VersusDefendingPokemon": [
        {"wram": state(0, 0, 0)},
        {"wram": state(1, 1, 1)},
        {"wram": state(0xFF, 0xFF, 0xFF)},
        {"wram": state(0x100 & 0xFF, 0x101 & 0xFF, 0x100 & 0xFF)},
        dict(POISON, wram=state(20, 20, 20, opponent_status=0x80)),
        dict(POISON, wram=state(20, 20, 20, opponent_status=0xC0)),
        dict(POISON, wram=state(20, 20, 20, location=1)),
    ],
    "CalculateDamage_FromDefendingPokemon": [
        {"wram": state(0, 0, 0)},
        {"wram": state(1, 1, 1)},
        {"wram": state(0xFF, 0xFF, 0xFF)},
        {"wram": state(0x100 & 0xFF, 0x101 & 0xFF, 0x100 & 0xFF)},
        dict(POISON, wram=state(20, 20, 20, player_status=0x80)),
        dict(POISON, wram=state(20, 20, 20, player_status=0xC0)),
        dict(POISON, wram=state(20, 20, 20, location=1)),
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "CalculateDamage_VersusDefendingPokemon": {
        "source_symbol": "CalculateDamage_VersusDefendingPokemon",
        "before": "damage = HandleDoubleDamageSubstatus(damage);\n        if (!(damage & (1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F))) {",
        "after": "damage = (uint16_t)(damage + 1u);\n        if (!(damage & (1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F))) {",
        "case_ids": ["CalculateDamage_VersusDefendingPokemon-1"],
    },
    "CalculateDamage_FromDefendingPokemon": {
        "source_symbol": "CalculateDamage_FromDefendingPokemon",
        "before": "damage = HandleDoubleDamageSubstatus(damage);\n    b = TranslateColorToWR(GetArenaCardColor());",
        "after": "damage = (uint16_t)(damage + 1u);\n    b = TranslateColorToWR(GetArenaCardColor());",
        "case_ids": ["CalculateDamage_FromDefendingPokemon-1"],
    },
}
