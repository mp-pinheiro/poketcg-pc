"""Extended oracle-diff cases for promotional_card: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('promotional_card')
OWN = ('_ShowPromotionalCardScreen',)
CONTRACT.update({
    '_ShowPromotionalCardScreen': {'compare': (), 'preserve': ()},
})
CASES.update({
    '_ShowPromotionalCardScreen': [
        {   'd': 0x00,
            'e': 0x1E,
            'keys': [0x00, 0x02],
            'read': {sym("wLoadedCard1Name"): 0x02, sym("hWhoseTurn"): 0x01},
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
            'read': {sym("wLoadedCard1Name"): 0x02, sym("hWhoseTurn"): 0x01},
            'setup': [{'fn': 'CopyDMAFunction'}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
})
MUTATIONS.update({
    '_ShowPromotionalCardScreen': {   'source_symbol': '_ShowPromotionalCardScreen',
        'before': '\t\tLoadCardDataToBuffer1_FromCardID(card);\n\t\tPauseSong();',
        'after': '\t\tLoadCardDataToBuffer1_FromCardID((uint8_t)(card + 1u));\n\t\tPauseSong();',
        'case_ids': ['_ShowPromotionalCardScreen-0', '_ShowPromotionalCardScreen-1'],
        'source': 'src/profiles/extended/home/promotional_card.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _record in SCHEMA2_CASES["_ShowPromotionalCardScreen"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("_ShowPromotionalCardScreen.loop")}
