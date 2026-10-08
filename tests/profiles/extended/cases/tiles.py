"""Extended oracle-diff cases for tiles: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('tiles', remove=(
    'Copy1bppTiles',
    'Func_1f96',
    'Func_2046',
    'Func_2051',
    'Func_2055',
    'Func_2057',
    'Func_212f',
    'LoadFullWidthFontTiles',
))
OWN = (
    'LoadDeckAndDiscardPileIcons',
)
CONTRACT.update({
    'LoadDeckAndDiscardPileIcons': {'compare': ('d', 'e', 'hl'), 'preserve': ()},
})
CASES.update({
    'LoadDeckAndDiscardPileIcons': [
        {'wram': {sym("wConsole"): b'\x01'}, 'vread': {0x00: {0x8D00: 0x0300}}},
        {'wram': {sym("wConsole"): b'\x02'}, 'vread': {0x00: {0x8D00: 0x0300}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wConsole"): b'\x02'},
            'vread': {0x00: {0x8D00: 0x0300}}},
    ],
})
MUTATIONS.update({
    'LoadDuelCardSymbolTiles': {   'source_symbol': 'LoadDuelCardSymbolTiles',
        'before': '\tuint16_t hl = DUEL_CGB_SYMBOL_GFX_FAR;',
        'after': '\tuint16_t hl = (uint16_t)(DUEL_CGB_SYMBOL_GFX_FAR + 1u);',
        'case_ids': ['LoadDuelCardSymbolTiles-0'],
        'source': 'src/profiles/extended/home/tiles.c'},
    'LoadDuelCardSymbolTiles2': {   'source_symbol': 'LoadDuelCardSymbolTiles2',
        'before': '\tuint16_t hl = (uint16_t)(DUEL_CGB_SYMBOL_GFX_FAR + 0x40u);',
        'after': '\tuint16_t hl = (uint16_t)(DUEL_CGB_SYMBOL_GFX_FAR + 0x41u);',
        'case_ids': ['LoadDuelCardSymbolTiles2-0'],
        'source': 'src/profiles/extended/home/tiles.c'},
    'LoadDeckAndDiscardPileIcons': {   'source_symbol': 'LoadDeckAndDiscardPileIcons',
        'before': 'TileCopyResult LoadDeckAndDiscardPileIcons(void)\n'
                  '{\n'
                  '\treturn load_deck_and_discard_pile_icons();',
        'after': 'TileCopyResult LoadDeckAndDiscardPileIcons(void)\n'
                 '{\n'
                 '\treturn (TileCopyResult){0u, 0u};',
        'case_ids': ['LoadDeckAndDiscardPileIcons-0'],
        'source': 'src/home/tiles.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
