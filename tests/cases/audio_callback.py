"""Oracle-diff cases for poketcg/src/home/audio_callback.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "Bankswitch3dTo3f": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Bankswitch3dTo3f": [
        {"read": {0x4000: 1}},
        dict(POISON, read={0x4000: 1}),
    ],
}

MUTATIONS = {
    "Bankswitch3dTo3f": {
        "source_symbol": "Bankswitch3dTo3f",
        "before": "BankswitchROM(0x3Du);",
        "after": "BankswitchROM(0x3Eu);",
        "case_ids": ["Bankswitch3dTo3f-0", "Bankswitch3dTo3f-1"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
