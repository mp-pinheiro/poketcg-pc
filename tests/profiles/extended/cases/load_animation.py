"""Extended oracle-diff cases for load_animation, seeded from tests/cases/load_animation.py."""

CONTRACT = {
    'GetFirstSpriteAnimBufferProperty': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GetSpriteAnimBufferProperty': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GetSpriteAnimBufferProperty_SpriteInA': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'DrawSpriteAnimationFrame': {'compare': ('f', 'hl'), 'preserve': ('f',)},
    'GetAnimationFramePointer': {'compare': ('f', 'hl'), 'preserve': ('f', 'hl')},
    'ClearSpriteAnimations': {'compare': ('f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'b', 'c', 'd', 'e', 'hl')},
    'HandleAllSpriteAnimations': {'compare': ('f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'b', 'c', 'd', 'e', 'hl')},
    'EnableAndClearSpriteAnimations': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'DrawPortrait': {'compare': (), 'preserve': ()},
    'DrawOpponentPortrait': {'compare': (), 'preserve': ()},
    'DrawPlayerPortrait': {'compare': (), 'preserve': ()},
    'Func_3e31': {'compare': ('a', 'f'), 'preserve': ('f',), 'wram_out': True},
    'LoadScene': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'GetFirstSpriteAnimBufferProperty': [
        {'c': 0x00, 'wram': {0xD4BC: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0x0F,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD4BC: b'\x0f'}},
        {'wram': {0xD4BC: b'\x10'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD4BC: b'\xff'}},
    ],
    'GetSpriteAnimBufferProperty': [
        {'c': 0x00, 'wram': {0xD4BC: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0x07,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD4BC: b'\x03'}},
        {'c': 0x0F, 'wram': {0xD4BC: b'\xff'}},
    ],
    'GetSpriteAnimBufferProperty_SpriteInA': [
        {'a': 0x00, 'c': 0x00},
        {'a': 0x03, 'f': 0xF0, 'b': 0xBB, 'c': 0x07, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x0F, 'c': 0x0F},
        {'a': 0x10, 'c': 0x00},
        {'a': 0xFF, 'c': 0x0F},
    ],
    'DrawSpriteAnimationFrame': [
        {   'hl': 0xC100,
            'wram': {   0xD5C3: b'\x00',
                        0xD5BE: b'\x90',
                        0xD5BF: b'`',
                        0xD5BD: b'\x00',
                        0xD5C0: b'\x10',
                        0xCAB5: b'\x00',
                        0xC100: b'\x01\x05\x08\x02\x00'},
            'read': {0xCA00: 0x04, 0xCAB5: 0x01, 0xD5C1: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC300,
            'wram': {0xFF80: b'\n', 0xD5C3: b'\x01', 0xD5BE: b'\xf5', 0xD5BF: b'\x10', 0xC300: b'\x00'},
            'read': {0xD5C1: 0x02}},
        {   'hl': 0xC100,
            'wram': {   0xD5C3: b'\x00',
                        0xD5BE: b'P',
                        0xD5BF: b'`',
                        0xD5BD: b'`',
                        0xD5C0: b' ',
                        0xCAB5: b'\x00',
                        0xC100: b'\x01\x05\x03\n\x11'},
            'read': {0xCA00: 0x04, 0xCAB5: 0x01}},
        {   'hl': 0xC200,
            'wram': {   0xD5C3: b'\x00',
                        0xD5BE: b'\x10',
                        0xD5BF: b'\x90',
                        0xD5BD: b'\x00',
                        0xD5C0: b'\x00',
                        0xCAB5: b'\x08',
                        0xCA08: b'\x11"3D',
                        0xC200: b'\x01\x7f\x00\x00\x00'},
            'read': {0xCA08: 0x04, 0xCAB5: 0x01}},
        {   'hl': 0xC400,
            'wram': {   0xD5C3: b'\x00',
                        0xD5BE: b'\x10',
                        0xD5BF: b'\x10',
                        0xD5BD: b'\x00',
                        0xD5C0: b'\x00',
                        0xCAB5: b'\x00',
                        0xC400: b'\x03\x01\x01\x01\x00\x02\x02\x02\x00\x03\x03\x03\x00'},
            'read': {0xCA00: 0x0C, 0xCAB5: 0x01}},
        {   'hl': 0x4000,
            'wram': {   0xD5C3: b'\x03',
                        0xD5BE: b'\x10',
                        0xD5BF: b'\x10',
                        0xD5BD: b'\x00',
                        0xD5C0: b'\x00',
                        0xCAB5: b'\x00',
                        0xFF80: b'\x00'},
            'read': {0xFF80: 0x01}},
    ],
    'GetAnimationFramePointer': [
        {'hl': 0xC4F0, 'wram': {0xD4B7: b'\xff'}, 'read': {0xC4FB: 0x03}},
        {   'hl': 0xC4F0,
            'wram': {0xD4B7: b'\x03', 0xD4B1: b'\x00\xc3\x02', 0xC300: b'\x02\x00\xc3', 0xC306: b'xV'},
            'read': {0xC4FB: 0x03}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC600,
            'wram': {   0xFF80: b'\t',
                        0xD4B7: b'\x00',
                        0xD4B1: b'\x00\xc3\x00',
                        0xC300: b'\x00\x80\xc3',
                        0xC380: b'\xab\xcd'},
            'read': {0xC60B: 0x03, 0xFF80: 0x01}},
        {   'hl': 0xC4F0,
            'wram': {   0xD4B7: b'\xfe',
                        0xD4B1: b'\x00\xc7\x01',
                        0xC700: b'\x01\x80\xc7',
                        0xC87D: b'\x11"'},
            'read': {0xC4FB: 0x03}},
    ],
    'ClearSpriteAnimations': [
        {'read': {0xD4BD: 0x0100, 0xCA00: 0xA0, 0xCAB5: 0x01, 0xCAC0: 0x01, 0xD4BC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD4BD: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'},
            'read': {0xD4BD: 0x0100, 0xCA00: 0xA0, 0xCAB5: 0x01, 0xCAC0: 0x01}},
        {   'wram': {   0xD5C4: b'\x01',
                        0xD4BD: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xD4BD: 0x0100, 0xCAC0: 0x01}},
    ],
    'HandleAllSpriteAnimations': [
        {   'wram': {   0xD4BD: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xD4BD: 0x0100, 0xCA00: 0xA0, 0xCAB5: 0x01, 0xCAC0: 0x01, 0xD4BC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD4BD: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xD4BD: 0x0100, 0xCA00: 0xA0, 0xCAB5: 0x01, 0xCAC0: 0x01}},
        {   'wram': {   0xD5C4: b'\x01',
                        0xD4BD: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'},
            'read': {0xD4BD: 0x0100, 0xCAC0: 0x01}},
    ],
    'EnableAndClearSpriteAnimations': [
        {   'wram': {0xD5C4: b'\x01'},
            'read': {0xD4BD: 0x0100, 0xCA00: 0xA0, 0xCAB5: 0x01, 0xCAC0: 0x01, 0xD4BC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD5C4: b'\x01',
                        0xD4BD: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'},
            'read': {0xD4BD: 0x0100, 0xCA00: 0xA0, 0xCAB5: 0x01, 0xCAC0: 0x01}},
        {   'wram': {   0xD5C4: b'\x00',
                        0xD4BD: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'},
            'read': {0xD4BD: 0x0100, 0xCAC0: 0x01}},
    ],
    'DrawPortrait': [
        {'a': 0x00, 'wram': {0xFF80: b'\x01', 0xD11E: b'\xff'}, 'read': {0xFF80: 0x01, 0xD11E: 0x01}},
        {   'a': 0x62,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x07', 0xD11E: b'\x00'},
            'read': {0xFF80: 0x01, 0xD11E: 0x01}},
    ],
    'DrawOpponentPortrait': [
        {   'a': 0x00,
            'wram': {0xFF80: b'\x01', 0xD60B: b'\xff', 0xD11E: b'\x00'},
            'read': {0xFF80: 0x01, 0xD60B: 0x01, 0xD11E: 0x01}},
        {   'a': 0x62,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x07', 0xD60B: b'\x00', 0xD11E: b'\xff'},
            'read': {0xFF80: 0x01, 0xD60B: 0x01, 0xD11E: 0x01}},
    ],
    'DrawPlayerPortrait': [
        {   'wram': {0xFF80: b'\x01', 0xD60B: b'\xff', 0xD11E: b'\x00'},
            'read': {0xFF80: 0x01, 0xD60B: 0x01, 0xD11E: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x07', 0xD60B: b'\x00', 0xD11E: b'\xff'},
            'read': {0xFF80: 0x01, 0xD60B: 0x01, 0xD11E: 0x01}},
    ],
    'Func_3e31': [
        {'wram': {0xFF80: b'\x03', 0xD30F: b'\x00'}, 'read': {0xFF80: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x05', 0xD30F: b'\x00'},
            'read': {0xFF80: 0x01}},
    ],
    'LoadScene': [
        {   'a': 0x00,
            'b': 0x00,
            'c': 0x00,
            'read': {   0xD609: 0x01,
                        0xD60A: 0x01,
                        0xD60F: 0x02,
                        0xD611: 0x02,
                        0xD27E: 0x01,
                        0xD11E: 0x01,
                        0xFF80: 0x01},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0x1312D00},
        {   'a': 0x00,
            'b': 0x02,
            'c': 0x03,
            'read': {   0xD609: 0x01,
                        0xD60A: 0x01,
                        0xD60F: 0x02,
                        0xD611: 0x02,
                        0xD27E: 0x01,
                        0xD11E: 0x01,
                        0xFF80: 0x01},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0x1312D00},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x00,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {   0xD609: 0x01,
                        0xD60A: 0x01,
                        0xD60F: 0x02,
                        0xD611: 0x02,
                        0xD27E: 0x01,
                        0xD11E: 0x01,
                        0xFF80: 0x01},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0x1312D00},
    ],
}

MUTATIONS = {
    'GetFirstSpriteAnimBufferProperty': {   'source_symbol': 'GetFirstSpriteAnimBufferProperty',
        'before': '\treturn GetSpriteAnimBufferProperty(SPRITE_ANIM_ENABLED);',
        'after': '\treturn GetSpriteAnimBufferProperty((SPRITE_ANIM_ENABLED + 1u));',
        'case_ids': ['GetFirstSpriteAnimBufferProperty-0'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'GetSpriteAnimBufferProperty': {   'source_symbol': 'GetSpriteAnimBufferProperty',
        'before': '\treturn GetSpriteAnimBufferProperty_SpriteInA(gb_read8(wWhichSprite_ADDR), c);',
        'after': '\treturn GetSpriteAnimBufferProperty_SpriteInA(gb_read8(wWhichSprite_ADDR), '
                 '(uint8_t)(c ^ 1u));',
        'case_ids': ['GetSpriteAnimBufferProperty-0'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'GetSpriteAnimBufferProperty_SpriteInA': {   'source_symbol': 'GetSpriteAnimBufferProperty_SpriteInA',
        'before': '\tif (a >= SPRITE_ANIM_BUFFER_CAPACITY)',
        'after': '\tif (a > SPRITE_ANIM_BUFFER_CAPACITY)',
        'case_ids': ['GetSpriteAnimBufferProperty_SpriteInA-3'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'DrawSpriteAnimationFrame': {   'source_symbol': 'DrawSpriteAnimationFrame',
        'before': 'wCurrSpriteRightEdgeCheck = (wCurrSpriteXPos >= 0xF0u) ? 0xFFu : 0x00u;',
        'after': 'wCurrSpriteRightEdgeCheck = (wCurrSpriteXPos >= 0x80u) ? 0xFFu : 0x00u;',
        'case_ids': [   'DrawSpriteAnimationFrame-0',
                        'DrawSpriteAnimationFrame-1',
                        'DrawSpriteAnimationFrame-2',
                        'DrawSpriteAnimationFrame-3',
                        'DrawSpriteAnimationFrame-4',
                        'DrawSpriteAnimationFrame-5'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'GetAnimationFramePointer': {   'source_symbol': 'GetAnimationFramePointer',
        'before': '\tif (wWhichAnimationFrame == 0xFFu) {',
        'after': '\tif (wWhichAnimationFrame != 0xFFu) {',
        'case_ids': ['GetAnimationFramePointer-0'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'ClearSpriteAnimations': {   'source_symbol': 'ClearSpriteAnimations',
        'before': '_ClearSpriteAnimations();',
        'after': '(void)0;',
        'case_ids': ['ClearSpriteAnimations-0', 'ClearSpriteAnimations-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'HandleAllSpriteAnimations': {   'source_symbol': 'HandleAllSpriteAnimations',
        'before': '_HandleAllSpriteAnimations();',
        'after': '(void)0;',
        'case_ids': ['HandleAllSpriteAnimations-0', 'HandleAllSpriteAnimations-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'EnableAndClearSpriteAnimations': {   'source_symbol': 'EnableAndClearSpriteAnimations',
        'before': 'wAllSpriteAnimationsDisabled = 0u;',
        'after': 'wAllSpriteAnimationsDisabled = 1u;',
        'case_ids': ['EnableAndClearSpriteAnimations-0', 'EnableAndClearSpriteAnimations-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'DrawPortrait': {   'source_symbol': 'DrawPortrait',
        'before': 'wCurTilemap = a;',
        'after': 'wCurTilemap = (uint8_t)(a ^ 1u);',
        'case_ids': ['DrawPortrait-0', 'DrawPortrait-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'DrawOpponentPortrait': {   'source_symbol': 'DrawOpponentPortrait',
        'before': 'wCurPortrait = a;',
        'after': 'wCurPortrait = (uint8_t)(a ^ 1u);',
        'case_ids': ['DrawOpponentPortrait-0', 'DrawOpponentPortrait-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'DrawPlayerPortrait': {   'source_symbol': 'DrawPlayerPortrait',
        'before': 'wCurPortrait = runtime_player_gender() ? MINT_PIC : PLAYER_PIC;',
        'after': 'wCurPortrait = runtime_player_gender() ? MINT_PIC : (uint8_t)(PLAYER_PIC + 1u);',
        'case_ids': ['DrawPlayerPortrait-0', 'DrawPlayerPortrait-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'Func_3e31': {   'source_symbol': 'Func_3e31',
        'before': 'uint8_t saved_bank = hBankROM;',
        'after': 'uint8_t saved_bank = (uint8_t)(hBankROM + 1u);',
        'case_ids': ['Func_3e31-0', 'Func_3e31-1'],
        'source': 'src/profiles/extended/home/load_animation.c'},
    'LoadScene': {   'source_symbol': 'LoadScene',
        'before': '\t_LoadScene(a, b, c);',
        'after': '\t(void)0;',
        'case_ids': ['LoadScene-0', 'LoadScene-1', 'LoadScene-2'],
        'source': 'src/profiles/extended/home/load_animation.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
