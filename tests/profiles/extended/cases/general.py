"""Extended oracle-diff cases for general, seeded from tests/cases/general.py."""
from pathlib import Path

from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D)
_AI_MAIN = Fixture("ai-duel-fire-charge-aimainturnlogic-entry",
                   directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)


def _fixture_case(fixture):
    case = fixture.case(vram=False)
    case["read"][0xCC00] = 0xBD
    case["read"][0xCCBE] = 0x42
    return case


POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIProcessRetreat': {'compare': ('a', 'f'), 'preserve': ()},
    'AIMainTurnLogic': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIProcessRetreat': [
        {'wram': {0xCD8A: b'\x01'}, 'expect_regs': {'a': 0x01, 'f': 0x00}},
        {'wram': {0xCD8A: b'\x00', 0xCBB6: b'\x01'}, 'expect_regs': {'a': 0x01, 'f': 0x00}},
        {'wram': {0xCD8A: b'\x00', 0xCBB6: b'\x80'}, 'expect_regs': {'a': 0x80, 'f': 0x00}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCD8A: b'\x00', 0xCBB6: b'\x01'},
            'expect_regs': {'a': 0x01, 'f': 0x00}},
    ],
    'AIMainTurnLogic': [
        dict(_fixture_case(_AI_MAIN), **_AI_MAIN.regs),
        dict(_fixture_case(_AI_MAIN), **POISON),
    ],
}

MUTATIONS = {
    'AIProcessRetreat': {   'source_symbol': 'AIProcessRetreat',
        'before': 'AIProcessRetreatResult AIProcessRetreat(void)\n'
                  '{\n'
                  '\tuint8_t already_retreated = wAIRetreatedThisTurn;',
        'after': 'AIProcessRetreatResult AIProcessRetreat(void)\n'
                 '{\n'
                 '\tuint8_t already_retreated = 0u;',
        'case_ids': ['AIProcessRetreat-0'],
        'source': 'src/profiles/extended/home/general.c'},
    'AIMainTurnLogic': {   'source_symbol': 'AIMainTurnLogic',
        'before': 'AIMainTurnLogicResult AIMainTurnLogic(uint8_t a, uint8_t f, uint8_t b, uint8_t '
                  'c, uint8_t d, uint8_t e, uint16_t hl)\n'
                  '{\n'
                  '\tInitAITurnVars();',
        'after': 'AIMainTurnLogicResult AIMainTurnLogic(uint8_t a, uint8_t f, uint8_t b, uint8_t '
                 'c, uint8_t d, uint8_t e, uint16_t hl)\n'
                 '{\n'
                 '\tuint8_t unused = 0u;',
        'case_ids': ['AIMainTurnLogic-0', 'AIMainTurnLogic-1'],
        'source': 'src/profiles/extended/home/general.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
