"""Extended oracle-diff cases for legendary_articuno, seeded from tests/cases/legendary_articuno.py."""

from pathlib import Path
from tests.cases._fixtures import Fixture

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCCBD, 0xCE4D)


def _fixture_case(fixture):
    case = fixture.case(vram=False)
    case["read"][0xCC00] = 0xBD
    case["read"][0xCCBE] = 0x42
    return case


_ARTICUNO_AI = Fixture("legendary-articuno-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
_ARTICUNO_SCORE = Fixture("legendary-articuno-score-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
_ARTICUNO_SCORING = Fixture("legendary-articuno-score-2-entry", directory=_FIXTURES, holes=_HOLES, lcdc=0xCABB)
_ARTICUNO_SCORING_THREE = _ARTICUNO_SCORING.case(vram=False, bank=5)
_ARTICUNO_SCORING_THREE["read"][0xCC00] = 0xBD
_ARTICUNO_SCORING_THREE["read"][0xCCBE] = 0x42
_ARTICUNO_SCORING_THREE["snapshot"] = True
_ARTICUNO_SCORING_THREE["wram"][0xC3EC] = b"\x07"
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    'ScoreLegendaryArticunoCards': {'compare': (), 'preserve': (), 'wram_out': True},
    'AIDoTurn_LegendaryArticuno': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'ScoreLegendaryArticunoCards': [
        dict(_fixture_case(_ARTICUNO_SCORE), **_ARTICUNO_SCORE.regs),
        dict(_fixture_case(_ARTICUNO_SCORE), **POISON),
        dict(_ARTICUNO_SCORING_THREE, **_ARTICUNO_SCORING.regs),
        dict(_ARTICUNO_SCORING_THREE, **_ARTICUNO_SCORING.regs),
    ],
    'AIDoTurn_LegendaryArticuno': [
        dict(_fixture_case(_ARTICUNO_AI), **_ARTICUNO_AI.regs),
        dict(_fixture_case(_ARTICUNO_AI), **POISON),
        _fixture_case(_ARTICUNO_AI),
    ],
}

MUTATIONS = {
    'ScoreLegendaryArticunoCards': {   'source_symbol': 'ScoreLegendaryArticunoCards',
        'before': '\tif (prizes < 3u)\n\t\treturn;',
        'after': '\tif (prizes < 7u)\n\t\treturn;',
        'case_ids': ['ScoreLegendaryArticunoCards-2',
                     'ScoreLegendaryArticunoCards-3'],
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
