"""Extended oracle-diff cases for copy_card_name, seeded from tests/cases/copy_card_name.py."""

CONTRACT = {
    '_CopyCardNameAndLevel_HalfwidthText': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    '_CopyCardNameAndLevel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
}

CASES = {
    '_CopyCardNameAndLevel_HalfwidthText': [
        {   'wram': {0xC580: b'AB\x00', 0xCBCF: b'\x08', 0xCC08: b'\x00', 0xCD21: b'\x04'},
            'stack': [0xBBCC, 0xDDEE],
            'read': {0xC580: 0x0A}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC580: b'AB\x00', 0xCBCF: b'\x08', 0xCC08: b'\x00', 0xCD21: b'\x04'},
            'stack': [0xBBCC, 0xDDEE],
            'read': {0xC580: 0x0A}},
        {   'wram': {0xC580: b'AB\x00', 0xCBCF: b'\x00', 0xCC08: b'\x0c', 0xCD21: b'\x04'},
            'stack': [0xBBCC, 0xDDEE],
            'read': {0xC580: 0x0A}},
    ],
    '_CopyCardNameAndLevel': [
        {   'a': 0x0D,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'setup': [{'fn': 'LoadCardDataToBuffer1_FromCardID', 'e': 0x43}],
            'read': {0xC580: 0x20}},
        {   'a': 0x0D,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'setup': [{'fn': 'LoadCardDataToBuffer1_FromCardID', 'e': 0x03}],
            'read': {0xC580: 0x20}},
        {   'a': 0x0D,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'setup': [{'fn': 'LoadCardDataToBuffer1_FromCardID', 'e': 0x43}],
            'read': {0xC580: 0x20}},
    ],
}

MUTATIONS = {
    '_CopyCardNameAndLevel_HalfwidthText': {   'source_symbol': '_CopyCardNameAndLevel_HalfwidthText',
        'before': '\tuint8_t b = (uint8_t)((uint8_t)(wCardNameLength + 1u) << 1);',
        'after': '\tuint8_t b = (uint8_t)((uint8_t)(wCardNameLength + 2u) << 1);',
        'case_ids': [   '_CopyCardNameAndLevel_HalfwidthText-0',
                        '_CopyCardNameAndLevel_HalfwidthText-2'],
        'source': 'src/profiles/extended/home/copy_card_name.c'},
    '_CopyCardNameAndLevel': {   'source_symbol': '_CopyCardNameAndLevel',
        'before': '\tif (gb_read8(wDefaultText_ADDR) == TX_HALFWIDTH)',
        'after': '\tif (gb_read8(wDefaultText_ADDR) != TX_HALFWIDTH)',
        'case_ids': ['_CopyCardNameAndLevel-0', '_CopyCardNameAndLevel-1'],
        'source': 'src/profiles/extended/home/copy_card_name.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
