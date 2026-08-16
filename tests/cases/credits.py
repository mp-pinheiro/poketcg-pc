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

# >>> factory Func_1d765
CONTRACT["Func_1d765"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_1d765"] = [
    {"wram": {0xD647: b"\x00\x00\x00\x00", 0xD659: b"\x00\x00\x00\x00", 0xD65F: b"\x00\x00\x00\x00", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 4, 0xD65F: 4, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    dict(POISON, wram={0xD647: b"\x02\x01\x05\x01", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\xAA", 0xCABB: b"\x00"}, read={0xD659: 4, 0xD65F: 4, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}),
    {"wram": {0xD647: b"\x01\x00\x00\x00", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 4, 0xD65F: 4, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    {"wram": {0xD647: b"\x01\x01\x01\x00", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 4, 0xD65F: 4, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    {"wram": {0xD647: b"\x03\x02\x05\x02", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 4, 0xD65F: 4, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
]
# <<< factory Func_1d765

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_1d758
MUTATIONS["Func_1d758"] = {"source_symbol": "Func_1d758", "before": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) & (uint8_t)~STAT_LYC_MASK));", "after": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) | STAT_LYC_MASK));", "case_ids": ["Func_1d758-0", "Func_1d758-1"]}
# <<< factory-mutation Func_1d758
# >>> factory-mutation Func_1d765
MUTATIONS["Func_1d765"] = {"source_symbol": "Func_1d765", "before": "if (gb_read8(wd648_ADDR) == 0x00u)", "after": "if (gb_read8(wd648_ADDR) == 0x01u)", "case_ids": ["Func_1d765-0", "Func_1d765-1", "Func_1d765-2", "Func_1d765-3", "Func_1d765-4"]}
# <<< factory-mutation Func_1d765
