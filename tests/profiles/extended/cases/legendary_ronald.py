"""Extended oracle-diff cases for legendary_ronald, seeded from tests/cases/legendary_ronald.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_RONALD_AI = Fixture("legendary-ronald-aidoturn-entry", directory=_FIXTURES)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'AIDoTurn_LegendaryRonald': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_LegendaryRonald': [
        dict(_RONALD_AI.case(vram=False), **_RONALD_AI.regs),
        dict(_RONALD_AI.case(vram=False), **POISON),
        _RONALD_AI.case(vram=False),
    ],
}

MUTATIONS = {
    'AIDoTurn_LegendaryRonald': {   'source_symbol': 'AIDoTurn_LegendaryRonald',
        'before': '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);\n'
                  '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);\n'
                  '\tAIProcessRetreat();',
        'after': '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);\n'
                 '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);',
        'case_ids': ['AIDoTurn_LegendaryRonald-0'],
        'source': 'src/profiles/extended/home/legendary_ronald.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
