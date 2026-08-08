POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wSerialOp = 0xCB74
wSerialFlags = 0xCB75
wSerialCounter = 0xCB76
wSerialCounter2 = 0xCB77
wSerialTimeoutCounter = 0xCB78
rSC = 0xFF02

CONTRACT = {
    "SerialTimerHandler": ("b", "c", "d", "e"),
}

CASES = {
    # Opcode 0 is neither $29 nor $12: pure early return, nothing touched.
    "SerialTimerHandler": [
        {"wram": {wSerialOp: b"\x00"},
         "read": {wSerialOp: 1, wSerialFlags: 1, wSerialTimeoutCounter: 1, rSC: 1}},
        # Begin a transfer: internal clock, then start. rSC lands at $81.
        {"wram": {wSerialOp: b"\x29", rSC: b"\x00"},
         "read": {rSC: 1}},
        # Transfer already in progress (rSC bit 7 set): early carry return, rSC untouched.
        {"wram": {wSerialOp: b"\x29", rSC: b"\x80"},
         "read": {rSC: 1}},
        # Timeout check: counter advanced -> counter2 follows, timeout resets.
        {"wram": {wSerialOp: b"\x12", wSerialCounter: b"\x05",
                  wSerialCounter2: b"\x03", wSerialTimeoutCounter: b"\x03"},
         "read": {wSerialCounter2: 1, wSerialTimeoutCounter: 1, wSerialFlags: 1}},
        # Timeout check: counter steady, timeout below 4 -> counts up, no flag.
        {"wram": {wSerialOp: b"\x12", wSerialCounter: b"\x05",
                  wSerialCounter2: b"\x05", wSerialTimeoutCounter: b"\x02"},
         "read": {wSerialCounter2: 1, wSerialTimeoutCounter: 1, wSerialFlags: 1}},
        # Timeout check: counter steady, timeout reaches 4 -> wSerialFlags bit 7.
        {"wram": {wSerialOp: b"\x12", wSerialCounter: b"\x05",
                  wSerialCounter2: b"\x05", wSerialTimeoutCounter: b"\x03",
                  wSerialFlags: b"\x00"},
         "read": {wSerialCounter2: 1, wSerialTimeoutCounter: 1, wSerialFlags: 1}},
        # Poisoned registers come back untouched on the early-return path.
        dict(POISON, wram={wSerialOp: b"\x00"}),
    ],
}
