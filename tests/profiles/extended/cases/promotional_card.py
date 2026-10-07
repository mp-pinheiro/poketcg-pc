"""Extended oracle-diff cases for promotional_card, seeded from tests/cases/promotional_card.py."""

CONTRACT = {
    '_ShowPromotionalCardScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    '_ShowPromotionalCardScreen': [
        {   'oracle': False,
            'why': 'Extended promotional screen waits for song and input completion outside the isolated oracle.',
            'a': 0x1E,
            'expect': {0xCBD2: b'\x02', 0xFF97: b'\x01', 0xCCB2: b'\x01', 0xCCB4: b'\x02', 0xFFA8: b'\x01'}},
        {   'oracle': False,
            'why': 'Extended promotional screen waits for song and input completion outside the isolated oracle.',
            'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'expect': {0xCBD2: b'\x02', 0xFF97: b'\x01', 0xCCB2: b'\x01', 0xCCB4: b'\x02', 0xFFA8: b'\x01'}},
    ],
}

MUTATIONS = {
    '_ShowPromotionalCardScreen': {   'source_symbol': '_ShowPromotionalCardScreen',
        'before': '\t\tLoadCardDataToBuffer1_FromCardID(card);\n\t\tPauseSong();',
        'after': '\t\tLoadCardDataToBuffer1_FromCardID((uint8_t)(card + 1u));\n\t\tPauseSong();',
        'case_ids': ['_ShowPromotionalCardScreen-0', '_ShowPromotionalCardScreen-1'],
        'source': 'src/profiles/extended/home/promotional_card.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
