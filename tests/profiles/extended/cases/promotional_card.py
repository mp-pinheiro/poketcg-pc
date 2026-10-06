"""Extended oracle-diff cases for promotional_card, seeded from tests/cases/promotional_card.py."""

CONTRACT = {
    '_ShowPromotionalCardScreen': {'compare': (), 'preserve': ()},
}

CASES = {
    '_ShowPromotionalCardScreen': [
        {   'a': 0x1E,
            'keys': [0x00, 0x02],
            'read': {0xCBD2: 0x02, 0xFF97: 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}],
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
            'read': {0xCBD2: 0x02, 0xFF97: 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
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
