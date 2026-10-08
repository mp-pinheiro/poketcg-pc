"""Extended oracle-diff cases for card_color: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('card_color')
OWN = ('HandleEnergyBurn',)
CONTRACT.update({
    'HandleEnergyBurn': {'compare': (), 'preserve': ()},
})
CASES.update({
    'HandleEnergyBurn': [
        {'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCard"): b'\x00', sym("wBoosterCardsDrawn"): b'\x08\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hWhoseTurn"): b'\xc2', sym("wPlayerArenaCard"): b'\x02', sym("wBoosterCardsDrawn") + 4: b'2\x00', sym("wPlayerArenaCardStatus"): b'\x01'}},
        {   'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerArenaCard"): b'\x05',
                        sym("wBoosterCardsDrawn") + 0xA: b'2\x00',
                        sym("wPlayerArenaCardChangedType"): b'\x00',
                        sym("wPlayerArenaCardStatus"): b'\x00',
                        sym("wPlayerBench"): b'\xff',
                        sym("wOpponentArenaCard"): b'\xff',
                        sym("wOpponentBench"): b'\xff',
                        sym("wAttachedEnergies"): b'\x01\x02\x03\x04\x05\x06',
                        sym("wTotalAttachedEnergies"): b'\x07'},
            'read': {sym("wAttachedEnergies"): 0x06}},
        {   'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerArenaCard"): b'\x07',
                        sym("wBoosterCardsDrawn") + 0xE: b'2\x00',
                        sym("wPlayerArenaCardChangedType"): b'\x00',
                        sym("wPlayerArenaCardStatus"): b'\x00',
                        sym("wPlayerBench"): b'\xff',
                        sym("wOpponentArenaCard"): b'\xff',
                        sym("wOpponentBench"): b'\xff',
                        sym("wAttachedEnergies"): b'\x02\x03\x01\x00\x00\x00',
                        sym("wTotalAttachedEnergies"): b'\x06'},
            'read': {sym("wAttachedEnergies"): 0x06}},
        {   'wram': {   sym("hWhoseTurn"): b'\xc2',
                        sym("wPlayerArenaCard"): b'\x05',
                        sym("wBoosterCardsDrawn") + 0xA: b'2\x01',
                        sym("wPlayerArenaCardChangedType"): b'\x00',
                        sym("wPlayerArenaCardStatus"): b'\x00',
                        sym("wPlayerBench"): b'\xff',
                        sym("wOpponentArenaCard"): b'\xff',
                        sym("wOpponentBench"): b'\xff',
                        sym("wAttachedEnergies"): b'\x01\x02\x03\x04\x05\x06',
                        sym("wTotalAttachedEnergies"): b'\x07'},
            'read': {sym("wAttachedEnergies"): 0x06}},
    ],
})
MUTATIONS.update({
    'HandleEnergyBurn': {   'source_symbol': 'HandleEnergyBurn',
        'before': '\tif (card_id != CHARIZARD)',
        'after': '\tif (card_id == CHARIZARD)',
        'case_ids': ['HandleEnergyBurn-4'],
        'source': 'src/home/card_color.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
