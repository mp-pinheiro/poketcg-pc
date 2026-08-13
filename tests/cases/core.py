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
CONTRACT["LoadCardNameToTxRam2_b"] = {"compare": (), "preserve": ()}
CASES["LoadCardNameToTxRam2_b"] = [
    {"wram": {0xCE3F: b"\x11\x22\xA5\x5A"}, "read": {0xCC27: 2}},
    dict(POISON, a=5, wram={0xCE3F: b"\x11\x22\xA5\x5A"}, read={0xCC27: 2}),
    {"a": 0x3B, "wram": {0xCE3F: b"\x11\x22\xA5\x5A"}, "read": {0xCC27: 2}},
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
	dict(POISON, hl=0xC100, wram={0xC156: b"\x00\x00\x00\x00"}, read={0xC156: 4}),
	dict(POISON, hl=0xC100, wram={0xC156: b"\x00\x00\x00\x00"}, read={0xC156: 4}),
	dict(POISON, hl=0xC100, wram={0xC156: b"\x00\x00\x00\x00"}, read={0xC156: 4}),
]
# <<< factory PrintCardPageRarityIcon

# >>> factory SetNoLineSeparation
CONTRACT["SetNoLineSeparation"] = {"compare": ("a",), "preserve": ()}
CASES["SetNoLineSeparation"] = [
	{"wram": {0xCD08: b"\x00"}, "read": {0xCD08: 1}},
	dict(POISON, wram={0xCD08: b"\xff"}, read={0xCD08: 1}),
]
# <<< factory SetNoLineSeparation

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
    "before": "\treturn CardPageSwitch_00();\n}",
    "after": "\treturn (CardPageResult){0u, 0u};\n}",
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
    "before": "\twTxRam2_b = wLoadedCard1Name;",
    "after": "\twTxRam2 = wLoadedCard1Name;",
    "case_ids": ["LoadCardNameToTxRam2_b-0", "LoadCardNameToTxRam2_b-1", "LoadCardNameToTxRam2_b-2"],
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
MUTATIONS["DiscardRetreatCostCards"] = {"source_symbol": "DiscardRetreatCostCards", "before": "hl = (uint16_t)(hl + 1u);", "after": "hl = (uint16_t)(hl + 2u);", "case_ids": ["DiscardRetreatCostCards-0", "DiscardRetreatCostCards-1", "DiscardRetreatCostCards-2"]}
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
	"after": "SetLineSeparation(2u);",
	"case_ids": ["SetNoLineSeparation-0", "SetNoLineSeparation-1"],
}
# <<< factory-mutation SetNoLineSeparation
