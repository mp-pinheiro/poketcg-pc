"""Extended oracle-diff cases for color, seeded from tests/cases/color.py."""

CONTRACT = {
    'FadeScreenToWhite': {'compare': (), 'preserve': ()},
    'FadeScreenFromWhite.BackupPalsAndSetWhite': {'compare': (), 'preserve': ()},
    'SetWhitePalettes': {'compare': (), 'preserve': ()},
    'Func_10d17': {'compare': (), 'preserve': ()},
    'Func_10d50': {'compare': (), 'preserve': ()},
    'FadeScreenFromWhite': {'compare': ('a',), 'preserve': ()},
    'FadeScreenToTempPals': {'compare': ('a',), 'preserve': ()},
    'RestoreFirstColorInOBPals': {'compare': ('b',), 'preserve': ('b',)},
    'FadeDMGPalettes': {'compare': ('b', 'c'), 'preserve': ('b', 'c')},
    'FadeDMGPalettes.CalculateMixPalette': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'FadeDMGPalettes.GetMixShadeValue': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'FadeOBPalIntoTemp': {'compare': ('b', 'c'), 'preserve': ('b', 'c')},
    'FadeBGPalIntoTemp1': {'compare': ('b', 'c'), 'preserve': ('b', 'c')},
    'FadeBGPalIntoTemp2': {'compare': ('b', 'c'), 'preserve': ('b', 'c')},
    'FadeBGPalIntoTemp3': {'compare': ('b', 'c'), 'preserve': ('b', 'c')},
    'FadePalIntoAnother.GetFadedColor': {'compare': ('a', 'c', 'd', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'FadePalIntoAnother.FadeColor': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'FlashScreenToWhite': {'compare': ('f',), 'preserve': ()},
    'CopyPalsToSRAMBuffer': {'compare': ('f',), 'preserve': ()},
    'LoadPalsFromSRAMBuffer': {'compare': ('f',), 'preserve': ()},
    'Func_10d74': {'compare': ('b',), 'preserve': ('b',)},
}

CASES = {
    'FadeScreenToWhite': [
        {   'wram': {   0xCABB: b'\x00',
                        0xCAB4: b'\x02',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCABC: 0x01, 0xCABD: 0x01, 0xCABE: 0x01, 0xCAF0: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABB: b'\x00',
                        0xCAB4: b'\x1f',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCABC: 0x01, 0xCABD: 0x01, 0xCABE: 0x01, 0xCAF0: 0x40}},
    ],
    'FadeScreenFromWhite.BackupPalsAndSetWhite': [
        {   'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD281: 0x01, 0xD282: 0x01, 0xD283: 0x01, 0xD284: 0x80, 0xCABC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD281: 0x01, 0xD282: 0x01, 0xD283: 0x01, 0xD284: 0x80, 0xCABC: 0x01}},
    ],
    'SetWhitePalettes': [
        {   'wram': {   0xD280: b'\x00',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCABC: 0x01, 0xCABD: 0x01, 0xCABE: 0x01, 0xCAF0: 0x40, 0xCB30: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD280: b'\x1f',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCABC: 0x01, 0xCABD: 0x01, 0xCABE: 0x01, 0xCAF0: 0x40, 0xCB30: 0x40}},
    ],
    'Func_10d17': [
        {   'wram': {   0xCAB4: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD281: 0x01, 0xD284: 0x80, 0xCABC: 0x01, 0xD304: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB4: b'\x1c',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD281: 0x01, 0xD284: 0x80, 0xCABC: 0x01, 0xD304: 0x01}},
    ],
    'Func_10d50': [
        {   'wram': {   0xCAB4: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD281: 0x01, 0xD282: 0x01, 0xD283: 0x01, 0xD284: 0x80, 0xD304: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCAB4: b'\x1c',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD281: 0x01, 0xD282: 0x01, 0xD283: 0x01, 0xD284: 0x80, 0xD304: 0x01}},
    ],
    'FadeScreenFromWhite': [
        {   'wram': {0xCABB: b'\x00', 0xCAB8: b'\xfe'},
            'instruction_budget': 0xF4240,
            'cycle_budget': 0x3D0900,
            'read': {   0xCABB: 0x01,
                        0xFF40: 0x01,
                        0xCAB8: 0x01,
                        0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCAF0: 0x40,
                        0xCB30: 0x40,
                        0xD281: 0x01,
                        0xD282: 0x01,
                        0xD283: 0x01,
                        0xD284: 0x40,
                        0xD2C4: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCABB: b'\x00', 0xCAB8: b'\xfe'},
            'instruction_budget': 0xF4240,
            'cycle_budget': 0x3D0900,
            'read': {   0xCABB: 0x01,
                        0xFF40: 0x01,
                        0xCAB8: 0x01,
                        0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCAF0: 0x40,
                        0xCB30: 0x40,
                        0xD281: 0x01,
                        0xD282: 0x01,
                        0xD283: 0x01,
                        0xD284: 0x40,
                        0xD2C4: 0x40}},
    ],
    'FadeScreenToTempPals': [
        {   'wram': {   0xCABB: b'\x00',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCABC: 0x03, 0xCAF0: 0x40, 0xCB30: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABB: b'\x00',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCABC: 0x03, 0xCAF0: 0x40, 0xCB30: 0x40}},
        {   'wram': {   0xCABB: b'\x80',
                        0xFF40: b'\x80',
                        0xCAB8: b'\xfe',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
                        0xCB30: b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'
                                b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'
                                b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'
                                b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
                        0xD2C4: b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'
                                b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'
                                b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'
                                b'\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18'},
            'instruction_budget': 0xF4240,
            'cycle_budget': 0x3D0900,
            'read': {   0xCAB8: 0x01,
                        0xCABB: 0x01,
                        0xFF40: 0x01,
                        0xCAF0: 0x40,
                        0xD284: 0x40,
                        0xCB30: 0x40,
                        0xD2C4: 0x40}},
    ],
    'RestoreFirstColorInOBPals': [
        {   'wram': {   0xCB30: b'\x10\x11 !01@A\x10\x11 !01@A\x10\x11 !01@A\x10\x11 !01@A\x10\x11 !'
                                b'01@A\x10\x11 !01@A\x10\x11 !01@A\x10\x11 !01@A',
                        0xD2C4: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f'},
            'read': {0xCB30: 0x10}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCB30: b'\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11'
                                b'\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11'
                                b'\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11'
                                b'\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11\x10\x11',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'
                                b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00'},
            'read': {0xCB30: 0x10}},
    ],
    'FadeDMGPalettes': [
        {   'wram': {   0xCABC: b'\x00',
                        0xCABD: b'U',
                        0xCABE: b'\xaa',
                        0xD281: b'\xff',
                        0xD282: b'\x00',
                        0xD283: b'U'},
            'read': {0xCABC: 0x03}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xD281: b'\x1b',
                        0xD282: b'\xb4',
                        0xD283: b'\xe4'},
            'read': {0xCABC: 0x03}},
    ],
    'FadeDMGPalettes.CalculateMixPalette': [
        {'b': 0x00, 'c': 0x00},
        {'b': 0xFF, 'c': 0xFF},
        {'b': 0xE4, 'c': 0x1B},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xE4, 'c': 0x1B, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'FadeDMGPalettes.GetMixShadeValue': [
        {'b': 0x00, 'c': 0x00},
        {'b': 0x00, 'c': 0x01},
        {'b': 0x00, 'c': 0x02},
        {'b': 0x00, 'c': 0x03},
        {'b': 0x01, 'c': 0x00},
        {'b': 0x01, 'c': 0x01},
        {'b': 0x01, 'c': 0x02},
        {'b': 0x01, 'c': 0x03},
        {'b': 0x02, 'c': 0x00},
        {'b': 0x02, 'c': 0x01},
        {'b': 0x02, 'c': 0x02},
        {'b': 0x02, 'c': 0x03},
        {'b': 0x03, 'c': 0x00},
        {'b': 0x03, 'c': 0x01},
        {'b': 0x03, 'c': 0x02},
        {'b': 0x03, 'c': 0x03},
        {'a': 0xAA, 'f': 0xF0, 'b': 0x03, 'c': 0x03, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'FadeOBPalIntoTemp': [
        {   'wram': {   0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCB30: 0x40, 0xD2C4: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCB30: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@',
                        0xD2C4: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'},
            'read': {0xCB30: 0x40, 0xD2C4: 0x40}},
    ],
    'FadeBGPalIntoTemp1': [
        {   'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCAF0: 0x20, 0xD284: 0x20}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCAF0: 0x20, 0xD284: 0x20}},
    ],
    'FadeBGPalIntoTemp2': [
        {   'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCAF0: 0x40, 0xD284: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCAF0: 0x40, 0xD284: 0x40}},
    ],
    'FadeBGPalIntoTemp3': [
        {   'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCAF0: 0x40, 0xD284: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xCAF0: 0x40, 0xD284: 0x40}},
    ],
    'FadePalIntoAnother.GetFadedColor': [
        {'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0x00, 'read': {0xFFB6: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x1234,
            'read': {0xFFB6: 0x02}},
        {'b': 0x7C, 'c': 0x1F, 'd': 0x7C, 'e': 0x1F, 'read': {0xFFB6: 0x02}},
        {'b': 0x00, 'c': 0x00, 'd': 0x7C, 'e': 0xFF, 'read': {0xFFB6: 0x02}},
        {'b': 0x04, 'c': 0x21, 'd': 0x08, 'e': 0xA5, 'read': {0xFFB6: 0x02}},
    ],
    'FadePalIntoAnother.FadeColor': [
        {'a': 0x00, 'hl': 0x00},
        {'a': 0x1F, 'hl': 0x00},
        {'a': 0x00, 'hl': 0x1F},
        {'a': 0x01, 'hl': 0x05},
        {'a': 0x04, 'hl': 0x00},
        {'a': 0x00, 'hl': 0x04},
        {'a': 0x1F, 'hl': 0x1B},
        {'a': 0x00, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1F},
    ],
    'FlashScreenToWhite': [
        {   'c': 0x01,
            'wram': {   0xCABB: b'\x00',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'read': {0xCABB: 0x01, 0xCAF0: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0x01,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCABB: b'\x00',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'read': {0xCABB: 0x01, 0xCAF0: 0x40}},
        {   'c': 0x00,
            'wram': {   0xCABB: b'\x00',
                        0xFF40: b'\x00',
                        0xCAB8: b'\xfe',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'oracle': False,
            'why': 'Fade-in reaches dissolved VBlank context',
            'expect': {   0xCABB: b'\x80',
                          0xFF40: b'\x80',
                          0xCAB8: b'\x06',
                          0xCABC: b'\xe4',
                          0xCABD: b'\x1b',
                          0xCABE: b'\xb4',
                          0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                  b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
                                  b' !"#$%&\'()*+,-./0123456789:;<=>?',
                          0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{'
                                  b'|}~\x7f',
                          0xD281: b'\xe4',
                          0xD282: b'\x1b',
                          0xD283: b'\xb4',
                          0xD284: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                  b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
                                  b' !"#$%&\'()*+,-./0123456789:;<=>?',
                          0xD2C4: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{'
                                  b'|}~\x7f',
                          0xA000: b'\xff'},
            'read': {   0xCABB: 0x01,
                        0xFF40: 0x01,
                        0xCAB8: 0x01,
                        0xCABC: 0x01,
                        0xCABD: 0x01,
                        0xCABE: 0x01,
                        0xCAF0: 0x40,
                        0xCB30: 0x40,
                        0xD281: 0x01,
                        0xD282: 0x01,
                        0xD283: 0x01,
                        0xD284: 0x40,
                        0xD2C4: 0x40,
                        0xA000: 0x01}},
    ],
    'CopyPalsToSRAMBuffer': [
        {   'wram': {   0xFF81: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'sram': {   0x01: {   0xA800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
            'oracle': False,
            'why': 'The 131-byte bank-1 palette save is outside ordinary oracle readback',
            'expect': {0xFF81: b'\x03', 0xA000: b'\xff'},
            'expect_sram': {   0x01: {   0xA800: b'\xe4\x1b\xb4\x00\x01\x02\x03\x04\x05\x06\x07\x08'
                                                 b'\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14'
                                                 b'\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$'
                                                 b"%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWX"
                                                 b'YZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'}},
            'read': {0xFF81: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF81: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'sram': {   0x01: {   0xA800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {0xFF81: 0x01}},
    ],
    'LoadPalsFromSRAMBuffer': [
        {   'wram': {   0xFF81: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'sram': {   0x01: {   0xA800: b'\xe4\x1b\xb4\x00\x01\x02\x03\x04\x05\x06\x07\x08'
                                          b'\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18'
                                          b'\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<'
                                          b'=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrst'
                                          b'uvwxyz{|}~\x7f'}},
            'expect': {0xCABC: b'\xe4', 0xCABD: b'\x1b', 0xCABE: b'\xb4'},
            'sread': {0x01: {0xA000: 0x01}},
            'read': {0xCABC: 0x01, 0xCABD: 0x01, 0xCABE: 0x01, 0xCAF0: 0x80, 0xFF81: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF81: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'ramg': False,
            'sram': {   0x01: {   0xA800: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONML'
                                          b'KJIHGFEDCBA@?>=<;:9876543210/.-,+*)(\'&%$#"! '
                                          b'\x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x17\x16\x15\x14'
                                          b'\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x04'
                                          b'\x03\x02\x01\x00\xb4\x1b\xe4'}},
            'sread': {0x01: {0xA000: 0x01}},
            'read': {0xCABC: 0x01, 0xCAF0: 0x80, 0xFF81: 0x01}},
    ],
    'Func_10d74': [
        {   'b': 0x00,
            'wram': {   0xD304: b'\x00',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD304: 0x01, 0xCAF0: 0x40}},
        {   'b': 0x01,
            'wram': {   0xD304: b'\x01',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD304: 0x01, 0xCAF0: 0x20}},
        {   'b': 0x02,
            'wram': {   0xD304: b'\x02',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD304: 0x01, 0xCAF0: 0x20}},
        {   'b': 0x03,
            'wram': {   0xD304: b'\x03',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD304: 0x01, 0xCAF0: 0x40}},
        {   'b': 0x04,
            'wram': {   0xD304: b'\x04',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD304: 0x01, 0xCAF0: 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x04,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD304: b'\x04',
                        0xCABC: b'\xe4',
                        0xCABD: b'\x1b',
                        0xCABE: b'\xb4',
                        0xCAF0: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?",
                        0xCB30: b'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                        0xD281: b'\x00',
                        0xD282: b'U',
                        0xD283: b'\xaa',
                        0xD284: b'?>=<;:9876543210/.-,+*)(\'&%$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18'
                                b'\x17\x16\x15\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08'
                                b'\x07\x06\x05\x04\x03\x02\x01\x00',
                        0xD2C4: b'\x7f~}|{zyxwvutsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@'},
            'read': {0xD304: 0x01, 0xCAF0: 0x40}},
    ],
}

MUTATIONS = {
    'FadeScreenToWhite': {   'source_symbol': 'FadeScreenToWhite',
        'before': '\tif (gb_read8(wLCDC_ADDR) & 0x80u) {',
        'after': '\tif (gb_read8(wLCDC_ADDR) | 0x80u) {',
        'case_ids': ['FadeScreenToWhite-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeScreenFromWhite.BackupPalsAndSetWhite': {   'source_symbol': 'FadeScreenFromWhite.BackupPalsAndSetWhite',
        'before': '    SetWhitePalettes();',
        'after': '    ;',
        'case_ids': ['FadeScreenFromWhite.BackupPalsAndSetWhite-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'SetWhitePalettes': {   'source_symbol': 'SetWhitePalettes',
        'before': '\tgb_write8(wBGP_ADDR, 0u);',
        'after': '\tgb_write8(wBGP_ADDR, 1u);',
        'case_ids': ['SetWhitePalettes-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'Func_10d17': {   'source_symbol': 'Func_10d17',
        'before': '\tgb_write8(wBGP_ADDR, 0u);',
        'after': '\tgb_write8(wBGP_ADDR, 1u);',
        'case_ids': ['Func_10d17-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'Func_10d50': {   'source_symbol': 'Func_10d50',
        'before': '\twhite_cgb(wTempBackgroundPalettesCGB_ADDR, 32u);',
        'after': '\twhite_cgb(wTempBackgroundPalettesCGB_ADDR, 64u);',
        'case_ids': ['Func_10d50-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeScreenFromWhite': {   'source_symbol': 'FadeScreenFromWhite',
        'before': '    FlushAllPalettes();\n    EnableLCD();',
        'after': '    FlushAllPalettes();\n    ;',
        'case_ids': ['FadeScreenFromWhite-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeScreenToTempPals': {   'source_symbol': 'FadeScreenToTempPals',
        'before': '    for (uint8_t count = 0x10; count != 0; count = (uint8_t)(count - 2)) {',
        'after': '    for (uint8_t count = 0x10; count != 0; count = (uint8_t)(count + 2)) {',
        'case_ids': ['FadeScreenToTempPals-2'],
        'source': 'src/profiles/extended/home/color.c'},
    'RestoreFirstColorInOBPals': {   'source_symbol': 'RestoreFirstColorInOBPals',
        'before': '        uint16_t source = (uint16_t)(wTempObjectPalettesCGB_ADDR + palette * '
                  '8);',
        'after': '        uint16_t source = (uint16_t)(wTempObjectPalettesCGB_ADDR - palette * 8);',
        'case_ids': ['RestoreFirstColorInOBPals-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeDMGPalettes': {   'source_symbol': 'FadeDMGPalettes',
        'before': '        gb_write8(current, '
                  'FadeDMGPalettes_CalculateMixPalette(gb_read8(current), gb_read8(target)));',
        'after': '        ;',
        'case_ids': ['FadeDMGPalettes-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeDMGPalettes.CalculateMixPalette': {   'source_symbol': 'FadeDMGPalettes.CalculateMixPalette',
        'before': '        uint8_t combined = (uint8_t)(shade | output);',
        'after': '        uint8_t combined = (uint8_t)(shade & output);',
        'case_ids': ['FadeDMGPalettes.CalculateMixPalette-1'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeDMGPalettes.GetMixShadeValue': {   'source_symbol': 'FadeDMGPalettes.GetMixShadeValue',
        'before': '    return mix_shades[((b & 3) << 2) | (c & 3)];',
        'after': '    return mix_shades[((b | 3) << 2) | (c & 3)];',
        'case_ids': ['FadeDMGPalettes.GetMixShadeValue-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeOBPalIntoTemp': {   'source_symbol': 'FadeOBPalIntoTemp',
        'before': '    fade_palette_bytes(wObjectPalettesCGB_ADDR, wTempObjectPalettesCGB_ADDR, '
                  '32);',
        'after': '    ;',
        'case_ids': ['FadeOBPalIntoTemp-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeBGPalIntoTemp1': {   'source_symbol': 'FadeBGPalIntoTemp1',
        'before': '    fade_palette_bytes(wBackgroundPalettesCGB_ADDR, '
                  'wTempBackgroundPalettesCGB_ADDR, 16);',
        'after': '    ;',
        'case_ids': ['FadeBGPalIntoTemp1-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeBGPalIntoTemp2': {   'source_symbol': 'FadeBGPalIntoTemp2',
        'before': '    fade_palette_bytes((uint16_t)(wBackgroundPalettesCGB_ADDR + 32), '
                  '(uint16_t)(wTempBackgroundPalettesCGB_ADDR + 32), 16);',
        'after': '    fade_palette_bytes((uint16_t)(wBackgroundPalettesCGB_ADDR - 32), '
                 '(uint16_t)(wTempBackgroundPalettesCGB_ADDR + 32), 16);',
        'case_ids': ['FadeBGPalIntoTemp2-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadeBGPalIntoTemp3': {   'source_symbol': 'FadeBGPalIntoTemp3',
        'before': '    fade_palette_bytes(wBackgroundPalettesCGB_ADDR, '
                  'wTempBackgroundPalettesCGB_ADDR, 32);',
        'after': '    ;',
        'case_ids': ['FadeBGPalIntoTemp3-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadePalIntoAnother.GetFadedColor': {   'source_symbol': 'FadePalIntoAnother.GetFadedColor',
        'before': '    if (c != e || b != d) {',
        'after': '    if (c == e || b != d) {',
        'case_ids': ['FadePalIntoAnother.GetFadedColor-2'],
        'source': 'src/profiles/extended/home/color.c'},
    'FadePalIntoAnother.FadeColor': {   'source_symbol': 'FadePalIntoAnother.FadeColor',
        'before': '    return fade_component(a, (uint8_t)hl);',
        'after': '    return fade_component((uint8_t)(a ^ 1u), (uint8_t)hl);',
        'case_ids': ['FadePalIntoAnother.FadeColor-1'],
        'source': 'src/profiles/extended/home/color.c'},
    'FlashScreenToWhite': {   'source_symbol': 'FlashScreenToWhite',
        'before': '    if (c == 0) {',
        'after': '    if (c != 0) {',
        'case_ids': ['FlashScreenToWhite-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'CopyPalsToSRAMBuffer': {   'source_symbol': 'CopyPalsToSRAMBuffer',
        'before': 'void CopyPalsToSRAMBuffer(void)\n{',
        'after': 'void CopyPalsToSRAMBuffer(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['CopyPalsToSRAMBuffer-1'],
        'source': 'src/profiles/extended/home/color.c'},
    'LoadPalsFromSRAMBuffer': {   'source_symbol': 'LoadPalsFromSRAMBuffer',
        'before': '        gb_write8((uint16_t)(wBackgroundPalettesCGB_ADDR + i), '
                  'gb_read8((uint16_t)(address + i)));',
        'after': '        gb_write8((uint16_t)(wBackgroundPalettesCGB_ADDR - i), '
                 'gb_read8((uint16_t)(address + i)));',
        'case_ids': ['LoadPalsFromSRAMBuffer-0'],
        'source': 'src/profiles/extended/home/color.c'},
    'Func_10d74': {   'source_symbol': 'Func_10d74',
        'before': '    if (value == 0)',
        'after': '    if (value != 0)',
        'case_ids': ['Func_10d74-0'],
        'source': 'src/profiles/extended/home/color.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
