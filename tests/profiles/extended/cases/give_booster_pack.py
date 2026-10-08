"""Extended oracle-diff cases for give_booster_pack: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym, sym_bank
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('give_booster_pack')
OWN = ('GiveBoosterPack',)
CONTRACT.update({
    'GiveBoosterPack': {'compare': (), 'preserve': ()},
})
CASES.update({
    'GiveBoosterPack': [
        {   'a': 0x00,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {sym("wLCDC"): b'\x00', sym("wAnotherBoosterPack"): b'\x00'},
            'read': {sym("wTxRam2"): 0x02, sym("wTxRam3"): 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x08,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {sym("wLCDC"): b'\x00', sym("wAnotherBoosterPack"): b'\x00'},
            'read': {sym("wTxRam2"): 0x02, sym("wTxRam3"): 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x17,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {sym("wLCDC"): b'\x00', sym("wAnotherBoosterPack"): b'\x01'},
            'read': {sym("wTxRam2"): 0x02, sym("wTxRam3"): 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x0E,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x02],
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {sym("wLCDC"): b'\x00', sym("wAnotherBoosterPack"): b'\x00'},
            'read': {sym("wTxRam2"): 0x02, sym("wTxRam3"): 0x02},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
    ],
})
MUTATIONS.update({
    'GiveBoosterPack': {   'source_symbol': 'GiveBoosterPack',
        'before': '\twTxRam3 = scene;\n\tgb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);',
        'after': '\twTxRam3 = (uint8_t)(scene + 1u);\n'
                 '\tgb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);',
        'case_ids': ['GiveBoosterPack-0', 'GiveBoosterPack-1', 'GiveBoosterPack-3'],
        'source': 'src/home/give_booster_pack.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
for _record in SCHEMA2_CASES["GiveBoosterPack"]:
    _record["completion"] = {"mode": "entry", "pc": sym("WaitForSongToFinish"), "bank": sym_bank("WaitForSongToFinish"),
                             "routine": "WaitForSongToFinish"}
