"""Extended oracle-diff cases for legendary_zapdos, seeded from tests/cases/legendary_zapdos.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_ZAPDOS_AI = Fixture("legendary-zapdos-aidoturn-entry", directory=_FIXTURES)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryZapdos': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryZapdos': [
        dict(_ZAPDOS_AI.case(vram=False), **_ZAPDOS_AI.regs),
        dict(_ZAPDOS_AI.case(vram=False), **POISON),
        _ZAPDOS_AI.case(vram=False),
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryZapdos': {   'source_symbol': 'AIDoTurn_LegendaryZapdos',
        'before': '\treturn (AIDoTurn_LegendaryZapdosResult){decision.f};',
        'after': '\treturn (AIDoTurn_LegendaryZapdosResult){0xffu};',
        'case_ids': ['AIDoTurn_LegendaryZapdos-0', 'AIDoTurn_LegendaryZapdos-1'],
        'source': 'src/profiles/extended/home/legendary_zapdos.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
