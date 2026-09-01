"""Oracle-diff cases for poketcg/src/home/clear_sram.asm.

ValidateSRAM is not registered: both non-matching paths call InitSaveDataAndSetUppercase
(home/init.asm, unported), and the only clean path (signature $04,$21,$05 match) writes
no memory and yields only a carry flag -- not enough coverage to register.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "ClearSRAMBank": {
        "compare": ("a", "d", "e", "f"),
        "preserve": ("a", "d", "e", "f"),
    },
    "RestartSRAM": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("d", "e"),
    },
}

SIG = b"\x04\x21\x05"

CASES = {
    "ClearSRAMBank": [
        {"a": 1, "sram": {0: {0xA000: b"\x11\x22"}, 1: {0xA000: b"\xaa\xbb\xcc"}}},
        {"a": 2, "sram": {2: {0xA000: b"\xde\xad", 0xBFFF: b"\x7f"}}, "sread": {2: {0xBFFF: 1}}},
        {"a": 1, "sram": {1: {0xA000: b"\x01" * 8}}, "sread": {1: {0xBFFF: 1, 0xA800: 4}}},
        dict(POISON, a=3, sram={3: {0xA000: b"\x99\x88\x77\x66\x55\x44"}}),
    ],
    "RestartSRAM": [
        {"instruction_budget": 300_000, "cycle_budget": 2_000_000,
         "sram": {0: {0xA000: b"\xff" * 8}, 1: {0xA000: b"\xee" * 4},
                  2: {0xA000: b"\x01"}, 3: {0xA000: b"\x02"}},
         "sread": {0: {0xBFFF: 1}, 1: {0xBFFF: 1}, 2: {0xBFFF: 1}, 3: {0xBFFF: 1}}},
        dict(POISON, instruction_budget=300_000, cycle_budget=2_000_000,
             sram={0: {0xA000: b"\xaa\xbb\xcc"}, 3: {0xBFFF: b"\xff"}}),
    ],
}

MUTATIONS = {
    "ClearSRAMBank": {
        "source_symbol": "ClearSRAMBank",
        "before": "for (uint16_t i = 0; i < 0x2000u; i++)",
        "after": "for (uint16_t i = 0; i < 0x1FFFu; i++)",
        "case_ids": ["ClearSRAMBank-1", "ClearSRAMBank-0", "ClearSRAMBank-2", "ClearSRAMBank-3"],
    },
}
# >>> factory ValidateSRAM
CONTRACT["ValidateSRAM"] = {"compare": (), "preserve": ()}
CASES["ValidateSRAM"] = [
    {"instruction_budget": 500000, "cycle_budget": 4000000,
     "sram": {0: {0xA000: bytes([0x41, 0x93] * 4096)}},
     "sread": {0: {0xA000: 8, 0xBFF8: 8}}},
    {"sram": {0: {0xA000: b"\x04\x21\x05\x00" * 2048}},
     "sread": {0: {0xA000: 8}}},
    dict(POISON, instruction_budget=500000, cycle_budget=4000000,
         sram={0: {0xA000: bytes(8192)}},
         sread={0: {0xA000: 8, 0xBFF8: 8}}),
]
# <<< factory ValidateSRAM

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation ValidateSRAM
MUTATIONS["ValidateSRAM"] = {"source_symbol": "ValidateSRAM", "before": "\t\t\tif (b2 == 0x05u)", "after": "\t\t\tif (b2 == 0x06u)", "case_ids": ["ValidateSRAM-1"]}
# <<< factory-mutation ValidateSRAM
