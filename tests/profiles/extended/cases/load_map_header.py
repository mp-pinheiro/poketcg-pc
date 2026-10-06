"""Extended oracle-diff cases for load_map_header, seeded from tests/cases/load_map_header.py."""

CONTRACT = {
    'LoadMapHeader': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'LoadMapHeader': [
        {   'wram': {   0xCAB4: b'\x02',
                        0xD31C: b'\x00',
                        0xD11E: b'\xaa',
                        0xD11F: b'\xaa',
                        0xD27C: b'\xaa',
                        0xD27D: b'\xaa',
                        0xD0FE: b'\xaa'}},
        {   'wram': {   0xCAB4: b'\x00',
                        0xD31C: b'\x00',
                        0xD11E: b'\x00',
                        0xD11F: b'\x00',
                        0xD27C: b'\x00',
                        0xD27D: b'\x00',
                        0xD0FE: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB4: b'\x00',
                        0xD31C: b'\x01',
                        0xD11E: b'\xaa',
                        0xD11F: b'\xaa',
                        0xD27C: b'\xaa',
                        0xD27D: b'\xaa',
                        0xD0FE: b'\xaa'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB4: b'\x02',
                        0xD31C: b'#',
                        0xD11E: b'\xaa',
                        0xD11F: b'\xaa',
                        0xD27C: b'\xaa',
                        0xD27D: b'\xaa',
                        0xD0FE: b'\xaa'}},
    ],
}

MUTATIONS = {
    'LoadMapHeader': {   'source_symbol': 'LoadMapHeader',
        'before': 'cgb_tilemap != 0',
        'after': 'cgb_tilemap == 0',
        'case_ids': ['LoadMapHeader-0', 'LoadMapHeader-1', 'LoadMapHeader-2', 'LoadMapHeader-3'],
        'source': 'src/profiles/extended/home/load_map_header.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
