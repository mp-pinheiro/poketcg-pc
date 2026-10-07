"""Extended oracle-diff cases for energy, seeded from tests/cases/energy.py."""

from pathlib import Path

from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D)
_BENCH = Fixture("ai-duel-fire-charge-determineaiscore-bench-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
_ARTICUNO_ENERGY = Fixture("legendary-articuno-aiprocessandtrytoplayenergy-entry", directory=_FIXTURES, holes=_HOLES)
_FIRE_ENERGY = Fixture("ai-duel-fire-charge-aiprocessandtrytoplayenergy-entry", directory=_FIXTURES, holes=_HOLES)
def _fixture_case(fixture):
    case = fixture.case(vram=False)
    case["read"][0xCC00] = 0xBD
    case["read"][0xCCBE] = 0x42
    return case


CONTRACT = {
    'RetrievePlayAreaAIScoreFromBackup1': {'compare': ('a', 'f', 'c', 'd', 'e', 'hl'), 'preserve': ('a', 'f', 'c')},
    'FindPlayAreaCardWithHighestAIScore': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'CheckSpecificDecksToAttachDoubleColorless': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetEnergyCardForDiscardOrEnergyBoostAttack': {'compare': ('a', 'b', 'c', 'e', 'f'), 'preserve': (), 'wram_out': True},
    'CheckIfEvolutionNeedsEnergyForAttack': {'compare': ('a', 'f', 'b', 'c', 'e'), 'preserve': ()},
    'AITryToPlayEnergyCard': {'compare': ('a',), 'preserve': ()},
    'DetermineAIScoreOfAttackEnergyRequirement': {'compare': (), 'preserve': ()},
    'AIProcessEnergyCards': {'compare': ('a', 'f'), 'preserve': (), 'wram_out': True},
    'AIProcessAndTryToPlayEnergy': {'compare': ('a', 'f'), 'preserve': ()},
    'AIProcessButDontPlayEnergy_SkipEvolution': {'compare': ('a', 'f'), 'preserve': ()},
    'AIProcessButDontPlayEnergy_SkipEvolutionAndArena': {'compare': ('a', 'f'), 'preserve': ()},
}

CASES = {
    'RetrievePlayAreaAIScoreFromBackup1': [
        {   'wram': {0xCD64: b'\x00\x00\x00\x00\x00\x00\x00', 0xCD44: b'\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xCD44: 0x07}},
        {   'wram': {0xCD64: b'\x11"3DUfw', 0xCD44: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xCD44: 0x07}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCD64: b'\x01\x02\x03\x04\x05\x06\x07', 0xCD44: b'\xff\xff\xff\xff\xff\xff\xff'},
            'read': {0xCD44: 0x07}},
    ],
    'FindPlayAreaCardWithHighestAIScore': [
        {   'wram': {   0xCD45: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
        {   'wram': {   0xCD45: b'\x85\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
        {   'wram': {   0xCD45: b'\x84\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
        {   'wram': {   0xCD45: b'\x00\x00\x00\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
        {   'wram': {   0xCD45: b'\x00@\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCD45: b'\x00\x91\x00\x00\x91\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCD45: b'\x90\x00\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xFF9D: 0x01}},
    ],
    'CheckSpecificDecksToAttachDoubleColorless': [
        {'b': 0x11, 'c': 0x22, 'd': 0x33, 'e': 0x44, 'hl': 0x5566, 'wram': {0xCBB8: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCBB8: b'\x00'}},
        {   'b': 0x11,
            'c': 0x22,
            'd': 0x33,
            'e': 0x44,
            'hl': 0x5566,
            'wram': {   0xCBB8: b'\x17',
                        0xFF97: b'\xc2',
                        0xC2BB: b'\x03',
                        0xC403: b'6',
                        0xC2EE: b'\x01',
                        0xC242: b'\x06',
                        0xC406: b'\x07'}},
        {'wram': {0xCBB8: b'\x0f', 0xFF97: b'\xc2', 0xC2BB: b'\x00',
                  0xC2EE: b'\x01', 0xC242: b'\x01',
                  0xC400: b'\x30\x01\x07\x00'}},
    ],
    'GetEnergyCardForDiscardOrEnergyBoostAttack': [
        {   'c': 0x77,
            'wram': {   0xFF97: b'\xc2',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x00',
                        0xC400: b'\x08',
                        0xCC74: b'\x00'},
            'read': {0xCC10: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC2BB: b'\x01', 0xC401: b'\t', 0xCC74: b'\x01'},
            'read': {0xCC10: 0x40}},
        {   'c': 0x99,
            'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC2BB: b'\x02', 0xC402: b'u', 0xCC74: b'\x01'},
            'read': {0xCC10: 0x40}},
        {   'c': 0x55,
            'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC2BB: b'\x03', 0xC403: b'2', 0xCC74: b'\x01'},
            'read': {0xCC10: 0x40}},
    ],
    'CheckIfEvolutionNeedsEnergyForAttack': [
        {'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC2BB: b'\x07',
                  0xC200: b'\xff' * 60},
         'compare': ('a', 'f')},
        {'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x01', 0xC2BB: b'\x03',
                  0xC2BC: b'\x05', 0xC200: b'\xff' * 60},
         'compare': ('a', 'f')},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC2BB: b'\x07',
                  0xC200: b'\xff' * 60},
         'compare': ('a', 'f')},
        {   'a': 0x00,
            'compare': ('a', 'f'),
            'f': 0xA0,
            'b': 0x00,
            'c': 0x00,
            'd': 0xCB,
            'e': 0xAA,
            'hl': 0xCC56,
            'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC2BB: b'\x07',
                     0xC200: b'\xff' * 60}},
    ],
    'AITryToPlayEnergyCard': [
        {'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC200: b'\xff' * 60}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC200: b'\xff' * 60}},
        {'a': 0x08, 'b': 0x00, 'c': 0x03, 'd': 0x00,
         'e': 0x8C, 'f': 0x00, 'hl': 0xCD48,
         'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC200: b'\xff' * 60}},
        {'a': 0x0A, 'b': 0x00, 'c': 0x03, 'd': 0x00,
         'e': 0x8F, 'f': 0x00, 'hl': 0xCD48,
         'wram': {0xFF97: b'\xc2', 0xFF9D: b'\x00', 0xC200: b'\xff' * 60}},
    ],
    'DetermineAIScoreOfAttackEnergyRequirement': [
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xc2',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x07',
                        0xC200: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xCD78: b'\xff'},
            'read': {0xCC74: 0x01, 0xCD44: 0x01}},
        {   'a': 0x01,
            'wram': {   0xFF97: b'\xc2',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x07',
                        0xC200: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xCD78: b'\xff'},
            'read': {0xCC74: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xc2',
                        0xFF9D: b'\x00',
                        0xC2BB: b'\x07',
                        0xC200: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xCD78: b'\xff'},
            'read': {0xCC74: 0x01}},
        dict(_fixture_case(_BENCH), **_BENCH.regs),
        dict(_fixture_case(_BENCH), **_BENCH.regs),
    ],
    'AIProcessEnergyCards': [
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {0xCD38: b'\x00\x00', 0xCD5F: b'\x02',
                  0xCD2D: b'\x00', 0xC2EF: b'\x01', 0xC2C8: b'\x00',
                  0xFF97: b'\xc2', 0xCABB: b'\x00', 0xC500: b'\xff'}},
        {'wram': {0xCD5F: b'\x02', 0xC2EF: b'\x01',
                  0xC2C8: b'\x00', 0xFF97: b'\xc2',
                  0xCABB: b'\x00', 0xC500: b'\xff'}},
        {'a': 0x08, 'b': 0x73, 'c': 0x00, 'd': 0x0C,
         'e': 0x6D, 'f': 0x00, 'hl': 0xD732,
         'wram': {0xCD5F: b'\x02', 0xC2EF: b'\x01',
                  0xC2C8: b'\x00', 0xFF97: b'\xc2',
                  0xCABB: b'\x00', 0xC500: b'\xff'}},
        {'a': 0x08, 'b': 0x73, 'c': 0x00, 'd': 0x0C,
         'e': 0x6D, 'f': 0x00, 'hl': 0xD732,
         'wram': {0xCD6B: b'\x00' * 7, 0xCD5F: b'\x02',
                  0xC2EF: b'\x01', 0xC2C8: b'\x00', 0xFF97: b'\xc2',
                  0xCABB: b'\x00', 0xC500: b'\xff'},
         'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400, 'snapshot': True},
    ],
    'AIProcessAndTryToPlayEnergy': [
        {'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00',
                  0xCD44: b'\x10' * 7, 0xCD45: b'\x00' * 7},
         'read': {0xCD45: 0x07}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
         'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00',
                  0xCD44: b' ' * 7, 0xCD45: b'\x00' * 7},
         'read': {0xCD45: 0x07}},
        {'a': 0x00, 'f': 0x80, 'b': 0x05, 'c': 0x00,
         'd': 0x0C, 'e': 0x6D, 'hl': 0xD732,
         'wram': {0xFF97: b'\xc2', 0xC2EE: b'\x00',
                  0xCD44: b'\x10' * 7, 0xCD45: b'\x00' * 7},
         'read': {0xCD45: 0x07}},
    ],
    'AIProcessButDontPlayEnergy_SkipEvolution': [
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCD44: b'Z',
                        0xCD45: b'\x10 0@P`p',
                        0xCD38: b'\x00\x00',
                        0xCD2D: b'\x00',
                        0xC2EF: b'\x01',
                        0xC2C8: b'\x00',
                        0xFF97: b'\xc2',
                        0xCABB: b'\x00',
                        0xC500: b'\xff'},
            'read': {0xCD5F: 0x01, 0xCD64: 0x07, 0xCD6B: 0x06},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'wram': {   0xCD44: b'Z',
                        0xCD45: b'\x10 0@P`p',
                        0xCD38: b'\x00\x00',
                        0xCD2D: b'\x00',
                        0xC2EF: b'\x01',
                        0xC2C8: b'\x00',
                        0xFF97: b'\xc2',
                        0xCABB: b'\x00',
                        0xC500: b'\xff'},
            'read': {0xCD5F: 0x01, 0xCD64: 0x07, 0xCD6B: 0x06},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'AIProcessButDontPlayEnergy_SkipEvolutionAndArena': [
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCD44: b'\x11\x10 0@P`p',
                        0xCD38: b'\x00\x00',
                        0xCD2D: b'\x00',
                        0xC2EF: b'\x01',
                        0xC2C8: b'\x00',
                        0xFF97: b'\xc2',
                        0xCABB: b'\x00',
                        0xC500: b'\xff'},
            'read': {0xCD5F: 0x01, 0xCD64: 0x07, 0xCD6B: 0x06},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'wram': {   0xCD44: b'\x7f\x81\x00\x00\x00\x00\x00\x00',
                        0xCD38: b'\x00\x00',
                        0xCD2D: b'\x00',
                        0xC2EF: b'\x01',
                        0xC2C8: b'\x00',
                        0xFF97: b'\xc2',
                        0xCABB: b'\x00',
                        0xC500: b'\xff'},
            'read': {0xCD5F: 0x01, 0xCD64: 0x07, 0xCD6B: 0x06},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}
CASES['AIProcessAndTryToPlayEnergy'] += [
    dict(_fixture_case(_ARTICUNO_ENERGY), **_ARTICUNO_ENERGY.regs),
    dict(_fixture_case(_FIRE_ENERGY), **_FIRE_ENERGY.regs),
]

MUTATIONS = {
    'RetrievePlayAreaAIScoreFromBackup1': {   'source_symbol': 'RetrievePlayAreaAIScoreFromBackup1',
        'before': 'for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {',
        'after': 'for (uint8_t b = MAX_PLAY_AREA_POKEMON - 1u; b != 0u; b--) {',
        'case_ids': [   'RetrievePlayAreaAIScoreFromBackup1-1',
                        'RetrievePlayAreaAIScoreFromBackup1-2'],
        'source': 'src/profiles/extended/home/energy.c'},
    'FindPlayAreaCardWithHighestAIScore': {   'source_symbol': 'FindPlayAreaCardWithHighestAIScore',
        'before': '\tif (e < 0x85u) {',
        'after': '\tif (e < 0x86u) {',
        'case_ids': ['FindPlayAreaCardWithHighestAIScore-1'],
        'source': 'src/profiles/extended/home/energy.c'},
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
    'CheckIfEvolutionNeedsEnergyForAttack': {   'source_symbol': 'CheckIfEvolutionNeedsEnergyForAttack',
        'before': 'uint8_t f_out = (evo.a == 0u) ? 0x80u : 0x00u;',
        'after': 'uint8_t f_out = (evo.a == 0u) ? 0x00u : 0x80u;',
        'case_ids': [   'CheckIfEvolutionNeedsEnergyForAttack-0',
                        'CheckIfEvolutionNeedsEnergyForAttack-1'],
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
        'case_ids': ['AIProcessEnergyCards-0', 'AIProcessEnergyCards-2',
                     'AIProcessEnergyCards-3'],
        'source': 'src/profiles/extended/home/energy.c'},
    'AIProcessAndTryToPlayEnergy': {   'source_symbol': 'AIProcessAndTryToPlayEnergy',
        'before': 'AIEnergyResult AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 0u;',
        'after': 'AIEnergyResult AIProcessAndTryToPlayEnergy(void)\n{\n\twAIEnergyAttachLogicFlags = 1u;',
        'case_ids': ['AIProcessAndTryToPlayEnergy-0', 'AIProcessAndTryToPlayEnergy-1'],
        'source': 'src/profiles/extended/home/energy.c'},
    'AIProcessButDontPlayEnergy_SkipEvolution': {   'source_symbol': 'AIProcessButDontPlayEnergy_SkipEvolution',
        'before': '\tgb_write8(de, wAIScore);\n'
                  '\treturn AIProcessEnergyCards();\n'
                  '}\n'
                  '/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */',
        'after': '\twAIScore = gb_read8(hl);\n'
                 '\treturn AIProcessEnergyCards();\n'
                 '}\n'
                 '/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */',
        'case_ids': ['AIProcessButDontPlayEnergy_SkipEvolution-0'],
        'source': 'src/profiles/extended/home/energy.c'},
    'AIProcessButDontPlayEnergy_SkipEvolutionAndArena': {   'source_symbol': 'AIProcessButDontPlayEnergy_SkipEvolutionAndArena',
        'before': '\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | '
                  'AI_ENERGY_FLAG_SKIP_EVOLUTION | AI_ENERGY_FLAG_SKIP_ARENA_CARD;',
        'after': '\twAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | '
                 'AI_ENERGY_FLAG_SKIP_EVOLUTION;',
        'case_ids': [   'AIProcessButDontPlayEnergy_SkipEvolutionAndArena-0',
                        'AIProcessButDontPlayEnergy_SkipEvolutionAndArena-1'],
        'source': 'src/profiles/extended/home/energy.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
