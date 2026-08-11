"""Oracle-diff cases for engine/duel/ai/attacks.asm."""

wAIScore = 0xCDBE
wPlayAreaAIScore = 0xCDBF
wTempPlayAreaAIScore = 0xCDDD
wTempAIScore = 0xCDE3

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "RetrievePlayAreaAIScoreFromBackup2": {
        "compare": ("a", "f"),
        "preserve": ("a", "f"),
    },
}

CASES = {
    "RetrievePlayAreaAIScoreFromBackup2": [
        # All-zero registers with distinct source bytes prove both copies.
        {"wram": {
            wAIScore: b"\x00\x00\x00\x00\x00\x00\x00",
            wTempPlayAreaAIScore: b"\x10\x20\x30\x40\x50\x60\x70",
        }},
        # Poisoned registers prove AF is restored by push/pop and untouched by the adapter.
        dict(POISON, wram={
            wAIScore: b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA",
            wTempPlayAreaAIScore: b"\x01\x23\x45\x67\x89\xAB\xCD",
        }),
        # Guards immediately before and after each seven-byte source/destination region.
        {"wram": {
            wAIScore - 1: b"\x11\x00\x00\x00\x00\x00\x00\x00\x22",
            wTempPlayAreaAIScore - 1: b"\x33\xDE\xAD\xBE\xEF\x01\x02\x03\x44",
        }},
        # A second non-zero pattern catches swapped order and off-by-one copies.
        dict(POISON, wram={
            wAIScore: b"\xFE\xFD\xFC\xFB\xFA\xF9\xF8",
            wTempPlayAreaAIScore: b"\x80\x00\x7F\x01\x7E\x02\x7D",
        }),
    ],
}

MUTATIONS = {
    "RetrievePlayAreaAIScoreFromBackup2": {
        "source_symbol": "RetrievePlayAreaAIScoreFromBackup2",
        "before": "gb_write8(wAIScore_ADDR, gb_read8(wTempAIScore_ADDR));",
        "after": "gb_write8(wAIScore_ADDR, 0x00);",
        "case_ids": [
            "RetrievePlayAreaAIScoreFromBackup2-0",
            "RetrievePlayAreaAIScoreFromBackup2-1",
            "RetrievePlayAreaAIScoreFromBackup2-2",
            "RetrievePlayAreaAIScoreFromBackup2-3",
        ],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
