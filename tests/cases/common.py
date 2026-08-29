"""Oracle-diff cases for poketcg/src/engine/duel/ai/common.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory CountOppEnergyCardsInHand
CONTRACT["CountOppEnergyCardsInHand"] = {"compare": ("a", "f", "b"), "preserve": ()}
CASES["CountOppEnergyCardsInHand"] = [
    {"wram": {0xC510: b"\xff" + b"\x00" * 31}, "read": {0xC510: 32}},
    {"a": 1, "wram": {0xC510: b"\xff" + b"\x00" * 31}, "read": {0xC510: 32}},
    {"a": 0xFF, "wram": {0xC510: b"\x01\x02\xff" + b"\x00" * 29}, "read": {0xC510: 32}},
    dict(POISON, wram={0xC510: b"\xff" + b"\x00" * 31}, read={0xC510: 32}),
]
# <<< factory CountOppEnergyCardsInHand

# >>> factory ConvertHPToDamageCounters_Bank8
CONTRACT["ConvertHPToDamageCounters_Bank8"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ConvertHPToDamageCounters_Bank8"] = [
    {"a": 0},
    {"a": 1},
    {"a": 9},
    {"a": 10},
    {"a": 11},
    {"a": 100},
    {"a": 255},
    dict(POISON, a=70),
]
# <<< factory ConvertHPToDamageCounters_Bank8

# >>> factory CalculateWordTensDigit
CONTRACT["CalculateWordTensDigit"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e")}
CASES["CalculateWordTensDigit"] = [
    {"hl": 0},
    {"hl": 1},
    {"hl": 9},
    {"hl": 10},
    {"hl": 99},
    {"hl": 100},
    {"hl": 0x0100},
    {"hl": 0x7FFF},
    {"hl": 0xFFFF},
    dict(POISON, hl=250),
]
# <<< factory CalculateWordTensDigit

# >>> factory PickTwoAttachedEnergyCards
CONTRACT["PickTwoAttachedEnergyCards"] = {"compare": ("a",), "preserve": ()}
CASES["PickTwoAttachedEnergyCards"] = [
    {"a": 0, "read": {0xCDF1: 2, 0xCDB9: 2, 0xC510: 8}},
    {"a": 1, "read": {0xCDF1: 2, 0xCDB9: 2, 0xC510: 8}},
    {"a": 5, "read": {0xCDF1: 2, 0xCDB9: 2, 0xC510: 8}},
    dict(POISON, a=0, read={0xCDF1: 2, 0xCDB9: 2, 0xC510: 8}),
    dict(POISON, a=2, read={0xCDF1: 2, 0xCDB9: 2, 0xC510: 8}),
]
# <<< factory PickTwoAttachedEnergyCards

# >>> factory ClearMemory_Bank8
CONTRACT["ClearMemory_Bank8"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["ClearMemory_Bank8"] = [
    {"a": 0, "hl": 0xC100, "wram": {0xC100: b"\xaa" * 256}, "read": {0xC100: 260}},
    {"a": 1, "hl": 0xC200, "wram": {0xC200: b"\xaa\xaa\xaa"}, "read": {0xC200: 4}},
    {"a": 5, "hl": 0xC300, "wram": {0xC300: b"\xaa" * 8}, "read": {0xC300: 8}},
    dict(POISON, a=0, hl=0xC400, wram={0xC400: b"\xaa" * 256}, read={0xC400: 260}),
    dict(POISON, a=3, hl=0xC600, wram={0xC600: b"\xaa" * 8}, read={0xC600: 8}),
]
# <<< factory ClearMemory_Bank8

# >>> factory PickAttachedEnergyCardToRemove
CONTRACT["PickAttachedEnergyCardToRemove"] = {"compare": ("a",), "preserve": ()}
CASES["PickAttachedEnergyCardToRemove"] = [
    {"a": 0, "wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, "read": {0xC200: 60, 0xC510: 32}},
    {"a": 1, "wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, "read": {0xC200: 60, 0xC510: 32}},
    {"a": 5, "wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, "read": {0xC200: 60, 0xC510: 32}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, "read": {0xC200: 60, 0xC510: 32}},
]
# <<< factory PickAttachedEnergyCardToRemove

# >>> factory CopyListWithFFTerminatorFromHLToDE_Bank8
CONTRACT["CopyListWithFFTerminatorFromHLToDE_Bank8"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["CopyListWithFFTerminatorFromHLToDE_Bank8"] = [
    {"hl": 0xC100, "d": 0xC2, "e": 0x00, "wram": {0xC100: b"\xFF"}, "read": {0xC100: 1, 0xC200: 1}},
    dict(POISON, hl=0xC100, d=0xC2, e=0x00, wram={0xC100: b"\x01\x02\xFF"}, read={0xC100: 3, 0xC200: 3}),
    {"hl": 0xC1FF, "d": 0xC2, "e": 0xFF, "wram": {0xC1FF: b"\x01\xFF"}, "read": {0xC1FF: 2, 0xC2FF: 2}},
]
# <<< factory CopyListWithFFTerminatorFromHLToDE_Bank8

# >>> factory LookForCardIDInPlayArea_Bank8
CONTRACT["LookForCardIDInPlayArea_Bank8"] = {"compare": ("a", "f", "b", "d", "e"), "preserve": ("d", "e")}
CASES["LookForCardIDInPlayArea_Bank8"] = [
    {"a": 0, "b": 0},
    {"a": 1, "b": 0},
    {"a": 0x08, "b": 3},
    {"a": 0x20, "b": 5},
    {"a": 0xFF, "b": 0},
    dict(POISON, a=0x08, b=0),
]
# <<< factory LookForCardIDInPlayArea_Bank8

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400

wDuelTempList = 0xC510
wTempAI = 0xCDF1
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC27E

_CASE_WRAM_EMPTY = {
    hWhoseTurn: b"\xC2",
    0xC200: b"\x00" * 0x3C,
    wPlayerDeck: b"\x00" * 0x3C,
    wDuelTempList: b"\x00" * 0x40,
}
_CASE_WRAM_MATCH = {
    hWhoseTurn: b"\xC2",
    0xC200: b"\x01\x00\x01\x00\x01" + b"\x00" * 0x37,
    wPlayerDeck: b"\x01\x00\x06\x00\x07" + b"\x00" * 0x37,
    wDuelTempList: b"\x00" * 0x40,
}

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wLoadedCard2Type = 0xCC65
wLoadedCard2ID = 0xCC6C
DECK_SIZE = 60
MEWTWO_LV53 = 0x9D
BULBASAUR = 0x08

hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
wTempAIPokemonCard = 0xCDF3

hWhoseTurn = 0xFF97
sCardCollection = 0xA100
sDeck1 = 0xA200
wOpponentDeck = 0xC480
wPlayerDeck = 0xC400

hWhoseTurn = 0xFF97
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
wTempAI = 0xCDF1
wDuelTempList = 0xC510
IVYSAUR = 0x09

wAIBarrierFlagCounter = 0xCDA7

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wAIBarrierFlagCounter = 0xCDA7
wAIExecuteProcessedAttack = 0xCDD9
wAIScore = 0xCDBE
wTempPlayAreaAIScore = 0xCDDD
wPlayAreaAIScore = 0xCDBF
wTempAIScore = 0xCDE3

# Shared seeds for the PrintCardList wrapper cases: an empty card collection in
# SRAM bank 0 (0xA100 sCardCollection) plus four unnamed deck slots (0xA200
# sDeck1Name, 0xA254 sDeck2Name, 0xA2A8 sDeck3Name, 0xA2FC sDeck4Name) so the
# callee's CreateTempCardCollection .AddDeckCards pass walks all four and leaves
# wTempCardCollection all zero on both sides -- the same seeds the landed
# _PrintCardList cases in tests/cases/printer.py use.
_PRINT_CARD_LIST_WRAPPER_SRAM = {0: {0xA100: b"\x00" * 0x100, 0xA200: b"\x00",
                                     0xA254: b"\x00", 0xA2A8: b"\x00",
                                     0xA2FC: b"\x00"}}
_PRINT_CARD_LIST_WRAPPER_SETUP = [{"fn": "CopyDMAFunction"},
                                  {"fn": "SetupText", "d": 0x20, "e": 0x40}]

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = 0xCAB4
hWhoseTurn = 0xFF97
wLCDC = 0xCABB
# <<< factory-cases-statics

# >>> factory CheckIfHasCardIDInHand
CONTRACT["CheckIfHasCardIDInHand"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfHasCardIDInHand"] = [
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 32}},
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01"}, "read": {0xC510: 32}},
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x02", 0xC242: b"\x00", 0xC243: b"\x01", 0xC200: b"\x00", 0xC201: b"\x00", wPlayerDeck: b"\x01\x01"}, "read": {0xC510: 32}},
    dict(POISON, a=0x01, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x02", 0xC242: b"\x00", 0xC243: b"\x01", 0xC200: b"\x00", 0xC201: b"\x00", wPlayerDeck: b"\x01\x01"}, read={0xC510: 32}),
]
# <<< factory CheckIfHasCardIDInHand

# >>> factory FindBasicEnergyCardsInLocation
CONTRACT["FindBasicEnergyCardsInLocation"] = {"compare": ("a", "f", "d", "e", "hl"), "preserve": ()}
CASES["FindBasicEnergyCardsInLocation"] = [
    {"a": 0x02, "wram": _CASE_WRAM_EMPTY, "read": {wDuelTempList: 0x40}},
    {"a": 0x01, "wram": _CASE_WRAM_MATCH, "read": {wDuelTempList: 0x03}},
    dict(POISON, a=0x01, wram=_CASE_WRAM_MATCH, read={wDuelTempList: 0x03}),
]
# <<< factory FindBasicEnergyCardsInLocation

# >>> factory CalculateBDividedByA_Bank8
CONTRACT["CalculateBDividedByA_Bank8"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CalculateBDividedByA_Bank8"] = [
	{"a": 0, "b": 0, "oracle": False, "why": "Divisor zero enters the assembly loop forever.", "expect_regs": {"a": 0, "b": 0}},
	{"a": 1, "b": 1},
	{"a": 1, "b": 255},
	{"a": 2, "b": 5},
	{"a": 255, "b": 255},
	dict(POISON, a=3, b=10),
]
# <<< factory CalculateBDividedByA_Bank8

# >>> factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53
CONTRACT["CheckIfPlayerHasPokemonOtherThanMewtwoLv53"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "hl")}
CASES["CheckIfPlayerHasPokemonOtherThanMewtwoLv53"] = [
    {"wram": {hWhoseTurn: b"\xC3", wPlayerDeck: bytes((BULBASAUR,))},
     "read": {hWhoseTurn: 1, wLoadedCard2Type: 1, wLoadedCard2ID: 1}},
    {"wram": {hWhoseTurn: b"\xC3", wPlayerDeck: bytes((MEWTWO_LV53,)) * DECK_SIZE},
     "read": {hWhoseTurn: 1, wLoadedCard2Type: 1, wLoadedCard2ID: 1}},
    dict(POISON,
         wram={hWhoseTurn: b"\xC3", wPlayerDeck: bytes((MEWTWO_LV53,)) * DECK_SIZE},
         read={hWhoseTurn: 1, wLoadedCard2Type: 1, wLoadedCard2ID: 1}),
]
# <<< factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53

# >>> factory RemoveFromListDifferentCardOfGivenType
CONTRACT["RemoveFromListDifferentCardOfGivenType"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["RemoveFromListDifferentCardOfGivenType"] = [
    {"b": 0x11, "c": 0x22, "d": 0x00, "e": 0xAA, "hl": 0xC510,
     "wram": {0xC510: b"\xFF"}},
    dict(POISON, d=0x00, e=0xAA, hl=0xC510,
         wram={0xC510: b"\xFF"}),
    {"b": 0x11, "c": 0x22, "d": 0x02, "e": 0xAA, "hl": 0xC510,
     "wram": {0xFF97: b"\xC2", 0xC400: b"\x01", 0xC510: b"\x00\xFF"}},
]
# <<< factory RemoveFromListDifferentCardOfGivenType

# >>> factory CountPokemonCardsInHandAndInPlayArea
CONTRACT["CountPokemonCardsInHandAndInPlayArea"] = {"compare": ("a",), "preserve": (), "wram_out": True}
CASES["CountPokemonCardsInHandAndInPlayArea"] = [
    {"c": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2EF: b"\x03"}, "read": {wTempAI: 1}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2EF: b"\x03"}, read={wTempAI: 1}),
]
# <<< factory CountPokemonCardsInHandAndInPlayArea

# >>> factory LookForCardIDInLocation_Bank8
hWhoseTurn = 0xFF97
wPlayerDeck = 0xC400
_LOCATIONS_SEED = {0xC200 + i: b"\x00" for i in range(60)}
_LOCATIONS_SEED[0xC205] = b"\x10"
_BASE_WRAM = {**_LOCATIONS_SEED, hWhoseTurn: b"\xC2", wPlayerDeck + 5: b"\x2A"}
CONTRACT["LookForCardIDInLocation_Bank8"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDInLocation_Bank8"] = [
    {"a": 0x10, "e": 0x2A, "wram": _BASE_WRAM},
    dict(POISON, a=0x10, e=0x99, wram=_BASE_WRAM),
]
# <<< factory LookForCardIDInLocation_Bank8

# >>> factory LookForCardIDInHandList_Bank8
CONTRACT["LookForCardIDInHandList_Bank8"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDInHandList_Bank8"] = [
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 32}},
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01"}, "read": {0xC510: 32}},
    dict(POISON, a=0x01, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01"}, read={0xC510: 32}),
]
# <<< factory LookForCardIDInHandList_Bank8

# >>> factory LookForCardIDInHandAndPlayArea
CONTRACT["LookForCardIDInHandAndPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDInHandAndPlayArea"] = [
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01", 0xC2BB: b"\xFF"}, "read": {0xC510: 32}},
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, "read": {0xC510: 32}},
    dict(POISON, a=0x01, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01", 0xC2BB: b"\xFF"}, read={0xC510: 32}),
]
# <<< factory LookForCardIDInHandAndPlayArea

# >>> factory LookForCardIDToTradeWithDifferentHandCard
CONTRACT["LookForCardIDToTradeWithDifferentHandCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDToTradeWithDifferentHandCard"] = [
    {"a": 0x01, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01"}, "read": {0xC510: 32}},
    {"a": 0xAB, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}},
    {"a": 0x00, "e": 0x00, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 32}},
    {"a": 0x00, "e": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x01", 0xC200: b"\x00", 0xC401: b"\x01"}, "read": {0xC510: 32}},
    dict(POISON, a=0x01, e=0x00, wram={hWhoseTurn: b"\xC2", 0xC2EE: b"\x01", 0xC242: b"\x00", 0xC200: b"\x00", wPlayerDeck: b"\x01"}, read={0xC510: 32}),
]
# <<< factory LookForCardIDToTradeWithDifferentHandCard

# >>> factory LookForCardIDInDeck_GivenCardIDInHand
CONTRACT["LookForCardIDInDeck_GivenCardIDInHand"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDInDeck_GivenCardIDInHand"] = [
    {"a": 0xAB, "b": 0x01, "wram": {hWhoseTurn: b"\xC2"}},
    {"a": 0x00, "b": 0xAB, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00"}, "read": {0xC510: 32}},
    {"a": 0x00, "b": 0x01, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x03",
        0xC200: b"\x00",
        0xC403: b"\x01",
        0xC2BB: b"\xFF",
    }, "read": {0xC510: 32}},
    dict(POISON, a=0x00, b=0x01, wram={
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x03",
        0xC200: b"\x00",
        0xC403: b"\x01",
        0xC2BB: b"\xFF",
    }, read={0xC510: 32}),
]
# <<< factory LookForCardIDInDeck_GivenCardIDInHand

# >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea
CONTRACT["LookForCardIDInDeck_GivenCardIDInHandAndPlayArea"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LookForCardIDInDeck_GivenCardIDInHandAndPlayArea"] = [
    {"a": 0xAB, "b": 0x01, "wram": {hWhoseTurn: b"\xC2"}},
    {"a": 0x00, "b": 0xAB, "wram": {hWhoseTurn: b"\xC2", 0xC2EE: b"\x00", 0xC2BB: b"\xFF"}, "read": {0xC510: 32}},
    {"a": 0x00, "b": 0x01, "wram": {
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x03",
        0xC200: b"\x00",
        0xC403: b"\x01",
        0xC2BB: b"\xFF",
    }, "read": {0xC510: 32}},
    dict(POISON, a=0x00, b=0x01, wram={
        hWhoseTurn: b"\xC2",
        0xC2EE: b"\x01",
        0xC242: b"\x03",
        0xC200: b"\x00",
        0xC403: b"\x01",
        0xC2BB: b"\xFF",
    }, read={0xC510: 32}),
]
# <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea

# >>> factory AddStarterDeck
CONTRACT["AddStarterDeck"] = {"compare": (), "preserve": ()}
CASES["AddStarterDeck"] = [
    {"a": 0x00, "wram": {hWhoseTurn: b"\xFF", wPlayerDeck: bytes(range(60)), wOpponentDeck: bytes(range(60, 90))},
     "sram": {0: {sCardCollection: bytes([0x80] * 256)}},
     "read": {hWhoseTurn: 1},
     "sread": {0: {sCardCollection: 256, sDeck1: 32}}},
    dict(POISON, a=0x01, wram={hWhoseTurn: b"\xFF", wPlayerDeck: bytes(range(60)), wOpponentDeck: bytes(range(60, 90))},
         sram={0: {sCardCollection: bytes([0x80] * 256)}},
         read={hWhoseTurn: 1},
         sread={0: {sCardCollection: 256, sDeck1: 32}}),
]
# <<< factory AddStarterDeck

# >>> factory FindDuplicatePokemonCards
CONTRACT["FindDuplicatePokemonCards"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["FindDuplicatePokemonCards"] = [
    {"wram": {hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x02",
              wPlayerDuelVariables + 0x42: bytes((5, 6)),
              wPlayerDuelVariables + 5: b"\x00", wPlayerDuelVariables + 6: b"\x00",
              wPlayerDeck + 5: bytes((IVYSAUR,)), wPlayerDeck + 6: bytes((IVYSAUR,))},
     "read": {wTempAI: 1, wDuelTempList: 3}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", wPlayerDuelVariables + 0xEE: b"\x01",
                       wPlayerDuelVariables + 0x42: bytes((5,)),
                       wPlayerDuelVariables + 5: b"\x00",
                       wPlayerDeck + 5: bytes((IVYSAUR,))},
         read={wTempAI: 1, wDuelTempList: 2}),
]
# <<< factory FindDuplicatePokemonCards

# >>> factory AIPickEnergyCardToDiscard
CONTRACT["AIPickEnergyCardToDiscard"] = {"compare": ("a",), "preserve": ()}
CASES["AIPickEnergyCardToDiscard"] = [
    {"a": 0, "wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, "read": {0xC510: 32}},
    {"a": 3, "wram": {0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, "read": {0xC510: 32}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC200: b"\x00" * 60}, read={0xC510: 32}),
]
# <<< factory AIPickEnergyCardToDiscard

# >>> factory HandleAIAntiMewtwoDeckStrategy
CONTRACT["HandleAIAntiMewtwoDeckStrategy"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleAIAntiMewtwoDeckStrategy"] = [
    {"wram": {wAIBarrierFlagCounter: b"\x00"}, "sram": {0: {}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"wram": {wAIBarrierFlagCounter: b"\x00"}, "sram": {0: {}}, "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "instruction_budget": 2000000, "cycle_budget": 8000000},
]
# <<< factory HandleAIAntiMewtwoDeckStrategy

# >>> factory OpenBoosterPack
CONTRACT["OpenBoosterPack"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["OpenBoosterPack"] = [
    {"wram": {0xC200: b"\xAA" * 0x3C, 0xC400: b"\x00", 0xCABB: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x02], "read": {0xFF97: 1, 0xC200: 0x3C, 0xC510: 1, 0xCBD6: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={0xC200: b"\xAA" * 0x3C, 0xC400: b"\x00", 0xCABB: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x02], read={0xFF97: 1, 0xC200: 0x3C, 0xC510: 1, 0xCBD6: 1}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory OpenBoosterPack

# >>> factory PreparePrinterConnection
# The reference never returns from here: the farcall reaches
# _PreparePrinterConnection, whose SendPrinterPacket parks in the
# .wait_printer_packet_transmission DoFrame loop ($315D) because no printer
# hardware raises the serial interrupt that advances wPrinterPacketSequence.
# Completion is therefore declared pre-ret at that loop head in the
# factory-completion block at the end of this module, exactly as the landed
# _PreparePrinterConnection cases in tests/cases/printer.py do. That is the
# genuine spin, not a small budget, so the generous budgets below only cover
# the reference's walk down to the loop head.
#
# Registers are mid-flight on the reference at that stop, so nothing is
# compared. The observed bytes are the ones both sides agree on:
# wPrinterPacketDataPtr ($CE6A), which SendPrinterPacket writes from hl before
# the wait and neither side rewrites, plus the two seeded serial bytes
# wSerialTransferData ($CE6E) and wPrinterStatus ($CE6F). $81 is the device
# number the packet engine expects, so the port's synchronous state machine
# writes it straight back, and a zero status clears the error nibble, so the
# port takes the `ret nc` exit without touching wPrinterStatus again -- no
# scene, no text box, no frames.
CONTRACT["PreparePrinterConnection"] = {"compare": (), "preserve": ()}
CASES["PreparePrinterConnection"] = [
    {"hl": 0xC100,
     "wram": {0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "read": {0xCE6A: 2},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON,
         wram={0xCE6E: b"\x81", 0xCE6F: b"\x00"},
         read={0xCE6A: 2},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory PreparePrinterConnection

# >>> factory AICheckIfAttackIsHighRecoil
CONTRACT["AICheckIfAttackIsHighRecoil"] = {"compare": ("f",), "preserve": ()}
CASES["AICheckIfAttackIsHighRecoil"] = [
    {"wram": {wAIBarrierFlagCounter: b"\x80", wAIExecuteProcessedAttack: b"\x00", wAIScore: b"\x10", wTempAIScore: b"\x00", wPlayAreaAIScore: b"\x01\x02\x03\x04\x05\x06", wTempPlayAreaAIScore: b"\x00\x00\x00\x00\x00\x00"}, "expect": {wAIExecuteProcessedAttack: b"\x01"}, "expect_regs": {"f": 0x00}, "read": {wAIExecuteProcessedAttack: 1}},
    {"wram": {wAIBarrierFlagCounter: b"\x80", wAIExecuteProcessedAttack: b"\xff", wAIScore: b"\x7f", wTempAIScore: b"\x00", wPlayAreaAIScore: b"\x20\x30\x40\x50\x60\x70", wTempPlayAreaAIScore: b"\xaa\xbb\xcc\xdd\xee\xff"}, "expect": {wAIExecuteProcessedAttack: b"\x01"}, "expect_regs": {"f": 0x00}, "read": {wAIExecuteProcessedAttack: 1}},
    dict(POISON, wram={wAIBarrierFlagCounter: b"\x80", wAIExecuteProcessedAttack: b"\xaa", wAIScore: b"\xbb", wTempAIScore: b"\xcc", wPlayAreaAIScore: b"\x01\x23\x45\x67\x89\xab", wTempPlayAreaAIScore: b"\xde\xad\xbe\xef\x10\x20"}, expect={wAIExecuteProcessedAttack: b"\x01"}, expect_regs={"f": 0x00}, read={wAIExecuteProcessedAttack: 1}),
]
# <<< factory AICheckIfAttackIsHighRecoil

# >>> factory PrintDeckConfiguration
CONTRACT["PrintDeckConfiguration"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintDeckConfiguration"] = [{"a": 0x00, "wram": {0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00", 0xCE92: b"\xFF\xFF", 0xCE9C: b"\xFF", 0xCF17: b"\x00"}, "sram": {0: {0xA350: b"\x00" * 0x53 + b"\xA5"}}, "ramg": True, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": 0x00, "read": {0xC510: 0x54, 0xCE92: 2, 0xCE9C: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000}, dict(POISON, a=0x00, wram={0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00", 0xCE92: b"\xFF\xFF", 0xCE9C: b"\xFF", 0xCF17: b"\x00"}, sram={0: {0xA350: b"\x00" * 0x53 + b"\xA5"}}, ramg=True, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=0x00, read={0xC510: 0x54, 0xCE92: 2, 0xCE9C: 1}, instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory PrintDeckConfiguration

# >>> factory ShowPromotionalCardScreen
# Same shape as the landed _ShowPromotionalCardScreen cases in
# tests/cases/promotional_card.py, because this wrapper is nothing but the
# farcall to it. a != 0 in both cases: with a == 0 the ROM re-enters its own
# tail four times and the pre-ret stop below would land on the first pass, so
# the legendary branch is not comparable at this completion point. 0x1E is
# VILEPLUME; POISON's 0xAA takes the promotional fallback. keys=[0x00, 0x02]
# taps B, which is what WaitForWideTextBoxInput reads inside
# _DisplayCardDetailScreen. CopyDMAFunction installs hDMAFunction for the VBlank
# handler; the callee calls SetupText itself, so no second setup entry is
# needed. The observed bytes are the two the asm writes before the wait: the
# wLoadedCard1Name pointer ($CC27) that LoadCardDataToBuffer1_FromCardID fills
# in, and hWhoseTurn ($FF97), set to PLAYER_TURN.
CONTRACT["ShowPromotionalCardScreen"] = {"compare": (), "preserve": ()}
CASES["ShowPromotionalCardScreen"] = [
    {"a": 0x1E, "keys": [0x00, 0x02],
     "read": {0xCC27: 2, 0xFF97: 1},
     "setup": [{"fn": "CopyDMAFunction"}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02],
         read={0xCC27: 2, 0xFF97: 1},
         setup=[{"fn": "CopyDMAFunction"}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ShowPromotionalCardScreen

# >>> factory RequestToPrintCard
# The reference never returns from here: the farcall reaches
# _RequestToPrintCard, whose Func_19f87 path reaches
# TryInitPrinterCommunications, and that first packet parks in
# SendPrinterPacket's .wait_printer_packet_transmission DoFrame loop ($315D)
# because no printer hardware raises the serial interrupt that advances
# wPrinterPacketSequence. Completion is therefore declared pre-ret at that loop
# head in the factory-completion block at the end of this module, exactly as the
# landed _RequestToPrintCard cases in tests/cases/printer.py and the landed
# PreparePrinterConnection wrapper cases here do. That is the genuine spin, not
# a small budget, so the generous budgets below only cover the reference's walk
# down to the loop head.
#
# Registers are mid-flight on the reference at that stop, so nothing is
# compared. The observed bytes are wLoadedCard1's type/gfx/name/HP/level, which
# LoadCardDataToBuffer1_FromCardID writes from the entry card id at the callee's
# very first instruction and which nothing on either side rewrites afterwards.
# The seeded serial bytes agree too: $81 is the device number the port's
# synchronous packet engine writes straight back, and a zero status keeps it off
# every error path. wLCDC ($CABB) starts clear so the text box before EnableLCD
# stays out of WaitForVBlank's halt; CopyDMAFunction installs hDMAFunction for
# the frames that elapse after EnableLCD.
CONTRACT["RequestToPrintCard"] = {"compare": (), "preserve": ()}
CASES["RequestToPrintCard"] = [
    {"a": 0x01,
     "wram": {0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": 0x00,
     "read": {0xCC24: 5, 0xCC2C: 1, 0xCC5D: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=0x00,
         read={0xCC24: 5, 0xCC2C: 1, 0xCC5D: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory RequestToPrintCard

# >>> factory PrintCardList
# The reference never returns from here: the farcall reaches _PrintCardList,
# whose card loop reaches its seventh new card type with
# wPrinterHorizontalOffset at 19, so AddToPrinterGfxBuffer falls into
# LoadGfxBufferForPrinter, whose TryInitPrinterCommunications parks in
# SendPrinterPacket's .wait_printer_packet_transmission DoFrame loop ($315D)
# because no printer hardware raises the serial interrupt that advances
# wPrinterPacketSequence. Completion is therefore declared pre-ret at that loop
# head in the factory-completion block at the end of this module, exactly as the
# landed PreparePrinterConnection and RequestToPrintCard wrapper cases here do.
# That is the genuine spin, not a small budget, so the generous budgets below
# only cover the reference's walk down to the loop head.
#
# Registers are mid-flight on the reference at that stop, so nothing is
# compared. The observed bytes are the ones the callee writes before the stop
# and never rewrites afterwards, so the port's full run agrees with the
# reference's partial one:
#   $FF97 hWhoseTurn             - PLAYER_TURN, written once before the loop
#   $CE91 wPrinterCardCount      - the collection slot of the card being
#                                  examined; the seeded collection is empty, so
#                                  every iteration writes 0 on both sides
#   $CE92 wPrinterTotalCardCount - zeroed before the loop and only advanced by
#                                  owned cards, of which there are none
#   $CE97 wPrinterNumCardTypes   - same, and only on the all-owned path
#   $CE9C wPrintOnlyStarRarity   - the SELECT decision, written once at entry
# Every one of those is seeded to $FF first so the write itself is witnessed.
# wCurPrinterCardType ($CE94) and wPrinterHorizontalOffset ($CE90) are NOT
# observed: they keep moving past the reference's stop.
#
# wLCDC ($CABB) starts clear so the text boxes before ShowPrinterTransmitting's
# EnableLCD stay out of WaitForVBlank's halt; CopyDMAFunction installs
# hDMAFunction for the frames that elapse afterwards and SetupText primes the
# glyph cache. $81 in wSerialTransferData ($CE6E) is the device number the
# port's synchronous packet engine writes straight back, and a zero
# wPrinterStatus ($CE6F) keeps both sides off every error path.
#
# Both cases release SELECT (hKeysHeld $FF90 seeded 0, keys=0x00), so both take
# the callee's all-owned mode. The star-rarity branch is deliberately not
# exercised through this wrapper: with SELECT held the callee prints every Star
# card of the empty collection, and at the $315D stop the reference and the port
# disagree inside the implicitly compared sCardCollection seed span -- the
# oracle measured bank 0 $A1F0 as $2D/$00/$20 on the reference against zeroes
# natively. That divergence is the callee's own SRAM behaviour, not this
# wrapper's, and _PrintCardList carries its own star-mode case in
# tests/cases/printer.py. The wrapper's contract is the farcall's register
# transparency, which the poisoned second case below covers on the mode both
# sides agree on.
CONTRACT["PrintCardList"] = {"compare": (), "preserve": ()}
CASES["PrintCardList"] = [
    {"wram": {0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00",
              0xCE91: b"\xFF", 0xCE92: b"\xFF\xFF", 0xCE97: b"\xFF",
              0xCE9C: b"\xFF", 0xFF90: b"\x00", 0xFF97: b"\x00"},
     "sram": _PRINT_CARD_LIST_WRAPPER_SRAM,
     "ramg": True,
     "setup": _PRINT_CARD_LIST_WRAPPER_SETUP,
     "keys": 0x00,
     "read": {0xCE91: 1, 0xCE92: 2, 0xCE97: 1, 0xCE9C: 1, 0xFF97: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00",
               0xCE91: b"\xFF", 0xCE92: b"\xFF\xFF", 0xCE97: b"\xFF",
               0xCE9C: b"\xFF", 0xFF90: b"\x00", 0xFF97: b"\x00"},
         sram=_PRINT_CARD_LIST_WRAPPER_SRAM,
         ramg=True,
         setup=_PRINT_CARD_LIST_WRAPPER_SETUP,
         keys=0x00,
         read={0xCE91: 1, 0xCE92: 2, 0xCE97: 1, 0xCE9C: 1, 0xFF97: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrintCardList

# >>> factory ReceiveCard
CONTRACT["ReceiveCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ReceiveCard"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block is observed.", "keys": [0x82, 0x10, 0x01], "wram": {0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC5EB: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC5EB: 4}, "expect": {0xC5EB: b"\x02\x4F\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block is observed.", "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x82, 0x10, 0x01], "wram": {0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC5EB: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC5EB: 4}, "expect": {0xC5EB: b"\x02\x4F\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory ReceiveCard

# >>> factory ReceiveDeckConfiguration
CONTRACT["ReceiveDeckConfiguration"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ReceiveDeckConfiguration"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block and carry return are asserted.", "keys": [0x82, 0x10, 0x01], "wram": {0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC5EB: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC5EB: 4}, "expect": {0xC5EB: b"\x02\x4F\x4B\x31"}, "expect_regs": {"a": 0x01, "f": 0x90}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block and carry return are asserted.", "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "keys": [0x82, 0x10, 0x01], "wram": {0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC5EB: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {0xC5EB: 4}, "expect": {0xC5EB: b"\x02\x4F\x4B\x31"}, "expect_regs": {"a": 0x01, "f": 0x90}, "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory ReceiveDeckConfiguration

# >>> factory DoCardPop
CONTRACT["DoCardPop"] = {"compare": (), "preserve": ()}
CASES["DoCardPop"] = [
    {"oracle": False, "evidence": "primary", "why": "The SGB guard deterministically takes Card Pop!'s error-screen path without requiring infrared hardware; the seeded turn byte verifies that the communication branch is not entered.", "wram": {wConsole: b"\x01", hWhoseTurn: b"\x00", wLCDC: b"\x00"}, "keys": [0x00, 0x01], "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {hWhoseTurn: 1}, "expect": {hWhoseTurn: b"\x00"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The SGB guard deterministically takes Card Pop!'s error-screen path without requiring infrared hardware; poisoned entry registers must not alter the turn byte.", wram={wConsole: b"\x01", hWhoseTurn: b"\x00", wLCDC: b"\x00"}, keys=[0x00, 0x01], setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={hWhoseTurn: 1}, expect={hWhoseTurn: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DoCardPop

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation CountOppEnergyCardsInHand
MUTATIONS["CountOppEnergyCardsInHand"] = {
    "source_symbol": "CountOppEnergyCardsInHand",
    "before": "\tif (r.f & F_C)",
    "after": "\tif (r.f & 0x20u)",
    "case_ids": ["CountOppEnergyCardsInHand-0", "CountOppEnergyCardsInHand-1", "CountOppEnergyCardsInHand-3"],
}
# <<< factory-mutation CountOppEnergyCardsInHand
# >>> factory-mutation ConvertHPToDamageCounters_Bank8
MUTATIONS["ConvertHPToDamageCounters_Bank8"] = {
    "source_symbol": "ConvertHPToDamageCounters_Bank8",
    "before": "\treturn (uint8_t)(a / 10u);",
    "after": "\treturn (uint8_t)(a / 5u);",
    "case_ids": ["ConvertHPToDamageCounters_Bank8-3", "ConvertHPToDamageCounters_Bank8-5", "ConvertHPToDamageCounters_Bank8-6"],
}
# <<< factory-mutation ConvertHPToDamageCounters_Bank8
# >>> factory-mutation CalculateWordTensDigit
MUTATIONS["CalculateWordTensDigit"] = {
    "source_symbol": "CalculateWordTensDigit",
    "before": "\treturn (uint16_t)(hl / 10u);",
    "after": "\treturn (uint16_t)(hl / 100u);",
    "case_ids": ["CalculateWordTensDigit-3", "CalculateWordTensDigit-4", "CalculateWordTensDigit-8"],
}
# <<< factory-mutation CalculateWordTensDigit
# >>> factory-mutation PickTwoAttachedEnergyCards
MUTATIONS["PickTwoAttachedEnergyCards"] = {
    "source_symbol": "PickTwoAttachedEnergyCards",
    "before": "\t\treturn (PickTwoResult){0xffu, 0u, 0u};",
    "after": "\t\treturn (PickTwoResult){0xfeu, 0u, 0u};",
    "case_ids": ["PickTwoAttachedEnergyCards-0", "PickTwoAttachedEnergyCards-1", "PickTwoAttachedEnergyCards-2", "PickTwoAttachedEnergyCards-3", "PickTwoAttachedEnergyCards-4"],
}
# <<< factory-mutation PickTwoAttachedEnergyCards
# >>> factory-mutation ClearMemory_Bank8
MUTATIONS["ClearMemory_Bank8"] = {
    "source_symbol": "ClearMemory_Bank8",
    "before": "\tuint32_t n = a ? (uint32_t)a : 0x100u;",
    "after": "\tuint32_t n = (uint32_t)a;",
    "case_ids": ["ClearMemory_Bank8-0", "ClearMemory_Bank8-3"],
}
# <<< factory-mutation ClearMemory_Bank8
# >>> factory-mutation PickAttachedEnergyCardToRemove
MUTATIONS["PickAttachedEnergyCardToRemove"] = {"source_symbol": "PickAttachedEnergyCardToRemove", "before": "\t\treturn 0xffu;", "after": "\t\treturn 0xfeu;", "case_ids": ["PickAttachedEnergyCardToRemove-0", "PickAttachedEnergyCardToRemove-1", "PickAttachedEnergyCardToRemove-2", "PickAttachedEnergyCardToRemove-3"]}
# <<< factory-mutation PickAttachedEnergyCardToRemove
# >>> factory-mutation CopyListWithFFTerminatorFromHLToDE_Bank8
MUTATIONS["CopyListWithFFTerminatorFromHLToDE_Bank8"] = {"source_symbol": "CopyListWithFFTerminatorFromHLToDE_Bank8", "before": "\t\tif (a == 0xFFu)", "after": "\t\tif (a == 0xFEu)", "case_ids": ["CopyListWithFFTerminatorFromHLToDE_Bank8-0", "CopyListWithFFTerminatorFromHLToDE_Bank8-1", "CopyListWithFFTerminatorFromHLToDE_Bank8-2"]}
# <<< factory-mutation CopyListWithFFTerminatorFromHLToDE_Bank8
# >>> factory-mutation LookForCardIDInPlayArea_Bank8
MUTATIONS["LookForCardIDInPlayArea_Bank8"] = {
    "source_symbol": "LookForCardIDInPlayArea_Bank8",
    "before": "\twTempCardIDToLook = a;",
    "after": "\twTempCardIDToLook = (uint8_t)(a + 1u);",
    "case_ids": ["LookForCardIDInPlayArea_Bank8-0", "LookForCardIDInPlayArea_Bank8-1", "LookForCardIDInPlayArea_Bank8-2", "LookForCardIDInPlayArea_Bank8-3", "LookForCardIDInPlayArea_Bank8-4", "LookForCardIDInPlayArea_Bank8-5"],
}
# <<< factory-mutation LookForCardIDInPlayArea_Bank8
# >>> factory-mutation CheckIfHasCardIDInHand
MUTATIONS["CheckIfHasCardIDInHand"] = {
    "source_symbol": "CheckIfHasCardIDInHand",
    "before": "\t\tif (count != 0u)",
    "after": "\t\tif (count == 0u)",
    "case_ids": ["CheckIfHasCardIDInHand-2", "CheckIfHasCardIDInHand-3"],
}
# <<< factory-mutation CheckIfHasCardIDInHand
# >>> factory-mutation FindBasicEnergyCardsInLocation
MUTATIONS["FindBasicEnergyCardsInLocation"] = {"source_symbol": "FindBasicEnergyCardsInLocation", "before": "\t\tgb_write8(hl++, e);", "after": "\t\tgb_write8(hl++, (uint8_t)(e + 1u));", "case_ids": ["FindBasicEnergyCardsInLocation-1", "FindBasicEnergyCardsInLocation-2"]}
# <<< factory-mutation FindBasicEnergyCardsInLocation
# >>> factory-mutation CalculateBDividedByA_Bank8
MUTATIONS["CalculateBDividedByA_Bank8"] = {"source_symbol": "CalculateBDividedByA_Bank8", "before": "\t\tuint8_t result = (uint8_t)(remainder - divisor);", "after": "\t\tuint8_t result = (uint8_t)(remainder + divisor);", "case_ids": ["CalculateBDividedByA_Bank8-1", "CalculateBDividedByA_Bank8-2", "CalculateBDividedByA_Bank8-3", "CalculateBDividedByA_Bank8-4", "CalculateBDividedByA_Bank8-5"]}
# <<< factory-mutation CalculateBDividedByA_Bank8
# >>> factory-mutation CheckIfPlayerHasPokemonOtherThanMewtwoLv53
MUTATIONS["CheckIfPlayerHasPokemonOtherThanMewtwoLv53"] = {"source_symbol": "CheckIfPlayerHasPokemonOtherThanMewtwoLv53", "before": "if (card_id != MEWTWO_LV53) {", "after": "if (card_id == MEWTWO_LV53) {", "case_ids": ["CheckIfPlayerHasPokemonOtherThanMewtwoLv53-0", "CheckIfPlayerHasPokemonOtherThanMewtwoLv53-2"]}
# <<< factory-mutation CheckIfPlayerHasPokemonOtherThanMewtwoLv53
# >>> factory-mutation RemoveFromListDifferentCardOfGivenType
MUTATIONS["RemoveFromListDifferentCardOfGivenType"] = {"source_symbol": "RemoveFromListDifferentCardOfGivenType", "before": "matches = (d == 0x02u);", "after": "matches = (d == 0x03u);", "case_ids": ["RemoveFromListDifferentCardOfGivenType-2"]}
# <<< factory-mutation RemoveFromListDifferentCardOfGivenType
# >>> factory-mutation CountPokemonCardsInHandAndInPlayArea
MUTATIONS["CountPokemonCardsInHandAndInPlayArea"] = {
    "source_symbol": "CountPokemonCardsInHandAndInPlayArea",
    "before": "GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;",
    "after": "GetTurnDuelistVariable((uint8_t)(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA + 1u)).a;",
    "case_ids": ["CountPokemonCardsInHandAndInPlayArea-0", "CountPokemonCardsInHandAndInPlayArea-1"],
}
# <<< factory-mutation CountPokemonCardsInHandAndInPlayArea
# >>> factory-mutation LookForCardIDInLocation_Bank8
MUTATIONS["LookForCardIDInLocation_Bank8"] = {
    "source_symbol": "LookForCardIDInLocation_Bank8",
    "before": "if (loc != location)",
    "after": "if (loc == location)",
    "case_ids": ["LookForCardIDInLocation_Bank8-0"],
}
# <<< factory-mutation LookForCardIDInLocation_Bank8
# >>> factory-mutation LookForCardIDInHandList_Bank8
MUTATIONS["LookForCardIDInHandList_Bank8"] = {"source_symbol": "LookForCardIDInHandList_Bank8", "before": "\t\t\treturn (LookForCardIDInHandListResult){hTempCardIndex_ff98, 0x90u};", "after": "\t\t\treturn (LookForCardIDInHandListResult){hTempCardIndex_ff98, 0x10u};", "case_ids": ["LookForCardIDInHandList_Bank8-1"]}
# <<< factory-mutation LookForCardIDInHandList_Bank8
# >>> factory-mutation LookForCardIDInHandAndPlayArea
MUTATIONS["LookForCardIDInHandAndPlayArea"] = {"source_symbol": "LookForCardIDInHandAndPlayArea", "before": "\tif (r1.f & 0x10u)", "after": "\tif (r1.f & 0x20u)", "case_ids": ["LookForCardIDInHandAndPlayArea-0"]}
# <<< factory-mutation LookForCardIDInHandAndPlayArea
# >>> factory-mutation LookForCardIDToTradeWithDifferentHandCard
MUTATIONS["LookForCardIDToTradeWithDifferentHandCard"] = {"source_symbol": "LookForCardIDToTradeWithDifferentHandCard", "before": "\tLookForCardIDInLocationBank8Result r2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, wTempAI);", "after": "\tLookForCardIDInLocationBank8Result r2 = LookForCardIDInLocation_Bank8((uint8_t)(CARD_LOCATION_DECK + 1u), wTempAI);", "case_ids": ["LookForCardIDToTradeWithDifferentHandCard-3"]}
# <<< factory-mutation LookForCardIDToTradeWithDifferentHandCard
# >>> factory-mutation LookForCardIDInDeck_GivenCardIDInHand
MUTATIONS["LookForCardIDInDeck_GivenCardIDInHand"] = {"source_symbol": "LookForCardIDInDeck_GivenCardIDInHand", "before": "\tuint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);", "after": "\tuint8_t f = (uint8_t)((r3.f & 0x80u) | 0x00u);", "case_ids": ["LookForCardIDInDeck_GivenCardIDInHand-2"]}
# <<< factory-mutation LookForCardIDInDeck_GivenCardIDInHand
# >>> factory-mutation LookForCardIDInDeck_GivenCardIDInHandAndPlayArea
MUTATIONS["LookForCardIDInDeck_GivenCardIDInHandAndPlayArea"] = {"source_symbol": "LookForCardIDInDeck_GivenCardIDInHandAndPlayArea", "before": '\tif (r3.f & 0x10u) {\n\t\tuint8_t f = (r3.a == 0u) ? 0x80u : 0u;\n\t\treturn (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r3.a, f};\n\t}\n\tuint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);', "after": '\tif (r3.f & 0x10u) {\n\t\tuint8_t f = (r3.a == 0u) ? 0x80u : 0u;\n\t\treturn (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r3.a, f};\n\t}\n\tuint8_t f = (uint8_t)((r3.f & 0x80u) | 0x00u);', "case_ids": ["LookForCardIDInDeck_GivenCardIDInHandAndPlayArea-2"]}
# <<< factory-mutation LookForCardIDInDeck_GivenCardIDInHandAndPlayArea
# >>> factory-mutation AddStarterDeck
MUTATIONS["AddStarterDeck"] = {"source_symbol": "AddStarterDeck", "before": "\t_AddStarterDeck(a);", "after": "\t_AddStarterDeck((uint8_t)(a + 1u));", "case_ids": ["AddStarterDeck-0", "AddStarterDeck-1"]}
# <<< factory-mutation AddStarterDeck
# >>> factory-mutation FindDuplicatePokemonCards
MUTATIONS["FindDuplicatePokemonCards"] = {"source_symbol": "FindDuplicatePokemonCards", "before": "wTempAI = inner_idx;", "after": "wTempAI = outer_idx;", "case_ids": ["FindDuplicatePokemonCards-0"]}
# <<< factory-mutation FindDuplicatePokemonCards
# >>> factory-mutation AIPickEnergyCardToDiscard
MUTATIONS["AIPickEnergyCardToDiscard"] = {"source_symbol": "AIPickEnergyCardToDiscard", "before": "if (total == 0u)\n\t\treturn 0xFFu;", "after": "if (total == 0u)\n\t\treturn 0xFEu;", "case_ids": ["AIPickEnergyCardToDiscard-0", "AIPickEnergyCardToDiscard-1"]}
# <<< factory-mutation AIPickEnergyCardToDiscard
# >>> factory-mutation HandleAIAntiMewtwoDeckStrategy
MUTATIONS["HandleAIAntiMewtwoDeckStrategy"] = {
    "source_symbol": "HandleAIAntiMewtwoDeckStrategy",
    "before": "\tf = (uint8_t)((f & 0x80u) | 0x10u);\n\treturn (HandleAIAntiMewtwoDeckStrategyResult){a, f};",
    "after": "\tf = (uint8_t)((f & 0x80u) | 0x00u);\n\treturn (HandleAIAntiMewtwoDeckStrategyResult){a, f};",
    "case_ids": ["HandleAIAntiMewtwoDeckStrategy-0", "HandleAIAntiMewtwoDeckStrategy-1"],
}
# <<< factory-mutation HandleAIAntiMewtwoDeckStrategy
# >>> factory-mutation OpenBoosterPack
MUTATIONS["OpenBoosterPack"] = {"source_symbol": "OpenBoosterPack", "before": "void OpenBoosterPack(void)\n{\n\t_OpenBoosterPack();", "after": "void OpenBoosterPack(void)\n{\n\t(void)0;", "case_ids": ["OpenBoosterPack-0", "OpenBoosterPack-1"]}
# <<< factory-mutation OpenBoosterPack
# >>> factory-mutation PreparePrinterConnection
MUTATIONS["PreparePrinterConnection"] = {
    "source_symbol": "PreparePrinterConnection",
    "before": "uint8_t PreparePrinterConnection(uint16_t hl)\n{\n\treturn _PreparePrinterConnection(hl).f;",
    "after": "uint8_t PreparePrinterConnection(uint16_t hl)\n{\n\treturn _PreparePrinterConnection((uint16_t)(hl + 1u)).f;",
    "case_ids": ["PreparePrinterConnection-0", "PreparePrinterConnection-1"],
}
# <<< factory-mutation PreparePrinterConnection
# >>> factory-completion PreparePrinterConnection
# $315D is SendPrinterPacket.wait_printer_packet_transmission (home/printer.asm,
# ROM0, so the capture hook is bank-independent), the DoFrame loop the reference
# can never leave without a printer answering on the serial line. The farcall
# wrapper inherits that spin from its callee. legacy_to_schema always emits
# completion "return", so the split is applied after migration.
for _record in SCHEMA2_CASES["PreparePrinterConnection"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion PreparePrinterConnection
# >>> factory-mutation AICheckIfAttackIsHighRecoil
MUTATIONS["AICheckIfAttackIsHighRecoil"] = {"source_symbol": "AICheckIfAttackIsHighRecoil", "before": "AIProcessAttacksResult processed = AIProcessButDontUseAttack();", "after": "AIProcessAttacksResult processed = AIProcessAttacks();", "case_ids": ["AICheckIfAttackIsHighRecoil-0", "AICheckIfAttackIsHighRecoil-1", "AICheckIfAttackIsHighRecoil-2"]}
# <<< factory-mutation AICheckIfAttackIsHighRecoil
# >>> factory-mutation PrintDeckConfiguration
MUTATIONS["PrintDeckConfiguration"] = {"source_symbol": "PrintDeckConfiguration", "before": "void PrintDeckConfiguration(uint8_t a)\n{\n\t_PrintDeckConfiguration(a);", "after": "void PrintDeckConfiguration(uint8_t a)\n{\n\t(void)0;", "case_ids": ["PrintDeckConfiguration-0"]}
# <<< factory-mutation PrintDeckConfiguration
# >>> factory-completion PrintDeckConfiguration
for _record in SCHEMA2_CASES["PrintDeckConfiguration"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion PrintDeckConfiguration
# >>> factory-mutation ShowPromotionalCardScreen
MUTATIONS["ShowPromotionalCardScreen"] = {
    "source_symbol": "ShowPromotionalCardScreen",
    "before": "void ShowPromotionalCardScreen(uint8_t a)\n{\n\tLoadCardDataToBuffer1_FromCardID(a);",
    "after": "void ShowPromotionalCardScreen(uint8_t a)\n{\n\tLoadCardDataToBuffer1_FromCardID((uint8_t)(a + 1u));",
    "case_ids": ["ShowPromotionalCardScreen-0", "ShowPromotionalCardScreen-1"],
}
# <<< factory-mutation ShowPromotionalCardScreen
# >>> factory-completion ShowPromotionalCardScreen
# The reference never returns: the farcall reaches _ShowPromotionalCardScreen,
# whose `.loop` (06:6680) waits on AssertSongFinished, which only reports done
# once wCurSongID reads $80 -- nothing but the timer ISR's Music1_Update can put
# it there, and the call-level runner arms VBlank alone. That is a genuine spin,
# not a small budget, so completion is declared pre-ret at that wait, exactly as
# the landed _ShowPromotionalCardScreen and PreparePrinterConnection cases do.
# The stop pc is AssertSongFinished itself (poketcg.sym 00:378A), one call
# deeper than the 06:6680 loop head, because $378A is ROM0 and therefore
# bank-independent -- the same reason the PreparePrinterConnection wrapper stops
# at $315D. This wrapper is 01:7594 while the loop lives in bank 06, and the
# PyBoy backend arms a banked stop pc against the routine's OWN bank
# (tools/oracle/pyboy_oracle.py, `_arm(stop_pc, 0 if stop_pc < 0x4000 else
# fn_bank)`), so a $6680 hook would sit on bank 01 and could never fire while
# bank 06 is mapped. Nothing ahead of the loop calls AssertSongFinished --
# SetupText, LoadCardDataToBuffer1_FromCardID, PauseSong, PlaySong, LoadTxRam2
# and _DisplayCardDetailScreen do not -- so the first hit is the wait itself,
# after both observed bytes are written. legacy_to_schema always emits
# completion "return", so the split is applied after migration.
for _record in SCHEMA2_CASES["ShowPromotionalCardScreen"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x378A}
# <<< factory-completion ShowPromotionalCardScreen
# >>> factory-mutation RequestToPrintCard
MUTATIONS["RequestToPrintCard"] = {
    "source_symbol": "RequestToPrintCard",
    "before": "uint8_t RequestToPrintCard(uint8_t a)\n{\n\treturn _RequestToPrintCard(a).f;",
    "after": "uint8_t RequestToPrintCard(uint8_t a)\n{\n\treturn _RequestToPrintCard((uint8_t)(a + 1u)).f;",
    "case_ids": ["RequestToPrintCard-0", "RequestToPrintCard-1"],
}
# <<< factory-mutation RequestToPrintCard
# >>> factory-completion RequestToPrintCard
# $315D is SendPrinterPacket.wait_printer_packet_transmission (home/printer.asm,
# ROM0, so the capture hook is bank-independent), the DoFrame loop the reference
# can never leave without a printer answering on the serial line. The farcall
# wrapper itself lives in another bank, so the ROM0 stop pc is what makes this
# work, exactly as it does for the landed PreparePrinterConnection wrapper.
# legacy_to_schema always emits completion "return", so the split is applied
# after migration.
for _record in SCHEMA2_CASES["RequestToPrintCard"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion RequestToPrintCard
# >>> factory-mutation PrintCardList
MUTATIONS["PrintCardList"] = {
    "source_symbol": "PrintCardList",
    "before": "uint8_t PrintCardList(void)\n{\n\treturn _PrintCardList().f;",
    "after": "uint8_t PrintCardList(void)\n{\n\treturn 0u;",
    "case_ids": ["PrintCardList-0", "PrintCardList-1"],
}
# <<< factory-mutation PrintCardList
# >>> factory-completion PrintCardList
# $315D is SendPrinterPacket.wait_printer_packet_transmission
# (poketcg/src/home/printer.asm, ROM0, so the capture hook is bank-independent),
# the DoFrame loop the reference can never leave without a printer answering on
# the serial line. The farcall wrapper inherits that spin from its callee, and
# because the wrapper itself lives in another bank the ROM0 stop pc is what
# makes the hook reachable at all -- exactly as it is for the landed
# PreparePrinterConnection and RequestToPrintCard wrappers. legacy_to_schema
# always emits completion "return", so the split is applied after migration.
for _record in SCHEMA2_CASES["PrintCardList"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion PrintCardList
# >>> factory-mutation ReceiveCard
MUTATIONS["ReceiveCard"] = {"source_symbol": "ReceiveCard", "before": "ReceiveCardResult ReceiveCard(void)\n{\n\t_ReceiveCardResult r = _ReceiveCard();\n\treturn (ReceiveCardResult){r.a, r.f};", "after": "ReceiveCardResult ReceiveCard(void)\n{\n\treturn (ReceiveCardResult){0x00u, 0x90u};", "case_ids": ["ReceiveCard-0", "ReceiveCard-1"]}
# <<< factory-mutation ReceiveCard
# >>> factory-mutation ReceiveDeckConfiguration
MUTATIONS["ReceiveDeckConfiguration"] = {"source_symbol": "ReceiveDeckConfiguration", "before": "ReceiveDeckConfigurationResult ReceiveDeckConfiguration(void)\n{\n\t_ReceiveDeckConfigurationResult result = _ReceiveDeckConfiguration();\n\treturn (ReceiveDeckConfigurationResult){result.a, result.f};", "after": "ReceiveDeckConfigurationResult ReceiveDeckConfiguration(void)\n{\n\t_ReceiveDeckConfigurationResult result = _ReceiveDeckConfiguration();\n\treturn (ReceiveDeckConfigurationResult){0u, 0u};", "case_ids": ["ReceiveDeckConfiguration-0", "ReceiveDeckConfiguration-1"]}
# <<< factory-mutation ReceiveDeckConfiguration
# >>> factory-mutation DoCardPop
MUTATIONS["DoCardPop"] = {"source_symbol": "DoCardPop", "before": "void DoCardPop(void)\n{\n\t_DoCardPop();", "after": "void DoCardPop(void)\n{\n\thWhoseTurn = 1u;", "case_ids": ["DoCardPop-0", "DoCardPop-1"]}
# <<< factory-mutation DoCardPop
