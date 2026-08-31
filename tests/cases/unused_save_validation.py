"""Oracle-diff cases for poketcg/src/engine/unused_save_validation.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory StubbedUnusedSaveDataValidation
CONTRACT["StubbedUnusedSaveDataValidation"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["StubbedUnusedSaveDataValidation"] = [
    {"wram": {0xC100: b"\x00"}, "read": {0xC100: 1}},
    dict(POISON, wram={0xC100: b"\xAB"}, read={0xC100: 1}),
]
# <<< factory StubbedUnusedSaveDataValidation

# >>> factory UnusedCalculateSaveDataValidationByte
hBankSRAM = 0xFF81
sCardCollection = 0xA100
sUnusedSaveDataValidationByte = 0xA00B
SAVE_VALIDATION_RANGE = 0x250
_CHECKSUM_PATTERN = bytes((i * 37 + 5) & 0xFF for i in range(SAVE_VALIDATION_RANGE))
_CHECKSUM_PATTERN_2 = bytes((i * 91 + 13) & 0xFF for i in range(SAVE_VALIDATION_RANGE))

CONTRACT["UnusedCalculateSaveDataValidationByte"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UnusedCalculateSaveDataValidationByte"] = [
    {"sram": {0: {sUnusedSaveDataValidationByte: b"\xFF"}}},
    {"sram": {0: {sCardCollection: _CHECKSUM_PATTERN, sUnusedSaveDataValidationByte: b"\x00"}}},
    {"wram": {hBankSRAM: b"\x01"}, "sram": {0: {sUnusedSaveDataValidationByte: b"\x77"}}},
    dict(POISON, wram={hBankSRAM: b"\x00"},
         sram={0: {sCardCollection: _CHECKSUM_PATTERN_2, sUnusedSaveDataValidationByte: b"\x00"}}),
    # nonzero-bank early exit; 0..3 is the probe's valid ram_bank domain
    dict(POISON, wram={hBankSRAM: b"\x03"}),
]
# <<< factory UnusedCalculateSaveDataValidationByte

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hBankSRAM = 0xFF81
wTileMapFill = 0xCAB6
# <<< factory-cases-statics

# >>> factory UnusedSaveDataValidation
CONTRACT["UnusedSaveDataValidation"] = {"compare": (), "preserve": ()}
CASES["UnusedSaveDataValidation"] = [
    {"oracle": False, "evidence": "primary", "why": "The routine is unreferenced and its bounded SRAM-bank guard is the observable path available to this probe.", "ram_bank": 1, "wram": {hBankSRAM: b"\x01", wTileMapFill: b"\x5A"}, "read": {wTileMapFill: 1}, "expect": {wTileMapFill: b"\x5A"}},
    dict(POISON, oracle=False, evidence="primary", why="Poisoned entry registers do not affect the early SRAM-bank return.", ram_bank=1, wram={hBankSRAM: b"\x01", wTileMapFill: b"\xA5"}, read={wTileMapFill: 1}, expect={wTileMapFill: b"\xA5"}),
]
# <<< factory UnusedSaveDataValidation

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation StubbedUnusedSaveDataValidation
MUTATIONS["StubbedUnusedSaveDataValidation"] = {
    "source_symbol": "StubbedUnusedSaveDataValidation",
    "before": "void StubbedUnusedSaveDataValidation(void)\n{\n}",
    "after": "void StubbedUnusedSaveDataValidation(void)\n{\n\tgb_write8(0xC100u, 0xFFu);\n}",
    "case_ids": ["StubbedUnusedSaveDataValidation-0", "StubbedUnusedSaveDataValidation-1"],
}
# <<< factory-mutation StubbedUnusedSaveDataValidation
# >>> factory-mutation UnusedCalculateSaveDataValidationByte
MUTATIONS["UnusedCalculateSaveDataValidationByte"] = {
    "source_symbol": "UnusedCalculateSaveDataValidationByte",
    "before": "checksum ^= gb_read8((uint16_t)(sCardCollection_ADDR + i));",
    "after": "checksum += gb_read8((uint16_t)(sCardCollection_ADDR + i));",
    "case_ids": ["UnusedCalculateSaveDataValidationByte-1", "UnusedCalculateSaveDataValidationByte-3"],
}
# <<< factory-mutation UnusedCalculateSaveDataValidationByte
# >>> factory-mutation UnusedSaveDataValidation
MUTATIONS["UnusedSaveDataValidation"] = {"source_symbol": "UnusedSaveDataValidation", "before": "if (gb_read8(0xFF81u) != 0u)\n\t\treturn;", "after": "if (gb_read8(0xFF81u) != 0u) {\n\t\tgb_write8(0xCAB6u, 0xFFu);\n\t\treturn;\n\t}", "case_ids": ["UnusedSaveDataValidation-0", "UnusedSaveDataValidation-1"]}
# <<< factory-mutation UnusedSaveDataValidation
# >>> factory-completion UnusedSaveDataValidation
for _record in SCHEMA2_CASES["UnusedSaveDataValidation"]:
    _record["completion"] = {"mode": "return"}
# <<< factory-completion UnusedSaveDataValidation
