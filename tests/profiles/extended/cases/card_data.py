"""Extended oracle-diff cases for card_data: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('card_data', remove=(
    'CopyFontsOrDuelGraphicsTiles2',
    'LoadCardGfx',
))
OWN = (
    'GetCardPointer',
    'GetCardTypeRarityAndSet',
)
CONTRACT.update({
    'GetCardTypeRarityAndSet': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('d', 'hl')},
    'GetCardPointer': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
})
CASES.update({
    'GetCardTypeRarityAndSet': [
        {'e': 0x01},
        {'e': 0x08},
        {'e': 0x40},
        {'e': 0xE4},
        {'a': 0x30, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0x00, 'e': 0x60, 'hl': 0x1234},
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
})
MUTATIONS.update({
    'GetCardType': {   'source_symbol': 'GetCardType',
        'before': '\treturn rom_ptr(pointer.bank, pointer.hl)[CARD_DATA_TYPE];',
        'after': '\treturn rom_ptr(pointer.bank, pointer.hl)[CARD_DATA_RARITY];',
        'case_ids': [   'GetCardType-0',
                        'GetCardType-1',
                        'GetCardType-2',
                        'GetCardType-3',
                        'GetCardType-4',
                        'GetCardType-5'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'GetCardName': {   'source_symbol': 'GetCardName',
        'before': '\treturn (uint16_t)(p[0] | (uint16_t)p[1] << 8);',
        'after': '\treturn e;',
        'case_ids': ['GetCardName-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'GetCardTypeRarityAndSet': {   'source_symbol': 'GetCardTypeRarityAndSet',
        'before': '\treturn (CardTRS){p[CARD_DATA_TYPE], p[CARD_DATA_RARITY], p[CARD_DATA_SET], 0u};',
        'after': '\treturn (CardTRS){p[(CARD_DATA_TYPE + 1u)], p[CARD_DATA_RARITY], p[CARD_DATA_SET], 0u};',
        'case_ids': ['GetCardTypeRarityAndSet-0'],
        'source': 'src/profiles/extended/home/card_data.c'},
    'GetCardPointer': {   'source_symbol': 'get_card_pointer',
        'before': '\tif (entry >= GETCARDPTR_BOUND)',
        'after': '\tif (entry > GETCARDPTR_BOUND)',
        'case_ids': ['GetCardPointer-2'],
        'source': 'src/profiles/extended/home/card_data.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
