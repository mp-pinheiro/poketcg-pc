"""Oracle-diff cases for poketcg/src/home/time.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPlayTimeCounterEnable = 0xCAC4
wPlayTimeCounter = 0xCAC5
wConsole = 0xCAB4
rTMA = 0xFF06
rTAC = 0xFF07


CONTRACT = {
    "IncrementPlayTimeCounter": {"compare": ("b", "c", "d", "e"),
                                 "preserve": ("b", "c", "d", "e")},
    "CheckForCGB": {"compare": ("f", "b", "c", "d", "e", "hl"),
                    "preserve": ("b", "c", "d", "e", "hl")},
    "SetupTimer": {"compare": ("c", "d", "e", "hl"),
                   "preserve": ("c", "d", "e", "hl")},
}


CASES = {
    "IncrementPlayTimeCounter": [
        {"wram": {wPlayTimeCounterEnable: b"\x00" + b"\x3b\x00\x00\x00\x00"}},
        {"wram": {wPlayTimeCounterEnable: b"\x01" + b"\x00\x00\x00\x00\x00"}},
        {"wram": {wPlayTimeCounterEnable: b"\x01" + b"\x3b\x00\x00\x00\x00"}},
        {"wram": {wPlayTimeCounterEnable: b"\x01" + b"\x3b\x3b\x3b\x00\x00"}},
        {"wram": {wPlayTimeCounterEnable: b"\x01" + b"\x3b\x3b\x3b\xff\x05"}},
        dict(POISON, wram={wPlayTimeCounterEnable: b"\x01" + b"\x05\x09\x21\x80\x07"}),
    ],
    "CheckForCGB": [
        {"wram": {wConsole: b"\x02"}},
        {"wram": {wConsole: b"\x00"}},
        {"wram": {wConsole: b"\x01"}},
        {"wram": {wConsole: b"\x03"}},
        dict(POISON, wram={wConsole: b"\x02"}),
    ],
    # Oracle-run: the snapshot now captures $FF00-$FF7F, so TMA/TAC are diffed
    # against the real ROM rather than against an asm-derived expectation.
    "SetupTimer": [
        {"wram": {wConsole: b"\x00"}, "read": {rTMA: 1, rTAC: 1}},
        {"wram": {wConsole: b"\x02"}, "read": {rTMA: 1, rTAC: 1}},
        dict(POISON, wram={wConsole: b"\x02"}, read={rTMA: 1, rTAC: 1}),
    ],
}
# >>> factory-cases-statics
hBankROM_A = 0xFF80
wReentrancyFlag_A = 0xCABA
wTimerCounter_A = 0xCAC3
# <<< factory-cases-statics

# >>> factory TimerHandler
CONTRACT["TimerHandler"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["TimerHandler"] = [
    {"wram": {hBankROM_A: b"\x01", wReentrancyFlag_A: b"\x00", wTimerCounter_A: b"\x00"},
     "instruction_budget": 200000, "cycle_budget": 1000000,
     "read": {hBankROM_A: 1, wReentrancyFlag_A: 1, wTimerCounter_A: 1}},
    dict(POISON, wram={hBankROM_A: b"\x01", wReentrancyFlag_A: b"\x00", wTimerCounter_A: b"\x03"},
         instruction_budget=200000, cycle_budget=1000000,
         read={hBankROM_A: 1, wReentrancyFlag_A: 1, wTimerCounter_A: 1}),
]
# <<< factory TimerHandler

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)


MUTATIONS = {
    "IncrementPlayTimeCounter": {
        "source_symbol": "IncrementPlayTimeCounter",
        "before": "if (b0 < 60u)",
        "after": "if (b0 <= 60u)",
        "case_ids": ["IncrementPlayTimeCounter-2", "IncrementPlayTimeCounter-0",
                      "IncrementPlayTimeCounter-1", "IncrementPlayTimeCounter-3",
                      "IncrementPlayTimeCounter-4", "IncrementPlayTimeCounter-5"],
    },
}
# >>> factory-mutation TimerHandler
MUTATIONS["TimerHandler"] = {"source_symbol": "TimerHandler", "before": "\twTimerCounter = (uint8_t)(counter + 1u);", "after": "\twTimerCounter = counter;", "case_ids": ["TimerHandler-0", "TimerHandler-1"]}
# <<< factory-mutation TimerHandler
