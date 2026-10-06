"""Extended oracle-diff cases for card_data, seeded from tests/cases/card_data.py."""

CONTRACT = {
    'GetCardType': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GetCardName': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'GetCardTypeRarityAndSet': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'LoadCardDataToBuffer1_FromCardID': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadCardDataToBuffer2_FromCardID': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadCardDataToBuffer1_FromName': {'compare': (), 'preserve': ()},
    'GetCardPointer': {'compare': ('f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'LoadCardDataToHL_FromCardID': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
}

CASES = {
    'GetCardType': [
        {'e': 0x01},
        {'e': 0x08},
        {'e': 0x40},
        {'e': 0x80},
        {'e': 0xE4},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0x20, 'hl': 0x1234},
    ],
    'GetCardName': [
        {'e': 0x01},
        {'e': 0x08},
        {'e': 0x40},
        {'e': 0xE4},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0x60, 'hl': 0x1234},
    ],
    'GetCardTypeRarityAndSet': [
        {'a': 0x01},
        {'a': 0x08},
        {'a': 0x40},
        {'a': 0xE4},
        {'a': 0x30, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'LoadCardDataToBuffer1_FromCardID': [
        {   'e': 0x08,
            'wram': {   0xCBCF: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xCBCF: 0x41}},
        {'e': 0x80, 'read': {0xCBCF: 0x41}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xD8,
            'e': 0x07,
            'hl': 0x1234,
            'wram': {   0xCBCF: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xCBCF: 0x41}},
    ],
    'LoadCardDataToBuffer2_FromCardID': [
        {   'e': 0x08,
            'wram': {   0xCC10: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xCC10: 0x41}},
        {'e': 0xE4, 'read': {0xCC10: 0x41}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0x40,
            'hl': 0x1234,
            'wram': {   0xCC10: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xCC10: 0x41}},
    ],
    'LoadCardDataToBuffer1_FromName': [
        {'d': 0x08, 'e': 0x0A, 'read': {0xCBCF: 0x41}},
        {'d': 0x09, 'e': 0x1C, 'read': {0xCBCF: 0x41}},
        {   'd': 0xFF,
            'e': 0xFF,
            'wram': {   0xCBCF: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xCBCF: 0x41}},
    ],
    'GetCardPointer': [
        {'e': 0x00},
        {'e': 0xE4},
        {'e': 0xE5},
        {'e': 0xE6},
        {'e': 0xFF},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0x08, 'hl': 0x1234},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xD8, 'e': 0x08, 'hl': 0x1234},
    ],
    'LoadCardDataToHL_FromCardID': [
        {'stack': [0x00]},
        {   'e': 0x01,
            'hl': 0xC100,
            'stack': [0xC100],
            'wram': {   0xC100: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xC100: 0x41}},
        {   'e': 0xE4,
            'hl': 0xC200,
            'stack': [0xC200],
            'wram': {   0xC200: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xC200: 0x41}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'stack': [0x1234]},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0x01,
            'hl': 0xC300,
            'stack': [0xC300],
            'wram': {   0xC300: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa'},
            'read': {0xC300: 0x41}},
        {   'e': 0x10,
            'hl': 0xC100,
            'stack': [0xC100],
            'wram': {   0xC100: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
                        0xFF80: b'\x03'},
            'read': {0xC100: 0x41, 0xFF80: 0x01},
            'rom_bank': 0x03},
    ],
}

MUTATIONS = {
    'GetCardType': {   'source_symbol': 'GetCardType',
        'before': '\treturn card_data(e)[CARD_DATA_TYPE];',
        'after': '\treturn card_data(e)[CARD_DATA_RARITY];',
        'case_ids': [   'GetCardType-0',
                        'GetCardType-1',
                        'GetCardType-2',
                        'GetCardType-3',
                        'GetCardType-4',
                        'GetCardType-5'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'GetCardName': {   'source_symbol': 'GetCardName',
        'before': '\tconst uint8_t *p = card_data(e) + CARD_DATA_NAME;',
        'after': '\tconst uint8_t *p = card_data(e) - CARD_DATA_NAME;',
        'case_ids': ['GetCardName-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'GetCardTypeRarityAndSet': {   'source_symbol': 'GetCardTypeRarityAndSet',
        'before': '\treturn (CardTRS){p[CARD_DATA_TYPE], p[CARD_DATA_RARITY], p[CARD_DATA_SET]};',
        'after': '\treturn (CardTRS){p[(CARD_DATA_TYPE + 1u)], p[CARD_DATA_RARITY], '
                 'p[CARD_DATA_SET]};',
        'case_ids': ['GetCardTypeRarityAndSet-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'LoadCardDataToBuffer1_FromCardID': {   'source_symbol': 'LoadCardDataToBuffer1_FromCardID',
        'before': '\tload_card_data(e, wLoadedCard1_ADDR);',
        'after': '\tload_card_data((uint8_t)(e ^ 1u), wLoadedCard1_ADDR);',
        'case_ids': ['LoadCardDataToBuffer1_FromCardID-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'LoadCardDataToBuffer2_FromCardID': {   'source_symbol': 'LoadCardDataToBuffer2_FromCardID',
        'before': '\tload_card_data(e, wLoadedCard2_ADDR);',
        'after': '\tload_card_data((uint8_t)(e ^ 1u), wLoadedCard2_ADDR);',
        'case_ids': ['LoadCardDataToBuffer2_FromCardID-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'LoadCardDataToBuffer1_FromName': {   'source_symbol': 'LoadCardDataToBuffer1_FromName',
        'before': '\t\tif (ptr == 0)',
        'after': '\t\tif (ptr != 0)',
        'case_ids': ['LoadCardDataToBuffer1_FromName-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'GetCardPointer': {   'source_symbol': 'GetCardPointer',
        'before': '\tif (hl >= GETCARDPTR_BOUND)',
        'after': '\tif (hl > GETCARDPTR_BOUND)',
        'case_ids': ['GetCardPointer-2'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'LoadCardDataToHL_FromCardID': {   'source_symbol': 'LoadCardDataToHL_FromCardID',
        'before': '\tuint8_t copy_length = PKMN_CARD_DATA_LENGTH;',
        'after': '\tuint8_t copy_length = 0x40u;',
        'case_ids': [   'LoadCardDataToHL_FromCardID-1',
                        'LoadCardDataToHL_FromCardID-2',
                        'LoadCardDataToHL_FromCardID-4'],
        'source': 'src/profiles/extended/home/card_data.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
