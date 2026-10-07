"""Extended oracle-diff cases for init, seeded from tests/cases/init.py."""

CONTRACT = {
    'InitAIDuelVars': {'compare': ('b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'InitAITurnVars': {'compare': (), 'preserve': ()},
}

CASES = {
    'InitAIDuelVars': [
        {'wram': {0xCD2B: b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCD2B: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'}},
    ],
    'InitAITurnVars': [
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCD2C: b'\x05',
                        0xCDA6: b'\xaa',
                        0xCD62: b'\xbb',
                        0xCD63: b'\xcc',
                        0xCD8A: b'\xdd',
                        0xCBBA: b'\xff',
                        0xCBBB: b'\x00',
                        0xCD2D: b'\x05'},
            'expect': {   0xCD2C: b'\x06',
                          0xCDA6: b'\x00',
                          0xCD62: b'\x00',
                          0xCD63: b'\x00',
                          0xCD8A: b'\x00',
                          0xCD2D: b'\x00'}},
    ],
}

MUTATIONS = {
    'InitAIDuelVars': {   'source_symbol': 'InitAIDuelVars',
        'before': 'wAIPokedexCounter = 5u;',
        'after': 'wAIPokedexCounter = 4u;',
        'case_ids': ['InitAIDuelVars-0', 'InitAIDuelVars-1'],
        'source': 'src/home/init.c'},
    'InitAITurnVars': {   'source_symbol': 'InitAITurnVars',
        'before': 'wAIPokedexCounter = (uint8_t)(wAIPokedexCounter + 1u);',
        'after': 'wAIPokedexCounter = (uint8_t)(wAIPokedexCounter + 2u);',
        'case_ids': ['InitAITurnVars-0'],
        'source': 'src/home/init.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
