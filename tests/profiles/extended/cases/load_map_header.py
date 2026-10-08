"""Extended oracle-diff cases for load_map_header: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('load_map_header', remove=('LoadMapHeader',))
OWN = ('LoadMapHeader',)
CONTRACT.update({
    'LoadMapHeader': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
})
CASES.update({
    'LoadMapHeader': [
        {   'wram': {   sym("wConsole"): b'\x02',
                        sym("wCurMap"): b'\x00',
                        sym("wCurTilemap"): b'\xaa',
                        sym("wCurTilemap") + 1: b'\xaa',
                        sym("wCurMapInitialPalette"): b'\xaa',
                        sym("wCurMapPalette"): b'\xaa',
                        sym("wDefaultSong"): b'\xaa'}},
        {   'wram': {   sym("wConsole"): b'\x00',
                        sym("wCurMap"): b'\x00',
                        sym("wCurTilemap"): b'\x00',
                        sym("wCurTilemap") + 1: b'\x00',
                        sym("wCurMapInitialPalette"): b'\x00',
                        sym("wCurMapPalette"): b'\x00',
                        sym("wDefaultSong"): b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wConsole"): b'\x00',
                        sym("wCurMap"): b'\x01',
                        sym("wCurTilemap"): b'\xaa',
                        sym("wCurTilemap") + 1: b'\xaa',
                        sym("wCurMapInitialPalette"): b'\xaa',
                        sym("wCurMapPalette"): b'\xaa',
                        sym("wDefaultSong"): b'\xaa'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wConsole"): b'\x02',
                        sym("wCurMap"): b'#',
                        sym("wCurTilemap"): b'\xaa',
                        sym("wCurTilemap") + 1: b'\xaa',
                        sym("wCurMapInitialPalette"): b'\xaa',
                        sym("wCurMapPalette"): b'\xaa',
                        sym("wDefaultSong"): b'\xaa'}},
    ],
})
MUTATIONS.update({
    'LoadMapHeader': {   'source_symbol': 'LoadMapHeader',
        'before': '\tgb_write8(wCurTilemap_ADDR, header[0]);',
        'after': '\tgb_write8(wCurTilemap_ADDR, header[1]);',
        'case_ids': ['LoadMapHeader-0', 'LoadMapHeader-1', 'LoadMapHeader-2', 'LoadMapHeader-3'],
        'source': 'src/profiles/extended/home/load_map_header.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
