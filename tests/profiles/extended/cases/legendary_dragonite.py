"""Extended oracle-diff cases for legendary_dragonite, seeded from tests/cases/legendary_dragonite.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_DRAGONITE_AI = Fixture("legendary-dragonite-aidoturn-entry", directory=_FIXTURES)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryDragonite': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryDragonite': [
        dict(_DRAGONITE_AI.case(vram=False), **_DRAGONITE_AI.regs),
        dict(_DRAGONITE_AI.case(vram=False), **POISON),
        _DRAGONITE_AI.case(vram=False),
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryDragonite': {   'source_symbol': 'AIDoTurn_LegendaryDragonite',
        'before': '\treturn (AIDoTurn_LegendaryDragoniteResult){decision.f};',
        'after': '\treturn (AIDoTurn_LegendaryDragoniteResult){0xffu};',
        'case_ids': ['AIDoTurn_LegendaryDragonite-0', 'AIDoTurn_LegendaryDragonite-1'],
        'source': 'src/profiles/extended/home/legendary_dragonite.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
