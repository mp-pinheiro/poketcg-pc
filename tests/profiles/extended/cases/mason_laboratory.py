"""Extended oracle-diff cases for mason_laboratory, seeded from tests/cases/mason_laboratory.py."""

CONTRACT = {
    'Preload_DrMason': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Preload_Sam': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Preload_Tech5': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'MasonLaboratoryAfterDuel': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': (), 'wram_out': True},
    'MasonLabCloseTextBox': {'compare': (), 'preserve': ()},
    'MasonLabLoadMap': {'compare': (), 'preserve': ()},
    'MasonLabPressedA': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ()},
    'Func_d703': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Script_Tech1': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ()},
}

CASES = {
    'Preload_DrMason': [
        {   'wram': {0xD3CE: b'\x00', 0xD39A: b'U', 0xD39B: b'f'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\xff', 0xD39A: b'U', 0xD39B: b'f'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01}},
        {   'wram': {0xD3CE: b'\x02', 0xD39A: b'U', 0xD39B: b'f'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\xf2', 0xD39A: b'U', 0xD39B: b'f'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01}},
        {   'wram': {0xD3CE: b'\x04', 0xD39A: b'U', 0xD39B: b'f'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\x01', 0xD39A: b'U', 0xD39B: b'f'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01}},
    ],
    'Preload_Sam': [
        {   'wram': {0xD3CE: b'\x00', 0xD39A: b'U', 0xD39B: b'f', 0xD39C: b'w', 0xD3C0: b'\x00'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01, 0xD39C: 0x01, 0xD3C0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\xf1', 0xD39A: b'U', 0xD39B: b'f', 0xD39C: b'w', 0xD3C0: b'\x00'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01, 0xD39C: 0x01, 0xD3C0: 0x01}},
        {   'wram': {0xD3CE: b'\x02', 0xD39A: b'U', 0xD39B: b'f', 0xD39C: b'w', 0xD3C0: b'\x00'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01, 0xD39C: 0x01, 0xD3C0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\xf3', 0xD39A: b'U', 0xD39B: b'f', 0xD39C: b'w', 0xD3C0: b'\x00'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01, 0xD39C: 0x01, 0xD3C0: 0x01}},
        {   'wram': {0xD3CE: b'\x04', 0xD39A: b'U', 0xD39B: b'f', 0xD39C: b'w', 0xD3C0: b'\x00'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01, 0xD39C: 0x01, 0xD3C0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\x0e', 0xD39A: b'U', 0xD39B: b'f', 0xD39C: b'w', 0xD3C0: b'\x00'},
            'read': {0xD3CE: 0x01, 0xD39A: 0x01, 0xD39B: 0x01, 0xD39C: 0x01, 0xD3C0: 0x01}},
    ],
    'Preload_Tech5': [
        {   'wram': {0xD3C7: b'\x00', 0xD39A: b'U', 0xD3C0: b'\x00'},
            'read': {0xD3C7: 0x01, 0xD39A: 0x01, 0xD3C0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\xfd', 0xD39A: b'U', 0xD3C0: b'\x00'},
            'read': {0xD3C7: 0x01, 0xD39A: 0x01, 0xD3C0: 0x01}},
        {   'wram': {0xD3C7: b'\x02', 0xD39A: b'U', 0xD3C0: b'\x00'},
            'read': {0xD3C7: 0x01, 0xD39A: 0x01, 0xD3C0: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\xff', 0xD39A: b'\xfe', 0xD3C0: b'\x00'},
            'read': {0xD3C7: 0x01, 0xD39A: 0x01, 0xD3C0: 0x01}},
    ],
    'MasonLaboratoryAfterDuel': [
        {'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
        {   'wram': {   0xD0B0: b'\x00',
                        0xD0B1: b'\x07',
                        0xD337: b'\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD397: b'\xee',
                        0xD3A3: b'\xaa',
                        0xD321: b'\x01',
                        0xD0AE: b'\x00',
                        0xD0B3: b'\xff\xff',
                        0xD0AC: b'\x00'},
            'expect': {0xD399: b'\x07', 0xD3A3: b'\x00', 0xD0AC: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0B0: b'\x01', 0xD0B1: b'\x99'}},
    ],
    'MasonLabCloseTextBox': [
        {   'wram': {0xD319: b'\x00\x01\x00', 0xD11E: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD27F: 0x01, 0xD319: 0x03, 0xD120: 0x0100}},
        {   'wram': {0xD319: b'\x00\x02\x00', 0xD11E: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD27F: 0x01, 0xD319: 0x03, 0xD120: 0x0100}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD319: b'\x00\x03\x00', 0xD11E: b'\x00', 0xCAB4: b'\x00'},
            'read': {0xD27F: 0x01, 0xD319: 0x03, 0xD120: 0x0100}},
    ],
    'MasonLabLoadMap': [
        {   'wram': {0xD3CE: b'\x00', 0xD399: b'\x00', 0xD0B3: b'\x00\x00'},
            'read': {0xD399: 0x01, 0xD0B3: 0x02}},
        {   'wram': {0xD3CE: b'\x06', 0xD399: b'\x00', 0xD0B3: b'\x00\x00'},
            'read': {0xD399: 0x01, 0xD0B3: 0x02}},
        {   'wram': {0xD3CE: b'\x08', 0xD399: b'\x00', 0xD0B3: b'\x00\x00'},
            'read': {0xD399: 0x01, 0xD0B3: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3CE: b'\x00', 0xD399: b'\x00', 0xD0B3: b'\x00\x00'},
            'read': {0xD399: 0x01, 0xD0B3: 0x02}},
    ],
    'MasonLabPressedA': [
        {   'wram': {   0xD3C7: b'\x00',
                        0xD31D: b'\n',
                        0xD31E: b'\x04',
                        0xD321: b'\x00',
                        0xD0B3: b'\x00\x00'},
            'read': {0xD0B3: 0x02}},
        {   'wram': {   0xD3C7: b'\x02',
                        0xD31D: b'\n',
                        0xD31E: b'\x04',
                        0xD321: b'\x00',
                        0xD0B3: b'\x00\x00'},
            'read': {0xD0B3: 0x02}},
        {   'wram': {   0xD3C7: b'\x02',
                        0xD31D: b'\x0c',
                        0xD31E: b'\x04',
                        0xD321: b'\x00',
                        0xD0B3: b'\x00\x00'},
            'read': {0xD0B3: 0x02}},
        {   'wram': {   0xD3C7: b'\x02',
                        0xD31D: b'\n',
                        0xD31E: b'\x04',
                        0xD321: b'\x02',
                        0xD0B3: b'\x00\x00'},
            'read': {0xD0B3: 0x02}},
        {   'wram': {0xD3C7: b'\x02', 0xD31D: b'3', 0xD31E: b'D', 0xD321: b'\x00', 0xD0B3: b'\x00\x00'},
            'read': {0xD0B3: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD3C7: b'\x02',
                        0xD31D: b'\n',
                        0xD31E: b'\x04',
                        0xD321: b'\x00',
                        0xD0B3: b'\x00\x00'},
            'read': {0xD0B3: 0x02}},
    ],
    'Func_d703': [
        {'wram': {0xD3C7: b'\x00'}, 'read': {0xD3C7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\x00'},
            'read': {0xD3C7: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3C7: b'\x01'},
            'read': {0xD3C7: 0x01}},
    ],
    'Script_Tech1': [
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'sram': {   0x00: {   0xA100: b'\x00\x02\x02\x02\x02\x01\x01\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'sread': {0x00: {0xA100: 0x08}},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'sram': {   0x00: {   0xA100: b'\x00\x02\x02\x02\x02\x02\x02\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'sread': {0x00: {0xA100: 0x08}},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'sram': {   0x00: {   0xA100: b'\x00\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'sread': {0x00: {0xA100: 0x08}},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0x00,
            'f': 0x00,
            'b': 0x00,
            'c': 0x00,
            'd': 0x00,
            'e': 0x00,
            'hl': 0x00,
            'sram': {   0x00: {   0xA100: b'\x00\x02\x02\x02\x01\x01\x01\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'sread': {0x00: {0xA100: 0x08}},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'sram': {   0x00: {   0xA100: b'\x00\x02\x02\x02\x02\x02\x02\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00'}},
            'sread': {0x00: {0xA100: 0x08}},
            'instruction_budget': 0x3938700,
            'cycle_budget': 0xE4E1C00},
    ],
}

MUTATIONS = {
    'Preload_DrMason': {   'source_symbol': 'Preload_DrMason',
        'before': '\tif (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) != 0u)',
        'after': '\tif (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) == 0u)',
        'case_ids': [   'Preload_DrMason-5',
                        'Preload_DrMason-0',
                        'Preload_DrMason-1',
                        'Preload_DrMason-2',
                        'Preload_DrMason-3',
                        'Preload_DrMason-4'],
        'source': 'src/home/mason_laboratory.c'},
    'Preload_Sam': {   'source_symbol': 'Preload_Sam',
        'before': 'if (state < MASON_LAB_IN_PRACTICE_DUEL) {',
        'after': 'if (state >= MASON_LAB_IN_PRACTICE_DUEL) {',
        'case_ids': [   'Preload_Sam-0',
                        'Preload_Sam-1',
                        'Preload_Sam-2',
                        'Preload_Sam-3',
                        'Preload_Sam-4',
                        'Preload_Sam-5'],
        'source': 'src/home/mason_laboratory.c'},
    'Preload_Tech5': {   'source_symbol': 'Preload_Tech5',
        'before': 'uint8_t moved = (uint8_t)(gb_read8(hl) + 2u);',
        'after': 'uint8_t moved = (uint8_t)(gb_read8(hl) + 1u);',
        'case_ids': ['Preload_Tech5-2', 'Preload_Tech5-0', 'Preload_Tech5-1', 'Preload_Tech5-3'],
        'source': 'src/home/mason_laboratory.c'},
    'MasonLaboratoryAfterDuel': {   'source_symbol': 'MasonLaboratoryAfterDuel',
        'before': '\tFindEndOfDuelScriptResult r = '
                  'FindEndOfDuelScript(MasonLaboratoryAfterDuelTable);',
        'after': '\tFindEndOfDuelScriptResult r = '
                 'FindEndOfDuelScript((uint16_t)(MasonLaboratoryAfterDuelTable + 1u));',
        'case_ids': ['MasonLaboratoryAfterDuel-0'],
        'source': 'src/home/mason_laboratory.c'},
    'MasonLabCloseTextBox': {   'source_symbol': 'MasonLabCloseTextBox',
        'before': '\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_CHALLENGE_MACHINE);',
        'after': '\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_CHALLENGE_MACHINE + 1u));',
        'case_ids': ['MasonLabCloseTextBox-0', 'MasonLabCloseTextBox-1'],
        'source': 'src/home/mason_laboratory.c'},
    'MasonLabLoadMap': {   'source_symbol': 'MasonLabLoadMap',
        'before': '\tif (GetEventValue(EVENT_MASON_LAB_STATE) >= MASON_LAB_RECEIVED_STARTER_DECK)',
        'after': '\tif (GetEventValue(EVENT_MASON_LAB_STATE) > MASON_LAB_RECEIVED_STARTER_DECK)',
        'case_ids': ['MasonLabLoadMap-1'],
        'source': 'src/home/mason_laboratory.c'},
    'MasonLabPressedA': {   'source_symbol': 'MasonLabPressedA',
        'before': '\tif (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) == 0u)',
        'after': '\tif (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) != 0u)',
        'case_ids': ['MasonLabPressedA-0'],
        'source': 'src/home/mason_laboratory.c'},
    'Func_d703': {   'source_symbol': 'Func_d703',
        'before': 'if (event == 0u)',
        'after': 'if (event != 0u)',
        'case_ids': ['Func_d703-0', 'Func_d703-1'],
        'source': 'src/home/mason_laboratory.c'},
    'Script_Tech1': {   'source_symbol': 'Script_Tech1',
        'before': '\tif (a >= 10u)',
        'after': '\tif (a > 10u)',
        'case_ids': ['Script_Tech1-0'],
        'source': 'src/profiles/extended/home/mason_laboratory.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record, _high in zip(SCHEMA2_CASES["Script_Tech1"], (True, True, False, False, True)):
    _record["completion"] = {"mode": "pre-ret", "pc": 0x53DB if _high else 0x53FC, "bank": 3}
