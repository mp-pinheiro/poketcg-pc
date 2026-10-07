"""Oracle-diff cases for poketcg/src/engine/credits.asm."""
from tests.cases._symbols import sym, sym_bank

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
    {"wram": {sym("wd647"): b"\x00\x00\x00\x00", sym("wd659"): b"\x00\x00\x00\x00", sym("wd65f"): b"\x00\x00\x00\x00", sym("wd665"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("wd659"): 6, sym("wd65f"): 6, sym("wd665"): 1, sym("wLCDC"): 1, sym("hWX"): 1, sym("hWY"): 1}},
    dict(POISON, wram={sym("wd647"): b"\x02\x01\x05\x01", sym("wd659"): b"\xAA\xAA\xAA\xAA", sym("wd65f"): b"\xAA\xAA\xAA\xAA", sym("wd665"): b"\xAA", sym("wLCDC"): b"\x00"}, read={sym("wd659"): 6, sym("wd65f"): 6, sym("wd665"): 1, sym("wLCDC"): 1, sym("hWX"): 1, sym("hWY"): 1}),
    {"wram": {sym("wd647"): b"\x01\x00\x00\x00", sym("wd659"): b"\xAA\xAA\xAA\xAA", sym("wd65f"): b"\xAA\xAA\xAA\xAA", sym("wd665"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("wd659"): 6, sym("wd65f"): 6, sym("wd665"): 1, sym("wLCDC"): 1, sym("hWX"): 1, sym("hWY"): 1}},
    {"wram": {sym("wd647"): b"\x01\x01\x01\x00", sym("wd659"): b"\xAA\xAA\xAA\xAA", sym("wd65f"): b"\xAA\xAA\xAA\xAA", sym("wd665"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("wd659"): 6, sym("wd65f"): 6, sym("wd665"): 1, sym("wLCDC"): 1, sym("hWX"): 1, sym("hWY"): 1}},
    {"wram": {sym("wd647"): b"\x03\x02\x05\x02", sym("wd659"): b"\xAA\xAA\xAA\xAA", sym("wd65f"): b"\xAA\xAA\xAA\xAA", sym("wd665"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("wd659"): 6, sym("wd65f"): 6, sym("wd665"): 1, sym("wLCDC"): 1, sym("hWX"): 1, sym("hWY"): 1}},
    # credits-1 863612: the first credits window (wd647=0, wd648=2, wd649=144,
    # wd64a=0): one split, and with no second window the list ends after it
    # (credits.asm:155 `jr z, .asm_1d7e2`), the terminator at wd65f+1.
    dict(_credits_scroll_table_fixture(vram=False, bank=7), **_CREDITS_SCROLL_TABLE_REGS, read={sym("wd659"): 6, sym("wd65f"): 6, sym("wd665"): 1, sym("hWX"): 1, sym("hWY"): 1, sym("wLCDC"): 1}),
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
wd647 = sym("wd647")
wd648 = sym("wd648")
wd649 = sym("wd649")
wd64a = sym("wd64a")
wd657 = sym("wd657")
wLCDCFunctionTrampoline = sym("wLCDCFunctionTrampoline")
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
_CREDITS_READ = {sym("wOWMapEvents") + 1: 1, sym("wCurSongID"): 1, sym("wMastersBeatenList"): 10, sym("wDoFrameFunction"): 2, sym("wd648"): 1, sym("wd657"): 1, 0xFF41: 1, 0xFF45: 1}
CASES["PlayCreditsSequence"] = [
    {"wram": {sym("wCurSongID"): b"\x7F", sym("wOWMapEvents") + 1: b"\xFF", sym("wMastersBeatenList"): b"\x00" * 10, sym("wLCDC"): b"\xC3", 0xFF40: b"\xC3"},
     "read": _CREDITS_READ, "ramg": True, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={sym("wCurSongID"): b"\x7F", sym("wOWMapEvents") + 1: b"\xFF", sym("wMastersBeatenList"): b"\x03\x07\x00" + b"\x00" * 7, sym("wLCDC"): b"\xC3", 0xFF40: b"\xC3"},
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
    _record["completion"] = {"mode": "entry", "pc": sym("FlashWhiteScreen"), "bank": sym_bank("FlashWhiteScreen"),
                             "routine": "FlashWhiteScreen"}
# <<< factory-completion PlayCreditsSequence
