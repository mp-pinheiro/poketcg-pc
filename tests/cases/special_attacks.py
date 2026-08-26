POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_LOCATIONS = 0xC200
OPPONENT_LOCATIONS = 0xC300
PLAYER_DECK = 0xC400
OPPONENT_DECK = 0xC480
wLoadedCard2 = 0xCC65

CONTRACT = {
    "CheckIfAnyBasicPokemonInDeck": {
        "compare": ("a", "b", "c", "d", "e", "f", "hl"),
        "preserve": ("b", "c", "d"),
    },
}

CASES = {
    "CheckIfAnyBasicPokemonInDeck": [
        {"wram": {hWhoseTurn: b"\xC2"}},
        dict(POISON, wram={hWhoseTurn: b"\xC2",
                           PLAYER_LOCATIONS: b"\x00",
                           PLAYER_DECK: b"\x08"},
             read={wLoadedCard2: 64}),
        {"wram": {hWhoseTurn: b"\xC2",
                   PLAYER_LOCATIONS: b"\x00\x00",
                   PLAYER_DECK: b"\x09\x01"},
         "read": {wLoadedCard2: 64}},
        {"wram": {hWhoseTurn: b"\xC2",
                   PLAYER_LOCATIONS: b"\x10" * 59 + b"\x00",
                   PLAYER_DECK: b"\x09" * 59 + b"\x08"},
         "read": {wLoadedCard2: 64}},
        {"wram": {hWhoseTurn: b"\xC2",
                   PLAYER_LOCATIONS: b"\x00" * 60,
                   PLAYER_DECK: b"\x01" * 60},
         "read": {wLoadedCard2: 64}},
        {"wram": {hWhoseTurn: b"\xC3",
                   OPPONENT_LOCATIONS: b"\x00",
                   OPPONENT_DECK: b"\x08"},
         "read": {wLoadedCard2: 64}},
    ],
}

MUTATIONS = {
    "CheckIfAnyBasicPokemonInDeck": {
        "source_symbol": "CheckIfAnyBasicPokemonInDeck",
        "before": "if (gb_read8(wLoadedCard2Stage_ADDR) != 0)",
        "after": "if (gb_read8(wLoadedCard2Stage_ADDR) == 0)",
        "case_ids": [
            "CheckIfAnyBasicPokemonInDeck-1",
            "CheckIfAnyBasicPokemonInDeck-2",
            "CheckIfAnyBasicPokemonInDeck-3",
            "CheckIfAnyBasicPokemonInDeck-5",
        ],
    },
}

# >>> factory-cases-statics
wFirstAttackAIScore = 0xCDBF
wSelectedAttack = 0xCCC6
# <<< factory-cases-statics

# >>> factory CheckWhetherToSwitchToFirstAttack
CONTRACT["CheckWhetherToSwitchToFirstAttack"] = {"compare": (), "preserve": ()}
CASES["CheckWhetherToSwitchToFirstAttack"] = [
    {"wram": {wFirstAttackAIScore: b"\x00", wSelectedAttack: b"\xAA"}, "read": {wSelectedAttack: 1}},
    {"wram": {wFirstAttackAIScore: b"\x4F", wSelectedAttack: b"\x55"}, "read": {wSelectedAttack: 1}},
    dict(POISON, wram={wFirstAttackAIScore: b"\x40", wSelectedAttack: b"\xCC"}, read={wSelectedAttack: 1}),
]
# <<< factory CheckWhetherToSwitchToFirstAttack

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation CheckWhetherToSwitchToFirstAttack
MUTATIONS["CheckWhetherToSwitchToFirstAttack"] = {"source_symbol": "CheckWhetherToSwitchToFirstAttack", "before": "\tif (first_score < 0x50u) {\n\t\twSelectedAttack = SECOND_ATTACK;", "after": "\tif (first_score < 0x50u) {\n\t\twSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;", "case_ids": ["CheckWhetherToSwitchToFirstAttack-0", "CheckWhetherToSwitchToFirstAttack-1", "CheckWhetherToSwitchToFirstAttack-2"]}
# <<< factory-mutation CheckWhetherToSwitchToFirstAttack
