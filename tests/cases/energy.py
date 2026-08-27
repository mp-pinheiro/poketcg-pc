"""Oracle-diff cases for poketcg/src/engine/duel/ai/energy.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory RetrievePlayAreaAIScoreFromBackup1
CONTRACT["RetrievePlayAreaAIScoreFromBackup1"] = {"compare": ("a", "f", "c", "d", "e", "hl"), "preserve": ("a", "f", "c")}
CASES["RetrievePlayAreaAIScoreFromBackup1"] = [
    {"wram": {0xCDDD: b"\x00" * 7, 0xCDBE: b"\x00" * 7}, "read": {0xCDBE: 7}},
    {"wram": {0xCDDD: b"\x11\x22\x33\x44\x55\x66\x77", 0xCDBE: b"\xaa" * 7}, "read": {0xCDBE: 7}},
    dict(POISON, wram={0xCDDD: b"\x01\x02\x03\x04\x05\x06\x07", 0xCDBE: b"\xff" * 7}, read={0xCDBE: 7}),
]
# <<< factory RetrievePlayAreaAIScoreFromBackup1

# >>> factory FindPlayAreaCardWithHighestAIScore
CONTRACT["FindPlayAreaCardWithHighestAIScore"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["FindPlayAreaCardWithHighestAIScore"] = [
    # the whole 256-byte window scanned by the count-0 (== 256 iterations) loop is
    # seeded; wAIEnergyAttachLogicFlags (0xCDD8) lives at offset 25 inside it.
    {"wram": {0xCDBF: b"\x00" * 256}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x85" + b"\x00" * 255}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x84" + b"\x00" * 255}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x00\x00\x00\x90" + b"\x00" * 252}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x00\x40\x90" + b"\x00" * 22 + b"\x80" + b"\x00" * 230}, "read": {0xFF9D: 1}},
    dict(POISON, wram={0xCDBF: b"\x00\x91\x00\x00\x91" + b"\x00" * 20 + b"\x80" + b"\x00" * 230}, read={0xFF9D: 1}),
    dict(POISON, wram={0xCDBF: b"\x90\x00\x90" + b"\x00" * 253}, read={0xFF9D: 1}),
]
# <<< factory FindPlayAreaCardWithHighestAIScore

# >>> factory CheckSpecificDecksToAttachDoubleColorless
CONTRACT["CheckSpecificDecksToAttachDoubleColorless"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckSpecificDecksToAttachDoubleColorless"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {0xCC0E: b"\x00"}},
    dict(POISON, wram={0xCC0E: b"\x00"}),
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {0xCC0E: b"\x17", 0xFF97: b"\xC2", 0xC2BB: b"\x03", 0xC400+3: b"\x36",
               0xC2EE: b"\x01", 0xC242: b"\x06", 0xC400+6: b"\x07"}},
]
# <<< factory CheckSpecificDecksToAttachDoubleColorless

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D
wPlayerDeck = 0xC400
wPlayerArenaCard = 0xC2BB
wSelectedAttack = 0xCCC6
wLoadedCard2 = 0xCC65
BULBASAUR = 0x08
IVYSAUR = 0x09
ZAPDOS_LV64_ID = 0x75
CHARIZARD_ID = 0x32

hTempPlayAreaLocation_ff9d = 0xFF9D
wSelectedAttack = 0xCCC6
wTempAI = 0xCDF1
wLoadedAttackEffectParam = 0xCCB7
wLoadedCard1ID = 0xCC2B
hWhoseTurn = 0xFF97

wAIEnergyAttachLogicFlags = 0xCDD8
wAIBarrierFlagCounter = 0xCDA7
wAICardListEnergyBonus = 0xCDB2
wAIScore = 0xCDBE
wDuelTempList = 0xC510
wPlayAreaAIScore = 0xCDBF
wPlayAreaEnergyAIScore = 0xCDE4
wTempAI = 0xCDF1
wTotalAttachedEnergies = 0xCC23
hTempPlayAreaLocation_ff9d = 0xFF9D

wAIEnergyAttachLogicFlags = 0xCDD8
wAIScore = 0xCDBE
wPlayAreaAIScore = 0xCDBF
wTempPlayAreaAIScore = 0xCDDD
# <<< factory-cases-statics

# >>> factory GetEnergyCardForDiscardOrEnergyBoostAttack
CONTRACT["GetEnergyCardForDiscardOrEnergyBoostAttack"] = {"compare": ("a", "b", "c", "e", "f"), "preserve": (), "wram_out": True}
CASES["GetEnergyCardForDiscardOrEnergyBoostAttack"] = [
    {"c": 0x77, "wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
              wPlayerArenaCard: b"\x00", wPlayerDeck: bytes((BULBASAUR,)),
              wSelectedAttack: b"\x00"},
     "read": {wLoadedCard2: 64}},
    dict(POISON, wram={hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
                       wPlayerArenaCard: b"\x01", wPlayerDeck + 1: bytes((IVYSAUR,)),
                       wSelectedAttack: b"\x01"},
         read={wLoadedCard2: 64}),
    {"c": 0x99, "wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
              wPlayerArenaCard: b"\x02", wPlayerDeck + 2: bytes((ZAPDOS_LV64_ID,)),
              wSelectedAttack: b"\x01"},
     "read": {wLoadedCard2: 64}},
    {"c": 0x55, "wram": {hWhoseTurn: b"\xC2", hTempPlayAreaLocation_ff9d: b"\x00",
              wPlayerArenaCard: b"\x03", wPlayerDeck + 3: bytes((CHARIZARD_ID,)),
              wSelectedAttack: b"\x01"},
     "read": {wLoadedCard2: 64}},
]
# <<< factory GetEnergyCardForDiscardOrEnergyBoostAttack

# >>> factory CheckIfEvolutionNeedsEnergyForAttack
CONTRACT["CheckIfEvolutionNeedsEnergyForAttack"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CheckIfEvolutionNeedsEnergyForAttack"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x07", 0xC200: b"\xFF" * 60}},
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x01", 0xC2BB: b"\x03", 0xC2BC: b"\x05", 0xC200: b"\xFF" * 60}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x07", 0xC200: b"\xFF" * 60}),
]
# <<< factory CheckIfEvolutionNeedsEnergyForAttack

# >>> factory AITryToPlayEnergyCard
CONTRACT["AITryToPlayEnergyCard"] = {"compare": ("a",), "preserve": ()}
CASES["AITryToPlayEnergyCard"] = [
    {"wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC200: b"\xFF" * 60}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC200: b"\xFF" * 60}),
]
# <<< factory AITryToPlayEnergyCard

# >>> factory DetermineAIScoreOfAttackEnergyRequirement
CONTRACT["DetermineAIScoreOfAttackEnergyRequirement"] = {"compare": (), "preserve": ()}
CASES["DetermineAIScoreOfAttackEnergyRequirement"] = [
    {"a": 0x00, "wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x07", 0xC200: b"\xFF" * 60, 0xCDF1: b"\xFF"}, "read": {0xCCC6: 1}},
    {"a": 0x01, "wram": {0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x07", 0xC200: b"\xFF" * 60, 0xCDF1: b"\xFF"}, "read": {0xCCC6: 1}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xFF9D: b"\x00", 0xC2BB: b"\x07", 0xC200: b"\xFF" * 60, 0xCDF1: b"\xFF"}, read={0xCCC6: 1}),
]
# <<< factory DetermineAIScoreOfAttackEnergyRequirement

# >>> factory AIProcessEnergyCards
CONTRACT["AIProcessEnergyCards"]={"compare":(),"preserve":()}
CASES["AIProcessEnergyCards"]=[
 {"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234,"wram":{0xCDB2:b"\0\0",0xCDD8:b"\2",0xCDA7:b"\0",0xC2EF:b"\1",0xC2C8:b"\0",0xFF97:b"\xC2",0xCABB:b"\0",0xC510:b"\xff"},"read":{0xCDBF:6,0xCDE4:6},"setup":[{"fn":"CopyDMAFunction"},{"fn":"SetupText","d":0x20,"e":0x40}],"instruction_budget":20000000,"cycle_budget":80000000},
 {"wram":{0xCDD8:b"\2",0xC2EF:b"\1",0xC2C8:b"\0",0xFF97:b"\xC2",0xCABB:b"\0",0xC510:b"\xff"},"read":{0xCDBF:6,0xCDE4:6},"setup":[{"fn":"CopyDMAFunction"},{"fn":"SetupText","d":0x20,"e":0x40}],"instruction_budget":20000000,"cycle_budget":80000000}
]
# <<< factory AIProcessEnergyCards

# >>> factory AIProcessAndTryToPlayEnergy
CONTRACT["AIProcessAndTryToPlayEnergy"] = {"compare": (), "preserve": ()}
CASES["AIProcessAndTryToPlayEnergy"] = [
    {"wram": {0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xCDBE: b"\x10" * 7, 0xCDBF: b"\x00" * 7}, "read": {0xCDBF: 7}},
    dict(POISON, wram={0xFF97: b"\xC2", 0xC2EE: b"\x00", 0xCDBE: b"\x20" * 7, 0xCDBF: b"\x00" * 7}, read={0xCDBF: 7}),
]
# <<< factory AIProcessAndTryToPlayEnergy

# >>> factory AIProcessButDontPlayEnergy_SkipEvolution
CONTRACT["AIProcessButDontPlayEnergy_SkipEvolution"] = {"compare": (), "preserve": ()}
CASES["AIProcessButDontPlayEnergy_SkipEvolution"] = [
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCDBF: b"\x10\x20\x30\x40\x50\x60\x70", 0xCDB2: b"\0\0", 0xCDA7: b"\0", 0xC2EF: b"\1", 0xC2C8: b"\0", 0xFF97: b"\xC2", 0xCABB: b"\0", 0xC510: b"\xff"}, "read": {0xCDD8: 1, 0xCDDD: 7, 0xCDE4: 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {0xCDBF: b"\x10\x20\x30\x40\x50\x60\x70", 0xCDB2: b"\0\0", 0xCDA7: b"\0", 0xC2EF: b"\1", 0xC2C8: b"\0", 0xFF97: b"\xC2", 0xCABB: b"\0", 0xC510: b"\xff"}, "read": {0xCDD8: 1, 0xCDDD: 7, 0xCDE4: 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory AIProcessButDontPlayEnergy_SkipEvolution

# >>> factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena
CONTRACT["AIProcessButDontPlayEnergy_SkipEvolutionAndArena"] = {"compare": (), "preserve": ()}
CASES["AIProcessButDontPlayEnergy_SkipEvolutionAndArena"] = [
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCDBE: b"\x11\x10\x20\x30\x40\x50\x60\x70", 0xCDB2: b"\0\0", 0xCDA7: b"\0", 0xC2EF: b"\1", 0xC2C8: b"\0", 0xFF97: b"\xC2", 0xCABB: b"\0", 0xC510: b"\xff"}, "read": {0xCDD8: 1, 0xCDDD: 7, 0xCDE4: 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {0xCDBE: b"\x7f\x81\x00\x00\x00\x00\x00\x00", 0xCDB2: b"\0\0", 0xCDA7: b"\0", 0xC2EF: b"\1", 0xC2C8: b"\0", 0xFF97: b"\xC2", 0xCABB: b"\0", 0xC510: b"\xff"}, "read": {0xCDD8: 1, 0xCDDD: 7, 0xCDE4: 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena

# >>> factory Func_16488
CONTRACT["Func_16488"] = {"compare": (), "preserve": ()}
CASES["Func_16488"] = [
    {"wram": {0xC2EE: b"\x00", 0xCDBE: b"\x77", 0xCDBF: b"\x10\x20\x30\x40\x50\x60\x70"}, "read": {0xCDD8: 1, 0xCDBE: 1, 0xCDBF: 7, 0xCDDD: 7}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xC2EE: b"\x00", 0xCDBE: b"\x88", 0xCDBF: b"\x01\x02\x03\x04\x05\x06\x07"}, "read": {0xCDD8: 1, 0xCDBE: 1, 0xCDBF: 7, 0xCDDD: 7}},
]
# <<< factory Func_16488

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation RetrievePlayAreaAIScoreFromBackup1
MUTATIONS["RetrievePlayAreaAIScoreFromBackup1"] = {
    "source_symbol": "RetrievePlayAreaAIScoreFromBackup1",
    "before": "for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {",
    "after": "for (uint8_t b = MAX_PLAY_AREA_POKEMON - 1u; b != 0u; b--) {",
    "case_ids": ["RetrievePlayAreaAIScoreFromBackup1-1", "RetrievePlayAreaAIScoreFromBackup1-2"],
}
# <<< factory-mutation RetrievePlayAreaAIScoreFromBackup1
# >>> factory-mutation FindPlayAreaCardWithHighestAIScore
MUTATIONS["FindPlayAreaCardWithHighestAIScore"] = {
    "source_symbol": "FindPlayAreaCardWithHighestAIScore",
    "before": "\tif (e < 0x85u) {",
    "after": "\tif (e < 0x86u) {",
    "case_ids": ["FindPlayAreaCardWithHighestAIScore-1"],
}
# <<< factory-mutation FindPlayAreaCardWithHighestAIScore
# >>> factory-mutation CheckSpecificDecksToAttachDoubleColorless
MUTATIONS["CheckSpecificDecksToAttachDoubleColorless"] = {"source_symbol": "CheckSpecificDecksToAttachDoubleColorless", "before": "return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x10u, b, c, d, e, hl};", "after": "return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x00u, b, c, d, e, hl};", "case_ids": ["CheckSpecificDecksToAttachDoubleColorless-2"]}
# <<< factory-mutation CheckSpecificDecksToAttachDoubleColorless
# >>> factory-mutation GetEnergyCardForDiscardOrEnergyBoostAttack
MUTATIONS["GetEnergyCardForDiscardOrEnergyBoostAttack"] = {"source_symbol": "GetEnergyCardForDiscardOrEnergyBoostAttack", "before": "return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, b, c_in, 0u, 0x00u};", "after": "return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, b, (uint8_t)(c_in + 1u), 0u, 0x00u};", "case_ids": ["GetEnergyCardForDiscardOrEnergyBoostAttack-2"]}
# <<< factory-mutation GetEnergyCardForDiscardOrEnergyBoostAttack
# >>> factory-mutation CheckIfEvolutionNeedsEnergyForAttack
MUTATIONS["CheckIfEvolutionNeedsEnergyForAttack"] = {"source_symbol": "CheckIfEvolutionNeedsEnergyForAttack", "before": "uint8_t f_out = (evo.a == 0u) ? 0x80u : 0x00u;", "after": "uint8_t f_out = (evo.a == 0u) ? 0x00u : 0x80u;", "case_ids": ["CheckIfEvolutionNeedsEnergyForAttack-0", "CheckIfEvolutionNeedsEnergyForAttack-1"]}
# <<< factory-mutation CheckIfEvolutionNeedsEnergyForAttack
# >>> factory-mutation AITryToPlayEnergyCard
MUTATIONS["AITryToPlayEnergyCard"] = {"source_symbol": "AITryToPlayEnergyCard", "before": "CheckIfEvolutionNeedsEnergyForAttackResult evo =\n\t\t\tCheckIfEvolutionNeedsEnergyForAttack(0u, 0u, 0u, 0u, 0u);\n\t\tif ((evo.f & 0x10u) == 0u)\n\t\t\treturn 0u;", "after": "CheckIfEvolutionNeedsEnergyForAttackResult evo =\n\t\t\tCheckIfEvolutionNeedsEnergyForAttack(0u, 0u, 0u, 0u, 0u);\n\t\tif ((evo.f & 0x10u) == 0u)\n\t\t\treturn 1u;", "case_ids": ["AITryToPlayEnergyCard-0"]}
# <<< factory-mutation AITryToPlayEnergyCard
# >>> factory-mutation DetermineAIScoreOfAttackEnergyRequirement
MUTATIONS["DetermineAIScoreOfAttackEnergyRequirement"] = {"source_symbol": "DetermineAIScoreOfAttackEnergyRequirement", "before": "void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)\n{\n\twSelectedAttack = a;", "after": "void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)\n{\n\twSelectedAttack = (uint8_t)(a ^ 1u);", "case_ids": ["DetermineAIScoreOfAttackEnergyRequirement-0", "DetermineAIScoreOfAttackEnergyRequirement-1", "DetermineAIScoreOfAttackEnergyRequirement-2"]}
# <<< factory-mutation DetermineAIScoreOfAttackEnergyRequirement
# >>> factory-mutation AIProcessEnergyCards
MUTATIONS["AIProcessEnergyCards"]={"source_symbol":"AIProcessEnergyCards","before":"\tfor (uint8_t i=0; i<MAX_PLAY_AREA_POKEMON; ++i) gb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR+i),0x80u);","after":"\tfor (uint8_t i=0; i<MAX_PLAY_AREA_POKEMON; ++i) gb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR+i),0x81u);","case_ids":["AIProcessEnergyCards-0"]}
# <<< factory-mutation AIProcessEnergyCards
# >>> factory-mutation AIProcessAndTryToPlayEnergy
MUTATIONS["AIProcessAndTryToPlayEnergy"] = {"source_symbol": "AIProcessAndTryToPlayEnergy", "before": "void AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;", "after": "void AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 1u;", "case_ids": ["AIProcessAndTryToPlayEnergy-0", "AIProcessAndTryToPlayEnergy-1"]}
# <<< factory-mutation AIProcessAndTryToPlayEnergy
# >>> factory-mutation AIProcessButDontPlayEnergy_SkipEvolution
MUTATIONS["AIProcessButDontPlayEnergy_SkipEvolution"] = {"source_symbol": "AIProcessButDontPlayEnergy_SkipEvolution", "before": "void AIProcessButDontPlayEnergy_SkipEvolution(void)\n{\n\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | AI_ENERGY_FLAG_SKIP_EVOLUTION;", "after": "void AIProcessButDontPlayEnergy_SkipEvolution(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;", "case_ids": ["AIProcessButDontPlayEnergy_SkipEvolution-0"]}
# <<< factory-mutation AIProcessButDontPlayEnergy_SkipEvolution
# >>> factory-mutation AIProcessButDontPlayEnergy_SkipEvolutionAndArena
MUTATIONS["AIProcessButDontPlayEnergy_SkipEvolutionAndArena"] = {"source_symbol": "AIProcessButDontPlayEnergy_SkipEvolutionAndArena", "before": "void AIProcessButDontPlayEnergy_SkipEvolutionAndArena(void)\n{\n\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | AI_ENERGY_FLAG_SKIP_EVOLUTION | AI_ENERGY_FLAG_SKIP_ARENA_CARD;", "after": "void AIProcessButDontPlayEnergy_SkipEvolutionAndArena(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;", "case_ids": ["AIProcessButDontPlayEnergy_SkipEvolutionAndArena-0", "AIProcessButDontPlayEnergy_SkipEvolutionAndArena-1"]}
# <<< factory-mutation AIProcessButDontPlayEnergy_SkipEvolutionAndArena
# >>> factory-mutation Func_16488
MUTATIONS["Func_16488"] = {"source_symbol": "Func_16488", "before": "void Func_16488(void)\n{\n\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY;", "after": "void Func_16488(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;", "case_ids": ["Func_16488-0", "Func_16488-1"]}
# <<< factory-mutation Func_16488
