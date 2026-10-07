"""Extended oracle-diff cases for map, seeded from tests/cases/map.py."""

CONTRACT = {
    'GetPermissionByteOfMapPosition': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GetPermissionOfMapPosition': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'SetPermissionOfMapPosition': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('a', 'b', 'c', 'd', 'e', 'hl')},
    'UpdatePermissionOfMapPosition': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetLoadedNPCID': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GetItemInLoadedNPCIndex': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e')},
    'GameEvent_Overworld': {'compare': ('f', 'a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('a', 'b', 'c', 'd', 'e', 'hl')},
    'CopyGfxDataFromTempBank': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('f', 'c')},
    'FindLoadedNPC': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetNextNPCMovementByte': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'GetDefaultSong': {'compare': ('a', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'PlayDefaultSong': {'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'), 'preserve': ('b', 'c', 'd', 'e', 'hl')},
    'HandleMapWarp': {'compare': (), 'preserve': ()},
    'GetReceivedLegendaryCards': {   'compare': ('a', 'f', 'b', 'c', 'd', 'e', 'hl'),
    'preserve': ('b', 'c', 'd', 'e', 'hl'),
    'sram_out': True},
    'OverworldDoFrameFunction': {'compare': (), 'preserve': (), 'wram_out': True},
    'GameEvent_Duel': {'compare': (), 'preserve': ()},
    'GameEvent_ChallengeMachine': {'compare': (), 'preserve': ()},
    'GameEvent_Credits': {'compare': (), 'preserve': ()},
    'GameEvent_ContinueDuel': {'compare': ('a', 'f'), 'preserve': ()},
    '_ExecuteGameEvent': {'compare': ('f',), 'preserve': ()},
    'ExecuteGameEvent': {'compare': (), 'preserve': ()},
}

CASES = {
    'GetPermissionByteOfMapPosition': [
        {   'b': 0x04,
            'c': 0x08,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x1F,
            'c': 0x2F,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
    ],
    'GetPermissionOfMapPosition': [
        {   'b': 0x04,
            'c': 0x08,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x1F,
            'c': 0x2F,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
    ],
    'SetPermissionOfMapPosition': [
        {   'a': 0x5A,
            'b': 0x04,
            'c': 0x08,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
        {   'a': 0xC3,
            'f': 0xF0,
            'b': 0x1F,
            'c': 0x2F,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
    ],
    'UpdatePermissionOfMapPosition': [
        {   'a': 0x0F,
            'b': 0x04,
            'c': 0x08,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
        {   'a': 0xF0,
            'f': 0xF0,
            'b': 0x1F,
            'c': 0x2F,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD120: b'\x07\n\r\x10\x13\x16\x19\x1c\x1f"%(+.147:=@CFILORUX[^adgjmpsvy|'
                                b'\x7f\x82\x85\x88\x8b\x8e\x91\x94\x97\x9a\x9d\xa0\xa3\xa6\xa9\xac'
                                b'\xaf\xb2\xb5\xb8\xbb\xbe\xc1\xc4\xc7\xca\xcd\xd0\xd3\xd6\xd9\xdc'
                                b'\xdf\xe2\xe5\xe8\xeb\xee\xf1\xf4\xf7\xfa\xfd\x00\x03\x06\t\x0c'
                                b"\x0f\x12\x15\x18\x1b\x1e!$'*-0369<?BEHKNQTWZ]`cfilorux{~\x81\x84"
                                b'\x87\x8a\x8d\x90\x93\x96\x99\x9c\x9f\xa2\xa5\xa8\xab\xae\xb1\xb4'
                                b'\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xcf\xd2\xd5\xd8\xdb\xde\xe1\xe4'
                                b'\xe7\xea\xed\xf0\xf3\xf6\xf9\xfc\xff\x02\x05\x08\x0b\x0e\x11\x14'
                                b'\x17\x1a\x1d #&),/258;>ADGJMPSVY\\_behknqtwz}\x80\x83\x86\x89\x8c'
                                b'\x8f\x92\x95\x98\x9b\x9e\xa1\xa4\xa7\xaa\xad\xb0\xb3\xb6\xb9\xbc'
                                b'\xbf\xc2\xc5\xc8\xcb\xce\xd1\xd4\xd7\xda\xdd\xe0\xe3\xe6\xe9\xec'
                                b'\xef\xf2\xf5\xf8\xfb\xfe\x01\x04'},
            'read': {0xD120: 0x0100}},
    ],
    'GetLoadedNPCID': [
        {   'a': 0x00,
            'wram': {   0xD337: b'\x01\x06\x0b\x10\x15\x1a\x1f$).38=BGLQV[`ejoty~\x83\x88'
                                b'\x8d\x92\x97\x9c\xa1\xa6\xab\xb0\xb5\xba\xbf\xc4\xc9\xce\xd3\xd8'
                                b'\xdd\xe2\xe7\xec\xf1\xf6\xfb\x00\x05\n\x0f\x14\x19\x1e#(-27<AFKPUZ_d'
                                b'insx}\x82\x87\x8c\x91\x96\x9b\xa0\xa5\xaa\xaf\xb4\xb9\xbe\xc3\xc8'
                                b'\xcd\xd2\xd7\xdc'},
            'read': {0xD337: 0x60}},
        {   'a': 0x07,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\x01\x06\x0b\x10\x15\x1a\x1f$).38=BGLQV[`ejoty~\x83\x88'
                                b'\x8d\x92\x97\x9c\xa1\xa6\xab\xb0\xb5\xba\xbf\xc4\xc9\xce\xd3\xd8'
                                b'\xdd\xe2\xe7\xec\xf1\xf6\xfb\x00\x05\n\x0f\x14\x19\x1e#(-27<AFKPUZ_d'
                                b'insx}\x82\x87\x8c\x91\x96\x9b\xa0\xa5\xaa\xaf\xb4\xb9\xbe\xc3\xc8'
                                b'\xcd\xd2\xd7\xdc'},
            'read': {0xD337: 0x60}},
        {   'a': 0xFF,
            'wram': {   0xD337: b'\x01\x06\x0b\x10\x15\x1a\x1f$).38=BGLQV[`ejoty~\x83\x88'
                                b'\x8d\x92\x97\x9c\xa1\xa6\xab\xb0\xb5\xba\xbf\xc4\xc9\xce\xd3\xd8'
                                b'\xdd\xe2\xe7\xec\xf1\xf6\xfb\x00\x05\n\x0f\x14\x19\x1e#(-27<AFKPUZ_d'
                                b'insx}\x82\x87\x8c\x91\x96\x9b\xa0\xa5\xaa\xaf\xb4\xb9\xbe\xc3\xc8'
                                b'\xcd\xd2\xd7\xdc'},
            'read': {0xD337: 0x60}},
    ],
    'GetItemInLoadedNPCIndex': [
        {   'a': 0x00,
            'hl': 0x00,
            'wram': {   0xD337: b'\x01\x06\x0b\x10\x15\x1a\x1f$).38=BGLQV[`ejoty~\x83\x88'
                                b'\x8d\x92\x97\x9c\xa1\xa6\xab\xb0\xb5\xba\xbf\xc4\xc9\xce\xd3\xd8'
                                b'\xdd\xe2\xe7\xec\xf1\xf6\xfb\x00\x05\n\x0f\x14\x19\x1e#(-27<AFKPUZ_d'
                                b'insx}\x82\x87\x8c\x91\x96\x9b\xa0\xa5\xaa\xaf\xb4\xb9\xbe\xc3\xc8'
                                b'\xcd\xd2\xd7\xdc'},
            'read': {0xD337: 0x60}},
        {   'a': 0x03,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x0B,
            'wram': {   0xD337: b'\x01\x06\x0b\x10\x15\x1a\x1f$).38=BGLQV[`ejoty~\x83\x88'
                                b'\x8d\x92\x97\x9c\xa1\xa6\xab\xb0\xb5\xba\xbf\xc4\xc9\xce\xd3\xd8'
                                b'\xdd\xe2\xe7\xec\xf1\xf6\xfb\x00\x05\n\x0f\x14\x19\x1e#(-27<AFKPUZ_d'
                                b'insx}\x82\x87\x8c\x91\x96\x9b\xa0\xa5\xaa\xaf\xb4\xb9\xbe\xc3\xc8'
                                b'\xcd\xd2\xd7\xdc'},
            'read': {0xD337: 0x60}},
        {   'a': 0x08,
            'hl': 0x00,
            'wram': {   0xD337: b'\x01\x06\x0b\x10\x15\x1a\x1f$).38=BGLQV[`ejoty~\x83\x88'
                                b'\x8d\x92\x97\x9c\xa1\xa6\xab\xb0\xb5\xba\xbf\xc4\xc9\xce\xd3\xd8'
                                b'\xdd\xe2\xe7\xec\xf1\xf6\xfb\x00\x05\n\x0f\x14\x19\x1e#(-27<AFKPUZ_d'
                                b'insx}\x82\x87\x8c\x91\x96\x9b\xa0\xa5\xaa\xaf\xb4\xb9\xbe\xc3\xc8'
                                b'\xcd\xd2\xd7\xdc'},
            'read': {0xD337: 0x60}},
    ],
    'GameEvent_Overworld': [
        {},
        {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC, 'd': 0xDD, 'e': 0xEE, 'hl': 0x1234},
        {'f': 0x60},
        {'f': 0x80},
    ],
    'CopyGfxDataFromTempBank': [
        {   'b': 0x01,
            'c': 0x01,
            'hl': 0xC100,
            'd': 0xC4,
            'e': 0xF0,
            'wram': {0xFF80: b'\x01', 0xD4B3: b'\x01', 0xC100: b'\x05'},
            'read': {0xFF80: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0x04,
            'c': 0x03,
            'd': 0xC4,
            'e': 0xF0,
            'hl': 0xC100,
            'wram': {   0xFF80: b'\x07',
                        0xD4B3: b'\x02',
                        0xC100: b'\x05\x10\x1b&1<GR]hs~\x89\x94\x9f\xaa'},
            'read': {0xC4F0: 0x10, 0xFF80: 0x01}},
        {   'b': 0x01,
            'c': 0x00,
            'hl': 0xC100,
            'd': 0xC4,
            'e': 0xF0,
            'wram': {   0xD4B3: b'\x02',
                        0xC100: b'\x05\x10\x1b&1<GR]hs~\x89\x94\x9f\xaa\xb5\xc0\xcb\xd6\xe1\xec\xf7\x02'
                                b'\r\x18#.9DOZep{\x86\x91\x9c\xa7\xb2\xbd\xc8\xd3\xde\xe9\xf4\xff\n'
                                b'\x15 +6ALWbmx\x83\x8e\x99\xa4\xaf\xba\xc5\xd0\xdb\xe6\xf1\xfc\x07\x12'
                                b'\x1d(3>IT_ju\x80\x8b\x96\xa1\xac\xb7\xc2\xcd\xd8\xe3\xee'
                                b'\xf9\x04\x0f\x1a%0;FQ\\gr}\x88\x93\x9e\xa9\xb4\xbf\xca'
                                b'\xd5\xe0\xeb\xf6\x01\x0c\x17"-8CNYdoz\x85\x90\x9b\xa6\xb1\xbc\xc7\xd2'
                                b'\xdd\xe8\xf3\xfe\t\x14\x1f*5@KValw\x82\x8d\x98\xa3\xae'
                                b"\xb9\xc4\xcf\xda\xe5\xf0\xfb\x06\x11\x1c'2=HS^it\x7f\x8a"
                                b'\x95\xa0\xab\xb6\xc1\xcc\xd7\xe2\xed\xf8\x03\x0e\x19$/:EP[fq|\x87\x92'
                                b'\x9d\xa8\xb3\xbe\xc9\xd4\xdf\xea\xf5\x00\x0b\x16!,7BMXcny\x84\x8f\x9a'
                                b'\xa5\xb0\xbb\xc6\xd1\xdc\xe7\xf2\xfd\x08\x13\x1e)4?JU`kv'
                                b'\x81\x8c\x97\xa2\xad\xb8\xc3\xce\xd9\xe4\xef\xfa'},
            'read': {0xC4F0: 0x0104}},
        {   'b': 0x00,
            'c': 0x01,
            'hl': 0xC100,
            'd': 0xC4,
            'e': 0xF0,
            'wram': {   0xD4B3: b'\x02',
                        0xC100: b'\x05\x10\x1b&1<GR]hs~\x89\x94\x9f\xaa\xb5\xc0\xcb\xd6\xe1\xec\xf7\x02'
                                b'\r\x18#.9DOZep{\x86\x91\x9c\xa7\xb2\xbd\xc8\xd3\xde\xe9\xf4\xff\n'
                                b'\x15 +6ALWbmx\x83\x8e\x99\xa4\xaf\xba\xc5\xd0\xdb\xe6\xf1\xfc\x07\x12'
                                b'\x1d(3>IT_ju\x80\x8b\x96\xa1\xac\xb7\xc2\xcd\xd8\xe3\xee'
                                b'\xf9\x04\x0f\x1a%0;FQ\\gr}\x88\x93\x9e\xa9\xb4\xbf\xca'
                                b'\xd5\xe0\xeb\xf6\x01\x0c\x17"-8CNYdoz\x85\x90\x9b\xa6\xb1\xbc\xc7\xd2'
                                b'\xdd\xe8\xf3\xfe\t\x14\x1f*5@KValw\x82\x8d\x98\xa3\xae'
                                b"\xb9\xc4\xcf\xda\xe5\xf0\xfb\x06\x11\x1c'2=HS^it\x7f\x8a"
                                b'\x95\xa0\xab\xb6\xc1\xcc\xd7\xe2\xed\xf8\x03\x0e\x19$/:EP[fq|\x87\x92'
                                b'\x9d\xa8\xb3\xbe\xc9\xd4\xdf\xea\xf5\x00\x0b\x16!,7BMXcny\x84\x8f\x9a'
                                b'\xa5\xb0\xbb\xc6\xd1\xdc\xe7\xf2\xfd\x08\x13\x1e)4?JU`kv'
                                b'\x81\x8c\x97\xa2\xad\xb8\xc3\xce\xd9\xe4\xef\xfa'},
            'read': {0xC4F0: 0x0104}},
        {   'b': 0x01,
            'c': 0x08,
            'hl': 0x4000,
            'd': 0xC4,
            'e': 0xF0,
            'wram': {0xD4B3: b'\x03'},
            'read': {0xC4F0: 0x08, 0xFF80: 0x01}},
        {   'evidence': 'dependency-blocked',
            'reason': "b=c=0 requests a 64 KiB nested copy; it overwrites the wrapper's saved bank and "
                      'return frames before wrapper restoration can run'},
    ],
    'FindLoadedNPC': [
        {   'wram': {   0xD337: b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x04\x1d\x1e\x1f !"#$%&\'\x05$%&\'()*+,-.\x06+,-./012345\x072345678'
                                b'9:;<',
                        0xD397: b'\xee',
                        0xD399: b'\x00'},
            'read': {0xD397: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD337: b'\t\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x01\x08\t\n\x0b\x0c\r\x0e'
                                b'\x0f\x10\x11\x12\x02\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19'
                                b'\x03\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x04\x1d\x1e\x1f !"#'
                                b"$%&'\x05$%&'()*+,-.\x06+,-./012345\x0723456789:;<",
                        0xD397: b'\xee',
                        0xD399: b'\x05'},
            'read': {0xD397: 0x01}},
        {   'wram': {   0xD337: b'\x01\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x02\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x03\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x04\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x05\x1d\x1e\x1f !"#$%&\'\x06$%&\'()*+,-.\x07+,-./012345\x082345678'
                                b'9:;<',
                        0xD397: b'\xee',
                        0xD399: b'\xff'},
            'read': {0xD397: 0x01}},
        {   'wram': {   0xD337: b'\x01\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x02\x08\t\n'
                                b'\x0b\x0c\r\x0e\x0f\x10\x11\x12\x03\x0f\x10\x11\x12\x13\x14\x15'
                                b'\x16\x17\x18\x19\x04\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
                                b'\x05\x1d\x1e\x1f !"#$%&\'\x06$%&\'()*+,-.\x07+,-./012345M23456789:;<',
                        0xD397: b'\xee',
                        0xD399: b'M'},
            'read': {0xD397: 0x01}},
    ],
    'GetNextNPCMovementByte': [
        {'b': 0x00, 'c': 0x00, 'read': {0xFF80: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xC1,
            'c': 0x00,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xFF80: b'\t', 0xC100: b'B'},
            'read': {0xFF80: 0x01}},
        {'b': 0x40, 'c': 0x00, 'wram': {0xFF80: b'\x05'}, 'read': {0xFF80: 0x01}},
    ],
    'GetDefaultSong': [
        {},
        {'wram': {0xD3A5: b'\x01', 0xD0FE: b'\x05', 0xD31B: b'\x02'}},
        {'wram': {0xD3A5: b'\x01', 0xD0FE: b'\x05', 0xD31B: b'\x0b'}},
        {'wram': {0xD3A5: b'\x01', 0xD0FE: b'\x05', 0xD31B: b'\x0c'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD3A5: b'\x01', 0xD0FE: b'"', 0xD31B: b'\x01'}},
    ],
    'PlayDefaultSong': [
        {'read': {0xD7A4: 0x01, 0xD0FF: 0x01}},
        {'wram': {0xD7A4: b'\x80', 0xD0FE: b'\x05', 0xD0FF: b'\xff'}, 'read': {0xD0FF: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD7A4: b'\x80', 0xD0FE: b'\x1e', 0xD0FF: b'\x01'},
            'read': {0xD0FF: 0x01}},
        {'wram': {0xD7A4: b'\x01', 0xD0FE: b'\x05', 0xD0FF: b'\x05'}, 'read': {0xD0FF: 0x01}},
        {'wram': {0xD7A4: b'\x80', 0xD0FE: b'\x1f', 0xD0FF: b'\x01'}, 'read': {0xD0FF: 0x01}},
        {   'wram': {0xD7A4: b'\x80', 0xD0FE: b'\x05', 0xD0FF: b'\x01'},
            'read': {0xD0FF: 0x01}},
    ],
    'HandleMapWarp': [
        {   'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x00',
                        0xD31E: b'\x00',
                        0xD321: b'\x00',
                        0xD0A8: b'\x11"3D'},
            'read': {0xD0A8: 0x01, 0xD0A9: 0x01, 0xD0AA: 0x01, 0xD0AB: 0x01}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x1a',
                        0xD31E: b'\n',
                        0xD321: b'\x02',
                        0xD0A8: b'\x00\x00\x00\x00'},
            'read': {0xD0A8: 0x01, 0xD0A9: 0x01, 0xD0AA: 0x01, 0xD0AB: 0x01}},
        {   'wram': {   0xD31C: b'\x01',
                        0xD31D: b'\x0e',
                        0xD31E: b'\x1c',
                        0xD321: b'\x01',
                        0xD0A8: b'\x11"3D'},
            'read': {0xD0A8: 0x01, 0xD0A9: 0x01, 0xD0AA: 0x01, 0xD0AB: 0x01}},
        {   'wram': {   0xD31C: b'\x02',
                        0xD31D: b'\x00',
                        0xD31E: b'\n',
                        0xD321: b'\x04',
                        0xD0A8: b'\x11"3D'},
            'read': {0xD0A8: 0x01, 0xD0A9: 0x01, 0xD0AA: 0x01, 0xD0AB: 0x01}},
    ],
    'GetReceivedLegendaryCards': [
        {'sram': {0x00: {0xA00A: b'\xaa'}}, 'expect_sram': {0x00: {0xA00A: b'\x00'}}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'sram': {0x00: {0xA00A: b'U'}},
            'expect_sram': {0x00: {0xA00A: b'\x00'}}},
    ],
    'OverworldDoFrameFunction': [
        {'hram': {0xFF80: b'\x01'}, 'wram': {0xD0AE: b'\x80'}},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'hram': {0xFF80: b'\x05'},
            'wram': {0xD0AE: b'\x00', 0xD222: b'\x11', 0xD223: b'"'},
            'read': {0xD0A3: 0x01, 0xD0A4: 0x01, 0xFF80: 0x01},
            'instruction_budget': 0x1E8480,
            'cycle_budget': 0x7A1200},
    ],
    'GameEvent_Duel': [
        {   'keys': [0x00, 0x01],
            'entry_sp': 0xDCBE,
            'wram': {   0xCBC3: b'\x06',
                        0xCBC5: b'\x01',
                        0xFF97: b'\xc2',
                        0xC2F1: b'\x80',
                        0xC3F1: b'\x80',
                        0xCBB3: b'\x80',
                        0xC400: b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08',
                        0xC478: b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08',
                        0xCABB: b'\x00',
                        0xCCA0: b'\x01',
                        0xD417: b'\xff',
                        0xD4AD: b'\xff',
                        0xD410: b'\xff\xff\xff\xff\xff\xff\xff',
                        0xCAD3: b'\xc92',
                        0xD499: b'\x00',
                        0xD49A: b'\x08',
                        0xCBC4: b'\x01',
                        0xD0AF: b'\x00',
                        0xD0FF: b'\xaa'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'sram': {   0x00: {   0xBA44: b'\xaa',
                                  0xB668: b'\x00',
                                  0xA318: b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'}},
            'read': {0xD0AF: 0x01, 0xD0FF: 0x01},
            'sread': {0x00: {0xBA44: 0x01}},
            'instruction_budget': 0xBEBC200,
            'cycle_budget': 0x2FAF0800},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'keys': [0x00, 0x01],
            'entry_sp': 0xDCBE,
            'wram': {   0xCBC3: b'\x06',
                        0xCBC5: b'\x01',
                        0xFF97: b'\xc2',
                        0xC2F1: b'\x80',
                        0xC3F1: b'\x80',
                        0xCBB3: b'\x80',
                        0xC400: b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08',
                        0xC478: b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08',
                        0xCABB: b'\x00',
                        0xCCA0: b'\x01',
                        0xD417: b'\xff',
                        0xD4AD: b'\xff',
                        0xD410: b'\xff\xff\xff\xff\xff\xff\xff',
                        0xCAD3: b'\xc92',
                        0xD499: b'\x00',
                        0xD49A: b'\x08',
                        0xCBC4: b'\x01',
                        0xD0AF: b'\x00',
                        0xD0FF: b'\xaa'},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'sram': {   0x00: {   0xBA44: b'\xaa',
                                  0xB668: b'\x00',
                                  0xA318: b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
                                          b'\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'}},
            'read': {0xD0AF: 0x01, 0xD0FF: 0x01},
            'sread': {0x00: {0xBA44: 0x01}},
            'instruction_budget': 0xBEBC200,
            'cycle_budget': 0x2FAF0800},
    ],
    'GameEvent_ChallengeMachine': [
        {   'ramg': False,
            'sram': {0x00: {0xBA44: b'\xaa'}},
            'wram': {0xD0FE: b'U', 0xD7A4: b'\x80'},
            'sread': {0x00: {0xBA44: 0x01}},
            'read': {0xD0FE: 0x01},
            'expect': {0xD0FE: b'\x06'},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'ramg': False,
            'sram': {0x00: {0xBA44: b'U'}},
            'wram': {0xD0FE: b'\xaa', 0xD7A4: b'\x80'},
            'sread': {0x00: {0xBA44: 0x01}},
            'read': {0xD0FE: 0x01},
            'expect': {0xD0FE: b'\x06'},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'GameEvent_Credits': [
        {   'wram': {   0xD7A4: b'\x7f',
                        0xD311: b'\xff',
                        0xD3A8: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCABB: b'\xc3',
                        0xFF40: b'\xc3'},
            'read': {   0xD311: 0x01,
                        0xD7A4: 0x01,
                        0xD3A8: 0x0A,
                        0xCAD3: 0x02,
                        0xD635: 0x01,
                        0xD644: 0x01,
                        0xFF41: 0x01,
                        0xFF45: 0x01},
            'ramg': True,
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {   0xD7A4: b'\x7f',
                        0xD311: b'\xff',
                        0xD3A8: b'\x03\x07\x00\x00\x00\x00\x00\x00\x00\x00',
                        0xCABB: b'\xc3',
                        0xFF40: b'\xc3'},
            'read': {   0xD311: 0x01,
                        0xD7A4: 0x01,
                        0xD3A8: 0x0A,
                        0xCAD3: 0x02,
                        0xD635: 0x01,
                        0xD644: 0x01,
                        0xFF41: 0x01,
                        0xFF45: 0x01},
            'ramg': True,
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    'GameEvent_ContinueDuel': [
        {   'wram': {0xCABB: b'\x00', 0xCBB1: b'\xa5', 0xD0FF: b'U'},
            'sram': {0x00: {0xBC00: b'\x00', 0xBA44: b'\x00'}},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'read': {0xD0FF: 0x01},
            'sread': {0x00: {0xBA44: 0x01}},
            'expect_regs': {'a': 0x00, 'f': 0x10},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCABB: b'\x00', 0xCBB1: b'\xa5', 0xD0FF: b'\xaa'},
            'sram': {0x00: {0xBC00: b'\x00', 0xBA44: b'\x01'}},
            'setup': [{'fn': 'CopyDMAFunction'}, {'fn': 'SetupText', 'd': 0x20, 'e': 0x40}],
            'keys': [0x00, 0x01],
            'read': {0xD0FF: 0x01},
            'sread': {0x00: {0xBA44: 0x01}},
            'expect_regs': {'a': 0x01, 'f': 0x10},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
    '_ExecuteGameEvent': [
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xD0A2: b'\x00', 0xD0FE: b'U'},
            'read': {0xD0FE: 0x01},
            'expect': {0xD0FE: b'U'},
            'expect_regs': {'f': 0x10}},
        {   'oracle': False,
            'evidence': 'native-stress',
            'why': 'The bounded native fallback models the challenge-machine event prefix without '
                   'entering its interactive UI loop.',
            'wram': {0xD0A2: b'\x07', 0xD0FE: b'U'},
            'read': {0xD0FE: 0x01},
            'expect': {0xD0FE: b'\x06'},
            'expect_regs': {'f': 0x10}},
    ],
    'ExecuteGameEvent': [
        {   'wram': {0xCAC4: b'\x00'},
            'read': {0xCAC4: 0x01},
            'expect': {0xCAC4: b'\x01'},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
        {   'a': 0xAA,
            'f': 0xF0,
            'b': 0xBB,
            'c': 0xCC,
            'd': 0xDD,
            'e': 0xEE,
            'hl': 0x1234,
            'wram': {0xCAC4: b'\x00'},
            'read': {0xCAC4: 0x01},
            'expect': {0xCAC4: b'\x01'},
            'instruction_budget': 0x1312D00,
            'cycle_budget': 0x4C4B400},
    ],
}

MUTATIONS = {
    'GetPermissionByteOfMapPosition': {   'source_symbol': 'GetPermissionByteOfMapPosition',
        'before': '\treturn (PermissionResult){(uint8_t)(hl - wPermissionMap_ADDR), hl};',
        'after': '\treturn (PermissionResult){(uint8_t)(hl + wPermissionMap_ADDR), hl};',
        'case_ids': ['GetPermissionByteOfMapPosition-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'GetPermissionOfMapPosition': {   'source_symbol': 'GetPermissionOfMapPosition',
        'before': 'return gb_read8(permission_address(b, c));',
        'after': 'return (uint8_t)(gb_read8(permission_address(b, c)) ^ 1u);',
        'case_ids': ['GetPermissionOfMapPosition-0', 'GetPermissionOfMapPosition-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'SetPermissionOfMapPosition': {   'source_symbol': 'SetPermissionOfMapPosition',
        'before': '\tgb_write8(permission_address(b, c), a);',
        'after': '\t;',
        'case_ids': ['SetPermissionOfMapPosition-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'UpdatePermissionOfMapPosition': {   'source_symbol': 'UpdatePermissionOfMapPosition',
        'before': '\tuint8_t result = (uint8_t)(gb_read8(address) & (uint8_t)~a);',
        'after': '\tuint8_t result = (uint8_t)(gb_read8(address) | (uint8_t)~a);',
        'case_ids': ['UpdatePermissionOfMapPosition-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'GetLoadedNPCID': {   'source_symbol': 'GetLoadedNPCID',
        'before': '\treturn GetItemInLoadedNPCIndex(a, 0);',
        'after': '\treturn GetItemInLoadedNPCIndex((uint8_t)(a ^ 1u), 0);',
        'case_ids': ['GetLoadedNPCID-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'GetItemInLoadedNPCIndex': {   'source_symbol': 'GetItemInLoadedNPCIndex',
        'before': '\tif (a >= 8u)',
        'after': '\tif (a > 8u)',
        'case_ids': ['GetItemInLoadedNPCIndex-2'],
        'source': 'src/profiles/extended/home/map.c'},
    'GameEvent_Overworld': {   'source_symbol': 'GameEvent_Overworld',
        'before': '\treturn (uint8_t)((f & 0x80u) | 0x10u);',
        'after': '\treturn (uint8_t)((f | 0x80u) | 0x10u);',
        'case_ids': ['GameEvent_Overworld-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'CopyGfxDataFromTempBank': {   'source_symbol': 'CopyGfxDataFromTempBank',
        'before': '\tBankswitchROM(wTempPointerBank);',
        'after': '\t;',
        'case_ids': ['CopyGfxDataFromTempBank-4'],
        'source': 'src/profiles/extended/home/map.c'},
    'FindLoadedNPC': {   'source_symbol': 'FindLoadedNPC',
        'before': '\t\tif (gb_read8(entry) == target) {',
        'after': '\t\tif (gb_read8(entry) != target) {',
        'case_ids': ['FindLoadedNPC-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'GetNextNPCMovementByte': {   'source_symbol': 'GetNextNPCMovementByte',
        'before': '\treturn value;',
        'after': '\treturn 1u + value;',
        'case_ids': ['GetNextNPCMovementByte-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'GetDefaultSong': {   'source_symbol': 'GetDefaultSong',
        'before': '\tif (wOverworldMapSelection == OWMAP_ISHIHARAS_HOUSE',
        'after': '\tif (wOverworldMapSelection != OWMAP_ISHIHARAS_HOUSE',
        'case_ids': ['GetDefaultSong-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'PlayDefaultSong': {   'source_symbol': 'PlayDefaultSong',
        'before': 'wSongOverride = song;',
        'after': 'wSongOverride = (uint8_t)(song ^ 1u);',
        'case_ids': ['PlayDefaultSong-1', 'PlayDefaultSong-2'],
        'source': 'src/profiles/extended/home/map.c'},
    'HandleMapWarp': {   'source_symbol': 'HandleMapWarp',
        'before': '(void)_HandleMapWarp();',
        'after': '',
        'case_ids': ['HandleMapWarp-1', 'HandleMapWarp-2', 'HandleMapWarp-3'],
        'source': 'src/profiles/extended/home/map.c'},
    'GetReceivedLegendaryCards': {   'source_symbol': 'GetReceivedLegendaryCards',
        'before': '\tsReceivedLegendaryCards = a;',
        'after': '\tsReceivedLegendaryCards = (uint8_t)(a ^ 1u);',
        'case_ids': ['GetReceivedLegendaryCards-0', 'GetReceivedLegendaryCards-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'OverworldDoFrameFunction': {   'source_symbol': 'OverworldDoFrameFunction',
        'before': 'BankswitchROM(saved_bank);',
        'after': 'BankswitchROM(0u);',
        'case_ids': ['OverworldDoFrameFunction-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'GameEvent_Duel': {   'source_symbol': 'GameEvent_Duel',
        'before': 'uint8_t GameEvent_Duel(void)\n{\n\twActiveGameEvent = GAME_EVENT_DUEL;',
        'after': 'uint8_t GameEvent_Duel(void)\n{\n\twActiveGameEvent = 0u;',
        'case_ids': ['GameEvent_Duel-0', 'GameEvent_Duel-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'GameEvent_ChallengeMachine': {   'source_symbol': 'GameEvent_ChallengeMachine',
        'before': 'uint8_t GameEvent_ChallengeMachine(void)\n'
                  '{\n'
                  '\twDefaultSong = MUSIC_PC_MAIN_MENU;',
        'after': 'uint8_t GameEvent_ChallengeMachine(void)\n{\n\twDefaultSong = MUSIC_OVERWORLD;',
        'case_ids': ['GameEvent_ChallengeMachine-0', 'GameEvent_ChallengeMachine-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'GameEvent_Credits': {   'source_symbol': 'GameEvent_Credits',
        'before': '\t(void)PlayCreditsSequence();',
        'after': '\tPlaySong(0u);',
        'case_ids': ['GameEvent_Credits-0', 'GameEvent_Credits-1'],
        'source': 'src/profiles/extended/home/map.c'},
    'GameEvent_ContinueDuel': {   'source_symbol': 'GameEvent_ContinueDuel',
        'before': 'SongResult GameEvent_ContinueDuel(void)\n{\n\twSongOverride = 0u;',
        'after': 'SongResult GameEvent_ContinueDuel(void)\n{\n\twSongOverride = 1u;',
        'case_ids': ['GameEvent_ContinueDuel-0', 'GameEvent_ContinueDuel-1'],
        'source': 'src/profiles/extended/home/map.c'},
    '_ExecuteGameEvent': {   'source_symbol': '_ExecuteGameEvent',
        'before': 'uint8_t _ExecuteGameEvent(void)\n{\n\tuint8_t event = wGameEvent;',
        'after': 'uint8_t _ExecuteGameEvent(void)\n{\n\tuint8_t event = 7u;',
        'case_ids': ['_ExecuteGameEvent-0'],
        'source': 'src/profiles/extended/home/map.c'},
    'ExecuteGameEvent': {   'source_symbol': 'ExecuteGameEvent',
        'before': '\twPlayTimeCounterEnable = 1u;',
        'after': '\twPlayTimeCounterEnable = 0u;',
        'case_ids': ['ExecuteGameEvent-0', 'ExecuteGameEvent-1'],
        'source': 'src/profiles/extended/home/map.c'},
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _record in SCHEMA2_CASES["GameEvent_Duel"]:
    _record["completion"] = {"mode": "entry", "pc": 0x4CD5, "bank": 1, "routine": "ChooseInitialArenaAndBenchPokemon"}
for _record in SCHEMA2_CASES["GameEvent_ChallengeMachine"]:
    _record["completion"] = {"mode": "entry", "pc": 0x6D0B, "bank": 4, "routine": "ChallengeMachine_Start"}
for _record in SCHEMA2_CASES["GameEvent_Credits"]:
    _record["completion"] = {"mode": "entry", "pc": 0x4031, "bank": 4, "routine": "FlashWhiteScreen"}
for _record in SCHEMA2_CASES["ExecuteGameEvent"]:
    _record["completion"] = {"mode": "entry", "pc": 0x4000, "bank": 3, "routine": "LoadMap"}
