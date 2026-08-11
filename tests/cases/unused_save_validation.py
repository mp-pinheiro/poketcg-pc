POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hBankSRAM = 0xFF81
hProbeGuard = 0xC000
sCardCollection = 0xA100
sUnusedSaveDataValidationByte = 0xA00B
CHECKSUM_SIZE = 0x250

CONTRACT = {
    "StubbedUnusedSaveDataValidation": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
    "UnusedCalculateSaveDataValidationByte": {
        "compare": ("a", "f"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "StubbedUnusedSaveDataValidation": [
        {"read": {hProbeGuard: 1}},
        dict(POISON, read={hProbeGuard: 1}),
    ],
    "UnusedCalculateSaveDataValidationByte": [
        {"ramg": True, "sram": {0: {sCardCollection: b"\x00" * CHECKSUM_SIZE}},
         "read": {sUnusedSaveDataValidationByte: 1}},
        dict(POISON, ramg=True,
             sram={0: {sCardCollection: bytes(range(256)) + bytes(range(256)) + bytes(range(80))}},
             read={sUnusedSaveDataValidationByte: 1}),
        {"wram": {hBankSRAM: b"\x01"}, "ramg": True,
         "sram": {0: {sCardCollection: b"\xAA" * CHECKSUM_SIZE,
                      sUnusedSaveDataValidationByte: b"\x5A"}},
         "read": {sUnusedSaveDataValidationByte: 1}},
        {"ramg": False,
         "sram": {0: {sCardCollection: b"\x11" * CHECKSUM_SIZE,
                      sUnusedSaveDataValidationByte: b"\x5A"}},
         "read": {sUnusedSaveDataValidationByte: 1}},
        {"ramg": True,
         "sram": {0: {sCardCollection - 1: b"\x7E",
                      sCardCollection: bytes((i * 13 + 3) & 0xFF for i in range(CHECKSUM_SIZE)),
                      sCardCollection + CHECKSUM_SIZE: b"\x81",
                      sUnusedSaveDataValidationByte: b"\x00"}},
         "sread": {0: {sCardCollection - 1: 1,
                       sCardCollection: CHECKSUM_SIZE,
                       sCardCollection + CHECKSUM_SIZE: 1,
                       sUnusedSaveDataValidationByte: 1}},
         "read": {sUnusedSaveDataValidationByte: 1}},
    ],
}

MUTATIONS = {
    "StubbedUnusedSaveDataValidation": {
        "source_symbol": "StubbedUnusedSaveDataValidation",
        "before": "void StubbedUnusedSaveDataValidation(void)\n{\n}",
        "after": "void StubbedUnusedSaveDataValidation(void)\n{\n\tgb_write8(0xC000, 0x01);\n}",
        "case_ids": ["StubbedUnusedSaveDataValidation-0", "StubbedUnusedSaveDataValidation-1"],
    },
    "UnusedCalculateSaveDataValidationByte": {
        "source_symbol": "UnusedCalculateSaveDataValidationByte",
        "before": "gb_write8(sUnusedSaveDataValidationByte_ADDR, value);",
        "after": "gb_write8(sUnusedSaveDataValidationByte_ADDR, (uint8_t)(value ^ 0xFFu));",
        "case_ids": ["UnusedCalculateSaveDataValidationByte-0", "UnusedCalculateSaveDataValidationByte-1", "UnusedCalculateSaveDataValidationByte-2", "UnusedCalculateSaveDataValidationByte-3", "UnusedCalculateSaveDataValidationByte-4"],
    },
}
from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
