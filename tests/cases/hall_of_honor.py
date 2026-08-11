"""Oracle-diff cases for poketcg/src/scripts/hall_of_honor.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "HallOfHonorLoadMap": {
        "compare": ("b", "c", "hl"),
        "preserve": ("b", "c", "hl"),
    },
}

CASES = {
    "HallOfHonorLoadMap": [
        # The routine has no inputs; all registers start at zero.
        {"read": {0xDD82: 1, 0xDD83: 1}},
        # Register poison proves the fixed SFX selection is independent of A
        # and that the callee's preserved register ABI is retained.
        dict(POISON, read={0xDD82: 1, 0xDD83: 1}),
        # A higher-priority active effect is the boundary where PlaySFX skips
        # replacing the current effect, while the fixed ID remains an input.
        {"wram": {0xDD82: b"\xFF", 0xDD83: b"\xFF"},
         "read": {0xDD82: 1, 0xDD83: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "HallOfHonorLoadMap": {
        "source_symbol": "HallOfHonorLoadMap",
        "before": "PlaySFX(SFX_LEGENDARY_CARDS)",
        "after": "PlaySFX(0x11u)",
        "case_ids": [
            "HallOfHonorLoadMap-0",
            "HallOfHonorLoadMap-1",
            "HallOfHonorLoadMap-2",
        ],
    },
}
