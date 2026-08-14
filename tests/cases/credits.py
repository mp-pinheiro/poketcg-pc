"""Oracle-diff cases for poketcg/src/engine/credits.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Func_1d758
CONTRACT["Func_1d758"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["Func_1d758"] = [
    {"read": {0xFF41: 1, 0xFFFF: 1}},
    dict(POISON, read={0xFF41: 1, 0xFFFF: 1}),
]
# <<< factory Func_1d758

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_1d758
MUTATIONS["Func_1d758"] = {"source_symbol": "Func_1d758", "before": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) & (uint8_t)~STAT_LYC_MASK));", "after": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) | STAT_LYC_MASK));", "case_ids": ["Func_1d758-0", "Func_1d758-1"]}
# <<< factory-mutation Func_1d758
