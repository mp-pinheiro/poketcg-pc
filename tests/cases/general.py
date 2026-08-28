"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/general.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wAIPlayAreaCardToSwitch = 0xCDD5
wAIRetreatedThisTurn = 0xCE03
wPreviousAIFlags = 0xCE20
wConfusionRetreatCheckWasUnsuccessful = 0xCC0C
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory AIProcessRetreat
CONTRACT["AIProcessRetreat"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIProcessRetreat"] = [
    {"wram": {wAIRetreatedThisTurn: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x00}},
    {"wram": {wAIRetreatedThisTurn: b"\x00", wConfusionRetreatCheckWasUnsuccessful: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x00}},
    {"wram": {wAIRetreatedThisTurn: b"\x00", wConfusionRetreatCheckWasUnsuccessful: b"\x80"}, "expect_regs": {"a": 0x80, "f": 0x00}},
    dict(POISON, wram={wAIRetreatedThisTurn: b"\x00", wConfusionRetreatCheckWasUnsuccessful: b"\x01"}, expect_regs={"a": 0x01, "f": 0x00}),
]
# <<< factory AIProcessRetreat

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AIProcessRetreat
MUTATIONS["AIProcessRetreat"] = {"source_symbol": "AIProcessRetreat", "before": "AIProcessRetreatResult AIProcessRetreat(void)\n{\n\tuint8_t already_retreated = wAIRetreatedThisTurn;", "after": "AIProcessRetreatResult AIProcessRetreat(void)\n{\n\tuint8_t already_retreated = 0u;", "case_ids": ["AIProcessRetreat-0"]}
# <<< factory-mutation AIProcessRetreat
