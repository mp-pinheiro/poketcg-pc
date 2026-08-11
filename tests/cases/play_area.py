wOAM = 0xCA00
wVBlankOAMCopyToggle = 0xCAC0
OAM_SIZE = 160

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "ZeroObjectPositionsAndToggleOAMCopy_Bank6": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "d", "e"),
    },
}

OAM = bytes((0x10, 0x20, 0x30, 0x40)) * 40

CASES = {
    "ZeroObjectPositionsAndToggleOAMCopy_Bank6": [
        {"wram": {wOAM: b"\x00" * OAM_SIZE,
                  wVBlankOAMCopyToggle: b"\x00"},
         "read": {wOAM: OAM_SIZE, wVBlankOAMCopyToggle: 1}},
        dict(POISON, wram={wOAM: OAM,
                           wVBlankOAMCopyToggle: b"\xFF"},
             read={wOAM: OAM_SIZE, wVBlankOAMCopyToggle: 1}),
        {"wram": {wOAM: OAM,
                  wVBlankOAMCopyToggle: b"\x00"},
         "read": {wOAM: OAM_SIZE, wVBlankOAMCopyToggle: 1}},
    ],
}

MUTATIONS = {
    "ZeroObjectPositionsAndToggleOAMCopy_Bank6": {
        "source_symbol": "ZeroObjectPositionsAndToggleOAMCopy_Bank6",
        "before": "gb_write8(wVBlankOAMCopyToggle_ADDR, 1);",
        "after": "gb_write8(wVBlankOAMCopyToggle_ADDR, 0);",
        "case_ids": ["ZeroObjectPositionsAndToggleOAMCopy_Bank6-0",
                     "ZeroObjectPositionsAndToggleOAMCopy_Bank6-1",
                     "ZeroObjectPositionsAndToggleOAMCopy_Bank6-2"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
