"""Oracle-diff cases for poketcg/src/engine/duel/ai/energy.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory RetrievePlayAreaAIScoreFromBackup1
CONTRACT["RetrievePlayAreaAIScoreFromBackup1"] = {"compare": ("a", "f", "c", "d", "e", "hl"), "preserve": ("a", "f", "c")}
CASES["RetrievePlayAreaAIScoreFromBackup1"] = [
    {"wram": {0xCDDD: b"\x00" * 7, 0xCDBE: b"\x00" * 7}, "read": {0xCDBE: 7}},
    {"wram": {0xCDDD: b"\x11\x22\x33\x44\x55\x66\x77", 0xCDBE: b"\xaa" * 7}, "read": {0xCDBE: 7}},
    dict(POISON, wram={0xCDDD: b"\x01\x02\x03\x04\x05\x06\x07", 0xCDBE: b"\xff" * 7}, read={0xCDBE: 7}),
]
# <<< factory RetrievePlayAreaAIScoreFromBackup1

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation RetrievePlayAreaAIScoreFromBackup1
MUTATIONS["RetrievePlayAreaAIScoreFromBackup1"] = {
    "source_symbol": "RetrievePlayAreaAIScoreFromBackup1",
    "before": "for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {",
    "after": "for (uint8_t b = MAX_PLAY_AREA_POKEMON - 1u; b != 0u; b--) {",
    "case_ids": ["RetrievePlayAreaAIScoreFromBackup1-1", "RetrievePlayAreaAIScoreFromBackup1-2"],
}
# <<< factory-mutation RetrievePlayAreaAIScoreFromBackup1
