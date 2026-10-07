"""Extended oracle-diff cases for legendary_moltres, seeded from tests/cases/legendary_moltres.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_MOLTRES_AI = Fixture("legendary-moltres-aidoturn-entry", directory=_FIXTURES)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryMoltres': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryMoltres': [
        dict(_MOLTRES_AI.case(vram=False), **_MOLTRES_AI.regs),
        dict(_MOLTRES_AI.case(vram=False), **POISON),
        _MOLTRES_AI.case(vram=False),
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
