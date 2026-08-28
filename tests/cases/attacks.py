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

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wSelectedAttack = 0xCCC6
wAIScore = 0xCDBE
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wAIBarrierFlagCounter = 0xCDA7
wAIExecuteProcessedAttack = 0xCDD9
wAIPlusPowerAttack = 0xCDD6
wAIRetreatScore = 0xCDB4
wAITriedAttack = 0xCDDB
wDamage = 0xCCB9
wFirstAttackAIScore = 0xCDBF
wPreviousAIFlags = 0xCE20
wSelectedAttack = 0xCCC6
hTempPlayAreaLocation_ff9d = 0xFF9D
# <<< factory-cases-statics

# >>> factory GetAIScoreOfAttack
CONTRACT["GetAIScoreOfAttack"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["GetAIScoreOfAttack"] = [
    {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2E8: b"\x05", wSelectedAttack: b"\x00", wAIScore: b"\x99"}, "expect": {wSelectedAttack: b"\x01", wAIScore: b"\x00"}, "read": {wSelectedAttack: 1, wAIScore: 1}},
    {"a": 0x5A, "wram": {hWhoseTurn: b"\xC2", 0xC2E8: b"\x05", wSelectedAttack: b"\x00", wAIScore: b"\x12"}, "expect": {wSelectedAttack: b"\x5A", wAIScore: b"\x00"}, "read": {wSelectedAttack: 1, wAIScore: 1}},
    dict(POISON, a=0xEE, wram={hWhoseTurn: b"\xC2", 0xC2E8: b"\x05", wSelectedAttack: b"\x00", wAIScore: b"\x44"}, expect={wSelectedAttack: b"\xEE", wAIScore: b"\x00"}, read={wSelectedAttack: 1, wAIScore: 1}),
]
# <<< factory GetAIScoreOfAttack

# >>> factory AIProcessAttacks
CONTRACT["AIProcessAttacks"] = {"compare": ("f",), "preserve": ()}
CASES["AIProcessAttacks"] = [
    {"wram": {wAIBarrierFlagCounter: b"\x80", wAIExecuteProcessedAttack: b"\x00", wAIRetreatScore: b"\x00"}, "expect": {wAIRetreatScore: b"\x01"}, "read": {wAIRetreatScore: 1}},
    {"wram": {wPreviousAIFlags: b"\x01", wAIPlusPowerAttack: b"\x03", wAIExecuteProcessedAttack: b"\x01"}, "expect": {wSelectedAttack: b"\x03"}, "read": {wSelectedAttack: 1}},
    dict(POISON, wram={wPreviousAIFlags: b"\x01", wAIPlusPowerAttack: b"\x7e", wAIExecuteProcessedAttack: b"\x01"}, expect={wSelectedAttack: b"\x7e"}, read={wSelectedAttack: 1}),
    {"wram": {wAIBarrierFlagCounter: b"\x80", wAIExecuteProcessedAttack: b"\x01"}},
]
# <<< factory AIProcessAttacks

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation GetAIScoreOfAttack
MUTATIONS["GetAIScoreOfAttack"] = {"source_symbol": "GetAIScoreOfAttack", "before": "void GetAIScoreOfAttack(uint8_t a)\n{\n\twSelectedAttack = a;", "after": "void GetAIScoreOfAttack(uint8_t a)\n{\n\twSelectedAttack = 0u;", "case_ids": ["GetAIScoreOfAttack-0", "GetAIScoreOfAttack-1", "GetAIScoreOfAttack-2"]}
# <<< factory-mutation GetAIScoreOfAttack
# >>> factory-mutation AIProcessAttacks
MUTATIONS["AIProcessAttacks"] = {"source_symbol": "AIProcessAttacks", "before": "\t\twSelectedAttack = wAIPlusPowerAttack;", "after": "\t\twSelectedAttack = 0u;", "case_ids": ["AIProcessAttacks-1", "AIProcessAttacks-2"]}
# <<< factory-mutation AIProcessAttacks
