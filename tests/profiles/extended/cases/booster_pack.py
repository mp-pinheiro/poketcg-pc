"""Extended oracle-diff cases for booster_pack, seeded from tests/cases/booster_pack.py."""

CONTRACT = {
    '_OpenBoosterPack': {'compare': (), 'preserve': (), 'wram_out': True},
}

CASES = {
    '_OpenBoosterPack': [
        {   'wram': {   0xC200: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
                        0xC400: b'\x00',
                        0xCABB: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x02],
            'read': {0xFF97: 0x01, 0xC200: 0x3C, 0xC500: 0x01, 0xCB84: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xC200: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
                        0xC400: b'\x00',
                        0xCABB: b'\x00'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x02],
            'read': {0xFF97: 0x01, 0xC200: 0x3C, 0xC500: 0x01, 0xCB84: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    '_OpenBoosterPack': {   'source_symbol': '_OpenBoosterPack',
        'before': 'void _OpenBoosterPack(void)\n{\n\thWhoseTurn = PLAYER_TURN;',
        'after': 'void _OpenBoosterPack(void)\n{\n\thWhoseTurn = (uint8_t)(PLAYER_TURN + 1u);',
        'case_ids': ['_OpenBoosterPack-0', '_OpenBoosterPack-1'],
        'source': 'src/profiles/extended/home/booster_pack.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
