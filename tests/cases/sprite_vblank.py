"""Oracle-diff cases for poketcg/src/engine/gfx/sprite_vblank.asm."""

SRC = 0xC100
DST = 0xC500
BOUNDARY_SRC = 0xCFFE
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
        # All-zero registers exercise the 16-bit pointer arithmetic and bus writes.
        {},
        # Poisoned registers prove that only HL and DE are consumed, with A returning
        # the second copied byte and the other untouched registers preserved.
        dict(POISON, hl=SRC, d=DST >> 8, e=DST & 0xFF,
             wram={SRC: b"\x12\x34"}, read={DST: 2}),
        # Crossing a page boundary pins both post-increment destination bytes.
        {"hl": BOUNDARY_SRC, "d": BOUNDARY_DST >> 8, "e": BOUNDARY_DST & 0xFF,
         "wram": {BOUNDARY_SRC: b"\xA5\x5A"}, "read": {BOUNDARY_DST: 2}},
        # Input events are ignored by this routine but remain part of the ABI probe.
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
            "BackupVBlankFunctionTrampoline-0",
            "BackupVBlankFunctionTrampoline-1",
            "BackupVBlankFunctionTrampoline-2",
            "BackupVBlankFunctionTrampoline-3",
        ],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
