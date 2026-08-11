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
rSB = 0xFF01

CONTRACT = {
    "SendNextPrinterPacketByte": {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c")},
    "SendByteThroughSerialData": ("b", "c", "d", "e", "hl"),
    "ExecutePrinterPacketSequence": {"compare": ("a", "b", "c", "d", "e"), "preserve": ("b", "c")},
}


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
        {"a": 11, "d": 0xDD, "e": 0xEE, "wram": {rSB: b"\xFF", wPrinterPacketSequence: b"\x0B"},
         "read": {wPrinterPacketSequence: 1, wSerialTransferData: 1}},
        {"a": 12, "d": 0xDD, "e": 0xEE, "wram": {rSB: b"\xFF", wPrinterPacketSequence: b"\x0C"},
         "read": {wPrinterPacketSequence: 1, wPrinterStatus: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SendByteThroughSerialData": {
        "source_symbol": "SendByteThroughSerialData",
        "before": "\tgb_write8(rSB, a);",
        "after": "\tgb_write8(rSB, (uint8_t)(a ^ 1u));",
        "case_ids": ["SendByteThroughSerialData-0", "SendByteThroughSerialData-1", "SendByteThroughSerialData-2"],
    },
    "ExecutePrinterPacketSequence": {
        "source_symbol": "ExecutePrinterPacketSequence",
        "before": "\t\tgb_write8(wSerialTransferData_ADDR, gb_read8(rSB));",
        "after": "\t\tgb_write8(wSerialTransferData_ADDR, (uint8_t)(gb_read8(rSB) ^ 0xFFu));",
        "case_ids": [
            "ExecutePrinterPacketSequence-0", "ExecutePrinterPacketSequence-1",
            "ExecutePrinterPacketSequence-2", "ExecutePrinterPacketSequence-3",
            "ExecutePrinterPacketSequence-4", "ExecutePrinterPacketSequence-5",
            "ExecutePrinterPacketSequence-6", "ExecutePrinterPacketSequence-7",
            "ExecutePrinterPacketSequence-8", "ExecutePrinterPacketSequence-9",
        ],
    },
}
