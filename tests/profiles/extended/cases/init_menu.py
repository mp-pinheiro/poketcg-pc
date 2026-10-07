"""Extended oracle-diff cases for init_menu, seeded from tests/cases/init_menu.py."""

CONTRACT = {
    'InitMenuScreen': {'compare': (), 'preserve': ()},
    'FlashWhiteScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    'InitMenuScreen': [
        {   'wram': {   0xCAB6: b'\xff',
                        0xCABB: b'\x00',
                        0xFF92: b'\x12',
                        0xFF93: b'4',
                        0xFF43: b'U',
                        0xFF42: b'f'},
            'read': {   0xCAB6: 0x01,
                        0xCABB: 0x01,
                        0xFF92: 0x01,
                        0xFF93: 0x01,
                        0xFF43: 0x01,
                        0xFF42: 0x01,
                        0xCAC0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCAB6: b'\x7f', 0xCABB: b'\x00', 0xFF92: b'\xaa', 0xFF93: b'\xbb'},
            'read': {   0xCAB6: 0x01,
                        0xCABB: 0x01,
                        0xFF92: 0x01,
                        0xFF93: 0x01,
                        0xFF43: 0x01,
                        0xFF42: 0x01,
                        0xCAC0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCAB6: b'\xff', 0xCABB: b'\x80', 0xFF92: b'\xaa', 0xFF93: b'\xbb'},
            'read': {   0xCAB6: 0x01,
                        0xCABB: 0x01,
                        0xFF92: 0x01,
                        0xFF93: 0x01,
                        0xFF40: 0x01,
                        0xCAC0: 0x01}},
    ],
    'FlashWhiteScreen': [
        {   'wram': {   0xFF40: b'\x00',
                        0xCABB: b'\x00',
                        0xFF81: b'\x00',
                        0xCABC: b'\x11',
                        0xCABD: b'"',
                        0xCABE: b'3',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f',
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'},
            'sram': {   0x01: {   0xA800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xFF81: 0x01,
                        0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCAF0: 0x80,
                        0xCB30: 0x80},
            'sread': {0x01: {0xA800: 0x83}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF40: b'\x00',
                        0xCABB: b'\x00',
                        0xFF81: b'\x03',
                        0xCABC: b'\x11',
                        0xCABD: b'"',
                        0xCABE: b'3',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f',
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'},
            'sram': {   0x01: {   0xA800: b'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU'
                                          b'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU'
                                          b'UUUUUUUUUUUUUUUUUUU'},
                        0x03: {   0xA800: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'}},
            'read': {   0xFF81: 0x01,
                        0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCAF0: 0x80,
                        0xCB30: 0x80},
            'sread': {0x01: {0xA800: 0x83}, 0x03: {0xA800: 0x83}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF40: b'\x80',
                        0xCABB: b'\x80',
                        0xFF81: b'\x02',
                        0xCABC: b'\x11',
                        0xCABD: b'"',
                        0xCABE: b'3',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f',
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'},
            'sram': {   0x01: {   0xA800: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'},
                        0x02: {   0xA800: b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'"""""""""""""""""""'}},
            'read': {   0xFF81: 0x01,
                        0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCAF0: 0x80,
                        0xCB30: 0x80},
            'sread': {0x01: {0xA800: 0x83}, 0x02: {0xA800: 0x83}}},
    ],
}

MUTATIONS = {
    'InitMenuScreen': {   'source_symbol': 'InitMenuScreen',
        'before': 'if (!(wLCDC & LCDC_ON)) {',
        'after': 'if ((wLCDC & LCDC_ON)) {',
        'case_ids': ['InitMenuScreen-0', 'InitMenuScreen-1', 'InitMenuScreen-2'],
        'source': 'src/home/init_menu.c'},
    'FlashWhiteScreen': {   'source_symbol': 'FlashWhiteScreen',
        'before': '\tCopyPalsToSRAMBuffer();',
        'after': '\t;',
        'case_ids': ['FlashWhiteScreen-0'],
        'source': 'src/home/init_menu.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
