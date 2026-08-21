# >>> factory-cases-statics
wScriptPointer = 0xD413
wLoadedEventBits = 0xD3D1
wEventVars = 0xD3D2

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wNextScript = 0xD0C6
wOverworldMode = 0xD0BF
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wEventVars = 0xD3D2
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wScriptPointer = 0xD413
wLoadedEventBits = 0xD3D1
wEventVars = 0xD3D2
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPCPacks = 0xD11E
wScriptPointer = 0xD413

wLoadedNPCTempIndex = 0xD3AA
wScriptNPC = 0xD3B6
wScriptPointer = 0xD413
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics



















CONTRACT = {}
CASES = {}

# >>> factory IncreaseScriptPointer
CONTRACT["IncreaseScriptPointer"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "d", "e", "hl"),
}
CASES["IncreaseScriptPointer"] = [
    {"a": 0, "wram": {wScriptPointer: b"\x00\x00"},
     "read": {wScriptPointer: 2}},
    dict(POISON, a=1, wram={wScriptPointer: b"\x00\xC1"},
         read={wScriptPointer: 2}),
    {"a": 0xFF, "wram": {wScriptPointer: b"\xFF\xFF"},
     "read": {wScriptPointer: 2}},
    {"a": 1, "wram": {wScriptPointer: b"\xFF\xFF"},
     "read": {wScriptPointer: 2}},
]
# <<< factory IncreaseScriptPointer


# >>> factory SetScriptPointer
CONTRACT["SetScriptPointer"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "f", "b", "c", "d", "e"),
}
CASES["SetScriptPointer"] = [
    {"b": 0, "c": 0, "wram": {wScriptPointer: b"\xFF\xFF"},
     "read": {wScriptPointer: 2}},
    dict(POISON, b=0xBB, c=0xCC,
         wram={wScriptPointer: b"\x11\x22"}, read={wScriptPointer: 2}),
    {"b": 0xFF, "c": 0xFF, "wram": {wScriptPointer: b"\x00\x00"},
     "read": {wScriptPointer: 2}},
]
# <<< factory SetScriptPointer


# >>> factory GetScriptArgsAfterPointer
CONTRACT["GetScriptArgsAfterPointer"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("d", "e", "hl"),
}
CASES["GetScriptArgsAfterPointer"] = [
    {"a": 0, "wram": {wScriptPointer: b"\x00\xC1",
                        0xC100: b"\x34\x12"}},
    dict(POISON, a=1, wram={wScriptPointer: b"\x00\xC1",
                            0xC101: b"\x56\x78"}),
    {"a": 0xFF, "wram": {wScriptPointer: b"\x00\xC1",
                           0xC1FF: b"\x00\x00"}},
    {"a": 1, "wram": {wScriptPointer: b"\xFF\xC1",
                        0xC200: b"\xAA\xBB"}},
]
# <<< factory GetScriptArgsAfterPointer


# >>> factory GetEventVar
CONTRACT["GetEventVar"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e"),
}
CASES["GetEventVar"] = [
    {"a": 0, "read": {wLoadedEventBits: 1}},
    dict(POISON, a=1, read={wLoadedEventBits: 1}),
    {"a": 0x7F, "read": {wLoadedEventBits: 1}},
    {"a": 0x80, "read": {wLoadedEventBits: 1}},
    {"a": 0xFF, "read": {wLoadedEventBits: 1}},
]
# <<< factory GetEventVar


# >>> factory IncreaseScriptPointerBy1
CONTRACT["IncreaseScriptPointerBy1"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy1"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy1

# >>> factory IncreaseScriptPointerBy2
CONTRACT["IncreaseScriptPointerBy2"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy2"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy2

# >>> factory IncreaseScriptPointerBy4
CONTRACT["IncreaseScriptPointerBy4"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy4"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy4

# >>> factory IncreaseScriptPointerBy3
CONTRACT["IncreaseScriptPointerBy3"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy3"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy3

# >>> factory GetScriptArgs5AfterPointer
CONTRACT["GetScriptArgs5AfterPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetScriptArgs5AfterPointer"] = [
	# All-zero entry state. The setup is mandatory warmth: with the script
	# pointer left at $0000 the routine reads bus addresses the oracle's RAM
	# snapshot cannot capture (previous round's ValueError), so every case
	# points the script pointer at scratch WRAM via the ported SetScriptPointer.
	# The first two seeded bytes spell the pointer little-endian so the pointer
	# is $C1xx under either reading of SetScriptPointer's bc operand.
	{"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x00}], "read": {0xC100: 16}},
	dict(POISON, setup=[{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x00}],
	     wram={0xC100: b"\x00\xc1\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\x0f"}),
	{"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x40}],
	 "wram": {0xC140: b"\x40\xc1\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\x0f"},
	 "read": {0xC140: 16}},
	{"setup": [{"fn": "SetScriptPointer", "b": 0xC9, "c": 0xF0}],
	 "wram": {0xC9F0: b"\xf0\xc9\x7e\x81\xfe\x01\xc3\x3c"}},
]
# <<< factory GetScriptArgs5AfterPointer

# >>> factory SetScriptControlByteFail
CONTRACT["SetScriptControlByteFail"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetScriptControlByteFail"] = [
	{},
	{"a": 0x5A, "wram": {0xD415: b"\x80"}},
	{"f": 0x50, "wram": {0xD415: b"\xff"}},
	dict(POISON, wram={0xD415: b"\xff"}),
]
# <<< factory SetScriptControlByteFail

# >>> factory IncreaseScriptPointerBy5
CONTRACT["IncreaseScriptPointerBy5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["IncreaseScriptPointerBy5"] = [
	{},
	dict(POISON),
	dict(POISON, wram={0xC100: b"\x11\x22\x33\x44"}),
]
# <<< factory IncreaseScriptPointerBy5

# >>> factory IncreaseScriptPointerBy6
CONTRACT["IncreaseScriptPointerBy6"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["IncreaseScriptPointerBy6"] = [
	{},
	dict(POISON),
	dict(POISON, wram={0xC100: b"\x11\x22\x33\x44"}),
]
# <<< factory IncreaseScriptPointerBy6

# >>> factory IncreaseScriptPointerBy7
CONTRACT["IncreaseScriptPointerBy7"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["IncreaseScriptPointerBy7"] = [
	{},
	dict(POISON),
	dict(POISON, wram={0xC100: b"\x11\x22\x33\x44"}),
]
# <<< factory IncreaseScriptPointerBy7

# >>> factory GetScriptArgs2AfterPointer
CONTRACT["GetScriptArgs2AfterPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetScriptArgs2AfterPointer"] = [
    {},
    dict(POISON, setup=[{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x00}], wram={0xC100: b"\x10\x21\x32\x43\x54\x65"}),
    {"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0xFE}], "wram": {0xC1FE: b"\x76\x87\x98\xa9\xba\xcb"}},
]
# <<< factory GetScriptArgs2AfterPointer

# >>> factory GetScriptArgs3AfterPointer
CONTRACT["GetScriptArgs3AfterPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetScriptArgs3AfterPointer"] = [{}, dict(POISON), {"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x00}], "wram": {0xC100: b"\x10\x21\x32\x43\x54\x65\x76\x87"}, "read": {0xC100: 8}}, {"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0xFC}], "wram": {0xC1FC: b"\x91\xa2\xb3\xc4\xd5\xe6\xf7\x08"}, "read": {0xC1FC: 8}}]
# <<< factory GetScriptArgs3AfterPointer

# >>> factory SetScriptControlBytePass
CONTRACT["SetScriptControlBytePass"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["SetScriptControlBytePass"] = [{"wram": {0xD415: b"\x00"}}, dict(POISON, wram={0xD415: b"\x00"})]
# <<< factory SetScriptControlBytePass

# >>> factory ScriptCommand_JumpIfCardInCollection
CONTRACT["ScriptCommand_JumpIfCardInCollection"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("d", "e")}
CASES["ScriptCommand_JumpIfCardInCollection"] = [
    {},
    {"c": 1},
    {"c": 4},
    {"c": 0xE4},
    {"c": 0xFF},
    dict(POISON, b=0xBB, c=0x04),
    dict(POISON, b=0xBB, c=0x00),
    dict(POISON, b=0xBB, c=0xFF),
]
# <<< factory ScriptCommand_JumpIfCardInCollection

# >>> factory ScriptCommand_GiveCard
CONTRACT["ScriptCommand_GiveCard"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_GiveCard"] = [
    {"c": 0, "wram": {0xD697: b"\x00"}, "sread": {0: {0xA000: 0x400}}},
    {"c": 2, "wram": {0xD697: b"\x08"}, "sread": {0: {0xA000: 0x400}}},
    {"c": 0, "wram": {0xD697: b"\x08"}, "sread": {0: {0xA000: 0x400}}},
    {"c": 1, "wram": {0xD697: b"\xE4"}, "sread": {0: {0xA000: 0x400}}},
    dict(POISON, c=0, wram={0xD697: b"\x40"}, sread={0: {0xA000: 0x400}}),
    dict(POISON, c=0x80, wram={0xD697: b"\x01"}, sread={0: {0xA000: 0x400}}),
]
# <<< factory ScriptCommand_GiveCard

# >>> factory ScriptCommand_TakeCard
CONTRACT["ScriptCommand_TakeCard"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_TakeCard"] = [
    {"c": 0},
    {"c": 1},
    {"c": 2},
    {"c": 0x40},
    {"c": 0xFF},
    dict(POISON, c=8),
]
# <<< factory ScriptCommand_TakeCard

# >>> factory ScriptCommand_PauseSong
CONTRACT["ScriptCommand_PauseSong"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_PauseSong"] = [
    {},
    dict(POISON),
]
# <<< factory ScriptCommand_PauseSong

# >>> factory ScriptCommand_ResumeSong
CONTRACT["ScriptCommand_ResumeSong"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_ResumeSong"] = [
    {},
    dict(POISON),
]
# <<< factory ScriptCommand_ResumeSong

# >>> factory ScriptCommand_nop
# wram keys 0xD111/0xD112 are wDefaultSong/wSongOverride, verified untouched
CONTRACT["ScriptCommand_nop"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_nop"] = [
	{"wram": {0xD111: b"\x00", 0xD112: b"\x00"}},
	dict(POISON, wram={0xD111: b"\x11", 0xD112: b"\x22"}),
]
# <<< factory ScriptCommand_nop

# >>> factory ScriptCommand_OverrideSong
# wram keys: 0xD111 = wDefaultSong, 0xD112 = wSongOverride
CONTRACT["ScriptCommand_OverrideSong"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_OverrideSong"] = [
	{"c": 0, "wram": {0xD111: b"\x00", 0xD112: b"\x00"}},
	{"c": 0x0F, "wram": {0xD111: b"\x11", 0xD112: b"\x22"}},
	{"c": 0xFF, "wram": {0xD111: b"\x00", 0xD112: b"\x00"}},
	dict(POISON, c=0x0C, wram={0xD111: b"\x00", 0xD112: b"\x00"}),
]
# <<< factory ScriptCommand_OverrideSong

# >>> factory ScriptCommand_SetDefaultSong
# wram keys: 0xD111 = wDefaultSong, 0xD112 = wSongOverride
CONTRACT["ScriptCommand_SetDefaultSong"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_SetDefaultSong"] = [
	{"c": 0, "wram": {0xD111: b"\x00", 0xD112: b"\x00"}},
	{"c": 0x33, "wram": {0xD111: b"\x11", 0xD112: b"\x22"}},
	{"c": 0xFF, "wram": {0xD111: b"\x00", 0xD112: b"\x00"}},
	dict(POISON, c=0x07, wram={0xD111: b"\x00", 0xD112: b"\x00"}),
]
# <<< factory ScriptCommand_SetDefaultSong

# >>> factory ScriptCommand_RecordMasterWin
CONTRACT["ScriptCommand_RecordMasterWin"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_RecordMasterWin"] = [
	{"c": 0},
	{"c": 1},
	{"c": 8},
	{"c": 0x1F},
	dict(POISON, c=0x05),
]
# <<< factory ScriptCommand_RecordMasterWin

# >>> factory ScriptCommand_ChallengeMachine
CONTRACT["ScriptCommand_ChallengeMachine"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_ChallengeMachine"] = [
	{"wram": {0xD0B5: b"\x00", 0xD0B4: b"\x00"}},  # wGameEvent, wOverworldTransition
	{"wram": {0xD0B5: b"\xFF", 0xD0B4: b"\x35"}},  # set 6 must leave the other bits alone
	{"wram": {0xD0B5: b"\x69", 0xD0B4: b"\xBF"}},  # bit 6 already set stays set; wGameEvent overwritten
	dict(POISON, wram={0xD0B5: b"\x00", 0xD0B4: b"\x35"}),
]
# <<< factory ScriptCommand_ChallengeMachine

# >>> factory ScriptCommand_PlaySong
CONTRACT["ScriptCommand_PlaySong"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_PlaySong"] = [
    {},
    {"c": 0x01},
    {"c": 0x64},
    dict(POISON, c=0x05),
]
# <<< factory ScriptCommand_PlaySong

# >>> factory ScriptCommand_PlaySFX
CONTRACT["ScriptCommand_PlaySFX"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_PlaySFX"] = [
    {},
    {"c": 0x01},
    {"c": 0x10},
    dict(POISON, c=0x02),
]
# <<< factory ScriptCommand_PlaySFX

# >>> factory ScriptCommand_PlayDefaultSong
CONTRACT["ScriptCommand_PlayDefaultSong"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_PlayDefaultSong"] = [
    {},
    dict(POISON),
]
# <<< factory ScriptCommand_PlayDefaultSong

# >>> factory ScriptCommand_SetSpriteAttributes
CONTRACT["ScriptCommand_SetSpriteAttributes"] = {"compare": ("a", "f", "b", "c", "e"), "preserve": ("b",)}
CASES["ScriptCommand_SetSpriteAttributes"] = [
	{"wram": {0xD3B6: b"\x00", 0xD3AA: b"\x00", 0xCAB4: b"\x00"}},  # all zero, wConsole below CONSOLE_CGB
	{"b": 0x11, "c": 0x22, "wram": {0xCAB4: b"\x02", 0xD3B6: b"\x01", 0xD3AA: b"\x00"}},  # wConsole == CONSOLE_CGB: e = b
	{"b": 0x33, "c": 0x44, "wram": {0xCAB4: b"\x03", 0xD3B6: b"\x02", 0xD3AA: b"\xff"}},  # just above CONSOLE_CGB: e = c
	dict(POISON, b=0x10, c=0x20, wram={0xCAB4: b"\x02", 0xD3B6: b"\x01", 0xD3AA: b"\xaa"}),
]
# <<< factory ScriptCommand_SetSpriteAttributes

# >>> factory ScriptCommand_DoFrames
CONTRACT["ScriptCommand_DoFrames"] = {"compare": ("a", "f", "b", "c"), "preserve": ("b",)}
CASES["ScriptCommand_DoFrames"] = [
	{"c": 0},  # count 0 acts as 256 frames, never a no-op
	{"c": 1},
	{"c": 2},
	dict(POISON, c=3),
]
# <<< factory ScriptCommand_DoFrames

# >>> factory ScriptCommand_EndScript
wBreakScriptLoop = 0xD412
wDuelTheme = 0xCC1A
wGameEvent = 0xD0B5
wNPCDuelDeckID = 0xCC19
wNPCDuelPrizes = 0xCC18
wOverworldTransition = 0xD0B4
wScriptControlByte = 0xD415
CONTRACT["ScriptCommand_EndScript"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["ScriptCommand_EndScript"] = [
	{},
	dict(POISON),
	{"wram": {wBreakScriptLoop: b"\x00", wScriptControlByte: b"\x00"}},
	{"wram": {wBreakScriptLoop: b"\x5a", wScriptControlByte: b"\xff"}},
	dict(POISON, wram={wBreakScriptLoop: b"\x00", wScriptControlByte: b"\x00"}),
]
# <<< factory ScriptCommand_EndScript

# >>> factory SetNPCDuelParams
CONTRACT["SetNPCDuelParams"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["SetNPCDuelParams"] = [
	{},
	{"b": 0x00, "c": 0x00, "wram": {wNPCDuelPrizes: b"\x00", wNPCDuelDeckID: b"\x00", wDuelTheme: b"\x00", wScriptControlByte: b"\x00"}},
	{"b": 0x15, "c": 0x06, "wram": {wNPCDuelPrizes: b"\xaa", wNPCDuelDeckID: b"\xbb", wDuelTheme: b"\xcc"}},
	{"b": 0xFF, "c": 0xFF, "wram": {wNPCDuelPrizes: b"\x00", wNPCDuelDeckID: b"\x00", wDuelTheme: b"\x00"}},
	{"b": 0x01, "c": 0x00, "wram": {wNPCDuelPrizes: b"\x00", wNPCDuelDeckID: b"\x00", wDuelTheme: b"\x00"}},
	dict(POISON, b=0x34, c=0x12, wram={wNPCDuelPrizes: b"\x11", wNPCDuelDeckID: b"\x22", wDuelTheme: b"\x33"}),
]
# <<< factory SetNPCDuelParams

# >>> factory ScriptCommand_BattleCenter
wOverworldTransition = 0xD0B4
wGameEvent = 0xD0B5
CONTRACT["ScriptCommand_BattleCenter"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_BattleCenter"] = [
	{"wram": {wOverworldTransition: b"\x00\x00"}},
	{"wram": {wOverworldTransition: b"\xff\xff"}},
	{"wram": {wOverworldTransition: b"\xbf\x77"}},
	{"wram": {wOverworldTransition: b"\x40\x02"}},
	dict(POISON, wram={wOverworldTransition: b"\x35\x99"}),
]
# <<< factory ScriptCommand_BattleCenter

# >>> factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot
CONTRACT["ScriptCommand_LoadCurrentMapNameIntoTxRamSlot"] = {"compare": ("a", "f", "b", "c"), "preserve": ()}
CASES["ScriptCommand_LoadCurrentMapNameIntoTxRamSlot"] = [
	{"c": 0, "wram": {0xD413: b"\x00\x00"}},
	{"c": 0, "wram": {0xD32E: b"\x00", 0xD413: b"\xff\xff"}},
	{"c": 1, "wram": {0xD32E: b"\x01", 0xD413: b"\x10\x06"}},
	{"c": 2, "wram": {0xD32E: b"\x0b"}},
	{"c": 0x40, "wram": {0xD32E: b"\x80"}},
	{"c": 0x7f, "wram": {0xD32E: b"\xff"}},
	dict(POISON, c=3, wram={0xD32E: b"\x05", 0xD413: b"\x00\xd0"}),
]
# <<< factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot

# >>> factory ScriptCommand_EnterMap
CONTRACT["ScriptCommand_EnterMap"] = {"compare": ("a", "f", "c", "b", "d", "e"), "preserve": ("b", "d", "e")}
CASES["ScriptCommand_EnterMap"] = [
	{},
	{"wram": {0xD413: b"\x3f\x06", 0xD0B4: b"\x00"}},
	{"wram": {0xD413: b"\xfd\xff", 0xD0B4: b"\xef"}},
	{"wram": {0xD413: b"\xff\xff", 0xD0B4: b"\xff", 0xD0BB: b"\x00", 0xD0BC: b"\x00", 0xD0BD: b"\x00", 0xD0BE: b"\x00"}},
	dict(POISON, wram={0xD413: b"\x00\xd0", 0xD0B4: b"\x0f", 0xD0BB: b"\x11", 0xD0BC: b"\x22", 0xD0BD: b"\x33", 0xD0BE: b"\x44"}),
]
# <<< factory ScriptCommand_EnterMap

# >>> factory GetScriptArgs1AfterPointer
CONTRACT["GetScriptArgs1AfterPointer"] = {"compare": ("a", "f", "b", "c"), "preserve": ()}
CASES["GetScriptArgs1AfterPointer"] = [{}, dict(POISON), {"a": 0xFF, "f": 0x40, "b": 0x12, "c": 0x34}]
# <<< factory GetScriptArgs1AfterPointer

# >>> factory SetNextScript
CONTRACT["SetNextScript"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNextScript"] = [
	{"b": 0x00, "c": 0x00, "wram": {wNextScript: b"\x00\x00", wOverworldMode: b"\x00"}, "expect": {wNextScript: b"\x00\x00", wOverworldMode: b"\x03"}},
	{"b": 0x12, "c": 0x34, "wram": {wNextScript: b"\xFF\xFF", wOverworldMode: b"\xFF"}, "expect": {wNextScript: b"\x34\x12", wOverworldMode: b"\x03"}},
	dict(POISON, wram={wNextScript: b"\x00\x00", wOverworldMode: b"\x00"}, expect={wNextScript: b"\xCC\xBB", wOverworldMode: b"\x03"}),
]
# <<< factory SetNextScript

# >>> factory SetEventValue
CONTRACT["SetEventValue"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["SetEventValue"] = [
    {"a": 0, "c": 0, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    dict(POISON, a=1, c=0x5A, read={wLoadedEventBits: 1, wEventVars: 64}),
    {"a": 0x7F, "c": 0xFF, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    {"a": 0x80, "c": 0x01, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    {"a": 0xFF, "c": 0xA5, "read": {wLoadedEventBits: 1, wEventVars: 64}},
]
# <<< factory SetEventValue

# >>> factory MaxOutEventValue
CONTRACT["MaxOutEventValue"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["MaxOutEventValue"] = [
    {"a": 0, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    dict(POISON, a=1, read={wLoadedEventBits: 1, wEventVars: 64}),
    {"a": 0x7F, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    {"a": 0x80, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    {"a": 0xFF, "read": {wLoadedEventBits: 1, wEventVars: 64}},
]
# <<< factory MaxOutEventValue

# >>> factory ZeroOutEventValue
CONTRACT["ZeroOutEventValue"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ZeroOutEventValue"] = [
    {"a": 0, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    dict(POISON, a=1, read={wLoadedEventBits: 1, wEventVars: 64}),
    {"a": 0x7F, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    {"a": 0x80, "read": {wLoadedEventBits: 1, wEventVars: 64}},
    {"a": 0xFF, "read": {wLoadedEventBits: 1, wEventVars: 64}},
]
# <<< factory ZeroOutEventValue

# >>> factory ClearEvents
CONTRACT["ClearEvents"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["ClearEvents"] = [
    {"wram": {wEventVars: b"\x11" * 0x40}, "read": {wEventVars: 0x40}},
    dict(POISON, wram={wEventVars: b"\xAA" * 0x40},
         read={wEventVars: 0x40}),
    {"wram": {wEventVars: b"\xFF" * 0x40}, "read": {wEventVars: 0x40}},
]
# <<< factory ClearEvents

# >>> factory ScriptCommand_Jump
CONTRACT["ScriptCommand_Jump"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["ScriptCommand_Jump"] = [
    {"wram": {wScriptPointer: b"\x00\xC5", 0xC501: b"\x34\x12"}, "read": {wScriptPointer: 2}},
    {"wram": {wScriptPointer: b"\xFE\xC4", 0xC4FF: b"\x00\x00"}, "read": {wScriptPointer: 2}},
    dict(POISON, wram={wScriptPointer: b"\x00\xC5", 0xC501: b"\xCC\xBB"}, read={wScriptPointer: 2}),
    {"a": 0xFF, "f": 0x40, "wram": {wScriptPointer: b"\x10\xC5", 0xC511: b"\x00\x80"}, "read": {wScriptPointer: 2}},
]
# <<< factory ScriptCommand_Jump

# >>> factory ScriptCommand_MaxOutEventValue
CONTRACT["ScriptCommand_MaxOutEventValue"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["ScriptCommand_MaxOutEventValue"] = [
    {"c": 0, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    dict(POISON, c=1, wram={wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, read={wScriptPointer: 2, wEventVars: 0x40}),
    {"c": 0x7F, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    {"c": 0x80, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    {"c": 0xFF, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
]
# <<< factory ScriptCommand_MaxOutEventValue

# >>> factory ScriptCommand_ZeroOutEventValue
CONTRACT["ScriptCommand_ZeroOutEventValue"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["ScriptCommand_ZeroOutEventValue"] = [
    {"c": 0, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    dict(POISON, c=1, wram={wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, read={wScriptPointer: 2, wEventVars: 0x40}),
    {"c": 0x7F, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    {"c": 0x80, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    {"c": 0xFF, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
]
# <<< factory ScriptCommand_ZeroOutEventValue

# >>> factory ScriptCommand_SetEventValue
CONTRACT["ScriptCommand_SetEventValue"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["ScriptCommand_SetEventValue"] = [
    {"c": 0, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    dict(POISON, c=1, wram={wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, read={wScriptPointer: 2, wEventVars: 0x40}),
    {"c": 0x7F, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    {"c": 0x80, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
    {"c": 0xFF, "wram": {wScriptPointer: b"\x00\xC5", wLoadedEventBits: b"\x01", wEventVars: b"\x00" * 0x40}, "read": {wScriptPointer: 2, wEventVars: 0x40}},
]
# <<< factory ScriptCommand_SetEventValue

# >>> factory ScriptCommand_TryGivePCPack
CONTRACT["ScriptCommand_TryGivePCPack"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["ScriptCommand_TryGivePCPack"] = [
    {"c": 0, "wram": {wPCPacks: bytes(15), wScriptPointer: b"\x00\x00"}, "read": {wPCPacks: 15, wScriptPointer: 2}},
    {"c": 1, "wram": {wPCPacks: bytes(15), wScriptPointer: b"\xfe\x00"}, "read": {wPCPacks: 15, wScriptPointer: 2}},
    {"c": 14, "wram": {wPCPacks: bytes(14) + b"\x01", wScriptPointer: b"\xff\x12"}, "read": {wPCPacks: 15, wScriptPointer: 2}},
    {"c": 0x7F, "wram": {wPCPacks: bytes([1] * 15), wScriptPointer: b"\x00\x80"}, "read": {wPCPacks: 15, wScriptPointer: 2}},
    dict(POISON, wram={wPCPacks: bytes(15), wScriptPointer: b"\x00\x00"}, read={wPCPacks: 15, wScriptPointer: 2}),
]
# <<< factory ScriptCommand_TryGivePCPack

# >>> factory ScriptCommand_SetActiveNPCCoords
CONTRACT["ScriptCommand_SetActiveNPCCoords"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["ScriptCommand_SetActiveNPCCoords"] = [
    {"b": 0x06, "c": 0x04, "wram": {wScriptNPC: b"\x00", wLoadedNPCTempIndex: b"\x00", wScriptPointer: b"\x00\xC5", 0xD34C: b"\x00\x00", 0xD133: b"\xFF", 0xD165: b"\x00"}, "expect": {0xD34C: b"\x06\x04", 0xD133: b"\xBF", 0xD165: b"\x40", wScriptPointer: b"\x03\xC5"}, "read": {wScriptPointer: 2}},
    {"b": 0x10, "c": 0x0E, "wram": {wScriptNPC: b"\x01", wLoadedNPCTempIndex: b"\x00", wScriptPointer: b"\x00\xC5", 0xD356: b"\x04\x06", 0xD165: b"\xFF", 0xD1BA: b"\x7F"}, "expect": {0xD356: b"\x0E\x10", 0xD165: b"\xBF", 0xD1BA: b"\x40", wScriptPointer: b"\x03\xC5"}, "read": {wScriptPointer: 2}},
    {"b": 0x04, "c": 0x02, "wram": {wScriptNPC: b"\x07", wLoadedNPCTempIndex: b"\x00", wScriptPointer: b"\x00\xC5", 0xD39C: b"\x0E\x10", 0xD1BA: b"\xFF", 0xD154: b"\x00"}, "expect": {0xD39C: b"\x02\x04", 0xD1BA: b"\xBF", 0xD154: b"\x40", wScriptPointer: b"\x03\xC5"}, "read": {wScriptPointer: 2}},
    dict(POISON, b=0x14, c=0x12, wram={wScriptNPC: b"\xAA", wLoadedNPCTempIndex: b"\x00", wScriptPointer: b"\x00\xC5", 0xD34C: b"\x08\x0A", 0xD183: b"\xFF", 0xD1DC: b"\x00"}, expect={0xD34C: b"\x12\x14", 0xD183: b"\xBF", 0xD1DC: b"\x40", wScriptPointer: b"\x03\xC5"}, read={wScriptPointer: 2}),
]
# <<< factory ScriptCommand_SetActiveNPCCoords

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}

# >>> factory-mutation IncreaseScriptPointer
MUTATIONS["IncreaseScriptPointer"] = {
    "source_symbol": "IncreaseScriptPointer",
    "before": "uint16_t low_sum = (uint16_t)low + a;",
    "after": "uint16_t low_sum = (uint16_t)low + (uint8_t)(a << 1);",
    "case_ids": ["IncreaseScriptPointer-1", "IncreaseScriptPointer-2"],
}
# <<< factory-mutation IncreaseScriptPointer

# >>> factory-mutation SetScriptPointer
MUTATIONS["SetScriptPointer"] = {
    "source_symbol": "SetScriptPointer",
    "before": "gb_write8(wScriptPointer_ADDR, (uint8_t)bc);",
    "after": "gb_write8(wScriptPointer_ADDR, (uint8_t)(bc ^ 0xFFu));",
    "case_ids": ["SetScriptPointer-1", "SetScriptPointer-2"],
}
# <<< factory-mutation SetScriptPointer

# >>> factory-mutation GetScriptArgsAfterPointer
MUTATIONS["GetScriptArgsAfterPointer"] = {
    "source_symbol": "GetScriptArgsAfterPointer",
    "before": "uint16_t target = (uint16_t)(pointer + a);",
    "after": "uint16_t target = (uint16_t)(pointer + (uint8_t)(a + 1u));",
    "case_ids": ["GetScriptArgsAfterPointer-1", "GetScriptArgsAfterPointer-3"],
}
# <<< factory-mutation GetScriptArgsAfterPointer

# >>> factory-mutation GetEventVar
MUTATIONS["GetEventVar"] = {
    "source_symbol": "GetEventVar",
    "before": "uint16_t bc = (uint16_t)a * 2u;",
    "after": "uint16_t bc = (uint16_t)a * 4u;",
    "case_ids": ["GetEventVar-1", "GetEventVar-3", "GetEventVar-4"],
}
# <<< factory-mutation GetEventVar
# >>> factory-mutation IncreaseScriptPointerBy1
MUTATIONS["IncreaseScriptPointerBy1"] = {"source_symbol": "IncreaseScriptPointerBy1", "before": "return IncreaseScriptPointer(1u);", "after": "return IncreaseScriptPointer(2u);", "case_ids": ["IncreaseScriptPointerBy1-0", "IncreaseScriptPointerBy1-1"]}
# <<< factory-mutation IncreaseScriptPointerBy1
# >>> factory-mutation IncreaseScriptPointerBy2
MUTATIONS["IncreaseScriptPointerBy2"] = {"source_symbol": "IncreaseScriptPointerBy2", "before": "return IncreaseScriptPointer(2u);", "after": "return IncreaseScriptPointer(1u);", "case_ids": ["IncreaseScriptPointerBy2-0", "IncreaseScriptPointerBy2-1"]}
# <<< factory-mutation IncreaseScriptPointerBy2
# >>> factory-mutation IncreaseScriptPointerBy4
MUTATIONS["IncreaseScriptPointerBy4"] = {"source_symbol": "IncreaseScriptPointerBy4", "before": "return IncreaseScriptPointer(4u);", "after": "return IncreaseScriptPointer(1u);", "case_ids": ["IncreaseScriptPointerBy4-0", "IncreaseScriptPointerBy4-1"]}
# <<< factory-mutation IncreaseScriptPointerBy4
# >>> factory-mutation IncreaseScriptPointerBy3
MUTATIONS["IncreaseScriptPointerBy3"] = {
	"source_symbol": "IncreaseScriptPointerBy3",
	"before": "return IncreaseScriptPointer(3u);",
	"after": "return IncreaseScriptPointer(4u);",
	"case_ids": ["IncreaseScriptPointerBy3-0", "IncreaseScriptPointerBy3-1"],
}
# <<< factory-mutation IncreaseScriptPointerBy3
# >>> factory-mutation GetScriptArgs5AfterPointer
MUTATIONS["GetScriptArgs5AfterPointer"] = {
	"source_symbol": "GetScriptArgs5AfterPointer",
	"before": "\treturn GetScriptArgsAfterPointer(5u);",
	"after": "\treturn GetScriptArgsAfterPointer(4u);",
	"case_ids": ["GetScriptArgs5AfterPointer-1", "GetScriptArgs5AfterPointer-2", "GetScriptArgs5AfterPointer-3"],
}
# <<< factory-mutation GetScriptArgs5AfterPointer
# >>> factory-mutation SetScriptControlByteFail
MUTATIONS["SetScriptControlByteFail"] = {
	"source_symbol": "SetScriptControlByteFail",
	"before": "\treturn (SetScriptControlByteFailResult){0x00u, 0x80u};",
	"after": "\treturn (SetScriptControlByteFailResult){0x00u, 0x90u};",
	"case_ids": ["SetScriptControlByteFail-0", "SetScriptControlByteFail-1", "SetScriptControlByteFail-2", "SetScriptControlByteFail-3"],
}
# <<< factory-mutation SetScriptControlByteFail
# >>> factory-mutation IncreaseScriptPointerBy5
MUTATIONS["IncreaseScriptPointerBy5"] = {
	"source_symbol": "IncreaseScriptPointerBy5",
	"before": "\treturn IncreaseScriptPointer(5u);",
	"after": "\treturn IncreaseScriptPointer(6u);",
	"case_ids": ["IncreaseScriptPointerBy5-0", "IncreaseScriptPointerBy5-1", "IncreaseScriptPointerBy5-2"],
}
# <<< factory-mutation IncreaseScriptPointerBy5
# >>> factory-mutation IncreaseScriptPointerBy6
MUTATIONS["IncreaseScriptPointerBy6"] = {
	"source_symbol": "IncreaseScriptPointerBy6",
	"before": "\treturn IncreaseScriptPointer(6u);",
	"after": "\treturn IncreaseScriptPointer(5u);",
	"case_ids": ["IncreaseScriptPointerBy6-0", "IncreaseScriptPointerBy6-1", "IncreaseScriptPointerBy6-2"],
}
# <<< factory-mutation IncreaseScriptPointerBy6
# >>> factory-mutation IncreaseScriptPointerBy7
MUTATIONS["IncreaseScriptPointerBy7"] = {
	"source_symbol": "IncreaseScriptPointerBy7",
	"before": "\treturn IncreaseScriptPointer(7u);",
	"after": "\treturn IncreaseScriptPointer(6u);",
	"case_ids": ["IncreaseScriptPointerBy7-0", "IncreaseScriptPointerBy7-1", "IncreaseScriptPointerBy7-2"],
}
# <<< factory-mutation IncreaseScriptPointerBy7
# >>> factory-mutation GetScriptArgs2AfterPointer
MUTATIONS["GetScriptArgs2AfterPointer"] = {"source_symbol": "GetScriptArgs2AfterPointer", "before": "\treturn GetScriptArgsAfterPointer(2u);", "after": "\treturn GetScriptArgsAfterPointer(3u);", "case_ids": ["GetScriptArgs2AfterPointer-1", "GetScriptArgs2AfterPointer-2"]}
# <<< factory-mutation GetScriptArgs2AfterPointer
# >>> factory-mutation GetScriptArgs3AfterPointer
MUTATIONS["GetScriptArgs3AfterPointer"] = {"source_symbol": "GetScriptArgs3AfterPointer", "before": "\treturn GetScriptArgsAfterPointer(3u);", "after": "\treturn GetScriptArgsAfterPointer(4u);", "case_ids": ["GetScriptArgs3AfterPointer-2", "GetScriptArgs3AfterPointer-3"]}
# <<< factory-mutation GetScriptArgs3AfterPointer
# >>> factory-mutation SetScriptControlBytePass
MUTATIONS["SetScriptControlBytePass"] = {"source_symbol": "SetScriptControlBytePass", "before": "\twScriptControlByte = 0xffu;", "after": "\twScriptControlByte = 0xfeu;", "case_ids": ["SetScriptControlBytePass-0", "SetScriptControlBytePass-1"]}
# <<< factory-mutation SetScriptControlBytePass
# >>> factory-mutation ScriptCommand_JumpIfCardInCollection
MUTATIONS["ScriptCommand_JumpIfCardInCollection"] = {
    "source_symbol": "ScriptCommand_JumpIfCardInCollection",
    "before": "\tif (cnt.a == 0) {",
    "after": "\tif (cnt.a != 0) {",
    "case_ids": [
        "ScriptCommand_JumpIfCardInCollection-5",
        "ScriptCommand_JumpIfCardInCollection-6",
        "ScriptCommand_JumpIfCardInCollection-7",
    ],
}
# <<< factory-mutation ScriptCommand_JumpIfCardInCollection
# >>> factory-mutation ScriptCommand_GiveCard
MUTATIONS["ScriptCommand_GiveCard"] = {
    "source_symbol": "ScriptCommand_GiveCard",
    "before": "\t\ta = wCardReceived;",
    "after": "\t\ta = (uint8_t)(c + 1u);",
    "case_ids": ["ScriptCommand_GiveCard-2", "ScriptCommand_GiveCard-4"],
}
# <<< factory-mutation ScriptCommand_GiveCard
# >>> factory-mutation ScriptCommand_TakeCard
MUTATIONS["ScriptCommand_TakeCard"] = {
    "source_symbol": "ScriptCommand_TakeCard",
    "before": "\tRemoveCardFromCollection(c);\n\treturn IncreaseScriptPointerBy2();",
    "after": "\tRemoveCardFromCollection(c);\n\treturn IncreaseScriptPointerBy3();",
    "case_ids": ["ScriptCommand_TakeCard-0", "ScriptCommand_TakeCard-1", "ScriptCommand_TakeCard-2", "ScriptCommand_TakeCard-3", "ScriptCommand_TakeCard-4", "ScriptCommand_TakeCard-5"],
}
# <<< factory-mutation ScriptCommand_TakeCard
# >>> factory-mutation ScriptCommand_PauseSong
MUTATIONS["ScriptCommand_PauseSong"] = {
    "source_symbol": "ScriptCommand_PauseSong",
    "before": "\tPauseSong();\n\tIncreaseScriptPointerResult r = IncreaseScriptPointerBy1();\n\treturn r;",
    "after": "\tPauseSong();\n\tIncreaseScriptPointerResult r = IncreaseScriptPointerBy1();\n\tr.c = (uint8_t)(r.c + 1u);\n\treturn r;",
    "case_ids": ["ScriptCommand_PauseSong-0", "ScriptCommand_PauseSong-1"],
}
# <<< factory-mutation ScriptCommand_PauseSong
# >>> factory-mutation ScriptCommand_ResumeSong
MUTATIONS["ScriptCommand_ResumeSong"] = {
    "source_symbol": "ScriptCommand_ResumeSong",
    "before": "\tResumeSong();\n\tIncreaseScriptPointerResult r = IncreaseScriptPointerBy1();\n\treturn r;",
    "after": "\tResumeSong();\n\tIncreaseScriptPointerResult r = IncreaseScriptPointerBy1();\n\tr.c = (uint8_t)(r.c + 1u);\n\treturn r;",
    "case_ids": ["ScriptCommand_ResumeSong-0", "ScriptCommand_ResumeSong-1"],
}
# <<< factory-mutation ScriptCommand_ResumeSong
# >>> factory-mutation ScriptCommand_nop
MUTATIONS["ScriptCommand_nop"] = {
	"source_symbol": "ScriptCommand_nop",
	"before": "\treturn IncreaseScriptPointerBy1();",
	"after": "\treturn IncreaseScriptPointerBy2();",
	"case_ids": ["ScriptCommand_nop-0", "ScriptCommand_nop-1"],
}
# <<< factory-mutation ScriptCommand_nop
# >>> factory-mutation ScriptCommand_OverrideSong
MUTATIONS["ScriptCommand_OverrideSong"] = {
	"source_symbol": "ScriptCommand_OverrideSong",
	"before": "\twSongOverride = c;",
	"after": "\twDefaultSong = c;",
	"case_ids": ["ScriptCommand_OverrideSong-1", "ScriptCommand_OverrideSong-2", "ScriptCommand_OverrideSong-3"],
}
# <<< factory-mutation ScriptCommand_OverrideSong
# >>> factory-mutation ScriptCommand_SetDefaultSong
MUTATIONS["ScriptCommand_SetDefaultSong"] = {
	"source_symbol": "ScriptCommand_SetDefaultSong",
	"before": "\twDefaultSong = c;",
	"after": "\twSongOverride = c;",
	"case_ids": ["ScriptCommand_SetDefaultSong-1", "ScriptCommand_SetDefaultSong-2", "ScriptCommand_SetDefaultSong-3"],
}
# <<< factory-mutation ScriptCommand_SetDefaultSong
# >>> factory-mutation ScriptCommand_RecordMasterWin
MUTATIONS["ScriptCommand_RecordMasterWin"] = {
	"source_symbol": "ScriptCommand_RecordMasterWin",
	"before": "\tAddMasterBeatenToList(c, &f);\n\treturn IncreaseScriptPointerBy2();",
	"after": "\tAddMasterBeatenToList(c, &f);\n\treturn IncreaseScriptPointerBy1();",
	"case_ids": ["ScriptCommand_RecordMasterWin-0", "ScriptCommand_RecordMasterWin-1", "ScriptCommand_RecordMasterWin-2", "ScriptCommand_RecordMasterWin-3", "ScriptCommand_RecordMasterWin-4"],
}
# <<< factory-mutation ScriptCommand_RecordMasterWin
# >>> factory-mutation ScriptCommand_ChallengeMachine
MUTATIONS["ScriptCommand_ChallengeMachine"] = {
	"source_symbol": "ScriptCommand_ChallengeMachine",
	"before": "\twOverworldTransition |= 0x40u;",
	"after": "\twOverworldTransition = 0x40u;",
	"case_ids": ["ScriptCommand_ChallengeMachine-1", "ScriptCommand_ChallengeMachine-2", "ScriptCommand_ChallengeMachine-3"],
}
# <<< factory-mutation ScriptCommand_ChallengeMachine
# >>> factory-mutation ScriptCommand_PlaySong
MUTATIONS["ScriptCommand_PlaySong"] = {
    "source_symbol": "ScriptCommand_PlaySong",
    "before": "\tScriptPlaySong(c);\n\treturn IncreaseScriptPointerBy2();",
    "after": "\tScriptPlaySong(c);\n\treturn IncreaseScriptPointerBy1();",
    "case_ids": ["ScriptCommand_PlaySong-0", "ScriptCommand_PlaySong-1", "ScriptCommand_PlaySong-2", "ScriptCommand_PlaySong-3"],
}
# <<< factory-mutation ScriptCommand_PlaySong
# >>> factory-mutation ScriptCommand_PlaySFX
MUTATIONS["ScriptCommand_PlaySFX"] = {
    "source_symbol": "ScriptCommand_PlaySFX",
    "before": "\tPlaySFX(c);\n\treturn IncreaseScriptPointerBy2();",
    "after": "\tPlaySFX(c);\n\treturn IncreaseScriptPointerBy1();",
    "case_ids": ["ScriptCommand_PlaySFX-0", "ScriptCommand_PlaySFX-1", "ScriptCommand_PlaySFX-2", "ScriptCommand_PlaySFX-3"],
}
# <<< factory-mutation ScriptCommand_PlaySFX
# >>> factory-mutation ScriptCommand_PlayDefaultSong
MUTATIONS["ScriptCommand_PlayDefaultSong"] = {
    "source_symbol": "ScriptCommand_PlayDefaultSong",
    "before": "\tPlayDefaultSong();\n\treturn IncreaseScriptPointerBy1();",
    "after": "\tPlayDefaultSong();\n\treturn IncreaseScriptPointerBy2();",
    "case_ids": ["ScriptCommand_PlayDefaultSong-0", "ScriptCommand_PlayDefaultSong-1"],
}
# <<< factory-mutation ScriptCommand_PlayDefaultSong
# >>> factory-mutation ScriptCommand_SetSpriteAttributes
MUTATIONS["ScriptCommand_SetSpriteAttributes"] = {
	"source_symbol": "ScriptCommand_SetSpriteAttributes",
	"before": "if (wConsole == CONSOLE_CGB)",
	"after": "if (wConsole != CONSOLE_CGB)",
	"case_ids": ["ScriptCommand_SetSpriteAttributes-1", "ScriptCommand_SetSpriteAttributes-2", "ScriptCommand_SetSpriteAttributes-3"],
}
# <<< factory-mutation ScriptCommand_SetSpriteAttributes
# >>> factory-mutation ScriptCommand_DoFrames
MUTATIONS["ScriptCommand_DoFrames"] = {
	"source_symbol": "ScriptCommand_DoFrames",
	"before": "\t\tDoFrameIfLCDEnabled();\n\treturn IncreaseScriptPointerBy2();",
	"after": "\t\tDoFrameIfLCDEnabled();\n\treturn IncreaseScriptPointerBy3();",
	"case_ids": ["ScriptCommand_DoFrames-0", "ScriptCommand_DoFrames-1", "ScriptCommand_DoFrames-2", "ScriptCommand_DoFrames-3"],
}
# <<< factory-mutation ScriptCommand_DoFrames
# >>> factory-mutation ScriptCommand_EndScript
MUTATIONS["ScriptCommand_EndScript"] = {
	"source_symbol": "ScriptCommand_EndScript",
	"before": "\twBreakScriptLoop = TRUE;",
	"after": "\twBreakScriptLoop = 0x00u;",
	"case_ids": ["ScriptCommand_EndScript-2", "ScriptCommand_EndScript-3", "ScriptCommand_EndScript-4"],
}
# <<< factory-mutation ScriptCommand_EndScript
# >>> factory-mutation SetNPCDuelParams
MUTATIONS["SetNPCDuelParams"] = {
	"source_symbol": "SetNPCDuelParams",
	"before": "\twNPCDuelDeckID = b;",
	"after": "\twNPCDuelDeckID = c;",
	"case_ids": ["SetNPCDuelParams-2", "SetNPCDuelParams-4", "SetNPCDuelParams-5"],
}
# <<< factory-mutation SetNPCDuelParams
# >>> factory-mutation ScriptCommand_BattleCenter
MUTATIONS["ScriptCommand_BattleCenter"] = {
	"source_symbol": "ScriptCommand_BattleCenter",
	"before": "wGameEvent = GAME_EVENT_BATTLE_CENTER;",
	"after": "wGameEvent = 0x03u;",
	"case_ids": ["ScriptCommand_BattleCenter-0", "ScriptCommand_BattleCenter-1", "ScriptCommand_BattleCenter-2", "ScriptCommand_BattleCenter-3", "ScriptCommand_BattleCenter-4"],
}
# <<< factory-mutation ScriptCommand_BattleCenter
# >>> factory-mutation ScriptCommand_LoadCurrentMapNameIntoTxRamSlot
MUTATIONS["ScriptCommand_LoadCurrentMapNameIntoTxRamSlot"] = {"source_symbol": "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot", "before": "\treturn (ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult){r.a, r.f, 0x00u, r.c};", "after": "\treturn (ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult){r.a, r.f, 0x01u, r.c};", "case_ids": ["ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-0", "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-1", "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-2", "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-3", "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-4", "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-5", "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot-6"]}
# <<< factory-mutation ScriptCommand_LoadCurrentMapNameIntoTxRamSlot
# >>> factory-mutation ScriptCommand_EnterMap
MUTATIONS["ScriptCommand_EnterMap"] = {"source_symbol": "ScriptCommand_EnterMap", "before": "\twOverworldTransition |= 0x10u;", "after": "\twOverworldTransition |= 0x20u;", "case_ids": ["ScriptCommand_EnterMap-1", "ScriptCommand_EnterMap-2", "ScriptCommand_EnterMap-3", "ScriptCommand_EnterMap-4"]}
# <<< factory-mutation ScriptCommand_EnterMap
# >>> factory-mutation GetScriptArgs1AfterPointer
MUTATIONS["GetScriptArgs1AfterPointer"] = {"source_symbol": "GetScriptArgs1AfterPointer", "before": "GetScriptArgsAfterPointerResult r = GetScriptArgsAfterPointer(1u);\n\treturn r;", "after": "GetScriptArgsAfterPointerResult r = GetScriptArgsAfterPointer(1u);\n\tr.a = (uint8_t)(r.a ^ 1u);\n\treturn r;", "case_ids": ["GetScriptArgs1AfterPointer-0", "GetScriptArgs1AfterPointer-1", "GetScriptArgs1AfterPointer-2"]}
# <<< factory-mutation GetScriptArgs1AfterPointer
# >>> factory-mutation SetNextScript
MUTATIONS["SetNextScript"] = {"source_symbol": "SetNextScript", "before": "wNextScript_PTR[1] = (uint8_t)(bc >> 8);", "after": "wNextScript_PTR[1] = (uint8_t)(bc >> 8) + 1u;", "case_ids": ["SetNextScript-0", "SetNextScript-1", "SetNextScript-2"]}
# <<< factory-mutation SetNextScript
# >>> factory-mutation SetEventValue
MUTATIONS["SetEventValue"] = {
    "source_symbol": "SetEventValue",
    "before": "\tuint8_t value = c;",
    "after": "\tuint8_t value = (uint8_t)(c ^ 1u);",
    "case_ids": ["SetEventValue-0", "SetEventValue-1", "SetEventValue-2", "SetEventValue-3", "SetEventValue-4"],
}
# <<< factory-mutation SetEventValue
# >>> factory-mutation MaxOutEventValue
MUTATIONS["MaxOutEventValue"] = {
    "source_symbol": "MaxOutEventValue",
    "before": "\treturn SetEventValue(a, f, b, 0xffu);",
    "after": "\treturn SetEventValue(a, f, b, 0xfeu);",
    "case_ids": ["MaxOutEventValue-0", "MaxOutEventValue-1", "MaxOutEventValue-2", "MaxOutEventValue-3", "MaxOutEventValue-4"],
}
# <<< factory-mutation MaxOutEventValue
# >>> factory-mutation ZeroOutEventValue
MUTATIONS["ZeroOutEventValue"] = {
    "source_symbol": "ZeroOutEventValue",
    "before": "\treturn SetEventValue(a, f, b, 0u);",
    "after": "\treturn SetEventValue(a, f, b, 1u);",
    "case_ids": ["ZeroOutEventValue-0", "ZeroOutEventValue-1", "ZeroOutEventValue-2", "ZeroOutEventValue-3", "ZeroOutEventValue-4"],
}
# <<< factory-mutation ZeroOutEventValue
# >>> factory-mutation ClearEvents
MUTATIONS["ClearEvents"] = {
    "source_symbol": "ClearEvents",
    "before": "\tfor (uint16_t i = 0; i < EVENT_VAR_BYTES; ++i) {",
    "after": "\tfor (uint16_t i = 0; i < EVENT_VAR_BYTES - 1u; ++i) {",
    "case_ids": ["ClearEvents-0", "ClearEvents-1", "ClearEvents-2"],
}
# <<< factory-mutation ClearEvents
# >>> factory-mutation ScriptCommand_Jump
MUTATIONS["ScriptCommand_Jump"] = {
    "source_symbol": "ScriptCommand_Jump",
    "before": "\tuint16_t target = (uint16_t)(((uint16_t)args.b << 8) | args.c);",
    "after": "\tuint16_t target = (uint16_t)((((uint16_t)args.b << 8) | args.c) + 1u);",
    "case_ids": ["ScriptCommand_Jump-1", "ScriptCommand_Jump-2", "ScriptCommand_Jump-3"],
}
# <<< factory-mutation ScriptCommand_Jump
# >>> factory-mutation ScriptCommand_MaxOutEventValue
MUTATIONS["ScriptCommand_MaxOutEventValue"] = {
    "source_symbol": "ScriptCommand_MaxOutEventValue",
    "before": "\t(void)MaxOutEventValue(c, f, b, c);",
    "after": "\t(void)MaxOutEventValue((uint8_t)(c + 1u), f, b, c);",
    "case_ids": ["ScriptCommand_MaxOutEventValue-0", "ScriptCommand_MaxOutEventValue-1", "ScriptCommand_MaxOutEventValue-2", "ScriptCommand_MaxOutEventValue-3", "ScriptCommand_MaxOutEventValue-4"],
}
# <<< factory-mutation ScriptCommand_MaxOutEventValue
# >>> factory-mutation ScriptCommand_ZeroOutEventValue
MUTATIONS["ScriptCommand_ZeroOutEventValue"] = {
    "source_symbol": "ScriptCommand_ZeroOutEventValue",
    "before": "\t(void)ZeroOutEventValue(c, f, b, c);",
    "after": "\t(void)ZeroOutEventValue((uint8_t)(c + 1u), f, b, c);",
    "case_ids": ["ScriptCommand_ZeroOutEventValue-0", "ScriptCommand_ZeroOutEventValue-1", "ScriptCommand_ZeroOutEventValue-2", "ScriptCommand_ZeroOutEventValue-3", "ScriptCommand_ZeroOutEventValue-4"],
}
# <<< factory-mutation ScriptCommand_ZeroOutEventValue
# >>> factory-mutation ScriptCommand_SetEventValue
MUTATIONS["ScriptCommand_SetEventValue"] = {
    "source_symbol": "ScriptCommand_SetEventValue",
    "before": "\t(void)SetEventValue(c, f, b, c);",
    "after": "\t(void)SetEventValue((uint8_t)(c + 1u), f, b, c);",
    "case_ids": ["ScriptCommand_SetEventValue-0", "ScriptCommand_SetEventValue-1", "ScriptCommand_SetEventValue-2", "ScriptCommand_SetEventValue-3", "ScriptCommand_SetEventValue-4"],
}
# <<< factory-mutation ScriptCommand_SetEventValue
# >>> factory-mutation ScriptCommand_TryGivePCPack
MUTATIONS["ScriptCommand_TryGivePCPack"] = {"source_symbol": "ScriptCommand_TryGivePCPack", "before": "\tTryGivePCPack(c);", "after": "\tTryGivePCPack((uint8_t)(c + 1u));", "case_ids": ["ScriptCommand_TryGivePCPack-0", "ScriptCommand_TryGivePCPack-1", "ScriptCommand_TryGivePCPack-2", "ScriptCommand_TryGivePCPack-4"]}
# <<< factory-mutation ScriptCommand_TryGivePCPack
# >>> factory-mutation ScriptCommand_SetActiveNPCCoords
MUTATIONS["ScriptCommand_SetActiveNPCCoords"] = {
    "source_symbol": "ScriptCommand_SetActiveNPCCoords",
    "before": "\t(void)SetNPCPosition(c, b);",
    "after": "\t(void)SetNPCPosition(b, c);",
    "case_ids": ["ScriptCommand_SetActiveNPCCoords-0", "ScriptCommand_SetActiveNPCCoords-1", "ScriptCommand_SetActiveNPCCoords-2", "ScriptCommand_SetActiveNPCCoords-3"],
}
# <<< factory-mutation ScriptCommand_SetActiveNPCCoords
