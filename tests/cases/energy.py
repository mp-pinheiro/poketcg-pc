from tests.cases._symbols import sym
from tests.cases._fixtures import ai_energy_play_fixture as _ai_energy_play_fixture, AI_ENERGY_PLAY_REGS as _AI_ENERGY_PLAY_REGS, ai_energy_scoring_fixture as _ai_energy_scoring_fixture, AI_ENERGY_SCORING_REGS as _AI_ENERGY_SCORING_REGS
from tests.cases._fixtures import ai_energy_fixture as _ai_energy_fixture, AI_ENERGY_REGS as _AI_ENERGY_REGS, ai_try_energy_fixture as _ai_try_energy_fixture, AI_TRY_ENERGY_REGS as _AI_TRY_ENERGY_REGS, ai_evolution_energy_fixture as _ai_evolution_energy_fixture, AI_EVOLUTION_ENERGY_REGS as _AI_EVOLUTION_ENERGY_REGS
"""Oracle-diff cases for poketcg/src/engine/duel/ai/energy.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory RetrievePlayAreaAIScoreFromBackup1
CONTRACT["RetrievePlayAreaAIScoreFromBackup1"] = {"compare": ("a", "f", "c", "d", "e", "hl"), "preserve": ("a", "f", "c")}
CASES["RetrievePlayAreaAIScoreFromBackup1"] = [
    {"wram": {sym("wTempPlayAreaAIScore"): b"\x00" * 7, sym("wAIScore"): b"\x00" * 7}, "read": {sym("wAIScore"): 7}},
    {"wram": {sym("wTempPlayAreaAIScore"): b"\x11\x22\x33\x44\x55\x66\x77", sym("wAIScore"): b"\xaa" * 7}, "read": {sym("wAIScore"): 7}},
    dict(POISON, wram={sym("wTempPlayAreaAIScore"): b"\x01\x02\x03\x04\x05\x06\x07", sym("wAIScore"): b"\xff" * 7}, read={sym("wAIScore"): 7}),
]
# <<< factory RetrievePlayAreaAIScoreFromBackup1

# >>> factory FindPlayAreaCardWithHighestAIScore
CONTRACT["FindPlayAreaCardWithHighestAIScore"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["FindPlayAreaCardWithHighestAIScore"] = [
    # the whole 256-byte window scanned by the count-0 (== 256 iterations) loop is
    # seeded; wAIEnergyAttachLogicFlags (0xCDD8) lives at offset 25 inside it.
    {"wram": {sym("wFirstAttackAIScore"): b"\x00" * 256}, "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    {"wram": {sym("wFirstAttackAIScore"): b"\x85" + b"\x00" * 255}, "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    {"wram": {sym("wFirstAttackAIScore"): b"\x84" + b"\x00" * 255}, "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    {"wram": {sym("wFirstAttackAIScore"): b"\x00\x00\x00\x90" + b"\x00" * 252}, "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    {"wram": {sym("wFirstAttackAIScore"): b"\x00\x40\x90" + b"\x00" * 22 + b"\x80" + b"\x00" * 230}, "read": {sym("hTempPlayAreaLocation_ff9d"): 1}},
    dict(POISON, wram={sym("wFirstAttackAIScore"): b"\x00\x91\x00\x00\x91" + b"\x00" * 20 + b"\x80" + b"\x00" * 230}, read={sym("hTempPlayAreaLocation_ff9d"): 1}),
    dict(POISON, wram={sym("wFirstAttackAIScore"): b"\x90\x00\x90" + b"\x00" * 253}, read={sym("hTempPlayAreaLocation_ff9d"): 1}),
]
# <<< factory FindPlayAreaCardWithHighestAIScore

# >>> factory CheckSpecificDecksToAttachDoubleColorless
CONTRACT["CheckSpecificDecksToAttachDoubleColorless"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckSpecificDecksToAttachDoubleColorless"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {sym("wOpponentDeckID"): b"\x00"}},
    dict(POISON, wram={sym("wOpponentDeckID"): b"\x00"}),
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {sym("wOpponentDeckID"): b"\x17", sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x03", sym("wBoosterCardsDrawn")+3: b"\x36",
               sym("wPlayerNumberOfCardsInHand"): b"\x01", sym("wPlayerHand"): b"\x06", sym("wBoosterCardsDrawn")+6: b"\x07"}},
]
# <<< factory CheckSpecificDecksToAttachDoubleColorless

# >>> factory-cases-statics
hWhoseTurn = sym("hWhoseTurn")
hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")
wPlayerDeck = sym("wPlayerDeck")
wPlayerArenaCard = sym("wPlayerArenaCard")
wSelectedAttack = sym("wSelectedAttack")
wLoadedCard2 = sym("wLoadedCard2")
BULBASAUR = 0x08
IVYSAUR = 0x09
ZAPDOS_LV64_ID = 0x75
CHARIZARD_ID = 0x32

hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")
wSelectedAttack = sym("wSelectedAttack")
wTempAI = sym("wTempAI")
wLoadedCard1ID = sym("wLoadedCard1ID")
hWhoseTurn = sym("hWhoseTurn")

wAIBarrierFlagCounter = sym("wAIBarrierFlagCounter")
wAIScore = sym("wAIScore")
wDuelTempList = sym("wDuelTempList")
wPlayAreaAIScore = sym("wPlayAreaAIScore")
wPlayAreaEnergyAIScore = sym("wPlayAreaEnergyAIScore")
wTempAI = sym("wTempAI")
wTotalAttachedEnergies = sym("wTotalAttachedEnergies")
hTempPlayAreaLocation_ff9d = sym("hTempPlayAreaLocation_ff9d")

wAIScore = sym("wAIScore")
wPlayAreaAIScore = sym("wPlayAreaAIScore")
wTempPlayAreaAIScore = sym("wTempPlayAreaAIScore")
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
# b, c and e are CheckEnergyNeededForAttack's outputs for the evolution: the
# basic energy still needed, the colorless still needed and the basic energy's
# card ID, which AITryToPlayEnergyCard carries into .check_deck (energy.asm:849).
CONTRACT["CheckIfEvolutionNeedsEnergyForAttack"] = {"compare": ("a", "f", "b", "c", "e"), "preserve": ()}
# The three no-evolution exits leave through `or a / ret` with whatever
# CheckCardEvolutionInHandOrDeck left in bc and de; the caller returns on that
# no-carry without reading them, so they compare the verdict only.
CASES["CheckIfEvolutionNeedsEnergyForAttack"] = [
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerArenaCard"): b"\x07", sym("wPlayerCardLocations"): b"\xFF" * 60}, "compare": ("a", "f")},
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x01", sym("wPlayerArenaCard"): b"\x03", sym("wPlayerBench"): b"\x05", sym("wPlayerCardLocations"): b"\xFF" * 60}, "compare": ("a", "f")},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerArenaCard"): b"\x07", sym("wPlayerCardLocations"): b"\xFF" * 60}, compare=("a", "f")),
    dict(_ai_evolution_energy_fixture(bank=5), **_AI_EVOLUTION_ENERGY_REGS),
]
# <<< factory CheckIfEvolutionNeedsEnergyForAttack

# >>> factory AITryToPlayEnergyCard
CONTRACT["AITryToPlayEnergyCard"] = {"compare": ("a",), "preserve": ()}
CASES["AITryToPlayEnergyCard"] = [
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerCardLocations"): b"\xFF" * 60}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerCardLocations"): b"\xFF" * 60}),
    dict(_ai_try_energy_fixture(bank=5), **_AI_TRY_ENERGY_REGS),
    dict(_ai_energy_play_fixture(vram=False, bank=8), **_AI_ENERGY_PLAY_REGS, read={sym("wDuelTempList"): 8, sym("wRNG1"): 3, sym("hTempList"): 2}),
]
# <<< factory AITryToPlayEnergyCard

# >>> factory DetermineAIScoreOfAttackEnergyRequirement
CONTRACT["DetermineAIScoreOfAttackEnergyRequirement"] = {"compare": (), "preserve": ()}
CASES["DetermineAIScoreOfAttackEnergyRequirement"] = [
    {"a": 0x00, "wram": {sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerArenaCard"): b"\x07", sym("wPlayerCardLocations"): b"\xFF" * 60, sym("wTempAI"): b"\xFF"}, "read": {sym("wSelectedAttack"): 1}},
    {"a": 0x01, "wram": {sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerArenaCard"): b"\x07", sym("wPlayerCardLocations"): b"\xFF" * 60, sym("wTempAI"): b"\xFF"}, "read": {sym("wSelectedAttack"): 1}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("hTempPlayAreaLocation_ff9d"): b"\x00", sym("wPlayerArenaCard"): b"\x07", sym("wPlayerCardLocations"): b"\xFF" * 60, sym("wTempAI"): b"\xFF"}, read={sym("wSelectedAttack"): 1}),
]
# <<< factory DetermineAIScoreOfAttackEnergyRequirement

# >>> factory AIProcessEnergyCards
# energy.asm:265-285. The carry is the routine's only modelled output: set
# when a card was chosen, clear on every other exit.
CONTRACT["AIProcessEnergyCards"]={"compare":("a","f"),"preserve":()}
CASES["AIProcessEnergyCards"]=[
 {"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234,"wram":{sym("wAICardListEnergyBonus"):b"\0\0",sym("wAIEnergyAttachLogicFlags"):b"\2",sym("wAIBarrierFlagCounter"):b"\0",sym("wPlayerNumberOfPokemonInPlayArea"):b"\1",sym("wPlayerArenaCardHP"):b"\0",sym("hWhoseTurn"):b"\xC2",sym("wLCDC"):b"\0",sym("wDuelTempList"):b"\xff"},"read":{sym("wFirstAttackAIScore"):6,sym("wPlayAreaEnergyAIScore"):6},"setup":[{"fn":"CopyDMAFunction"},{"fn":"SetupText","d":0x20,"e":0x40}],"instruction_budget":20000000,"cycle_budget":80000000},
 {"wram":{sym("wAIEnergyAttachLogicFlags"):b"\2",sym("wPlayerNumberOfPokemonInPlayArea"):b"\1",sym("wPlayerArenaCardHP"):b"\0",sym("hWhoseTurn"):b"\xC2",sym("wLCDC"):b"\0",sym("wDuelTempList"):b"\xff"},"read":{sym("wFirstAttackAIScore"):6,sym("wPlayAreaEnergyAIScore"):6},"setup":[{"fn":"CopyDMAFunction"},{"fn":"SetupText","d":0x20,"e":0x40}],"instruction_budget":20000000,"cycle_budget":80000000},
 dict(_ai_energy_fixture(bank=5), **_AI_ENERGY_REGS),
]
# <<< factory AIProcessEnergyCards

# >>> factory AIProcessAndTryToPlayEnergy
CONTRACT["AIProcessAndTryToPlayEnergy"] = {"compare": (), "preserve": ()}
CASES["AIProcessAndTryToPlayEnergy"] = [
    {"wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wAIScore"): b"\x10" * 7, sym("wFirstAttackAIScore"): b"\x00" * 7}, "read": {sym("wFirstAttackAIScore"): 7}},
    dict(POISON, wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wAIScore"): b"\x20" * 7, sym("wFirstAttackAIScore"): b"\x00" * 7}, read={sym("wFirstAttackAIScore"): 7}),
    dict(_ai_energy_scoring_fixture(vram=False, bank=8), **_AI_ENERGY_SCORING_REGS, read={sym("wDuelTempList"): 8, sym("wRNG1"): 3, sym("hTempPlayAreaLocation_ff9d"): 1, sym("hTempList"): 2, sym("wAIScore"): 6}),
]
# <<< factory AIProcessAndTryToPlayEnergy

# >>> factory AIProcessButDontPlayEnergy_SkipEvolution
CONTRACT["AIProcessButDontPlayEnergy_SkipEvolution"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIProcessButDontPlayEnergy_SkipEvolution"] = [
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wAIScore"): b"\x5A", sym("wFirstAttackAIScore"): b"\x10\x20\x30\x40\x50\x60\x70", sym("wAICardListEnergyBonus"): b"\0\0", sym("wAIBarrierFlagCounter"): b"\0", sym("wPlayerNumberOfPokemonInPlayArea"): b"\1", sym("wPlayerArenaCardHP"): b"\0", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\0", sym("wDuelTempList"): b"\xff"}, "read": {sym("wAIEnergyAttachLogicFlags"): 1, sym("wTempPlayAreaAIScore"): 7, sym("wPlayAreaEnergyAIScore"): 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {sym("wAIScore"): b"\x5A", sym("wFirstAttackAIScore"): b"\x10\x20\x30\x40\x50\x60\x70", sym("wAICardListEnergyBonus"): b"\0\0", sym("wAIBarrierFlagCounter"): b"\0", sym("wPlayerNumberOfPokemonInPlayArea"): b"\1", sym("wPlayerArenaCardHP"): b"\0", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\0", sym("wDuelTempList"): b"\xff"}, "read": {sym("wAIEnergyAttachLogicFlags"): 1, sym("wTempPlayAreaAIScore"): 7, sym("wPlayAreaEnergyAIScore"): 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000}
]
# <<< factory AIProcessButDontPlayEnergy_SkipEvolution

# >>> factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena
CONTRACT["AIProcessButDontPlayEnergy_SkipEvolutionAndArena"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AIProcessButDontPlayEnergy_SkipEvolutionAndArena"] = [
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wAIScore"): b"\x11\x10\x20\x30\x40\x50\x60\x70", sym("wAICardListEnergyBonus"): b"\0\0", sym("wAIBarrierFlagCounter"): b"\0", sym("wPlayerNumberOfPokemonInPlayArea"): b"\1", sym("wPlayerArenaCardHP"): b"\0", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\0", sym("wDuelTempList"): b"\xff"}, "read": {sym("wAIEnergyAttachLogicFlags"): 1, sym("wTempPlayAreaAIScore"): 7, sym("wPlayAreaEnergyAIScore"): 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {sym("wAIScore"): b"\x7f\x81\x00\x00\x00\x00\x00\x00", sym("wAICardListEnergyBonus"): b"\0\0", sym("wAIBarrierFlagCounter"): b"\0", sym("wPlayerNumberOfPokemonInPlayArea"): b"\1", sym("wPlayerArenaCardHP"): b"\0", sym("hWhoseTurn"): b"\xC2", sym("wLCDC"): b"\0", sym("wDuelTempList"): b"\xff"}, "read": {sym("wAIEnergyAttachLogicFlags"): 1, sym("wTempPlayAreaAIScore"): 7, sym("wPlayAreaEnergyAIScore"): 6}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena

# >>> factory Func_16488
CONTRACT["Func_16488"] = {"compare": (), "preserve": ()}
CASES["Func_16488"] = [
    {"wram": {sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wAIScore"): b"\x77", sym("wFirstAttackAIScore"): b"\x10\x20\x30\x40\x50\x60\x70"}, "read": {sym("wAIEnergyAttachLogicFlags"): 1, sym("wAIScore"): 1, sym("wFirstAttackAIScore"): 7, sym("wTempPlayAreaAIScore"): 7}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wPlayerNumberOfCardsInHand"): b"\x00", sym("wAIScore"): b"\x88", sym("wFirstAttackAIScore"): b"\x01\x02\x03\x04\x05\x06\x07"}, "read": {sym("wAIEnergyAttachLogicFlags"): 1, sym("wAIScore"): 1, sym("wFirstAttackAIScore"): 7, sym("wTempPlayAreaAIScore"): 7}},
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
MUTATIONS["AITryToPlayEnergyCard"] = {"source_symbol": "AITryToPlayEnergyCard", "before": "\t\tif ((evo.f & 0x10u) == 0u)\n\t\t\treturn (AITryToPlayEnergyCardResult){evo.a, evo.f};", "after": "\t\tif ((evo.f & 0x10u) == 0u)\n\t\t\treturn (AITryToPlayEnergyCardResult){(uint8_t)(evo.a + 1u), evo.f};", "case_ids": ["AITryToPlayEnergyCard-0"]}
# <<< factory-mutation AITryToPlayEnergyCard
# >>> factory-mutation DetermineAIScoreOfAttackEnergyRequirement
MUTATIONS["DetermineAIScoreOfAttackEnergyRequirement"] = {"source_symbol": "DetermineAIScoreOfAttackEnergyRequirement", "before": "void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)\n{\n\twSelectedAttack = a;", "after": "void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)\n{\n\twSelectedAttack = (uint8_t)(a ^ 1u);", "case_ids": ["DetermineAIScoreOfAttackEnergyRequirement-0", "DetermineAIScoreOfAttackEnergyRequirement-1", "DetermineAIScoreOfAttackEnergyRequirement-2"]}
# <<< factory-mutation DetermineAIScoreOfAttackEnergyRequirement
# >>> factory-mutation AIProcessEnergyCards
MUTATIONS["AIProcessEnergyCards"] = {"source_symbol": "AIProcessEnergyCards", "before": "\t\tgb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + i), 0x80u);", "after": "\t\tgb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + i), 0x81u);", "case_ids": ["AIProcessEnergyCards-0", "AIProcessEnergyCards-2"]}
# <<< factory-mutation AIProcessEnergyCards
# >>> factory-mutation AIProcessAndTryToPlayEnergy
MUTATIONS["AIProcessAndTryToPlayEnergy"] = {"source_symbol": "AIProcessAndTryToPlayEnergy", "before": "AIEnergyResult AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;", "after": "AIEnergyResult AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 1u;", "case_ids": ["AIProcessAndTryToPlayEnergy-0", "AIProcessAndTryToPlayEnergy-1"]}
# <<< factory-mutation AIProcessAndTryToPlayEnergy
# >>> factory-mutation AIProcessButDontPlayEnergy_SkipEvolution
MUTATIONS["AIProcessButDontPlayEnergy_SkipEvolution"] = {"source_symbol": "AIProcessButDontPlayEnergy_SkipEvolution", "before": "\tgb_write8(de, wAIScore);\n\treturn AIProcessEnergyCards();\n}\n/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */", "after": "\twAIScore = gb_read8(hl);\n\treturn AIProcessEnergyCards();\n}\n/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */", "case_ids": ["AIProcessButDontPlayEnergy_SkipEvolution-0"]}
# <<< factory-mutation AIProcessButDontPlayEnergy_SkipEvolution
# >>> factory-mutation AIProcessButDontPlayEnergy_SkipEvolutionAndArena
MUTATIONS["AIProcessButDontPlayEnergy_SkipEvolutionAndArena"] = {"source_symbol": "AIProcessButDontPlayEnergy_SkipEvolutionAndArena", "before": "\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | AI_ENERGY_FLAG_SKIP_EVOLUTION | AI_ENERGY_FLAG_SKIP_ARENA_CARD;", "after": "\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | AI_ENERGY_FLAG_SKIP_EVOLUTION;", "case_ids": ["AIProcessButDontPlayEnergy_SkipEvolutionAndArena-0", "AIProcessButDontPlayEnergy_SkipEvolutionAndArena-1"]}
# <<< factory-mutation AIProcessButDontPlayEnergy_SkipEvolutionAndArena
# >>> factory-mutation Func_16488
MUTATIONS["Func_16488"] = {"source_symbol": "Func_16488", "before": "void Func_16488(void)\n{\n\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY;", "after": "void Func_16488(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;", "case_ids": ["Func_16488-0", "Func_16488-1"]}
# <<< factory-mutation Func_16488
