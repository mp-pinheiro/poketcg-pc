"""Oracle-diff cases for sgb.asm:258-270."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "Wait": {"compare": ("a", "d", "e", "hl"),
              "preserve": ("hl",)},
}

CASES = {
    "Wait": [
        # BC=0 is the maximum 65536-iteration delay; the standalone oracle
        # cannot execute its full timing loop, but its register result is fixed.
        {"oracle": False,
         "why": "BC=0 expands to 65536 * 1750 delay iterations, exceeding the oracle time budget",
         "expect_regs": {"a": 0, "d": 0, "e": 0, "hl": 0}},
        # Poisoned registers with a short delay prove HL preservation and the
        # deterministic A/DE results without relying on zero-valued inputs.
        dict(POISON, b=0, c=1,
             expect_regs={"a": 0, "d": 0, "e": 0, "hl": 0x1234}),
        {"b": 0, "c": 1, "d": 0x12, "e": 0x34, "hl": 0xC100},
        {"b": 1, "c": 0, "d": 0x56, "e": 0x78, "hl": 0xC101},
        {"b": 1, "c": 1, "d": 0x9A, "e": 0xBC, "hl": 0xC102},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "Wait": {
        "source_symbol": "Wait",
        "before": "\t*de = 0;",
        "after": "\t*de = 1;",
        "case_ids": ["Wait-0", "Wait-1", "Wait-2", "Wait-3", "Wait-4"],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
