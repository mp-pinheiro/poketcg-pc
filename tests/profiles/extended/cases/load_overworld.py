"""Extended oracle-diff cases for load_overworld, seeded from tests/cases/load_overworld.py."""

CONTRACT = {
    'LoadMapTilesAndPals': {'compare': (), 'preserve': (), 'wram_out': True},
    'ReloadMapAfterTextClose': {'compare': (), 'preserve': (), 'wram_out': True},
    'LoadMapGfxAndPermissions': {'compare': (), 'preserve': (), 'wram_out': True},
}

CASES = {
    'LoadMapTilesAndPals': [
        {   'wram': {0xD31C: b'\x00', 0xD27E: b'\x00'},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0xF42400,
            'read': {0xD4B7: 0x01, 0xD4B8: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD31C: b'\x00', 0xD27E: b'\x00'},
            'instruction_budget': 0x3D0900,
            'cycle_budget': 0xF42400,
            'read': {0xD4B7: 0x01, 0xD4B8: 0x01}},
    ],
    'ReloadMapAfterTextClose': [
        {   'wram': {   0xD120: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {0xD120: 0x0100},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD120: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
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
            'read': {0xD120: 0x0100},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'LoadMapGfxAndPermissions': [
        {   'wram': {0xD31C: b'\x01'},
            'read': {0xCCA1: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'wram': {0xD31C: b'\x00'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {0xCCA1: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD31C: b'\x01'},
            'read': {0xCCA1: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'LoadMapTilesAndPals': {   'source_symbol': 'LoadMapTilesAndPals',
        'before': '\twWhichBGPalIndex = wd291;\n\tuint8_t pal = wCurMapPalette;',
        'after': '\twWhichBGPalIndex = (uint8_t)(wd291 + 1u);\n\tuint8_t pal = wCurMapPalette;',
        'case_ids': ['LoadMapTilesAndPals-0', 'LoadMapTilesAndPals-1'],
        'source': 'src/home/load_overworld.c'},
    'ReloadMapAfterTextClose': {   'source_symbol': 'ReloadMapAfterTextClose',
        'before': '\tFunc_c3ee();',
        'after': '\tFunc_c3ff();',
        'case_ids': ['ReloadMapAfterTextClose-1'],
        'source': 'src/home/load_overworld.c'},
    'LoadMapGfxAndPermissions': {   'source_symbol': 'LoadMapGfxAndPermissions',
        'before': 'void LoadMapGfxAndPermissions(void)\n'
                  '{\n'
                  '\tClearSRAMBGMaps();\n'
                  '\twTextBoxFrameType = 0u;',
        'after': 'void LoadMapGfxAndPermissions(void)\n'
                 '{\n'
                 '\tClearSRAMBGMaps();\n'
                 '\twTextBoxFrameType = 1u;',
        'case_ids': [   'LoadMapGfxAndPermissions-0',
                        'LoadMapGfxAndPermissions-1',
                        'LoadMapGfxAndPermissions-2'],
        'source': 'src/home/load_overworld.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
