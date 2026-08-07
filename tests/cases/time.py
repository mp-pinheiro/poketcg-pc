"""Oracle-diff cases for poketcg/src/home/time.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPlayTimeCounterEnable = 0xCAC4
wPlayTimeCounter = 0xCAC5
wConsole = 0xCAB4

CONTRACT = {
    "IncrementPlayTimeCounter": ("b", "c", "d", "e"),
    "CheckForCGB": ("f", "b", "c", "d", "e", "hl"),
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
}
