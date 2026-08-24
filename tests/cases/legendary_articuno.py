"""Oracle-diff cases for poketcg/src/engine/duel/ai/decks/legendary_articuno.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
ARTICUNO_SCORE = 0xCDE5
# <<< factory-cases-statics

# >>> factory ScoreLegendaryArticunoCards
CONTRACT["ScoreLegendaryArticunoCards"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ScoreLegendaryArticunoCards"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, "expect": {ARTICUNO_SCORE: b"\x05"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, expect={ARTICUNO_SCORE: b"\x05"}),
]
# <<< factory ScoreLegendaryArticunoCards

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation ScoreLegendaryArticunoCards
MUTATIONS["ScoreLegendaryArticunoCards"] = {
    "source_symbol": "ScoreLegendaryArticunoCards",
    "before": "\t\t(void)RaiseAIScoreToAllMatchingIDsInBench(ARTICUNO_LV35);",
    "after": "\t\t(void)RaiseAIScoreToAllMatchingIDsInBench(DEWGONG);",
    "case_ids": ["ScoreLegendaryArticunoCards-0", "ScoreLegendaryArticunoCards-1"],
}
# <<< factory-mutation ScoreLegendaryArticunoCards
