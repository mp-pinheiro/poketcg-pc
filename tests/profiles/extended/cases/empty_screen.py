"""Extended oracle-diff cases for empty_screen, seeded from tests/cases/empty_screen.py."""

CONTRACT = {
    'EmptyScreen': {'compare': (), 'preserve': ()},
    'BCCoordToBGMap0Address': {'compare': ('d', 'e'), 'preserve': ()},
}

CASES = {
    'EmptyScreen': [
        {   'wram': {0xCAB6: b'\x00', 0xCAB4: b'\x00', 0xCABB: b'\x91', 0xFF40: b'\x91'},
            'read': {0x9800: 0x0800, 0xFF82: 0x01, 0xFF40: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB6: b'\xa5',
                        0xCAB4: b'\x00',
                        0xCAC2: b'\x7f',
                        0xCABB: b'\x91',
                        0xFF40: b'\x91'},
            'read': {0x9800: 0x0800, 0xFF82: 0x01, 0xFF40: 0x01}},
        {   'wram': {0xCAB6: b'Z', 0xCAB4: b'\x02', 0xCABB: b'\x91', 0xFF40: b'\x91'},
            'read': {0x9800: 0x0800, 0xFF82: 0x01, 0xFF40: 0x01}},
    ],
    'BCCoordToBGMap0Address': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0x12, 'c': 0x34, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'b': 0xFF, 'c': 0xFF},
        {'b': 0x01, 'c': 0x20},
    ],
}

MUTATIONS = {
    'EmptyScreen': {   'source_symbol': 'EmptyScreen',
        'before': '\tDisableLCD();\n\t(void)FillTileMap();',
        'after': '\t(void)FillTileMap();',
        'case_ids': ['EmptyScreen-0', 'EmptyScreen-1', 'EmptyScreen-2'],
        'source': 'src/profiles/extended/home/empty_screen.c'},
    'BCCoordToBGMap0Address': {   'source_symbol': 'BCCoordToBGMap0Address',
        'before': 'uint16_t offset = (uint16_t)((uint16_t)c * TILEMAP_W + b);',
        'after': 'uint16_t offset = (uint16_t)((uint16_t)b * TILEMAP_W + c);',
        'case_ids': [   'BCCoordToBGMap0Address-1',
                        'BCCoordToBGMap0Address-2',
                        'BCCoordToBGMap0Address-3'],
        'source': 'src/profiles/extended/home/empty_screen.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
