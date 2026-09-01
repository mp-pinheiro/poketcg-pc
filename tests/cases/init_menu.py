POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

TILE_MAP_FILL = 0xCAB6
LCDC = 0xCABB
VBLANK_OAM_TOGGLE = 0xCAC0
H_BANK_SRAM = 0xFF81
H_SCX = 0xFF92
H_SCY = 0xFF93
R_SCX = 0xFF43
R_SCY = 0xFF42
R_LCDC = 0xFF40
BGP = 0xCABC
OBP0 = 0xCABD
OBP1 = 0xCABE
BG_PALS = 0xCAF0
OBJ_PALS = 0xCB30
SRAM_PALS = 0xA800

SRAM_PALETTE = b"\x11\x22\x33" + bytes(range(128))

PALETTE_SEED = {
    BGP: b"\x11", OBP0: b"\x22", OBP1: b"\x33",
    BG_PALS: bytes(range(128)), OBJ_PALS: bytes(range(64, 128)),
}

CONTRACT = {
    "InitMenuScreen": {
        "compare": (),
        "preserve": (),
    },
    "FlashWhiteScreen": {
        "compare": (),
        "preserve": (),
    },
}

CASES = {
    "InitMenuScreen": [
        {"wram": {TILE_MAP_FILL: b"\xff", LCDC: b"\x00", H_SCX: b"\x12", H_SCY: b"\x34",
                  R_SCX: b"\x55", R_SCY: b"\x66"},
         "read": {TILE_MAP_FILL: 1, LCDC: 1, H_SCX: 1, H_SCY: 1, R_SCX: 1, R_SCY: 1,
                  VBLANK_OAM_TOGGLE: 1}},
        dict(POISON, wram={TILE_MAP_FILL: b"\x7f", LCDC: b"\x00", H_SCX: b"\xaa", H_SCY: b"\xbb"},
             read={TILE_MAP_FILL: 1, LCDC: 1, H_SCX: 1, H_SCY: 1, R_SCX: 1, R_SCY: 1,
                   VBLANK_OAM_TOGGLE: 1}),
        dict(POISON, wram={TILE_MAP_FILL: b"\xff", LCDC: b"\x80", H_SCX: b"\xaa", H_SCY: b"\xbb"},
             read={TILE_MAP_FILL: 1, LCDC: 1, H_SCX: 1, H_SCY: 1, R_LCDC: 1,
                   VBLANK_OAM_TOGGLE: 1}),
    ],
    "FlashWhiteScreen": [
        {"wram": {R_LCDC: b"\x00", LCDC: b"\x00", H_BANK_SRAM: b"\x00", **PALETTE_SEED},
         "sram": {1: {SRAM_PALS: b"\x00" * 131}},
         "read": {H_BANK_SRAM: 1, BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 128, OBJ_PALS: 128},
         "sread": {1: {SRAM_PALS: 131}}},
        dict(POISON, wram={R_LCDC: b"\x00", LCDC: b"\x00", H_BANK_SRAM: b"\x03", **PALETTE_SEED},
             sram={1: {SRAM_PALS: b"\x55" * 131}, 3: {SRAM_PALS: b"\xaa" * 131}},
             read={H_BANK_SRAM: 1, BGP: 1, OBP0: 1, OBP1: 1, BG_PALS: 128, OBJ_PALS: 128},
             sread={1: {SRAM_PALS: 131}, 3: {SRAM_PALS: 131}}),
        dict(POISON, wram={R_LCDC: b"\x80", LCDC: b"\x80", H_BANK_SRAM: b"\x02", **PALETTE_SEED},
             sram={1: {SRAM_PALS: b"\x11" * 131}, 2: {SRAM_PALS: b"\x22" * 131}},
             read={H_BANK_SRAM: 1, BGP: 1, OBP0: 1, OBP1: 1,
                   BG_PALS: 128, OBJ_PALS: 128},
             sread={1: {SRAM_PALS: 131}, 2: {SRAM_PALS: 131}}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "InitMenuScreen": {
        "source_symbol": "InitMenuScreen",
        "before": "if (!(wLCDC & LCDC_ON)) {",
        "after": "if ((wLCDC & LCDC_ON)) {",
        "case_ids": ["InitMenuScreen-0", "InitMenuScreen-1", "InitMenuScreen-2"],
    },
}
