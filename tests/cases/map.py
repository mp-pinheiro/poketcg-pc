POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
W_PERMISSION_MAP = 0xD133
PERMISSIONS = bytes((i * 3 + 7) & 0xFF for i in range(256))
READ_MAP = {W_PERMISSION_MAP: 256}
NPC_BASE = 0xD34A
NPC_DATA = bytes((i * 5 + 1) & 0xFF for i in range(96))
NPC_READ = {NPC_BASE: 96}

CONTRACT = {
    "GetPermissionByteOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "GetPermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "SetPermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "UpdatePermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "GetLoadedNPCID": ("a", "b", "c", "d", "e", "hl"),
    "GetItemInLoadedNPCIndex": ("a", "b", "c", "d", "e", "hl"),
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
}
