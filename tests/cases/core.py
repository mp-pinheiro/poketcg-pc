"""Oracle-diff cases for poketcg/src/engine/duel/core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory SetLineSeparation
CONTRACT["SetLineSeparation"] = {"compare": ("a",), "preserve": ()}
wLineSeparation = 0xCD08
CASES["SetLineSeparation"] = [
	{"a": 0, "wram": {wLineSeparation: b"\xff"}},
	{"a": 1, "wram": {wLineSeparation: b"\x00"}},
	dict(POISON, a=0x20, wram={wLineSeparation: b"\x00"}),
]
# <<< factory SetLineSeparation

# >>> factory PlayAreaScreenMenuFunction
CONTRACT["PlayAreaScreenMenuFunction"] = {"compare": ("f",), "preserve": ()}
CASES["PlayAreaScreenMenuFunction"] = [
    {"keys": 0},
    {"keys": 0x01},
    {"keys": 0x02},
    {"keys": 0x08},
    dict(POISON, keys=0x02),
    dict(POISON, keys=0x00),
]
# <<< factory PlayAreaScreenMenuFunction

# >>> factory SwitchAttackPage
CONTRACT["SwitchAttackPage"] = {"compare": (), "preserve": ()}
CASES["SwitchAttackPage"] = [
	{"wram": {0xCC04: b"\x00"}, "read": {0xCC04: 1}},
	{"wram": {0xCC04: b"\x01"}, "read": {0xCC04: 1}},
	dict(POISON, wram={0xCC04: b"\xff"}, read={0xCC04: 1}),
]
# <<< factory SwitchAttackPage

# >>> factory CopyCGBCardPalette
CONTRACT["CopyCGBCardPalette"] = {"compare": (), "preserve": ()}
CASES["CopyCGBCardPalette"] = [
    {"wram": {0xCE23: bytes(range(8))}, "read": {0xCAF0: 8}},
    dict(POISON, a=2, wram={0xCE23: bytes(range(0x10, 0x18))},
         read={0xCAF0 + 16: 8}),
]
# <<< factory CopyCGBCardPalette

# >>> factory CreateCardAttrBlkPacket
CONTRACT["CreateCardAttrBlkPacket"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["CreateCardAttrBlkPacket"] = [
    {"wram": {0xCAE0: b"\xAA" * 32}, "read": {0xCAE0: 32}},
    dict(POISON, a=0, d=0, e=0, wram={0xCAE0: b"\xAA" * 32}, read={0xCAE0: 32}),
    {"a": 1, "d": 2, "e": 3, "wram": {0xCAE0: b"\x55" * 32}, "read": {0xCAE0: 32}},
]
# <<< factory CreateCardAttrBlkPacket
# >>> factory CreateCardAttrBlkPacket_DataSet
CONTRACT["CreateCardAttrBlkPacket_DataSet"] = {"compare": ("hl",), "preserve": ()}
CASES["CreateCardAttrBlkPacket_DataSet"] = [
	{"hl": 0xC100, "a": 0, "d": 0, "e": 0,
	 "wram": {0xC100: b"\x00" * 6}, "read": {0xC100: 6}},
	dict(POISON, hl=0xC100, wram={0xC100: b"\x00" * 6}, read={0xC100: 6}),
	{"hl": 0xC100, "a": 0x12, "d": 0x30, "e": 0x40,
	 "wram": {0xC100: b"\x00" * 6}, "read": {0xC100: 6}},
]
# <<< factory CreateCardAttrBlkPacket_DataSet


# >>> factory SaveDuelDataToDE
CONTRACT["SaveDuelDataToDE"] = {"compare": (), "preserve": ()}
sCurrentDuel = 0xBC00
sCurrentDuelData = 0xBC04
wDuelType = 0xCC09
wPlayerDuelVariables = 0xC200
CASES["SaveDuelDataToDE"] = [
	{"d": 0xBC, "e": 0x00, "wram": {wDuelType: b"\x02"}, "sread": {0: {sCurrentDuel: 4}}},
	dict(POISON, d=0xBC, e=0x00, wram={wDuelType: b"\x03", wPlayerDuelVariables: b"\x11\x22"}),
	{"d": 0xBC, "e": 0x00, "wram": {wDuelType: b"\x00"}, "sread": {0: {sCurrentDuel: 1}}},
]
# <<< factory SaveDuelDataToDE

# >>> factory LoadSavedDuelDataFromDE
CONTRACT["LoadSavedDuelDataFromDE"] = {"compare": (), "preserve": ()}
sCurrentDuelData = 0xBC04
wPlayerDuelVariables = 0xC200
hWhoseTurn = 0xFF97
CASES["LoadSavedDuelDataFromDE"] = [
	{"d": 0xBC, "e": 0x00, "sram": {0: {sCurrentDuelData: bytes(range(0, 4))}},
	 "read": {wPlayerDuelVariables: 4}},
	dict(POISON, d=0xBC, e=0x00, sram={0: {sCurrentDuelData: bytes([0xAA, 0xBB])}}),
	{"d": 0xBC, "e": 0x00, "sram": {0: {sCurrentDuelData: b"\x00" * 4}},
	 "read": {wPlayerDuelVariables: 4}},
]
# <<< factory LoadSavedDuelDataFromDE

# >>> factory SetBGP7OrSGB2ToCardPalette
CONTRACT["SetBGP7OrSGB2ToCardPalette"] = {"compare": (), "preserve": ()}
CASES["SetBGP7OrSGB2ToCardPalette"] = [
	{"wram": {0xCAB4: bytes([0x00])}},
	{"wram": {0xCAB4: bytes([0x01]), 0xCE23: bytes([0x11, 0x22, 0x33, 0x44])},
	 "read": {0xCAE1: 4}},
	dict(POISON, wram={0xCAB4: bytes([0x02])}),
]
# <<< factory SetBGP7OrSGB2ToCardPalette

# >>> factory JPWriteByteToBGMap0
CONTRACT["JPWriteByteToBGMap0"] = {"compare": (), "preserve": ()}
CASES["JPWriteByteToBGMap0"] = [
	{"a": 0x41, "b": 0, "c": 0, "read": {0x9800: 1}},
	dict(POISON, a=0x50, b=5, c=3, read={0x9800 + 3 * 32 + 5: 1}),
]
# <<< factory JPWriteByteToBGMap0


# >>> factory ZeroObjectPositionsAndToggleOAMCopy
wVBlankOAMCopyToggle = 0xCAC0
CONTRACT["ZeroObjectPositionsAndToggleOAMCopy"] = {"compare": (), "preserve": ()}
CASES["ZeroObjectPositionsAndToggleOAMCopy"] = [
	{"wram": {wVBlankOAMCopyToggle: b"\x00"}},
	dict(POISON, wram={wVBlankOAMCopyToggle: b"\xFF"}),
]
# <<< factory ZeroObjectPositionsAndToggleOAMCopy

# >>> factory LoadPlayerDeck
CONTRACT["LoadPlayerDeck"] = {"compare": (), "preserve": ()}
sCurrentlySelectedDeck_ = 0xB700
sDeck1Cards_ = 0xA218
wPlayerDeck_ = 0xC400
CASES["LoadPlayerDeck"] = [
    {"sram": {0: {sCurrentlySelectedDeck_: b"\x00", sDeck1Cards_: bytes(range(60))}},
     "read": {wPlayerDeck_: 60}},
    dict(POISON, sram={0: {sCurrentlySelectedDeck_: b"\x01", sDeck1Cards_: bytes(range(60)), sDeck1Cards_ + 60: bytes(range(60))}},
         read={wPlayerDeck_: 60}),
    {"sram": {0: {sCurrentlySelectedDeck_: b"\x00", sDeck1Cards_: bytes([0xFF] * 60)}},
     "read": {wPlayerDeck_: 60}},
    {"sram": {0: {sCurrentlySelectedDeck_: b"\x01", sDeck1Cards_: bytes([1] * 60), sDeck1Cards_ + 60: bytes([2] * 60)}},
     "read": {wPlayerDeck_: 60}},
    {"ramg": False, "sram": {0: {sCurrentlySelectedDeck_: b"\x00", sDeck1Cards_: bytes(range(60))}},
     "read": {wPlayerDeck_: 60}},
]
# <<< factory LoadPlayerDeck
# >>> factory CheckSkipDelayAllowed
CONTRACT["CheckSkipDelayAllowed"] = {"compare": ("f", "b", "c", "d", "e", "hl"), "preserve": ()}
wSkipDelayAllowed_ = 0xCCF2
hKeysHeld_ = 0xFF90
CASES["CheckSkipDelayAllowed"] = [
    {"wram": {wSkipDelayAllowed_: b"\x00", hKeysHeld_: b"\x02"}},
    {"wram": {wSkipDelayAllowed_: b"\x01", hKeysHeld_: b"\x00"}},
    {"wram": {wSkipDelayAllowed_: b"\x01", hKeysHeld_: b"\x02"}},
    dict(POISON, wram={wSkipDelayAllowed_: b"\xff", hKeysHeld_: b"\xff"}),
]
# <<< factory CheckSkipDelayAllowed

# >>> factory AIMakeDecision
CONTRACT["AIMakeDecision"] = {"compare": ("f",), "preserve": ()}
hOppActionTableIndex_ = 0xFF9E
wSkipDuelistIsThinkingDelay_ = 0xCBF9
wVBlankCounter_ = 0xCAB8
wOpponentTurnEnded_ = 0xCBE1
wDuelFinished_ = 0xCC07
CASES["AIMakeDecision"] = [
    {"a": 0x08, "wram": {
        hOppActionTableIndex_: b"\x00",
        wSkipDuelistIsThinkingDelay_: b"\x01",
        wVBlankCounter_: b"\x01",
        wOpponentTurnEnded_: b"\x00",
        wDuelFinished_: b"\x00",
    }},
    dict(POISON, a=0x08, wram={
        hOppActionTableIndex_: b"\x00",
        wSkipDuelistIsThinkingDelay_: b"\x01",
        wVBlankCounter_: b"\x01",
        wOpponentTurnEnded_: b"\x00",
        wDuelFinished_: b"\x00",
    }),
    {"a": 0x08, "wram": {
        hOppActionTableIndex_: b"\x00",
        wSkipDuelistIsThinkingDelay_: b"\x01",
        wVBlankCounter_: b"\x01",
        wOpponentTurnEnded_: b"\x00",
        wDuelFinished_: b"\x00",
    }},
]
# <<< factory AIMakeDecision

# >>> factory PrintPracticeDuelDrMasonInstructions
CONTRACT["PrintPracticeDuelDrMasonInstructions"] = {"compare": ("a", "f"), "preserve": ("a", "f")}
CASES["PrintPracticeDuelDrMasonInstructions"] = [
    {"hl": 0x01DB, "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, hl=0x01DC, keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory PrintPracticeDuelDrMasonInstructions

# >>> factory PrintPracticeDuelInstructionsTextBoxLabel
CONTRACT["PrintPracticeDuelInstructionsTextBoxLabel"] = {"compare": (), "preserve": ()}
CASES["PrintPracticeDuelInstructionsTextBoxLabel"] = [
    {"wram": {0xCC06: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    {"wram": {0xCC06: b"\x07"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, wram={0xCC06: b"\x06"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory PrintPracticeDuelInstructionsTextBoxLabel

# >>> factory SwitchCardPage
CONTRACT["SwitchCardPage"] = {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["SwitchCardPage"] = [
    {"a": 0},
    dict(POISON, a=0, f=0),
]
# <<< factory SwitchCardPage



# >>> factory CardPageSwitch_00
CONTRACT["CardPageSwitch_00"] = {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_00"] = [
    {},
    dict(POISON, f=0),
]
# <<< factory CardPageSwitch_00



# >>> factory LoadLoaded1CardGfx
CONTRACT["LoadLoaded1CardGfx"] = {"compare": (), "preserve": ()}
CASES["LoadLoaded1CardGfx"] = [
    {"d": 0x88, "e": 0x00, "wram": {0xCC25: b"\xA7\x02"}, "vread": {0: {0x8800: 0x300}}},
    {"d": 0x90, "e": 0x00, "wram": {0xCC25: b"\x00\x18"}, "vread": {0: {0x9000: 0x300}}},
    dict(POISON, d=0x88, e=0x00, wram={0xCC25: b"\xA7\x02"}, vread={0: {0x8800: 0x300}}),
]
# <<< factory LoadLoaded1CardGfx

# >>> factory SetSGB3ToCardPalette
CONTRACT["SetSGB3ToCardPalette"] = {"compare": (), "preserve": ()}
CASES["SetSGB3ToCardPalette"] = [
	{"wram": {0xCE25: b"\x00\x00\x00\x00\x00\x00", 0xCAE9: b"\xAA\xAA\xAA\xAA\xAA\xAA"}, "read": {0xCE25: 6}},
	dict(POISON, wram={0xCE25: b"\x01\x23\x45\x67\x89\xAB", 0xCAE9: b"\xAA\xAA\xAA\xAA\xAA\xAA"}, read={0xCE25: 6}),
	{"wram": {0xCE25: b"\xFF\x80\x7F\x01\xFE\x02", 0xCAE9: b"\x00\x00\x00\x00\x00\x00"}, "read": {0xCE25: 6}},
]
# <<< factory SetSGB3ToCardPalette


# >>> factory LookForCardIDInPlayArea_Bank5
CONTRACT["LookForCardIDInPlayArea_Bank5"] = {"compare": ("a", "f", "b", "d", "e"), "preserve": ("d", "e")}
CASES["LookForCardIDInPlayArea_Bank5"] = [
    {"a": 0, "b": 0, "read": {0xCDD4: 1}},
    {"a": 1, "b": 0, "read": {0xCDD4: 1}},
    {"a": 0x08, "b": 3, "read": {0xCDD4: 1}},
    {"a": 0x20, "b": 5, "read": {0xCDD4: 1}},
    {"a": 0xFF, "b": 0, "read": {0xCDD4: 1}},
    dict(POISON, a=0x08, b=0, read={0xCDD4: 1}),
]
# <<< factory LookForCardIDInPlayArea_Bank5

# >>> factory ClearMemory_Bank5
CONTRACT["ClearMemory_Bank5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClearMemory_Bank5"] = [
    {"a": 0, "hl": 0xC300, "wram": {0xC300: b"\xaa" * 0x101}},
    {"a": 1, "hl": 0xC300, "wram": {0xC300: b"\xaa\xbb"}},
    {"a": 8, "hl": 0xC400, "wram": {0xC400: b"\x55" * 9}},
    dict(POISON, a=4, hl=0xC300, wram={0xC300: b"\xaa" * 5}),
]
# <<< factory ClearMemory_Bank5

# >>> factory CheckCardPageExists
CONTRACT["CheckCardPageExists"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["CheckCardPageExists"] = [
    {"hl": 0xC100, "wram": {0xC100: b"\x00\x00"}},
    {"hl": 0xC100, "wram": {0xC100: b"\x0F\xF0"}},
    {"hl": 0xC100, "wram": {0xC100: b"\x00\x01"}},
    {"hl": 0xC100, "wram": {0xC100: b"\x80\x00"}},
    dict(POISON, hl=0xC200, wram={0xC200: b"\x12\x34"}),
]
# <<< factory CheckCardPageExists


# >>> factory CardPageSwitch_PokemonEnd
CONTRACT["CardPageSwitch_PokemonEnd"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CardPageSwitch_PokemonEnd"] = [
    {},
    dict(POISON),
    {"f": 0x80},
]
# <<< factory CardPageSwitch_PokemonEnd


# >>> factory SetCardListInfoBoxText
CONTRACT["SetCardListInfoBoxText"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetCardListInfoBoxText"] = [
    {"hl": 0x0000, "read": {0xCBDA: 2}},
    {"hl": 0x1234, "read": {0xCBDA: 2}},
    dict(POISON, hl=0xBEEF, wram={0xCBDA: b"\x00\x00"}, read={0xCBDA: 2}),
]
# <<< factory SetCardListInfoBoxText

# >>> factory PrintCardListHeaderAndInfoBoxTexts
CONTRACT["PrintCardListHeaderAndInfoBoxTexts"] = {"compare": (), "preserve": ()}
CASES["PrintCardListHeaderAndInfoBoxTexts"] = [
    {"wram": {0xCBDA: b"\x00\x00", 0xCBDC: b"\x00\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, wram={0xCBDA: b"\x00\x00", 0xCBDC: b"\x00\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintCardListHeaderAndInfoBoxTexts


# >>> factory LoadCardNameToTxRam2
CONTRACT["LoadCardNameToTxRam2"] = {"compare": (), "preserve": ()}
CASES["LoadCardNameToTxRam2"] = [
    {"a": 0, "wram": {0xCE3F: b"\xaa\xaa\xaa\xaa"}, "read": {0xCC24: 0x41, 0xCE3F: 4}},
    {"a": 0x10, "wram": {0xCE3F: b"\x55\x55\x55\x55"}, "read": {0xCC24: 0x41, 0xCE3F: 4}},
    {"a": 0x3B, "wram": {0xCE3F: b"\xaa\xaa\xaa\xaa"}, "read": {0xCC24: 0x41, 0xCE3F: 4}},
    dict(POISON, a=0x20, wram={0xCE3F: b"\xaa\xaa\xaa\xaa"}, read={0xCC24: 0x41, 0xCE3F: 4}),
]
# <<< factory LoadCardNameToTxRam2




# >>> factory LoadCardNameToTxRam2_b
CONTRACT["LoadCardNameToTxRam2_b"] = {"compare": ("a",), "preserve": ()}
CASES["LoadCardNameToTxRam2_b"] = [
    {"a": 0, "wram": {0xCE41: b"\x00\x00"}},
    {"a": 0, "wram": {0xCE41: b"\xAA\xAA"}, "read": {0xCC27: 2}},
    {"a": 1, "wram": {0xCE41: b"\xAA\xAA"}, "read": {0xCC27: 2}},
    dict(POISON, a=0x3B, wram={0xCE41: b"\xAA\xAA"}, read={0xCC27: 2}),
]
# <<< factory LoadCardNameToTxRam2_b




# >>> factory GetAnimCoordsAndFlags
wAnimFlags = 0xD42B
wDuelAnimationScreen = 0xD4AE
wDuelAnimDuelistSide = 0xD4AF
wDuelAnimLocationParam = 0xD4B0
CONTRACT["GetAnimCoordsAndFlags"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetAnimCoordsAndFlags"] = [
    {"wram": {wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x00", wDuelAnimDuelistSide: b"\x00", wDuelAnimLocationParam: b"\x00"}},
    dict(POISON, wram={wAnimFlags: b"\x04", wDuelAnimationScreen: b"\x00", wDuelAnimDuelistSide: b"\x00", wDuelAnimLocationParam: b"\x00"}),
    {"wram": {wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x01", wDuelAnimDuelistSide: b"\xc2", wDuelAnimLocationParam: b"\x03"}},
    {"wram": {wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x02", wDuelAnimDuelistSide: b"\xc3", wDuelAnimLocationParam: b"\x05"}},
    {"wram": {wAnimFlags: b"\x0c", wDuelAnimationScreen: b"\x00", wDuelAnimDuelistSide: b"\x00", wDuelAnimLocationParam: b"\x00"}},
    {"wram": {wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x00", wDuelAnimDuelistSide: b"\xc2", wDuelAnimLocationParam: b"\x00"}},
]
# <<< factory GetAnimCoordsAndFlags


# >>> factory PlayBufferedDuelAnimations
wDuelAnimBufferCurPos = 0xD4AC
wDuelAnimBufferSize = 0xD4AD
wDuelAnimBuffer = 0xD42C
wActiveScreenAnim = 0xD42A
wAnimationQueue = 0xD423
wd4c0 = 0xD4C0
CONTRACT["PlayBufferedDuelAnimations"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PlayBufferedDuelAnimations"] = [
    {"wram": {wDuelAnimBufferCurPos: b"\x05", wDuelAnimBufferSize: b"\x05"}},
    dict(POISON, wram={wDuelAnimBufferCurPos: b"\x09", wDuelAnimBufferSize: b"\x09"}),
    {"wram": {
        wDuelAnimBufferCurPos: b"\x00", wDuelAnimBufferSize: b"\x08",
        wDuelAnimBuffer: bytes([0x05, 0x01, 0xc2, 0x02, 0x10, 0x00, 0x00, 0x07]),
        wActiveScreenAnim: b"\x00", wd4c0: b"\x00", wAnimationQueue: b"\x00" * 7,
    }},
    {"wram": {
        wDuelAnimBufferCurPos: b"\x78", wDuelAnimBufferSize: b"\x7f",
        wDuelAnimBuffer + 120: bytes([0x02, 0x00, 0xc3, 0x01, 0x00, 0x00, 0x00, 0x01]),
        wActiveScreenAnim: b"\x00", wd4c0: b"\x00", wAnimationQueue: b"\x00" * 7,
    }},
    {"wram": {
        wDuelAnimBufferCurPos: b"\x00", wDuelAnimBufferSize: b"\x08",
        wDuelAnimBuffer: bytes([0x01, 0x00, 0xc2, 0x00, 0x00, 0x00, 0x00, 0x07]),
        wActiveScreenAnim: b"\xff", wd4c0: b"\xff", wAnimationQueue: b"\xff" * 7,
    }},
]
# <<< factory PlayBufferedDuelAnimations

# >>> factory ReturnWrongAction
CONTRACT["ReturnWrongAction"] = {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["ReturnWrongAction"] = [
    {},
    {"f": 0x80},
    dict(POISON, f=0xF0),
]
# <<< factory ReturnWrongAction


# >>> factory CopyListWithFFTerminatorFromHLToDE_Bank5
CONTRACT["CopyListWithFFTerminatorFromHLToDE_Bank5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["CopyListWithFFTerminatorFromHLToDE_Bank5"] = [
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\xFF"}, "read": {0xC100: 1, 0xC200: 1}},
    dict(POISON, hl=0xC100, d=0xC2, e=0x00, wram={0xC100: b"\x01\x02\xFF"}, read={0xC100: 3, 0xC200: 3}),
    {"hl": 0xC1FF, "d": 0xC2, "e": 0xFF, "wram": {0xC1FF: b"\x01\xFF"}, "read": {0xC1FF: 2, 0xC2FF: 2}},
]
# <<< factory CopyListWithFFTerminatorFromHLToDE_Bank5

# >>> factory CheckEnergyFlagsNeededInList
CONTRACT["CheckEnergyFlagsNeededInList"] = {"compare": ("a", "f", "b", "c"), "preserve": ("b", "c")}
CASES["CheckEnergyFlagsNeededInList"] = [
    {"a": 0, "wram": {0xC510: b"\xFF"}, "read": {0xC510: 1}},
    dict(POISON, a=0, wram={0xC510: b"\xFF"}, read={0xC510: 1}),
    {"a": 1, "wram": {0xC510: b"\xFF"}, "read": {0xC510: 1}},
    {"a": 0xFF, "wram": {0xC510: b"\xFF"}, "read": {0xC510: 1}},
]
# <<< factory CheckEnergyFlagsNeededInList

# >>> factory CardPageSwitch_EnergyEnd
CONTRACT["CardPageSwitch_EnergyEnd"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CardPageSwitch_EnergyEnd"] = [{"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}, {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}]
# <<< factory CardPageSwitch_EnergyEnd

# >>> factory CardPageSwitch_0c
CONTRACT["CardPageSwitch_0c"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CardPageSwitch_0c"] = [{"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}, {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}]
# <<< factory CardPageSwitch_0c

# >>> factory PlaceCardImageOAM
CONTRACT["PlaceCardImageOAM"] = {"compare": ("a", "d", "e", "hl"), "preserve": ("e",)}
CASES["PlaceCardImageOAM"] = [
    {"wram": {0xCAC0: b"\x00"}, "read": {0xCAC0: 1}},
    dict(POISON, hl=0x1234, d=0x20, e=0x30, wram={0xCAC0: b"\x00"}, read={0xCAC0: 1}),
]
# <<< factory PlaceCardImageOAM

# >>> factory PrintPlayAreaCardAttachedEnergies
CONTRACT["PrintPlayAreaCardAttachedEnergies"] = {"compare": (), "preserve": ()}
CASES["PrintPlayAreaCardAttachedEnergies"] = [
    {"read": {0xC590: 8}, "vread": {0: {0x9800: 8}}},
    dict(POISON, read={0xC590: 8}, vread={0: {0x9800: 8}}),
    {"b": 2, "c": 3, "e": 1,
     "read": {0xC590: 8}, "vread": {0: {0x9862: 8}}},
]
# <<< factory PrintPlayAreaCardAttachedEnergies

# >>> factory DiscardRetreatCostCards
CONTRACT["DiscardRetreatCostCards"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["DiscardRetreatCostCards"] = [
    {"wram": {0xFFA2: b"\xFF"}},
    dict(POISON, wram={0xFFA2: b"\x00\xFF"}),
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5,
     "wram": {0xFFA2: b"\x01\x02\x03\xFF"}},
]
# <<< factory DiscardRetreatCostCards


# >>> factory OppAction_DrawCard
CONTRACT["OppAction_DrawCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["OppAction_DrawCard"] = [{}, dict(POISON), {"a": 1, "f": 0x10, "b": 1, "c": 2, "d": 3, "e": 4, "hl": 0xC100}]
# <<< factory OppAction_DrawCard

# >>> factory PrintSortNumberInCardList
CONTRACT["PrintSortNumberInCardList_SetPointer"] = {"compare": (), "preserve": ()}
CASES["PrintSortNumberInCardList_SetPointer"] = [
	{"wram": {0xCBD8: b"\x00\x00", 0xCBDF: b"\x00"}, "read": {0xCBD8: 3}},
	dict(POISON, wram={0xCBD8: b"\xff\xff", 0xCBDF: b"\x00"}, read={0xCBD8: 3}),
]
# <<< factory PrintSortNumberInCardList
# >>> factory PrintSortNumberInCardList_body
CONTRACT["PrintSortNumberInCardList"] = {"compare": (), "preserve": ()}
CASES["PrintSortNumberInCardList"] = [
	{"wram": {0xC51A: b"\x00\x01\xff"}, "read": {0x9841: 2}},
	dict(POISON, wram={0xC51A: b"\x01\x00\xff"}, read={0x9841: 2}),
	{"wram": {0xC51A: b"\xff"}},
]
# <<< factory PrintSortNumberInCardList_body


# >>> factory PrintEnergiesOfColor
CONTRACT["PrintEnergiesOfColor"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("c", "d", "hl")}
CASES["PrintEnergiesOfColor"] = [
    {},
    dict(POISON, a=0, read={}),
    {"a": 1, "b": 0, "c": 0, "e": 0x20, "read": {0x9800: 1}},
    {"a": 2, "b": 0, "c": 0, "e": 0x30, "read": {0x9800: 2}},
    dict(POISON, a=0x0F, b=0, c=0, e=0x40, read={0x9800: 15}),
]
# <<< factory PrintEnergiesOfColor

# >>> factory PrintCardPageWeaknessesOrResistances
CONTRACT["PrintCardPageWeaknessesOrResistances"] = {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["PrintCardPageWeaknessesOrResistances"] = [
    {"read": {0x9800: 0x400}},
    dict(POISON, a=0x80, b=0, c=0, read={0x9800: 0x400}),
    dict(POISON, a=0xAA, b=1, c=1, read={0x9800: 0x400}),
    {"a": 0x40, "b": 2, "c": 3, "read": {0x9800: 0x400}},
    {"a": 0xC0, "b": 0x1F, "c": 2, "read": {0x9800: 0x400}},
]
# <<< factory PrintCardPageWeaknessesOrResistances

# >>> factory Func_6423
CONTRACT["Func_6423"] = {"compare": ("a", "b", "c", "d", "hl"), "preserve": ("c", "d")}
CASES["Func_6423"] = [
    {"wram": {0xC590: b"\x00\x00\x00\x00\x00\x00\x00\x00"}},
    dict(POISON, wram={0xC590: b"\x01\x23\x45\x67\x89\xAB\xCD\xEF"}),
    {"b": 1, "c": 2, "wram": {0xC590: b"\x10\x20\x30\x40\x50\x60\x70\x80"}},
]
# <<< factory Func_6423

# >>> factory InitVariablesToBeginDuel
CONTRACT["InitVariablesToBeginDuel"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["InitVariablesToBeginDuel"] = [
    {"sram": {0: {0xA009: b"\x12"}},
     "sread": {0: {0xA009: 1}}},
    dict(POISON,
         wram={0xCC07: b"\xAA", 0xCC06: b"\xAA", 0xCCE7: b"\xAA",
               0xCC0F: b"\x55", 0xCC11: b"\x44", 0xCC10: b"\x44",
               0xCCF2: b"\x99", 0xC2F1: b"\x80", 0xC3F1: b"\x55",
               0xCC09: b"\x77"},
         sram={0: {0xA009: b"\xA5"}},
         sread={0: {0xA009: 1}}),
    {"wram": {0xC2F1: b"\x01"}, "sram": {0: {0xA009: b"\x01"}}},
    {"wram": {0xC2F1: b"\x80"}, "sram": {0: {0xA009: b"\x02"}}},
    {"wram": {0xC2F1: b"\x00", 0xC3F1: b"\x01"},
     "sram": {0: {0xA009: b"\x03"}}},
    {"wram": {0xC2F1: b"\x00", 0xC3F1: b"\x80"},
     "sram": {0: {0xA009: b"\x04"}}},
    {"wram": {0xC2F1: b"\x02", 0xC3F1: b"\x03"},
     "sram": {0: {0xA009: b"\x05"}}},
]
# <<< factory InitVariablesToBeginDuel

# >>> factory CardPageSwitch_PokemonAttack1Page2
CONTRACT["CardPageSwitch_PokemonAttack1Page2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_PokemonAttack1Page2"] = [
    {},
    dict(POISON, wram={0xCC36: b"\x00\x00\x01", 0xCC47: b"\x00"}),
    {"wram": {0xCC36: b"\x00\x00\x00", 0xCC47: b"\x01"}},
]
# <<< factory CardPageSwitch_PokemonAttack1Page2

# >>> factory CardPageSwitch_PokemonAttack2Page1
CONTRACT["CardPageSwitch_PokemonAttack2Page1"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_PokemonAttack2Page1"] = [
	{"wram": {0xCC36: b"\x00\x00\x00\x00", 0xCC47: b"\x00\x00\x00\x00"}},
	{"wram": {0xCC36: b"\x11\x22\x33\x44", 0xCC47: b"\x00\x00\x00\x00"}},
	{"wram": {0xCC36: b"\x00\x00\x00\x00", 0xCC47: b"\x11\x22\x33\x44"}},
	dict(POISON, wram={0xCC36: b"\xAA\xBB\xCC\xDD", 0xCC47: b"\x00\x00\x00\x00"}),
	{"b": 1, "c": 2, "d": 3, "e": 4, "wram": {0xCC36: b"\x55\x66\x77\x88", 0xCC47: b"\x99\xAA\xBB\xCC"}},
]
# <<< factory CardPageSwitch_PokemonAttack2Page1

# >>> factory AIDiscourage
CONTRACT["AIDiscourage"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["AIDiscourage"] = [
    {"wram": {0xCDBE: b"\x00"}, "read": {0xCDBE: 1}},
    dict(POISON, wram={0xCDBE: b"\x40"}, read={0xCDBE: 1}),
    {"a": 1, "wram": {0xCDBE: b"\x01"}, "read": {0xCDBE: 1}},
    {"a": 2, "wram": {0xCDBE: b"\x01"}, "read": {0xCDBE: 1}},
    {"a": 1, "wram": {0xCDBE: b"\xFF"}, "read": {0xCDBE: 1}},
]
# <<< factory AIDiscourage

# >>> factory ConvertHPToDamageCounters_Bank5
CONTRACT["ConvertHPToDamageCounters_Bank5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ConvertHPToDamageCounters_Bank5"] = [
	{},
	{"a": 1},
	{"a": 10},
	{"a": 255},
	dict(POISON, a=20),
]
# <<< factory ConvertHPToDamageCounters_Bank5

# >>> factory CalculateBDividedByA_Bank5
CONTRACT["CalculateBDividedByA_Bank5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CalculateBDividedByA_Bank5"] = [
	{"a": 0, "b": 0, "oracle": False, "why": "Divisor zero enters the assembly loop forever.", "expect_regs": {"a": 0, "b": 0}},
	{"a": 1, "b": 1},
	{"a": 1, "b": 255},
	{"a": 2, "b": 5},
	{"a": 255, "b": 255},
	dict(POISON, a=3, b=10),
]
# <<< factory CalculateBDividedByA_Bank5

# >>> factory PrintCardPageRarityIcon
CONTRACT["PrintCardPageRarityIcon"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintCardPageRarityIcon"] = [
	{"a": 0, "d": 0, "e": 0, "hl": 0xC100,
	 "wram": {0xC100: b"\x00\x00\x00\x00"}, "read": {0xC100: 4}},
	dict(POISON, hl=0xC100, wram={0xC156: b"\x00\x00\x00\x00"}, read={0xC156: 4}),
	{"a": 0, "d": 0xDD, "e": 0xEE, "hl": 0xC100,
	 "wram": {0xC156: b"\x00\x00\x00\x00"}, "read": {0xC156: 4}},
	{"a": 0xFF, "d": 0, "e": 0, "hl": 0xC100,
	 "wram": {0xC100: b"\x00\x00\x00\x00"}, "read": {0xC100: 4}},
]
# <<< factory PrintCardPageRarityIcon



# >>> factory SetNoLineSeparation
CONTRACT["SetNoLineSeparation"] = {"compare": ("a",), "preserve": ()}
CASES["SetNoLineSeparation"] = [
	{"wram": {0xCD08: b"\x00"}, "read": {0xCD08: 1}},
	dict(POISON, wram={0xCD08: b"\xff"}, read={0xCD08: 1}),
]
# <<< factory SetNoLineSeparation



# >>> factory AIPlayInitialBasicCards
CONTRACT["AIPlayInitialBasicCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIPlayInitialBasicCards"] = [
    {},
    dict(POISON),
]
# <<< factory AIPlayInitialBasicCards

# >>> factory CheckIfEnoughParticularAttachedEnergy
CONTRACT["CheckIfEnoughParticularAttachedEnergy"] = {
    "compare": ("a", "f", "b", "hl"),
    "preserve": (),
}
CASES["CheckIfEnoughParticularAttachedEnergy"] = [
    {"a": 0, "hl": 0xC100, "b": 0, "wram": {0xC100: b"\x00"}},
    {"a": 2, "hl": 0xC100, "b": 3, "wram": {0xC100: b"\x01"}},
    dict(POISON, a=2, hl=0xC100, b=3, wram={0xC100: b"\x01"}),
]
# <<< factory CheckIfEnoughParticularAttachedEnergy

# >>> factory Func_14323
CONTRACT["Func_14323"] = {"compare": ("f",), "preserve": ()}
CASES["Func_14323"] = [
    {},
    dict(POISON),
]
# <<< factory Func_14323

# >>> factory CreateEnergyCardListFromHand
CONTRACT["CreateEnergyCardListFromHand"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CreateEnergyCardListFromHand"] = [
	{"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x02", 0xC242: b"\x00\x01",
	          0xC400: b"\x01\xCB"}, "read": {0xC510: 3}},
	{"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00",
	          0xC400: b"\x01"}, "read": {0xC510: 2}},
	dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x02",
	                   0xC242: b"\x01\x00", 0xC400: b"\x01\x02"},
	     read={0xC510: 3}),
]
# <<< factory CreateEnergyCardListFromHand

# >>> factory LookForCardIDInHand
CONTRACT["LookForCardIDInHand"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LookForCardIDInHand"] = [
	{"a": 0x01, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x02",
	                     0xC242: b"\x00\x01", 0xC400: b"\xCB\x01"}},
	{"a": 0x09, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x01",
	                     0xC242: b"\x00", 0xC400: b"\xCB"}},
	dict(POISON, a=0xCB, wram={0xFF97: b"\xC2", 0xC2EE: b"\x01",
	                            0xC242: b"\x00", 0xC400: b"\xCB"}),
	{"a": 0x09, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00"}},
]
# <<< factory LookForCardIDInHand


# >>> factory LookForCardIDInHandList_Bank5
CONTRACT["LookForCardIDInHandList_Bank5"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDInHandList_Bank5"] = [
	{"a": 0x01, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x02",
	                     0xC242: b"\x00\x01", 0xC400: b"\xCB\x01"}},
	{"a": 0x09, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x01",
	                     0xC242: b"\x00", 0xC400: b"\xCB"}},
	dict(POISON, a=0xCB, wram={0xFF97: b"\xC2", 0xC2EE: b"\x01",
	                            0xC242: b"\x00", 0xC400: b"\xCB"}),
	{"a": 0x09, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00"}},
]
# <<< factory LookForCardIDInHandList_Bank5


# >>> factory CheckForEvolutionInDeck
CONTRACT["CheckForEvolutionInDeck"]={"compare":("a","f"),"preserve":()}
CASES["CheckForEvolutionInDeck"]=[{"a":7,"f":0,"wram":{0xFF97:b"\xC2",0xC2BB:b"\x03",0xC200:b"\xFF"*60}},dict(POISON,a=2,f=0x80,wram={0xFF97:b"\xC3",0xC3BB:b"\x05",0xC300:b"\xFF"*60})]
# <<< factory CheckForEvolutionInDeck


# >>> factory LookForCardThatIsKnockedOutOnDevolution
CONTRACT["LookForCardThatIsKnockedOutOnDevolution"]={"compare":("a","f"),"preserve":()}
CASES["LookForCardThatIsKnockedOutOnDevolution"]=[dict(POISON,f=0,wram={0xFF97:b"\xC2",0xFF9D:b"\x02",0xC3EF:b"\x02",0xC3BB:b"\x01",0xC3CE:b"\x01",0xC300:b"\x10\x10",0xC480:b"\x08\x09",0xC3C8:b"\xC8"})]
# <<< factory LookForCardThatIsKnockedOutOnDevolution


# >>> factory CalculateParticularAttachedEnergyNeeded
CONTRACT["CalculateParticularAttachedEnergyNeeded"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("c", "d", "e")}
CASES["CalculateParticularAttachedEnergyNeeded"] = [{"a": 0, "b": 1, "hl": 0xC100, "wram": {0xC100: b"\x00"}}, {"a": 3, "b": 1, "hl": 0xC100, "wram": {0xC100: b"\x01"}}, dict(POISON, a=0x12, b=2, hl=0xC100, wram={0xC100: b"\x01"})]
# <<< factory CalculateParticularAttachedEnergyNeeded

# >>> factory GetAnimationData
wTempAnimation = 0xD422
CONTRACT["GetAnimationData"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["GetAnimationData"] = [
    {"wram": {wTempAnimation: b"\x00"}},
    dict(POISON, wram={wTempAnimation: b"\x01"}),
    {"wram": {wTempAnimation: b"\xff"}},
]
# <<< factory GetAnimationData


# >>> factory CardPageSwitch_PokemonOverviewOrDescription
CONTRACT["CardPageSwitch_PokemonOverviewOrDescription"] = {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_PokemonOverviewOrDescription"] = [
    {},
    dict(POISON, f=0),
]
# <<< factory CardPageSwitch_PokemonOverviewOrDescription



# >>> factory CheckCardEvolutionInHandOrDeck
CONTRACT["CheckCardEvolutionInHandOrDeck"] = {"compare": ("a", "f"), "preserve": ()}
hWhoseTurn = 0xFF97
CASES["CheckCardEvolutionInHandOrDeck"] = [
    {"a": 7, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x09", 0xC200: b"\xFF" * 60}},
    dict(POISON, a=0x2A, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x2A", 0xC200: b"\xFF" * 60}),
]
# <<< factory CheckCardEvolutionInHandOrDeck

# >>> factory CheckIfOpponentHasBossDeckID
CONTRACT["CheckIfOpponentHasBossDeckID"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
wOpponentDeckID = 0xCC0E
CASES["CheckIfOpponentHasBossDeckID"] = [
    {"a": 0x00, "f": 0x00, "wram": {wOpponentDeckID: b"\x0B"}},
    {"a": 0x12, "f": 0x80, "wram": {wOpponentDeckID: b"\x0C"}},
    dict(POISON, wram={wOpponentDeckID: b"\x1B"}),
    {"a": 0x34, "f": 0x80, "wram": {wOpponentDeckID: b"\x1C"}},
]
# <<< factory CheckIfOpponentHasBossDeckID


# >>> factory RaiseAIScoreToAllMatchingIDsInBench
CONTRACT["RaiseAIScoreToAllMatchingIDsInBench"] = {"compare": ("hl",), "preserve": (), "wram_out": True}
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wOpponentDeck = 0xC500
wPlayAreaEnergyAIScore = 0xCDE4
CASES["RaiseAIScoreToAllMatchingIDsInBench"] = [
    {"a": 0x2A, "wram": {hWhoseTurn: b"\x01", 0xC2BC: b"\x01\x02\xFF", wPlayerDeck + 1: b"\x2A", wPlayerDeck + 2: b"\x2B", wPlayAreaEnergyAIScore + 1: b"\x03\x04"}, "expect": {wPlayAreaEnergyAIScore + 1: b"\x08\x04"}, "read": {wPlayAreaEnergyAIScore + 1: 2}},
    {"a": 0x2A, "wram": {hWhoseTurn: b"\x01", 0xC2BC: b"\x01\x02\x03\xFF", wPlayerDeck + 1: b"\x2A", wPlayerDeck + 2: b"\x2A", wPlayerDeck + 3: b"\x2B", wPlayAreaEnergyAIScore + 1: b"\x00\x00\x00"}, "read": {wPlayAreaEnergyAIScore + 1: 3}},
    dict(POISON, a=0x2A, wram={hWhoseTurn: b"\x00", 0xC3BC: b"\x01\xFF", wOpponentDeck + 1: b"\x2B", wPlayAreaEnergyAIScore + 1: b"\xFA"}, read={wPlayAreaEnergyAIScore + 1: 1}),
]
# <<< factory RaiseAIScoreToAllMatchingIDsInBench


# >>> factory GetDamageNumberChars
wDuelAnimDamage = 0xD4B1
wDecimalChars = 0xD4B4
CONTRACT["GetDamageNumberChars"] = {"compare": (), "preserve": ()}
CASES["GetDamageNumberChars"] = [
	{"wram": {wDuelAnimDamage: b"\x00\x00", wDecimalChars: b"\xAA\xAA\xAA"}, "read": {wDecimalChars: 3}},
	{"wram": {wDuelAnimDamage: b"\x01\x00", wDecimalChars: b"\xAA\xAA\xAA"}, "read": {wDecimalChars: 3}},
	{"wram": {wDuelAnimDamage: b"\x2C\x01", wDecimalChars: b"\xAA\xAA\xAA"}, "read": {wDecimalChars: 3}},
	dict(POISON, wram={wDuelAnimDamage: b"\xFF\x00", wDecimalChars: b"\xAA\xAA\xAA"}, read={wDecimalChars: 3}),
]
# <<< factory GetDamageNumberChars

# >>> factory CardPageSwitch_PokemonAttack2Page2
CONTRACT["CardPageSwitch_PokemonAttack2Page2"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_PokemonAttack2Page2"] = [
    {"wram": {0xCC49: b"\x00\x00\x00\x00\x00"}},
    {"wram": {0xCC49: b"\x11\x22\x00\x00\x01"}},
    {"wram": {0xCC49: b"\x00\x00\x00\x11\x22"}},
    dict(POISON, wram={0xCC49: b"\xAA\xBB\xCC\xDD\x00"}),
    {"b": 1, "c": 2, "d": 3, "e": 4, "wram": {0xCC49: b"\x55\x66\x77\x88\x99"}},
]
# <<< factory CardPageSwitch_PokemonAttack2Page2

# >>> factory CardPageSwitch_08
CONTRACT["CardPageSwitch_08"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_08"] = [
    {},
    dict(POISON),
    {"f": 0x80, "b": 1, "c": 2, "d": 3, "e": 4},
]
# <<< factory CardPageSwitch_08

# >>> factory LoadPlayAreaCardGfx
CONTRACT["LoadPlayAreaCardGfx"] = {"compare": (), "preserve": ()}
CASES["LoadPlayAreaCardGfx"] = [
	{"a": 0xFF, "d": 0x88, "e": 0x00},
	{"a": 0x00, "d": 0x88, "e": 0x00,
	 "wram": {0xC400: b"\x01\x02"}, "vread": {0: {0x8800: 0x300}}},
	dict(POISON, a=0x00, d=0x90, e=0x00,
	     wram={0xC400: b"\x02\x03"}, vread={0: {0x9000: 0x300}}),
]
# <<< factory LoadPlayAreaCardGfx

# >>> factory SetBGP6OrSGB3ToCardPalette
CONTRACT["SetBGP6OrSGB3ToCardPalette"] = {"compare": (), "preserve": ()}
CASES["SetBGP6OrSGB3ToCardPalette"] = [
	{"wram": {0xCAB4: b"\x00"}},
	{"wram": {0xCAB4: b"\x01", 0xCE23: b"\x11\x22\x33\x44\x55\x66\x77\x88"},
	 "read": {0xCE2E: 6}},
	dict(POISON, wram={0xCAB4: b"\x02", 0xCE23: bytes(range(8))},
	     read={0xCB20: 8}),
]
# <<< factory SetBGP6OrSGB3ToCardPalette

# >>> factory SetOneLineSeparation
CONTRACT["SetOneLineSeparation"] = {"compare": ("a",), "preserve": ()}
CASES["SetOneLineSeparation"] = [
	{"wram": {0xCD08: b"\xff"}, "read": {0xCD08: 1}},
	dict(POISON, wram={0xCD08: b"\xff"}, read={0xCD08: 1}),
]
# <<< factory SetOneLineSeparation


# >>> factory _HasAlivePokemonInPlayArea
CONTRACT["_HasAlivePokemonInPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_HasAlivePokemonInPlayArea"] = [
    {"a": 0, "wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC2C8: b"\x10"},
     "read": {0xCBD2: 1, 0xCBD3: 1, 0xCBD4: 1}},
    {"a": 1, "wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03",
                      0xC2C8: b"\x00\x10\x00"}, "read": {0xCBD2: 1}},
    dict(POISON, a=0, wram={0xFF97: b"\xC3", 0xC3EF: b"\x02",
                            0xC3C8: b"\x00\x00"}),
]
# <<< factory _HasAlivePokemonInPlayArea

# >>> factory PrintPlayAreaCardLocation
CONTRACT["PrintPlayAreaCardLocation"] = {"compare": (), "preserve": ()}
CASES["PrintPlayAreaCardLocation"] = [
    {"wram": {0xCBC9: b"\x00", 0xCBCA: b"\x00", 0xFF97: b"\x00"},
     "read": {0x9801: 1, 0x9802: 1, 0x9803: 1}},
    dict(POISON,
         wram={0xCBC9: b"\x01", 0xCBCA: b"\x05", 0xFF97: b"\xC2"},
         read={0x98A1: 1, 0x98A2: 1, 0x98A3: 1}),
    {"wram": {0xCBC9: b"\x05", 0xCBCA: b"\x1F", 0xFF97: b"\x00"},
     "read": {0x9BE1: 1, 0x9BE2: 1, 0x9BE3: 1}},
]
# <<< factory PrintPlayAreaCardLocation


# >>> factory CheckPrintPoisoned
CONTRACT["CheckPrintPoisoned"] = {"compare": ("a",), "preserve": ()}
CASES["CheckPrintPoisoned"] = [
    {"a": 0, "b": 1, "c": 2, "read": {0x9841: 1}},
    {"a": 0x80, "b": 2, "c": 3, "read": {0x9862: 1}},
    dict(POISON, a=0xC0, b=4, c=5, read={0x98A4: 1}),
]
# <<< factory CheckPrintPoisoned

# >>> factory DrawHPBar
CONTRACT["DrawHPBar"] = {"compare": (), "preserve": ()}
CASES["DrawHPBar"] = [
    {"d": 120, "e": 120, "read": {0xC590: 12}},
    {"d": 120, "e": 70, "wram": {0xC590: b"\xaa" * 12}, "read": {0xC590: 12}},
    dict(POISON, d=80, e=0, wram={0xC590: b"\xaa" * 12}, read={0xC590: 12}),
]
# <<< factory DrawHPBar
# >>> factory ValidateSavedDuelDataFromHL
CONTRACT["ValidateSavedDuelDataFromHL"] = {"compare": ("f", "hl", "d", "e"), "preserve": ("d", "e")}
CASES["ValidateSavedDuelDataFromHL"] = [
    {"hl": 0xBC00, "sram": {0: {0xBC00: b"\x00"}}},
    {"hl": 0xBC00, "sram": {0: {0xBC00: b"\x01\x45\x23\x00" + b"\x00" * 826}}},
    {"hl": 0xBC00, "sram": {0: {0xBC00: b"\x01\x23\x45\x00" + b"\x00" * 826}}},
    dict(POISON, hl=0xBC00, sram={0: {0xBC00: b"\x01\x45\x23\x00" + b"\x00" * 826}}),
]
# <<< factory ValidateSavedDuelDataFromHL
# >>> factory ResetDoFrameFunction_Bank1
CONTRACT["ResetDoFrameFunction_Bank1"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e"),
}
CASES["ResetDoFrameFunction_Bank1"] = [
    {"a": 0x12, "f": 0x00, "b": 0x34, "c": 0x56, "d": 0x78,
     "e": 0x9A, "hl": 0x2468, "wram": {0xCAD3: b"\x34\x12"},
     "read": {0xCAD3: 2}},
    dict(POISON, wram={0xCAD3: b"\x78\x56"}, read={0xCAD3: 2}),
]
# <<< factory ResetDoFrameFunction_Bank1

# >>> factory OppAction_NoAction
CONTRACT["OppAction_NoAction"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
}
CASES["OppAction_NoAction"] = [
    dict(POISON, wram={0xCC24: b"\xA5"}, read={0xCC24: 1}),
]
# <<< factory OppAction_NoAction

# >>> factory ReturnRetreatCostCardsToArena
CONTRACT["ReturnRetreatCostCardsToArena"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d")}
CASES["ReturnRetreatCostCardsToArena"] = [
    {"wram": {0xFFA2: b"\xFF"}},
    dict(POISON, wram={0xFFA2: b"\xFF"}),
]
# <<< factory ReturnRetreatCostCardsToArena


# >>> factory FindHighestBenchScore
CONTRACT["FindHighestBenchScore"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
wPlayAreaAIScore = 0xCDBF
CASES["FindHighestBenchScore"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x01", wPlayAreaAIScore: b"\x00\x07"}, "expect": {hTempPlayAreaLocation_ff9d: b"\x00"}, "read": {hTempPlayAreaLocation_ff9d: 1}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x04", wPlayAreaAIScore: b"\x00\x01\x09\x09\x02"}, "expect": {hTempPlayAreaLocation_ff9d: b"\x02"}, "read": {hTempPlayAreaLocation_ff9d: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EF: b"\x03", wPlayAreaAIScore: b"\xAA\x00\xFF\x01\x02"}, expect={hTempPlayAreaLocation_ff9d: b"\x01"}, read={hTempPlayAreaLocation_ff9d: 1}),
]
# <<< factory FindHighestBenchScore

# >>> factory AIEncourage
CONTRACT["AIEncourage"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
wAIScore = 0xCDBE
CASES["AIEncourage"] = [
    {"a": 0x00, "wram": {wAIScore: b"\x00"}, "expect": {wAIScore: b"\x00"}, "read": {wAIScore: 1}},
    {"a": 0x01, "wram": {wAIScore: b"\x02"}, "expect": {wAIScore: b"\x03"}, "read": {wAIScore: 1}},
    {"a": 0x01, "wram": {wAIScore: b"\xFF"}, "expect": {wAIScore: b"\xFF"}, "read": {wAIScore: 1}},
    dict(POISON, a=0x10, wram={wAIScore: b"\x20"}, expect={wAIScore: b"\x30"}, read={wAIScore: 1}),
]
# <<< factory AIEncourage

# >>> factory HandleFailedToContinueDuel
CONTRACT["HandleFailedToContinueDuel"] = {"compare": ("f",), "preserve": ()}
CASES["HandleFailedToContinueDuel"] = [
    {"hl": 0x0000, "keys": 0x01, "wram": {
        0xC590: b"\x00", 0xCD0F: b"\x05", 0xCD10: b"\x01",
        0xCD11: b"\x04", 0xCD12: b"\x00", 0xCD13: b"\x00",
        0xCD15: b"\x00", 0xCD16: b"\x22"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, hl=0x00CA, keys=0x01, wram={
        0xC590: b"\x00", 0xCD0F: b"\x05", 0xCD10: b"\x01",
        0xCD11: b"\x04", 0xCD12: b"\x00", 0xCD13: b"\x00",
        0xCD15: b"\x00", 0xCD16: b"\x22"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory HandleFailedToContinueDuel

# >>> factory IsLoadedCard1BasicPokemon
CONTRACT["IsLoadedCard1BasicPokemon"] = {"compare": ("a", "f"), "preserve": ()}
CASES["IsLoadedCard1BasicPokemon"] = [
    {"wram": {0xCC2B: b"\x01", 0xCC24: b"\x00", 0xCC2D: b"\x00"}},
    {"wram": {0xCC2B: b"\x00", 0xCC24: b"\x00", 0xCC2D: b"\x00"}},
    {"wram": {0xCC2B: b"\x01", 0xCC24: b"\xFF", 0xCC2D: b"\xFF"}},
    {"wram": {0xCC2B: b"\x01", 0xCC24: b"\x00", 0xCC2D: b"\x00"}},
    {"wram": {0xCC2B: b"\xFF", 0xCC24: b"\xCB", 0xCC2D: b"\xFF"}},
    dict(POISON, wram={0xCC2B: b"\xFF", 0xCC24: b"\x53", 0xCC2D: b"\xFF"}),
    {"wram": {0xCC2B: b"\xCC", 0xCC24: b"\xFF", 0xCC2D: b"\xFF"}},
]
# <<< factory IsLoadedCard1BasicPokemon
# >>> factory PracticeDuel_PlayGoldeen
CONTRACT["PracticeDuel_PlayGoldeen"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuel_PlayGoldeen"] = [
    {"wram": {0xCC2B: b"\x53"}},
    dict(POISON, wram={0xCC2B: b"\x53"}),
    dict(POISON, a=0x01, wram={0xCC2B: b"\x53"}),
    dict(POISON, hl=0x4567, wram={0xCC2B: b"\x53"}),
]
# <<< factory PracticeDuel_PlayGoldeen
CONTRACT["Func_6ba2"] = {"compare": (), "preserve": ()}
CASES["Func_6ba2"] = [
    {"hl": 0x0000, "wram": {0xCC0D: b"\x01", 0xC590: b"\x00"},
     "vread": {0: {0x9980: 192}}},
    dict(POISON, hl=0x0000, keys=0x01,
         wram={0xCC0D: b"\x00", 0xC590: b"\x00",
               0xCD0F: b"\x05", 0xCD10: b"\x01", 0xCD11: b"\x04",
               0xCD12: b"\x00", 0xCD13: b"\x00", 0xCD15: b"\x00",
               0xCD16: b"\x22"},
         read={0xCD0F: 1, 0xCD10: 1, 0xCD16: 1},
         vread={0: {0x9980: 1, 0x9A32: 1}}),
]
# <<< factory Func_6ba2

# >>> factory TwoByteNumberToTxSymbol_PadSpace_Bank1
CONTRACT["TwoByteNumberToTxSymbol_PadSpace_Bank1"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["TwoByteNumberToTxSymbol_PadSpace_Bank1"] = [
    {"d": 0, "e": 0, "wram": {0xCAA0: b"\x00" * 6}, "read": {0xCAA0: 6}},
    {"d": 0x30, "e": 0x39, "wram": {0xCAA0: b"\x00" * 6}, "read": {0xCAA0: 6}},
    dict(POISON, d=0xFF, e=0xFF, wram={0xCAA0: b"\x00" * 6}, read={0xCAA0: 6}),
]
# <<< factory TwoByteNumberToTxSymbol_PadSpace_Bank1

# >>> factory DrawWideTextBox_WaitForInput_Bank1
CONTRACT["DrawWideTextBox_WaitForInput_Bank1"] = {"compare": ("f",), "preserve": ()}
CASES["DrawWideTextBox_WaitForInput_Bank1"] = [
    {"hl": 0, "keys": 0x01, "wram": {0xC590: b"\x00"},
     "read": {0xCD0F: 1, 0xCD10: 1, 0xCD16: 1},
     "vread": {0: {0x9980: 1, 0x9A32: 1}}},
    dict(POISON, hl=0, keys=0x02, wram={0xC590: b"\x00"},
         read={0xCD0F: 1, 0xCD10: 1, 0xCD16: 1},
         vread={0: {0x9980: 1, 0x9A32: 1}}),
]
# <<< factory DrawWideTextBox_WaitForInput_Bank1


# >>> factory CardPageSwitch_EnergyOrTrainerPage1
CONTRACT["CardPageSwitch_EnergyOrTrainerPage1"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CardPageSwitch_EnergyOrTrainerPage1"] = [
    {},
    dict(POISON),
]
# <<< factory CardPageSwitch_EnergyOrTrainerPage1

# >>> factory CardPageSwitch_TrainerEnd
CONTRACT["CardPageSwitch_TrainerEnd"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CardPageSwitch_TrainerEnd"] = [{"a": 0, "f": 0}, dict(POISON), {"a": 0xFF, "f": 0x80}]
# <<< factory CardPageSwitch_TrainerEnd

# >>> factory CheckIfEnoughEnergiesOfType
CONTRACT["CheckIfEnoughEnergiesOfType"] = {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e")}
wAttachedEnergiesAccum = 0xCBCE
CASES["CheckIfEnoughEnergiesOfType"] = [
    {"a": 0, "hl": 0xCC1B, "wram": {wAttachedEnergiesAccum: b"\x00", 0xCC1B: b"\x00"}},
    {"a": 2, "hl": 0xCC1B, "wram": {wAttachedEnergiesAccum: b"\x01", 0xCC1B: b"\x02"}},
    {"a": 3, "hl": 0xCC1B, "wram": {wAttachedEnergiesAccum: b"\x01", 0xCC1B: b"\x02"}},
    dict(POISON, a=0xF4, hl=0xCC1B, wram={wAttachedEnergiesAccum: b"\xFE", 0xCC1B: b"\x01"}),
]
# <<< factory CheckIfEnoughEnergiesOfType
# >>> factory CheckIfActiveCardParalyzedOrAsleep
CONTRACT["CheckIfActiveCardParalyzedOrAsleep"] = {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e")}
hWhoseTurn = 0xFF97
CASES["CheckIfActiveCardParalyzedOrAsleep"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F0: b"\x00"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F0: b"\x02"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2F0: b"\x03"}},
    dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC3F0: b"\x04"}),
]
# <<< factory CheckIfActiveCardParalyzedOrAsleep
# >>> factory GetAttacksEnergyCostBits
CONTRACT["GetAttacksEnergyCostBits"] = {"compare": ("a",), "preserve": ()}
wLoadedCard2Atk1EnergyCost = 0xCC71
wLoadedCard2Atk2EnergyCost = 0xCC84
CASES["GetAttacksEnergyCostBits"] = [
    {"a": 0, "wram": {wLoadedCard2Atk1EnergyCost: b"\x00\x00\x00\x00", wLoadedCard2Atk2EnergyCost: b"\x00\x00\x00\x00"}},
    {"a": 1, "wram": {wLoadedCard2Atk1EnergyCost: b"\x10\x01\x20\x04", wLoadedCard2Atk2EnergyCost: b"\x00\x00\x00\x80"}},
    dict(POISON, a=2, wram={wLoadedCard2Atk1EnergyCost: b"\x00" * 4, wLoadedCard2Atk2EnergyCost: b"\x00" * 4}),
]
# <<< factory GetAttacksEnergyCostBits
# >>> factory CheckForEvolutionInList
CONTRACT["CheckForEvolutionInList"] = {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("c",)}
wDuelTempList = 0xC510
wPlayerDuelVariables = 0xC200
hWhoseTurn = 0xFF97
CASES["CheckForEvolutionInList"] = [
    {"a": 0, "wram": {wDuelTempList: b"\xff", hWhoseTurn: b"\xc2", wPlayerDuelVariables + 0xbb: b"\x00"}},
    {"a": 0, "wram": {wDuelTempList: b"\x01\xff", hWhoseTurn: b"\xc2", wPlayerDuelVariables + 0xbb: b"\x08", wPlayerDuelVariables + 0xc2: b"\x80"}},
    dict(POISON, a=0, wram={wDuelTempList: b"\x01\xff", hWhoseTurn: b"\xc2", wPlayerDuelVariables + 0xbb: b"\x08", wPlayerDuelVariables + 0xc2: b"\x80"}),
]
# <<< factory CheckForEvolutionInList
# >>> factory CountNumberOfEnergyCardsAttached
CONTRACT["CountNumberOfEnergyCardsAttached"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CountNumberOfEnergyCardsAttached"] = [
    {"e": 0, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10", 0xC400: b"\x01"}, "read": {0xCC1B: 8, 0xCC23: 1}},
    {"e": 0, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10", 0xC400: b"\x01", 0xC201: b"\x10", 0xC401: b"\x01"}, "read": {0xCC1B: 8, 0xCC23: 1}},
    dict(POISON, e=0, wram={hWhoseTurn: b"\xC3", 0xC300: b"\x10", 0xC500: b"\x01"}, read={0xCC1B: 8, 0xCC23: 1}),
]
# <<< factory CountNumberOfEnergyCardsAttached
# >>> factory LookForCardIDInLocation_Bank5
CONTRACT["LookForCardIDInLocation_Bank5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["LookForCardIDInLocation_Bank5"] = [
    {"a": 0x10, "e": 0x2A, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x10", 0xC400: b"\x2A"}},
    {"a": 0x11, "e": 0x2A, "wram": {hWhoseTurn: b"\xC2", 0xC200: b"\x11", 0xC400: b"\x2A"}},
    dict(POISON, a=0x12, e=0x2A, wram={hWhoseTurn: b"\xC3", 0xC300: b"\x12", 0xC500: b"\x2A"}),
]
# <<< factory LookForCardIDInLocation_Bank5
# >>> factory LoadDefendingPokemonColorWRAndPrizeCards
CONTRACT["LoadDefendingPokemonColorWRAndPrizeCards"] = {"compare": (), "preserve": ()}
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wPlayerPrizes = 0xC2EC
wOpponentPrizes = 0xC3EC
wAIPlayerColor = 0xCDCF
wAIPlayerWeakness = 0xCDD0
wAIPlayerResistance = 0xCDD1
wAIPlayerPrizeCount = 0xCDD2
wAIOpponentPrizeCount = 0xCDD3
CASES["LoadDefendingPokemonColorWRAndPrizeCards"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC3BB: b"\x00", wOpponentDeck: b"\x44",
              wPlayerPrizes: b"\x15", wOpponentPrizes: b"\x03"},
     "read": {wAIPlayerColor: 1, wAIPlayerWeakness: 1, wAIPlayerResistance: 1,
              wAIPlayerPrizeCount: 1, wAIOpponentPrizeCount: 1, hWhoseTurn: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC3BB: b"\x00", wOpponentDeck: b"\x45",
                       wPlayerPrizes: b"\x3F", wOpponentPrizes: b"\x00"},
         read={wAIPlayerColor: 1, wAIPlayerWeakness: 1, wAIPlayerResistance: 1,
               wAIPlayerPrizeCount: 1, wAIOpponentPrizeCount: 1, hWhoseTurn: 1}),
]
# <<< factory LoadDefendingPokemonColorWRAndPrizeCards

# >>> factory CheckIfEnergyIsUseful
CONTRACT["CheckIfEnergyIsUseful"] = {"compare": ("f",), "preserve": ()}
wTempCardID = 0xCDB9
wTempCardType = 0xCDBA
CASES["CheckIfEnergyIsUseful"] = [
    {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x07",
                      wTempCardID: b"\x00", wTempCardType: b"\x08"}},
    {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x03",
                      wTempCardID: b"\x28", wTempCardType: b"\x08"}},
    {"a": 0, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x02",
                      wTempCardID: b"\xBC", wTempCardType: b"\x08"}},
    dict(POISON, a=0, wram={hWhoseTurn: b"\xC2", wPlayerDeck: b"\x01",
                            wTempCardID: b"\x00", wTempCardType: b"\x01"}),
]
# <<< factory CheckIfEnergyIsUseful

# >>> factory PickRandomBenchPokemon
CONTRACT["PickRandomBenchPokemon"] = {"compare": ("a",), "preserve": ()}
wPlayerPokemonCount = 0xC2EF
CASES["PickRandomBenchPokemon"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerPokemonCount: b"\x02",
              0xCACA: b"\x12", 0xCACB: b"\x34", 0xCACC: b"\x56"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerPokemonCount: b"\x06",
                       0xCACA: b"\xA5", 0xCACB: b"\x5A", 0xCACC: b"\x01"}),
]
# <<< factory PickRandomBenchPokemon

# >>> factory PracticeDuel_VerifyPlayerTurnActions
CONTRACT["PracticeDuel_VerifyPlayerTurnActions"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuel_VerifyPlayerTurnActions"] = [
    dict(POISON, wram={0xFF97: b"\xC2", 0xCC06: b"\x00", 0xCCC2: b"\x53"}),
]
# <<< factory PracticeDuel_VerifyPlayerTurnActions

# >>> factory PrintCardNameFromCardIDInTextBox
wTempNonTurnDuelistCardID = 0xCCC4
CONTRACT["PrintCardNameFromCardIDInTextBox"] = {"compare": (), "preserve": ()}
CASES["PrintCardNameFromCardIDInTextBox"] = [
    {"hl": 0x0081, "wram": {wTempNonTurnDuelistCardID: b"\x08", 0xCAD3: b"\x48\x03"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 1000000, "cycle_budget": 4000000, "read": {0xCE3F: 2}, "vread": {0: {0x9980: 192}}},
    dict(POISON, hl=0x0081, wram={wTempNonTurnDuelistCardID: b"\x08", 0xCAD3: b"\x48\x03"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=1000000, cycle_budget=4000000, read={0xCE3F: 2}, vread={0: {0x9980: 192}}),
]
# <<< factory PrintCardNameFromCardIDInTextBox
# >>> factory RemoveCardIDInList
CONTRACT["RemoveCardIDInList"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["RemoveCardIDInList"] = [
    {"hl": 0xC100, "e": 0x10, "hram": {0xFF97: b"\xC2"}, "wram": {0xC100: b"\x00\x01\xFF", 0xC400: b"\x10\x20"}, "read": {0xC100: 3, 0xC400: 2}},
    {"hl": 0xC100, "e": 0x30, "hram": {0xFF97: b"\xC2"}, "wram": {0xC100: b"\x00\x01\xFF", 0xC400: b"\x10\x20"}, "read": {0xC100: 3, 0xC400: 2}},
    dict(POISON, hl=0xC1FF, e=0x20, hram={0xFF97: b"\xC2"}, wram={0xC1FF: b"\x00\xFF", 0xC400: b"\x10\x20"}, read={0xC1FF: 2, 0xC400: 2}),
]
# <<< factory RemoveCardIDInList
# >>> factory SortTempHandByIDList
CONTRACT["SortTempHandByIDList"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["SortTempHandByIDList"] = [
    {"wram": {0xCDAE: b"\x00\xC6", 0xC600: b"\x20\x10\x00", 0xC510: b"\x00\x01\xFF", 0xC400: b"\x10\x20"}, "read": {0xC510: 3, 0xC600: 3, 0xCDAE: 2}},
    {"wram": {0xCDAE: b"\x00\xC6", 0xC600: b"\x00", 0xC510: b"\x00\xFF"}, "read": {0xC510: 2, 0xC600: 1, 0xCDAE: 2}},
    dict(POISON, wram={0xCDAE: b"\x00\xC6", 0xC600: b"\x20\x00", 0xC510: b"\x01\xFF", 0xC400: b"\x10\x20"}, read={0xC510: 2, 0xC600: 2, 0xCDAE: 2}),
]
# <<< factory SortTempHandByIDList


# >>> factory ApplyCardCGBAttributes
CONTRACT["ApplyCardCGBAttributes"] = {"compare": (), "preserve": ()}
CASES["ApplyCardCGBAttributes"] = [
    {"d": 0x02, "e": 0x03},
    dict(POISON, d=0x09, e=0x05),
]
# <<< factory ApplyCardCGBAttributes
# >>> factory ApplyStatusConditionToArenaPokemon
CONTRACT["ApplyStatusConditionToArenaPokemon"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d")}
CASES["ApplyStatusConditionToArenaPokemon"] = [
    {},
    {"d": 0xC2, "hl": 0xC100, "wram": {0xC100: b"\x0F\x30", 0xC2F0: b"\xFF" * 16}, "read": {0xC2F0: 16}},
    {"d": 0xC2, "hl": 0xC100, "wram": {0xC100: b"\x00\x00", 0xC2F0: b"\xAA" * 16}, "read": {0xC2F0: 16}},
    {"d": 0xC2, "hl": 0xC100, "wram": {0xC100: b"\xFF\x00", 0xC2F0: b"\x5A" * 16}, "read": {0xC2F0: 16}},
    dict(POISON, d=0xC2, hl=0xC100, wram={0xC100: b"\x3C\xC3", 0xC2F0: b"\x0F" * 16}, read={0xC2F0: 16}),
]
# <<< factory ApplyStatusConditionToArenaPokemon

# >>> factory CheckIfEnoughEnergiesToRetreat
CONTRACT["CheckIfEnoughEnergiesToRetreat"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfEnoughEnergiesToRetreat"] = [
    {},
    dict(POISON),
]
# <<< factory CheckIfEnoughEnergiesToRetreat
# >>> factory DecideLinkDuelVariables
CONTRACT["DecideLinkDuelVariables"] = {"compare": ("f",), "preserve": ()}
CASES["DecideLinkDuelVariables"] = [
    {"keys": 0x02, "wram": {0xC590: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0x02, wram={0xC590: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DecideLinkDuelVariables
# >>> factory DisplayAttackPage
CONTRACT["DisplayAttackPage"] = {"compare": (), "preserve": ()}
CASES["DisplayAttackPage"] = [
    {"wram": {0xCC04: b"\x00"}},
    dict(POISON, wram={0xCC04: b"\x03"}),
]
# <<< factory DisplayAttackPage
# >>> factory DisplayCardPage
CONTRACT["DisplayCardPage"] = {"compare": (), "preserve": ()}
CASES["DisplayCardPage"] = [
    {"oracle": False, "why": "Page zero enters the scene loop without a prepared duel screen.", "wram": {0xCBC7: b"\x00"}},
    dict(POISON, wram={0xCBC7: b"\x0D"}),
]
# <<< factory DisplayCardPage
# >>> factory DoPracticeDuelAction
CONTRACT["DoPracticeDuelAction"] = {"compare": ("f",), "preserve": ()}
CASES["DoPracticeDuelAction"] = [
    {"a": 0, "wram": {0xCC13: b"\x00"}},
    dict(POISON, a=0xFF, wram={0xCC13: b"\x00"}),
]
# <<< factory DoPracticeDuelAction
# >>> factory DrawDuelHorizontalSeparator
CONTRACT["DrawDuelHorizontalSeparator"] = {"compare": (), "preserve": ()}
CASES["DrawDuelHorizontalSeparator"] = [
    {},
    dict(POISON),
]
# <<< factory DrawDuelHorizontalSeparator
# >>> factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile
CONTRACT["MoveAllTurnHolderKnockedOutPokemonToDiscardPile"] = {"compare": (), "preserve": ()}
CASES["MoveAllTurnHolderKnockedOutPokemonToDiscardPile"] = [
    {"hram": {0xFF97: b"\xC2"}, "wram": {0xC2EF: b"\x01", 0xC2C9: b"\x00"}},
    dict(POISON, hram={0xFF97: b"\xC3"}, wram={0xC3EF: b"\x02", 0xC3C9: b"\x00\x01"}),
]
# <<< factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile
# >>> factory PrintSortNumberInCardList_CallFromPointer
CONTRACT["PrintSortNumberInCardList_CallFromPointer"] = {"compare": (), "preserve": ()}
CASES["PrintSortNumberInCardList_CallFromPointer"] = [
    {"wram": {0xC51A: b"\x01\x02\xFF"}},
    dict(POISON, wram={0xC51A: b"\x03\x04\xFF"}),
]
# <<< factory PrintSortNumberInCardList_CallFromPointer
# >>> factory PracticeDuel_VerifyInitialPlay
CONTRACT["PracticeDuel_VerifyInitialPlay"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuel_VerifyInitialPlay"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x02"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x02"}),
]
# <<< factory PracticeDuel_VerifyInitialPlay

# >>> factory CheckIfNoSurplusEnergyForAttack
CONTRACT["CheckIfNoSurplusEnergyForAttack"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfNoSurplusEnergyForAttack"] = [
    {"read": {0xCC1B: 9, 0xCDB5: 3}},
    {"wram": {0xCCC6: b"\x01"}, "read": {0xCC1B: 9, 0xCDB5: 3}},
    {"wram": {0xFF9D: b"\x01", 0xCCC6: b"\x01"}, "read": {0xCC1B: 9, 0xCDB5: 3}},
    dict(POISON, wram={0xCCC6: b"\x00"}, read={0xCC1B: 9, 0xCDB5: 3}),
]
# <<< factory CheckIfNoSurplusEnergyForAttack

# >>> factory Func_1585b
CONTRACT["Func_1585b"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_1585b"] = [
    # Immediate terminator: a = 0, `or a` sets Z only.
    {"hl": 0xC100, "wram": {0xC100: b"\x00"}},
    # Poisoned entry registers: only hl is consumed. One skipped (type 2)
    # entry, then the terminator.
    dict(POISON, hl=0xC100, wram={0xC100: b"\x02\x11\x22\x00\x00\x00"}),
    # Type-1 entry for an implausible card ID: lookup fails, single inc hl,
    # then the terminator on the next iteration.
    {"hl": 0xC100, "wram": {0xC100: b"\x01\xFE\x00\x00\x00\x00"}},
    # Type-1 entry with card ID 0 and a zero requirement.
    {"hl": 0xC100, "wram": {0xC100: b"\x01\x00\x00\x00\x00\x00"}},
    # Type-1 entry with the maximum requirement byte.
    {"hl": 0xC100, "wram": {0xC100: b"\x01\x00\xFF\x00\x00\x00"}},
    # Several mixed entries before the terminator, proving the 3-byte stride
    # of the skip path stays in phase with the type-1 path.
    {"hl": 0xC100,
     "wram": {0xC100: b"\x02\x01\x03\x01\x05\x02\xFF\x07\x09\x00\x00\x00"}},
    # High first byte (not 1): still a plain 3-byte skip.
    {"hl": 0xC100, "wram": {0xC100: b"\xFF\xFF\xFF\x00"}},
]
# <<< factory Func_1585b

# >>> factory CheckIfNotABossDeckID
CONTRACT["CheckIfNotABossDeckID"] = {"compare": ("a",), "preserve": ()}
sReceivedLegendaryCards = 0xA00A
CASES["CheckIfNotABossDeckID"] = [
    # All-zero: the flag byte is 0, so the deck-ID check runs.
    {"sram": {0: {sReceivedLegendaryCards: b"\x00\x00"}},
     "sread": {0: {sReceivedLegendaryCards: 2}}},
    # Poisoned entry registers: the routine takes no arguments. Flag byte
    # nonzero, so a is the flag value itself and the check is skipped.
    dict(POISON, sram={0: {sReceivedLegendaryCards: b"\x07\x00"}},
         sread={0: {sReceivedLegendaryCards: 2}}),
    # Flag byte 0 but the following byte nonzero: pins the read address.
    {"sram": {0: {sReceivedLegendaryCards: b"\x00\x05"}},
     "sread": {0: {sReceivedLegendaryCards: 2}}},
    # Maximum flag value.
    {"sram": {0: {sReceivedLegendaryCards: b"\xFF\x00"}},
     "sread": {0: {sReceivedLegendaryCards: 2}}},
    # ramg False after seeding: only the routine's own EnableSRAM makes the
    # zero byte observable, otherwise it reads open bus $FF.
    {"ramg": False, "sram": {0: {sReceivedLegendaryCards: b"\x00\x00"}},
     "sread": {0: {sReceivedLegendaryCards: 2}}},
]
# <<< factory CheckIfNotABossDeckID

# >>> factory AIChooseRandomlyNotToDoAction
wOpponentDeckID = 0xCC0E
CONTRACT["AIChooseRandomlyNotToDoAction"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["AIChooseRandomlyNotToDoAction"] = [
	# deck id 0: below every boss range and not one of the six 50% decks -> 25% path
	{"wram": {wOpponentDeckID: b"\x00"}},
	# above every deck id: not-boss via the high side, still the 25% path
	{"wram": {wOpponentDeckID: b"\x7f"}},
	{"wram": {wOpponentDeckID: b"\xff"}},
	dict(POISON, wram={wOpponentDeckID: b"\x00"}),
]
# <<< factory AIChooseRandomlyNotToDoAction

# >>> factory TrySetUpBossStartingPlayArea
CONTRACT["TrySetUpBossStartingPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TrySetUpBossStartingPlayArea"] = [
	{"wram": {0xCDAA: b"\x00\x00"}},
	dict(POISON, wram={0xCDAA: b"\x00\xc1", 0xC100: b"\x00"}),
	{"wram": {0xCDAA: b"\x00\xc1", 0xC100: b"\x05\x00", 0xCDAC: b"\x00\xc2", 0xC200: b"\x09\x00"}},
	{"wram": {0xCDAA: b"\x00\xc1", 0xC100: b"\x07\x08\x03\x00"}},
	{"wram": {0xCDAA: b"\x00\xc1", 0xC100: b"\x00", 0xCDF1: b"\x2b"}},
]
# <<< factory TrySetUpBossStartingPlayArea

# >>> factory CardPageSwitch_TrainerPage2
CONTRACT["CardPageSwitch_TrainerPage2"] = {"compare": ("a", "f", "hl", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_TrainerPage2"] = [
    {"wram": {0xCC30: b"\x00"}, "read": {0xCC30: 1}},
    dict(POISON, wram={0xCC30: b"\x00"}, read={0xCC30: 1}),
    {"wram": {0xCC30: b"\x09"}, "read": {0xCC30: 1}},
]
# <<< factory CardPageSwitch_TrainerPage2

# >>> factory LoadAndValidateDuelSaveData
CONTRACT["LoadAndValidateDuelSaveData"] = {"compare": ("f",), "preserve": ()}
CASES["LoadAndValidateDuelSaveData"] = [
	{"sram": {0: {0xBC00: b"\x00" * 0x100}}},
	dict(POISON, sram={0: {0xBC00: b"\x00" * 0x100}}),
	{"sram": {0: {0xBC00: b"\x01" + b"\x00" * 0xFF}}},
]
# <<< factory LoadAndValidateDuelSaveData

# >>> factory ValidateSavedNonLinkDuelData
CONTRACT["ValidateSavedNonLinkDuelData"] = {"compare": ("f",), "preserve": ()}
CASES["ValidateSavedNonLinkDuelData"] = [
	{"sram": {0: {0xBC03: b"\x00", 0xBC00: b"\x00" * 0x100}}},
	dict(POISON, sram={0: {0xBC03: b"\x00", 0xBC00: b"\x00" * 0x100}}),
	{"sram": {0: {0xBC03: b"\x01", 0xBC00: b"\x00" * 0x100}}},
]
# <<< factory ValidateSavedNonLinkDuelData

# >>> factory SetupPlayAreaScreen
CONTRACT["SetupPlayAreaScreen"] = {"compare": (), "preserve": ()}
CASES["SetupPlayAreaScreen"] = [
    {"wram": {0xCAC2: b"\x00", 0xCBD2: b"\x00"}},
    dict(POISON, wram={0xCAC2: b"\x02", 0xCBD2: b"\xAA"}),
    {"wram": {0xCAC2: b"\x01", 0xCBD2: b"\xAA"}},
]
# <<< factory SetupPlayAreaScreen

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wAttachedEnergies = 0xCC1B
wAttachedEnergiesAccum = 0xCBCE
wTotalAttachedEnergies = 0xCC23
wLoadedCard1Atk1EnergyCost = 0xCC30
wLoadedCard1Atk2EnergyCost = 0xCC43

wCardPageNumber = 0xCBC7

hWhoseTurn = 0xFF97
wCardListHeaderText = 0xCBDC
wCardListInfoBoxText = 0xCBDA

hWhoseTurn = 0xFF97
hTempCardIndex_ff98 = 0xFF98
hTempPlayAreaLocation_ff9d = 0xFF9D
wPlayerDeck = 0xC400

hTempCardIndex_ff98 = 0xFF98
wPreEvolutionPokemonCard = 0xCCEE

hWhoseTurn = 0xFF97
wPlayerCardLocations = 0xC200
wPlayerDeck = 0xC400

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wPlayerDuelVariables = 0xC200

hWhoseTurn = 0xFF97
wDuelType = 0xCC09

wStringBuffer = 0xCAA0
BGMAP0 = 0x9800
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

def write_case(a, b, c, d=0, e=0, hl=0, poison=False, expected=b"\x00\x00"):
    dst = BGMAP0 + c * 32 + b
    values = dict(POISON) if poison else {"a": a, "b": b, "c": c, "d": d, "e": e, "hl": hl}
    values["wram"] = {wStringBuffer: b"\xff" * 6}
    if dst < 0xA000:
        values["vram"] = {0: {dst: b"\xee" * 3}}
        values["expect_vram"] = {0: {dst: expected + b"\xee"}}
    else:
        values["sram"] = {0: {dst: b"\xee" * 3}}
        values["expect_sram"] = {0: {dst: expected + b"\xee"}}
    return values

wNumCardsBeingDrawn = 0xCBE9
wOpponentNumberOfCardsInHand = 0xC3EE
wOpponentNumberOfCardsNotInDeck = 0xC3BA

wNumCardsBeingDrawn = 0xCBE9
wPlayerNumberOfCardsInHand = 0xC2EE
wPlayerNumberOfCardsNotInDeck = 0xC2BA

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
TEXT_READ = {0xCD05: 2, 0xCD0A: 1, 0xCAA0: 5}
VRAM_FIRST = {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}
VRAM_SECOND = VRAM_FIRST

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCardPageNumber = 0xCBC7
wLoadedCard1Type = 0xCC24

wPracticeDuelTextPointer = 0xCC01
wPracticeDuelTextY = 0xCBCA

wCardPageNumber = 0xCBC7
wLCDC = 0xCABB

hWhoseTurn = 0xFF97
BGMAP0 = 0x9800
wPlayerNumberOfCardsInHand = 0xC2EE
wNumCardsBeingDrawn = 0xCBE9
wPlayerNumberOfCardsNotInDeck = 0xC2BA
wOpponentNumberOfCardsInHand = 0xC3EE
wOpponentNumberOfCardsNotInDeck = 0xC3BA
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wAnimationQueue = 0xD423
wAnimFlags = 0xD42B
wDuelAnimationScreen = 0xD4AE
wDuelAnimDuelistSide = 0xD4AF
wDuelAnimLocationParam = 0xD4B0
SPRITE_BUFFER = 0xD4D0
def entry_base(idx):
    return SPRITE_BUFFER + (min(idx, 15) * 16)

wLoadedCard1Name = 0xCC27
wLoadedCard1NonPokemonDescription = 0xCC2E
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
GENERIC_VREAD = {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
wAttachedEnergies = 0xCC1B
wTempCardID_ccc2 = 0xCCC2
WATER_ENERGY = 0x03
STARYU = 0x55

hWhoseTurn = 0xFF97
wTempCardID_ccc2 = 0xCCC2

hWhoseTurn = 0xFF97
wTempCardID_ccc2 = 0xCCC2
wSelectedAttack = 0xCCC6
wAttachedEnergies = 0xCC1B

wDuelTurns = 0xCC06

hWhoseTurn = 0xFF97

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
wConsole = 0xCAB4
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

wConsole = 0xCAB4
wLCDC = 0xCABB
wPokemonLengthPrintOffset = 0xCC03

hWhoseTurn = 0xFF97
hTemp_ffa0 = 0xFFA0

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
wConsole = 0xCAB4
wDefaultText = 0xC590
wLoadedCard1HP = 0xCC2C
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wConsole = 0xCAB4
wDefaultText = 0xC590
wLoadedCard1HP = 0xCC2C
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

hTempPlayAreaLocation_ff9d = 0xFF9D
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
wLoadedCard1Atk1Name = 0xCC34
wLoadedCard1Atk1Description = 0xCC36
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wConsole = 0xCAB4
wDefaultText = 0xC590
wLoadedCard1HP = 0xCC2C
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

hTempPlayAreaLocation_ff9d = 0xFF9D
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wConsole = 0xCAB4
wDefaultText = 0xC590
wLoadedCard1HP = 0xCC2C
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

hTempPlayAreaLocation_ff9d = 0xFF9D
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wConsole = 0xCAB4
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
wDuelDisplayedScreen = 0xCAC2
wDuelTempList = 0xC510
wExcludeArenaPokemon = 0xCBD2
wNumPlayAreaItems = 0xCBC8
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerArenaCard = 0xC2BB

hTempCardIndex_ff9f = 0xFF9F
hTempPlayAreaLocation_ff9d = 0xFF9D
hTemp_ffa0 = 0xFFA0
wLoadedAttackName = 0xCCAA
wSkipDuelistIsThinkingDelay = 0xCBF9
wTxRam2_b = 0xCE41
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wConsole = 0xCAB4
wDuelType = 0xCE22
DUELVARS_ARENA_CARD_HP_OFF = 0xC8 - 0xBB
DUELVARS_ARENA_CARD_STAGE_OFF = 0xCE - 0xBB
DUELVARS_ARENA_CARD_STATUS_OFF = 0xF0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF = 0xE0 - 0xBB
DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF = 0xDA - 0xBB

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerArenaCard = 0xC2BB
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerArenaCard = 0xC2BB
wExcludeArenaPokemon = 0xCBD2
wNumPlayAreaItems = 0xCBC8

hTempCardIndex_ff9f = 0xFF9F
wAlreadyPlayedEnergy = 0xCC0B
wLoadedCard1Stage = 0xCC2D
wLoadedCard1Type = 0xCC24

wSkipDuelistIsThinkingDelay = 0xCBF9

hCurMenuItem = 0xFFB1
V0_TILES1 = 0x8800

hKeysPressed = 0xFF91
hKeysReleased = 0xFF8E
hCurMenuItem = 0xFFB1

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
wArenaCard = 0xC2BB
hTempPlayAreaLocation_ff9d = 0xFF9D
wSelectedAttack = 0xCCC6
wSamePokemonCardID = 0xCDF9

hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
wSelectedAttack = 0xCCC6

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wOpponentDeckID = 0xCC0E
hWhoseTurn = 0xFF97
ARTICUNO_SCORE = 0xCDE5

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
wLoadedCard1AIInfo = 0xCC64
wLoadedCard1HP = 0xCC2C
wSelectedAttack = 0xCCC6

wDuelDisplayedScreen = 0xCAC2
wLoadedCard1Type = 0xCC24

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
wHUDEnergyAndHPBarsX = 0xCBC9
wHUDEnergyAndHPBarsY = 0xCBCA

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
HUD_TILE = 0x996F

wDuelTempList = 0xC510
wCardListScratch = 0xC51A

hWhoseTurn = 0xFF97
wDuelDisplayedScreen = 0xCAC2
wPlayerDuelistType = 0xC2F1
wOpponentDuelistType = 0xC3F1
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wSelectedDuelSubMenuItem = 0xCBCF
wSortCardListByID = 0xCBDF
wPrintSortNumberInCardListPtr = 0xCBD8
wCardListInfoBoxText = 0xCBDA
wCardListHeaderText = 0xCBDC
wCardListItemSelectionMenuType = 0xCBDE
wNoItemSelectionMenuKeys = 0xCBD6
wDuelTempList = 0xC510
wCardListScratch = 0xC51A

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
wWhoseTurn = 0xCC05
HUD_TILE = 0x996F
HUD_SEED = {hWhoseTurn: b"\xC2", wWhoseTurn: b"\xC2", 0xC2BB: b"\xFF", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC2F0: b"\x00", 0xC2F1: b"\x00", 0xC3BB: b"\xFF", 0xC3EC: b"\x00", 0xC3EF: b"\x00", 0xC3F0: b"\x00", 0xC3F1: b"\x00"}
HUD_BUDGET = {"instruction_budget": 20000000, "cycle_budget": 80000000}

hWhoseTurn = 0xFF97
wOpponentDuelistType = 0xC2F1
wDuelDisplayedScreen = 0xCAC2
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDuelTempList = 0xC510
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDuelDisplayedScreen = 0xCAC2
wLCDC = 0xCABB
wOpponentTurnEnded = 0xCBE1

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hWhoseTurn = 0xFF97
wDuelTempList = 0xC510
wListItemXPosition = 0xCD1A
wNumListItems = 0xCD1B

hWhoseTurn = 0xFF97
wPlayerArenaCard = 0xC2BB
wPlayerDeck = 0xC400

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wLoadedCard1AttackDescriptions = 0xCEA0

wEnergyDiscardMenuDenominator = 0xCBFA
wEnergyDiscardMenuNumerator = 0xCBFB

wEnergyCardsRequiredToRetreat = 0xCBCC
hTempRetreatCostCards = 0xFFA2

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wCardPageExitKeys = 0xCBD7
wCardPageNumber = 0xCBC7
wCardPageType = 0xCBD1

DCDS_TURN = 0xC2
DCDS_hWhoseTurn = 0xFF97
DCDS_wPlayerDeck = 0xC400
DCDS_wLoadedCard1 = 0xCC24
DCDS_wLCDC = 0xCABB
DCDS_rLCDC = 0xFF40

DUT_hTempCardIndex_ff9f = 0xFF9F
DUT_hWhoseTurn = 0xFF97
DUT_TURN = 0xC2
DUT_wPlayerDeck = 0xC400
DUT_wLoadedCard1 = 0xCC24
DUT_wLCDC = 0xCABB
DUT_rLCDC = 0xFF40

wCardPageExitKeys = 0xCBD7

wCardPageType = 0xCBD1
wCurPlayAreaSlot = 0xCBC9
wCurPlayAreaY = 0xCBCA
wLoadedCard1Atk1Name = 0xCC34
wLoadedCard1Atk2Name = 0xCC47
wLoadedCard1HP = 0xCC2C
wLoadedCard1Level = 0xCC5D
wLoadedCard1PokedexNumber = 0xCC5B
wLoadedCard1PreEvoName = 0xCC2E
wLoadedCard1Resistance = 0xCC58
wLoadedCard1RetreatCost = 0xCC56
wLoadedCard1Stage = 0xCC2D
wLoadedCard1Weakness = 0xCC57

SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wLoadedCard1NonPokemonDescription = 0xCC2E
# <<< factory-cases-statics

# >>> factory CheckIfEnoughEnergiesForGivenAttack
CONTRACT["CheckIfEnoughEnergiesForGivenAttack"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["CheckIfEnoughEnergiesForGivenAttack"] = [
	{"d": 0x00, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck: b"\x10", wAttachedEnergies: b"\x00\x00\x00\x00", wTotalAttachedEnergies: b"\x00"}},
	{"d": 0x01, "e": 0x01, "wram": {hWhoseTurn: b"\xC2", wPlayerDeck + 1: b"\x20", wAttachedEnergies: b"\x11\x11\x11\x00", wTotalAttachedEnergies: b"\x03"}},
	dict(POISON, d=0x05, e=0x01, wram={hWhoseTurn: b"\xC2", wPlayerDeck + 5: b"\x20", wAttachedEnergies: b"\x22\x22\x22\x00", wTotalAttachedEnergies: b"\x06"}),
]
# <<< factory CheckIfEnoughEnergiesForGivenAttack

# >>> factory SaveDuelData
CONTRACT["SaveDuelData"] = {"compare": (), "preserve": ()}
sCurrentDuel = 0xBC00
wDuelType = 0xCC09
CASES["SaveDuelData"] = [
    {"wram": {wDuelType: b"\x02"}, "sread": {0: {sCurrentDuel: 4}}},
    dict(POISON, wram={wDuelType: b"\x03", 0xC200: b"\x11\x22"}, sread={0: {sCurrentDuel: 4}}),
    {"wram": {wDuelType: b"\x00"}, "sread": {0: {sCurrentDuel: 1}}},
]
# <<< factory SaveDuelData

# >>> factory SetCardListHeaderText
CONTRACT["SetCardListHeaderText"] = {"compare": (), "preserve": ()}
CASES["SetCardListHeaderText"] = [
	{"d": 0x12, "e": 0x34, "hl": 0x0000, "wram": {0xCBDC: b"\x00\x00"}, "expect": {0xCBDC: b"\x34\x12"}},
	{"d": 0xAB, "e": 0xCD, "hl": 0x0000, "wram": {0xCBDC: b"\xFF\xFF"}, "expect": {0xCBDC: b"\xCD\xAB"}},
	dict(POISON, d=0xDD, e=0xEE, hl=0x1234, wram={0xCBDC: b"\x00\x00"}, expect={0xCBDC: b"\xEE\xDD"}),
]
# <<< factory SetCardListHeaderText

# >>> factory AIAttachEnergyInHandToCardInPlayArea
CONTRACT["AIAttachEnergyInHandToCardInPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIAttachEnergyInHandToCardInPlayArea"] = [
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00\x01", 0xC400: b"\xCB\x01"}, expect_regs={"a": 0xFF, "f": 0xC0}),
]
# <<< factory AIAttachEnergyInHandToCardInPlayArea

# >>> factory GoToPreviousCardPage
CONTRACT["GoToPreviousCardPage"] = {"compare": ("a", "f"), "preserve": ()}
CASES["GoToPreviousCardPage"] = [
    {"wram": {wCardPageNumber: b"\x02"}, "read": {wCardPageNumber: 1}},
    dict(POISON, wram={wCardPageNumber: b"\x02"}, read={wCardPageNumber: 1}),
]
# <<< factory GoToPreviousCardPage

# >>> factory DrawWholeScreenTextBox
CONTRACT["DrawWholeScreenTextBox"] = {"compare": (), "preserve": ()};
CASES["DrawWholeScreenTextBox"] = [
    {"hl": 0x01DB, "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, hl=0x01DB, keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory DrawWholeScreenTextBox

# >>> factory HasAlivePokemonInPlayArea
CONTRACT["HasAlivePokemonInPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HasAlivePokemonInPlayArea"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x01", 0xC2C8: b"\x10"},
     "read": {0xCBD2: 1, 0xCBD3: 1, 0xCBD4: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03",
              0xC2C8: b"\x00\x10\x00"}, "read": {0xCBD2: 1}},
    dict(POISON, wram={0xFF97: b"\xC3", 0xC3EF: b"\x02",
                       0xC3C8: b"\x00\x00"}),
]
# <<< factory HasAlivePokemonInPlayArea

# >>> factory CardPageSwitch_PokemonAttack1Page1
CONTRACT["CardPageSwitch_PokemonAttack1Page1"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["CardPageSwitch_PokemonAttack1Page1"] = [
    {"wram": {0xCC34: b"\x00\x00", 0xCC36: b"\x12\x34"}},
    {"wram": {0xCC34: b"\x0F\xF0", 0xCC36: b"\x00\x00"}},
    {"wram": {0xCC34: b"\x00\x01", 0xCC36: b"\xAA\xBB"}},
    dict(POISON, wram={0xCC34: b"\x12\x34", 0xCC36: b"\x00\x00"}),
    {"b": 1, "c": 2, "d": 3, "e": 4, "wram": {0xCC34: b"\x80\x00", 0xCC36: b"\xFF\xEE"}},
]
# <<< factory CardPageSwitch_PokemonAttack1Page1

# >>> factory CheckPrintDoublePoisoned
CONTRACT["CheckPrintDoublePoisoned"] = {"compare": ("a",), "preserve": ()}
CASES["CheckPrintDoublePoisoned"] = [
    {"a": 0x00, "b": 0x01, "c": 0x02, "read": {0x9841: 1}},
    {"a": 0x40, "b": 0x02, "c": 0x03, "read": {0x9862: 1}},
    {"a": 0x80, "b": 0x03, "c": 0x04, "read": {0x9883: 1}},
    {"a": 0xC0, "b": 0x04, "c": 0x05, "read": {0x98A4: 1}},
    dict(POISON),
]
# <<< factory CheckPrintDoublePoisoned

# >>> factory PrintPracticeDuelLetsPlayTheGame
CONTRACT["PrintPracticeDuelLetsPlayTheGame"] = {"compare": ("a", "f"), "preserve": ("a", "f")}
CASES["PrintPracticeDuelLetsPlayTheGame"] = [
    {"keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
]
# <<< factory PrintPracticeDuelLetsPlayTheGame

# >>> factory AIAttachEnergyInHandToCardInBench
CONTRACT["AIAttachEnergyInHandToCardInBench"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIAttachEnergyInHandToCardInBench"] = [
	dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00\x01", 0xC400: b"\xCB\x01"}, expect_regs={"a": 0xFF, "f": 0xC0}),
]
# <<< factory AIAttachEnergyInHandToCardInBench

# >>> factory DrawPracticeDuelInstructionsTextBox
CONTRACT["DrawPracticeDuelInstructionsTextBox"] = {"compare": (), "preserve": ()};
CASES["DrawPracticeDuelInstructionsTextBox"] = [
    {"wram": {0xCC06: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, wram={0xCC06: b"\x06"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory DrawPracticeDuelInstructionsTextBox

# >>> factory PracticeDuelVerify_Turn7Or8
CONTRACT["PracticeDuelVerify_Turn7Or8"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuelVerify_Turn7Or8"] = [
    {"wram": {0xCCC2: b"\x56", 0xCCC6: b"\x01"}},
    {"wram": {0xCCC2: b"\x00", 0xCCC6: b"\x01"}},
    dict(POISON, wram={0xCCC2: b"\x56", 0xCCC6: b"\x01"}),
]
# <<< factory PracticeDuelVerify_Turn7Or8

# >>> factory SetDiscardPileScreenTexts
CONTRACT["SetDiscardPileScreenTexts"] = {"compare": (), "preserve": ()}
CASES["SetDiscardPileScreenTexts"] = [
    {"hram": {hWhoseTurn: b"\xC2"}, "wram": {wCardListHeaderText: b"\x00\x00", wCardListInfoBoxText: b"\x00\x00"}, "expect": {wCardListHeaderText: b"\x17\x02", wCardListInfoBoxText: b"\x56\x00"}},
    {"hram": {hWhoseTurn: b"\x00"}, "wram": {wCardListHeaderText: b"\xFF\xFF", wCardListInfoBoxText: b"\xFF\xFF"}, "expect": {wCardListHeaderText: b"\x18\x02", wCardListInfoBoxText: b"\x56\x00"}},
    dict(POISON, hram={hWhoseTurn: b"\xC2"}, wram={wCardListHeaderText: b"\x00\x00", wCardListInfoBoxText: b"\x00\x00"}, expect={wCardListHeaderText: b"\x17\x02", wCardListInfoBoxText: b"\x56\x00"}),
]
# <<< factory SetDiscardPileScreenTexts

# >>> factory PrintAttachedEnergyToPokemon
CONTRACT["PrintAttachedEnergyToPokemon"] = {"compare": (), "preserve": ()}
CASES["PrintAttachedEnergyToPokemon"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00", hTempCardIndex_ff98: b"\x01", 0xC2BB: b"\x00", wPlayerDeck: b"\x08\x09"},
     "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 1000000, "cycle_budget": 4000000,
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9980: 0x400}, 1: {0x9980: 0x400}}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00", hTempCardIndex_ff98: b"\x01", 0xC2BB: b"\x00", wPlayerDeck: b"\x08\x09"},
         keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=1000000, cycle_budget=4000000,
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9980: 0x400}, 1: {0x9980: 0x400}}),
]
# <<< factory PrintAttachedEnergyToPokemon

# >>> factory PrintPokemonEvolvedIntoPokemon
CONTRACT["PrintPokemonEvolvedIntoPokemon"] = {"compare": (), "preserve": ()}
CASES["PrintPokemonEvolvedIntoPokemon"] = [
    {"wram": {wPreEvolutionPokemonCard: b"\x01"},
     "hram": {hTempCardIndex_ff98: b"\x02"},
     "keys": 0x01,
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 1000000, "cycle_budget": 4000000,
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9980: 0x400}, 1: {0x9980: 0x400}}},
    dict(POISON, wram={wPreEvolutionPokemonCard: b"\x01"},
         hram={hTempCardIndex_ff98: b"\x02"},
         keys=0x01,
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=1000000, cycle_budget=4000000,
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9980: 0x400}, 1: {0x9980: 0x400}}),
]
# <<< factory PrintPokemonEvolvedIntoPokemon

# >>> factory SetupDuel
CONTRACT["SetupDuel"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["SetupDuel"] = [
	{"wram": {0xCAB6: b"\xFF"}},
	dict(a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234, wram={0xCAB6: b"\xFF"}),
]
# <<< factory SetupDuel

# >>> factory PracticeDuelVerify_Turn6
CONTRACT["PracticeDuelVerify_Turn6"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuelVerify_Turn6"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerCardLocations: b"\x10" * 60, wPlayerDeck: b"\x03\x03\x03" + b"\x00" * 57, 0xC2C8: b"\x28", 0xCCC2: b"\x55"}},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerCardLocations: b"\x10" * 60, wPlayerDeck: b"\x03\x03" + b"\x00" * 58, 0xC2C8: b"\x28", 0xCCC2: b"\x55"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerCardLocations: b"\x10" * 60, wPlayerDeck: b"\x03\x03\x03" + b"\x00" * 57, 0xC2C8: b"\x28", 0xCCC2: b"\x55"}),
]
# <<< factory PracticeDuelVerify_Turn6

# >>> factory PracticeDuelVerify_Turn4
CONTRACT["PracticeDuelVerify_Turn4"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuelVerify_Turn4"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x12", wPlayerDeck: b"\x03", 0xC2EF: b"\x03", 0xCCC2: b"\x54", 0xCCC6: b"\x01"}},
    {"wram": {0xC2EF: b"\x02", 0xCCC2: b"\x54", 0xCCC6: b"\x01"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EF: b"\x03", 0xCCC2: b"\x54", 0xCCC6: b"\x01"}},
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x12", wPlayerDeck: b"\x03", 0xC2EF: b"\x03", 0xCCC2: b"\x55", 0xCCC6: b"\x01"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x12", wPlayerDeck: b"\x03", 0xC2EF: b"\x03", 0xCCC2: b"\x54", 0xCCC6: b"\x02"}),
]
# <<< factory PracticeDuelVerify_Turn4

# >>> factory ShuffleDeckAndDrawSevenCards
CONTRACT["ShuffleDeckAndDrawSevenCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ShuffleDeckAndDrawSevenCards"] = [
    {"wram": {0xFF97: b"\xC2", 0xCC09: b"\x80"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xCC09: b"\x80"}),
]
# <<< factory ShuffleDeckAndDrawSevenCards

# >>> factory WriteTwoDigitNumberInTxSymbol_PadSpace
CONTRACT["WriteTwoDigitNumberInTxSymbol_PadSpace"] = {"compare": (), "preserve": ()}
CASES["WriteTwoDigitNumberInTxSymbol_PadSpace"] = [
    write_case(0x00, 0x07, 0x04, d=0x12, e=0x34, hl=0x5678, expected=b"\x00\x20"),
    write_case(0x63, 0x1B, 0x3E, d=0x56, e=0x78, hl=0x0000, expected=b"\x29\x29"),
    write_case(0xAA, 0xBB, 0xCC, d=0xDD, e=0xEE, hl=0x1234, poison=True, expected=b"\x27\x20"),
]
# <<< factory WriteTwoDigitNumberInTxSymbol_PadSpace

# >>> factory PrintOpponentNumberOfHandAndDeckCards
CONTRACT["PrintOpponentNumberOfHandAndDeckCards"] = {"compare": (), "preserve": ()}
CASES["PrintOpponentNumberOfHandAndDeckCards"] = [
    {"wram": {wOpponentNumberOfCardsInHand: b"\x02", wNumCardsBeingDrawn: b"\x03", wOpponentNumberOfCardsNotInDeck: b"\x0A"},
     "vram": {0: {0x9865: b"\xA5\xA5", 0x986B: b"\xA5\xA5"}},
     "expect_vram": {0: {0x9865: b"\x25\x25", 0x986B: b"\x24\x27"}}},
    {"wram": {wOpponentNumberOfCardsInHand: b"\x5A", wNumCardsBeingDrawn: b"\x09", wOpponentNumberOfCardsNotInDeck: b"\x00"},
     "vram": {0: {0x9865: b"\xA5\xA5", 0x986B: b"\xA5\xA5"}},
     "expect_vram": {0: {0x9865: b"\x29\x29", 0x986B: b"\x23\x21"}}},
    dict(POISON, wram={wOpponentNumberOfCardsInHand: b"\xAA", wNumCardsBeingDrawn: b"\x00", wOpponentNumberOfCardsNotInDeck: b"\x00"},
         vram={0: {0x9865: b"\xA5\xA5", 0x986B: b"\xA5\xA5"}},
         expect_vram={0: {0x9865: b"\x27\x20", 0x986B: b"\x26\x20"}}),
]
# <<< factory PrintOpponentNumberOfHandAndDeckCards

# >>> factory PrintPlayerNumberOfHandAndDeckCards
CONTRACT["PrintPlayerNumberOfHandAndDeckCards"] = {"compare": (), "preserve": ()}
CASES["PrintPlayerNumberOfHandAndDeckCards"] = [
    {"wram": {wPlayerNumberOfCardsInHand: b"\x02", wNumCardsBeingDrawn: b"\x03", wPlayerNumberOfCardsNotInDeck: b"\x0A"},
     "vram": {0: {0x9950: b"\xA5\xA5", 0x994A: b"\xA5\xA5"}},
     "expect_vram": {0: {0x9950: b"\x00\x25", 0x994A: b"\x24\x27"}}},
    {"wram": {wPlayerNumberOfCardsInHand: b"\x5A", wNumCardsBeingDrawn: b"\x09", wPlayerNumberOfCardsNotInDeck: b"\x00"},
     "vram": {0: {0x9950: b"\xA5\xA5", 0x994A: b"\xA5\xA5"}},
     "expect_vram": {0: {0x9950: b"\x29\x29", 0x994A: b"\x23\x21"}}},
    dict(POISON, wram={wPlayerNumberOfCardsInHand: b"\x00", wNumCardsBeingDrawn: b"\x00", wPlayerNumberOfCardsNotInDeck: b"\x00"}, vram={0: {0x9950: b"\xEE\xEE", 0x994A: b"\xEE\xEE"}}, expect_vram={0: {0x9950: b"\x00\x20", 0x994A: b"\x26\x20"}}),
]
# <<< factory PrintPlayerNumberOfHandAndDeckCards

# >>> factory PrintDuelResultStats
CONTRACT["PrintDuelResultStats"] = {"compare": (), "preserve": ()}
CASES["PrintDuelResultStats"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EC: b"\x15", 0xC2EF: b"\x01", 0xC2BA: b"\x1E", 0xC3EC: b"\x3F", 0xC3EF: b"\x00", 0xC3BA: b"\x3C"}, "setup": SETUP_TEXT, "read": TEXT_READ},
    {"wram": {0xFF97: b"\xC2", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC2BA: b"\x3C", 0xC3EC: b"\x01", 0xC3EF: b"\x02", 0xC3BA: b"\x00"}, "setup": SETUP_TEXT, "read": TEXT_READ},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EC: b"\x01", 0xC2EF: b"\x02", 0xC2BA: b"\x1E", 0xC3EC: b"\x08", 0xC3EF: b"\x01", 0xC3BA: b"\x01"}, setup=SETUP_TEXT, read=TEXT_READ),
]
# <<< factory PrintDuelResultStats

# >>> factory ConvertColorToEnergyCardID
CONTRACT["ConvertColorToEnergyCardID"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ConvertColorToEnergyCardID"] = [
    {},
    dict(POISON, a=0),
]
# <<< factory ConvertColorToEnergyCardID

# >>> factory WriteOneByteNumberInTxSymbol_PadSpace
CONTRACT["WriteOneByteNumberInTxSymbol_PadSpace"] = {"compare": (), "preserve": ()}
CASES["WriteOneByteNumberInTxSymbol_PadSpace"] = [
    {"a": 0x00, "b": 0x07, "c": 0x04, "d": 0x12, "e": 0x34, "hl": 0x5678,
     "wram": {0xCAA0: b"\xff" * 6},
     "vram": {0: {0x9887: b"\xee" * 4}},
     "expect_vram": {0: {0x9887: b"\x00\x20\xff\xee"}}},
    {"a": 0x63, "b": 0x1B, "c": 0x3E, "d": 0x56, "e": 0x78, "hl": 0x0000,
     "wram": {0xCAA0: b"\xff" * 6},
     "vram": {0: {0x9FDB: b"\xee" * 4}},
     "expect_vram": {0: {0x9FDB: b"\x29\x29\xff\xee"}}},
    dict(POISON,
         wram={0xCAA0: b"\xff" * 6},
         sram={0: {0xAF1B: b"\xee" * 4}},
         expect_sram={0: {0xAF1B: b"\x27\x20\xff\xee"}}),
]
# <<< factory WriteOneByteNumberInTxSymbol_PadSpace

# >>> factory PrintPracticeDuelNumberedInstruction
CONTRACT["PrintPracticeDuelNumberedInstruction"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintPracticeDuelNumberedInstruction"] = [
    {"d": 0x20, "e": 0x40, "hl": 0xC500,
     "wram": {0xC502: b"\xA9\x01", 0xC504: b"\x00\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD08: 1, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    {"d": 0x01, "e": 0x08, "hl": 0xC500,
     "wram": {0xC502: b"\xAA\x01", 0xC504: b"\xFF\xFF"},
     "setup": [{"fn": "SetupText", "d": 0x01, "e": 0x08}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD08: 1, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, hl=0xC500,
         wram={0xC502: b"\xAA\x01", 0xC504: b"\x00\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD08: 1, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory PrintPracticeDuelNumberedInstruction

# >>> factory PrintNextPracticeDuelInstruction
CONTRACT["PrintNextPracticeDuelInstruction"] = {"compare": (), "preserve": (), "hram_out": True}
CASES["PrintNextPracticeDuelInstruction"] = [
    {"wram": {0xCC01: b"\x00\xC5", 0xCBCA: b"\x00", 0xC500: b"\x00"},
     "hram": {0xFFB0: b"\x7F"},
     "read": {0xFFB0: 1}},
    dict(POISON,
         wram={0xCC01: b"\x00\xC5", 0xCBCA: b"\x00", 0xC500: b"\x00"},
         hram={0xFFB0: b"\x7F"},
         read={0xFFB0: 1}),
]
# <<< factory PrintNextPracticeDuelInstruction

# >>> factory GoToFirstOrNextCardPage
CONTRACT["GoToFirstOrNextCardPage"] = {"compare": ("a", "f"), "preserve": ()}
CASES["GoToFirstOrNextCardPage"] = [
    {"wram": {wCardPageNumber: b"\x00", wLoadedCard1Type: b"\x08"}, "read": {wCardPageNumber: 1}},
    {"wram": {wCardPageNumber: b"\x00", wLoadedCard1Type: b"\x10"}, "read": {wCardPageNumber: 1}},
    {"wram": {wCardPageNumber: b"\x00", wLoadedCard1Type: b"\x00"}, "read": {wCardPageNumber: 1}},
    dict(POISON, wram={wCardPageNumber: b"\x00", wLoadedCard1Type: b"\x00"}, read={wCardPageNumber: 1}),
]
# <<< factory GoToFirstOrNextCardPage

# >>> factory PrintPracticeDuelInstructions
CONTRACT["PrintPracticeDuelInstructions"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintPracticeDuelInstructions"] = [
    {"hl": 0xC500, "keys": 0x01,
     "wram": {0xC500: b"\x00"},
     "expect": {0xCC01: b"\x00\xC5", 0xCBCA: b"\x00"},
     "read": {0xCC01: 2, 0xCBCA: 1, 0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}},
    dict(POISON, hl=0xC500, keys=0x01,
         wram={0xC500: b"\x00"},
         expect={0xCC01: b"\x00\xC5", 0xCBCA: b"\x00"},
         read={0xCC01: 2, 0xCBCA: 1, 0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}),
]
# <<< factory PrintPracticeDuelInstructions

# >>> factory DisplayPreviousCardPage
CONTRACT["DisplayPreviousCardPage"] = {"compare": (), "preserve": ()}
CASES["DisplayPreviousCardPage"] = [
    {"wram": {wCardPageNumber: b"\x01", wLCDC: b"\x00"}, "hram": {0xFF40: b"\x00"}, "expect": {0xFF40: b"\x00"}},
    dict(POISON, wram={wCardPageNumber: b"\x01", wLCDC: b"\x00"}, hram={0xFF40: b"\x00"}, expect={0xFF40: b"\x00"}),
]
# <<< factory DisplayPreviousCardPage

# >>> factory PrintNumberOfHandAndDeckCards
CONTRACT["PrintNumberOfHandAndDeckCards"] = {"compare": (), "preserve": ()}
CASES["PrintNumberOfHandAndDeckCards"] = [
    {"hram": {hWhoseTurn: b"\xC2"},
     "wram": {wPlayerNumberOfCardsInHand: b"\x02", wNumCardsBeingDrawn: b"\x03", wPlayerNumberOfCardsNotInDeck: b"\x0A"},
     "vram": {0: {BGMAP0 + 10 * 32 + 16: b"\xA5\xA5", BGMAP0 + 10 * 32 + 10: b"\xA5\xA5"}},
     "expect_vram": {0: {BGMAP0 + 10 * 32 + 16: b"\x00\x25", BGMAP0 + 10 * 32 + 10: b"\x24\x27"}}},
    {"hram": {hWhoseTurn: b"\x00"},
     "wram": {wOpponentNumberOfCardsInHand: b"\x02", wNumCardsBeingDrawn: b"\x03", wOpponentNumberOfCardsNotInDeck: b"\x0A"},
     "vram": {0: {0x9865: b"\xA5\xA5", 0x986B: b"\xA5\xA5"}},
     "expect_vram": {0: {0x9865: b"\x25\x25", 0x986B: b"\x24\x27"}}},
    dict(POISON, hram={hWhoseTurn: b"\xC2"},
         wram={wPlayerNumberOfCardsInHand: b"\x00", wNumCardsBeingDrawn: b"\x00", wPlayerNumberOfCardsNotInDeck: b"\x00"},
         vram={0: {BGMAP0 + 10 * 32 + 16: b"\xEE\xEE\xEE", BGMAP0 + 10 * 32 + 10: b"\xEE\xEE\xEE"}},
         expect_vram={0: {BGMAP0 + 10 * 32 + 16: b"\x20\x00\xEE", BGMAP0 + 10 * 32 + 10: b"\x26\x20\xEE"}}),
]
# <<< factory PrintNumberOfHandAndDeckCards

# >>> factory PrintReturnCardsToDeckDrawAgain
CONTRACT["PrintReturnCardsToDeckDrawAgain"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["PrintReturnCardsToDeckDrawAgain"] = [
    {"keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 1000000, "cycle_budget": 4000000},
    dict(POISON, keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=1000000, cycle_budget=4000000),
]
# <<< factory PrintReturnCardsToDeckDrawAgain

# >>> factory PracticeDuelVerify_Turn3
CONTRACT["PracticeDuelVerify_Turn3"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PracticeDuelVerify_Turn3"] = [
    {"wram": {0xCCC2: b"\x54", 0xFF97: b"\xC2"}},
    dict(POISON, wram={0xCCC2: b"\x00", 0xFF97: b"\xC2"}),
]
# <<< factory PracticeDuelVerify_Turn3

# >>> factory CheckIfEnoughEnergiesToAttack
CONTRACT["CheckIfEnoughEnergiesToAttack"] = {"compare": ("a", "f", "d", "e", "b", "c", "hl"), "preserve": ("b", "c", "hl"), "wram_out": True}
CASES["CheckIfEnoughEnergiesToAttack"] = [
    {"wram": {0xFF97: b"\xC2", 0xFFB1: b"\x00", 0xC510: b"\x00\x00", 0xC400: b"\x10"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFFB1: b"\x01", 0xC512: b"\x01\x01", 0xC401: b"\x20"}),
]
# <<< factory CheckIfEnoughEnergiesToAttack

# >>> factory PlayTurnDuelistDrawAnimation
CONTRACT["PlayTurnDuelistDrawAnimation"] = {"compare": ("e", "f"), "preserve": ()}
_ANIM_SAFE = {0xD42A: b"\xff", 0xD4C0: b"\xff", 0xD423: b"\xff" * 7,
              0xCAD3: bytes([0xA2, 0x3B]), 0xD4AC: b"\x00", 0xD4AD: b"\x08"}
CASES["PlayTurnDuelistDrawAnimation"] = [
    {"wram": {**_ANIM_SAFE, 0xFF97: b"\xC2", 0xCCF2: b"\x01"}, "keys": 0x02},
    dict(POISON, wram={**_ANIM_SAFE, 0xFF97: b"\xC2", 0xCCF2: b"\x01"}, keys=0x02),
    {"wram": {**_ANIM_SAFE, 0xFF97: b"\xC3", 0xCCF2: b"\x01"}, "keys": 0x02},
]
# <<< factory PlayTurnDuelistDrawAnimation

# >>> factory DrawCardPageSet2AndRarityIcons
CONTRACT["DrawCardPageSet2AndRarityIcons"] = {"compare": ("hl",), "preserve": ()}
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CASES["DrawCardPageSet2AndRarityIcons"] = [
    {"wram": {0xCC29: b"\xff", 0xCC2A: b"\x01"}, "setup": SETUP_TEXT, "rom_bank": 1},
    dict(POISON, wram={0xCC29: b"\xff", 0xCC2A: b"\x01"}, setup=SETUP_TEXT, rom_bank=1),
    {"wram": {0xCC29: b"\x00", 0xCC2A: b"\x00"}, "setup": SETUP_TEXT, "rom_bank": 1},
    {"wram": {0xCC29: b"\x00", 0xCC2A: b"\x07"}, "setup": SETUP_TEXT, "rom_bank": 1},
]
# <<< factory DrawCardPageSet2AndRarityIcons

# >>> factory CountOppEnergyCardsInHandAndAttached
CONTRACT["CountOppEnergyCardsInHandAndAttached"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["CountOppEnergyCardsInHandAndAttached"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x02", 0xC242: b"\x00\x01",
               0xC400: b"\x01\xCB", 0xC2EF: b"\x01"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00",
               0xC400: b"\xCB", 0xC2EF: b"\x01", 0xC205: b"\x10", 0xC405: b"\x01"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x02", 0xC242: b"\x00\x01",
                        0xC400: b"\x01\xCB", 0xC2EF: b"\x01"}),
]
# <<< factory CountOppEnergyCardsInHandAndAttached

# >>> factory AIPickPrizeCards
CONTRACT["AIPickPrizeCards"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["AIPickPrizeCards"] = [
    {"wram": {0xFF97: b"\xC3", 0xCCC8: b"\x01", 0xC3EC: b"\x3F", 0xC3EE: b"\x00",
               0xC33C: b"\x00\x00\x00\x00\x00\x00"},
     "read": {0xC3EC: 1, 0xC3EE: 1, 0xC342: 1}},
    dict(POISON, wram={0xFF97: b"\xC3", 0xCCC8: b"\x01", 0xC3EC: b"\x3F", 0xC3EE: b"\x00",
                        0xC33C: b"\x00\x00\x00\x00\x00\x00"},
         read={0xC3EC: 1, 0xC3EE: 1, 0xC342: 1}),
]
# <<< factory AIPickPrizeCards

# >>> factory HandleAIEnergyScoringForRepeatedBenchPokemon
CONTRACT["HandleAIEnergyScoringForRepeatedBenchPokemon"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIEnergyScoringForRepeatedBenchPokemon"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "instruction_budget": 2000000,
        "cycle_budget": 8000000,
        "wram": {0xC2BC: b"\xFF"},   # wPlayerDuelVariables DUELVARS_BENCH[0] = 0xFF (empty bench)
        "hram": {0xFF97: b"\xC2"},
        "expect_regs": {"a": 0xFF, "f": 0xC0},
    },
]
# <<< factory HandleAIEnergyScoringForRepeatedBenchPokemon

# >>> factory CheckPrintCnfSlpPrz
CONTRACT["CheckPrintCnfSlpPrz"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["CheckPrintCnfSlpPrz"] = [
    {"a": 0x00, "b": 0x05, "c": 0x03, "vread": {0: {0x9865: 1}}},
    {"a": 0x01, "b": 0x05, "c": 0x03, "vread": {0: {0x9865: 1}}},
    {"a": 0x02, "b": 0x05, "c": 0x03, "vread": {0: {0x9865: 1}}},
    dict(POISON, a=0x03, b=0x05, c=0x03, vread={0: {0x9865: 1}}),
]
# <<< factory CheckPrintCnfSlpPrz

# >>> factory LoadAnimCoordsAndFlags
CONTRACT["LoadAnimCoordsAndFlags"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["LoadAnimCoordsAndFlags"] = [
    {"wram": {wAnimationQueue: b"\x02", wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x00",
              wDuelAnimDuelistSide: b"\x00", wDuelAnimLocationParam: b"\x00",
              entry_base(2) + 1: b"\x80\x00\x00", entry_base(2) + 15: b"\x80\x00"},
     "read": {entry_base(2) + 1: 3, entry_base(2) + 15: 2}},
    dict(POISON, wram={wAnimationQueue: b"\x05", wAnimFlags: b"\x04", wDuelAnimationScreen: b"\x00",
                       wDuelAnimDuelistSide: b"\x00", wDuelAnimLocationParam: b"\x00",
                       entry_base(5) + 1: b"\x00\x00\x00", entry_base(5) + 15: b"\x00\x00"},
         read={entry_base(5) + 1: 3, entry_base(5) + 15: 2}),
    {"wram": {wAnimationQueue: b"\x00", wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x01",
              wDuelAnimDuelistSide: b"\xc2", wDuelAnimLocationParam: b"\x03",
              entry_base(0) + 1: b"\x00\x00\x00", entry_base(0) + 15: b"\x00\x00"},
     "read": {entry_base(0) + 1: 3, entry_base(0) + 15: 2}},
    {"wram": {wAnimationQueue: b"\x10", wAnimFlags: b"\x00", wDuelAnimationScreen: b"\x00",
              wDuelAnimDuelistSide: b"\x00", wDuelAnimLocationParam: b"\x00",
              entry_base(15) + 1: b"\x10\x00\x00", entry_base(15) + 15: b"\x20\x00"},
     "read": {entry_base(15) + 1: 3, entry_base(15) + 15: 2}},
]
# <<< factory LoadAnimCoordsAndFlags

# >>> factory PrintUsedTrainerCardDescription
CONTRACT["PrintUsedTrainerCardDescription"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintUsedTrainerCardDescription"] = [
    {"keys": 0x01, "wram": {wLoadedCard1Name: b"\x33\x00", wLoadedCard1NonPokemonDescription: b"\x00\x00"},
     "setup": SETUP,
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "vread": GENERIC_VREAD},
    dict(POISON, keys=0x01, wram={wLoadedCard1Name: b"\x33\x00", wLoadedCard1NonPokemonDescription: b"\x00\x00"},
         setup=SETUP,
         instruction_budget=2000000, cycle_budget=8000000,
         vread=GENERIC_VREAD),
]
# <<< factory PrintUsedTrainerCardDescription

# >>> factory PracticeDuelVerify_Turn5
CONTRACT["PracticeDuelVerify_Turn5"] = {"compare": ("f",), "preserve": (), "wram_out": True}
CASES["PracticeDuelVerify_Turn5"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x10\x10",
              wPlayerDeck: bytes((WATER_ENERGY, WATER_ENERGY)),
              wTempCardID_ccc2: bytes((STARYU,))}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables: b"\x10\x10\x10",
                       wPlayerDeck: bytes((WATER_ENERGY, WATER_ENERGY, STARYU)),
                       wTempCardID_ccc2: b"\x00"}),
]
# <<< factory PracticeDuelVerify_Turn5

# >>> factory PracticeDuelVerify_Turn1
CONTRACT["PracticeDuelVerify_Turn1"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuelVerify_Turn1"] = [
    {"wram": {hWhoseTurn: b"\xC2", wTempCardID_ccc2: b"\x53"}},
    {"wram": {hWhoseTurn: b"\xC2", wTempCardID_ccc2: b"\x54"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wTempCardID_ccc2: b"\x53"}),
]
# <<< factory PracticeDuelVerify_Turn1

# >>> factory PracticeDuelVerify_Turn2
CONTRACT["PracticeDuelVerify_Turn2"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuelVerify_Turn2"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wTempCardID_ccc2: b"\x54", wSelectedAttack: b"\x01", 0xC300 + 0x05: b"\x01"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wTempCardID_ccc2: b"\x55", wSelectedAttack: b"\x01"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wTempCardID_ccc2: b"\x54", wSelectedAttack: b"\x02"}},
    {"wram": {hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wTempCardID_ccc2: b"\x54", wSelectedAttack: b"\x01"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC000: b"\x00" * 0xF00, wTempCardID_ccc2: b"\x54", wSelectedAttack: b"\x01", 0xC300 + 0x05: b"\x01"}),
]
# <<< factory PracticeDuelVerify_Turn2

# >>> factory PracticeDuel_PlayStaryuFromBench
CONTRACT["PracticeDuel_PlayStaryuFromBench"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuel_PlayStaryuFromBench"] = [
    {"wram": {wDuelTurns: b"\x05"}},
    {"wram": {wDuelTurns: b"\x00"}},
    dict(POISON, wram={wDuelTurns: b"\x05"}),
    {"wram": {wDuelTurns: b"\x07"}, "oracle": False,
     "why": "PrintPracticeDuelInstructions walks the real PracticeDuelText_SamTurn4 table (2 scrollable-text pages plus a final print), each needing a fresh button press-then-release edge; the harness keys field is a single static value and cannot simulate that sequence, so the run never terminates under any budget. DrawPracticeDuelInstructionsTextBox, EnableLCD, and PrintPracticeDuelInstructions are independently verified by their own landed suites; this case only confirms the draw branch is entered with the correct table pointer.",
     "expect": {0xCC01: b"\x46\x53", 0xCBCA: b"\x00"}},
]
# <<< factory PracticeDuel_PlayStaryuFromBench

# >>> factory DisplayDuelistTurnScreen
CONTRACT["DisplayDuelistTurnScreen"] = {"compare": (), "preserve": ()}
CASES["DisplayDuelistTurnScreen"] = [
    {"wram": {hWhoseTurn: b"\xC2"},
     "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}}},
    {"wram": {hWhoseTurn: b"\xC3"},
     "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}}},
    dict(POISON, wram={hWhoseTurn: b"\xC2"},
         keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=2000000, cycle_budget=8000000,
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}}),
]
# <<< factory DisplayDuelistTurnScreen

# >>> factory DrawDuelistPortraitsAndNames
CONTRACT["DrawDuelistPortraitsAndNames"] = {"compare": (), "preserve": (), "wram_out": True, "vram_out": True}
CASES["DrawDuelistPortraitsAndNames"] = [
    {"wram": {0xCC15: b"\x02"}, "sram": {0: {0xA010: b"\x21\x22\x00"}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xD61E: 1}},
    dict(POISON, wram={0xCC15: b"\x02"}, sram={0: {0xA010: b"\x21\x22\x00"}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xD61E: 1}),
]
# <<< factory DrawDuelistPortraitsAndNames

# >>> factory CheckEnergyNeededForAttack
CONTRACT["CheckEnergyNeededForAttack"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["CheckEnergyNeededForAttack"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08",
              0xCCC6: b"\x00", 0xCC23: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08",
                        0xCCC6: b"\x00", 0xCC23: b"\x00"}),
]
# <<< factory CheckEnergyNeededForAttack

# >>> factory CreateDamageCharSprite
CONTRACT["CreateDamageCharSprite"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["CreateDamageCharSprite"] = [
    {"a": 1, "f": 0, "d": 0xC1, "e": 0x00,
     "wram": {0xFF80: b"\x07", 0xD618: b"\x00", 0xD4B7: b"\x02", 0xD4B8: b"\x05", 0xC100: b"\x00"},
     "read": {0xC100: 1, 0xD42B: 1}},
    dict(POISON, d=0xC1, e=0x00,
         wram={0xFF80: b"\x07", 0xD618: b"\x00", 0xD4B7: b"\x02", 0xD4B8: b"\x05", 0xC100: b"\x00"},
         read={0xC100: 1, 0xD42B: 1}),
]
# <<< factory CreateDamageCharSprite

# >>> factory HasAlivePokemonInBench
CONTRACT["HasAlivePokemonInBench"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HasAlivePokemonInBench"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EF: b"\x03", 0xC2C8: b"\x00\x10\x00"}, "read": {0xCBD2: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EF: b"\x03", 0xC2C8: b"\x00\x10\x00"}),
]
# <<< factory HasAlivePokemonInBench

# >>> factory DrawOpponentSelectionScreen
CONTRACT["DrawOpponentSelectionScreen"] = {"compare": (), "preserve": ()}
CASES["DrawOpponentSelectionScreen"] = [
    {"wram": {0xCC0E: b"\x00", 0xCC15: b"\x02", 0xCC18: b"\x03"},
     "sram": {0: {0xA010: b"\x21\x22\x00"}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "rom_bank": 1, "read": {0xCC15: 1}, "vread": {0: {0x9A05: 3}}},
    dict(POISON, wram={0xCC0E: b"\x00", 0xCC15: b"\x02", 0xCC18: b"\x03"},
         sram={0: {0xA010: b"\x21\x22\x00"}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         rom_bank=1, read={0xCC15: 1}),
]
# <<< factory DrawOpponentSelectionScreen

# >>> factory PracticeDuel_ReplaceKnockedOutPokemon
CONTRACT["PracticeDuel_ReplaceKnockedOutPokemon"] = {"compare": (), "preserve": ()}
CASES["PracticeDuel_ReplaceKnockedOutPokemon"] = [
    {"wram": {0xFF9D: b"\x01"}},
    {"wram": {0xFF9D: b"\x00", 0xFF97: b"\xC2", 0xC2EF: b"\x03", 0xC2C8: b"\x00\x10\x00"},
     "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}},
    dict(POISON, wram={0xFF9D: b"\x01"}),
]
# <<< factory PracticeDuel_ReplaceKnockedOutPokemon

# >>> factory DrawDamageAnimationArrow
CONTRACT["DrawDamageAnimationArrow"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawDamageAnimationArrow"] = [
    {"f": 0x00, "wram": {0xFF80: b"\x07", 0xD618: b"\x00", 0xD4B8: b"\x05", 0xD429: b"\x00\x00"},
     "read": {0xD4B7: 1}},
    dict(POISON, wram={0xFF80: b"\x07", 0xD618: b"\x00", 0xD4B8: b"\x05", 0xD429: b"\x00\x00"},
         read={0xD4B7: 1}),
]
# <<< factory DrawDamageAnimationArrow

# >>> factory DrawDamageAnimationWeak
CONTRACT["DrawDamageAnimationWeak"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawDamageAnimationWeak"] = [
    {"wram": {0xFF80: b"\x07"}, "read": {0xD4B7: 1}},
    dict(POISON, wram={0xFF80: b"\x07"}, read={0xD4B7: 1}),
]
# <<< factory DrawDamageAnimationWeak

# >>> factory DrawDamageAnimationResist
CONTRACT["DrawDamageAnimationResist"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawDamageAnimationResist"] = [
    {"wram": {0xFF80: b"\x07", 0xD4B8: b"\x05"}, "read": {0xD4B7: 1, 0xD4B8: 1}},
    dict(POISON, wram={0xFF80: b"\x07", 0xD4B8: b"\x05"}, read={0xD4B7: 1, 0xD4B8: 1}),
]
# <<< factory DrawDamageAnimationResist

# >>> factory DrawDamageAnimationNumbers
CONTRACT["DrawDamageAnimationNumbers"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawDamageAnimationNumbers"] = [
    {"wram": {0xFF80: b"\x07", 0xD4B1: b"\x2A\x00", 0xD4B6: b"\x00"}, "read": {0xD4B7: 1}},
    dict(POISON, wram={0xFF80: b"\x07", 0xD4B1: b"\x2A\x00", 0xD4B6: b"\x00"}, read={0xD4B7: 1}),
]
# <<< factory DrawDamageAnimationNumbers

# >>> factory Func_15886
CONTRACT["Func_15886"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_15886"] = [
    {"hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00"}),
]
# <<< factory Func_15886

# >>> factory CheckAbleToRetreat
CONTRACT["CheckAbleToRetreat"] = {"compare": ("f",), "preserve": ()}
CASES["CheckAbleToRetreat"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2E8: b"\x09"}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2E8: b"\x09"}),
]
# <<< factory CheckAbleToRetreat

# >>> factory LookForEnergyNeededInHand
CONTRACT["LookForEnergyNeededInHand"] = {"compare": ("f",), "preserve": ()}
CASES["LookForEnergyNeededInHand"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCC23: b"\x00"},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCC23: b"\x00"},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory LookForEnergyNeededInHand

# >>> factory Func_7364
CONTRACT["Func_7364"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_7364"] = [
    {"keys": 0x02, "wram": {0xCC0E: b"\x00", 0xCC15: b"\x02", 0xCC18: b"\x03"},
     "sram": {0: {0xA010: b"\x21\x22\x00"}}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=0x02, wram={0xCC0E: b"\x00", 0xCC15: b"\x02", 0xCC18: b"\x03"},
         sram={0: {0xA010: b"\x21\x22\x00"}}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_7364

# >>> factory CheckEnergyNeededForAttackAfterDiscard
CONTRACT["CheckEnergyNeededForAttackAfterDiscard"] = {"compare": ("f", "b", "c", "d", "e"), "preserve": ()}
CASES["CheckEnergyNeededForAttackAfterDiscard"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", wPlayerDeck: b"\x08", wSelectedAttack: b"\x00",
             hTempPlayAreaLocation_ff9d: b"\x00"}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", wPlayerDeck: b"\x08", wSelectedAttack: b"\x00",
             hTempPlayAreaLocation_ff9d: b"\x00"}),
]
# <<< factory CheckEnergyNeededForAttackAfterDiscard

# >>> factory DisplayFirstOrNextCardPage
CONTRACT["DisplayFirstOrNextCardPage"] = {"compare": ("a", "f", "b"), "preserve": ()}
CASES["DisplayFirstOrNextCardPage"] = [
    {"wram": {wCardPageNumber: b"\xFF"}, "read": {wCardPageNumber: 1}},
    dict(POISON, wram={wCardPageNumber: b"\xFF"}, read={wCardPageNumber: 1}),
]
# <<< factory DisplayFirstOrNextCardPage

# >>> factory PrintAttackOrCardDescription
CONTRACT["PrintAttackOrCardDescription"] = {"compare": ("a", "hl"), "preserve": ()}
CASES["PrintAttackOrCardDescription"] = [
    {"hl": 0xC500, "d": 0x01, "e": 0x0E, "wram": {0xC500: b"\x00\x00"}},
    dict(POISON, hl=0xC500, d=0x01, e=0x0E, wram={0xC500: b"\x00\x00"}),
]
# <<< factory PrintAttackOrCardDescription

# >>> factory PrintAttackOrPkmnPowerInformation
CONTRACT["PrintAttackOrPkmnPowerInformation"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["PrintAttackOrPkmnPowerInformation"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x00\x00"}},
    dict(POISON, hl=0xC500, wram={0xC500: b"\x00\x00"}),
]
# <<< factory PrintAttackOrPkmnPowerInformation

# >>> factory PrintAttackOrNonPokemonCardDescription
CONTRACT["PrintAttackOrNonPokemonCardDescription"] = {"compare": ("a", "f", "hl", "d", "e"), "preserve": ("d", "e")}
CASES["PrintAttackOrNonPokemonCardDescription"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x00\x00"}},
    dict(POISON, hl=0xC500, wram={0xC500: b"\x00\x00"}),
]
# <<< factory PrintAttackOrNonPokemonCardDescription

# >>> factory DisplayCardPageOnLeftOrRightPressed
CONTRACT["DisplayCardPageOnLeftOrRightPressed"] = {"compare": (), "preserve": ()}
CASES["DisplayCardPageOnLeftOrRightPressed"] = [
    {"a": 1 << 5, "wram": {wCardPageNumber: b"\x0E"}, "read": {wCardPageNumber: 1}},
    dict(POISON, a=1 << 5, wram={wCardPageNumber: b"\x0E"}, read={wCardPageNumber: 1}),
]
# <<< factory DisplayCardPageOnLeftOrRightPressed

# >>> factory PrintPlayAreaCardHeader
CONTRACT["PrintPlayAreaCardHeader"] = {"compare": (), "preserve": ()}
CASES["PrintPlayAreaCardHeader"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x04",
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "vread": {0: {0x9800 + 3 * 32: 32 * 5}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x01", wCurPlayAreaY: b"\x03",
              wConsole: b"\x02", wPlayerArenaCard + 1: b"\x01", wPlayerDeck + 1: b"\x08",
              wPlayerArenaCard + 1 + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x02",
              wPlayerArenaCard + 1 + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x05",
              wPlayerArenaCard + 1 + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x07"},
     "vread": {0: {0x9800 + 2 * 32: 32 * 5}, 1: {0x9800 + 2 * 32: 32 * 5}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x04",
                        wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
                        wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
                        wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
                        wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
                        wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
         vread={0: {0x9800 + 3 * 32: 32 * 5}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintPlayAreaCardHeader

# >>> factory PrintPokemonCardLength
CONTRACT["PrintPokemonCardLength"] = {"compare": (), "preserve": ()}
CASES["PrintPokemonCardLength"] = [
    {"instruction_budget": 20000000, "cycle_budget": 80000000,
     "hl": 0x0503, "b": 4, "c": 2, "wram": {wConsole: b"\x00", wLCDC: b"\x00"},
     "read": {wPokemonLengthPrintOffset: 1},
     "vread": {0: {0x9800: 32 * 8}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, instruction_budget=20000000, cycle_budget=80000000,
         hl=0x0503, b=4, c=2, wram={wConsole: b"\x00", wLCDC: b"\x00"},
         read={wPokemonLengthPrintOffset: 1},
         vread={0: {0x9800: 32 * 8}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintPokemonCardLength

# >>> factory PlayDeckShuffleAnimation
CONTRACT["PlayDeckShuffleAnimation"] = {"compare": ("a",), "preserve": ()}
CASES["PlayDeckShuffleAnimation"] = [
    {"keys": 0, "instruction_budget": 3000000, "cycle_budget": 10000000,
     "wram": {0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCAC2: b"\x09",
              0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=3000000, cycle_budget=10000000,
         wram={0xFF97: b"\xC2", 0xC2BA: b"\x3C", 0xCAC2: b"\x09",
               0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PlayDeckShuffleAnimation

# >>> factory OppAction_6b30
CONTRACT["OppAction_6b30"] = {"compare": ("a",), "preserve": ()}
CASES["OppAction_6b30"] = [
    {"keys": 0, "instruction_budget": 3000000, "cycle_budget": 10000000,
     "wram": {hWhoseTurn: b"\xC3", hTemp_ffa0: b"\xC2", 0xC2BA: b"\x3C", 0xCAC2: b"\x09",
              0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
     "read": {hWhoseTurn: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=3000000, cycle_budget=10000000,
         wram={hWhoseTurn: b"\xC3", hTemp_ffa0: b"\xC2", 0xC2BA: b"\x3C", 0xCAC2: b"\x09",
               0xFF90: b"\x02", 0xCE47: b"\x00", 0xFFA9: b"\x00", 0xC600: b"\x00"},
         read={hWhoseTurn: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory OppAction_6b30

# >>> factory PrintPlayAreaCardInformation
CONTRACT["PrintPlayAreaCardInformation"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintPlayAreaCardInformation"] = [
    {"keys": 0, "instruction_budget": 4000000, "cycle_budget": 16000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x04",
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=4000000, cycle_budget=16000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x04",
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintPlayAreaCardInformation

# >>> factory PrintPlayAreaCardInformationAndLocation
CONTRACT["PrintPlayAreaCardInformationAndLocation"] = {"compare": (), "preserve": ()}
CASES["PrintPlayAreaCardInformationAndLocation"] = [
    {"keys": 0, "instruction_budget": 4000000, "cycle_budget": 16000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x04",
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "vread": {0: {0x9800 + 4 * 32 + 1: 1, 0x9800 + 5 * 32 + 1: 1, 0x9800 + 6 * 32 + 1: 1}},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=4000000, cycle_budget=16000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x04",
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
         vread={0: {0x9800 + 4 * 32 + 1: 1, 0x9800 + 5 * 32 + 1: 1, 0x9800 + 6 * 32 + 1: 1}},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PrintPlayAreaCardInformationAndLocation

# >>> factory DisplayUsePokemonPowerScreen
CONTRACT["DisplayUsePokemonPowerScreen"] = {"compare": (), "preserve": ()}
CASES["DisplayUsePokemonPowerScreen"] = [
    {"keys": 0, "instruction_budget": 5000000, "cycle_budget": 20000000,
     "hram": {hTempPlayAreaLocation_ff9d: b"\x00"},
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00",
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
              wLoadedCard1Atk1Name: b"\x00\x00",
              wLoadedCard1Atk1Description: b"\x00\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=5000000, cycle_budget=20000000,
         hram={hTempPlayAreaLocation_ff9d: b"\x00"},
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wCurPlayAreaSlot: b"\x00", wCurPlayAreaY: b"\x00",
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
               wLoadedCard1Atk1Name: b"\x00\x00",
               wLoadedCard1Atk1Description: b"\x00\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory DisplayUsePokemonPowerScreen

# >>> factory InitAndPrintPlayAreaCardInformationAndLocation
CONTRACT["InitAndPrintPlayAreaCardInformationAndLocation"] = {"compare": (), "preserve": ()}
CASES["InitAndPrintPlayAreaCardInformationAndLocation"] = [
    {"keys": 0, "instruction_budget": 5000000, "cycle_budget": 20000000,
     "hram": {hTempPlayAreaLocation_ff9d: b"\x00"},
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)),
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "read": {wCurPlayAreaSlot: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0, instruction_budget=5000000, cycle_budget=20000000,
         hram={hTempPlayAreaLocation_ff9d: b"\x00"},
         wram={hWhoseTurn: bytes((PLAYER_TURN,)),
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
         read={wCurPlayAreaSlot: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory InitAndPrintPlayAreaCardInformationAndLocation

# >>> factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox
CONTRACT["InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox"] = {"compare": (), "preserve": ()}
CASES["InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox"] = [
    {"keys": 0x01, "instruction_budget": 5000000, "cycle_budget": 20000000,
     "hram": {hTempPlayAreaLocation_ff9d: b"\x00"},
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)),
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
     "read": {0xCD11: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0x01, instruction_budget=5000000, cycle_budget=20000000,
         hram={hTempPlayAreaLocation_ff9d: b"\x00"},
         wram={hWhoseTurn: bytes((PLAYER_TURN,)),
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00"},
         read={0xCD11: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox

# >>> factory PrintPlayAreaCardList
CONTRACT["PrintPlayAreaCardList"] = {"compare": (), "preserve": ()}
CASES["PrintPlayAreaCardList"] = [
    {"instruction_budget": 4000000, "cycle_budget": 16000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
              wPlayerArenaCard: b"\xFF", wExcludeArenaPokemon: b"\x00"},
     "read": {wNumPlayAreaItems: 1, wDuelTempList: 1}},
    dict(POISON, instruction_budget=4000000, cycle_budget=16000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
               wPlayerArenaCard: b"\xFF", wExcludeArenaPokemon: b"\x00"},
         read={wNumPlayAreaItems: 1, wDuelTempList: 1}),
    {"instruction_budget": 4000000, "cycle_budget": 16000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard + 0xEF - 0xBB: b"\x01",
              wPlayerArenaCard: b"\xFF", wExcludeArenaPokemon: b"\x01"},
     "read": {wNumPlayAreaItems: 1, wDuelTempList: 1}},
]
# <<< factory PrintPlayAreaCardList

# >>> factory OppAction_UsePokemonPower
CONTRACT["OppAction_UsePokemonPower"] = {"compare": (), "preserve": ()}
CASES["OppAction_UsePokemonPower"] = [
    {"keys": 0x01, "instruction_budget": 5000000, "cycle_budget": 20000000,
     "hram": {hTempCardIndex_ff9f: b"\x00", hTemp_ffa0: b"\x00"},
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)),
              wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
              wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
              wDuelType: b"\x00"},
     "read": {wSkipDuelistIsThinkingDelay: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=0x01, instruction_budget=5000000, cycle_budget=20000000,
         hram={hTempCardIndex_ff9f: b"\x00", hTemp_ffa0: b"\x00"},
         wram={hWhoseTurn: bytes((PLAYER_TURN,)),
               wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00",
               wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00",
               wDuelType: b"\x00"},
         read={wSkipDuelistIsThinkingDelay: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory OppAction_UsePokemonPower

# >>> factory Func_616e
CONTRACT["Func_616e"] = {"compare": (), "preserve": ()}
CASES["Func_616e"] = [
    {"a": 0x00, "instruction_budget": 6000000, "cycle_budget": 20000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: b"\xFF",
              wPlayerArenaCard + 0xEF - 0xBB: b"\x01", wExcludeArenaPokemon: b"\x01"},
     "read": {wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}},
    dict(POISON, a=0xAA, instruction_budget=6000000, cycle_budget=20000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: b"\xFF",
               wPlayerArenaCard + 0xEF - 0xBB: b"\x01", 0xC265: b"\xFF", wExcludeArenaPokemon: b"\x01"},
         read={wCurPlayAreaSlot: 1, wCurPlayAreaY: 1}),
]
# <<< factory Func_616e

# >>> factory PrintPlayAreaCardList_EnableLCD
CONTRACT["PrintPlayAreaCardList_EnableLCD"] = {"compare": ("a",), "preserve": ()}
CASES["PrintPlayAreaCardList_EnableLCD"] = [
    {"instruction_budget": 6000000, "cycle_budget": 20000000,
     "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: b"\xFF",
              wPlayerArenaCard + 0xEF - 0xBB: b"\x01", wExcludeArenaPokemon: b"\x00"}},
    dict(POISON, instruction_budget=6000000, cycle_budget=20000000,
         wram={hWhoseTurn: bytes((PLAYER_TURN,)), wPlayerArenaCard: b"\xFF",
               wPlayerArenaCard + 0xEF - 0xBB: b"\x01", wExcludeArenaPokemon: b"\x00"}),
]
# <<< factory PrintPlayAreaCardList_EnableLCD

# >>> factory FlushAllPalettesOrSendPal23Packet
CONTRACT["FlushAllPalettesOrSendPal23Packet"] = {"compare": (), "preserve": ()}
CASES["FlushAllPalettesOrSendPal23Packet"] = [
    {"wram": {0xCAB4: b"\x00", 0xCAE0: b"\xAA" * 16}, "read": {0xCAE0: 16}},
    {"wram": {0xCAB4: b"\x02", 0xCAE0: b"\x55" * 16}, "read": {0xCAE0: 16}},
    {"wram": {0xCAB4: b"\x01", 0xCAE0: b"\x00" * 16}, "read": {0xCAE0: 16}},
    dict(POISON, wram={0xCAB4: b"\x01", 0xCAE0: b"\x00" * 16}, read={0xCAE0: 16}),
]
# <<< factory FlushAllPalettesOrSendPal23Packet

# >>> factory CheckIfCardCanBePlayed
CONTRACT["CheckIfCardCanBePlayed"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfCardCanBePlayed"] = [
    {"a": 0x00, "wram": {0xCC0B: b"\x01", 0xCC24: b"\x08", 0xCC2D: b"\x00"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xCC0B: b"\x01", 0xCC24: b"\x08", 0xCC2D: b"\x00"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory CheckIfCardCanBePlayed

# >>> factory OppAction_6b15
CONTRACT["OppAction_6b15"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e")}
CASES["OppAction_6b15"] = [
    {"wram": {wSkipDuelistIsThinkingDelay: b"\x00"}, "expect_wram": {wSkipDuelistIsThinkingDelay: b"\x01"}, "sram": {0: {}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={wSkipDuelistIsThinkingDelay: b"\x00"}, expect_wram={wSkipDuelistIsThinkingDelay: b"\x01"}, sram={0: {}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory OppAction_6b15

# >>> factory OppAction_ExecutePokemonPowerEffect
CONTRACT["OppAction_ExecutePokemonPowerEffect"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e")}
CASES["OppAction_ExecutePokemonPowerEffect"] = [
    {"wram": {wSkipDuelistIsThinkingDelay: b"\x00"}, "expect_wram": {wSkipDuelistIsThinkingDelay: b"\x01"}, "sram": {0: {}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={wSkipDuelistIsThinkingDelay: b"\x00"}, expect_wram={wSkipDuelistIsThinkingDelay: b"\x01"}, sram={0: {}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory OppAction_ExecutePokemonPowerEffect

# >>> factory LoadSelectedCardGfx
CONTRACT["LoadSelectedCardGfx"] = {"compare": (), "preserve": ()}
CASES["LoadSelectedCardGfx"] = [
    {"vread": {0: {0x8A00: 0x300}}},
    dict(POISON, vread={0: {0x8A00: 0x300}}),
]
# <<< factory LoadSelectedCardGfx

# >>> factory AIProcessHandTrainerCards
CONTRACT["AIProcessHandTrainerCards"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIProcessHandTrainerCards"] = [
    {"a": 0x00},
    dict(POISON, a=0xAA),
]
# <<< factory AIProcessHandTrainerCards

# >>> factory CardListFunction
CONTRACT["CardListFunction"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CardListFunction"] = [
    {"wram": {hKeysPressed: b"\x00", hKeysReleased: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0xA0}},
    {"wram": {hKeysPressed: b"\x02", hKeysReleased: b"\x00", hCurMenuItem: b"\x00"}, "expect": {hCurMenuItem: b"\xFF"}, "expect_regs": {"a": 0xFF, "f": 0x10}},
    {"wram": {hKeysPressed: b"\x01", hKeysReleased: b"\x00"}, "expect_regs": {"a": 0x01, "f": 0x10}},
    {"wram": {hKeysPressed: b"\x04", hKeysReleased: b"\x00"}, "expect_regs": {"a": 0x04, "f": 0x10}},
    {"wram": {hKeysPressed: b"\x08", hKeysReleased: b"\x00"}, "expect_regs": {"a": 0x08, "f": 0x10}},
    dict(POISON, wram={hKeysPressed: b"\x02", hKeysReleased: b"\x00", hCurMenuItem: b"\x55"}, expect={hCurMenuItem: b"\xFF"}, expect_regs={"a": 0xFF, "f": 0x10}),
]
# <<< factory CardListFunction

# >>> factory CheckIfSelectedAttackIsUnusable
CONTRACT["CheckIfSelectedAttackIsUnusable"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["CheckIfSelectedAttackIsUnusable"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCCC6: b"\x00", 0xCC23: b"\x00"},
     "sram": {0: {}}, "instruction_budget": 4000000, "cycle_budget": 20000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x00", 0xC400: b"\x08", 0xCCC6: b"\x00", 0xCC23: b"\x00"},
         sram={0: {}}, instruction_budget=4000000, cycle_budget=20000000),
]
# <<< factory CheckIfSelectedAttackIsUnusable

# >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack
CONTRACT["CheckForBenchIDAtHalfHPAndCanUseSecondAttack"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["CheckForBenchIDAtHalfHPAndCanUseSecondAttack"] = [
    {"a": 0x12, "wram": {hWhoseTurn: b"\xC2", wArenaCard: b"\xFF", hTempPlayAreaLocation_ff9d: b"\x03", wSelectedAttack: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x01, "d": 0x03, "e": 0x00, "hl": 0xC2BC}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wArenaCard: b"\xFF", hTempPlayAreaLocation_ff9d: b"\x5A", wSelectedAttack: b"\x01"}, expect_regs={"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x01, "d": 0x5A, "e": 0x01, "hl": 0xC2BC}),
]
# <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack

# >>> factory CountNumberOfSetUpBenchPokemon
CONTRACT["CountNumberOfSetUpBenchPokemon"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["CountNumberOfSetUpBenchPokemon"] = [
    {"wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x03", wSelectedAttack: b"\x00", 0xC2BC: b"\xFF"}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x01, "d": 0x03, "e": 0x00, "hl": 0xC2BC}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x5A", wSelectedAttack: b"\x01", 0xC2BC: b"\xFF"}, expect_regs={"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x01, "d": 0x5A, "e": 0x01, "hl": 0xC2BC}),
]
# <<< factory CountNumberOfSetUpBenchPokemon

# >>> factory HandleLegendaryArticunoEnergyScoring
CONTRACT["HandleLegendaryArticunoEnergyScoring"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["HandleLegendaryArticunoEnergyScoring"] = [
    {"wram": {wOpponentDeckID: b"\x0E", hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, "expect": {ARTICUNO_SCORE: b"\x05"}},
    dict(POISON, wram={wOpponentDeckID: b"\x0E", hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, expect={ARTICUNO_SCORE: b"\x05"}),
    {"wram": {wOpponentDeckID: b"\x00", hWhoseTurn: b"\xC2", 0xC3EC: b"\x07", 0xC2BB: b"\xFF", 0xC2BC: b"\x00\xFF", 0xC400: b"\x5E", 0xC2C9: b"\x00", ARTICUNO_SCORE: b"\x00"}, "expect": {ARTICUNO_SCORE: b"\x00"}},
]
# <<< factory HandleLegendaryArticunoEnergyScoring

# >>> factory CheckIfArenaCardIsFullyPowered
CONTRACT["CheckIfArenaCardIsFullyPowered"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfArenaCardIsFullyPowered"] = [
    {"hram": {0xFF97: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00"}, "wram": {0xC2BB: b"\xFF", wSelectedAttack: b"\x00"}, "sram": {0: {}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hram={0xFF97: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00"}, wram={0xC2BB: b"\x0A", 0xC2C8: b"\x00", wSelectedAttack: b"\x00"}, sram={0: {}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory CheckIfArenaCardIsFullyPowered

# >>> factory SendCardAttrBlkPacket
CONTRACT["SendCardAttrBlkPacket"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["SendCardAttrBlkPacket"] = [
    {"instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory SendCardAttrBlkPacket

# >>> factory ApplyBGP6OrSGB3ToCardImage
CONTRACT["ApplyBGP6OrSGB3ToCardImage"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ApplyBGP6OrSGB3ToCardImage"] = [
    {"wram": {0xCAB4: b"\x00"}},
    dict(POISON, wram={0xCAB4: b"\x00"}),
]
# <<< factory ApplyBGP6OrSGB3ToCardImage

# >>> factory DrawLargePictureOfCard
CONTRACT["DrawLargePictureOfCard"] = {"compare": (), "preserve": ()}
CASES["DrawLargePictureOfCard"] = [
    {"wram": {wDuelDisplayedScreen: b"\x00", wLoadedCard1Type: b"\x00"}, "read": {wDuelDisplayedScreen: 1}, "vread": {0: {0x9800: 1}}},
    dict(POISON, wram={wDuelDisplayedScreen: b"\x00", wLoadedCard1Type: b"\x00"}, read={wDuelDisplayedScreen: 1}, vread={0: {0x9800: 1}}),
    {"wram": {wDuelDisplayedScreen: b"\x00", wLoadedCard1Type: b"\x01"}, "read": {wDuelDisplayedScreen: 1}, "vread": {0: {0x9800: 1}}},
    {"wram": {wDuelDisplayedScreen: b"\x00", wLoadedCard1Type: b"\x08"}, "read": {wDuelDisplayedScreen: 1}, "vread": {0: {0x9800: 1}}},
]
# <<< factory DrawLargePictureOfCard

# >>> factory DrawCardPageSurroundingBox
CONTRACT["DrawCardPageSurroundingBox"] = {"compare": (), "preserve": ()}
CASES["DrawCardPageSurroundingBox"] = [
    {"wram": {0xCCF3: b"\x00"}, "expect": {0xCCF3: b"\x00"}},
    dict(POISON, wram={0xCCF3: b"\x00"}, expect={0xCCF3: b"\x00"}),
]
# <<< factory DrawCardPageSurroundingBox

# >>> factory PrintPokemonCardPageGenericInformation
CONTRACT["PrintPokemonCardPageGenericInformation"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintPokemonCardPageGenericInformation"] = [
    {"wram": {0xCBD1: b"\x00", 0xCC24: b"\x00", 0xCC27: b"\x00\x00", 0xCC29: b"\xff", 0xCC2A: b"\x01"},
     "setup": SETUP_TEXT, "rom_bank": 1,
     "vram": {0: {0x9832: b"\xA5"}},
     "expect_vram": {0: {0x9832: b"\x01"}},
     "instruction_budget": 1000000, "cycle_budget": 4000000},
    dict(POISON, wram={0xCBD1: b"\x00", 0xCC24: b"\x00", 0xCC27: b"\x00\x00", 0xCC29: b"\xff", 0xCC2A: b"\x01"},
         setup=SETUP_TEXT, rom_bank=1,
         vram={0: {0x9832: b"\xEE"}},
         expect_vram={0: {0x9832: b"\x01"}},
         instruction_budget=1000000, cycle_budget=4000000),
]
# <<< factory PrintPokemonCardPageGenericInformation

# >>> factory DrawDuelHUD
CONTRACT["DrawDuelHUD"] = {"compare": (), "preserve": ()}
CASES["DrawDuelHUD"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "wram": {0xC2BB: b"\xFF", 0xC2EC: b"\x00", 0xC2EF: b"\x00", hWhoseTurn: b"\xC2"}, "read": {wHUDEnergyAndHPBarsX: 1, wHUDEnergyAndHPBarsY: 1}},
    dict(POISON, wram={0xC2BB: b"\xFF", 0xC2EC: b"\x00", 0xC2EF: b"\x00", hWhoseTurn: b"\xC2"}, read={wHUDEnergyAndHPBarsX: 1, wHUDEnergyAndHPBarsY: 1}),
]
# <<< factory DrawDuelHUD

# >>> factory DrawDuelHUDs
CONTRACT["DrawDuelHUDs"] = {"compare": (), "preserve": ()}
CASES["DrawDuelHUDs"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\xFF", 0xC3BB: b"\xFF", 0xC2F1: b"\x00", 0xC2F0: b"\x00", 0xC3F1: b"\x00", 0xC3F0: b"\x00", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC3EC: b"\x00", 0xC3EF: b"\x00"}, "vread": {0: {HUD_TILE: 1}}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2BB: b"\xFF", 0xC3BB: b"\xFF", 0xC2F1: b"\x00", 0xC2F0: b"\x00", 0xC3F1: b"\x00", 0xC3F0: b"\x00", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC3EC: b"\x00", 0xC3EF: b"\x00"}, vread={0: {HUD_TILE: 1}}),
]
# <<< factory DrawDuelHUDs

# >>> factory DrawCardListScreenLayout
CONTRACT["DrawCardListScreenLayout"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DrawCardListScreenLayout"] = [
    {"wram": {0xC510: b"\xff", 0xC51A: b"\xff"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"wram": {0xC510: b"\x00\xff", 0xC51A: b"\xff"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xC510: b"\xff", 0xC51A: b"\xff"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DrawCardListScreenLayout

# >>> factory ApplyBGP7OrSGB2ToCardImage
CONTRACT["ApplyBGP7OrSGB2ToCardImage"] = {"compare": ("a",), "preserve": ()}
CASES["ApplyBGP7OrSGB2ToCardImage"] = [
    {"wram": {0xCAB4: b"\x00"}},
    {"wram": {0xCAB4: b"\x01"}, "read": {0xCAE3: 1}},
    {"wram": {0xCAB4: b"\x02"}},
    dict(POISON, wram={0xCAB4: b"\x00"}),
]
# <<< factory ApplyBGP7OrSGB2ToCardImage

# >>> factory DisplayPracticeDuelPlayerHandScreen
CONTRACT["DisplayPracticeDuelPlayerHandScreen"] = {"compare": (), "preserve": ()}
CASES["DisplayPracticeDuelPlayerHandScreen"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xCABB: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xC510: 1, 0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xCABB: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xC510: 1, 0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory DisplayPracticeDuelPlayerHandScreen

# >>> factory DrawDuelMainScene
CONTRACT["DrawDuelMainScene"] = {"compare": (), "preserve": ()}
CASES["DrawDuelMainScene"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelistType: b"\x00", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"},
     "read": {hWhoseTurn: 1, wDuelDisplayedScreen: 1}},
    {"wram": {hWhoseTurn: b"\xC3", wPlayerDuelistType: b"\x00", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"},
     "read": {hWhoseTurn: 1, wDuelDisplayedScreen: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC3", wPlayerDuelistType: b"\x00", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"},
         read={hWhoseTurn: 1, wDuelDisplayedScreen: 1}),
]
# <<< factory DrawDuelMainScene

# >>> factory InitAndDrawCardListScreenLayout
CONTRACT["InitAndDrawCardListScreenLayout"] = {"compare": ("a", "f"), "preserve": ()}
CASES["InitAndDrawCardListScreenLayout"] = [
    {"wram": {0xCBCF: b"\xFF", 0xCBDF: b"\xFF", 0xCBD8: b"\xFF\xFF", 0xCBDE: b"\xFF", 0xCBD6: b"\xFF", 0xCBDA: b"\xFF\xFF", 0xCBDC: b"\xFF\xFF", 0xC510: b"\xFF", 0xC51A: b"\xFF"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xCBCF: b"\xFF", 0xCBDF: b"\xFF", 0xCBD8: b"\xFF\xFF", 0xCBDE: b"\xFF", 0xCBD6: b"\xFF", 0xCBDA: b"\xFF\xFF", 0xCBDC: b"\xFF\xFF", 0xC510: b"\xFF", 0xC51A: b"\xFF"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory InitAndDrawCardListScreenLayout

# >>> factory RedrawTurnDuelistsDuelHUD
CONTRACT["RedrawTurnDuelistsDuelHUD"] = {"compare": (), "preserve": ()}
CASES["RedrawTurnDuelistsDuelHUD"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "wram": HUD_SEED, "read": {wWhoseTurn: 0xC2}, "vread": {0: {HUD_TILE: 1}}, **HUD_BUDGET},
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "wram": {**HUD_SEED, hWhoseTurn: b"\xC2", wWhoseTurn: b"\xC3"}, "read": {wWhoseTurn: 0xC3}, "vread": {0: {HUD_TILE: 1}}, **HUD_BUDGET},
    dict(POISON, wram={**HUD_SEED, hWhoseTurn: b"\xC2", wWhoseTurn: b"\xC3"}, read={wWhoseTurn: 0xC3}, vread={0: {HUD_TILE: 1}}, **HUD_BUDGET),
]
# <<< factory RedrawTurnDuelistsDuelHUD

# >>> factory OppAction_DrawDuelMainScene
CONTRACT["OppAction_DrawDuelMainScene"] = {"compare": (), "preserve": ()}
CASES["OppAction_DrawDuelMainScene"] = [
    {"wram": {hWhoseTurn: b"\xC3", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"},
     "read": {hWhoseTurn: 1, wDuelDisplayedScreen: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC3", wOpponentDuelistType: b"\x01", wDuelDisplayedScreen: b"\x01"},
         read={hWhoseTurn: 1, wDuelDisplayedScreen: 1}),
]
# <<< factory OppAction_DrawDuelMainScene

# >>> factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu
CONTRACT["InitAndDrawCardListScreenLayout_WithSelectCheckMenu"] = {"compare": ("a", "f"), "preserve": ()}
CASES["InitAndDrawCardListScreenLayout_WithSelectCheckMenu"] = [
    {"wram": {0xCBCF: b"\xFF", 0xCBDF: b"\xFF", 0xCBD8: b"\xFF\xFF", 0xCBDE: b"\xFF", 0xCBD6: b"\xFF", 0xCBDA: b"\xFF\xFF", 0xCBDC: b"\xFF\xFF", 0xC510: b"\xFF", 0xC51A: b"\xFF"}, "read": {0xCBDE: 1}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xCBCF: b"\xFF", 0xCBDF: b"\xFF", 0xCBD8: b"\xFF\xFF", 0xCBDE: b"\xFF", 0xCBD6: b"\xFF", 0xCBDA: b"\xFF\xFF", 0xCBDC: b"\xFF\xFF", 0xC510: b"\xFF", 0xC51A: b"\xFF"}, read={0xCBDE: 1}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu

# >>> factory DisplayCardListDetails
CONTRACT["DisplayCardListDetails"] = {"compare": ("a", "f"), "preserve": ()}
CASES["DisplayCardListDetails"] = [
    {"wram": {wDuelTempList: b"\xFF"}, "read": {wDuelTempList: 1}, "expect_regs": {"a": 0xFF, "f": 0xC0}},
    dict(POISON, wram={wDuelTempList: b"\xFF"}, read={wDuelTempList: 1}, expect_regs={"a": 0xFF, "f": 0xC0}),
]
# <<< factory DisplayCardListDetails

# >>> factory OppAction_FinishTurnWithoutAttacking
CONTRACT["OppAction_FinishTurnWithoutAttacking"] = {"compare": (), "preserve": ()}
CASES["OppAction_FinishTurnWithoutAttacking"] = [
    {"wram": {wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wOpponentTurnEnded: b"\x00"}, "keys": 0x01, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "expect": {wOpponentTurnEnded: b"\x01"}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={wDuelDisplayedScreen: b"\x01", wLCDC: b"\x00", wOpponentTurnEnded: b"\x00"}, keys=0x01, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], expect={wOpponentTurnEnded: b"\x01"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory OppAction_FinishTurnWithoutAttacking

# >>> factory RedrawTurnDuelistsMainSceneOrDuelHUD
CONTRACT["RedrawTurnDuelistsMainSceneOrDuelHUD"] = {"compare": (), "preserve": ()}
CASES["RedrawTurnDuelistsMainSceneOrDuelHUD"] = [
    {"wram": {**HUD_SEED, wDuelDisplayedScreen: b"\x01"}, "read": {wDuelDisplayedScreen: 1}, "vread": {0: {HUD_TILE: 1}}, **HUD_BUDGET},
    {"wram": {**HUD_SEED, wDuelDisplayedScreen: b"\x00", hWhoseTurn: b"\xC2", wWhoseTurn: b"\xC2"}, "read": {wDuelDisplayedScreen: 1, wWhoseTurn: 1}, **HUD_BUDGET},
    {"wram": {**HUD_SEED, wDuelDisplayedScreen: b"\x00", hWhoseTurn: b"\xC2", wWhoseTurn: b"\xC3"}, "read": {wDuelDisplayedScreen: 1, wWhoseTurn: 1}, **HUD_BUDGET},
    dict(POISON, wram={**HUD_SEED, wDuelDisplayedScreen: b"\x00", hWhoseTurn: b"\xC2", wWhoseTurn: b"\xC3"}, read={wDuelDisplayedScreen: 1, wWhoseTurn: 1}, **HUD_BUDGET),
]
# <<< factory RedrawTurnDuelistsMainSceneOrDuelHUD

# >>> factory DisplayNoBasicPokemonInHandScreen
CONTRACT["DisplayNoBasicPokemonInHandScreen"] = {"compare": (), "preserve": ()}
CASES["DisplayNoBasicPokemonInHandScreen"] = [
    {"wram": {hWhoseTurn: b"\xC2", 0xFF80: b"\x01", 0xC2EE: b"\x00", 0xCABB: b"\x00", wDuelTempList: b"\xFF"}, "read": {wListItemXPosition: 1, wNumListItems: 1}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": 0x01, "instruction_budget": 40000000, "cycle_budget": 160000000},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xFF80: b"\x01", 0xC2EE: b"\x00", 0xCABB: b"\x00", wDuelTempList: b"\xFF"}, read={wListItemXPosition: 1, wNumListItems: 1}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=0x01, instruction_budget=40000000, cycle_budget=160000000),
]
# <<< factory DisplayNoBasicPokemonInHandScreen

# >>> factory PrintAndLoadAttacksToDuelTempList
CONTRACT["PrintAndLoadAttacksToDuelTempList"] = {"compare": ("a",), "preserve": ()}
CASES["PrintAndLoadAttacksToDuelTempList"] = [
    {"setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "wram": {hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x07"}, "read": {0xC510: 4, 0xCBC7: 1}, "instruction_budget": 200000, "cycle_budget": 2000000},
    dict(POISON, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], wram={hWhoseTurn: b"\xC2", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x07"}, read={0xC510: 4, 0xCBC7: 1}, instruction_budget=200000, cycle_budget=2000000),
]
# <<< factory PrintAndLoadAttacksToDuelTempList

# >>> factory DisplayPokemonAttackCardPage
CONTRACT["DisplayPokemonAttackCardPage"] = {"compare": (), "preserve": ()}
CASES["DisplayPokemonAttackCardPage"] = [
    {"hl": 0x0114, "d": 0x01, "e": 0x14, "wram": {wLoadedCard1AttackDescriptions: b"\x00\x00", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xCC27: 1}, "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0x0114, d=0x01, e=0x14, wram={wLoadedCard1AttackDescriptions: b"\x00\x00", 0xFF80: b"\x01", 0xCABB: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xCC27: 1}, vread={0: {0x9800: 0x400}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DisplayPokemonAttackCardPage

# >>> factory DisplayCardPage_PokemonAttack2Page2
CONTRACT["DisplayCardPage_PokemonAttack2Page2"] = {"compare": (), "preserve": ()}
CASES["DisplayCardPage_PokemonAttack2Page2"] = [
    {"b": 0x01, "c": 0x02, "d": 0x03, "wram": {0xCEA0: b"\x00\x00", 0xCC47: b"\x00\x00", 0xCC4B: b"\x00\x00", 0xCC4D: b"\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xCC27: 1}, "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, b=0xBB, c=0xCC, d=0xDD, wram={0xCEA0: b"\x00\x00", 0xCC47: b"\x00\x00", 0xCC4B: b"\x00\x00", 0xCC4D: b"\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xCC27: 1}, vread={0: {0x9800: 0x400}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DisplayCardPage_PokemonAttack2Page2

# >>> factory DisplayCardPage_PokemonAttack1Page1
CONTRACT["DisplayCardPage_PokemonAttack1Page1"] = {"compare": (), "preserve": ()}
CASES["DisplayCardPage_PokemonAttack1Page1"] = [
    {"wram": {0xCC34: b"\x14\x01", 0xCC36: b"\x14\x01\x14\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCC34: b"\x14\x01", 0xCC36: b"\x11\x01\x14\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory DisplayCardPage_PokemonAttack1Page1

# >>> factory DisplayCardPage_PokemonAttack1Page2
CONTRACT["DisplayCardPage_PokemonAttack1Page2"] = {"compare": (), "preserve": ()}
CASES["DisplayCardPage_PokemonAttack1Page2"] = [
    {"wram": {0xCC34: b"\x14\x01", 0xCC36: b"\x14\x01\x14\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCC34: b"\x14\x01", 0xCC36: b"\x11\x01\x14\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory DisplayCardPage_PokemonAttack1Page2

# >>> factory DisplayCardPage_PokemonAttack2Page1
CONTRACT["DisplayCardPage_PokemonAttack2Page1"] = {"compare": (), "preserve": ()}
CASES["DisplayCardPage_PokemonAttack2Page1"] = [
    {"b": 0x01, "c": 0x02, "d": 0x03, "wram": {0xCC47: b"\x00\x00", 0xCC49: b"\x00\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, b=0xBB, c=0xCC, d=0xDD, wram={0xCC47: b"\x00\x00", 0xCC49: b"\x00\x01", 0xFF80: b"\x01", 0xCABB: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], vread={0: {0x9800: 0x400}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DisplayCardPage_PokemonAttack2Page1

# >>> factory DisplayAttackPage_Attack1Page1
CONTRACT["DisplayAttackPage_Attack1Page1"] = {"compare": (), "preserve": ()}
CASES["DisplayAttackPage_Attack1Page1"] = [
    {"wram": {0xCC34: b"\x14\x01", 0xCC36: b"\x14\x01\x14\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCC34: b"\x14\x01", 0xCC36: b"\x11\x01\x14\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory DisplayAttackPage_Attack1Page1

# >>> factory DisplayAttackPage_Attack2Page1
CONTRACT["DisplayAttackPage_Attack2Page1"] = {"compare": (), "preserve": ()}
CASES["DisplayAttackPage_Attack2Page1"] = [
    {"b": 0x01, "c": 0x02, "d": 0x03, "wram": {0xCC47: b"\x00\x00", 0xCC49: b"\x00\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCC47: b"\x00\x00", 0xCC49: b"\x00\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory DisplayAttackPage_Attack2Page1

# >>> factory DisplayAttackPage_Attack2Page2
CONTRACT["DisplayAttackPage_Attack2Page2"] = {"compare": (), "preserve": ()}
CASES["DisplayAttackPage_Attack2Page2"] = [
    {"b": 0x01, "c": 0x02, "d": 0x03, "wram": {0xCC47: b"\x00\x00", 0xCC49: b"\x00\x00\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCC47: b"\x00\x00", 0xCC49: b"\x00\x00\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory DisplayAttackPage_Attack2Page2

# >>> factory DisplayAttackPage_Attack1Page2
CONTRACT["DisplayAttackPage_Attack1Page2"] = {"compare": (), "preserve": ()}
CASES["DisplayAttackPage_Attack1Page2"] = [
    {"b": 0x01, "c": 0x02, "d": 0x03, "wram": {0xCC34: b"\x00\x00", 0xCC36: b"\x00\x00\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCC34: b"\x00\x00", 0xCC36: b"\x00\x00\x01\x01", 0xFF80: b"\x01", 0xCABB: b"\x00", 0xCC04: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "vread": {0: {0x9800: 0x400}}, "read": {0xCC04: 0x01}, "instruction_budget": 2000000, "cycle_budget": 8000000}
]
# <<< factory DisplayAttackPage_Attack1Page2

# >>> factory DisplayEnergyDiscardMenu
CONTRACT["DisplayEnergyDiscardMenu"] = {"compare": (), "preserve": ()}
CASES["DisplayEnergyDiscardMenu"] = [
    {"wram": {wDuelTempList: b"\xFF", 0xCABB: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {wDuelTempList: 1, 0xCD97: 1, 0xCD05: 2, 0xCD0A: 1},
     "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, wram={wDuelTempList: b"\xFF", 0xCABB: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={wDuelTempList: 1, 0xCD97: 1, 0xCD05: 2, 0xCD0A: 1},
         vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory DisplayEnergyDiscardMenu

# >>> factory DisplayEnergyDiscardScreen
CONTRACT["DisplayEnergyDiscardScreen"] = {"compare": (), "preserve": ()}
CASES["DisplayEnergyDiscardScreen"] = [
    {"a": 0x00, "keys": 0, "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08", wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00", wDuelTempList: b"\xFF", 0xCABB: b"\x00"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {wDuelTempList: 1, 0xCD97: 1, 0xCD05: 2, 0xCD0A: 1, 0xCBE0: 1, wCurPlayAreaSlot: 1, wCurPlayAreaY: 1, 0xCBFB: 1, 0xCBFA: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, a=0x00, keys=0, wram={hWhoseTurn: bytes((PLAYER_TURN,)), wConsole: b"\x00", wPlayerArenaCard: b"\x00", wPlayerDeck: b"\x08", wPlayerArenaCard + DUELVARS_ARENA_CARD_HP_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_STAGE_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_STATUS_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER_OFF: b"\x00", wPlayerArenaCard + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER_OFF: b"\x00", wDuelTempList: b"\xFF", 0xCABB: b"\x00"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={wDuelTempList: 1, 0xCD97: 1, 0xCD05: 2, 0xCD0A: 1, 0xCBE0: 1, wCurPlayAreaSlot: 1, wCurPlayAreaY: 1, 0xCBFB: 1, 0xCBFA: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory DisplayEnergyDiscardScreen

# >>> factory OpenAttackPage
CONTRACT["OpenAttackPage"] = {"compare": (), "preserve": ()}
CASES["OpenAttackPage"] = [
    {"keys": 0x01, "wram": {wDuelTempList: b"\xFF", 0xCABB: b"\x00", 0xFF97: b"\xC2"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {0xCBC7: 1, 0xCBC9: 1, 0xCBCF: 1, 0xCC04: 1, wDuelTempList: 1},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=0x01, wram={wDuelTempList: b"\xFF", 0xCABB: b"\x00", 0xFF97: b"\xC2"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={0xCBC7: 1, 0xCBC9: 1, 0xCBCF: 1, 0xCC04: 1, wDuelTempList: 1},
         instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory OpenAttackPage

# >>> factory HandleEnergyDiscardMenuInput
CONTRACT["HandleEnergyDiscardMenuInput"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleEnergyDiscardMenuInput"] = [
    {"keys": 0x02, "wram": {wEnergyDiscardMenuDenominator: b"\x00", wEnergyDiscardMenuNumerator: b"\x07", 0xCABB: b"\x00"}, "vread": {0: {0x9A10: 4}}, "instruction_budget": 10000, "cycle_budget": 40000},
    {"keys": 0x02, "wram": {wEnergyDiscardMenuDenominator: b"\x01", wEnergyDiscardMenuNumerator: b"\x07", 0xCABB: b"\x00"}, "vread": {0: {0x9A10: 4}}, "instruction_budget": 10000, "cycle_budget": 40000},
    dict(POISON, keys=0x02, wram={wEnergyDiscardMenuDenominator: b"\x01", wEnergyDiscardMenuNumerator: b"\x07", 0xCABB: b"\x00"}, vread={0: {0x9A10: 4}}, instruction_budget=10000, cycle_budget=40000),
]
# <<< factory HandleEnergyDiscardMenuInput

# >>> factory DisplayRetreatScreen
CONTRACT["DisplayRetreatScreen"] = {"compare": (), "preserve": ()}
CASES["DisplayRetreatScreen"] = [
    {"a": 0x00, "wram": {wEnergyCardsRequiredToRetreat: b"\x00"}, "read": {wEnergyCardsRequiredToRetreat: 1, hTempRetreatCostCards: 1}},
    dict(POISON, wram={wEnergyCardsRequiredToRetreat: b"\x00"}, read={wEnergyCardsRequiredToRetreat: 1, hTempRetreatCostCards: 1}),
]
# <<< factory DisplayRetreatScreen

# >>> factory PrintPracticeDuelInstructions_Fast
CONTRACT["PrintPracticeDuelInstructions_Fast"] = {"compare": (), "preserve": ()}
CASES["PrintPracticeDuelInstructions_Fast"] = [
    {"hl": 0xC500, "keys": 0x01, "wram": {0xC500: b"\x00", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}, "vread": {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0xC500, keys=0x01, wram={0xC500: b"\x00", 0xCABB: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}, vread={0: {0x8000: 0x1000, 0x9000: 0x800, 0x9800: 0x400}, 1: {0x9800: 0x400}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory PrintPracticeDuelInstructions_Fast

# >>> factory PracticeDuel_RepeatInstructions
CONTRACT["PracticeDuel_RepeatInstructions"] = {"compare": ("f",), "preserve": ()}
CASES["PracticeDuel_RepeatInstructions"] = [
    {"keys": [0x00, 0x01], "instruction_budget": 4000000, "cycle_budget": 16000000,
     "wram": {0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"},
               {"fn": "SetupText", "d": 0x20, "e": 0x40}]},
    dict(POISON, keys=[0x00, 0x01], instruction_budget=4000000, cycle_budget=16000000,
         wram={0xCABB: b"\x80", 0xFF40: b"\x80"},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}]),
]
# <<< factory PracticeDuel_RepeatInstructions

# >>> factory _DisplayCardDetailScreen
CONTRACT["_DisplayCardDetailScreen"] = {"compare": ("f",), "preserve": ()}
CASES["_DisplayCardDetailScreen"] = [
    {"hl": 0xC100, "keys": [0x00, 0x01], "wram": {0xCABB: b"\x80", 0xFF40: b"\x80", 0xCC24: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 10000000, "cycle_budget": 40000000},
    dict(POISON, hl=0x1234, keys=[0x00, 0x01], wram={0xCABB: b"\x80", 0xFF40: b"\x80", 0xCC24: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=10000000, cycle_budget=40000000),
]
# <<< factory _DisplayCardDetailScreen

# >>> factory OpenCardPage
CONTRACT["OpenCardPage"] = {"compare": (), "preserve": ()}
CASES["OpenCardPage"] = [
    {"a": 0x02, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": [0x00, 0x01], "wram": {wCardPageExitKeys: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wCardPageType: 1, wCardPageNumber: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x01], wram={wCardPageExitKeys: b"\x01", 0xCABB: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wCardPageType: 1, wCardPageNumber: 1}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory OpenCardPage

# >>> factory DisplayCardDetailScreen
CONTRACT["DisplayCardDetailScreen"] = {"compare": ("f",), "preserve": ()}
CASES["DisplayCardDetailScreen"] = [
    # wLoadedCard1 is the observable: the deck index picks which card is loaded
    # before the detail screen draws it.
    {"a": 0, "hl": 0xC100, "keys": [0x00, 0x01],
     "wram": {DCDS_wLCDC: b"\x80", DCDS_rLCDC: b"\x80", DCDS_wLoadedCard1: b"\x00",
      DCDS_hWhoseTurn: bytes((DCDS_TURN,)), DCDS_wPlayerDeck: b"\x10"},
     "read": {DCDS_wLoadedCard1: 64},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 10000000, "cycle_budget": 40000000},
    dict(POISON, a=3, hl=0xC100, keys=[0x00, 0x01],
         wram={DCDS_wLCDC: b"\x80", DCDS_rLCDC: b"\x80", DCDS_wLoadedCard1: b"\x00",
         DCDS_hWhoseTurn: bytes((DCDS_TURN,)), DCDS_wPlayerDeck + 3: b"\x20"},
         read={DCDS_wLoadedCard1: 64},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=10000000, cycle_budget=40000000),
]
# <<< factory DisplayCardDetailScreen

# >>> factory OpenCardPage_FromHand
CONTRACT["OpenCardPage_FromHand"] = {"compare": (), "preserve": ()}
CASES["OpenCardPage_FromHand"] = [
    {"a": 0x02, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": [0x00, 0x01], "wram": {wCardPageExitKeys: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wCardPageExitKeys: 0x02}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x01], wram={wCardPageExitKeys: b"\x01", 0xCABB: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wCardPageExitKeys: 0x02}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory OpenCardPage_FromHand

# >>> factory OpenCardPage_FromCheckPlayArea
CONTRACT["OpenCardPage_FromCheckPlayArea"] = {"compare": (), "preserve": ()}
CASES["OpenCardPage_FromCheckPlayArea"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": [0x00, 0x01], "wram": {wCardPageExitKeys: b"\x01", 0xCABB: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wCardPageExitKeys: 1, wCardPageType: 1}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, keys=[0x00, 0x01], wram={wCardPageExitKeys: b"\x01", 0xCABB: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wCardPageExitKeys: 1, wCardPageType: 1}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory OpenCardPage_FromCheckPlayArea

# >>> factory DisplayUsedTrainerCardDetailScreen
CONTRACT["DisplayUsedTrainerCardDetailScreen"] = {"compare": ("f",), "preserve": ()}
CASES["DisplayUsedTrainerCardDetailScreen"] = [
    # hTempCardIndex_ff9f picks the deck slot whose card data gets loaded.
    {"keys": [0x00, 0x01],
     "wram": {DUT_wLCDC: b"\x80", DUT_rLCDC: b"\x80", DUT_wLoadedCard1: b"\x00",
      DUT_hWhoseTurn: bytes((DUT_TURN,)), DUT_wPlayerDeck: b"\x10",
      DUT_hTempCardIndex_ff9f: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {DUT_wLoadedCard1: 64},
     "instruction_budget": 10000000, "cycle_budget": 40000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={DUT_wLCDC: b"\x80", DUT_rLCDC: b"\x80", DUT_wLoadedCard1: b"\x00",
         DUT_hWhoseTurn: bytes((DUT_TURN,)), DUT_wPlayerDeck + 3: b"\x20",
         DUT_hTempCardIndex_ff9f: b"\x03"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={DUT_wLoadedCard1: 64},
         instruction_budget=10000000, cycle_budget=40000000),
]
# <<< factory DisplayUsedTrainerCardDetailScreen

# >>> factory DisplayNoBasicPokemonInHandScreenAndText
CONTRACT["DisplayNoBasicPokemonInHandScreenAndText"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["DisplayNoBasicPokemonInHandScreenAndText"] = [
    {"keys": [0x00, 0x01], "wram": {0xCABB: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xCABB: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DisplayNoBasicPokemonInHandScreenAndText

# >>> factory OpenCardPage_FromCheckHandOrDiscardPile
CONTRACT["OpenCardPage_FromCheckHandOrDiscardPile"] = {"compare": (), "preserve": ()}
CASES["OpenCardPage_FromCheckHandOrDiscardPile"] = [
    {"a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": [0x00, 0x01], "wram": {wCardPageExitKeys: b"\x01", 0xCABB: b"\x80", 0xFF40: b"\x84"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wCardPageExitKeys: 1}, "expect": {wCardPageExitKeys: b"\xC2"}, "instruction_budget": 20000000, "cycle_budget": 100000000},
    dict(POISON, keys=[0x00, 0x01], wram={wCardPageExitKeys: b"\x01", 0xCABB: b"\x80", 0xFF40: b"\x84"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wCardPageExitKeys: 1}, expect={wCardPageExitKeys: b"\xC2"}, instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory OpenCardPage_FromCheckHandOrDiscardPile

# >>> factory CardListItemSelectionMenu
CONTRACT["CardListItemSelectionMenu"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CardListItemSelectionMenu"] = [
    {"wram": {0xCBDE: b"\x00"}},
    dict(POISON, wram={0xCBDE: b"\x00"}),
]
# <<< factory CardListItemSelectionMenu

# >>> factory DisplayPlayerDrawCardScreen
CONTRACT["DisplayPlayerDrawCardScreen"] = {"compare": ("f",), "preserve": ()}
CASES["DisplayPlayerDrawCardScreen"] = [
    {"wram": {0xFF98: b"\x00", DCDS_wLCDC: b"\x80", DCDS_rLCDC: b"\x80", DCDS_wLoadedCard1: b"\x00", DCDS_hWhoseTurn: bytes((DCDS_TURN,)), DCDS_wPlayerDeck: b"\x10"}, "read": {DCDS_wLoadedCard1: 64}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 10000000, "cycle_budget": 40000000},
    dict(POISON, wram={0xFF98: b"\x03", DCDS_wLCDC: b"\x80", DCDS_rLCDC: b"\x80", DCDS_wLoadedCard1: b"\x00", DCDS_hWhoseTurn: bytes((DCDS_TURN,)), DCDS_wPlayerDeck + 3: b"\x20"}, read={DCDS_wLoadedCard1: 64}, keys=[0x00, 0x01], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=10000000, cycle_budget=40000000),
]
# <<< factory DisplayPlayerDrawCardScreen

# >>> factory OppAction_PlayTrainerCard
CONTRACT["OppAction_PlayTrainerCard"] = {"compare": (), "preserve": ()}
CASES["OppAction_PlayTrainerCard"] = [
    {"keys": [0x00, 0x01],
     "wram": {DUT_wLCDC: b"\x80", DUT_rLCDC: b"\x80", DUT_wLoadedCard1: b"\x00",
              DUT_hWhoseTurn: bytes((DUT_TURN,)), DUT_wPlayerDeck: b"\x10",
              DUT_hTempCardIndex_ff9f: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "read": {DUT_wLoadedCard1: 64, wSkipDuelistIsThinkingDelay: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01],
         wram={DUT_wLCDC: b"\x80", DUT_rLCDC: b"\x80", DUT_wLoadedCard1: b"\x00",
               DUT_hWhoseTurn: bytes((DUT_TURN,)), DUT_wPlayerDeck + 3: b"\x20",
               DUT_hTempCardIndex_ff9f: b"\x03"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         read={DUT_wLoadedCard1: 64, wSkipDuelistIsThinkingDelay: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OppAction_PlayTrainerCard

# >>> factory OpenActivePokemonScreen
CONTRACT["OpenActivePokemonScreen"] = {"compare": (), "preserve": ()}
CASES["OpenActivePokemonScreen"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\xFF", 0xCBC9: b"\xAA", 0xCBCA: b"\x55"}, "read": {0xCBC9: 1, 0xCBCA: 1}},
    {"wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xCBC9: b"\xAA", 0xCBCA: b"\x55", 0xCABB: b"\x00", 0xCBD7: b"\x01"}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 4000000, "cycle_budget": 16000000, "read": {0xCBC9: 1, 0xCBCA: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xC2BB: b"\x00", 0xCBC9: b"\xAA", 0xCBCA: b"\x55", 0xCABB: b"\x00", 0xCBD7: b"\x01"}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 4000000, "cycle_budget": 16000000, "read": {0xCBC9: 1, 0xCBCA: 1}}]
# <<< factory OpenActivePokemonScreen

# >>> factory DisplayPlayAreaScreenToUsePkmnPower
CONTRACT["DisplayPlayAreaScreenToUsePkmnPower"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DisplayPlayAreaScreenToUsePkmnPower"] = [
    {"keys": [0x00, 0x02], "instruction_budget": 5000000, "cycle_budget": 20000000, "wram": {0xFF97: b"\x00", 0xC2EF: b"\x00", 0xCABB: b"\x00"}, "read": {0xCBCF: 1}, "expect": {0xCBCF: b"\x00"}},
    dict(POISON, keys=[0x00, 0x02], instruction_budget=5000000, cycle_budget=20000000, wram={0xFF97: b"\x00", 0xC2EF: b"\x00", 0xCABB: b"\x00"}, read={0xCBCF: 1}, expect={0xCBCF: b"\x00"}),
]
# <<< factory DisplayPlayAreaScreenToUsePkmnPower

# >>> factory DisplayCardPage_PokemonOverview
CONTRACT["DisplayCardPage_PokemonOverview"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DisplayCardPage_PokemonOverview"] = [
    dict(id="DisplayCardPage_PokemonOverview-0", wram={wCardPageType: b"\x01", wCurPlayAreaSlot: b"\x01", wCurPlayAreaY: b"\x00", wLoadedCard1Stage: b"\x00", wLoadedCard1RetreatCost: b"\x01", 0xCABB: b"\x00", 0xFF80: b"\x01"}, read={wCurPlayAreaY: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000),
    dict(POISON, id="DisplayCardPage_PokemonOverview-1", wram={wCardPageType: b"\x01", wCurPlayAreaSlot: b"\x01", wCurPlayAreaY: b"\x00", wLoadedCard1Stage: b"\x00", wLoadedCard1RetreatCost: b"\x02", 0xCABB: b"\x00", 0xFF80: b"\x01"}, read={wCurPlayAreaY: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], instruction_budget=20000000, cycle_budget=100000000),
]
# <<< factory DisplayCardPage_PokemonOverview

# >>> factory DisplayEnergyOrTrainerCardPage
CONTRACT["DisplayEnergyOrTrainerCardPage"] = {"compare": ("a", "f", "hl", "d", "e"), "preserve": ()}
CASES["DisplayEnergyOrTrainerCardPage"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x00\x00", 0xCC27: b"\x33\x00", 0xCABB: b"\x00"}, "setup": SETUP_TEXT, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0xC500, wram={0xC500: b"\x00\x00", 0xCC27: b"\x33\x00", 0xCABB: b"\x00"}, setup=SETUP_TEXT, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DisplayEnergyOrTrainerCardPage

# >>> factory DisplayCardPage_Energy
CONTRACT["DisplayCardPage_Energy"] = {"compare": ("a", "f", "hl", "d", "e"), "preserve": ()}
CASES["DisplayCardPage_Energy"] = [
    {"wram": {0xCC2E: b"\x00\x00", 0xCC27: b"\x33\x00", 0xCABB: b"\x00"}, "setup": SETUP_TEXT, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, wram={0xCC2E: b"\x00\x00", 0xCC27: b"\x33\x00", 0xCABB: b"\x00"}, setup=SETUP_TEXT, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory DisplayCardPage_Energy

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {}
# >>> factory-mutation SetLineSeparation
MUTATIONS["SetLineSeparation"] = {
	"source_symbol": "SetLineSeparation",
	"before": "wLineSeparation = a;",
	"after": "wLineSeparation = (uint8_t)(a + 1u);",
	"case_ids": ["SetLineSeparation-0", "SetLineSeparation-1"],
}
# <<< factory-mutation SetLineSeparation
# >>> factory-mutation PlayAreaScreenMenuFunction
MUTATIONS["PlayAreaScreenMenuFunction"] = {
    "source_symbol": "PlayAreaScreenMenuFunction",
    "before": "return 0xA0u;",
    "after": "return 0x80u;",
    "case_ids": ["PlayAreaScreenMenuFunction-0", "PlayAreaScreenMenuFunction-5"],
}
# <<< factory-mutation PlayAreaScreenMenuFunction
# >>> factory-mutation SwitchAttackPage
MUTATIONS["SwitchAttackPage"] = {
	"source_symbol": "SwitchAttackPage",
	"before": "wAttackPageNumber ^ 0x01u",
	"after": "wAttackPageNumber & 0x01u",
	"case_ids": ["SwitchAttackPage-0", "SwitchAttackPage-1"],
}
# <<< factory-mutation SwitchAttackPage
# >>> factory-mutation CopyCGBCardPalette
MUTATIONS["CopyCGBCardPalette"] = {
    "source_symbol": "CopyCGBCardPalette",
    "before": "wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE)",
    "after": "wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE) + 1u",
    "case_ids": ["CopyCGBCardPalette-0", "CopyCGBCardPalette-1"],
}
# <<< factory-mutation CopyCGBCardPalette
# >>> factory-mutation CreateCardAttrBlkPacket
MUTATIONS["CreateCardAttrBlkPacket"] = {"source_symbol": "CreateCardAttrBlkPacket", "before": "gb_write8(hl, (uint8_t)((ATTR_BLK << 3) + 1u));", "after": "gb_write8(hl, (uint8_t)((ATTR_BLK << 3) + 2u));", "case_ids": ["CreateCardAttrBlkPacket-0", "CreateCardAttrBlkPacket-1", "CreateCardAttrBlkPacket-2"]}
# <<< factory-mutation CreateCardAttrBlkPacket
# >>> factory-mutation SaveDuelDataToDE
MUTATIONS["SaveDuelDataToDE"] = {
	"source_symbol": "SaveDuelDataToDE",
	"before": "gb_write8(base, TRUE);",
	"after": "gb_write8(base, 0u);",
	"case_ids": ["SaveDuelDataToDE-0"],
}
# <<< factory-mutation SaveDuelDataToDE
# >>> factory-mutation LoadSavedDuelDataFromDE
MUTATIONS["LoadSavedDuelDataFromDE"] = {
	"source_symbol": "LoadSavedDuelDataFromDE",
	"before": "de = (uint16_t)(de + SAVE_DUEL_HEADER_SIZE);",
	"after": "de = (uint16_t)(de + SAVE_DUEL_HEADER_SIZE - 1u);",
	"case_ids": ["LoadSavedDuelDataFromDE-0"],
}
# <<< factory-mutation LoadSavedDuelDataFromDE
# >>> factory-mutation SetBGP7OrSGB2ToCardPalette
MUTATIONS["SetBGP7OrSGB2ToCardPalette"] = {
	"source_symbol": "SetBGP7OrSGB2ToCardPalette",
	"before": "if (console == CONSOLE_SGB) {",
	"after": "if (console != CONSOLE_SGB) {",
	"case_ids": ["SetBGP7OrSGB2ToCardPalette-1"],
}
# <<< factory-mutation SetBGP7OrSGB2ToCardPalette
# >>> factory-mutation JPWriteByteToBGMap0
MUTATIONS["JPWriteByteToBGMap0"] = {
	"source_symbol": "JPWriteByteToBGMap0",
	"before": "WriteByteToBGMap0(a, b, c);",
	"after": "WriteByteToBGMap0(a, c, b);",
	"case_ids": ["JPWriteByteToBGMap0-1"],
}
# <<< factory-mutation JPWriteByteToBGMap0
# >>> factory-mutation ZeroObjectPositionsAndToggleOAMCopy
MUTATIONS["ZeroObjectPositionsAndToggleOAMCopy"] = {
	"source_symbol": "ZeroObjectPositionsAndToggleOAMCopy",
	"before": "wVBlankOAMCopyToggle = TRUE;",
	"after": "wVBlankOAMCopyToggle = 0u;",
	"case_ids": ["ZeroObjectPositionsAndToggleOAMCopy-0", "ZeroObjectPositionsAndToggleOAMCopy-1"],
}
# <<< factory-mutation ZeroObjectPositionsAndToggleOAMCopy
# >>> factory-mutation LoadPlayerDeck
MUTATIONS["LoadPlayerDeck"] = {
    "source_symbol": "LoadPlayerDeck",
    "before": "hl = (uint16_t)(hl + sDeck1Cards_ADDR);",
    "after": "hl = (uint16_t)(hl + sDeck1Cards_ADDR + 1u);",
    "case_ids": ["LoadPlayerDeck-0", "LoadPlayerDeck-2"],
}
# <<< factory-mutation LoadPlayerDeck
# >>> factory-mutation PrintPracticeDuelDrMasonInstructions
MUTATIONS["PrintPracticeDuelDrMasonInstructions"] = {
    "source_symbol": "PrintPracticeDuelDrMasonInstructions",
    "before": "PrintScrollableText_WithTextBoxLabel(hl, DrMasonText)",
    "after": "PrintScrollableText_WithTextBoxLabel(hl, DrMasonText + 1u)",
    "case_ids": ["PrintPracticeDuelDrMasonInstructions-0", "PrintPracticeDuelDrMasonInstructions-1"],
}
# <<< factory-mutation PrintPracticeDuelDrMasonInstructions
# >>> factory-mutation PrintPracticeDuelInstructionsTextBoxLabel
MUTATIONS["PrintPracticeDuelInstructionsTextBoxLabel"] = {
    "source_symbol": "PrintPracticeDuelInstructionsTextBoxLabel",
    "before": "if (a == 7u)",
    "after": "if (a == 8u)",
    "case_ids": ["PrintPracticeDuelInstructionsTextBoxLabel-1"],
}
# <<< factory-mutation PrintPracticeDuelInstructionsTextBoxLabel
# >>> factory-mutation SwitchCardPage
MUTATIONS["SwitchCardPage"] = {
    "source_symbol": "SwitchCardPage",
    "before": "\t\treturn CardPageSwitch_00();",
    "after": "\t\treturn (CardPageResult){0u, 0u};",
    "case_ids": ["SwitchCardPage-0", "SwitchCardPage-1"],
}
# <<< factory-mutation SwitchCardPage
# >>> factory-mutation CardPageSwitch_00
MUTATIONS["CardPageSwitch_00"] = {
    "source_symbol": "CardPageSwitch_00",
    "before": "return (CardPageResult){CARDPAGE_POKEMON_DESCRIPTION_C, 1u};",
    "after": "return (CardPageResult){CARDPAGE_POKEMON_DESCRIPTION_C + 1u, 1u};",
    "case_ids": ["CardPageSwitch_00-0", "CardPageSwitch_00-1"],
}
# <<< factory-mutation CardPageSwitch_00
# >>> factory-mutation LoadLoaded1CardGfx
MUTATIONS["LoadLoaded1CardGfx"] = {
    "source_symbol": "LoadLoaded1CardGfx",
    "before": "LoadCardGfx(hl, de, 0x30u, TILE_SIZE);",
    "after": "LoadCardGfx(hl, de, 0x20u, TILE_SIZE);",
    "case_ids": ["LoadLoaded1CardGfx-0", "LoadLoaded1CardGfx-1", "LoadLoaded1CardGfx-2"],
}
# <<< factory-mutation LoadLoaded1CardGfx
# >>> factory-mutation CreateCardAttrBlkPacket_DataSet
MUTATIONS["CreateCardAttrBlkPacket_DataSet"] = {
	"source_symbol": "CreateCardAttrBlkPacket_DataSet",
	"before": "gb_write8(hl++, d);",
	"after": "gb_write8(hl++, (uint8_t)(d + 1u));",
	"case_ids": ["CreateCardAttrBlkPacket_DataSet-1", "CreateCardAttrBlkPacket_DataSet-2"],
}
# <<< factory-mutation CreateCardAttrBlkPacket_DataSet
# >>> factory-mutation SetSGB3ToCardPalette
MUTATIONS["SetSGB3ToCardPalette"] = {"source_symbol": "SetSGB3ToCardPalette", "before": "wCardPalette_ADDR + 2u", "after": "wCardPalette_ADDR + 3u", "case_ids": ["SetSGB3ToCardPalette-1", "SetSGB3ToCardPalette-2"]}
# <<< factory-mutation SetSGB3ToCardPalette
# >>> factory-mutation LookForCardIDInPlayArea_Bank5
MUTATIONS["LookForCardIDInPlayArea_Bank5"] = {
    "source_symbol": "LookForCardIDInPlayArea_Bank5",
    "before": "\twTempCardIDToLook = a;",
    "after": "\twTempCardIDToLook = (uint8_t)(a + 1u);",
    "case_ids": ["LookForCardIDInPlayArea_Bank5-0", "LookForCardIDInPlayArea_Bank5-1", "LookForCardIDInPlayArea_Bank5-2", "LookForCardIDInPlayArea_Bank5-3", "LookForCardIDInPlayArea_Bank5-4", "LookForCardIDInPlayArea_Bank5-5"],
}
# <<< factory-mutation LookForCardIDInPlayArea_Bank5
# >>> factory-mutation PrintCardListHeaderAndInfoBoxTexts
MUTATIONS["PrintCardListHeaderAndInfoBoxTexts"] = {
    "source_symbol": "PrintCardListHeaderAndInfoBoxTexts",
    "before": "e = 14u;",
    "after": "e = 13u;",
    "case_ids": ["PrintCardListHeaderAndInfoBoxTexts-0", "PrintCardListHeaderAndInfoBoxTexts-1"],
}
# <<< factory-mutation PrintCardListHeaderAndInfoBoxTexts
# >>> factory-mutation ClearMemory_Bank5
MUTATIONS["ClearMemory_Bank5"] = {
    "source_symbol": "ClearMemory_Bank5",
    "before": "uint32_t n = a ? a : 0x100u;",
    "after": "uint32_t n = a ? a : 0x1u;",
    "case_ids": ["ClearMemory_Bank5-0"],
}
# <<< factory-mutation ClearMemory_Bank5
# >>> factory-mutation CheckCardPageExists
MUTATIONS["CheckCardPageExists"] = {
    "source_symbol": "CheckCardPageExists",
    "before": "\ta |= gb_read8(*hl);",
    "after": "\ta &= gb_read8(*hl);",
    "case_ids": ["CheckCardPageExists-2", "CheckCardPageExists-3", "CheckCardPageExists-4"],
}
# <<< factory-mutation CheckCardPageExists
# >>> factory-mutation CardPageSwitch_PokemonEnd
MUTATIONS["CardPageSwitch_PokemonEnd"] = {
    "source_symbol": "CardPageSwitch_PokemonEnd",
    "before": "return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 1u};",
    "after": "return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 0u};",
    "case_ids": ["CardPageSwitch_PokemonEnd-0", "CardPageSwitch_PokemonEnd-1", "CardPageSwitch_PokemonEnd-2"],
}
# <<< factory-mutation CardPageSwitch_PokemonEnd
# >>> factory-mutation SetCardListInfoBoxText
MUTATIONS["SetCardListInfoBoxText"] = {
    "source_symbol": "SetCardListInfoBoxText",
    "before": "wCardListInfoBoxText = (uint8_t)hl;",
    "after": "wCardListInfoBoxText = (uint8_t)(hl >> 8);",
    "case_ids": ["SetCardListInfoBoxText-1", "SetCardListInfoBoxText-2"],
}
# <<< factory-mutation SetCardListInfoBoxText
# >>> factory-mutation LoadCardNameToTxRam2
MUTATIONS["LoadCardNameToTxRam2"] = {
    "source_symbol": "LoadCardNameToTxRam2",
    "before": "\tgb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)));",
    "after": "\tgb_write8((uint16_t)(wTxRam2_ADDR + 2u), gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)));",
    "case_ids": ["LoadCardNameToTxRam2-0", "LoadCardNameToTxRam2-1", "LoadCardNameToTxRam2-2", "LoadCardNameToTxRam2-3"],
}
# <<< factory-mutation LoadCardNameToTxRam2
# >>> factory-mutation LoadCardNameToTxRam2_b
MUTATIONS["LoadCardNameToTxRam2_b"] = {
    "source_symbol": "LoadCardNameToTxRam2_b",
    "before": "\tgb_write8((uint16_t)(wTxRam2_b_ADDR + 1u), hi);",
    "after": "\tgb_write8((uint16_t)(wTxRam2_b_ADDR + 2u), hi);",
    "case_ids": ["LoadCardNameToTxRam2_b-1", "LoadCardNameToTxRam2_b-2", "LoadCardNameToTxRam2_b-3"],
}
# <<< factory-mutation LoadCardNameToTxRam2_b
# >>> factory-mutation GetAnimCoordsAndFlags
MUTATIONS["GetAnimCoordsAndFlags"] = {
    "source_symbol": "GetAnimCoordsAndFlags",
    "before": "if (wDuelAnimDuelistSide != PLAYER_TURN)",
    "after": "if (wDuelAnimDuelistSide == PLAYER_TURN)",
    "case_ids": ["GetAnimCoordsAndFlags-0", "GetAnimCoordsAndFlags-2", "GetAnimCoordsAndFlags-3", "GetAnimCoordsAndFlags-5"],
}
# <<< factory-mutation GetAnimCoordsAndFlags
# >>> factory-mutation PlayBufferedDuelAnimations
MUTATIONS["PlayBufferedDuelAnimations"] = {
    "source_symbol": "PlayBufferedDuelAnimations",
    "before": "if (cur == size) {",
    "after": "if (cur != size) {",
    "case_ids": ["PlayBufferedDuelAnimations-0", "PlayBufferedDuelAnimations-1"],
}
# <<< factory-mutation PlayBufferedDuelAnimations
# >>> factory-mutation CopyListWithFFTerminatorFromHLToDE_Bank5
MUTATIONS["CopyListWithFFTerminatorFromHLToDE_Bank5"] = {"source_symbol": "CopyListWithFFTerminatorFromHLToDE_Bank5", "before": "\t\tif (a == 0xFFu)", "after": "\t\tif (a == 0xFEu)", "case_ids": ["CopyListWithFFTerminatorFromHLToDE_Bank5-0", "CopyListWithFFTerminatorFromHLToDE_Bank5-1", "CopyListWithFFTerminatorFromHLToDE_Bank5-2"]}
# <<< factory-mutation CopyListWithFFTerminatorFromHLToDE_Bank5
# >>> factory-mutation CheckEnergyFlagsNeededInList
MUTATIONS["CheckEnergyFlagsNeededInList"] = {"source_symbol": "CheckEnergyFlagsNeededInList", "before": "return (EnergyFlagsResult){0xffu, 0u};", "after": "return (EnergyFlagsResult){0u, 0u};", "case_ids": ["CheckEnergyFlagsNeededInList-0", "CheckEnergyFlagsNeededInList-1", "CheckEnergyFlagsNeededInList-2", "CheckEnergyFlagsNeededInList-3"]}
# <<< factory-mutation CheckEnergyFlagsNeededInList
# >>> factory-mutation CardPageSwitch_EnergyEnd
MUTATIONS["CardPageSwitch_EnergyEnd"] = {"source_symbol": "CardPageSwitch_EnergyEnd", "before": "return (CardPageResult){CARDPAGE_ENERGY, 1u};", "after": "return (CardPageResult){CARDPAGE_TRAINER_2, 1u};", "case_ids": ["CardPageSwitch_EnergyEnd-0", "CardPageSwitch_EnergyEnd-1"]}
# <<< factory-mutation CardPageSwitch_EnergyEnd
# >>> factory-mutation CardPageSwitch_0c
MUTATIONS["CardPageSwitch_0c"] = {"source_symbol": "CardPageSwitch_0c", "before": "return (CardPageResult){CARDPAGE_TRAINER_2, 1u};", "after": "return (CardPageResult){CARDPAGE_ENERGY, 1u};", "case_ids": ["CardPageSwitch_0c-0", "CardPageSwitch_0c-1"]}
# <<< factory-mutation CardPageSwitch_0c
# >>> factory-mutation PlaceCardImageOAM
MUTATIONS["PlaceCardImageOAM"] = {"source_symbol": "PlaceCardImageOAM", "before": "\tgb_write8(0xcac0u, TRUE);", "after": "\tgb_write8(0xcac0u, 0u);", "case_ids": ["PlaceCardImageOAM-0", "PlaceCardImageOAM-1"]}
# <<< factory-mutation PlaceCardImageOAM
# >>> factory-mutation PrintPlayAreaCardAttachedEnergies
MUTATIONS["PrintPlayAreaCardAttachedEnergies"] = {
    "source_symbol": "PrintPlayAreaCardAttachedEnergies",
    "before": "gb_write8((uint16_t)(wDefaultText_ADDR + i), SYM_SPACE);",
    "after": "gb_write8((uint16_t)(wDefaultText_ADDR + i), SYM_FIRE);",
    "case_ids": ["PrintPlayAreaCardAttachedEnergies-0", "PrintPlayAreaCardAttachedEnergies-1", "PrintPlayAreaCardAttachedEnergies-2"],
}
# <<< factory-mutation PrintPlayAreaCardAttachedEnergies
# >>> factory-mutation DiscardRetreatCostCards
MUTATIONS["DiscardRetreatCostCards"] = {"source_symbol": "DiscardRetreatCostCards", "before": "uint8_t card = gb_read8(hl);", "after": "uint8_t card = gb_read8((uint16_t)(hl + 2u));", "case_ids": ["DiscardRetreatCostCards-0", "DiscardRetreatCostCards-1", "DiscardRetreatCostCards-2"]}
# <<< factory-mutation DiscardRetreatCostCards
# >>> factory-mutation OppAction_DrawCard
MUTATIONS["OppAction_DrawCard"] = {"source_symbol": "OppAction_DrawCard", "before": "return (OppActionDrawResult){r.a, r.f};", "after": "return (OppActionDrawResult){r.a, 0u};", "case_ids": ["OppAction_DrawCard-0", "OppAction_DrawCard-1", "OppAction_DrawCard-2"]}
# <<< factory-mutation OppAction_DrawCard
# >>> factory-mutation PrintSortNumberInCardList
MUTATIONS["PrintSortNumberInCardList_SetPointer"] = {
	"source_symbol": "PrintSortNumberInCardList_SetPointer",
	"before": "wSortCardListByID = TRUE_VAL;",
	"after": "wSortCardListByID = 0u;",
	"case_ids": ["PrintSortNumberInCardList_SetPointer-0", "PrintSortNumberInCardList_SetPointer-1"],
}
# <<< factory-mutation PrintSortNumberInCardList
# >>> factory-mutation PrintEnergiesOfColor
MUTATIONS["PrintEnergiesOfColor"] = {
    "source_symbol": "PrintEnergiesOfColor",
    "before": "count = (uint8_t)(a & 0x0Fu);",
    "after": "count = (uint8_t)(a & 0x0Eu);",
    "case_ids": ["PrintEnergiesOfColor-2", "PrintEnergiesOfColor-3", "PrintEnergiesOfColor-4"],
}
# <<< factory-mutation PrintEnergiesOfColor
# >>> factory-mutation PrintCardPageWeaknessesOrResistances
MUTATIONS["PrintCardPageWeaknessesOrResistances"] = {"source_symbol": "PrintCardPageWeaknessesOrResistances", "before": "if (mask & 0x80u)", "after": "if (mask & 0x40u)", "case_ids": ["PrintCardPageWeaknessesOrResistances-1", "PrintCardPageWeaknessesOrResistances-2", "PrintCardPageWeaknessesOrResistances-4"]}
# <<< factory-mutation PrintCardPageWeaknessesOrResistances
# >>> factory-mutation Func_6423
MUTATIONS["Func_6423"] = {"source_symbol": "Func_6423", "before": "value = gb_read8(pos);", "after": "value = gb_read8((uint16_t)(pos + 1u));", "case_ids": ["Func_6423-1", "Func_6423-2"]}
# <<< factory-mutation Func_6423
# >>> factory-mutation InitVariablesToBeginDuel
MUTATIONS["InitVariablesToBeginDuel"] = {"source_symbol": "InitVariablesToBeginDuel", "before": "\t\t((a & DUELIST_TYPE_AI_OPP) != 0u));", "after": "\t\t((a & 0x40u) != 0u));", "case_ids": ["InitVariablesToBeginDuel-1", "InitVariablesToBeginDuel-3", "InitVariablesToBeginDuel-5"]}
# <<< factory-mutation InitVariablesToBeginDuel
# >>> factory-mutation CardPageSwitch_PokemonAttack1Page2
MUTATIONS["CardPageSwitch_PokemonAttack1Page2"] = {"source_symbol": "CardPageSwitch_PokemonAttack1Page2", "before": "*hl = (uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u);", "after": "*hl = (uint16_t)(wLoadedCard1Atk1Description_ADDR + 1u);", "case_ids": ["CardPageSwitch_PokemonAttack1Page2-1", "CardPageSwitch_PokemonAttack1Page2-2"]}
# <<< factory-mutation CardPageSwitch_PokemonAttack1Page2
# >>> factory-mutation CardPageSwitch_PokemonAttack2Page1
MUTATIONS["CardPageSwitch_PokemonAttack2Page1"] = {"source_symbol": "CardPageSwitch_PokemonAttack2Page1", "before": "\tuint16_t hl = wLoadedCard1Atk2Name_ADDR;", "after": "\tuint16_t hl = wLoadedCard1Atk1Description_ADDR;", "case_ids": ["CardPageSwitch_PokemonAttack2Page1-2", "CardPageSwitch_PokemonAttack2Page1-3", "CardPageSwitch_PokemonAttack2Page1-4"]}
# <<< factory-mutation CardPageSwitch_PokemonAttack2Page1
# >>> factory-mutation AIDiscourage
MUTATIONS["AIDiscourage"] = {"source_symbol": "AIDiscourage", "before": "\tif (score < a) {", "after": "\tif (score > a) {", "case_ids": ["AIDiscourage-1", "AIDiscourage-2", "AIDiscourage-3", "AIDiscourage-4"]}
# <<< factory-mutation AIDiscourage
# >>> factory-mutation ConvertHPToDamageCounters_Bank5
MUTATIONS["ConvertHPToDamageCounters_Bank5"] = {"source_symbol": "ConvertHPToDamageCounters_Bank5", "before": "\t\tif (value < 10u)", "after": "\t\tif (value <= 10u)", "case_ids": ["ConvertHPToDamageCounters_Bank5-2", "ConvertHPToDamageCounters_Bank5-4"]}
# <<< factory-mutation ConvertHPToDamageCounters_Bank5
# >>> factory-mutation CalculateBDividedByA_Bank5
MUTATIONS["CalculateBDividedByA_Bank5"] = {"source_symbol": "CalculateBDividedByA_Bank5", "before": "\t\tuint8_t result = (uint8_t)(remainder - divisor);", "after": "\t\tuint8_t result = (uint8_t)(remainder + divisor);", "case_ids": ["CalculateBDividedByA_Bank5-1", "CalculateBDividedByA_Bank5-2", "CalculateBDividedByA_Bank5-3", "CalculateBDividedByA_Bank5-4", "CalculateBDividedByA_Bank5-5"]}
# <<< factory-mutation CalculateBDividedByA_Bank5
# >>> factory-mutation PrintCardPageRarityIcon
MUTATIONS["PrintCardPageRarityIcon"] = {
	"source_symbol": "PrintCardPageRarityIcon",
	"before": "a = (uint8_t)((a + 1u) << 1);",
	"after": "a = (uint8_t)((a + 2u) << 1);",
	"case_ids": ["PrintCardPageRarityIcon-0", "PrintCardPageRarityIcon-1"],
}
# <<< factory-mutation PrintCardPageRarityIcon
# >>> factory-mutation SetNoLineSeparation
MUTATIONS["SetNoLineSeparation"] = {
	"source_symbol": "SetNoLineSeparation",
	"before": "SetLineSeparation(1u);",
	"after": "SetLineSeparation(0u);",
	"case_ids": ["SetNoLineSeparation-0"],
}
# <<< factory-mutation SetNoLineSeparation
# >>> factory-mutation AIPlayInitialBasicCards
MUTATIONS["AIPlayInitialBasicCards"] = {
    "source_symbol": "AIPlayInitialBasicCards",
    "before": "return (AIPlayInitialBasicCardsResult){0xFFu, 0xC0u};",
    "after": "return (AIPlayInitialBasicCardsResult){0x00u, 0xC0u};",
    "case_ids": ["AIPlayInitialBasicCards-0"],
}
# <<< factory-mutation AIPlayInitialBasicCards
# >>> factory-mutation CheckIfEnoughParticularAttachedEnergy
MUTATIONS["CheckIfEnoughParticularAttachedEnergy"] = {
    "source_symbol": "CheckIfEnoughParticularAttachedEnergy",
    "before": "return (CheckIfEnoughParticularAttachedEnergyResult){b, 0x80u, (uint8_t)(b + 1u), (uint16_t)(hl + 1u)};",
    "after": "return (CheckIfEnoughParticularAttachedEnergyResult){b, 0x00u, (uint8_t)(b + 1u), (uint16_t)(hl + 1u)};",
    "case_ids": ["CheckIfEnoughParticularAttachedEnergy-0"],
}
# <<< factory-mutation CheckIfEnoughParticularAttachedEnergy
# >>> factory-mutation LookForCardIDInHand
MUTATIONS["LookForCardIDInHand"] = {
	"source_symbol": "LookForCardIDInHand",
	"before": "if (last_id == a)",
	"after": "if (last_id != a)",
	"case_ids": ["LookForCardIDInHand-0"],
}
# <<< factory-mutation LookForCardIDInHand
# >>> factory-mutation LookForCardIDInHandList_Bank5
MUTATIONS["LookForCardIDInHandList_Bank5"] = {
	"source_symbol": "LookForCardIDInHandList_Bank5",
	"before": "if ((uint8_t)LoadCardDataToBuffer1_FromDeckIndex(deck_index) == a)",
	"after": "if ((uint8_t)LoadCardDataToBuffer1_FromDeckIndex(deck_index) != a)",
	"case_ids": ["LookForCardIDInHandList_Bank5-0"],
}
# <<< factory-mutation LookForCardIDInHandList_Bank5
# >>> factory-mutation CheckForEvolutionInDeck
MUTATIONS["CheckForEvolutionInDeck"]={"source_symbol":"CheckForEvolutionInDeck","before":"arena == 0u ? 0x80u : 0u","after":"arena != 0u ? 0x80u : 0u","case_ids":["CheckForEvolutionInDeck-0","CheckForEvolutionInDeck-1"]}
# <<< factory-mutation CheckForEvolutionInDeck
# >>> factory-mutation LookForCardThatIsKnockedOutOnDevolution
MUTATIONS["LookForCardThatIsKnockedOutOnDevolution"]={"source_symbol":"LookForCardThatIsKnockedOutOnDevolution","before":"if (hp <= rem)","after":"if (hp > rem)","case_ids":["LookForCardThatIsKnockedOutOnDevolution-0"]}
# <<< factory-mutation LookForCardThatIsKnockedOutOnDevolution
# >>> factory-mutation CalculateParticularAttachedEnergyNeeded
MUTATIONS["CalculateParticularAttachedEnergyNeeded"] = {"source_symbol": "CalculateParticularAttachedEnergyNeeded", "before": "return (CalculateParticularAttachedEnergyNeededResult){0u, (uint8_t)(next_b == 0u ? 0x80u : 0u), next_b, (uint16_t)(hl + 1u)};", "after": "return (CalculateParticularAttachedEnergyNeededResult){1u, (uint8_t)(next_b == 0u ? 0x80u : 0u), next_b, (uint16_t)(hl + 1u)};", "case_ids": ["CalculateParticularAttachedEnergyNeeded-0"]}
# <<< factory-mutation CalculateParticularAttachedEnergyNeeded
# >>> factory-mutation GetAnimationData
MUTATIONS["GetAnimationData"] = {
    "source_symbol": "GetAnimationData",
    "before": "uint16_t offset = (uint16_t)animation * 6u;",
    "after": "uint16_t offset = (uint16_t)animation * 5u;",
    "case_ids": ["GetAnimationData-1", "GetAnimationData-2"],
}
# <<< factory-mutation GetAnimationData
# >>> factory-mutation CardPageSwitch_PokemonOverviewOrDescription
MUTATIONS["CardPageSwitch_PokemonOverviewOrDescription"] = {
    "source_symbol": "CardPageSwitch_PokemonOverviewOrDescription",
    "before": "return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 0u};",
    "after": "return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW + 1u, 0u};",
    "case_ids": ["CardPageSwitch_PokemonOverviewOrDescription-0", "CardPageSwitch_PokemonOverviewOrDescription-1"],
}
# <<< factory-mutation CardPageSwitch_PokemonOverviewOrDescription
# >>> factory-mutation CheckCardEvolutionInHandOrDeck
MUTATIONS["CheckCardEvolutionInHandOrDeck"] = {"source_symbol": "CheckCardEvolutionInHandOrDeck", "before": "return (CheckCardEvolutionInHandOrDeckResult){original, (uint8_t)(original == 0u ? 0x80u : 0u)};", "after": "return (CheckCardEvolutionInHandOrDeckResult){0u, 0u};", "case_ids": ["CheckCardEvolutionInHandOrDeck-0", "CheckCardEvolutionInHandOrDeck-1"]}
# <<< factory-mutation CheckCardEvolutionInHandOrDeck
# >>> factory-mutation CheckIfOpponentHasBossDeckID
MUTATIONS["CheckIfOpponentHasBossDeckID"] = {"source_symbol": "CheckIfOpponentHasBossDeckID", "before": "return (CheckIfOpponentHasBossDeckIDResult){a, carry};", "after": "return (CheckIfOpponentHasBossDeckIDResult){0u, carry};", "case_ids": ["CheckIfOpponentHasBossDeckID-1", "CheckIfOpponentHasBossDeckID-2", "CheckIfOpponentHasBossDeckID-3"]}
# <<< factory-mutation CheckIfOpponentHasBossDeckID
# >>> factory-mutation RaiseAIScoreToAllMatchingIDsInBench
MUTATIONS["RaiseAIScoreToAllMatchingIDsInBench"] = {"source_symbol": "RaiseAIScoreToAllMatchingIDsInBench", "before": "bench.hl = (uint16_t)(bench.hl + 1u);", "after": "bench.hl = (uint16_t)(bench.hl + 2u);", "case_ids": ["RaiseAIScoreToAllMatchingIDsInBench-0", "RaiseAIScoreToAllMatchingIDsInBench-1", "RaiseAIScoreToAllMatchingIDsInBench-2"]}
# <<< factory-mutation RaiseAIScoreToAllMatchingIDsInBench
# >>> factory-mutation GetDamageNumberChars
MUTATIONS["GetDamageNumberChars"] = {
	"source_symbol": "GetDamageNumberChars",
	"before": "digit = (uint8_t)(digit + 1u);",
	"after": "digit = (uint8_t)(digit + 2u);",
	"case_ids": ["GetDamageNumberChars-0", "GetDamageNumberChars-1", "GetDamageNumberChars-2", "GetDamageNumberChars-3"],
}
# <<< factory-mutation GetDamageNumberChars
# >>> factory-mutation CardPageSwitch_PokemonAttack2Page2
MUTATIONS["CardPageSwitch_PokemonAttack2Page2"] = {"source_symbol": "CardPageSwitch_PokemonAttack2Page2", "before": "\tuint16_t hl = (uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u);", "after": "\tuint16_t hl = (uint16_t)(wLoadedCard1Atk2Description_ADDR + 3u);", "case_ids": ["CardPageSwitch_PokemonAttack2Page2-1", "CardPageSwitch_PokemonAttack2Page2-2", "CardPageSwitch_PokemonAttack2Page2-3"]}
# <<< factory-mutation CardPageSwitch_PokemonAttack2Page2
# >>> factory-mutation CardPageSwitch_08
MUTATIONS["CardPageSwitch_08"] = {"source_symbol": "CardPageSwitch_08", "before": "CARDPAGE_ENERGY + 1u", "after": "CARDPAGE_ENERGY + 2u", "case_ids": ["CardPageSwitch_08-0", "CardPageSwitch_08-1"]}
# <<< factory-mutation CardPageSwitch_08
# >>> factory-mutation LoadPlayAreaCardGfx
MUTATIONS["LoadPlayAreaCardGfx"] = {
	"source_symbol": "LoadPlayAreaCardGfx",
	"before": "LoadLoaded1CardGfx(de);",
	"after": "LoadLoaded1CardGfx((uint16_t)(de + 1u));",
	"case_ids": ["LoadPlayAreaCardGfx-1", "LoadPlayAreaCardGfx-2"],
}
# <<< factory-mutation LoadPlayAreaCardGfx
# >>> factory-mutation SetBGP6OrSGB3ToCardPalette
MUTATIONS["SetBGP6OrSGB3ToCardPalette"] = {
	"source_symbol": "SetBGP6OrSGB3ToCardPalette",
	"before": "CopyCGBCardPalette(0x06u);",
	"after": "CopyCGBCardPalette(0x07u);",
	"case_ids": ["SetBGP6OrSGB3ToCardPalette-2"],
}
# <<< factory-mutation SetBGP6OrSGB3ToCardPalette
# >>> factory-mutation SetOneLineSeparation
MUTATIONS["SetOneLineSeparation"] = {
	"source_symbol": "SetOneLineSeparation",
	"before": "SetLineSeparation(0u);",
	"after": "SetLineSeparation(1u);",
	"case_ids": ["SetOneLineSeparation-0"],
}
# <<< factory-mutation SetOneLineSeparation
# >>> factory-mutation _HasAlivePokemonInPlayArea
MUTATIONS["_HasAlivePokemonInPlayArea"] = {
    "source_symbol": "_HasAlivePokemonInPlayArea",
    "before": "wPlayAreaSelectAction = 0u;",
    "after": "wPlayAreaSelectAction = 1u;",
    "case_ids": ["_HasAlivePokemonInPlayArea-0", "_HasAlivePokemonInPlayArea-1"],
}
# <<< factory-mutation _HasAlivePokemonInPlayArea
# >>> factory-mutation PrintPlayAreaCardLocation
MUTATIONS["PrintPlayAreaCardLocation"] = {
    "source_symbol": "PrintPlayAreaCardLocation",
    "before": "uint8_t tile = kPlayAreaLocationTileNumbers[index + i];",
    "after": "uint8_t tile = kPlayAreaLocationTileNumbers[index + i + 1u];",
    "case_ids": ["PrintPlayAreaCardLocation-0", "PrintPlayAreaCardLocation-1", "PrintPlayAreaCardLocation-2"],
}
# <<< factory-mutation PrintPlayAreaCardLocation
# >>> factory-mutation CheckPrintPoisoned
MUTATIONS["CheckPrintPoisoned"] = {
    "source_symbol": "CheckPrintPoisoned",
    "before": "if ((status & POISONED) != 0u)",
    "after": "if ((status & POISONED) == 0u)",
    "case_ids": ["CheckPrintPoisoned-1", "CheckPrintPoisoned-2"],
}
# <<< factory-mutation CheckPrintPoisoned
# >>> factory-mutation Func_14323
MUTATIONS["Func_14323"] = {
    "source_symbol": "Func_14323",
    "before": "return (Func14323Result){selection.carry == 0u ? FLAG_C : FLAG_Z};",
    "after": "return (Func14323Result){selection.carry == 0u ? FLAG_Z : FLAG_C};",
    "case_ids": ["Func_14323-0"],
}
# <<< factory-mutation Func_14323
# >>> factory-mutation CreateEnergyCardListFromHand
MUTATIONS["CreateEnergyCardListFromHand"] = {
    "source_symbol": "CreateEnergyCardListFromHand",
    "before": "uint8_t remaining = count;",
    "after": "uint8_t remaining = (uint8_t)(count + 1u);",
    "case_ids": ["CreateEnergyCardListFromHand-1"],
}
# <<< factory-mutation CreateEnergyCardListFromHand

# >>> factory-mutation DrawHPBar
MUTATIONS["DrawHPBar"] = {
    "source_symbol": "DrawHPBar",
    "before": "uint8_t tile = SYM_HP_OK;",
    "after": "uint8_t tile = SYM_HP_NOK;",
    "case_ids": ["DrawHPBar-0", "DrawHPBar-1"],
}
# <<< factory-mutation DrawHPBar
# >>> factory-mutation ValidateSavedDuelDataFromHL
MUTATIONS["ValidateSavedDuelDataFromHL"] = {
    "source_symbol": "ValidateSavedDuelDataFromHL",
    "before": "if (valid != 0u)",
    "after": "if (valid == 0u)",
    "case_ids": ["ValidateSavedDuelDataFromHL-0", "ValidateSavedDuelDataFromHL-1"],
}
# <<< factory-mutation ValidateSavedDuelDataFromHL# >>> factory-mutation ResetDoFrameFunction_Bank1
MUTATIONS["ResetDoFrameFunction_Bank1"] = {
    "source_symbol": "ResetDoFrameFunction_Bank1",
    "before": "gb_write8(wDoFrameFunction_ADDR, 0u);",
    "after": "gb_write8(wDoFrameFunction_ADDR, 1u);",
    "case_ids": ["ResetDoFrameFunction_Bank1-0"],
}
# <<< factory-mutation ResetDoFrameFunction_Bank1
# >>> factory-mutation OppAction_NoAction
MUTATIONS["OppAction_NoAction"] = {
    "source_symbol": "OppAction_NoAction",
    "before": "void OppAction_NoAction(void)\n{\n}",
    "after": "void OppAction_NoAction(void)\n{\n\tgb_write8(0xCC24u, 0u);\n}",
    "case_ids": ["OppAction_NoAction-0"],
}
# <<< factory-mutation OppAction_NoAction
# >>> factory-mutation ReturnRetreatCostCardsToArena
MUTATIONS["ReturnRetreatCostCardsToArena"] = {"source_symbol": "ReturnRetreatCostCardsToArena", "before": "b, c, d, e, hl};", "after": "b, c, d, e, (uint16_t)(hl + 1u)};", "case_ids": ["ReturnRetreatCostCardsToArena-0", "ReturnRetreatCostCardsToArena-1"]}
# <<< factory-mutation ReturnRetreatCostCardsToArena
# >>> factory-mutation FindHighestBenchScore
MUTATIONS["FindHighestBenchScore"] = {
    "source_symbol": "FindHighestBenchScore",
    "before": "if (value >= best)",
    "after": "if (value > best)",
    "case_ids": ["FindHighestBenchScore-1", "FindHighestBenchScore-2"],
}
# <<< factory-mutation FindHighestBenchScore
# >>> factory-mutation AIEncourage
MUTATIONS["AIEncourage"] = {
    "source_symbol": "AIEncourage",
    "before": "wAIScore = sum > 0xFFu ? 0xFFu : result;",
    "after": "wAIScore = result;",
    "case_ids": ["AIEncourage-2", "AIEncourage-3"],
}
# <<< factory-mutation AIEncourage
# >>> factory-mutation ReturnWrongAction
MUTATIONS["ReturnWrongAction"] = {
    "source_symbol": "ReturnWrongAction",
    "before": "return (uint8_t)((f & 0x80u) | 0x10u);",
    "after": "return (uint8_t)((f & 0x80u) | 0x20u);",
    "case_ids": ["ReturnWrongAction-0", "ReturnWrongAction-1", "ReturnWrongAction-2"],
}
# <<< factory-mutation ReturnWrongAction
# >>> factory-mutation IsLoadedCard1BasicPokemon
MUTATIONS["IsLoadedCard1BasicPokemon"] = {
    "source_symbol": "IsLoadedCard1BasicPokemon",
    "before": "id == 0xCCu || id == 0xCBu",
    "after": "id == 0xCDu || id == 0xCBu",
    "case_ids": ["IsLoadedCard1BasicPokemon-6"],
}
# <<< factory-mutation IsLoadedCard1BasicPokemon
# >>> factory-mutation HandleFailedToContinueDuel
MUTATIONS["HandleFailedToContinueDuel"] = {
    "source_symbol": "HandleFailedToContinueDuel",
    "before": "return (uint8_t)(0x80u | 0x10u);",
    "after": "return (uint8_t)(0x80u | 0x20u);",
    "case_ids": ["HandleFailedToContinueDuel-0", "HandleFailedToContinueDuel-1"],
}
# <<< factory-mutation HandleFailedToContinueDuel
MUTATIONS["PracticeDuel_PlayGoldeen"] = {
    "source_symbol": "PracticeDuel_PlayGoldeen",
    "before": "return (PracticeDuelPlayGoldeenResult){0xC0u};",
    "after": "return (PracticeDuelPlayGoldeenResult){0x80u};",
    "case_ids": ["PracticeDuel_PlayGoldeen-0"],
}
# <<< factory-mutation PracticeDuel_PlayGoldeen
# >>> factory-mutation CheckSkipDelayAllowed
MUTATIONS["CheckSkipDelayAllowed"] = {
    "source_symbol": "CheckSkipDelayAllowed",
    "before": "(gb_read8(hKeysHeld_ADDR) & PAD_B) != 0u",
    "after": "(gb_read8(hKeysHeld_ADDR) & PAD_B) == 0u",
    "case_ids": ["CheckSkipDelayAllowed-2", "CheckSkipDelayAllowed-3"],
}
# <<< factory-mutation CheckSkipDelayAllowed
# >>> factory-mutation AIMakeDecision
MUTATIONS["AIMakeDecision"] = {
    "source_symbol": "AIMakeDecision",
    "before": "gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);",
    "after": "gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 0u);",
    "case_ids": ["AIMakeDecision-0"],
}
# <<< factory-mutation AIMakeDecision

# >>> factory-mutation Func_6ba2
MUTATIONS["Func_6ba2"] = {
    "source_symbol": "Func_6ba2",
    "before": "wDuelistType != DUELIST_TYPE_LINK_OPP",
    "after": "wDuelistType == DUELIST_TYPE_LINK_OPP",
    "case_ids": ["Func_6ba2-0", "Func_6ba2-1"],
}
# <<< factory-mutation Func_6ba2# >>> factory-mutation TwoByteNumberToTxSymbol_PadSpace_Bank1
MUTATIONS["TwoByteNumberToTxSymbol_PadSpace_Bank1"] = {"source_symbol": "TwoByteNumberToTxSymbol_PadSpace_Bank1", "before": "gb_write8((uint16_t)(wStringBuffer_ADDR + i), SYM_SPACE);", "after": "gb_write8((uint16_t)(wStringBuffer_ADDR + i), SYM_FIRE);", "case_ids": ["TwoByteNumberToTxSymbol_PadSpace_Bank1-0", "TwoByteNumberToTxSymbol_PadSpace_Bank1-1", "TwoByteNumberToTxSymbol_PadSpace_Bank1-2"]}
# <<< factory-mutation TwoByteNumberToTxSymbol_PadSpace_Bank1
# >>> factory-mutation DrawWideTextBox_WaitForInput_Bank1
MUTATIONS["DrawWideTextBox_WaitForInput_Bank1"] = {
    "source_symbol": "DrawWideTextBox_WaitForInput_Bank1",
    "before": "return DrawWideTextBox_WaitForInput(hl);",
    "after": "return (WaitResult){0x10u};",
    "case_ids": ["DrawWideTextBox_WaitForInput_Bank1-0", "DrawWideTextBox_WaitForInput_Bank1-1"],
}
# <<< factory-mutation DrawWideTextBox_WaitForInput_Bank1

# >>> factory-mutation CheckForEvolutionInList
MUTATIONS["CheckForEvolutionInList"] = {
    "source_symbol": "CheckForEvolutionInList",
    "before": "if (check.f & 0x10u)",
    "after": "if (check.f & 0x00u)",
    "case_ids": ["CheckForEvolutionInList-0", "CheckForEvolutionInList-1"],
}
# <<< factory-mutation CheckForEvolutionInList
# >>> factory-mutation CheckIfEnergyIsUseful
MUTATIONS["CheckIfEnergyIsUseful"] = {
    "source_symbol": "CheckIfEnergyIsUseful",
    "before": "if (energy == DOUBLE_COLORLESS_ENERGY || wTempCardType == TYPE_ENERGY_DOUBLE_COLORLESS)",
    "after": "if (energy == DOUBLE_COLORLESS_ENERGY && wTempCardType == TYPE_ENERGY_DOUBLE_COLORLESS)",
    "case_ids": ["CheckIfEnergyIsUseful-0"],
}
# <<< factory-mutation CheckIfEnergyIsUseful
# >>> factory-mutation CountNumberOfEnergyCardsAttached
MUTATIONS["CountNumberOfEnergyCardsAttached"] = {
    "source_symbol": "CountNumberOfEnergyCardsAttached",
    "before": "colorless >> 1",
    "after": "colorless",
    "case_ids": ["CountNumberOfEnergyCardsAttached-1", "CountNumberOfEnergyCardsAttached-2"],
}
# <<< factory-mutation CountNumberOfEnergyCardsAttached
# >>> factory-mutation GetAttacksEnergyCostBits
MUTATIONS["GetAttacksEnergyCostBits"] = {
    "source_symbol": "GetAttacksEnergyCostBits",
    "before": "c |= FIRE_F;",
    "after": "c |= GRASS_F;",
    "case_ids": ["GetAttacksEnergyCostBits-1", "GetAttacksEnergyCostBits-2"],
}
# <<< factory-mutation GetAttacksEnergyCostBits
# >>> factory-mutation LoadDefendingPokemonColorWRAndPrizeCards
MUTATIONS["LoadDefendingPokemonColorWRAndPrizeCards"] = {
    "source_symbol": "LoadDefendingPokemonColorWRAndPrizeCards",
    "before": "wAIPlayerPrizeCount = CountPrizes();",
    "after": "wAIPlayerPrizeCount = 0u;",
    "case_ids": ["LoadDefendingPokemonColorWRAndPrizeCards-0", "LoadDefendingPokemonColorWRAndPrizeCards-1"],
}
# <<< factory-mutation LoadDefendingPokemonColorWRAndPrizeCards
# >>> factory-mutation LookForCardIDInLocation_Bank5
MUTATIONS["LookForCardIDInLocation_Bank5"] = {
    "source_symbol": "LookForCardIDInLocation_Bank5",
    "before": "(uint8_t)GetCardIDFromDeckIndex(index) == card_id",
    "after": "(uint8_t)GetCardIDFromDeckIndex(index) != card_id",
    "case_ids": ["LookForCardIDInLocation_Bank5-0", "LookForCardIDInLocation_Bank5-1"],
}
# <<< factory-mutation LookForCardIDInLocation_Bank5
# >>> factory-mutation PickRandomBenchPokemon
MUTATIONS["PickRandomBenchPokemon"] = {
    "source_symbol": "PickRandomBenchPokemon",
    "before": "Random((uint8_t)(count - 1u)) + 1u",
    "after": "Random((uint8_t)(count - 1u)) + 2u",
    "case_ids": ["PickRandomBenchPokemon-0", "PickRandomBenchPokemon-1"],
}
# <<< factory-mutation PickRandomBenchPokemon
# >>> factory-mutation RemoveCardIDInList
MUTATIONS["RemoveCardIDInList"] = {
    "source_symbol": "RemoveCardIDInList",
    "before": "(uint8_t)GetCardIDFromDeckIndex(index) != e",
    "after": "(uint8_t)GetCardIDFromDeckIndex(index) == e",
    "case_ids": ["RemoveCardIDInList-0", "RemoveCardIDInList-1"],
}
# <<< factory-mutation RemoveCardIDInList
# >>> factory-mutation SortTempHandByIDList
MUTATIONS["SortTempHandByIDList"] = {
    "source_symbol": "SortTempHandByIDList",
    "before": "if (b == 0u)",
    "after": "if (b != 0u)",
    "case_ids": ["SortTempHandByIDList-0", "SortTempHandByIDList-1"],
}
# <<< factory-mutation SortTempHandByIDList
# >>> factory-mutation ApplyCardCGBAttributes
MUTATIONS["ApplyCardCGBAttributes"] = {
    "source_symbol": "ApplyCardCGBAttributes",
    "before": "FillRectangle(0x80u, 8u, 6u, de, 0u);",
    "after": "FillRectangle(0x00u, 8u, 6u, de, 0u);",
    "case_ids": ["ApplyCardCGBAttributes-0", "ApplyCardCGBAttributes-1"],
}
# <<< factory-mutation ApplyCardCGBAttributes
# >>> factory-mutation ApplyStatusConditionToArenaPokemon
MUTATIONS["ApplyStatusConditionToArenaPokemon"] = {
    "source_symbol": "ApplyStatusConditionToArenaPokemon",
    "before": "\t*hl = (uint16_t)(p + 2u);",
    "after": "\t*hl = (uint16_t)(p + 1u);",
    "case_ids": ["ApplyStatusConditionToArenaPokemon-1", "ApplyStatusConditionToArenaPokemon-4"],
}
# <<< factory-mutation ApplyStatusConditionToArenaPokemon
# >>> factory-mutation CardPageSwitch_EnergyOrTrainerPage1
MUTATIONS["CardPageSwitch_EnergyOrTrainerPage1"] = {"source_symbol": "CardPageSwitch_EnergyOrTrainerPage1", "before": "return (CardPageSwitchEnergyResult){1u, 0u};", "after": "return (CardPageSwitchEnergyResult){2u, 0u};", "case_ids": ["CardPageSwitch_EnergyOrTrainerPage1-0", "CardPageSwitch_EnergyOrTrainerPage1-1"]}
# <<< factory-mutation CardPageSwitch_EnergyOrTrainerPage1
# >>> factory-mutation CardPageSwitch_TrainerEnd
MUTATIONS["CardPageSwitch_TrainerEnd"] = {"source_symbol": "CardPageSwitch_TrainerEnd", "before": "return (CardPageResult){CARDPAGE_TRAINER_1, TRUE};", "after": "return (CardPageResult){0x0eu, TRUE};", "case_ids": ["CardPageSwitch_TrainerEnd-0", "CardPageSwitch_TrainerEnd-1", "CardPageSwitch_TrainerEnd-2"]}
# <<< factory-mutation CardPageSwitch_TrainerEnd
# >>> factory-mutation CheckIfActiveCardParalyzedOrAsleep
MUTATIONS["CheckIfActiveCardParalyzedOrAsleep"] = {
    "source_symbol": "CheckIfActiveCardParalyzedOrAsleep",
    "before": "masked == 0x03u",
    "after": "masked == 0x04u",
    "case_ids": ["CheckIfActiveCardParalyzedOrAsleep-0", "CheckIfActiveCardParalyzedOrAsleep-1"],
}
# <<< factory-mutation CheckIfActiveCardParalyzedOrAsleep
# >>> factory-mutation CheckIfEnoughEnergiesOfType
MUTATIONS["CheckIfEnoughEnergiesOfType"] = {
    "source_symbol": "CheckIfEnoughEnergiesOfType",
    "before": "required == 0u || required <= attached",
    "after": "required == 0u || required < attached",
    "case_ids": ["CheckIfEnoughEnergiesOfType-0", "CheckIfEnoughEnergiesOfType-1"],
}
# <<< factory-mutation CheckIfEnoughEnergiesOfType
# >>> factory-mutation CheckIfEnoughEnergiesToRetreat
MUTATIONS["CheckIfEnoughEnergiesToRetreat"] = {
    "source_symbol": "CheckIfEnoughEnergiesToRetreat",
    "before": "attached < required",
    "after": "attached <= required",
    "case_ids": ["CheckIfEnoughEnergiesToRetreat-0", "CheckIfEnoughEnergiesToRetreat-1"],
}
# <<< factory-mutation CheckIfEnoughEnergiesToRetreat
# >>> factory-mutation DecideLinkDuelVariables
MUTATIONS["DecideLinkDuelVariables"] = {
    "source_symbol": "DecideLinkDuelVariables",
    "before": "ResetSerial();\n\t\t\treturn 0x90u;",
    "after": "return 0x00u;",
    "case_ids": ["DecideLinkDuelVariables-0", "DecideLinkDuelVariables-1"],
}
# <<< factory-mutation DecideLinkDuelVariables
# >>> factory-mutation DisplayAttackPage
MUTATIONS["DisplayAttackPage"] = {
    "source_symbol": "DisplayAttackPage",
    "before": "case 2u:\n\t\tSwitchAttackPage();",
    "after": "SwitchCardPage();",
    "case_ids": ["DisplayAttackPage-0", "DisplayAttackPage-1"],
}
# <<< factory-mutation DisplayAttackPage
# >>> factory-mutation DisplayCardPage
MUTATIONS["DisplayCardPage"] = {
    "source_symbol": "DisplayCardPage",
    "before": "void DisplayCardPage(void)\n{\n\tEnableLCD();",
    "after": "DisableLCD();",
    "case_ids": ["DisplayCardPage-0", "DisplayCardPage-1"],
}
# <<< factory-mutation DisplayCardPage
# >>> factory-mutation DoPracticeDuelAction
MUTATIONS["DoPracticeDuelAction"] = {
    "source_symbol": "DoPracticeDuelAction",
    "before": "if (wIsPracticeDuel == 0u)",
    "after": "if (wIsPracticeDuel != 0u)",
    "case_ids": ["DoPracticeDuelAction-0", "DoPracticeDuelAction-1"],
}
# <<< factory-mutation DoPracticeDuelAction
# >>> factory-mutation DrawDuelHorizontalSeparator
MUTATIONS["DrawDuelHorizontalSeparator"] = {
    "source_symbol": "DrawDuelHorizontalSeparator",
    "before": "WriteByteToBGMap0(0x31u, 9u, 4u);",
    "after": "WriteByteToBGMap0(0x32u, 9u, 4u);",
    "case_ids": ["DrawDuelHorizontalSeparator-0", "DrawDuelHorizontalSeparator-1"],
}
# <<< factory-mutation DrawDuelHorizontalSeparator
# >>> factory-mutation MoveAllTurnHolderKnockedOutPokemonToDiscardPile
MUTATIONS["MoveAllTurnHolderKnockedOutPokemonToDiscardPile"] = {
    "source_symbol": "MoveAllTurnHolderKnockedOutPokemonToDiscardPile",
    "before": "if (gb_read8(hp) == 0u)",
    "after": "if (gb_read8(hp) != 0u)",
    "case_ids": ["MoveAllTurnHolderKnockedOutPokemonToDiscardPile-0", "MoveAllTurnHolderKnockedOutPokemonToDiscardPile-1"],
}
# <<< factory-mutation MoveAllTurnHolderKnockedOutPokemonToDiscardPile
# >>> factory-mutation PracticeDuel_VerifyPlayerTurnActions
MUTATIONS["PracticeDuel_VerifyPlayerTurnActions"] = {"source_symbol": "PracticeDuel_VerifyPlayerTurnActions", "before": "card == 0x53u", "after": "card == 0x54u", "case_ids": ["PracticeDuel_VerifyPlayerTurnActions-0"]}
# <<< factory-mutation PracticeDuel_VerifyPlayerTurnActions
# >>> factory-mutation PrintCardNameFromCardIDInTextBox
MUTATIONS["PrintCardNameFromCardIDInTextBox"] = {
    "source_symbol": "PrintCardNameFromCardIDInTextBox",
    "before": "LoadTxRam2(name);",
    "after": "LoadTxRam2(0u);",
    "case_ids": ["PrintCardNameFromCardIDInTextBox-0", "PrintCardNameFromCardIDInTextBox-1"],
}
# <<< factory-mutation PrintCardNameFromCardIDInTextBox
# >>> factory-mutation PrintSortNumberInCardList
MUTATIONS["PrintSortNumberInCardList"] = {
    "source_symbol": "PrintSortNumberInCardList",
    "before": "value = (uint8_t)(value + SYM_0);",
    "after": "value = (uint8_t)(value + SYM_1);",
    "case_ids": ["PrintSortNumberInCardList-0", "PrintSortNumberInCardList-1"],
}
# <<< factory-mutation PrintSortNumberInCardList
# >>> factory-mutation PrintSortNumberInCardList_CallFromPointer
MUTATIONS["PrintSortNumberInCardList_CallFromPointer"] = {
    "source_symbol": "PrintSortNumberInCardList_CallFromPointer",
    "before": "PrintSortNumberInCardList();",
    "after": "return;",
    "case_ids": ["PrintSortNumberInCardList_CallFromPointer-0", "PrintSortNumberInCardList_CallFromPointer-1"],
}
# Keep schema-2 inventory after appended routine cases.
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# <<< factory-mutation PrintSortNumberInCardList_CallFromPointer# >>> factory-mutation PracticeDuel_VerifyInitialPlay
MUTATIONS["PracticeDuel_VerifyInitialPlay"] = {"source_symbol": "PracticeDuel_VerifyInitialPlay", "before": "count == 2u", "after": "count == 3u", "case_ids": ["PracticeDuel_VerifyInitialPlay-0"]}
# <<< factory-mutation PracticeDuel_VerifyInitialPlay
# >>> factory-mutation CheckIfNoSurplusEnergyForAttack
MUTATIONS["CheckIfNoSurplusEnergyForAttack"] = {
    "source_symbol": "CheckIfNoSurplusEnergyForAttack",
    "before": "\tif (a1 < b)\n\t\treturn (CheckIfNoSurplusEnergyResult){a2, f};",
    "after": "\tif (a1 <= b)\n\t\treturn (CheckIfNoSurplusEnergyResult){a2, f};",
    "case_ids": ["CheckIfNoSurplusEnergyForAttack-0", "CheckIfNoSurplusEnergyForAttack-3"],
}
# <<< factory-mutation CheckIfNoSurplusEnergyForAttack
# >>> factory-mutation Func_1585b
MUTATIONS["Func_1585b"] = {
    "source_symbol": "Func_1585b",
    "before": "return (Func1585bResult){ .a = 0, .f = 0x80u };",
    "after": "return (Func1585bResult){ .a = 0, .f = 0x00u };",
    "case_ids": ["Func_1585b-0", "Func_1585b-1", "Func_1585b-2", "Func_1585b-3", "Func_1585b-4", "Func_1585b-5", "Func_1585b-6"],
}
# <<< factory-mutation Func_1585b
# >>> factory-mutation CheckIfNotABossDeckID
MUTATIONS["CheckIfNotABossDeckID"] = {
    "source_symbol": "CheckIfNotABossDeckID",
    "before": "uint8_t a = gb_read8(sReceivedLegendaryCards_ADDR);",
    "after": "uint8_t a = gb_read8((uint16_t)(sReceivedLegendaryCards_ADDR + 1u));",
    "case_ids": ["CheckIfNotABossDeckID-1", "CheckIfNotABossDeckID-2", "CheckIfNotABossDeckID-3"],
}
# <<< factory-mutation CheckIfNotABossDeckID
# >>> factory-mutation AIChooseRandomlyNotToDoAction
MUTATIONS["AIChooseRandomlyNotToDoAction"] = {
	"source_symbol": "AIChooseRandomlyNotToDoAction",
	"before": "uint8_t cpflags = 0x40u;",
	"after": "uint8_t cpflags = 0x00u;",
	"case_ids": ["AIChooseRandomlyNotToDoAction-0", "AIChooseRandomlyNotToDoAction-1", "AIChooseRandomlyNotToDoAction-2", "AIChooseRandomlyNotToDoAction-3"],
}
# <<< factory-mutation AIChooseRandomlyNotToDoAction
# >>> factory-mutation TrySetUpBossStartingPlayArea
MUTATIONS["TrySetUpBossStartingPlayArea"] = {
	"source_symbol": "TrySetUpBossStartingPlayArea",
	"before": "return (TrySetUpBossStartingPlayAreaResult){r.a, r.f};",
	"after": "return (TrySetUpBossStartingPlayAreaResult){r.a, 0x00u};",
	"case_ids": ["TrySetUpBossStartingPlayArea-0", "TrySetUpBossStartingPlayArea-1", "TrySetUpBossStartingPlayArea-2", "TrySetUpBossStartingPlayArea-3", "TrySetUpBossStartingPlayArea-4"],
}
# <<< factory-mutation TrySetUpBossStartingPlayArea
# >>> factory-mutation CardPageSwitch_TrainerPage2
MUTATIONS["CardPageSwitch_TrainerPage2"] = {"source_symbol": "CardPageSwitch_TrainerPage2", "before": "return (TrainerPageResult){hl, r.a, r.zero};", "after": "return (TrainerPageResult){hl, r.a, (uint8_t)!r.zero};", "case_ids": ["CardPageSwitch_TrainerPage2-0", "CardPageSwitch_TrainerPage2-1", "CardPageSwitch_TrainerPage2-2"]}
# <<< factory-mutation CardPageSwitch_TrainerPage2
# >>> factory-mutation LoadAndValidateDuelSaveData
MUTATIONS["LoadAndValidateDuelSaveData"] = {"source_symbol": "LoadAndValidateDuelSaveData", "before": "if (duel.f & 0x10u)", "after": "if (!(duel.f & 0x10u))", "case_ids": ["LoadAndValidateDuelSaveData-0", "LoadAndValidateDuelSaveData-1", "LoadAndValidateDuelSaveData-2"]}
# <<< factory-mutation LoadAndValidateDuelSaveData
# >>> factory-mutation ValidateSavedNonLinkDuelData
MUTATIONS["ValidateSavedNonLinkDuelData"] = {"source_symbol": "ValidateSavedNonLinkDuelData", "before": "if (duel_type != DUELTYPE_LINK)", "after": "if (duel_type == DUELTYPE_LINK)", "case_ids": ["ValidateSavedNonLinkDuelData-0", "ValidateSavedNonLinkDuelData-1", "ValidateSavedNonLinkDuelData-2"]}
# <<< factory-mutation ValidateSavedNonLinkDuelData
# >>> factory-mutation SetupPlayAreaScreen
MUTATIONS["SetupPlayAreaScreen"] = {"source_symbol": "SetupPlayAreaScreen", "before": "if (wDuelDisplayedScreen == PLAY_AREA_CARD_LIST)", "after": "if (wDuelDisplayedScreen != PLAY_AREA_CARD_LIST)", "case_ids": ["SetupPlayAreaScreen-1", "SetupPlayAreaScreen-2"]}
# <<< factory-mutation SetupPlayAreaScreen
# >>> factory-mutation CheckIfEnoughEnergiesForGivenAttack
MUTATIONS["CheckIfEnoughEnergiesForGivenAttack"] = {"source_symbol": "CheckIfEnoughEnergiesForGivenAttack", "before": "if (category == 0x04u) {", "after": "if (category != 0x04u) {", "case_ids": ["CheckIfEnoughEnergiesForGivenAttack-0", "CheckIfEnoughEnergiesForGivenAttack-1"]}
# <<< factory-mutation CheckIfEnoughEnergiesForGivenAttack
# >>> factory-mutation SaveDuelData
MUTATIONS["SaveDuelData"] = {"source_symbol": "SaveDuelData", "before": "SaveDuelDataToDE(sCurrentDuel_ADDR);", "after": "SaveDuelDataToDE((uint16_t)(sCurrentDuel_ADDR + 1u));", "case_ids": ["SaveDuelData-1"]}
# <<< factory-mutation SaveDuelData
# >>> factory-mutation SetCardListHeaderText
MUTATIONS["SetCardListHeaderText"] = {"source_symbol": "SetCardListHeaderText", "before": "wCardListHeaderText_PTR[1] = (uint8_t)(de >> 8);", "after": "wCardListHeaderText_PTR[1] = (uint8_t)de;", "case_ids": ["SetCardListHeaderText-0", "SetCardListHeaderText-1", "SetCardListHeaderText-2"]}
# <<< factory-mutation SetCardListHeaderText
# >>> factory-mutation AIAttachEnergyInHandToCardInPlayArea
MUTATIONS["AIAttachEnergyInHandToCardInPlayArea"] = {
    "source_symbol": "AIAttachEnergyInHandToCardInPlayArea",
    "before": "if ((hand.f & 0x10u) == 0u)",
    "after": "if ((hand.f & 0x10u) != 0u)",
    "case_ids": ["AIAttachEnergyInHandToCardInPlayArea-0"],
}
# <<< factory-mutation AIAttachEnergyInHandToCardInPlayArea
# >>> factory-mutation GoToPreviousCardPage
MUTATIONS["GoToPreviousCardPage"] = {
    "source_symbol": "GoToPreviousCardPage",
    "before": "uint8_t page = (uint8_t)(wCardPageNumber - 1u);",
    "after": "uint8_t page = (uint8_t)(wCardPageNumber - 2u);",
    "case_ids": ["GoToPreviousCardPage-0", "GoToPreviousCardPage-1"],
}
# <<< factory-mutation GoToPreviousCardPage
# >>> factory-mutation DrawWholeScreenTextBox
MUTATIONS["DrawWholeScreenTextBox"] = {
    "source_symbol": "DrawWholeScreenTextBox",
    "before": "DrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);",
    "after": "DrawRegularTextBox(&box, 0u, 20u, 17u, 0u, 0u);",
    "case_ids": ["DrawWholeScreenTextBox-0", "DrawWholeScreenTextBox-1"],
}
# <<< factory-mutation DrawWholeScreenTextBox
# >>> factory-mutation HasAlivePokemonInPlayArea
MUTATIONS["HasAlivePokemonInPlayArea"] = {
    "source_symbol": "HasAlivePokemonInPlayArea",
    "before": "return _HasAlivePokemonInPlayArea(0u);",
    "after": "return _HasAlivePokemonInPlayArea(1u);",
    "case_ids": ["HasAlivePokemonInPlayArea-0", "HasAlivePokemonInPlayArea-1"],
}
# <<< factory-mutation HasAlivePokemonInPlayArea
# >>> factory-mutation CardPageSwitch_PokemonAttack1Page1
MUTATIONS["CardPageSwitch_PokemonAttack1Page1"] = {"source_symbol": "CardPageSwitch_PokemonAttack1Page1", "before": "\tuint16_t hl = wLoadedCard1Atk1Name_ADDR;", "after": "\tuint16_t hl = wLoadedCard1Atk1Description_ADDR;", "case_ids": ["CardPageSwitch_PokemonAttack1Page1-0", "CardPageSwitch_PokemonAttack1Page1-1", "CardPageSwitch_PokemonAttack1Page1-2", "CardPageSwitch_PokemonAttack1Page1-3", "CardPageSwitch_PokemonAttack1Page1-4"]}
# <<< factory-mutation CardPageSwitch_PokemonAttack1Page1
# >>> factory-mutation CheckPrintDoublePoisoned
MUTATIONS["CheckPrintDoublePoisoned"] = {"source_symbol": "CheckPrintDoublePoisoned", "before": "printed_status = POISONED;", "after": "printed_status = 0u;", "case_ids": ["CheckPrintDoublePoisoned-1", "CheckPrintDoublePoisoned-3"]}
# <<< factory-mutation CheckPrintDoublePoisoned
# >>> factory-mutation PrintPracticeDuelLetsPlayTheGame
MUTATIONS["PrintPracticeDuelLetsPlayTheGame"] = {
    "source_symbol": "PrintPracticeDuelLetsPlayTheGame",
    "before": "\t(void)PrintPracticeDuelDrMasonInstructions(LetsPlayTheGamePracticeDuelText);",
    "after": "\t(void)PrintPracticeDuelDrMasonInstructions(LetsPlayTheGamePracticeDuelText + 1u);",
    "case_ids": ["PrintPracticeDuelLetsPlayTheGame-0", "PrintPracticeDuelLetsPlayTheGame-1"],
}
# <<< factory-mutation PrintPracticeDuelLetsPlayTheGame
# >>> factory-mutation AIAttachEnergyInHandToCardInBench
MUTATIONS["AIAttachEnergyInHandToCardInBench"] = {
	"source_symbol": "AIAttachEnergyInHandToCardInBench",
	"before": "return (AIAttachEnergyInHandToCardInBenchResult){hand.a, hand.f};",
	"after": "return (AIAttachEnergyInHandToCardInBenchResult){(uint8_t)(hand.a ^ 1u), hand.f};",
	"case_ids": ["AIAttachEnergyInHandToCardInBench-0"],
}
# <<< factory-mutation AIAttachEnergyInHandToCardInBench
# >>> factory-mutation DrawPracticeDuelInstructionsTextBox
MUTATIONS["DrawPracticeDuelInstructionsTextBox"] = {
    "source_symbol": "DrawPracticeDuelInstructionsTextBox",
    "before": "\tDrawRegularTextBox(&box, 0u, 20u, 12u, 0u, 0u);",
    "after": "\tDrawRegularTextBox(&box, 0u, 20u, 11u, 0u, 0u);",
    "case_ids": ["DrawPracticeDuelInstructionsTextBox-0", "DrawPracticeDuelInstructionsTextBox-1"],
}
# <<< factory-mutation DrawPracticeDuelInstructionsTextBox
# >>> factory-mutation PracticeDuelVerify_Turn7Or8
MUTATIONS["PracticeDuelVerify_Turn7Or8"] = {"source_symbol": "PracticeDuelVerify_Turn7Or8", "before": "card != STARMIE", "after": "card != 0x57u", "case_ids": ["PracticeDuelVerify_Turn7Or8-0", "PracticeDuelVerify_Turn7Or8-1", "PracticeDuelVerify_Turn7Or8-2"]}
# <<< factory-mutation PracticeDuelVerify_Turn7Or8
# >>> factory-mutation SetDiscardPileScreenTexts
MUTATIONS["SetDiscardPileScreenTexts"] = {"source_symbol": "SetDiscardPileScreenTexts", "before": "\tSetCardListHeaderText(de, ChooseTheCardYouWishToExamineText);", "after": "\tSetCardListHeaderText(de, YourDiscardPileText);", "case_ids": ["SetDiscardPileScreenTexts-0", "SetDiscardPileScreenTexts-1", "SetDiscardPileScreenTexts-2"]}
# <<< factory-mutation SetDiscardPileScreenTexts
# >>> factory-mutation PrintAttachedEnergyToPokemon
MUTATIONS["PrintAttachedEnergyToPokemon"] = {"source_symbol": "PrintAttachedEnergyToPokemon", "before": "\t(void)DrawWideTextBox_WaitForInput(AttachedEnergyToPokemonText);", "after": "\t(void)DrawWideTextBox_WaitForInput(0x0060u);", "case_ids": ["PrintAttachedEnergyToPokemon-0", "PrintAttachedEnergyToPokemon-1"]}
# <<< factory-mutation PrintAttachedEnergyToPokemon
# >>> factory-mutation PrintPokemonEvolvedIntoPokemon
MUTATIONS["PrintPokemonEvolvedIntoPokemon"] = {"source_symbol": "PrintPokemonEvolvedIntoPokemon", "before": "\t(void)DrawWideTextBox_WaitForInput(PokemonEvolvedIntoPokemonText);", "after": "\t(void)DrawWideTextBox_WaitForInput(0x0061u);", "case_ids": ["PrintPokemonEvolvedIntoPokemon-0", "PrintPokemonEvolvedIntoPokemon-1"]}
# <<< factory-mutation PrintPokemonEvolvedIntoPokemon
# >>> factory-mutation SetupDuel
MUTATIONS["SetupDuel"] = {
    "source_symbol": "SetupDuel",
    "before": "\twTileMapFill = SYM_SPACE;",
    "after": "\twTileMapFill = 0x01u;",
    "case_ids": ["SetupDuel-0", "SetupDuel-1"],
}
# <<< factory-mutation SetupDuel
# >>> factory-mutation PracticeDuelVerify_Turn6
MUTATIONS["PracticeDuelVerify_Turn6"] = {"source_symbol": "PracticeDuelVerify_Turn6", "before": "if (wAttachedEnergies_PTR[WATER] != 3u)", "after": "if (wAttachedEnergies_PTR[WATER] == 3u)", "case_ids": ["PracticeDuelVerify_Turn6-0", "PracticeDuelVerify_Turn6-1", "PracticeDuelVerify_Turn6-2"]}
# <<< factory-mutation PracticeDuelVerify_Turn6
# >>> factory-mutation PracticeDuelVerify_Turn4
MUTATIONS["PracticeDuelVerify_Turn4"] = {"source_symbol": "PracticeDuelVerify_Turn4", "before": "if (gb_read8(wPlayerNumberOfPokemonInPlayArea_ADDR) != 3u)", "after": "if (gb_read8(wPlayerNumberOfPokemonInPlayArea_ADDR) == 3u)", "case_ids": ["PracticeDuelVerify_Turn4-0", "PracticeDuelVerify_Turn4-1", "PracticeDuelVerify_Turn4-2", "PracticeDuelVerify_Turn4-3", "PracticeDuelVerify_Turn4-4"]}
# <<< factory-mutation PracticeDuelVerify_Turn4
# >>> factory-mutation ShuffleDeckAndDrawSevenCards
MUTATIONS["ShuffleDeckAndDrawSevenCards"] = {"source_symbol": "ShuffleDeckAndDrawSevenCards", "before": "if (basic.a != 0u)", "after": "if (basic.a == 0u)", "case_ids": ["ShuffleDeckAndDrawSevenCards-0", "ShuffleDeckAndDrawSevenCards-1"]}
# <<< factory-mutation ShuffleDeckAndDrawSevenCards
# >>> factory-mutation WriteTwoDigitNumberInTxSymbol_PadSpace
MUTATIONS["WriteTwoDigitNumberInTxSymbol_PadSpace"] = {
    "source_symbol": "WriteTwoDigitNumberInTxSymbol_PadSpace",
    "before": "SafeCopyDataHLtoDE(&src, &dst, 2u);",
    "after": "SafeCopyDataHLtoDE(&src, &dst, 3u);",
    "case_ids": ["WriteTwoDigitNumberInTxSymbol_PadSpace-0", "WriteTwoDigitNumberInTxSymbol_PadSpace-1", "WriteTwoDigitNumberInTxSymbol_PadSpace-2"],
}
# <<< factory-mutation WriteTwoDigitNumberInTxSymbol_PadSpace
# >>> factory-mutation PrintOpponentNumberOfHandAndDeckCards
MUTATIONS["PrintOpponentNumberOfHandAndDeckCards"] = {"source_symbol": "PrintOpponentNumberOfHandAndDeckCards", "before": "uint8_t deck = (uint8_t)(DECK_SIZE - wOpponentNumberOfCardsNotInDeck - wNumCardsBeingDrawn);", "after": "uint8_t deck = (uint8_t)(DECK_SIZE - wOpponentNumberOfCardsNotInDeck + wNumCardsBeingDrawn);", "case_ids": ["PrintOpponentNumberOfHandAndDeckCards-0", "PrintOpponentNumberOfHandAndDeckCards-1", "PrintOpponentNumberOfHandAndDeckCards-2"]}
# <<< factory-mutation PrintOpponentNumberOfHandAndDeckCards
# >>> factory-mutation PrintPlayerNumberOfHandAndDeckCards
MUTATIONS["PrintPlayerNumberOfHandAndDeckCards"] = {"source_symbol": "PrintPlayerNumberOfHandAndDeckCards", "before": "uint8_t deck = (uint8_t)(DECK_SIZE - wPlayerNumberOfCardsNotInDeck - wNumCardsBeingDrawn);", "after": "uint8_t deck = (uint8_t)(DECK_SIZE - wPlayerNumberOfCardsNotInDeck + wNumCardsBeingDrawn);", "case_ids": ["PrintPlayerNumberOfHandAndDeckCards-0", "PrintPlayerNumberOfHandAndDeckCards-1", "PrintPlayerNumberOfHandAndDeckCards-2"]}
# <<< factory-mutation PrintPlayerNumberOfHandAndDeckCards
# >>> factory-mutation PrintDuelResultStats
MUTATIONS["PrintDuelResultStats"] = {"source_symbol": "PrintDuelResultStats", "before": "\t\tuint8_t cards = (uint8_t)(DECK_SIZE - gb_read8(cards_var.hl));", "after": "\t\tuint8_t cards = (uint8_t)(DECK_SIZE - gb_read8(cards_var.hl) + 1u);", "case_ids": ["PrintDuelResultStats-0", "PrintDuelResultStats-1", "PrintDuelResultStats-2"]}
# <<< factory-mutation PrintDuelResultStats
# >>> factory-mutation ConvertColorToEnergyCardID
MUTATIONS["ConvertColorToEnergyCardID"] = {"source_symbol": "ConvertColorToEnergyCardID", "before": "\treturn result;", "after": "\treturn (uint8_t)(result ^ 1u);", "case_ids": ["ConvertColorToEnergyCardID-0", "ConvertColorToEnergyCardID-1"]}
# <<< factory-mutation ConvertColorToEnergyCardID
# >>> factory-mutation WriteOneByteNumberInTxSymbol_PadSpace
MUTATIONS["WriteOneByteNumberInTxSymbol_PadSpace"] = {
    "source_symbol": "WriteOneByteNumberInTxSymbol_PadSpace",
    "before": "SafeCopyDataHLtoDE(&src, &dst, 3u);",
    "after": "SafeCopyDataHLtoDE(&src, &dst, 4u);",
    "case_ids": ["WriteOneByteNumberInTxSymbol_PadSpace-0", "WriteOneByteNumberInTxSymbol_PadSpace-1", "WriteOneByteNumberInTxSymbol_PadSpace-2"],
}
# <<< factory-mutation WriteOneByteNumberInTxSymbol_PadSpace
# >>> factory-mutation PrintPracticeDuelNumberedInstruction
MUTATIONS["PrintPracticeDuelNumberedInstruction"] = {
    "source_symbol": "PrintPracticeDuelNumberedInstruction",
    "before": "uint8_t c = gb_read8((uint16_t)(hl + 2u));",
    "after": "uint8_t c = gb_read8((uint16_t)(hl + 3u));",
    "case_ids": ["PrintPracticeDuelNumberedInstruction-0", "PrintPracticeDuelNumberedInstruction-1", "PrintPracticeDuelNumberedInstruction-2"],
}
# <<< factory-mutation PrintPracticeDuelNumberedInstruction
# >>> factory-mutation PrintNextPracticeDuelInstruction
MUTATIONS["PrintNextPracticeDuelInstruction"] = {"source_symbol": "PrintNextPracticeDuelInstruction", "before": "gb_write8(hffb0_ADDR, 0u);", "after": "gb_write8(hffb0_ADDR, 1u);", "case_ids": ["PrintNextPracticeDuelInstruction-0", "PrintNextPracticeDuelInstruction-1"]}
# <<< factory-mutation PrintNextPracticeDuelInstruction
# >>> factory-mutation GoToFirstOrNextCardPage
MUTATIONS["GoToFirstOrNextCardPage"] = {"source_symbol": "GoToFirstOrNextCardPage", "before": "\t\twCardPageNumber = initial_page;", "after": "\t\twCardPageNumber = CARDPAGE_POKEMON_OVERVIEW;", "case_ids": ["GoToFirstOrNextCardPage-0", "GoToFirstOrNextCardPage-1", "GoToFirstOrNextCardPage-2", "GoToFirstOrNextCardPage-3"]}
# <<< factory-mutation GoToFirstOrNextCardPage
# >>> factory-mutation PrintPracticeDuelInstructions
MUTATIONS["PrintPracticeDuelInstructions"] = {
    "source_symbol": "PrintPracticeDuelInstructions",
    "before": "\tgb_write8(wPracticeDuelTextPointer_ADDR, (uint8_t)hl);",
    "after": "\tgb_write8(wPracticeDuelTextPointer_ADDR, (uint8_t)(hl + 1u));",
    "case_ids": ["PrintPracticeDuelInstructions-0", "PrintPracticeDuelInstructions-1"],
}
# <<< factory-mutation PrintPracticeDuelInstructions
# >>> factory-mutation DisplayPreviousCardPage
MUTATIONS["DisplayPreviousCardPage"] = {"source_symbol": "DisplayPreviousCardPage", "before": "\tif ((navigation.f & 0x10u) == 0u)", "after": "\tif ((navigation.f & 0x10u) != 0u)", "case_ids": ["DisplayPreviousCardPage-0", "DisplayPreviousCardPage-1"]}
# <<< factory-mutation DisplayPreviousCardPage
# >>> factory-mutation PrintNumberOfHandAndDeckCards
MUTATIONS["PrintNumberOfHandAndDeckCards"] = {"source_symbol": "PrintNumberOfHandAndDeckCards", "before": "\tif (hWhoseTurn != PLAYER_TURN) {", "after": "\tif (hWhoseTurn == PLAYER_TURN) {", "case_ids": ["PrintNumberOfHandAndDeckCards-0", "PrintNumberOfHandAndDeckCards-1", "PrintNumberOfHandAndDeckCards-2"]}
# <<< factory-mutation PrintNumberOfHandAndDeckCards
# >>> factory-mutation PrintReturnCardsToDeckDrawAgain
MUTATIONS["PrintReturnCardsToDeckDrawAgain"] = {"source_symbol": "PrintReturnCardsToDeckDrawAgain", "before": "\tExchangeRNGResult x = ExchangeRNG(0x12u, 0x11u, 0x1211u, 0xCD12u);", "after": "\tExchangeRNGResult x = ExchangeRNG(0x12u, 0x11u, 0x1211u, 0xCD13u);", "case_ids": ["PrintReturnCardsToDeckDrawAgain-0", "PrintReturnCardsToDeckDrawAgain-1"]}
# <<< factory-mutation PrintReturnCardsToDeckDrawAgain
# >>> factory-mutation PracticeDuelVerify_Turn3
MUTATIONS["PracticeDuelVerify_Turn3"] = {"source_symbol": "PracticeDuelVerify_Turn3", "before": "\tif (a != SEAKING) {", "after": "\tif (a != (uint8_t)(SEAKING + 1u)) {", "case_ids": ["PracticeDuelVerify_Turn3-0", "PracticeDuelVerify_Turn3-1"]}
# <<< factory-mutation PracticeDuelVerify_Turn3
# >>> factory-mutation CheckIfEnoughEnergiesToAttack
MUTATIONS["CheckIfEnoughEnergiesToAttack"] = {"source_symbol": "CheckIfEnoughEnergiesToAttack", "before": "\tuint8_t doubled = (uint8_t)(menu_item * 2u);", "after": "\tuint8_t doubled = menu_item;", "case_ids": ["CheckIfEnoughEnergiesToAttack-1"]}
# <<< factory-mutation CheckIfEnoughEnergiesToAttack
# >>> factory-mutation PlayTurnDuelistDrawAnimation
MUTATIONS["PlayTurnDuelistDrawAnimation"] = {"source_symbol": "PlayTurnDuelistDrawAnimation", "before": "\tuint8_t e = (hWhoseTurn == PLAYER_TURN) ? DUEL_ANIM_PLAYER_DRAW : DUEL_ANIM_OPP_DRAW;", "after": "\tuint8_t e = (hWhoseTurn != PLAYER_TURN) ? DUEL_ANIM_PLAYER_DRAW : DUEL_ANIM_OPP_DRAW;", "case_ids": ["PlayTurnDuelistDrawAnimation-0", "PlayTurnDuelistDrawAnimation-2"]}
# <<< factory-mutation PlayTurnDuelistDrawAnimation
# >>> factory-mutation DrawCardPageSet2AndRarityIcons
MUTATIONS["DrawCardPageSet2AndRarityIcons"] = {"source_symbol": "DrawCardPageSet2AndRarityIcons", "before": "\tif (rarity != PROMOSTAR) {", "after": "\tif (rarity == PROMOSTAR) {", "case_ids": ["DrawCardPageSet2AndRarityIcons-0", "DrawCardPageSet2AndRarityIcons-2"]}
# <<< factory-mutation DrawCardPageSet2AndRarityIcons
# >>> factory-mutation CountOppEnergyCardsInHandAndAttached
MUTATIONS["CountOppEnergyCardsInHandAndAttached"] = {"source_symbol": "CountOppEnergyCardsInHandAndAttached", "before": "\tif (!(listed.f & 0x10u)) {", "after": "\tif ((listed.f & 0x10u)) {", "case_ids": ["CountOppEnergyCardsInHandAndAttached-0"]}
# <<< factory-mutation CountOppEnergyCardsInHandAndAttached
# >>> factory-mutation AIPickPrizeCards
MUTATIONS["AIPickPrizeCards"] = {"source_symbol": "AIPickPrizeCards", "before": "gb_write8(hl, (uint8_t)(gb_read8(hl) & (uint8_t)~bit));", "after": "gb_write8(hl, (uint8_t)(gb_read8(hl) | bit));", "case_ids": ["AIPickPrizeCards-0", "AIPickPrizeCards-1"]}
# <<< factory-mutation AIPickPrizeCards
# >>> factory-mutation HandleAIEnergyScoringForRepeatedBenchPokemon
MUTATIONS["HandleAIEnergyScoringForRepeatedBenchPokemon"] = {
    "source_symbol": "HandleAIEnergyScoringForRepeatedBenchPokemon",
    "before": "return (HandleAIEnergyScoringForRepeatedBenchPokemonResult){0xFFu, 0xC0u};",
    "after": "return (HandleAIEnergyScoringForRepeatedBenchPokemonResult){0xFFu, 0x00u};",
    "case_ids": ["HandleAIEnergyScoringForRepeatedBenchPokemon-0"],
}
# <<< factory-mutation HandleAIEnergyScoringForRepeatedBenchPokemon
# >>> factory-mutation CheckPrintCnfSlpPrz
MUTATIONS["CheckPrintCnfSlpPrz"] = {"source_symbol": "CheckPrintCnfSlpPrz", "before": "\tstatic const uint8_t status_symbols[4] = {SYM_SPACE, SYM_CONFUSED, SYM_ASLEEP, SYM_PARALYZED};", "after": "\tstatic const uint8_t status_symbols[4] = {SYM_SPACE, SYM_PARALYZED, SYM_ASLEEP, SYM_CONFUSED};", "case_ids": ["CheckPrintCnfSlpPrz-1"]}
# <<< factory-mutation CheckPrintCnfSlpPrz
# >>> factory-mutation LoadAnimCoordsAndFlags
MUTATIONS["LoadAnimCoordsAndFlags"] = {"source_symbol": "LoadAnimCoordsAndFlags", "before": "gb_write8(hl, attr);", "after": "gb_write8(hl, (uint8_t)(attr ^ 0xFFu));", "case_ids": ["LoadAnimCoordsAndFlags-0", "LoadAnimCoordsAndFlags-1"]}
# <<< factory-mutation LoadAnimCoordsAndFlags
# >>> factory-mutation PrintUsedTrainerCardDescription
MUTATIONS["PrintUsedTrainerCardDescription"] = {"source_symbol": "PrintUsedTrainerCardDescription", "before": "InitTextPrinting(1u, 1u);", "after": "InitTextPrinting(2u, 1u);", "case_ids": ["PrintUsedTrainerCardDescription-0", "PrintUsedTrainerCardDescription-1"]}
# <<< factory-mutation PrintUsedTrainerCardDescription
# >>> factory-mutation PracticeDuelVerify_Turn5
MUTATIONS["PracticeDuelVerify_Turn5"] = {"source_symbol": "PracticeDuelVerify_Turn5", "before": "if (gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER)) != 2u)", "after": "if (gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER)) != 3u)", "case_ids": ["PracticeDuelVerify_Turn5-0"]}
# <<< factory-mutation PracticeDuelVerify_Turn5
# >>> factory-mutation PracticeDuelVerify_Turn1
MUTATIONS["PracticeDuelVerify_Turn1"] = {"source_symbol": "PracticeDuelVerify_Turn1", "before": "if (a != GOLDEEN)", "after": "if (a == GOLDEEN)", "case_ids": ["PracticeDuelVerify_Turn1-0", "PracticeDuelVerify_Turn1-1"]}
# <<< factory-mutation PracticeDuelVerify_Turn1
# >>> factory-mutation PracticeDuelVerify_Turn2
MUTATIONS["PracticeDuelVerify_Turn2"] = {"source_symbol": "PracticeDuelVerify_Turn2", "before": "if (psychic == 0u)", "after": "if (psychic != 0u)", "case_ids": ["PracticeDuelVerify_Turn2-0", "PracticeDuelVerify_Turn2-3"]}
# <<< factory-mutation PracticeDuelVerify_Turn2
# >>> factory-mutation PracticeDuel_PlayStaryuFromBench
MUTATIONS["PracticeDuel_PlayStaryuFromBench"] = {"source_symbol": "PracticeDuel_PlayStaryuFromBench", "before": "(uint8_t)(turns == 0u ? 0x80u : 0x00u)", "after": "(uint8_t)(turns == 0u ? 0x00u : 0x80u)", "case_ids": ["PracticeDuel_PlayStaryuFromBench-0", "PracticeDuel_PlayStaryuFromBench-1"]}
# <<< factory-mutation PracticeDuel_PlayStaryuFromBench
# >>> factory-mutation DisplayDuelistTurnScreen
MUTATIONS["DisplayDuelistTurnScreen"] = {"source_symbol": "DisplayDuelistTurnScreen", "before": "if (turn != PLAYER_TURN)", "after": "if (turn == PLAYER_TURN)", "case_ids": ["DisplayDuelistTurnScreen-0", "DisplayDuelistTurnScreen-1"]}
# <<< factory-mutation DisplayDuelistTurnScreen
# >>> factory-mutation DrawDuelistPortraitsAndNames
MUTATIONS["DrawDuelistPortraitsAndNames"] = {"source_symbol": "DrawDuelistPortraitsAndNames", "before": "DrawOpponentPortrait(wOpponentPortrait);", "after": "DrawOpponentPortrait(0);", "case_ids": ["DrawDuelistPortraitsAndNames-0", "DrawDuelistPortraitsAndNames-1"]}
# <<< factory-mutation DrawDuelistPortraitsAndNames
# >>> factory-mutation CheckEnergyNeededForAttack
MUTATIONS["CheckEnergyNeededForAttack"] = {"source_symbol": "CheckEnergyNeededForAttack", "before": "uint8_t e = wSelectedAttack;\n\t(void)CopyAttackDataAndDamage_FromDeckIndex(d, e);", "after": "uint8_t e = (uint8_t)(wSelectedAttack + 1u);\n\t(void)CopyAttackDataAndDamage_FromDeckIndex(d, e);", "case_ids": ["CheckEnergyNeededForAttack-0"]}
# <<< factory-mutation CheckEnergyNeededForAttack
# >>> factory-mutation CreateDamageCharSprite
MUTATIONS["CreateDamageCharSprite"] = {"source_symbol": "CreateDamageCharSprite", "before": "gb_write8(de, wWhichSprite);", "after": "gb_write8(de, (uint8_t)(wWhichSprite + 1u));", "case_ids": ["CreateDamageCharSprite-0"]}
# <<< factory-mutation CreateDamageCharSprite
# >>> factory-mutation HasAlivePokemonInBench
MUTATIONS["HasAlivePokemonInBench"] = {"source_symbol": "HasAlivePokemonInBench", "before": "return _HasAlivePokemonInPlayArea(1u);", "after": "return _HasAlivePokemonInPlayArea(2u);", "case_ids": ["HasAlivePokemonInBench-0", "HasAlivePokemonInBench-1"]}
# <<< factory-mutation HasAlivePokemonInBench
# >>> factory-mutation DrawOpponentSelectionScreen
MUTATIONS["DrawOpponentSelectionScreen"] = {"source_symbol": "DrawOpponentSelectionScreen", "before": "WriteOneByteNumberInTxSymbol_PadSpace(deck_id2, 5u, 16u, 0u, 0u, 0u);", "after": "WriteOneByteNumberInTxSymbol_PadSpace(deck_id2, 6u, 16u, 0u, 0u, 0u);", "case_ids": ["DrawOpponentSelectionScreen-0"]}
# <<< factory-mutation DrawOpponentSelectionScreen
# >>> factory-mutation PracticeDuel_ReplaceKnockedOutPokemon
MUTATIONS["PracticeDuel_ReplaceKnockedOutPokemon"] = {"source_symbol": "PracticeDuel_ReplaceKnockedOutPokemon", "before": "PrintPracticeDuelDrMasonInstructions(SelectStaryuPracticeDuelText);", "after": "PrintPracticeDuelDrMasonInstructions((uint16_t)(SelectStaryuPracticeDuelText + 1u));", "case_ids": ["PracticeDuel_ReplaceKnockedOutPokemon-1"]}
# <<< factory-mutation PracticeDuel_ReplaceKnockedOutPokemon
# >>> factory-mutation DrawDamageAnimationArrow
MUTATIONS["DrawDamageAnimationArrow"] = {"source_symbol": "DrawDamageAnimationArrow", "before": "gb_write8(wDamageCharIndex_ADDR, 5u);", "after": "gb_write8(wDamageCharIndex_ADDR, 4u);", "case_ids": ["DrawDamageAnimationArrow-0", "DrawDamageAnimationArrow-1"]}
# <<< factory-mutation DrawDamageAnimationArrow
# >>> factory-mutation DrawDamageAnimationWeak
MUTATIONS["DrawDamageAnimationWeak"] = {"source_symbol": "DrawDamageAnimationWeak", "before": "wDamageCharIndex = 3u;", "after": "wDamageCharIndex = 4u;", "case_ids": ["DrawDamageAnimationWeak-0", "DrawDamageAnimationWeak-1"]}
# <<< factory-mutation DrawDamageAnimationWeak
# >>> factory-mutation DrawDamageAnimationResist
MUTATIONS["DrawDamageAnimationResist"] = {"source_symbol": "DrawDamageAnimationResist", "before": "wDamageCharAnimDelay = (uint8_t)(wDamageCharAnimDelay + 18u);", "after": "wDamageCharAnimDelay = (uint8_t)(wDamageCharAnimDelay + 19u);", "case_ids": ["DrawDamageAnimationResist-0", "DrawDamageAnimationResist-1"]}
# <<< factory-mutation DrawDamageAnimationResist
# >>> factory-mutation DrawDamageAnimationNumbers
MUTATIONS["DrawDamageAnimationNumbers"] = {"source_symbol": "DrawDamageAnimationNumbers", "before": "wDamageCharIndex = (uint8_t)(wDamageCharIndex + 1u);", "after": "wDamageCharIndex = (uint8_t)(wDamageCharIndex + 2u);", "case_ids": ["DrawDamageAnimationNumbers-0", "DrawDamageAnimationNumbers-1"]}
# <<< factory-mutation DrawDamageAnimationNumbers
# >>> factory-mutation Func_15886
MUTATIONS["Func_15886"] = {"source_symbol": "Func_15886", "before": "\tif (check.f & 0x10u) {", "after": "\tif (check.f & 0x20u) {", "case_ids": ["Func_15886-0", "Func_15886-1"]}
# <<< factory-mutation Func_15886
# >>> factory-mutation CheckAbleToRetreat
MUTATIONS["CheckAbleToRetreat"] = {"source_symbol": "CheckAbleToRetreat", "before": "\tif (r1.f & 0x10u) {", "after": "\tif (r1.f & 0x20u) {", "case_ids": ["CheckAbleToRetreat-0", "CheckAbleToRetreat-1"]}
# <<< factory-mutation CheckAbleToRetreat
# >>> factory-mutation LookForEnergyNeededInHand
MUTATIONS["LookForEnergyNeededInHand"] = {"source_symbol": "LookForEnergyNeededInHand", "before": "\t}\n\treturn 0x80u;\n}", "after": "\t}\n\treturn 0x00u;\n}", "case_ids": ["LookForEnergyNeededInHand-0", "LookForEnergyNeededInHand-1"]}
# <<< factory-mutation LookForEnergyNeededInHand
# >>> factory-mutation Func_7364
MUTATIONS["Func_7364"] = {"source_symbol": "Func_7364", "before": "\t\tif (b & (1u << B_PAD_B)) {\n\t\t\treturn (Func_7364Result){0u, 0x10u};", "after": "\t\tif (b & (1u << B_PAD_B)) {\n\t\t\treturn (Func_7364Result){0u, 0x20u};", "case_ids": ["Func_7364-0", "Func_7364-1"]}
# <<< factory-mutation Func_7364
# >>> factory-mutation CheckEnergyNeededForAttackAfterDiscard
MUTATIONS["CheckEnergyNeededForAttackAfterDiscard"] = {"source_symbol": "CheckEnergyNeededForAttackAfterDiscard", "before": "uint8_t final_f = (uint8_t)((colorless_needed2 == 0u ? 0x80u : 0u) | 0x10u);", "after": "uint8_t final_f = (uint8_t)((colorless_needed2 == 0u ? 0x20u : 0u) | 0x10u);", "case_ids": ["CheckEnergyNeededForAttackAfterDiscard-0"]}
# <<< factory-mutation CheckEnergyNeededForAttackAfterDiscard
# >>> factory-mutation DisplayFirstOrNextCardPage
MUTATIONS["DisplayFirstOrNextCardPage"] = {"source_symbol": "DisplayFirstOrNextCardPage", "before": "\tCardPageNavigationResult r = GoToFirstOrNextCardPage();\n\tr.b = b;", "after": "\tCardPageNavigationResult r = GoToFirstOrNextCardPage();\n\tr.b = (uint8_t)(b + 1u);", "case_ids": ["DisplayFirstOrNextCardPage-0", "DisplayFirstOrNextCardPage-1"]}
# <<< factory-mutation DisplayFirstOrNextCardPage
# >>> factory-mutation PrintAttackOrCardDescription
MUTATIONS["PrintAttackOrCardDescription"] = {"source_symbol": "PrintAttackOrCardDescription", "before": "\treturn (PrintAttackOrCardDescriptionResult){text.a, text.d, text.e, text.f, text.hl};", "after": "\treturn (PrintAttackOrCardDescriptionResult){(uint8_t)(text.a + 1u), text.d, text.e, text.f, text.hl};", "case_ids": ["PrintAttackOrCardDescription-0", "PrintAttackOrCardDescription-1"]}
# <<< factory-mutation PrintAttackOrCardDescription
# >>> factory-mutation PrintAttackOrPkmnPowerInformation
MUTATIONS["PrintAttackOrPkmnPowerInformation"] = {"source_symbol": "PrintAttackOrPkmnPowerInformation", "before": "\tif ((uint8_t)(lo | hi) == 0u) {", "after": "\tif ((uint8_t)(lo | hi) == 1u) {", "case_ids": ["PrintAttackOrPkmnPowerInformation-0", "PrintAttackOrPkmnPowerInformation-1"]}
# <<< factory-mutation PrintAttackOrPkmnPowerInformation
# >>> factory-mutation PrintAttackOrNonPokemonCardDescription
MUTATIONS["PrintAttackOrNonPokemonCardDescription"] = {
    "source_symbol": "PrintAttackOrNonPokemonCardDescription",
    "before": "\t\treturn (PrintAttackOrCardDescriptionResult){a, d, e, 0x80u, hl};",
    "after": "\t\treturn (PrintAttackOrCardDescriptionResult){a, d, e, 0x00u, hl};",
    "case_ids": ["PrintAttackOrNonPokemonCardDescription-0", "PrintAttackOrNonPokemonCardDescription-1"],
}
# <<< factory-mutation PrintAttackOrNonPokemonCardDescription
# >>> factory-mutation DisplayCardPageOnLeftOrRightPressed
MUTATIONS["DisplayCardPageOnLeftOrRightPressed"] = {
    "source_symbol": "DisplayCardPageOnLeftOrRightPressed",
    "before": "\tif (a & (1u << B_PAD_LEFT)) {",
    "after": "\tif (a & (1u << B_PAD_LEFT + 1u)) {",
    "case_ids": ["DisplayCardPageOnLeftOrRightPressed-0", "DisplayCardPageOnLeftOrRightPressed-1"],
}
# <<< factory-mutation DisplayCardPageOnLeftOrRightPressed
# >>> factory-mutation PrintPlayAreaCardHeader
MUTATIONS["PrintPlayAreaCardHeader"] = {"source_symbol": "PrintPlayAreaCardHeader", "before": "\tWriteByteToBGMap0(SYM_Lv, 14u, y);", "after": "\tWriteByteToBGMap0(SYM_0, 14u, y);", "case_ids": ["PrintPlayAreaCardHeader-0", "PrintPlayAreaCardHeader-1"]}
# <<< factory-mutation PrintPlayAreaCardHeader
# >>> factory-mutation PrintPokemonCardLength
MUTATIONS["PrintPokemonCardLength"] = {"source_symbol": "PrintPokemonCardLength", "before": "\t\trow = (uint8_t)(new_row + 1u);", "after": "\t\trow = new_row;", "case_ids": ["PrintPokemonCardLength-0", "PrintPokemonCardLength-1"]}
# <<< factory-mutation PrintPokemonCardLength
# >>> factory-mutation PlayDeckShuffleAnimation
MUTATIONS["PlayDeckShuffleAnimation"] = {"source_symbol": "PlayDeckShuffleAnimation", "before": "\te = DUEL_ANIM_PLAYER_SHUFFLE_490;\n\tif (gb_read8(hWhoseTurn_ADDR) != PLAYER_TURN_490)\n\t\te = DUEL_ANIM_OPP_SHUFFLE_490;", "after": "\te = DUEL_ANIM_OPP_SHUFFLE_490;\n\tif (gb_read8(hWhoseTurn_ADDR) != PLAYER_TURN_490)\n\t\te = DUEL_ANIM_PLAYER_SHUFFLE_490;", "case_ids": ["PlayDeckShuffleAnimation-0"]}
# <<< factory-mutation PlayDeckShuffleAnimation
# >>> factory-mutation OppAction_6b30
MUTATIONS["OppAction_6b30"] = {"source_symbol": "OppAction_6b30", "before": "\treturn saved;", "after": "\treturn hTemp_ffa0;", "case_ids": ["OppAction_6b30-0", "OppAction_6b30-1"]}
# <<< factory-mutation OppAction_6b30
# >>> factory-mutation PrintPlayAreaCardInformation
MUTATIONS["PrintPlayAreaCardInformation"] = {"source_symbol": "PrintPlayAreaCardInformation", "before": "\t\tProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromID(kd, ke, KnockOutText);", "after": "\t\tProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromID(kd, ke, 0u);", "case_ids": ["PrintPlayAreaCardInformation-0", "PrintPlayAreaCardInformation-1"]}
# <<< factory-mutation PrintPlayAreaCardInformation
# >>> factory-mutation PrintPlayAreaCardInformationAndLocation
MUTATIONS["PrintPlayAreaCardInformationAndLocation"] = {"source_symbol": "PrintPlayAreaCardInformationAndLocation", "before": "\tDuelistVarResult r = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD));\n\tif (r.a == 0xFFu)", "after": "\tDuelistVarResult r = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD));\n\tif (r.a != 0xFFu)", "case_ids": ["PrintPlayAreaCardInformationAndLocation-0", "PrintPlayAreaCardInformationAndLocation-1"]}
# <<< factory-mutation PrintPlayAreaCardInformationAndLocation
# >>> factory-mutation DisplayUsePokemonPowerScreen
MUTATIONS["DisplayUsePokemonPowerScreen"] = {"source_symbol": "DisplayUsePokemonPowerScreen", "before": "\twCurPlayAreaY = 0u;", "after": "\twCurPlayAreaY = 1u;", "case_ids": ["DisplayUsePokemonPowerScreen-0", "DisplayUsePokemonPowerScreen-1"]}
# <<< factory-mutation DisplayUsePokemonPowerScreen
# >>> factory-mutation InitAndPrintPlayAreaCardInformationAndLocation
MUTATIONS["InitAndPrintPlayAreaCardInformationAndLocation"] = {"source_symbol": "InitAndPrintPlayAreaCardInformationAndLocation", "before": "\twCurPlayAreaSlot = a;", "after": "\twCurPlayAreaSlot = (uint8_t)(a + 1u);", "case_ids": ["InitAndPrintPlayAreaCardInformationAndLocation-0", "InitAndPrintPlayAreaCardInformationAndLocation-1"]}
# <<< factory-mutation InitAndPrintPlayAreaCardInformationAndLocation
# >>> factory-mutation InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox
MUTATIONS["InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox"] = {"source_symbol": "InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox", "before": "\t(void)SetCursorParametersForTextBox_Default(0u, e);", "after": "\t(void)SetCursorParametersForTextBox_Default(1u, e);", "case_ids": ["InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox-0", "InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox-1"]}
# <<< factory-mutation InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox
# >>> factory-mutation PrintPlayAreaCardList
MUTATIONS["PrintPlayAreaCardList"] = {"source_symbol": "PrintPlayAreaCardList", "before": "\tb = saved_count;\n\tgb_write8(wNumPlayAreaItems_ADDR, b);\n\tif (gb_read8(wExcludeArenaPokemon_ADDR) == 0u)", "after": "\tb = (uint8_t)(saved_count + 1u);\n\tgb_write8(wNumPlayAreaItems_ADDR, b);\n\tif (gb_read8(wExcludeArenaPokemon_ADDR) == 0u)", "case_ids": ["PrintPlayAreaCardList-0", "PrintPlayAreaCardList-1"]}
# <<< factory-mutation PrintPlayAreaCardList
# >>> factory-mutation OppAction_UsePokemonPower
MUTATIONS["OppAction_UsePokemonPower"] = {"source_symbol": "OppAction_UsePokemonPower", "before": "\t(void)ExchangeRNG(0u, 0u, 0u, 0u);\n\tgb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);", "after": "\t(void)ExchangeRNG(0u, 0u, 0u, 0u);\n\tgb_write8(wSkipDuelistIsThinkingDelay_ADDR, 0u);", "case_ids": ["OppAction_UsePokemonPower-0", "OppAction_UsePokemonPower-1"]}
# <<< factory-mutation OppAction_UsePokemonPower
# >>> factory-mutation Func_616e
MUTATIONS["Func_616e"] = {"source_symbol": "Func_616e", "before": "\tgb_write8(wExcludeArenaPokemon_ADDR, 0u);", "after": "\tgb_write8(wExcludeArenaPokemon_ADDR, 1u);", "case_ids": ["Func_616e-0", "Func_616e-1"]}
# <<< factory-mutation Func_616e
# >>> factory-mutation PrintPlayAreaCardList_EnableLCD
MUTATIONS["PrintPlayAreaCardList_EnableLCD"] = {"source_symbol": "PrintPlayAreaCardList_EnableLCD", "before": "\treturn (NumPlayAreaItemsResult){gb_read8(wNumPlayAreaItems_ADDR)};", "after": "\treturn (NumPlayAreaItemsResult){0u};", "case_ids": ["PrintPlayAreaCardList_EnableLCD-0", "PrintPlayAreaCardList_EnableLCD-1"]}
# <<< factory-mutation PrintPlayAreaCardList_EnableLCD
# >>> factory-mutation FlushAllPalettesOrSendPal23Packet
MUTATIONS["FlushAllPalettesOrSendPal23Packet"] = {
    "source_symbol": "FlushAllPalettesOrSendPal23Packet",
    "before": "\tgb_write8(wTempSGBPacket_ADDR, 9u);\n\tgb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 0x9Cu);\n\tgb_write8((uint16_t)(wTempSGBPacket_ADDR + 2u), 0x63u);\n\tgb_write8((uint16_t)(wTempSGBPacket_ADDR + 0x0Fu), 0u);",
    "after": "\tgb_write8(wTempSGBPacket_ADDR, 9u);\n\tgb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 0x9Cu);\n\tgb_write8((uint16_t)(wTempSGBPacket_ADDR + 2u), 0x63u);\n\tgb_write8((uint16_t)(wTempSGBPacket_ADDR + 0x0Fu), 1u);",
    "case_ids": ["FlushAllPalettesOrSendPal23Packet-2", "FlushAllPalettesOrSendPal23Packet-3"]
}
# <<< factory-mutation FlushAllPalettesOrSendPal23Packet
# >>> factory-mutation CheckIfCardCanBePlayed
MUTATIONS["CheckIfCardCanBePlayed"] = {
    "source_symbol": "CheckIfCardCanBePlayed",
    "before": "\tuint8_t f = (energy == 0u) ? 0x80u : 0x10u;\n\treturn (CheckIfCardCanBePlayedResult){energy, f};",
    "after": "\tuint8_t f = (energy == 0u) ? 0x80u : 0x00u;\n\treturn (CheckIfCardCanBePlayedResult){energy, f};",
    "case_ids": ["CheckIfCardCanBePlayed-0", "CheckIfCardCanBePlayed-1"],
}
# <<< factory-mutation CheckIfCardCanBePlayed
# >>> factory-mutation OppAction_6b15
MUTATIONS["OppAction_6b15"] = {
    "source_symbol": "OppAction_6b15",
    "before": "\twSkipDuelistIsThinkingDelay = 0x01u;",
    "after": "\twSkipDuelistIsThinkingDelay = 0x00u;",
    "case_ids": ["OppAction_6b15-0", "OppAction_6b15-1"],
}
# <<< factory-mutation OppAction_6b15
# >>> factory-mutation OppAction_ExecutePokemonPowerEffect
MUTATIONS["OppAction_ExecutePokemonPowerEffect"] = {
    "source_symbol": "OppAction_ExecutePokemonPowerEffect",
    "before": "\twSkipDuelistIsThinkingDelay = 0x01u;\n\treturn (OppAction_ExecutePokemonPowerEffectResult){0x01u, effect.f, effect.c, effect.hl};",
    "after": "\twSkipDuelistIsThinkingDelay = 0x00u;\n\treturn (OppAction_ExecutePokemonPowerEffectResult){0x01u, effect.f, effect.c, effect.hl};",
    "case_ids": ["OppAction_ExecutePokemonPowerEffect-0", "OppAction_ExecutePokemonPowerEffect-1"],
}
# <<< factory-mutation OppAction_ExecutePokemonPowerEffect
# >>> factory-mutation LoadSelectedCardGfx
MUTATIONS["LoadSelectedCardGfx"] = {
    "source_symbol": "LoadSelectedCardGfx",
    "before": "LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));",
    "after": "LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x201u));",
    "case_ids": ["LoadSelectedCardGfx-0", "LoadSelectedCardGfx-1"],
}
# <<< factory-mutation LoadSelectedCardGfx
# >>> factory-mutation AIProcessHandTrainerCards
MUTATIONS["AIProcessHandTrainerCards"] = {
    "source_symbol": "AIProcessHandTrainerCards",
    "before": "\treturn (AIProcessHandTrainerCardsWrapResult){r.a, r.f};",
    "after": "\treturn (AIProcessHandTrainerCardsWrapResult){r.a, (uint8_t)(r.f ^ 1u)};",
    "case_ids": ["AIProcessHandTrainerCards-0", "AIProcessHandTrainerCards-1"],
}
# <<< factory-mutation AIProcessHandTrainerCards
# >>> factory-mutation CardListFunction
MUTATIONS["CardListFunction"] = {
    "source_symbol": "CardListFunction",
    "before": "\tif ((a & PAD_B) != 0u) {\n\t\thCurMenuItem = MENU_CANCEL;\n\t\treturn (CardListFunctionResult){MENU_CANCEL, 0x10u};\n\t}",
    "after": "\tif ((a & PAD_B) != 0u) {\n\t\thCurMenuItem = 0u;\n\t\treturn (CardListFunctionResult){MENU_CANCEL, 0x10u};\n\t}",
    "case_ids": ["CardListFunction-1", "CardListFunction-5"],
}
# <<< factory-mutation CardListFunction
# >>> factory-mutation CheckIfSelectedAttackIsUnusable
MUTATIONS["CheckIfSelectedAttackIsUnusable"] = {
    "source_symbol": "CheckIfSelectedAttackIsUnusable",
    "before": "\tif (energy.f & 0x10u)\n\t\treturn (CheckIfSelectedAttackIsUnusableResult){energy.a, energy.f, energy.b, energy.c, energy.d, energy.e, energy.hl};",
    "after": "\tif (energy.f & 0x10u)\n\t\treturn (CheckIfSelectedAttackIsUnusableResult){energy.a, 0u, energy.b, energy.c, energy.d, energy.e, energy.hl};",
    "case_ids": ["CheckIfSelectedAttackIsUnusable-0", "CheckIfSelectedAttackIsUnusable-1"],
}
# <<< factory-mutation CheckIfSelectedAttackIsUnusable
# >>> factory-mutation CheckForBenchIDAtHalfHPAndCanUseSecondAttack
MUTATIONS["CheckForBenchIDAtHalfHPAndCanUseSecondAttack"] = {
    "source_symbol": "CheckForBenchIDAtHalfHPAndCanUseSecondAttack",
    "before": "\tf = (uint8_t)(b == 0u ? 0x80u : 0x10u);",
    "after": "\tf = (uint8_t)(b == 0u ? 0x00u : 0x10u);",
    "case_ids": ["CheckForBenchIDAtHalfHPAndCanUseSecondAttack-0", "CheckForBenchIDAtHalfHPAndCanUseSecondAttack-1"],
}
# <<< factory-mutation CheckForBenchIDAtHalfHPAndCanUseSecondAttack
# >>> factory-mutation CountNumberOfSetUpBenchPokemon
MUTATIONS["CountNumberOfSetUpBenchPokemon"] = {
    "source_symbol": "CountNumberOfSetUpBenchPokemon",
    "before": "\ta = b;\n\tf = (uint8_t)(b == 0u ? 0x80u : 0x10u);\n\treturn (CountNumberOfSetUpBenchPokemonResult){a, f, b, c, saved_location, saved_attack, hl};",
    "after": "\ta = b;\n\tf = (uint8_t)(b == 0u ? 0x00u : 0x10u);\n\treturn (CountNumberOfSetUpBenchPokemonResult){a, f, b, c, saved_location, saved_attack, hl};",
    "case_ids": ["CountNumberOfSetUpBenchPokemon-0", "CountNumberOfSetUpBenchPokemon-1"],
}
# <<< factory-mutation CountNumberOfSetUpBenchPokemon
# >>> factory-mutation HandleLegendaryArticunoEnergyScoring
MUTATIONS["HandleLegendaryArticunoEnergyScoring"] = {
    "source_symbol": "HandleLegendaryArticunoEnergyScoring",
    "before": "\tif (wOpponentDeckID == 0x0Eu) {",
    "after": "\tif (wOpponentDeckID != 0x0Eu) {",
    "case_ids": ["HandleLegendaryArticunoEnergyScoring-0", "HandleLegendaryArticunoEnergyScoring-2"],
}
# <<< factory-mutation HandleLegendaryArticunoEnergyScoring
# >>> factory-mutation CheckIfArenaCardIsFullyPowered
MUTATIONS["CheckIfArenaCardIsFullyPowered"] = {
    "source_symbol": "CheckIfArenaCardIsFullyPowered",
    "before": "\tif (a >= d) {\n\t\tf = (uint8_t)(a == 0u ? 0x80u : 0x00u);\n\t\treturn (CheckIfArenaCardIsFullyPoweredResult){a, f};\n\t}",
    "after": "\tif (a >= d) {\n\t\tf = 0xFFu;\n\t\treturn (CheckIfArenaCardIsFullyPoweredResult){a, f};\n\t}",
    "case_ids": ["CheckIfArenaCardIsFullyPowered-0", "CheckIfArenaCardIsFullyPowered-1"],
}
# <<< factory-mutation CheckIfArenaCardIsFullyPowered
# >>> factory-mutation SendCardAttrBlkPacket
MUTATIONS["SendCardAttrBlkPacket"] = {
    "source_symbol": "SendCardAttrBlkPacket",
    "before": "\tSendSGBResult result = SendSGB(a, f, b, c, d, e, packet);",
    "after": "\tSendSGBResult result = SendSGB(a, f, b, c, d, e, 0u);",
    "case_ids": ["SendCardAttrBlkPacket-0", "SendCardAttrBlkPacket-1"],
}
# <<< factory-mutation SendCardAttrBlkPacket
# >>> factory-mutation ApplyBGP6OrSGB3ToCardImage
MUTATIONS["ApplyBGP6OrSGB3ToCardImage"] = {
    "source_symbol": "ApplyBGP6OrSGB3ToCardImage",
    "before": "if (console == CONSOLE_DMG) {",
    "after": "if (console != CONSOLE_DMG) {",
    "case_ids": ["ApplyBGP6OrSGB3ToCardImage-0", "ApplyBGP6OrSGB3ToCardImage-1"],
}
# <<< factory-mutation ApplyBGP6OrSGB3ToCardImage
# >>> factory-mutation DrawLargePictureOfCard
MUTATIONS["DrawLargePictureOfCard"] = {
    "source_symbol": "DrawLargePictureOfCard",
    "before": "wDuelDisplayedScreen = LARGE_CARD_PICTURE;",
    "after": "wDuelDisplayedScreen = 0u;",
    "case_ids": ["DrawLargePictureOfCard-0"],
}
# <<< factory-mutation DrawLargePictureOfCard
# >>> factory-mutation DrawCardPageSurroundingBox
MUTATIONS["DrawCardPageSurroundingBox"] = {
    "source_symbol": "DrawCardPageSurroundingBox",
    "before": "gb_write8(wTextBoxFrameType_ADDR, (uint8_t)(gb_read8(wTextBoxFrameType_ADDR) & 0x7fu));",
    "after": "gb_write8(wTextBoxFrameType_ADDR, (uint8_t)(gb_read8(wTextBoxFrameType_ADDR) | 0x80u));",
    "case_ids": ["DrawCardPageSurroundingBox-0", "DrawCardPageSurroundingBox-1"],
}
# <<< factory-mutation DrawCardPageSurroundingBox
# >>> factory-mutation PrintPokemonCardPageGenericInformation
MUTATIONS["PrintPokemonCardPageGenericInformation"] = {"source_symbol": "PrintPokemonCardPageGenericInformation", "before": "JPWriteByteToBGMap0((uint8_t)(color + 1u), 18u, 1u);", "after": "JPWriteByteToBGMap0((uint8_t)(color + 2u), 18u, 1u);", "case_ids": ["PrintPokemonCardPageGenericInformation-0", "PrintPokemonCardPageGenericInformation-1"]}
# <<< factory-mutation PrintPokemonCardPageGenericInformation
# >>> factory-mutation DrawDuelHUD
MUTATIONS["DrawDuelHUD"] = {"source_symbol": "DrawDuelHUD", "before": "wHUDEnergyAndHPBarsX = b;", "after": "wHUDEnergyAndHPBarsX = (uint8_t)(b + 1u);", "case_ids": ["DrawDuelHUD-0", "DrawDuelHUD-1"]}
# <<< factory-mutation DrawDuelHUD
# >>> factory-mutation DrawDuelHUDs
MUTATIONS["DrawDuelHUDs"] = {"source_symbol": "DrawDuelHUDs", "before": "\tDrawDuelHUD(11u, 8u, 1u, 11u);\n\tDuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);", "after": "\tDrawDuelHUD(11u, 8u, 1u, 12u);\n\tDuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);", "case_ids": ["DrawDuelHUDs-0", "DrawDuelHUDs-1"]}
# <<< factory-mutation DrawDuelHUDs
# >>> factory-mutation DrawCardListScreenLayout
MUTATIONS["DrawCardListScreenLayout"] = {"source_symbol": "DrawCardListScreenLayout", "before": "return (DrawCardListScreenLayoutResult){a, 0x90u};", "after": "return (DrawCardListScreenLayoutResult){a, 0x10u};", "case_ids": ["DrawCardListScreenLayout-0", "DrawCardListScreenLayout-2"]}
# <<< factory-mutation DrawCardListScreenLayout
# >>> factory-mutation ApplyBGP7OrSGB2ToCardImage
MUTATIONS["ApplyBGP7OrSGB2ToCardImage"] = {"source_symbol": "ApplyBGP7OrSGB2ToCardImage", "before": "\t\ta = 0x0Au;", "after": "\t\ta = 0x20u;", "case_ids": ["ApplyBGP7OrSGB2ToCardImage-1"]}
# <<< factory-mutation ApplyBGP7OrSGB2ToCardImage
# >>> factory-mutation DisplayPracticeDuelPlayerHandScreen
MUTATIONS["DisplayPracticeDuelPlayerHandScreen"] = {"source_symbol": "DisplayPracticeDuelPlayerHandScreen", "before": "\tDrawRegularTextBox(&box, 0u, 20u, 13u, 0u, 0u);", "after": "\tDrawRegularTextBox(&box, 0u, 20u, 12u, 0u, 0u);", "case_ids": ["DisplayPracticeDuelPlayerHandScreen-0", "DisplayPracticeDuelPlayerHandScreen-1"]}
# <<< factory-mutation DisplayPracticeDuelPlayerHandScreen
# >>> factory-mutation DrawDuelMainScene
MUTATIONS["DrawDuelMainScene"] = {
    "source_symbol": "DrawDuelMainScene",
    "before": "\t\t\tgb_write8(hWhoseTurn_ADDR, saved_turn);\n\t\t\treturn;",
    "after": "\t\t\tgb_write8(hWhoseTurn_ADDR, PLAYER_TURN);\n\t\t\treturn;",
    "case_ids": ["DrawDuelMainScene-1"],
}
# <<< factory-mutation DrawDuelMainScene
# >>> factory-mutation InitAndDrawCardListScreenLayout
MUTATIONS["InitAndDrawCardListScreenLayout"] = {"source_symbol": "InitAndDrawCardListScreenLayout", "before": "\twSelectedDuelSubMenuItem = 0u;", "after": "\twSelectedDuelSubMenuItem = 1u;", "case_ids": ["InitAndDrawCardListScreenLayout-0", "InitAndDrawCardListScreenLayout-1"]}
# <<< factory-mutation InitAndDrawCardListScreenLayout
# >>> factory-mutation RedrawTurnDuelistsDuelHUD
MUTATIONS["RedrawTurnDuelistsDuelHUD"] = {"source_symbol": "RedrawTurnDuelistsDuelHUD", "before": "\tSwapTurn();\n\tDrawDuelHUDs();\n\tSwapTurn();", "after": "\tSwapTurn();\n\tDrawDuelHUDs();", "case_ids": ["RedrawTurnDuelistsDuelHUD-1", "RedrawTurnDuelistsDuelHUD-2"]}
# <<< factory-mutation RedrawTurnDuelistsDuelHUD
# >>> factory-mutation OppAction_DrawDuelMainScene
MUTATIONS["OppAction_DrawDuelMainScene"] = {"source_symbol": "OppAction_DrawDuelMainScene", "before": "\tDrawDuelMainScene();", "after": "\tgb_write8(0xCAC2u, 0u);", "case_ids": ["OppAction_DrawDuelMainScene-0", "OppAction_DrawDuelMainScene-1"]}
# <<< factory-mutation OppAction_DrawDuelMainScene
# >>> factory-mutation InitAndDrawCardListScreenLayout_WithSelectCheckMenu
MUTATIONS["InitAndDrawCardListScreenLayout_WithSelectCheckMenu"] = {"source_symbol": "InitAndDrawCardListScreenLayout_WithSelectCheckMenu", "before": "\tgb_write8(wCardListItemSelectionMenuType_ADDR, SELECT_CHECK);", "after": "\tgb_write8(wCardListItemSelectionMenuType_ADDR, 0u);", "case_ids": ["InitAndDrawCardListScreenLayout_WithSelectCheckMenu-0", "InitAndDrawCardListScreenLayout_WithSelectCheckMenu-1"]}
# <<< factory-mutation InitAndDrawCardListScreenLayout_WithSelectCheckMenu
# >>> factory-mutation DisplayCardListDetails
MUTATIONS["DisplayCardListDetails"] = {"source_symbol": "DisplayCardListDetails", "before": "\t\tuint8_t f = (uint8_t)(0x40u | (((value & 0x0Fu) < 0x0Fu) ? 0x20u : 0u) | ((value < 0xFFu) ? 0x10u : 0u) | 0x80u);", "after": "\t\tuint8_t f = (uint8_t)(0x40u | (((value & 0x0Fu) < 0x0Fu) ? 0x20u : 0u) | ((value < 0xFFu) ? 0x10u : 0u));", "case_ids": ["DisplayCardListDetails-0", "DisplayCardListDetails-1"]}
# <<< factory-mutation DisplayCardListDetails
# >>> factory-mutation OppAction_FinishTurnWithoutAttacking
MUTATIONS["OppAction_FinishTurnWithoutAttacking"] = {"source_symbol": "OppAction_FinishTurnWithoutAttacking", "before": "\t(void)DrawWideTextBox_WaitForInput(FinishedTurnWithoutAttackingText);\n\twOpponentTurnEnded = 1u;", "after": "\t(void)DrawWideTextBox_WaitForInput(FinishedTurnWithoutAttackingText);\n\twOpponentTurnEnded = 0u;", "case_ids": ["OppAction_FinishTurnWithoutAttacking-0", "OppAction_FinishTurnWithoutAttacking-1"]}
# <<< factory-mutation OppAction_FinishTurnWithoutAttacking
# >>> factory-mutation RedrawTurnDuelistsMainSceneOrDuelHUD
MUTATIONS["RedrawTurnDuelistsMainSceneOrDuelHUD"] = {"source_symbol": "RedrawTurnDuelistsMainSceneOrDuelHUD", "before": "\tif (wDuelDisplayedScreen == DUEL_MAIN_SCENE) {", "after": "\tif (wDuelDisplayedScreen != DUEL_MAIN_SCENE) {", "case_ids": ["RedrawTurnDuelistsMainSceneOrDuelHUD-0", "RedrawTurnDuelistsMainSceneOrDuelHUD-1"]}
# <<< factory-mutation RedrawTurnDuelistsMainSceneOrDuelHUD
# >>> factory-mutation DisplayNoBasicPokemonInHandScreen
MUTATIONS["DisplayNoBasicPokemonInHandScreen"] = {"source_symbol": "DisplayNoBasicPokemonInHandScreen", "before": "void DisplayNoBasicPokemonInHandScreen(void)\n{\n\tEmptyScreen();\n\tTileCopyResult tiles = LoadDuelCardSymbolTiles();\n\tuint16_t box = tiles.hl;\n\tDrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);\n\t(void)CreateHandCardList(0u);\n\tuint8_t count = CountCardsInDuelTempList().a;", "after": "void DisplayNoBasicPokemonInHandScreen(void)\n{\n\tEmptyScreen();\n\tTileCopyResult tiles = LoadDuelCardSymbolTiles();\n\tuint16_t box = tiles.hl;\n\tDrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);\n\t(void)CreateHandCardList(0u);\n\tuint8_t count = (uint8_t)(CountCardsInDuelTempList().a + 1u);", "case_ids": ["DisplayNoBasicPokemonInHandScreen-0", "DisplayNoBasicPokemonInHandScreen-1"]}
# <<< factory-mutation DisplayNoBasicPokemonInHandScreen
# >>> factory-mutation PrintAndLoadAttacksToDuelTempList
MUTATIONS["PrintAndLoadAttacksToDuelTempList"] = {"source_symbol": "PrintAndLoadAttacksToDuelTempList", "before": "\t\tc = (uint8_t)(c + 1u);\n\t\t(void)PrintAttackOrPkmnPowerInformation(b, c, 0u, b, wLoadedCard1Atk1Name_ADDR);", "after": "\t\t(void)PrintAttackOrPkmnPowerInformation(b, c, 0u, b, wLoadedCard1Atk1Name_ADDR);", "case_ids": ["PrintAndLoadAttacksToDuelTempList-0", "PrintAndLoadAttacksToDuelTempList-1"]}
# <<< factory-mutation PrintAndLoadAttacksToDuelTempList
# >>> factory-mutation DisplayPokemonAttackCardPage
MUTATIONS["DisplayPokemonAttackCardPage"] = {"source_symbol": "DisplayPokemonAttackCardPage", "before": "\tPrintAttackOrPkmnPowerInformationResult printed = PrintAttackOrPkmnPowerInformation(b, c, d, 2u, hl);", "after": "\tPrintAttackOrPkmnPowerInformationResult printed = PrintAttackOrPkmnPowerInformation(b, c, d, 3u, hl);", "case_ids": ["DisplayPokemonAttackCardPage-0", "DisplayPokemonAttackCardPage-1"]}
# <<< factory-mutation DisplayPokemonAttackCardPage
# >>> factory-mutation DisplayCardPage_PokemonAttack2Page2
MUTATIONS["DisplayCardPage_PokemonAttack2Page2"] = {"source_symbol": "DisplayCardPage_PokemonAttack2Page2", "before": "\tDisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u), wLoadedCard1Atk2Name_ADDR);", "after": "\tDisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk2Description_ADDR + 3u), wLoadedCard1Atk2Name_ADDR);", "case_ids": ["DisplayCardPage_PokemonAttack2Page2-0", "DisplayCardPage_PokemonAttack2Page2-1"]}
# <<< factory-mutation DisplayCardPage_PokemonAttack2Page2
# >>> factory-mutation DisplayCardPage_PokemonAttack1Page1
MUTATIONS["DisplayCardPage_PokemonAttack1Page1"] = {"source_symbol": "DisplayCardPage_PokemonAttack1Page1", "before": "\tDisplayPokemonAttackCardPage(b, c, d, wLoadedCard1Atk1Description_ADDR, wLoadedCard1Atk1Name_ADDR);", "after": "\tDisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk1Description_ADDR + 1u), wLoadedCard1Atk1Name_ADDR);", "case_ids": ["DisplayCardPage_PokemonAttack1Page1-0", "DisplayCardPage_PokemonAttack1Page1-1"]}
# <<< factory-mutation DisplayCardPage_PokemonAttack1Page1
# >>> factory-mutation DisplayCardPage_PokemonAttack1Page2
MUTATIONS["DisplayCardPage_PokemonAttack1Page2"] = {"source_symbol": "DisplayCardPage_PokemonAttack1Page2", "before": "\tDisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u), wLoadedCard1Atk1Name_ADDR);", "after": "\tDisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk1Description_ADDR + 3u), wLoadedCard1Atk1Name_ADDR);", "case_ids": ["DisplayCardPage_PokemonAttack1Page2-0", "DisplayCardPage_PokemonAttack1Page2-1"]}
# <<< factory-mutation DisplayCardPage_PokemonAttack1Page2
# >>> factory-mutation DisplayCardPage_PokemonAttack2Page1
MUTATIONS["DisplayCardPage_PokemonAttack2Page1"] = {"source_symbol": "DisplayCardPage_PokemonAttack2Page1", "before": "\tDisplayPokemonAttackCardPage(b, c, d, wLoadedCard1Atk2Description_ADDR, wLoadedCard1Atk2Name_ADDR);", "after": "\tDisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk2Description_ADDR + 1u), wLoadedCard1Atk2Name_ADDR);", "case_ids": ["DisplayCardPage_PokemonAttack2Page1-0", "DisplayCardPage_PokemonAttack2Page1-1"]}
# <<< factory-mutation DisplayCardPage_PokemonAttack2Page1
# >>> factory-mutation DisplayAttackPage_Attack1Page1
MUTATIONS["DisplayAttackPage_Attack1Page1"] = {"source_symbol": "DisplayAttackPage_Attack1Page1", "before": "void DisplayAttackPage_Attack1Page1(uint8_t b, uint8_t c, uint8_t d)\n{\n\tDisplayCardPage_PokemonAttack1Page1(b, c, d);\n\tSwitchAttackPage();", "after": "void DisplayAttackPage_Attack1Page1(uint8_t b, uint8_t c, uint8_t d)\n{\n\tDisplayCardPage_PokemonAttack1Page1(b, c, d);\n\t(void)0;", "case_ids": ["DisplayAttackPage_Attack1Page1-0", "DisplayAttackPage_Attack1Page1-1"]}
# <<< factory-mutation DisplayAttackPage_Attack1Page1
# >>> factory-mutation DisplayAttackPage_Attack2Page1
MUTATIONS["DisplayAttackPage_Attack2Page1"] = {"source_symbol": "DisplayAttackPage_Attack2Page1", "before": "void DisplayAttackPage_Attack2Page1(uint8_t b, uint8_t c, uint8_t d)\n{\n\tDisplayCardPage_PokemonAttack2Page1(b, c, d);\n\tSwitchAttackPage();", "after": "void DisplayAttackPage_Attack2Page1(uint8_t b, uint8_t c, uint8_t d)\n{\n\tDisplayCardPage_PokemonAttack2Page1(b, c, d);\n\t(void)0;", "case_ids": ["DisplayAttackPage_Attack2Page1-0", "DisplayAttackPage_Attack2Page1-1"]}
# <<< factory-mutation DisplayAttackPage_Attack2Page1
# >>> factory-mutation DisplayAttackPage_Attack2Page2
MUTATIONS["DisplayAttackPage_Attack2Page2"] = {"source_symbol": "DisplayAttackPage_Attack2Page2", "before": "void DisplayAttackPage_Attack2Page2(uint8_t b, uint8_t c, uint8_t d)\n{\n\tuint8_t lo = gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u));\n\tuint8_t hi = gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 3u));\n\tif ((uint8_t)(lo | hi) == 0u)", "after": "void DisplayAttackPage_Attack2Page2(uint8_t b, uint8_t c, uint8_t d)\n{\n\tuint8_t lo = gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u));\n\tuint8_t hi = gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 3u));\n\tif ((uint8_t)(lo | hi) != 0u)", "case_ids": ["DisplayAttackPage_Attack2Page2-0", "DisplayAttackPage_Attack2Page2-1"]}
# <<< factory-mutation DisplayAttackPage_Attack2Page2
# >>> factory-mutation DisplayAttackPage_Attack1Page2
MUTATIONS["DisplayAttackPage_Attack1Page2"] = {"source_symbol": "DisplayAttackPage_Attack1Page2", "before": "void DisplayAttackPage_Attack1Page2(uint8_t b, uint8_t c, uint8_t d)\n{\n\tuint8_t lo = gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u));\n\tuint8_t hi = gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 3u));\n\tif ((uint8_t)(lo | hi) == 0u)", "after": "void DisplayAttackPage_Attack1Page2(uint8_t b, uint8_t c, uint8_t d)\n{\n\tuint8_t lo = gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u));\n\tuint8_t hi = gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 3u));\n\tif ((uint8_t)(lo | hi) != 0u)", "case_ids": ["DisplayAttackPage_Attack1Page2-0", "DisplayAttackPage_Attack1Page2-1"]}
# <<< factory-mutation DisplayAttackPage_Attack1Page2
# >>> factory-mutation DisplayEnergyDiscardMenu
MUTATIONS["DisplayEnergyDiscardMenu"] = {"source_symbol": "DisplayEnergyDiscardMenu", "before": "\twCardListIndicatorYPosition = 4u;", "after": "\twCardListIndicatorYPosition = 5u;", "case_ids": ["DisplayEnergyDiscardMenu-0", "DisplayEnergyDiscardMenu-1"]}
# <<< factory-mutation DisplayEnergyDiscardMenu
# >>> factory-mutation DisplayEnergyDiscardScreen
MUTATIONS["DisplayEnergyDiscardScreen"] = {"source_symbol": "DisplayEnergyDiscardScreen", "before": "\twEnergyDiscardMenuDenominator = 1u;", "after": "\twEnergyDiscardMenuDenominator = 2u;", "case_ids": ["DisplayEnergyDiscardScreen-0", "DisplayEnergyDiscardScreen-1"]}
# <<< factory-mutation DisplayEnergyDiscardScreen
# >>> factory-mutation OpenAttackPage
MUTATIONS["OpenAttackPage"] = {"source_symbol": "OpenAttackPage", "before": "\twAttackPageNumber = (v != 0u) ? ATTACKPAGE_ATTACK2_1 : ATTACKPAGE_ATTACK1_1;", "after": "\twAttackPageNumber = (v != 0u) ? ATTACKPAGE_ATTACK1_1 : ATTACKPAGE_ATTACK2_1;", "case_ids": ["OpenAttackPage-0", "OpenAttackPage-1"]}
# <<< factory-mutation OpenAttackPage
# >>> factory-mutation HandleEnergyDiscardMenuInput
MUTATIONS["HandleEnergyDiscardMenuInput"] = {
    "source_symbol": "HandleEnergyDiscardMenuInput",
    "before": "uint8_t denominator = gb_read8(wEnergyDiscardMenuDenominator_ADDR);",
    "after": "uint8_t denominator = gb_read8(wEnergyDiscardMenuNumerator_ADDR);",
    "case_ids": ["HandleEnergyDiscardMenuInput-1"],
}
# <<< factory-mutation HandleEnergyDiscardMenuInput
# >>> factory-mutation DisplayRetreatScreen
MUTATIONS["DisplayRetreatScreen"] = {"source_symbol": "DisplayRetreatScreen", "before": "\thTempRetreatCostCards = 0xFFu;", "after": "\thTempRetreatCostCards = 0u;", "case_ids": ["DisplayRetreatScreen-0", "DisplayRetreatScreen-1"]}
# <<< factory-mutation DisplayRetreatScreen
# >>> factory-mutation PrintPracticeDuelInstructions_Fast
MUTATIONS["PrintPracticeDuelInstructions_Fast"] = {"source_symbol": "PrintPracticeDuelInstructions_Fast", "before": "void PrintPracticeDuelInstructions_Fast(uint16_t hl)\n{\n\tfor (;;) {\n\t\tuint8_t count = gb_read8(hl);\n\t\thl = (uint16_t)(hl + 1u);\n\t\tif (count == 0u) {\n\t\t\tPrintPracticeDuelLetsPlayTheGame();\n\t\t\treturn;\n\t\t}", "after": "void PrintPracticeDuelInstructions_Fast(uint16_t hl)\n{\n\tfor (;;) {\n\t\tuint8_t count = gb_read8(hl);\n\t\thl = (uint16_t)(hl + 1u);\n\t\tif (count == 0u) {\n\t\t\treturn;\n\t\t}", "case_ids": ["PrintPracticeDuelInstructions_Fast-0", "PrintPracticeDuelInstructions_Fast-1"]}
# <<< factory-mutation PrintPracticeDuelInstructions_Fast
# >>> factory-mutation PracticeDuel_RepeatInstructions
MUTATIONS["PracticeDuel_RepeatInstructions"] = {
 "source_symbol": "PracticeDuel_RepeatInstructions",
 "before": "\t * clear it, so the caller sees Z|C, not carry alone. */\n\treturn 0x90u;",
 "after": "\t * clear it, so the caller sees Z|C, not carry alone. */\n\treturn 0x00u;",
 "case_ids": ["PracticeDuel_RepeatInstructions-0", "PracticeDuel_RepeatInstructions-1"],
}
# <<< factory-mutation PracticeDuel_RepeatInstructions
# >>> factory-mutation _DisplayCardDetailScreen
MUTATIONS["_DisplayCardDetailScreen"] = {"source_symbol": "_DisplayCardDetailScreen", "before": "\tWaitResult waited = DrawWideTextBox_WaitForInput(saved_hl);", "after": "\tWaitResult waited = (WaitResult){0u};", "case_ids": ["_DisplayCardDetailScreen-0", "_DisplayCardDetailScreen-1"]}
# <<< factory-mutation _DisplayCardDetailScreen
# >>> factory-mutation OpenCardPage
MUTATIONS["OpenCardPage"] = {"source_symbol": "OpenCardPage", "before": "void OpenCardPage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageType_ADDR, a);", "after": "void OpenCardPage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageType_ADDR, 0u);", "case_ids": ["OpenCardPage-0", "OpenCardPage-1"]}
# <<< factory-mutation OpenCardPage
# >>> factory-mutation DisplayCardDetailScreen
MUTATIONS["DisplayCardDetailScreen"] = {
 "source_symbol": "DisplayCardDetailScreen",
 "before": "\t * what reaches the screen routine. */\n\t(void)LoadCardDataToBuffer1_FromDeckIndex(a);",
 "after": "\t * what reaches the screen routine. */\n\t(void)LoadCardDataToBuffer1_FromDeckIndex((uint8_t)(a + 1u));",
 "case_ids": ["DisplayCardDetailScreen-0", "DisplayCardDetailScreen-1"],
}
# <<< factory-mutation DisplayCardDetailScreen
# >>> factory-mutation OpenCardPage_FromHand
MUTATIONS["OpenCardPage_FromHand"] = {"source_symbol": "OpenCardPage_FromHand", "before": "void OpenCardPage_FromHand(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageExitKeys_ADDR, PAD_B);", "after": "void OpenCardPage_FromHand(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageExitKeys_ADDR, 0u);", "case_ids": ["OpenCardPage_FromHand-0", "OpenCardPage_FromHand-1"]}
# <<< factory-mutation OpenCardPage_FromHand
# >>> factory-mutation OpenCardPage_FromCheckPlayArea
MUTATIONS["OpenCardPage_FromCheckPlayArea"] = {"source_symbol": "OpenCardPage_FromCheckPlayArea", "before": "void OpenCardPage_FromCheckPlayArea(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageExitKeys_ADDR, PAD_B);", "after": "void OpenCardPage_FromCheckPlayArea(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageExitKeys_ADDR, 0u);", "case_ids": ["OpenCardPage_FromCheckPlayArea-0", "OpenCardPage_FromCheckPlayArea-1"]}
# <<< factory-mutation OpenCardPage_FromCheckPlayArea
# >>> factory-mutation DisplayUsedTrainerCardDetailScreen
MUTATIONS["DisplayUsedTrainerCardDetailScreen"] = {
 "source_symbol": "DisplayUsedTrainerCardDetailScreen",
 "before": "WaitResult DisplayUsedTrainerCardDetailScreen(void)\n{\n\treturn DisplayCardDetailScreen(hTempCardIndex_ff9f, UsedText);",
 "after": "WaitResult DisplayUsedTrainerCardDetailScreen(void)\n{\n\treturn DisplayCardDetailScreen((uint8_t)(hTempCardIndex_ff9f + 1u), UsedText);",
 "case_ids": ["DisplayUsedTrainerCardDetailScreen-0", "DisplayUsedTrainerCardDetailScreen-1"],
}
# <<< factory-mutation DisplayUsedTrainerCardDetailScreen
# >>> factory-mutation DisplayNoBasicPokemonInHandScreenAndText
MUTATIONS["DisplayNoBasicPokemonInHandScreenAndText"] = {"source_symbol": "DisplayNoBasicPokemonInHandScreenAndText", "before": "DisplayNoBasicPokemonInHandScreenAndTextResult DisplayNoBasicPokemonInHandScreenAndText(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ThereAreNoBasicPokemonInHand);\n\tDisplayNoBasicPokemonInHandScreen();\n\tPrintReturnCardsToDeckDrawAgainResult result = PrintReturnCardsToDeckDrawAgain();\n\treturn (DisplayNoBasicPokemonInHandScreenAndTextResult){result.a, result.b, result.c, result.f, result.hl, result.de};\n}", "after": "DisplayNoBasicPokemonInHandScreenAndTextResult DisplayNoBasicPokemonInHandScreenAndText(void)\n{\n\t(void)DrawWideTextBox_WaitForInput(ThereAreNoBasicPokemonInHand);\n\tDisplayNoBasicPokemonInHandScreen();\n\tPrintReturnCardsToDeckDrawAgainResult result = PrintReturnCardsToDeckDrawAgain();\n\treturn (DisplayNoBasicPokemonInHandScreenAndTextResult){0u};\n}", "case_ids": ["DisplayNoBasicPokemonInHandScreenAndText-0", "DisplayNoBasicPokemonInHandScreenAndText-1"]}
# <<< factory-mutation DisplayNoBasicPokemonInHandScreenAndText
# >>> factory-mutation OpenCardPage_FromCheckHandOrDiscardPile
MUTATIONS["OpenCardPage_FromCheckHandOrDiscardPile"] = {"source_symbol": "OpenCardPage_FromCheckHandOrDiscardPile", "before": "void OpenCardPage_FromCheckHandOrDiscardPile(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageExitKeys_ADDR, (uint8_t)(PAD_B | PAD_UP | PAD_DOWN));", "after": "void OpenCardPage_FromCheckHandOrDiscardPile(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(wCardPageExitKeys_ADDR, 0u);", "case_ids": ["OpenCardPage_FromCheckHandOrDiscardPile-0", "OpenCardPage_FromCheckHandOrDiscardPile-1"]}
# <<< factory-mutation OpenCardPage_FromCheckHandOrDiscardPile
# >>> factory-mutation CardListItemSelectionMenu
MUTATIONS["CardListItemSelectionMenu"] = {"source_symbol": "CardListItemSelectionMenu", "before": "\t\treturn (CardListItemSelectionMenuResult){0u, 0x80u};", "after": "\t\treturn (CardListItemSelectionMenuResult){1u, 0x80u};", "case_ids": ["CardListItemSelectionMenu-0", "CardListItemSelectionMenu-1"]}
# <<< factory-mutation CardListItemSelectionMenu
# >>> factory-mutation DisplayPlayerDrawCardScreen
MUTATIONS["DisplayPlayerDrawCardScreen"] = {"source_symbol": "DisplayPlayerDrawCardScreen", "before": "WaitResult DisplayPlayerDrawCardScreen(void)\n{\n\treturn DisplayCardDetailScreen(hTempCardIndex_ff98, YouDrewText);", "after": "WaitResult DisplayPlayerDrawCardScreen(void)\n{\n\treturn DisplayCardDetailScreen((uint8_t)(hTempCardIndex_ff98 + 1u), YouDrewText);", "case_ids": ["DisplayPlayerDrawCardScreen-0", "DisplayPlayerDrawCardScreen-1"]}
# <<< factory-mutation DisplayPlayerDrawCardScreen
# >>> factory-mutation OppAction_PlayTrainerCard
MUTATIONS["OppAction_PlayTrainerCard"] = {"source_symbol": "OppAction_PlayTrainerCard", "before": "void OppAction_PlayTrainerCard(void)\n{\n\t(void)LoadNonPokemonCardEffectCommands();\n\t(void)DisplayUsedTrainerCardDetailScreen();\n\tPrintUsedTrainerCardDescription();\n\t(void)ExchangeRNG(0u, 0u, 0u, 0u);\n\tgb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);", "after": "void OppAction_PlayTrainerCard(void)\n{\n\t(void)LoadNonPokemonCardEffectCommands();\n\t(void)DisplayUsedTrainerCardDetailScreen();\n\tPrintUsedTrainerCardDescription();\n\t(void)ExchangeRNG(0u, 0u, 0u, 0u);\n\tgb_write8(wSkipDuelistIsThinkingDelay_ADDR, 0u);", "case_ids": ["OppAction_PlayTrainerCard-0", "OppAction_PlayTrainerCard-1"]}
# <<< factory-mutation OppAction_PlayTrainerCard
# >>> factory-mutation OpenActivePokemonScreen
MUTATIONS["OpenActivePokemonScreen"] = {"source_symbol": "OpenActivePokemonScreen", "before": "void OpenActivePokemonScreen(void)\n{\n\tDuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);\n\tif (arena.a == 0xFFu)\n\t\treturn;\n\tuint16_t card_id = GetCardIDFromDeckIndex(arena.a);\n\tLoadCardDataToBuffer1_FromCardID((uint8_t)card_id);\n\twCurPlayAreaSlot = 0u;", "after": "void OpenActivePokemonScreen(void)\n{\n\tDuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);\n\tif (arena.a == 0xFFu)\n\t\treturn;\n\tuint16_t card_id = GetCardIDFromDeckIndex(arena.a);\n\tLoadCardDataToBuffer1_FromCardID((uint8_t)card_id);\n\twCurPlayAreaSlot = 1u;", "case_ids": ["OpenActivePokemonScreen-1", "OpenActivePokemonScreen-2"]}
# <<< factory-mutation OpenActivePokemonScreen
# >>> factory-mutation DisplayPlayAreaScreenToUsePkmnPower
MUTATIONS["DisplayPlayAreaScreenToUsePkmnPower"] = {"source_symbol": "DisplayPlayAreaScreenToUsePkmnPower", "before": "\tgb_write8(wSelectedDuelSubMenuItem_ADDR, 0u);", "after": "\tgb_write8(wSelectedDuelSubMenuItem_ADDR, 1u);", "case_ids": ["DisplayPlayAreaScreenToUsePkmnPower-0", "DisplayPlayAreaScreenToUsePkmnPower-1"]}
# <<< factory-mutation DisplayPlayAreaScreenToUsePkmnPower
# >>> factory-mutation DisplayCardPage_PokemonOverview
MUTATIONS["DisplayCardPage_PokemonOverview"] = {
    "source_symbol": "DisplayCardPage_PokemonOverview",
    "before": "if (page_type != CARDPAGETYPE_NOT_PLAY_AREA) {",
    "after": "if (page_type == CARDPAGETYPE_NOT_PLAY_AREA) {",
    "case_ids": ["DisplayCardPage_PokemonOverview-0", "DisplayCardPage_PokemonOverview-1"],
}
# <<< factory-mutation DisplayCardPage_PokemonOverview
# >>> factory-mutation DisplayEnergyOrTrainerCardPage
MUTATIONS["DisplayEnergyOrTrainerCardPage"] = {
    "source_symbol": "DisplayEnergyOrTrainerCardPage",
    "before": "\treturn PrintAttackOrNonPokemonCardDescription(saved_hl, d, e);",
    "after": "\treturn PrintAttackOrNonPokemonCardDescription(saved_hl, 1u, 1u);",
    "case_ids": ["DisplayEnergyOrTrainerCardPage-0", "DisplayEnergyOrTrainerCardPage-1"],
}
# <<< factory-mutation DisplayEnergyOrTrainerCardPage
# >>> factory-mutation DisplayCardPage_Energy
MUTATIONS["DisplayCardPage_Energy"] = {"source_symbol": "DisplayCardPage_Energy", "before": "\tPrintAttackOrCardDescriptionResult result = DisplayEnergyOrTrainerCardPage(HEADER_ENERGY, f, b, c, d, e, wLoadedCard1NonPokemonDescription_ADDR);", "after": "\tPrintAttackOrCardDescriptionResult result = DisplayEnergyOrTrainerCardPage(HEADER_ENERGY, f, b, c, d, e, 0u);", "case_ids": ["DisplayCardPage_Energy-0", "DisplayCardPage_Energy-1"]}
# <<< factory-mutation DisplayCardPage_Energy
