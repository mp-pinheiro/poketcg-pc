"""Extended oracle-diff cases for energy: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter"))
_BENCH = Fixture("ai-duel-fire-charge-determineaiscore-bench-entry", directory=_FIXTURES, holes=_HOLES, lcdc=sym("wLCDC"))
_ARTICUNO_ENERGY = Fixture("legendary-articuno-aiprocessandtrytoplayenergy-entry", directory=_FIXTURES, holes=_HOLES)
_FIRE_ENERGY = Fixture("ai-duel-fire-charge-aiprocessandtrytoplayenergy-entry", directory=_FIXTURES, holes=_HOLES)

def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('energy', remove=('Func_16488',))
OWN = (
    'AIProcessAndTryToPlayEnergy',
    'AIProcessEnergyCards',
    'AITryToPlayEnergyCard',
    'CheckSpecificDecksToAttachDoubleColorless',
    'DetermineAIScoreOfAttackEnergyRequirement',
)
CONTRACT.update({
    'CheckSpecificDecksToAttachDoubleColorless': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'AITryToPlayEnergyCard': {'compare': ('a',), 'preserve': ()},
    'DetermineAIScoreOfAttackEnergyRequirement': {'compare': (), 'preserve': ()},
    'AIProcessEnergyCards': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'AIProcessAndTryToPlayEnergy': {'compare': ('a', 'f'), 'preserve': ()},
})
CASES.update({
    'CheckSpecificDecksToAttachDoubleColorless': [
        {'b': 0x11, 'c': 0x22, 'd': 0x33, 'e': 0x44, 'hl': 0x5566, 'wram': {sym("wOpponentDeckID"): b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wOpponentDeckID"): b'\x00'}},
        {   'b': 0x11,
            'c': 0x22,
            'd': 0x33,
            'e': 0x44,
            'hl': 0x5566,
            'wram': {   sym("wOpponentDeckID"): b'\x17',
                        sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerArenaCard"): b'\x03',
                        sym("wBoosterCardsDrawn") + 3: b'6',
                        sym("wPlayerNumberOfCardsInHand"): b'\x01',
                        sym("wPlayerHand"): b'\x06',
                        sym("wBoosterCardsDrawn") + 6: b'\x07'}},
        {'wram': {sym("wOpponentDeckID"): b'\x0f', sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCard"): b'\x00',
                  sym("wPlayerNumberOfCardsInHand"): b'\x01', sym("wPlayerHand"): b'\x01',
                  sym("wBoosterCardsDrawn"): b'\x30\x01\x07\x00'}},
    ],
    'AITryToPlayEnergyCard': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempPlayAreaLocation_ff9d"): b'\x00', sym("wPlayerCardLocations"): b'\xff' * 60}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempPlayAreaLocation_ff9d"): b'\x00', sym("wPlayerCardLocations"): b'\xff' * 60}},
        {'a': 0x08, 'b': 0x00, 'c': 0x03, 'd': 0x00,
         'e': 0x8C, 'f': 0x00, 'hl': sym("wFirstAttackAIScore") + 3,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempPlayAreaLocation_ff9d"): b'\x00', sym("wPlayerCardLocations"): b'\xff' * 60}},
        {'a': 0x0A, 'b': 0x00, 'c': 0x03, 'd': 0x00,
         'e': 0x8F, 'f': 0x00, 'hl': sym("wFirstAttackAIScore") + 3,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("hTempPlayAreaLocation_ff9d"): b'\x00', sym("wPlayerCardLocations"): b'\xff' * 60}},
    ],
    'DetermineAIScoreOfAttackEnergyRequirement': [
        {   'a': 0x00,
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("hTempPlayAreaLocation_ff9d"): b'\x00',
                        sym("wPlayerArenaCard"): b'\x07',
                        sym("wPlayerCardLocations"): b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        sym("wTempAI"): b'\xff'},
            'read': {sym("wSelectedAttack"): 0x01, sym("wAIScore"): 0x01}},
        {   'a': 0x01,
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("hTempPlayAreaLocation_ff9d"): b'\x00',
                        sym("wPlayerArenaCard"): b'\x07',
                        sym("wPlayerCardLocations"): b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        sym("wTempAI"): b'\xff'},
            'read': {sym("wSelectedAttack"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("hTempPlayAreaLocation_ff9d"): b'\x00',
                        sym("wPlayerArenaCard"): b'\x07',
                        sym("wPlayerCardLocations"): b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        sym("wTempAI"): b'\xff'},
            'read': {sym("wSelectedAttack"): 0x01}},
        dict(_fixture_case(_BENCH), **_BENCH.regs),
        dict(_fixture_case(_BENCH), **_BENCH.regs),
    ],
    'AIProcessEnergyCards': [
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {sym("wAICardListEnergyBonus"): b'\x00\x00', sym("wAIEnergyAttachLogicFlags"): b'\x02',
                  sym("wAIBarrierFlagCounter"): b'\x00', sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01', sym("wPlayerArenaCardHP"): b'\x00',
                  sym("hWhoseTurn"): b'\xc2', sym("wLCDC"): b'\x00', sym("wDuelTempList"): b'\xff'},
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400},
        {'wram': {sym("wAIEnergyAttachLogicFlags"): b'\x02', sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01',
                  sym("wPlayerArenaCardHP"): b'\x00', sym("hWhoseTurn"): b'\xc2',
                  sym("wLCDC"): b'\x00', sym("wDuelTempList"): b'\xff'},
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400},
        {'a': 0x08, 'b': 0x73, 'c': 0x00, 'd': 0x0C,
         'e': 0x6D, 'f': 0x00, 'hl': sym("wUniqueDeckCardList") + 6,
         'wram': {sym("wAIEnergyAttachLogicFlags"): b'\x02', sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01',
                  sym("wPlayerArenaCardHP"): b'\x00', sym("hWhoseTurn"): b'\xc2',
                  sym("wLCDC"): b'\x00', sym("wDuelTempList"): b'\xff'},
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400},
        {'a': 0x08, 'b': 0x73, 'c': 0x00, 'd': 0x0C,
         'e': 0x6D, 'f': 0x00, 'hl': sym("wUniqueDeckCardList") + 6,
         'wram': {sym("wPlayAreaEnergyAIScore"): b'\x00' * 7, sym("wAIEnergyAttachLogicFlags"): b'\x02',
                  sym("wPlayerNumberOfPokemonInPlayArea"): b'\x01', sym("wPlayerArenaCardHP"): b'\x00', sym("hWhoseTurn"): b'\xc2',
                  sym("wLCDC"): b'\x00', sym("wDuelTempList"): b'\xff'},
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400, 'snapshot': True},
    ],
    'AIProcessAndTryToPlayEnergy': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerNumberOfCardsInHand"): b'\x00',
                  sym("wAIScore"): b'\x10' * 7, sym("wFirstAttackAIScore"): b'\x00' * 7},
         'read': {sym("wFirstAttackAIScore"): 0x07}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerNumberOfCardsInHand"): b'\x00',
                  sym("wAIScore"): b' ' * 7, sym("wFirstAttackAIScore"): b'\x00' * 7},
         'read': {sym("wFirstAttackAIScore"): 0x07}},
        {'a': 0x00, 'f': 0x80, 'b': 0x05, 'c': 0x00,
         'd': 0x0C, 'e': 0x6D, 'hl': sym("wUniqueDeckCardList") + 6,
         'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerNumberOfCardsInHand"): b'\x00',
                  sym("wAIScore"): b'\x10' * 7, sym("wFirstAttackAIScore"): b'\x00' * 7},
         'read': {sym("wFirstAttackAIScore"): 0x07}},
    ],
})
CASES['AIProcessAndTryToPlayEnergy'] += [
    dict(_fixture_case(_ARTICUNO_ENERGY), **_ARTICUNO_ENERGY.regs),
    dict(_fixture_case(_FIRE_ENERGY), **_FIRE_ENERGY.regs),
]
MUTATIONS.update({
    'CheckSpecificDecksToAttachDoubleColorless': {   'source_symbol': 'CheckSpecificDecksToAttachDoubleColorless',
        'before': 'if (card_id == CHARMANDER || card_id == DRATINI)',
        'after': 'if ((uint8_t)card_id == CHARMANDER || (uint8_t)card_id == DRATINI)',
        'case_ids': ['CheckSpecificDecksToAttachDoubleColorless-3'],
        'source': 'src/profiles/extended/home/energy.c'},
    'GetEnergyCardForDiscardOrEnergyBoostAttack': {   'source_symbol': 'GetEnergyCardForDiscardOrEnergyBoostAttack',
        'before': 'return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, TRUE, FALSE, e, f};',
        'after': 'return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, FALSE, FALSE, e, f};',
        'case_ids': ['GetEnergyCardForDiscardOrEnergyBoostAttack-0'],
        'source': 'src/profiles/extended/home/energy.c'},
    'AITryToPlayEnergyCard': {   'source_symbol': 'AITryToPlayEnergyCard',
        'before': '\t\tif ((evo.f & 0x10u) == 0u)\n'
                  '\t\t\treturn (AITryToPlayEnergyCardResult){evo.a, evo.f};',
        'after': '\t\tif ((evo.f & 0x10u) == 0u)\n'
                 '\t\t\treturn (AITryToPlayEnergyCardResult){(uint8_t)(evo.a + 1u), evo.f};',
        'case_ids': ['AITryToPlayEnergyCard-0'],
        'source': 'src/profiles/extended/home/energy.c'},
    'DetermineAIScoreOfAttackEnergyRequirement': {   'source_symbol': 'DetermineAIScoreOfAttackEnergyRequirement',
        'before': 'void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)\n'
                  '{\n'
                  '\twSelectedAttack = a;',
        'after': 'void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)\n'
                 '{\n'
                 '\twSelectedAttack = (uint8_t)(a ^ 1u);',
        'case_ids': [   'DetermineAIScoreOfAttackEnergyRequirement-0',
                        'DetermineAIScoreOfAttackEnergyRequirement-1',
                        'DetermineAIScoreOfAttackEnergyRequirement-2'],
        'source': 'src/profiles/extended/home/energy.c'},
    'AIProcessEnergyCards': {   'source_symbol': 'AIProcessEnergyCards',
        'before': '\t\tgb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + i), 0x80u);',
        'after': '\t\tgb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + i), 0x81u);',
        'case_ids': ['AIProcessEnergyCards-3', 'AIProcessEnergyCards-0',
                     'AIProcessEnergyCards-2'],
        'source': 'src/profiles/extended/home/energy.c'},
    'AIProcessAndTryToPlayEnergy': {   'source_symbol': 'AIProcessAndTryToPlayEnergy',
        'before': 'AIEnergyResult AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;',
        'after': 'AIEnergyResult AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 1u;',
        'case_ids': ['AIProcessAndTryToPlayEnergy-0', 'AIProcessAndTryToPlayEnergy-1'],
        'source': 'src/profiles/extended/home/energy.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
