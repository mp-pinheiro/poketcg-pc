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
