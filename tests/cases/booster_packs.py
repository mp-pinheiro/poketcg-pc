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

wRNG1 = 0xCACA
wBoosterTempEnergiesDrawn = 0xC40B
wTempCardCollection = 0xC000

wBoosterTempEnergiesDrawn = 0xC40B
wBoosterTempNonEnergiesDrawn = 0xC400
wBoosterCurrentCard = 0xD66A

wBoosterData_CommonAmount = 0xD66E
wBoosterData_RareAmount = 0xD670
wBoosterData_Set = 0xD686
wBoosterData_UncommonAmount = 0xD66F

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wBoosterJustDrawnCardType = 0xD66B
wBoosterTempTypeChancesTable = 0xD67A
wTempBoosterChances = 0xD4CA

wBoosterPackID = 0xD669
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

# >>> factory ZeroBoosterRarityData
CONTRACT["ZeroBoosterRarityData"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["ZeroBoosterRarityData"] = [
    {"wram": {0xD66E: b"\x01", 0xD66F: b"\x02", 0xD670: b"\x03"}, "expect": {0xD66E: b"\x00", 0xD66F: b"\x00", 0xD670: b"\x00"}},
    {"wram": {0xD66E: b"\xFF", 0xD66F: b"\x80", 0xD670: b"\x7F"}, "expect": {0xD66E: b"\x00", 0xD66F: b"\x00", 0xD670: b"\x00"}},
    dict(POISON, wram={0xD66E: b"\xAA", 0xD66F: b"\xBB", 0xD670: b"\xCC"}, expect={0xD66E: b"\x00", 0xD66F: b"\x00", 0xD670: b"\x00"}),
]
# <<< factory ZeroBoosterRarityData

# >>> factory GenerateTwoTypesEnergyBooster
CONTRACT["GenerateTwoTypesEnergyBooster"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e"), "wram_out": True}
CASES["GenerateTwoTypesEnergyBooster"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x12\x2A", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection + 0x12: b"\x00", wTempCardCollection + 0x2A: b"\x00", 0xD66E: b"\x01", 0xD66F: b"\x02", 0xD670: b"\x03"}, "expect": {wBoosterTempEnergiesDrawn: b"\x12\x12\x12\x12\x12\x2A\x2A\x2A\x2A\x2A\x00", wBoosterCurrentCard: b"\x2A", wTempCardCollection + 0x12: b"\x05", wTempCardCollection + 0x2A: b"\x05", 0xD66E: b"\x00", 0xD66F: b"\x00", 0xD670: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "hl": 0xC502}},
    {"hl": 0xC510, "wram": {0xC510: b"\x03\x7E", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection + 0x03: b"\x00", wTempCardCollection + 0x7E: b"\x00", 0xD66E: b"\xFF", 0xD66F: b"\xFF", 0xD670: b"\xFF"}, "expect": {wBoosterTempEnergiesDrawn: b"\x03\x03\x03\x03\x03\x7E\x7E\x7E\x7E\x7E\x00", wBoosterCurrentCard: b"\x7E", wTempCardCollection + 0x03: b"\x05", wTempCardCollection + 0x7E: b"\x05", 0xD66E: b"\x00", 0xD66F: b"\x00", 0xD670: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "hl": 0xC512}},
    dict(POISON, hl=0xC530, wram={0xC530: b"\x80\xFF", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection + 0x80: b"\x00", wTempCardCollection + 0xFF: b"\x00", 0xD66E: b"\xAA", 0xD66F: b"\xBB", 0xD670: b"\xCC"}, expect={wBoosterTempEnergiesDrawn: b"\x80\x80\x80\x80\x80\xFF\xFF\xFF\xFF\xFF\x00", wBoosterCurrentCard: b"\xFF", wTempCardCollection + 0x80: b"\x05", wTempCardCollection + 0xFF: b"\x05", 0xD66E: b"\x00", 0xD66F: b"\x00", 0xD670: b"\x00"}, expect_regs={"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "d": 0xDD, "e": 0xEE, "hl": 0xC532}),
]
# <<< factory GenerateTwoTypesEnergyBooster

# >>> factory GenerateRandomEnergy
CONTRACT["GenerateRandomEnergy"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["GenerateRandomEnergy"] = [
    {"wram": {wRNG1: b"\x00\x00\x00", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection: b"\x00" * 0x100}},
    {"wram": {wRNG1: b"\x12\x34\x56", wBoosterTempEnergiesDrawn: b"\x01\x02\x00", wTempCardCollection: b"\x00" * 0x100}},
    {"wram": {wRNG1: b"\xde\xad\xbe", wBoosterTempEnergiesDrawn: b"\xaa\xbb\x00", wTempCardCollection: b"\x00" * 0x100}},
    dict(POISON, wram={wRNG1: b"\x01\x00\x80", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection: b"\x00" * 0x100}),
]
# <<< factory GenerateRandomEnergy

# >>> factory GenerateEnergyBoosterGrassPsychic
CONTRACT["GenerateEnergyBoosterGrassPsychic"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e"), "wram_out": True}
CASES["GenerateEnergyBoosterGrassPsychic"] = [
    {},
    dict(POISON),
]
# <<< factory GenerateEnergyBoosterGrassPsychic

# >>> factory GenerateEnergyBoosterLightningFire
CONTRACT["GenerateEnergyBoosterLightningFire"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e"), "wram_out": True};
CASES["GenerateEnergyBoosterLightningFire"] = [
    {},
    dict(POISON),
]
# <<< factory GenerateEnergyBoosterLightningFire

# >>> factory GenerateEnergyBoosterWaterFighting
CONTRACT["GenerateEnergyBoosterWaterFighting"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e"), "wram_out": True}
CASES["GenerateEnergyBoosterWaterFighting"] = [
    {},
    dict(POISON),
]
# <<< factory GenerateEnergyBoosterWaterFighting

# >>> factory GenerateRandomEnergyBooster
CONTRACT["GenerateRandomEnergyBooster"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["GenerateRandomEnergyBooster"] = [
    {"wram": {0xCACA: b"\x00\x00\x00", 0xC40B: b"\x00", 0xC000: b"\x00" * 0x100}},
    {"wram": {0xCACA: b"\x12\x34\x56", 0xC40B: b"\x01\x02\x00", 0xC000: b"\x00" * 0x100}},
    {"wram": {0xCACA: b"\xde\xad\xbe", 0xC40B: b"\xaa\xbb\x00", 0xC000: b"\x00" * 0x100}},
    dict(POISON, wram={0xCACA: b"\x01\x00\x80", 0xC40B: b"\x00", 0xC000: b"\x00" * 0x100}),
]
# <<< factory GenerateRandomEnergyBooster

# >>> factory PutEnergiesAndNonEnergiesTogether
CONTRACT["PutEnergiesAndNonEnergiesTogether"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["PutEnergiesAndNonEnergiesTogether"] = [
	{"a": 0x11, "f": 0x00, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x2468, "wram": {wBoosterTempEnergiesDrawn: b"\x00", wBoosterTempNonEnergiesDrawn: b"\x00", wBoosterCurrentCard: b"\x77"}, "expect": {wBoosterTempNonEnergiesDrawn: b"\x00", wBoosterCurrentCard: b"\x77"}},
	{"a": 0x66, "f": 0x10, "b": 0x77, "c": 0x88, "d": 0x99, "e": 0xAA, "hl": 0x1357, "wram": {wBoosterTempEnergiesDrawn: b"\x12\x00", wBoosterTempNonEnergiesDrawn: b"\x00", wBoosterCurrentCard: b"\x00"}, "expect": {wBoosterTempNonEnergiesDrawn: b"\x12\x00", wBoosterCurrentCard: b"\x12"}},
	{"a": 0x01, "f": 0x20, "b": 0x02, "c": 0x03, "d": 0x04, "e": 0x05, "hl": 0x3456, "wram": {wBoosterTempEnergiesDrawn: b"\x12\x2A\x00", wBoosterTempNonEnergiesDrawn: b"\x99\x00", wBoosterCurrentCard: b"\x00"}, "expect": {wBoosterTempNonEnergiesDrawn: b"\x99\x12\x2A\x00", wBoosterCurrentCard: b"\x2A"}},
	dict(POISON, wram={wBoosterTempEnergiesDrawn: b"\x80\xFF\x00", wBoosterTempNonEnergiesDrawn: b"\xAA\x00", wBoosterCurrentCard: b"\xCC"}, expect={wBoosterTempNonEnergiesDrawn: b"\xAA\x80\xFF\x00", wBoosterCurrentCard: b"\xFF"}),
]
# <<< factory PutEnergiesAndNonEnergiesTogether

# >>> factory LoadRarityAmountsToWram
CONTRACT["LoadRarityAmountsToWram"] = {"compare": (), "preserve": ()}
CASES["LoadRarityAmountsToWram"] = [
    {"wram": {wBoosterData_Set: b"\x00"}, "read": {wBoosterData_CommonAmount: 1, wBoosterData_UncommonAmount: 1, wBoosterData_RareAmount: 1}},
    {"wram": {wBoosterData_Set: b"\x01"}, "read": {wBoosterData_CommonAmount: 1, wBoosterData_UncommonAmount: 1, wBoosterData_RareAmount: 1}},
    {"wram": {wBoosterData_Set: b"\x02"}, "read": {wBoosterData_CommonAmount: 1, wBoosterData_UncommonAmount: 1, wBoosterData_RareAmount: 1}},
    {"wram": {wBoosterData_Set: b"\x03"}, "read": {wBoosterData_CommonAmount: 1, wBoosterData_UncommonAmount: 1, wBoosterData_RareAmount: 1}},
    dict(POISON, wram={wBoosterData_Set: b"\x00"}, read={wBoosterData_CommonAmount: 1, wBoosterData_UncommonAmount: 1, wBoosterData_RareAmount: 1}),
]
# <<< factory LoadRarityAmountsToWram

# >>> factory DetermineBoosterCardType
CONTRACT["DetermineBoosterCardType"] = {"compare": ("a",), "preserve": ()}
CASES["DetermineBoosterCardType"] = [
	{"a": 0x00, "wram": {wBoosterTempTypeChancesTable: b"\x00" * 9, wBoosterJustDrawnCardType: b"\xFF", wTempBoosterChances: b"\xFF"}, "read": {wBoosterJustDrawnCardType: 1, wTempBoosterChances: 1}},
	{"a": 0x00, "wram": {wBoosterTempTypeChancesTable: b"\x01\x00\x00\x00\x00\x00\x00\x00\x00", wBoosterJustDrawnCardType: b"\xFF"}, "read": {wBoosterJustDrawnCardType: 1, wTempBoosterChances: 1}},
	{"a": 0x02, "wram": {wBoosterTempTypeChancesTable: b"\x00\x02\x03\x00\x00\x00\x00\x00\x00", wBoosterJustDrawnCardType: b"\xFF"}, "read": {wBoosterJustDrawnCardType: 1, wTempBoosterChances: 1}},
	dict(POISON, a=0xAA, wram={wBoosterTempTypeChancesTable: b"\x20\x10\x08\x04\x02\x01\x00\x00\x00", wBoosterJustDrawnCardType: b"\xFF"}, read={wBoosterJustDrawnCardType: 1, wTempBoosterChances: 1}),
]
# <<< factory DetermineBoosterCardType

# >>> factory FindBoosterDataPointer
CONTRACT["FindBoosterDataPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["FindBoosterDataPointer"] = [
    {"wram": {wBoosterPackID: b"\x00"}},
    {"wram": {wBoosterPackID: b"\x01"}},
    {"wram": {wBoosterPackID: b"\x02"}},
    {"wram": {wBoosterPackID: b"\x1B"}},
    {"wram": {wBoosterPackID: b"\x1C"}},
    dict(POISON, wram={wBoosterPackID: b"\x1B"}),
]
# <<< factory FindBoosterDataPointer

# >>> factory AddBoosterCardToDrawnNonEnergies
CONTRACT["AddBoosterCardToDrawnNonEnergies"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["AddBoosterCardToDrawnNonEnergies"] = [
    {"wram": {0xC400: b"\x00", 0xD66A: b"\x12", 0xC012: b"\x00"}, "read": {0xC400: 2, 0xC012: 1}},
    {"wram": {0xC400: b"\x01\x02\x00", 0xD66A: b"\xFF", 0xC0FF: b"\x0F"}, "read": {0xC400: 4, 0xC0FF: 1}},
    dict(POISON, wram={0xC400: b"\x00", 0xD66A: b"\x7E", 0xC07E: b"\x00"}, read={0xC400: 2, 0xC07E: 1}),
]
# <<< factory AddBoosterCardToDrawnNonEnergies

# >>> factory AddBoosterCardsToCollection
CONTRACT["AddBoosterCardsToCollection"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",), "wram_out": True}
CASES["AddBoosterCardsToCollection"] = [
    {"hl": 0x1234, "wram": {0xC400: b"\x05\x0C\x00"}, "sram": {0: {0xA100: bytes(256)}}, "read": {0xC400: 3}, "sread": {0: {0xA105: 1, 0xA10C: 1}}},
    dict(POISON, hl=0x5678, wram={0xC400: b"\x2A\x00"}, sram={0: {0xA100: bytes(256)}}, read={0xC400: 2}, sread={0: {0xA12A: 1}}),
]
# <<< factory AddBoosterCardsToCollection

# >>> factory GenerateBoosterEnergies
CONTRACT["GenerateBoosterEnergies"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["GenerateBoosterEnergies"] = [
    {"wram": {0xD687: b"\x01\x00", 0xC40B: b"\x00", 0xD66A: b"\x00", 0xC001: b"\x00"},
     "expect": {0xC40B: b"\x01\x00", 0xD66A: b"\x01", 0xC001: b"\x01"}},
    dict(POISON, wram={0xD687: b"\x01\x00", 0xC40B: b"\x00", 0xD66A: b"\x00", 0xC001: b"\x00"},
         expect={0xC40B: b"\x01\x00", 0xD66A: b"\x01", 0xC001: b"\x01"}),
]
# <<< factory GenerateBoosterEnergies

# >>> factory DetermineBoosterCard
CONTRACT["DetermineBoosterCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["DetermineBoosterCard"] = [
    {"d": 0xDD, "e": 0xEE,
     "wram": {0xD66B: b"\x02", 0xD673: b"\x00",
               0xD133: b"\x10\x01\x20\x02\x00"}},
    dict(POISON,
         wram={0xD66B: b"\x02", 0xD673: b"\x00",
               0xD133: b"\x10\x01\x20\x02\x00"}),
    {"d": 0x11, "e": 0x22,
     "wram": {0xD66B: b"\x03", 0xD674: b"\x00",
               0xD133: b"\x00"}},
]
# <<< factory DetermineBoosterCard

# >>> factory CheckCardInSetAndRarity
CONTRACT["CheckCardInSetAndRarity"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckCardInSetAndRarity"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x01, "hl": 0x4455,
     "wram": {0xD66C: b"\x01"}},
    dict(POISON, e=0x01, wram={0xD66C: b"\x00"}),
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x40, "hl": 0x4455,
     "wram": {0xD66C: b"\x02", 0xD686: b"\x09"}},
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x40, "hl": 0x4455,
     "wram": {0xD66C: b"\x02", 0xD686: b"\x04"}},
]
# <<< factory CheckCardInSetAndRarity

# >>> factory CheckCardAlreadyDrawn
CONTRACT["CheckCardAlreadyDrawn"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckCardAlreadyDrawn"] = [
    {"wram": {0xD66A: b"\x03", 0xC003: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x00}},
    {"wram": {0xD66A: b"\x03", 0xC003: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x90}},
    dict(POISON, wram={0xD66A: b"\x03", 0xC003: b"\x02"}, expect_regs={"a": 0x02, "f": 0x10}),
]
# <<< factory CheckCardAlreadyDrawn

# >>> factory FindCardsInSetAndRarity
CONTRACT["FindCardsInSetAndRarity"] = {"compare": ("a", "f", "d", "e"), "preserve": (), "wram_out": True}
CASES["FindCardsInSetAndRarity"] = [
    dict(wram={0xC001: b"\x01" * 228}, read={0xD671: 9, 0xD133: 1, 0xD66A: 1}),
    dict(POISON, wram={0xC001: b"\x01" * 228}, read={0xD671: 9, 0xD133: 1, 0xD66A: 1}),
]
# <<< factory FindCardsInSetAndRarity

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
# >>> factory-mutation ZeroBoosterRarityData
MUTATIONS["ZeroBoosterRarityData"] = {"source_symbol": "ZeroBoosterRarityData", "before": "\twBoosterData_RareAmount = 0u;", "after": "\twBoosterData_RareAmount = 1u;", "case_ids": ["ZeroBoosterRarityData-0", "ZeroBoosterRarityData-1", "ZeroBoosterRarityData-2"]}
# <<< factory-mutation ZeroBoosterRarityData
# >>> factory-mutation GenerateTwoTypesEnergyBooster
MUTATIONS["GenerateTwoTypesEnergyBooster"] = {"source_symbol": "GenerateTwoTypesEnergyBooster", "before": "(void)AddBoosterEnergyToDrawnEnergies(card);", "after": "(void)AddBoosterEnergyToDrawnEnergies((uint8_t)(card + 1u));", "case_ids": ["GenerateTwoTypesEnergyBooster-0", "GenerateTwoTypesEnergyBooster-1", "GenerateTwoTypesEnergyBooster-2"]}
# <<< factory-mutation GenerateTwoTypesEnergyBooster
# >>> factory-mutation GenerateRandomEnergy
MUTATIONS["GenerateRandomEnergy"] = {"source_symbol": "GenerateRandomEnergy", "before": "return AddBoosterEnergyToDrawnEnergies((uint8_t)(random + 1u));", "after": "return AddBoosterEnergyToDrawnEnergies((uint8_t)(random + 2u));", "case_ids": ["GenerateRandomEnergy-0", "GenerateRandomEnergy-1", "GenerateRandomEnergy-2", "GenerateRandomEnergy-3"]}
# <<< factory-mutation GenerateRandomEnergy
# >>> factory-mutation GenerateEnergyBoosterGrassPsychic
MUTATIONS["GenerateEnergyBoosterGrassPsychic"] = {"source_symbol": "GenerateEnergyBoosterGrassPsychic", "before": "\treturn GenerateTwoTypesEnergyBooster(0x63CDu);", "after": "\treturn GenerateTwoTypesEnergyBooster(0x63CBu);", "case_ids": ["GenerateEnergyBoosterGrassPsychic-0", "GenerateEnergyBoosterGrassPsychic-1"]}
# <<< factory-mutation GenerateEnergyBoosterGrassPsychic
# >>> factory-mutation GenerateEnergyBoosterLightningFire
MUTATIONS["GenerateEnergyBoosterLightningFire"] = {"source_symbol": "GenerateEnergyBoosterLightningFire", "before": "\treturn GenerateTwoTypesEnergyBooster(0x63C9u);", "after": "\treturn GenerateTwoTypesEnergyBooster(0x63CBu);", "case_ids": ["GenerateEnergyBoosterLightningFire-0", "GenerateEnergyBoosterLightningFire-1"]}
# <<< factory-mutation GenerateEnergyBoosterLightningFire
# >>> factory-mutation GenerateEnergyBoosterWaterFighting
MUTATIONS["GenerateEnergyBoosterWaterFighting"] = {"source_symbol": "GenerateEnergyBoosterWaterFighting", "before": "\treturn GenerateTwoTypesEnergyBooster(0x63CBu);", "after": "\treturn GenerateTwoTypesEnergyBooster(0x63C9u);", "case_ids": ["GenerateEnergyBoosterWaterFighting-0", "GenerateEnergyBoosterWaterFighting-1"]}
# <<< factory-mutation GenerateEnergyBoosterWaterFighting
# >>> factory-mutation GenerateRandomEnergyBooster
MUTATIONS["GenerateRandomEnergyBooster"] = {"source_symbol": "GenerateRandomEnergyBooster", "before": "\t\t(void)GenerateRandomEnergy();", "after": "\t\t(void)GenerateRandomEnergy();\n\t\t(void)GenerateRandomEnergy();", "case_ids": ["GenerateRandomEnergyBooster-0", "GenerateRandomEnergyBooster-1", "GenerateRandomEnergyBooster-2", "GenerateRandomEnergyBooster-3"]}
# <<< factory-mutation GenerateRandomEnergyBooster
# >>> factory-mutation PutEnergiesAndNonEnergiesTogether
MUTATIONS["PutEnergiesAndNonEnergiesTogether"] = {"source_symbol": "PutEnergiesAndNonEnergiesTogether", "before": "	while ((a = *energy++) != 0u) {", "after": "	while ((a = *energy++) == 0u) {", "case_ids": ["PutEnergiesAndNonEnergiesTogether-0", "PutEnergiesAndNonEnergiesTogether-1", "PutEnergiesAndNonEnergiesTogether-2", "PutEnergiesAndNonEnergiesTogether-3"]}
# <<< factory-mutation PutEnergiesAndNonEnergiesTogether
# >>> factory-mutation LoadRarityAmountsToWram
MUTATIONS["LoadRarityAmountsToWram"] = {"source_symbol": "LoadRarityAmountsToWram", "before": "\tuint8_t common = (set < 2u) ? 5u : 6u;", "after": "\tuint8_t common = (set < 2u) ? 6u : 5u;", "case_ids": ["LoadRarityAmountsToWram-0", "LoadRarityAmountsToWram-1", "LoadRarityAmountsToWram-2", "LoadRarityAmountsToWram-3", "LoadRarityAmountsToWram-4"]}
# <<< factory-mutation LoadRarityAmountsToWram
# >>> factory-mutation DetermineBoosterCardType
MUTATIONS["DetermineBoosterCardType"] = {"source_symbol": "DetermineBoosterCardType", "before": "\t\tuint8_t chance = *table;", "after": "\t\tuint8_t chance = (uint8_t)(*table + 1u);", "case_ids": ["DetermineBoosterCardType-1", "DetermineBoosterCardType-2", "DetermineBoosterCardType-3"]}
# <<< factory-mutation DetermineBoosterCardType
# >>> factory-mutation FindBoosterDataPointer
MUTATIONS["FindBoosterDataPointer"] = {"source_symbol": "FindBoosterDataPointer", "before": "return (uint16_t)(BOOSTER_DATA_BASE + (uint16_t)pack * 0x0Cu);", "after": "return (uint16_t)(BOOSTER_DATA_BASE + 1u + (uint16_t)pack * 0x0Cu);", "case_ids": ["FindBoosterDataPointer-0", "FindBoosterDataPointer-1", "FindBoosterDataPointer-2", "FindBoosterDataPointer-3", "FindBoosterDataPointer-4", "FindBoosterDataPointer-5"]}
# <<< factory-mutation FindBoosterDataPointer
# >>> factory-mutation AddBoosterCardToDrawnNonEnergies
MUTATIONS["AddBoosterCardToDrawnNonEnergies"] = {"source_symbol": "AddBoosterCardToDrawnNonEnergies", "before": "\tAppendCurrentCardToHL(&cursor);\n\tAddBoosterCardToTempCardCollection();", "after": "\tAppendCurrentCardToHL(&cursor);\n\t(void)0;", "case_ids": ["AddBoosterCardToDrawnNonEnergies-0", "AddBoosterCardToDrawnNonEnergies-1", "AddBoosterCardToDrawnNonEnergies-2"]}
# <<< factory-mutation AddBoosterCardToDrawnNonEnergies
# >>> factory-mutation AddBoosterCardsToCollection
MUTATIONS["AddBoosterCardsToCollection"] = {"source_symbol": "AddBoosterCardsToCollection", "before": "\t\tAddCardToCollection(card);", "after": "\t\t(void)card;", "case_ids": ["AddBoosterCardsToCollection-0", "AddBoosterCardsToCollection-1"]}
# <<< factory-mutation AddBoosterCardsToCollection
# >>> factory-mutation GenerateBoosterEnergies
MUTATIONS["GenerateBoosterEnergies"] = {"source_symbol": "GenerateBoosterEnergies", "before": "\t(void)AddBoosterEnergyToDrawnEnergies(a);", "after": "\t(void)AddBoosterEnergyToDrawnEnergies(0u);", "case_ids": ["GenerateBoosterEnergies-0", "GenerateBoosterEnergies-1"]}
# <<< factory-mutation GenerateBoosterEnergies
# >>> factory-mutation DetermineBoosterCard
MUTATIONS["DetermineBoosterCard"] = {"source_symbol": "DetermineBoosterCard", "before": "return (DetermineBoosterCardResult){0u, 0x90u, b, c, d, e, hl};", "after": "return (DetermineBoosterCardResult){0u, 0x80u, b, c, d, e, hl};", "case_ids": ["DetermineBoosterCard-2"]}
# <<< factory-mutation DetermineBoosterCard
# >>> factory-mutation CheckCardInSetAndRarity
MUTATIONS["CheckCardInSetAndRarity"] = {"source_symbol": "CheckCardInSetAndRarity", "before": "if (cur_rarity != rarity) {", "after": "if (cur_rarity == rarity) {", "case_ids": ["CheckCardInSetAndRarity-0", "CheckCardInSetAndRarity-1"]}
# <<< factory-mutation CheckCardInSetAndRarity
# >>> factory-mutation CheckCardAlreadyDrawn
MUTATIONS["CheckCardAlreadyDrawn"] = {
    "source_symbol": "CheckCardAlreadyDrawn",
    "before": "uint8_t value = gb_read8((uint16_t)(wTempCardCollection_ADDR + index));",
    "after": "uint8_t value = gb_read8((uint16_t)(wTempCardCollection_ADDR + index + 1u));",
    "case_ids": ["CheckCardAlreadyDrawn-1", "CheckCardAlreadyDrawn-2"],
}
# <<< factory-mutation CheckCardAlreadyDrawn
# >>> factory-mutation FindCardsInSetAndRarity
MUTATIONS["FindCardsInSetAndRarity"] = {
    "source_symbol": "FindCardsInSetAndRarity",
    "before": "for (uint16_t card_id = 1u; card_id <= NUM_CARDS; card_id++) {",
    "after": "for (uint16_t card_id = 1u; card_id <= NUM_CARDS + 1u; card_id++) {",
    "case_ids": ["FindCardsInSetAndRarity-0", "FindCardsInSetAndRarity-1"],
}
# <<< factory-mutation FindCardsInSetAndRarity
