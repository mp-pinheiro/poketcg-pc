"""Extended oracle-diff cases for legendary_dragonite, seeded from tests/cases/legendary_dragonite.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D)


def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case


_DRAGONITE_AI = Fixture("legendary-dragonite-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryDragonite': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryDragonite': [
        dict(_fixture_case(_DRAGONITE_AI), **_DRAGONITE_AI.regs),
        dict(_fixture_case(_DRAGONITE_AI), **POISON),
        _fixture_case(_DRAGONITE_AI),
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryDragonite': {   'source_symbol': 'AIDoTurn_LegendaryDragonite',
        'before': 'if (skip_energy == 0u)',
        'after': 'if (skip_energy == 1u)',
        'case_ids': ['AIDoTurn_LegendaryDragonite-0', 'AIDoTurn_LegendaryDragonite-1'],
        'source': 'src/profiles/extended/home/legendary_dragonite.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
