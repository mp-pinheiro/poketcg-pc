"""Extended oracle-diff cases for legendary_dragonite: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter"))

def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case

_DRAGONITE_AI = Fixture("legendary-dragonite-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=sym("wLCDC"))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('legendary_dragonite')
OWN = ('AIDoTurn_LegendaryDragonite',)
CONTRACT.update({
    'AIDoTurn_LegendaryDragonite': {'compare': ('f',), 'preserve': ()},
})
CASES.update({
    'AIDoTurn_LegendaryDragonite': [
        dict(_fixture_case(_DRAGONITE_AI), **_DRAGONITE_AI.regs),
        dict(_fixture_case(_DRAGONITE_AI), **POISON),
        _fixture_case(_DRAGONITE_AI),
    ],
})
MUTATIONS.update({
    'AIDoTurn_LegendaryDragonite': {   'source_symbol': 'AIDoTurn_LegendaryDragonite',
        'before': 'if (skip_energy == 0u)',
        'after': 'if (skip_energy == 1u)',
        'case_ids': ['AIDoTurn_LegendaryDragonite-0', 'AIDoTurn_LegendaryDragonite-1'],
        'source': 'src/profiles/extended/home/legendary_dragonite.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
