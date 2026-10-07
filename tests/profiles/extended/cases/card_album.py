"""Extended oracle-diff cases for card_album, seeded from tests/cases/card_album.py."""

CONTRACT = {
    'GetFirstOwnedCardIndex': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('c', 'd', 'e')},
    'PrintCardSetListEntries': {'compare': ('hl',), 'preserve': ()},
    'CreateCardSetList': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleCardAlbumCardPage': {'compare': ('a', 'f'), 'preserve': ()},
    'CreateCardSetListAndInitListCoords': {'compare': ('a', 'f'), 'preserve': ('a', 'f')},
    'CardAlbum': {'compare': (), 'preserve': ()},
}

CASES = {
    'GetFirstOwnedCardIndex': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'setup': [{'fn': 'FillMemoryWithA', 'hl': 0xD72C, 'b': 0x00, 'c': 0x03, 'a': 0x80}]},
        {'setup': [{'fn': 'FillMemoryWithA', 'hl': 0xD72C, 'b': 0x00, 'c': 0x40, 'a': 0x80}]},
        {   'setup': [   {'fn': 'FillMemoryWithA', 'hl': 0xD72C, 'b': 0x00, 'c': 0x01, 'a': 0x80},
                         {'fn': 'FillMemoryWithA', 'hl': 0xD72D, 'b': 0x00, 'c': 0x01, 'a': 0x81}]},
    ],
    'PrintCardSetListEntries': [
        {   'wram': {0xCE81: b'\x10\x08', 0xCE4C: b'\x00', 0xCE7C: b'\x00', 0xCE8B: b'\x00\x00'},
            'read': {0xCE7E: 0x01, 0xCE8B: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCE81: b'\x10\x08', 0xCE4C: b'\x00', 0xCE7C: b'\x00', 0xCE8B: b'\x00\x00'},
            'read': {0xCE7E: 0x01, 0xCE8B: 0x02}},
    ],
    'CreateCardSetList': [
        {   'a': 0x00,
            'wram': {   0xC000: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80'},
            'read': {0xCE8B: 0x3C, 0xD72C: 0x3C, 0xCE58: 0x01, 0xCFE4: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0x02,
            'wram': {   0xC000: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80'},
            'read': {0xCE8B: 0x3C, 0xD72C: 0x3C, 0xCE58: 0x01, 0xCFE4: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xC000: b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x80\x80\x80\x80'},
            'read': {0xCE8B: 0x3C, 0xD72C: 0x3C, 0xCE58: 0x01, 0xCFE4: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'HandleCardAlbumCardPage': [
        {'d': 0x00,
            'e': 0x00,
            'keys': 0x01,
            'wram': {0xCE4E: b'\x03', 0xCE4C: b'\x02', 0xCF6A: b'\x80', 0xFF8F: b'\x01'},
            'read': {0xCAC0: 0x01, 0xCE85: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'keys': 0x0f,
            'hl': 0x1234,
            'wram': {0xCE4E: b'\x05', 0xCE4C: b'\x00', 0xCF6A: b'\x80', 0xFF8F: b'\x0f'},
            'read': {0xCAC0: 0x01, 0xCE85: 0x01}},
        {   'd': 0xDD,
            'e': 0xEE,
            'keys': 0x08,
            'wram': {0xCE4E: b'\x00', 0xCE4C: b'\x00', 0xCF6A: b'\x80', 0xFF8F: b'\x08'},
            'read': {0xCAC0: 0x01, 0xCE85: 0x01}},
    ],
    'CreateCardSetListAndInitListCoords': [
        {   'a': 0x04,
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00'}},
            'read': {0xC000: 0xFF, 0xCE7C: 0x01, 0xCE81: 0x02, 0xCFBB: 0x02},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0x03,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'sram': {   0x00: {   0xA100: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00'}},
            'read': {0xC000: 0xFF, 0xCE7C: 0x01, 0xCE81: 0x02, 0xCFBB: 0x02},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
'CardAlbum': [
    {'completion': {'mode': 'entry', 'pc': 0x04CA, 'bank': 0x00, 'routine': 'DoFrame'},
     'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400},
    {'oracle': False,
     'why': 'CardAlbum enters the interactive indirect menu loop outside isolated oracle return.',
     'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    {'oracle': False,
     'why': 'CardAlbum depends on live menu dispatch and frame-driven input.'},
],
}

MUTATIONS = {
    'GetFirstOwnedCardIndex': {   'source_symbol': 'GetFirstOwnedCardIndex',
        'before': 'index++;',
        'after': '',
        'case_ids': [   'GetFirstOwnedCardIndex-2',
                        'GetFirstOwnedCardIndex-3',
                        'GetFirstOwnedCardIndex-4'],
        'source': 'src/profiles/extended/home/card_album.c'},
    'PrintCardSetListEntries': {   'source_symbol': 'PrintCardSetListEntries',
        'before': '\t\t\twUnableToScrollDown = (uint8_t)((low | high) == 0u);',
        'after': '\t\t\twUnableToScrollDown = (uint8_t)((low | high) != 0u);',
        'case_ids': ['PrintCardSetListEntries-0', 'PrintCardSetListEntries-1'],
        'source': 'src/profiles/extended/home/card_album.c'},
    'CreateCardSetList': {   'source_symbol': 'CreateCardSetList',
        'before': 'void CreateCardSetList(uint8_t a)\n{\n\tuint8_t set = a;',
        'after': 'void CreateCardSetList(uint8_t a)\n{\n\tuint8_t set = 0u;',
        'case_ids': ['CreateCardSetList-1'],
        'source': 'src/profiles/extended/home/card_album.c'},
    'HandleCardAlbumCardPage': {   'source_symbol': 'HandleCardAlbumCardPage',
        'before': 'wVBlankOAMCopyToggle = TRUE;\n'
                  '\ta = wCardListCursorPos;\n'
                  '\twTempCardListCursorPos = a;',
        'after': 'wVBlankOAMCopyToggle = FALSE;\n'
                 '\ta = wCardListCursorPos;\n'
                 '\twTempCardListCursorPos = (uint8_t)(a + 1u);',
        'case_ids': [   'HandleCardAlbumCardPage-0',
                        'HandleCardAlbumCardPage-1',
                        'HandleCardAlbumCardPage-2'],
        'source': 'src/profiles/extended/home/card_album.c'},
    'CreateCardSetListAndInitListCoords': {   'source_symbol': 'CreateCardSetListAndInitListCoords',
        'before': '\tgb_write8(wCardListCoords_ADDR, 0x04u);\n'
                  '\tgb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x02u);',
        'after': '\tgb_write8(wCardListCoords_ADDR, 0x03u);\n'
                 '\tgb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x02u);',
        'case_ids': [   'CreateCardSetListAndInitListCoords-0',
                        'CreateCardSetListAndInitListCoords-1'],
        'source': 'src/profiles/extended/home/card_album.c'},
    'CardAlbum': {   'source_symbol': 'CardAlbum',
        'before': '\t(void)DrawWideTextBox_PrintText(ViewWhichCardFileText);',
        'after': '\t(void)DrawWideTextBox_PrintText(EmptyPromotionalCardText);',
        'case_ids': ['CardAlbum-2', 'CardAlbum-0', 'CardAlbum-1'],
        'source': 'src/profiles/extended/home/card_album.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _name, _entries in CASES.items():
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
