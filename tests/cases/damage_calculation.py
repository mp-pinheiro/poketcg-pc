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


# >>> factory EstimateDamage_VersusDefendingCard
_edvdc_wDamage = 0xCCB9
_edvdc_wAIMinDamage = 0xCCBB
_edvdc_wAIMaxDamage = 0xCCBC
_edvdc_wLoadedAttackCategory = 0xCCB1
# The reference runs the seeded card's real EFFECTCMDTYPE_AI command, so these cases
# need a budget far above the defaults on BOTH backends; tests/test_leaves.py derives
# PyBoy's frame allowance from cycle_budget.
def _edvdc(location, extra=None, **kw):
    wram = {0xFF97: b"\xC2", 0xFF9D: location, 0xC2BB: b"\x00",
            _edvdc_wDamage: b"\x00\x00", _edvdc_wAIMinDamage: b"\x00",
            _edvdc_wAIMaxDamage: b"\x00"}
    if extra:
        wram.update(extra)
    case = {"wram": wram, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
            "instruction_budget": 40000000, "cycle_budget": 160000000,
            "read": {_edvdc_wDamage: 2, _edvdc_wAIMinDamage: 1, _edvdc_wAIMaxDamage: 1}}
    case.update(kw)
    return case

CONTRACT["EstimateDamage_VersusDefendingCard"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": ()}
CASES["EstimateDamage_VersusDefendingCard"] = [
    _edvdc(b"\x00", a=0),
    _edvdc(b"\x01", extra={0xC2BC: b"\x00"}, a=0),
    _edvdc(b"\x00", extra={_edvdc_wLoadedAttackCategory: b"\x04"}, a=0),
    dict(POISON, **_edvdc(b"\x00")),
]
# <<< factory EstimateDamage_VersusDefendingCard


# >>> factory EstimateDamage_FromDefendingPokemon
# Mirror of the routine above; the opponent's arena card supplies the attack, so
# 0xC3BB is seeded too. Same large budget: the real EFFECTCMDTYPE_AI command runs.
def _edfdp(location, extra=None, **kw):
    wram = {0xFF97: b"\xC2", 0xFF9D: location, 0xC2BB: b"\x00", 0xC3BB: b"\x00",
            _edvdc_wDamage: b"\x00\x00", _edvdc_wAIMinDamage: b"\x00",
            _edvdc_wAIMaxDamage: b"\x00"}
    if extra:
        wram.update(extra)
    case = {"wram": wram, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}],
            "instruction_budget": 40000000, "cycle_budget": 160000000,
            "read": {_edvdc_wDamage: 2, _edvdc_wAIMinDamage: 1, _edvdc_wAIMaxDamage: 1}}
    case.update(kw)
    return case

CONTRACT["EstimateDamage_FromDefendingPokemon"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": ()}
CASES["EstimateDamage_FromDefendingPokemon"] = [
    _edfdp(b"\x00", a=0),
    _edfdp(b"\x01", extra={0xC3BC: b"\x00"}, a=0),
    _edfdp(b"\x00", extra={_edvdc_wLoadedAttackCategory: b"\x04"}, a=0),
    dict(POISON, **_edfdp(b"\x00")),
]
# <<< factory EstimateDamage_FromDefendingPokemon

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
# >>> factory-mutation EstimateDamage_VersusDefendingCard
MUTATIONS["EstimateDamage_VersusDefendingCard"] = {"source_symbol": "EstimateDamage_VersusDefendingCard", "before": "\tgb_write8(wAIMinDamage_ADDR, damage);\n\tgb_write8(wAIMaxDamage_ADDR, damage);\n\t(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI, 0u, 0u, 0u);", "after": "\tgb_write8(wAIMinDamage_ADDR, (uint8_t)(damage + 1u));\n\tgb_write8(wAIMaxDamage_ADDR, damage);\n\t(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI, 0u, 0u, 0u);", "case_ids": ["EstimateDamage_VersusDefendingCard-0", "EstimateDamage_VersusDefendingCard-1", "EstimateDamage_VersusDefendingCard-3"]}
# <<< factory-mutation EstimateDamage_VersusDefendingCard
# >>> factory-mutation EstimateDamage_FromDefendingPokemon
MUTATIONS["EstimateDamage_FromDefendingPokemon"] = {"source_symbol": "EstimateDamage_FromDefendingPokemon", "before": "\tgb_write8(wAIMinDamage_ADDR, damage);\n\tgb_write8(wAIMaxDamage_ADDR, damage);\n\tSwapTurn();", "after": "\tgb_write8(wAIMinDamage_ADDR, (uint8_t)(damage + 1u));\n\tgb_write8(wAIMaxDamage_ADDR, damage);\n\tSwapTurn();", "case_ids": ["EstimateDamage_FromDefendingPokemon-0", "EstimateDamage_FromDefendingPokemon-1", "EstimateDamage_FromDefendingPokemon-3"]}
# <<< factory-mutation EstimateDamage_FromDefendingPokemon
