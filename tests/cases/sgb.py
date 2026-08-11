"""Oracle-diff cases for poketcg/src/home/sgb.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "Wait": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("hl",),
    },
}

_ZERO_RESULT = {"a": 0, "f": 0x80, "b": 0, "c": 0, "d": 0, "e": 0}

CASES = {
    "Wait": [
        {"oracle": False,
         "why": "bc=0 expands to 65536 delay iterations and exceeds the oracle budget",
         "expect_regs": _ZERO_RESULT},
        dict(POISON, b=0, c=1, expect_regs=_ZERO_RESULT),
        {"b": 0, "c": 2},
        {"oracle": False, "b": 1, "c": 0,
         "why": "256 outer delay passes exceed the live PyBoy frame budget",
         "expect_regs": _ZERO_RESULT},
        {"oracle": False, "b": 1, "c": 1,
         "why": "257 outer delay passes exceed the live PyBoy frame budget",
         "expect_regs": _ZERO_RESULT},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Wait": {
        "source_symbol": "Wait",
        "before": "\treturn (SGBWaitResult){0, 0x80u, 0, 0, 0, 0};",
        "after": "\treturn (SGBWaitResult){1, 0x80u, 0, 0, 0, 0};",
        "case_ids": ["Wait-0", "Wait-1", "Wait-2"],
    },
}
