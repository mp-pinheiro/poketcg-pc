"""Oracle-diff cases for poketcg/src/engine/duel/ai/init.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
WAIDUELVARS_START = sym("wAIDuelVars")
WAIDUELVARS_SIZE = 0x10
# <<< factory-cases-statics

# >>> factory InitAIDuelVars
CONTRACT["InitAIDuelVars"] = {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["InitAIDuelVars"] = [
    {"wram": {WAIDUELVARS_START: bytes([0xA5] * WAIDUELVARS_SIZE)}},
    dict(POISON, wram={WAIDUELVARS_START: bytes([0xFF] * WAIDUELVARS_SIZE)}),
]
# <<< factory InitAIDuelVars

# >>> factory InitAITurnVars
CONTRACT["InitAITurnVars"] = {"compare": (), "preserve": ()}
CASES["InitAITurnVars"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {
            sym("wAIPokedexCounter"): b"\x05", sym("wPreviousAIFlags"): b"\xAA", sym("wAITriedAttack"): b"\xBB", sym("wUnused_cddc"): b"\xCC",
            sym("wAIRetreatedThisTurn"): b"\xDD", sym("wPlayerAttackingAttackIndex"): b"\xFF", sym("wPlayerAttackingCardIndex"): b"\x00", sym("wAIBarrierFlagCounter"): b"\x05",
        },
        "expect": {
            sym("wAIPokedexCounter"): b"\x06", sym("wPreviousAIFlags"): b"\x00", sym("wAITriedAttack"): b"\x00", sym("wUnused_cddc"): b"\x00",
            sym("wAIRetreatedThisTurn"): b"\x00", sym("wAIBarrierFlagCounter"): b"\x00",
        },
    },
]
# <<< factory InitAITurnVars

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
# >>> factory-mutation InitAITurnVars
MUTATIONS["InitAITurnVars"] = {
    "source_symbol": "InitAITurnVars",
    "before": "wAIPokedexCounter = (uint8_t)(wAIPokedexCounter + 1u);",
    "after": "wAIPokedexCounter = (uint8_t)(wAIPokedexCounter + 2u);",
    "case_ids": ["InitAITurnVars-0"],
}
# <<< factory-mutation InitAITurnVars
