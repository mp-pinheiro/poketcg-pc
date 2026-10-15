"""Extended oracle-diff cases for card_album: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import VRAM_START, sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('card_album')
OWN = (
    'CardAlbum',
    'CreateCardSetList',
    'HandleCardAlbumCardPage',
    'PrintCardSetListEntries',
    'CreateCardSetListAndInitListCoords',
)
CONTRACT.update({
    'PrintCardSetListEntries': {'compare': ('hl',), 'preserve': ()},
    'CreateCardSetList': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleCardAlbumCardPage': {'compare': ('a', 'f'), 'preserve': ()},
    'CardAlbum': {'compare': (), 'preserve': ()},
})
CASES.update({
    'PrintCardSetListEntries': [
        {   'wram': {sym("wCardListCoords"): b'\x10\x08', sym("wCardListVisibleOffset"): b'\x00', sym("wNumVisibleCardListEntries"): b'\x00', sym("wHandTempList"): b'\x00\x00'},
            'read': {sym("wUnableToScrollDown"): 0x01, sym("wHandTempList"): 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wCardListCoords"): b'\x10\x08', sym("wCardListVisibleOffset"): b'\x00', sym("wNumVisibleCardListEntries"): b'\x00', sym("wHandTempList"): b'\x00\x00'},
            'read': {sym("wUnableToScrollDown"): 0x01, sym("wHandTempList"): 0x02}},
    ],
    'CreateCardSetList': [
        {   'a': 0x00,
            'wram': {   sym("wDeckToBuild"): b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
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
            'read': {sym("wHandTempList"): 0x3C, sym("wUniqueDeckCardList"): 0x3C, sym("wNumEntriesInCurFilter"): 0x01, sym("wOwnedPhantomCardFlags"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0x02,
            'wram': {   sym("wDeckToBuild"): b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
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
            'read': {sym("wHandTempList"): 0x3C, sym("wUniqueDeckCardList"): 0x3C, sym("wNumEntriesInCurFilter"): 0x01, sym("wOwnedPhantomCardFlags"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wDeckToBuild"): b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
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
            'read': {sym("wHandTempList"): 0x3C, sym("wUniqueDeckCardList"): 0x3C, sym("wNumEntriesInCurFilter"): 0x01, sym("wOwnedPhantomCardFlags"): 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'HandleCardAlbumCardPage': [
        {'d': 0x00,
            'e': 0x00,
            'keys': 0x01,
            'wram': {sym("wCardListCursorPos"): b'\x03', sym("wCardListVisibleOffset"): b'\x02', sym("wCurDeckCardsEnd"): b'\x80', sym("hDPadHeld"): b'\x01'},
            'read': {sym("wVBlankOAMCopyToggle"): 0x01, sym("wTempCardListCursorPos"): 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'keys': 0x0f,
            'hl': 0x1234,
            'wram': {sym("wCardListCursorPos"): b'\x05', sym("wCardListVisibleOffset"): b'\x00', sym("wCurDeckCardsEnd"): b'\x80', sym("hDPadHeld"): b'\x0f'},
            'read': {sym("wVBlankOAMCopyToggle"): 0x01, sym("wTempCardListCursorPos"): 0x01}},
        {   'd': 0xDD,
            'e': 0xEE,
            'keys': 0x08,
            'wram': {sym("wCardListCursorPos"): b'\x00', sym("wCardListVisibleOffset"): b'\x00', sym("wCurDeckCardsEnd"): b'\x80', sym("hDPadHeld"): b'\x08'},
            'read': {sym("wVBlankOAMCopyToggle"): 0x01, sym("wTempCardListCursorPos"): 0x01}},
    ],
    'CardAlbum': [
    {'completion': {'mode': 'entry', 'pc': sym("DoFrame"), 'bank': sym_bank("DoFrame"), 'routine': 'DoFrame'},
     'instruction_budget': 0x1312D00, 'cycle_budget': 0x4C4B400},
    {'oracle': False,
     'why': 'CardAlbum enters the interactive indirect menu loop outside isolated oracle return.',
     'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    {'oracle': False,
     'why': 'CardAlbum depends on live menu dispatch and frame-driven input.'},
],
})
MUTATIONS.update({
    'PrintCardSetListEntries': {   'source_symbol': 'PrintCardSetListEntries',
        'before': '\t\t\twUnableToScrollDown = (uint8_t)((low | high) == 0u);',
        'after': '\t\t\twUnableToScrollDown = (uint8_t)((low | high) != 0u);',
        'case_ids': ['PrintCardSetListEntries-0', 'PrintCardSetListEntries-1'],
        'source': 'src/profiles/extended/home/card_album.c'},
    'CreateCardSetList': {'source_symbol': 'CreateCardSetList', 'before': '\twOwnedPhantomCardFlags = 0u;', 'after': '\twOwnedPhantomCardFlags = (uint8_t)((0u) ^ 1u);', 'case_ids': ['CreateCardSetList-0'], 'source': 'src/profiles/extended/home/card_album.c'},
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
        'source': 'src/home/card_album.c'},
    'CardAlbum': {'source_symbol': 'CardAlbum', 'before': '{\n\twTileMapFill = 0u;', 'after': '{\n\twTileMapFill = (uint8_t)((0u) ^ 1u);', 'case_ids': ['CardAlbum-0'], 'source': 'src/home/card_album.c'},
})
CASES['CreateCardSetListAndInitListCoords'] = [
    *CASES['CreateCardSetListAndInitListCoords'],
    {'a': 0,
     'sram': {0: {sym("sCardCollection") + 0xFF: b'\x05',
                  sym("sCardCollection") + 0x1FD: b'\x07'}},
     'wram': {sym("wTempCardCollection") + 0xFF: bytes(0xFF)},
     'read': {sym("wTempCardCollection") + 0xFF: 0xFF},
     'instruction_budget': 2000000, 'cycle_budget': 8000000},
]
CASES['HandleCardAlbumCardPage'] = [
    *CASES['HandleCardAlbumCardPage'],
    {'wram': {sym("wCardListCursorPos"): b'\x01', sym("wCardListVisibleOffset"): b'\x00',
              sym("wOwnedCardsCountList") + 1: b'\x01',
              sym("wCurCardListPtr"): sym("wFilteredCardList").to_bytes(2, 'little'),
              sym("wFilteredCardList"): b'\x08\x00\x09\x00\x00\x00'},
     'read': {sym("wLoadedCard1ID"): 2},
     'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
     'keys': [0, 2, 0, 2],
     'instruction_budget': 20000000, 'cycle_budget': 80000000},
]
CASES['CardAlbum'] = [
    *CASES['CardAlbum'],
    {'wram': {sym("wConsole"): b'\x02', sym("wLCDC"): b'\x00',
              sym("hCurMenuItem"): b'\x00'},
     'sram': {0: {sym("sCardCollection"): b'\x00' + b'\x01' * 228}},
     'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
     'keys': [0, 1],
     'read': {sym("wNumCardListEntries"): 1, sym("wNumEntriesInCurFilter"): 1},
     'completion': {'mode': 'entry', 'pc': sym("HandleCardAlbumCardPage"),
                    'bank': sym_bank("HandleCardAlbumCardPage"), 'routine': 'HandleCardAlbumCardPage'},
     'instruction_budget': 20000000, 'cycle_budget': 80000000},
]
MUTATIONS['CreateCardSetListAndInitListCoords'] = {
    'source': 'src/home/card_album.c',
    'source_symbol': 'CreateCardSetListAndInitListCoords',
    'before': 'CopyNBytesFromHLToDE_Long(&hl, &de, (uint16_t)(CARD_COLLECTION_SIZE - 2u));',
    'after': 'CopyNBytesFromHLToDE(&hl, &de, (uint8_t)(CARD_COLLECTION_SIZE - 1u));',
    'case_ids': ['CreateCardSetListAndInitListCoords-3'],
}
MUTATIONS['CardAlbum'] = {
    'source': 'src/home/card_album.c',
    'source_symbol': 'CardAlbum',
    'before': 'for (uint16_t hl = wFilteredCardList_ADDR;; hl = (uint16_t)(hl + sizeof(CardId))) {\n'
              '\t\tif (card_id_read_at(hl) == 0u)\n\t\t\tbreak;\n\t\tcount++;\n\t}',
    'after': 'for (uint16_t hl = wFilteredCardList_ADDR; gb_read8(hl) != 0u; hl++)\n\t\tcount++;',
    'case_ids': ['CardAlbum-3'],
}
MUTATIONS['HandleCardAlbumCardPage'] = {
    'source': 'src/home/card_album.c',
    'source_symbol': 'HandleCardAlbumCardPage',
    'before': 'hl = (uint16_t)(hl + (uint16_t)c * sizeof(CardId));\n'
              '\t\t\tCardId card_id = card_id_read_at(hl);',
    'after': 'hl = (uint16_t)(hl + c);\n\t\t\tCardId card_id = card_id_read_at(hl);',
    'case_ids': ['HandleCardAlbumCardPage-3'],
}


from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _name, _entries in ((_fn, CASES[_fn]) for _fn in OWN):
    for _index, _entry in enumerate(_entries):
        if "completion" in _entry:
            SCHEMA2_CASES[_name][_index]["completion"] = _entry["completion"]
SCHEMA2_CASES["CardAlbum"][0].setdefault("bus", {}).update({VRAM_START: 0x2000})
