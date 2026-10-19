"""Extended oracle-diff cases for legendary_zapdos: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from pathlib import Path
from tests.cases._fixtures import Fixture
from tests.cases._inherit import inherit
_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_HOLES = (sym("wIE"), sym("wVBlankCounter"), sym("wFlushPaletteFlags"), sym("wVBlankOAMCopyToggle"), sym("wCursorBlinkCounter"), sym("wCheckMenuCursorBlinkCounter"))

def _fixture_case(fixture):
    case = fixture.case(vram=False)
    return case

_ZAPDOS_AI = Fixture("legendary-zapdos-aidoturn-entry", directory=_FIXTURES, holes=_HOLES, lcdc=sym("wLCDC"))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('legendary_zapdos')
OWN = ('AIDoTurn_LegendaryZapdos',)
CONTRACT.update({
    'AIDoTurn_LegendaryZapdos': {'compare': ('f',), 'preserve': ()},
})
CASES.update({
    'AIDoTurn_LegendaryZapdos': [
        _ZAPDOS_AI.case({
            sym("wOpponentArenaCard"): b"\x00",
            sym("wOpponentBench"): b"\x03\xFF\xFF\xFF\xFF\xFF",
            sym("wOpponentNumberOfPokemonInPlayArea"): b"\x02",
            sym("wOpponentHand"): b"\x01\x02",
            sym("wOpponentNumberOfCardsInHand"): b"\x02",
            sym("wOpponentDeck"): b"\x6D\x00\x04\x00\x0F\x00\x75\x00",
            sym("wPlayerNumberOfCardsInHand"): b"\x04",
        }),
    ],
})
MUTATIONS.update({
    'AIDoTurn_LegendaryZapdos': {   'source_symbol': 'AIDoTurn_LegendaryZapdos',
        'before': 'attach_to_arena = (LookForCardIDInHandList_Bank5(ELECTRODE_LV35).f & 0x10u) != 0u;',
        'after': 'attach_to_arena = (LookForCardIDInHandList_Bank5(ELECTRODE_LV35).f & 0x10u) == 0u;',
        'case_ids': ['AIDoTurn_LegendaryZapdos-0'],
        'source': 'src/profiles/extended/home/legendary_zapdos.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
