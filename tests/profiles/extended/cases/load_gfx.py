"""Extended oracle-diff cases for load_gfx, seeded from tests/cases/load_gfx.py."""

CONTRACT = {
    'LoadTilemap_ToSRAM': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadTilemap_ToVRAM': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadTilemap': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadTilemap.InitAndDecompressBGMap': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadTilemap.Decompress': {'compare': ('b', 'd', 'e', 'hl'), 'preserve': ('hl',)},
    'Func_80148': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'CopyBGDataToVRAMOrSRAM': {'compare': ('c', 'd', 'e', 'hl'), 'preserve': ('c',)},
    'SafelyCopyBGMapFromSRAMToVRAM': {'compare': ('f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'ClearSRAMBGMaps': {'compare': ('f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetMapDataPointer': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'LoadGraphicsPointerFromHL': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'LoadSpriteGfx': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadGfxDataFromTempPointerToVRAMBank': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadGfxDataFromTempPointer': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetTileOffsetPointerAndSwitchVRAM': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2': {'compare': ('f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'b', 'c', 'd', 'e', 'hl')},
    'LoadTilesetGfx': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadTilesetGfx.LoadTileGfx': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadTilesetGfx.CopyGfxData': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'Func_803b9': {'compare': ('b', 'c', 'd', 'e'), 'preserve': ('b', 'c', 'd', 'e')},
    'LoadBGPalette': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadPaletteDataFromHL': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadOBPalette': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadPaletteDataToBuffer': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    '_DrawPortrait': {'compare': (), 'preserve': ()},
}

CASES = {
    'LoadTilemap_ToSRAM': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {'b': 0x01, 'c': 0x01, 'wram': {0xFF80: b' '}},
    ],
    'LoadTilemap_ToVRAM': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {'b': 0x01, 'c': 0x01, 'wram': {0xFF80: b' '}},
    ],
    'LoadTilemap': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {'b': 0x01, 'c': 0x01, 'wram': {0xFF80: b' '}},
    ],
    'LoadTilemap.InitAndDecompressBGMap': [
        {   'wram': {   0xD4B1: b'\x00\x98',
                        0xD4AF: b'\x00\x98',
                        0xD11C: b'\x01',
                        0xD11D: b'\x01',
                        0xD11E: b'\x00',
                        0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD4B1: b'\x00\x98',
                        0xD4AF: b'\x00\x98',
                        0xD11C: b'\x01',
                        0xD11D: b'\x01',
                        0xD11E: b'\x00',
                        0xFF80: b' '}},
        {   'wram': {   0xD4B1: b'\x00\x98',
                        0xD4AF: b'\x00\x98',
                        0xD11C: b'\x01',
                        0xD11D: b'\x01',
                        0xD11E: b'\x00',
                        0xFF80: b' '}},
    ],
    'LoadTilemap.Decompress': [
        {   'wram': {   0xD4B1: b'\x00\x98',
                        0xD4AF: b'\x00\x98',
                        0xD11C: b'\x01',
                        0xD11D: b'\x01',
                        0xD11E: b'\x00',
                        0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD4B1: b'\x00\x98',
                        0xD4AF: b'\x00\x98',
                        0xD11C: b'\x01',
                        0xD11D: b'\x01',
                        0xD11E: b'\x00',
                        0xFF80: b' '}},
        {   'b': 0x01,
            'wram': {   0xD4B1: b'\x00\x98',
                        0xD4AF: b'\x00\x98',
                        0xD11C: b'\x01',
                        0xD11D: b'\x01',
                        0xD11E: b'\x00',
                        0xFF80: b' '}},
    ],
    'Func_80148': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'b': 0x01},
        {'b': 0xFF},
    ],
    'CopyBGDataToVRAMOrSRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'b': 0x01},
        {'b': 0xFF},
        {'b': 0x00, 'wram': {0xFF80: b' ', 0xD4AF: b'\x00\x98'}, 'read': {0x9800: 0x0100}},
    ],
    'SafelyCopyBGMapFromSRAMToVRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'wram': {0xFF80: b' '},
            'sram': {   0x01: {   0xA000: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                          b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b'
                                          b'\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFG'
                                          b'HIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{'
                                          b'|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b'
                                          b'\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                          b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3'
                                          b'\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                          b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb'
                                          b'\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                          b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3'
                                          b'\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                          b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb'
                                          b'\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03'
                                          b'\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13'
                                          b'\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\''
                                          b'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'
                                          b'`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83'
                                          b'\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                          b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b'
                                          b'\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                          b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3'
                                          b'\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                          b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb'
                                          b'\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                          b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3'
                                          b'\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                          b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb'
                                          b'\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                          b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                          b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
                                          b'89:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmno'
                                          b'pqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                          b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93'
                                          b'\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                          b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab'
                                          b'\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                          b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3'
                                          b'\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                          b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb'
                                          b'\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                          b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3'
                                          b'\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
                                          b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                          b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b'
                                          b'\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFG'
                                          b'HIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{'
                                          b'|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b'
                                          b'\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                          b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3'
                                          b'\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                          b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb'
                                          b'\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                          b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3'
                                          b'\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                          b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb'
                                          b'\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03'
                                          b'\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13'
                                          b'\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\''
                                          b'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'
                                          b'`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83'
                                          b'\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                          b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b'
                                          b'\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                          b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3'
                                          b'\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                          b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb'
                                          b'\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                          b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3'
                                          b'\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                          b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb'
                                          b'\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04\x05\x06\x07'
                                          b'\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
                                          b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
                                          b'89:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmno'
                                          b'pqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                                          b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93'
                                          b'\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
                                          b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab'
                                          b'\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7'
                                          b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3'
                                          b'\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
                                          b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb'
                                          b'\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7'
                                          b'\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3'
                                          b'\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
                                          b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
                                          b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b'
                                          b'\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFG'
                                          b'HIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{'
                                          b'|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b'
                                          b'\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97'
                                          b'\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3'
                                          b'\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
                                          b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb'
                                          b'\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
                                          b'\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3'
                                          b'\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
                                          b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb'
                                          b'\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7'
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03'
                                          b'\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13'
                                          b'\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\''
                                          b'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'
                                          b'`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83'
                                          b'\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
                                          b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b'
                                          b'\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7'
                                          b'\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3'
                                          b'\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
                                          b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb'
                                          b'\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7'
                                          b'\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3'
                                          b'\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
                                          b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb'
                                          b'\xfc\xfd\xfe\xff'}},
            'vread': {0x00: {0x9800: 0x0400}, 0x01: {0x9800: 0x0400}}},
    ],
    'ClearSRAMBGMaps': [
        {   'wram': {0xFF81: b'\x01'},
            'sram': {   0x01: {   0xA000: b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
                                          b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'}},
            'sread': {0x01: {0xA000: 0x0800}}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'GetMapDataPointer': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'a': 0x00, 'hl': 0x00},
        {'a': 0xFF, 'hl': 0x04},
    ],
    'LoadGraphicsPointerFromHL': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'hl': 0x7FFF},
        {'hl': 0x8000},
    ],
    'LoadSpriteGfx': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
    ],
    'LoadGfxDataFromTempPointerToVRAMBank': [
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x00\x01',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x01',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'b': 0x00,
            'c': 0x00,
            'oracle': False,
            'why': 'zero tile count and zero tile size expand to 65536 bytes, overwriting the '
                   'synthesized call frame',
            'wram': {   0xD4AF: b'\x00\x90',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x00',
                        0xD4B5: b'\x00\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x01',
                        0xFF4F: b'\x01',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xC202: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'expect_vram': {   0x01: {   0x8000: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                                         0x8200: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca'}},
            'expect': {0xFF4F: b'\xfe'},
            'expect_regs': {'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0x00, 'hl': 0x00}},
    ],
    'LoadGfxDataFromTempPointer': [
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x00\x01',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'wram': {   0xD4AF: b'\x00\x80',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x10',
                        0xD4B5: b'\x01\x01',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x00',
                        0xFF4F: b'\x00',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'vread': {0x00: {0x8000: 0x10}}},
        {   'b': 0x00,
            'c': 0x00,
            'oracle': False,
            'why': 'zero tile count and zero tile size expand to 65536 bytes, overwriting the '
                   'synthesized call frame',
            'wram': {   0xD4AF: b'\x00\x90',
                        0xD4B1: b'\x00\xc0',
                        0xD4B3: b'\x00',
                        0xD4B4: b'\x00',
                        0xD4B5: b'\x00\x00',
                        0xD4B7: b'\x00',
                        0xD4B8: b'\x01',
                        0xFF4F: b'\x01',
                        0xC002: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xC202: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                        0xFF80: b' '},
            'expect_vram': {   0x01: {   0x9000: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca',
                                         0x9200: b'\x07\x14!.;HUbo|\x89\x96\xa3\xb0\xbd\xca'}},
            'expect': {0xFF4F: b'\xfe'},
            'expect_regs': {'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0x00, 'hl': 0x00}},
    ],
    'GetTileOffsetPointerAndSwitchVRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'wram': {0xD4B7: b'\x00', 0xD4B8: b'\x00'}, 'read': {0xD4B7: 0x01, 0xD4B8: 0x01}},
    ],
    'GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'wram': {0xD4B7: b'\x80', 0xD4B8: b'\x01'}, 'read': {0xD4B7: 0x01, 0xD4B8: 0x01}},
    ],
    'LoadTilesetGfx': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
    ],
    'LoadTilesetGfx.LoadTileGfx': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {   'wram': {   0xD4AF: b'\x80\x00',
                        0xD4B7: b'\x80',
                        0xD4B5: b'\x01\x00',
                        0xD4B1: b'\x00@',
                        0xD4B3: b' ',
                        0xFF80: b' '}},
    ],
    'LoadTilesetGfx.CopyGfxData': [
        {   'oracle': False,
            'why': 'zero remaining count expands to the 65536-tile copy and overwrites the synthesized '
                   'call frame',
            'expect': {0xD4B5: b'\x00\x00'},
            'expect_regs': {'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0x00, 'hl': 0x00}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'b': 0x00,
            'c': 0x00,
            'oracle': False,
            'why': 'zero remaining count expands to the 65536-tile copy and overwrites the synthesized '
                   'call frame',
            'expect': {0xD4B5: b'\x00\x00'},
            'expect_regs': {'b': 0x00, 'c': 0x00, 'd': 0x00, 'e': 0x00, 'hl': 0x00}},
        {'b': 0x00, 'c': 0x80},
        {'b': 0x01, 'c': 0x00},
        {'b': 0x01, 'c': 0x80},
        {'b': 0x00, 'c': 0xFF},
    ],
    'Func_803b9': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
    ],
    'LoadBGPalette': [
        {'read': {0xFF47: 0x01}, 'wram': {0xFF80: b' '}},
        {'a': 0x01, 'read': {0xCAF0: 0x40}, 'wram': {0xFF80: b' '}},
        {'a': 0x00, 'read': {0xCAF0: 0x40}, 'wram': {0xFF80: b' '}},
        {   'a': 0x01,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'read': {0xCAF0: 0x40},
            'wram': {0xFF80: b' '}},
    ],
    'LoadPaletteDataFromHL': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {'b': 0x00, 'c': 0x00, 'wram': {0xFF80: b' '}},
        {'b': 0x00, 'c': 0x01, 'wram': {0xFF80: b' '}},
        {'b': 0x0F, 'c': 0x08, 'wram': {0xFF80: b' '}},
        {'b': 0x10, 'c': 0x01, 'wram': {0xFF80: b' '}},
        {'b': 0x17, 'c': 0x01, 'wram': {0xFF80: b' '}},
        {'b': 0x18, 'c': 0x01, 'wram': {0xFF80: b' '}},
        {'b': 0x00, 'c': 0x09, 'wram': {0xFF80: b' '}},
    ],
    'LoadOBPalette': [
        {'read': {0xCB30: 0x40}, 'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {'a': 0x75, 'read': {0xCB30: 0x40}, 'wram': {0xFF80: b' '}},
        {'a': 0x00, 'wram': {0xD4B7: b'\x01', 0xFF80: b' '}, 'read': {0xCB30: 0x40}},
        {'a': 0x6C, 'read': {0xCB30: 0x40}, 'wram': {0xFF80: b' '}},
        {'a': 0x72, 'read': {0xCB30: 0x40}, 'wram': {0xFF80: b' '}},
        {'a': 0x72, 'wram': {0xD4B7: b'\x01', 0xFF80: b' '}, 'read': {0xCB30: 0x40}},
    ],
    'LoadPaletteDataToBuffer': [
        {'wram': {0xFF80: b' '}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b' '}},
        {'a': 0x00, 'wram': {0xFF80: b' '}},
        {'a': 0xFF, 'wram': {0xFF80: b' '}},
    ],
    '_DrawPortrait': [
        {   'wram': {0xD11E: b'b', 0xD27E: b'\x19', 0xD60B: b'\x00'},
            'read': {   0xD11E: 0x01,
                        0xD226: 0x01,
                        0xD4B7: 0x01,
                        0xD4B8: 0x01,
                        0xD27E: 0x01,
                        0xD60B: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD11E: b'\x00', 0xD27E: b'*', 0xD60B: b'\x02'},
            'read': {   0xD11E: 0x01,
                        0xD226: 0x01,
                        0xD4B7: 0x01,
                        0xD4B8: 0x01,
                        0xD27E: 0x01,
                        0xD60B: 0x01}},
        {   'wram': {0xD11E: b'b', 0xD27E: b'\x19', 0xD60B: b')'},
            'read': {   0xD11E: 0x01,
                        0xD226: 0x01,
                        0xD4B7: 0x01,
                        0xD4B8: 0x01,
                        0xD27E: 0x01,
                        0xD60B: 0x01}},
        {   'wram': {0xD11E: b'b', 0xD27E: b'\x19', 0xD60B: b'\x28'},
            'read': {   0xD11E: 0x01,
                        0xD226: 0x01,
                        0xD4B7: 0x01,
                        0xD4B8: 0x01,
                        0xD27E: 0x01,
                        0xD60B: 0x01}},
    ],
}

MUTATIONS = {
    'LoadTilemap_ToSRAM': {   'source_symbol': 'LoadTilemap_ToSRAM',
        'before': '\twWriteBGMapToSRAM = 1;\n\tLoadTilemap(b, c);',
        'after': '\twWriteBGMapToSRAM = 1;\n\tLoadTilemap((uint8_t)(b ^ 1u), c);',
        'case_ids': ['LoadTilemap_ToSRAM-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilemap_ToVRAM': {   'source_symbol': 'LoadTilemap_ToVRAM',
        'before': '\twWriteBGMapToSRAM = 0;\n\tLoadTilemap(b, c);',
        'after': '\twWriteBGMapToSRAM = 0;\n\tLoadTilemap((uint8_t)(b ^ 1u), c);',
        'case_ids': ['LoadTilemap_ToVRAM-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilemap': {   'source_symbol': 'LoadTilemap',
        'before': '\twBGMapCGBMode = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 4u));',
        'after': '\twBGMapCGBMode = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 5u));',
        'case_ids': ['LoadTilemap-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilemap.InitAndDecompressBGMap': {   'source_symbol': 'LoadTilemap.InitAndDecompressBGMap',
        'before': '\t\tLoadTilemap_Decompress(&de);',
        'after': '\t\t;',
        'case_ids': ['LoadTilemap.InitAndDecompressBGMap-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilemap.Decompress': {   'source_symbol': 'LoadTilemap.Decompress',
        'before': '\t\tif ((uint8_t)(row + 1u) == rows)',
        'after': '\t\tif ((uint8_t)(row + 1u) != rows)',
        'case_ids': ['LoadTilemap.Decompress-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'Func_80148': {   'source_symbol': 'FuncEightZeroOneFourEight',
        'before': 'void FuncEightZeroOneFourEight(uint16_t hl, uint8_t b)\n{',
        'after': 'void FuncEightZeroOneFourEight(uint16_t hl, uint8_t b)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['Func_80148-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'CopyBGDataToVRAMOrSRAM': {   'source_symbol': 'CopyBGDataToVRAMOrSRAM',
        'before': '\t\tSafeCopyDataHLtoDE(hl, de, b);',
        'after': '\t\t;',
        'case_ids': ['CopyBGDataToVRAMOrSRAM-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'SafelyCopyBGMapFromSRAMToVRAM': {   'source_symbol': 'SafelyCopyBGMapFromSRAMToVRAM',
        'before': '\t\tuint16_t src = (uint16_t)(0xa000u + row * 32u);',
        'after': '\t\tuint16_t src = (uint16_t)(0x9FFFu + row * 32u);',
        'case_ids': ['SafelyCopyBGMapFromSRAMToVRAM-2'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'ClearSRAMBGMaps': {   'source_symbol': 'ClearSRAMBGMaps',
        'before': '\tFillMemoryWithA(0xa000u, 0x0800u, 0);',
        'after': '\tFillMemoryWithA(0x9FFFu, 0x0800u, 0);',
        'case_ids': ['ClearSRAMBGMaps-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'GetMapDataPointer': {   'source_symbol': 'GetMapDataPointer',
        'before': '\tuint16_t offset = (uint16_t)a * 4u;',
        'after': '\tuint16_t offset = (uint16_t)a * 5u;',
        'case_ids': ['GetMapDataPointer-1'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadGraphicsPointerFromHL': {   'source_symbol': 'LoadGraphicsPointerFromHL',
        'before': '\tgb_write8(wTempPointer_ADDR + 1u, gb_read8(p++));',
        'after': '\t;',
        'case_ids': ['LoadGraphicsPointerFromHL-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadSpriteGfx': {   'source_symbol': 'LoadSpriteGfx',
        'before': '\treturn total;',
        'after': '\treturn 1u + total;',
        'case_ids': ['LoadSpriteGfx-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadGfxDataFromTempPointerToVRAMBank': {   'source_symbol': 'LoadGfxDataFromTempPointerToVRAMBank',
        'before': '\tGetTileOffsetPointerAndSwitchVRAM();\n\tLoadGfxDataFromTempPointer();',
        'after': '\tGetTileOffsetPointerAndSwitchVRAM();\n\t;',
        'case_ids': ['LoadGfxDataFromTempPointerToVRAMBank-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadGfxDataFromTempPointer': {   'source_symbol': 'LoadGfxDataFromTempPointer',
        'before': '\tuint16_t src = state16(wTempPointer_ADDR);',
        'after': '\tuint16_t src = (uint16_t)(state16(wTempPointer_ADDR) + 1u);',
        'case_ids': ['LoadGfxDataFromTempPointer-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'GetTileOffsetPointerAndSwitchVRAM': {   'source_symbol': 'GetTileOffsetPointerAndSwitchVRAM',
        'before': '\tput16(wVRAMPointer_ADDR, (uint16_t)(0x8000u + ((uint16_t)offset << 4)));',
        'after': '\tput16(wVRAMPointer_ADDR, (uint16_t)(0x7FFFu + ((uint16_t)offset << 4)));',
        'case_ids': ['GetTileOffsetPointerAndSwitchVRAM-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2': {   'source_symbol': 'GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2',
        'before': '\tuint8_t saved = wVRAMTileOffset;',
        'after': '\tuint8_t saved = (wVRAMTileOffset) ^ 1u;',
        'case_ids': ['GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2-2'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilesetGfx': {   'source_symbol': 'LoadTilesetGfx',
        'before': '\t} else {\n'
                  '\t\tuint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;\n'
                  '\t\tLoadGraphicsPointerFromHL(&hl);',
        'after': '\t} else {\n'
                 '\t\tuint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;\n'
                 '\t\t(void)hl;',
        'case_ids': ['LoadTilesetGfx-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilesetGfx.LoadTileGfx': {   'source_symbol': 'LoadTilesetGfx.LoadTileGfx',
        'before': '\tif (LoadTilesetGfx_CopyGfxData(1, 0).f & 0x80u)',
        'after': '\tif (LoadTilesetGfx_CopyGfxData(1, 1).f & 0x80u)',
        'case_ids': ['LoadTilesetGfx.LoadTileGfx-2'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadTilesetGfx.CopyGfxData': {   'source_symbol': 'LoadTilesetGfx.CopyGfxData',
        'before': 'LoadTilesetChunkResult LoadTilesetGfx_CopyGfxData(uint8_t b, uint8_t c)\n{',
        'after': 'LoadTilesetChunkResult LoadTilesetGfx_CopyGfxData(uint8_t b, uint8_t c)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['LoadTilesetGfx.CopyGfxData-1'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'Func_803b9': {   'source_symbol': 'Func_803b9',
        'before': 'void Func_803b9(void)\n{\n\tuint8_t saved = hBankROM;\n\tBankswitchROM(0x20u);',
        'after': 'void Func_803b9(void)\n{\n\tuint8_t saved = hBankROM;\n\tBankswitchROM(0x21u);',
        'case_ids': ['Func_803b9-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadBGPalette': {   'source_symbol': 'LoadBGPalette',
        'before': '\tuint8_t count = gb_read8(wLoadedPalData_ADDR);',
        'after': '\tuint8_t count = (uint8_t)(gb_read8(wLoadedPalData_ADDR) + 1u);',
        'case_ids': ['LoadBGPalette-0', 'LoadBGPalette-1'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadPaletteDataFromHL': {   'source_symbol': 'LoadPaletteDataFromHL',
        'before': 'void LoadPaletteDataFromHL(uint16_t hl, uint8_t b, uint8_t c)\n{',
        'after': 'void LoadPaletteDataFromHL(uint16_t hl, uint8_t b, uint8_t c)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['LoadPaletteDataFromHL-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadOBPalette': {   'source_symbol': 'LoadOBPalette',
        'before': '\tuint8_t count = gb_read8(wLoadedPalData_ADDR);',
        'after': '\tuint8_t count = (uint8_t)(gb_read8(wLoadedPalData_ADDR) + 1u);',
        'case_ids': ['LoadOBPalette-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    'LoadPaletteDataToBuffer': {   'source_symbol': 'LoadPaletteDataToBuffer',
        'before': '\tcount = (uint16_t)size * 8u + 1u;',
        'after': '\tcount = (uint16_t)size * 8u + 2u;',
        'case_ids': ['LoadPaletteDataToBuffer-0'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
    '_DrawPortrait': {   'source_symbol': '_DrawPortrait',
        'before': '\twBGMapCGBMode = 1u;',
        'after': '\twBGMapCGBMode = 0u;',
        'case_ids': ['_DrawPortrait-0', '_DrawPortrait-1'],
        'source': 'src/profiles/extended/home/load_gfx.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
