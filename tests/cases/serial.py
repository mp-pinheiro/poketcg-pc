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
    "SerialTimerHandler": {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    "Func_0cc5": {"compare": ("a", "b", "c", "d", "e", "f"), "preserve": ("d",)},
    "SerialHandler": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "f", "hl")},
    "SerialHandleRecv": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "SerialHandleSend": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")},
    "SerialSendByte": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")},
    "Func_0e32": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SerialRecvByte": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "SerialExchangeBytes": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ()},
    "Func_0e8e": {"compare": ("a", "d", "e"), "preserve": ("d", "e")},
    "ResetSerial": {"compare": ("d", "e"), "preserve": ("d", "e")},
    "ClearSerialData": {"compare": ("d", "e"), "preserve": ("d", "e")},
    "SerialSendBytes": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e")},
    "SerialRecvBytes": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e")},
}

CASES = {
    # Opcode 0 is neither $29 nor $12: pure early return, nothing touched.
    "SerialTimerHandler": [
        {"wram": {wSerialOp: b"\x00", rSC: b"\x00"},
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
# >>> factory DuelTransmissionError
wDuelReturnAddress = 0xCBE5
wDuelResult = 0xD0C3
wCurSongID = 0xDD80
wTxRam3 = 0xCE43
wTxRam3_b = 0xCE45
DUEL_TRANSMISSION_ERROR_RET_PC = 0x0F57

CONTRACT["DuelTransmissionError"] = {"compare": (), "preserve": ()}
TRANSMISSION_ERROR_SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
TRANSMISSION_ERROR_READ = {wTxRam3: 1, wTxRam3_b: 1, wDuelResult: 1, wCurSongID: 1,
                            wSerialOp: wSerialEnd - wSerialOp}
TRANSMISSION_ERROR_VREAD = {0: {0x9980: 1, 0x9A32: 1}}
CASES["DuelTransmissionError"] = [
    {"keys": 0x01, "wram": {wSerialFlags: b"\x00", wDuelReturnAddress: b"\x00\xC3"},
     "setup": TRANSMISSION_ERROR_SETUP,
     "read": TRANSMISSION_ERROR_READ, "vread": TRANSMISSION_ERROR_VREAD},
    # wSerialFlags == 0xFF: `ld h, 0` zero-extends into hl, so wTxRam3_b must
    # read back 0x00, never 0xFF.
    {"keys": 0x01, "wram": {wSerialFlags: b"\xFF", wDuelReturnAddress: b"\x00\xC3"},
     "setup": TRANSMISSION_ERROR_SETUP,
     "read": TRANSMISSION_ERROR_READ, "vread": TRANSMISSION_ERROR_VREAD},
    dict(POISON, keys=0x01, wram={wSerialFlags: b"\x2A", wDuelReturnAddress: b"\x00\xC3"},
         setup=TRANSMISSION_ERROR_SETUP,
         read=TRANSMISSION_ERROR_READ, vread=TRANSMISSION_ERROR_VREAD),
]
# <<< factory DuelTransmissionError

# >>> factory SerialRecv8Bytes
CONTRACT["SerialRecv8Bytes"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["SerialRecv8Bytes"] = [
	{"wram": {wSerialRecvCounter: b"\x08", wcba3: b"\x08", wSerialRecvBuf: b"\x01\x02\x03\x04\x05\x06\x07\x08"}, "read": {0xCBED: 8}},
	dict(POISON, wram={wSerialRecvCounter: b"\x08", wcba3: b"\x08", wSerialRecvBuf: b"\x11\x22\x33\x44\x55\x66\x77\x88", 0xCBED: b"\xff" * 8}, read={0xCBED: 8}),
	{"wram": {wSerialRecvCounter: b"\x0a", wcba3: b"\x0a", wSerialRecvBuf: b"\xf0\x81\x00\x7f\xff\x30\x0a\xc0"}, "read": {0xCBED: 8}},
]
# <<< factory SerialRecv8Bytes

# >>> factory ExchangeRNG
CONTRACT["ExchangeRNG"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ExchangeRNG"] = [
    {"wram": {0xCC09: b"\x00"}},
    {"wram": {0xCC09: b"\x02"}},
    {"wram": {0xCC09: b"\x11"}},
    dict(POISON, wram={0xCC09: b"\xff"}),
]
# <<< factory ExchangeRNG

# >>> factory SerialSend8Bytes
CONTRACT["SerialSend8Bytes"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["SerialSend8Bytes"] = [
    {"wram": {0xCBED: b"\x00" * 8}, "read": {0xCBED: 8}},
    dict(POISON, wram={0xCBED: b"\x5a" * 8}, read={0xCBED: 8}),
    {"a": 0x12, "f": 0x30, "b": 0x34, "c": 0x56, "d": 0x78, "e": 0x9A, "hl": 0xBCDE,
     "wram": {0xCBED: b"\xff" * 8}, "read": {0xCBED: 8}},
]
# <<< factory SerialSend8Bytes

# >>> factory LinkOpponentTurnFrameFunction
CONTRACT["LinkOpponentTurnFrameFunction"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["LinkOpponentTurnFrameFunction"] = [
    {"wram": {0xCB75: b"\x00"}},
    dict(POISON, wram={0xCB75: b"\x00"}),
    {"a": 0x5A, "hl": 0x4321, "wram": {0xCB75: b"\x00"}},
]
# <<< factory LinkOpponentTurnFrameFunction

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
hOppActionTableIndex = 0xFF9E
wDuelType = 0xCC09
wSerialFlags = 0xCB75
wSerialSendBufToggle = 0xCB7E
wSerialSendBufIndex = 0xCB7F
wcb80 = 0xCB80
wSerialSendBuf = 0xCB81

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory SetOppAction_SerialSendDuelData
CONTRACT["SetOppAction_SerialSendDuelData"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "hl"),
}
CASES["SetOppAction_SerialSendDuelData"] = [
    {"a": 0x37, "wram": {hWhoseTurn: b"\xC2", 0xC3F1: b"\x00"},
     "read": {hOppActionTableIndex: 1}},
    dict(POISON, a=0x37, wram={hWhoseTurn: b"\xC2", 0xC3F1: b"\x00",
                               hOppActionTableIndex: b"\xFF"},
         read={hOppActionTableIndex: 1}),
    {"a": 0x42, "wram": {hWhoseTurn: b"\xC2", 0xC3F1: b"\x01", wDuelType: b"\x00",
                         wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
                         wSerialFlags: b"\x00",
                         hOppActionTableIndex: b"\x00" * 10},
     "read": {hOppActionTableIndex: 10, wSerialSendBuf: 10,
              wSerialSendBufIndex: 1, wcb80: 1, wSerialSendBufToggle: 1}},
    dict(POISON, a=0x77,
         wram={hWhoseTurn: b"\xC2", 0xC3F1: b"\x01", wDuelType: b"\x00",
               wcb80: b"\x00", wSerialSendBufIndex: b"\x00",
               wSerialFlags: b"\x00", hOppActionTableIndex: b"\x00" * 10},
         read={hOppActionTableIndex: 10, wSerialSendBuf: 10,
               wSerialSendBufIndex: 1, wcb80: 1, wSerialSendBufToggle: 1}),
]
# <<< factory SetOppAction_SerialSendDuelData

# >>> factory SerialRecvDuelData
CONTRACT["SerialRecvDuelData"] = {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SerialRecvDuelData"] = [
    {"b": 0x12, "c": 0x34, "d": 0x56, "e": 0x78, "hl": 0x4321,
     "wram": {wDuelType: b"\x00", wSerialRecvCounter: b"\x0A", wcba3: b"\x00",
              wSerialRecvBuf: b"\x10\x20\x30\x40\x50\x60\x70\x80\x90\xA0", wSerialFlags: b"\x00"},
     "read": {hOppActionTableIndex: 10}},
    dict(POISON, wram={wDuelType: b"\x00", wSerialRecvCounter: b"\x0A", wcba3: b"\x00",
                       wSerialRecvBuf: b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A", wSerialFlags: b"\x00"},
         read={hOppActionTableIndex: 10}),
]
# <<< factory SerialRecvDuelData

# >>> factory UnreferencedGoToSerialReturnAddress
CONTRACT["UnreferencedGoToSerialReturnAddress"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UnreferencedGoToSerialReturnAddress"] = [{}, dict(POISON)]
# <<< factory UnreferencedGoToSerialReturnAddress

# >>> factory UnreferencedSaveSerialReturnAddress
CONTRACT["UnreferencedSaveSerialReturnAddress"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c")}
CASES["UnreferencedSaveSerialReturnAddress"] = [
    {"entry_sp": 0xFFFC, "wram": {0xCB79: b"\x00\x00", 0xCB7B: b"\x00\x00"}, "read": {0xCB79: 2, 0xCB7B: 2}},
    dict(POISON, entry_sp=0xFFFC, wram={0xCB79: b"\x00\x00", 0xCB7B: b"\x00\x00"}, read={0xCB79: 2, 0xCB7B: 2}),
]
# <<< factory UnreferencedSaveSerialReturnAddress

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SerialTimerHandler": {
        "source_symbol": "SerialTimerHandler",
        "before": "if (op == 0x29u)",
        "after":  "if (op == 0x28u)",
        "case_ids": ["SerialTimerHandler-0", "SerialTimerHandler-1", "SerialTimerHandler-2", "SerialTimerHandler-3", "SerialTimerHandler-4", "SerialTimerHandler-5", "SerialTimerHandler-6"],
    },
}
# >>> factory-mutation DuelTransmissionError
MUTATIONS["DuelTransmissionError"] = {
    "source_symbol": "DuelTransmissionError",
    "before": "gb_write8(wDuelResult_ADDR, (uint8_t)-1);",
    "after": "gb_write8(wDuelResult_ADDR, 0);",
    "case_ids": ["DuelTransmissionError-0", "DuelTransmissionError-1", "DuelTransmissionError-2"],
}
# <<< factory-mutation DuelTransmissionError
# >>> factory-completion DuelTransmissionError
# The asm tail (`ld sp, hl` then `ret`) never lands on a fixed address
# either oracle can arm as a sentinel -- it unwinds to whatever the real
# caller saved at wDuelReturnAddress. Stop at the `ret` opcode itself
# (poketcg.sym DuelTransmissionError+0x22) instead: every observable write
# has already happened by then, so wDuelReturnAddress only needs to be a
# safe scratch cell for PlaySong/ResetSerial's own call/ret pairs, not a
# real target.
for record in SCHEMA2_CASES["DuelTransmissionError"]:
    record["completion"] = {"mode": "pre-ret", "pc": DUEL_TRANSMISSION_ERROR_RET_PC}
# <<< factory-completion DuelTransmissionError
# >>> factory-mutation SerialRecv8Bytes
MUTATIONS["SerialRecv8Bytes"] = {
	"source_symbol": "SerialRecv8Bytes",
	"before": "SerialRecvBytes(wTempSerialBuf_ADDR, 0x0008u)",
	"after": "SerialRecvBytes(wTempSerialBuf_ADDR, 0x0007u)",
	"case_ids": ["SerialRecv8Bytes-0", "SerialRecv8Bytes-1", "SerialRecv8Bytes-2"],
}
# <<< factory-mutation SerialRecv8Bytes
# >>> factory-mutation ExchangeRNG
MUTATIONS["ExchangeRNG"] = {
    "source_symbol": "ExchangeRNG",
    "before": "\tif (a < DUELTYPE_LINK)\n\t\tf |= F_C;",
    "after": "\tif (a < DUELTYPE_LINK)\n\t\tf |= F_H;",
    "case_ids": ["ExchangeRNG-0"],
}
# <<< factory-mutation ExchangeRNG
# >>> factory-mutation SerialSend8Bytes
MUTATIONS["SerialSend8Bytes"] = {
    "source_symbol": "SerialSend8Bytes",
    "before": "\tif (r.a != DUELIST_TYPE_LINK_OPP)\n\t\treturn;",
    "after": "\tif (r.a == DUELIST_TYPE_LINK_OPP)\n\t\treturn;",
    "case_ids": ["SerialSend8Bytes-1", "SerialSend8Bytes-2"],
}
# <<< factory-mutation SerialSend8Bytes
# >>> factory-mutation LinkOpponentTurnFrameFunction
MUTATIONS["LinkOpponentTurnFrameFunction"] = {
    "source_symbol": "LinkOpponentTurnFrameFunction",
    "before": "\tif (wSerialFlags == 0u) {",
    "after": "\tif (wSerialFlags != 0u) {",
    "case_ids": ["LinkOpponentTurnFrameFunction-0", "LinkOpponentTurnFrameFunction-1", "LinkOpponentTurnFrameFunction-2"],
}
# <<< factory-mutation LinkOpponentTurnFrameFunction
# >>> factory-mutation SetOppAction_SerialSendDuelData
MUTATIONS["SetOppAction_SerialSendDuelData"] = {
    "source_symbol": "SetOppAction_SerialSendDuelData",
    "before": "SerialSendBytes(hOppActionTableIndex_ADDR, 10u);",
    "after": "SerialSendBytes(hOppActionTableIndex_ADDR, 9u);",
    "case_ids": ["SetOppAction_SerialSendDuelData-2", "SetOppAction_SerialSendDuelData-3"],
}
# <<< factory-mutation SetOppAction_SerialSendDuelData
# >>> factory-mutation SerialRecvDuelData
MUTATIONS["SerialRecvDuelData"] = {
    "source_symbol": "SerialRecvDuelData",
    "before": "SerialRecvBytes(0xFF9Eu, 10u);",
    "after": "SerialRecvBytes(0xFF9Eu, 9u);",
    "case_ids": ["SerialRecvDuelData-0"],
}
# <<< factory-mutation SerialRecvDuelData
# >>> factory-mutation UnreferencedGoToSerialReturnAddress
MUTATIONS["UnreferencedGoToSerialReturnAddress"] = {"source_symbol": "UnreferencedGoToSerialReturnAddress", "before": "\tif ((low | high) == 0u) {", "after": "\tif ((low | high) != 0u) {", "case_ids": ["UnreferencedGoToSerialReturnAddress-0", "UnreferencedGoToSerialReturnAddress-1"]}
# <<< factory-mutation UnreferencedGoToSerialReturnAddress
# >>> factory-mutation UnreferencedSaveSerialReturnAddress
MUTATIONS["UnreferencedSaveSerialReturnAddress"] = {"source_symbol": "UnreferencedSaveSerialReturnAddress", "before": "UnreferencedSaveSerialReturnAddressResult UnreferencedSaveSerialReturnAddress(void)\n{\n\tuint16_t entry_sp = 0xFFFCu;", "after": "UnreferencedSaveSerialReturnAddressResult UnreferencedSaveSerialReturnAddress(void)\n{\n\tuint16_t entry_sp = 0xFFFDu;", "case_ids": ["UnreferencedSaveSerialReturnAddress-0", "UnreferencedSaveSerialReturnAddress-1"]}
# <<< factory-mutation UnreferencedSaveSerialReturnAddress
