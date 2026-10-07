"""Extended oracle-diff cases for glossary, seeded from tests/cases/glossary.py."""

CONTRACT = {
    'OpenGlossaryScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    'OpenGlossaryScreen': [
        {   'keys': [0x00, 0x02],
            'wram': {   0xCE28: b'\x00',
                        0xCE18: b'\x00',
                        0xCE1B: b'\xff',
                        0xCE4D: b'\x00',
                        0xCAB6: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'keys': [0x00, 0x02],
            'wram': {   0xCE28: b'\x01',
                        0xCE18: b'\x00',
                        0xCE1B: b'\xff',
                        0xCE4D: b'\x00',
                        0xCAB6: b'\x00'},
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
            'keys': [0x00, 0x02],
            'wram': {   0xCE28: b'\x00',
                        0xCE18: b'\x00',
                        0xCE1B: b'\xff',
                        0xCE4D: b'\x00',
                        0xCAB6: b'\x00'},
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
            'keys': [0x00, 0x02],
            'wram': {   0xCE28: b'\x00',
                        0xCE18: b'U',
                        0xCE19: b'UU',
                        0xCE1B: b'\x00',
                        0xCE4D: b'\x00',
                        0xCAB6: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {0xCE28: 0x01, 0xCE18: 0x01, 0xCE19: 0x02, 0xCE1B: 0x01},
            'vread': {0x00: {0x9800: 0x0400}},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'OpenGlossaryScreen': {   'source_symbol': 'OpenGlossaryScreen',
        'before': '\twMenuInputTablePointer = (uint8_t)GLOSSARY_TRANSITION_TABLE;',
        'after': '\twMenuInputTablePointer = (uint8_t)(GLOSSARY_TRANSITION_TABLE + 1u);',
        'case_ids': ['OpenGlossaryScreen-3'],
        'source': 'src/home/glossary.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
