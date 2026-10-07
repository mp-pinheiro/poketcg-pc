from tests.cases._symbols import sym
from tests.cases._fixtures import SPECIAL_ATTACK_REGS, special_attack_fixture
from tests.cases._fixtures import SPECIAL_AI_ATTACKS_REGS, special_ai_attacks_fixture

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = sym("hWhoseTurn")
PLAYER_LOCATIONS = sym("wPlayerCardLocations")
OPPONENT_LOCATIONS = sym("wOpponentCardLocations")
PLAYER_DECK = sym("wBoosterCardsDrawn")
OPPONENT_DECK = sym("wOpponentDeck")
wLoadedCard2 = sym("wLoadedCard2")

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
wFirstAttackAIScore = sym("wFirstAttackAIScore")
wSelectedAttack = sym("wSelectedAttack")

hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")
wDamage = sym("wDamage")
wDuelTempList = sym("wDuelTempList")
wSelectedAttack = sym("wSelectedAttack")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory CheckWhetherToSwitchToFirstAttack
CONTRACT["CheckWhetherToSwitchToFirstAttack"] = {"compare": (), "preserve": ()}
CASES["CheckWhetherToSwitchToFirstAttack"] = [
    {"wram": {wFirstAttackAIScore: b"\x00", wSelectedAttack: b"\xAA"}, "read": {wSelectedAttack: 1}},
    {"wram": {wFirstAttackAIScore: b"\x4F", wSelectedAttack: b"\x55"}, "read": {wSelectedAttack: 1}},
    dict(POISON, wram={wFirstAttackAIScore: b"\x40", wSelectedAttack: b"\xCC"}, read={wSelectedAttack: 1}),
]
# <<< factory CheckWhetherToSwitchToFirstAttack

# >>> factory HandleSpecialAIAttacks
CONTRACT["HandleSpecialAIAttacks"] = {"compare": ("a", "f"), "preserve": ()}
_SPECIAL_ARENA = {sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerBench"): b"\xFF",
                  sym("wOpponentArenaCard"): b"\xFF", sym("wOpponentBench"): b"\xFF"}
CASES["HandleSpecialAIAttacks"] = [
    # water-master 437339: Scyther in the arena; Swords Dance is unusable (the
    # second attack is not powered), so the score is $85 with that carry.
    dict(special_ai_attacks_fixture(vram=False, bank=8), **SPECIAL_AI_ATTACKS_REGS, read={sym("wTotalAttachedEnergies"): 1, sym("wDealtDamage"): 2}),
    {},
    dict(POISON),
    dict(special_attack_fixture(vram=False, bank=5), **SPECIAL_ATTACK_REGS),
    # Big Thunder: the score is unconditional, the flags are the matching `cp`.
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\x76"}},
    # Fetch: 10 cards used keeps the attack; 45 dismisses it.
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\xB9", sym("wPlayerNumberOfCardsNotInDeck"): b"\x0A"}},
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\xB9", sym("wPlayerNumberOfCardsNotInDeck"): b"\x2D"}},
    # Hyper Beam with nothing attached to the player's arena card.
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\x45"}},
    # Conversion 1 with an empty bench: fewer than two set-up Pokemon.
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\xBD", sym("wPlayerArenaCardStatus"): b"\x00", sym("wSelectedAttack"): b"\x00"}},
    # Call for Family: a second Oddish still in the deck, one Pokemon in play.
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\x1C\x1C", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01"}},
    # Earthquake with an empty bench: six prizes left versus no KOs.
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\x7A", sym("wPlayerPrizes"): b"\x3F"}},
    {"wram": {**_SPECIAL_ARENA, sym("wBoosterCardsDrawn"): b"\x7A", sym("wPlayerPrizes"): b"\x00"}},
]
# <<< factory HandleSpecialAIAttacks

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation CheckWhetherToSwitchToFirstAttack
MUTATIONS["CheckWhetherToSwitchToFirstAttack"] = {"source_symbol": "CheckWhetherToSwitchToFirstAttack", "before": "\tif (first_score < 0x50u) {\n\t\twSelectedAttack = SECOND_ATTACK;", "after": "\tif (first_score < 0x50u) {\n\t\twSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;", "case_ids": ["CheckWhetherToSwitchToFirstAttack-0", "CheckWhetherToSwitchToFirstAttack-1", "CheckWhetherToSwitchToFirstAttack-2"]}
# <<< factory-mutation CheckWhetherToSwitchToFirstAttack
# >>> factory-mutation HandleSpecialAIAttacks
MUTATIONS["HandleSpecialAIAttacks"] = {"source_symbol": "HandleSpecialAIAttacks", "before": "\t\tif (u.f & 0x10u)\n\t\t\treturn (HandleSpecialAIAttacksResult){0x85u, u.f};", "after": "\t\tif (u.f & 0x10u)\n\t\t\treturn (HandleSpecialAIAttacksResult){0x84u, u.f};", "case_ids": ["HandleSpecialAIAttacks-0"]}
# <<< factory-mutation HandleSpecialAIAttacks
