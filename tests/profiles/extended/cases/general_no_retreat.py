"""Extended oracle-diff cases for general_no_retreat: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter"))
_AI_MAIN = Fixture("ai-duel-fire-charge-aimainturnlogic-entry",
                   directory=_FIXTURES, holes=_HOLES, lcdc=sym("wLCDC"))

def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('general_no_retreat')
OWN = ('AIDoTurn_GeneralNoRetreat',)
CONTRACT.update({
    'AIDoTurn_GeneralNoRetreat': {'compare': ('f',), 'preserve': ()},
})
CASES.update({
    'AIDoTurn_GeneralNoRetreat': [
        dict(_fixture_case(_AI_MAIN), **_AI_MAIN.regs),
        dict(_fixture_case(_AI_MAIN), **POISON),
    ],
})
MUTATIONS.update({
    'AIDoTurn_GeneralNoRetreat': {   'source_symbol': 'AIDoTurn_GeneralNoRetreat',
        'before': 'AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, '
                  'uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n'
                  '{\n'
                  '\tInitAITurnVars();',
        'after': 'AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, '
                 'uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n'
                 '{\n'
                 '\tuint8_t unused = 0u;',
        'case_ids': ['AIDoTurn_GeneralNoRetreat-0', 'AIDoTurn_GeneralNoRetreat-1'],
        'source': 'src/home/general_no_retreat.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
