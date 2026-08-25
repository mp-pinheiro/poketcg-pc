"""Oracle-diff cases for engine/overworld/debug_player_coordinates.asm."""

wLCDC = 0xCABB

POISON = {
    "a": 0xAA,
    "f": 0xF0,
    "b": 0xBB,
    "c": 0xCC,
    "d": 0xDD,
    "e": 0xEE,
    "hl": 0x1234,
}

CONTRACT = {
    "JumpSetWindowOff": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "JumpSetWindowOff": [
        {"wram": {wLCDC: b"\x00"}, "read": {wLCDC: 1}},
        dict(POISON, wram={wLCDC: b"\xff"}, read={wLCDC: 1}),
        {"wram": {wLCDC: b"\x3f"}, "read": {wLCDC: 1}},
    ],
}

# >>> factory-cases-statics
hKeysHeld = 65424
hKeysPressed = 65425
hWX = 65428
hWY = 65429
wCurMap = 54063
wOverworldMode = 53439
wPlayerXCoord = 54064
wPlayerYCoord = 54065
# <<< factory-cases-statics

# >>> factory Func_1c003
CONTRACT["Func_1c003"] = {"compare": (), "preserve": ()}
CASES["Func_1c003"] = [
    {"wram": {wCurMap: b"\x00"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {wCurMap: b"\x01", wOverworldMode: b"\x00", wPlayerXCoord: b"\x01", wPlayerYCoord: b"\x02", hKeysHeld: b"\x02", hKeysPressed: b"\x00"},
     "read": {hWX: 1, hWY: 1}},
    {"wram": {wCurMap: b"\x01", wOverworldMode: b"\x00", wPlayerXCoord: b"\x01", wPlayerYCoord: b"\x02", hKeysHeld: b"\x02", hKeysPressed: b"\x00"},
     "read": {hWX: 1, hWY: 1}},
]
# <<< factory Func_1c003

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "JumpSetWindowOff": {
        "source_symbol": "JumpSetWindowOff",
        "before": "gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_WIN_ON));",
        "after": "gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | LCDC_WIN_ON));",
        "case_ids": ["JumpSetWindowOff-0", "JumpSetWindowOff-1", "JumpSetWindowOff-2"],
    },
}
# >>> factory-mutation Func_1c003
MUTATIONS["Func_1c003"] = {
    "source_symbol": "Func_1c003",
    "before": "\thWX = (uint8_t)(112u + WX_OFS);\n\thWY = 136u;",
    "after": "\thWX = (uint8_t)(113u + WX_OFS);\n\thWY = 136u;",
    "case_ids": ["Func_1c003-1", "Func_1c003-2"],
}
# <<< factory-mutation Func_1c003
