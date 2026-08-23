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

# >>> factory FindPlayAreaCardWithHighestAIScore
CONTRACT["FindPlayAreaCardWithHighestAIScore"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["FindPlayAreaCardWithHighestAIScore"] = [
    # the whole 256-byte window scanned by the count-0 (== 256 iterations) loop is
    # seeded; wAIEnergyAttachLogicFlags (0xCDD8) lives at offset 25 inside it.
    {"wram": {0xCDBF: b"\x00" * 256}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x85" + b"\x00" * 255}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x84" + b"\x00" * 255}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x00\x00\x00\x90" + b"\x00" * 252}, "read": {0xFF9D: 1}},
    {"wram": {0xCDBF: b"\x00\x40\x90" + b"\x00" * 22 + b"\x80" + b"\x00" * 230}, "read": {0xFF9D: 1}},
    dict(POISON, wram={0xCDBF: b"\x00\x91\x00\x00\x91" + b"\x00" * 20 + b"\x80" + b"\x00" * 230}, read={0xFF9D: 1}),
    dict(POISON, wram={0xCDBF: b"\x90\x00\x90" + b"\x00" * 253}, read={0xFF9D: 1}),
]
# <<< factory FindPlayAreaCardWithHighestAIScore

# >>> factory CheckSpecificDecksToAttachDoubleColorless
CONTRACT["CheckSpecificDecksToAttachDoubleColorless"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckSpecificDecksToAttachDoubleColorless"] = [
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {0xCC0E: b"\x00"}},
    dict(POISON, wram={0xCC0E: b"\x00"}),
    {"b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x5566,
     "wram": {0xCC0E: b"\x17", 0xFF97: b"\xC2", 0xC2BB: b"\x03", 0xC400+3: b"\x36",
               0xC2EE: b"\x01", 0xC242: b"\x06", 0xC400+6: b"\x07"}},
]
# <<< factory CheckSpecificDecksToAttachDoubleColorless

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
# >>> factory-mutation FindPlayAreaCardWithHighestAIScore
MUTATIONS["FindPlayAreaCardWithHighestAIScore"] = {
    "source_symbol": "FindPlayAreaCardWithHighestAIScore",
    "before": "\tif (e < 0x85u) {",
    "after": "\tif (e < 0x86u) {",
    "case_ids": ["FindPlayAreaCardWithHighestAIScore-1"],
}
# <<< factory-mutation FindPlayAreaCardWithHighestAIScore
# >>> factory-mutation CheckSpecificDecksToAttachDoubleColorless
MUTATIONS["CheckSpecificDecksToAttachDoubleColorless"] = {"source_symbol": "CheckSpecificDecksToAttachDoubleColorless", "before": "return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x10u, b, c, d, e, hl};", "after": "return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x00u, b, c, d, e, hl};", "case_ids": ["CheckSpecificDecksToAttachDoubleColorless-2"]}
# <<< factory-mutation CheckSpecificDecksToAttachDoubleColorless
