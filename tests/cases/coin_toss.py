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

# >>> factory-cases-statics
wCoinTossNumHeads = 0xCD9D
wCoinTossScreenTextID = 0xCE4E
# <<< factory-cases-statics

# >>> factory TossCoinATimes
CONTRACT["TossCoinATimes"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["TossCoinATimes"] = [
    dict(POISON, a=0x01, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"a": 0x00, "d": 0x12, "e": 0x34,
     "keys": [0x00, 0x01],
     "wram": {0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x80",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
     "read": {0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
     "setup": [{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, a=0x01, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={0xFF97: b"\xC2", 0xC2F1: b"\x00", 0xCC09: b"\x00",
               0xCAC2: b"\x06", 0xCABB: b"\x00",
               0xCACA: b"\x00\x00\x00",
               0xCD9C: b"\xFF", 0xCD9D: b"\xFF", 0xCD9E: b"\xFF",
               0xCD9F: b"\x01", 0xCE4E: b"\x34\x12"},
         read={0xCD9C: 1, 0xCD9D: 1, 0xCD9E: 1, 0xCD9F: 1, 0xCE4E: 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory TossCoinATimes

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
# >>> factory-mutation TossCoinATimes
MUTATIONS["TossCoinATimes"] = {"source_symbol": "TossCoinATimes", "before": "\tTossCoinResult result = _TossCoin(a);", "after": "\tTossCoinResult result = _TossCoin((uint8_t)(a + 1u));", "case_ids": ["TossCoinATimes-0", "TossCoinATimes-1", "TossCoinATimes-2"]}
# <<< factory-mutation TossCoinATimes
