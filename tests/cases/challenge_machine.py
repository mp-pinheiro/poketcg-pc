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

# >>> factory ChallengeMachine_GetCurrentOpponent
CONTRACT["ChallengeMachine_GetCurrentOpponent"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["ChallengeMachine_GetCurrentOpponent"] = [
    # All-zero: index 0 selects the first opponent byte.
    {"sram": {0: {0xBA4B: bytes(range(1, 11)), 0xBA55: b"\x00"}},
     "read": {0xD692: 1}},
    # Poisoned entry registers: the routine takes no arguments, b/c must survive
    # and d/e/hl are recomputed from SRAM regardless of what came in.
    dict(POISON,
         sram={0: {0xBA4B: bytes(range(1, 11)), 0xBA55: b"\x03"}},
         read={0xD692: 1}),
    # Last in-table index (opponent slot 9).
    {"sram": {0: {0xBA4B: bytes(range(0x90, 0x9A)), 0xBA55: b"\x09"}},
     "read": {0xD692: 1}},
    # Index 10 aliases sChallengeMachineOpponentNumber itself: the byte read back
    # is the index, proving no bounds check exists.
    {"sram": {0: {0xBA4B: b"\x00" * 10, 0xBA55: b"\x0A"}},
     "read": {0xD692: 1}},
    # Large index: hl = base + 0xFF with no wrap inside the page.
    {"sram": {0: {0xBA4B: b"\x11" * 10, 0xBA55: b"\xFF", 0xBB4A: b"\x77"}},
     "read": {0xD692: 1}},
    # ramg False after seeding: the routine's own EnableSRAM is load-bearing,
    # otherwise index and opponent both read as open-bus $FF.
    {"ramg": False,
     "sram": {0: {0xBA4B: bytes(range(1, 11)), 0xBA55: b"\x02"}},
     "read": {0xD692: 1}},
]
# <<< factory ChallengeMachine_GetCurrentOpponent

# >>> factory ChallengeMachine_IncrementHLMax999
CONTRACT["ChallengeMachine_IncrementHLMax999"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["ChallengeMachine_IncrementHLMax999"] = [
    # All-zero registers: hl = 0 points at ROM, so the writes are dropped and the
    # only observable output is the advanced hl.
    {},
    # Counter at 0 in SRAM: 0 -> 1, hl advances.
    {"hl": 0xBA47, "sram": {0: {0xBA47: b"\x00\x00"}}, "sread": {0: {0xBA47: 2}}},
    # Poisoned entry: b/c/d/e must survive; 998 -> 999.
    dict(POISON, hl=0xBA47, sram={0: {0xBA47: b"\xE6\x03"}}, sread={0: {0xBA47: 2}}),
    # Exactly 999: capped, no write at all, hl left on the low byte.
    {"hl": 0xBA47, "sram": {0: {0xBA47: b"\xE7\x03"}}, "sread": {0: {0xBA47: 2}}},
    # High byte 3 but low byte not $E7: increments (1000 -> 1001), proving the
    # cap tests both bytes.
    {"hl": 0xBA47, "sram": {0: {0xBA47: b"\xE8\x03"}}, "sread": {0: {0xBA47: 2}}},
    # Low byte $E7 but high byte not 3: increments ($02E7 -> $02E8).
    {"hl": 0xBA47, "sram": {0: {0xBA47: b"\xE7\x02"}}, "sread": {0: {0xBA47: 2}}},
    # Carry out of the low byte: $03FF -> $0400.
    {"hl": 0xBA47, "sram": {0: {0xBA47: b"\xFF\x03"}}, "sread": {0: {0xBA47: 2}}},
    # Full 16-bit wrap: $FFFF -> $0000.
    {"hl": 0xBA47, "sram": {0: {0xBA47: b"\xFF\xFF"}}, "sread": {0: {0xBA47: 2}}},
    # WRAM target: no SRAM involved, plain increment of $00FF -> $0100.
    {"hl": 0xC100, "wram": {0xC100: b"\xFF\x00"}},
    # ramg False after seeding: without the routine's own EnableSRAM the read
    # would be open bus and the write would be dropped.
    {"ramg": False, "hl": 0xBA47, "sram": {0: {0xBA47: b"\xE7\x03"}}, "sread": {0: {0xBA47: 2}}},
]
# <<< factory ChallengeMachine_IncrementHLMax999

# >>> factory ChallengeMachine_CheckForNewRecord
CONTRACT["ChallengeMachine_CheckForNewRecord"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()}
CASES["ChallengeMachine_CheckForNewRecord"] = [
    # All-zero: present == max == 0, equal on both bytes -> no record.
    {"sram": {0: {0xBA47: b"\x00\x00", 0xBA56: b"\x00\x00", 0xBA58: b"\x00" * 16,
                  0xBA68: b"\x00", 0xA010: b"\x00" * 16}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
    # Poisoned entry with a genuine new record (present 5 > max 3, equal high
    # bytes): bc/de/hl are all overwritten by the copy setup.
    dict(POISON,
         sram={0: {0xBA47: b"\x05\x00", 0xBA56: b"\x03\x00",
                   0xBA58: b"\xFF" * 16, 0xBA68: b"\x00",
                   0xA010: bytes(range(0x41, 0x51))}},
         sread={0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}),
    # Present low byte less than max, high bytes equal: no record, hl ends on
    # sMaximumConsecutiveWins after the `dec hl`.
    {"sram": {0: {0xBA47: b"\x02\x00", 0xBA56: b"\x09\x00",
                  0xBA58: b"\xAA" * 16, 0xBA68: b"\x00", 0xA010: b"\xBB" * 16}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
    # High bytes differ with present greater: record taken without ever reading
    # the low bytes for the comparison, and hl stays at sMaximumConsecutiveWins+1
    # on the compare path. Present low byte is smaller than max's on purpose.
    {"sram": {0: {0xBA47: b"\x00\x02", 0xBA56: b"\xFF\x01",
                  0xBA58: b"\x00" * 16, 0xBA68: b"\x00", 0xA010: b"\x5A" * 16}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
    # High bytes differ with present smaller: no record, hl left at +1.
    {"sram": {0: {0xBA47: b"\xFF\x01", 0xBA56: b"\x00\x02",
                  0xBA58: b"\x33" * 16, 0xBA68: b"\x00", 0xA010: b"\x44" * 16}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
    # Exact equality on both bytes at a nonzero value: the `jr z` guard means
    # equal is NOT a new record.
    {"sram": {0: {0xBA47: b"\xE7\x03", 0xBA56: b"\xE7\x03",
                  0xBA58: b"\x77" * 16, 0xBA68: b"\x00", 0xA010: b"\x88" * 16}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
    # Off-by-one above equality: present is max+1, the smallest new record.
    {"sram": {0: {0xBA47: b"\xE8\x03", 0xBA56: b"\xE7\x03",
                  0xBA58: b"\x00" * 16, 0xBA68: b"\x00", 0xA010: bytes(range(16))}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
    # ramg False after seeding: without the routine's own EnableSRAM neither the
    # comparison nor any of the three writes would behave.
    {"ramg": False,
     "sram": {0: {0xBA47: b"\x05\x00", 0xBA56: b"\x03\x00",
                  0xBA58: b"\x00" * 16, 0xBA68: b"\x00", 0xA010: b"\x63" * 16}},
     "sread": {0: {0xBA56: 2, 0xBA58: 16, 0xBA68: 1}}},
]
# <<< factory ChallengeMachine_CheckForNewRecord

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
sChallengeMachineDuelResults = 0xBA50
sChallengeMachineOpponentNumber = 0xBA55
sPresentConsecutiveWins = 0xBA47
wDuelResult = 0xD0C3
# <<< factory-cases-statics

# >>> factory ChallengeMachine_RecordDuelResult
CONTRACT["ChallengeMachine_RecordDuelResult"] = {"compare": (), "preserve": ()}
CASES["ChallengeMachine_RecordDuelResult"] = [
    {"sram": {0: {sChallengeMachineDuelResults: b"\x00\x00\x00\x00\x00", sChallengeMachineOpponentNumber: b"\x00", sPresentConsecutiveWins: b"\x00\x00"}}, "wram": {wDuelResult: b"\x00"}, "sread": {0: {sChallengeMachineDuelResults: 5, sPresentConsecutiveWins: 2}}},
    {"sram": {0: {sChallengeMachineDuelResults: b"\x00\x00\x00\x00\x00", sChallengeMachineOpponentNumber: b"\x03", sPresentConsecutiveWins: b"\x07\x00"}}, "wram": {wDuelResult: b"\x01"}, "sread": {0: {sChallengeMachineDuelResults: 5, sPresentConsecutiveWins: 2}}},
    dict(POISON, sram={0: {sChallengeMachineDuelResults: b"\x11\x22\x33\x44\x55", sChallengeMachineOpponentNumber: b"\x02", sPresentConsecutiveWins: b"\xE6\x03"}}, wram={wDuelResult: b"\x00"}, sread={0: {sChallengeMachineDuelResults: 5, sPresentConsecutiveWins: 2}}),
    {"ramg": False, "sram": {0: {sChallengeMachineDuelResults: b"\x00\x00\x00\x00\x00", sChallengeMachineOpponentNumber: b"\x01", sPresentConsecutiveWins: b"\x00\x00"}}, "wram": {wDuelResult: b"\x01"}, "sread": {0: {sChallengeMachineDuelResults: 5, sPresentConsecutiveWins: 2}}},
]
# <<< factory ChallengeMachine_RecordDuelResult

# >>> factory ChallengeMachine_Initialize
CONTRACT["ChallengeMachine_Initialize"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ChallengeMachine_Initialize"] = [
    {"sram": {0: {0xBA42: b"\xE3\x95" + b"\xAA" * 0x25}},
     "sread": {0: {0xBA42: 0x27}},
     "expect_regs": {"a": 0xAA, "f": 0xC0}},
    dict(POISON,
         sram={0: {0xBA42: b"\x00" * 0x27}},
         sread={0: {0xBA42: 0x27}},
         expect_sram={0: {0xBA42: b"\xE3\x95" + b"\x00" * 0x14 + b"\x01\x00" + b"Dr. Mason" + b"\x00" * 7 + b"\x00"}},
         expect_regs={"a": 0x00, "f": 0x80}),
    {"sram": {0: {0xBA42: b"\xE3\x94" + b"\x55" * 0x25}},
     "sread": {0: {0xBA42: 0x27}},
     "expect_regs": {"a": 0x00, "f": 0x80},
     "expect_sram": {0: {0xBA42: b"\xE3\x95" + b"\x00" * 0x14 + b"\x01\x00" + b"Dr. Mason" + b"\x00" * 7 + b"\x00"}}},
]
# <<< factory ChallengeMachine_Initialize

# >>> factory ChallengeMachine_Reset
CONTRACT["ChallengeMachine_Reset"] = {"compare": (), "preserve": (), "sram_out": True}
CASES["ChallengeMachine_Reset"] = [
    {"sram": {0: {0xBA42: b"\xE3\x95" + b"\xAA" * 0x25}},
     "sread": {0: {0xBA42: 0x27}},
     "expect_sram": {0: {0xBA44: b"\x00\x00\x00\x00\x00\x00\x00"}}},
    dict(POISON,
         sram={0: {0xBA42: b"\x00" * 0x27}},
         sread={0: {0xBA42: 0x27}},
         expect_sram={0: {0xBA44: b"\x00\x00\x00\x00\x00\x00\x00"}}),
    {"sram": {0: {0xBA42: b"\xE3\x94" + b"\x55" * 0x25}},
     "sread": {0: {0xBA42: 0x27}},
     "expect_sram": {0: {0xBA44: b"\x00\x00\x00\x00\x00\x00\x00"}}},
]
# <<< factory ChallengeMachine_Reset

# >>> factory ChallengeMachine_PrintFinalConsecutiveWinStreak
CONTRACT["ChallengeMachine_PrintFinalConsecutiveWinStreak"] = {"compare": ("f",), "preserve": (), "wram_out": True}
CASES["ChallengeMachine_PrintFinalConsecutiveWinStreak"] = [
    {"hl": 0x5678, "sram": {0: {0xBA47: b"\x00\x00"}}, "read": {0xCE43: 2}},
    dict(POISON, sram={0: {0xBA47: b"\x00\x00"}}, read={0xCE43: 2}),
    {"hl": 0x1111, "keys": 0x01, "sram": {0: {0xBA47: b"\x05\x01"}},
     "wram": {0xC590: b"\x00", 0xCE4B: b"\xff", 0xCD0F: b"\x05", 0xCD10: b"\x04", 0xCD16: b"\x22"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCE43: 2}},
    {"hl": 0x2222, "keys": 0x01, "sram": {0: {0xBA47: b"\x02\x00"}},
     "wram": {0xC590: b"\x00", 0xCE4B: b"\xff", 0xCD0F: b"\x05", 0xCD10: b"\x04", 0xCD16: b"\x22"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCE43: 2}},
    {"hl": 0x3333, "keys": 0x01, "sram": {0: {0xBA47: b"\x01\x00"}},
     "wram": {0xC590: b"\x00", 0xCE4B: b"\xff", 0xCD0F: b"\x05", 0xCD10: b"\x04", 0xCD16: b"\x22"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCE43: 2}},
]
# <<< factory ChallengeMachine_PrintFinalConsecutiveWinStreak

# >>> factory ChallengeMachine_ShowNewRecord
CONTRACT["ChallengeMachine_ShowNewRecord"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["ChallengeMachine_ShowNewRecord"] = [
    {"hl": 0x5678, "sram": {0: {0xBA68: b"\x00"}}},
    dict(POISON, sram={0: {0xBA68: b"\x00"}}),
]
# <<< factory ChallengeMachine_ShowNewRecord

# >>> factory ChallengeMachine_DuelWon
CONTRACT["ChallengeMachine_DuelWon"] = {"compare": ("f",), "preserve": (), "wram_out": True}
CASES["ChallengeMachine_DuelWon"] = [
    {"keys": 0x01, "sram": {0: {0xBA55: b"\x00"}},
     "wram": {0xC590: b"\x00", 0xCE4B: b"\xff", 0xCD0F: b"\x05", 0xCD10: b"\x04", 0xCD16: b"\x22"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCE43: 2}},
    dict(POISON, keys=0x01, sram={0: {0xBA55: b"\x00"}},
         wram={0xC590: b"\x00", 0xCE4B: b"\xff", 0xCD0F: b"\x05", 0xCD10: b"\x04", 0xCD16: b"\x22"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xCE43: 2}),
    {"keys": 0x01, "sram": {0: {0xBA55: b"\x02"}},
     "wram": {0xC590: b"\x00", 0xCE4B: b"\xff", 0xCD0F: b"\x05", 0xCD10: b"\x04", 0xCD16: b"\x22"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCE43: 2}},
]
# <<< factory ChallengeMachine_DuelWon

# >>> factory ChallengeMachine_GetOpponentNameAndDeck
CONTRACT["ChallengeMachine_GetOpponentNameAndDeck"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["ChallengeMachine_GetOpponentNameAndDeck"] = [
    {"wram": {0xD692: b"\x00"}},
    {"wram": {0xD692: b"\x05"}},
    dict(POISON, wram={0xD692: b"\x00"}),
]
# <<< factory ChallengeMachine_GetOpponentNameAndDeck

# >>> factory ChallengeMachine_PrintScores
CONTRACT["ChallengeMachine_PrintScores"] = {"compare": (), "preserve": ()}
CASES["ChallengeMachine_PrintScores"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x00\x00"}},
    {"hl": 0xC500, "wram": {0xC500: b"\x00\xA2\x00\x00\x00\x00"},
     "sram": {0: {0xA200: b"\x34\x12"}}, "read": {0xD4B4: 3},
     "vread": {0: {0x9800: 3}}},
    dict(POISON, hl=0xC500, wram={0xC500: b"\x00\x00"}),
]
# <<< factory ChallengeMachine_PrintScores

# >>> factory ChallengeMachine_PrintOpponentName
CONTRACT["ChallengeMachine_PrintOpponentName"] = {"compare": ("d", "e", "hl"), "preserve": ()}
CASES["ChallengeMachine_PrintOpponentName"] = [
    {"wram": {0xD692: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "rom_bank": 4},
    dict(POISON, wram={0xD692: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], rom_bank=4),
]
# <<< factory ChallengeMachine_PrintOpponentName

# >>> factory ChallengeMachine_PrintOpponentClubStatus
CONTRACT["ChallengeMachine_PrintOpponentClubStatus"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c")}
CASES["ChallengeMachine_PrintOpponentClubStatus"] = [
    {"wram": {0xD692: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "rom_bank": 4},
    dict(POISON, wram={0xD692: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], rom_bank=4),
]
# <<< factory ChallengeMachine_PrintOpponentClubStatus

# >>> factory ChallengeMachine_PrepareDuel
CONTRACT["ChallengeMachine_PrepareDuel"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ChallengeMachine_PrepareDuel"] = [
    {"sram": {0: {0xBA55: b"\x02"}}, "rom_bank": 4, "read": {0xCC18: 1}},
    dict(POISON, sram={0: {0xBA55: b"\x02"}}, rom_bank=4, read={0xCC18: 1}),
]
# <<< factory ChallengeMachine_PrepareDuel

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
# >>> factory-mutation ChallengeMachine_GetCurrentOpponent
MUTATIONS["ChallengeMachine_GetCurrentOpponent"] = {
    "source_symbol": "ChallengeMachine_GetCurrentOpponent",
    "before": "\tuint16_t hl = (uint16_t)(sChallengeMachineOpponents_ADDR + e);",
    "after": "\tuint16_t hl = (uint16_t)(sChallengeMachineOpponents_ADDR + e + 1u);",
    "case_ids": ["ChallengeMachine_GetCurrentOpponent-0", "ChallengeMachine_GetCurrentOpponent-1", "ChallengeMachine_GetCurrentOpponent-2"],
}
# <<< factory-mutation ChallengeMachine_GetCurrentOpponent
# >>> factory-mutation ChallengeMachine_IncrementHLMax999
MUTATIONS["ChallengeMachine_IncrementHLMax999"] = {
    "source_symbol": "ChallengeMachine_IncrementHLMax999",
    "before": "\tif (high == WIN_CAP_HIGH && gb_read8(hl) == WIN_CAP_LOW) {",
    "after": "\tif (high == WIN_CAP_HIGH || gb_read8(hl) == WIN_CAP_LOW) {",
    "case_ids": ["ChallengeMachine_IncrementHLMax999-4", "ChallengeMachine_IncrementHLMax999-5", "ChallengeMachine_IncrementHLMax999-6"],
}
# <<< factory-mutation ChallengeMachine_IncrementHLMax999
# >>> factory-mutation ChallengeMachine_CheckForNewRecord
MUTATIONS["ChallengeMachine_CheckForNewRecord"] = {
    "source_symbol": "ChallengeMachine_CheckForNewRecord",
    "before": "\t\tnew_record = present_low > max_low;",
    "after": "\t\tnew_record = present_low >= max_low;",
    "case_ids": ["ChallengeMachine_CheckForNewRecord-0", "ChallengeMachine_CheckForNewRecord-5"],
}
# <<< factory-mutation ChallengeMachine_CheckForNewRecord
# >>> factory-mutation ChallengeMachine_RecordDuelResult
MUTATIONS["ChallengeMachine_RecordDuelResult"] = {"source_symbol": "ChallengeMachine_RecordDuelResult", "before": "\tif (result == 0u) {", "after": "\tif (result != 0u) {", "case_ids": ["ChallengeMachine_RecordDuelResult-0", "ChallengeMachine_RecordDuelResult-1", "ChallengeMachine_RecordDuelResult-2", "ChallengeMachine_RecordDuelResult-3"]}
# <<< factory-mutation ChallengeMachine_RecordDuelResult
# >>> factory-mutation ChallengeMachine_Initialize
MUTATIONS["ChallengeMachine_Initialize"] = {"source_symbol": "ChallengeMachine_Initialize", "before": "\t\tgb_write8(sMaximumConsecutiveWins_ADDR, 1u);", "after": "\t\tgb_write8(sMaximumConsecutiveWins_ADDR, 2u);", "case_ids": ["ChallengeMachine_Initialize-1", "ChallengeMachine_Initialize-2"]}
# <<< factory-mutation ChallengeMachine_Initialize
# >>> factory-mutation ChallengeMachine_Reset
MUTATIONS["ChallengeMachine_Reset"] = {"source_symbol": "ChallengeMachine_Reset", "before": "\tgb_write8(sPlayerInChallengeMachine_ADDR, 0u);", "after": "\tgb_write8(sPlayerInChallengeMachine_ADDR, 1u);", "case_ids": ["ChallengeMachine_Reset-0", "ChallengeMachine_Reset-2"]}
# <<< factory-mutation ChallengeMachine_Reset
# >>> factory-mutation ChallengeMachine_PrintFinalConsecutiveWinStreak
MUTATIONS["ChallengeMachine_PrintFinalConsecutiveWinStreak"] = {"source_symbol": "ChallengeMachine_PrintFinalConsecutiveWinStreak", "before": "\tif (high == 0u && low < 2u) {", "after": "\tif (high == 0u && low < 1u) {", "case_ids": ["ChallengeMachine_PrintFinalConsecutiveWinStreak-4"]}
# <<< factory-mutation ChallengeMachine_PrintFinalConsecutiveWinStreak
# >>> factory-mutation ChallengeMachine_ShowNewRecord
MUTATIONS["ChallengeMachine_ShowNewRecord"] = {"source_symbol": "ChallengeMachine_ShowNewRecord", "before": "return (ChallengeMachineShowNewRecordResult){0u, 0x80u, hl};", "after": "return (ChallengeMachineShowNewRecordResult){0u, 0x90u, hl};", "case_ids": ["ChallengeMachine_ShowNewRecord-0", "ChallengeMachine_ShowNewRecord-1"]}
# <<< factory-mutation ChallengeMachine_ShowNewRecord
# >>> factory-mutation ChallengeMachine_DuelWon
MUTATIONS["ChallengeMachine_DuelWon"] = {"source_symbol": "ChallengeMachine_DuelWon", "before": "gb_write8(wTxRam3_ADDR, (uint8_t)(opponent_number + 1u));", "after": "gb_write8(wTxRam3_ADDR, (uint8_t)(opponent_number + 2u));", "case_ids": ["ChallengeMachine_DuelWon-0", "ChallengeMachine_DuelWon-2"]}
# <<< factory-mutation ChallengeMachine_DuelWon
# >>> factory-mutation ChallengeMachine_GetOpponentNameAndDeck
MUTATIONS["ChallengeMachine_GetOpponentNameAndDeck"] = {"source_symbol": "ChallengeMachine_GetOpponentNameAndDeck", "before": "gb_write8(wNPCDuelDeckID_ADDR, deck_id);", "after": "gb_write8(wNPCDuelDeckID_ADDR, (uint8_t)(deck_id + 1u));", "case_ids": ["ChallengeMachine_GetOpponentNameAndDeck-0", "ChallengeMachine_GetOpponentNameAndDeck-1"]}
# <<< factory-mutation ChallengeMachine_GetOpponentNameAndDeck
# >>> factory-mutation ChallengeMachine_PrintScores
MUTATIONS["ChallengeMachine_PrintScores"] = {"source_symbol": "ChallengeMachine_PrintScores", "before": "if (de == 0u)\n\t\t\tbreak;", "after": "if (de == 1u)\n\t\t\tbreak;", "case_ids": ["ChallengeMachine_PrintScores-1"]}
# <<< factory-mutation ChallengeMachine_PrintScores
# >>> factory-mutation ChallengeMachine_PrintOpponentName
MUTATIONS["ChallengeMachine_PrintOpponentName"] = {"source_symbol": "ChallengeMachine_PrintOpponentName", "before": "uint16_t hl2 = (uint16_t)(r1.hl + 2u);", "after": "uint16_t hl2 = (uint16_t)(r1.hl + 3u);", "case_ids": ["ChallengeMachine_PrintOpponentName-0"]}
# <<< factory-mutation ChallengeMachine_PrintOpponentName
# >>> factory-mutation ChallengeMachine_PrintOpponentClubStatus
MUTATIONS["ChallengeMachine_PrintOpponentClubStatus"] = {"source_symbol": "ChallengeMachine_PrintOpponentClubStatus", "before": "uint16_t elem_addr = (uint16_t)(entry_hl + 8u);", "after": "uint16_t elem_addr = (uint16_t)(entry_hl + 9u);", "case_ids": ["ChallengeMachine_PrintOpponentClubStatus-0"]}
# <<< factory-mutation ChallengeMachine_PrintOpponentClubStatus
# >>> factory-mutation ChallengeMachine_PrepareDuel
MUTATIONS["ChallengeMachine_PrepareDuel"] = {"source_symbol": "ChallengeMachine_PrepareDuel", "before": "uint16_t prize_addr = (uint16_t)(CHALLENGE_MACHINE_PRIZES_ADDR + opponent_num);", "after": "uint16_t prize_addr = (uint16_t)(CHALLENGE_MACHINE_PRIZES_ADDR + opponent_num + 1u);", "case_ids": ["ChallengeMachine_PrepareDuel-0", "ChallengeMachine_PrepareDuel-1"]}
# <<< factory-mutation ChallengeMachine_PrepareDuel
