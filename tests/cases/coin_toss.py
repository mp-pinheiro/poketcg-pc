"""Oracle-diff cases for poketcg/src/home/coin_toss.asm.

TossCoin and TossCoinATimes are not registered: both bank1call _TossCoin
(engine/duel/core.asm:7847), the full coin-toss animation/RNG sequence, which is
not ported and whose video/RNG side effects the differ cannot reproduce.
"""
from tests.cases._symbols import sym

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

# >>> factory TossCoinATimes
CONTRACT["TossCoinATimes"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["TossCoinATimes"] = [
    dict(POISON, a=0x01, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x00", sym("wDuelType"): b"\x00",
               sym("wDuelDisplayedScreen"): b"\x06", sym("wLCDC"): b"\x00",
               sym("wRNG1"): b"\x00\x00\x00",
               sym("wCoinTossTotalNum"): b"\xFF", sym("wCoinTossNumHeads"): b"\xFF", sym("wCoinTossDuelistType"): b"\xFF",
               sym("wCoinTossNumTossed"): b"\x01", sym("wCoinTossScreenTextID"): b"\x34\x12"},
         read={sym("wCoinTossTotalNum"): 1, sym("wCoinTossNumHeads"): 1, sym("wCoinTossDuelistType"): 1, sym("wCoinTossNumTossed"): 1, sym("wCoinTossScreenTextID"): 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"a": 0x00, "d": 0x12, "e": 0x34,
     "keys": [0x00, 0x01],
     "wram": {sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x00", sym("wDuelType"): b"\x00",
               sym("wDuelDisplayedScreen"): b"\x06", sym("wLCDC"): b"\x00",
               sym("wRNG1"): b"\x00\x00\x80",
               sym("wCoinTossTotalNum"): b"\xFF", sym("wCoinTossNumHeads"): b"\xFF", sym("wCoinTossDuelistType"): b"\xFF",
               sym("wCoinTossNumTossed"): b"\x01", sym("wCoinTossScreenTextID"): b"\x34\x12"},
     "read": {sym("wCoinTossTotalNum"): 1, sym("wCoinTossNumHeads"): 1, sym("wCoinTossDuelistType"): 1, sym("wCoinTossNumTossed"): 1, sym("wCoinTossScreenTextID"): 2},
     "setup": [{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, a=0x01, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x00", sym("wDuelType"): b"\x00",
               sym("wDuelDisplayedScreen"): b"\x06", sym("wLCDC"): b"\x00",
               sym("wRNG1"): b"\x00\x00\x00",
               sym("wCoinTossTotalNum"): b"\xFF", sym("wCoinTossNumHeads"): b"\xFF", sym("wCoinTossDuelistType"): b"\xFF",
               sym("wCoinTossNumTossed"): b"\x01", sym("wCoinTossScreenTextID"): b"\x34\x12"},
         read={sym("wCoinTossTotalNum"): 1, sym("wCoinTossNumHeads"): 1, sym("wCoinTossDuelistType"): 1, sym("wCoinTossNumTossed"): 1, sym("wCoinTossScreenTextID"): 2},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory TossCoinATimes

# >>> factory TossCoin
CONTRACT["TossCoin"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["TossCoin"] = [
    dict(POISON, d=0x12, e=0x34,
         keys=[0x00, 0x01],
         wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x00", sym("wDuelType"): b"\x00",
               sym("wDuelDisplayedScreen"): b"\x06", sym("wLCDC"): b"\x00",
               sym("wRNG1"): b"\x00\x00\x00",
               sym("wCoinTossTotalNum"): b"\xFF", sym("wCoinTossNumHeads"): b"\xFF", sym("wCoinTossDuelistType"): b"\xFF",
               sym("wCoinTossNumTossed"): b"\x01", sym("wCoinTossScreenTextID"): b"\x34\x12"},
         read={sym("wCoinTossTotalNum"): 1, sym("wCoinTossNumHeads"): 1, sym("wCoinTossDuelistType"): 1, sym("wCoinTossNumTossed"): 1, sym("wCoinTossScreenTextID"): 2, sym("wDuelDisplayedScreen"): 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, d=0x56, e=0x78,
         keys=[0x00, 0x01],
         wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x00", sym("wDuelType"): b"\x00",
               sym("wDuelDisplayedScreen"): b"\x06", sym("wLCDC"): b"\x00",
               sym("wRNG1"): b"\x00\x00\x80",
               sym("wCoinTossTotalNum"): b"\xFF", sym("wCoinTossNumHeads"): b"\xFF", sym("wCoinTossDuelistType"): b"\xFF",
               sym("wCoinTossNumTossed"): b"\x01", sym("wCoinTossScreenTextID"): b"\x78\x56"},
         read={sym("wCoinTossTotalNum"): 1, sym("wCoinTossNumHeads"): 1, sym("wCoinTossDuelistType"): 1, sym("wCoinTossNumTossed"): 1, sym("wCoinTossScreenTextID"): 2, sym("wDuelDisplayedScreen"): 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, d=0xDD, e=0xEE,
         keys=[0x00, 0x01],
         wram={sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x00", sym("wDuelType"): b"\x00",
               sym("wDuelDisplayedScreen"): b"\x06", sym("wLCDC"): b"\x00",
               sym("wRNG1"): b"\x00\x00\x00",
               sym("wCoinTossTotalNum"): b"\xFF", sym("wCoinTossNumHeads"): b"\xFF", sym("wCoinTossDuelistType"): b"\xFF",
               sym("wCoinTossNumTossed"): b"\x01", sym("wCoinTossScreenTextID"): b"\xEE\xDD"},
         read={sym("wCoinTossTotalNum"): 1, sym("wCoinTossNumHeads"): 1, sym("wCoinTossDuelistType"): 1, sym("wCoinTossNumTossed"): 1, sym("wCoinTossScreenTextID"): 2, sym("wDuelDisplayedScreen"): 1},
         setup=[{"fn": "CopyDMAFunction"},
                {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory TossCoin

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {
    "CompareDEtoBC": {
        "source_symbol": "CompareDEtoBC",
        "before": "if (d != b)",
        "after": "if (d == b)",
        "case_ids": ["CompareDEtoBC-1", "CompareDEtoBC-0", "CompareDEtoBC-5"],
    },
}
# >>> factory-mutation TossCoinATimes
MUTATIONS["TossCoinATimes"] = {"source_symbol": "TossCoinATimes", "before": "\tTossCoinResult result = _TossCoin(a);", "after": "\tTossCoinResult result = _TossCoin((uint8_t)(a + 1u));", "case_ids": ["TossCoinATimes-0", "TossCoinATimes-1", "TossCoinATimes-2"]}
# <<< factory-mutation TossCoinATimes
# >>> factory-mutation TossCoin
MUTATIONS["TossCoin"] = {"source_symbol": "TossCoin", "before": "TossCoinRoutineResult TossCoin(uint16_t de, uint16_t hl)\n{\n\twCoinTossScreenTextID = (uint8_t)de;\n\tgb_write8((uint16_t)(wCoinTossScreenTextID_ADDR + 1u), (uint8_t)(de >> 8));\n\tTossCoinResult result = _TossCoin(1u);", "after": "TossCoinRoutineResult TossCoin(uint16_t de, uint16_t hl)\n{\n\twCoinTossScreenTextID = (uint8_t)de;\n\tgb_write8((uint16_t)(wCoinTossScreenTextID_ADDR + 1u), (uint8_t)(de >> 8));\n\tTossCoinResult result = _TossCoin(2u);", "case_ids": ["TossCoin-0", "TossCoin-1", "TossCoin-2"]}
# <<< factory-mutation TossCoin
