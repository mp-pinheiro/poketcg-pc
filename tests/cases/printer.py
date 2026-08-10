POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wPrinterPacketSequence = 0xCE63
wPrinterPacketDataSize = 0xCE68
wPrinterPacketDataPtr = 0xCE6A
wPrinterPacketChecksum = 0xCE6C
wSerialTransferData = 0xCE6E
wPrinterStatus = 0xCE6F
wSerialDataPtr = 0xCE70
rSC = 0xFF02
rIE = 0xFFFF

CONTRACT = {
    "SendNextPrinterPacketByte": ("b", "c", "d", "e"),
    "SendByteThroughSerialData": ("b", "c", "d", "e", "hl"),
    "ExecutePrinterPacketSequence": ("a", "b", "c", "d", "e"),
}

# pyboy's serial model hardcodes SB ($FF01) to always read back $FF
# ("Always 0xFF for a disconnected link cable", pyboy/core/serial.py), for
# both real ROM writes and case seeds -- confirmed empirically via
# ResetSerial's unconditional `xor a / ldh [rSB],a` still reading back $FF
# on the oracle. rSB is therefore never diffed via `read`, and any handler
# that reads rSB as data (.GetDeviceNumber, .GetStatusAndFinishSequence)
# always sees exactly $FF, never a seeded value.

CASES = {
    "SendNextPrinterPacketByte": [
        {"wram": {wSerialDataPtr: b"\x00\xC1", 0xC100: b"\x00",
                  wPrinterPacketChecksum: b"\x00\x00"},
         "read": {wSerialDataPtr: 2, wPrinterPacketChecksum: 2}},
        # Checksum low-byte carry into the high byte.
        dict(POISON, wram={wSerialDataPtr: b"\x00\xC1", 0xC100: b"\xFF",
                            wPrinterPacketChecksum: b"\x01\x05"},
             read={wPrinterPacketChecksum: 2}),
        # Pointer wraps $FFFF -> $0000; reads rIE as the "data byte".
        {"wram": {wSerialDataPtr: b"\xFF\xFF", rIE: b"\x77",
                  wPrinterPacketChecksum: b"\x00\x00"},
         "read": {wSerialDataPtr: 2, wPrinterPacketChecksum: 2}},
    ],

    "SendByteThroughSerialData": [
        {"a": 0, "read": {rSC: 1}},
        dict(POISON, read={rSC: 1}),
        {"a": 0xFF, "read": {rSC: 1}},
    ],

    # Real domain is a in [1,12] (SerialHandler only dispatches within that
    # range); a==0/>12 would index off the end of the jump table and is not
    # part of the callable contract.
    "ExecutePrinterPacketSequence": [
        # Preamble/header group (a in 1-5): send one byte, sequence += 1.
        {"a": 1, "wram": {wSerialDataPtr: b"\x00\xC1", 0xC100: b"\x55",
                           wPrinterPacketChecksum: b"\x00\x00",
                           wPrinterPacketSequence: b"\x01"},
         "read": {wPrinterPacketSequence: 1, wSerialDataPtr: 2}},
        {"a": 5, "wram": {wSerialDataPtr: b"\x10\xC1", 0xC110: b"\x66",
                           wPrinterPacketChecksum: b"\x00\x00",
                           wPrinterPacketSequence: b"\x05"},
         "read": {wPrinterPacketSequence: 1}},
        # a==6, dataSize==0: skips straight through to the checksum, three
        # sequence increments land it at 9. d/e preserved (no data-pointer
        # copy on this path).
        {"a": 6, "d": 0xDD, "e": 0xEE,
         "wram": {wPrinterPacketDataSize: b"\x00\x00", wPrinterPacketChecksum: b"\x22\x00",
                  wPrinterPacketSequence: b"\x06"},
         "read": {wPrinterPacketSequence: 1}},
        # a==6, dataSize==1: sends the one byte, sequence 6->7->8.
        {"a": 6, "wram": {wPrinterPacketDataSize: b"\x01\x00",
                           wPrinterPacketDataPtr: b"\x20\xC1", 0xC120: b"\x33",
                           wPrinterPacketChecksum: b"\x00\x00",
                           wPrinterPacketSequence: b"\x06"},
         "read": {wPrinterPacketSequence: 1, wSerialDataPtr: 2}},
        # a==7, dataSize==2: mid-data continuation, sequence does not advance.
        {"a": 7, "wram": {wPrinterPacketDataSize: b"\x02\x00",
                           wSerialDataPtr: b"\x30\xC1", 0xC130: b"\x44",
                           wPrinterPacketChecksum: b"\x00\x00",
                           wPrinterPacketSequence: b"\x07"},
         "read": {wPrinterPacketSequence: 1}},
        {"a": 8, "d": 0xDD, "e": 0xEE,
         "wram": {wPrinterPacketChecksum: b"\x11\x00", wPrinterPacketSequence: b"\x08"},
         "read": {wPrinterPacketSequence: 1}},
        {"a": 9, "d": 0xDD, "e": 0xEE,
         "wram": {wPrinterPacketChecksum: b"\x00\x22", wPrinterPacketSequence: b"\x09"},
         "read": {wPrinterPacketSequence: 1}},
        {"a": 10, "d": 0xDD, "e": 0xEE, "wram": {wPrinterPacketSequence: b"\x0A"},
         "read": {wPrinterPacketSequence: 1}},
        # a==11: rSB always reads $FF, so wSerialTransferData captures $FF.
        {"a": 11, "d": 0xDD, "e": 0xEE, "wram": {wPrinterPacketSequence: b"\x0B"},
         "setup": [{"fn": "SendByteThroughSerialData", "a": 0xFF}],
         "read": {wPrinterPacketSequence: 1, wSerialTransferData: 1}},
        # a==12: same rSB==$FF capture, into wPrinterStatus this time.
        {"a": 12, "d": 0xDD, "e": 0xEE, "wram": {wPrinterPacketSequence: b"\x0C"},
         "setup": [{"fn": "SendByteThroughSerialData", "a": 0xFF}],
         "read": {wPrinterPacketSequence: 1, wPrinterStatus: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
