"""Extended oracle-diff cases for menus, seeded from tests/cases/menus.py."""

CONTRACT = {
    'InitializeCardListParameters': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'InitializeMenuParameters': {'compare': ('c', 'hl'), 'preserve': ('c',)},
    'SetMenuItem': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'OneByteNumberToTxSymbol': {'compare': ('a', 'hl'), 'preserve': ()},
    'OneByteNumberToTxSymbol_TrimLeadingZeros': {'compare': ('a', 'hl'), 'preserve': ()},
    'CardTypeToSymbolID': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetCardSymbolData': {'compare': ('d', 'e', 'hl'), 'preserve': ('d', 'e')},
    'SetCursorParametersForTextBox': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('d', 'e')},
    'SetCursorParametersForTextBox_Default': {'compare': ('d', 'e', 'f'), 'preserve': ('d', 'e')},
    'DrawCursor': {'compare': (), 'preserve': ()},
    'EraseCursor': {'compare': (), 'preserve': ()},
    'DrawCursor2': {'compare': (), 'preserve': ()},
    'RefreshMenuCursor': {'compare': (), 'preserve': ()},
    'DrawCardSymbol': {'compare': ('b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'DrawNarrowTextBox': {'compare': ('hl',), 'preserve': ()},
    'DrawWideTextBox': {'compare': ('hl',), 'preserve': ()},
    'DrawNarrowTextBox_PrintTextNoDelay': {'compare': ('hl',), 'preserve': ()},
    'DrawWideTextBox_PrintTextNoDelay': {'compare': ('hl',), 'preserve': ()},
    'DrawWideTextBox_PrintText': {'compare': ('hl',), 'preserve': ()},
    'PrintYesOrNoItems': {'compare': ('b', 'c', 'hl'), 'preserve': ('b', 'c')},
    'WaitForButtonAorB': {'compare': ('f',), 'preserve': ()},
    'DrawWideTextBox_WaitForInput': {'compare': (), 'preserve': ()},
    'WaitForWideTextBoxInput': {'compare': (), 'preserve': ()},
    'RefreshMenuCursor_CheckPlaySFX': {'compare': (), 'preserve': (), 'wram_out': True},
    'PlayOpenOrExitScreenSFX': {'compare': ('a', 'f'), 'preserve': ('a', 'f'), 'wram_out': True},
    'HandleYesOrNoMenu': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ()},
    'CopyCardNameAndLevel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'ReloadCardListItems': {'compare': (), 'preserve': (), 'wram_out': True},
    'PrintCardListItems': {'compare': (), 'preserve': (), 'wram_out': True},
    'CardListMenuFunction': {'compare': ('a', 'f'), 'preserve': ()},
    'HandleMenuInput': {'compare': ('a', 'e', 'f'), 'preserve': ()},
    'HandleCardListInput': {'compare': ('a', 'd', 'e', 'f'), 'preserve': ()},
    'HandleDuelMenuInput': {'compare': ('a', 'e', 'f'), 'preserve': ()},
    'YesOrNoMenuWithText_LeftAligned': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ()},
    'TwoItemHorizontalMenu': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ()},
    'YesOrNoMenu': {'compare': ('a', 'f'), 'preserve': ()},
    'YesOrNoMenuWithText': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ()},
    'YesOrNoMenuWithText_SetCursorToYes': {'compare': ('a', 'f'), 'preserve': ()},
    'DrawTextBox_PrintTextNoDelay': {'compare': ('hl',), 'preserve': ()},
}

CASES = {
    'InitializeCardListParameters': [
        {'hl': 0xC100, 'wram': {0xC100: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08'}},
        {   'a': 0x07,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x03,
            'e': 0x02,
            'hl': 0xC100,
            'wram': {0xC100: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08'}},
    ],
    'InitializeMenuParameters': [
        {'hl': 0xC100, 'wram': {0xC100: b'\x00\x01\x02\x03\x04\x05\x06\x07'}},
        {   'a': 0x04,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC100,
            'wram': {0xC100: b'\x00\x01\x02\x03\x04\x05\x06\x07'}},
    ],
    'SetMenuItem': [
        {},
        {'a': 0x05, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'OneByteNumberToTxSymbol': [
        {'read': {0xC580: 0x03}},
        {   'a': 0x09,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xC580: 0x03}},
        {'a': 0x0A, 'read': {0xC580: 0x03}},
        {'a': 0x63, 'read': {0xC580: 0x03}},
        {'a': 0xFF, 'read': {0xC580: 0x03}},
    ],
    'OneByteNumberToTxSymbol_TrimLeadingZeros': [
        {'read': {0xC580: 0x03}},
        {'a': 0x09, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE,
         'hl': 0x1234, 'read': {0xC580: 0x03}},
        {'a': 0x2A, 'read': {0xC580: 0x03}},
    ],
    'CardTypeToSymbolID': [
        {'wram': {0xCBCF: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCBCF: b'\x07'}},
        {'wram': {0xCBCF: b'\x08'}},
        {'wram': {0xCBCF: b'\x0f'}},
        {'wram': {0xCBCF: b'\x10', 0xCBD9: b'\x03'}},
    ],
    'GetCardSymbolData': [
        {'wram': {0xCBCF: b'\x00', 0xCBD9: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCBCF: b'\x10', 0xCBD9: b'\x02'}},
        {'wram': {0xCBCF: b'\x08'}},
    ],
    'SetCursorParametersForTextBox': [
        {'d': 0x03, 'e': 0x04, 'b': 0x12, 'c': 0x34},
        {'a': 0xAA, 'f': 0xF0, 'b': 0x56, 'c': 0x78, 'd': 0x07, 'e': 0x08, 'hl': 0x1234},
        {   'd': 0x03,
            'e': 0x04,
            'b': 0x12,
            'c': 0x34,
            'oracle': False,
            'why': 'cursor state is inside the synthesized frame',
            'expect': {0xCCBD: b'\x00\x00\x03\x04\x00\x01\x124'}},
    ],
    'SetCursorParametersForTextBox_Default': [
        {'d': 0x02, 'e': 0x05, 'keys': 0x01, 'read': {0xCCBD: 0x08}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x09,
            'e': 0x01,
            'hl': 0x1234,
            'keys': 0x01,
            'read': {0xCCBD: 0x08}},
    ],
    'DrawCursor': [
        {   'a': 0x05,
            'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x00',
                        0xCCBF: b'\x00',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'\x00'},
            'vread': {0x00: {0x9800: 0x01}, 0x01: {0x9800: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x03',
                        0xCCBF: b'\x05',
                        0xCCC0: b'\x07',
                        0xCCC1: b'\x04',
                        0xCCC3: b'\x00',
                        0xCCC4: b'\x00'},
            'vread': {0x00: {0x9A65: 0x01}, 0x01: {0x9A65: 0x01}}},
        {   'a': 0x07,
            'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\xfa',
                        0xCCBF: b'\x0f',
                        0xCCC0: b'\n',
                        0xCCC1: b'\x01',
                        0xCCC3: b'\x00',
                        0xCCC4: b'\x00'},
            'vread': {0x00: {0x988F: 0x01}}},
    ],
    'EraseCursor': [
        {   'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x03',
                        0xCCC1: b'\x02',
                        0xCCC3: b'\x00',
                        0xCCC4: b'\x07'},
            'vread': {0x00: {0x98A2: 0x01}, 0x01: {0x98A2: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x06',
                        0xCCBF: b'\t',
                        0xCCC0: b'\x0b',
                        0xCCC1: b'\x05',
                        0xCCC3: b'\x00',
                        0xCCC4: b'*'},
            'vread': {0x00: {0x9D29: 0x01}}},
    ],
    'DrawCursor2': [
        {   'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x02',
                        0xCCBF: b'\x01',
                        0xCCC0: b'\x01',
                        0xCCC1: b'\x03',
                        0xCCC3: b'\t',
                        0xCCC4: b'\x00'},
            'vread': {0x00: {0x98E1: 0x01}, 0x01: {0x98E1: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x08',
                        0xCCBF: b'\x04',
                        0xCCC0: b'\x06',
                        0xCCC1: b'\x07',
                        0xCCC3: b';',
                        0xCCC4: b'\x00'},
            'vread': {0x00: {0x9FC4: 0x01}}},
    ],
    'RefreshMenuCursor': [
        {   'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x03',
                        0xCCBF: b'\x01',
                        0xCCC0: b'\x01',
                        0xCCC1: b'\x02',
                        0xCCC3: b'\xab',
                        0xCCC4: b'\x00'},
            'setup': [{'fn': 'DrawCursor2'}],
            'read': {0x98E1: 0x01}},
        {   'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x03',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x02',
                        0xCCC1: b'\x01',
                        0xCCC3: b'\x11',
                        0xCCC4: b'\x00'},
            'read': {0x98A2: 0x01}},
        {   'wram': {   0xCCBD: b'\x10',
                        0xCCBE: b'\x04',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x01',
                        0xCCC1: b'\x05',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"'},
            'read': {0x9AA2: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xCCBD: b'\xff',
                        0xCCBE: b'\t',
                        0xCCBF: b'\n',
                        0xCCC0: b'\x02',
                        0xCCC1: b'\x06',
                        0xCCC3: b'D',
                        0xCCC4: b'\x00'},
            'setup': [{'fn': 'DrawCursor2'}],
            'read': {0x9F0A: 0x01}},
    ],
    'DrawCardSymbol': [
        {   'd': 0x05,
            'e': 0x05,
            'vread': {0x00: {0x9883: 0x02, 0x98A3: 0x02}, 0x01: {0x9883: 0x02, 0x98A3: 0x02}}},
        {   'd': 0x0A,
            'e': 0x0A,
            'wram': {0xCAB4: b'\x02', 0xCBCF: b'\x10'},
            'vread': {0x00: {0x9928: 0x02, 0x9948: 0x02}, 0x01: {0x9928: 0x02, 0x9948: 0x02}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x00,
            'e': 0x01,
            'hl': 0x1234,
            'wram': {0xCBCF: b'\t'},
            'vread': {0x00: {0x98FE: 0x02, 0x991E: 0x02}}},
        {'d': 0x14, 'e': 0x03, 'wram': {0xCBCF: b'\x08'}, 'vread': {0x00: {0x9852: 0x02, 0x9872: 0x02}}},
    ],
    'DrawNarrowTextBox': [
        {'vread': {0x00: {0x9980: 0xC0}}},
        {'wram': {0xCAB4: b'\x02'}, 'vread': {0x01: {0x9980: 0xC0}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'vread': {0x00: {0x9980: 0xC0}}},
    ],
    'DrawWideTextBox': [
        {'vread': {0x00: {0x9980: 0xC0}}},
        {'wram': {0xCAB4: b'\x02'}, 'vread': {0x01: {0x9980: 0xC0}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'vread': {0x00: {0x9980: 0xC0}}},
    ],
    'DrawNarrowTextBox_PrintTextNoDelay': [
        {'hl': 0x00, 'vread': {0x00: {0x9980: 0xC0}}},
        {   'hl': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
    ],
    'DrawWideTextBox_PrintTextNoDelay': [
        {'hl': 0x00, 'vread': {0x00: {0x9980: 0xC0}}},
        {   'hl': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
    ],
    'DrawWideTextBox_PrintText': [
        {'hl': 0x00, 'wram': {0xC580: b'\x00'}, 'vread': {0x00: {0x9980: 0xC0}}},
        {   'hl': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
    ],
    'PrintYesOrNoItems': [
        {   'd': 0x07,
            'e': 0x10,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x03,
            'e': 0x10,
            'hl': 0x1234,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
    ],
    'WaitForButtonAorB': [
        {   'keys': 0x01,
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x04',
                        0xCCC0: b'\x01',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'\x11'},
            'vread': {0x00: {0x9884: 0x01}}},
        {   'keys': 0x02,
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x04',
                        0xCCC0: b'\x01',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'\x11'},
            'vread': {0x00: {0x9884: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x01,
            'wram': {   0xCCBD: b'\x00',
                        0xCCBE: b'\x02',
                        0xCCBF: b'\x01',
                        0xCCC0: b'\x02',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'3'},
            'vread': {0x00: {0x9841: 0x01}}},
        {   'wram': {0xCAD3: b'\xc9\x32', 0xD410: b'\xff\xff\xff\xff\xff\xff\xff', 0xD417: b'\xff', 0xC000: b'\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0'
                                b'\xf1\xf2\xf3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd0'
                                b'\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x03\x03'
                                b'\x03\x03\x03\x03\x03\x03\x03\x08\x08\t\x0b\x0c\x0c\r\x14\x14'
                                b'\x17\x17\x18->KLOOPSST[\xaf\xb1\xbc\xbc\xb9\xc3\xd2\xd4\xd8\xd8'
                                b'\xd9\xdf\xdf\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x06Bulbasaur & Friends\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x000I RZ BU O@O N ADCLETN!\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x03 SCAYAOTPKMNADCR OLCIG\x03'
                                b'\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03'
                                b'\x03\x03\x03\x03\x03\x03\x03\x00\x00\x03\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x0001234567>9:;8=<?@ABCDEFGHIJKLMN'
                                b'OPQRSTUVWXYZ[\\]^_`abcdefghijklm\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x0012345678=:;<?>9@ABCDEFGHIJKLMNOPQRST'
                                b'UVWXYZ[\\]^_`abcdefghijklmnE\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x80'
                                b'\x00\x00\x16\x80\x00\x00\x17\x80\x00\x00\x1c\x02\x00\x00\x1d\x02'
                                b'\x00\x00\x1e\x02\x00\x00\x1f\x02\x00\x00\x08\x00\x00\x00\t\x00'
                                b'\x00\x00\n\x00\x00\x00\x0b\x00\x00\x00\x0c\x00\x00\x00\r\x00'
                                b'\x00\x00\x0e\x00\x00\x00\x0f\x00\x00\x00\x10\x00\x00\x00\x13\x00'
                                b'\x00\x00\x12\x00\x00\x00\x11\x00\x00\x00\x14\x80\x00\x00\x15\x80'
                                b'\x00\x00\x16\x80\x00\x00\x17\x80\x00\x00\x1c\x02\x00\x00\x1d\x02'
                                b'\x00\x00\x1e\x02\x00\x00\x1f\x02\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030'
                                b'\x00\x00\x00\x00\x00\x00\x00\x11\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xe4\xe4',
                        0xCAC0: b'',
                        0xCAC1: b'\x0f\x00(\x00\x00\x00\x00\x00\x00\xaa\xea\xd9\xc3\x00\x00\xc3"\x03\xc73\x00\xe5s\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9cc\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x9cc\x1c2\x9c \x00 \x9cc\xb5BJ!\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4\x01\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\xe4\xe4\x84\x84\x84\x84\xa4\xa4\xa4\xa4\xa0\xa0\xe4\xe4FF\x88\x80\x00\x04\x01\x00\x00\x01\x00',
                        0xCCBE: b'\x00\x12\x11\x00\x01/\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x01\x0f\xfao'
                                b'\x0f\x00\x0f\xac\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x0f\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b'\x00\x00\x00\x00\x00\xc2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x7fFA\x9a\x00\x01\x13\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFE8,
            'rom_bank': 0x0F,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x00,
            'b': 0x2F,
            'c': 0x1D,
            'd': 0x12,
            'e': 0x11,
            'f': 0x80,
            'hl': 0xCCC4},
    ],
    'DrawWideTextBox_WaitForInput': [
        {   'hl': 0x00,
            'keys': 0x01,
            'wram': {   0xC580: b'\x00',
                        0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x04',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"'},
            'read': {0xCCBD: 0x01, 0xCCBE: 0x01, 0xCCC4: 0x01},
            'vread': {0x00: {0x9980: 0x01, 0x9A32: 0x01}}},
    ],
    'WaitForWideTextBoxInput': [
        {   'keys': 0x01,
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x00',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x03',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"'},
            'vread': {0x00: {0x9A32: 0x01}}},
    ],
    'RefreshMenuCursor_CheckPlaySFX': [
        {'wram': {0xCD1F: b'\x00'}},
        {'wram': {0xCD1F: b'\x12', 0xD7A7: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCD1F: b'4', 0xD7A7: b'\x00'}},
    ],
    'PlayOpenOrExitScreenSFX': [
        {'a': 0x11, 'f': 0x00, 'wram': {0xFFB1: b'\xff'}, 'read': {0xD7A6: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFFB1: b'\x02'},
            'read': {0xD7A6: 0x01}},
    ],
    'HandleYesOrNoMenu': [
        {   'd': 0x20,
            'e': 0x10,
            'b': 0xAC,
            'c': 0x8B,
            'keys': 0x01,
            'wram': {0xCD20: b'\x00'},
            'expect': {0xCD20: b'\x00', 0xFFB1: b'\x01', 0xCCBE: b'\x01'},
            'expect_regs': {'a': 0x01, 'f': 0x90},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0x20,
            'e': 0x10,
            'hl': 0x1234,
            'keys': 0x01,
            'wram': {0xCD20: b'\x01'},
            'expect': {0xCD20: b'\x00', 0xFFB1: b'\x00', 0xCCBE: b'\x00'},
            'expect_regs': {'a': 0x00, 'f': 0x80},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'CopyCardNameAndLevel': [
        {   'a': 0x0D,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'setup': [{'fn': 'LoadCardDataToBuffer1_FromCardID', 'e': 0x43}],
            'read': {0xC580: 0x20}},
        {   'a': 0x0D,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'setup': [{'fn': 'LoadCardDataToBuffer1_FromCardID', 'e': 0x03}],
            'read': {0xC580: 0x20}},
        {   'a': 0x0D,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'setup': [{'fn': 'LoadCardDataToBuffer1_FromCardID', 'e': 0x43}],
            'read': {0xC580: 0x20}},
    ],
    'ReloadCardListItems': [
        {   'wram': {0xCCC7: b'\x00', 0xCCC0: b'\n', 0xCCC2: b'\x03', 0xCCC9: b'\x03', 0xC500: b'\xff'},
            'read': {0x9932: 0x01, 0x99D2: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCCC7: b'\x01', 0xCCC0: b'\n', 0xCCC2: b'\x02', 0xCCC9: b'\x05', 0xC501: b'\xff'},
            'read': {0x9932: 0x01, 0x99B2: 0x01}},
    ],
    'PrintCardListItems': [
        {   'a': 0x01,
            'd': 0x00,
            'e': 0x00,
            'hl': 0xC4F0,
            'wram': {0xC4F0: b'\x01\x02\x03\x04\x01 !\x00\x00', 0xC500: b'\xff'},
            'read': {0xCCC1: 0x01, 0xCCC5: 0x02, 0xCD1D: 0x01},
            'vread': {0x00: {0x9832: 0x01, 0x9872: 0x01}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC5DD: b'\xff'},
            'read': {0xCCC1: 0x01, 0xCCC5: 0x02, 0xCD1D: 0x01},
            'vread': {0x00: {0x9832: 0x01, 0x9872: 0x01}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'CardListMenuFunction': [
        {   'keys': 0x00,
            'wram': {   0xCCBE: b'\x00',
                        0xCCC2: b'\x02',
                        0xCCC7: b'\x00',
                        0xCCC9: b'\x04',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'w'},
            'read': {0xFFB1: 0x01}},
        {   'keys': 0x00,
            'wram': {   0xCCBE: b'\x01',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'\x12'},
            'read': {0xFFB1: 0x01}},
        {   'keys': 0x02,
            'wram': {   0xCCBE: b'\x01',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'\xaa'},
            'read': {0xFFB1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x01',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'U'},
            'read': {0xFFB1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x01',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x84\x56',
                        0xCD1F: b'U',
                        0xFF91: b'\x08',
                        0xFF80: b'\x01'},
            'read': {0xFFB1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x01',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x84\x56',
                        0xCD1F: b'U',
                        0xFF91: b'\x02',
                        0xFF80: b'\x01'},
            'read': {0xFFB1: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x02',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x00',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'\x01',
                        0xFF8F: b'@'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x00',
                        0xCCC2: b'\x03',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x05',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'\x01',
                        0xFF8F: b'\x80'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x04',
                        0xCCC2: b'\x05',
                        0xCCC7: b'\x02',
                        0xCCC9: b'\x07',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'\x01',
                        0xFF8F: b' '},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x00,
            'wram': {   0xCCBE: b'\x00',
                        0xCCC2: b'\x05',
                        0xCCC7: b'\x00',
                        0xCCC9: b'\x07',
                        0xCD1D: b'\xff',
                        0xCCCB: b'\x00\x00',
                        0xCD1F: b'\x01',
                        0xFF8F: b'\x10'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'HandleMenuInput': [
        {   'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x01',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x02',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x02',
                        0xCCC3: b'\x00',
                        0xCD1F: b'\x99'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCD1F: 0x01}},
        {   'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x02',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x03',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x03',
                        0xCCC3: b'\x00',
                        0xCD1F: b'*'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCD1F: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x02',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x01',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x01',
                        0xCCC3: b'\x00',
                        0xCD1F: b'w'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCD1F: 0x01}},
        {   'wram': {   0xFF8F: b'@',
                        0xFF91: b'\x00',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x02',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x02',
                        0xCCC3: b'\x00',
                        0xCD1F: b'\x99'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCD1F: 0x01}},
        {   'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x08',
                        0xCCC5: b'\xc5\x5e',
                        0xCCBE: b'\x02',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x02',
                        0xCCC3: b'\x00',
                        0xCD1F: b'\x99',
                        0xCCBD: b'\x05',
                        0xFF80: b'\x01'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCD1F: 0x01, 0xCCBD: 0x01}},
        {   'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x00',
                        0xCCC5: b'\xc5\x5e',
                        0xCCBE: b'\x02',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x02',
                        0xCCC3: b'\x00',
                        0xCD1F: b'\x00',
                        0xCCBD: b'\x05',
                        0xFF80: b'\x01'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCD1F: 0x01, 0xCCBD: 0x01}},
        {   'wram': {0xCCC5: b'\xc5\x5e', 0xC000: b'\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0'
                                b'\xc1\xc2\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0'
                                b'\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x01\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00'
                                b'\x00\x00\x00\x00\x08\x01\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x10\x00\x00\x00'
                                b'\x00\x08\x01\x00\x00\x00\x00\x00\x01\x01\x00\x00\x141\x02\x1b'
                                b"\x00\x00'\x00\r9\x1582\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\x00\r9\x15,8\x141\x02"
                                b'\x1b2\x10\x06*\x1d\x1e\x1f35:!\x13$".\x12#(\x0b\x0e\x16\x0f7'
                                b'\x07+\x184)\x1a\n6\x05\x1c-\x17 ;%\x0c0&\t\x08\x04\x03\x01/'
                                b'\x11\x19\x0c,\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00'
                                b'(\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x0f\x00\x07\x01\x00\x00\x00\n\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00'
                                b'\x01\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00'
                                b'\x00\x00\x08\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x08\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x08'
                                b'\x00\x01\x00\x0171\x1a*\x00\x00\x08\x02\x049;;\x13\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x1b\x0b\x08\x02\x049;71\x1a*\x13&3\x1f08\x14,\x165$'
                                b'\x0c+\x0f.#\x11\n\x10\'\x03(\x12\x1e\x01\x18\r\x1742"\x1d\x1c:%'
                                b'\x0e\x19)\x00\x07!\x05\t6\x15/\x06 -\x0c\x1b\x13\xff\xff\xff'
                                b'\xff\xff\x00\x00\x00\x00\x00\x00Z(\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x05\x02'
                                b'\x00\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x04\x04\x04\x04\x04\x04'
                                b'\x04\x04\x05\x05\x05\x05\x05\x05001266899;``giikuyyz}~\xa7\xa7'
                                b'\xa8\xb1\xc3\xc5\xc5\xd2\xd6\xd8\xdd\xdd\xdf\xdf\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x02\x02\x02\x02\x05\x05\x05\x05\x05\x05\x05\x05\x06\x06\x06\x06'
                                b'\x06\x07\x07999::\x83\x83\x83\x83\x84\x84\x84\x84\x85\x85\x89\x89'
                                b'\x89\x89\x8a\x8a\x9c\x9c\xc3\xc3\xc5\xc5\xc5\xc9\xc9\xcd\xc6\xc6'
                                b'\xd2\xd2\xd2\xd9\xd9\xd9\xdb\xdb\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030'
                                b"\x030\x030\x00\x00\x00\x00,8\x159\r\x00'\xff\x00\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x17\x16\x16\x16\x16\x00\x00\x00\x00\x00\x00\x00    '
                                b'     \x00       \x00                                   \x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x000NRNAHPOEDL  ER HGB. SDCTFSO A  OIO EKPNOSWX1NCLFIN '
                                b"TH HEMAL2RRGGIRWATN RYESW RO R() KI1IIY0E.O' KG.KADE\x00\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00RC LBMME\x03AOTEC P'
                                b"SEEDKRTETR XT' E OESRO 2DTRMDCOOTSAI E P FMYAG. NAM VDPINNHOTHIGEG  "
                                b'ESUYUADS0PLV KA1HN 2!OAEAHNF\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x000123456noam\x81rjk<J\x839OWEH'
                                b'[p\x94yB8\x93\x92\x9bvQRST^\x8f{?\x84hG|=Y\x98\x9f\x95\x8cb\x7fdC'
                                b'\x8bU\x8dIF\x8e\x9eM\x82NDc\x9c\x88XAi}\x85>lw;~e\x80x@u\x97P\\'
                                b'\x87f\x89\x8at]_sK\x90g\x99\x00\x86:\x91z`q\x9a\x96L\x9dZ'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x001234'
                                b'5678MC\x96~@^{Y\x83wLgrFl\\GkA\x90\x9doqD\x86RSTUi\x00Ev_\x9fH'
                                b'\x87\x8dV\x8e\x99:dsf\x80\x89\x92[x>?|;89I\x9a=\x8f\x8c\x84Q}'
                                b'\x82K\x98X]y\x7fe\x81<pBZz\x95\x88u\x8a\x8bhcjmW\x91\x97ONJb\x9c\x85'
                                b'`\x93\x9bPt\x9ena\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\x00'
                                b"\x00\x00\x03 \x00\x00' \x00\x00) \x00\x00'@\x00\x00(@\x00\x00'`"
                                b"\x00\x00) \x00\x00'@\x00\x00(@\x00\x00'`\x00\x00\x01@\x00\x00\x02@"
                                b'\x00\x00\x03@\x00\x004 \x00\x006 \x00\x008\x00\x00\x009\x00'
                                b'\x00\x00:\x00\x00\x00;\x00\x00\x00(\x00\x00\x00)\x00\x00\x00( '
                                b'\x00\x00) \x00\x00* \x00\x00, \x00\x00,\x00\x00\x00-\x00\x00\x00( '
                                b'\x00\x00) \x00\x00 \x00\x00\x00!\x00\x00\x001\x00\x00\x002\x00'
                                b'\x00\x003\x00\x00\x00\x19\x00\x00\x00"\x00\x00\x00#\x00\x00\x00\x00"'
                                b' \x00\x030\x030\x030\x00\x00\x00\x00\x00\x00\x00\x11\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xe6\xe4',
                        0xCAC0: b'',
                        0xCAC1: b'\x00\x02M\x01\x0f\x0c!\x00\x00\xe3*\x02\xc3\x00\x00\xc3"\x03\x00\x00\x00\x13t\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9cc\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7fUk\x10i\x00\x10\xfakLC\x08"\x80\x00\x9cc\xb5BJ!\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x00\x00\x11\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x05\x0f\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x08\x02\x00\x00\xaa\x00\xa7\x00\x01\x00\x00\x01\x00\x00\x00\xe8\xdf\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x06\x00\x0e;S\x00\x00\xc2\x01\x00\x04\xa0\x00\x00\x00\x00 \xff\xff\xffV\x00\x1d\x1c\xba\x03\x04 \x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x043/"\n\x00\x00}2\x00\x00\x00\x00\x00\x10\x00#\n\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00$\nB\x00\x14\x02\x07\xae\x01%\n\x15\x043/"\n\x00\x00}2\x00\x00\x00\x00\x00\x10\x00#\n\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00$\nB\x00\x14\x02\x07\xae\x01%\n\x15\x00\x00\x10\x00:\n\x00\x00\x00\x00\n\x00\xa8N\x00\x00\x00\x00 \n\x00\n\n\x00\x00\n\x00\x00\x83}\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc3\xf0\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfd\x01\x00\x00\x00\x04\x00\x00\x00\x00\x04\x00\x00JJ\xaa\xaa\xaa\xaa\xea\xea\xa4\xa4\xa4\xa4\xa4\xa4\x9fV\x88\x80\x00\x00\x01\x00\n\x01\x00',
                        0xCCBE: b"\x00\x00\x00\x03\x01\x0f\x00\xc5^\x00\x04\x07\x0e\x19W\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00\x0e\x01\x00\x00\x01\x00\x00\x00\x00\x00\xff\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x04\x01\x01\xa8\x0e\x00\x00\x00\x00Q\x88\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x04\x00\x04\x04}\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x80\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x13\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xd8\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\xff\x7fUk\x10i\x00\x10\x0f\x01\r o\x0f\x00\r\xac\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00:\n\x01\x00\x00\x00\x02\x00\x00\x00\x00\xba\x03\x00\x00\xc3\xc2\x00[K\xc3\x01\x00\x00\x00\xa2\xff\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\x00\x01\n\x00\x00\x80\xc3}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00;9\x04\x02\x08\xff\xff\xff\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00;9\x04\x02\x08\xff\xff\xff\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x01\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'\x02',
                        0xFF90: b'\x02',
                        0xFF91: b'\x02',
                        0xFF92: b'\x00\x00\x00\x00\n\xc28\x00\x00\x00\x00\x00\n8\x00\x00'
                                b'\xff\xff\x00\x00\x00\x00\x9fV\x0e\x98\n\x04\x00\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x1f\x03',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFD4,
            'rom_bank': 0x01,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100, 0xFF92: 0x01, 0xCCBE: 0x01},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'f': 0x80,
            'hl': 0xCCBD},
    ],
    'HandleCardListInput': [
        {   'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x01',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x02',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x02',
                        0xCCC3: b'\x00',
                        0xCCC7: b'\x03'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01}},
        {   'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x02',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x03',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x03',
                        0xCCC3: b'\x00',
                        0xCCC7: b'\x01'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xFF8F: b'\x00',
                        0xFF91: b'\x02',
                        0xCCC5: b'\x00\x00',
                        0xCCBE: b'\x01',
                        0xCCC2: b'\x04',
                        0xFFB1: b'\x01',
                        0xCCC3: b'\x00',
                        0xCCC7: b'\x07'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCC7: 0x01}},
        {   'wram': {0xCCCB: b'\x84\x56', 0xC000: b'\x05\x18p\x06Dr. Mason\x07p\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05'
                                b'\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x19\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8'
                                b'\xa9\xaa\xab\xac\xad\xae\xaf\xb0\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05'
                                b'\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t'
                                b'\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19'
                                b'\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;\x07\xff'
                                b'\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r'
                                b'\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d'
                                b'\x1e\x1f !"#$%&\'()*+,-./0123456789:;\x07\xff\xff\xff\xff\xff'
                                b'\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00'
                                b'\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x03\x03\x06TU\xdfS\x03\x03\x03\x03\x03\x99\xddTV\x03\xc5\x06\x9c'
                                b'A\x03A\x03\x06B\xc5\x03C\x03\x06\x03\x06\xa7\x8e\x06\x9a\x03\x06K'
                                b'\x06\x8f\xdd\x06\x99\x06\xa7SKLSUY\x8e\x99\x9a\xa7\xa8\xa8\x90'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x04\x04\x05\x05}\xa8\x7f\x05\x05\x7f\xa7\x05'
                                b'\x05}\x05\xa8\x04}\xc5\x05yz\x05~\x04\x04\xdbs\x04q\x05\x88'
                                b'\x04\xc3\x05\xbc\x05\x07`\x04`\x04\xdd\x04a\x04gh\x04sy}~\x83\x89\x89'
                                b'\x8a\xa7\xbc\xbc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030'
                                b'\x00\x00\x00\x00\x06\x05\x04\x03\x02\x01\x00\xff\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x06Psychic Energy              \x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x000EO Y HOISITP,OC@OIGLERESADY.AHAR EL'
                                b'L AD.OEABSKMNOE RN.ODEV2 UH UL1 KN 8SCI RYSN pR AOW7CS E ED OAT YUCI'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TC S'
                                b'MMSP\x03VYULETH OSS LPIKME ODOL T RUECLPRULP7CRSOS  AO@OTCNAEAGLEL1'
                                b" F LY V5AIG2PYHCEG'AD\x00D.MSA  D,GTRAYFBT! OAT\x00\x00\x00\x00"
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000142356'
                                b'\x8b\x9f\x9b:^AJ\x90W?\x99w9ZBdFH\x9caKL>\x9aNPjQSvEiY\x9dRuM\x00;]'
                                b'_V{`cIDfgGXqC\x83@\x88op~k\x85s[Ulxyzb|}r\x7f\x80\x81\x82m\x848\x86'
                                b'\x87\x8dTh\x8a\x8cn\x8e\\\x8fe\x91\x93\x94\x95\x96\x89<\x97O'
                                b'\x92\x98=\x9e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x0012453678\x86D;^\x99\x9eNAn=FlfVHiIe>LM\\P\x9bQSZT'
                                b'\x8awa@jXEv\x90_<`cK|dG\x92gh\x8bWRsx\x84\x8epqk\x7fu\x00[UCyz{b'
                                b'}~r\x80\x81\x82\x83m\x85t\x87\x88o\x98\x8c8\x8d\x89\x8f\x91'
                                b'?\x93\x9c\x94\x95\x96\x97\x9a\x9dBO:JY\x9f9\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\x00'
                                b'\x00\x00\x03 \x00\x00\x03\x00\x00\x00\x03 \x00\x008\x00\x00\x009\x00'
                                b'\x00\x00:\x00\x00\x00;\x00\x00\x005 \x00\x007 \x00\x004 \x00\x006 '
                                b'\x00\x00+ \x00\x00- \x00\x00* \x00\x00, \x00\x005 \x00\x007 '
                                b'\x00\x004 \x00\x006 \x00\x008\x00\x00\x009\x00\x00\x00:\x00'
                                b'\x00\x00;\x00\x00\x00(\x00\x00\x00)\x00\x00\x00( \x00\x00) '
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x030\x030\x030\x030\x030\x030\x00\x00\x00\x00\x00\x00\x00\x11'
                                b'\x02\x00\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xe6\xe4',
                        0xCAC0: b'',
                        0xCAC1: b'\x1d\x00\xa6\x01\x11+\x06\x00\x00WWW\xc3\x00\x00\xc3"\x03\x00\x00\x00\x13t\x05\x00\x00\x00\x00\xc0\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9cc\xb5BJ!\x00\x00\x9cc\xbe\x03~\x00\x00\x00\x9cc@\x02lQ\x00\x00\x9cc\x16X\xfb\x0c\x00\x00\x9ccZ\x01\x1c\x00\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xffC\xa4\x02\x15\x00\x04\x00\x9cc\x1c2\x9c \x00 \x10R\x9cc\x8cQ\x00\x00\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00n\x00\xa7\x00\x01\x00\x00\x00\x00\x00\x00\xe8\xdf\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x80\x00\x00\x00\x00\x00\xff\xff\xff\x00\x01\x07\x03\xb1\x03\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x033\x1fz\t\x00\x01S(\x00\x00\x00\x00\x01\x00\x00{\t\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00|\tv\x00\x0c\x02\x00J\x01}\t\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdf\x01\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\xe8\xe8\xa8\xa8\xa8\xa8\xa8\xa8\xe8\xe8\x88\x88\x8e\x8e\x9ft\x88\x80\x00\x00\x01\x00\x00\x01\x00',
                        0xCCBE: b'\x00\x01\x03\x02\x05\x0f\x00.\x1f\x00\x04\x07\x0e\x19W\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x06\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xffC\xa4\x02\x15\x00\x04\x00\x0f\x01\r\x9bs\x0f\x00\r\xac\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdf\x01\xb1\x03\x00\x00\x00\x00\x02\x00\x00\x00\x01\xa3\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x01\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b'\x00\x00\x00\x00\x00\xc2\x06\x00\x00\x00\x00\x00\x00\x00\x01\x00'
                                b'\x00\x00\x00\x00\x00\x00\x9ftr\x99\x0e\x04\x00\x0f\x00\x00'
                                b'\x00\x00\x00\x00\x1f\x03',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFDC,
            'rom_bank': 0x01,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x00,
            'b': 0x00,
            'c': 0x10,
            'd': 0xCD,
            'e': 0xF1,
            'f': 0xA0,
            'hl': 0xCB28},
    ],
    'HandleDuelMenuInput': [
        {   'e': 0x00,
            'wram': {0xFF8F: b'\x01', 0xCCBE: b'\x02', 0xFFB1: b'\x02', 0xCCBD: b'\x00'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01}},
        {   'e': 0x00,
            'wram': {0xFF8F: b'@', 0xCCBE: b'\x00', 0xFFB1: b'\x00', 0xCCBD: b'\x00'},
            'read': {0xFFB1: 0x01, 0xCCBE: 0x01, 0xCCBD: 0x01},
            'vread': {0x00: {0x99C2: 0x01}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF8F: b'\x00', 0xCCBE: b'\x00', 0xFFB1: b'\x00', 0xCCBD: b'\x01'},
            'read': {0xCCBD: 0x01}},
    ],
    'YesOrNoMenuWithText_LeftAligned': [
        {   'hl': 0x01,
            'b': 0x12,
            'c': 0x34,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x00'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x01, 'f': 0x90},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x01,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x01'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x00, 'f': 0x80},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'TwoItemHorizontalMenu': [
        {   'hl': 0x00,
            'keys': 0x01,
            'wram': {0xFF97: b'\xc2'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'expect_regs': {'a': 0x00, 'f': 0x80},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x00,
            'keys': 0x01,
            'wram': {0xFF97: b'\xc2'},
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'expect_regs': {'a': 0x00, 'f': 0x80},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'YesOrNoMenu': [
        {   'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x00'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x01, 'f': 0x90},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x01'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x00, 'f': 0x80},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'wram': {0xCAD3: b'\xc9\x32', 0xD410: b'\xff\xff\xff\xff\xff\xff\xff', 0xD417: b'\xff', 0xC000: b'\x05\x18p\x06Sam\x07p\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05'
                                b'\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05\x1c\x05'
                                b'\x1c\x05\x19\x00\xa3\xa3\xa5\x02\x02\x02\x02\x02\x02\x02\x02\x02'
                                b'\x02\x02\x02\x02\x02\x05\x05\x05\x05\x02\x02\x02\x02\x02\x02\x02'
                                b'\x02\x02\x02\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
                                b'\x80\x81\x81\x81\x81\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x02'
                                b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x05\x05\x05'
                                b'\x05\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x81\x81\x8a\x88\x02'
                                b'\x02\t\t\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05'
                                b'\x05\x05\x05\x05\x05\x05\x05\x05\x05\x02\x02\x87\x90\x83\x83\x83'
                                b'\x83\x83\x83\x83\x83\x83\x83\x83\x86\x81\x81\x81\x81\x85\x83\x83'
                                b'\x83\x83\x83\x83\x83\x92\x89\x02\x02\x02\x02\x02\x02\x02\x02\x02'
                                b'\x02\x02\x02\x02\x02\x05\x05\x05\x05\x02\x02\x02\x02\x02\x02\x02'
                                b'\x02\x02\x02\x96\x93\x93\x93\x93\x93\x93\x93\x93\x93\x93\x93\x93'
                                b'\x94\x81\x81\x81\x81\x94\x93\x93\x93\x93\x93\x93\x93\x93\x95\x02'
                                b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x03\x03\x03\x03\x03\x03'
                                b'\x03\x03\x03\x08\x08\t\x0b\x0c\x0c\r\x14\x14\x17\x17\x18->KLOOPSS'
                                b'T[\xaf\xb1\xbc\xbc\xb9\xc3\xd2\xd4\xd8\xd8\xd9\xdf\xdf\xe0'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x06Bulbasaur & Friends\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00TTSIR EKADOFGXTpA STA L?\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00SAUDAYDCCRCNIEI\x00SMI HTALTNEOV O@OPKMNWR OTRWO OS'
                                b'O  ULNTTSILTRTET TPSO NRS RS,FWT\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x000123456789:;<=A>@?BCDEFG3HJKLMN'
                                b'OS2R[QXIWVYZT\\]^_g`bcdeDahN\x007l3moFqLptuv9xyj:Iz~\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00123456789:;<=>@BA?CD'
                                b'EFGHJWKLMNOP2USQ\\?YXVZ[T]^_`bhcdefCa\x00F{7modptrCEuvw5yz~J=B\x7f2'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PH\r$'
                                b'XH\x0f$PP\x0c$XP\x0e$@(\x16\x06@0\x17\x06H(\x18\x06H0\x19\x06'
                                b'P\x184\x00P 5\x00X\x186\x00X 7\x00 \xa89 (\xa8;  \xb08 (\xb0: '
                                b'\x80\xa8(\x00\x88\xa8)\x00\x80\xb0( \x88\xb0) \x90\xa89 \x98\xa8; '
                                b'\x90\xb08 \x98\xb0: \x00(+ \x08(- \x000* \x080, \x00\x00+ \x00\x00- '
                                b'\x00\x00* \x00\x00, \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x030\x030\x030\x030\x030\x030\x00\x00\x00\x00'
                                b'\x00\x00\x00\x11\x02p\x00',
                        0xCAB8: b'',
                        0xCAB9: b'\x00\x00\xc3\xe4\xd3\xe3',
                        0xCAC0: b'',
                        0xCAC1: b'\x1d\x00\xf0\x01\x07 \x05\x00\x00\xfc\x1b\xd3\xc3\x00\x00\xc3"\x03\x17.\x00\xb4^\x05\x00\x00\xf9\x00\xc0\xd7\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x7f\x94B\x08!\x00\x00\xf9\x7f\xa9~\xb8\x01e\x00\x9cs\x99\x02\xc8\x04\x00\x00~?\xb8\x01\x0e\x01\x00\x00\x9cs\x81\x02\xc8\x04\x00\x00\xf9\x7f\xa9~\xe5|\x00\x14\xf9\x7f\xa9~\x1f|\x00\x14\xf9\x7f\xa9~\xa4\x06A\x01\xc6-~c\xe6e\x00\x00\xc6-~c\xbeI\x00\x00\xc6-~c\x1c\x17\x00\x00\xc6-~cd\x0e\x00\x00\xc6-~c\xbe$\x00\x00\xc6-~c\x0fi\x00\x00\xc6-~c\xff\x7f\x00\x00\xc6-~c)m\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8e\x8e\x82\x82\x82\x82\x86\x86\x84\x84\x80\x80\xe4\xe4GG\x88\x80\x00\x00\x01\x00\x00\x01\x00',
                        0xCCBE: b'\x00\x12\x11\x00\x01/\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x01\x13\x86J'
                                b'\x0f\x00\x13\xac\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\xb1\x03\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00',
                        0xCE4E: b'\x05\x00\x00\x00\x00\x06\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x030\x030\x030\x030\x03',
                        0xFF80: b'\x03\x00\x00>\xca\xe0F>(= \xfd\xc9',
                        0xFF8E: b'',
                        0xFF8F: b'',
                        0xFF90: b'',
                        0xFF91: b'',
                        0xFF92: b'\x100\x00\x00\x00\xc2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x7fG\x89\x9a\x06\x03\x13\x0f\x00\x07'
                                b'\x00\x00\x00\x00\x00\x00',
                        0xFF40: b'\xc3'},
            'entry_sp': 0xDFDC,
            'rom_bank': 0x03,
            'read': {0xC200: 0x0200, 0xCBAA: 0x0100},
            'keys': [0x00, 0x01],
            'instruction_budget': 0x2625A00,
            'cycle_budget': 0x9896800,
            'a': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x14,
            'e': 0x17,
            'f': 0x80,
            'hl': 0x00},
    ],
    'YesOrNoMenuWithText': [
        {   'hl': 0x01,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x00'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x01, 'f': 0x90},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x01,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x01'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x00, 'f': 0x80},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'YesOrNoMenuWithText_SetCursorToYes': [
        {   'hl': 0x01,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x00'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x01, 'f': 0x90},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x01,
            'keys': 0x01,
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'wram': {   0xCCBD: b'\x05',
                        0xCCBE: b'\x01',
                        0xCCBF: b'\x02',
                        0xCCC0: b'\x00',
                        0xCCC1: b'\x00',
                        0xCCC3: b'\x00',
                        0xCCC4: b'"',
                        0xCD20: b'\x00'},
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}},
            'expect_regs': {'a': 0x01, 'f': 0x90},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'DrawTextBox_PrintTextNoDelay': [
        {   'a': 0x0B,
            'stack': [0x00],
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0x0B,
            'stack': [0x01],
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0x13,
            'stack': [0x01],
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
        {   'a': 0x13,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'stack': [0x01],
            'setup': [{'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'read': {   0xC620: 0x04,
                        0xC720: 0x04,
                        0xC820: 0x04,
                        0xC920: 0x04,
                        0xCCB3: 0x02,
                        0xCCB8: 0x01,
                        0xFFAA: 0x02,
                        0xFFAD: 0x01,
                        0xFFAE: 0x01},
            'vread': {0x00: {0x8000: 0x1000, 0x9000: 0x0800, 0x9980: 0xC0}, 0x01: {0x9980: 0xC0}}},
    ],
}

MUTATIONS = {
    'InitializeCardListParameters': {   'source_symbol': 'InitializeCardListParameters',
        'before': '\tgb_write8((uint16_t)(wListFunctionPointer_ADDR + 1), gb_read8((*hl)++));',
        'after': '\t;',
        'case_ids': ['InitializeCardListParameters-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'InitializeMenuParameters': {   'source_symbol': 'InitializeMenuParameters',
        'before': '\t\tgb_write8((uint16_t)(wMenuCursorXOffset_ADDR + i), gb_read8((*hl)++));',
        'after': '\t\t;',
        'case_ids': ['InitializeMenuParameters-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'SetMenuItem': {   'source_symbol': 'SetMenuItem',
        'before': 'void SetMenuItem(uint8_t a)\n{\n\twCurMenuItem = a;',
        'after': 'void SetMenuItem(uint8_t a)\n{\n\twCurMenuItem = (a) ^ 1u;',
        'case_ids': ['SetMenuItem-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'OneByteNumberToTxSymbol': {   'source_symbol': 'OneByteNumberToTxSymbol',
        'before': 'return tx_symbol_core(a);',
        'after': 'return tx_symbol_core((uint8_t)(a + 1u));',
        'case_ids': [   'OneByteNumberToTxSymbol-0',
                        'OneByteNumberToTxSymbol-1',
                        'OneByteNumberToTxSymbol-2',
                        'OneByteNumberToTxSymbol-3',
                        'OneByteNumberToTxSymbol-4'],
        'source': 'src/profiles/extended/home/menus.c'},
    'OneByteNumberToTxSymbol_TrimLeadingZeros': {   'source_symbol': 'OneByteNumberToTxSymbol_TrimLeadingZeros',
        'before': '\t\tgb_write8(result.hl, SYM_SPACE);',
        'after': '\t\t;',
        'case_ids': ['OneByteNumberToTxSymbol_TrimLeadingZeros-0',
                     'OneByteNumberToTxSymbol_TrimLeadingZeros-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'CardTypeToSymbolID': {   'source_symbol': 'CardTypeToSymbolID',
        'before': 'uint8_t CardTypeToSymbolID(void)\n{',
        'after': 'uint8_t CardTypeToSymbolID(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['CardTypeToSymbolID-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'GetCardSymbolData': {   'source_symbol': 'GetCardSymbolData',
        'before': 'uint8_t GetCardSymbolData(void)\n{',
        'after': 'uint8_t GetCardSymbolData(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['GetCardSymbolData-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'SetCursorParametersForTextBox': {   'source_symbol': 'SetCursorParametersForTextBox',
        'before': '\tgb_write8(wMenuCursorXOffset_ADDR, d);',
        'after': '\tgb_write8(wMenuCursorXOffset_ADDR, (uint8_t)(d ^ 1u));',
        'case_ids': ['SetCursorParametersForTextBox-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'SetCursorParametersForTextBox_Default': {   'source_symbol': 'SetCursorParametersForTextBox_Default',
        'before': '\tresult.f = WaitForButtonAorB().f;',
        'after': '\tresult.f = (WaitForButtonAorB().f) ^ 1u;',
        'case_ids': ['SetCursorParametersForTextBox_Default-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawCursor': {   'source_symbol': 'DrawCursor',
        'before': '\t(void)DrawCursorRegs(a);',
        'after': '\t;',
        'case_ids': ['DrawCursor-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'EraseCursor': {   'source_symbol': 'EraseCursor',
        'before': '\tDrawCursor(wMenuInvisibleCursorTile);',
        'after': '\t;',
        'case_ids': ['EraseCursor-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawCursor2': {   'source_symbol': 'DrawCursor2',
        'before': '\tDrawCursor(wMenuVisibleCursorTile);',
        'after': '\t;',
        'case_ids': ['DrawCursor2-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'RefreshMenuCursor': {   'source_symbol': 'RefreshMenuCursor',
        'before': '\t(void)RefreshMenuCursorRegs();',
        'after': '\t;',
        'case_ids': ['RefreshMenuCursor-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawCardSymbol': {   'source_symbol': 'DrawCardSymbol',
        'before': '\tuint8_t attr = gb_read8((uint16_t)(entry + 1));',
        'after': '\tuint8_t attr = 0u;',
        'case_ids': ['DrawCardSymbol-0', 'DrawCardSymbol-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawNarrowTextBox': {   'source_symbol': 'DrawNarrowTextBox',
        'before': '\tDrawRegularTextBox(&hl, 0, 12, 6, d, e);',
        'after': '\t;',
        'case_ids': ['DrawNarrowTextBox-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawWideTextBox': {   'source_symbol': 'DrawWideTextBox',
        'before': '\tDrawRegularTextBox(&hl, 0, 20, 6, d, e);',
        'after': '\t;',
        'case_ids': ['DrawWideTextBox-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawNarrowTextBox_PrintTextNoDelay': {   'source_symbol': 'DrawNarrowTextBox_PrintTextNoDelay',
        'before': '\tDrawNarrowTextBox();',
        'after': '\t;',
        'case_ids': ['DrawNarrowTextBox_PrintTextNoDelay-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawWideTextBox_PrintTextNoDelay': {   'source_symbol': 'DrawWideTextBox_PrintTextNoDelay',
        'before': '{\n\tDrawWideTextBox();',
        'after': '{\n\t;',
        'case_ids': ['DrawWideTextBox_PrintTextNoDelay-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawWideTextBox_PrintText': {   'source_symbol': 'DrawWideTextBox_PrintText',
        'before': '\tInitTextPrintingInTextbox(19, d, e);',
        'after': '\tInitTextPrintingInTextbox(19, (uint8_t)(d ^ 1u), e);',
        'case_ids': ['DrawWideTextBox_PrintText-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'PrintYesOrNoItems': {   'source_symbol': 'PrintYesOrNoItems',
        'before': '\treturn InitTextPrinting_ProcessTextFromID(d, e, YES_OR_NO_TEXT_ID);',
        'after': '\treturn InitTextPrinting_ProcessTextFromID((uint8_t)(d ^ 1u), e, '
                 'YES_OR_NO_TEXT_ID);',
        'case_ids': ['PrintYesOrNoItems-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'WaitForButtonAorB': {   'source_symbol': 'WaitForButtonAorB',
        'before': '\t\t\t|| gb_read8(wMenuInvisibleCursorTile_ADDR) == 0u ? 0x80u : 0x00u;',
        'after': '\t\t\t|| gb_read8(wMenuInvisibleCursorTile_ADDR) != 0u ? 0x80u : 0x00u;',
        'case_ids': ['WaitForButtonAorB-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawWideTextBox_WaitForInput': {   'source_symbol': 'DrawWideTextBox_WaitForInput',
        'before': 'WaitResult DrawWideTextBox_WaitForInput(uint16_t hl)\n'
                  '{\n'
                  '\t(void)DrawWideTextBox_PrintText(hl);',
        'after': 'WaitResult DrawWideTextBox_WaitForInput(uint16_t hl)\n{\n\t;',
        'case_ids': ['DrawWideTextBox_WaitForInput-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'WaitForWideTextBoxInput': {   'source_symbol': 'WaitForWideTextBoxInput',
        'before': '\tuint16_t params = WTBM_PARAMS;\n\tInitializeMenuParameters(0, &params);',
        'after': '\tuint16_t params = WTBM_PARAMS;\n\t;',
        'case_ids': ['WaitForWideTextBoxInput-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'RefreshMenuCursor_CheckPlaySFX': {   'source_symbol': 'RefreshMenuCursor_CheckPlaySFX',
        'before': '\t\tPlaySFX(a);',
        'after': '\t\tPlaySFX(0u);',
        'case_ids': ['RefreshMenuCursor_CheckPlaySFX-1', 'RefreshMenuCursor_CheckPlaySFX-2'],
        'source': 'src/profiles/extended/home/menus.c'},
    'PlayOpenOrExitScreenSFX': {   'source_symbol': 'PlayOpenOrExitScreenSFX',
        'before': 'if ((uint8_t)(item + 1u) == 0u)',
        'after': 'if ((uint8_t)(item + 2u) == 0u)',
        'case_ids': ['PlayOpenOrExitScreenSFX-0', 'PlayOpenOrExitScreenSFX-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'HandleYesOrNoMenu': {   'source_symbol': 'HandleYesOrNoMenu',
        'before': '\twCurMenuItem = (uint8_t)(wDefaultYesOrNo ^ 1u);',
        'after': '\twCurMenuItem = (uint8_t)(wDefaultYesOrNo ^ 0u);',
        'case_ids': ['HandleYesOrNoMenu-0', 'HandleYesOrNoMenu-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'CopyCardNameAndLevel': {   'source_symbol': 'CopyCardNameAndLevel',
        'before': '\treturn _CopyCardNameAndLevel(a, b, c, d, e);',
        'after': '\treturn _CopyCardNameAndLevel((uint8_t)(a + 1u), b, c, d, e);',
        'case_ids': ['CopyCardNameAndLevel-0', 'CopyCardNameAndLevel-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'ReloadCardListItems': {   'source_symbol': 'ReloadCardListItems',
        'before': 'uint8_t up = SYM_SPACE;',
        'after': 'uint8_t up = SYM_CURSOR_U;',
        'case_ids': ['ReloadCardListItems-0', 'ReloadCardListItems-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'PrintCardListItems': {   'source_symbol': 'PrintCardListItems',
        'before': '\twMenuYSeparation = 2u;',
        'after': '\twMenuYSeparation = 3u;',
        'case_ids': ['PrintCardListItems-0', 'PrintCardListItems-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'CardListMenuFunction': {   'source_symbol': 'CardListMenuFunction',
        'before': '\tif (list_fn == CARD_LIST_FUNCTION) {\n'
                  '\t\tCardListFunctionResult r = CardListFunction();\n'
                  '\t\treturn (CardListMenuFunctionResult){r.a, r.f};\n'
                  '\t}',
        'after': '\tif (list_fn == CARD_LIST_FUNCTION)\n'
                 '\t\treturn (CardListMenuFunctionResult){0u, 0x00u};',
        'case_ids': ['CardListMenuFunction-4', 'CardListMenuFunction-5'],
        'source': 'src/profiles/extended/home/menus.c'},
    'HandleMenuInput': {   'source_symbol': 'HandleMenuInput',
        'before': '\t\t} else if (update == PLAY_AREA_SCREEN_MENU_FUNCTION) {\n'
                  '\t\t\tupdate_f = PlayAreaScreenMenuFunction();',
        'after': '\t\t} else if (update == PLAY_AREA_SCREEN_MENU_FUNCTION) {\n'
                 '\t\t\tupdate_f = CardListMenuFunction().f;',
        'case_ids': ['HandleMenuInput-4'],
        'source': 'src/profiles/extended/home/menus.c'},
    'HandleCardListInput': {   'source_symbol': 'HandleCardListInput',
        'before': '\tHandleCardListInputResult result = {input.a, input.d, input.e, input.f};',
        'after': '\tHandleCardListInputResult result = {input.a, 0u, input.e, input.f};',
        'case_ids': ['HandleCardListInput-3'],
        'source': 'src/profiles/extended/home/menus.c'},
    'HandleDuelMenuInput': {   'source_symbol': 'HandleDuelMenuInput',
        'before': '\t\tif ((b & (PAD_UP | PAD_DOWN)) != 0u) {',
        'after': '\t\tif ((b & (PAD_UP | PAD_DOWN)) == 0u) {',
        'case_ids': ['HandleDuelMenuInput-0'],
        'source': 'src/profiles/extended/home/menus.c'},
    'YesOrNoMenuWithText_LeftAligned': {   'source_symbol': 'YesOrNoMenuWithText_LeftAligned',
        'before': '\treturn HandleYesOrNoMenu(2u, 16u, b, c);',
        'after': '\treturn (HandleYesOrNoMenuResult){0u, 0x80u};',
        'case_ids': ['YesOrNoMenuWithText_LeftAligned-0', 'YesOrNoMenuWithText_LeftAligned-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'TwoItemHorizontalMenu': {   'source_symbol': 'TwoItemHorizontalMenu',
        'before': '\tEnableLCD();\n'
                  '\t/* jp target lands inside .refresh_menu, whose own xor $1 flips */\n'
                  '\t/* wCurMenuItem unconditionally before the wait loop begins. */\n'
                  '\twCurMenuItem = (uint8_t)(wCurMenuItem ^ 1u);',
        'after': '\tEnableLCD();\n'
                 '\t/* jp target lands inside .refresh_menu, whose own xor $1 flips */\n'
                 '\t/* wCurMenuItem unconditionally before the wait loop begins. */\n',
        'case_ids': ['TwoItemHorizontalMenu-0', 'TwoItemHorizontalMenu-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'YesOrNoMenu': {   'source_symbol': 'YesOrNoMenu',
        'before': '\treturn HandleYesOrNoMenu(6u, 16u, 0u, 0u);',
        'after': '\treturn HandleYesOrNoMenu(7u, 16u, 0u, 0u);',
        'case_ids': ['YesOrNoMenu-0', 'YesOrNoMenu-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'YesOrNoMenuWithText': {   'source_symbol': 'YesOrNoMenuWithText',
        'before': 'HandleYesOrNoMenuResult YesOrNoMenuWithText(uint16_t hl)\n'
                  '{\n'
                  '\t(void)DrawWideTextBox_PrintText(hl);',
        'after': 'HandleYesOrNoMenuResult YesOrNoMenuWithText(uint16_t hl)\n'
                 '{\n'
                 '\t(void)DrawWideTextBox_PrintText(0u);',
        'case_ids': ['YesOrNoMenuWithText-0', 'YesOrNoMenuWithText-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'YesOrNoMenuWithText_SetCursorToYes': {   'source_symbol': 'YesOrNoMenuWithText_SetCursorToYes',
        'before': 'HandleYesOrNoMenuResult YesOrNoMenuWithText_SetCursorToYes(uint16_t hl)\n'
                  '{\n'
                  '\twDefaultYesOrNo = 1u;',
        'after': 'HandleYesOrNoMenuResult YesOrNoMenuWithText_SetCursorToYes(uint16_t hl)\n'
                 '{\n'
                 '\twDefaultYesOrNo = 0u;',
        'case_ids': [   'YesOrNoMenuWithText_SetCursorToYes-0',
                        'YesOrNoMenuWithText_SetCursorToYes-1'],
        'source': 'src/profiles/extended/home/menus.c'},
    'DrawTextBox_PrintTextNoDelay': {   'source_symbol': 'DrawTextBox_PrintTextNoDelay',
        'before': '\tInitTextPrintingInTextbox(a, d, e);',
        'after': '\tInitTextPrintingInTextbox(a, d, (uint8_t)(e + 1u));',
        'case_ids': ['DrawTextBox_PrintTextNoDelay-1', 'DrawTextBox_PrintTextNoDelay-2'],
        'source': 'src/profiles/extended/home/menus.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record in SCHEMA2_CASES["HandleCardListInput"][3:]:
    _record["completion"] = {"mode": "entry", "pc": 0x1F2E, "bank": 0,
                             "routine": "CardListMenuFunction"}
CASES["WaitForButtonAorB"][3].update({
    "oracle": False,
    "evidence": "native-stress",
    "why": "The full seeded text and VRAM fixture exercises frame-driven cursor rendering whose scratch screen map is not stable in the isolated native oracle.",
    "expect_regs": {"f": 0x80},
})
CASES["YesOrNoMenu"][2].update({
    "oracle": False,
    "evidence": "native-stress",
    "why": "The full seeded text and VRAM fixture exercises frame-driven cursor rendering whose scratch screen map is not stable in the isolated native oracle.",
    "expect_regs": {"a": 0x00, "f": 0x80},
})
SCHEMA2_CASES["HandleCardListInput"][3]["compare"] = ()
SCHEMA2_CASES["WaitForButtonAorB"][3]["evidence"] = "native-stress"
SCHEMA2_CASES["YesOrNoMenu"][2]["evidence"] = "native-stress"
CASES["HandleCardListInput"][3]["compare"] = ()
