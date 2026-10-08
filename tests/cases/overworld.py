from tests.cases._symbols import data, sym, sym_bank, sym_pointer
from tests.cases._fixtures import after_duel_fixture, AFTER_DUEL_REGS, move_step_fixture as _move_step_fixture, MOVE_STEP_REGS as _MOVE_STEP_REGS
from tests.cases._fixtures import (FIND_NPC_REGS, MAP_SCRIPT_REGS, find_npc_fixture)
"""Oracle-diff cases for poketcg/src/engine/overworld/overworld.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Func_c6cc
wPlayerXCoordPixels = sym("wPlayerXCoordPixels")
wPlayerYCoordPixels = sym("wPlayerYCoordPixels")
wPlayerSpriteIndex = sym("wPlayerSpriteIndex")
wWhichSprite = sym("wWhichSprite")
wSpriteAnimScratch = sym("wSprite1Enabled")
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
    {"wram": {sym("wOverworldNPCFlags"): b"\x00"}},
    dict(POISON, a=0x0F, wram={sym("wOverworldNPCFlags"): b"\xF0"}),
    {"a": 0x00, "wram": {sym("wOverworldNPCFlags"): b"\x80"}},
]
# <<< factory SetOverworldNPCFlags

# >>> factory Func_c158
CONTRACT["Func_c158"] = {"compare": ("a",), "preserve": ()}
CASES["Func_c158"] = [
	{},  # all-zero: wActiveGameEvent=0 -> cp/r nz early return
	{"wram": {sym("wActiveGameEvent"): b"\x01", sym("wTempNPC"): b"\x00", sym("wNPCDuelist"): b"\x42", sym("wNPCDuelistDirection"): b"\x0c", sym("wLoadedNPCTempIndex"): b"\x01"},
	 "read": {sym("wActiveGameEvent"): 1, sym("wNPCDuelist"): 1}},  # duel event: wTempNPC <- wNPCDuelist before FindLoadedNPC
	{"wram": {sym("wActiveGameEvent"): b"\x02", sym("wTempNPC"): b"\x77"}, "read": {sym("wActiveGameEvent"): 1}},  # not duel -> early return, wTempNPC untouched
	dict(POISON, wram={sym("wActiveGameEvent"): b"\x01", sym("wTempNPC"): b"\x33", sym("wNPCDuelist"): b"\x21", sym("wNPCDuelistDirection"): b"\x06"},
	     read={sym("wActiveGameEvent"): 1, sym("wNPCDuelist"): 1}),
]
# <<< factory Func_c158

# >>> factory Func_c184
CONTRACT["Func_c184"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c184"] = [
	{},  # all-zero: wCurMap=0 -> OWMODE_MAP written to both mode bytes
	{"wram": {sym("wOverworldMode"): b"\x5a", sym("wOverworldModeBackup"): b"\xa5"}, "read": {sym("wCurMap"): 1}},  # wCurMap=0 overwrites both with 00
	{"wram": {sym("wCurMap"): b"\x01", sym("wOverworldMode"): b"\x00", sym("wOverworldModeBackup"): b"\x00"}, "read": {sym("wCurMap"): 1}},  # first nonzero map id
	{"wram": {sym("wCurMap"): b"\xff", sym("wOverworldMode"): b"\x00", sym("wOverworldModeBackup"): b"\x00"}, "read": {sym("wCurMap"): 1}},
	dict(POISON, wram={sym("wCurMap"): b"\x02", sym("wOverworldMode"): b"\x00", sym("wOverworldModeBackup"): b"\x00"}, read={sym("wCurMap"): 1}),
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
        sym("wSelectedPauseMenuItem"): b"\x00",
        sym("wSelectedPCMenuItem"): b"\x00",
        sym("wSelectedGiftCenterMenuItem"): b"\x00",
        sym("wConfigCursorYPos"): b"\x00",
        sym("wActiveGameEvent"): b"\x00",
        sym("wDefaultSong"): b"\x00",
        sym("wSongOverride"): b"\x00",
        sym("wRonaldIsInMap"): b"\x00",
        sym("wAnimationsDisabled"): b"\x00",
        sym("wTextSpeed"): b"\x00",
    },
     "sram": {0: {sym("sAnimationsDisabled"): b"\x00", sym("sTextSpeed"): b"\x00"}}},
    dict(POISON,
         wram={
             sym("wSelectedPauseMenuItem"): b"\x11",
             sym("wSelectedPCMenuItem"): b"\x22",
             sym("wSelectedGiftCenterMenuItem"): b"\x33",
             sym("wConfigCursorYPos"): b"\x44",
             sym("wActiveGameEvent"): b"\x55",
             sym("wDefaultSong"): b"\x66",
             sym("wSongOverride"): b"\x77",
             sym("wRonaldIsInMap"): b"\x88",
             sym("wAnimationsDisabled"): b"\x99",
             sym("wTextSpeed"): b"\xAA",
         },
         sram={0: {sym("sAnimationsDisabled"): b"\x01", sym("sTextSpeed"): b"\x02"}}),
    {"ramg": False,
     "wram": {
         sym("wSelectedPauseMenuItem"): b"\xFF",
         sym("wSelectedPCMenuItem"): b"\xFE",
         sym("wSelectedGiftCenterMenuItem"): b"\xFD",
         sym("wConfigCursorYPos"): b"\xFC",
         sym("wActiveGameEvent"): b"\xFB",
         sym("wDefaultSong"): b"\xFA",
         sym("wSongOverride"): b"\xF9",
         sym("wRonaldIsInMap"): b"\xF8",
         sym("wAnimationsDisabled"): b"\xF7",
         sym("wTextSpeed"): b"\xF6",
     },
     "sram": {0: {sym("sAnimationsDisabled"): b"\xA5", sym("sTextSpeed"): b"\x5A"}}},
]
# <<< factory Func_c1f8

# >>> factory BackupPlayerPosition
CONTRACT["BackupPlayerPosition"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["BackupPlayerPosition"] = [
    {"wram": {sym("wCurMap"): b"\x00", sym("wPlayerXCoord"): b"\x00", sym("wPlayerYCoord"): b"\x00", sym("wPlayerDirection"): b"\x00",
              sym("wTempMap"): b"\x00", sym("wTempPlayerXCoord"): b"\x00", sym("wTempPlayerYCoord"): b"\x00", sym("wTempPlayerDirection"): b"\x00"}},
    dict(POISON,
         wram={sym("wCurMap"): b"\x12", sym("wPlayerXCoord"): b"\x34", sym("wPlayerYCoord"): b"\x56", sym("wPlayerDirection"): b"\x78",
               sym("wTempMap"): b"\xA1", sym("wTempPlayerXCoord"): b"\xA2", sym("wTempPlayerYCoord"): b"\xA3", sym("wTempPlayerDirection"): b"\xA4"}),
    {"wram": {sym("wCurMap"): b"\xFF", sym("wPlayerXCoord"): b"\x80", sym("wPlayerYCoord"): b"\x01", sym("wPlayerDirection"): b"\xFE",
              sym("wTempMap"): b"\x00", sym("wTempPlayerXCoord"): b"\x00", sym("wTempPlayerYCoord"): b"\x00", sym("wTempPlayerDirection"): b"\x00"}},
]
# <<< factory BackupPlayerPosition

# >>> factory Func_c469
CONTRACT["Func_c469"] = {"compare": (), "preserve": ()}
CASES["Func_c469"] = [
    {"wram": {sym("wSCXBuffer"): b"\x00", sym("wSCYBuffer"): b"\x00"}, "read": {sym("wd233"): 1, sym("wd234"): 1}},
    {"wram": {sym("wSCXBuffer"): b"\x01", sym("wSCYBuffer"): b"\x01"}, "read": {sym("wd233"): 1, sym("wd234"): 1}},
    dict(POISON, wram={sym("wSCXBuffer"): b"\xAA", sym("wSCYBuffer"): b"\x55"}, read={sym("wd233"): 1, sym("wd234"): 1}),
]
# <<< factory Func_c469



# >>> factory SetScreenScroll
CONTRACT["SetScreenScroll"] = {"compare": (), "preserve": ()}
CASES["SetScreenScroll"] = [
    {"wram": {sym("wSCX"): b"\x00", sym("wSCY"): b"\x00"}, "read": {sym("hSCX"): 1, sym("hSCY"): 1}},
    {"wram": {sym("wSCX"): b"\x01", sym("wSCY"): b"\x02"}, "read": {sym("hSCX"): 1, sym("hSCY"): 1}},
    dict(POISON, wram={sym("wSCX"): b"\xAA", sym("wSCY"): b"\x55"}, read={sym("hSCX"): 1, sym("hSCY"): 1}),
]
# <<< factory SetScreenScroll




# >>> factory SetScreenScrollWram
CONTRACT["SetScreenScrollWram"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["SetScreenScrollWram"] = [
	{"wram": {sym("wSCXBuffer"): b"\x12", sym("wSCYBuffer"): b"\x34", sym("wSCX"): b"\xAA", sym("wSCY"): b"\xBB"}},
	dict(POISON, wram={sym("wSCXBuffer"): b"\x56", sym("wSCYBuffer"): b"\x78", sym("wSCX"): b"\xCC", sym("wSCY"): b"\xDD"}),
]
# <<< factory SetScreenScrollWram


# >>> factory Func_c70d
CONTRACT["Func_c70d"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c70d"] = [
    {"wram": {sym("wCurMap"): b"\x00", sym("wTempMap"): b"\x00", sym("wOverworldTransition"): b"\x00"}, "read": {sym("wCurMap"): 1, sym("wTempMap"): 1}},
    {"wram": {sym("wCurMap"): b"\x01", sym("wTempMap"): b"\x00", sym("wOverworldTransition"): b"\x00"}, "read": {sym("wCurMap"): 1, sym("wTempMap"): 1}},
    dict(POISON, wram={sym("wCurMap"): b"\x00", sym("wTempMap"): b"\x01", sym("wOverworldTransition"): b"\x00"}, read={sym("wCurMap"): 1, sym("wTempMap"): 1}),
]
# <<< factory Func_c70d

# >>> factory Func_c430
CONTRACT["Func_c430"] = {"compare": (), "preserve": ()}
CASES["Func_c430"] = [
    {"wram": {sym("wSCXBuffer"): b"\x50", sym("wSCYBuffer"): b"\x40", sym("wd237"): b"\x04", sym("wd238"): b"\x03"},
     "read": {sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1}},
    {"wram": {sym("wSCXBuffer"): b"\x20", sym("wSCYBuffer"): b"\x20", sym("wd237"): b"\x08", sym("wd238"): b"\x08"},
     "read": {sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1}},
    {"wram": {sym("wSCXBuffer"): b"\xB1", sym("wSCYBuffer"): b"\xB9", sym("wd237"): b"\x01", sym("wd238"): b"\x01"},
     "read": {sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1}},
    dict(POISON, wram={sym("wSCXBuffer"): b"\x80", sym("wSCYBuffer"): b"\x90", sym("wd237"): b"\x10", sym("wd238"): b"\x02"},
         read={sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1}),
]
# <<< factory Func_c430

# >>> factory-cases-statics
wSCXBuffer = sym("wSCXBuffer")
wSCYBuffer = sym("wSCYBuffer")
wd237 = sym("wd237")
wd238 = sym("wd238")

wPermissionMap = sym("wPermissionMap")

wPlayerXCoord = sym("wPlayerXCoord")
wPlayerYCoord = sym("wPlayerYCoord")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wOBP0 = sym("wOBP0")
wOBP0Backup = sym("wOBP0Backup")
wOBP1 = sym("wOBP1")
wOBP1Backup = sym("wOBP1Backup")
wObjectPalettesCGB = sym("wObjectPalettesCGB")
wObjectPalettesCGBBackup = sym("wObjectPalettesCGBBackup")

wPlayerCurrentlyMoving = sym("wPlayerCurrentlyMoving")
wPlayerXCoord = sym("wPlayerXCoord")
wPlayerYCoord = sym("wPlayerYCoord")
wd338 = sym("wd338")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPlayerDirection = sym("wPlayerDirection")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPlayerXCoord = sym("wPlayerXCoord")
wPlayerYCoord = sym("wPlayerYCoord")
wPlayerDirection = sym("wPlayerDirection")
wPlayerCurrentlyMoving = sym("wPlayerCurrentlyMoving")
wd338 = sym("wd338")
wWhichSprite = sym("wWhichSprite")
wSpriteAnimBuffer = sym("wSpriteAnimBuffer")
wPermissionMap = sym("wPermissionMap")

wd339 = sym("wd339")
wd33a = sym("wd33a")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wOWMapEvents = sym("wOWMapEvents")
wCurMap = sym("wCurMap")

hSCX = sym("hSCX")
hSCY = sym("hSCY")

wPlayerXCoord = sym("wPlayerXCoord")
wPlayerYCoord = sym("wPlayerYCoord")
wPlayerXCoordPixels = sym("wPlayerXCoordPixels")
wPlayerYCoordPixels = sym("wPlayerYCoordPixels")

wPlayerDirection = sym("wPlayerDirection")
wPlayerSpriteIndex = sym("wPlayerSpriteIndex")
wPlayerSpriteBaseAnimation = sym("wPlayerSpriteBaseAnimation")
wWhichSprite = sym("wWhichSprite")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDoFrameFunction = sym("wDoFrameFunction")

wBGMapBank = sym("wBGMapBank")
wBGMapHeight = sym("wBGMapHeight")
wBGMapPermissionDataPtr = sym("wBGMapPermissionDataPtr")
wBGMapWidth = sym("wBGMapWidth")
wDecompressionSecondaryBuffer = sym("wDecompressionSecondaryBuffer")

wBGMapPermissionDataPtr = sym("wBGMapPermissionDataPtr")
wPermissionMap = sym("wPermissionMap")

hBankROM = sym("hBankROM")

wOverworldMapSelection_A = sym("wOverworldMapSelection")
wTempMap_A = sym("wTempMap")
wTempPlayerXCoord_A = sym("wTempPlayerXCoord")
wTempPlayerYCoord_A = sym("wTempPlayerYCoord")
wTempPlayerDirection_A = sym("wTempPlayerDirection")
wPlayTimeCounter_A = sym("wPlayTimeCounter")
wOWMapEvents_A = sym("wOWMapEvents")
wMastersBeatenList_A = sym("wMastersBeatenList")
hBankROM_A = sym("hBankROM")

wCurMap_A = sym("wCurMap")
wPlayerSpriteIndex_A = sym("wPlayerSpriteIndex")
wWhichSprite_A = sym("wWhichSprite")
wPlayerXCoordPixels_A = sym("wPlayerXCoordPixels")
wPlayerYCoordPixels_A = sym("wPlayerYCoordPixels")
wSCXBuffer_A = sym("wSCXBuffer")
wSCYBuffer_A = sym("wSCYBuffer")

wVBlankOAMCopyToggle = sym("wVBlankOAMCopyToggle")

hCurMenuItem = sym("hCurMenuItem")
wCurMenuItem = sym("wCurMenuItem")
wSelectedPauseMenuItem = sym("wSelectedPauseMenuItem")

def menu_state(default_yes=0):
    return {sym("wLCDC"): b"\x00", sym("wCursorBlinkCounter"): b"\x05", sym("wCurMenuItem"): b"\x01", sym("wMenuCursorXOffset"): b"\x02", sym("wMenuCursorYOffset"): b"\x00", sym("wNumMenuItems"): b"\x02", sym("wLeftmostItemCursorX"): b"\x02", sym("wDefaultYesOrNo"): bytes([default_yes]), sym("wBoosterViableCardList"): b"\x00" * 0x100}

SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
wMedalScreenYOffset = sym("wMedalScreenYOffset")

wOverworldNPCFlags = sym("wOverworldNPCFlags")

wd3b9 = sym("wd3b9")

# overworld.asm:1264 (PCMenu_ReadMail). This is a bare farcall wrapper around
# the already-ported _PCMenu_ReadMail, so it inherits that routine's measured
# case shape from tests/cases/mail.py: FlashWhiteScreen calls EnableLCD, so the
# menu loop always lets real frames elapse (CopyDMAFunction has to be installed
# because InitMenuScreen sets wVBlankOAMCopyToggle), and B has to arrive as an
# edge on hKeysPressed rather than being held from the first instruction.
wd291 = sym("wd291")
hKeysPressed = sym("hKeysPressed")
hDPadHeld = sym("hDPadHeld")
wLCDC = sym("wLCDC")
wPCPackSelection = sym("wPCPackSelection")
wPCPacks = sym("wPCPacks")
READ_MAIL_KEYS = [0x00, 0x02]
# A menu screen load plus the mail screen's frame loop.
READ_MAIL_INSTRUCTIONS = 60000000
READ_MAIL_CYCLES = 240000000

PAUSE_CARD_SRAM = {0: {sym("sCardAndDeckSaveData"): b"\x00" * 0xFF, sym("sDeck1Cards"): b"\x00", sym("sDeck2Cards"): b"\x00", sym("sDeck3Cards"): b"\x00", sym("sDeck4Cards"): b"\x00", sym("sPlayerName"): bytes([0x81, 0x82, 0x00] + [0] * 13)}}

wNextScript = sym("wNextScript")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wScriptNPC = sym("wScriptNPC")
wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
wOverworldMode = sym("wOverworldMode")
wNextScript = sym("wNextScript")
wPlayerDirection = sym("wPlayerDirection")
wOverworldNPCFlags = sym("wOverworldNPCFlags")
LOADED_NPCS = sym("wLoadedNPC1ID")

hKeysPressed = sym("hKeysPressed")
wPlayerCurrentlyMoving = sym("wPlayerCurrentlyMoving")
wPlayerSpriteIndex = sym("wPlayerSpriteIndex")
wWhichSprite = sym("wWhichSprite")
# <<< factory-cases-statics

# >>> factory Func_c41c
CONTRACT["Func_c41c"] = {"compare": (), "preserve": ()}
CASES["Func_c41c"] = [
	{"wram": {sym("wPlayerXCoordPixels"): b"\x40", sym("wPlayerYCoordPixels"): b"\x40", wd237: b"\x00", wd238: b"\x00"}, "read": {wSCXBuffer: 1, wSCYBuffer: 1}},
	{"wram": {sym("wPlayerXCoordPixels"): b"\x90", sym("wPlayerYCoordPixels"): b"\xA0", wd237: b"\x10", wd238: b"\x10"}, "read": {wSCXBuffer: 1, wSCYBuffer: 1}},
	{"wram": {sym("wPlayerXCoordPixels"): b"\x00", sym("wPlayerYCoordPixels"): b"\x01", wd237: b"\x10", wd238: b"\x04"}, "read": {wSCXBuffer: 1, wSCYBuffer: 1}},
	dict(POISON, wram={sym("wPlayerXCoordPixels"): b"\xAA", sym("wPlayerYCoordPixels"): b"\x55", wd237: b"\x10", wd238: b"\x04"}, read={wSCXBuffer: 1, wSCYBuffer: 1}),
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
    {"a": 0x00, "c": 0x01, "wram": {sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x01", sym("wd338"): b"\x10", sym("wd237"): b"\x00", sym("wd238"): b"\x00"}, "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wLoadedNPC8CoordX"): 1, sym("wLoadedNPC8CoordY"): 1}},
    {"a": 0x01, "c": 0x03, "wram": {sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x00", sym("wd338"): b"\x03", sym("wd237"): b"\x02", sym("wd238"): b"\x03"}, "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1}},
    {"a": 0x03, "c": 0x02, "wram": {sym("wPlayerXCoordPixels"): b"\x80", sym("wPlayerYCoordPixels"): b"\x80", sym("wPlayerCurrentlyMoving"): b"\x04", sym("wd338"): b"\x01", sym("wd237"): b"\x10", sym("wd238"): b"\x10"}, "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1}},
    dict(POISON, a=0x02, c=0x01, wram={sym("wPlayerXCoordPixels"): b"\x40", sym("wPlayerYCoordPixels"): b"\x40", sym("wPlayerCurrentlyMoving"): b"\x00", sym("wd338"): b"\x01", sym("wd237"): b"\x00", sym("wd238"): b"\x00"}, read={sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1}),
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

# >>> factory BackupObjectPalettes
CONTRACT["BackupObjectPalettes"] = {"compare": (), "preserve": ()}
CASES["BackupObjectPalettes"] = [
	{"wram": {wOBP0: b"\x12", wOBP1: b"\x34", wObjectPalettesCGB: bytes(range(64))}, "read": {wOBP0Backup: 1, wOBP1Backup: 1, wObjectPalettesCGBBackup: 64}},
	dict(POISON, wram={wOBP0: b"\xAA", wOBP1: b"\x55", wObjectPalettesCGB: bytes([0xA5] * 64)}, read={wOBP0Backup: 1, wOBP1Backup: 1, wObjectPalettesCGBBackup: 64}),
	{"wram": {wOBP0: b"\x00", wOBP1: b"\xFF", wObjectPalettesCGB: b"\x00" * 64}, "read": {wOBP0Backup: 1, wOBP1Backup: 1, wObjectPalettesCGBBackup: 64}},
]
# <<< factory BackupObjectPalettes

# >>> factory AttemptPlayerMovement
CONTRACT["AttemptPlayerMovement"] = {"compare": (), "preserve": ()}
CASES["AttemptPlayerMovement"] = [
    {"b": 0x1F, "c": 0x00, "wram": {wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34", wPlayerCurrentlyMoving: b"\x00", wd338: b"\x56"}, "expect": {wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34", wPlayerCurrentlyMoving: b"\x00", wd338: b"\x56"}},
    dict(POISON, b=0x00, c=0x1F, wram={wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56"}, expect={wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56"}),
]
# <<< factory AttemptPlayerMovement

# >>> factory FindPlayerMovementFromDirection
CONTRACT["FindPlayerMovementFromDirection"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["FindPlayerMovementFromDirection"] = [
    {"wram": {wPlayerDirection: b"\x00", sym("wPlayerXCoord"): b"\x10", sym("wPlayerYCoord"): b"\x20"}},
    {"wram": {wPlayerDirection: b"\x01", sym("wPlayerXCoord"): b"\x10", sym("wPlayerYCoord"): b"\x20"}},
    {"wram": {wPlayerDirection: b"\x02", sym("wPlayerXCoord"): b"\x10", sym("wPlayerYCoord"): b"\x20"}},
    {"wram": {wPlayerDirection: b"\x03", sym("wPlayerXCoord"): b"\x10", sym("wPlayerYCoord"): b"\x20"}},
    dict(POISON, wram={wPlayerDirection: b"\x01", sym("wPlayerXCoord"): b"\xF0", sym("wPlayerYCoord"): b"\x01"}),
]
# <<< factory FindPlayerMovementFromDirection

# >>> factory Func_c1a0
CONTRACT["Func_c1a0"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e")}
CASES["Func_c1a0"] = [
    {"hl": 0x5678, "read": {sym("wDoFrameFunction"): 2}},
    dict(POISON, read={sym("wDoFrameFunction"): 2}),
]
# <<< factory Func_c1a0

# >>> factory PauseMenu_Exit
CONTRACT["PauseMenu_Exit"] = {"compare": (), "preserve": ()}
CASES["PauseMenu_Exit"] = [
    {"read": {sym("wOverworldMode"): 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "read": {sym("wOverworldMode"): 1}},
]
# <<< factory PauseMenu_Exit

# >>> factory AttemptPlayerMovementFromDirection
CONTRACT["AttemptPlayerMovementFromDirection"] = {"compare": (), "preserve": ()}
CASES["AttemptPlayerMovementFromDirection"] = [
    {"wram": {wPlayerXCoord: b"\x1e", wPlayerYCoord: b"\x10", wPlayerDirection: b"\x02", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56"}, "expect": {wPlayerXCoord: b"\x1e", wPlayerYCoord: b"\x10", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56"}},
    dict(POISON, wram={wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x10", wPlayerDirection: b"\x00", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56", wWhichSprite: b"\x00", wSpriteAnimBuffer + 0x0E: b"\x00", wSpriteAnimBuffer + 0x0F: b"\x01", wPermissionMap + 0x88: b"\x00"}, expect={wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x10", wPlayerCurrentlyMoving: b"\x81", wd338: b"\x10", wSpriteAnimBuffer + 0x0E: b"\x04", wSpriteAnimBuffer + 0x0F: b"\x03"}),
]
# <<< factory AttemptPlayerMovementFromDirection

# >>> factory Func_c687
CONTRACT["Func_c687"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c687"] = [
    {"b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x4567, "wram": {wd339: b"\x00", wd33a: b"\x01", sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x01", sym("wd338"): b"\x10", sym("wd237"): b"\x00", sym("wd238"): b"\x00"}, "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wLoadedNPC8CoordX"): 1, sym("wLoadedNPC8CoordY"): 1}},
    {"b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x4567, "wram": {wd339: b"\x01", wd33a: b"\x03", sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x00", sym("wd338"): b"\x03", sym("wd237"): b"\x02", sym("wd238"): b"\x03"}, "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1}},
    {"b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x4567, "wram": {wd339: b"\x03", wd33a: b"\x02", sym("wPlayerXCoordPixels"): b"\x80", sym("wPlayerYCoordPixels"): b"\x80", sym("wPlayerCurrentlyMoving"): b"\x04", sym("wd338"): b"\x01", sym("wd237"): b"\x10", sym("wd238"): b"\x10"}, "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1}},
    dict(POISON, wram={wd339: b"\x02", wd33a: b"\x01", sym("wPlayerXCoordPixels"): b"\x40", sym("wPlayerYCoordPixels"): b"\x40", sym("wPlayerCurrentlyMoving"): b"\x00", sym("wd338"): b"\x01", sym("wd237"): b"\x00", sym("wd238"): b"\x00"}, read={sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1}),
]
# <<< factory Func_c687

# >>> factory Func_c36a
CONTRACT["Func_c36a"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c36a"] = [
	{"wram": {wOWMapEvents: b"\x12\x34", wCurMap: b"\x00"}, "read": {wOWMapEvents: 2}},
	{"wram": {wOWMapEvents: b"\x12\x34", wCurMap: b"\x01"}, "read": {wOWMapEvents: 2}},
	{"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {wOWMapEvents: b"\x12\x34", wCurMap: b"\x1F"}, "read": {wOWMapEvents: 2}},
]
# <<< factory Func_c36a

# >>> factory Func_c915
CONTRACT["Func_c915"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c915"] = [
	{"hram": {hSCX: b"\x00", hSCY: b"\x00"}, "wram": {wPermissionMap: b"\x00" * 0x100}, "read": {wPermissionMap: 0x100}},
	{"hram": {hSCX: b"\x20", hSCY: b"\x10"}, "wram": {wPermissionMap: b"\x0f" * 0x100}, "read": {wPermissionMap: 0x100}},
	{"hram": {hSCX: b"\xf8", hSCY: b"\xf8"}, "wram": {wPermissionMap: b"\xf0" * 0x100}, "read": {wPermissionMap: 0x100}},
	dict(POISON, hram={hSCX: b"\xaa", hSCY: b"\x55"}, wram={wPermissionMap: b"\x00" * 0x100}, read={wPermissionMap: 0x100}),
]
# <<< factory Func_c915

# >>> factory StartScriptedMovement
CONTRACT["StartScriptedMovement"] = {"compare": (), "preserve": ()};
CASES["StartScriptedMovement"] = [
    {"b": 0x22, "c": 0x33, "wram": {wPlayerSpriteIndex: b"\x00", wWhichSprite: b"\x00", wd339: b"\x00", wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x10", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56", wSpriteAnimBuffer + 0x0E: b"\x00", wSpriteAnimBuffer + 0x0F: b"\x01", wPermissionMap + 0x88: b"\x00"}, "expect": {wWhichSprite: b"\x00", wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x10", wPlayerCurrentlyMoving: b"\x81", wd338: b"\x10", wSpriteAnimBuffer + 0x0E: b"\x04", wSpriteAnimBuffer + 0x0F: b"\x03"}},
    dict(POISON, wram={wPlayerSpriteIndex: b"\x00", wWhichSprite: b"\x00", wd339: b"\x00", wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x10", wPlayerCurrentlyMoving: b"\x80", wd338: b"\x56", wSpriteAnimBuffer + 0x0E: b"\x00", wSpriteAnimBuffer + 0x0F: b"\x01", wPermissionMap + 0x88: b"\x00"}, expect={wWhichSprite: b"\x00", wPlayerXCoord: b"\x10", wPlayerYCoord: b"\x10", wPlayerCurrentlyMoving: b"\x81", wd338: b"\x10", wSpriteAnimBuffer + 0x0E: b"\x04", wSpriteAnimBuffer + 0x0F: b"\x03"}),
]
# <<< factory StartScriptedMovement

# >>> factory RestoreObjectPalettes
CONTRACT["RestoreObjectPalettes"] = {"compare": (), "preserve": ()}
CASES["RestoreObjectPalettes"] = [
	{"wram": {wOBP0Backup: b"\x12", wOBP1Backup: b"\x34", wObjectPalettesCGBBackup: b"\x01" * 64}, "read": {wOBP0: 1, wOBP1: 1, wObjectPalettesCGB: 64}},
	dict(POISON, wram={wOBP0Backup: b"\xA5", wOBP1Backup: b"\x5A", wObjectPalettesCGBBackup: b"\xDE" * 64}, read={wOBP0: 1, wOBP1: 1, wObjectPalettesCGB: 64}),
	{"wram": {wOBP0Backup: b"\xFF", wOBP1Backup: b"\x00", wObjectPalettesCGBBackup: b"\x80\x7F" * 32}, "read": {wOBP0: 1, wOBP1: 1, wObjectPalettesCGB: 64}},
]
# <<< factory RestoreObjectPalettes

# >>> factory Func_c3ff
CONTRACT["Func_c3ff"] = {"compare": (), "preserve": ()}
CASES["Func_c3ff"] = [
	{"wram": {sym("wBGMapWidth"): b"\x14", sym("wBGMapHeight"): b"\x12", sym("wPlayerXCoordPixels"): b"\x40", sym("wPlayerYCoordPixels"): b"\x40"}, "read": {sym("wd237"): 1, sym("wd238"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1, sym("wSCX"): 1, sym("wSCY"): 1, sym("hSCX"): 1, sym("hSCY"): 1}},
	{"wram": {sym("wBGMapWidth"): b"\x28", sym("wBGMapHeight"): b"\x24", sym("wPlayerXCoordPixels"): b"\x90", sym("wPlayerYCoordPixels"): b"\xA0"}, "read": {sym("wd237"): 1, sym("wd238"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1, sym("wSCX"): 1, sym("wSCY"): 1, sym("hSCX"): 1, sym("hSCY"): 1}},
	{"wram": {sym("wBGMapWidth"): b"\x1E", sym("wBGMapHeight"): b"\x20", sym("wPlayerXCoordPixels"): b"\x00", sym("wPlayerYCoordPixels"): b"\x01"}, "read": {sym("wd237"): 1, sym("wd238"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1, sym("wSCX"): 1, sym("wSCY"): 1, sym("hSCX"): 1, sym("hSCY"): 1}},
	dict(POISON, wram={sym("wBGMapWidth"): b"\xAA", sym("wBGMapHeight"): b"\x55", sym("wPlayerXCoordPixels"): b"\xAA", sym("wPlayerYCoordPixels"): b"\x55"}, read={sym("wd237"): 1, sym("wd238"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wSCXBuffer"): 1, sym("wSCYBuffer"): 1, sym("wSCX"): 1, sym("wSCY"): 1, sym("hSCX"): 1, sym("hSCY"): 1}),
]
# <<< factory Func_c3ff

# >>> factory Func_c49c
CONTRACT["Func_c49c"] = {"compare": (), "preserve": ()}
CASES["Func_c49c"] = [
	{"wram": {wPlayerXCoord: b"\x00", wPlayerYCoord: b"\x00"}, "read": {wPlayerXCoord: 1, wPlayerYCoord: 1, wPlayerXCoordPixels: 1, wPlayerYCoordPixels: 1}},
	{"wram": {wPlayerXCoord: b"\x1f", wPlayerYCoord: b"\x1f"}, "read": {wPlayerXCoord: 1, wPlayerYCoord: 1, wPlayerXCoordPixels: 1, wPlayerYCoordPixels: 1}},
	{"wram": {wPlayerXCoord: b"\x20", wPlayerYCoord: b"\xe0"}, "read": {wPlayerXCoord: 1, wPlayerYCoord: 1, wPlayerXCoordPixels: 1, wPlayerYCoordPixels: 1}},
	{"wram": {wPlayerXCoord: b"\xa5", wPlayerYCoord: b"\xe7"}, "read": {wPlayerXCoord: 1, wPlayerYCoord: 1, wPlayerXCoordPixels: 1, wPlayerYCoordPixels: 1}},
	dict(POISON, wram={wPlayerXCoord: b"\x3f", wPlayerYCoord: b"\x7f"}, read={wPlayerXCoord: 1, wPlayerYCoord: 1, wPlayerXCoordPixels: 1, wPlayerYCoordPixels: 1}),
]
# <<< factory Func_c49c

# >>> factory Func_c58b
CONTRACT["Func_c58b"] = {"compare": (), "preserve": ()}
CASES["Func_c58b"] = [
	{"wram": {wPlayerXCoord: b"\x00", wPlayerYCoord: b"\x00", wWhichSprite: b"\x00", wPermissionMap: b"\x00", wSpriteAnimBuffer + 0x0F: b"\x00"}, "read": {wPermissionMap: 1, wSpriteAnimBuffer + 0x0F: 1}},
	{"wram": {wPlayerXCoord: b"\x00", wPlayerYCoord: b"\x00", wWhichSprite: b"\x00", wPermissionMap: b"\x10", wSpriteAnimBuffer + 0x0F: b"\x20"}, "read": {wPermissionMap: 1, wSpriteAnimBuffer + 0x0F: 1}},
	dict(POISON, wram={wPlayerXCoord: b"\x02", wPlayerYCoord: b"\x02", wWhichSprite: b"\x01", wPermissionMap + 0x11: b"\x10", wSpriteAnimBuffer + 0x1F: b"\xff"}, read={wPermissionMap + 0x11: 1, wSpriteAnimBuffer + 0x1F: 1}),
]
# <<< factory Func_c58b

# >>> factory UpdatePlayerSprite
CONTRACT["UpdatePlayerSprite"] = {"compare": ("b", "c"), "preserve": ("b", "c")}
CASES["UpdatePlayerSprite"] = [
    {"wram": {
        wPlayerDirection: b"\x01",
        wPlayerSpriteIndex: b"\x07",
        wPlayerSpriteBaseAnimation: b"\x10",
        wWhichSprite: b"\x00",
    }, "read": {wWhichSprite: 1}},
    dict(POISON,
         wram={
             wPlayerDirection: b"\x03",
             wPlayerSpriteIndex: b"\x0B",
             wPlayerSpriteBaseAnimation: b"\x20",
             wWhichSprite: b"\x00",
         },
         read={wWhichSprite: 1}),
    {"wram": {
        wPlayerDirection: b"\xFF",
        wPlayerSpriteIndex: b"\x42",
        wPlayerSpriteBaseAnimation: b"\x01",
        wWhichSprite: b"\xAA",
    }, "read": {wWhichSprite: 1}},
]
# <<< factory UpdatePlayerSprite

# >>> factory UpdatePlayerDirection
CONTRACT["UpdatePlayerDirection"] = {"compare": ("b", "c"), "preserve": ("b", "c")}
CASES["UpdatePlayerDirection"] = [
    {"a": 0x01, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x07", sym("wPlayerSpriteBaseAnimation"): b"\x10", sym("wWhichSprite"): b"\x00"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0x03, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x0B", sym("wPlayerSpriteBaseAnimation"): b"\x20", sym("wWhichSprite"): b"\x00"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0xFF, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x42", sym("wPlayerSpriteBaseAnimation"): b"\x01", sym("wWhichSprite"): b"\xAA"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x0B", sym("wPlayerSpriteBaseAnimation"): b"\x20", sym("wWhichSprite"): b"\x00"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}}
]
# <<< factory UpdatePlayerDirection

# >>> factory UpdatePlayerDirectionFromDPad
CONTRACT["UpdatePlayerDirectionFromDPad"] = {"compare": ("b", "c"), "preserve": ("b", "c")}
CASES["UpdatePlayerDirectionFromDPad"] = [
    {"a": 0x00, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x07", sym("wPlayerSpriteBaseAnimation"): b"\x10", sym("wWhichSprite"): b"\x00"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0x10, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x0B", sym("wPlayerSpriteBaseAnimation"): b"\x20", sym("wWhichSprite"): b"\x00"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0x20, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x42", sym("wPlayerSpriteBaseAnimation"): b"\x01", sym("wWhichSprite"): b"\xAA"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0x40, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x0B", sym("wPlayerSpriteBaseAnimation"): b"\x20", sym("wWhichSprite"): b"\x00"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wPlayerDirection"): b"\x00", sym("wPlayerSpriteIndex"): b"\x42", sym("wPlayerSpriteBaseAnimation"): b"\x01", sym("wWhichSprite"): b"\xAA"}, "read": {sym("wPlayerDirection"): 1, sym("wWhichSprite"): 1}},
]
# <<< factory UpdatePlayerDirectionFromDPad

# >>> factory SetOverworldDoFrameFunction
CONTRACT["SetOverworldDoFrameFunction"] = {"compare": (), "preserve": ()}
CASES["SetOverworldDoFrameFunction"] = [
	{"wram": {wDoFrameFunction: b"\x00\x00"}, "read": {wDoFrameFunction: 2}},
	dict(POISON, wram={wDoFrameFunction: b"\xAA\xBB"}, read={wDoFrameFunction: 2}),
]
# <<< factory SetOverworldDoFrameFunction

# >>> factory Func_c3ee
CONTRACT["Func_c3ee"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_c3ee"] = [
    {"wram": {sym("wBoosterViableCardList"): b"\xFF" * 256}, "read": {sym("wBoosterViableCardList"): 256}},
    dict(POISON, wram={sym("wBoosterViableCardList"): b"\xFF" * 256}, read={sym("wBoosterViableCardList"): 256}),
]
# <<< factory Func_c3ee

# >>> factory Func_c66c
CONTRACT["Func_c66c"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_c66c"] = [
    {"wram": {sym("hKeysHeld"): b"\x00", sym("wPlayerDirection"): b"\x00", sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x01", sym("wd338"): b"\x10", sym("wd237"): b"\x00", sym("wd238"): b"\x00"},
     "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wLoadedNPC8CoordX"): 1, sym("wLoadedNPC8CoordY"): 1}},
    dict(POISON, wram={sym("hKeysHeld"): b"\x02", sym("wPlayerDirection"): b"\x00", sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x01", sym("wd338"): b"\x01", sym("wd237"): b"\x00", sym("wd238"): b"\x00"},
         read={sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wLoadedNPC8CoordX"): 1, sym("wLoadedNPC8CoordY"): 1}),
    {"wram": {sym("hKeysHeld"): b"\x02", sym("wPlayerDirection"): b"\x00", sym("wPlayerXCoordPixels"): b"\x20", sym("wPlayerYCoordPixels"): b"\x30", sym("wPlayerCurrentlyMoving"): b"\x01", sym("wd338"): b"\x02", sym("wd237"): b"\x00", sym("wd238"): b"\x00"},
     "read": {sym("wPlayerXCoordPixels"): 1, sym("wPlayerYCoordPixels"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wd233"): 1, sym("wd234"): 1, sym("wLoadedNPC8CoordX"): 1, sym("wLoadedNPC8CoordY"): 1}},
]
# <<< factory Func_c66c

# >>> factory Func_c4b9
CONTRACT["Func_c4b9"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_c4b9"] = [
    {"wram": {sym("wConsole"): b"\x00", sym("wCurMap"): b"\x00", sym("wTempPlayerDirection"): b"\x05"},
     "read": {sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1, sym("wPlayerSpriteBaseAnimation"): 1, sym("wPlayerSpriteIndex"): 1, sym("wPlayerDirection"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1}},
    dict(POISON, wram={sym("wConsole"): b"\x00", sym("wCurMap"): b"\x00", sym("wTempPlayerDirection"): b"\x05"},
         read={sym("wTempBoosterChances"): 1, sym("wWhichBGPalIndex"): 1, sym("wPlayerSpriteBaseAnimation"): 1, sym("wPlayerSpriteIndex"): 1, sym("wPlayerDirection"): 1, sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1}),
]
# <<< factory Func_c4b9

# >>> factory DecompressPermissionMap
CONTRACT["DecompressPermissionMap"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["DecompressPermissionMap"] = [
    {"hl": 0x1234, "wram": {wBGMapPermissionDataPtr: b"\x00\x00"}},
    {"hl": sym("wOpponentCardLocations"), "wram": {
        wBGMapPermissionDataPtr: b"\x01\x00",
        wBGMapBank: b"\x00",
        wBGMapHeight: b"\x01",
        wBGMapWidth: b"\x01",
    }, "read": {wBGMapPermissionDataPtr: 2, wDecompressionSecondaryBuffer: 0x10, sym("wOpponentCardLocations"): 0x10}},
    dict(POISON, hl=0x1234, wram={wBGMapPermissionDataPtr: b"\x00\x00"}),
]
# <<< factory DecompressPermissionMap

# >>> factory LoadPermissionMap
CONTRACT["LoadPermissionMap"] = {"compare": ("hl", "b", "c"), "preserve": ("hl", "b", "c")}
CASES["LoadPermissionMap"] = [
    {"wram": {wBGMapPermissionDataPtr: b"\x00\x00"}, "read": {wPermissionMap: 256}},
    dict(POISON, wram={wBGMapPermissionDataPtr: b"\x00\x00"}, read={wPermissionMap: 256}),
]
# <<< factory LoadPermissionMap

# >>> factory Func_c1ed
CONTRACT["Func_c1ed"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_c1ed"] = [
    {"wram": {hBankROM: b"\x03"}, "sram": {0: {sym("sGeneralSaveData"): bytes([0xAB]) * 256}},
     "read": {sym("wOverworldMapSelection"): 1}, "instruction_budget": 500000, "cycle_budget": 4000000},
    dict(POISON, wram={hBankROM: b"\x03"}, sram={0: {sym("sGeneralSaveData"): bytes([0xAB]) * 256}},
         read={sym("wOverworldMapSelection"): 1}, instruction_budget=500000, cycle_budget=4000000),
]
# <<< factory Func_c1ed

# >>> factory Func_c1b1
CONTRACT["Func_c1b1"] = {"compare": (), "preserve": (), "wram_out": True, "sram_out": True}
CASES["Func_c1b1"] = [
    {"wram": {hBankROM_A: b"\x03", wOverworldMapSelection_A: b"\x00", wTempMap_A: b"\xFF",
              wTempPlayerXCoord_A: b"\xFF", wTempPlayerYCoord_A: b"\xFF", wTempPlayerDirection_A: b"\xFF",
              wPlayTimeCounter_A: b"\xFF\xFF\xFF\xFF\xFF", wOWMapEvents_A: bytes([0xFF] * 11),
              wMastersBeatenList_A: bytes([0xFF] * 10)},
     "sram": {0: {sym("sChallengeMachineStart"): b"\xFF\xFF\xFF\xFF\xFF\xFF"}},
     "read": {wOverworldMapSelection_A: 1, wTempMap_A: 1, wTempPlayerXCoord_A: 1, wTempPlayerYCoord_A: 1,
              wTempPlayerDirection_A: 1, wPlayTimeCounter_A: 5, wOWMapEvents_A: 11, wMastersBeatenList_A: 10},
     "sread": {0: {sym("sChallengeMachineStart"): 6}}, "instruction_budget": 500000, "cycle_budget": 4000000},
    dict(POISON, wram={hBankROM_A: b"\x03", wOverworldMapSelection_A: b"\x00", wTempMap_A: b"\xFF",
              wTempPlayerXCoord_A: b"\xFF", wTempPlayerYCoord_A: b"\xFF", wTempPlayerDirection_A: b"\xFF",
              wPlayTimeCounter_A: b"\xFF\xFF\xFF\xFF\xFF", wOWMapEvents_A: bytes([0xFF] * 11),
              wMastersBeatenList_A: bytes([0xFF] * 10)},
         sram={0: {sym("sChallengeMachineStart"): b"\xFF\xFF\xFF\xFF\xFF\xFF"}},
         read={wOverworldMapSelection_A: 1, wTempMap_A: 1, wTempPlayerXCoord_A: 1, wTempPlayerYCoord_A: 1,
              wTempPlayerDirection_A: 1, wPlayTimeCounter_A: 5, wOWMapEvents_A: 11, wMastersBeatenList_A: 10},
         sread={0: {sym("sChallengeMachineStart"): 6}}, instruction_budget=500000, cycle_budget=4000000),
]
# <<< factory Func_c1b1

# >>> factory Func_c554
CONTRACT["Func_c554"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_c554"] = [
    {"wram": {wCurMap_A: b"\x00", wPlayerSpriteIndex_A: b"\x00"},
     "read": {wWhichSprite_A: 1}},
    dict(POISON, wram={wCurMap_A: b"\x05", wPlayerSpriteIndex_A: b"\x00",
                       wPlayerXCoordPixels_A: b"\x20", wPlayerYCoordPixels_A: b"\x30",
                       wSCXBuffer_A: b"\x04", wSCYBuffer_A: b"\x08"},
         read={wWhichSprite_A: 1, sym("wSprite1CoordX"): 2}),
]
# <<< factory Func_c554

# >>> factory Func_c280
CONTRACT["Func_c280"] = {"compare": (), "preserve": ()}
CASES["Func_c280"] = [
    {"keys": 0, "instruction_budget": 3000000, "cycle_budget": 10000000,
     "wram": {wVBlankOAMCopyToggle: b"\x05"},
     "read": {wVBlankOAMCopyToggle: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=3000000, cycle_budget=10000000,
         wram={wVBlankOAMCopyToggle: b"\x05"},
         read={wVBlankOAMCopyToggle: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory Func_c280

# >>> factory UpdateOverworldMap
CONTRACT["UpdateOverworldMap"] = {"compare": (), "preserve": ()}
CASES["UpdateOverworldMap"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "hram": {sym("hKeysPressed"): b"\x00"}, "wram": {sym("wPlayerSpriteIndex"): b"\x12", sym("wOverworldMapPlayerAnimationState"): b"\x00", sym("wWhichSprite"): b"\x00"}, "read": {sym("wWhichSprite"): 1}},
    {"hram": {sym("hKeysPressed"): b"\x00"}, "wram": {sym("wPlayerSpriteIndex"): b"\x34", sym("wOverworldMapPlayerAnimationState"): b"\x00", sym("wWhichSprite"): b"\x00"}, "read": {sym("wWhichSprite"): 1}},
    dict(POISON, hram={sym("hKeysPressed"): b"\x00"}, wram={sym("wPlayerSpriteIndex"): b"\x56", sym("wOverworldMapPlayerAnimationState"): b"\x00", sym("wWhichSprite"): b"\x00"}, read={sym("wWhichSprite"): 1}),
]
# <<< factory UpdateOverworldMap

# >>> factory DisplayPauseMenu
CONTRACT["DisplayPauseMenu"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DisplayPauseMenu"] = [
    {"wram": {wSelectedPauseMenuItem: b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wCurMenuItem: 1, hCurMenuItem: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wSelectedPauseMenuItem: b"\x05", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wCurMenuItem: 1, hCurMenuItem: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={wSelectedPauseMenuItem: b"\x02", sym("wLCDC"): b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wCurMenuItem: 1, hCurMenuItem: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DisplayPauseMenu

# >>> factory Func_c8ed
CONTRACT["Func_c8ed"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c8ed"] = [
    {"hl": 0x0000, "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": menu_state(0), "read": {sym("wd3b9"): 2}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"hl": 0x0001, "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {**menu_state(0), sym("wd3b9"): b"\xAA\xAA"}, "read": {sym("wd3b9"): 2}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0x1234, keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={**menu_state(1), sym("wd3b9"): b"\xAA\xAA"}, read={sym("wd3b9"): 2}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_c8ed

# >>> factory PauseMenu_Diary
CONTRACT["PauseMenu_Diary"] = {"compare": (), "preserve": ()}
CASES["PauseMenu_Diary"] = [
    {"keys": [0x00, 0x01], "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("wd291"): b"\x5A"}, "read": {sym("wd291"): 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x01], setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("wd291"): b"\x5A"}, read={sym("wd291"): 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory PauseMenu_Diary

# >>> factory DisplayPCMenu
CONTRACT["DisplayPCMenu"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DisplayPCMenu"] = [
    {"wram": {sym("wSelectedPCMenuItem"): b"\x00", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {sym("wCurMenuItem"): 1, sym("hCurMenuItem"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {sym("wSelectedPCMenuItem"): b"\x04", sym("wLCDC"): b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {sym("wCurMenuItem"): 1, sym("hCurMenuItem"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={sym("wSelectedPCMenuItem"): b"\x02", sym("wLCDC"): b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={sym("wCurMenuItem"): 1, sym("hCurMenuItem"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DisplayPCMenu

# >>> factory Func_c268
CONTRACT["Func_c268"] = {"compare": (), "preserve": ()}
CASES["Func_c268"] = [
    {"setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7f}],
     "wram": {sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"},
     "read": {sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON,
         setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7f}],
         wram={sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"},
         read={sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_c268

# >>> factory PauseMenu_Status
CONTRACT["PauseMenu_Status"] = {"compare": (), "preserve": ()}
CASES["PauseMenu_Status"] = [
    {"keys": [0x00, 0x01], "setup": SETUP, "wram": {sym("wLCDC"): b"\x00", sym("wd291"): b"\x5A"}, "read": {sym("wd291"): 1, wMedalScreenYOffset: 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x01], setup=SETUP, wram={sym("wLCDC"): b"\x00", sym("wd291"): b"\x5A"}, read={sym("wd291"): 1, wMedalScreenYOffset: 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory PauseMenu_Status

# >>> factory Func_c258
CONTRACT["Func_c258"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c258"] = [
    {"f": 0x00, "wram": {sym("hffb0"): b"\x00", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}], "read": {sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"f": 0xF0, "wram": {sym("hffb0"): b"\x01", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}], "read": {sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, f=0x0F, wram={sym("hffb0"): b"\xEE", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7F}], read={sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_c258

# >>> factory Func_c251
CONTRACT["Func_c251"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_c251"] = [
    {"f": 0x00, "wram": {sym("hffb0"): b"\x00", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}], "read": {sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"f": 0xF0, "wram": {sym("hffb0"): b"\x01", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}], "read": {sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, f=0x0F, wram={sym("hffb0"): b"\xEE", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7F}], read={sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, instruction_budget=2000000, cycle_budget=8000000)
]
# <<< factory Func_c251

# >>> factory Func_c241
CONTRACT["Func_c241"] = {"compare": ("f",), "preserve": ()}
CASES["Func_c241"] = [
    {"f": 0x00, "wram": {sym("hffb0"): b"\x00", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, "setup": [{"fn": "SetupText", "d": 0x30, "e": 0x7F}], "read": {sym("wcd04"): 1, sym("hffa8"): 1, sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={sym("hffb0"): b"\xEE", sym("hTextBGMap0Address"): b"\x00", sym("hTextBGMap0Address") + 1: b"\x98"}, setup=[{"fn": "SetupText", "d": 0x30, "e": 0x7F}], read={sym("wcd04"): 1, sym("hffa8"): 1, sym("wc600") + 0x30: 1, sym("wc700") + 0x30: 1, sym("wc800") + 0x30: 1, sym("wc900"): 1, sym("hffa9"): 1}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_c241

# >>> factory CloseTextBox
CONTRACT["CloseTextBox"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["CloseTextBox"] = [
    {"hl": 0x4567, "wram": {wOverworldNPCFlags: b"\x01", sym("wBoosterViableCardList"): b"\x00" * 0x100}, "read": {wOverworldNPCFlags: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, hl=0x1357, wram={wOverworldNPCFlags: b"\xFF", sym("wBoosterViableCardList"): b"\xFF" * 0x100}, read={wOverworldNPCFlags: 1}, instruction_budget=20000000, cycle_budget=80000000),
    {"hl": 0x2468, "wram": {wOverworldNPCFlags: b"\x00", sym("wBoosterViableCardList"): b"\x00" * 0x100}, "read": {wOverworldNPCFlags: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory CloseTextBox

# >>> factory Func_c891
CONTRACT["Func_c891"] = {"compare": (), "preserve": ()}
CASES["Func_c891"] = [
    {"hl": 0x01DB, "wram": {wOverworldNPCFlags: b"\x00", wd3b9: b"\x12\x34"}, "setup": SETUP, "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {wOverworldNPCFlags: 1, wd3b9: 2}},
    {"hl": 0x01DC, "wram": {wOverworldNPCFlags: b"\x00", wd3b9: b"\x56\x78"}, "setup": SETUP, "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {wOverworldNPCFlags: 1, wd3b9: 2}},
    dict(POISON, hl=0x01DB, wram={wOverworldNPCFlags: b"\x00", wd3b9: b"\x9A\xBC"}, setup=SETUP, keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=80000000, read={wOverworldNPCFlags: 1, wd3b9: 2}),
]
# <<< factory Func_c891

# >>> factory ReturnToOverworld
CONTRACT["ReturnToOverworld"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ReturnToOverworld"] = [
    {"wram": {sym("wOverworldNPCFlags"): b"\xFF", sym("wReloadOverworldCallbackPtr"): b"\x00\x00", sym("wDefaultSong"): b"\x37"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wDefaultSong"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {sym("wOverworldNPCFlags"): b"\x80", sym("wReloadOverworldCallbackPtr"): b"\x00\x00", sym("wDefaultSong"): b"\xA5"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wDefaultSong"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={sym("wOverworldNPCFlags"): b"\x55", sym("wReloadOverworldCallbackPtr"): b"\x00\x00", sym("wDefaultSong"): b"\x00"}, read={sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wDefaultSong"): 1}, instruction_budget=20000000, cycle_budget=80000000),
    # wReloadOverworldCallbackPtr set: the pause menu redraw runs through CallHL2.
    {"setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("wOverworldNPCFlags"): b"\x80", sym("wReloadOverworldCallbackPtr"): sym_pointer("DisplayPauseMenu"), sym("wDefaultSong"): b"\xA5", sym("wSelectedPauseMenuItem"): b"\x03"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wDefaultSong"): 1, sym("wc600"): 0x400}, "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory ReturnToOverworld

# >>> factory CloseAdvancedDialogueBox
CONTRACT["CloseAdvancedDialogueBox"] = {"compare": (), "preserve": ()}
CASES["CloseAdvancedDialogueBox"] = [
	{"wram": {sym("wOverworldNPCFlags"): b"\x00", sym("wOverworldModeBackup"): b"\x00", sym("wOverworldMode"): b"\x00"}, "read": {sym("wOverworldNPCFlags"): 1, sym("wOverworldMode"): 1}},
	{"wram": {sym("wOverworldNPCFlags"): b"\x00", sym("wOverworldModeBackup"): b"\x5A", sym("wOverworldMode"): b"\x00"}, "read": {sym("wOverworldNPCFlags"): 1, sym("wOverworldMode"): 1}},
	dict(POISON, wram={sym("wOverworldNPCFlags"): b"\x00", sym("wOverworldModeBackup"): b"\xA5", sym("wOverworldMode"): b"\x11"}, read={sym("wOverworldNPCFlags"): 1, sym("wOverworldMode"): 1}),
]
# <<< factory CloseAdvancedDialogueBox

# >>> factory Func_c8ba
CONTRACT["Func_c8ba"] = {"compare": (), "preserve": ()}
CASES["Func_c8ba"] = [
    {"hl": 0x01DB, "d": 0x00, "e": 0x00, "wram": {wOverworldNPCFlags: b"\x00", wd3b9: b"\x12\x34"}, "setup": SETUP, "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {wOverworldNPCFlags: 1, wd3b9: 2}},
    {"hl": 0x01DC, "d": 0x00, "e": 0x03, "wram": {wOverworldNPCFlags: b"\x01", wd3b9: b"\x12\x34"}, "setup": SETUP, "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 80000000, "read": {wOverworldNPCFlags: 1, wd3b9: 2}},
    dict(POISON, hl=0x01DB, d=0x00, e=0x04, wram={wOverworldNPCFlags: b"\x01", wd3b9: b"\x12\x34"}, setup=SETUP, keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=80000000, read={wOverworldNPCFlags: 1, wd3b9: 2}),
]
# <<< factory Func_c8ba

# >>> factory ReturnToOverworldNoCallback
CONTRACT["ReturnToOverworldNoCallback"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ReturnToOverworldNoCallback"] = [
    {"wram": {sym("wOverworldNPCFlags"): b"\xFF", sym("wReloadOverworldCallbackPtr"): b"\x12\x34", sym("wDefaultSong"): b"\x37"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wReloadOverworldCallbackPtr"): 2, sym("wDefaultSong"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {sym("wOverworldNPCFlags"): b"\x80", sym("wReloadOverworldCallbackPtr"): b"\xAB\xCD", sym("wDefaultSong"): b"\xA5"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wReloadOverworldCallbackPtr"): 2, sym("wDefaultSong"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={sym("wOverworldNPCFlags"): b"\x55", sym("wReloadOverworldCallbackPtr"): b"\xFE\xED", sym("wDefaultSong"): b"\x00"}, read={sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wReloadOverworldCallbackPtr"): 2, sym("wDefaultSong"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ReturnToOverworldNoCallback

# >>> factory ReturnToOverworldWithCallback
CONTRACT["ReturnToOverworldWithCallback"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ReturnToOverworldWithCallback"] = [
    # The game passes exactly two callbacks (overworld.asm: PauseMenu and PCMenu),
    # both menu redraws, so a case needs the text setup a menu draw relies on.
    {"hl": sym("DisplayPauseMenu"), "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("wOverworldNPCFlags"): b"\xFF", sym("wReloadOverworldCallbackPtr"): b"\x00\x00", sym("wDefaultSong"): b"\x37", sym("wSelectedPauseMenuItem"): b"\x02"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wReloadOverworldCallbackPtr"): 2, sym("wDefaultSong"): 1, sym("wc600"): 0x400}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"hl": sym("DisplayPCMenu"), "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("wOverworldNPCFlags"): b"\x80", sym("wReloadOverworldCallbackPtr"): b"\x12\x34", sym("wDefaultSong"): b"\xA5", sym("wSelectedPCMenuItem"): b"\x01"}, "read": {sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wReloadOverworldCallbackPtr"): 2, sym("wDefaultSong"): 1, sym("wc600"): 0x400}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, hl=sym("DisplayPauseMenu"), setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("wOverworldNPCFlags"): b"\x55", sym("wReloadOverworldCallbackPtr"): b"\xFE\xED", sym("wDefaultSong"): b"\x00", sym("wSelectedPauseMenuItem"): b"\x05"}, read={sym("hWhoseTurn"): 1, sym("wOverworldNPCFlags"): 1, sym("wReloadOverworldCallbackPtr"): 2, sym("wDefaultSong"): 1, sym("wc600"): 0x400}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ReturnToOverworldWithCallback

# >>> factory FindNPCOrObject
CONTRACT["FindNPCOrObject"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["FindNPCOrObject"] = [
    # water-club 91959: the live entry whose `.set_mode` exit carries the Z the
    # callee left set, which `scf` preserves and the port used to drop.
    dict(find_npc_fixture(vram=False, bank=3), **FIND_NPC_REGS),
    {"keys": [0x00], "wram": {sym("wScriptNPC"): b"\x00", sym("wOverworldMode"): b"\x55", sym("wPlayerDirection"): b"\x00", sym("wPlayerXCoord"): b"\x00", sym("wPlayerYCoord"): b"\x00"}, "read": {sym("wScriptNPC"): 1, sym("wOverworldMode"): 1}},
    dict(POISON, keys=[0x00], wram={sym("wScriptNPC"): b"\x00", sym("wOverworldMode"): b"\x55", sym("wPlayerDirection"): b"\x00", sym("wPlayerXCoord"): b"\x00", sym("wPlayerYCoord"): b"\x00"}, read={sym("wScriptNPC"): 1, sym("wOverworldMode"): 1}),
]
# <<< factory FindNPCOrObject

# >>> factory Func_c6dc
CONTRACT["Func_c6dc"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["Func_c6dc"] = [
    {"hl": 0x1234, "wram": {sym("wPlayerCurrentlyMoving"): b"\x03", sym("wOverworldMode"): b"\x00"}, "read": {sym("wPlayerCurrentlyMoving"): 1, sym("wOverworldMode"): 1}},
    {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wPlayerCurrentlyMoving"): b"\xFF", sym("wOverworldMode"): b"\x01"}, "read": {sym("wPlayerCurrentlyMoving"): 1, sym("wOverworldMode"): 1}},
    {"hl": sym("wPlayerCardLocations"), "wram": {sym("wPlayerCurrentlyMoving"): b"\x00", sym("wOverworldMode"): b"\x02"}, "read": {sym("wPlayerCurrentlyMoving"): 1, sym("wOverworldMode"): 1}},
    dict(POISON, hl=sym("wOpponentCardLocations"), wram={sym("wPlayerCurrentlyMoving"): b"\x03", sym("wOverworldMode"): b"\x00"}, read={sym("wPlayerCurrentlyMoving"): 1, sym("wOverworldMode"): 1}),
    dict(POISON, hl=sym("wBoosterCardsDrawn"), wram={sym("wPlayerCurrentlyMoving"): b"\xFF", sym("wOverworldMode"): b"\x01"}, read={sym("wPlayerCurrentlyMoving"): 1, sym("wOverworldMode"): 1}),
]
# <<< factory Func_c6dc

# >>> factory HandlePlayerMoveModeInput
CONTRACT["HandlePlayerMoveModeInput"] = {"compare": (), "preserve": ()}
CASES["HandlePlayerMoveModeInput"] = [
    {"wram": {sym("hKeysHeld"): b"\x00", sym("hKeysPressed"): b"\x00"}},
    {"wram": {sym("hKeysHeld"): b"\x00", sym("hKeysPressed"): b"\x01", sym("wScriptNPC"): b"\x5A"}, "read": {sym("wScriptNPC"): 1}},
    dict(POISON, wram={sym("hKeysHeld"): b"\x00", sym("hKeysPressed"): b"\x01", sym("wScriptNPC"): b"\x5A"}, read={sym("wScriptNPC"): 1}),
    {"wram": {sym("hKeysHeld"): b"\x10", sym("hKeysPressed"): b"\x00"}, "read": {sym("wPlayerCurrentlyMoving"): 1}},
]
# <<< factory HandlePlayerMoveModeInput

# >>> factory PCMenu_Glossary
CONTRACT["PCMenu_Glossary"] = {"compare": (), "preserve": ()}
CASES["PCMenu_Glossary"] = [
    {"keys": [0x00, 0x02], "setup": SETUP, "wram": {sym("wLCDC"): b"\x00", sym("wd291"): b"\x5A"}, "read": {sym("wd291"): 1, sym("wDuelInitialPrizesUpperBitsSet"): 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x02], setup=SETUP, wram={sym("wLCDC"): b"\x00", sym("wd291"): b"\x5A"}, read={sym("wd291"): 1, sym("wDuelInitialPrizesUpperBitsSet"): 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory PCMenu_Glossary

# >>> factory Func_c17a
CONTRACT["Func_c17a"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["Func_c17a"] = [
    {"hl": 0x0000, "wram": {sym("wOverworldMode"): b"\x03"}, "read": {sym("wOverworldMode"): 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wOverworldMode"): b"\x03"}, "read": {sym("wOverworldMode"): 1}},
    {**MAP_SCRIPT_REGS, "hl": sym("wActiveGameEvent"), "wram": {sym("wOverworldMode"): b"\x00", sym("wCurMap"): b"\x03"}, "read": {sym("wOverworldMode"): 1}},
]
# <<< factory Func_c17a

# >>> factory Func_c53d
CONTRACT["Func_c53d"] = {"compare": ("b", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["Func_c53d"] = [
	{"wram": {sym("wPlayerCurrentlyMoving"): b"\x00", sym("wPlayerSpriteIndex"): b"\x00"}, "read": {sym("wWhichSprite"): 1}},
	{"wram": {sym("wPlayerCurrentlyMoving"): b"\x00", sym("wPlayerSpriteIndex"): b"\xA5"}, "read": {sym("wWhichSprite"): 1}},
	{"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wPlayerCurrentlyMoving"): b"\x00", sym("wPlayerSpriteIndex"): b"\x5A"}, "read": {sym("wWhichSprite"): 1}},
]
# <<< factory Func_c53d

# >>> factory PCMenu_CardAlbum
CONTRACT["PCMenu_CardAlbum"] = {"compare": (), "preserve": ()}
CASES["PCMenu_CardAlbum"] = [
    {"keys": [0x00, 0x02], "setup": SETUP, "wram": {sym("hSCX"): b"\x55", sym("hSCY"): b"\x66", sym("hCurMenuItem"): b"\xFF", sym("wLCDC"): b"\x00"}, "read": {sym("hSCX"): 1, sym("hSCY"): 1, sym("wLCDC"): 1}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x02], setup=SETUP, wram={sym("hSCX"): b"\x55", sym("hSCY"): b"\x66", sym("hCurMenuItem"): b"\xFF", sym("wLCDC"): b"\x00"}, read={sym("hSCX"): 1, sym("hSCY"): 1, sym("wLCDC"): 1}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory PCMenu_CardAlbum

# >>> factory PauseMenu_Config
CONTRACT["PauseMenu_Config"] = {"compare": (), "preserve": ()}
CASES["PauseMenu_Config"] = [
    {
        "keys": [0x00, 0x02],
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "wram": {sym("wLCDC"): b"\x00", sym("wDuelTempList"): b"\xff", sym("wd291"): b"\x5a", sym("wLineSeparation"): b"\x00"},
        "read": {sym("wConfigExitSettingsCursorPos"): 1, sym("wd291"): 1, sym("wLineSeparation"): 1},
        "instruction_budget": 20000000,
        "cycle_budget": 80000000,
    },
    dict(POISON,
         keys=[0x00, 0x02],
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         wram={sym("wLCDC"): b"\x00", sym("wDuelTempList"): b"\xff", sym("wd291"): b"\x5a", sym("wLineSeparation"): b"\x00"},
         read={sym("wConfigExitSettingsCursorPos"): 1, sym("wd291"): 1, sym("wLineSeparation"): 1},
         instruction_budget=20000000,
         cycle_budget=80000000),
]
# <<< factory PauseMenu_Config

# >>> factory PCMenu_ReadMail
CONTRACT["PCMenu_ReadMail"] = {"compare": ("a",), "preserve": ()}
CASES["PCMenu_ReadMail"] = [
    # No packs owned, so PrintObtainedPCPacks and BlinkUnopenedPCPacks print
    # nothing and the only byte the wrapped screen writes that is worth
    # observing is wd291, which must come back holding exactly the byte it was
    # seeded with. hDPadHeld is cleared so PCMailHandleDPadInput returns at
    # once, and hKeysPressed is seeded with B so the native side leaves on its
    # first pass; the reference leaves on the frame the cycled B lands its edge,
    # and both end with $02 in hKeysPressed.
    {"wram": {wd291: b"\x00", hKeysPressed: b"\x02", hDPadHeld: b"\x00",
              wPCPackSelection: b"\x00", wPCPacks: bytes(15), wLCDC: b"\x00"},
     "keys": READ_MAIL_KEYS, "setup": SETUP,
     "read": {wd291: 1},
     "instruction_budget": READ_MAIL_INSTRUCTIONS, "cycle_budget": READ_MAIL_CYCLES},
    # One opened pack in slot 0: PrintObtainedPCPacks prints its name and
    # BlinkUnopenedPCPacks skips it (bit 7 clear), so the drawn screen does not
    # depend on how many frames elapsed. wd291 carries a distinctive byte, which
    # is also the byte the farcall has to forward back in a.
    {"wram": {wd291: b"\x5a", hKeysPressed: b"\x02", hDPadHeld: b"\x00",
              wPCPackSelection: b"\x00", wPCPacks: b"\x01" + bytes(14),
              wLCDC: b"\x00"},
     "keys": READ_MAIL_KEYS, "setup": SETUP,
     "read": {wd291: 1},
     "instruction_budget": READ_MAIL_INSTRUCTIONS, "cycle_budget": READ_MAIL_CYCLES},
    # Poisoned entry registers on the last slot: the wrapper reads no register
    # input at all, and $FF is the wd291 byte a stuck-at-zero save would lose.
    dict(POISON,
         wram={wd291: b"\xff", hKeysPressed: b"\x02", hDPadHeld: b"\x00",
               wPCPackSelection: b"\x0e", wPCPacks: bytes(14) + b"\x01",
               wLCDC: b"\x00"},
         keys=READ_MAIL_KEYS, setup=SETUP,
         read={wd291: 1},
         instruction_budget=READ_MAIL_INSTRUCTIONS, cycle_budget=READ_MAIL_CYCLES),
]
# <<< factory PCMenu_ReadMail

# >>> factory Func_c2a3
CONTRACT["Func_c2a3"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
# 0xCABB wLCDC and 0xFF40 rLCDC are seeded enabled together so the reference's
# VBlank scheduler is armed and EnableLCD takes its "already on" early return;
# CopyDMAFunction installs hDMAFunction so VBlankHandler does not run junk.
# 0xD0C1 is wOverworldNPCFlags, which SetOverworldNPCFlags ORs 0x80 into.
# wVBlankOAMCopyToggle (0xCAC0) is cleared by the reference VBlank handler, so
# it is neither seeded nor observed.
CASES["Func_c2a3"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {sym("wLCDC"): b"\x80", 0xFF40: b"\x80", sym("wOverworldNPCFlags"): b"\x00"},
     "read": {sym("wOverworldNPCFlags"): 1},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={sym("wLCDC"): b"\x80", 0xFF40: b"\x80", sym("wOverworldNPCFlags"): b"\x01"},
         read={sym("wOverworldNPCFlags"): 1},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=[0x00, 0x01],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Func_c2a3

# >>> factory PauseMenu_Card
CONTRACT["PauseMenu_Card"] = {"compare": (), "preserve": ()}
CASES["PauseMenu_Card"] = [
    {"keys": [0x00, 0x02], "setup": SETUP,
     "wram": {hSCX: b"\x55", hSCY: b"\x66", sym("wLCDC"): b"\x00",
               sym("wCardListVisibleOffset"): b"\xFF", sym("wCurCardTypeFilter"): b"\xFF", sym("hffb3"): b"\xFF"},
     "sram": PAUSE_CARD_SRAM,
     "read": {hSCX: 1, hSCY: 1},
     "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x02], setup=SETUP,
         wram={hSCX: b"\x55", hSCY: b"\x66", sym("wLCDC"): b"\x00",
               sym("wCardListVisibleOffset"): b"\xFF", sym("wCurCardTypeFilter"): b"\xFF", sym("hffb3"): b"\xFF"},
         sram=PAUSE_CARD_SRAM, read={hSCX: 1, hSCY: 1},
         instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory PauseMenu_Card

# >>> factory EnterScript
CONTRACT["EnterScript"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["EnterScript"] = [
    {"wram": {wNextScript: b"\x00\xC0", sym("wDeckToBuild"): b"\xC9"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={wNextScript: b"\x00\xC0", sym("wDeckToBuild"): b"\xC9"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory EnterScript

# >>> factory SetScriptData
CONTRACT["SetScriptData"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ()}
CASES["SetScriptData"] = [
	{"hl": 0x0000, "wram": {wScriptNPC: b"\x00", wLoadedNPCTempIndex: b"\xA5", wOverworldMode: b"\x00", wNextScript: b"\x12\x34", wPlayerDirection: b"\x00", wOverworldNPCFlags: b"\x00", LOADED_NPCS: b"\x4A" + b"\x00" * 95}},
	dict(POISON, hl=0x1234, wram={wScriptNPC: b"\x00", wLoadedNPCTempIndex: b"\xEE", wOverworldMode: b"\xA5", wNextScript: b"\xAA\x55", wPlayerDirection: b"\x02", wOverworldNPCFlags: b"\x04", LOADED_NPCS: b"\x4A" + b"\x00" * 95}),
	{"hl": data(0xBEEF), "wram": {wScriptNPC: b"\x01", wLoadedNPCTempIndex: b"\xFE", wOverworldMode: b"\x01", wNextScript: b"\xFE\xED", wPlayerDirection: b"\x03", wOverworldNPCFlags: b"\x80", LOADED_NPCS: b"\x00" * 12 + b"\x4A" + b"\x00" * 83}},
]
# <<< factory SetScriptData

# >>> factory PauseMenu_Deck
CONTRACT["PauseMenu_Deck"] = {"compare": (), "preserve": ()}
CASES["PauseMenu_Deck"] = [
    {"keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("hSCX"): b"\x55", sym("hSCY"): b"\x66", sym("wCurDeck"): b"\x00", sym("wLCDC"): b"\x00"}, "read": {sym("hSCX"): 1, sym("hSCY"): 1, sym("wCurDeck"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("hSCX"): b"\x55", sym("hSCY"): b"\x66", sym("wCurDeck"): b"\x00", sym("wLCDC"): b"\x00"}, read={sym("hSCX"): 1, sym("hSCY"): 1, sym("wCurDeck"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PauseMenu_Deck

# >>> factory PauseMenu
CONTRACT["PauseMenu"] = {"compare": (), "preserve": ()}
CASES["PauseMenu"] = [
    {
        "keys": [0x00, 0x02],
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "wram": {sym("wSelectedPauseMenuItem"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"},
        "read": {sym("wSelectedPauseMenuItem"): 1},
        "instruction_budget": 20000000,
        "cycle_budget": 80000000,
    },
    {
        "keys": [0x00, 0x02],
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "wram": {sym("wSelectedPauseMenuItem"): b"\x05", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"},
        "read": {sym("wSelectedPauseMenuItem"): 1},
        "instruction_budget": 20000000,
        "cycle_budget": 80000000,
    },
    dict(POISON,
         keys=[0x00, 0x02],
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         wram={sym("wSelectedPauseMenuItem"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"},
         read={sym("wSelectedPauseMenuItem"): 1},
         instruction_budget=20000000,
         cycle_budget=80000000),
]
# <<< factory PauseMenu

# >>> factory OpenPauseMenu
CONTRACT["OpenPauseMenu"] = {"compare": (), "preserve": ()}
CASES["OpenPauseMenu"] = [
    {"keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("wSelectedPauseMenuItem"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"}, "read": {sym("wSelectedPauseMenuItem"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("wSelectedPauseMenuItem"): b"\x05", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"}, read={sym("wSelectedPauseMenuItem"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OpenPauseMenu

# >>> factory HandlePlayerMoveMode
CONTRACT["HandlePlayerMoveMode"] = {"compare": (), "preserve": ()}
_MOVE_STEP = _move_step_fixture(vram=False, bank=3)
_MOVE_STEP["wram"] = {**_MOVE_STEP["wram"], sym("hDPadHeld"): b"\x00", sym("hKeysHeld"): b"\x80", sym("hKeysPressed"): b"\x00"}
_MOVE_STEP["read"] = {**_MOVE_STEP["read"], sym("wPlayerCurrentlyMoving"): 1, sym("wd338"): 1, sym("wSprite1Counter"): 2}
CASES["HandlePlayerMoveMode"] = [
    {"wram": {wPlayerSpriteIndex: b"\x12", wPlayerCurrentlyMoving: b"\x00", hKeysPressed: b"\x00"}, "read": {wWhichSprite: 1}},
    {"keys": [0x08, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {wPlayerSpriteIndex: b"\x34", wPlayerCurrentlyMoving: b"\x00", sym("wLCDC"): b"\x00"}, "read": {wWhichSprite: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wPlayerSpriteIndex: b"\x56", wPlayerCurrentlyMoving: b"\x10", hKeysPressed: b"\x00"}, "read": {wWhichSprite: 1}},
    {"wram": {wPlayerSpriteIndex: b"\x78", wPlayerCurrentlyMoving: b"\x01", hKeysPressed: b"\x00", sym("wOverworldMode"): b"\x00"}, "read": {wWhichSprite: 1}},
    {"wram": {wPlayerSpriteIndex: b"\xBC", wPlayerCurrentlyMoving: b"\x02", hKeysPressed: b"\x00", sym("wOverworldMode"): b"\x00"}, "read": {wWhichSprite: 1}},
    dict(POISON, wram={wPlayerSpriteIndex: b"\x9A", wPlayerCurrentlyMoving: b"\x03", hKeysPressed: b"\x00", sym("wOverworldMode"): b"\x00"}, read={wWhichSprite: 1}),
    # The joypad is read, not polled: DOWN held as the frame had it.
    dict(_MOVE_STEP, **_MOVE_STEP_REGS),
]
# <<< factory HandlePlayerMoveMode

# >>> factory CallHandlePlayerMoveMode
CONTRACT["CallHandlePlayerMoveMode"] = {"compare": (), "preserve": ()}
CASES["CallHandlePlayerMoveMode"] = [
	{"wram": {sym("wPlayerCurrentlyMoving"): b"\x10", sym("wPlayerSpriteIndex"): b"\x5A"}, "read": {sym("wWhichSprite"): 1}},
	dict(POISON, wram={sym("wPlayerCurrentlyMoving"): b"\x10", sym("wPlayerSpriteIndex"): b"\xC3"}, read={sym("wWhichSprite"): 1}),
]
# <<< factory CallHandlePlayerMoveMode

# >>> factory HandleOverworldMode
CONTRACT["HandleOverworldMode"] = {"compare": (), "preserve": ()}
CASES["HandleOverworldMode"] = [
    {"wram": {sym("wOverworldMode"): b"\x00", sym("wPlayerSpriteIndex"): b"\x12", sym("wOverworldMapPlayerAnimationState"): b"\x00", sym("wWhichSprite"): b"\x00"}, "expect": {sym("wWhichSprite"): b"\x12"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"wram": {sym("wOverworldMode"): b"\x01", sym("wPlayerCurrentlyMoving"): b"\x10", sym("wPlayerSpriteIndex"): b"\x34", sym("wWhichSprite"): b"\x00"}, "expect": {sym("wWhichSprite"): b"\x34"}},
    {"hl": 0x0000, "wram": {sym("wOverworldMode"): b"\x02", sym("wScriptNPC"): b"\x00", sym("wLoadedNPCTempIndex"): b"\xA5", sym("wOverworldNPCFlags"): b"\x00", sym("wNextScript"): b"\x12\x34", sym("wPlayerDirection"): b"\x00", sym("wLoadedNPC1ID"): b"\x4A" + b"\x00" * 95}, "expect": {sym("wOverworldMode"): b"\x03"}},
    {"wram": {sym("wOverworldMode"): b"\x03", sym("wNextScript"): b"\x00\xC0", sym("wDeckToBuild"): b"\xC9"}},
    dict(POISON, wram={sym("wOverworldMode"): b"\x80", sym("wPlayerSpriteIndex"): b"\x56", sym("wOverworldMapPlayerAnimationState"): b"\x00", sym("wWhichSprite"): b"\x00"}, expect={sym("wWhichSprite"): b"\x56"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory HandleOverworldMode

# >>> factory LoadMap
CONTRACT["LoadMap"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LoadMap"] = [
	{"wram": {sym("wTempMap"): b"\x01", sym("wTempPlayerXCoord"): b"\x0E", sym("wTempPlayerYCoord"): b"\x1B", sym("wTempPlayerDirection"): b"\x02"}, "keys": [0x80], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {sym("wGameEvent"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
	dict(POISON, wram={sym("wTempMap"): b"\x01", sym("wTempPlayerXCoord"): b"\x0E", sym("wTempPlayerYCoord"): b"\x1B", sym("wTempPlayerDirection"): b"\x02"}, keys=[0x80], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={sym("wGameEvent"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LoadMap

# >>> factory PCMenu_Print
CONTRACT["PCMenu_Print"] = {"compare": (), "preserve": ()}
CASES["PCMenu_Print"] = [
    {"keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("hSCX"): b"\x55", sym("hSCY"): b"\x66"}, "read": {sym("hSCX"): 1, sym("hSCY"): 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("hSCX"): b"\x55", sym("hSCY"): b"\x66"}, read={sym("hSCX"): 1, sym("hSCY"): 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PCMenu_Print

# >>> factory PCMenu
CONTRACT["PCMenu"] = {"compare": (), "preserve": ()}
CASES["PCMenu"] = [
    # B cancels the menu at once, so the routine runs to its `ret`: the on/off
    # texts, the menu draw, the NPC flags and the song override reset.
    {"keys": [0x00, 0x02], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {sym("wSelectedPCMenuItem"): b"\x00", sym("wSongOverride"): b"\x09", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"}, "read": {sym("wSelectedPCMenuItem"): 1, sym("wSongOverride"): 1, sym("wOverworldMode"): 3, sym("wc600"): 0x400}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={sym("wSelectedPCMenuItem"): b"\x03", sym("wSongOverride"): b"\x09", sym("wLCDC"): b"\x80", 0xFF40: b"\x80"}, read={sym("wSelectedPCMenuItem"): 1, sym("wSongOverride"): 1, sym("wOverworldMode"): 3, sym("wc600"): 0x400}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PCMenu

from tests.cases._schema_migration import legacy_to_schema

# >>> factory Func_c141
# The pending game event is cleared and its handler runs to completion.
# Fixture: Func_c141's entry after the practice duel (GAME_EVENT_DUEL, Dr.
# Mason's lab): the after-duel table names Sam's script and
# SetNextNPCAndScript loads it. Event 0 returns at once. The battle and gift
# centers open link sessions that never return without a peer, so they stay
# uncovered here.
_C141_EVENT = sym("wActiveGameEvent")
_C141_READ = {sym("wNamingScreenDestPointer"): 0x400, _C141_EVENT: 1}
# Only the flags survive the map-script jump (see CallMapScriptPointerIfExists).
CONTRACT["Func_c141"] = {"compare": ("f",), "preserve": ()}
CASES["Func_c141"] = [
    dict(after_duel_fixture(vram=False), read=_C141_READ, **AFTER_DUEL_REGS),
    dict(after_duel_fixture(vram=False, changes={sym("wActiveGameEvent"): b"\x00"}), read=_C141_READ, **POISON),
    dict(POISON, wram={_C141_EVENT: b"\x00"}, read={_C141_EVENT: 1}),
]
# <<< factory Func_c141

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
# >>> factory-mutation BackupObjectPalettes
MUTATIONS["BackupObjectPalettes"] = {
	"source_symbol": "BackupObjectPalettes",
	"before": "CopyDataHLtoDE_SaveRegisters(wObjectPalettesCGB_ADDR, wObjectPalettesCGBBackup_ADDR, 64u);",
	"after": "CopyDataHLtoDE_SaveRegisters(wObjectPalettesCGB_ADDR, wObjectPalettesCGBBackup_ADDR, 63u);",
	"case_ids": ["BackupObjectPalettes-0", "BackupObjectPalettes-1", "BackupObjectPalettes-2"],
}
# <<< factory-mutation BackupObjectPalettes
# >>> factory-mutation AttemptPlayerMovement
MUTATIONS["AttemptPlayerMovement"] = {"source_symbol": "AttemptPlayerMovement", "before": "if (b >= 0x1fu || c >= 0x1fu)", "after": "if (b > 0x1fu || c > 0x1fu)", "case_ids": ["AttemptPlayerMovement-0", "AttemptPlayerMovement-1"]}
# <<< factory-mutation AttemptPlayerMovement
# >>> factory-mutation FindPlayerMovementFromDirection
MUTATIONS["FindPlayerMovementFromDirection"] = {"source_symbol": "FindPlayerMovementFromDirection", "before": "return FindPlayerMovementWithOffset(wPlayerDirection);", "after": "return FindPlayerMovementWithOffset((uint8_t)(wPlayerDirection + 1u));", "case_ids": ["FindPlayerMovementFromDirection-0", "FindPlayerMovementFromDirection-1", "FindPlayerMovementFromDirection-2", "FindPlayerMovementFromDirection-3", "FindPlayerMovementFromDirection-4"]}
# <<< factory-mutation FindPlayerMovementFromDirection
# >>> factory-mutation Func_c1a0
MUTATIONS["Func_c1a0"] = {
    "source_symbol": "Func_c1a0",
    "before": "FrameFunctionResult result = ResetDoFrameFunction(hl);",
    "after": "FrameFunctionResult result = ResetDoFrameFunction((uint16_t)(hl + 1u));",
    "case_ids": ["Func_c1a0-1"],
}
# <<< factory-mutation Func_c1a0
# >>> factory-mutation PauseMenu_Exit
MUTATIONS["PauseMenu_Exit"] = {"source_symbol": "PauseMenu_Exit", "before": "\t_PauseMenu_Exit();", "after": "\twOverworldMode = 1u;", "case_ids": ["PauseMenu_Exit-1"]}
# <<< factory-mutation PauseMenu_Exit
# >>> factory-mutation AttemptPlayerMovementFromDirection
MUTATIONS["AttemptPlayerMovementFromDirection"] = {"source_symbol": "AttemptPlayerMovementFromDirection", "before": "AttemptPlayerMovement(movement.b, movement.c);", "after": "AttemptPlayerMovement(movement.b, (uint8_t)(movement.c + 1u));", "case_ids": ["AttemptPlayerMovementFromDirection-0", "AttemptPlayerMovementFromDirection-1"]}
# <<< factory-mutation AttemptPlayerMovementFromDirection
# >>> factory-mutation Func_c687
MUTATIONS["Func_c687"] = {"source_symbol": "Func_c687", "before": "\tFunc_c694(a, c);", "after": "\tFunc_c694((uint8_t)(a + 1u), c);", "case_ids": ["Func_c687-0", "Func_c687-1", "Func_c687-2", "Func_c687-3"]}
# <<< factory-mutation Func_c687
# >>> factory-mutation Func_c36a
MUTATIONS["Func_c36a"] = {"source_symbol": "Func_c36a", "before": "\twOWMapEvents = 0u;", "after": "\twOWMapEvents = 1u;", "case_ids": ["Func_c36a-0", "Func_c36a-1", "Func_c36a-2"]}
# <<< factory-mutation Func_c36a
# >>> factory-mutation Func_c915
MUTATIONS["Func_c915"] = {"source_symbol": "Func_c915", "before": "FuncC3caResult result = Func_c3ca(b, c, d, e);", "after": "FuncC3caResult result = Func_c3ca(b, c, e, d);", "case_ids": ["Func_c915-0", "Func_c915-1", "Func_c915-2", "Func_c915-3"]}
# <<< factory-mutation Func_c915
# >>> factory-mutation StartScriptedMovement
MUTATIONS["StartScriptedMovement"] = {"source_symbol": "StartScriptedMovement", "before": "	AttemptPlayerMovement(result.b, result.c);", "after": "	AttemptPlayerMovement(result.b, (uint8_t)(result.c + 1u));", "case_ids": ["StartScriptedMovement-0", "StartScriptedMovement-1"]};
# <<< factory-mutation StartScriptedMovement
# >>> factory-mutation RestoreObjectPalettes
MUTATIONS["RestoreObjectPalettes"] = {"source_symbol": "RestoreObjectPalettes", "before": "\twOBP0 = wOBP0Backup;", "after": "\twOBP0 = (uint8_t)(wOBP0Backup + 1u);", "case_ids": ["RestoreObjectPalettes-0", "RestoreObjectPalettes-1", "RestoreObjectPalettes-2"]}
# <<< factory-mutation RestoreObjectPalettes
# >>> factory-mutation Func_c3ff
MUTATIONS["Func_c3ff"] = {
	"source_symbol": "Func_c3ff",
	"before": "wd237 = (uint8_t)(wBGMapWidth - SCREEN_WIDTH);",
	"after": "wd237 = (uint8_t)(wBGMapWidth + SCREEN_WIDTH);",
	"case_ids": ["Func_c3ff-0", "Func_c3ff-1", "Func_c3ff-2", "Func_c3ff-3"],
}
# <<< factory-mutation Func_c3ff
# >>> factory-mutation Func_c49c
MUTATIONS["Func_c49c"] = {
	"source_symbol": "Func_c49c",
	"before": "\twPlayerXCoord = (uint8_t)(wPlayerXCoord & 0x1Fu);",
	"after": "\twPlayerXCoord = (uint8_t)(wPlayerXCoord | 0xE0u);",
	"case_ids": ["Func_c49c-0", "Func_c49c-1", "Func_c49c-2", "Func_c49c-3", "Func_c49c-4"],
}
# <<< factory-mutation Func_c49c
# >>> factory-mutation Func_c58b
MUTATIONS["Func_c58b"] = {"source_symbol": "Func_c58b", "before": "\tgb_write8(hl, flags);", "after": "\tgb_write8(hl, (uint8_t)(flags ^ 0x01u));", "case_ids": ["Func_c58b-0", "Func_c58b-1", "Func_c58b-2"]}
# <<< factory-mutation Func_c58b
# >>> factory-mutation UpdatePlayerSprite
MUTATIONS["UpdatePlayerSprite"] = {"source_symbol": "UpdatePlayerSprite", "before": "void UpdatePlayerSprite(void)\n{\n\twWhichSprite = wPlayerSpriteIndex;", "after": "void UpdatePlayerSprite(void)\n{\n\twWhichSprite = wPlayerDirection;", "case_ids": ["UpdatePlayerSprite-0", "UpdatePlayerSprite-1", "UpdatePlayerSprite-2"]}
# <<< factory-mutation UpdatePlayerSprite
# >>> factory-mutation UpdatePlayerDirection
MUTATIONS["UpdatePlayerDirection"] = {"source_symbol": "UpdatePlayerDirection", "before": "\twPlayerDirection = a;", "after": "\twPlayerDirection = 0;", "case_ids": ["UpdatePlayerDirection-0", "UpdatePlayerDirection-1", "UpdatePlayerDirection-2", "UpdatePlayerDirection-3"]}
# <<< factory-mutation UpdatePlayerDirection
# >>> factory-mutation UpdatePlayerDirectionFromDPad
MUTATIONS["UpdatePlayerDirectionFromDPad"] = {"source_symbol": "UpdatePlayerDirectionFromDPad", "before": "void UpdatePlayerDirectionFromDPad(uint8_t a)\n{\n\tGetDirectionFromDPadResult result = GetDirectionFromDPad(a);\n\tUpdatePlayerDirection(result.a);\n}", "after": "void UpdatePlayerDirectionFromDPad(uint8_t a)\n{\n\tGetDirectionFromDPadResult result = GetDirectionFromDPad(a);\n\tUpdatePlayerDirection(result.f);\n}", "case_ids": ["UpdatePlayerDirectionFromDPad-0", "UpdatePlayerDirectionFromDPad-1", "UpdatePlayerDirectionFromDPad-2", "UpdatePlayerDirectionFromDPad-3", "UpdatePlayerDirectionFromDPad-4"]}
# <<< factory-mutation UpdatePlayerDirectionFromDPad
# >>> factory-mutation SetOverworldDoFrameFunction
MUTATIONS["SetOverworldDoFrameFunction"] = {"source_symbol": "SetOverworldDoFrameFunction", "before": "\t(void)SetDoFrameFunction(OverworldDoFrameFunction_ADDR);", "after": "\t(void)SetDoFrameFunction((uint16_t)(OverworldDoFrameFunction_ADDR + 1u));", "case_ids": ["SetOverworldDoFrameFunction-0", "SetOverworldDoFrameFunction-1"]}
# <<< factory-mutation SetOverworldDoFrameFunction
# >>> factory-mutation Func_c3ee
MUTATIONS["Func_c3ee"] = {"source_symbol": "Func_c3ee", "before": "\t\tgb_write8(hl, (uint8_t)(gb_read8(hl) & (uint8_t)~0x10u));", "after": "\t\tgb_write8(hl, gb_read8(hl));", "case_ids": ["Func_c3ee-0", "Func_c3ee-1"]}
# <<< factory-mutation Func_c3ee
# >>> factory-mutation Func_c66c
MUTATIONS["Func_c66c"] = {"source_symbol": "Func_c66c", "before": "\t\tif (wd338_val >= 2u)\n\t\t\tc = 2u;", "after": "\t\tif (wd338_val >= 3u)\n\t\t\tc = 2u;", "case_ids": ["Func_c66c-2"]}
# <<< factory-mutation Func_c66c
# >>> factory-mutation Func_c4b9
MUTATIONS["Func_c4b9"] = {
    "source_symbol": "Func_c4b9",
    "before": "if (cur_map != OVERWORLD_MAP)\n\t\tdir = wTempPlayerDirection;",
    "after": "if (cur_map == OVERWORLD_MAP)\n\t\tdir = wTempPlayerDirection;",
    "case_ids": ["Func_c4b9-0", "Func_c4b9-1"],
}
# <<< factory-mutation Func_c4b9
# >>> factory-mutation DecompressPermissionMap
MUTATIONS["DecompressPermissionMap"] = {"source_symbol": "DecompressPermissionMap", "before": "\t\tdest = (uint16_t)(dest + 0x10u);", "after": "\t\tdest = (uint16_t)(dest + 0x08u);", "case_ids": ["DecompressPermissionMap-1"]}
# <<< factory-mutation DecompressPermissionMap
# >>> factory-mutation LoadPermissionMap
MUTATIONS["LoadPermissionMap"] = {"source_symbol": "LoadPermissionMap", "before": "gb_write8((uint16_t)(wPermissionMap_ADDR + i), 0x80u);", "after": "gb_write8((uint16_t)(wPermissionMap_ADDR + i), 0x00u);", "case_ids": ["LoadPermissionMap-0", "LoadPermissionMap-1"]}
# <<< factory-mutation LoadPermissionMap
# >>> factory-mutation Func_c1ed
MUTATIONS["Func_c1ed"] = {"source_symbol": "Func_c1ed", "before": "\tLoadBackupSaveData();", "after": "\t(void)0;", "case_ids": ["Func_c1ed-0", "Func_c1ed-1"]}
# <<< factory-mutation Func_c1ed
# >>> factory-mutation Func_c1b1
MUTATIONS["Func_c1b1"] = {"source_symbol": "Func_c1b1", "before": "\twOverworldMapSelection = OWMAP_POKEMON_DOME;", "after": "\twOverworldMapSelection = 0u;", "case_ids": ["Func_c1b1-0", "Func_c1b1-1"]}
# <<< factory-mutation Func_c1b1
# >>> factory-mutation Func_c554
MUTATIONS["Func_c554"] = {"source_symbol": "Func_c554", "before": "\tuint8_t x = (uint8_t)((uint8_t)(wPlayerXCoordPixels - scx) + 8u);", "after": "\tuint8_t x = (uint8_t)((uint8_t)(wPlayerXCoordPixels - scx) + 9u);", "case_ids": ["Func_c554-1"]}
# <<< factory-mutation Func_c554
# >>> factory-mutation Func_c280
MUTATIONS["Func_c280"] = {"source_symbol": "Func_c280", "before": "\tFunc_12871();", "after": "", "case_ids": ["Func_c280-0", "Func_c280-1"]}
# <<< factory-mutation Func_c280
# >>> factory-mutation UpdateOverworldMap
MUTATIONS["UpdateOverworldMap"] = {"source_symbol": "UpdateOverworldMap", "before": "\tOverworldMap_Update();", "after": "\t(void)0;", "case_ids": ["UpdateOverworldMap-0", "UpdateOverworldMap-1", "UpdateOverworldMap-2"]}
# <<< factory-mutation UpdateOverworldMap
# >>> factory-mutation DisplayPauseMenu
MUTATIONS["DisplayPauseMenu"] = {"source_symbol": "DisplayPauseMenu", "before": "\tInitAndPrintMenu(PAUSE_MENU_PARAMS, selected);", "after": "\tInitAndPrintMenu(PAUSE_MENU_PARAMS, (uint8_t)(selected ^ 1u));", "case_ids": ["DisplayPauseMenu-0", "DisplayPauseMenu-1", "DisplayPauseMenu-2"]}
# <<< factory-mutation DisplayPauseMenu
# >>> factory-mutation Func_c8ed
MUTATIONS["Func_c8ed"] = {"source_symbol": "Func_c8ed", "before": "\tgb_write8(wd3b9_ADDR, 0u);", "after": "\tgb_write8(wd3b9_ADDR, 0xFFu);", "case_ids": ["Func_c8ed-1", "Func_c8ed-2"]}
# <<< factory-mutation Func_c8ed
# >>> factory-mutation PauseMenu_Diary
MUTATIONS["PauseMenu_Diary"] = {"source_symbol": "PauseMenu_Diary", "before": "\t_PauseMenu_Diary();", "after": "\twd291 = 0xFFu;", "case_ids": ["PauseMenu_Diary-0", "PauseMenu_Diary-1"]}
# <<< factory-mutation PauseMenu_Diary
# >>> factory-mutation DisplayPCMenu
MUTATIONS["DisplayPCMenu"] = {"source_symbol": "DisplayPCMenu", "before": "\tInitAndPrintMenu(PC_MENU_PARAMS, selected);", "after": "\tInitAndPrintMenu(PC_MENU_PARAMS, (uint8_t)(selected ^ 1u));", "case_ids": ["DisplayPCMenu-0", "DisplayPCMenu-1", "DisplayPCMenu-2"]}
# <<< factory-mutation DisplayPCMenu
# >>> factory-mutation Func_c268
MUTATIONS["Func_c268"] = {
    "source_symbol": "Func_c268",
    "before": "void Func_c268(void)\n{\n\tuint16_t hl = PAUSE_MENU_TEXT_LIST_ADDR;\n\tfor (;;) {\n\t\tconst uint8_t *entry = rom_ptr(PAUSE_MENU_TEXT_LIST_BANK, hl);\n\t\tuint16_t text_id = (uint16_t)(entry[0] | ((uint16_t)entry[1] << 8));\n\t\thl = (uint16_t)(hl + 2u);\n\t\tif (text_id == 0u)\n\t\t\tbreak;\n\t\t(void)ProcessTextFromID(text_id);",
    "after": "void Func_c268(void)\n{\n\tuint16_t hl = PAUSE_MENU_TEXT_LIST_ADDR;\n\tfor (;;) {\n\t\tconst uint8_t *entry = rom_ptr(PAUSE_MENU_TEXT_LIST_BANK, hl);\n\t\tuint16_t text_id = (uint16_t)(entry[0] | ((uint16_t)entry[1] << 8));\n\t\thl = (uint16_t)(hl + 2u);\n\t\tif (text_id == 0u)\n\t\t\tbreak;\n\t\t(void)ProcessTextFromID(0u);",
    "case_ids": ["Func_c268-0", "Func_c268-1"]
}
# <<< factory-mutation Func_c268
# >>> factory-mutation PauseMenu_Status
MUTATIONS["PauseMenu_Status"] = {"source_symbol": "PauseMenu_Status", "before": "\t_PauseMenu_Status();", "after": "\treturn;", "case_ids": ["PauseMenu_Status-0", "PauseMenu_Status-1"]}
# <<< factory-mutation PauseMenu_Status
# >>> factory-mutation Func_c258
MUTATIONS["Func_c258"] = {"source_symbol": "Func_c258", "before": "\tuint8_t saved_hffb0 = hffb0;\n\thffb0 = 2u;", "after": "\tuint8_t saved_hffb0 = hffb0;\n\thffb0 = 1u;", "case_ids": ["Func_c258-0", "Func_c258-1", "Func_c258-2"]}
# <<< factory-mutation Func_c258
# >>> factory-mutation Func_c251
MUTATIONS["Func_c251"] = {"source_symbol": "Func_c251", "before": "/* >>> factory Func_c251 */\nvoid Func_c251(void)\n{\n\tuint8_t saved_hffb0 = hffb0;\n\thffb0 = 1u;", "after": "/* >>> factory Func_c251 */\nvoid Func_c251(void)\n{\n\tuint8_t saved_hffb0 = hffb0;\n\thffb0 = 2u;", "case_ids": ["Func_c251-0", "Func_c251-1", "Func_c251-2"]}
# <<< factory-mutation Func_c251
# >>> factory-mutation Func_c241
MUTATIONS["Func_c241"] = {"source_symbol": "Func_c241", "before": "void Func_c241(void)\n{\n\t(void)SetupText(0x30u, 0x7Fu);", "after": "void Func_c241(void)\n{\n\t(void)SetupText(0x31u, 0x7Fu);", "case_ids": ["Func_c241-0", "Func_c241-1"]}
# <<< factory-mutation Func_c241
# >>> factory-mutation Func_c141
MUTATIONS["Func_c141"] = {"source_symbol": "Func_c141", "before": "\tgb_write8(wActiveGameEvent_ADDR, 0u);", "after": "\tgb_write8(wActiveGameEvent_ADDR, event);", "case_ids": ["Func_c141-0"]}
# <<< factory-mutation Func_c141
# >>> factory-mutation CloseTextBox
MUTATIONS["CloseTextBox"] = {"source_symbol": "CloseTextBox", "before": "\tflags = (uint8_t)(flags & (uint8_t)~(1u << AUTO_CLOSE_TEXTBOX));", "after": "\tflags = (uint8_t)(flags | (uint8_t)(1u << AUTO_CLOSE_TEXTBOX));", "case_ids": ["CloseTextBox-0", "CloseTextBox-1"]}
# <<< factory-mutation CloseTextBox
# >>> factory-mutation Func_c891
MUTATIONS["Func_c891"] = {"source_symbol": "Func_c891", "before": "void Func_c891(uint16_t hl)\n{\n\tif ((wOverworldNPCFlags & (1u << AUTO_CLOSE_TEXTBOX)) != 0u &&\n\t    (wd3b9 != 0u || gb_read8((uint16_t)(wd3b9_ADDR + 1u)) != 0u)) {\n\t\tCloseTextBox();\n\t}\n\twd3b9 = 0u;\n\tgb_write8((uint16_t)(wd3b9_ADDR + 1u), 0u);", "after": "void Func_c891(uint16_t hl)\n{\n\tif ((wOverworldNPCFlags & (1u << AUTO_CLOSE_TEXTBOX)) != 0u &&\n\t    (wd3b9 != 0u || gb_read8((uint16_t)(wd3b9_ADDR + 1u)) != 0u)) {\n\t\tCloseTextBox();\n\t}\n\twd3b9 = 0xFFu;\n\tgb_write8((uint16_t)(wd3b9_ADDR + 1u), 0u);", "case_ids": ["Func_c891-0", "Func_c891-1", "Func_c891-2"]}
# <<< factory-mutation Func_c891
# >>> factory-mutation ReturnToOverworld
MUTATIONS["ReturnToOverworld"] = {"source_symbol": "ReturnToOverworld", "before": "\tcase DISPLAY_PAUSE_MENU:\n\t\tDisplayPauseMenu();\n\t\tbreak;", "after": "\tcase DISPLAY_PAUSE_MENU:\n\t\tbreak;", "case_ids": ["ReturnToOverworld-3"]}
# <<< factory-mutation ReturnToOverworld
# >>> factory-mutation CloseAdvancedDialogueBox
MUTATIONS["CloseAdvancedDialogueBox"] = {"source_symbol": "CloseAdvancedDialogueBox", "before": "\twOverworldNPCFlags = 0u;\n\twOverworldMode = wOverworldModeBackup;", "after": "\twOverworldNPCFlags = 0xFFu;\n\twOverworldMode = wOverworldModeBackup;", "case_ids": ["CloseAdvancedDialogueBox-0", "CloseAdvancedDialogueBox-1", "CloseAdvancedDialogueBox-2"]}
# <<< factory-mutation CloseAdvancedDialogueBox
# >>> factory-mutation Func_c8ba
MUTATIONS["Func_c8ba"] = {"source_symbol": "Func_c8ba", "before": "\twd3b9 = de;", "after": "\twd3b9 = 0xFFu;", "case_ids": ["Func_c8ba-1", "Func_c8ba-2"]}
# <<< factory-mutation Func_c8ba
# >>> factory-mutation ReturnToOverworldNoCallback
MUTATIONS["ReturnToOverworldNoCallback"] = {"source_symbol": "ReturnToOverworldNoCallback", "before": "uint8_t ReturnToOverworldNoCallback(void)\n{\n\twReloadOverworldCallbackPtr = 0u;", "after": "uint8_t ReturnToOverworldNoCallback(void)\n{\n\twReloadOverworldCallbackPtr = 0xFFu;", "case_ids": ["ReturnToOverworldNoCallback-0", "ReturnToOverworldNoCallback-1", "ReturnToOverworldNoCallback-2"]}
# <<< factory-mutation ReturnToOverworldNoCallback
# >>> factory-mutation ReturnToOverworldWithCallback
MUTATIONS["ReturnToOverworldWithCallback"] = {"source_symbol": "ReturnToOverworldWithCallback", "before": "uint8_t ReturnToOverworldWithCallback(uint16_t hl)\n{\n\twReloadOverworldCallbackPtr = (uint8_t)hl;", "after": "uint8_t ReturnToOverworldWithCallback(uint16_t hl)\n{\n\twReloadOverworldCallbackPtr = 0xFFu;", "case_ids": ["ReturnToOverworldWithCallback-0", "ReturnToOverworldWithCallback-1", "ReturnToOverworldWithCallback-2"]}
# <<< factory-mutation ReturnToOverworldWithCallback
# >>> factory-mutation FindNPCOrObject
MUTATIONS["FindNPCOrObject"] = {"source_symbol": "FindNPCOrObject", "before": "\t\t\t\t(uint8_t)(0x10u | (npc.f & 0x80u)),", "after": "\t\t\t\t0x10u,", "case_ids": ["FindNPCOrObject-0", "FindNPCOrObject-1", "FindNPCOrObject-2"]}
# <<< factory-mutation FindNPCOrObject
# >>> factory-mutation Func_c6dc
MUTATIONS["Func_c6dc"] = {"source_symbol": "Func_c6dc", "before": "\twPlayerCurrentlyMoving = (uint8_t)(wPlayerCurrentlyMoving & (uint8_t)~0x03u);", "after": "\twPlayerCurrentlyMoving = (uint8_t)(wPlayerCurrentlyMoving & (uint8_t)~0x01u);", "case_ids": ["Func_c6dc-0", "Func_c6dc-1", "Func_c6dc-3", "Func_c6dc-4"]}
# <<< factory-mutation Func_c6dc
# >>> factory-mutation HandlePlayerMoveModeInput
MUTATIONS["HandlePlayerMoveModeInput"] = {"source_symbol": "HandlePlayerMoveModeInput", "before": "\tif ((hKeysPressed & PAD_A) != 0u) {\n\t\t(void)FindNPCOrObject(1u, 0u, 0u, 0u, 0u, 0u, 0u);", "after": "\tif ((hKeysPressed & PAD_A) == 0u) {\n\t\t(void)FindNPCOrObject(1u, 0u, 0u, 0u, 0u, 0u, 0u);", "case_ids": ["HandlePlayerMoveModeInput-1", "HandlePlayerMoveModeInput-2"]}
# <<< factory-mutation HandlePlayerMoveModeInput
# >>> factory-mutation PCMenu_Glossary
MUTATIONS["PCMenu_Glossary"] = {"source_symbol": "PCMenu_Glossary", "before": "void PCMenu_Glossary(void)\n{\n\t_PCMenu_Glossary();", "after": "void PCMenu_Glossary(void)\n{\n\t(void)0;", "case_ids": ["PCMenu_Glossary-0", "PCMenu_Glossary-1"]}
# <<< factory-mutation PCMenu_Glossary
# >>> factory-mutation Func_c17a
MUTATIONS["Func_c17a"] = {
    "source": "src/home/scripting.c",
    "source_symbol": "CallMapScriptPointerIfExists",
    "before": "\treturn (CallMapScriptResult){entered.a, entered.f, entered.hl};",
    "after": "\treturn (CallMapScriptResult){r.a, entered.f, r.hl};",
    "case_ids": ["Func_c17a-2"],
}
# <<< factory-mutation Func_c17a
# >>> factory-mutation Func_c53d
MUTATIONS["Func_c53d"] = {"source_symbol": "Func_c53d", "before": "void Func_c53d(void)\n{\n\twWhichSprite = wPlayerSpriteIndex;", "after": "void Func_c53d(void)\n{\n\twWhichSprite = (uint8_t)(wPlayerSpriteIndex ^ 0x01u);", "case_ids": ["Func_c53d-0", "Func_c53d-1", "Func_c53d-2"]}
# <<< factory-mutation Func_c53d
# >>> factory-mutation PCMenu_CardAlbum
MUTATIONS["PCMenu_CardAlbum"] = {"source_symbol": "PCMenu_CardAlbum", "before": "void PCMenu_CardAlbum(void)\n{\n\thSCX = 0u;", "after": "void PCMenu_CardAlbum(void)\n{\n\thSCX = 1u;", "case_ids": ["PCMenu_CardAlbum-0", "PCMenu_CardAlbum-1"]}
# <<< factory-mutation PCMenu_CardAlbum
# >>> factory-mutation PauseMenu_Config
MUTATIONS["PauseMenu_Config"] = {"source_symbol": "PauseMenu_Config", "before": "\t_PauseMenu_Config();", "after": "\t(void)0;", "case_ids": ["PauseMenu_Config-0", "PauseMenu_Config-1"]}
# <<< factory-mutation PauseMenu_Config
# >>> factory-mutation PCMenu_ReadMail
MUTATIONS["PCMenu_ReadMail"] = {
	"source_symbol": "PCMenu_ReadMail",
	"before": "uint8_t PCMenu_ReadMail(void)\n{\n\treturn _PCMenu_ReadMail();",
	"after": "uint8_t PCMenu_ReadMail(void)\n{\n\treturn (uint8_t)(_PCMenu_ReadMail() + 1u);",
	"case_ids": ["PCMenu_ReadMail-0", "PCMenu_ReadMail-1", "PCMenu_ReadMail-2"],
}
# <<< factory-mutation PCMenu_ReadMail
# >>> factory-mutation Func_c2a3
MUTATIONS["Func_c2a3"] = {"source_symbol": "Func_c2a3", "before": "void Func_c2a3(void)\n{\n\tBackupObjectPalettes();\n\tFadeScreenToWhite();\n\t(void)SetOverworldNPCFlags(0x80u); /* 1 << HIDE_ALL_NPC_SPRITES, HIDE_ALL_NPC_SPRITES = 7 */", "after": "void Func_c2a3(void)\n{\n\tBackupObjectPalettes();\n\tFadeScreenToWhite();\n\t(void)SetOverworldNPCFlags(0x00u); /* mutated */", "case_ids": ["Func_c2a3-0", "Func_c2a3-1"]}
# <<< factory-mutation Func_c2a3
# >>> factory-mutation PauseMenu_Card
MUTATIONS["PauseMenu_Card"] = {"source_symbol": "PauseMenu_Card", "before": "void PauseMenu_Card(void)\n{\n\thSCX = 0u;", "after": "void PauseMenu_Card(void)\n{\n\thSCX = 1u;", "case_ids": ["PauseMenu_Card-0", "PauseMenu_Card-1"]}
# <<< factory-mutation PauseMenu_Card
# >>> factory-mutation EnterScript
MUTATIONS["EnterScript"] = {"source_symbol": "EnterScript", "before": "\treturn (EnterScriptResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};", "after": "\treturn (EnterScriptResult){(uint8_t)(r.a ^ 1u), r.f, r.b, r.c, r.d, r.e, r.hl};", "case_ids": ["EnterScript-0", "EnterScript-1"]}
# <<< factory-mutation EnterScript
# >>> factory-mutation SetScriptData
MUTATIONS["SetScriptData"] = {"source_symbol": "SetScriptData", "before": "SetScriptDataResult SetScriptData(uint16_t hl)\n{\n\tuint8_t script_npc = wScriptNPC;\n\twLoadedNPCTempIndex = script_npc;\n\tSetNewScriptNPCResult npc = SetNewScriptNPC(hl);\n\twNextScript = npc.c;\n\twNextScript_PTR[1] = npc.b;\n\twOverworldMode = OWMODE_SCRIPT;", "after": "SetScriptDataResult SetScriptData(uint16_t hl)\n{\n\tuint8_t script_npc = wScriptNPC;\n\twLoadedNPCTempIndex = script_npc;\n\tSetNewScriptNPCResult npc = SetNewScriptNPC(hl);\n\twNextScript = npc.c;\n\twNextScript_PTR[1] = npc.b;\n\twOverworldMode = 0u;", "case_ids": ["SetScriptData-0", "SetScriptData-1", "SetScriptData-2"]}
# <<< factory-mutation SetScriptData
# >>> factory-completion SetScriptData
for _record in SCHEMA2_CASES["SetScriptData"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("EnterScript"), "bank": sym_bank("EnterScript")}
# <<< factory-completion SetScriptData
# >>> factory-mutation PauseMenu_Deck
MUTATIONS["PauseMenu_Deck"] = {"source_symbol": "PauseMenu_Deck", "before": "void PauseMenu_Deck(void)\n{\n\thSCX = 0u;", "after": "void PauseMenu_Deck(void)\n{\n\thSCX = 1u;", "case_ids": ["PauseMenu_Deck-0", "PauseMenu_Deck-1"]}
# <<< factory-mutation PauseMenu_Deck
# >>> factory-mutation PauseMenu
MUTATIONS["PauseMenu"] = {"source_symbol": "PauseMenu", "before": "void PauseMenu(void)\n{\n\tPauseSong();\n\tPlaySong(MUSIC_PAUSE_MENU);\n\tDisplayPauseMenu();\n\tfor (;;) {\n\t\t(void)SetOverworldNPCFlags((uint8_t)(1u << AUTO_CLOSE_TEXTBOX));\n\t\tHandleMenuInputResult input;\n\t\tdo {\n\t\t\tDoFrameIfLCDEnabled();\n\t\t\tinput = HandleMenuInput();\n\t\t} while ((input.f & 0x10u) == 0u);\n\t\twSelectedPauseMenuItem = input.e;", "after": "void PauseMenu(void)\n{\n\tPauseSong();\n\tPlaySong(MUSIC_PAUSE_MENU);\n\tDisplayPauseMenu();\n\tfor (;;) {\n\t\t(void)SetOverworldNPCFlags((uint8_t)(1u << AUTO_CLOSE_TEXTBOX));\n\t\tHandleMenuInputResult input;\n\t\tdo {\n\t\t\tDoFrameIfLCDEnabled();\n\t\t\tinput = HandleMenuInput();\n\t\t} while ((input.f & 0x10u) == 0u);\n\t\twSelectedPauseMenuItem = input.a;", "case_ids": ["PauseMenu-0", "PauseMenu-1", "PauseMenu-2"]}
# <<< factory-mutation PauseMenu
# >>> factory-mutation OpenPauseMenu
MUTATIONS["OpenPauseMenu"] = {"source_symbol": "OpenPauseMenu", "before": "\tCloseAdvancedDialogueBox();", "after": "\twSelectedPauseMenuItem = 1u;\n\tCloseAdvancedDialogueBox();", "case_ids": ["OpenPauseMenu-0", "OpenPauseMenu-1"]}
# <<< factory-mutation OpenPauseMenu
# >>> factory-mutation HandlePlayerMoveMode
MUTATIONS["HandlePlayerMoveMode"] = {"source_symbol": "HandlePlayerMoveMode", "before": "void HandlePlayerMoveMode(void)\n{\n\twWhichSprite = wPlayerSpriteIndex;", "after": "void HandlePlayerMoveMode(void)\n{\n\twWhichSprite = 0u;", "case_ids": ["HandlePlayerMoveMode-0", "HandlePlayerMoveMode-1", "HandlePlayerMoveMode-2", "HandlePlayerMoveMode-3", "HandlePlayerMoveMode-4", "HandlePlayerMoveMode-5"]}
# <<< factory-mutation HandlePlayerMoveMode
# >>> factory-mutation CallHandlePlayerMoveMode
MUTATIONS["CallHandlePlayerMoveMode"] = {"source_symbol": "CallHandlePlayerMoveMode", "before": "void CallHandlePlayerMoveMode(void)\n{\n\tHandlePlayerMoveMode();", "after": "void CallHandlePlayerMoveMode(void)\n{\n\treturn;", "case_ids": ["CallHandlePlayerMoveMode-0", "CallHandlePlayerMoveMode-1"]}
# <<< factory-mutation CallHandlePlayerMoveMode
# >>> factory-mutation HandleOverworldMode
MUTATIONS["HandleOverworldMode"] = {"source_symbol": "HandleOverworldMode", "before": "\tuint8_t mode = (uint8_t)(wOverworldMode & 0x7fu);", "after": "\tuint8_t mode = 3u;", "case_ids": ["HandleOverworldMode-4"]}
# <<< factory-mutation HandleOverworldMode
# >>> factory-mutation LoadMap
MUTATIONS["LoadMap"] = {"source_symbol": "LoadMap", "before": "\twGameEvent = GAME_EVENT_OVERWORLD;", "after": "\twGameEvent = 0x01u;", "case_ids": ["LoadMap-0", "LoadMap-1"]}
# <<< factory-mutation LoadMap
# >>> factory-completion LoadMap
for _record in SCHEMA2_CASES["LoadMap"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("DrawSpriteAnimationFrame.finishYPosition") + 4}
# <<< factory-completion LoadMap
# >>> factory-mutation PCMenu_Print
MUTATIONS["PCMenu_Print"] = {"source_symbol": "PCMenu_Print", "before": "void PCMenu_Print(void)\n{\n\thSCX = 0u;", "after": "void PCMenu_Print(void)\n{\n\thSCX = 1u;", "case_ids": ["PCMenu_Print-0", "PCMenu_Print-1"]}
# <<< factory-mutation PCMenu_Print
# >>> factory-completion PCMenu_Print
for _record in SCHEMA2_CASES["PCMenu_Print"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("DoFrame.done") + 2}
# <<< factory-completion PCMenu_Print
# >>> factory-mutation PCMenu
MUTATIONS["PCMenu"] = {"source_symbol": "PCMenu", "before": "\tFunc_c891(TurnedPCOffText);", "after": "\tFunc_c891(TurnedPCOnText);", "case_ids": ["PCMenu-0", "PCMenu-1"]}
# <<< factory-mutation PCMenu
