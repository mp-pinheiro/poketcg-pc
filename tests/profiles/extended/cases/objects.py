"""Extended oracle-diff cases for objects, seeded from tests/cases/objects.py."""

CONTRACT = {
    'SetOneObjectAttributes': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'ZeroObjectPositions': {'compare': ('b', 'd', 'e'), 'preserve': ('b', 'd', 'e')},
}

CASES = {
    'SetOneObjectAttributes': [
        {   'e': 0x10,
            'd': 0x20,
            'c': 0x30,
            'b': 0x40,
            'wram': {0xCAB5: b'\xa0'},
            'read': {0xCAA0: 0x04, 0xCAB5: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x80,
            'c': 0x70,
            'd': 0x60,
            'e': 0x50,
            'hl': 0x1234,
            'wram': {0xCAB5: b'\x08'},
            'read': {0xCA08: 0x04, 0xCAB5: 0x01}},
        {   'e': 0xA5,
            'd': 0x5A,
            'c': 0x01,
            'b': 0x02,
            'wram': {0xCAB5: b'\x9c'},
            'read': {0xCA9C: 0x04, 0xCAB5: 0x01}},
        {'wram': {0xCAB5: b'\xa0'}, 'read': {0xCA00: 0x04, 0xCAB5: 0x01}},
    ],
    'ZeroObjectPositions': [
        {'read': {0xCA00: 0xA0, 0xCAB5: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCA00: b'\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D'
                                b'\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D'
                                b'\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D'
                                b'\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D\x11"3D'
                                b'\x11"3D\x11"3D\x11"3D\x11"3D',
                        0xCAB5: b'('},
            'read': {0xCA00: 0xA0, 0xCAB5: 0x01}},
    ],
}

MUTATIONS = {
    'SetOneObjectAttributes': {   'source_symbol': 'SetOneObjectAttributes',
        'before': 'void SetOneObjectAttributes(uint8_t e, uint8_t d, uint8_t c, uint8_t b)\n'
                  '{\n'
                  '\tuint8_t off = wOAMOffset;\n'
                  '\tif (off >= OAM_SIZE)',
        'after': 'void SetOneObjectAttributes(uint8_t e, uint8_t d, uint8_t c, uint8_t b)\n'
                 '{\n'
                 '\tuint8_t off = wOAMOffset;\n'
                 '\tif (off > OAM_SIZE)',
        'case_ids': [   'SetOneObjectAttributes-0',
                        'SetOneObjectAttributes-1',
                        'SetOneObjectAttributes-2',
                        'SetOneObjectAttributes-3'],
        'source': 'src/home/objects.c'},
    'ZeroObjectPositions': {   'source_symbol': 'ZeroObjectPositions',
        'before': '\t\tuint16_t p = (uint16_t)(wOAM_ADDR + (uint16_t)i * 4u);',
        'after': '\t\tuint16_t p = (uint16_t)(wOAM_ADDR + (uint16_t)i * 5u);',
        'case_ids': ['ZeroObjectPositions-1'],
        'source': 'src/home/objects.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
