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
