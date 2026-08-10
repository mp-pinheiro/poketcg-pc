POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
W_PERMISSION_MAP = 0xD133
PERMISSIONS = bytes((i * 3 + 7) & 0xFF for i in range(256))
READ_MAP = {W_PERMISSION_MAP: 256}
NPC_BASE = 0xD34A
NPC_DATA = bytes((i * 5 + 1) & 0xFF for i in range(96))
NPC_READ = {NPC_BASE: 96}

hBankROM = 0xFF80
wLoadedNPCTempIndex = 0xD3AA
wTempNPC = 0xD3AB
wTempPointerBank = 0xD4C6
wRonaldIsInMap = 0xD3B8
wOverworldMapSelection = 0xD32E
wDefaultSong = 0xD111
OWMAP_ISHIHARAS_HOUSE = 0x02
OWMAP_CHALLENGE_HALL = 0x0B
OWMAP_POKEMON_DOME = 0x0C
MUSIC_RONALD = 0x0F


def npc_table(ids):
    """8 entries x 12 bytes; only byte 0 (LOADED_NPC_ID) is read by FindLoadedNPC."""
    entries = bytearray()
    for i, npc_id in enumerate(ids):
        entries += bytes([npc_id & 0xFF]) + bytes((i * 7 + k) & 0xFF for k in range(1, 12))
    return bytes(entries)


CG_SRC = 0xC100
CG_DST = 0xC500
CG_PAT = bytes((i * 11 + 5) & 0xFF for i in range(300))

CONTRACT = {
    "GetPermissionByteOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "GetPermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "SetPermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "UpdatePermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "GetLoadedNPCID": ("a", "b", "c", "d", "e", "hl"),
    "GetItemInLoadedNPCIndex": ("a", "b", "c", "d", "e", "hl"),
    "GameEvent_Overworld": ("f", "a", "b", "c", "d", "e", "hl"),
    "CopyGfxDataFromTempBank": ("a", "f", "c", "d", "e", "hl"),
    "FindLoadedNPC": ("a", "f", "b", "c", "d", "e", "hl"),
    "GetNextNPCMovementByte": ("a", "f", "b", "c", "d", "e", "hl"),
    "GetDefaultSong": ("a", "b", "c", "d", "e", "hl"),
}


CASES = {
    "GetPermissionByteOfMapPosition": [
        {"b": 4, "c": 8, "wram": {W_PERMISSION_MAP: PERMISSIONS}, "read": READ_MAP},
        dict(POISON, b=31, c=47, wram={W_PERMISSION_MAP: PERMISSIONS}, read=READ_MAP),
    ],
    "GetPermissionOfMapPosition": [
        {"b": 4, "c": 8, "wram": {W_PERMISSION_MAP: PERMISSIONS}, "read": READ_MAP},
        dict(POISON, b=31, c=47, wram={W_PERMISSION_MAP: PERMISSIONS}, read=READ_MAP),
    ],
    "SetPermissionOfMapPosition": [
        {"a": 0x5A, "b": 4, "c": 8, "wram": {W_PERMISSION_MAP: PERMISSIONS}, "read": READ_MAP},
        dict(POISON, a=0xC3, b=31, c=47, wram={W_PERMISSION_MAP: PERMISSIONS}, read=READ_MAP),
    ],
    "UpdatePermissionOfMapPosition": [
        {"a": 0x0F, "b": 4, "c": 8, "wram": {W_PERMISSION_MAP: PERMISSIONS}, "read": READ_MAP},
        dict(POISON, a=0xF0, b=31, c=47, wram={W_PERMISSION_MAP: PERMISSIONS}, read=READ_MAP),
    ],
    "GetLoadedNPCID": [
        {"a": 0, "wram": {NPC_BASE: NPC_DATA}, "read": NPC_READ},
        dict(POISON, a=7, wram={NPC_BASE: NPC_DATA}, read=NPC_READ),
        {"a": 255, "wram": {NPC_BASE: NPC_DATA}, "read": NPC_READ},
    ],
    "GetItemInLoadedNPCIndex": [
        {"a": 0, "hl": 0, "wram": {NPC_BASE: NPC_DATA}, "read": NPC_READ},
        dict(POISON, a=3, hl=0x000B, wram={NPC_BASE: NPC_DATA}, read=NPC_READ),
        {"a": 8, "hl": 0x0000, "wram": {NPC_BASE: NPC_DATA}, "read": NPC_READ},
    ],
    "GameEvent_Overworld": [
        {},
        dict(POISON),
        {"f": 0x60},
        {"f": 0x80},
    ],
    "CopyGfxDataFromTempBank": [
        {},
        dict(POISON, b=4, c=3, hl=CG_SRC, d=CG_DST >> 8, e=CG_DST & 0xFF,
             wram={hBankROM: b"\x07", wTempPointerBank: b"\x02", CG_SRC: CG_PAT[:16]},
             read={CG_DST: 16, hBankROM: 1}),
        {"b": 1, "c": 0, "hl": CG_SRC, "d": CG_DST >> 8, "e": CG_DST & 0xFF,
         "wram": {wTempPointerBank: b"\x02", CG_SRC: CG_PAT[:256]}, "read": {CG_DST: 260}},
        {"b": 0, "c": 1, "hl": CG_SRC, "d": CG_DST >> 8, "e": CG_DST & 0xFF,
         "wram": {wTempPointerBank: b"\x02", CG_SRC: CG_PAT[:256]}, "read": {CG_DST: 260}},
        # Real bank switch: reads bank 3 ROM, not whatever bank happened to be live.
        {"b": 1, "c": 8, "hl": 0x4000, "d": CG_DST >> 8, "e": CG_DST & 0xFF,
         "wram": {wTempPointerBank: b"\x03"}, "read": {CG_DST: 8, hBankROM: 1}},
    ],
    "FindLoadedNPC": [
        {"wram": {NPC_BASE: npc_table([0, 1, 2, 3, 4, 5, 6, 7]),
                  wLoadedNPCTempIndex: b"\xEE", wTempNPC: b"\x00"},
         "read": {wLoadedNPCTempIndex: 1}},
        dict(POISON,
             wram={NPC_BASE: npc_table([9, 1, 2, 3, 4, 5, 6, 7]),
                   wLoadedNPCTempIndex: b"\xEE", wTempNPC: b"\x05"},
             read={wLoadedNPCTempIndex: 1}),
        {"wram": {NPC_BASE: npc_table([1, 2, 3, 4, 5, 6, 7, 8]),
                  wLoadedNPCTempIndex: b"\xEE", wTempNPC: b"\xFF"},
         "read": {wLoadedNPCTempIndex: 1}},
        {"wram": {NPC_BASE: npc_table([1, 2, 3, 4, 5, 6, 7, 77]),
                  wLoadedNPCTempIndex: b"\xEE", wTempNPC: b"\x4D"},
         "read": {wLoadedNPCTempIndex: 1}},
    ],
    "GetNextNPCMovementByte": [
        {"b": 0, "c": 0, "read": {hBankROM: 1}},
        dict(POISON, b=0xC1, c=0x00,
             wram={hBankROM: b"\x09", 0xC100: b"\x42"}, read={hBankROM: 1}),
        # Real bank switch: bc=$4000 is read under bank 3's ROM image.
        {"b": 0x40, "c": 0x00, "wram": {hBankROM: b"\x05"}, "read": {hBankROM: 1}},
    ],
    "GetDefaultSong": [
        {},
        {"wram": {wRonaldIsInMap: b"\x01", wDefaultSong: b"\x05",
                  wOverworldMapSelection: bytes((OWMAP_ISHIHARAS_HOUSE,))}},
        {"wram": {wRonaldIsInMap: b"\x01", wDefaultSong: b"\x05",
                  wOverworldMapSelection: bytes((OWMAP_CHALLENGE_HALL,))}},
        {"wram": {wRonaldIsInMap: b"\x01", wDefaultSong: b"\x05",
                  wOverworldMapSelection: bytes((OWMAP_POKEMON_DOME,))}},
        dict(POISON, wram={wRonaldIsInMap: b"\x01", wDefaultSong: b"\x22",
                            wOverworldMapSelection: b"\x01"}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
