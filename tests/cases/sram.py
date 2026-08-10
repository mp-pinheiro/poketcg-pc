"""Oracle-diff cases for poketcg/src/home/sram.asm."""

HBANK = 0xFF81

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "BankswitchSRAM": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "b", "c", "d", "e", "hl"),
    },
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

MUTATIONS = {
    "BankswitchSRAM": {
        "source_symbol": "BankswitchSRAM",
        "source": "src/home/switch_sram.c",
        "before": "mbc5_write(0x4000, bank);\n\tmbc5_write(0x0000, 0x0A);",
        "after": "mbc5_write(0x4000, bank);\n\tmbc5_write(0x0000, 0x00);",
        "case_ids": ["BankswitchSRAM-0", "BankswitchSRAM-1", "BankswitchSRAM-2"],
    },
}
