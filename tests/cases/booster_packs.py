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

# >>> factory AppendCurrentCardToHL
CONTRACT["AppendCurrentCardToHL"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e"), "wram_out": True}
CASES["AppendCurrentCardToHL"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x00", 0xD66A: b"\x12"}, "read": {0xC500: 2}},
    {"hl": 0xC510, "wram": {0xC510: b"\x01\x02\x00", 0xD66A: b"\x34"}, "read": {0xC510: 4}},
    {"hl": 0xC520, "wram": {0xC520: b"\xAA\xBB\xCC\x00", 0xD66A: b"\x7E"}, "read": {0xC520: 5}},
    dict(POISON, hl=0xC530, wram={0xC530: b"\x00", 0xD66A: b"\xFF"}, read={0xC530: 2}),
]
# <<< factory AppendCurrentCardToHL

# >>> factory-cases-statics
wBoosterCurrentCard = 0xD66A
wTempCardCollection = 0xC000

wBoosterCurrentCard = 0xD66A
wBoosterTempEnergiesDrawn = 0xC40B
wTempCardCollection = 0xC000
# <<< factory-cases-statics

# >>> factory AddBoosterCardToTempCardCollection
CONTRACT["AddBoosterCardToTempCardCollection"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["AddBoosterCardToTempCardCollection"] = [
    {"wram": {wBoosterCurrentCard: b"\x00", wTempCardCollection: b"\x00"}, "expect": {wTempCardCollection: b"\x01"}, "expect_regs": {"a": 0x00, "f": 0x00, "hl": 0x0000}},
    {"wram": {wBoosterCurrentCard: b"\x2A", wTempCardCollection + 0x2A: b"\x0F"}, "expect": {wTempCardCollection + 0x2A: b"\x10"}, "expect_regs": {"a": 0x2A, "f": 0x20, "hl": 0x0000}},
    {"wram": {wBoosterCurrentCard: b"\xFF", wTempCardCollection + 0xFF: b"\xFF"}, "expect": {wTempCardCollection + 0xFF: b"\x00"}, "expect_regs": {"a": 0xFF, "f": 0xA0, "hl": 0x0000}},
    dict(POISON, wram={wBoosterCurrentCard: b"\x80", wTempCardCollection + 0x80: b"\xFE"}, expect={wTempCardCollection + 0x80: b"\xFF"}, expect_regs={"a": 0x80, "f": 0x10, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory AddBoosterCardToTempCardCollection

# >>> factory AddBoosterCardToDrawnEnergies
CONTRACT["AddBoosterCardToDrawnEnergies"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["AddBoosterCardToDrawnEnergies"] = [
    {"wram": {0xD66A: b"\x12", 0xC40B: b"\x00", 0xC012: b"\x00"}, "read": {0xC40B: 2, 0xC012: 1}},
    {"wram": {0xD66A: b"\xFF", 0xC40B: b"\x01\x02\x00", 0xC0FF: b"\x0F"}, "read": {0xC40B: 4, 0xC0FF: 1}},
    {"wram": {0xD66A: b"\x00", 0xC40B: b"\xAA\x00", 0xC000: b"\xFF"}, "read": {0xC40B: 3, 0xC000: 1}},
    dict(POISON, wram={0xD66A: b"\x7E", 0xC40B: b"\x00", 0xC07E: b"\xFF"}, read={0xC40B: 2, 0xC07E: 1}),
]
# <<< factory AddBoosterCardToDrawnEnergies

# >>> factory AddBoosterEnergyToDrawnEnergies
CONTRACT["AddBoosterEnergyToDrawnEnergies"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["AddBoosterEnergyToDrawnEnergies"] = [
    {"a": 0x12, "wram": {wBoosterTempEnergiesDrawn: b"\x00", wBoosterCurrentCard: b"\x00", wTempCardCollection + 0x12: b"\x00"}, "expect": {wBoosterTempEnergiesDrawn: b"\x12\x00", wBoosterCurrentCard: b"\x12", wTempCardCollection + 0x12: b"\x01"}, "expect_regs": {"a": 0x12, "f": 0x00, "hl": 0x0000}},
    {"a": 0x2A, "hl": 0x4567, "wram": {wBoosterTempEnergiesDrawn: b"\x01\x02\x00", wBoosterCurrentCard: b"\x00", wTempCardCollection + 0x2A: b"\x0F"}, "expect": {wBoosterTempEnergiesDrawn: b"\x01\x02\x2A\x00", wBoosterCurrentCard: b"\x2A", wTempCardCollection + 0x2A: b"\x10"}, "expect_regs": {"a": 0x2A, "f": 0x20, "hl": 0x4567}},
    {"a": 0xFF, "wram": {wBoosterTempEnergiesDrawn: b"\xAA\xBB\x00", wBoosterCurrentCard: b"\x00", wTempCardCollection + 0xFF: b"\xFF"}, "expect": {wBoosterTempEnergiesDrawn: b"\xAA\xBB\xFF\x00", wBoosterCurrentCard: b"\xFF", wTempCardCollection + 0xFF: b"\x00"}, "expect_regs": {"a": 0xFF, "f": 0x80, "hl": 0x0000}},
    dict(POISON, a=0x80, wram={wBoosterTempEnergiesDrawn: b"\x00", wBoosterCurrentCard: b"\x00", wTempCardCollection + 0x80: b"\xFE"}, expect={wBoosterTempEnergiesDrawn: b"\x80\x00", wBoosterCurrentCard: b"\x80", wTempCardCollection + 0x80: b"\xFF"}, expect_regs={"a": 0x80, "f": 0x00, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory AddBoosterEnergyToDrawnEnergies

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
# >>> factory-mutation AppendCurrentCardToHL
MUTATIONS["AppendCurrentCardToHL"] = {
    "source_symbol": "AppendCurrentCardToHL",
    "before": "while (gb_read8(cursor++) != 0u)",
    "after": "while (gb_read8(cursor++) == 0u)",
    "case_ids": ["AppendCurrentCardToHL-0", "AppendCurrentCardToHL-1", "AppendCurrentCardToHL-2", "AppendCurrentCardToHL-3"],
}
# <<< factory-mutation AppendCurrentCardToHL
# >>> factory-mutation AddBoosterCardToTempCardCollection
MUTATIONS["AddBoosterCardToTempCardCollection"] = {"source_symbol": "AddBoosterCardToTempCardCollection", "before": "gb_write8(slot, (uint8_t)(gb_read8(slot) + 1u));", "after": "gb_write8(slot, (uint8_t)(gb_read8(slot) + 2u));", "case_ids": ["AddBoosterCardToTempCardCollection-0", "AddBoosterCardToTempCardCollection-1", "AddBoosterCardToTempCardCollection-2", "AddBoosterCardToTempCardCollection-3"]}
# <<< factory-mutation AddBoosterCardToTempCardCollection
# >>> factory-mutation AddBoosterCardToDrawnEnergies
MUTATIONS["AddBoosterCardToDrawnEnergies"] = {
    "source_symbol": "AddBoosterCardToDrawnEnergies",
    "before": "AddBoosterCardToTempCardCollection();",
    "after": "gb_write8(address, (uint8_t)(old + 2u));",
    "case_ids": ["AddBoosterCardToDrawnEnergies-0", "AddBoosterCardToDrawnEnergies-1", "AddBoosterCardToDrawnEnergies-2", "AddBoosterCardToDrawnEnergies-3"],
}
# <<< factory-mutation AddBoosterCardToDrawnEnergies
# >>> factory-mutation AddBoosterEnergyToDrawnEnergies
MUTATIONS["AddBoosterEnergyToDrawnEnergies"] = {"source_symbol": "AddBoosterEnergyToDrawnEnergies", "before": "wBoosterCurrentCard = a;", "after": "wBoosterCurrentCard = (uint8_t)(a + 1u);", "case_ids": ["AddBoosterEnergyToDrawnEnergies-0", "AddBoosterEnergyToDrawnEnergies-1", "AddBoosterEnergyToDrawnEnergies-2", "AddBoosterEnergyToDrawnEnergies-3"]}
# <<< factory-mutation AddBoosterEnergyToDrawnEnergies
