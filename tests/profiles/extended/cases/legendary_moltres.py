"""Extended oracle-diff cases for legendary_moltres, seeded from tests/cases/legendary_moltres.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D)


def _fixture_case(fixture):
    case = fixture.case(vram=False)
    case["read"][0xCC00] = 0xBD
    case["read"][0xCCBE] = 0x42
    return case


_MOLTRES_AI = Fixture("legendary-moltres-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryMoltres': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryMoltres': [
        dict(_fixture_case(_MOLTRES_AI), **_MOLTRES_AI.regs),
        dict(_fixture_case(_MOLTRES_AI), **POISON),
        _fixture_case(_MOLTRES_AI),
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryMoltres': {   'source_symbol': 'AIDoTurn_LegendaryMoltres',
        'before': '\treturn (AIDoTurn_LegendaryMoltresResult){decision.f};',
        'after': '\treturn (AIDoTurn_LegendaryMoltresResult){(uint8_t)(decision.f ^ 0x01u)};',
        'case_ids': ['AIDoTurn_LegendaryMoltres-0', 'AIDoTurn_LegendaryMoltres-1'],
        'source': 'src/profiles/extended/home/legendary_moltres.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
