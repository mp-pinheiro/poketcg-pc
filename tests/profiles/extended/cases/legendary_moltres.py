"""Extended oracle-diff cases for legendary_moltres: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter"))

def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case

_MOLTRES_AI = Fixture("legendary-moltres-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=sym("wLCDC"))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('legendary_moltres')
OWN = ('AIDoTurn_LegendaryMoltres',)
CONTRACT.update({
    'AIDoTurn_LegendaryMoltres': {'compare': ('f',), 'preserve': ()},
})
CASES.update({
    'AIDoTurn_LegendaryMoltres': [
        dict(_fixture_case(_MOLTRES_AI), **_MOLTRES_AI.regs),
        dict(_fixture_case(_MOLTRES_AI), **POISON),
        _fixture_case(_MOLTRES_AI),
    ],
})
MUTATIONS.update({
    'AIDoTurn_LegendaryMoltres': {   'source_symbol': 'AIDoTurn_LegendaryMoltres',
        'before': '\treturn (AIDoTurn_LegendaryMoltresResult){decision.f};',
        'after': '\treturn (AIDoTurn_LegendaryMoltresResult){(uint8_t)(decision.f ^ 0x01u)};',
        'case_ids': ['AIDoTurn_LegendaryMoltres-0', 'AIDoTurn_LegendaryMoltres-1'],
        'source': 'src/profiles/extended/home/legendary_moltres.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
