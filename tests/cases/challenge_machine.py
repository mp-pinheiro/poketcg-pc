POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sChallengeMachineOpponents = 0xBA4B

CONTRACT = {
    "ChallengeMachine_CheckIfOpponentAlreadySelected": {
        "compare": ("a", "b", "d", "e", "f", "hl"),
        "preserve": ("b", "d", "e"),
    },
    "ChallengeMachine_PrintText": {
        "compare": ("d", "e", "hl"),
        "preserve": (),
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
        {"hl": 0xC100, "b": 0, "c": 0, "wram": {0xC100: b"\x00\x00"}},
        dict(POISON, hl=0xC100, b=3, c=4,
             wram={0xC100: b"\x01\x00"}, setup=SETUP,
             read={**CACHE_READ, **PLACEMENT_READ}, vread=VRAM_READ),
        {"hl": 0xC100, "b": 1, "c": 2, "wram": {0xC100: b"\x00\x00"}},
        {"hl": 0xC1FF, "b": 0xFF, "c": 0xFF,
         "wram": {0xC1FF: b"\x01\x00", 0xC200: b"\x00"},
         "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": VRAM_READ},
    ],
}

# >>> factory ChallengeMachine_PickOpponentSequence
CONTRACT["ChallengeMachine_PickOpponentSequence"] = {"compare": (), "preserve": ()}
CASES["ChallengeMachine_PickOpponentSequence"] = [
    # All-zero entry: nothing pre-seeded, RNG state at its reset value. The five
    # opponent bytes, the opponent number, the record-increased flag, the five
    # duel-result bytes and the two consecutive-win bytes are all diffed as one
    # block ($BA47..$BA68).
    {"sram": {0: {0xBA47: b"\x00" * 0x22}},
     "sread": {0: {0xBA47: 0x22}}},
    # Poisoned entry registers: the routine takes no arguments and must ignore
    # every one of them; the SRAM image must be identical to the case above's
    # shape (same RNG start, so the same picks).
    dict(POISON,
         sram={0: {0xBA47: b"\x00" * 0x22}},
         sread={0: {0xBA47: 0x22}}),
    # Pre-existing duel results all nonzero: every one of the five bytes at
    # sChallengeMachineDuelResults must be cleared. A clear loop that ran four
    # times (or six) shows up here and nowhere else.
    {"sram": {0: {0xBA47: b"\x00" * 0x09,
                  0xBA50: b"\x11\x22\x33\x44\x55",
                  0xBA55: b"\x77",
                  0xBA68: b"\x99"}},
     "sread": {0: {0xBA47: 0x22}}},
    # Backup consecutive wins nonzero and distinct in both bytes, with the live
    # sPresentConsecutiveWins pre-loaded with different values: both bytes must be
    # copied from the backup, low byte then high byte, and the backup left alone.
    {"sram": {0: {0xBA47: b"\xDE\xAD",
                  0xBA49: b"\x34\x12",
                  0xBA4B: b"\xFF\xFF\xFF\xFF\xFF",
                  0xBA50: b"\x01\x01\x01\x01\x01",
                  0xBA55: b"\x05",
                  0xBA68: b"\x01"}},
     "sread": {0: {0xBA47: 0x22}}},
    # Warm RNG: a prelude call to UpdateRNGSources moves the RNG state off its
    # reset value, so the picked opponent sequence differs from the cases above.
    {"setup": [{"fn": "UpdateRNGSources"}],
     "sram": {0: {0xBA47: b"\x00" * 0x22}},
     "sread": {0: {0xBA47: 0x22}}},
    # ramg False after seeding: only the routine's own EnableSRAM makes any of
    # the writes land, and only it makes the backup bytes readable.
    {"ramg": False,
     "sram": {0: {0xBA47: b"\x00\x00\x21\x43",
                  0xBA4B: b"\x00" * 0x1E}},
     "sread": {0: {0xBA47: 0x22}}},
]
# <<< factory ChallengeMachine_PickOpponentSequence

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "ChallengeMachine_CheckIfOpponentAlreadySelected": {
        "source_symbol": "ChallengeMachine_CheckIfOpponentAlreadySelected",
        "before": "if (a == gb_read8(hl))",
        "after": "if (a != gb_read8(hl))",
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
# >>> factory-mutation ChallengeMachine_PickOpponentSequence
MUTATIONS["ChallengeMachine_PickOpponentSequence"] = {
    "source_symbol": "ChallengeMachine_PickOpponentSequence",
    "before": "\tfor (uint8_t i = 0; i < NUM_CHALLENGE_MACHINE_OPPONENTS; i++)",
    "after": "\tfor (uint8_t i = 0; i < NUM_CHALLENGE_MACHINE_OPPONENTS - 1u; i++)",
    "case_ids": ["ChallengeMachine_PickOpponentSequence-2", "ChallengeMachine_PickOpponentSequence-3"],
}
# <<< factory-mutation ChallengeMachine_PickOpponentSequence
