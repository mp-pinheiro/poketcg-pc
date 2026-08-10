"""Oracle-diff cases for poketcg/src/home/sram.asm."""

HBANK = 0xFF81

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "BankswitchSRAM": ("a", "b", "c", "d", "e", "hl"),
}

CASES = {
    "BankswitchSRAM": [
        {"a": 0, "sram": {0: {0xA000: b"\xAA"}, 1: {0xA000: b"\xBB"}},
         "read": {0xA000: 1, HBANK: 1}},
        dict(POISON, a=1, sram={0: {0xA000: b"\xAA"}, 1: {0xA000: b"\xBB"}},
             read={0xA000: 1, HBANK: 1}),
        {"a": 3, "sram": {0: {0xA000: b"\x01"}, 3: {0xA000: b"\x99"}},
         "read": {0xA000: 1, HBANK: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
