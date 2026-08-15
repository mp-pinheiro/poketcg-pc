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
