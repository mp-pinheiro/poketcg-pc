"""Extended oracle-diff cases for intro, seeded from tests/cases/intro.py."""

CONTRACT = {
    'LoadTitleScreenSprites': {'compare': (), 'preserve': ()},
    'PlayIntroSequence': {'compare': (), 'preserve': ()},
}

CASES = {
    'LoadTitleScreenSprites': [
        {   'read': {   0xD616: 0x07,
                        0xD4BE: 0x01,
                        0xD4C1: 0x01,
                        0xD4CE: 0x01,
                        0xD4D1: 0x01,
                        0xD4DE: 0x01,
                        0xD4E1: 0x01,
                        0xD4EE: 0x01,
                        0xD4F1: 0x01,
                        0xD4FE: 0x01,
                        0xD501: 0x01,
                        0xD50E: 0x01,
                        0xD511: 0x01,
                        0xD51E: 0x01,
                        0xD521: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {   0xD616: 0x07,
                        0xD4BE: 0x01,
                        0xD4C1: 0x01,
                        0xD4CE: 0x01,
                        0xD4D1: 0x01,
                        0xD4DE: 0x01,
                        0xD4E1: 0x01,
                        0xD4EE: 0x01,
                        0xD4F1: 0x01,
                        0xD4FE: 0x01,
                        0xD501: 0x01,
                        0xD50E: 0x01,
                        0xD511: 0x01,
                        0xD51E: 0x01,
                        0xD521: 0x01}},
    ],
    'PlayIntroSequence': [
        {   'completion': {'mode': 'entry', 'pc': 0x336C, 'bank': 0x00, 'routine': 'DoFrameIfLCDEnabled'},
            'wram': {0xD61E: b'\x00\x00', 0xD304: b'\xff', 0xD621: b'\xff', 0xD620: b'\xff'},
            'read': {0xD61E: 0x02, 0xD304: 0x01, 0xD621: 0x01, 0xD620: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'completion': {'mode': 'entry', 'pc': 0x336C, 'bank': 0x00, 'routine': 'DoFrameIfLCDEnabled'},
            'wram': {0xD61E: b'\x00\x00', 0xD304: b'\xff', 0xD621: b'\xff', 0xD620: b'\xff'},
            'read': {0xD61E: 0x02, 0xD304: 0x01, 0xD621: 0x01, 0xD620: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'LoadTitleScreenSprites': {   'source_symbol': 'LoadTitleScreenSprites',
        'before': 'gb_write8(property, (uint8_t)(gb_read8(property) | index));',
        'after': 'gb_write8(property, (uint8_t)(gb_read8(property) | (uint8_t)(index + 1u)));',
        'case_ids': ['LoadTitleScreenSprites-0', 'LoadTitleScreenSprites-1'],
        'source': 'src/profiles/extended/home/intro.c'},
    'PlayIntroSequence': {   'source_symbol': 'PlayIntroSequence',
        'before': '\twd317 = 0u;',
        'after': '\twd317 = 0xFFu;',
        'case_ids': ['PlayIntroSequence-0', 'PlayIntroSequence-1'],
        'source': 'src/profiles/extended/home/intro.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _name, _entries in CASES.items():
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
