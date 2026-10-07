"""Oracle-diff cases for poketcg/src/scripts/hall_of_honor.asm."""
from tests.cases._symbols import sym

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
        {"read": {sym("wCurSfxID"): 1, sym("wSfxPriority"): 1}},
        # Register poison proves the fixed SFX selection is independent of A
        # and that the callee's preserved register ABI is retained.
        dict(POISON, read={sym("wCurSfxID"): 1, sym("wSfxPriority"): 1}),
        # A higher-priority active effect is the boundary where PlaySFX skips
        # replacing the current effect, while the fixed ID remains an input.
        {"wram": {sym("wCurSfxID"): b"\xFF", sym("wSfxPriority"): b"\xFF"},
         "read": {sym("wCurSfxID"): 1, sym("wSfxPriority"): 1}},
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
