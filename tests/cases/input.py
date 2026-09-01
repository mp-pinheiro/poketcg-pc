"""Oracle-diff cases for poketcg/src/home/input.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "ReadJoypad": {"compare": ("d", "e"), "preserve": ("d", "e")},
    "SaveButtonsHeld": {"compare": ("b", "c", "d", "e", "f", "hl"), "preserve": ("b", "d", "e", "f", "hl")},
    "ClearJoypad": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "ReadJoypad": [
        {"wram": {0xFF8D: b"\x00\x00\x00\x00\x00"},
         "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\x12\x34\x56\x78\x9A"},
             read={0xFF8D: 5}),
        {"keys": 0x01, "wram": {0xFF8D: b"\x00\x00\x00\x00\x00"},
         "read": {0xFF8D: 5}},
        {"wram": {0xFF8D: b"\x00\x00\x00\x0F\x00"},
         "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\x00\x00\x00\x0F\x00"},
             read={0xFF8D: 5}),
    ],
    "SaveButtonsHeld": [
        {"c": 0x00, "read": {0xFF90: 1}},
        dict(POISON, c=0xA5, read={0xFF90: 1}),
    ],
    "ClearJoypad": [
        {"wram": {0xFF8D: b"\x01\x02\x03\x04\x05"},
         "read": {0xFF8D: 5}},
        dict(POISON, wram={0xFF8D: b"\x01\x02\x03\x04\x05"},
             read={0xFF8D: 5}),
    ],
}
# >>> factory Reset
CONTRACT["Reset"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["Reset"] = [
    {"wram": {0xCAB3: b"\x37"}, "read": {0xCAB3: 1}},
    dict(POISON, wram={0xCAB3: b"\xC3"}, read={0xCAB3: 1}),
]
# <<< factory Reset

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SaveButtonsHeld": {
        "source_symbol": "SaveButtonsHeld",
        "before": "gb_write8(JOYP, JOYP_GET_NONE);",
        "after": "gb_write8(hKeysHeld_ADDR, (uint8_t)(c + 1u));",
        "case_ids": ["SaveButtonsHeld-0", "SaveButtonsHeld-1"],
    },
}
# >>> factory-mutation Reset
MUTATIONS["Reset"] = {"source_symbol": "Reset", "before": "return wInitialA;", "after": "return 0u;", "case_ids": ["Reset-0", "Reset-1"]}
# <<< factory-mutation Reset
# >>> factory-completion Reset
for _record in SCHEMA2_CASES["Reset"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x0150, "bank": 0}
# <<< factory-completion Reset
# >>> factory-mutation ReadJoypad
MUTATIONS["ReadJoypad"] = {"source_symbol": "ReadJoypad", "before": "\t\t(void)Reset();\n\t\treturn;", "after": "\t\t(void)Reset();\n\t\tSaveButtonsHeld(c);\n\t\treturn;", "case_ids": ["ReadJoypad-3", "ReadJoypad-4"]}
# <<< factory-mutation ReadJoypad
# >>> factory-completion ReadJoypad
# The reset combo falls into Reset's `jp Start`, which never returns; the
# combo witnesses stop the oracle at that jump instead (input.asm Reset+4).
SCHEMA2_CASES["ReadJoypad"][3]["completion"] = {"mode": "pre-ret", "pc": 0x051F}
SCHEMA2_CASES["ReadJoypad"][4]["completion"] = {"mode": "pre-ret", "pc": 0x051F}
# <<< factory-completion ReadJoypad
