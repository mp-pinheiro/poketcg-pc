"""Extended oracle-diff cases for give_booster_pack, seeded from tests/cases/give_booster_pack.py."""

CONTRACT = {
    '_PauseMenu_Exit': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('a', 'f', 'b', 'c', 'd', 'e', 'hl')},
    'GiveBoosterPack': {'compare': (), 'preserve': ()},
}

CASES = {
    '_PauseMenu_Exit': [
        {'wram': {0xC000: b'Z'}, 'read': {0xC000: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC000: b'\xa5'},
            'read': {0xC000: 0x01}},
    ],
    'GiveBoosterPack': [
        {   'a': 0x00,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xD104: b'\x00'},
            'read': {0xCE05: 0x02, 0xCE09: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x08,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xD104: b'\x00'},
            'read': {0xCE05: 0x02, 0xCE09: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x17,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xD104: b'\x01'},
            'read': {0xCE05: 0x02, 0xCE09: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x0E,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {0xCABB: b'\x00', 0xD104: b'\x00'},
            'read': {0xCE05: 0x02, 0xCE09: 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
    ],
}

MUTATIONS = {
    '_PauseMenu_Exit': {   'source_symbol': '_PauseMenu_Exit',
        'before': 'void _PauseMenu_Exit(void)\n{\n}',
        'after': 'void _PauseMenu_Exit(void)\n{\n\tgb_write8(0xC000, 0x01);\n}',
        'case_ids': ['_PauseMenu_Exit-0', '_PauseMenu_Exit-1'],
        'source': 'src/profiles/extended/home/give_booster_pack.c'},
    'GiveBoosterPack': {   'source_symbol': 'GiveBoosterPack',
        'before': '\twTxRam3 = scene;\n\tgb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);',
        'after': '\twTxRam3 = (uint8_t)(scene + 1u);\n'
                 '\tgb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);',
        'case_ids': ['GiveBoosterPack-0', 'GiveBoosterPack-1', 'GiveBoosterPack-3'],
        'source': 'src/profiles/extended/home/give_booster_pack.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
