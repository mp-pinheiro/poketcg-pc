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
