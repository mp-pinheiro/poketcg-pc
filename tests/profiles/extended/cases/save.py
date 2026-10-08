"""Extended oracle-diff cases for save: the shared cases of its unchanged routines plus Extended cases for the routines it changes."""
from tests.cases._symbols import SRAM_START, sym
from tests.cases._inherit import inherit
CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('save', remove=(
    'AddCardToCollectionAndUpdateAlbumProgress',
    'CopyGeneralSaveDataToSRAM',
    'LoadGeneralSaveDataFromDE',
    'SaveAndBackupData',
    'SaveGame',
    'SaveGeneralSaveData',
    'SaveGeneralSaveDataFromDE',
    '_AddCardToCollectionAndUpdateAlbumProgress',
    '_SaveGame',
    '_SaveGeneralSaveData',
))
OWN = (
    'CopyGeneralSaveDataToSRAM',
    'LoadAlbumProgressFromSRAM',
    'LoadBackupCardAndDeckSaveData',
    'LoadBackupSaveData',
    'LoadGeneralSaveDataFromDE',
    'SaveAndBackupData',
    'SaveGeneralSaveData',
    'SaveGeneralSaveDataFromDE',
    'UpdateAlbumProgress',
    'WriteBackupCardAndDeckSaveData',
    '_SaveGame',
    '_SaveGeneralSaveData',
)
CONTRACT.update({
    'CopyGeneralSaveDataToSRAM': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'LoadGeneralSaveDataFromDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'WriteBackupCardAndDeckSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'LoadBackupCardAndDeckSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'UpdateAlbumProgress': {'compare': ('d', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'LoadAlbumProgressFromSRAM': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'LoadBackupSaveData': {'compare': ('d', 'e', 'hl'), 'preserve': ('d', 'e', 'hl')},
    'SaveGeneralSaveDataFromDE': {'compare': ('b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    '_SaveGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'SaveAndBackupData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    '_SaveGame': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
    'SaveGeneralSaveData': {'compare': ('d', 'e'), 'preserve': ('d', 'e')},
})
CASES.update({
    'CopyGeneralSaveDataToSRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0x00,
            'ramg': True,
            'wram': {   sym("wMedalCount"): b'\x0b',
                        sym("wCurOverworldMap"): b'\x18',
                        sym("wPlayTimeCounter"): b'%',
                        sym("wPlayTimeCounter") + 1: b'2',
                        sym("wPlayTimeCounter") + 2: b'?',
                        sym("wPlayTimeCounter") + 3: b'LS',
                        sym("wOverworldMapSelection"): b'Y',
                        sym("wTempMap"): b'f',
                        sym("wTempPlayerXCoord"): b's',
                        sym("wTempPlayerYCoord"): b'\x80',
                        sym("wTempPlayerDirection"): b'\x8d',
                        sym("wActiveGameEvent"): b'\x9a',
                        sym("wDuelResult"): b'\xa7',
                        sym("wNPCDuelist"): b'\xb4',
                        sym("wChallengeHallNPC"): b'\xc1',
                        sym("wd698"): b'\xce\xd5\xdc\xe3',
                        sym("wOWMapEvents"): b'\xdb\xe2\xe9\xf0\xf7\xfe\x05\x0c\x13\x1a!',
                        sym("wSelectedPauseMenuItem"): b'\xf5',
                        sym("wSelectedPCMenuItem"): b'\x02',
                        sym("wConfigCursorYPos"): b'\x0f',
                        sym("wSelectedPCMenuItem") + 1: b'\x1c',
                        sym("wPCPackSelection"): b'\x0c',
                        sym("wPCPacks"): b'6=DKRY`gnu|\x83\x8a\x91\x98',
                        sym("wDefaultSong"): b'C',
                        sym("wDebugPauseAllowed"): b'P',
                        sym("wRonaldIsInMap"): b']',
                        sym("wMastersBeatenList"): b'jqx\x7f\x86\x8d\x94\x9b\xa2\xa9',
                        sym("wNPCDuelistDirection"): b'w',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x84',
                        sym("wReloadOverworldCallbackPtr"): b'\x91',
                        sym("wEventVars"): b"\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd\x04\x0b\x12\x19 '.5<CJQX_f"
                                b'mt{\x82\x89\x90\x97\x9e\xa5\xac\xb3\xba\xc1\xc8\xcf\xd6'
                                b'\xdd\xe4\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#*18?FMT[bipw~'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {sym("sGeneralSaveData"): 0xBB, sym("wGeneralSaveDataByteCount"): 0x02, sym("wGeneralSaveDataCheckSum"): 0x02, sym("wTempPointer"): 0x02}},
    ],
    'LoadGeneralSaveDataFromDE': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0x00,
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wPlayTimeCounter"): 0x01,
                        sym("wPlayTimeCounter") + 1: 0x01,
                        sym("wPlayTimeCounter") + 2: 0x01,
                        sym("wPlayTimeCounter") + 3: 0x02,
                        sym("wOverworldMapSelection"): 0x01,
                        sym("wTempMap"): 0x01,
                        sym("wTempPlayerXCoord"): 0x01,
                        sym("wTempPlayerYCoord"): 0x01,
                        sym("wTempPlayerDirection"): 0x01,
                        sym("wActiveGameEvent"): 0x01,
                        sym("wDuelResult"): 0x01,
                        sym("wNPCDuelist"): 0x01,
                        sym("wChallengeHallNPC"): 0x01,
                        sym("wd698"): 0x04,
                        sym("wOWMapEvents"): 0x0B,
                        sym("wSelectedPauseMenuItem"): 0x01,
                        sym("wSelectedPCMenuItem"): 0x01,
                        sym("wConfigCursorYPos"): 0x01,
                        sym("wSelectedPCMenuItem") + 1: 0x01,
                        sym("wPCPackSelection"): 0x01,
                        sym("wPCPacks"): 0x0F,
                        sym("wDefaultSong"): 0x01,
                        sym("wDebugPauseAllowed"): 0x01,
                        sym("wRonaldIsInMap"): 0x01,
                        sym("wMastersBeatenList"): 0x0A,
                        sym("wNPCDuelistDirection"): 0x01,
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): 0x01,
                        sym("wReloadOverworldCallbackPtr"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wAnimationsDisabled"): 0x01,
                        sym("wTextSpeed"): 0x01,
                        sym("wTempPointer"): 0x02}},
        {   'd': 0xB8,
            'e': 0x00,
            'sram': {   0x03: {   SRAM_START + 0x187B: b'\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")'
                                          b'07>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5'
                                          b'\xbc\xc3\xca\xd1\xd8\xdf\xe6\xed\xf4\xfb\x02\t\x10\x17\x1e%'
                                          b',3:AHOV]dkry'},
                        0x02: {   sym("sBackupGeneralSaveData") + 0x7B: b'\x80\x85\x8a\x8f\x94\x99\x9e\xa3\xa8\xad\xb2\xb7'
                                          b'\xbc\xc1\xc6\xcb\xd0\xd5\xda\xdf\xe4\xe9\xee\xf3'
                                          b'\xf8\xfd\x02\x07\x0c\x11\x16\x1b %*/49>CHMRW\\afkpuz\x7f'
                                          b'\x84\x89\x8e\x93\x98\x9d\xa2\xa7\xac\xb1\xb6\xbb'},
                        0x01: {   sym("sGfxBuffer5") + 0x47B: b'@CFILORUX[^adgjmpsvy|\x7f\x82\x85\x88\x8b\x8e\x91'
                                          b'\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac\xaf\xb2\xb5'
                                          b'\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9'
                                          b'\xdc\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd'},
                        0x00: {   sym("sGeneralSaveData"): b'\x08\x00\xb3\x00\xe3G\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
                                          b'\x9a\xa7\xb4\xc1\xce\xd5\xdc\xe3\xdb\xe2\xe9\xf0'
                                          b'\xf7\xfe\x05\x0c\x13\x1a!\x11\xf5\x02\x0f\x1c\x0c6=DKRY`'
                                          b'gnu|\x83\x8a\x91\x98CP]jqx\x7f\x86\x8d\x94\x9b\xa2'
                                          b'\xa9w\x84\x91"#$%&\'()*+,-./03456789:;<=>?@ABDEFGHIJKLMNOP'
                                          b"QRS\xc5\xcc\xd3\xda\xe1\xe8\xef\xf6\xfd\x04\x0b\x12\x19 '.5"
                                          b'<CJQX_fmt{\x82\x89\x90\x97\x9e\xa5\xac\xb3\xba\xc1'
                                          b'\xc8\xcf\xd6\xdd\xe4\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#*18?FM'
                                          b'T[bipw~',
                                  sym("sEventVars"): b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b'
                                          b'\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFG'
                                          b'HIJKLMNO'}},
            'read': {sym("wEventVars"): 0x40}},
    ],
    'WriteBackupCardAndDeckSaveData': [
        {'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'ramg': True,
            'sram': {   0x00: {   sym("sCardAndDeckSaveData"): b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
                                  sym("sSavedDeck41Cards") + 0x18: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
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
            'sread': {0x00: {sym("sCardAndDeckSaveData"): 0x0FA0, sym("sSavedDeck41Cards") + 0x18: 0x0667}, 0x02: {SRAM_START + 0x100: 0x0FA0, SRAM_START + 0x10A0: 0x0667}},
            'read': {sym("hBankSRAM"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'LoadBackupCardAndDeckSaveData': [
        {'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'wram': {sym("hBankSRAM"): b'\x03'},
            'ramg': True,
            'sram': {   0x02: {   SRAM_START + 0x100: b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
                                  SRAM_START + 0x10A0: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
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
            'sread': {0x02: {SRAM_START + 0x100: 0x0FA0, SRAM_START + 0x10A0: 0x0667}, 0x00: {sym("sCardAndDeckSaveData"): 0x0FA0, sym("sSavedDeck41Cards") + 0x18: 0x0667}},
            'read': {sym("hBankSRAM"): 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'UpdateAlbumProgress': [
        {'read': {sym("wTotalNumCardsCollected"): 0x02, sym("wTotalNumCardsToCollect"): 0x02}},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234,
         'read': {sym("wTotalNumCardsCollected"): 0x02, sym("wTotalNumCardsToCollect"): 0x02}},
        {   'd': 0xB8,
            'e': 0xFC,
            'sram': {0x01: {}},
            'sread': {0x01: {sym("sGfxBuffer5") + 0x4FE: 0x02}, 0x02: {sym("sAlbumProgress"): 0x02}},
            'read': {sym("wTotalNumCardsCollected"): 0x01, sym("wTotalNumCardsToCollect"): 0x01}},
        {   'd': 0xB8,
            'e': 0xFC,
            'sram': {0x03: {}},
            'sread': {0x03: {SRAM_START + 0x18FE: 0x02}, 0x02: {sym("sAlbumProgress"): 0x02}},
            'read': {sym("wTotalNumCardsCollected"): 0x01, sym("wTotalNumCardsToCollect"): 0x01}},
    ],
    'LoadAlbumProgressFromSRAM': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {   'd': 0xB8,
            'e': 0xFC,
            'ramg': True,
            'sram': {0x00: {sym("sEventVars") + 0x83: b'*7'}},
            'read': {sym("wTotalNumCardsCollected"): 0x01, sym("wTotalNumCardsToCollect"): 0x01}},
        {'d': 0xFF, 'e': 0xFF, 'read': {sym("wTotalNumCardsCollected"): 0x01, sym("wTotalNumCardsToCollect"): 0x01}},
    ],
    'LoadBackupSaveData': [
        {'wram': {sym("hBankROM"): b'\x04'},
         'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hBankROM"): b'\x04'},
            'instruction_budget': 0x1E8480, 'cycle_budget': 0x7A1200},
        {   'wram': {sym("hBankROM"): b'\x04'},
            'sram': {   0x02: {   sym("sBackupGeneralSaveData"): b'\x08\x00\xb3\x00\x0b=\x00\x00\x0b\x18%2?LSYfs\x80\x8d'
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
            'read': {sym("wMedalCount"): 0x01, sym("wEventVars"): 0x40},
            'sread': {0x00: {sym("sGeneralSaveData"): 0x0100}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'SaveGeneralSaveDataFromDE': [
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {sym("hBankROM"): b'\x04'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xB8,
            'e': 0x00,
            'hl': 0x1234,
            'wram': {sym("hBankROM"): b'\x04'}},
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\x07',
                        sym("wCurOverworldMap"): b'\x14',
                        sym("wPlayTimeCounter"): b'!',
                        sym("wPlayTimeCounter") + 1: b'.',
                        sym("wPlayTimeCounter") + 2: b';',
                        sym("wPlayTimeCounter") + 3: b'HO',
                        sym("wOverworldMapSelection"): b'\x05',
                        sym("wTempMap"): b'b',
                        sym("wTempPlayerXCoord"): b'o',
                        sym("wTempPlayerYCoord"): b'|',
                        sym("wTempPlayerDirection"): b'\x89',
                        sym("wActiveGameEvent"): b'\x96',
                        sym("wDuelResult"): b'\xa3',
                        sym("wNPCDuelist"): b'\xb0',
                        sym("wChallengeHallNPC"): b'\xbd',
                        sym("wd698"): b'\xca\xd1\xd8\xdf',
                        sym("wOWMapEvents"): b'\xd7\xde\xe5\xec\xf3\xfa\x01\x08\x0f\x16\x1d',
                        sym("wSelectedPauseMenuItem"): b'\xf1',
                        sym("wSelectedPCMenuItem"): b'\xfe',
                        sym("wConfigCursorYPos"): b'\x0b',
                        sym("wSelectedPCMenuItem") + 1: b'\x18',
                        sym("wPCPackSelection"): b'\x08',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'?',
                        sym("wDebugPauseAllowed"): b'L',
                        sym("wRonaldIsInMap"): b'Y',
                        sym("wMastersBeatenList"): b'fmt{\x82\x89\x90\x97\x9e\xa5',
                        sym("wNPCDuelistDirection"): b's',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x80',
                        sym("wReloadOverworldCallbackPtr"): b'\x8d',
                        sym("wEventVars"): b'\xe0\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB}}},
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\t',
                        sym("wCurOverworldMap"): b'\x16',
                        sym("wPlayTimeCounter"): b'#',
                        sym("wPlayTimeCounter") + 1: b'0',
                        sym("wPlayTimeCounter") + 2: b'=',
                        sym("wPlayTimeCounter") + 3: b'JQ',
                        sym("wOverworldMapSelection"): b'\x06',
                        sym("wTempMap"): b'd',
                        sym("wTempPlayerXCoord"): b'q',
                        sym("wTempPlayerYCoord"): b'~',
                        sym("wTempPlayerDirection"): b'\x8b',
                        sym("wActiveGameEvent"): b'\x98',
                        sym("wDuelResult"): b'\xa5',
                        sym("wNPCDuelist"): b'\xb2',
                        sym("wChallengeHallNPC"): b'\xbf',
                        sym("wd698"): b'\xcc\xd3\xda\xe1',
                        sym("wOWMapEvents"): b'\xd9\xe0\xe7\xee\xf5\xfc\x03\n\x11\x18\x1f',
                        sym("wSelectedPauseMenuItem"): b'\xf3',
                        sym("wSelectedPCMenuItem"): b'\x00',
                        sym("wConfigCursorYPos"): b'\r',
                        sym("wSelectedPCMenuItem") + 1: b'\x1a',
                        sym("wPCPackSelection"): b'\n',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'A',
                        sym("wDebugPauseAllowed"): b'N',
                        sym("wRonaldIsInMap"): b'[',
                        sym("wMastersBeatenList"): b'hov}\x84\x8b\x92\x99\xa0\xa7',
                        sym("wNPCDuelistDirection"): b'u',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x82',
                        sym("wReloadOverworldCallbackPtr"): b'\x8f',
                        sym("wEventVars"): b'\xff\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB}}},
        {   'd': 0xB8,
            'e': 0x00,
            'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\x0b',
                        sym("wCurOverworldMap"): b'\x18',
                        sym("wPlayTimeCounter"): b'%',
                        sym("wPlayTimeCounter") + 1: b'2',
                        sym("wPlayTimeCounter") + 2: b'?',
                        sym("wPlayTimeCounter") + 3: b'LS',
                        sym("wOverworldMapSelection"): b'\x02',
                        sym("wTempMap"): b'f',
                        sym("wTempPlayerXCoord"): b's',
                        sym("wTempPlayerYCoord"): b'\x80',
                        sym("wTempPlayerDirection"): b'\x8d',
                        sym("wActiveGameEvent"): b'\x9a',
                        sym("wDuelResult"): b'\xa7',
                        sym("wNPCDuelist"): b'\xb4',
                        sym("wChallengeHallNPC"): b'\xc1',
                        sym("wd698"): b'\xce\xd5\xdc\xe3',
                        sym("wOWMapEvents"): b'\xdb\xe2\xe9\xf0\xf7\xfe\x05\x0c\x13\x1a!',
                        sym("wSelectedPauseMenuItem"): b'\xf5',
                        sym("wSelectedPCMenuItem"): b'\x02',
                        sym("wConfigCursorYPos"): b'\x0f',
                        sym("wSelectedPCMenuItem") + 1: b'\x1c',
                        sym("wPCPackSelection"): b'\x0c',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'C',
                        sym("wDebugPauseAllowed"): b'P',
                        sym("wRonaldIsInMap"): b']',
                        sym("wMastersBeatenList"): b'jqx\x7f\x86\x8d\x94\x9b\xa2\xa9',
                        sym("wNPCDuelistDirection"): b'w',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x84',
                        sym("wReloadOverworldCallbackPtr"): b'\x91',
                        sym("wEventVars"): b'\xc0\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB}}},
    ],
    '_SaveGeneralSaveData': [
        {   'wram': {sym("hBankROM"): b'\x04'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hBankROM"): b'\x04'}},
        {   'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\x0e',
                        sym("wCurOverworldMap"): b'\x1b',
                        sym("wPlayTimeCounter"): b'(',
                        sym("wPlayTimeCounter") + 1: b'5',
                        sym("wPlayTimeCounter") + 2: b'B',
                        sym("wPlayTimeCounter") + 3: b'OV',
                        sym("wOverworldMapSelection"): b'\x02',
                        sym("wTempMap"): b'i',
                        sym("wTempPlayerXCoord"): b'v',
                        sym("wTempPlayerYCoord"): b'\x83',
                        sym("wTempPlayerDirection"): b'\x90',
                        sym("wActiveGameEvent"): b'\x9d',
                        sym("wDuelResult"): b'\xaa',
                        sym("wNPCDuelist"): b'\xb7',
                        sym("wChallengeHallNPC"): b'\xc4',
                        sym("wd698"): b'\xd1\xd8\xdf\xe6',
                        sym("wOWMapEvents"): b'\xde\xe5\xec\xf3\xfa\x01\x08\x0f\x16\x1d$',
                        sym("wSelectedPauseMenuItem"): b'\xf8',
                        sym("wSelectedPCMenuItem"): b'\x05',
                        sym("wConfigCursorYPos"): b'\x12',
                        sym("wSelectedPCMenuItem") + 1: b'\x1f',
                        sym("wPCPackSelection"): b'\x00',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'F',
                        sym("wDebugPauseAllowed"): b'S',
                        sym("wRonaldIsInMap"): b'`',
                        sym("wMastersBeatenList"): b'mt{\x82\x89\x90\x97\x9e\xa5\xac',
                        sym("wNPCDuelistDirection"): b'z',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x87',
                        sym("wReloadOverworldCallbackPtr"): b'\x94',
                        sym("wEventVars"): b'\xf0\n\x11\x18\x1f6/4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                  sym("sCardAndDeckSaveData"): b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wTotalNumCardsCollected"): 0x01,
                        sym("wTotalNumCardsToCollect"): 0x01,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB, sym("sEventVars") + 0x83: 0x02, sym("sReceivedLegendaryCards"): 0x01}}},
    ],
    'SaveAndBackupData': [
        {   'wram': {sym("hBankROM"): b'\x04'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB, sym("sEventVars") + 0x83: 0x02}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hBankROM"): b'\x04'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\r',
                        sym("wCurOverworldMap"): b'\x1a',
                        sym("wPlayTimeCounter"): b"'",
                        sym("wPlayTimeCounter") + 1: b'4',
                        sym("wPlayTimeCounter") + 2: b'A',
                        sym("wPlayTimeCounter") + 3: b'NU',
                        sym("wOverworldMapSelection"): b'\x03',
                        sym("wTempMap"): b'h',
                        sym("wTempPlayerXCoord"): b'u',
                        sym("wTempPlayerYCoord"): b'\x82',
                        sym("wTempPlayerDirection"): b'\x8f',
                        sym("wActiveGameEvent"): b'\x9c',
                        sym("wDuelResult"): b'\xa9',
                        sym("wNPCDuelist"): b'\xb6',
                        sym("wChallengeHallNPC"): b'\xc3',
                        sym("wd698"): b'\xd0\xd7\xde\xe5',
                        sym("wOWMapEvents"): b'\xdd\xe4\xeb\xf2\xf9\x00\x07\x0e\x15\x1c#',
                        sym("wSelectedPauseMenuItem"): b'\xf7',
                        sym("wSelectedPCMenuItem"): b'\x04',
                        sym("wConfigCursorYPos"): b'\x11',
                        sym("wSelectedPCMenuItem") + 1: b'\x1e',
                        sym("wPCPackSelection"): b'\x0e',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'E',
                        sym("wDebugPauseAllowed"): b'R',
                        sym("wRonaldIsInMap"): b'_',
                        sym("wMastersBeatenList"): b'lsz\x81\x88\x8f\x96\x9d\xa4\xab',
                        sym("wNPCDuelistDirection"): b'y',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x86',
                        sym("wReloadOverworldCallbackPtr"): b'\x93',
                        sym("wEventVars"): b'\xf8\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                  sym("sCardAndDeckSaveData"): b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
                                  sym("sSavedDeck41Cards") + 0x18: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wTotalNumCardsCollected"): 0x01,
                        sym("wTotalNumCardsToCollect"): 0x01,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {   0x00: {sym("sGeneralSaveData"): 0xBB, sym("sEventVars") + 0x83: 0x02},
                         0x02: {sym("sBackupGeneralSaveData"): 0xBB, sym("sAlbumProgress"): 0x02, SRAM_START + 0x100: 0x0FA0, SRAM_START + 0x10A0: 0x0667}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    '_SaveGame': [
        {   'c': 0x00,
            'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\x0f',
                        sym("wCurOverworldMap"): b'\x1c',
                        sym("wPlayTimeCounter"): b')',
                        sym("wPlayTimeCounter") + 1: b'6',
                        sym("wPlayTimeCounter") + 2: b'C',
                        sym("wPlayTimeCounter") + 3: b'PW',
                        sym("wOverworldMapSelection"): b'\x04',
                        sym("wTempMap"): b'j',
                        sym("wTempPlayerXCoord"): b'w',
                        sym("wTempPlayerYCoord"): b'\x84',
                        sym("wTempPlayerDirection"): b'\x91',
                        sym("wActiveGameEvent"): b'\x9e',
                        sym("wDuelResult"): b'\xab',
                        sym("wNPCDuelist"): b'\xb8',
                        sym("wChallengeHallNPC"): b'\xc5',
                        sym("wd698"): b'\xd2\xd9\xe0\xe7',
                        sym("wOWMapEvents"): b'\xdf\xe6\xed\xf4\xfb\x02\t\x10\x17\x1e%',
                        sym("wSelectedPauseMenuItem"): b'\xf9',
                        sym("wSelectedPCMenuItem"): b'\x06',
                        sym("wConfigCursorYPos"): b'\x13',
                        sym("wSelectedPCMenuItem") + 1: b' ',
                        sym("wPCPackSelection"): b'\x01',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'G',
                        sym("wDebugPauseAllowed"): b'T',
                        sym("wRonaldIsInMap"): b'a',
                        sym("wMastersBeatenList"): b'nu|\x83\x8a\x91\x98\x9f\xa6\xad',
                        sym("wNPCDuelistDirection"): b'{',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x88',
                        sym("wReloadOverworldCallbackPtr"): b'\x95',
                        sym("wEventVars"): b'\xfc\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc',
                        sym("wCurMap"): b'\x07',
                        sym("wPlayerXCoord"): b'\x12',
                        sym("wPlayerYCoord"): b'4',
                        sym("wPlayerDirection"): b'\x01'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                  sym("sCardAndDeckSaveData"): b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
                                  sym("sSavedDeck41Cards") + 0x18: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
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
            'read': {   sym("wTempMap"): 0x01,
                        sym("wTempPlayerXCoord"): 0x01,
                        sym("wTempPlayerYCoord"): 0x01,
                        sym("wTempPlayerDirection"): 0x01,
                        sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wTotalNumCardsCollected"): 0x01,
                        sym("wTotalNumCardsToCollect"): 0x01,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {   0x00: {sym("sGeneralSaveData"): 0xBB, sym("sEventVars") + 0x83: 0x02},
                         0x02: {sym("sBackupGeneralSaveData"): 0xBB, sym("sAlbumProgress"): 0x02, SRAM_START + 0x100: 0x0FA0, SRAM_START + 0x10A0: 0x0667}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'c': 0x01,
            'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\x10',
                        sym("wCurOverworldMap"): b'\x1d',
                        sym("wPlayTimeCounter"): b'*',
                        sym("wPlayTimeCounter") + 1: b'7',
                        sym("wPlayTimeCounter") + 2: b'D',
                        sym("wPlayTimeCounter") + 3: b'QX',
                        sym("wOverworldMapSelection"): b'^',
                        sym("wTempMap"): b'k',
                        sym("wTempPlayerXCoord"): b'x',
                        sym("wTempPlayerYCoord"): b'\x85',
                        sym("wTempPlayerDirection"): b'\x92',
                        sym("wActiveGameEvent"): b'\x9f',
                        sym("wDuelResult"): b'\xac',
                        sym("wNPCDuelist"): b'\xb9',
                        sym("wChallengeHallNPC"): b'\xc6',
                        sym("wd698"): b'\xd3\xda\xe1\xe8',
                        sym("wOWMapEvents"): b'\xe0\xe7\xee\xf5\xfc\x03\n\x11\x18\x1f&',
                        sym("wSelectedPauseMenuItem"): b'\xfa',
                        sym("wSelectedPCMenuItem"): b'\x07',
                        sym("wConfigCursorYPos"): b'\x14',
                        sym("wSelectedPCMenuItem") + 1: b'!',
                        sym("wPCPackSelection"): b'\x02',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'H',
                        sym("wDebugPauseAllowed"): b'U',
                        sym("wRonaldIsInMap"): b'b',
                        sym("wMastersBeatenList"): b'ov}\x84\x8b\x92\x99\xa0\xa7\xae',
                        sym("wNPCDuelistDirection"): b'|',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x89',
                        sym("wReloadOverworldCallbackPtr"): b'\x96',
                        sym("wEventVars"): b'\xfe\n\x11\x18\x1f&-4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                  sym("sCardAndDeckSaveData"): b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
                                  sym("sSavedDeck41Cards") + 0x18: b'\xa3\xb4\xc5\xd6\xe7\xf8\t\x1a+<M^o\x80\x91\xa2'
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
            'read': {   sym("wTempMap"): 0x01,
                        sym("wTempPlayerXCoord"): 0x01,
                        sym("wTempPlayerYCoord"): 0x01,
                        sym("wTempPlayerDirection"): 0x01,
                        sym("wOverworldMapSelection"): 0x01,
                        sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wTotalNumCardsCollected"): 0x01,
                        sym("wTotalNumCardsToCollect"): 0x01,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {   0x00: {sym("sGeneralSaveData"): 0xBB, sym("sEventVars") + 0x83: 0x02},
                         0x02: {sym("sBackupGeneralSaveData"): 0xBB, sym("sAlbumProgress"): 0x02, SRAM_START + 0x100: 0x0FA0, SRAM_START + 0x10A0: 0x0667}},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0x01,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hBankROM"): b'\x04'},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'SaveGeneralSaveData': [
        {   'wram': {sym("hBankROM"): b'\x04'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {sym("hBankROM"): b'\x04'}},
        {   'wram': {   sym("hBankROM"): b'\x04',
                        sym("wMedalCount"): b'\x0e',
                        sym("wCurOverworldMap"): b'\x1b',
                        sym("wPlayTimeCounter"): b'(',
                        sym("wPlayTimeCounter") + 1: b'5',
                        sym("wPlayTimeCounter") + 2: b'B',
                        sym("wPlayTimeCounter") + 3: b'OV',
                        sym("wOverworldMapSelection"): b'\x02',
                        sym("wTempMap"): b'i',
                        sym("wTempPlayerXCoord"): b'v',
                        sym("wTempPlayerYCoord"): b'\x83',
                        sym("wTempPlayerDirection"): b'\x90',
                        sym("wActiveGameEvent"): b'\x9d',
                        sym("wDuelResult"): b'\xaa',
                        sym("wNPCDuelist"): b'\xb7',
                        sym("wChallengeHallNPC"): b'\xc4',
                        sym("wd698"): b'\xd1\xd8\xdf\xe6',
                        sym("wOWMapEvents"): b'\xde\xe5\xec\xf3\xfa\x01\x08\x0f\x16\x1d$',
                        sym("wSelectedPauseMenuItem"): b'\xf8',
                        sym("wSelectedPCMenuItem"): b'\x05',
                        sym("wConfigCursorYPos"): b'\x12',
                        sym("wSelectedPCMenuItem") + 1: b'\x1f',
                        sym("wPCPackSelection"): b'\x00',
                        sym("wPCPacks"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        sym("wDefaultSong"): b'F',
                        sym("wDebugPauseAllowed"): b'S',
                        sym("wRonaldIsInMap"): b'`',
                        sym("wMastersBeatenList"): b'mt{\x82\x89\x90\x97\x9e\xa5\xac',
                        sym("wNPCDuelistDirection"): b'z',
                        sym("wMultichoiceTextboxResult_ChooseDeckToDuelAgainst"): b'\x87',
                        sym("wReloadOverworldCallbackPtr"): b'\x94',
                        sym("wEventVars"): b'\xf0\n\x11\x18\x1f6/4;BIPW^elsz\x81\x88\x8f\x96\x9d\xa4'
                                b'\xab\xb2\xb9\xc0\xc7\xce\xd5\xdc\xe3\xea\xf1\xf8\xff\x06\r\x14\x1b")0'
                                b'7>ELSZahov}\x84\x8b\x92\x99\xa0\xa7\xae\xb5\xbc'},
            'sram': {   0x00: {   sym("sGeneralSaveData"): b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
                                  sym("sCardAndDeckSaveData"): b'\x03\x14%6GXiz\x8b\x9c\xad\xbe\xcf\xe0\xf1\x02\x13$5F'
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
            'read': {   sym("wMedalCount"): 0x01,
                        sym("wCurOverworldMap"): 0x01,
                        sym("wLoadedEventBits"): 0x01,
                        sym("wEventVars"): 0x40,
                        sym("wPCPacks"): 0x0F,
                        sym("wTotalNumCardsCollected"): 0x01,
                        sym("wTotalNumCardsToCollect"): 0x01,
                        sym("wGeneralSaveDataByteCount"): 0x02,
                        sym("wGeneralSaveDataCheckSum"): 0x02,
                        sym("wTempPointer"): 0x02},
            'sread': {0x00: {sym("sGeneralSaveData"): 0xBB, sym("sEventVars") + 0x83: 0x02, sym("sReceivedLegendaryCards"): 0x01}}},
    ],
})
MUTATIONS.update({
    'CopyGeneralSaveDataToSRAM': {   'source_symbol': 'CopyGeneralSaveDataToSRAM',
        'before': '\t\tif (src == 0)',
        'after': '\t\tif (src != 0)',
        'case_ids': ['CopyGeneralSaveDataToSRAM-2'],
        'source': 'src/home/save.c'},
    'LoadGeneralSaveDataFromDE': {   'source_symbol': 'LoadGeneralSaveDataFromDE',
        'before': '\t\tif (dst == 0)',
        'after': '\t\tif (dst != 0)',
        'case_ids': ['LoadGeneralSaveDataFromDE-2'],
        'source': 'src/home/save.c'},
    'WriteBackupCardAndDeckSaveData': {   'source_symbol': 'WriteBackupCardAndDeckSaveData',
        'before': 'void WriteBackupCardAndDeckSaveData(void)\n{',
        'after': 'void WriteBackupCardAndDeckSaveData(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['WriteBackupCardAndDeckSaveData-0'],
        'source': 'src/home/save.c'},
    'LoadBackupCardAndDeckSaveData': {   'source_symbol': 'LoadBackupCardAndDeckSaveData',
        'before': 'void LoadBackupCardAndDeckSaveData(void)\n{',
        'after': 'void LoadBackupCardAndDeckSaveData(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);',
        'case_ids': ['LoadBackupCardAndDeckSaveData-0'],
        'source': 'src/home/save.c'},
    'UpdateAlbumProgress': {   'source_symbol': 'UpdateAlbumProgress',
        'before': '\tgb_write8(wTotalNumCardsCollected_ADDR, ap.e);',
        'after': '\tgb_write8(wTotalNumCardsCollected_ADDR, (uint8_t)(ap.e + 1u));',
        'case_ids': ['UpdateAlbumProgress-0'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadAlbumProgressFromSRAM': {   'source_symbol': 'LoadAlbumProgressFromSRAM',
        'before': '\tgb_write8(wTotalNumCardsToCollect_ADDR, gb_read8((uint16_t)(de + 2u)));',
        'after': '\tgb_write8(wTotalNumCardsToCollect_ADDR, gb_read8((uint16_t)(de + 1u)));',
        'case_ids': ['LoadAlbumProgressFromSRAM-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'LoadBackupSaveData': {   'source_symbol': 'LoadBackupSaveData',
        'before': '\tLoadBackupGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['LoadBackupSaveData-2'],
        'source': 'src/profiles/extended/home/save.c'},
    'SaveGeneralSaveDataFromDE': {   'source_symbol': 'SaveGeneralSaveDataFromDE',
        'before': '\tCopyGeneralSaveDataToSRAM(de);',
        'after': '\tCopyGeneralSaveDataToSRAM((uint16_t)(de ^ 1u));',
        'case_ids': ['SaveGeneralSaveDataFromDE-0'],
        'source': 'src/home/save.c'},
    '_SaveGeneralSaveData': {   'source_symbol': '_SaveGeneralSaveData',
        'before': '\tget_received_legendary_cards();',
        'after': '\t;',
        'case_ids': ['_SaveGeneralSaveData-2'],
        'source': 'src/home/save.c'},
    'SaveAndBackupData': {   'source_symbol': 'SaveAndBackupData',
        'before': '\tWriteBackupGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['SaveAndBackupData-2'],
        'source': 'src/home/save.c'},
    '_SaveGame': {   'source_symbol': '_SaveGame',
        'before': '\t\tgb_write8(wTempPlayerXCoord_ADDR, 0x02);',
        'after': '\t\t;',
        'case_ids': ['_SaveGame-1'],
        'source': 'src/home/save.c'},
    'SaveGeneralSaveData': {   'source_symbol': 'SaveGeneralSaveData',
        'before': '\t_SaveGeneralSaveData();',
        'after': '\t;',
        'case_ids': ['SaveGeneralSaveData-0'],
        'source': 'src/home/save.c'},
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES.update(legacy_to_schema({fn: CASES[fn] for fn in OWN}, CONTRACT))
