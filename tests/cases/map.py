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
wSongOverride = 0xD112
wCurSongID = 0xDD80
NUM_SONGS = 0x1F
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
    "GetPermissionByteOfMapPosition": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetPermissionOfMapPosition": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SetPermissionOfMapPosition": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")},
    "UpdatePermissionOfMapPosition": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetLoadedNPCID": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GetItemInLoadedNPCIndex": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "GameEvent_Overworld": {"compare": ("f", "a", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")},
    # CopyGfxData decrements B to zero, preserves C, and final pop af restores A/F.
    "CopyGfxDataFromTempBank": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "c")},
    "FindLoadedNPC": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetNextNPCMovementByte": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "PlayDefaultSong": {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                        "preserve": ("b", "c", "d", "e", "hl")},
    "GetDefaultSong": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
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
        {"b": 1, "c": 1, "hl": CG_SRC, "d": CG_DST >> 8, "e": CG_DST & 0xFF,
         "wram": {hBankROM: b"\x01", wTempPointerBank: b"\x01", CG_SRC: CG_PAT[:1]},
         "read": {hBankROM: 1}},
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
        {
            "evidence": "dependency-blocked",
            "reason": (
                "b=c=0 requests a 64 KiB nested copy; it overwrites the wrapper's "
                "saved bank and return frames before wrapper restoration can run"
            ),
        },
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
    "PlayDefaultSong": [
        {"read": {wCurSongID: 1, wSongOverride: 1}},
        {"wram": {wCurSongID: b"\x80", wDefaultSong: b"\x05",
                  wSongOverride: b"\xFF"}, "read": {wSongOverride: 1}},
        dict(POISON, wram={wCurSongID: b"\x80", wDefaultSong: bytes((NUM_SONGS - 1,)),
                            wSongOverride: b"\x01"},
             read={wSongOverride: 1}),
        {"wram": {wCurSongID: b"\x01", wDefaultSong: b"\x05",
                  wSongOverride: b"\x05"}, "read": {wSongOverride: 1}},
        {"wram": {wCurSongID: b"\x80", wDefaultSong: bytes((NUM_SONGS,)),
                  wSongOverride: b"\x01"}, "read": {wSongOverride: 1}},
    ],
}
# >>> factory HandleMapWarp

wWarpCurMap = 0xD32F
wWarpPlayerXCoord = 0xD330
wWarpPlayerYCoord = 0xD331
wWarpPlayerDirection = 0xD334
wWarpTempMap = 0xD0BB
wWarpTempPlayerXCoord = 0xD0BC
wWarpTempPlayerYCoord = 0xD0BD
wWarpTempPlayerDirection = 0xD0BE
WARP_READ = {wWarpTempMap: 1, wWarpTempPlayerXCoord: 1, wWarpTempPlayerYCoord: 1,
             wWarpTempPlayerDirection: 1}


def _warp_memory(m, x, y, d, t=b"\x11\x22\x33\x44"):
    return {wWarpCurMap: bytes((m,)), wWarpPlayerXCoord: bytes((x,)),
            wWarpPlayerYCoord: bytes((y,)), wWarpPlayerDirection: bytes((d,)),
            wWarpTempMap: t}


CONTRACT["HandleMapWarp"] = {"compare": (), "preserve": ()}
CASES["HandleMapWarp"] = [
    {"wram": _warp_memory(1, 0, 0, 0), "read": WARP_READ},
    dict(POISON, wram=_warp_memory(1, 0x1A, 0x0A, 2, b"\x00\x00\x00\x00"), read=WARP_READ),
    {"wram": _warp_memory(1, 0x0E, 0x1C, 1), "read": WARP_READ},
    {"wram": _warp_memory(2, 0, 0x0A, 4), "read": WARP_READ},
]
# <<< factory HandleMapWarp

# >>> factory-cases-statics
sReceivedLegendaryCards = 0xA00A

wOverworldNPCFlags = 0xD0C1
hBankROM = 0xFF80
wSCXBuffer = 0xD235
wSCYBuffer = 0xD236
wSCX = 0xD0B6
wSCY = 0xD0B7
# <<< factory-cases-statics

# >>> factory GetReceivedLegendaryCards
CONTRACT["GetReceivedLegendaryCards"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "sram_out": True}
CASES["GetReceivedLegendaryCards"] = [
    {"sram": {0: {sReceivedLegendaryCards: b"\xAA"}}, "expect_sram": {0: {sReceivedLegendaryCards: b"\x00"}}},
    dict(POISON, sram={0: {sReceivedLegendaryCards: b"\x55"}}, expect_sram={0: {sReceivedLegendaryCards: b"\x00"}}),
]
# <<< factory GetReceivedLegendaryCards

# >>> factory OverworldDoFrameFunction
CONTRACT["OverworldDoFrameFunction"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["OverworldDoFrameFunction"] = [
    {"hram": {hBankROM: b"\x01"}, "wram": {wOverworldNPCFlags: b"\x80"}},
    dict(POISON, hram={hBankROM: b"\x05"}, wram={wOverworldNPCFlags: b"\x00",
                       wSCXBuffer: b"\x11", wSCYBuffer: b"\x22"},
         read={wSCX: 1, wSCY: 1, hBankROM: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory OverworldDoFrameFunction

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GetPermissionOfMapPosition": {
        "source_symbol": "GetPermissionOfMapPosition",
        "before": "return gb_read8(permission_address(b, c));",
        "after": "return (uint8_t)(gb_read8(permission_address(b, c)) ^ 1u);",
        "case_ids": ["GetPermissionOfMapPosition-0", "GetPermissionOfMapPosition-1"],
    },
    "PlayDefaultSong": {
        "source_symbol": "PlayDefaultSong",
        "before": "wSongOverride = song;",
        "after": "wSongOverride = (uint8_t)(song ^ 1u);",
        "case_ids": ["PlayDefaultSong-1", "PlayDefaultSong-2"],
    },
}
# >>> factory-mutation HandleMapWarp

MUTATIONS["HandleMapWarp"] = {
    "source_symbol": "HandleMapWarp",
    "before": "(void)_HandleMapWarp();",
    "after": "",
    "case_ids": ["HandleMapWarp-1", "HandleMapWarp-2", "HandleMapWarp-3"],
}
# <<< factory-mutation HandleMapWarp
# >>> factory-mutation GetReceivedLegendaryCards
MUTATIONS["GetReceivedLegendaryCards"] = {"source_symbol": "GetReceivedLegendaryCards", "before": "\tsReceivedLegendaryCards = a;", "after": "\tsReceivedLegendaryCards = (uint8_t)(a ^ 1u);", "case_ids": ["GetReceivedLegendaryCards-0", "GetReceivedLegendaryCards-1"]}
# <<< factory-mutation GetReceivedLegendaryCards
# >>> factory-mutation OverworldDoFrameFunction
MUTATIONS["OverworldDoFrameFunction"] = {"source_symbol": "OverworldDoFrameFunction", "before": "BankswitchROM(saved_bank);", "after": "BankswitchROM(0u);", "case_ids": ["OverworldDoFrameFunction-1"]}
# <<< factory-mutation OverworldDoFrameFunction
