POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sChallengeMachineOpponents = 0xBA4B

CONTRACT = {
    "ChallengeMachine_CheckIfOpponentAlreadySelected": {
        "compare": ("a", "f", "hl"),
        "preserve": ("b", "d", "e"),
    },
    "ChallengeMachine_PrintText": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c"),
    },
}

CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES = {
    "ChallengeMachine_CheckIfOpponentAlreadySelected": [
        {"a": 0, "c": 0, "sread": {0: {sChallengeMachineOpponents: 1}}},
        dict(POISON, a=3, c=3,
             sram={0: {sChallengeMachineOpponents: b"\x01\x02\x03\x04\x05"}}),
        {"a": 9, "c": 1,
         "sram": {0: {sChallengeMachineOpponents: b"\x01"}}},
        {"a": 2, "c": 2,
         "sram": {0: {sChallengeMachineOpponents: b"\x01\x02"}}},
        {"a": 0xAA, "c": 0,
         "sram": {0: {sChallengeMachineOpponents: bytes(255) + b"\xAA"}}},
    ],
    "ChallengeMachine_PrintText": [
        {"hl": 0, "b": 0, "c": 0},
        dict(POISON, hl=0xC100, b=3, c=4,
             wram={0xC100: b"\x01\x00"}, setup=SETUP,
             read={**CACHE_READ, **PLACEMENT_READ}, vread=VRAM_READ),
        {"hl": 0xC100, "b": 1, "c": 2, "wram": {0xC100: b"\x00\x00"}},
        {"hl": 0xC1FF, "b": 0xFF, "c": 0xFF,
         "wram": {0xC1FF: b"\x01\x00", 0xC200: b"\x00"},
         "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": VRAM_READ},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "ChallengeMachine_CheckIfOpponentAlreadySelected": {
        "source_symbol": "ChallengeMachine_CheckIfOpponentAlreadySelected",
        "before": "hl = (uint16_t)(hl + 1u);",
        "after": "hl = (uint16_t)(hl + 2u);",
        "case_ids": ["ChallengeMachine_CheckIfOpponentAlreadySelected-0", "ChallengeMachine_CheckIfOpponentAlreadySelected-1", "ChallengeMachine_CheckIfOpponentAlreadySelected-2", "ChallengeMachine_CheckIfOpponentAlreadySelected-3", "ChallengeMachine_CheckIfOpponentAlreadySelected-4"],
    },
    "ChallengeMachine_PrintText": {
        "source_symbol": "ChallengeMachine_PrintText",
        "before": "InitTextPrinting(b, c);",
        "after": "InitTextPrinting(c, b);",
        "case_ids": ["ChallengeMachine_PrintText-1", "ChallengeMachine_PrintText-3"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
