"""Oracle-diff cases for poketcg/src/engine/duel/ai/boss_deck_set_up.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = sym("hWhoseTurn")
wDuelistHand = sym("wPlayerHand")
wDuelistDeck = sym("wPlayerDeckCards")
wDuelistNotInDeck = sym("wPlayerNumberOfCardsNotInDeck")
wDuelistHandCount = sym("wPlayerNumberOfCardsInHand")
wPlayerDeck = sym("wPlayerDeck")
wAICardListAvoidPrize = sym("wAICardListAvoidPrize")
wAISetupBasicPokemonCount = sym("wAISetupBasicPokemonCount")
wAISetupEnergyCount = sym("wAISetupEnergyCount")
# <<< factory-cases-statics

# >>> factory SetUpBossStartingHandAndDeck
CONTRACT["SetUpBossStartingHandAndDeck"] = {"compare": (), "preserve": ()}
CASES["SetUpBossStartingHandAndDeck"] = [
    {
        "wram": {
            hWhoseTurn: b"\xC2",
            wDuelistNotInDeck: b"\x07",
            wDuelistHandCount: b"\x07",
            wDuelistHand: bytes(range(53, 60)),
            wDuelistDeck: bytes(range(19)),
            wPlayerDeck: bytes([1] * 13),
            sym("wBoosterTempEnergiesDrawn") + 2: b"\x08",
            sym("wBoosterTempEnergiesDrawn") + 3: bytes([1] * 41),
            sym("wBoosterCardsDrawnEnd") + 0x21: b"\x08\x08\x01\x01\x08",
            wAICardListAvoidPrize: b"\x00\x00",
        },
        "read": {wAISetupBasicPokemonCount: 1, wAISetupEnergyCount: 1},
        "instruction_budget": 2000000,
        "cycle_budget": 8000000,
    },
    dict(POISON, wram={
        hWhoseTurn: b"\xC2",
        wDuelistNotInDeck: b"\x07",
        wDuelistHandCount: b"\x07",
        wDuelistHand: bytes(range(53, 60)),
        wDuelistDeck: bytes(range(19)),
        wPlayerDeck: bytes([1] * 13),
        sym("wBoosterTempEnergiesDrawn") + 2: b"\x08",
        sym("wBoosterTempEnergiesDrawn") + 3: bytes([1] * 41),
        sym("wBoosterCardsDrawnEnd") + 0x21: b"\x08\x08\x01\x01\x08",
        wAICardListAvoidPrize: b"\x00\x00",
    }, read={wAISetupBasicPokemonCount: 1, wAISetupEnergyCount: 1}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory SetUpBossStartingHandAndDeck

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation SetUpBossStartingHandAndDeck
MUTATIONS["SetUpBossStartingHandAndDeck"] = {
    "source_symbol": "SetUpBossStartingHandAndDeck",
    "before": "\t\twAISetupBasicPokemonCount = 0u;\n\t\twAISetupEnergyCount = 0u;",
    "after": "\t\twAISetupBasicPokemonCount = 1u;\n\t\twAISetupEnergyCount = 0u;",
    "case_ids": ["SetUpBossStartingHandAndDeck-0", "SetUpBossStartingHandAndDeck-1"],
}
# <<< factory-mutation SetUpBossStartingHandAndDeck
