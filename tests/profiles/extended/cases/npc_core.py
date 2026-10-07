"""Extended oracle-diff cases for npc_core, seeded from tests/cases/npc_core.py."""

CONTRACT = {
    'CheckIfNPCIsRonald': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('a', 'b', 'c', 'd', 'e', 'hl')},
    'UpdateNPCAnimation': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ('f', 'b', 'c', 'hl')},
    'ApplyRandomCountToNPCAnim': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ('f', 'b', 'c', 'hl')},
    'SetNPCAnimation': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'SetNPCDirection': {'compare': ('a', 'hl'), 'preserve': ('hl',)},
    'StartNPCMovement': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('hl',)},
    'Func_1c5e9': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'UpdateNPCPosition': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'UpdateNPCSpritePosition': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CheckIsAnNPCMoving': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'UpdateNPCsTilePermission': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'SetNPCsTilePermission': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'SetNPCPosition': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Func_1c53f': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'GetNPCDirection': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetNPCPosition': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('hl',)},
    'UpdateIsAnNPCMovingFlag': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'ClearNPCs': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'SetAllNPCTilePermissions': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Func_1c557': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadNPC': {   'compare': ('a', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'SetNewScriptNPC': {'compare': ('a', 'f', 'b', 'c', 'hl'), 'preserve': ('hl',), 'wram_out': True},
    'UnloadNPC': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Func_1c52e': {'compare': ('a', 'b', 'c', 'hl'), 'preserve': ('b', 'c', 'hl')},
    'UpdateNPCMovementStep': {   'compare': ('a', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'wram_out': True},
    'FindNPCAtLocation': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'HandleAllNPCMovement': {'compare': (), 'preserve': (), 'wram_out': True},
}

CASES = {
    'CheckIfNPCIsRonald': [
        {},
        {'a': 0x00},
        {'a': 0x01},
        {'a': 0x02},
        {'a': 0x71},
        {'a': 0x72},
        {'a': 0x73},
        {'a': 0xFF},
        {'a': 0x02, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x71, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x72, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x00, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0xFF, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'UpdateNPCAnimation': [
        {},
        {'wram': {0xD397: b'\x03'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD4BC: b'7'}},
        {   'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD33B: b'\x02',
                     0xD33C: b'\x00',
                     0xD4BC: b'\x00',
                     0xD4CF: b'\x33'},
            'read': {0xD4BC: 0x01}},
        {   'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD33B: b'\x02',
                     0xD33C: b'\x10',
                     0xD4BC: b'\x00',
                     0xD4CF: b'\x44'},
            'read': {0xD4BC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD33B: b'\x02',
                     0xD33C: b'\x10',
                     0xD4BC: b'\x00',
                     0xD4CF: b'\x55'},
            'read': {0xD4BC: 0x01}},
    ],
    'ApplyRandomCountToNPCAnim': [
        {},
        {'wram': {0xD397: b'\x01'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD4BC: b'd'}},
        {   'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD4BC: b'\x05',
                     0xD4CF: b'\x33'},
            'read': {0xD4BC: 0x01}},
        {   'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD4BC: b'\xff',
                     0xD4CF: b'\x44'},
            'read': {0xD4BC: 0x01}},
        {   'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD4BC: b'\x00',
                     0xD4CF: b'\x55'},
            'read': {0xD4BC: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x00',
                     0xD337: b'\x01',
                     0xD338: b'\x00',
                     0xD4BC: b'\x05',
                     0xD4CF: b'\x66'},
            'read': {0xD4BC: 0x01}},
    ],
    'SetNPCAnimation': [
        {'a': 0x00, 'wram': {0xD397: b'\x00'}, 'read': {0xD2ED: 0x0100}},
        {'a': 0x01, 'wram': {0xD397: b'\x01'}, 'read': {0xD2ED: 0x0100}},
        {'a': 0xFF, 'wram': {0xD397: b'\x02'}, 'read': {0xD2ED: 0x0100}},
        {   'a': 0x33,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x01'},
            'read': {0xD2ED: 0x0100}},
    ],
    'SetNPCDirection': [
        {'a': 0x00, 'wram': {0xD397: b'\x00'}, 'read': {0xD2ED: 0x0100}},
        {'a': 0x01, 'wram': {0xD397: b'\x01'}, 'read': {0xD2ED: 0x0100}},
        {'a': 0xFF, 'wram': {0xD397: b'\x02'}, 'read': {0xD2ED: 0x0100}},
        {   'a': 0x02,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x01'},
            'read': {0xD2ED: 0x0100}},
    ],
    'StartNPCMovement': [
        {'b': 0x00, 'c': 0x00},
        {'b': 0xC1, 'c': 0x00, 'wram': {0xC100: b'\x02'}, 'read': {0xC100: 0x01}},
        {'b': 0xC1, 'c': 0x00, 'wram': {0xC100: b'\x81\x00'}, 'read': {0xC100: 0x02}},
        {'b': 0xC1, 'c': 0x00, 'wram': {0xC100: b'\xf5\x02\x00\x00\x03'}, 'read': {0xC100: 0x05}},
        {'b': 0xC1, 'c': 0x01, 'wram': {0xC100: b'\x00\xf5\xfe'}, 'read': {0xC100: 0x03}},
        {'b': 0xC1, 'c': 0x00, 'wram': {0xC100: b'\xff', 0xD397: b'\x02'}, 'read': {0xC100: 0x01}},
        {'b': 0xC1, 'c': 0x00, 'wram': {0xC100: b'\xef\x7f'}, 'read': {0xC100: 0x02}},
        {'b': 0xC1, 'c': 0x00, 'wram': {0xC100: b'\xf0\x01\x02'}, 'read': {0xC100: 0x03}},
        {   'b': 0xC1,
            'c': 0x00,
            'wram': {   0xC100: b'\xf1\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x01'},
            'read': {0xC100: 0x81}},
        {   'b': 0xC1,
            'c': 0x82,
            'wram': {0xC103: b'\x06', 0xC182: b'\xf3\x80'},
            'read': {0xC103: 0x01, 0xC182: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xC1,
            'c': 0x00,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC100: b'\x01'},
            'read': {0xC100: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xC1,
            'c': 0x02,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC102: b'\x81\x05'},
            'read': {0xC102: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xC1,
            'c': 0x00,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xC100: b'\xff'},
            'read': {0xC100: 0x01}},
        {   'b': 0x58,
            'c': 0x96,
            'd': 0x14,
            'e': 0x17,
            'hl': 0x4E4A,
            'wram': {0xC100: b'\xff'},
            'read': {0xC100: 0x01}},
    ],
    'Func_1c5e9': [
        {'read': {0xD2ED: 0x0200}},
        {   'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x00'},
            'read': {0xD2ED: 0x0200}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x01'},
            'read': {0xD2ED: 0x0200}},
    ],
    'UpdateNPCPosition': [
        {'wram': {0xD397: b'\x00', 0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00'}, 'read': {0xD337: 0x08}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x00', 0xD337: b'\x11"0@\x00\x00\x00\x00'},
            'read': {0xD337: 0x08}},
        {'wram': {0xD397: b'\x00', 0xD337: b'\x11"0@\x01\x00\x00\x00'}, 'read': {0xD337: 0x08}},
        {'wram': {0xD397: b'\x00', 0xD337: b'\x11"0@\x02\x00\x00\x00'}, 'read': {0xD337: 0x08}},
        {'wram': {0xD397: b'\x00', 0xD337: b'\x11"0@\x03\x00\x00\x00'}, 'read': {0xD337: 0x08}},
        {   'wram': {   0xD397: b'\x01',
                        0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11"0@'
                                b'\x01\x00\x00\x00'},
            'read': {0xD337: 0x14}},
    ],
    'UpdateNPCSpritePosition': [
        {   'hl': 0xD399,
            'wram': {0xD39B: b'\x01\x02', 0xD39E: b'\x00', 0xD4BC: b'\x00'},
            'hram': {0xFF92: b' ', 0xFF93: b'0'},
            'read': {   0xD39E: 0x01,
                        0xFF92: 0x01,
                        0xFF93: 0x01,
                        0xD4BC: 0x01,
                        0xD39B: 0x01,
                        0xD39C: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xD399,
            'wram': {0xD39B: b'\x10 ', 0xD39D: b'\x01', 0xD39E: b' ', 0xD3A1: b'\x08', 0xD4BC: b'\x00'},
            'hram': {0xFF92: b' ', 0xFF93: b'0'},
            'read': {   0xD39E: 0x01,
                        0xD39D: 0x01,
                        0xD3A1: 0x01,
                        0xFF92: 0x01,
                        0xFF93: 0x01,
                        0xD4BC: 0x01,
                        0xD39B: 0x01,
                        0xD39C: 0x01}},
    ],
    'CheckIsAnNPCMoving': [
        {'wram': {0xD3A4: b'\x00'}},
        {'wram': {0xD3A4: b'\x01'}},
        {'wram': {0xD3A4: b' '}},
        {'wram': {0xD3A4: b'!'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3A4: b' '}},
    ],
    'UpdateNPCsTilePermission': [
        {   'wram': {0xD397: b'\x00', 0xD339: b'\x00\x00', 0xD120: b'\xff'},
            'expect': {0xD120: b'\xbf'},
            'expect_regs': {'a': 0xBF}},
        {   'wram': {0xD397: b'\x01', 0xD343: b'\x04\x06', 0xD152: b'@'},
            'expect': {0xD152: b'\x00'},
            'expect_regs': {'a': 0x00}},
        {   'wram': {0xD397: b'\x07', 0xD389: b'\x0e\x10', 0xD1A7: b'\x7f'},
            'expect': {0xD1A7: b'?'},
            'expect_regs': {'a': 0x3F}},
        {   'wram': {0xD397: b'\x08', 0xD339: b'\x02\x04', 0xD141: b'\xff'},
            'expect': {0xD141: b'\xbf'},
            'expect_regs': {'a': 0xBF}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\xaa', 0xD339: b'\x08\n', 0xD170: b'\xff'},
            'expect': {0xD170: b'\xbf'},
            'expect_regs': {'a': 0xBF}},
    ],
    'SetNPCsTilePermission': [
        {   'wram': {0xD397: b'\x00', 0xD339: b'\x00\x00', 0xD120: b'\xff'},
            'expect': {0xD120: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'wram': {0xD397: b'\x01', 0xD343: b'\x04\x06', 0xD152: b'@'},
            'expect': {0xD152: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'wram': {0xD397: b'\x07', 0xD389: b'\x0e\x10', 0xD1A7: b'\x7f'},
            'expect': {0xD1A7: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'wram': {0xD397: b'\x08', 0xD339: b'\x02\x04', 0xD141: b'\xff'},
            'expect': {0xD141: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\xaa', 0xD339: b'\x08\n', 0xD170: b'\xff'},
            'expect': {0xD170: b'@'},
            'expect_regs': {'a': 0x40}},
    ],
    'SetNPCPosition': [
        {   'b': 0x04,
            'c': 0x06,
            'wram': {0xD397: b'\x00', 0xD339: b'\x00\x00', 0xD120: b'\xff', 0xD152: b'\x00'},
            'expect': {0xD120: b'\xbf', 0xD152: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'b': 0x0E,
            'c': 0x10,
            'wram': {0xD397: b'\x01', 0xD343: b'\x04\x06', 0xD152: b'\xff', 0xD1A7: b'\x7f'},
            'expect': {0xD152: b'\xbf', 0xD1A7: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'b': 0x02,
            'c': 0x04,
            'wram': {0xD397: b'\x07', 0xD389: b'\x0e\x10', 0xD1A7: b'\xff', 0xD141: b'\x00'},
            'expect': {0xD1A7: b'\xbf', 0xD141: b'@'},
            'expect_regs': {'a': 0x40}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x12,
            'c': 0x14,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\xaa', 0xD339: b'\x08\n', 0xD170: b'\xff', 0xD1C9: b'\x00'},
            'expect': {0xD170: b'\xbf', 0xD1C9: b'@'},
            'expect_regs': {'a': 0x40, 'b': 0x12, 'c': 0x14, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234}},
    ],
    'Func_1c53f': [
        {   'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x00'},
            'read': {0xD2ED: 0x0200}},
        {   'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x01'},
            'read': {0xD2ED: 0x0200}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x02'},
            'read': {0xD2ED: 0x0200}},
    ],
    'GetNPCDirection': [
        {'wram': {0xD397: b'\x00', 0xD33B: b'*'}, 'read': {0xD33B: 0x01}},
        {'wram': {0xD397: b'\x07', 0xD38F: b'\x91'}, 'read': {0xD38F: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x08', 0xD33B: b'~'},
            'read': {0xD33B: 0x01}},
    ],
    'GetNPCPosition': [
        {'wram': {0xD397: b'\x00', 0xD339: b'\x124'}, 'read': {0xD339: 0x02}},
        {'wram': {0xD397: b'\x01', 0xD345: b'Vx'}, 'read': {0xD345: 0x02}},
        {'wram': {0xD397: b'\x07', 0xD38F: b'\x9a\xbc'}, 'read': {0xD38F: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x07', 0xD38F: b'\xde\xf0'},
            'read': {0xD38F: 0x02}},
    ],
    'UpdateIsAnNPCMovingFlag': [
        {   'hl': 0xC4F0,
            'wram': {0xD3A4: b'\x00', 0xC4F5: b'\x00'},
            'expect': {0xD3A4: b'\x00'},
            'expect_regs': {'a': 0x00, 'f': 0x80}},
        {   'hl': 0xC4F0,
            'wram': {0xD3A4: b'\x01', 0xC4F5: b'\x02'},
            'expect': {0xD3A4: b'\x03'},
            'expect_regs': {'a': 0x03, 'f': 0x00}},
        {   'hl': 0xC4F0,
            'wram': {0xD3A4: b'\x80', 0xC4F5: b'\x01'},
            'expect': {0xD3A4: b'\x81'},
            'expect_regs': {'a': 0x81, 'f': 0x00}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC4F0,
            'wram': {0xD3A4: b' ', 0xC4F5: b'\x04'},
            'expect': {0xD3A4: b'$'},
            'expect_regs': {'a': 0x24, 'f': 0x00}},
    ],
    'ClearNPCs': [
        {   'wram': {   0xD337: b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                                b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
                        0xD336: b'\x7f',
                        0xD3A5: b'\x01'},
            'expect': {   0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                          0xD336: b'\x00',
                          0xD3A5: b'\x00'},
            'expect_regs': {'a': 0x00, 'f': 0xC0}},
        {   'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_",
                        0xD336: b'\xaa',
                        0xD3A5: b'\xbb'},
            'expect': {   0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                          0xD336: b'\x00',
                          0xD3A5: b'\x00'},
            'expect_regs': {'a': 0x00, 'f': 0xC0}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'
                                b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'
                                b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'
                                b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'
                                b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'
                                b'\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5',
                        0xD336: b'Z',
                        0xD3A5: b'\xc3'},
            'expect': {   0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                          0xD336: b'\x00',
                          0xD3A5: b'\x00'},
            'expect_regs': {   'a': 0x00,
                               'f': 0xC0,
                               'b': 0xBB,
                               'c': 0xCC,
                               'd': 0xDD,
                               'e': 0xEE,
                               'hl': 0x1234}},
    ],
    'SetAllNPCTilePermissions': [
        {   'wram': {   0xD337: b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD120: b'\xff'},
            'expect': {0xD120: b'@'},
            'expect_regs': {'a': 0x00, 'f': 0xC0}},
        {   'wram': {   0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x01\x00\x0e\x10\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD1A7: b'\x7f'},
            'expect': {0xD1A7: b'@'},
            'expect_regs': {'a': 0x40, 'f': 0xC0}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD397: b'w'},
            'expect_regs': {'a': 0x00, 'f': 0xC0}},
    ],
    'Func_1c557': [
        {   'a': 0xF0,
            'wram': {   0xD397: b'\x07',
                        0xD399: b'D',
                        0xD337: b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10'
                                b'\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$'
                                b"%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"},
            'read': {0xD337: 0x60}},
        {   'a': 0x12,
            'wram': {   0xD397: b'\x07',
                        0xD399: b'D',
                        0xD337: b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\x12"#$7&\'()*+,'
                                b'\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCD'
                                b'EFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'},
            'read': {0xD337: 0x60},
            'expect': {0xD34A: b'7', 0xD397: b'\x07', 0xD399: b'D'}},
        {   'a': 0x60,
            'wram': {   0xD397: b'\x00',
                        0xD399: b'\x01',
                        0xD337: b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10'
                                b'\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$'
                                b"%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"},
            'read': {0xD337: 0x60}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD397: b'\x03',
                        0xD399: b'U',
                        0xD337: b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10'
                                b'\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$'
                                b"%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"},
            'read': {0xD337: 0x60}},
    ],
    'LoadNPC': [
        {   'wram': {   0xD337: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'},
            'expect': {0xD397: b'\x00'},
            'expect_regs': {'a': 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
                                b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01',
                        0xD397: b'\xaa'},
            'expect': {0xD397: b'\x00'},
            'expect_regs': {'a': 0x01, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234}},
    ],
    'SetNewScriptNPC': [
        {   'hl': 0x4567,
            'wram': {   0xD397: b'\x00',
                        0xD321: b'\x01',
                        0xD0AE: b'\x00',
                        0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'expect': {0xD33B: b'\x03', 0xD0AE: b'\x02'},
            'read': {0xD0B6: 0x02}},
        {   'hl': 0x00,
            'wram': {   0xD397: b'\x01',
                        0xD321: b'\x03',
                        0xD0AE: b'\x80',
                        0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'expect': {0xD347: b'\x01', 0xD0AE: b'\x82'},
            'read': {0xD0B6: 0x02}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD397: b'\x00',
                        0xD321: b'\x02',
                        0xD0AE: b'\x04',
                        0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'expect': {0xD33B: b'\x00', 0xD0AE: b'\x06'},
            'read': {0xD0B6: 0x02}},
    ],
    'UnloadNPC': [
        {},
        {   'wram': {0xD397: b'\x00', 0xD337: b'\x01\x02\x00\x00', 0xD336: b'\x03'},
            'expect': {0xD337: b'\x00\x02', 0xD336: b'\x02'}},
        {   'wram': {0xD397: b'\x00', 0xD337: b'q\x03\x00\x00', 0xD336: b'\x02', 0xD3A5: b'\x01'},
            'expect': {0xD337: b'\x00\x03', 0xD336: b'\x01', 0xD3A5: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x01', 0xD343: b'\x01\x04\x00\x00', 0xD336: b'\x05'},
            'expect': {0xD343: b'\x00\x04', 0xD336: b'\x04'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD397: b'\x01', 0xD343: b'r\x07\x00\x00', 0xD336: b'\x01', 0xD3A5: b'\x01'},
            'expect': {0xD343: b'\x00\x07', 0xD336: b'\x00', 0xD3A5: b'\x00'}},
    ],
    'Func_1c52e': [
        {   'a': 0x00,
            'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x00'},
            'read': {0xD2ED: 0x0200},
            'expect': {0xD2F4: b'\x00'}},
        {   'a': 0x7F,
            'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x01'},
            'read': {0xD2ED: 0x0200},
            'expect': {0xD300: b'\x7f'}},
        {   'a': 0x33,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x00'},
            'read': {0xD2ED: 0x0200},
            'expect': {0xD2F4: b'3'}},
        {   'a': 0xFF,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD2ED: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#'
                                b"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefg"
                                b'hijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABC'
                                b'DEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
                                b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
                        0xD397: b'\x01'},
            'read': {0xD2ED: 0x0200},
            'expect': {0xD300: b'\xff'}},
    ],
    'UpdateNPCMovementStep': [
        {   'a': 0x17,
            'hl': 0xC4F0,
            'wram': {0xC4F5: b'\x00', 0xC4F8: b'\x0f'},
            'expect': {0xC4F8: b'\x0f'},
            'expect_regs': {'a': 0x17}},
        {   'a': 0x42,
            'hl': 0xC4F0,
            'wram': {0xC4F5: b' ', 0xC4F8: b'\x00'},
            'expect': {0xC4F8: b'\x01'},
            'expect_regs': {'a': 0x42}},
        {   'a': 0x99,
            'hl': 0xC4F0,
            'wram': {0xC4F5: b' ', 0xC4F8: b'\x0e'},
            'expect': {0xC4F8: b'\x0f'},
            'expect_regs': {'a': 0x99}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xC4F0,
            'wram': {0xC4F5: b' ', 0xC4F8: b'\x0e'},
            'expect': {0xC4F8: b'\x0f'},
            'expect_regs': {'a': 0xAA}},
    ],
    'FindNPCAtLocation': [
        {   'b': 0x05,
            'c': 0x07,
            'd': 0x11,
            'e': 0x22,
            'hl': 0x3344,
            'wram': {0xD338: b'\x01', 0xD339: b'\x05\x07', 0xD33C: b'\x00'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x09,
            'c': 0x0A,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD344: b'\x01', 0xD345: b'\t\n', 0xD348: b'\x00', 0xD339: b'\x00\x00'}},
        {'b': 0xFF, 'c': 0x00, 'd': 0x11, 'e': 0x22, 'hl': 0x3344},
    ],
    'HandleAllNPCMovement': [
        {'wram': {0xD3A4: b'\xff', 0xD336: b'\x00'}, 'read': {0xD3A4: 0x01}},
        {   'wram': {   0xD3A4: b'\xff',
                        0xD336: b'\x01',
                        0xD337: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'read': {0xD3A4: 0x01, 0xD337: 0x0C}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD3A4: b'\x00',
                        0xD336: b'\x01',
                        0xD337: b'\x05\x03\n\x0b\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD175: b'\x10',
                        0xD4EE: b'\x00',
                        0xD4EF: b'\x00',
                        0xD4F0: b'\x00',
                        0xD4FC: b'\x00',
                        0xFF92: b'\x00',
                        0xFF93: b'\x00'},
            'read': {0xD3A4: 0x01, 0xD337: 0x0C, 0xD4BC: 0x01, 0xD4EE: 0x03, 0xD4FC: 0x01}},
        {   'a': 0x07,
            'b': 0x58,
            'c': 0x96,
            'd': 0x14,
            'e': 0x17,
            'f': 0x00,
            'hl': 0x380E,
            'wram': {0xD3A4: b'\x00',
                     0xD336: b'\x01',
                     0xD337: b'\x05\x03\n\x0b\x00\x00\x00\x00\x00\x00\x00\x00',
                     0xD175: b'\x10',
                     0xD4EE: b'\x00',
                     0xD4EF: b'\x00',
                     0xD4F0: b'\x00',
                     0xD4FC: b'\x00',
                     0xFF92: b'\x00',
                     0xFF93: b'\x00'},
            'read': {0xD3A4: 0x01,
                     0xD337: 0x0C,
                     0xD4BC: 0x01,
                     0xD4EE: 0x03,
                     0xD4FC: 0x01}},
    ],
}

MUTATIONS = {
    'CheckIfNPCIsRonald': {   'source_symbol': 'CheckIfNPCIsRonald',
        'before': 'a == NPC_RONALD3',
        'after': 'a == NPC_RONALD1',
        'case_ids': ['CheckIfNPCIsRonald-5', 'CheckIfNPCIsRonald-10'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UpdateNPCAnimation': {   'source_symbol': 'UpdateNPCAnimation',
        'before': 'NPC_FLAG_DIRECTIONLESS_F)) == 0',
        'after': 'NPC_FLAG_DIRECTIONLESS_F)) != 0',
        'case_ids': ['UpdateNPCAnimation-3', 'UpdateNPCAnimation-4', 'UpdateNPCAnimation-5'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'ApplyRandomCountToNPCAnim': {   'source_symbol': 'ApplyRandomCountToNPCAnim',
        'before': 'gb_write8(counter, (uint8_t)(count - r));',
        'after': 'gb_write8((uint16_t)(counter + 1u), (uint8_t)(count - r));',
        'case_ids': [   'ApplyRandomCountToNPCAnim-3',
                        'ApplyRandomCountToNPCAnim-4',
                        'ApplyRandomCountToNPCAnim-5'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'SetNPCAnimation': {   'source_symbol': 'SetNPCAnimation',
        'before': 'GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_ANIM);',
        'after': 'GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);',
        'case_ids': ['SetNPCAnimation-1', 'SetNPCAnimation-2', 'SetNPCAnimation-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'SetNPCDirection': {   'source_symbol': 'SetNPCDirection',
        'before': 'GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);\n'
                  '\tgb_write8(r.hl, a);',
        'after': 'GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION_BACKUP);\n'
                 '\tgb_write8(r.hl, a);',
        'case_ids': ['SetNPCDirection-1', 'SetNPCDirection-2', 'SetNPCDirection-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'StartNPCMovement': {   'source_symbol': 'StartNPCMovement',
        'before': 'if (cmd >= MOVEMENT_CMD_SPECIAL)',
        'after': 'if (cmd > MOVEMENT_CMD_SPECIAL)',
        'case_ids': ['StartNPCMovement-7'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'Func_1c5e9': {   'source_symbol': 'Func_1c5e9',
        'before': 'uint16_t hl = (uint16_t)(r.hl + (uint16_t)(LOADED_NPC_DIRECTION - '
                  'LOADED_NPC_DIRECTION_BACKUP));',
        'after': 'uint16_t hl = (uint16_t)(r.hl + 0u);',
        'case_ids': ['Func_1c5e9-1', 'Func_1c5e9-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UpdateNPCPosition': {   'source_symbol': 'UpdateNPCPosition',
        'before': 'uint8_t x = (uint8_t)(gb_read8(hl) + x_offset);',
        'after': 'uint8_t x = (uint8_t)(gb_read8(hl) + y_offset);',
        'case_ids': [   'UpdateNPCPosition-1',
                        'UpdateNPCPosition-2',
                        'UpdateNPCPosition-3',
                        'UpdateNPCPosition-4'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UpdateNPCSpritePosition': {   'source_symbol': 'UpdateNPCSpritePosition',
        'before': 'uint8_t y = (uint8_t)(y_base * 8u + 0x10u);',
        'after': 'uint8_t y = (uint8_t)(y_base * 8u + 0x08u);',
        'case_ids': ['UpdateNPCSpritePosition-0', 'UpdateNPCSpritePosition-1'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'CheckIsAnNPCMoving': {   'source_symbol': 'CheckIsAnNPCMoving',
        'before': 'uint8_t a = (uint8_t)(wIsAnNPCMoving & NPC_FLAG_MOVING);',
        'after': 'uint8_t a = wIsAnNPCMoving;',
        'case_ids': [   'CheckIsAnNPCMoving-1',
                        'CheckIsAnNPCMoving-2',
                        'CheckIsAnNPCMoving-3',
                        'CheckIsAnNPCMoving-4'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UpdateNPCsTilePermission': {   'source_symbol': 'UpdateNPCsTilePermission',
        'before': 'uint8_t result = UpdatePermissionOfMapPosition(0x40u, x, y);',
        'after': 'uint8_t result = UpdatePermissionOfMapPosition(0x20u, x, y);',
        'case_ids': [   'UpdateNPCsTilePermission-0',
                        'UpdateNPCsTilePermission-1',
                        'UpdateNPCsTilePermission-2',
                        'UpdateNPCsTilePermission-3',
                        'UpdateNPCsTilePermission-4'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'SetNPCsTilePermission': {   'source_symbol': 'SetNPCsTilePermission',
        'before': 'SetPermissionOfMapPosition(0x40u, x, y);',
        'after': 'SetPermissionOfMapPosition(0x20u, x, y);',
        'case_ids': [   'SetNPCsTilePermission-0',
                        'SetNPCsTilePermission-1',
                        'SetNPCsTilePermission-2',
                        'SetNPCsTilePermission-3',
                        'SetNPCsTilePermission-4'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'SetNPCPosition': {   'source_symbol': 'SetNPCPosition',
        'before': 'gb_write8((uint16_t)(entry.hl + 1u), c);',
        'after': 'gb_write8((uint16_t)(entry.hl + 2u), c);',
        'case_ids': [   'SetNPCPosition-0',
                        'SetNPCPosition-1',
                        'SetNPCPosition-2',
                        'SetNPCPosition-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'Func_1c53f': {   'source_symbol': 'Func_1c53f',
        'before': 'uint16_t backup = (uint16_t)(r.hl + (LOADED_NPC_DIRECTION_BACKUP - '
                  'LOADED_NPC_DIRECTION));',
        'after': 'uint16_t backup = (uint16_t)(r.hl + 4u);',
        'case_ids': ['Func_1c53f-0', 'Func_1c53f-1', 'Func_1c53f-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'GetNPCDirection': {   'source_symbol': 'GetNPCDirection',
        'before': '\treturn gb_read8(r.hl);',
        'after': '\treturn (uint8_t)(gb_read8(r.hl) + 1u);',
        'case_ids': ['GetNPCDirection-0', 'GetNPCDirection-1', 'GetNPCDirection-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'GetNPCPosition': {   'source_symbol': 'GetNPCPosition',
        'before': '\tuint8_t y = gb_read8((uint16_t)(r.hl + 1u));',
        'after': '\tuint8_t y = gb_read8((uint16_t)(r.hl + 2u));',
        'case_ids': [   'GetNPCPosition-0',
                        'GetNPCPosition-1',
                        'GetNPCPosition-2',
                        'GetNPCPosition-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UpdateIsAnNPCMovingFlag': {   'source_symbol': 'UpdateIsAnNPCMovingFlag',
        'before': 'uint8_t a = (uint8_t)(wIsAnNPCMoving | gb_read8((uint16_t)(hl + '
                  'LOADED_NPC_FLAGS)));',
        'after': 'uint8_t a = wIsAnNPCMoving;',
        'case_ids': [   'UpdateIsAnNPCMovingFlag-1',
                        'UpdateIsAnNPCMovingFlag-2',
                        'UpdateIsAnNPCMovingFlag-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'ClearNPCs': {   'source_symbol': 'ClearNPCs',
        'before': 'wLoadedNPCs_PTR[i] = 0x00u;',
        'after': 'wLoadedNPCs_PTR[i + 1u] = 0x00u;',
        'case_ids': ['ClearNPCs-0', 'ClearNPCs-1', 'ClearNPCs-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'SetAllNPCTilePermissions': {   'source_symbol': 'SetAllNPCTilePermissions',
        'before': '\t\tif (wLoadedNPCs_PTR[(uint16_t)i * LOADED_NPC_LENGTH] != 0u) {',
        'after': '\t\tif (wLoadedNPCs_PTR[(uint16_t)i * LOADED_NPC_LENGTH] == 0u) {',
        'case_ids': [   'SetAllNPCTilePermissions-0',
                        'SetAllNPCTilePermissions-1',
                        'SetAllNPCTilePermissions-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'Func_1c557': {   'source_symbol': 'Func_1c557',
        'before': '\tif ((found.f & 0x10u) == 0u)',
        'after': '\tif ((found.f & 0x10u) != 0u)',
        'case_ids': ['Func_1c557-0', 'Func_1c557-1', 'Func_1c557-2', 'Func_1c557-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'LoadNPC': {   'source_symbol': 'LoadNPC',
        'before': 'remaining != 0u',
        'after': 'remaining == 0u',
        'case_ids': ['LoadNPC-0', 'LoadNPC-1'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'SetNewScriptNPC': {   'source_symbol': 'SetNewScriptNPC',
        'before': 'gb_write8(direction.hl, (uint8_t)(wPlayerDirection ^ 0x02u));',
        'after': 'gb_write8(direction.hl, wPlayerDirection);',
        'case_ids': ['SetNewScriptNPC-0', 'SetNewScriptNPC-1', 'SetNewScriptNPC-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UnloadNPC': {   'source_symbol': 'UnloadNPC',
        'before': 'gb_write8(npc.hl, 0u);',
        'after': 'gb_write8((uint16_t)(npc.hl + 1u), 0u);',
        'case_ids': ['UnloadNPC-1', 'UnloadNPC-2', 'UnloadNPC-3', 'UnloadNPC-4'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'Func_1c52e': {   'source_symbol': 'Func_1c52e',
        'before': 'PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,\n'
                  '\t\tLOADED_NPC_DIRECTION_BACKUP);\n'
                  '\tgb_write8(r.hl, a);',
        'after': 'PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,\n'
                 '\t\tLOADED_NPC_DIRECTION_BACKUP);\n'
                 '\tgb_write8((uint16_t)(r.hl + 1u), a);',
        'case_ids': ['Func_1c52e-0', 'Func_1c52e-1', 'Func_1c52e-2', 'Func_1c52e-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'UpdateNPCMovementStep': {   'source_symbol': 'UpdateNPCMovementStep',
        'before': '\tgb_write8(step, (uint8_t)(gb_read8(step) + 1u));',
        'after': '\tgb_write8(step, (uint8_t)(gb_read8(step) + 2u));',
        'case_ids': [   'UpdateNPCMovementStep-1',
                        'UpdateNPCMovementStep-2',
                        'UpdateNPCMovementStep-3'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'FindNPCAtLocation': {   'source_symbol': 'FindNPCAtLocation',
        'before': 'if (active != 0u) {',
        'after': 'if (active == 0u) {',
        'case_ids': ['FindNPCAtLocation-0', 'FindNPCAtLocation-1'],
        'source': 'src/profiles/extended/home/npc_core.c'},
    'HandleAllNPCMovement': {   'source_symbol': 'HandleAllNPCMovement',
        'before': 'wWhichSprite = a;',
        'after': 'wWhichSprite = 0u;',
        'case_ids': ['HandleAllNPCMovement-2'],
        'source': 'src/profiles/extended/home/npc_core.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
