"""Oracle-diff cases for poketcg/src/engine/menus/duel_init.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
DI_WLCDC = 0xCABB
DI_HW = 0xFF40
DI_WD291 = 0xD291
DI_FRAME = 0xCCF3
DI_KEYS = [0x00, 0x01]
DI_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
DI_BUDGET = 60000000
DI_CYCLES = 240000000
# <<< factory-cases-statics

# >>> factory Duel_Init
CONTRACT["Duel_Init"] = {"compare": (), "preserve": ()}
CASES["Duel_Init"] = [
    {"f": 0x00, "keys": DI_KEYS, "setup": DI_SETUP, "wram": {DI_WLCDC: b"\x00", DI_HW: b"\x80", DI_WD291: b"\x41"}, "read": {DI_FRAME: 1}, "instruction_budget": DI_BUDGET, "cycle_budget": DI_CYCLES},
    dict(POISON, keys=DI_KEYS, setup=DI_SETUP, wram={DI_WLCDC: b"\x00", DI_HW: b"\x80", DI_WD291: b"\x41"}, read={DI_FRAME: 1}, instruction_budget=DI_BUDGET, cycle_budget=DI_CYCLES),
]
# <<< factory Duel_Init

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Duel_Init
MUTATIONS["Duel_Init"] = {"source_symbol": "Duel_Init", "before": "\twTextBoxFrameType = 4u;", "after": "\twTextBoxFrameType = 5u;", "case_ids": ["Duel_Init-0", "Duel_Init-1"]}
# <<< factory-mutation Duel_Init
# >>> factory-completion Duel_Init
for _record in SCHEMA2_CASES["Duel_Init"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x378A}
# <<< factory-completion Duel_Init
