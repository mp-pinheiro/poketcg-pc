"""Oracle-diff cases for poketcg/src/home/switch_rom.asm."""

HBANK_ROM = 0xFF80

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "BankswitchROM": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "BankswitchROM": [
        {"a": 0, "read": {HBANK_ROM: 1}},
        dict(POISON, a=1, wram={HBANK_ROM: b"\x05"}, read={HBANK_ROM: 1}),
        {"a": 0xFF, "wram": {HBANK_ROM: b"\x01"},
         "read": {HBANK_ROM: 1}},
    ],
}

# >>> factory-cases-statics
HBANK_ROM = 0xFF80
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory BankpushROM
CONTRACT["BankpushROM"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e"), "wram_out": True}
CASES["BankpushROM"] = [
    {"a": 0x00, "hl": 0x0000, "hram": {HBANK_ROM: b"\x05"}, "read": {HBANK_ROM: 1}},
    dict(POISON, hram={HBANK_ROM: b"\x05"}, read={HBANK_ROM: 1}),
    {"a": 0xFE, "b": 0x12, "c": 0x34, "d": 0x56, "e": 0x78, "hl": 0xC3FF, "hram": {HBANK_ROM: b"\x01"}, "read": {HBANK_ROM: 1}},
]
# <<< factory BankpushROM

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "BankswitchROM": {
        "source_symbol": "BankswitchROM",
        "source": "src/home/switch_rom.c",
        "before": "hBankROM = bank;",
        "after": "hBankROM = 0;",
        "case_ids": ["BankswitchROM-0", "BankswitchROM-1", "BankswitchROM-2"],
    },
}
# >>> factory-mutation BankpushROM
MUTATIONS["BankpushROM"] = {"source_symbol": "BankpushROM", "before": "\tuint8_t bank = (uint8_t)(a + bank_offset);", "after": "\tuint8_t bank = (uint8_t)(a + (uint8_t)(bank_offset + 1u));", "case_ids": ["BankpushROM-0", "BankpushROM-1", "BankpushROM-2"]}
# <<< factory-mutation BankpushROM
