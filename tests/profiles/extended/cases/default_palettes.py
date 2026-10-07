"""Extended oracle-diff cases for default_palettes, seeded from tests/cases/default_palettes.py."""

CONTRACT = {
    'SetDefaultPalettes': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Func_12871': {'compare': ('b', 'd', 'e'), 'preserve': ('b', 'd', 'e')},
}

CASES = {
    'SetDefaultPalettes': [
        {   'wram': {   0xCAB4: b'\x00',
                        0xFF80: b'\x04',
                        0xCABC: b'\x00',
                        0xCABD: b'\x00',
                        0xCABE: b'\x00',
                        0xCCA1: b'\x00',
                        0xFF47: b'\xfc',
                        0xFF48: b'\xff',
                        0xFF49: b'\xff'},
            'read': {   0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCCA1: 0x01,
                        0xFF80: 0x01,
                        0xCABF: 0x01,
                        0xFF47: 0x01,
                        0xFF48: 0x01,
                        0xFF49: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB4: b'\x00',
                        0xFF80: b'\x04',
                        0xCABC: b'\x11',
                        0xCABD: b'"',
                        0xCABE: b'3',
                        0xCCA1: b'U',
                        0xFF47: b'\xfc',
                        0xFF48: b'\xff',
                        0xFF49: b'\xff'},
            'read': {   0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCCA1: 0x01,
                        0xFF80: 0x01,
                        0xCABF: 0x01,
                        0xFF47: 0x01,
                        0xFF48: 0x01,
                        0xFF49: 0x01}},
        {   'a': 0x01,
            'wram': {   0xCAB4: b'\x02',
                        0xFF80: b'\x04',
                        0xCAF0: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCB30: b'\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {   0xCAF0: 0x28,
                        0xCB30: 0x08,
                        0xCCA1: 0x01,
                        0xFF80: 0x01,
                        0xCABF: 0x01,
                        0xFF47: 0x01,
                        0xFF48: 0x01,
                        0xFF49: 0x01}},
    ],
    'Func_12871': [
        {   'wram': {   0xCAB4: b'\x00',
                        0xFF80: b'\x04',
                        0xCA00: b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00',
                        0xCAC0: b'\x00',
                        0xCABB: b'\x00',
                        0xFF92: b'\xaa\xbb\xcc\xdd'},
            'read': {   0xCA00: 0xA0,
                        0xCAC0: 0x01,
                        0xCABB: 0x01,
                        0xFF92: 0x04,
                        0xFF42: 0x02,
                        0xFF4A: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB4: b'\x00',
                        0xFF80: b'\x04',
                        0xCA00: b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00'
                                b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00',
                        0xCAC0: b'\x00',
                        0xCABB: b'\x00',
                        0xFF92: b'\x11"3D'},
            'read': {   0xCA00: 0xA0,
                        0xCAC0: 0x01,
                        0xCABB: 0x01,
                        0xFF92: 0x04,
                        0xFF42: 0x02,
                        0xFF4A: 0x02}},
    ],
}

MUTATIONS = {
    'SetDefaultPalettes': {   'source_symbol': 'SetDefaultPalettes',
        'before': 'gb_write8(wOBP1_ADDR, 0xE4u);',
        'after': 'gb_write8(wOBP1_ADDR, 0xE5u);',
        'case_ids': ['SetDefaultPalettes-0', 'SetDefaultPalettes-1', 'SetDefaultPalettes-2'],
        'source': 'src/profiles/extended/home/default_palettes.c'},
    'Func_12871': {   'source_symbol': 'Func_12871',
        'before': '\tZeroObjectPositions();',
        'after': '\t;',
        'case_ids': ['Func_12871-0'],
        'source': 'src/home/default_palettes.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
