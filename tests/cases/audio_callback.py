"""Oracle-diff cases for poketcg/src/home/audio_callback.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "Bankswitch3dTo3f": {
        "compare": (),
        "preserve": (),
    },
}

HBANK_ROM = 0xFF80
CALLBACK = 0x3FEE

CASES = {
    "Bankswitch3dTo3f": [
        {
            "oracle": False,
            "why": "The zero-register call has no valid caller callback; verify its bank-3d tail directly.",
            "expect": {HBANK_ROM: b"\x3D"},
        },
        {
            **POISON,
            "oracle": False,
            "why": "The standalone poisoned call has no valid caller callback; verify its bank-3d tail directly.",
            "expect": {HBANK_ROM: b"\x3D"},
        },
        {"hl": CALLBACK, "read": {HBANK_ROM: 1}},
        dict(POISON, hl=CALLBACK, read={HBANK_ROM: 1}),
    ],
}

MUTATIONS = {
    "Bankswitch3dTo3f": {
        "source_symbol": "Bankswitch3dTo3f",
        "before": "BankswitchROM(0x3Du);",
        "after": "BankswitchROM(0x3Eu);",
        "case_ids": ["Bankswitch3dTo3f-2", "Bankswitch3dTo3f-3"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
