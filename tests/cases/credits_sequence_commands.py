wSequenceCmdPtr = 0xD631
wSequenceDelay = 0xD633

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "SetCreditsSequenceCmdPtr": {"compare": ("b", "c", "d", "e", "hl"),
                                  "preserve": ("b", "c", "d", "e", "hl")},
    "ExecuteCreditsSequenceCmd": {"compare": ("b", "c", "d", "e", "hl"),
                                  "preserve": ("b", "c", "d", "e", "hl")},
    "AdvanceCreditsSequenceCmdPtr": {"compare": ("b", "c", "d", "e", "hl"),
                                     "preserve": ("b", "c", "d", "e", "hl")},
}
CASES = {
    "SetCreditsSequenceCmdPtr": [
        {"read": {wSequenceCmdPtr: 2, wSequenceDelay: 1}},
        dict(POISON, read={wSequenceCmdPtr: 2, wSequenceDelay: 1}),
    ],
    "ExecuteCreditsSequenceCmd": [
        {"wram": {wSequenceDelay: b"\xFF"}, "read": {wSequenceDelay: 1}},
        dict(POISON, wram={wSequenceDelay: b"\xFF"}, read={wSequenceDelay: 1}),
        {"wram": {wSequenceDelay: b"\x01"}, "read": {wSequenceDelay: 1}},
        {"wram": {wSequenceDelay: b"\x02"}, "read": {wSequenceDelay: 1}},
        {"wram": {wSequenceDelay: b"\x00", wSequenceCmdPtr: b"\x00\xC1"},
         "oracle": False,
         "why": "zero delay dispatches through CallHL2 into an unported credits command",
         "expect": {wSequenceDelay: b"\x00"}},
    ],
    "AdvanceCreditsSequenceCmdPtr": [
        {"a": 0, "wram": {wSequenceCmdPtr: b"\x00\x00"},
         "read": {wSequenceCmdPtr: 2}},
        dict(POISON, a=1, wram={wSequenceCmdPtr: b"\x00\x00"},
             read={wSequenceCmdPtr: 2}),
        {"a": 0xFF, "wram": {wSequenceCmdPtr: b"\xFF\xFF"},
         "read": {wSequenceCmdPtr: 2}},
        {"a": 0x00, "wram": {wSequenceCmdPtr: b"\xFE\x00"},
         "read": {wSequenceCmdPtr: 2}},
        {"a": 0xFF, "wram": {wSequenceCmdPtr: b"\x02\x01"},
         "read": {wSequenceCmdPtr: 2}},
    ],
}
# >>> factory AdvanceCreditsSequenceCmdPtrBy2
CONTRACT["AdvanceCreditsSequenceCmdPtrBy2"] = {"compare": ("b", "c", "d", "e", "hl"),
                     "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceCreditsSequenceCmdPtrBy2"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: bytes([254, 0x00])}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy2

# >>> factory AdvanceCreditsSequenceCmdPtrBy3
CONTRACT["AdvanceCreditsSequenceCmdPtrBy3"] = {"compare": ("b", "c", "d", "e", "hl"),
                     "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceCreditsSequenceCmdPtrBy3"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: bytes([253, 0x00])}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy3

# >>> factory AdvanceCreditsSequenceCmdPtrBy5
CONTRACT["AdvanceCreditsSequenceCmdPtrBy5"] = {"compare": ("b", "c", "d", "e", "hl"),
                     "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceCreditsSequenceCmdPtrBy5"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: bytes([251, 0x00])}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy5

# >>> factory AdvanceCreditsSequenceCmdPtrBy6
CONTRACT["AdvanceCreditsSequenceCmdPtrBy6"] = {
    "compare": ("b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["AdvanceCreditsSequenceCmdPtrBy6"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: b"\xFA\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xF9\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFC\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy6

# >>> factory AdvanceCreditsSequenceCmdPtrBy4
CONTRACT["AdvanceCreditsSequenceCmdPtrBy4"] = {
    "compare": ("b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["AdvanceCreditsSequenceCmdPtrBy4"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
    {"wram": {wSequenceCmdPtr: b"\xFC\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFB\x10"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\xFE\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceCreditsSequenceCmdPtrBy4

# >>> factory CreditsSequenceCmd_Wait
# wSequenceDelay = 0xD633 (given). SEQ_AREA is a diff-only watch window around the
# sequence-variable block: AdvanceCreditsSequenceCmdPtrBy3's pointer advance lands
# in WRAM near wSequenceDelay, so the window catches advance-corrupting mutations.
wSequenceDelay = 0xD633
SEQ_AREA = 0xD600
SEQ_AREA_LEN = 0x80
CONTRACT["CreditsSequenceCmd_Wait"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_Wait"] = [
	{"c": 0, "wram": {wSequenceDelay: b"\xff"}, "read": {SEQ_AREA: SEQ_AREA_LEN}},
	{"c": 1, "wram": {wSequenceDelay: b"\x00"}, "read": {SEQ_AREA: SEQ_AREA_LEN}},
	{"c": 0x80, "wram": {wSequenceDelay: b"\x01"}},
	dict(POISON, c=0x2A, wram={wSequenceDelay: b"\x7e"}, read={SEQ_AREA: SEQ_AREA_LEN}),
]
# <<< factory CreditsSequenceCmd_Wait


# >>> factory CreditsSequenceCmd_DisableLCD
# No register inputs are consumed and no register outputs survive the tail jump,
# so the cases watch the sequence-variable window the callee advances.
wSequenceDelay = 0xD633
SEQ_AREA = 0xD600
SEQ_AREA_LEN = 0x80
CONTRACT["CreditsSequenceCmd_DisableLCD"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_DisableLCD"] = [
	{"read": {SEQ_AREA: SEQ_AREA_LEN}},
	dict(POISON, read={SEQ_AREA: SEQ_AREA_LEN}),
]
# <<< factory CreditsSequenceCmd_DisableLCD


# >>> factory-cases-statics
wd647 = 0xD647
wd648 = 0xD648
wd649 = 0xD649
wd64a = 0xD64A
wSequenceDelay = 0xD633

BGP = 0xCABC
OBP0 = 0xCABD
OBP1 = 0xCABE
LCDC = 0xCABB
RLCDC = 0xFF40
VBLANK = 0xCAB8
BG_PALS = 0xCAF0
OBJ_PALS = 0xCB30
TEMP_BGP = 0xD294
TEMP_OBP0 = 0xD295
TEMP_OBP1 = 0xD296
TEMP_BG_PALS = 0xD297
TEMP_OBJ_PALS = 0xD2D7
SEQ_AREA = 0xD600
SEQ_AREA_LEN = 0x80
PALETTE_SEED = {
    BGP: b"\xE4", OBP0: b"\x1B", OBP1: b"\xB4",
    BG_PALS: bytes(range(64)), OBJ_PALS: bytes(range(64, 128)),
    TEMP_BGP: b"\x00", TEMP_OBP0: b"\x55", TEMP_OBP1: b"\xAA",
    TEMP_BG_PALS: bytes(reversed(range(64))), TEMP_OBJ_PALS: bytes(reversed(range(64, 128))),
}

wLineSeparation = 0xCD08
wSequenceCmdPtr = 0xD631

wd647 = 0xD647
wd648 = 0xD648
wd649 = 0xD649
wd64a = 0xD64A
wSequenceCmdPtr = 0xD631
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLineSeparation = 0xCD08
wSequenceCmdPtr = 0xD631
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1}
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}
BOX_READ = {0x9800: 0x400}

wSequenceCmdPtr = 0xD631
hSCX = 0xFF92
hSCY = 0xFF93
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory CreditsSequenceCmd_TransformOverlay
CONTRACT["CreditsSequenceCmd_TransformOverlay"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_TransformOverlay"] = [
    {"b": 2, "c": 2, "d": 2, "e": 2, "wram": {wd647: b"\x00", wd648: b"\x00", wd649: b"\x00", wd64a: b"\x00"}, "read": {wd647: 4, wSequenceDelay: 1}},
    dict(POISON, wram={wd647: b"\x10", wd648: b"\x10", wd649: b"\x10", wd64a: b"\x10"}, read={wd647: 4, wSequenceDelay: 1}),
]
# <<< factory CreditsSequenceCmd_TransformOverlay

# >>> factory CreditsSequenceCmd_FadeIn
CONTRACT["CreditsSequenceCmd_FadeIn"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_FadeIn"] = [
    {"wram": {LCDC: b"\x00", VBLANK: b"\xFE", **PALETTE_SEED},
     "instruction_budget": 1000000, "cycle_budget": 4000000,
     "read": {SEQ_AREA: SEQ_AREA_LEN, LCDC: 1, RLCDC: 1, VBLANK: 1,
              BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64,
              TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1,
              TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64}},
    dict(POISON, wram={LCDC: b"\x00", VBLANK: b"\xFE", **PALETTE_SEED},
         instruction_budget=1000000, cycle_budget=4000000,
         read={SEQ_AREA: SEQ_AREA_LEN, LCDC: 1, RLCDC: 1, VBLANK: 1,
               BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64,
               TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1,
               TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64}),
]
# <<< factory CreditsSequenceCmd_FadeIn

# >>> factory CreditsSequenceCmd_PrintTextBox
CONTRACT["CreditsSequenceCmd_PrintTextBox"] = {"compare": (), "preserve": ()};
CASES["CreditsSequenceCmd_PrintTextBox"] = [
    {"b": 0, "c": 0, "d": 0, "e": 0,
     "wram": {wLineSeparation: b"\x00", wSequenceCmdPtr: b"\x00\x00"},
     "read": {wLineSeparation: 1, wSequenceCmdPtr: 2}},
    dict(POISON, d=0, e=0,
         wram={wLineSeparation: b"\x00", wSequenceCmdPtr: b"\x00\x00"},
         read={wLineSeparation: 1, wSequenceCmdPtr: 2}),
]
# <<< factory CreditsSequenceCmd_PrintTextBox

# >>> factory CreditsSequenceCmd_InitOverlay
CONTRACT["CreditsSequenceCmd_InitOverlay"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_InitOverlay"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44,
     "wram": {wd647: b"\x00", wd648: b"\x00", wd649: b"\x00", wd64a: b"\x00", wSequenceCmdPtr: b"\x00\x00"},
     "read": {wd647: 1, wd648: 1, wd649: 1, wd64a: 1, wSequenceCmdPtr: 2}},
    dict(POISON,
         wram={wd647: b"\x10", wd648: b"\x20", wd649: b"\x30", wd64a: b"\x40", wSequenceCmdPtr: b"\x00\x00"},
         read={wd647: 1, wd648: 1, wd649: 1, wd64a: 1, wSequenceCmdPtr: 2}),
]
# <<< factory CreditsSequenceCmd_InitOverlay

# >>> factory CreditsSequenceCmd_InitVolcanoSprite
CONTRACT["CreditsSequenceCmd_InitVolcanoSprite"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_InitVolcanoSprite"] = [
    {"f": 0x00, "wram": {0xD631: b"\x00\x40"}, "expect": {0xD631: b"\x02\x40"}},
    dict(POISON, wram={0xD631: b"\xFE\xFF"}, expect={0xD631: b"\x00\x00"}),
]
# <<< factory CreditsSequenceCmd_InitVolcanoSprite

# >>> factory CreditsSequenceCmd_DrawRectangle
CONTRACT["CreditsSequenceCmd_DrawRectangle"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CreditsSequenceCmd_DrawRectangle"] = [
    {"b": 0x01, "c": 0x02, "wram": {0xD631: b"\x00\x00"}, "read": {0xD631: 2}},
    dict(POISON, b=0x01, c=0x02, wram={0xD631: b"\x00\x00"}, read={0xD631: 2}),
]
# <<< factory CreditsSequenceCmd_DrawRectangle

# >>> factory CreditsSequenceCmd_PrintText
CONTRACT["CreditsSequenceCmd_PrintText"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_PrintText"] = [
    {"b": 0, "c": 0, "d": 0, "e": 1,
     "wram": {wLineSeparation: b"\x00", wSequenceCmdPtr: b"\x00\x00"},
     "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ, wLineSeparation: 1, wSequenceCmdPtr: 2},
     "vread": VRAM_READ},
    {"b": 0, "c": 0, "d": 0, "e": 0,
     "wram": {wLineSeparation: b"\x00", wSequenceCmdPtr: b"\x00\x00"},
     "setup": SETUP, "vread": {0: BOX_READ}},
    dict(POISON,
         wram={wLineSeparation: b"\x00", wSequenceCmdPtr: b"\x00\x00"},
         setup=SETUP, vread={0: BOX_READ}),
]
# <<< factory CreditsSequenceCmd_PrintText

# >>> factory CreditsSequenceCmd_LoadBooster
CONTRACT["CreditsSequenceCmd_LoadBooster"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_LoadBooster"] = [
    {"b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00,
     "wram": {wSequenceCmdPtr: b"\x00\x00"},
     "read": {wSequenceCmdPtr: 2, hSCX: 1, hSCY: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, b=0x00, c=0x00, e=0x00,
         wram={wSequenceCmdPtr: b"\x00\x00"},
         read={wSequenceCmdPtr: 2, hSCX: 1, hSCY: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory CreditsSequenceCmd_LoadBooster

# >>> factory CreditsSequenceCmd_FadeOut
CONTRACT["CreditsSequenceCmd_FadeOut"] = {"compare": (), "preserve": ()}
CASES["CreditsSequenceCmd_FadeOut"] = [
    {"wram": {LCDC: b"\x80", RLCDC: b"\x00", VBLANK: b"\xfe", **PALETTE_SEED, wSequenceCmdPtr: b"\x00\x00"},
     "instruction_budget": 1000000, "cycle_budget": 4000000,
     "read": {SEQ_AREA: SEQ_AREA_LEN, LCDC: 1, RLCDC: 1, VBLANK: 1,
              BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64,
              TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1,
              TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64}},
    dict(POISON, wram={LCDC: b"\x80", RLCDC: b"\x00", VBLANK: b"\xfe", **PALETTE_SEED, wSequenceCmdPtr: b"\x00\x00"},
         instruction_budget=1000000, cycle_budget=4000000,
         read={SEQ_AREA: SEQ_AREA_LEN, LCDC: 1, RLCDC: 1, VBLANK: 1,
              BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 64, OBJ_PALS: 64,
              TEMP_BGP: 1, TEMP_OBP0: 1, TEMP_OBP1: 1,
              TEMP_BG_PALS: 64, TEMP_OBJ_PALS: 64}),
]
# <<< factory CreditsSequenceCmd_FadeOut

# >>> factory CreditsSequenceCmd_LoadScene
CONTRACT["CreditsSequenceCmd_LoadScene"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("d", "e")}
CASES["CreditsSequenceCmd_LoadScene"] = [
    {"e": 0x00, "wram": {wSequenceCmdPtr: b"\x00\x00", hSCX: b"\x7f", hSCY: b"\x7f"}, "read": {wSequenceCmdPtr: 2, hSCX: 1, hSCY: 1}, "instruction_budget": 4000000, "cycle_budget": 20000000},
    dict(POISON, e=0x00, wram={wSequenceCmdPtr: b"\x00\xc1", hSCX: b"\x7f", hSCY: b"\x7f"}, read={wSequenceCmdPtr: 2, hSCX: 1, hSCY: 1}, instruction_budget=4000000, cycle_budget=20000000),
]
# <<< factory CreditsSequenceCmd_LoadScene

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {
    "SetCreditsSequenceCmdPtr": {
        "source_symbol": "SetCreditsSequenceCmdPtr",
        "before": "gb_write8(wSequenceDelay_ADDR, 0);",
        "after": "gb_write8(wSequenceDelay_ADDR, 1);",
        "case_ids": ["SetCreditsSequenceCmdPtr-0", "SetCreditsSequenceCmdPtr-1"],
    },
    "ExecuteCreditsSequenceCmd": {
        "source_symbol": "ExecuteCreditsSequenceCmd",
        "before": "gb_write8(wSequenceDelay_ADDR, (uint8_t)(delay - 1u));",
        "after": "gb_write8(wSequenceDelay_ADDR, (uint8_t)(delay - 2u));",
        "case_ids": ["ExecuteCreditsSequenceCmd-2", "ExecuteCreditsSequenceCmd-3"],
    },
    "AdvanceCreditsSequenceCmdPtr": {
        "source_symbol": "AdvanceCreditsSequenceCmdPtr",
        "before": "ptr = (uint16_t)(ptr + a);",
        "after": "ptr = (uint16_t)(ptr + (uint8_t)(a << 1));",
        "case_ids": ["AdvanceCreditsSequenceCmdPtr-1", "AdvanceCreditsSequenceCmdPtr-2",
                     "AdvanceCreditsSequenceCmdPtr-4"],
    },
}
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy2
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy2"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy2",
    "before": "AdvanceCreditsSequenceCmdPtr(2u);",
    "after": "AdvanceCreditsSequenceCmdPtr(3u);",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy2-0", "AdvanceCreditsSequenceCmdPtrBy2-2"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy2
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy3
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy3"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy3",
    "before": "AdvanceCreditsSequenceCmdPtr(3u);",
    "after": "AdvanceCreditsSequenceCmdPtr(4u);",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy3-0", "AdvanceCreditsSequenceCmdPtrBy3-2"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy3
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy5
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy5"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy5",
    "before": "AdvanceCreditsSequenceCmdPtr(5u);",
    "after": "AdvanceCreditsSequenceCmdPtr(6u);",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy5-0", "AdvanceCreditsSequenceCmdPtrBy5-2"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy5
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy6
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy6"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy6",
    "before": "void AdvanceCreditsSequenceCmdPtrBy6(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(6u);\n}",
    "after": "void AdvanceCreditsSequenceCmdPtrBy6(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(7u);\n}",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy6-0", "AdvanceCreditsSequenceCmdPtrBy6-2",
                 "AdvanceCreditsSequenceCmdPtrBy6-3", "AdvanceCreditsSequenceCmdPtrBy6-4"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy6
# >>> factory-mutation AdvanceCreditsSequenceCmdPtrBy4
MUTATIONS["AdvanceCreditsSequenceCmdPtrBy4"] = {
    "source_symbol": "AdvanceCreditsSequenceCmdPtrBy4",
    "before": "void AdvanceCreditsSequenceCmdPtrBy4(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(4u);\n}",
    "after": "void AdvanceCreditsSequenceCmdPtrBy4(void)\n{\n\tAdvanceCreditsSequenceCmdPtr(5u);\n}",
    "case_ids": ["AdvanceCreditsSequenceCmdPtrBy4-0", "AdvanceCreditsSequenceCmdPtrBy4-2",
                 "AdvanceCreditsSequenceCmdPtrBy4-3", "AdvanceCreditsSequenceCmdPtrBy4-4"],
}
# <<< factory-mutation AdvanceCreditsSequenceCmdPtrBy4
# >>> factory-mutation CreditsSequenceCmd_Wait
MUTATIONS["CreditsSequenceCmd_Wait"] = {
	"source_symbol": "CreditsSequenceCmd_Wait",
	"before": "\twSequenceDelay = c;",
	"after": "\twSequenceDelay = 0x00u;",
	"case_ids": ["CreditsSequenceCmd_Wait-1", "CreditsSequenceCmd_Wait-2", "CreditsSequenceCmd_Wait-3"],
}
# <<< factory-mutation CreditsSequenceCmd_Wait
# >>> factory-mutation CreditsSequenceCmd_DisableLCD
MUTATIONS["CreditsSequenceCmd_DisableLCD"] = {
	"source_symbol": "CreditsSequenceCmd_DisableLCD",
	"before": "\tDisableLCD();\n\tAdvanceCreditsSequenceCmdPtrBy2();",
	"after": "\tDisableLCD();\n\tAdvanceCreditsSequenceCmdPtrBy3();",
	"case_ids": ["CreditsSequenceCmd_DisableLCD-0", "CreditsSequenceCmd_DisableLCD-1"],
}
# <<< factory-mutation CreditsSequenceCmd_DisableLCD
# >>> factory-mutation CreditsSequenceCmd_TransformOverlay
MUTATIONS["CreditsSequenceCmd_TransformOverlay"] = {"source_symbol": "CreditsSequenceCmd_TransformOverlay", "before": "wSequenceDelay = 1;", "after": "wSequenceDelay = 2;", "case_ids": ["CreditsSequenceCmd_TransformOverlay-0"]}
# <<< factory-mutation CreditsSequenceCmd_TransformOverlay
# >>> factory-mutation CreditsSequenceCmd_FadeIn
MUTATIONS["CreditsSequenceCmd_FadeIn"] = {
    "source_symbol": "CreditsSequenceCmd_FadeIn",
    "before": "\tDisableLCD();\n\tSetWindowOn();\n\tFadeScreenFromWhite();\n\tAdvanceCreditsSequenceCmdPtrBy2();",
    "after": "\tDisableLCD();\n\tSetWindowOn();\n\tFadeScreenFromWhite();\n\tAdvanceCreditsSequenceCmdPtrBy3();",
    "case_ids": ["CreditsSequenceCmd_FadeIn-0", "CreditsSequenceCmd_FadeIn-1"],
}
# <<< factory-mutation CreditsSequenceCmd_FadeIn
# >>> factory-mutation CreditsSequenceCmd_PrintTextBox
MUTATIONS["CreditsSequenceCmd_PrintTextBox"] = {
    "source_symbol": "CreditsSequenceCmd_PrintTextBox",
    "before": "\u0009wLineSeparation = SINGLE_SPACED;",
    "after": "\u0009wLineSeparation = 0u;",
    "case_ids": ["CreditsSequenceCmd_PrintTextBox-0", "CreditsSequenceCmd_PrintTextBox-1"],
}
# <<< factory-mutation CreditsSequenceCmd_PrintTextBox
# >>> factory-mutation CreditsSequenceCmd_InitOverlay
MUTATIONS["CreditsSequenceCmd_InitOverlay"] = {
    "source_symbol": "CreditsSequenceCmd_InitOverlay",
    "before": "\twd647 = c;",
    "after": "\twd647 = (uint8_t)(c + 1u);",
    "case_ids": ["CreditsSequenceCmd_InitOverlay-0", "CreditsSequenceCmd_InitOverlay-1"],
}
# <<< factory-mutation CreditsSequenceCmd_InitOverlay
# >>> factory-mutation CreditsSequenceCmd_InitVolcanoSprite
MUTATIONS["CreditsSequenceCmd_InitVolcanoSprite"] = {"source_symbol": "CreditsSequenceCmd_InitVolcanoSprite", "before": "\tOverworldMap_InitVolcanoSprite(f);\n\tAdvanceCreditsSequenceCmdPtrBy2();", "after": "\tOverworldMap_InitVolcanoSprite(f);", "case_ids": ["CreditsSequenceCmd_InitVolcanoSprite-0", "CreditsSequenceCmd_InitVolcanoSprite-1"]}
# <<< factory-mutation CreditsSequenceCmd_InitVolcanoSprite
# >>> factory-mutation CreditsSequenceCmd_DrawRectangle
MUTATIONS["CreditsSequenceCmd_DrawRectangle"] = {"source_symbol": "CreditsSequenceCmd_DrawRectangle", "before": "\tAdvanceCreditsSequenceCmdPtrBy4();", "after": "\t(void)0;", "case_ids": ["CreditsSequenceCmd_DrawRectangle-0", "CreditsSequenceCmd_DrawRectangle-1"]}
# <<< factory-mutation CreditsSequenceCmd_DrawRectangle
# >>> factory-mutation CreditsSequenceCmd_PrintText
MUTATIONS["CreditsSequenceCmd_PrintText"] = {"source_symbol": "CreditsSequenceCmd_PrintText", "before": "uint8_t e = (uint8_t)(b | 0x20u);", "after": "uint8_t e = b;", "case_ids": ["CreditsSequenceCmd_PrintText-0", "CreditsSequenceCmd_PrintText-1"]}
# <<< factory-mutation CreditsSequenceCmd_PrintText
# >>> factory-mutation CreditsSequenceCmd_LoadBooster
MUTATIONS["CreditsSequenceCmd_LoadBooster"] = {
    "source_symbol": "CreditsSequenceCmd_LoadBooster",
    "before": "\tAdvanceCreditsSequenceCmdPtrBy5();",
    "after": "\tAdvanceCreditsSequenceCmdPtrBy4();",
    "case_ids": ["CreditsSequenceCmd_LoadBooster-0", "CreditsSequenceCmd_LoadBooster-1"],
}
# <<< factory-mutation CreditsSequenceCmd_LoadBooster
# >>> factory-mutation CreditsSequenceCmd_FadeOut
MUTATIONS["CreditsSequenceCmd_FadeOut"] = {"source_symbol": "CreditsSequenceCmd_FadeOut", "before": "\tSetWindowOff();", "after": "\tSetWindowOn();", "case_ids": ["CreditsSequenceCmd_FadeOut-0", "CreditsSequenceCmd_FadeOut-1"]}
# <<< factory-mutation CreditsSequenceCmd_FadeOut
# >>> factory-mutation CreditsSequenceCmd_LoadScene
MUTATIONS["CreditsSequenceCmd_LoadScene"] = {
    "source_symbol": "CreditsSequenceCmd_LoadScene",
    "before": "\tuint8_t high = (uint8_t)high_sum;",
    "after": "\tuint8_t high = (uint8_t)(high_sum + 1u);",
    "case_ids": ["CreditsSequenceCmd_LoadScene-0", "CreditsSequenceCmd_LoadScene-1"],
}
# <<< factory-mutation CreditsSequenceCmd_LoadScene
