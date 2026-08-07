POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
W_PERMISSION_MAP = 0xD133
PERMISSIONS = bytes((i * 3 + 7) & 0xFF for i in range(256))
READ_MAP = {W_PERMISSION_MAP: 256}

CONTRACT = {
    "GetPermissionByteOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "GetPermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "SetPermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
    "UpdatePermissionOfMapPosition": ("a", "b", "c", "d", "e", "hl"),
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
}
