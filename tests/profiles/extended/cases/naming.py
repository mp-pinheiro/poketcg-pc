"""Extended oracle-diff cases for naming, seeded from tests/cases/naming.py."""

CONTRACT = {
    'DisplayPlayerNamingScreen': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
}

CASES = {
    'DisplayPlayerNamingScreen': [
        {   'rom_bank': 0x04,
            'keys': 0x41,
            'wram': {   0xC4F0: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xFF90: b'\x00',
                        0xD00B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCACA: b'Z',
                        0xCACB: b'\xc3',
                        0xCACC: b'\x00'},
            'sram': {0x00: {}},
            'sread': {0x00: {0xA010: 0x10}},
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
            'rom_bank': 0x04,
            'keys': 0x41,
            'wram': {   0xC4F0: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xFF90: b'\x00',
                        0xD00B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCACA: b'\xb7',
                        0xCACB: b'.',
                        0xCACC: b'\xfd'},
            'sram': {0x00: {}},
            'sread': {0x00: {0xA010: 0x10}},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'DisplayPlayerNamingScreen': {   'source_symbol': 'DisplayPlayerNamingScreen',
        'before': '\tif (gb_read8(hl) == 0u)',
        'after': '\tif (gb_read8(hl) != 0u)',
        'case_ids': ['DisplayPlayerNamingScreen-0', 'DisplayPlayerNamingScreen-1'],
        'source': 'src/profiles/extended/home/naming.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
