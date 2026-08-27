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
    dict(POISON, expect_regs={"a": 0xff, "f": 0x00})
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
CONTRACT["AIDecidePlayPokemonCard"] = {"compare": (), "preserve": ()}
CASES["AIDecidePlayPokemonCard"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 1, 0xCEDA: 1}, "expect": {0xC510: b"\xFF", 0xCEDA: b"\xFF"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00"}, read={0xC510: 1, 0xCEDA: 1}, expect={0xC510: b"\xFF", 0xCEDA: b"\xFF"}),
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
MUTATIONS["AIDecideEvolution"] = {"source_symbol": "AIDecideEvolution", "before": "uint8_t AIDecideEvolution(void)\n{\n\tuint8_t result = 0xffu;", "after": "uint8_t AIDecideEvolution(void)\n{\n\tuint8_t result = 0u;", "case_ids": ["AIDecideEvolution-0", "AIDecideEvolution-1"]}
# <<< factory-mutation AIDecideEvolution
# >>> factory-mutation AIDecidePlayLegendaryBirds
MUTATIONS["AIDecidePlayLegendaryBirds"] = {"source_symbol": "AIDecidePlayLegendaryBirds", "before": "void AIDecidePlayLegendaryBirds(void)\n{\n\tuint8_t deck = wOpponentDeckID;", "after": "void AIDecidePlayLegendaryBirds(void)\n{\n\tuint8_t deck = (uint8_t)(wOpponentDeckID + 1u);", "case_ids": ["AIDecidePlayLegendaryBirds-2"]}
# <<< factory-mutation AIDecidePlayLegendaryBirds
# >>> factory-mutation AIDecidePlayPokemonCard
MUTATIONS["AIDecidePlayPokemonCard"] = {"source_symbol": "AIDecidePlayPokemonCard", "before": "void AIDecidePlayPokemonCard(void)\n{\n\t(void)CreateHandCardList(0u);\n\t(void)SortTempHandByIDList();\n\tuint16_t hl = wDuelTempList_ADDR;\n\tuint16_t de = wHandTempList_ADDR;", "after": "void AIDecidePlayPokemonCard(void)\n{\n\t(void)CreateHandCardList(0u);\n\t(void)SortTempHandByIDList();\n\tuint16_t hl = wDuelTempList_ADDR;\n\tuint16_t de = wDuelTempList_ADDR;", "case_ids": ["AIDecidePlayPokemonCard-0", "AIDecidePlayPokemonCard-1"]}
# <<< factory-mutation AIDecidePlayPokemonCard
