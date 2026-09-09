from tests.cases._fixtures import ai_play_pokemon_fixture as _ai_play_pokemon_fixture, AI_PLAY_POKEMON_REGS as _AI_PLAY_POKEMON_REGS, ai_evolution_fixture as _ai_evolution_fixture, AI_EVOLUTION_REGS as _AI_EVOLUTION_REGS
"""Oracle-diff cases for poketcg/src/engine/duel/ai/hand_pokemon.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wOpponentDeckID = 0xCC0E
wLoadedCard2ID = 0xCC6C
wTotalAttachedEnergies = 0xCC23
hTempPlayAreaLocation_ff9d = 0xFF9D
wAIScore = 0xCDBE
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wOpponentDuelVariables = 0xC300
wLoadedCard1ID = 0xCC2B
wAIScore = 0xCDBE

wDuelTempList = 0xC510
wHandTempList = 0xCEDA
hWhoseTurn = 0xFF97
DUELVARS_NUMBER_OF_CARDS_IN_HAND = 0xEE
# <<< factory-cases-statics

# >>> factory AIDecideSpecialEvolutions
CONTRACT["AIDecideSpecialEvolutions"] = {"compare": (), "preserve": ()}
CASES["AIDecideSpecialEvolutions"] = [
    {"wram": {wOpponentDeckID: b"\x00", wAIScore: b"\x20"}},
    {"wram": {wOpponentDeckID: b"\x0e", wLoadedCard2ID: b"\x31", wAIScore: b"\x20"}, "hram": {hTempPlayAreaLocation_ff9d: b"\x00"}, "expect": {wAIScore: b"\x20"}},
    {"wram": {wOpponentDeckID: b"\x1a", wLoadedCard2ID: b"\x26", wAIScore: b"\x20"}, "hram": {hTempPlayAreaLocation_ff9d: b"\x00"}},
    dict(POISON, wram={wOpponentDeckID: b"\x00", wAIScore: b"\x20"}),
]
# <<< factory AIDecideSpecialEvolutions

# >>> factory AIDecideEvolution
CONTRACT["AIDecideEvolution"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecideEvolution"] = [
    {"expect_regs": {"a": 0xff, "f": 0x00}},
    dict(POISON, expect_regs={"a": 0xff, "f": 0x00}),
    dict(_ai_evolution_fixture(bank=5), **_AI_EVOLUTION_REGS),
]
# <<< factory AIDecideEvolution

# >>> factory AIDecidePlayLegendaryBirds
CONTRACT["AIDecidePlayLegendaryBirds"] = {"compare": (), "preserve": ()}
CASES["AIDecidePlayLegendaryBirds"] = [
    {"wram": {wOpponentDeckID: b"\x00", wLoadedCard1ID: b"\x00", wAIScore: b"\x20"}},
    {"wram": {wOpponentDeckID: b"\x0c", wLoadedCard1ID: b"\x40", hWhoseTurn: b"\xc2", wPlayerDuelVariables + 0xba: b"\x37", wAIScore: b"\x20"}},
    {"wram": {wOpponentDeckID: b"\x0c", wLoadedCard1ID: b"\x40", hWhoseTurn: b"\xc2", wPlayerDuelVariables + 0xba: b"\x38", wAIScore: b"\x20"}, "expect": {wAIScore: b"\x00"}},
    {"wram": {wOpponentDeckID: b"\x0c", wLoadedCard1ID: b"\x00", wAIScore: b"\x20"}},
    dict(POISON, wram={wOpponentDeckID: b"\x00", wLoadedCard1ID: b"\x00", wAIScore: b"\x20"}),
]
# <<< factory AIDecidePlayLegendaryBirds

# >>> factory AIDecidePlayPokemonCard
CONTRACT["AIDecidePlayPokemonCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIDecidePlayPokemonCard"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 1, 0xCEDA: 1}, "expect": {0xC510: b"\xFF", 0xCEDA: b"\xFF"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00"}, read={0xC510: 1, 0xCEDA: 1}, expect={0xC510: b"\xFF", 0xCEDA: b"\xFF"}),
    dict(_ai_play_pokemon_fixture(bank=5), **_AI_PLAY_POKEMON_REGS),
]
# <<< factory AIDecidePlayPokemonCard

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIDecideSpecialEvolutions
MUTATIONS["AIDecideSpecialEvolutions"] = {
    "source_symbol": "AIDecideSpecialEvolutions",
    "before": "\tuint8_t deck = wOpponentDeckID;",
    "after": "\tuint8_t deck = (uint8_t)(wOpponentDeckID + 1u);",
    "case_ids": ["AIDecideSpecialEvolutions-1", "AIDecideSpecialEvolutions-2", "AIDecideSpecialEvolutions-3"],
}
# <<< factory-mutation AIDecideSpecialEvolutions
# >>> factory-mutation AIDecideEvolution
MUTATIONS["AIDecideEvolution"] = {"source_symbol": "AIDecideEvolution", "before": "\t\twTempAIPokemonCard = card;\n\t\tif (IsPrehistoricPowerActive(hand).f & 0x10u)", "after": "\t\twTempAIPokemonCard = (uint8_t)(card + 1u);\n\t\tif (IsPrehistoricPowerActive(hand).f & 0x10u)", "case_ids": ["AIDecideEvolution-2"]}
# <<< factory-mutation AIDecideEvolution
# >>> factory-mutation AIDecidePlayLegendaryBirds
MUTATIONS["AIDecidePlayLegendaryBirds"] = {"source_symbol": "AIDecidePlayLegendaryBirds", "before": "void AIDecidePlayLegendaryBirds(void)\n{\n\tuint8_t deck = wOpponentDeckID;", "after": "void AIDecidePlayLegendaryBirds(void)\n{\n\tuint8_t deck = (uint8_t)(wOpponentDeckID + 1u);", "case_ids": ["AIDecidePlayLegendaryBirds-2"]}
# <<< factory-mutation AIDecidePlayLegendaryBirds
# >>> factory-mutation AIDecidePlayPokemonCard
MUTATIONS["AIDecidePlayPokemonCard"] = {"source_symbol": "AIDecidePlayPokemonCard", "before": "\t\t\treturn (AIDecidePlayPokemonCardResult){last, (uint8_t)(last == 0u ? 0x80u : 0u)};", "after": "\t\t\treturn (AIDecidePlayPokemonCardResult){last, 0x10u};", "case_ids": ["AIDecidePlayPokemonCard-0", "AIDecidePlayPokemonCard-1"]}
# <<< factory-mutation AIDecidePlayPokemonCard
