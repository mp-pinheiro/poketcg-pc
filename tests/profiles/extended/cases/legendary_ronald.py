"""Extended oracle-diff cases for legendary_ronald: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter"))

def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case

_RONALD_AI = Fixture("legendary-ronald-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=sym("wLCDC"))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('legendary_ronald')
OWN = ('AIDoTurn_LegendaryRonald',)
CONTRACT.update({
    'AIDoTurn_LegendaryRonald': {'compare': ('f',), 'preserve': ()},
})
CASES.update({
    'AIDoTurn_LegendaryRonald': [
        dict(_fixture_case(_RONALD_AI), **_RONALD_AI.regs),
        dict(_fixture_case(_RONALD_AI), **POISON),
        _fixture_case(_RONALD_AI),
    ],
})
MUTATIONS.update({
    'AIDoTurn_LegendaryRonald': {   'source_symbol': 'AIDoTurn_LegendaryRonald',
        'before': '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);\n'
                  '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);\n'
                  '\tAIProcessRetreat();',
        'after': '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);\n'
                 '\tAIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);',
        'case_ids': ['AIDoTurn_LegendaryRonald-0'],
        'source': 'src/home/legendary_ronald.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
