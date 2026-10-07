"""Extended oracle-diff cases for warp, seeded from tests/cases/warp.py."""

CONTRACT = {
    '_HandleMapWarp': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    '_HandleMapWarp': [
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x1a',
                        0xD31E: b'\n',
                        0xD321: b'\x02',
                        0xD0A8: b'\x00\x00\x00\x00'}},
        {   'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x00',
                        0xD31E: b'\x00',
                        0xD321: b'\x00',
                        0xD0A8: b'\x11"3D'}},
        {   'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x0e',
                        0xD31E: b'\x1c',
                        0xD321: b'\x01',
                        0xD0A8: b'\x11"3D'}},
        {   'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x10',
                        0xD31E: b'\x1c',
                        0xD321: b'\x03',
                        0xD0A8: b'\x11"3D'}},
        {'wram': {0xD31C: b'\x02', 0xD31D: b'\x00', 0xD31E: b'\n', 0xD321: b'\x04', 0xD0A8: b'\x11"3D'}},
        {   'a': 0x07,
            'b': 0x00,
            'c': 0x0E,
            'd': 0x16,
            'e': 0x15,
            'f': 0x00,
            'hl': 0xD4CB,
            'wram': {0xD31C: b'\x01',
                     0xD31D: b'\x00',
                     0xD31E: b'\x00',
                     0xD321: b'\x00',
                     0xD0A8: b'\x00\x00\x00\x00'},
            'read': {0xD0A8: 0x04}},
    ],
}

MUTATIONS = {
    '_HandleMapWarp': {   'source_symbol': '_HandleMapWarp',
        'before': 'if((uint8_t)(wx|wy)==0){flags=0x80u;break;}',
        'after': 'if((uint8_t)(wx|wy)==0){break;}',
        'case_ids': [   '_HandleMapWarp-5',
                        '_HandleMapWarp-0',
                        '_HandleMapWarp-1',
                        '_HandleMapWarp-2',
                        '_HandleMapWarp-3',
                        '_HandleMapWarp-4'],
        'source': 'src/profiles/extended/home/warp.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
