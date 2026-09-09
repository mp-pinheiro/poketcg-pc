"""Oracle-diff cases for poketcg/src/engine/credits.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

from tests.cases._fixtures import credits_scroll_table_fixture as _credits_scroll_table_fixture, CREDITS_SCROLL_TABLE_REGS as _CREDITS_SCROLL_TABLE_REGS

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
    {"wram": {0xD647: b"\x00\x00\x00\x00", 0xD659: b"\x00\x00\x00\x00", 0xD65F: b"\x00\x00\x00\x00", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 6, 0xD65F: 6, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    dict(POISON, wram={0xD647: b"\x02\x01\x05\x01", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\xAA", 0xCABB: b"\x00"}, read={0xD659: 6, 0xD65F: 6, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}),
    {"wram": {0xD647: b"\x01\x00\x00\x00", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 6, 0xD65F: 6, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    {"wram": {0xD647: b"\x01\x01\x01\x00", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 6, 0xD65F: 6, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    {"wram": {0xD647: b"\x03\x02\x05\x02", 0xD659: b"\xAA\xAA\xAA\xAA", 0xD65F: b"\xAA\xAA\xAA\xAA", 0xD665: b"\x00", 0xCABB: b"\x00"}, "read": {0xD659: 6, 0xD65F: 6, 0xD665: 1, 0xCABB: 1, 0xFF94: 1, 0xFF95: 1}},
    # credits-1 863612: the first credits window (wd647=0, wd648=2, wd649=144,
    # wd64a=0): one split, and with no second window the list ends after it
    # (credits.asm:155 `jr z, .asm_1d7e2`), the terminator at wd65f+1.
    dict(_credits_scroll_table_fixture(vram=False, bank=7), **_CREDITS_SCROLL_TABLE_REGS, read={0xD659: 6, 0xD65F: 6, 0xD665: 1, 0xFF94: 1, 0xFF95: 1, 0xCABB: 1}),
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
_CREDITS_READ = {0xD324: 1, 0xDD80: 1, 0xD3BB: 10, 0xCAD3: 2, 0xD648: 1, 0xD657: 1, 0xFF41: 1, 0xFF45: 1}
CASES["PlayCreditsSequence"] = [
    {"wram": {0xDD80: b"\x7F", 0xD324: b"\xFF", 0xD3BB: b"\x00" * 10, 0xCABB: b"\xC3", 0xFF40: b"\xC3"},
     "read": _CREDITS_READ, "ramg": True, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xDD80: b"\x7F", 0xD324: b"\xFF", 0xD3BB: b"\x03\x07\x00" + b"\x00" * 7, 0xCABB: b"\xC3", 0xFF40: b"\xC3"},
         read=_CREDITS_READ, ramg=True, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PlayCreditsSequence

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_1d758
MUTATIONS["Func_1d758"] = {"source_symbol": "Func_1d758", "before": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) & (uint8_t)~STAT_LYC_MASK));", "after": "\tgb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) | STAT_LYC_MASK));", "case_ids": ["Func_1d758-0", "Func_1d758-1"]}
# <<< factory-mutation Func_1d758
# >>> factory-mutation Func_1d765
MUTATIONS["Func_1d765"] = {"source_symbol": "Func_1d765", "before": "\t\t\tif (gb_read8(wd64a_ADDR) == 0x00u)\n\t\t\t\tgoto terminate;\n\t\t\ta = (uint8_t)(gb_read8(wd649_ADDR) - 1u);\n\t\t\tgb_write8(de, a);\n\t\t\tde = (uint16_t)(de + 1u);\n\t\t\tgb_write8(hl, 0x07u);\n\t\t\thl = (uint16_t)(hl + 1u);\n\t\t}", "after": "\t\t\tif (gb_read8(wd64a_ADDR) != 0x00u) {\n\t\t\ta = (uint8_t)(gb_read8(wd649_ADDR) - 1u);\n\t\t\tgb_write8(de, a);\n\t\t\tde = (uint16_t)(de + 1u);\n\t\t\tgb_write8(hl, 0x07u);\n\t\t\thl = (uint16_t)(hl + 1u);\n\t\t\t}\n\t\t}", "case_ids": ["Func_1d765-5"]}
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
MUTATIONS["PlayCreditsSequence"] = {"source_symbol": "PlayCreditsSequence", "before": "\t(void)AddAllMastersToMastersBeatenList(&f);", "after": "\t(void)f;", "case_ids": ["PlayCreditsSequence-0", "PlayCreditsSequence-1"]}
# <<< factory-mutation PlayCreditsSequence
# >>> factory-completion PlayCreditsSequence
for _record in SCHEMA2_CASES["PlayCreditsSequence"]:
    _record["completion"] = {"mode": "entry", "pc": 0x4031, "bank": 4,
                             "routine": "FlashWhiteScreen"}
# <<< factory-completion PlayCreditsSequence
