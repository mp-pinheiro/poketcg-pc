"""Extended oracle-diff cases for memory, seeded from tests/cases/memory.py."""

CONTRACT = {
    'DecompressDataFromBank': {'compare': ('d', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'CopyBankedDataToDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'FillMemoryWithA': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'FillMemoryWithDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetFarByte': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'DecompressDataFromBank': [
        {'c': 0x01, 'read': {0xCAD6: 0x0A, 0xFF80: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x10,
            'd': 0xC2,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {   0xCAD6: b'\x00@\x01\x00\x00\x00\x00\xc0\x00\xef',
                        0xD4B3: b'\x01',
                        0xFF80: b'\x05'},
            'read': {0xC200: 0x12, 0xC000: 0x0100}},
        {   'c': 0x01,
            'd': 0xC2,
            'e': 0x00,
            'wram': {0xCAD6: b'\x00P\x01\x00\x00\x00\x00\xc0\x00\xef', 0xD4B3: b'\x02'},
            'read': {0xC200: 0x03, 0xC000: 0x0100}},
        {   'b': 0x01,
            'c': 0x00,
            'd': 0xC2,
            'e': 0x00,
            'wram': {   0xCAD6: b'\x00@\x01\x00\x00\x00\x00\xc0\x00\xef',
                        0xD4B3: b'\x03',
                        0xFF80: b'\x11'},
            'read': {0xC200: 0x0102, 0xC000: 0x0100}},
        {   'b': 0x01,
            'c': 0x01,
            'd': 0xC2,
            'e': 0x00,
            'wram': {0xCAD6: b'\x00@\x01\x00\x00\x00\x00\xc0\x00\xef', 0xD4B3: b'\x04'},
            'read': {0xC200: 0x0104, 0xC000: 0x0100}},
        {   'c': 0x20,
            'd': 0xC2,
            'e': 0x00,
            'wram': {   0xCAD6: b'\x00`\x05\xa5\x017\x03\xc0 @',
                        0xD4B3: b'\x05',
                        0xFF80: b'\n',
                        0xC000: b'\x03\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc\xc3\xca\xd1\xd8'
                                b'\xdf\xe6\xed\xf4\xfb\x02\t\x10\x17\x1e%,3:AHOV]dkry\x80'
                                b'\x87\x8e\x95\x9c\xa3\xaa\xb1\xb8\xbf\xc6\xcd\xd4\xdb\xe2\xe9\xf0'
                                b'\xf7\xfe\x05\x0c\x13\x1a!(/6=DKRY`gnu|\x83\x8a\x91\x98'
                                b'\x9f\xa6\xad\xb4\xbb\xc2\xc9\xd0\xd7\xde\xe5\xec\xf3\xfa\x01\x08'
                                b'\x0f\x16\x1d$+29@GNU\\cjqx\x7f\x86\x8d\x94\x9b\xa2\xa9\xb0'
                                b"\xb7\xbe\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd\x04\x0b\x12\x19 '.5<CJQX"
                                b'_fmt{\x82\x89\x90\x97\x9e\xa5\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4'
                                b'\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#*18?FMT[bipw~\x85\x8c'
                                b'\x93\x9a\xa1\xa8\xaf\xb6\xbd\xc4\xcb\xd2\xd9\xe0\xe7\xee\xf5\xfc'},
            'read': {0xC200: 0x22}},
        {   'c': 0x10,
            'd': 0xC2,
            'e': 0x00,
            'wram': {0xCAD6: b'4\x01\x01\x00\x00\x00\x00\xc0\x00\xef', 0xD4B3: b'\n'},
            'read': {0xC200: 0x12, 0xC000: 0x0100}},
        {   'c': 0x08,
            'd': 0xC2,
            'e': 0x00,
            'wram': {0xCAD6: b'\x00@\x01\x00\x00\x00\x00\xc0\x00\xef', 0xD4B3: b'\x01', 0xFF80: b'?'},
            'read': {0xC200: 0x0A, 0xC000: 0x0100}},
    ],
    'CopyBankedDataToDE': [
        {   'oracle': False,
            'why': "bc=0 copies 65536 bytes and sweeps the whole address space, burying the oracle's "
                   'synthesized call frame.',
            'wram': {0xC100: b'Z\xa5Z\xa5'},
            'expect': {0xFF80: b'\x00'},
            'expect_regs': {'b': 0x00, 'c': 0x00, 'd': 0xC1, 'e': 0x00, 'hl': 0x00}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x20,
            'd': 0xC1,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {   0xD4B1: b'\x00@\x02',
                        0xFF80: b'\x05',
                        0xC100: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {'c': 0x01, 'd': 0xC2, 'e': 0x00, 'wram': {0xD4B1: b'\x00@\x01', 0xC200: b'\x11\x11\x11'}},
        {   'b': 0x01,
            'c': 0x00,
            'd': 0xC2,
            'e': 0x00,
            'wram': {   0xD4B1: b'\x00P\x03',
                        0xFF80: b'\x11',
                        0xC200: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
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
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {   'b': 0x01,
            'c': 0x01,
            'd': 0xC2,
            'e': 0x00,
            'wram': {   0xD4B1: b'\x00@?',
                        0xC200: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
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
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11'}},
        {   'c': 0x10,
            'd': 0xC3,
            'e': 0x00,
            'wram': {   0xD4B1: b'4\x01\n',
                        0xFF80: b'?',
                        0xC300: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {   'c': 0x10,
            'd': 0xC3,
            'e': 0x00,
            'wram': {   0xD4B1: b'\x00@\x00',
                        0xC300: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
    ],
    'FillMemoryWithA': [
        {   'oracle': False,
            'why': 'all-zero registers means bc=0, i.e. 65536 bytes from $0000, which sweeps the '
                   "oracle's synthesized call frame at $CE00-$CFFF",
            'wram': {0xC100: b'\xff\xff', 0xC800: b'\xff', 0xDA23: b'\xff', 0xFF80: b'\xff'},
            'expect': {0xC100: b'\x00\x00', 0xC800: b'\x00', 0xDA23: b'\x00', 0xFF80: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x40,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC100,
            'wram': {   0xC100: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {'a': 0x5A, 'b': 0x00, 'c': 0x01, 'hl': 0xC200, 'wram': {0xC200: b'\x11\x11\x11'}},
        {   'a': 0x77,
            'b': 0x01,
            'c': 0x00,
            'hl': 0xC300,
            'wram': {   0xC300: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
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
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {   'a': 0x99,
            'b': 0x01,
            'c': 0x01,
            'hl': 0xC400,
            'wram': {   0xC400: b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'}},
        {   'a': 0x5A,
            'hl': 0xC100,
            'oracle': False,
            'why': 'bc=0 is 65536 bytes, one full wrap of the address space; it overwrites the '
                   'synthesized call frame, so only the C side can run it',
            'expect': {0xC000: b'Z', 0xC100: b'Z', 0xD001: b'Z', 0xDA23: b'Z', 0xFF80: b'Z'}},
    ],
    'FillMemoryWithDE': [
        {   'oracle': False,
            'why': 'all-zero registers means bc=0, i.e. 65536 pairs = 131072 bytes, which sweeps the '
                   "oracle's synthesized call frame at $CE00-$CFFF",
            'wram': {0xC100: b'\xff\xff', 0xD001: b'\xff', 0xDA23: b'\xff'},
            'expect': {0xC100: b'\x00\x00', 0xD001: b'\x00', 0xDA23: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x08,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC4F0,
            'wram': {   0xC4F0: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {   'd': 0x12,
            'e': 0x34,
            'b': 0x00,
            'c': 0x01,
            'hl': 0xC600,
            'wram': {0xC600: b'\x11\x11\x11\x11'}},
        {   'd': 0xAD,
            'e': 0xB5,
            'b': 0x01,
            'c': 0x00,
            'hl': 0xC700,
            'wram': {   0xC700: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
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
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                b'\x11\x11'}},
        {   'd': 0x01,
            'e': 0x02,
            'b': 0x01,
            'c': 0x01,
            'hl': 0xC000,
            'wram': {   0xC000: b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'33333333333333333333333333333333333333333333333333333333333333333333'
                                b'3333333333333333333333333333333333333333'}},
        {   'd': 0x5A,
            'e': 0xA5,
            'hl': 0xC100,
            'oracle': False,
            'why': 'bc=0 is 65536 pairs = 131072 bytes, two full wraps of the address space; it '
                   'overwrites the synthesized call frame',
            'expect': {   0xC000: b'\xa5Z',
                          0xC100: b'\xa5Z',
                          0xD001: b'\xa5Z',
                          0xDA22: b'\xa5Z',
                          0xFF80: b'\xa5Z'}},
    ],
    'GetFarByte': [
        {'read': {0xFF80: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x07'}},
        {'a': 0x00, 'hl': 0x0134, 'read': {0xFF80: 0x01}},
        {'a': 0x00, 'hl': 0x4000, 'read': {0xFF80: 0x01}},
        {'a': 0x01, 'hl': 0x4000, 'read': {0xFF80: 0x01}},
        {'a': 0x02, 'hl': 0x4000, 'wram': {0xFF80: b'\x1f'}},
        {'a': 0x3F, 'hl': 0x4002, 'read': {0xFF80: 0x01}},
        {'a': 0x3F, 'hl': 0x0134, 'read': {0xFF80: 0x01}},
        {'a': 0x0A, 'hl': 0x1FFF, 'read': {0xFF80: 0x01}},
        {'a': 0x02, 'hl': 0xC200, 'wram': {0xC200: b'Z', 0xFF80: b'\x04'}},
        {'a': 0x11, 'hl': 0xFF90, 'wram': {0xFF90: b'w'}, 'read': {0xFF80: 0x01}},
        {'a': 0x05, 'hl': 0xDFFF, 'wram': {0xDA23: b'\xa3'}, 'read': {0xFF80: 0x01}},
        {'a': 0x02, 'hl': 0xA000, 'wram': {0xFF80: b'\x04'}, 'read': {0xFF80: 0x01}},
    ],
}

MUTATIONS = {
    'DecompressDataFromBank': {   'source_symbol': 'DecompressDataFromBank',
        'before': '\tDecompressData(bc, de);',
        'after': '\tDecompressData((uint16_t)(bc ^ 1u), de);',
        'case_ids': ['DecompressDataFromBank-0'],
        'source': 'src/profiles/extended/home/memory.c'},
    'CopyBankedDataToDE': {   'source_symbol': 'CopyBankedDataToDE',
        'before': 'void CopyBankedDataToDE(uint16_t bc, uint16_t de)\n{',
        'after': 'void CopyBankedDataToDE(uint16_t bc, uint16_t de)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['CopyBankedDataToDE-1'],
        'source': 'src/profiles/extended/home/memory.c'},
    'FillMemoryWithA': {   'source_symbol': 'FillMemoryWithA',
        'before': 'gb_write8(hl++, a);',
        'after': 'gb_write8(hl, a);',
        'case_ids': [   'FillMemoryWithA-1',
                        'FillMemoryWithA-0',
                        'FillMemoryWithA-2',
                        'FillMemoryWithA-3',
                        'FillMemoryWithA-4',
                        'FillMemoryWithA-5'],
        'source': 'src/profiles/extended/home/memory.c'},
    'FillMemoryWithDE': {   'source_symbol': 'FillMemoryWithDE',
        'before': 'void FillMemoryWithDE(uint16_t hl, uint16_t bc, uint8_t d, uint8_t e)\n{',
        'after': 'void FillMemoryWithDE(uint16_t hl, uint16_t bc, uint8_t d, uint8_t e)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['FillMemoryWithDE-1'],
        'source': 'src/profiles/extended/home/memory.c'},
    'GetFarByte': {   'source_symbol': 'GetFarByte',
        'before': '\treturn v;',
        'after': '\treturn 1u + v;',
        'case_ids': ['GetFarByte-0'],
        'source': 'src/profiles/extended/home/memory.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _rec in SCHEMA2_CASES["CopyBankedDataToDE"]:
    _rec.setdefault("bus", {}).update({0xdff0: 1})
for _rec in SCHEMA2_CASES["FillMemoryWithDE"]:
    _rec.setdefault("bus", {}).update({0xdff0: 1})
