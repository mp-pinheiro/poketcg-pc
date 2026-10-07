"""Extended oracle-diff cases for save, seeded from tests/cases/save.py."""

CONTRACT = {
    'CopyGeneralSaveDataToSRAM': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'ValidateGeneralSaveDataFromDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadGeneralSaveDataFromDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'WriteDataToBackup': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'LoadDataFromBackup': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'WriteBackupGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'WriteBackupCardAndDeckSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'LoadBackupGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'LoadBackupCardAndDeckSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'InvalidateSaveData': {'compare': ('hl',), 'preserve': ('hl',)},
    'UpdateAlbumProgress': {'compare': ('d', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'LoadAlbumProgressFromSRAM': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'ValidateBackupGeneralSaveData': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ('d', 'e')},
    '_ValidateGeneralSaveData': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ('d', 'e')},
    'LoadBackupSaveData': {'compare': ('d', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    '_LoadGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'SaveGeneralSaveDataFromDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    '_SaveGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'SaveAndBackupData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    '_SaveGame': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'SaveGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'LoadGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'ValidateGeneralSaveData': {'compare': ('a', 'f', 'd', 'e'), 'preserve': ('d', 'e')},
}

CASES = {
    'CopyGeneralSaveDataToSRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'wram': {   0xD3B9: b'\x0b',
                        0xD3B8: b'\x18',
                        0xCAC5: b'%',
                        0xCAC6: b'2',
                        0xCAC7: b'?',
                        0xCAC8: b'LS',
                        0xD31B: b'Y',
                        0xD0A8: b'f',
                        0xD0A9: b's',
                        0xD0AA: b'\x80',
                        0xD0AB: b'\x8d',
                        0xD0AF: b'\x9a',
                        0xD0B0: b'\xa7',
                        0xD0B1: b'\xb4',
                        0xD684: b'\xc1',
                        0xD686: b'\xce\xd5\xdc\xe3',
                        0xD310: b'\xdb\xe2\xe9\xf0\xf7\xfe\x05\x0c\x13\x1a!',
                        0xD0A5: b'\xf5',
                        0xD0A6: b'\x02',
                        0xD108: b'\x0f',
                        0xD0A7: b'\x1c',
                        0xD10A: b'\x0c',
                        0xD10B: b'6=DKRY`gnu|\x83\x8a\x91\x98',
                        0xD0FE: b'C',
                        0xCAD5: b'P',
                        0xD3A5: b']',
                        0xD3A8: b'jqx\x7f\x86\x8d\x94\x9b\xa2\xa9',
                        0xD0B2: b'w',
                        0xD683: b'\x84',
                        0xD0FC: b'\x91',
                        0xD3C1: b"\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd\x04\x0b\x12\x19 '.5<CJQX_f"
                                b'mt{\x82\x89\x90\x97\x9e\xa5\xac\xb3\xba\xc1\xc8\xcf\xd6'
                                b'\xdd\xe4\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {0xB800: 0xBB, 0xD4B5: 0x02, 0xD3B2: 0x02, 0xD4B1: 0x02}},
    ],
    'ValidateGeneralSaveDataFromDE': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01, 0xD4B5: 0x02, 0xD3B2: 0x02, 0xD4B1: 0x02, 0xD3B5: 0x05}},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0c\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01, 0xD4B5: 0x02, 0xD3B2: 0x02, 0xD4B1: 0x02, 0xD3B5: 0x05}},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0e=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0f6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01, 0xD4B5: 0x02, 0xD3B2: 0x02, 0xD4B1: 0x02, 0xD3B5: 0x05}},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\r=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0e6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01, 0xD4B5: 0x02, 0xD3B2: 0x02, 0xD4B1: 0x02, 0xD3B5: 0x05}},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'sram': {   0x00: {   0xB800: b'\x08\x00\xb2\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01, 0xD4B5: 0x02, 0xD3B2: 0x02, 0xD4B1: 0x02, 0xD3B5: 0x05}},
    ],
    'LoadGeneralSaveDataFromDE': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0x00,
            'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xCAC5: 0x01,
                        0xCAC6: 0x01,
                        0xCAC7: 0x01,
                        0xCAC8: 0x02,
                        0xD31B: 0x01,
                        0xD0A8: 0x01,
                        0xD0A9: 0x01,
                        0xD0AA: 0x01,
                        0xD0AB: 0x01,
                        0xD0AF: 0x01,
                        0xD0B0: 0x01,
                        0xD0B1: 0x01,
                        0xD684: 0x01,
                        0xD686: 0x04,
                        0xD310: 0x0B,
                        0xD0A5: 0x01,
                        0xD0A6: 0x01,
                        0xD108: 0x01,
                        0xD0A7: 0x01,
                        0xD10A: 0x01,
                        0xD10B: 0x0F,
                        0xD0FE: 0x01,
                        0xCAD5: 0x01,
                        0xD3A5: 0x01,
                        0xD3A8: 0x0A,
                        0xD0B2: 0x01,
                        0xD683: 0x01,
                        0xD0FC: 0x01,
                        0xD3C1: 0x40,
                        0xD40E: 0x01,
                        0xCE0D: 0x01,
                        0xD4B1: 0x02}},
        {   'd': 0xB8,
            'e': 0x00,
            'sram': {   0x03: {   0xB87B: b'\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")'
                                          b'07>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5'
                                          b'\xbc\xc3\xca\xd1\xd8\xdf\xe6\xed\xf4\xfb\x02\t\x10\x17\x1e%'
                                          b',3:AHOV]dkry'},
                        0x02: {   0xB87B: b'\x80\x85\x8a\x8f\x94\x99\x9e\xa3\xa8\xad\xb2\xb7'
                                          b'\xbc\xc1\xc6\xcb\xd0\xd5\xda\xdf\xe4\xe9\xee\xf3'
                                          b'\xf8\xfd\x02\x07\x0c\x11\x16\x1b %*/49>CHMRW\\afkpuz\x7f'
                                          b'\x84\x89\x8e\x93\x98\x9d\xa2\xa7\xac\xb1\xb6\xbb'},
                        0x01: {   0xB87B: b'@CFILORUX[^adgjmpsvy|\x7f\x82\x85\x88\x8b\x8e\x91'
                                          b'\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac\xaf\xb2\xb5'
                                          b'\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9'
                                          b'\xdc\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd'},
                        0x00: {   0xB800: b'\x08\x00\xb3\x00\xe3G\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x11\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91"#$%&\'()*+,-./03456789:;<=>?@ABDEFGHIJKLMNOP'
                                          b"QRS\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd\x04\x0b\x12\x19 '.5"
                                          b'<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5\xac\xb3\xba\xc1'
                                          b'\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#*18?FM'
                                          b'T[bipw~',
                                  0xB879: b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b'
                                          b'\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFG'
                                          b'HIJKLMNO'}},
            'read': {0xD3C1: 0x40}},
    ],
    'WriteDataToBackup': [
        {   'wram': {0xFF81: b'\x02'},
            'ramg': True,
            'sram': {0x00: {0xA100: b'\xde\xad\xbe\xef'}},
            'oracle': False,
            'why': "bc=0 is 65536 iterations (two SRAM bank switches each), which exceeds the oracle's "
                   '240-frame synthesized-call-frame budget.',
            'expect_sram': {0x00: {0xA100: b'\xde\xad\xbe\xef'}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x04,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xA100,
            'ramg': True,
            'sram': {0x00: {0xA100: b'\xde\xad\xbe\xef'}},
            'sread': {0x02: {0xA100: 0x04}}},
        {   'hl': 0xA100,
            'b': 0x00,
            'c': 0x01,
            'ramg': True,
            'sram': {0x00: {0xA100: b'B'}},
            'sread': {0x02: {0xA100: 0x01}}},
        {   'hl': 0xA100,
            'b': 0x01,
            'c': 0x00,
            'ramg': True,
            'sram': {   0x00: {   0xA100: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
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
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'}},
            'sread': {0x02: {0xA100: 0x0100}}},
        {   'hl': 0xA100,
            'b': 0x01,
            'c': 0x01,
            'ramg': True,
            'sram': {   0x00: {   0xA100: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
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
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\xaa'}},
            'sread': {0x02: {0xA100: 0x0101}}},
    ],
    'LoadDataFromBackup': [
        {   'sram': {0x02: {0xA100: b'\xde\xad\xbe\xef'}},
            'ramg': True,
            'oracle': False,
            'why': "bc=0 is 65536 iterations (two SRAM bank switches each), which exceeds the oracle's "
                   '240-frame synthesized-call-frame budget.',
            'expect_sram': {0x02: {0xA100: b'\xde\xad\xbe\xef'}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x00,
            'c': 0x04,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0xA100,
            'ramg': True,
            'sram': {0x02: {0xA100: b'\xde\xad\xbe\xef'}},
            'sread': {0x00: {0xA100: 0x04}}},
        {   'hl': 0xA100,
            'b': 0x00,
            'c': 0x01,
            'ramg': True,
            'sram': {0x02: {0xA100: b'B'}},
            'sread': {0x00: {0xA100: 0x01}}},
        {   'hl': 0xA100,
            'b': 0x01,
            'c': 0x00,
            'ramg': True,
            'sram': {   0x02: {   0xA100: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
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
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'}},
            'sread': {0x00: {0xA100: 0x0100}}},
        {   'hl': 0xA100,
            'b': 0x01,
            'c': 0x01,
            'ramg': True,
            'sram': {   0x02: {   0xA100: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
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
                                          b'\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\xaa'}},
            'sread': {0x00: {0xA100: 0x0101}}},
    ],
    'WriteBackupGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'ramg': True,
            'sram': {   0x00: {   0xB800: b'\x07&Ed\x83\xa2\xc1\xe0\xff\x1e=\\{\x9a\xb9\xd8\xf7\x165T'
                                          b's\x92\xb1\xd0\xef\x0e-Lk\x8a\xa9\xc8\xe7\x06%Dc\x82\xa1\xc0'
                                          b'\xdf\xfe\x1d<[z\x99\xb8\xd7\xf6\x154Sr\x91\xb0\xcf\xee\r,'
                                          b'Kj\x89\xa8\xc7\xe6\x05$Cb\x81\xa0\xbf\xde\xfd\x1c;Zy\x98'
                                          b'\xb7\xd6\xf5\x143Rq\x90\xaf\xce\xed\x0c+Ji\x88'
                                          b'\xa7\xc6\xe5\x04#Ba\x80\x9f\xbe\xdd\xfc\x1b:Yx'
                                          b'\x97\xb6\xd5\xf4\x132Qp\x8f\xae\xcd\xec\x0b*Ih'
                                          b'\x87\xa6\xc5\xe4\x03"A`\x7f\x9e\xbd\xdc\xfb\x1a9X'
                                          b'w\x96\xb5\xd4\xf3\x121Po\x8e\xad\xcc\xeb\n)Hg\x86\xa5\xc4'
                                          b'\xe3\x02!@_~\x9d\xbc\xdb\xfa\x198Wv\x95\xb4\xd3\xf2\x110'
                                          b'On\x8d\xac\xcb\xea\t(Gf\x85\xa4\xc3\xe2\x01 ?^}\x9c'
                                          b'\xbb\xda\xf9\x187Vu\x94\xb3\xd2\xf1\x10/Nm\x8c'
                                          b"\xab\xca\xe9\x08'Fe\x84\xa3\xc2\xe1\x00\x1f>]|"
                                          b'\x9b\xba\xd9\xf8\x176Ut\x93\xb2\xd1\xf0\x0f.Ml'
                                          b'\x8b\xaa\xc9\xe8'}},
            'sread': {0x00: {0xB800: 0x0100}, 0x02: {0xB800: 0x0100}},
            'read': {0xFF81: 0x01}},
    ],
    'WriteBackupCardAndDeckSaveData': [
        {'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'ramg': True,
            'sram': {   0x00: {   0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92',
                                  0xB300: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXi'}},
            'sread': {0x00: {0xA100: 0x0FA0, 0xB300: 0x0667}, 0x02: {0xA100: 0x0FA0, 0xB0A0: 0x0667}},
            'read': {0xFF81: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'LoadBackupGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'ramg': True,
            'sram': {   0x02: {   0xB800: b'\x07&Ed\x83\xa2\xc1\xe0\xff\x1e=\\{\x9a\xb9\xd8\xf7\x165T'
                                          b's\x92\xb1\xd0\xef\x0e-Lk\x8a\xa9\xc8\xe7\x06%Dc\x82\xa1\xc0'
                                          b'\xdf\xfe\x1d<[z\x99\xb8\xd7\xf6\x154Sr\x91\xb0\xcf\xee\r,'
                                          b'Kj\x89\xa8\xc7\xe6\x05$Cb\x81\xa0\xbf\xde\xfd\x1c;Zy\x98'
                                          b'\xb7\xd6\xf5\x143Rq\x90\xaf\xce\xed\x0c+Ji\x88'
                                          b'\xa7\xc6\xe5\x04#Ba\x80\x9f\xbe\xdd\xfc\x1b:Yx'
                                          b'\x97\xb6\xd5\xf4\x132Qp\x8f\xae\xcd\xec\x0b*Ih'
                                          b'\x87\xa6\xc5\xe4\x03"A`\x7f\x9e\xbd\xdc\xfb\x1a9X'
                                          b'w\x96\xb5\xd4\xf3\x121Po\x8e\xad\xcc\xeb\n)Hg\x86\xa5\xc4'
                                          b'\xe3\x02!@_~\x9d\xbc\xdb\xfa\x198Wv\x95\xb4\xd3\xf2\x110'
                                          b'On\x8d\xac\xcb\xea\t(Gf\x85\xa4\xc3\xe2\x01 ?^}\x9c'
                                          b'\xbb\xda\xf9\x187Vu\x94\xb3\xd2\xf1\x10/Nm\x8c'
                                          b"\xab\xca\xe9\x08'Fe\x84\xa3\xc2\xe1\x00\x1f>]|"
                                          b'\x9b\xba\xd9\xf8\x176Ut\x93\xb2\xd1\xf0\x0f.Ml'
                                          b'\x8b\xaa\xc9\xe8'}},
            'sread': {0x02: {0xB800: 0x0100}, 0x00: {0xB800: 0x0100}},
            'read': {0xFF81: 0x01}},
    ],
    'LoadBackupCardAndDeckSaveData': [
        {'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'wram': {0xFF81: b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92',
                                  0xB0A0: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXi'}},
            'sread': {0x02: {0xA100: 0x0FA0, 0xB0A0: 0x0667}, 0x00: {0xA100: 0x0FA0, 0xB300: 0x0667}},
            'read': {0xFF81: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'InvalidateSaveData': [
        {'wram': {0xFF80: b'\x04'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'}},
        {   'wram': {0xFF80: b'\x04', 0xFF81: b'\x03'},
            'ramg': True,
            'sram': {0x02: {0xB800: b'\x08\x00'}, 0x00: {0xB800: b'\x11"'}},
            'sread': {0x02: {0xB800: 0x02}, 0x00: {0xB800: 0x02}},
            'read': {0xFF81: 0x01}},
    ],
    'UpdateAlbumProgress': [
        {'read': {0xD3BA: 0x02, 0xD3BC: 0x02}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'read': {0xD3BA: 0x02, 0xD3BC: 0x02}},
        {   'd': 0xB8,
            'e': 0xFC,
            'sram': {0x01: {}},
            'sread': {0x01: {0xB8FE: 0x02}, 0x02: {0xB8FC: 0x02}},
            'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
        {   'd': 0xB8,
            'e': 0xFC,
            'sram': {0x03: {}},
            'sread': {0x03: {0xB8FE: 0x02}, 0x02: {0xB8FC: 0x02}},
            'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
    ],
    'LoadAlbumProgressFromSRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0xFC,
            'ramg': True,
            'sram': {0x00: {0xB8FC: b'*7'}},
            'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
        {'d': 0xFF, 'e': 0xFF, 'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
    ],
    'ValidateBackupGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'wram': {0xFF81: b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01, 0xFF81: 0x01}},
        {   'sram': {   0x02: {   0xB800: b'\xf7\xff\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'ramg': True,
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x02: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0f6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'ramg': True,
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x00: {0xB8FC: b'\x99\x88'},
                        0x02: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~',
                                  0xB8FC: b'*7'}},
            'ramg': True,
            'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
    ],
    '_ValidateGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0c\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0f6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x02: {0xB8FC: b'\x99\x88'},
                        0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~',
                                  0xB8FC: b'*7'}},
            'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
    ],
    'LoadBackupSaveData': [
        {'wram': {0xFF80: b'\x04'},
         'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'},
            'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'wram': {0xFF80: b'\x04'},
            'sram': {   0x02: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B9: 0x01, 0xD3C1: 0x40},
            'sread': {0x00: {0xB800: 0x0100}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    '_LoadGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B9: 0x01, 0xD3C1: 0x40}},
    ],
    'SaveGeneralSaveDataFromDE': [
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {0xFF80: b'\x04'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xB8,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'}},
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\x07',
                        0xD3B8: b'\x14',
                        0xCAC5: b'!',
                        0xCAC6: b'.',
                        0xCAC7: b';',
                        0xCAC8: b'HO',
                        0xD31B: b'\x05',
                        0xD0A8: b'b',
                        0xD0A9: b'o',
                        0xD0AA: b'|',
                        0xD0AB: b'\x89',
                        0xD0AF: b'\x96',
                        0xD0B0: b'\xa3',
                        0xD0B1: b'\xb0',
                        0xD684: b'\xbd',
                        0xD686: b'\xca\xd1\xd8\xdf',
                        0xD310: b'\xd7\xde\xe5\xec\xf3\xfa\x01\x08\x0f\x16\x1d',
                        0xD0A5: b'\xf1',
                        0xD0A6: b'\xfe',
                        0xD108: b'\x0b',
                        0xD0A7: b'\x18',
                        0xD10A: b'\x08',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'?',
                        0xCAD5: b'L',
                        0xD3A5: b'Y',
                        0xD3A8: b'fmt{\x82\x89\x90\x97\x9e\xa5',
                        0xD0B2: b's',
                        0xD683: b'\x80',
                        0xD0FC: b'\x8d',
                        0xD3C1: b'\xe0\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB}}},
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\t',
                        0xD3B8: b'\x16',
                        0xCAC5: b'#',
                        0xCAC6: b'0',
                        0xCAC7: b'=',
                        0xCAC8: b'JQ',
                        0xD31B: b'\x06',
                        0xD0A8: b'd',
                        0xD0A9: b'q',
                        0xD0AA: b'~',
                        0xD0AB: b'\x8b',
                        0xD0AF: b'\x98',
                        0xD0B0: b'\xa5',
                        0xD0B1: b'\xb2',
                        0xD684: b'\xbf',
                        0xD686: b'\xcc\xd3\xda\xe1',
                        0xD310: b'\xd9\xe0\xe7\xee\xf5\xfc\x03\n\x11\x18\x1f',
                        0xD0A5: b'\xf3',
                        0xD0A6: b'\x00',
                        0xD108: b'\r',
                        0xD0A7: b'\x1a',
                        0xD10A: b'\n',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'A',
                        0xCAD5: b'N',
                        0xD3A5: b'[',
                        0xD3A8: b'hov}\x84\x8b\x92\x99\xa0\xa7',
                        0xD0B2: b'u',
                        0xD683: b'\x82',
                        0xD0FC: b'\x8f',
                        0xD3C1: b'\xff\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB}}},
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\x0b',
                        0xD3B8: b'\x18',
                        0xCAC5: b'%',
                        0xCAC6: b'2',
                        0xCAC7: b'?',
                        0xCAC8: b'LS',
                        0xD31B: b'\x02',
                        0xD0A8: b'f',
                        0xD0A9: b's',
                        0xD0AA: b'\x80',
                        0xD0AB: b'\x8d',
                        0xD0AF: b'\x9a',
                        0xD0B0: b'\xa7',
                        0xD0B1: b'\xb4',
                        0xD684: b'\xc1',
                        0xD686: b'\xce\xd5\xdc\xe3',
                        0xD310: b'\xdb\xe2\xe9\xf0\xf7\xfe\x05\x0c\x13\x1a!',
                        0xD0A5: b'\xf5',
                        0xD0A6: b'\x02',
                        0xD108: b'\x0f',
                        0xD0A7: b'\x1c',
                        0xD10A: b'\x0c',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'C',
                        0xCAD5: b'P',
                        0xD3A5: b']',
                        0xD3A8: b'jqx\x7f\x86\x8d\x94\x9b\xa2\xa9',
                        0xD0B2: b'w',
                        0xD683: b'\x84',
                        0xD0FC: b'\x91',
                        0xD3C1: b'\xc0\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB}}},
    ],
    '_SaveGeneralSaveData': [
        {   'wram': {0xFF80: b'\x04'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'}},
        {   'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\x0e',
                        0xD3B8: b'\x1b',
                        0xCAC5: b'(',
                        0xCAC6: b'5',
                        0xCAC7: b'B',
                        0xCAC8: b'OV',
                        0xD31B: b'\x02',
                        0xD0A8: b'i',
                        0xD0A9: b'v',
                        0xD0AA: b'\x83',
                        0xD0AB: b'\x90',
                        0xD0AF: b'\x9d',
                        0xD0B0: b'\xaa',
                        0xD0B1: b'\xb7',
                        0xD684: b'\xc4',
                        0xD686: b'\xd1\xd8\xdf\xe6',
                        0xD310: b'\xde\xe5\xec\xf3\xfa\x01\x08\x0f\x16\x1d$',
                        0xD0A5: b'\xf8',
                        0xD0A6: b'\x05',
                        0xD108: b'\x12',
                        0xD0A7: b'\x1f',
                        0xD10A: b'\x00',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'F',
                        0xCAD5: b'S',
                        0xD3A5: b'`',
                        0xD3A8: b'mt{\x82\x89\x90\x97\x9e\xa5\xac',
                        0xD0B2: b'z',
                        0xD683: b'\x87',
                        0xD0FC: b'\x94',
                        0xD3C1: b'\xf0\n\x11\x18\x1f6/4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00',
                                  0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD3BA: 0x01,
                        0xD3BC: 0x01,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB, 0xB8FC: 0x02, 0xA00A: 0x01}}},
    ],
    'SaveAndBackupData': [
        {   'wram': {0xFF80: b'\x04'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB, 0xB8FC: 0x02}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\r',
                        0xD3B8: b'\x1a',
                        0xCAC5: b"'",
                        0xCAC6: b'4',
                        0xCAC7: b'A',
                        0xCAC8: b'NU',
                        0xD31B: b'\x03',
                        0xD0A8: b'h',
                        0xD0A9: b'u',
                        0xD0AA: b'\x82',
                        0xD0AB: b'\x8f',
                        0xD0AF: b'\x9c',
                        0xD0B0: b'\xa9',
                        0xD0B1: b'\xb6',
                        0xD684: b'\xc3',
                        0xD686: b'\xd0\xd7\xde\xe5',
                        0xD310: b'\xdd\xe4\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#',
                        0xD0A5: b'\xf7',
                        0xD0A6: b'\x04',
                        0xD108: b'\x11',
                        0xD0A7: b'\x1e',
                        0xD10A: b'\x0e',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'E',
                        0xCAD5: b'R',
                        0xD3A5: b'_',
                        0xD3A8: b'lsz\x81\x88\x8f\x96\x9d\xa4\xab',
                        0xD0B2: b'y',
                        0xD683: b'\x86',
                        0xD0FC: b'\x93',
                        0xD3C1: b'\xf8\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00',
                                  0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92',
                                  0xB300: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXi'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD3BA: 0x01,
                        0xD3BC: 0x01,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {   0x00: {0xB800: 0xBB, 0xB8FC: 0x02},
                         0x02: {0xB800: 0xBB, 0xB8FC: 0x02, 0xA100: 0x0FA0, 0xB0A0: 0x0667}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    '_SaveGame': [
        {   'c': 0x00,
            'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\x0f',
                        0xD3B8: b'\x1c',
                        0xCAC5: b')',
                        0xCAC6: b'6',
                        0xCAC7: b'C',
                        0xCAC8: b'PW',
                        0xD31B: b'\x04',
                        0xD0A8: b'j',
                        0xD0A9: b'w',
                        0xD0AA: b'\x84',
                        0xD0AB: b'\x91',
                        0xD0AF: b'\x9e',
                        0xD0B0: b'\xab',
                        0xD0B1: b'\xb8',
                        0xD684: b'\xc5',
                        0xD686: b'\xd2\xd9\xe0\xe7',
                        0xD310: b'\xdf\xe6\xed\xf4\xfb\x02\t\x10\x17\x1e%',
                        0xD0A5: b'\xf9',
                        0xD0A6: b'\x06',
                        0xD108: b'\x13',
                        0xD0A7: b' ',
                        0xD10A: b'\x01',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'G',
                        0xCAD5: b'T',
                        0xD3A5: b'a',
                        0xD3A8: b'nu|\x83\x8a\x91\x98\x9f\xa6\xad',
                        0xD0B2: b'{',
                        0xD683: b'\x88',
                        0xD0FC: b'\x95',
                        0xD3C1: b'\xfc\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc',
                        0xD31C: b'\x07',
                        0xD31D: b'\x12',
                        0xD31E: b'4',
                        0xD321: b'\x01'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00',
                                  0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92',
                                  0xB300: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXi'}},
            'read': {   0xD0A8: 0x01,
                        0xD0A9: 0x01,
                        0xD0AA: 0x01,
                        0xD0AB: 0x01,
                        0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD3BA: 0x01,
                        0xD3BC: 0x01,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {   0x00: {0xB800: 0xBB, 0xB8FC: 0x02},
                         0x02: {0xB800: 0xBB, 0xB8FC: 0x02, 0xA100: 0x0FA0, 0xB0A0: 0x0667}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'c': 0x01,
            'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\x10',
                        0xD3B8: b'\x1d',
                        0xCAC5: b'*',
                        0xCAC6: b'7',
                        0xCAC7: b'D',
                        0xCAC8: b'QX',
                        0xD31B: b'^',
                        0xD0A8: b'k',
                        0xD0A9: b'x',
                        0xD0AA: b'\x85',
                        0xD0AB: b'\x92',
                        0xD0AF: b'\x9f',
                        0xD0B0: b'\xac',
                        0xD0B1: b'\xb9',
                        0xD684: b'\xc6',
                        0xD686: b'\xd3\xda\xe1\xe8',
                        0xD310: b'\xe0\xe7\xee\xf5\xfc\x03\n\x11\x18\x1f&',
                        0xD0A5: b'\xfa',
                        0xD0A6: b'\x07',
                        0xD108: b'\x14',
                        0xD0A7: b'!',
                        0xD10A: b'\x02',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'H',
                        0xCAD5: b'U',
                        0xD3A5: b'b',
                        0xD3A8: b'ov}\x84\x8b\x92\x99\xa0\xa7\xae',
                        0xD0B2: b'|',
                        0xD683: b'\x89',
                        0xD0FC: b'\x96',
                        0xD3C1: b'\xfe\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00',
                                  0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92',
                                  0xB300: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXiz'
                                          b'\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5FWhy\x8a'
                                          b'\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2\x03\x14%6GXi'}},
            'read': {   0xD0A8: 0x01,
                        0xD0A9: 0x01,
                        0xD0AA: 0x01,
                        0xD0AB: 0x01,
                        0xD31B: 0x01,
                        0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD3BA: 0x01,
                        0xD3BC: 0x01,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {   0x00: {0xB800: 0xBB, 0xB8FC: 0x02},
                         0x02: {0xB800: 0xBB, 0xB8FC: 0x02, 0xA100: 0x0FA0, 0xB0A0: 0x0667}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0x01,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'SaveGeneralSaveData': [
        {   'wram': {0xFF80: b'\x04'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\x04'}},
        {   'wram': {   0xFF80: b'\x04',
                        0xD3B9: b'\x0e',
                        0xD3B8: b'\x1b',
                        0xCAC5: b'(',
                        0xCAC6: b'5',
                        0xCAC7: b'B',
                        0xCAC8: b'OV',
                        0xD31B: b'\x02',
                        0xD0A8: b'i',
                        0xD0A9: b'v',
                        0xD0AA: b'\x83',
                        0xD0AB: b'\x90',
                        0xD0AF: b'\x9d',
                        0xD0B0: b'\xaa',
                        0xD0B1: b'\xb7',
                        0xD684: b'\xc4',
                        0xD686: b'\xd1\xd8\xdf\xe6',
                        0xD310: b'\xde\xe5\xec\xf3\xfa\x01\x08\x0f\x16\x1d$',
                        0xD0A5: b'\xf8',
                        0xD0A6: b'\x05',
                        0xD108: b'\x12',
                        0xD0A7: b'\x1f',
                        0xD10A: b'\x00',
                        0xD10B: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xD0FE: b'F',
                        0xCAD5: b'S',
                        0xD3A5: b'`',
                        0xD3A8: b'mt{\x82\x89\x90\x97\x9e\xa5\xac',
                        0xD0B2: b'z',
                        0xD683: b'\x87',
                        0xD0FC: b'\x94',
                        0xD3C1: b'\xf0\n\x11\x18\x1f6/4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   0xB800: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                          b'\x00\x00\x00\x00\x00\x00\x00',
                                  0xA100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
                                          b'Why\x8a\x9b\xac\xbd\xce\xdf\xf0\x01\x12#4EVgx\x89\x9a'
                                          b'\xab\xbc\xcd\xde\xef\x00\x11"3DUfw\x88\x99\xaa'
                                          b'\xbb\xcc\xdd\xee\xff\x10!2CTev\x87\x98\xa9\xba'
                                          b'\xcb\xdc\xed\xfe\x0f 1BSdu\x86\x97\xa8\xb9\xca'
                                          b'\xdb\xec\xfd\x0e\x1f0ARct\x85\x96\xa7\xb8\xc9\xda'
                                          b'\xeb\xfc\r\x1e/@Qbs\x84\x95\xa6\xb7\xc8\xd9\xea'
                                          b'\xfb\x0c\x1d.?Par\x83\x94\xa5\xb6\xc7\xd8\xe9\xfa\x0b\x1c->'
                                          b'O`q\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\n\x1b,=N_p\x81\x92'
                                          b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
                                          b'\xb3\xc4\xd5\xe6\xf7\x08\x19*;L]n\x7f\x90\xa1\xb2'
                                          b'\xc3\xd4\xe5\xf6\x07\x18):K\\m~\x8f\xa0\xb1\xc2'
                                          b'\xd3\xe4\xf5\x06\x17(9J[l}\x8e\x9f\xb0\xc1\xd2'
                                          b"\xe3\xf4\x05\x16'8IZk|\x8d\x9e\xaf\xc0\xd1\xe2\xf3\x04\x15&"
                                          b'7HYj{\x8c\x9d\xae\xbf\xd0\xe1\xf2'}},
            'read': {   0xD3B9: 0x01,
                        0xD3B8: 0x01,
                        0xD3C0: 0x01,
                        0xD3C1: 0x40,
                        0xD10B: 0x0F,
                        0xD3BA: 0x01,
                        0xD3BC: 0x01,
                        0xD4B5: 0x02,
                        0xD3B2: 0x02,
                        0xD4B1: 0x02},
            'sread': {0x00: {0xB800: 0xBB, 0xB8FC: 0x02, 0xA00A: 0x01}}},
    ],
    'LoadGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B9: 0x01, 0xD3C1: 0x40}},
    ],
    'ValidateGeneralSaveData': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0c\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0f6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'}},
            'read': {0xD3B4: 0x01}},
        {   'sram': {   0x02: {0xB8FC: b'\x99\x88'},
                        0x00: {   0xB800: b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x00\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                          b'\x00\x00\x00\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd'
                                          b"\x04\x0b\x12\x19 '.5<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5"
                                          b'\xac\xb3\xba\xc1\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9'
                                          b'\x00\x07\x0e\x15\x1c#*18?FMT[bipw~',
                                  0xB8FC: b'*7'}},
            'read': {0xD3BA: 0x01, 0xD3BC: 0x01}},
    ],
}

MUTATIONS = {
    'CopyGeneralSaveDataToSRAM': {   'source_symbol': 'CopyGeneralSaveDataToSRAM',
        'before': '\t\tif (src == 0)',
        'after': '\t\tif (src != 0)',
        'case_ids': ['CopyGeneralSaveDataToSRAM-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'ValidateGeneralSaveDataFromDE': {   'source_symbol': 'ValidateGeneralSaveDataFromDE',
        'before': '\t\tif (addr == 0)',
        'after': '\t\tif (addr != 0)',
        'case_ids': ['ValidateGeneralSaveDataFromDE-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadGeneralSaveDataFromDE': {   'source_symbol': 'LoadGeneralSaveDataFromDE',
        'before': '\t\tif (dst == 0)',
        'after': '\t\tif (dst != 0)',
        'case_ids': ['LoadGeneralSaveDataFromDE-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'WriteDataToBackup': {   'source_symbol': 'WriteDataToBackup',
        'before': 'void WriteDataToBackup(uint16_t hl, uint16_t bc)\n{',
        'after': 'void WriteDataToBackup(uint16_t hl, uint16_t bc)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['WriteDataToBackup-1'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadDataFromBackup': {   'source_symbol': 'LoadDataFromBackup',
        'before': 'void LoadDataFromBackup(uint16_t hl, uint16_t bc)\n{',
        'after': 'void LoadDataFromBackup(uint16_t hl, uint16_t bc)\n'
                 '{\n'
                 '\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['LoadDataFromBackup-1'],
        'source': 'src/profiles/extended/home/save.c'},
    'WriteBackupGeneralSaveData': {   'source_symbol': 'WriteBackupGeneralSaveData',
        'before': '\tWriteDataToBackup(sGeneralSaveData_ADDR, (uint16_t)(sGeneralSaveDataEnd_ADDR '
                  '- sGeneralSaveData_ADDR));',
        'after': '\t;',
        'case_ids': ['WriteBackupGeneralSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'WriteBackupCardAndDeckSaveData': {   'source_symbol': 'WriteBackupCardAndDeckSaveData',
        'before': 'void WriteBackupCardAndDeckSaveData(void)\n{',
        'after': 'void WriteBackupCardAndDeckSaveData(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['WriteBackupCardAndDeckSaveData-0'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadBackupGeneralSaveData': {   'source_symbol': 'LoadBackupGeneralSaveData',
        'before': '\tLoadDataFromBackup(sGeneralSaveData_ADDR, (uint16_t)(sGeneralSaveDataEnd_ADDR '
                  '- sGeneralSaveData_ADDR));',
        'after': '\t;',
        'case_ids': ['LoadBackupGeneralSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadBackupCardAndDeckSaveData': {   'source_symbol': 'LoadBackupCardAndDeckSaveData',
        'before': 'void LoadBackupCardAndDeckSaveData(void)\n{',
        'after': 'void LoadBackupCardAndDeckSaveData(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['LoadBackupCardAndDeckSaveData-0'],
        'source': 'src/profiles/extended/home/save.c'},
    'InvalidateSaveData': {   'source_symbol': 'InvalidateSaveData',
        'before': '\tgb_write8(sBackupGeneralSaveData_ADDR + 0, (uint8_t)(0x08 ^ 0xFF));',
        'after': '\tgb_write8(sBackupGeneralSaveData_ADDR + 0, (uint8_t)(0x08));',
        'case_ids': ['InvalidateSaveData-2', 'InvalidateSaveData-0', 'InvalidateSaveData-1'],
        'source': 'src/profiles/extended/home/save.c'},
    'UpdateAlbumProgress': {   'source_symbol': 'UpdateAlbumProgress',
        'before': '\tgb_write8(wTotalNumCardsCollected_ADDR, ap.e);',
        'after': '\tgb_write8(wTotalNumCardsCollected_ADDR, (uint8_t)(ap.e + 1u));',
        'case_ids': ['UpdateAlbumProgress-0'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadAlbumProgressFromSRAM': {   'source_symbol': 'LoadAlbumProgressFromSRAM',
        'before': '\tgb_write8(wTotalNumCardsToCollect_ADDR, gb_read8((uint16_t)(de + 1)));',
        'after': '\tgb_write8(wTotalNumCardsToCollect_ADDR, gb_read8((uint16_t)(de - 1)));',
        'case_ids': ['LoadAlbumProgressFromSRAM-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'ValidateBackupGeneralSaveData': {   'source_symbol': 'ValidateBackupGeneralSaveData',
        'before': '\tBankswitchSRAM(sBackupGeneralSaveData_BANK);',
        'after': '\t;',
        'case_ids': ['ValidateBackupGeneralSaveData-0'],
        'source': 'src/profiles/extended/home/save.c'},
    '_ValidateGeneralSaveData': {   'source_symbol': '_ValidateGeneralSaveData',
        'before': '\tValidateGeneralSaveDataFromDE(sGeneralSaveData_ADDR);',
        'after': '\t;',
        'case_ids': ['_ValidateGeneralSaveData-0'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadBackupSaveData': {   'source_symbol': 'LoadBackupSaveData',
        'before': '\tLoadBackupGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['LoadBackupSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    '_LoadGeneralSaveData': {   'source_symbol': '_LoadGeneralSaveData',
        'before': '{\n\tLoadGeneralSaveDataFromDE(sGeneralSaveData_ADDR);',
        'after': '{\n\t;',
        'case_ids': ['_LoadGeneralSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'SaveGeneralSaveDataFromDE': {   'source_symbol': 'SaveGeneralSaveDataFromDE',
        'before': '\tCopyGeneralSaveDataToSRAM(de);',
        'after': '\tCopyGeneralSaveDataToSRAM((uint16_t)(de ^ 1u));',
        'case_ids': ['SaveGeneralSaveDataFromDE-0'],
        'source': 'src/profiles/extended/home/save.c'},
    '_SaveGeneralSaveData': {   'source_symbol': '_SaveGeneralSaveData',
        'before': '\tget_received_legendary_cards();',
        'after': '\t;',
        'case_ids': ['_SaveGeneralSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'SaveAndBackupData': {   'source_symbol': 'SaveAndBackupData',
        'before': '\tWriteBackupGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['SaveAndBackupData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    '_SaveGame': {   'source_symbol': '_SaveGame',
        'before': '\t\tgb_write8(wTempPlayerXCoord_ADDR, 0x02);',
        'after': '\t\t;',
        'case_ids': ['_SaveGame-1'],
        'source': 'src/profiles/extended/home/save.c'},
    'SaveGeneralSaveData': {   'source_symbol': 'SaveGeneralSaveData',
        'before': '\t_SaveGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['SaveGeneralSaveData-0'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadGeneralSaveData': {   'source_symbol': 'LoadGeneralSaveData',
        'before': '\t_LoadGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['LoadGeneralSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'ValidateGeneralSaveData': {   'source_symbol': 'ValidateGeneralSaveData',
        'before': 'ValidateResult ValidateGeneralSaveData(void)\n{',
        'after': 'ValidateResult ValidateGeneralSaveData(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['ValidateGeneralSaveData-0'],
        'source': 'src/profiles/extended/home/save.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
