"""Extended oracle-diff cases for commands: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('commands')
OWN = (
    'PrintDamageText',
)
CONTRACT.update({
    'PrintDamageText': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
})
CASES.update({
    'PrintDamageText': [
        {   'hl': sym("wDecompressionSecondaryBufferStart") + 0x11,
            'wram': {   sym("wLoadedAttackAnimation"): b'\x00',
                        sym("wTempNonTurnDuelistCardID"): b'\x08',
                        sym("wDamageAnimAmount"): b'\x01\x00',
                        sym("wDoFrameFunction"): b'"\x03',
                        sym("wTxRam2"): b'\xaaU'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {sym("wTxRam2"): 0x02},
            'instruction_budget': 0xF4240,
            'cycle_budget': 0x3D0900},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wLoadedAttackAnimation"): b'\x00',
                        sym("wTempNonTurnDuelistCardID"): b'\x08',
                        sym("wDamageAnimAmount"): b'\x01\x00',
                        sym("wDoFrameFunction"): b'"\x03',
                        sym("wTxRam2"): b'\x124'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {sym("wTxRam2"): 0x02},
            'instruction_budget': 0xF4240,
            'cycle_budget': 0x3D0900},
        {   'b': 0x01,
            'c': 0x02,
            'd': 0x03,
            'e': 0x04,
            'hl': sym("wDecompressionSecondaryBufferStart") + 0x12,
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'read': {sym("wTxRam2"): 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'read': {sym("wTxRam2"): 0x02}},
    ],
})
MUTATIONS.update({
    'PrintDamageText': {   'source_symbol': 'PrintDamageText',
        'before': '\tgb_write8(wTxRam2_ADDR, 0u);',
        'after': '\tgb_write8(wTxRam2_ADDR, 1u);',
        'case_ids': ['PrintDamageText-0', 'PrintDamageText-1'],
        'source': 'src/profiles/extended/home/commands.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
