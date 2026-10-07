"""Extended oracle-diff cases for legendary_zapdos, seeded from tests/cases/legendary_zapdos.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D)


def _fixture_case(fixture):
    case = fixture.case(vram=False)
    case["read"][0xCC00] = 0xBD
    case["read"][0xCCBE] = 0x42
    return case


_ZAPDOS_AI = Fixture("legendary-zapdos-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryZapdos': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryZapdos': [
        dict(_fixture_case(_ZAPDOS_AI), **_ZAPDOS_AI.regs),
        dict(_fixture_case(_ZAPDOS_AI), **POISON),
        _fixture_case(_ZAPDOS_AI),
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryZapdos': {   'source_symbol': 'AIDoTurn_LegendaryZapdos',
        'before': 'if (skip_energy == 0u)',
        'after': 'if (skip_energy == 1u)',
        'case_ids': ['AIDoTurn_LegendaryZapdos-0', 'AIDoTurn_LegendaryZapdos-1'],
        'source': 'src/profiles/extended/home/legendary_zapdos.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
