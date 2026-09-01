"""Oracle-diff cases for poketcg/src/engine/gfx/sprite_vblank.asm."""

SRC = 0xC100
DST = 0xC500
BOUNDARY_SRC = 0xCEFE
BOUNDARY_DST = 0xDFFE
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "BackupVBlankFunctionTrampoline": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("f", "b", "c"),
    },
}

CASES = {
    "BackupVBlankFunctionTrampoline": [
        {},
        dict(POISON, hl=SRC, d=DST >> 8, e=DST & 0xFF,
             wram={SRC: b"\x12\x34"}, read={DST: 2}),
        {"hl": BOUNDARY_SRC, "d": BOUNDARY_DST >> 8,
         "e": BOUNDARY_DST & 0xFF, "wram": {BOUNDARY_SRC: b"\xA5\x5A"},
         "read": {BOUNDARY_DST: 2}},
        dict(POISON, hl=SRC, d=DST >> 8, e=DST & 0xFF, keys=0xA5,
             wram={SRC: b"\xDE\xAD"}, read={DST: 2}),
    ],
}

MUTATIONS = {
    "BackupVBlankFunctionTrampoline": {
        "source_symbol": "BackupVBlankFunctionTrampoline",
        "before": "gb_write8(*de, first);",
        "after": "gb_write8(*de, (uint8_t)(first ^ 0xFFu));",
        "case_ids": [
            "BackupVBlankFunctionTrampoline-1",
            "BackupVBlankFunctionTrampoline-0",
            "BackupVBlankFunctionTrampoline-2",
            "BackupVBlankFunctionTrampoline-3",
        ],
    },
}

# >>> factory-cases-statics
VBLANK_TRAMPOLINE_FN = 0xCAD1
VBLANK_TRAMPOLINE_BACKUP = 0xCE8D
VBLANK_OAM_COPY_TOGGLE = 0xCAC0
# <<< factory-cases-statics

# >>> factory SetSpriteAnimationsAsVBlankFunction
CONTRACT["SetSpriteAnimationsAsVBlankFunction"] = {"compare": (), "preserve": ()}
CASES["SetSpriteAnimationsAsVBlankFunction"] = [
    {"wram": {VBLANK_TRAMPOLINE_FN: b"\x00\x00"},
     "read": {VBLANK_TRAMPOLINE_FN: 2, VBLANK_TRAMPOLINE_BACKUP: 2}},
    dict(POISON, wram={VBLANK_TRAMPOLINE_FN: b"\x11\x22"},
         read={VBLANK_TRAMPOLINE_FN: 2, VBLANK_TRAMPOLINE_BACKUP: 2}),
    {"wram": {VBLANK_TRAMPOLINE_FN: b"\xB4\x3C"},
     "read": {VBLANK_TRAMPOLINE_FN: 2, VBLANK_TRAMPOLINE_BACKUP: 2}},
]
# <<< factory SetSpriteAnimationsAsVBlankFunction

# >>> factory RestoreVBlankFunction
CONTRACT["RestoreVBlankFunction"] = {"compare": (), "preserve": ()}
CASES["RestoreVBlankFunction"] = [
    {"wram": {VBLANK_TRAMPOLINE_BACKUP: b"\x00\x00"},
     "read": {VBLANK_TRAMPOLINE_FN: 2, VBLANK_OAM_COPY_TOGGLE: 1}},
    dict(POISON, wram={VBLANK_TRAMPOLINE_BACKUP: b"\x33\x44"},
         read={VBLANK_TRAMPOLINE_FN: 2, VBLANK_OAM_COPY_TOGGLE: 1}),
    {"wram": {VBLANK_TRAMPOLINE_BACKUP: b"\xFF\x00"},
     "read": {VBLANK_TRAMPOLINE_FN: 2, VBLANK_OAM_COPY_TOGGLE: 1}},
]
# <<< factory RestoreVBlankFunction

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation SetSpriteAnimationsAsVBlankFunction
MUTATIONS["SetSpriteAnimationsAsVBlankFunction"] = {
    "source_symbol": "SetSpriteAnimationsAsVBlankFunction",
    "before": "gb_write8(hl, (uint8_t)(HANDLEALLSPRITEANIMATIONS_ADDR & 0xFFu));",
    "after": "gb_write8(hl, (uint8_t)(HANDLEALLSPRITEANIMATIONS_ADDR >> 8));",
    "case_ids": [
        "SetSpriteAnimationsAsVBlankFunction-0",
        "SetSpriteAnimationsAsVBlankFunction-1",
        "SetSpriteAnimationsAsVBlankFunction-2",
    ],
}
# <<< factory-mutation SetSpriteAnimationsAsVBlankFunction
# >>> factory-mutation RestoreVBlankFunction
MUTATIONS["RestoreVBlankFunction"] = {
    "source_symbol": "RestoreVBlankFunction",
    "before": "BackupVBlankFunctionTrampoline(&hl, &de);\n\tClearSpriteAnimations();",
    "after": "BackupVBlankFunctionTrampoline(&de, &hl);\n\tClearSpriteAnimations();",
    "case_ids": [
        "RestoreVBlankFunction-1",
        "RestoreVBlankFunction-2",
    ],
}
# <<< factory-mutation RestoreVBlankFunction
