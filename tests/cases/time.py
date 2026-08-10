"""Oracle-diff cases for poketcg/src/home/time.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPlayTimeCounterEnable = 0xCAC4
wPlayTimeCounter = 0xCAC5
wConsole = 0xCAB4
rTMA = 0xFF06
rTAC = 0xFF07
rSPD = 0xFF4D

CONTRACT = {
    "IncrementPlayTimeCounter": ("b", "c", "d", "e"),
    "CheckForCGB": ("f", "b", "c", "d", "e", "hl"),
    "SetupTimer": ("a", "b", "f", "c", "d", "e", "hl"),
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
        {"wram": {wConsole: b"\x00", rSPD: b"\x00"}, "read": {rTMA: 1, rTAC: 1}},
        {"wram": {wConsole: b"\x02", rSPD: b"\x00"}, "read": {rTMA: 1, rTAC: 1}},
        dict(POISON, wram={wConsole: b"\x02", rSPD: b"\x80"}, read={rTMA: 1, rTAC: 1}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
