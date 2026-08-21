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
