"""Oracle-diff cases for poketcg/src/engine/duel/ai/init.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
WAIDUELVARS_START = 0xCDA5
WAIDUELVARS_SIZE = 0x10
# <<< factory-cases-statics

# >>> factory InitAIDuelVars
CONTRACT["InitAIDuelVars"] = {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["InitAIDuelVars"] = [
    {"wram": {WAIDUELVARS_START: bytes([0xA5] * WAIDUELVARS_SIZE)}},
    dict(POISON, wram={WAIDUELVARS_START: bytes([0xFF] * WAIDUELVARS_SIZE)}),
]
# <<< factory InitAIDuelVars

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation InitAIDuelVars
MUTATIONS["InitAIDuelVars"] = {
    "source_symbol": "InitAIDuelVars",
    "before": "wAIPokedexCounter = 5u;",
    "after": "wAIPokedexCounter = 4u;",
    "case_ids": ["InitAIDuelVars-0", "InitAIDuelVars-1"],
}
# <<< factory-mutation InitAIDuelVars
