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

# >>> factory Func_1d7ee
CONTRACT["Func_1d7ee"] = {"compare": (), "preserve": ()};
CASES["Func_1d7ee"] = [
    {"vread": {0: {0x9C00: 0x260}}},
    dict(POISON, vread={0: {0x9C00: 0x260}}),
]
# <<< factory Func_1d7ee

# >>> factory-cases-statics
wd647 = 0xD647
wd648 = 0xD648
wd649 = 0xD649
wd64a = 0xD64A
wd657 = 0xD657
wLCDCFunctionTrampoline = 0xCACD
# <<< factory-cases-statics

# >>> factory Func_1d705
CONTRACT["Func_1d705"] = {"compare": (), "preserve": ()};
CASES["Func_1d705"] = [
    {"read": {wd647: 1, wd648: 1, wd649: 1, wd64a: 1, wd657: 1, 0xFF41: 1, 0xFF45: 1, 0xFFFF: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "read": {wd647: 1, wd648: 1, wd649: 1, wd64a: 1, wd657: 1, 0xFF41: 1, 0xFF45: 1, 0xFFFF: 1}},
]
# <<< factory Func_1d705

# >>> factory PlayCreditsSequence
CONTRACT["PlayCreditsSequence"] = {"compare": (), "preserve": ()}
CASES["PlayCreditsSequence"] = [
    dict(oracle=False, evidence="primary", why="The bounded credits prefix stops immediately before its command-frame loop after resetting the overworld event byte and selecting credits music.", wram={0xD324: b"\xA5", 0xDD80: b"\x7F"}, read={0xD324: 1, 0xDD80: 1}, expect={0xD324: b"\x00", 0xDD80: b"\x12"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, oracle=False, evidence="primary", why="The credits setup writes the same event byte and music selection with poisoned entry registers.", wram={0xD324: b"\xA5", 0xDD80: b"\x7F"}, read={0xD324: 1, 0xDD80: 1}, expect={0xD324: b"\x00", 0xDD80: b"\x12"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PlayCreditsSequence

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_1d758
MUTATIONS["Func_1d758"] = {"source_symbol": "Func_1d758", "before": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) & (uint8_t)~STAT_LYC_MASK));", "after": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) | STAT_LYC_MASK));", "case_ids": ["Func_1d758-0", "Func_1d758-1"]}
# <<< factory-mutation Func_1d758
# >>> factory-mutation Func_1d765
MUTATIONS["Func_1d765"] = {"source_symbol": "Func_1d765", "before": "if (gb_read8(wd648_ADDR) == 0x00u)", "after": "if (gb_read8(wd648_ADDR) == 0x01u)", "case_ids": ["Func_1d765-0", "Func_1d765-1", "Func_1d765-2", "Func_1d765-3", "Func_1d765-4"]}
# <<< factory-mutation Func_1d765
# >>> factory-mutation Func_1d7ee
MUTATIONS["Func_1d7ee"] = {"source_symbol": "Func_1d7ee", "before": "FillRectangle(0x00u, 20u, 18u, 0x0020u, 0x0000u);", "after": "FillRectangle(0x01u, 20u, 18u, 0x0020u, 0x0000u);", "case_ids": ["Func_1d7ee-0", "Func_1d7ee-1"]}
# <<< factory-mutation Func_1d7ee
# >>> factory-mutation Func_1d705
MUTATIONS["Func_1d705"] = {
    "source_symbol": "Func_1d705",
    "before": "wd647 = 0x91u;",
    "after": "wd647 = 0x90u;",
    "case_ids": ["Func_1d705-0", "Func_1d705-1"],
}
# <<< factory-mutation Func_1d705
# >>> factory-mutation PlayCreditsSequence
MUTATIONS["PlayCreditsSequence"] = {"source_symbol": "PlayCreditsSequence", "before": "\tgb_write8((uint16_t)(wOWMapEvents_ADDR + 1u), 0u);", "after": "\tgb_write8((uint16_t)(wOWMapEvents_ADDR + 1u), 1u);", "case_ids": ["PlayCreditsSequence-0", "PlayCreditsSequence-1"]}
# <<< factory-mutation PlayCreditsSequence
# >>> factory-completion PlayCreditsSequence
for _record in SCHEMA2_CASES["PlayCreditsSequence"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x56C8, "bank": 7}
# <<< factory-completion PlayCreditsSequence
