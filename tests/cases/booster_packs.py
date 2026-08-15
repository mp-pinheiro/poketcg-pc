"""Oracle-diff cases for poketcg/src/engine/booster_packs.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetCurrentRarityAmount
CONTRACT["GetCurrentRarityAmount"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetCurrentRarityAmount"] = [
    {"wram": {0xD66C: b"\x00"}},
    {"wram": {0xD66C: b"\x01"}},
    {"wram": {0xD66C: b"\x02"}},
    {"wram": {0xD66C: b"\xFF"}},
    dict(POISON, wram={0xD66C: b"\x03"}),
]
# <<< factory GetCurrentRarityAmount

# >>> factory GetBoosterCardType
CONTRACT["GetBoosterCardType"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetBoosterCardType"] = [
    {"a": 0x00},
    {"a": 0x01},
    {"a": 0x07},
    {"a": 0x08},
    {"a": 0x0F},
    {"a": 0x10},
    {"a": 0x11},
    {"a": 0xFF},
    dict(POISON, a=0x05),
    dict(POISON, a=0x11),
]
# <<< factory GetBoosterCardType

# >>> factory CalculateTypeChances
CONTRACT["CalculateTypeChances"] = {"compare": ("a", "d", "e"), "preserve": ("d", "e")}
CASES["CalculateTypeChances"] = [
    {"wram": {0xD671: b"\x00" * 9, 0xD689: b"\x00" * 9, 0xD67A: b"\x00" * 9, 0xD4CA: b"\x00"}},
    {"wram": {0xD671: b"\x01" * 9, 0xD689: b"\x02" * 9, 0xD67A: b"\xFF" * 9, 0xD4CA: b"\xFF"}},
    {"wram": {0xD671: b"\x01\x00\x01\x00\x01\x00\x01\x00\x01",
              0xD689: b"\x0A\x0A\x00\x0A\x14\x00\x05\x0A\x1E",
              0xD67A: b"\xAA" * 9, 0xD4CA: b"\xAA"}},
    {"wram": {0xD671: b"\x00\x01\x01\x01\x01\x01\x01\x01\x01",
              0xD689: b"\xFF\x40\x40\x40\x40\x00\x00\x00\x00",
              0xD67A: b"\x11" * 9, 0xD4CA: b"\x11"}},
    dict(POISON, wram={0xD671: b"\x02" * 9, 0xD689: b"\x03" * 9,
                       0xD67A: b"\xEE" * 9, 0xD4CA: b"\xEE"}),
]
# <<< factory CalculateTypeChances

# >>> factory UpdateBoosterCardTypesChanceByte
CONTRACT["UpdateBoosterCardTypesChanceByte"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UpdateBoosterCardTypesChanceByte"] = [
    {"wram": {0xD66B: b"\x00", 0xD66D: b"\x00", 0xD689: b"\x00\x00\x00\x00\x00\x00\x00\x00"},
     "read": {0xD689: 8}},
    {"wram": {0xD66B: b"\x01", 0xD66D: b"\x02", 0xD689: b"\x09\x05\x07\x05\x00\x00\x00\x00"},
     "read": {0xD689: 8}},
    {"wram": {0xD66B: b"\x03", 0xD66D: b"\x05", 0xD689: b"\x09\x05\x07\x05\x00\x00\x00\x00"},
     "read": {0xD689: 8}},
    {"wram": {0xD66B: b"\x02", 0xD66D: b"\x40", 0xD689: b"\x01\x02\x01\x04\x00\x00\x00\x00"},
     "read": {0xD689: 8}},
    dict(POISON, wram={0xD66B: b"\x04", 0xD66D: b"\x03", 0xD689: b"\x09\x05\x07\x05\x03\x00\x00\x00"},
         read={0xD689: 8}),
]
# <<< factory UpdateBoosterCardTypesChanceByte

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetCurrentRarityAmount
MUTATIONS["GetCurrentRarityAmount"] = {
    "source_symbol": "GetCurrentRarityAmount",
    "before": "(uint16_t)(wBoosterData_CommonAmount_ADDR + a)",
    "after": "(uint16_t)(wBoosterData_CommonAmount_ADDR + a + 1u)",
    "case_ids": ["GetCurrentRarityAmount-0", "GetCurrentRarityAmount-1"],
}
# <<< factory-mutation GetCurrentRarityAmount
# >>> factory-mutation GetBoosterCardType
MUTATIONS["GetBoosterCardType"] = {
    "source_symbol": "GetBoosterCardType",
    "before": "\tif (a >= NUM_CARD_TYPES)",
    "after": "\tif (a > NUM_CARD_TYPES)",
    "case_ids": ["GetBoosterCardType-6"],
}
# <<< factory-mutation GetBoosterCardType
# >>> factory-mutation CalculateTypeChances
MUTATIONS["CalculateTypeChances"] = {
    "source_symbol": "CalculateTypeChances",
    "before": "\t\tif (amount == 0u)",
    "after": "\t\tif (amount == 1u)",
    "case_ids": ["CalculateTypeChances-1", "CalculateTypeChances-2"],
}
# <<< factory-mutation CalculateTypeChances
# >>> factory-mutation UpdateBoosterCardTypesChanceByte
MUTATIONS["UpdateBoosterCardTypesChanceByte"] = {
    "source_symbol": "UpdateBoosterCardTypesChanceByte",
    "before": "if (res == 0u || v < c) {",
    "after": "if (v < c) {",
    "case_ids": ["UpdateBoosterCardTypesChanceByte-0", "UpdateBoosterCardTypesChanceByte-2", "UpdateBoosterCardTypesChanceByte-4"],
}
# <<< factory-mutation UpdateBoosterCardTypesChanceByte
