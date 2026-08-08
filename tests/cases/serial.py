POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wSerialOp = 0xCB74
wSerialFlags = 0xCB75
wSerialCounter = 0xCB76
wSerialCounter2 = 0xCB77
wSerialTimeoutCounter = 0xCB78
wSerialSendSave = 0xCB7D
wSerialSendBufToggle = 0xCB7E
wSerialSendBufIndex = 0xCB7F
wcb80 = 0xCB80
wSerialSendBuf = 0xCB81
wSerialLastReadCA = 0xCBA1
wSerialRecvCounter = 0xCBA2
wcba3 = 0xCBA3
wSerialRecvIndex = 0xCBA4
wSerialRecvBuf = 0xCBA5
wSerialEnd = 0xCBC5
wPrinterPacketSequence = 0xCE63
wSerialDataPtr = 0xCE70
rSB = 0xFF01
rSC = 0xFF02
rIF = 0xFF0F
rIE = 0xFFFF

CONTRACT = {
    "SerialTimerHandler": ("b", "c", "d", "e"),
    "Func_0cc5": ("a", "b", "c", "d", "e", "f"),
    "SerialHandler": ("a", "b", "c", "d", "e", "f", "hl"),
    "SerialHandleRecv": ("a", "b", "c", "d", "e", "hl"),
    "SerialHandleSend": ("a", "b", "c", "d", "e", "hl"),
    "SerialSendByte": ("a", "b", "c", "d", "e", "f", "hl"),
    "Func_0e32": ("a", "b", "c", "d", "e", "f", "hl"),
    "SerialRecvByte": ("a", "b", "c", "d", "e", "f", "hl"),
    "SerialExchangeBytes": ("a", "b", "c", "d", "e", "f", "hl"),
    "Func_0e8e": ("a", "d", "e"),
    "ResetSerial": ("d", "e"),
    "ClearSerialData": ("d", "e"),
    "SerialSendBytes": ("a", "b", "c", "d", "e", "f", "hl"),
    "SerialRecvBytes": ("a", "b", "c", "d", "e", "f", "hl"),
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

    # a==0 branch is a poll; a!=0 branch kicks SC_INTERNAL then spins on
    # wSerialRecvCounter, so it must be pre-seeded nonzero or the call hangs
    # (no ISR ever runs mid-call).
    "Func_0cc5": [
        # a==0, counter==0: earliest return, carry clear.
        {"a": 0, "wram": {wSerialRecvCounter: b"\x00"}},
        dict(POISON, a=0, wram={wSerialRecvCounter: b"\x00"}),
        # a==0, counter!=0, recvbuf==$29: success, e=$12, delay loop skipped
        # (bc preserved), full WRAM reset, wSerialOp<-$12.
        {"a": 0, "b": 0xBB, "c": 0xCC, "e": 0xEE,
         "wram": {wSerialRecvCounter: b"\x05", wSerialRecvBuf: b"\x29"},
         "read": {wSerialSendBufIndex: 1, wcb80: 1, wSerialSendBufToggle: 1,
                   wSerialSendSave: 1, wcba3: 1, wSerialRecvIndex: 1,
                   wSerialRecvCounter: 1, wSerialLastReadCA: 1, wSerialOp: 1}},
        # a==0, counter!=0, recvbuf mismatch: a=0, e=$12, carry set, no reset.
        {"a": 0, "b": 0xBB, "c": 0xCC,
         "wram": {wSerialRecvCounter: b"\x07", wSerialRecvBuf: b"\x00",
                  wSerialOp: b"\x99"},
         "read": {wSerialOp: 1}},
        # a!=0, recvbuf==$12: success, e=$29, 2048-iteration delay leaves bc=0.
        {"a": 1, "b": 0xBB, "c": 0xCC,
         "wram": {wSerialRecvCounter: b"\x03", wSerialRecvBuf: b"\x12"},
         "read": {wSerialOp: 1}},
        # a!=0, recvbuf mismatch: a=0, e=$29, carry set, bc preserved.
        {"a": 1, "b": 0xBB, "c": 0xCC,
         "wram": {wSerialRecvCounter: b"\x02", wSerialRecvBuf: b"\x00"}},
    ],

    # pyboy's serial model hardcodes SB ($FF01) to always read back $FF
    # ("Always 0xFF for a disconnected link cable", pyboy/core/serial.py) --
    # confirmed empirically too: ResetSerial's unconditional `xor a /
    # ldh [rSB],a` still reads back $FF on the oracle. rSB is therefore
    # never diffed via `read`, and any branch keyed off the byte SerialHandler
    # reads from rSB sees exactly $FF, never a seeded value -- so the
    # wSerialOp==0 sub-branch where recvbuf ends up $12 (skipping the rSC
    # write) is unreachable here and not covered below.
    "SerialHandler": [
        # wSerialOp==0 default path: rSB always reads $FF, so recvbuf != $12
        # and the external-clock rewrite always happens. Seeded via `setup`,
        # not `wram`: `wram` keys are auto-diffed after the call too, and
        # pyboy hardcodes rSB to read back $FF regardless of what's written,
        # so a diffed rSB write always mismatches.
        {"wram": {wPrinterPacketSequence: b"\x00",
                  wSerialOp: b"\x00", wSerialCounter: b"\x00"},
         "setup": [{"fn": "SendByteThroughSerialData", "a": 0xFF}],
         "read": {wSerialRecvCounter: 1, wSerialRecvBuf: 1, rSC: 1,
                  wSerialCounter: 1}},
        dict(POISON, wram={wPrinterPacketSequence: b"\x00", wSerialOp: b"\x00"},
             setup=[{"fn": "SendByteThroughSerialData", "a": 0xFF}]),
        # Printer-sequence branch: dispatches into ExecutePrinterPacketSequence.
        {"wram": {wPrinterPacketSequence: b"\x01", wSerialDataPtr: b"\x00\xC1", 0xC100: b"\x42"},
         "read": {wPrinterPacketSequence: 1, rSC: 1, wSerialCounter: 1}},
        # wSerialOp!=0, ==$29: send/recv a byte (rSB forced $FF, so
        # SerialHandleRecv takes its $00-or-$FF branch), external-clock
        # rewrite skipped.
        {"wram": {wPrinterPacketSequence: b"\x00", wSerialOp: b"\x29", wSerialLastReadCA: b"\x02",
                  wSerialSendSave: b"\x33", rSC: b"\x00"},
         "read": {rSC: 1, wSerialCounter: 1, wSerialFlags: 1}},
        # wSerialOp!=0, !=$29: external-clock rewrite happens.
        {"wram": {wPrinterPacketSequence: b"\x00", wSerialOp: b"\x01", wSerialLastReadCA: b"\x02",
                  wSerialSendSave: b"\x00", wSerialSendBufToggle: b"\x00", rSC: b"\x00"},
         "read": {rSC: 1}},
    ],

    # d overridden to 0 only on the buffer-write path; e is reloaded from WRAM
    # on that same path and preserved (whatever `dec e` leaves it) elsewhere.
    "SerialHandleRecv": [
        {"a": 0, "d": 0, "wram": {wSerialLastReadCA: b"\x00", wSerialFlags: b"\x00"},
         "read": {wSerialFlags: 1}},
        dict(POISON, wram={wSerialLastReadCA: b"\x00", wSerialRecvIndex: b"\x05",
                            wcba3: b"\x0A", wSerialRecvCounter: b"\x00",
                            wSerialFlags: b"\x00"},
             read={wSerialRecvBuf + 5: 1, wSerialRecvIndex: 1,
                   wSerialRecvCounter: 1, wSerialFlags: 1}),
        # .last_was_ca: a complemented, then written into a non-full buffer.
        {"a": 0x55, "d": 0xDD,
         "wram": {wSerialLastReadCA: b"\x01", wSerialRecvIndex: b"\x00",
                  wcba3: b"\x00", wSerialRecvCounter: b"\x00", wSerialFlags: b"\x00"},
         "read": {wSerialLastReadCA: 1, wSerialRecvBuf: 1, wSerialRecvIndex: 1,
                   wSerialRecvCounter: 1}},
        {"a": 0xAC, "d": 0x77, "wram": {wSerialLastReadCA: b"\x05"},
         "read": {wSerialLastReadCA: 1}},
        {"a": 0xCA, "d": 0x77, "wram": {wSerialLastReadCA: b"\x05"},
         "read": {wSerialLastReadCA: 1}},
        {"a": 0xFF, "d": 0x77,
         "wram": {wSerialLastReadCA: b"\x05", wSerialFlags: b"\x00"},
         "read": {wSerialFlags: 1}},
        # Buffer full: d preserved, wSerialFlags bit 0 set.
        {"a": 0x33, "d": 0x77,
         "wram": {wSerialLastReadCA: b"\x05", wSerialRecvIndex: b"\x07",
                  wcba3: b"\x08", wSerialFlags: b"\x00"},
         "read": {wSerialFlags: 1}},
    ],

    "SerialHandleSend": [
        {"d": 0, "e": 0, "wram": {wSerialSendSave: b"\x00", wSerialSendBufToggle: b"\x00"}},
        dict(POISON, wram={wSerialSendSave: b"\x77"}, read={wSerialSendSave: 1}),
        dict(POISON, wram={wSerialSendSave: b"\x00", wSerialSendBufToggle: b"\x00"}),
        # send_buf, non-escaped byte.
        {"wram": {wSerialSendSave: b"\x00", wSerialSendBufToggle: b"\x05",
                  wSerialSendBufIndex: b"\x03", wSerialSendBuf + 3: b"\x10"},
         "read": {wSerialSendBufToggle: 1, wSerialSendBufIndex: 1}},
        # send_buf, escaped byte ($6C ^ $C0 == $AC).
        {"wram": {wSerialSendSave: b"\x00", wSerialSendBufToggle: b"\x02",
                  wSerialSendBufIndex: b"\x0A", wSerialSendBuf + 10: b"\x6C"},
         "read": {wSerialSendBufToggle: 1, wSerialSendBufIndex: 1, wSerialSendSave: 1}},
    ],

    # `.loop_wait` only advances once the ring isn't full; every case keeps
    # (wSerialSendBufIndex-1)&$1F != wcb80 at entry so it never spins.
    "SerialSendByte": [
        {"a": 0, "wram": {wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
                           wSerialSendBufToggle: b"\x00"},
         "read": {wcb80: 1, wSerialSendBuf: 1, wSerialSendBufToggle: 1}},
        # H-flag boundary: toggle $0F -> $10.
        dict(POISON, wram={wcb80: b"\x05", wSerialSendBufIndex: b"\x07",
                            wSerialSendBufToggle: b"\x0F"},
             read={wcb80: 1, wSerialSendBuf + 5: 1, wSerialSendBufToggle: 1}),
        # Z-flag boundary: toggle $FF -> $00; entry carry passes through.
        {"a": 0x42, "f": 0x10,
         "wram": {wcb80: b"\x00", wSerialSendBufIndex: b"\x02",
                  wSerialSendBufToggle: b"\xFF"},
         "read": {wcb80: 1, wSerialSendBuf: 1, wSerialSendBufToggle: 1}},
        # Ring index wraps $1F -> $00.
        {"a": 0x77, "wram": {wcb80: b"\x1F", wSerialSendBufIndex: b"\x01",
                              wSerialSendBufToggle: b"\x00"},
         "read": {wcb80: 1, wSerialSendBuf + 0x1F: 1}},
    ],

    "Func_0e32": [
        {"wram": {wSerialRecvCounter: b"\x00"}},
        dict(POISON, wram={wSerialRecvCounter: b"\x05"}),
        {"wram": {wSerialRecvCounter: b"\xFF"}},
    ],

    "SerialRecvByte": [
        {"wram": {wSerialRecvCounter: b"\x00", wSerialFlags: b"\x00"}},
        dict(POISON, wram={wSerialRecvCounter: b"\x00", wSerialFlags: b"\x40"}),
        {"wram": {wSerialRecvCounter: b"\x03", wcba3: b"\x02",
                  wSerialRecvBuf + 2: b"\x99"},
         "read": {wSerialRecvCounter: 1, wcba3: 1}},
        # Byte==0 is the Z-flag boundary.
        {"wram": {wSerialRecvCounter: b"\x01", wcba3: b"\x00", wSerialRecvBuf: b"\x00"},
         "read": {wSerialRecvCounter: 1, wcba3: 1}},
        # Ring index wraps $1F -> $00.
        {"wram": {wSerialRecvCounter: b"\x01", wcba3: b"\x1F",
                  wSerialRecvBuf + 0x1F: b"\x55"},
         "read": {wcba3: 1}},
    ],

    # Every receive that finds wSerialRecvCounter==0 returns carry, so `b`
    # can only reach 0 through pre-seeded receive data. The diff-b/diff-c
    # windowing throttle (send skipped once (b-c)>=$1F) is not separately
    # exercised: reaching it needs >=31 pre-seeded receive bytes for no
    # additional coverage over the send/receive/error paths below.
    "SerialExchangeBytes": [
        # c==0: no send, no receive, immediate success.
        {"c": 0, "hl": 0xC100, "d": 0xC2, "e": 0x00,
         "wram": {wSerialFlags: b"\x00"}},
        # c==1, receive data pre-seeded: full send+receive round trip.
        {"c": 1, "hl": 0xC100, "d": 0xC2, "e": 0x00,
         "wram": {0xC100: b"\x11", wSerialRecvCounter: b"\x01", wcba3: b"\x00",
                  wSerialRecvBuf: b"\x22", wcb80: b"\x00",
                  wSerialSendBufIndex: b"\x00", wSerialFlags: b"\x00"},
         "read": {0xC200: 1, wSerialSendBuf: 1}},
        # wSerialFlags pre-set: error exit after one iteration; b stays at
        # entry c (receive failed, carry) while c decrements (send succeeded).
        {"c": 1, "hl": 0xC100, "d": 0xC2, "e": 0x00,
         "wram": {0xC100: b"\x33", wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
                  wSerialFlags: b"\x40"},
         "read": {wSerialSendBuf: 1}},
    ],

    "Func_0e8e": [
        {"wram": {rIE: b"\x00", rIF: b"\x08", wSerialOp: b"\xFF", wSerialFlags: b"\xFF"},
         "read": {wSerialOp: 1, wSerialFlags: 1, rSC: 1, rIF: 1}},
        dict(POISON, wram={rIE: b"\xE0", rIF: b"\x08"}, read={rIE: 1, rIF: 1}),
        {"wram": {rIE: b"\x10", rIF: b"\x00"}, "read": {rIE: 1}},
    ],

    "ResetSerial": [
        {"wram": {wSerialOp: b"\xFF" * (wSerialEnd - wSerialOp), rIE: b"\xFF",
                  rSC: b"\x7F"},
         "read": {wSerialOp: wSerialEnd - wSerialOp, rIE: 1, rSC: 1}},
        dict(POISON, wram={wSerialOp: b"\xAB" * (wSerialEnd - wSerialOp)}),
    ],

    "ClearSerialData": [
        {"wram": {wSerialOp: b"\xFF" * (wSerialEnd - wSerialOp)},
         "read": {wSerialOp: wSerialEnd - wSerialOp}},
        dict(POISON, wram={wSerialOp: b"\xAB" * (wSerialEnd - wSerialOp)}),
    ],

    # wSerialSendBuf has only 32 slots and nothing drains it mid-call, so
    # bc==0 (the zero-means-maximum boundary) cannot complete standalone --
    # not even natively, since SerialSendByte's own ring-full spin would
    # hang the test process itself, not just the oracle. Coverage below uses
    # bc=1/2 (within ring capacity) plus the error-exit path instead.
    "SerialSendBytes": [
        {"hl": 0xC100, "b": 0, "c": 1,
         "wram": {0xC100: b"\x11", wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
                  wSerialFlags: b"\x00"},
         "read": {wSerialSendBuf: 1}},
        # bc preserved: exit b/c must equal entry, not the live decremented value.
        {"a": 0xAA, "f": 0xF0, "b": 0, "c": 2, "d": 0xDD, "e": 0xEE, "hl": 0xC100,
         "wram": {0xC100: b"\x11\x22", wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
                  wSerialFlags: b"\x00"},
         "read": {wSerialSendBuf: 2}},
        # wSerialFlags pre-set: error exit after 1 byte, bc preserved despite progress.
        {"hl": 0xC100, "b": 0, "c": 5,
         "wram": {0xC100: b"\x99", wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
                  wSerialFlags: b"\x40"},
         "read": {wSerialSendBuf: 1}},
    ],

    # Same untestable bc==0 boundary as SerialSendBytes (the asm's `halt` on
    # an empty queue can never wake up in this harness); every case
    # pre-seeds enough already-arrived bytes that SerialRecvByte never
    # returns carry.
    "SerialRecvBytes": [
        {"hl": 0xC100, "b": 0, "c": 1,
         "wram": {wSerialRecvCounter: b"\x01", wcba3: b"\x00",
                  wSerialRecvBuf: b"\x77", wSerialFlags: b"\x00"},
         "read": {0xC100: 1, wSerialRecvCounter: 1, wcba3: 1}},
        {"a": 0xAA, "f": 0xF0, "b": 0, "c": 2, "d": 0xDD, "e": 0xEE, "hl": 0xC100,
         "wram": {wSerialRecvCounter: b"\x02", wcba3: b"\x00",
                  wSerialRecvBuf: b"\x11\x22", wSerialFlags: b"\x00"},
         "read": {0xC100: 2, wcba3: 1}},
        {"hl": 0xC100, "b": 0, "c": 5,
         "wram": {wSerialRecvCounter: b"\x01", wcba3: b"\x00",
                  wSerialRecvBuf: b"\x88", wSerialFlags: b"\x40"},
         "read": {0xC100: 1, wcba3: 1}},
    ],
}
