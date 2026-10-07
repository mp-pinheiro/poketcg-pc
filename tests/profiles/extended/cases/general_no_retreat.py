"""Extended oracle-diff cases for general_no_retreat, seeded from tests/cases/general_no_retreat.py."""
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
    'AIDoTurn_GeneralNoRetreat': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_GeneralNoRetreat': [
        dict(_fixture_case(_AI_MAIN), **_AI_MAIN.regs),
        dict(_fixture_case(_AI_MAIN), **POISON),
    ],
}

MUTATIONS = {
    'AIDoTurn_GeneralNoRetreat': {   'source_symbol': 'AIDoTurn_GeneralNoRetreat',
        'before': 'AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, '
                  'uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n'
                  '{\n'
                  '\tInitAITurnVars();',
        'after': 'AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, '
                 'uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n'
                 '{\n'
                 '\tuint8_t unused = 0u;',
        'case_ids': ['AIDoTurn_GeneralNoRetreat-0', 'AIDoTurn_GeneralNoRetreat-1'],
        'source': 'src/profiles/extended/home/general_no_retreat.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
