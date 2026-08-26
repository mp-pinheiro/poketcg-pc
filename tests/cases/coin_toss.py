"""Oracle-diff cases for poketcg/src/home/coin_toss.asm.

TossCoin and TossCoinATimes are not registered: both bank1call _TossCoin
(engine/duel/core.asm:7847), the full coin-toss animation/RNG sequence, which is
not ported and whose video/RNG side effects the differ cannot reproduce.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "CompareDEtoBC": {
        "compare": ("f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "CompareDEtoBC": [
        {"d": 0x12, "e": 0x34, "b": 0x12, "c": 0x34},
        {"d": 0x10, "e": 0x00, "b": 0x20, "c": 0x00},
        {"d": 0x20, "e": 0x00, "b": 0x10, "c": 0x00},
        {"d": 0x12, "e": 0xAA, "b": 0x12, "c": 0x00},
        {"d": 0x12, "e": 0x00, "b": 0x23, "c": 0x00},
        dict(POISON, d=0x05, e=0x09, b=0x21, c=0x80),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {
    "CompareDEtoBC": {
        "source_symbol": "CompareDEtoBC",
        "before": "if (d != b)",
        "after": "if (d == b)",
        "case_ids": ["CompareDEtoBC-0", "CompareDEtoBC-1", "CompareDEtoBC-5"],
    },
}
