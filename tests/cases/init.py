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

# >>> factory InitAITurnVars
CONTRACT["InitAITurnVars"] = {"compare": (), "preserve": ()}
CASES["InitAITurnVars"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "wram": {
            0xCDA6: b"\x05", 0xCE20: b"\xAA", 0xCDDB: b"\xBB", 0xCDDC: b"\xCC",
            0xCE03: b"\xDD", 0xCC10: b"\xFF", 0xCC11: b"\x00", 0xCDA7: b"\x05",
        },
        "expect": {
            0xCDA6: b"\x06", 0xCE20: b"\x00", 0xCDDB: b"\x00", 0xCDDC: b"\x00",
            0xCE03: b"\x00", 0xCDA7: b"\x00",
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
