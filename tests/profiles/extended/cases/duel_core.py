"""Extended oracle-diff cases for duel_core: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('duel_core', remove=('SetDefaultConsolePalettes',))
OWN = (
    'SetDefaultConsolePalettes',
)
CONTRACT.update({
    'SetDefaultConsolePalettes': {'compare': ('b',), 'preserve': ('b',)},
})
CASES.update({
    'SetDefaultConsolePalettes': [
        {   'wram': {   sym("wConsole"): b'\x00',
                        sym("wBGP"): b'\xff',
                        sym("wOBP0"): b'\xff',
                        sym("wFlushPaletteFlags"): b'\xff',
                        0xFF47: b'\xfc',
                        0xFF48: b'\xff',
                        0xFF49: b'\xff'},
            'read': {   sym("wBGP"): 0x01,
                        sym("wOBP0"): 0x01,
                        sym("wFlushPaletteFlags"): 0x01,
                        0xFF47: 0x01,
                        0xFF48: 0x01,
                        0xFF49: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wConsole"): b'\x00',
                        sym("wBGP"): b'\x11',
                        sym("wOBP0"): b'"',
                        sym("wFlushPaletteFlags"): b'3',
                        0xFF47: b'\xfc',
                        0xFF48: b'\xff',
                        0xFF49: b'\xff'},
            'read': {   sym("wBGP"): 0x01,
                        sym("wOBP0"): 0x01,
                        sym("wFlushPaletteFlags"): 0x01,
                        0xFF47: 0x01,
                        0xFF48: 0x01,
                        0xFF49: 0x01}},
        {   'wram': {   sym("wConsole"): b'\x01',
                        sym("wTextBoxFrameType"): b'\x00',
                        sym("wDecompSecondaryBufferPtrLow") + 1: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {sym("wTextBoxFrameType"): 0x01, sym("wDecompSecondaryBufferPtrLow") + 1: 0x10},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'b': 0x01,
            'wram': {   sym("wConsole"): b'\x02',
                        sym("hBankROM"): b'\x01',
                        sym("wBackgroundPalettesCGB"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wObjectPalettesCGB"): b'\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wTextBoxFrameType"): b'\x00',
                        sym("wFlushPaletteFlags"): b'\xff'},
            'read': {   sym("wBackgroundPalettesCGB"): 0x28,
                        sym("wObjectPalettesCGB"): 0x08,
                        sym("wTextBoxFrameType"): 0x01,
                        sym("wFlushPaletteFlags"): 0x01,
                        0xFF47: 0x01,
                        0xFF48: 0x01,
                        0xFF49: 0x01}},
    ],
})
MUTATIONS.update({
    'SetDefaultConsolePalettes': {   'source_symbol': 'SetDefaultConsolePalettes',
        'before': '\tgb_write8(wTextBoxFrameType_ADDR, 1u);',
        'after': '\tgb_write8(wTextBoxFrameType_ADDR, 0u);',
        'case_ids': ['SetDefaultConsolePalettes-2', 'SetDefaultConsolePalettes-3'],
        'source': 'src/profiles/extended/home/duel_core.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
