"""Extended oracle-diff cases for legendary_articuno, seeded from tests/cases/legendary_articuno.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_ARTICUNO_AI = Fixture("legendary-articuno-aidoturn-entry", directory=_FIXTURES)
_ARTICUNO_SCORE = Fixture("legendary-articuno-score-entry", directory=_FIXTURES)
_ARTICUNO_SCORING = Fixture("legendary-articuno-score-2-entry", directory=_FIXTURES)
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'ScoreLegendaryArticunoCards': {'compare': (), 'preserve': (), 'wram_out': True},
    'AIDoTurn_LegendaryArticuno': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'ScoreLegendaryArticunoCards': [
        dict(_ARTICUNO_SCORE.case(vram=False), **_ARTICUNO_SCORE.regs),
        dict(_ARTICUNO_SCORE.case(vram=False), **POISON),
        dict(_ARTICUNO_SCORING.case(vram=False, bank=5), **_ARTICUNO_SCORING.regs),
    ],
    'AIDoTurn_LegendaryArticuno': [
        dict(_ARTICUNO_AI.case(vram=False), **_ARTICUNO_AI.regs),
        dict(_ARTICUNO_AI.case(vram=False), **POISON),
        _ARTICUNO_AI.case(vram=False),
    ],
}

MUTATIONS = {
    'ScoreLegendaryArticunoCards': {   'source_symbol': 'ScoreLegendaryArticunoCards',
        'before': '\t\t\tif (energy.a < 3u) {\n'
                  '\t\t\t\t(void)RaiseAIScoreToAllMatchingIDsInBench(LAPRAS);\n'
                  '\t\t\t\treturn;\n'
                  '\t\t\t}',
        'after': '\t\t\tif (energy.a < 3u)\n'
                 '\t\t\t\t(void)RaiseAIScoreToAllMatchingIDsInBench(LAPRAS);\n'
                 '\t\t\treturn;',
        'case_ids': ['ScoreLegendaryArticunoCards-2'],
        'source': 'src/profiles/extended/home/legendary_articuno.c'},
    'AIDoTurn_LegendaryArticuno': {   'source_symbol': 'AIDoTurn_LegendaryArticuno',
        'before': '\t\t(void)AIProcessRetreat();\n'
                  '\t\ttrainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);',
        'after': '\t\tAIProcessRetreatResult retreat = AIProcessRetreat();\n'
                 '\t\tif ((retreat.f & 0x10u) != 0u)\n'
                 '\t\t\treturn (AIDoTurn_LegendaryArticunoResult){retreat.f};\n'
                 '\t\ttrainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);',
        'case_ids': ['AIDoTurn_LegendaryArticuno-0'],
        'source': 'src/profiles/extended/home/legendary_articuno.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
