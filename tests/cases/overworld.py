"""Oracle-diff cases for poketcg/src/engine/overworld/overworld.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Func_c6cc
wPlayerXCoordPixels = 0xD332
wPlayerYCoordPixels = 0xD333
wPlayerSpriteIndex = 0xD336
wWhichSprite = 0xD4CF
wSpriteAnimScratch = 0xD4D0
CONTRACT["Func_c6cc"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c6cc"] = [
	{"a": 0, "wram": {wPlayerXCoordPixels: b"\x00"}},
	{"a": 1, "wram": {wPlayerXCoordPixels: b"\x02"}},
	{"a": 0x08, "wram": {wPlayerXCoordPixels: b"\x08"}},
	{"a": 0x80, "wram": {wPlayerXCoordPixels: b"\x80"}},
	{"a": 0x0F, "wram": {wPlayerXCoordPixels: b"\x01"}},
	dict(POISON, a=0x11, wram={wPlayerXCoordPixels: b"\xee"}),
]
# <<< factory Func_c6cc

# >>> factory Func_c6d4
CONTRACT["Func_c6d4"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c6d4"] = [
	{"a": 0, "wram": {wPlayerYCoordPixels: b"\x00"}},
	{"a": 1, "wram": {wPlayerYCoordPixels: b"\x02"}},
	{"a": 0x70, "wram": {wPlayerYCoordPixels: b"\x90"}},
	{"a": 0x0F, "wram": {wPlayerYCoordPixels: b"\x0F"}},
	{"a": 0xFF, "wram": {wPlayerYCoordPixels: b"\x01"}},
	dict(POISON, a=0x40, wram={wPlayerYCoordPixels: b"\x40"}),
]
# <<< factory Func_c6d4

# >>> factory Func_c6f7
CONTRACT["Func_c6f7"] = {"compare": ("a", "hl", "b", "d", "e"), "preserve": ("b", "d", "e")}
CASES["Func_c6f7"] = [
	{"wram": {wPlayerSpriteIndex: b"\x00"}},
	{"wram": {wPlayerSpriteIndex: b"\x01", wWhichSprite: b"\x00", wSpriteAnimScratch: b"\x00" * 0x80}},
	{"wram": {wPlayerSpriteIndex: b"\x02", wWhichSprite: b"\x00", wSpriteAnimScratch: b"\xff" * 0x80}},
	dict(POISON, wram={wPlayerSpriteIndex: b"\x03", wWhichSprite: b"\xaa", wSpriteAnimScratch: b"\x55" * 0x80}),
]
# <<< factory Func_c6f7

# >>> factory SetOverworldNPCFlags
CONTRACT["SetOverworldNPCFlags"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetOverworldNPCFlags"] = [
    {"wram": {0xD0C1: b"\x00"}},
    dict(POISON, a=0x0F, wram={0xD0C1: b"\xF0"}),
    {"a": 0x00, "wram": {0xD0C1: b"\x80"}},
]
# <<< factory SetOverworldNPCFlags

# >>> factory Func_c158
CONTRACT["Func_c158"] = {"compare": ("a",), "preserve": ()}
CASES["Func_c158"] = [
	{},  # all-zero: wActiveGameEvent=0 -> cp/r nz early return
	{"wram": {0xD0C2: b"\x01", 0xD3AB: b"\x00", 0xD0C4: b"\x42", 0xD0C5: b"\x0c", 0xD3AA: b"\x01"},
	 "read": {0xD0C2: 1, 0xD0C4: 1}},  # duel event: wTempNPC <- wNPCDuelist before FindLoadedNPC
	{"wram": {0xD0C2: b"\x02", 0xD3AB: b"\x77"}, "read": {0xD0C2: 1}},  # not duel -> early return, wTempNPC untouched
	dict(POISON, wram={0xD0C2: b"\x01", 0xD3AB: b"\x33", 0xD0C4: b"\x21", 0xD0C5: b"\x06"},
	     read={0xD0C2: 1, 0xD0C4: 1}),
]
# <<< factory Func_c158

# >>> factory Func_c184
CONTRACT["Func_c184"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c184"] = [
	{},  # all-zero: wCurMap=0 -> OWMODE_MAP written to both mode bytes
	{"wram": {0xD0BF: b"\x5a", 0xD0C0: b"\xa5"}, "read": {0xD32F: 1}},  # wCurMap=0 overwrites both with 00
	{"wram": {0xD32F: b"\x01", 0xD0BF: b"\x00", 0xD0C0: b"\x00"}, "read": {0xD32F: 1}},  # first nonzero map id
	{"wram": {0xD32F: b"\xff", 0xD0BF: b"\x00", 0xD0C0: b"\x00"}, "read": {0xD32F: 1}},
	dict(POISON, wram={0xD32F: b"\x02", 0xD0BF: b"\x00", 0xD0C0: b"\x00"}, read={0xD32F: 1}),
]
# <<< factory Func_c184

# >>> factory WhiteOutDMGPals
CONTRACT["WhiteOutDMGPals"] = {"compare": (), "preserve": ()}
CASES["WhiteOutDMGPals"] = [
    {"read": {0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
    dict(POISON, read={0xFF47: 1, 0xFF48: 1, 0xFF49: 1}),
    {"a": 1, "f": 0xF0, "b": 2, "c": 3, "d": 4, "e": 5, "hl": 0x1234,
     "read": {0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
]
# <<< factory WhiteOutDMGPals

# >>> factory Func_c1f8
CONTRACT["Func_c1f8"] = {"compare": (), "preserve": ()}
CASES["Func_c1f8"] = [
    {"wram": {
        0xD0B8: b"\x00",
        0xD0B9: b"\x00",
        0xD0BA: b"\x00",
        0xD11B: b"\x00",
        0xD0C2: b"\x00",
        0xD111: b"\x00",
        0xD112: b"\x00",
        0xD3B8: b"\x00",
        0xD421: b"\x00",
        0xCE47: b"\x00",
    },
     "sram": {0: {0xA007: b"\x00", 0xA006: b"\x00"}}},
    dict(POISON,
         wram={
             0xD0B8: b"\x11",
             0xD0B9: b"\x22",
             0xD0BA: b"\x33",
             0xD11B: b"\x44",
             0xD0C2: b"\x55",
             0xD111: b"\x66",
             0xD112: b"\x77",
             0xD3B8: b"\x88",
             0xD421: b"\x99",
             0xCE47: b"\xAA",
         },
         sram={0: {0xA007: b"\x01", 0xA006: b"\x02"}}),
    {"ramg": False,
     "wram": {
         0xD0B8: b"\xFF",
         0xD0B9: b"\xFE",
         0xD0BA: b"\xFD",
         0xD11B: b"\xFC",
         0xD0C2: b"\xFB",
         0xD111: b"\xFA",
         0xD112: b"\xF9",
         0xD3B8: b"\xF8",
         0xD421: b"\xF7",
         0xCE47: b"\xF6",
     },
     "sram": {0: {0xA007: b"\xA5", 0xA006: b"\x5A"}}},
]
# <<< factory Func_c1f8

# >>> factory BackupPlayerPosition
CONTRACT["BackupPlayerPosition"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["BackupPlayerPosition"] = [
    {"wram": {0xD32F: b"\x00", 0xD330: b"\x00", 0xD331: b"\x00", 0xD334: b"\x00",
              0xD0BB: b"\x00", 0xD0BC: b"\x00", 0xD0BD: b"\x00", 0xD0BE: b"\x00"}},
    dict(POISON,
         wram={0xD32F: b"\x12", 0xD330: b"\x34", 0xD331: b"\x56", 0xD334: b"\x78",
               0xD0BB: b"\xA1", 0xD0BC: b"\xA2", 0xD0BD: b"\xA3", 0xD0BE: b"\xA4"}),
    {"wram": {0xD32F: b"\xFF", 0xD330: b"\x80", 0xD331: b"\x01", 0xD334: b"\xFE",
              0xD0BB: b"\x00", 0xD0BC: b"\x00", 0xD0BD: b"\x00", 0xD0BE: b"\x00"}},
]
# <<< factory BackupPlayerPosition

# >>> factory Func_c469
CONTRACT["Func_c469"] = {"compare": (), "preserve": ()}
CASES["Func_c469"] = [
    {"wram": {0xD235: b"\x00", 0xD236: b"\x00"}, "read": {0xD233: 1, 0xD234: 1}},
    {"wram": {0xD235: b"\x01", 0xD236: b"\x01"}, "read": {0xD233: 1, 0xD234: 1}},
    dict(POISON, wram={0xD235: b"\xAA", 0xD236: b"\x55"}, read={0xD233: 1, 0xD234: 1}),
]
# <<< factory Func_c469



# >>> factory SetScreenScroll
CONTRACT["SetScreenScroll"] = {"compare": (), "preserve": ()}
CASES["SetScreenScroll"] = [
    {"wram": {0xD0B6: b"\x00", 0xD0B7: b"\x00"}, "read": {0xFF92: 1, 0xFF93: 1}},
    {"wram": {0xD0B6: b"\x01", 0xD0B7: b"\x02"}, "read": {0xFF92: 1, 0xFF93: 1}},
    dict(POISON, wram={0xD0B6: b"\xAA", 0xD0B7: b"\x55"}, read={0xFF92: 1, 0xFF93: 1}),
]
# <<< factory SetScreenScroll




# >>> factory SetScreenScrollWram
CONTRACT["SetScreenScrollWram"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["SetScreenScrollWram"] = [
	{"wram": {0xD235: b"\x12", 0xD236: b"\x34", 0xD0B6: b"\xAA", 0xD0B7: b"\xBB"}},
	dict(POISON, wram={0xD235: b"\x56", 0xD236: b"\x78", 0xD0B6: b"\xCC", 0xD0B7: b"\xDD"}),
]
# <<< factory SetScreenScrollWram


# >>> factory Func_c70d
CONTRACT["Func_c70d"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c70d"] = [
    {"wram": {0xD32F: b"\x00", 0xD0BB: b"\x00", 0xD0B4: b"\x00"}, "read": {0xD32F: 1, 0xD0BB: 1}},
    {"wram": {0xD32F: b"\x01", 0xD0BB: b"\x00", 0xD0B4: b"\x00"}, "read": {0xD32F: 1, 0xD0BB: 1}},
    dict(POISON, wram={0xD32F: b"\x00", 0xD0BB: b"\x01", 0xD0B4: b"\x00"}, read={0xD32F: 1, 0xD0BB: 1}),
]
# <<< factory Func_c70d

# >>> factory Func_c430
CONTRACT["Func_c430"] = {"compare": (), "preserve": ()}
CASES["Func_c430"] = [
    {"wram": {0xD235: b"\x50", 0xD236: b"\x40", 0xD237: b"\x04", 0xD238: b"\x03"},
     "read": {0xD235: 1, 0xD236: 1}},
    {"wram": {0xD235: b"\x20", 0xD236: b"\x20", 0xD237: b"\x08", 0xD238: b"\x08"},
     "read": {0xD235: 1, 0xD236: 1}},
    {"wram": {0xD235: b"\xB1", 0xD236: b"\xB9", 0xD237: b"\x01", 0xD238: b"\x01"},
     "read": {0xD235: 1, 0xD236: 1}},
    dict(POISON, wram={0xD235: b"\x80", 0xD236: b"\x90", 0xD237: b"\x10", 0xD238: b"\x02"},
         read={0xD235: 1, 0xD236: 1}),
]
# <<< factory Func_c430

# >>> factory-cases-statics
wSCXBuffer = 0xD235
wSCYBuffer = 0xD236
wd237 = 0xD237
wd238 = 0xD238

wPermissionMap = 0xD133

wPlayerXCoord = 0xD330
wPlayerYCoord = 0xD331
# <<< factory-cases-statics

# >>> factory Func_c41c
CONTRACT["Func_c41c"] = {"compare": (), "preserve": ()}
CASES["Func_c41c"] = [
	{"wram": {0xD332: b"\x40", 0xD333: b"\x40", wd237: b"\x00", wd238: b"\x00"}, "read": {wSCXBuffer: 1, wSCYBuffer: 1}},
	{"wram": {0xD332: b"\x90", 0xD333: b"\xA0", wd237: b"\x10", wd238: b"\x10"}, "read": {wSCXBuffer: 1, wSCYBuffer: 1}},
	{"wram": {0xD332: b"\x00", 0xD333: b"\x01", wd237: b"\x10", wd238: b"\x04"}, "read": {wSCXBuffer: 1, wSCYBuffer: 1}},
	dict(POISON, wram={0xD332: b"\xAA", 0xD333: b"\x55", wd237: b"\x10", wd238: b"\x04"}, read={wSCXBuffer: 1, wSCYBuffer: 1}),
]
# <<< factory Func_c41c

# >>> factory Func_c3ca
CONTRACT["Func_c3ca"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c3ca"] = [
	{"b": 0x14, "c": 0x0C, "d": 0x08, "e": 0x06, "wram": {wPermissionMap: b"\x00" * 0x100}, "read": {wPermissionMap: 0x100}},
	{"b": 0x08, "c": 0x06, "d": 0xAA, "e": 0x55, "wram": {wPermissionMap: b"\x0F" * 0x100}, "read": {wPermissionMap: 0x100}},
	{"b": 0x02, "c": 0x02, "d": 0x00, "e": 0x00, "wram": {wPermissionMap: b"\xF0" * 0x100}, "read": {wPermissionMap: 0x100}},
	dict(POISON, wram={wPermissionMap: b"\x00" * 0x100}, read={wPermissionMap: 0x100}),
]
# <<< factory Func_c3ca

# >>> factory GetDirectionFromDPad
CONTRACT["GetDirectionFromDPad"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetDirectionFromDPad"] = [
	{"a": 0x00},
	{"a": 0x10},
	{"a": 0x20},
	{"a": 0x40},
	dict(POISON, a=0x80),
]
# <<< factory GetDirectionFromDPad

# >>> factory Func_c694
CONTRACT["Func_c694"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c694"] = [
    {"a": 0x00, "c": 0x01, "wram": {0xD332: b"\x20", 0xD333: b"\x30", 0xD335: b"\x01", 0xD338: b"\x10", 0xD237: b"\x00", 0xD238: b"\x00"}, "read": {0xD332: 1, 0xD333: 1, 0xD335: 1, 0xD338: 1, 0xD233: 1, 0xD234: 1, 0xD3A0: 1, 0xD3A1: 1}},
    {"a": 0x01, "c": 0x03, "wram": {0xD332: b"\x20", 0xD333: b"\x30", 0xD335: b"\x00", 0xD338: b"\x03", 0xD237: b"\x02", 0xD238: b"\x03"}, "read": {0xD332: 1, 0xD333: 1, 0xD335: 1, 0xD338: 1, 0xD233: 1, 0xD234: 1}},
    {"a": 0x03, "c": 0x02, "wram": {0xD332: b"\x80", 0xD333: b"\x80", 0xD335: b"\x04", 0xD338: b"\x01", 0xD237: b"\x10", 0xD238: b"\x10"}, "read": {0xD332: 1, 0xD333: 1, 0xD335: 1, 0xD338: 1, 0xD233: 1, 0xD234: 1}},
    dict(POISON, a=0x02, c=0x01, wram={0xD332: b"\x40", 0xD333: b"\x40", 0xD335: b"\x00", 0xD338: b"\x01", 0xD237: b"\x00", 0xD238: b"\x00"}, read={0xD332: 1, 0xD333: 1, 0xD335: 1, 0xD338: 1, 0xD233: 1, 0xD234: 1}),
]
# <<< factory Func_c694

# >>> factory FindPlayerMovementWithOffset
CONTRACT["FindPlayerMovementWithOffset"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["FindPlayerMovementWithOffset"] = [
    {"a": 0x00, "wram": {wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x20"}},
    {"a": 0x01, "wram": {wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x20"}},
    {"a": 0x02, "wram": {wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x20"}},
    {"a": 0x03, "wram": {wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x20"}},
    dict(POISON, a=0x01, wram={wPlayerXCoord: b"\xF0", wPlayerYCoord: b"\x01"}),
]
# <<< factory FindPlayerMovementWithOffset

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_c6cc
MUTATIONS["Func_c6cc"] = {
	"source_symbol": "Func_c6cc",
	"before": "wPlayerXCoordPixels = sum;",
	"after": "wPlayerXCoordPixels = a;",
	"case_ids": ["Func_c6cc-1", "Func_c6cc-2", "Func_c6cc-3", "Func_c6cc-4", "Func_c6cc-5"],
}
# <<< factory-mutation Func_c6cc
# >>> factory-mutation Func_c6d4
MUTATIONS["Func_c6d4"] = {
	"source_symbol": "Func_c6d4",
	"before": "wPlayerYCoordPixels = sum;",
	"after": "wPlayerYCoordPixels = a;",
	"case_ids": ["Func_c6d4-1", "Func_c6d4-2", "Func_c6d4-3", "Func_c6d4-4", "Func_c6d4-5"],
}
# <<< factory-mutation Func_c6d4
# >>> factory-mutation Func_c6f7
MUTATIONS["Func_c6f7"] = {
	"source_symbol": "Func_c6f7",
	"before": "wWhichSprite = wPlayerSpriteIndex;",
	"after": "wWhichSprite = 0u;",
	"case_ids": ["Func_c6f7-1", "Func_c6f7-2", "Func_c6f7-3"],
}
# <<< factory-mutation Func_c6f7
# >>> factory-mutation SetOverworldNPCFlags
MUTATIONS["SetOverworldNPCFlags"] = {"source_symbol": "SetOverworldNPCFlags", "before": "uint8_t value = (uint8_t)(a | wOverworldNPCFlags);", "after": "uint8_t value = (uint8_t)(a & wOverworldNPCFlags);", "case_ids": ["SetOverworldNPCFlags-1", "SetOverworldNPCFlags-2"]}
# <<< factory-mutation SetOverworldNPCFlags
# >>> factory-mutation Func_c158
MUTATIONS["Func_c158"] = {
	"source_symbol": "Func_c158",
	"before": "if (event != GAME_EVENT_DUEL)",
	"after": "if (event == GAME_EVENT_DUEL)",
	"case_ids": ["Func_c158-1", "Func_c158-2", "Func_c158-3"],
}
# <<< factory-mutation Func_c158
# >>> factory-mutation Func_c184
MUTATIONS["Func_c184"] = {
	"source_symbol": "Func_c184",
	"before": "if (wCurMap == OVERWORLD_MAP)",
	"after": "if (wCurMap != OVERWORLD_MAP)",
	"case_ids": ["Func_c184-1", "Func_c184-2", "Func_c184-3", "Func_c184-4"],
}
# <<< factory-mutation Func_c184
# >>> factory-mutation WhiteOutDMGPals
MUTATIONS["WhiteOutDMGPals"] = {"source_symbol": "WhiteOutDMGPals", "before": "\tSetOBP1(0u);", "after": "\tSetOBP1(1u);", "case_ids": ["WhiteOutDMGPals-0", "WhiteOutDMGPals-1", "WhiteOutDMGPals-2"]}
# <<< factory-mutation WhiteOutDMGPals
# >>> factory-mutation Func_c1f8
MUTATIONS["Func_c1f8"] = {
    "source_symbol": "Func_c1f8",
    "before": "\twRonaldIsInMap = 0u;",
    "after": "\twRonaldIsInMap = 1u;",
    "case_ids": ["Func_c1f8-0", "Func_c1f8-1", "Func_c1f8-2"],
}
# <<< factory-mutation Func_c1f8
# >>> factory-mutation BackupPlayerPosition
MUTATIONS["BackupPlayerPosition"] = {"source_symbol": "BackupPlayerPosition", "before": "\twTempMap = wCurMap;", "after": "\twTempMap = wPlayerXCoord;", "case_ids": ["BackupPlayerPosition-1", "BackupPlayerPosition-2"]}
# <<< factory-mutation BackupPlayerPosition
# >>> factory-mutation Func_c469
MUTATIONS["Func_c469"] = {"source_symbol": "Func_c469", "before": "\tscx &= 0xf8u;", "after": "\tscx &= 0xf0u;", "case_ids": ["Func_c469-2"]}
# <<< factory-mutation Func_c469
# >>> factory-mutation SetScreenScroll
MUTATIONS["SetScreenScroll"] = {"source_symbol": "SetScreenScroll", "before": "\thSCX = wSCX;", "after": "\thSCX = wSCY;", "case_ids": ["SetScreenScroll-1", "SetScreenScroll-2"]}
# <<< factory-mutation SetScreenScroll
# >>> factory-mutation SetScreenScrollWram
MUTATIONS["SetScreenScrollWram"] = {"source_symbol": "SetScreenScrollWram", "before": "\twSCY = wSCYBuffer;", "after": "\twSCY = wSCXBuffer;", "case_ids": ["SetScreenScrollWram-0", "SetScreenScrollWram-1"]}
# <<< factory-mutation SetScreenScrollWram
# >>> factory-mutation Func_c70d
MUTATIONS["Func_c70d"] = {"source_symbol": "Func_c70d", "before": "\tif (current != temporary)", "after": "\tif (current == temporary)", "case_ids": ["Func_c70d-0", "Func_c70d-1", "Func_c70d-2"]}
# <<< factory-mutation Func_c70d
# >>> factory-mutation Func_c430
MUTATIONS["Func_c430"] = {
    "source_symbol": "Func_c430",
    "before": "if (scx >= 0xB1u)",
    "after": "if (scx < 0xB1u)",
    "case_ids": ["Func_c430-0", "Func_c430-1", "Func_c430-2", "Func_c430-3"],
}
# <<< factory-mutation Func_c430
# >>> factory-mutation Func_c41c
MUTATIONS["Func_c41c"] = {
	"source_symbol": "Func_c41c",
	"before": "wSCXBuffer = (uint8_t)(wPlayerXCoordPixels - 0x40u);",
	"after": "wSCXBuffer = (uint8_t)(wPlayerXCoordPixels + 0x40u);",
	"case_ids": ["Func_c41c-1", "Func_c41c-2", "Func_c41c-3"],
}
# <<< factory-mutation Func_c41c
# >>> factory-mutation Func_c3ca
MUTATIONS["Func_c3ca"] = {
	"source_symbol": "Func_c3ca",
	"before": "gb_write8(position++, a);",
	"after": "gb_write8(position++, (uint8_t)(a & (uint8_t)~0x10u));",
	"case_ids": ["Func_c3ca-0", "Func_c3ca-1", "Func_c3ca-2", "Func_c3ca-3"],
}
# <<< factory-mutation Func_c3ca
# >>> factory-mutation GetDirectionFromDPad
MUTATIONS["GetDirectionFromDPad"] = {"source_symbol": "GetDirectionFromDPad", "before": "\t} else if (a & 0x80u) {", "after": "\t} else if (a & 0x40u) {", "case_ids": ["GetDirectionFromDPad-3", "GetDirectionFromDPad-4"]}
# <<< factory-mutation GetDirectionFromDPad
# >>> factory-mutation Func_c694
MUTATIONS["Func_c694"] = {"source_symbol": "Func_c694", "before": "wd338--;", "after": "wd338 = (uint8_t)(wd338 - 2u);", "case_ids": ["Func_c694-0", "Func_c694-1", "Func_c694-2", "Func_c694-3"]}
# <<< factory-mutation Func_c694
# >>> factory-mutation FindPlayerMovementWithOffset
MUTATIONS["FindPlayerMovementWithOffset"] = {"source_symbol": "FindPlayerMovementWithOffset", "before": "uint8_t x_offset = offsets[index];", "after": "uint8_t x_offset = (uint8_t)(offsets[index] + 1u);", "case_ids": ["FindPlayerMovementWithOffset-0", "FindPlayerMovementWithOffset-1", "FindPlayerMovementWithOffset-2", "FindPlayerMovementWithOffset-3", "FindPlayerMovementWithOffset-4"]}
# <<< factory-mutation FindPlayerMovementWithOffset
