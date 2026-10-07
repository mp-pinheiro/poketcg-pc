"""Oracle-diff cases for poketcg/src/engine/booster_packs.asm."""
from tests.cases._symbols import sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetCurrentRarityAmount
CONTRACT["GetCurrentRarityAmount"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetCurrentRarityAmount"] = [
    {"wram": {sym("wBoosterCurrentRarity"): b"\x00"}},
    {"wram": {sym("wBoosterCurrentRarity"): b"\x01"}},
    {"wram": {sym("wBoosterCurrentRarity"): b"\x02"}},
    {"wram": {sym("wBoosterCurrentRarity"): b"\xFF"}},
    dict(POISON, wram={sym("wBoosterCurrentRarity"): b"\x03"}),
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
    {"wram": {sym("wBoosterAmountOfCardTypeTable"): b"\x00" * 9, sym("wBoosterData_TypeChances"): b"\x00" * 9, sym("wBoosterTempTypeChancesTable"): b"\x00" * 9, sym("wTempBoosterChances"): b"\x00"}},
    {"wram": {sym("wBoosterAmountOfCardTypeTable"): b"\x01" * 9, sym("wBoosterData_TypeChances"): b"\x02" * 9, sym("wBoosterTempTypeChancesTable"): b"\xFF" * 9, sym("wTempBoosterChances"): b"\xFF"}},
    {"wram": {sym("wBoosterAmountOfCardTypeTable"): b"\x01\x00\x01\x00\x01\x00\x01\x00\x01",
              sym("wBoosterData_TypeChances"): b"\x0A\x0A\x00\x0A\x14\x00\x05\x0A\x1E",
              sym("wBoosterTempTypeChancesTable"): b"\xAA" * 9, sym("wTempBoosterChances"): b"\xAA"}},
    {"wram": {sym("wBoosterAmountOfCardTypeTable"): b"\x00\x01\x01\x01\x01\x01\x01\x01\x01",
              sym("wBoosterData_TypeChances"): b"\xFF\x40\x40\x40\x40\x00\x00\x00\x00",
              sym("wBoosterTempTypeChancesTable"): b"\x11" * 9, sym("wTempBoosterChances"): b"\x11"}},
    dict(POISON, wram={sym("wBoosterAmountOfCardTypeTable"): b"\x02" * 9, sym("wBoosterData_TypeChances"): b"\x03" * 9,
                       sym("wBoosterTempTypeChancesTable"): b"\xEE" * 9, sym("wTempBoosterChances"): b"\xEE"}),
]
# <<< factory CalculateTypeChances

# >>> factory UpdateBoosterCardTypesChanceByte
CONTRACT["UpdateBoosterCardTypesChanceByte"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UpdateBoosterCardTypesChanceByte"] = [
    {"wram": {sym("wBoosterJustDrawnCardType"): b"\x00", sym("wBoosterAveragedTypeChances"): b"\x00", sym("wBoosterData_TypeChances"): b"\x00\x00\x00\x00\x00\x00\x00\x00"},
     "read": {sym("wBoosterData_TypeChances"): 8}},
    {"wram": {sym("wBoosterJustDrawnCardType"): b"\x01", sym("wBoosterAveragedTypeChances"): b"\x02", sym("wBoosterData_TypeChances"): b"\x09\x05\x07\x05\x00\x00\x00\x00"},
     "read": {sym("wBoosterData_TypeChances"): 8}},
    {"wram": {sym("wBoosterJustDrawnCardType"): b"\x03", sym("wBoosterAveragedTypeChances"): b"\x05", sym("wBoosterData_TypeChances"): b"\x09\x05\x07\x05\x00\x00\x00\x00"},
     "read": {sym("wBoosterData_TypeChances"): 8}},
    {"wram": {sym("wBoosterJustDrawnCardType"): b"\x02", sym("wBoosterAveragedTypeChances"): b"\x40", sym("wBoosterData_TypeChances"): b"\x01\x02\x01\x04\x00\x00\x00\x00"},
     "read": {sym("wBoosterData_TypeChances"): 8}},
    dict(POISON, wram={sym("wBoosterJustDrawnCardType"): b"\x04", sym("wBoosterAveragedTypeChances"): b"\x03", sym("wBoosterData_TypeChances"): b"\x09\x05\x07\x05\x03\x00\x00\x00"},
         read={sym("wBoosterData_TypeChances"): 8}),
]
# <<< factory UpdateBoosterCardTypesChanceByte

# >>> factory AppendCurrentCardToHL
CONTRACT["AppendCurrentCardToHL"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e"), "wram_out": True}
CASES["AppendCurrentCardToHL"] = [
    {"hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer"): b"\x00", sym("wBoosterCurrentCard"): b"\x12"}, "read": {sym("wNameBuffer"): 2}},
    {"hl": sym("wDuelTempList"), "wram": {sym("wDuelTempList"): b"\x01\x02\x00", sym("wBoosterCurrentCard"): b"\x34"}, "read": {sym("wDuelTempList"): 4}},
    {"hl": sym("wDuelTempList") + 0x10, "wram": {sym("wDuelTempList") + 0x10: b"\xAA\xBB\xCC\x00", sym("wBoosterCurrentCard"): b"\x7E"}, "read": {sym("wDuelTempList") + 0x10: 5}},
    dict(POISON, hl=sym("wDuelTempList") + 0x20, wram={sym("wDuelTempList") + 0x20: b"\x00", sym("wBoosterCurrentCard"): b"\xFF"}, read={sym("wDuelTempList") + 0x20: 2}),
]
# <<< factory AppendCurrentCardToHL

# >>> factory-cases-statics
wBoosterCurrentCard = sym("wBoosterCurrentCard")
wTempCardCollection = sym("wTempCardCollection")

wBoosterCurrentCard = sym("wBoosterCurrentCard")
wBoosterTempEnergiesDrawn = sym("wBoosterTempEnergiesDrawn")
wTempCardCollection = sym("wTempCardCollection")

wRNG1 = sym("wRNG1")
wBoosterTempEnergiesDrawn = sym("wBoosterTempEnergiesDrawn")
wTempCardCollection = sym("wTempCardCollection")

wBoosterTempEnergiesDrawn = sym("wBoosterTempEnergiesDrawn")
wBoosterTempNonEnergiesDrawn = sym("wBoosterTempNonEnergiesDrawn")
wBoosterCurrentCard = sym("wBoosterCurrentCard")

wBoosterData_CommonAmount = sym("wBoosterData_CommonAmount")
wBoosterData_RareAmount = sym("wBoosterData_RareAmount")
wBoosterData_Set = sym("wBoosterData_Set")
wBoosterData_UncommonAmount = sym("wBoosterData_UncommonAmount")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wBoosterJustDrawnCardType = sym("wBoosterJustDrawnCardType")
wBoosterTempTypeChancesTable = sym("wBoosterTempTypeChancesTable")
wTempBoosterChances = sym("wTempBoosterChances")

wBoosterPackID = sym("wBoosterPackID")

wBoosterCardsDrawn_A = sym("wBoosterCardsDrawn")
wTempCardCollection_A = sym("wDeckToBuild")
wBoosterData_Set_A = sym("wBoosterData_Set")
wBoosterPackID_A = sym("wBoosterPackID")
wBoosterAveragedTypeChances_A = sym("wBoosterAveragedTypeChances")

wBoosterPackID_A = sym("wBoosterPackID")
wBoosterCardsDrawn_A = sym("wBoosterCardsDrawn")
wTempCardCollection_A = sym("wDeckToBuild")
sCardCollection_A = sym("sCardAndDeckSaveData")
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
    {"wram": {sym("wBoosterCurrentCard"): b"\x12", sym("wBoosterTempEnergiesDrawn"): b"\x00", sym("wDeckToBuild") + 0x12: b"\x00"}, "read": {sym("wBoosterTempEnergiesDrawn"): 2, sym("wDeckToBuild") + 0x12: 1}},
    {"wram": {sym("wBoosterCurrentCard"): b"\xFF", sym("wBoosterTempEnergiesDrawn"): b"\x01\x02\x00", sym("wDecompressionSecondaryBufferStart") + 0x10: b"\x0F"}, "read": {sym("wBoosterTempEnergiesDrawn"): 4, sym("wDecompressionSecondaryBufferStart") + 0x10: 1}},
    {"wram": {sym("wBoosterCurrentCard"): b"\x00", sym("wBoosterTempEnergiesDrawn"): b"\xAA\x00", sym("wDeckToBuild"): b"\xFF"}, "read": {sym("wBoosterTempEnergiesDrawn"): 3, sym("wDeckToBuild"): 1}},
    dict(POISON, wram={sym("wBoosterCurrentCard"): b"\x7E", sym("wBoosterTempEnergiesDrawn"): b"\x00", sym("wDeckToBuild") + 0x7E: b"\xFF"}, read={sym("wBoosterTempEnergiesDrawn"): 2, sym("wDeckToBuild") + 0x7E: 1}),
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
    {"wram": {sym("wBoosterData_CommonAmount"): b"\x01", sym("wBoosterData_UncommonAmount"): b"\x02", sym("wBoosterData_RareAmount"): b"\x03"}, "expect": {sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}},
    {"wram": {sym("wBoosterData_CommonAmount"): b"\xFF", sym("wBoosterData_UncommonAmount"): b"\x80", sym("wBoosterData_RareAmount"): b"\x7F"}, "expect": {sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}},
    dict(POISON, wram={sym("wBoosterData_CommonAmount"): b"\xAA", sym("wBoosterData_UncommonAmount"): b"\xBB", sym("wBoosterData_RareAmount"): b"\xCC"}, expect={sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}),
]
# <<< factory ZeroBoosterRarityData

# >>> factory GenerateTwoTypesEnergyBooster
CONTRACT["GenerateTwoTypesEnergyBooster"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e"), "wram_out": True}
CASES["GenerateTwoTypesEnergyBooster"] = [
    {"hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer"): b"\x12\x2A", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection + 0x12: b"\x00", wTempCardCollection + 0x2A: b"\x00", sym("wBoosterData_CommonAmount"): b"\x01", sym("wBoosterData_UncommonAmount"): b"\x02", sym("wBoosterData_RareAmount"): b"\x03"}, "expect": {wBoosterTempEnergiesDrawn: b"\x12\x12\x12\x12\x12\x2A\x2A\x2A\x2A\x2A\x00", wBoosterCurrentCard: b"\x2A", wTempCardCollection + 0x12: b"\x05", wTempCardCollection + 0x2A: b"\x05", sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "hl": sym("wNameBuffer") + 2}},
    {"hl": sym("wDuelTempList"), "wram": {sym("wDuelTempList"): b"\x03\x7E", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection + 0x03: b"\x00", wTempCardCollection + 0x7E: b"\x00", sym("wBoosterData_CommonAmount"): b"\xFF", sym("wBoosterData_UncommonAmount"): b"\xFF", sym("wBoosterData_RareAmount"): b"\xFF"}, "expect": {wBoosterTempEnergiesDrawn: b"\x03\x03\x03\x03\x03\x7E\x7E\x7E\x7E\x7E\x00", wBoosterCurrentCard: b"\x7E", wTempCardCollection + 0x03: b"\x05", wTempCardCollection + 0x7E: b"\x05", sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "hl": sym("wDuelTempList") + 2}},
    dict(POISON, hl=sym("wDuelTempList") + 0x20, wram={sym("wDuelTempList") + 0x20: b"\x80\xFF", wBoosterTempEnergiesDrawn: b"\x00", wTempCardCollection + 0x80: b"\x00", wTempCardCollection + 0xFF: b"\x00", sym("wBoosterData_CommonAmount"): b"\xAA", sym("wBoosterData_UncommonAmount"): b"\xBB", sym("wBoosterData_RareAmount"): b"\xCC"}, expect={wBoosterTempEnergiesDrawn: b"\x80\x80\x80\x80\x80\xFF\xFF\xFF\xFF\xFF\x00", wBoosterCurrentCard: b"\xFF", wTempCardCollection + 0x80: b"\x05", wTempCardCollection + 0xFF: b"\x05", sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}, expect_regs={"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "d": 0xDD, "e": 0xEE, "hl": sym("wDuelTempList") + 0x22}),
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
    {"wram": {sym("wRNG1"): b"\x00\x00\x00", sym("wBoosterTempEnergiesDrawn"): b"\x00", sym("wDeckToBuild"): b"\x00" * 0x100}},
    {"wram": {sym("wRNG1"): b"\x12\x34\x56", sym("wBoosterTempEnergiesDrawn"): b"\x01\x02\x00", sym("wDeckToBuild"): b"\x00" * 0x100}},
    {"wram": {sym("wRNG1"): b"\xde\xad\xbe", sym("wBoosterTempEnergiesDrawn"): b"\xaa\xbb\x00", sym("wDeckToBuild"): b"\x00" * 0x100}},
    dict(POISON, wram={sym("wRNG1"): b"\x01\x00\x80", sym("wBoosterTempEnergiesDrawn"): b"\x00", sym("wDeckToBuild"): b"\x00" * 0x100}),
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
    {"wram": {sym("wBoosterCardsDrawn"): b"\x00", sym("wBoosterCurrentCard"): b"\x12", sym("wDeckToBuild") + 0x12: b"\x00"}, "read": {sym("wBoosterCardsDrawn"): 2, sym("wDeckToBuild") + 0x12: 1}},
    {"wram": {sym("wBoosterCardsDrawn"): b"\x01\x02\x00", sym("wBoosterCurrentCard"): b"\xFF", sym("wDecompressionSecondaryBufferStart") + 0x10: b"\x0F"}, "read": {sym("wBoosterCardsDrawn"): 4, sym("wDecompressionSecondaryBufferStart") + 0x10: 1}},
    dict(POISON, wram={sym("wBoosterCardsDrawn"): b"\x00", sym("wBoosterCurrentCard"): b"\x7E", sym("wDeckToBuild") + 0x7E: b"\x00"}, read={sym("wBoosterCardsDrawn"): 2, sym("wDeckToBuild") + 0x7E: 1}),
]
# <<< factory AddBoosterCardToDrawnNonEnergies

# >>> factory AddBoosterCardsToCollection
CONTRACT["AddBoosterCardsToCollection"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",), "wram_out": True}
CASES["AddBoosterCardsToCollection"] = [
    {"hl": 0x1234, "wram": {sym("wBoosterCardsDrawn"): b"\x05\x0C\x00"}, "sram": {0: {sym("sCardAndDeckSaveData"): bytes(256)}}, "read": {sym("wBoosterCardsDrawn"): 3}, "sread": {0: {sym("sCardAndDeckSaveData") + 5: 1, sym("sCardAndDeckSaveData") + 0xC: 1}}},
    dict(POISON, hl=0x5678, wram={sym("wBoosterCardsDrawn"): b"\x2A\x00"}, sram={0: {sym("sCardAndDeckSaveData"): bytes(256)}}, read={sym("wBoosterCardsDrawn"): 2}, sread={0: {sym("sCardAndDeckSaveData") + 0x2A: 1}}),
]
# <<< factory AddBoosterCardsToCollection

# >>> factory GenerateBoosterEnergies
CONTRACT["GenerateBoosterEnergies"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["GenerateBoosterEnergies"] = [
    {"wram": {sym("wBoosterData_EnergyFunctionPointer"): b"\x01\x00", sym("wBoosterTempEnergiesDrawn"): b"\x00", sym("wBoosterCurrentCard"): b"\x00", sym("wDeckToBuild") + 1: b"\x00"},
     "expect": {sym("wBoosterTempEnergiesDrawn"): b"\x01\x00", sym("wBoosterCurrentCard"): b"\x01", sym("wDeckToBuild") + 1: b"\x01"}},
    dict(POISON, wram={sym("wBoosterData_EnergyFunctionPointer"): b"\x01\x00", sym("wBoosterTempEnergiesDrawn"): b"\x00", sym("wBoosterCurrentCard"): b"\x00", sym("wDeckToBuild") + 1: b"\x00"},
         expect={sym("wBoosterTempEnergiesDrawn"): b"\x01\x00", sym("wBoosterCurrentCard"): b"\x01", sym("wDeckToBuild") + 1: b"\x01"}),
]
# <<< factory GenerateBoosterEnergies

# >>> factory DetermineBoosterCard
CONTRACT["DetermineBoosterCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e")}
CASES["DetermineBoosterCard"] = [
    {"d": 0xDD, "e": 0xEE,
     "wram": {sym("wBoosterJustDrawnCardType"): b"\x02", sym("wBoosterAmountOfCardTypeTable") + 2: b"\x00",
               sym("wBoosterViableCardList"): b"\x10\x01\x20\x02\x00"}},
    dict(POISON,
         wram={sym("wBoosterJustDrawnCardType"): b"\x02", sym("wBoosterAmountOfCardTypeTable") + 2: b"\x00",
               sym("wBoosterViableCardList"): b"\x10\x01\x20\x02\x00"}),
    {"d": 0x11, "e": 0x22,
     "wram": {sym("wBoosterJustDrawnCardType"): b"\x03", sym("wBoosterAmountOfCardTypeTable") + 3: b"\x00",
               sym("wBoosterViableCardList"): b"\x00"}},
]
# <<< factory DetermineBoosterCard

# >>> factory CheckCardInSetAndRarity
CONTRACT["CheckCardInSetAndRarity"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckCardInSetAndRarity"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x01, "hl": 0x4455,
     "wram": {sym("wBoosterCurrentRarity"): b"\x01"}},
    dict(POISON, e=0x01, wram={sym("wBoosterCurrentRarity"): b"\x00"}),
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x40, "hl": 0x4455,
     "wram": {sym("wBoosterCurrentRarity"): b"\x02", sym("wBoosterData_Set"): b"\x09"}},
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x40, "hl": 0x4455,
     "wram": {sym("wBoosterCurrentRarity"): b"\x02", sym("wBoosterData_Set"): b"\x04"}},
]
# <<< factory CheckCardInSetAndRarity

# >>> factory CheckCardAlreadyDrawn
CONTRACT["CheckCardAlreadyDrawn"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckCardAlreadyDrawn"] = [
    {"wram": {sym("wBoosterCurrentCard"): b"\x03", sym("wDeckToBuild") + 3: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x00}},
    {"wram": {sym("wBoosterCurrentCard"): b"\x03", sym("wDeckToBuild") + 3: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x90}},
    dict(POISON, wram={sym("wBoosterCurrentCard"): b"\x03", sym("wDeckToBuild") + 3: b"\x02"}, expect_regs={"a": 0x02, "f": 0x10}),
]
# <<< factory CheckCardAlreadyDrawn

# >>> factory FindCardsInSetAndRarity
CONTRACT["FindCardsInSetAndRarity"] = {"compare": ("a", "f", "d", "e"), "preserve": (), "wram_out": True}
CASES["FindCardsInSetAndRarity"] = [
    dict(wram={sym("wDeckToBuild") + 1: b"\x01" * 228}, read={sym("wBoosterAmountOfCardTypeTable"): 9, sym("wBoosterViableCardList"): 1, sym("wBoosterCurrentCard"): 1}),
    dict(POISON, wram={sym("wDeckToBuild") + 1: b"\x01" * 228}, read={sym("wBoosterAmountOfCardTypeTable"): 9, sym("wBoosterViableCardList"): 1, sym("wBoosterCurrentCard"): 1}),
]
# <<< factory FindCardsInSetAndRarity

# >>> factory GenerateBoosterNonEnergies
CONTRACT["GenerateBoosterNonEnergies"] = {"compare": ("a", "f"), "preserve": ()}
CASES["GenerateBoosterNonEnergies"] = [
    {"wram": {sym("wBoosterCurrentRarity"): b"\x00", sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}, "expect_regs": {"a": 0xFF, "f": 0x00}},
    dict(POISON, wram={sym("wBoosterCurrentRarity"): b"\x00", sym("wBoosterData_CommonAmount"): b"\x00", sym("wBoosterData_UncommonAmount"): b"\x00", sym("wBoosterData_RareAmount"): b"\x00"}, expect_regs={"a": 0xFF, "f": 0x00}),
]
# <<< factory GenerateBoosterNonEnergies

# >>> factory InitBoosterData
CONTRACT["InitBoosterData"] = {"compare": (), "preserve": (), "wram_out": True, "sram_out": True}
CASES["InitBoosterData"] = [
    {"wram": {wBoosterPackID_A: b"\x00", wBoosterCardsDrawn_A: bytes([0xFF] * 0x16),
              wTempCardCollection_A: bytes([0xFF] * 256), wBoosterData_Set_A: bytes([0xFF] * 12),
              wBoosterAveragedTypeChances_A: b"\xFF"},
     "instruction_budget": 200000, "cycle_budget": 1000000,
     "read": {wBoosterCardsDrawn_A: 0x16, wTempCardCollection_A: 256, wBoosterData_Set_A: 12,
              wBoosterAveragedTypeChances_A: 1}},
    dict(POISON, wram={wBoosterPackID_A: b"\x01", wBoosterCardsDrawn_A: bytes([0xFF] * 0x16),
              wTempCardCollection_A: bytes([0xFF] * 256), wBoosterData_Set_A: bytes([0xFF] * 12),
              wBoosterAveragedTypeChances_A: b"\xFF"},
         instruction_budget=200000, cycle_budget=1000000,
         read={wBoosterCardsDrawn_A: 0x16, wTempCardCollection_A: 256, wBoosterData_Set_A: 12,
              wBoosterAveragedTypeChances_A: 1}),
]
# <<< factory InitBoosterData

# >>> factory GenerateBoosterPack
CONTRACT["GenerateBoosterPack"] = {"compare": (), "preserve": (), "wram_out": True, "sram_out": True}
CASES["GenerateBoosterPack"] = [
    {"a": 0x00, "wram": {wBoosterCardsDrawn_A: bytes([0xFF] * 0x16), wTempCardCollection_A: bytes([0xFF] * 256)},
     "sram": {0: {sCardCollection_A: bytes(256)}},
     "instruction_budget": 2000000, "cycle_budget": 8000000,
     "read": {wBoosterCardsDrawn_A: 0x16}, "sread": {0: {sCardCollection_A: 256}}},
    dict(POISON, a=0x01, wram={wBoosterCardsDrawn_A: bytes([0xFF] * 0x16), wTempCardCollection_A: bytes([0xFF] * 256)},
         sram={0: {sCardCollection_A: bytes(256)}},
         instruction_budget=2000000, cycle_budget=8000000,
         read={wBoosterCardsDrawn_A: 0x16}, sread={0: {sCardCollection_A: 256}}),
]
# <<< factory GenerateBoosterPack

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
MUTATIONS["GenerateEnergyBoosterGrassPsychic"] = {"source_symbol": "GenerateEnergyBoosterGrassPsychic", "before": "\treturn GenerateTwoTypesEnergyBooster(EnergyBoosterGrassPsychicData_ADDR);", "after": "\treturn GenerateTwoTypesEnergyBooster(EnergyBoosterLightningFireData_ADDR);", "case_ids": ["GenerateEnergyBoosterGrassPsychic-0", "GenerateEnergyBoosterGrassPsychic-1"]}
# <<< factory-mutation GenerateEnergyBoosterGrassPsychic
# >>> factory-mutation GenerateEnergyBoosterLightningFire
MUTATIONS["GenerateEnergyBoosterLightningFire"] = {"source_symbol": "GenerateEnergyBoosterLightningFire", "before": "\treturn GenerateTwoTypesEnergyBooster(EnergyBoosterLightningFireData_ADDR);", "after": "\treturn GenerateTwoTypesEnergyBooster(EnergyBoosterWaterFightingData_ADDR);", "case_ids": ["GenerateEnergyBoosterLightningFire-0", "GenerateEnergyBoosterLightningFire-1"]}
# <<< factory-mutation GenerateEnergyBoosterLightningFire
# >>> factory-mutation GenerateEnergyBoosterWaterFighting
MUTATIONS["GenerateEnergyBoosterWaterFighting"] = {"source_symbol": "GenerateEnergyBoosterWaterFighting", "before": "\treturn GenerateTwoTypesEnergyBooster(EnergyBoosterWaterFightingData_ADDR);", "after": "\treturn GenerateTwoTypesEnergyBooster(EnergyBoosterGrassPsychicData_ADDR);", "case_ids": ["GenerateEnergyBoosterWaterFighting-0", "GenerateEnergyBoosterWaterFighting-1"]}
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
# >>> factory-mutation GenerateBoosterNonEnergies
MUTATIONS["GenerateBoosterNonEnergies"] = {
    "source_symbol": "GenerateBoosterNonEnergies",
    "before": "return (GenerateBoosterNonEnergiesResult){rarity, 0x00u};",
    "after": "return (GenerateBoosterNonEnergiesResult){rarity, 0x10u};",
    "case_ids": ["GenerateBoosterNonEnergies-0", "GenerateBoosterNonEnergies-1"],
}
# <<< factory-mutation GenerateBoosterNonEnergies
# >>> factory-mutation InitBoosterData
MUTATIONS["InitBoosterData"] = {"source_symbol": "InitBoosterData", "before": "\t\t\tc = (uint8_t)(a + c);", "after": "\t\t\tc = (uint8_t)(a + c + 1u);", "case_ids": ["InitBoosterData-0", "InitBoosterData-1"]}
# <<< factory-mutation InitBoosterData
# >>> factory-mutation GenerateBoosterPack
MUTATIONS["GenerateBoosterPack"] = {"source_symbol": "GenerateBoosterPack", "before": "\twBoosterPackID = a;", "after": "\twBoosterPackID = (uint8_t)(a + 1u);", "case_ids": ["GenerateBoosterPack-0", "GenerateBoosterPack-1"]}
# <<< factory-mutation GenerateBoosterPack
