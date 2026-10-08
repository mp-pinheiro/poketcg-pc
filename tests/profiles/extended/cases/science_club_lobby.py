"""Extended oracle-diff cases for science_club_lobby: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('science_club_lobby')
OWN = ('Script_Specs2',)
CONTRACT.update({
    'Script_Specs2': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
})
CASES.update({
    'Script_Specs2': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {sym("wTxRam2"): b'\xff\xff\xff', sym("wRNG1"): b'\x00@\x01'},
            'read': {sym("wTxRam2"): 0x03, sym("wRNG1"): 0x03}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {sym("wTxRam2"): b'\xff\xff\xff', sym("wRNG1"): b'\x00\x00\x00'},
            'read': {sym("wTxRam2"): 0x03, sym("wRNG1"): 0x03}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {sym("wTxRam2"): b'\xff\xff\xff', sym("wRNG1"): b'\x00@\x00'},
            'read': {sym("wTxRam2"): 0x03, sym("wRNG1"): 0x03}},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'wram': {sym("wTxRam2"): b'\xff\xff\xff', sym("wRNG1"): b'\x00\x00\x01'},
            'read': {sym("wTxRam2"): 0x03, sym("wRNG1"): 0x03}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("wTxRam2"): b'\xff\xff\xff', sym("wRNG1"): b'\x00@\x01'},
            'read': {sym("wTxRam2"): 0x03, sym("wRNG1"): 0x03}},
    ],
})
MUTATIONS.update({
    'Script_Specs2': {   'source_symbol': 'Script_Specs2',
        'before': '\tuint16_t hl = (uint16_t)(DATA_EBE7 + c);',
        'after': '\tuint16_t hl = (uint16_t)(DATA_EBE7 + c + 2u);',
        'case_ids': ['Script_Specs2-0', 'Script_Specs2-2', 'Script_Specs2-3', 'Script_Specs2-4'],
        'source': 'src/profiles/extended/home/science_club_lobby.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _record in SCHEMA2_CASES["Script_Specs2"]:
    _record["completion"] = {"mode": "pre-ret", "pc": sym("Script_Specs2") + 0x18, "bank": sym_bank("Script_Specs2")}
