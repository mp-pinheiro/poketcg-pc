"""Extended oracle-diff cases for bg_map, seeded from tests/cases/bg_map.py."""

CONTRACT = {
    'WriteDataBlocksToBGMap0': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'WriteDataBlockToBGMap0': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'WriteByteToBGMap0': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CopyDataToBGMap0': {'compare': ('d', 'e', 'hl'), 'preserve': ()},
    'SafeCopyDataHLtoDE': {'compare': ('c', 'd', 'e', 'hl'), 'preserve': ('c',)},
    'JPHblankCopyDataHLtoDE': {'compare': ('c', 'd', 'e', 'hl'), 'preserve': ('c',)},
}

CASES = {
    'WriteDataBlocksToBGMap0': [
        {'hl': 0xC100, 'wram': {0xC100: b'\x00\x00\x00\xff'}, 'read': {0x9800: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC100,
            'wram': {0xC100: b'\x01\x01\x07\x00\x04\x02\x08\t\x00\xff'},
            'read': {0x9821: 0x01, 0x9844: 0x02}},
    ],
    'WriteDataBlockToBGMap0': [
        {'hl': 0xC100, 'wram': {0xC100: b'\x00\x00\x00'}, 'read': {0x9800: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC100,
            'wram': {0xC100: b'\x02\x03\x11"\x00'},
            'read': {0x9862: 0x02}},
        {   'hl': 0xC100,
            'wram': {   0xC100: b'\x00\x00\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2'
                                b'\xef\xfc\t\x16#0=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'
                                b"'4AN[hu\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER"
                                b'_ly\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a'
                                b'\x97\xa4\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e'
                                b'\x9b\xa8\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92'
                                b'\x9f\xac\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96'
                                b'\xa3\xb0\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a'
                                b'\xa7\xb4\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e'
                                b'\xab\xb8\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2'
                                b'\xaf\xbc\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6'
                                b'\xb3\xc0\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa'
                                b'\xb7\xc4\xd1\xde\xeb\xf8\x00'},
            'read': {0x9800: 0x0100}},
        {   'hl': 0xC100,
            'wram': {   0xC100: b'\x00\x00\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2'
                                b'\xef\xfc\t\x16#0=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'
                                b"'4AN[hu\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER"
                                b'_ly\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a'
                                b'\x97\xa4\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e'
                                b'\x9b\xa8\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92'
                                b'\x9f\xac\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96'
                                b'\xa3\xb0\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a'
                                b'\xa7\xb4\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e'
                                b'\xab\xb8\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2'
                                b'\xaf\xbc\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6'
                                b'\xb3\xc0\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa'
                                b'\xb7\xc4\xd1\xde\xeb\xf8\x05\x00'},
            'read': {0x9800: 0x0100}},
    ],
    'WriteByteToBGMap0': [
        {'read': {0x9800: 0x01, 0xCAC1: 0x01}},
        {   'a': 0x5A,
            'b': 0x07,
            'c': 0x04,
            'wram': {0xCABB: b'\x00', 0xCAC1: b'\x00'},
            'read': {0x9887: 0x01, 0xCAC1: 0x01}},
        {   'a': 0x3C,
            'b': 0x07,
            'c': 0x04,
            'wram': {0xCABB: b'\x80', 0xCAC1: b'\x00'},
            'read': {0x9887: 0x01, 0xCAC1: 0x01}},
        {   'a': 0x5A,
            'f': 0xF0,
            'b': 0x07,
            'c': 0x04,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCABB: b'\x00', 0xCAC1: b'\x00'},
            'read': {0x9887: 0x01, 0xCAC1: 0x01}},
        {   'a': 0x5A,
            'f': 0xF0,
            'b': 0x07,
            'c': 0x04,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCABB: b'\x80', 0xCAC1: b'\x00'},
            'read': {0x9887: 0x01, 0xCAC1: 0x01}},
    ],
    'CopyDataToBGMap0': [
        {'a': 0x01, 'hl': 0xC100, 'wram': {0xC100: b'B'}, 'read': {0x9800: 0x01}},
        {   'a': 0x00,
            'b': 0x01,
            'c': 0x02,
            'hl': 0xC100,
            'wram': {   0xC100: b'\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2\xef\xfc\t\x16#0'
                                b"=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'4AN[h"
                                b'u\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER_l'
                                b'y\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a\x97\xa4'
                                b'\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e\x9b\xa8'
                                b'\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92\x9f\xac'
                                b'\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96\xa3\xb0'
                                b'\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a\xa7\xb4'
                                b'\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e\xab\xb8'
                                b'\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2\xaf\xbc'
                                b'\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6\xb3\xc0'
                                b'\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa\xb7\xc4'
                                b'\xd1\xde\xeb\xf8'},
            'read': {0x9841: 0x0100}},
        {   'a': 0x01,
            'b': 0x02,
            'c': 0x03,
            'hl': 0xC100,
            'wram': {   0xC100: b'\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2\xef\xfc\t\x16#0'
                                b"=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'4AN[h"
                                b'u\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER_l'
                                b'y\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a\x97\xa4'
                                b'\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e\x9b\xa8'
                                b'\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92\x9f\xac'
                                b'\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96\xa3\xb0'
                                b'\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a\xa7\xb4'
                                b'\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e\xab\xb8'
                                b'\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2\xaf\xbc'
                                b'\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6\xb3\xc0'
                                b'\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa\xb7\xc4'
                                b'\xd1\xde\xeb\xf8\x05'},
            'read': {0x9862: 0x01}},
    ],
    'SafeCopyDataHLtoDE': [
        {'b': 0x01, 'hl': 0xC100, 'd': 0x98, 'e': 0x00, 'wram': {0xC100: b'B'}, 'read': {0x9800: 0x01}},
        {   'b': 0x00,
            'hl': 0xC100,
            'd': 0x98,
            'e': 0x00,
            'wram': {   0xC100: b'\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2\xef\xfc\t\x16#0'
                                b"=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'4AN[h"
                                b'u\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER_l'
                                b'y\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a\x97\xa4'
                                b'\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e\x9b\xa8'
                                b'\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92\x9f\xac'
                                b'\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96\xa3\xb0'
                                b'\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a\xa7\xb4'
                                b'\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e\xab\xb8'
                                b'\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2\xaf\xbc'
                                b'\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6\xb3\xc0'
                                b'\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa\xb7\xc4'
                                b'\xd1\xde\xeb\xf8'},
            'read': {0x9800: 0x0100}},
        {   'b': 0x01,
            'hl': 0xC100,
            'd': 0x98,
            'e': 0x00,
            'wram': {   0xC100: b'\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2\xef\xfc\t\x16#0'
                                b"=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'4AN[h"
                                b'u\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER_l'
                                b'y\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a\x97\xa4'
                                b'\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e\x9b\xa8'
                                b'\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92\x9f\xac'
                                b'\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96\xa3\xb0'
                                b'\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a\xa7\xb4'
                                b'\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e\xab\xb8'
                                b'\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2\xaf\xbc'
                                b'\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6\xb3\xc0'
                                b'\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa\xb7\xc4'
                                b'\xd1\xde\xeb\xf8\x05'},
            'read': {0x9800: 0x01}},
    ],
    'JPHblankCopyDataHLtoDE': [
        {'b': 0x01, 'hl': 0xC100, 'd': 0x98, 'e': 0x00, 'wram': {0xC100: b'B'}, 'read': {0x9800: 0x01}},
        {   'b': 0x00,
            'hl': 0xC100,
            'd': 0x98,
            'e': 0x00,
            'wram': {   0xC100: b'\x05\x12\x1f,9FS`mz\x87\x94\xa1\xae\xbb\xc8\xd5\xe2\xef\xfc\t\x16#0'
                                b"=JWdq~\x8b\x98\xa5\xb2\xbf\xcc\xd9\xe6\xf3\x00\r\x1a'4AN[h"
                                b'u\x82\x8f\x9c\xa9\xb6\xc3\xd0\xdd\xea\xf7\x04\x11\x1e+8ER_l'
                                b'y\x86\x93\xa0\xad\xba\xc7\xd4\xe1\xee\xfb\x08\x15"/<IVcp}\x8a\x97\xa4'
                                b'\xb1\xbe\xcb\xd8\xe5\xf2\xff\x0c\x19&3@MZgt\x81\x8e\x9b\xa8'
                                b'\xb5\xc2\xcf\xdc\xe9\xf6\x03\x10\x1d*7DQ^kx\x85\x92\x9f\xac'
                                b'\xb9\xc6\xd3\xe0\xed\xfa\x07\x14!.;HUbo|\x89\x96\xa3\xb0'
                                b'\xbd\xca\xd7\xe4\xf1\xfe\x0b\x18%2?LYfs\x80\x8d\x9a\xa7\xb4'
                                b'\xc1\xce\xdb\xe8\xf5\x02\x0f\x1c)6CP]jw\x84\x91\x9e\xab\xb8'
                                b'\xc5\xd2\xdf\xec\xf9\x06\x13 -:GTan{\x88\x95\xa2\xaf\xbc'
                                b'\xc9\xd6\xe3\xf0\xfd\n\x17$1>KXer\x7f\x8c\x99\xa6\xb3\xc0'
                                b'\xcd\xda\xe7\xf4\x01\x0e\x1b(5BO\\iv\x83\x90\x9d\xaa\xb7\xc4'
                                b'\xd1\xde\xeb\xf8'},
            'read': {0x9800: 0x0100}},
    ],
}

MUTATIONS = {
    'WriteDataBlocksToBGMap0': {   'source_symbol': 'WriteDataBlocksToBGMap0',
        'before': '\t} while ((gb_read8(*hl) & 0x80) == 0);',
        'after': '\t} while ((gb_read8(*hl) & 0x80) != 0);',
        'case_ids': ['WriteDataBlocksToBGMap0-0'],
        'source': 'src/home/bg_map.c'},
    'WriteDataBlockToBGMap0': {   'source_symbol': 'WriteDataBlockToBGMap0',
        'before': '\tuint16_t source = data;',
        'after': '\tuint16_t source = (uint16_t)(data + 1);',
        'case_ids': ['WriteDataBlockToBGMap0-1', 'WriteDataBlockToBGMap0-0'],
        'source': 'src/home/bg_map.c'},
    'WriteByteToBGMap0': {   'source_symbol': 'WriteByteToBGMap0',
        'before': '\tif ((wLCDC & 0x80u) != 0u)',
        'after': '\tif ((wLCDC & 0x80u) == 0u)',
        'case_ids': ['WriteByteToBGMap0-1'],
        'source': 'src/home/bg_map.c'},
    'CopyDataToBGMap0': {   'source_symbol': 'CopyDataToBGMap0',
        'before': '\tSafeCopyDataHLtoDE(hl, de, a);',
        'after': '\t;',
        'case_ids': ['CopyDataToBGMap0-0'],
        'source': 'src/home/bg_map.c'},
    'SafeCopyDataHLtoDE': {   'source_symbol': 'SafeCopyDataHLtoDE',
        'before': '\t\tgb_write8(dst++, gb_read8(src++));',
        'after': '\t\t;',
        'case_ids': ['SafeCopyDataHLtoDE-0'],
        'source': 'src/home/bg_map.c'},
    'JPHblankCopyDataHLtoDE': {   'source_symbol': 'SafeCopyDataHLtoDE',
        'before': '\t\tgb_write8(dst++, gb_read8(src++));',
        'after': '\t\t;',
        'case_ids': ['JPHblankCopyDataHLtoDE-0'],
        'source': 'src/home/bg_map.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
