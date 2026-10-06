"""Extended oracle-diff cases for starter_deck, seeded from tests/cases/starter_deck.py."""

CONTRACT = {
    'InitSaveData': {'compare': (), 'preserve': ()},
    '_AddStarterDeck': {'compare': (), 'preserve': ()},
}

CASES = {
    'InitSaveData': [
        {   'wram': {0xFF97: b'\xff'},
            'sram': {   0x00: {   0xA100: b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
                                          b'\x11\x11\x11\x11',
                                  0xBC00: b'\xaa\xbb\xcc',
                                  0xBB00: b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""',
                                  0xA003: b'\xff',
                                  0xA006: b'\xff',
                                  0xA007: b'\xff',
                                  0xA009: b'\xff',
                                  0xA004: b'\xff',
                                  0xA005: b'\xff',
                                  0xA00A: b'\xff'}},
            'read': {0xFF97: 0x01, 0xCE0D: 0x01},
            'sread': {   0x00: {   0xA100: 0x0100,
                                   0xA470: 0x20,
                                   0xA4CC: 0x20,
                                   0xA528: 0x20,
                                   0xBC00: 0x03,
                                   0xBB00: 0x0100,
                                   0xA003: 0x01,
                                   0xA006: 0x01,
                                   0xA007: 0x01,
                                   0xA009: 0x01,
                                   0xA004: 0x01,
                                   0xA005: 0x01,
                                   0xA00A: 0x01}},
            'vread': {0x00: {0x9380: 0x20}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF97: b'\xff'},
            'sram': {   0x00: {   0xA100: b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333',
                                  0xBC00: b'\x11"3',
                                  0xBB00: b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'}},
            'read': {0xFF97: 0x01, 0xCE0D: 0x01},
            'sread': {   0x00: {   0xA100: 0x0100,
                                   0xA470: 0x20,
                                   0xA4CC: 0x20,
                                   0xA528: 0x20,
                                   0xBC00: 0x03,
                                   0xBB00: 0x0100,
                                   0xA003: 0x01,
                                   0xA006: 0x01,
                                   0xA007: 0x01,
                                   0xA009: 0x01,
                                   0xA004: 0x01,
                                   0xA005: 0x01,
                                   0xA00A: 0x01}},
            'vread': {0x00: {0x9380: 0x20}}},
    ],
    '_AddStarterDeck': [
        {   'a': 0x00,
            'wram': {   0xFF97: b'\xff',
                        0xC400: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;",
                        0xC478: b'<=>?@ABCDEFGHIJKLMNOPQRSTUVWXY'},
            'sram': {   0x00: {   0xA100: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80'}},
            'read': {0xFF97: 0x01},
            'sread': {0x00: {0xA100: 0x0100, 0xA300: 0x20}}},
        {   'a': 0x02,
            'wram': {   0xFF97: b'\xff',
                        0xC400: b'\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXY',
                        0xC478: b'Z[\\]^_`abcdefghijklmnopqrstuvw'},
            'sram': {   0x00: {   0xA100: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80'}},
            'read': {0xFF97: 0x01},
            'sread': {0x00: {0xA100: 0x0100, 0xA300: 0x20}}},
        {   'a': 0x00,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF97: b'\xff',
                        0xC400: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;",
                        0xC478: b'<=>?@ABCDEFGHIJKLMNOPQRSTUVWXY'},
            'sram': {   0x00: {   0xA100: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                          b'\x80\x80\x80\x80'}},
            'read': {0xFF97: 0x01},
            'sread': {0x00: {0xA100: 0x0100, 0xA300: 0x20}}},
    ],
}

MUTATIONS = {
    'InitSaveData': {   'source_symbol': 'InitSaveData',
        'before': '\tgb_write8(sTextSpeed_ADDR, TEXT_SPEED_3);',
        'after': '\tgb_write8(sTextSpeed_ADDR, 3u);',
        'case_ids': ['InitSaveData-0', 'InitSaveData-1'],
        'source': 'src/profiles/extended/home/starter_deck.c'},
    '_AddStarterDeck': {   'source_symbol': '_AddStarterDeck',
        'before': '\t\tgb_write8(slot, (uint8_t)(v + 1u));',
        'after': '\t\tgb_write8(slot, v);',
        'case_ids': ['_AddStarterDeck-0', '_AddStarterDeck-1'],
        'source': 'src/profiles/extended/home/starter_deck.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
