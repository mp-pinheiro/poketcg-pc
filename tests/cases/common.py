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
