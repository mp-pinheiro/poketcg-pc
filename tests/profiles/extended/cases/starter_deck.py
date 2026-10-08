"""Extended oracle-diff cases for starter_deck: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('starter_deck', remove=(
    'CopyDeckNameAndCards',
    'InitSaveData',
))
OWN = (
    'InitSaveData',
)
CONTRACT.update({
    'InitSaveData': {'compare': (), 'preserve': ()},
})
CASES.update({
    'InitSaveData': [
        {   'wram': {sym("hWhoseTurn"): b'\xff'},
            'sram': {   0x00: {   sym("sCardAndDeckSaveData"): b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
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
                                  sym("sChallengeMachineEnd") + 0x197: b'\xaa\xbb\xcc',
                                  sym("sChallengeMachineEnd") + 0x97: b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""""""""""""""""""""""""""'
                                          b'""""""""""""""""""""""""""""""""',
                                  sym("s0a000") + 3: b'\xff',
                                  sym("sTextSpeed"): b'\xff',
                                  sym("sAnimationsDisabled"): b'\xff',
                                  sym("sSkipDelayAllowed"): b'\xff',
                                  sym("s0a004"): b'\xff',
                                  sym("s0a004") + 1: b'\xff',
                                  sym("sReceivedLegendaryCards"): b'\xff'}},
            'read': {sym("hWhoseTurn"): 0x01, sym("wTextSpeed"): 0x01},
            'sread': {   0x00: {   sym("sCardAndDeckSaveData"): 0x0100,
                                   sym("sSavedDeck1"): 0x20,
                                   sym("sSavedDeck2"): 0x20,
                                   sym("sSavedDeck3"): 0x20,
                                   sym("sChallengeMachineEnd") + 0x197: 0x03,
                                   sym("sChallengeMachineEnd") + 0x97: 0x0100,
                                   sym("s0a000") + 3: 0x01,
                                   sym("sTextSpeed"): 0x01,
                                   sym("sAnimationsDisabled"): 0x01,
                                   sym("sSkipDelayAllowed"): 0x01,
                                   sym("s0a004"): 0x01,
                                   sym("s0a004") + 1: 0x01,
                                   sym("sReceivedLegendaryCards"): 0x01}},
            'vread': {0x00: {0x9380: 0x20}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hWhoseTurn"): b'\xff'},
            'sram': {   0x00: {   sym("sCardAndDeckSaveData"): b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333333333333333333333333333'
                                          b'33333333333333333333333333333333',
                                  sym("sChallengeMachineEnd") + 0x197: b'\x11"3',
                                  sym("sChallengeMachineEnd") + 0x97: b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                                          b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'}},
            'read': {sym("hWhoseTurn"): 0x01, sym("wTextSpeed"): 0x01},
            'sread': {   0x00: {   sym("sCardAndDeckSaveData"): 0x0100,
                                   sym("sSavedDeck1"): 0x20,
                                   sym("sSavedDeck2"): 0x20,
                                   sym("sSavedDeck3"): 0x20,
                                   sym("sChallengeMachineEnd") + 0x197: 0x03,
                                   sym("sChallengeMachineEnd") + 0x97: 0x0100,
                                   sym("s0a000") + 3: 0x01,
                                   sym("sTextSpeed"): 0x01,
                                   sym("sAnimationsDisabled"): 0x01,
                                   sym("sSkipDelayAllowed"): 0x01,
                                   sym("s0a004"): 0x01,
                                   sym("s0a004") + 1: 0x01,
                                   sym("sReceivedLegendaryCards"): 0x01}},
            'vread': {0x00: {0x9380: 0x20}}},
    ],
})
MUTATIONS.update({
    'InitSaveData': {   'source_symbol': 'InitSaveData',
        'before': '\tgb_write8(sTextSpeed_ADDR, TEXT_SPEED_3);',
        'after': '\tgb_write8(sTextSpeed_ADDR, 3u);',
        'case_ids': ['InitSaveData-0', 'InitSaveData-1'],
        'source': 'src/profiles/extended/home/starter_deck.c'},
    '_AddStarterDeck': {'source_symbol': '_AddStarterDeck', 'before': 'gb_write8(slot, (uint8_t)(value + 1u));', 'after': 'gb_write8(slot, value);', 'case_ids': ['_AddStarterDeck-0', '_AddStarterDeck-1'], 'source': 'src/profiles/extended/home/starter_deck.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
