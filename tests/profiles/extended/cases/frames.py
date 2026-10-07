"""Extended oracle-diff cases for frames, seeded from tests/cases/frames.py."""

CONTRACT = {
    'DoFrame': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'HandleDPadRepeat': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
}

CASES = {
    'DoFrame': [
        {'wram': {0xFF8D: b'\x00\x00\x00\x00\x00'}, 'read': {0xFF8D: 0x05}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF8D: b'\x00\x00\x00\x00\x00'},
            'read': {0xFF8D: 0x05}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCAB8: b'\xff', 0xCABB: b'\x80', 0xFF40: b'\x80'},
            'oracle': False,
            'why': 'LCD-on DoFrame reaches the dissolved VBlank boundary',
            'expect': {0xCAB8: b'\x00'},
            'expect_regs': {'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCAB8: b'*', 0xCABB: b'\x00', 0xFF40: b'\x00', 0xFF8D: b'\x00\x00\x00\x00\x00'},
            'read': {0xCAB8: 0x01, 0xFF8D: 0x05}},
    ],
    'HandleDPadRepeat': [
        {'wram': {0xFF8D: b'\x00\x00\x00\x00\x00'}, 'read': {0xFF8D: 0x05}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF8D: b'\x00\x00\x00\x00\x00'},
            'read': {0xFF8D: 0x05}},
        {'wram': {0xFF8D: b'\xf0\x00\x00\x00\x01'}, 'read': {0xFF8D: 0x05}},
        {'wram': {0xFF8D: b'\xf0\x00\x00\x00\x00'}, 'read': {0xFF8D: 0x05}},
        {'wram': {0xFF8D: b'\x00\x00\x00@@'}, 'read': {0xFF8D: 0x05}},
        {'wram': {0xFF8D: b'\n\x00\x00@\x00'}, 'read': {0xFF8D: 0x05}},
        {'wram': {0xFF8D: b'\x01\x00\x00@\x00'}, 'read': {0xFF8D: 0x05}},
        {'wram': {0xFF8D: b'\x05\x00\x00A\x01'}, 'read': {0xFF8D: 0x05}},
    ],
}

MUTATIONS = {
    'DoFrame': {   'source_symbol': 'DoFrame',
        'before': '\tif (!frame_boundary_is_installed() && (gb_read8(wLCDC_ADDR) & 0x80u) != 0u)',
        'after': '\tif (!frame_boundary_is_installed() && (gb_read8(wLCDC_ADDR) & 0x80u) == 0u)',
        'case_ids': ['DoFrame-3'],
        'source': 'src/home/frames.c'},
    'HandleDPadRepeat': {   'source_symbol': 'HandleDPadRepeat',
        'before': '\t\tif (repeat == 0) {',
        'after': '\t\tif (repeat != 0) {',
        'case_ids': ['HandleDPadRepeat-5'],
        'source': 'src/home/frames.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
