"""Extended oracle-diff cases for status, seeded from tests/cases/status.py."""

CONTRACT = {
    '_PauseMenu_Status': {'compare': (), 'preserve': ()},
}

CASES = {
    '_PauseMenu_Status': [
        {   'keys': [0x00, 0x01],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xD27E: b'Z'},
            'read': {0xD27E: 0x01, 0xD101: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xD27E: b'Z'},
            'read': {0xD27E: 0x01, 0xD101: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x5F5E100},
    ],
}

MUTATIONS = {
    '_PauseMenu_Status': {   'source_symbol': '_PauseMenu_Status',
        'before': 'void _PauseMenu_Status(void)\n{\n\tuint8_t saved_d291 = wd291;',
        'after': 'void _PauseMenu_Status(void)\n{\n\tuint8_t saved_d291 = 0u;',
        'case_ids': ['_PauseMenu_Status-0', '_PauseMenu_Status-1'],
        'source': 'src/profiles/extended/home/status.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
