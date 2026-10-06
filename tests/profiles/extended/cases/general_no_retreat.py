"""Extended oracle-diff cases for general_no_retreat, seeded from tests/cases/general_no_retreat.py."""

CONTRACT = {
    'AIDoTurn_GeneralNoRetreat': {'compare': ('f',), 'preserve': ()},
}

CASES = {
    'AIDoTurn_GeneralNoRetreat': [
        {   'keys': [0x00, 0x01],
            'wram': {   0xFF97: b'\xc2',
                        0xCD2D: b'\x80',
                        0xC2EE: b'\x00',
                        0xC3EE: b'\x00',
                        0xC2BB: b'\x00',
                        0xC3BB: b'\x00',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb9\xff',
                        0xC600: b'\xb9\xff',
                        0xCBB5: b'\x01',
                        0xCDA6: b'\x00',
                        0xCAC2: b'\x01',
                        0xCBA3: b'\x01'},
            'read': {0xCDA6: 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'wram': {   0xFF97: b'\xc2',
                        0xCD2D: b'\x80',
                        0xC2EE: b'\x00',
                        0xC3EE: b'\x00',
                        0xC2BB: b'\x00',
                        0xC3BB: b'\x00',
                        0xC2BC: b'\xff',
                        0xC3BC: b'\xff',
                        0xC400: b'\xb9\xff',
                        0xC600: b'\xb9\xff',
                        0xCBB5: b'\x01',
                        0xCDA6: b'\x00',
                        0xCAC2: b'\x01',
                        0xCBA3: b'\x01'},
            'read': {0xCDA6: 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'AIDoTurn_GeneralNoRetreat': {   'source_symbol': 'AIDoTurn_GeneralNoRetreat',
        'before': 'AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, '
                  'uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n'
                  '{\n'
                  '\tInitAITurnVars();',
        'after': 'AIDoTurn_GeneralNoRetreatResult AIDoTurn_GeneralNoRetreat(uint8_t a, uint8_t f, '
                 'uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n'
                 '{\n'
                 '\tuint8_t unused = 0u;',
        'case_ids': ['AIDoTurn_GeneralNoRetreat-0', 'AIDoTurn_GeneralNoRetreat-1'],
        'source': 'src/profiles/extended/home/general_no_retreat.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
