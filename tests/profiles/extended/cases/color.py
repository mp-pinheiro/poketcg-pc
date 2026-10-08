"""Extended oracle-diff cases for color: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('color', remove=(
    'LoadConsolePaletteData',
    'SetWhitePalettes',
))
OWN = (
    'SetWhitePalettes',
)
CONTRACT.update({
    'SetWhitePalettes': {'compare': (), 'preserve': ()},
})
CASES.update({
    'SetWhitePalettes': [
        {   'wram': {   sym("wWriteBGMapToSRAM") + 1: b'\x00',
                        sym("wBGP"): b'\xe4',
                        sym("wOBP0"): b'\x1b',
                        sym("wOBP1"): b'\xb4',
                        sym("wBackgroundPalettesCGB"): b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        sym("wObjectPalettesCGB"): b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        sym("wTempBGP"): b'\x00',
                        sym("wTempOBP0"): b'U',
                        sym("wTempOBP1"): b'\xaa',
                        sym("wTempBackgroundPalettesCGB"): b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        sym("wTempObjectPalettesCGB"): b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {sym("wBGP"): 0x01, sym("wOBP0"): 0x01, sym("wOBP1"): 0x01, sym("wBackgroundPalettesCGB"): 0x40, sym("wObjectPalettesCGB"): 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   sym("wWriteBGMapToSRAM") + 1: b'\x1f',
                        sym("wBGP"): b'\xe4',
                        sym("wOBP0"): b'\x1b',
                        sym("wOBP1"): b'\xb4',
                        sym("wBackgroundPalettesCGB"): b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        sym("wObjectPalettesCGB"): b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        sym("wTempBGP"): b'\x00',
                        sym("wTempOBP0"): b'U',
                        sym("wTempOBP1"): b'\xaa',
                        sym("wTempBackgroundPalettesCGB"): b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        sym("wTempObjectPalettesCGB"): b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {sym("wBGP"): 0x01, sym("wOBP0"): 0x01, sym("wOBP1"): 0x01, sym("wBackgroundPalettesCGB"): 0x40, sym("wObjectPalettesCGB"): 0x40}},
    ],
})
MUTATIONS.update({
    'FadeScreenToWhite': {   'source_symbol': 'FadeScreenToWhite',
        'before': '\tif (gb_read8(wLCDC_ADDR) & 0x80u) {',
        'after': '\tif (gb_read8(wLCDC_ADDR) | 0x80u) {',
        'case_ids': ['FadeScreenToWhite-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'SetWhitePalettes': {   'source_symbol': 'SetWhitePalettes',
        'before': 'void SetWhitePalettes(void)\n'
                  '{\n'
                  '\tgb_write8(wBGP_ADDR, 0u);',
        'after': 'void SetWhitePalettes(void)\n'
                 '{\n'
                 '\tgb_write8(wBGP_ADDR, 1u);',
        'case_ids': ['SetWhitePalettes-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'Func_10d17': {   'source_symbol': 'Func_10d17',
        'before': '\twhite_cgb(wBackgroundPalettesCGB_ADDR, 64u);',
        'after': '\twhite_cgb(wBackgroundPalettesCGB_ADDR, 32u);',
        'case_ids': ['Func_10d17-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'Func_10d50': {   'source_symbol': 'Func_10d50',
        'before': '\twhite_cgb(wTempBackgroundPalettesCGB_ADDR, 64u);',
        'after': '\twhite_cgb(wTempBackgroundPalettesCGB_ADDR, 32u);',
        'case_ids': ['Func_10d50-0'],
        'source': 'src/profiles/extended/home/color.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
