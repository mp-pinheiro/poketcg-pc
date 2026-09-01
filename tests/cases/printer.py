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
        {"a": 0, "read": {rSC: 1, wSerialTransferData: 1}},
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
# >>> factory-cases-statics
wce9d = 0xCE9D

SGFXBUFFER1 = 0xA400
SGFXBUFFER5 = 0xB400

wDefaultText = 0xC590
wPrintOnlyStarRarity = 0xCE9C
wPrinterCardCount = 0xCE91
wPrinterHorizontalOffset = 0xCE90
wPrinterTotalCardCount = 0xCE92

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wCardPageType = 0xCBD1
wLoadedCard1Type = 0xCC24

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wVBlankFunctionTrampoline = 0xCAD0
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]

wPrinterInitAttempts = 0xCE9E

wTxRam3 = 0xCE43

wPrinterStatus = 0xCE6F
wPrinterInitAttempts = 0xCE9E

# Shared seeds for the _PrintCardList cases: an empty card collection in SRAM
# bank 0 (0xA100 sCardCollection) plus four unnamed deck slots (0xA200 sDeck1Name,
# 0xA254 sDeck2Name, 0xA2A8 sDeck3Name, 0xA2FC sDeck4Name) so
# CreateTempCardCollection's .AddDeckCards passes over all four and leaves
# wTempCardCollection all zero on both sides.
_PRINT_CARD_LIST_SRAM = {0: {0xA100: b"\x00" * 0x100, 0xA200: b"\x00",
                             0xA254: b"\x00", 0xA2A8: b"\x00", 0xA2FC: b"\x00"}}
_PRINT_CARD_LIST_SETUP = [{"fn": "CopyDMAFunction"},
                          {"fn": "SetupText", "d": 0x20, "e": 0x40}]

# Shared seeds for the PrinterMenu_CardList cases: an empty card collection
# in SRAM bank 0 (0xA100 sCardCollection) plus an immediately terminated card
# list for each of the four built decks (0xA218 sDeck1Cards, 0xA26C
# sDeck2Cards, 0xA2C0 sDeck3Cards, 0xA314 sDeck4Cards), so
# CreateCardCollectionListWithDeckCards' ALL_DECKS pass ends at once and
# CreateFilteredCardList produces an empty visible list on both sides.
_PRINTER_MENU_CARD_LIST_SRAM = {0: {0xA100: b"\x00" * 0x100, 0xA218: b"\x00",
                                    0xA26C: b"\x00", 0xA2C0: b"\x00",
                                    0xA314: b"\x00"}}
_PRINTER_MENU_CARD_LIST_SETUP = [{"fn": "CopyDMAFunction"},
                                 {"fn": "SetupText", "d": 0x20, "e": 0x40}]

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hffb3 = 0xFFB3
sPrinterContrastLevel = 0xA003
wPrinterPacketDataPtr = 0xCE6A
wSelectedPrinterMenuItem = 0xCFE4
SETUP = [{"fn": "SetupRegisters"}, {"fn": "SetupText", "d": 0x30, "e": 0x7F}]
QUALITY_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory Func_1a14b
CONTRACT["Func_1a14b"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["Func_1a14b"] = [
    {"f": 0x00, "wram": {0xCE9D: b"\x00"}, "expect": {0xCE9D: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x10}},
    {"f": 0x80, "wram": {0xCE9D: b"\xFF"}, "expect": {0xCE9D: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x90}},
    dict(POISON, wram={0xCE9D: b"\x00"}, expect={0xCE9D: b"\x01"}, expect_regs={"a": 0x01, "f": 0x90, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory Func_1a14b

# >>> factory Func_1a025
CONTRACT["Func_1a025"] = {"compare": (), "preserve": (), "wram_out": True};
CASES["Func_1a025"] = [
    {"read": {0xCD06: 1, 0xCD07: 1}},
    dict(POISON, read={0xCD06: 1, 0xCD07: 1}),
]
# <<< factory Func_1a025

# >>> factory ResetPrinterCommunicationSettings
CONTRACT["ResetPrinterCommunicationSettings"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c"), "wram_out": True}
CASES["ResetPrinterCommunicationSettings"] = [
    {"wram": {0xCE8F: b"\x01"}, "read": {0xCE8F: 1, 0xCD04: 1, 0xCD06: 1, 0xCD07: 1, 0xCD0A: 1, 0xCD0B: 1, 0xC600: 256, 0xFF81: 1, 0xFFA8: 1, 0xFFA9: 1, 0xFFAF: 1, 0xFFB0: 1}},
    dict(POISON, wram={0xCE8F: b"\x02"}, read={0xCE8F: 1, 0xCD04: 1, 0xCD06: 1, 0xCD07: 1, 0xCD0A: 1, 0xCD0B: 1, 0xC600: 256, 0xFF81: 1, 0xFFA8: 1, 0xFFA9: 1, 0xFFAF: 1, 0xFFB0: 1}),
]
# <<< factory ResetPrinterCommunicationSettings

# >>> factory ClearPrinterGfxBuffer
CONTRACT["ClearPrinterGfxBuffer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e"), "wram_out": True}
CASES["ClearPrinterGfxBuffer"] = [
    {"wram": {0xCE9F: b"\x55"}, "sram": {0: {0xA000: b"\xAA" * 0x400}}, "expect": {0xCE9F: b"\x00"}, "expect_sram": {0: {0xA000: b"\x00" * 0x400}}},
    dict(POISON, wram={0xCE9F: b"\xFF"}, sram={0: {0xA000: b"\xAA" * 0x400}}, expect={0xCE9F: b"\x00"}, expect_sram={0: {0xA000: b"\x00" * 0x400}}),
]
# <<< factory ClearPrinterGfxBuffer

# >>> factory GetPrinterContrastSerialData
CONTRACT["GetPrinterContrastSerialData"] = {"compare": ("a", "hl"), "preserve": ()}
CASES["GetPrinterContrastSerialData"] = [
    {"wram": {0xCE99: b"\x00"}},
    dict(POISON, wram={0xCE99: b"\x02"}),
]
# <<< factory GetPrinterContrastSerialData

# >>> factory PrepareForPrinterCommunications
CONTRACT["PrepareForPrinterCommunications"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["PrepareForPrinterCommunications"] = [
    {"wram": {0xFF81: b"\x00"}, "sram": {0: {0xA003: b"\x2A"}}, "read": {0xCE99: 1, 0xCE9B: 1, 0xCE8F: 1, 0xFF81: 1}},
    dict(POISON, wram={0xFF81: b"\x00"}, sram={0: {0xA003: b"\x2A"}}, read={0xCE99: 1, 0xCE9B: 1, 0xCE8F: 1, 0xFF81: 1}),
]
# <<< factory PrepareForPrinterCommunications

# >>> factory CheckDataCompression
CONTRACT["CheckDataCompression"] = {"compare": ("a", "e", "f", "hl"), "preserve": ()}
CASES["CheckDataCompression"] = [
    {"c": 0x06, "hl": 0xC500, "wram": {0xC500: bytes([1, 1, 1, 1, 5, 6])}},
    dict(POISON, c=0x04, hl=0xC500, wram={0xC500: bytes([1, 2, 3, 4])}),
]
# <<< factory CheckDataCompression

# >>> factory CompressDataForPrinterSerialTransfer
CONTRACT["CompressDataForPrinterSerialTransfer"] = {"compare": ("b", "c", "hl", "d", "e"), "preserve": ()}
CASES["CompressDataForPrinterSerialTransfer"] = [
    {"sram": {0: {SGFXBUFFER5: b"\x00" * 0x280}}, "ramg": True, "sread": {0: {SGFXBUFFER5 + 0x280: 0x280}}},
    dict(POISON, sram={0: {SGFXBUFFER5: b"\x00" * 0x280}}, ramg=True, sread={0: {SGFXBUFFER5 + 0x280: 0x280}}),
]
# <<< factory CompressDataForPrinterSerialTransfer

# >>> factory LoadCardInfoForPrinter
CONTRACT["LoadCardInfoForPrinter"] = {"compare": ("hl",), "preserve": ("hl",), "wram_out": True}
CASES["LoadCardInfoForPrinter"] = [
    {"b": 0x00, "c": 0x00, "wram": {wDefaultText: b"\x00" * 16, wPrintOnlyStarRarity: b"\x00", wPrinterCardCount: b"\x00", wPrinterHorizontalOffset: b"\x00", wPrinterTotalCardCount: b"\x00\x00"}, "read": {wDefaultText: 16, wPrintOnlyStarRarity: 1, wPrinterCardCount: 1, wPrinterHorizontalOffset: 1, wPrinterTotalCardCount: 2}, "vread": {0: {0x9800: 0x400, 0x9C00: 0x400}}, "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, b=0x00, c=0x00, wram={wDefaultText: b"\x00" * 16, wPrintOnlyStarRarity: b"\x00", wPrinterCardCount: b"\x01", wPrinterHorizontalOffset: b"\x02", wPrinterTotalCardCount: b"\x01\x00"}, read={wDefaultText: 16, wPrintOnlyStarRarity: 1, wPrinterCardCount: 1, wPrinterHorizontalOffset: 1, wPrinterTotalCardCount: 2}, vread={0: {0x9800: 0x400, 0x9C00: 0x400}}, instruction_budget=4000000, cycle_budget=16000000),
]
# <<< factory LoadCardInfoForPrinter

# >>> factory PrinterMenu_QuitPrint
CONTRACT["PrinterMenu_QuitPrint"] = {"compare": ("f",), "preserve": ()}
CASES["PrinterMenu_QuitPrint"] = [
    {"stack": [0], "wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "stack": [0x1234], "wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "keys": [0x00, 0x01], "instruction_budget": 20000000, "cycle_budget": 100000000}
]
# <<< factory PrinterMenu_QuitPrint

# >>> factory DrawBottomCardInfoInSRAMGfxBuffer0
CONTRACT["DrawBottomCardInfoInSRAMGfxBuffer0"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DrawBottomCardInfoInSRAMGfxBuffer0"] = [
    {"wram": {wLoadedCard1Type: b"\x08"}, "read": {wCardPageType: 1}},
    dict(POISON, wram={wLoadedCard1Type: b"\x08"}, read={wCardPageType: 1}),
]
# <<< factory DrawBottomCardInfoInSRAMGfxBuffer0

# >>> factory ShowPrinterTransmitting
CONTRACT["ShowPrinterTransmitting"] = {"compare": (), "preserve": ()}
CASES["ShowPrinterTransmitting"] = [
    {"wram": {0xCABB: b"\x00", wVBlankFunctionTrampoline: b"\x00\x00\x00"},
     "sram": {0: {}}, "setup": SETUP,
     "read": {wVBlankFunctionTrampoline: 3},
     "instruction_budget": 8000000, "cycle_budget": 32000000},
    dict(POISON,
         wram={0xCABB: b"\x00", wVBlankFunctionTrampoline: b"\x00\x00\x00"},
         sram={0: {}}, setup=SETUP,
         read={wVBlankFunctionTrampoline: 3},
         instruction_budget=8000000, cycle_budget=32000000),
]
# <<< factory ShowPrinterTransmitting

# >>> factory SendPrinterPacket
CONTRACT["SendPrinterPacket"] = {"compare": (), "preserve": ()}
CASES["SendPrinterPacket"] = [
    {"b": 0x00, "c": 0x00, "d": 0x12, "e": 0x34, "hl": 0xC500,
     "wram": {0xC500: b"\x00", wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
     "read": {wPrinterPacketSequence: 15}, "expect": {wPrinterPacketSequence: b"\x00\x88\x33\x12\x34\x00\x00\x00\xC5\x46\x00\x81\x00\x6A\xCE"},
     "expect_regs": {"a": 0x00, "f": 0x80}, "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
    {"b": 0x00, "c": 0x00, "d": 0x12, "e": 0x34, "hl": 0xC500,
     "wram": {0xC500: b"\x00", wSerialTransferData: b"\x42", wPrinterStatus: b"\x00"},
     "read": {wPrinterPacketSequence: 15}, "expect": {wPrinterPacketSequence: b"\x00\x88\x33\x12\x34\x00\x00\x00\xC5\x46\x00\x42\xFF\x6A\xCE"},
     "expect_regs": {"a": 0xFF, "f": 0x10}, "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
    dict(POISON, b=0x00, c=0x00, d=0x12, e=0x34, hl=0xC500,
         wram={0xC500: b"\x00", wSerialTransferData: b"\x81", wPrinterStatus: b"\xF0"},
         read={wPrinterPacketSequence: 15}, expect={wPrinterPacketSequence: b"\x00\x88\x33\x12\x34\x00\x00\x00\xC5\x46\x00\x81\xF0\x6A\xCE"},
         expect_regs={"a": 0xF0, "f": 0x10}, oracle=False, evidence="intentional-transform",
         why="PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"),
    {"b": 0x00, "c": 0x00, "d": 0x12, "e": 0x34, "hl": 0xC500,
     "wram": {0xC500: b"\x00", wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
     "read": {0xCE64: 8}, "instruction_budget": 2000000, "cycle_budget": 8000000},
]
# <<< factory SendPrinterPacket

# >>> factory SendTilesToPrinter
CONTRACT["SendTilesToPrinter"] = {"compare": (), "preserve": ()}
# 64 map entries naming 52 distinct tiles; sGfxBuffer1 seeds tile i as 16
# bytes of i, so both the row stride (32: 20 read, 12 skipped) and the tile
# resolution are observable in the staged buffer and its compressed output.
_SENDTILES_MAP = bytes(range(64))
_SENDTILES_GFX = b"".join(bytes([i]) * 16 for i in range(52))
_SENDTILES_SR = {0: {SGFXBUFFER1: _SENDTILES_GFX}}
_SENDTILES_STAGED = b"".join(bytes([i]) * 16 for i in list(range(20)) + list(range(32, 52)))
_SENDTILES_COMPRESSED = bytes.fromhex("8e008e018e028e038e048e058e068e078e088e098e0a8e0b8e0c8e0d8e0e8e0f8e108e118e128e138e208e218e228e238e248e258e268e278e288e298e2a8e2b8e2c8e2d8e2e8e2f8e308e318e328e33")
CASES["SendTilesToPrinter"] = [
    {"hl": 0xC500,
     "wram": {0xC500: _SENDTILES_MAP, wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
     "sram": _SENDTILES_SR, "ramg": True,
     "expect": {0xCE64: b"\x88\x33\x04\x01\x00\x00\x80\xB6"},
     "expect_regs": {"a": 0x00, "f": 0x80, "hl": 0xC540},
     "expect_sram": {0: {SGFXBUFFER5: _SENDTILES_STAGED, SGFXBUFFER5 + 0x280: _SENDTILES_COMPRESSED}},
     "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
    dict(POISON, hl=0xC500,
         wram={0xC500: _SENDTILES_MAP, wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
         sram=_SENDTILES_SR, ramg=True,
         expect={0xCE64: b"\x88\x33\x04\x01\x00\x00\x80\xB6"},
         expect_regs={"a": 0x00, "f": 0x80, "hl": 0xC540},
         expect_sram={0: {SGFXBUFFER5: _SENDTILES_STAGED, SGFXBUFFER5 + 0x280: _SENDTILES_COMPRESSED}},
         oracle=False, evidence="intentional-transform",
         why="PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"),
    {"hl": 0xC500,
     "wram": {0xC500: _SENDTILES_MAP, wSerialTransferData: b"\x42", wPrinterStatus: b"\x00"},
     "sram": _SENDTILES_SR, "ramg": True,
     "expect": {0xCE64: b"\x88\x33\x04\x01\x00\x00\x80\xB6"},
     "expect_regs": {"a": 0xFF, "f": 0x10, "hl": 0xC540},
     "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
    {"hl": 0xC500,
     "wram": {0xC500: _SENDTILES_MAP, wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
     "sram": _SENDTILES_SR, "ramg": True,
     "sread": {0: {SGFXBUFFER5: 0x280, SGFXBUFFER5 + 0x280: 0x50}},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
]
# <<< factory SendTilesToPrinter

# >>> factory ShowPrinterConnectionErrorScene
CONTRACT["ShowPrinterConnectionErrorScene"] = {"compare": ("f",), "preserve": ()}
CASES["ShowPrinterConnectionErrorScene"] = [
    {"a": 0x02, "hl": 0x0120, "keys": [0, 1],
     "wram": {0xCABB: b"\x00"},
     "setup": [{"fn": "SetupRegisters"}, {"fn": "SetupText", "d": 0x30, "e": 0x7F}],
     "read": {0xCE43: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, a=0x02, hl=0x0120, keys=[0, 1],
         wram={0xCABB: b"\x00"},
         setup=[{"fn": "SetupRegisters"}, {"fn": "SetupText", "d": 0x30, "e": 0x7F}],
         read={0xCE43: 2},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ShowPrinterConnectionErrorScene

# >>> factory TryInitPrinterCommunications
CONTRACT["TryInitPrinterCommunications"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TryInitPrinterCommunications"] = [
    # B held on the first frame is the only exit the real ROM reaches: every
    # packet path parks it inside SendPrinterPacket's transmission wait
    # because the oracles never complete a serial transfer.
    {"keys": [0x02], "wram": {wPrinterStatus: b"\x77", wPrinterInitAttempts: b"\xAA"},
     "read": {wPrinterStatus: 1, wPrinterInitAttempts: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=[0x02],
         wram={wPrinterStatus: b"\xAA", wPrinterInitAttempts: b"\x55"},
         read={wPrinterStatus: 1, wPrinterInitAttempts: 1},
         instruction_budget=2000000, cycle_budget=8000000),
    {"wram": {wSerialTransferData: b"\x81", wPrinterStatus: b"\x00", wPrinterInitAttempts: b"\xFF"},
     "expect": {wPrinterStatus: b"\x00", wPrinterInitAttempts: b"\x00"},
     "expect_regs": {"a": 0x00, "f": 0x80},
     "oracle": False, "evidence": "intentional-transform",
     "why": "an idle printer lets the NUL probe fall straight through to the INIT packet, which the PC runtime's synchronous packet engine answers without carry"},
    {"wram": {wSerialTransferData: b"\x81", wPrinterStatus: b"\x04"},
     "expect": {wPrinterStatus: b"\x04", wPrinterInitAttempts: b"\x00"},
     "expect_regs": {"a": 0x04, "f": 0x80},
     "oracle": False, "evidence": "intentional-transform",
     "why": "a status byte outside the error nibble and the busy bits rides out unchanged through the successful INIT packet"},
    {"wram": {wSerialTransferData: b"\x42", wPrinterStatus: b"\x00"},
     "expect": {wPrinterStatus: b"\xFF", wPrinterInitAttempts: b"\x03"},
     "expect_regs": {"a": 0x03, "f": 0x90},
     "oracle": False, "evidence": "intentional-transform",
     "why": "the wrong device number fails every packet, so the delay and retry ladder climbs to the three-attempt time-out that the parked reference can never reach"},
    {"keys": [0x00, 0x02],
     "wram": {wSerialTransferData: b"\x81", wPrinterStatus: b"\x0A"},
     "expect": {wPrinterStatus: b"\x00", wPrinterInitAttempts: b"\x00"},
     "expect_regs": {"a": 0x00, "f": 0x90},
     "oracle": False, "evidence": "intentional-transform",
     "why": "the busy bits keep the port polling DoFrame until B is held on the second frame, which aborts with carry"},
]
# <<< factory TryInitPrinterCommunications

# >>> factory ShowPrinterIsNotConnected
CONTRACT["ShowPrinterIsNotConnected"] = {"compare": ("f",), "preserve": ()}
CASES["ShowPrinterIsNotConnected"] = [
    {"keys": [0, 1],
     "wram": {0xCABB: b"\x00"},
     "setup": [{"fn": "SetupRegisters"}, {"fn": "SetupText", "d": 0x30, "e": 0x7F}],
     "read": {0xCE43: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0, 1],
         wram={0xCABB: b"\x00"},
         setup=[{"fn": "SetupRegisters"}, {"fn": "SetupText", "d": 0x30, "e": 0x7F}],
         read={0xCE43: 2},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ShowPrinterIsNotConnected

# >>> factory HandlePrinterError
CONTRACT["HandlePrinterError"] = {"compare": ("f",), "preserve": ()}
CASES["HandlePrinterError"] = [
    {"wram": {wPrinterStatus: b"\x00", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "read": {wTxRam3: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wPrinterStatus: b"\xFF", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "read": {wTxRam3: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wPrinterStatus: b"\x80", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "read": {wTxRam3: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wPrinterStatus: b"\x40", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "read": {wTxRam3: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wPrinterStatus: b"\x20", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "read": {wTxRam3: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wPrinterStatus: b"\x01", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": [0x00, 0x01], "read": {wTxRam3: 2},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, wram={wPrinterStatus: b"\x01", 0xCE43: b"\xAA\x55", 0xCABB: b"\x80", 0xFF40: b"\x80"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=[0x00, 0x01], read={wTxRam3: 2},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory HandlePrinterError

# >>> factory SendPrinterInstructionPacket
CONTRACT["SendPrinterInstructionPacket"] = {"compare": (), "preserve": ()}
CASES["SendPrinterInstructionPacket"] = [
    {"hl": 0xC100, "stack": [0xC100],
     "wram": {0xC100: b"\x00\x00\x00\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "read": {0xCE6A: 2}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, stack=[0x1234],
         wram={0xCE6E: b"\x81", 0xCE6F: b"\x00"},
         read={0xCE6A: 2}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory SendPrinterInstructionPacket

# >>> factory SendPrinterInstructionPacket_1Sheet
# The reference never returns from here: SendPrinterPacket parks in its
# .wait_printer_packet_transmission DoFrame loop ($315D) because no printer
# hardware raises the serial interrupt that advances wPrinterPacketSequence.
# Completion is therefore declared pre-ret at that loop head, exactly as the
# already-landed SendPrinterInstructionPacket cases do, so the reference stops
# inside the first packet. Only bytes that agree between that stop and the
# port's fully synchronous run are observed: wPrinterNumberLineFeeds (this
# routine's own write, zero on both sides), wPrinterContrastLevel (read, never
# written), and the seeded device/status bytes the port's state machine writes
# back unchanged. Registers are mid-flight on the reference, so nothing is
# compared; the packet buffer diverges after the second packet and is not read.
CONTRACT["SendPrinterInstructionPacket_1Sheet"] = {"compare": (), "preserve": ()}
CASES["SendPrinterInstructionPacket_1Sheet"] = [
    {"wram": {0xCE99: b"\x00", 0xCE9B: b"\x23", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "read": {0xCE9B: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON,
         wram={0xCE99: b"\x02", 0xCE9B: b"\x45", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
         read={0xCE9B: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory SendPrinterInstructionPacket_1Sheet

# >>> factory SendPrinterInstructionPacket_1Sheet_3LineFeeds
# Same wait shape as SendPrinterInstructionPacket_1Sheet above: the reference
# parks in SendPrinterPacket's DoFrame loop ($315D) and completion is declared
# pre-ret there. This routine writes nothing of its own (the line-feed count
# is the constant $0301, not a wPrinterNumberLineFeeds read), so the primary
# cases observe only the contrast seed; the synchronous port's full run is
# checked by the intentional-transform case below, whose exit hl is the
# contrast word (level 0 -> $00E4, level 2 -> $40E4) and whose packet staging
# carries the second packet's PRINT_INSTRUCTION bytes.
CONTRACT["SendPrinterInstructionPacket_1Sheet_3LineFeeds"] = {"compare": (), "preserve": ()}
CASES["SendPrinterInstructionPacket_1Sheet_3LineFeeds"] = [
    {"wram": {0xCE99: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "read": {0xCE99: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON,
         wram={0xCE99: b"\x02", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
         read={0xCE99: 1},
         instruction_budget=2000000, cycle_budget=8000000),
    {"wram": {0xCE99: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "read": {0xCE6B: 2},
     "expect_regs": {"a": 0x00, "f": 0x80, "hl": 0x00E4},
     "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
]
# <<< factory SendPrinterInstructionPacket_1Sheet_3LineFeeds

# >>> factory LoadGfxBufferForPrinter
# The B-exit primary case is the one path the real ROM finishes: TryInitPrinter
# Communications returns carry with B held, before any packet parks in the
# $315D transmission wait. The success path runs 10 synchronous packets on the
# port only (transform case below); its final state is the offset reset to 1
# with a=1, f=0x00 (`ld a, 1` / `or a`).
CONTRACT["LoadGfxBufferForPrinter"] = {"compare": ("a", "f", "hl"), "preserve": ("hl",)}
CASES["LoadGfxBufferForPrinter"] = [
    {"hl": 0xBEEF, "keys": [0x02],
     "wram": {0xCE90: b"\x14", 0xCE6F: b"\x77", 0xCE9B: b"\xAA"},
     "read": {0xCE90: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0xBEEF, keys=[0x02],
         wram={0xCE90: b"\x14", 0xCE6F: b"\x77", 0xCE9B: b"\xAA"},
         read={0xCE90: 1},
         instruction_budget=2000000, cycle_budget=8000000),
    {"hl": 0xBEEF,
     "wram": {0xCE90: b"\x14", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "sram": {0: {0xA000: bytes([1] * 64), 0xA410: b"\xab" * 16}}, "ramg": True,
     "read": {0xCE90: 1},
     "expect": {0xCE90: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x00},
     "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
]
# <<< factory LoadGfxBufferForPrinter

# >>> factory AddToPrinterGfxBuffer
# Below 18 the routine is pure arithmetic and returns fully on both backends;
# case 1 covers the H-flag shape ((offset & $0F) < 2). Case 2 crosses the
# boundary with B held, so the fallthrough continuation exits through
# TryInitPrinterCommunications' carry before any packet wait.
CONTRACT["AddToPrinterGfxBuffer"] = {"compare": ("a", "hl"), "preserve": ("hl",)}
CASES["AddToPrinterGfxBuffer"] = [
    {"hl": 0xBEEF, "wram": {0xCE90: b"\x0A"}, "read": {0xCE90: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0xBEEF, wram={0xCE90: b"\x0E"}, read={0xCE90: 1},
         instruction_budget=2000000, cycle_budget=8000000),
    {"hl": 0xBEEF, "keys": [0x02],
     "wram": {0xCE90: b"\x12", 0xCE6F: b"\x77", 0xCE9B: b"\xAA"},
     "read": {0xCE90: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"hl": 0xBEEF,
     "wram": {0xCE90: b"\x11", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "sram": {0: {0xA000: bytes([1] * 64), 0xA410: b"\xab" * 16}}, "ramg": True,
     "read": {0xCE90: 1},
     "expect": {0xCE90: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x00},
     "oracle": False, "evidence": "intentional-transform",
     "why": "PC runtime executes the verified printer state machine synchronously because no Game Boy Printer hardware raises serial interrupts"},
]
# <<< factory AddToPrinterGfxBuffer

# >>> factory _PreparePrinterConnection
# The reference never returns from here: SendPrinterPacket parks in its
# .wait_printer_packet_transmission DoFrame loop ($315D) because no printer
# hardware raises the serial interrupt that advances wPrinterPacketSequence.
# A previous attempt without that split died BUDGET_EXHAUSTED with pc inside
# DoFrame ($056F) after 7.1M instructions -- the genuine spin, not a small
# budget. Completion is therefore declared pre-ret at that loop head, exactly
# as the landed SendPrinterInstructionPacket cases do, so the reference stops
# inside the packet this routine sends.
#
# Registers are mid-flight on the reference, so nothing is compared. The
# observed bytes are the ones both sides agree on: wPrinterPacketDataPtr, which
# SendPrinterPacket writes from hl before the wait and neither side rewrites,
# plus the two seeded serial bytes. $81 is the device number the packet engine
# expects, so the port's synchronous state machine writes it straight back, and
# a zero status clears the error nibble, so the port takes the `ret nc` exit
# without touching wPrinterStatus again -- no scene, no text box, no frames.
CONTRACT["_PreparePrinterConnection"] = {"compare": (), "preserve": ()}
CASES["_PreparePrinterConnection"] = [
    {"hl": 0xC100,
     "wram": {wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
     "read": {wPrinterPacketDataPtr: 2},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON,
         wram={wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
         read={wPrinterPacketDataPtr: 2},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory _PreparePrinterConnection

# >>> factory SendCardListToPrinter
CONTRACT["SendCardListToPrinter"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["SendCardListToPrinter"] = [
    {"keys": [0x02],
     "wram": {0xCE90: b"\x01", 0xCE6F: b"\x77", 0xCE9E: b"\xAA"},
     "read": {0xCE90: 1, 0xCE6F: 1, 0xCE9E: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"keys": [0x02],
     "wram": {0xCE90: b"\x00", 0xCE6F: b"\x55", 0xCE9E: b"\xCC"},
     "read": {0xCE90: 1, 0xCE6F: 1, 0xCE9E: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=[0x02],
         wram={0xCE90: b"\x00", 0xCE6F: b"\xAA", 0xCE9E: b"\x55"},
         read={0xCE90: 1, 0xCE6F: 1, 0xCE9E: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory SendCardListToPrinter

# >>> factory Func_19f87
CONTRACT["Func_19f87"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_19f87"] = [
    {"keys": [0x02], "wram": {wPrinterStatus: b"\x77", wPrinterInitAttempts: b"\xAA"},
     "read": {wPrinterStatus: 1, wPrinterInitAttempts: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=[0x02],
         wram={wPrinterStatus: b"\xAA", wPrinterInitAttempts: b"\x55"},
         read={wPrinterStatus: 1, wPrinterInitAttempts: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_19f87

# >>> factory Func_1a011
CONTRACT["Func_1a011"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_1a011"] = [
    {"keys": [0x02], "wram": {wPrinterStatus: b"\x77", wPrinterInitAttempts: b"\xAA"},
     "read": {wPrinterStatus: 1, wPrinterInitAttempts: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=[0x02],
         wram={wPrinterStatus: b"\xAA", wPrinterInitAttempts: b"\x55"},
         read={wPrinterStatus: 1, wPrinterInitAttempts: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_1a011

# >>> factory Func_19f99
CONTRACT["Func_19f99"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_19f99"] = [
    {"keys": [0x02],
     "wram": {0xCE6F: b"\x77", 0xCE9E: b"\xAA"},
     "read": {0xCE6F: 1, 0xCE9E: 1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=[0x02],
         wram={0xCE6F: b"\xAA", 0xCE9E: b"\x55"},
         read={0xCE6F: 1, 0xCE9E: 1},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_19f99

# >>> factory _PrintDeckConfiguration
CONTRACT["_PrintDeckConfiguration"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["_PrintDeckConfiguration"] = [
    {"a": 0x00,
     "wram": {0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00", 0xCE92: b"\xFF\xFF", 0xCE9C: b"\xFF", 0xCF17: b"\x00"},
     "sram": {0: {0xA350: b"\x00" * 0x53 + b"\xA5"}},
     "ramg": True,
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": 0x00,
     "read": {0xC510: 0x54, 0xCE92: 2, 0xCE9C: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, a=0x00,
         wram={0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00", 0xCE92: b"\xFF\xFF", 0xCE9C: b"\xFF", 0xCF17: b"\x00"},
         sram={0: {0xA350: b"\x00" * 0x53 + b"\xA5"}}, ramg=True,
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=0x00, read={0xC510: 0x54, 0xCE92: 2, 0xCE9C: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _PrintDeckConfiguration

# >>> factory Func_1a080
# The reference never returns from here: SendPrinterPacket parks in its
# .wait_printer_packet_transmission DoFrame loop ($315D, poketcg.sym) because
# no printer hardware raises the serial interrupt that advances
# wPrinterPacketSequence. The previous attempt without that split died
# BUDGET_EXHAUSTED with pc inside DoFrame ($0505) after 710729 instructions --
# the genuine spin, not a small budget -- so completion is declared pre-ret at
# that loop head, exactly as the landed _PreparePrinterConnection cases do.
#
# Registers are mid-flight on the reference, so nothing is compared. The
# observed byte is wPrinterPacketDataPtr, which SendPrinterPacket writes from
# the entry hl before the wait and neither side rewrites. $81 is the device
# number the packet engine expects, so the port's synchronous state machine
# writes it straight back, and a zero status keeps the port off any error path,
# so both seeded serial bytes agree at the stop.
CONTRACT["Func_1a080"] = {"compare": (), "preserve": ()}
CASES["Func_1a080"] = [
    {"hl": 0xC100,
     "wram": {wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
     "read": {wPrinterPacketDataPtr: 2},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON,
         wram={wSerialTransferData: b"\x81", wPrinterStatus: b"\x00"},
         read={wPrinterPacketDataPtr: 2},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory Func_1a080

# >>> factory _RequestToPrintCard
# The reference never returns from here: Func_19f87 reaches
# TryInitPrinterCommunications, whose first packet parks in SendPrinterPacket's
# .wait_printer_packet_transmission DoFrame loop ($315D) because no printer
# hardware raises the serial interrupt that advances wPrinterPacketSequence.
# Completion is therefore declared pre-ret at that loop head, exactly as the
# landed _PrintDeckConfiguration cases do, so the reference stops inside the
# first packet -- after the card data load and the whole sGfxBuffer0 drawing
# pass, which is what these cases observe.
#
# Registers are mid-flight on the reference, so nothing is compared. The
# observed bytes are wLoadedCard1's type/gfx/name/HP/level, which
# LoadCardDataToBuffer1_FromCardID writes from the entry card id at the very
# first instruction and which nothing on either side rewrites afterwards. The
# seeded serial bytes agree too: $81 is the device number the port's
# synchronous packet engine writes straight back, and a zero status keeps it
# off every error path. wLCDC starts clear so the text box before EnableLCD
# stays out of WaitForVBlank's halt; CopyDMAFunction installs hDMAFunction for
# the frames that elapse after EnableLCD.
CONTRACT["_RequestToPrintCard"] = {"compare": (), "preserve": ()}
CASES["_RequestToPrintCard"] = [
    {"a": 0x01,
     "wram": {0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
     "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "keys": 0x00,
     "read": {0xCC24: 5, 0xCC2C: 1, 0xCC5D: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00"},
         setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
         keys=0x00,
         read={0xCC24: 5, 0xCC2C: 1, 0xCC5D: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _RequestToPrintCard

# >>> factory _PrintCardList
# The reference never returns from here. The card loop reaches its seventh new
# card type with wPrinterHorizontalOffset at 19, so AddToPrinterGfxBuffer falls
# into LoadGfxBufferForPrinter, whose TryInitPrinterCommunications parks in
# SendPrinterPacket's .wait_printer_packet_transmission DoFrame loop ($315D)
# because no printer hardware raises the serial interrupt that advances
# wPrinterPacketSequence. Completion is therefore declared pre-ret at that loop
# head, exactly as the landed _PrintDeckConfiguration and _RequestToPrintCard
# cases do.
#
# Registers are mid-flight on the reference, so nothing is compared. The
# observed bytes are the ones this routine writes before that stop and never
# rewrites afterwards, so the port's full run agrees with the reference's
# partial one:
#   $FF97 hWhoseTurn            - PLAYER_TURN, written once before the loop
#   $CE91 wPrinterCardCount     - the collection slot of the card being
#                                 examined; the seeded collection is empty, so
#                                 every iteration writes 0 on both sides
#   $CE92 wPrinterTotalCardCount - zeroed before the loop and only advanced by
#                                 owned cards, of which there are none
#   $CE97 wPrinterNumCardTypes  - same, and only on the all-owned path
#   $CE9C wPrintOnlyStarRarity  - the SELECT decision, written once at entry
# Every one of those is seeded to $FF first so the write itself is witnessed.
# wCurPrinterCardType ($CE94) and wPrinterHorizontalOffset ($CE90) are NOT
# observed: they keep moving past the reference's stop.
#
# wLCDC starts clear so the text boxes before ShowPrinterTransmitting's
# EnableLCD stay out of WaitForVBlank's halt; CopyDMAFunction installs
# hDMAFunction for the frames that elapse afterwards and SetupText primes the
# glyph cache. $81 in wSerialTransferData is the device number the port's
# synchronous packet engine writes straight back, and a zero wPrinterStatus
# keeps both sides off every error path.
#
# Case 1 holds SELECT for the whole run and so takes the star-rarity branch.
# hKeysHeld is seeded because the routine reads it before the first DoFrame,
# and keys=0x04 makes the reference's own joypad read write that same $04 back,
# so the seeded byte still matches at the stop. wPrinterNumCardTypes is not
# observed there: star mode advances it per printed card, so it is still moving
# when the reference parks.
CONTRACT["_PrintCardList"] = {"compare": (), "preserve": ()}
CASES["_PrintCardList"] = [
    {"wram": {0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00",
              0xCE91: b"\xFF", 0xCE92: b"\xFF\xFF", 0xCE97: b"\xFF",
              0xCE9C: b"\xFF", 0xFF90: b"\x00", 0xFF97: b"\x00"},
     "sram": _PRINT_CARD_LIST_SRAM,
     "ramg": True,
     "setup": _PRINT_CARD_LIST_SETUP,
     "keys": 0x00,
     "read": {0xCE91: 1, 0xCE92: 2, 0xCE97: 1, 0xCE9C: 1, 0xFF97: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={0xCABB: b"\x00", 0xCE6E: b"\x81", 0xCE6F: b"\x00",
               0xCE91: b"\xFF", 0xCE92: b"\xFF\xFF", 0xCE9C: b"\xFF",
               0xFF90: b"\x04", 0xFF97: b"\x00"},
         sram=_PRINT_CARD_LIST_SRAM,
         ramg=True,
         setup=_PRINT_CARD_LIST_SETUP,
         keys=0x04,
         read={0xCE91: 1, 0xCE92: 2, 0xCE9C: 1, 0xFF97: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _PrintCardList

# >>> factory PrinterMenu_CardList
# Both cases tap A while the cursor sits at position 1 (the `ld a, $01`
# handed to InitCardSelectionParams), so HandleCardSelectionInput returns
# carry with hffb3 = 1 and the routine takes its `ret nz` exit. The
# bank1call PrintCardList branch is unreachable that way, which is what keeps
# the reference out of SendPrinterPacket's .wait_printer_packet_transmission
# DoFrame loop -- these cases complete normally.
#
# wLCDC starts clear so every wait before the routine's own EnableLCD is a
# no-op; CopyDMAFunction installs hDMAFunction for the frames that elapse
# afterwards and SetupText primes the glyph cache before the card list and
# the PrintTheCardListText header are printed. keys=[0x00, 0x01] taps A as a
# cycle, because the ROM's edge-triggered hKeysPressed never sees a held
# button pressed a second time.
#
# Nothing register-wise is compared (the two exits disagree). The observed
# bytes are the ones this routine writes and never rewrites:
#   $CEA1 wCardListVisibleOffset - zeroed before the list is printed
#   $CED3 wCurCardTypeFilter     - zeroed with it
#   $CEA4 wCardListCursorPos + the nine Data_ad05 parameter bytes at
#         $CEA5-$CEAD, written once by InitCardSelectionParams
#   $FFB3 hffb3                  - 1, the cursor position the input handler
#                                  stored on the frame it reported carry
# All are seeded to $FF first so the writes themselves are witnessed.
# $CEA3 wCheckMenuCursorBlinkCounter is deliberately NOT observed: it counts
# elapsed frames, so it still differs when A lands on a different iteration.
CONTRACT["PrinterMenu_CardList"] = {"compare": (), "preserve": ()}
CASES["PrinterMenu_CardList"] = [
    {"wram": {0xCABB: b"\x00", 0xCEA1: b"\xFF", 0xCED3: b"\xFF",
              0xCEA4: b"\xFF" * 10, 0xFFB3: b"\xFF"},
     "sram": _PRINTER_MENU_CARD_LIST_SRAM,
     "ramg": True,
     "setup": _PRINTER_MENU_CARD_LIST_SETUP,
     "keys": [0x00, 0x01],
     "read": {0xCEA1: 1, 0xCEA4: 10, 0xCED3: 1, 0xFFB3: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={0xCABB: b"\x00", 0xCEA1: b"\xFF", 0xCED3: b"\xFF",
               0xCEA4: b"\xFF" * 10, 0xFFB3: b"\xFF"},
         sram=_PRINTER_MENU_CARD_LIST_SRAM,
         ramg=True,
         setup=_PRINTER_MENU_CARD_LIST_SETUP,
         keys=[0x00, 0x01],
         read={0xCEA1: 1, 0xCEA4: 10, 0xCED3: 1, 0xFFB3: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrinterMenu_CardList

# >>> factory PrinterMenu_PokemonCards
CONTRACT["PrinterMenu_PokemonCards"] = {"compare": (), "preserve": ()}
CASES["PrinterMenu_PokemonCards"] = [
    {"rom_bank": 2,
     "wram": {0xCAB4: b"\x00", 0xCABB: b"\x00", 0xCEA1: b"\xFF",
              0xCED3: b"\xFF", 0xCEA4: b"\xFF" * 10, 0xFFB3: b"\xFF"},
     "sram": _PRINTER_MENU_CARD_LIST_SRAM,
     "ramg": True,
     "setup": _PRINTER_MENU_CARD_LIST_SETUP,
     "keys": [0x00, 0x02],
     "read": {0xCEA1: 1, 0xCEA4: 10, 0xCED3: 1, 0xFFB3: 1},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         rom_bank=2,
         wram={0xCAB4: b"\x00", 0xCABB: b"\x00", 0xCEA1: b"\xFF",
               0xCED3: b"\xFF", 0xCEA4: b"\xFF" * 10, 0xFFB3: b"\xFF"},
         sram=_PRINTER_MENU_CARD_LIST_SRAM,
         ramg=True,
         setup=_PRINTER_MENU_CARD_LIST_SETUP,
         keys=[0x00, 0x02],
         read={0xCEA1: 1, 0xCEA4: 10, 0xCED3: 1, 0xFFB3: 1},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrinterMenu_PokemonCards

# >>> factory HandlePrinterMenu
CONTRACT["HandlePrinterMenu"] = {"compare": (), "preserve": ()}
CASES["HandlePrinterMenu"] = [
    {"wram": {0xCFE4: b"\x00"}, "read": {0xCFE4: 1}},
    dict(POISON, wram={0xCFE4: b"\x00"}, read={0xCFE4: 1}),
]
# <<< factory HandlePrinterMenu

# >>> factory PrinterMenu_PrintQuality
CONTRACT["PrinterMenu_PrintQuality"] = {"compare": (), "preserve": ()}
CASES["PrinterMenu_PrintQuality"] = [
    {"rom_bank": 2, "stack": [0], "wram": {0xCABB: b"\x00", hffb3: b"\x00", wSelectedPrinterMenuItem: b"\x00"}, "sram": {0: {sPrinterContrastLevel: b"\x02"}}, "setup": QUALITY_SETUP, "keys": [0x00, 0x01], "sread": {0: {sPrinterContrastLevel: 1}}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, rom_bank=2, stack=[0x1234], wram={0xCABB: b"\x00", hffb3: b"\x00", wSelectedPrinterMenuItem: b"\x00"}, sram={0: {sPrinterContrastLevel: b"\x03"}}, setup=QUALITY_SETUP, keys=[0x00, 0x01], sread={0: {sPrinterContrastLevel: 1}}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrinterMenu_PrintQuality

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
SCHEMA2_CASES["SendPrinterPacket"][3]["completion"] = {"mode": "pre-ret", "pc": 0x315D}

MUTATIONS = {
    "ShowPrinterConnectionErrorScene": {
        "source_symbol": "ShowPrinterConnectionErrorScene",
        "before": "\tLoadTxRam3((uint16_t)a);",
        "after": "\tLoadTxRam3((uint16_t)(a + 1u));",
        "case_ids": ["ShowPrinterConnectionErrorScene-0", "ShowPrinterConnectionErrorScene-1"],
    },
    "SendByteThroughSerialData": {
        "source_symbol": "SendByteThroughSerialData",
        "before": "\tgb_write8(rSB, a);",
        "after": "\tgb_write8(wSerialTransferData_ADDR, (uint8_t)(a ^ 1u));",
        "case_ids": ["SendByteThroughSerialData-0", "SendByteThroughSerialData-1", "SendByteThroughSerialData-2"],
    },
    "ExecutePrinterPacketSequence": {
        "source_symbol": "ExecutePrinterPacketSequence",
        "before": "\t\tgb_write8(wSerialTransferData_ADDR, gb_read8(rSB));",
        "after": "\t\tgb_write8(wSerialTransferData_ADDR, (uint8_t)(gb_read8(rSB) ^ 0xFFu));",
        "case_ids": [
            "ExecutePrinterPacketSequence-8",
            "ExecutePrinterPacketSequence-0", "ExecutePrinterPacketSequence-1",
            "ExecutePrinterPacketSequence-2", "ExecutePrinterPacketSequence-3",
            "ExecutePrinterPacketSequence-4", "ExecutePrinterPacketSequence-5",
            "ExecutePrinterPacketSequence-6", "ExecutePrinterPacketSequence-7",
            "ExecutePrinterPacketSequence-8",
        ],
    },
}
# >>> factory-mutation Func_1a14b
MUTATIONS["Func_1a14b"] = {"source_symbol": "Func_1a14b", "before": "wce9d = 0x01u;", "after": "wce9d = 0x02u;", "case_ids": ["Func_1a14b-0", "Func_1a14b-1", "Func_1a14b-2"]}
# <<< factory-mutation Func_1a14b
# >>> factory-mutation Func_1a025
MUTATIONS["Func_1a025"] = {"source_symbol": "Func_1a025", "before": "\twTilePatternSelector = 0xA4u;", "after": "\twTilePatternSelector = 0xA5u;", "case_ids": ["Func_1a025-0", "Func_1a025-1"]}
# <<< factory-mutation Func_1a025
# >>> factory-mutation ResetPrinterCommunicationSettings
MUTATIONS["ResetPrinterCommunicationSettings"] = {"source_symbol": "ResetPrinterCommunicationSettings", "before": "\tuint16_t result_hl = SetupText(0x30u, 0xBFu);", "after": "\tuint16_t result_hl = SetupText(0x31u, 0xBFu);", "case_ids": ["ResetPrinterCommunicationSettings-0", "ResetPrinterCommunicationSettings-1"]}
# <<< factory-mutation ResetPrinterCommunicationSettings
# >>> factory-mutation ClearPrinterGfxBuffer
MUTATIONS["ClearPrinterGfxBuffer"] = {"source_symbol": "ClearPrinterGfxBuffer", "before": "\t\tgb_write8(target, 0u);", "after": "\t\tgb_write8(target, 1u);", "case_ids": ["ClearPrinterGfxBuffer-0", "ClearPrinterGfxBuffer-1"]}
# <<< factory-mutation ClearPrinterGfxBuffer
# >>> factory-mutation GetPrinterContrastSerialData
MUTATIONS["GetPrinterContrastSerialData"] = {"source_symbol": "GetPrinterContrastSerialData", "before": "\tuint16_t hl = (uint16_t)(((uint16_t)h_val << 8) | 0xE4u);", "after": "\tuint16_t hl = (uint16_t)(((uint16_t)h_val << 8) | 0xE5u);", "case_ids": ["GetPrinterContrastSerialData-0", "GetPrinterContrastSerialData-1"]}
# <<< factory-mutation GetPrinterContrastSerialData
# >>> factory-mutation PrepareForPrinterCommunications
MUTATIONS["PrepareForPrinterCommunications"] = {
    "source_symbol": "PrepareForPrinterCommunications",
    "before": "wPrinterNumberLineFeeds = 0x10u;",
    "after": "wPrinterNumberLineFeeds = 0x11u;",
    "case_ids": ["PrepareForPrinterCommunications-0", "PrepareForPrinterCommunications-1"],
}
# <<< factory-mutation PrepareForPrinterCommunications
# >>> factory-mutation CheckDataCompression
MUTATIONS["CheckDataCompression"] = {"source_symbol": "CheckDataCompression", "before": "\t\thl = (uint16_t)(hl + 1u);\n\t\te = (uint8_t)(e + 1u);\n\t\tc = (uint8_t)(c - 1u);\n\t\tif (c == 0u) {\n\t\t\tz_flag = 1u;\n\t\t\tgoto set_carry;\n\t\t}", "after": "\t\thl = (uint16_t)(hl + 1u);\n\t\te = (uint8_t)(e + 2u);\n\t\tc = (uint8_t)(c - 1u);\n\t\tif (c == 0u) {\n\t\t\tz_flag = 1u;\n\t\t\tgoto set_carry;\n\t\t}", "case_ids": ["CheckDataCompression-0"]}
# <<< factory-mutation CheckDataCompression
# >>> factory-mutation CompressDataForPrinterSerialTransfer
MUTATIONS["CompressDataForPrinterSerialTransfer"] = {
    "source_symbol": "CompressDataForPrinterSerialTransfer",
    "before": "\t\t\tgb_write8(de, (uint8_t)(((uint8_t)(found - 2u)) | 0x80u));",
    "after": "\t\t\tgb_write8(de, (uint8_t)(((uint8_t)(found - 1u)) | 0x80u));",
    "case_ids": ["CompressDataForPrinterSerialTransfer-0", "CompressDataForPrinterSerialTransfer-1"],
}
# <<< factory-mutation CompressDataForPrinterSerialTransfer
# >>> factory-mutation LoadCardInfoForPrinter
MUTATIONS["LoadCardInfoForPrinter"] = {"source_symbol": "LoadCardInfoForPrinter", "before": "\tuint8_t x = (uint8_t)(wPrinterHorizontalOffset | 0x40u);\n\tuint8_t d = 3u;", "after": "\tuint8_t x = (uint8_t)(wPrinterHorizontalOffset | 0x20u);\n\tuint8_t d = 3u;", "case_ids": ["LoadCardInfoForPrinter-0", "LoadCardInfoForPrinter-1"]}
# <<< factory-mutation LoadCardInfoForPrinter
# >>> factory-mutation PrinterMenu_QuitPrint
MUTATIONS["PrinterMenu_QuitPrint"] = {"source_symbol": "PrinterMenu_QuitPrint", "before": "\treturn result.f;", "after": "\treturn 0u;", "case_ids": ["PrinterMenu_QuitPrint-0", "PrinterMenu_QuitPrint-1"]}
# <<< factory-mutation PrinterMenu_QuitPrint
# >>> factory-mutation DrawBottomCardInfoInSRAMGfxBuffer0
MUTATIONS["DrawBottomCardInfoInSRAMGfxBuffer0"] = {
    "source_symbol": "DrawBottomCardInfoInSRAMGfxBuffer0",
    "before": "void DrawBottomCardInfoInSRAMGfxBuffer0(void)\n{\n\tFunc_1a025();\n\tgb_write8(wCardPageType_ADDR, CARDPAGETYPE_NOT_PLAY_AREA);",
    "after": "void DrawBottomCardInfoInSRAMGfxBuffer0(void)\n{\n\tFunc_1a025();\n\tgb_write8(wCardPageType_ADDR, 0x01u);",
    "case_ids": ["DrawBottomCardInfoInSRAMGfxBuffer0-0", "DrawBottomCardInfoInSRAMGfxBuffer0-1"],
}
# <<< factory-mutation DrawBottomCardInfoInSRAMGfxBuffer0
# >>> factory-mutation ShowPrinterTransmitting
MUTATIONS["ShowPrinterTransmitting"] = {
    "source_symbol": "ShowPrinterTransmitting",
    "before": "\tSetSpriteAnimationsAsVBlankFunction();",
    "after": "\t(void)0;",
    "case_ids": ["ShowPrinterTransmitting-0", "ShowPrinterTransmitting-1"],
}
# <<< factory-mutation ShowPrinterTransmitting
# >>> factory-mutation SendPrinterPacket
MUTATIONS["SendPrinterPacket"] = {"source_symbol": "SendPrinterPacket", "before": "\tgb_write8(wPrinterPacketPreamble_ADDR, 0x88u);", "after": "\tgb_write8(wPrinterPacketPreamble_ADDR, 0x89u);", "case_ids": ["SendPrinterPacket-3"]}
# <<< factory-mutation SendPrinterPacket
# >>> factory-mutation TryInitPrinterCommunications
MUTATIONS["TryInitPrinterCommunications"] = {
    "source_symbol": "TryInitPrinterCommunications",
    "before": "TryInitPrinterCommunicationsResult TryInitPrinterCommunications(void)\n{\n\twPrinterInitAttempts = 0u;\n\tfor (;;) {\n\t\tDoFrame();\n\t\tif ((hKeysHeld & PAD_B) != 0u) {\n\t\t\twPrinterStatus = 0u;",
    "after": "TryInitPrinterCommunicationsResult TryInitPrinterCommunications(void)\n{\n\twPrinterInitAttempts = 0u;\n\tfor (;;) {\n\t\tDoFrame();\n\t\tif ((hKeysHeld & PAD_B) != 0u) {\n\t\t\twPrinterStatus = 0xFFu;",
    "case_ids": ["TryInitPrinterCommunications-0", "TryInitPrinterCommunications-1"],
}
# <<< factory-mutation TryInitPrinterCommunications
# >>> factory-mutation ShowPrinterIsNotConnected
MUTATIONS["ShowPrinterIsNotConnected"] = {"source_symbol": "ShowPrinterIsNotConnected", "before": "ShowPrinterIsNotConnectedResult ShowPrinterIsNotConnected(uint8_t a, uint8_t f, uint8_t d, uint8_t e, uint16_t hl)\n{\n\ta = 0x02u;", "after": "ShowPrinterIsNotConnectedResult ShowPrinterIsNotConnected(uint8_t a, uint8_t f, uint8_t d, uint8_t e, uint16_t hl)\n{\n\ta = 0x03u;", "case_ids": ["ShowPrinterIsNotConnected-0", "ShowPrinterIsNotConnected-1"]}
# <<< factory-mutation ShowPrinterIsNotConnected
# >>> factory-mutation HandlePrinterError
MUTATIONS["HandlePrinterError"] = {"source_symbol": "HandlePrinterError", "before": "\tShowPrinterConnectionErrorSceneResult scene =\n\t\tShowPrinterConnectionErrorScene(0x04u, 0xA0u, d, e, PrinterPacketErrorText);", "after": "\tShowPrinterConnectionErrorSceneResult scene =\n\t\tShowPrinterConnectionErrorScene(0x02u, 0xA0u, d, e, PrinterPacketErrorText);", "case_ids": ["HandlePrinterError-5", "HandlePrinterError-6"]}
# <<< factory-mutation HandlePrinterError
# >>> factory-mutation SendPrinterInstructionPacket
MUTATIONS["SendPrinterInstructionPacket"] = {
    "source_symbol": "SendPrinterInstructionPacket",
    "before": "\t\tpacket = SendPrinterPacket(0u, 4u, PRINTERPKT_PRINT_INSTRUCTION, FALSE, saved_hl);",
    "after": "\t\tpacket = SendPrinterPacket(0u, 4u, PRINTERPKT_PRINT_INSTRUCTION, FALSE, (uint16_t)(saved_hl + 1u));",
    "case_ids": ["SendPrinterInstructionPacket-0", "SendPrinterInstructionPacket-1"],
}
# <<< factory-mutation SendPrinterInstructionPacket
# >>> factory-completion SendPrinterInstructionPacket
for _record in SCHEMA2_CASES["SendPrinterInstructionPacket"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion SendPrinterInstructionPacket
# >>> factory-mutation SendPrinterInstructionPacket_1Sheet
MUTATIONS["SendPrinterInstructionPacket_1Sheet"] = {
    "source_symbol": "SendPrinterInstructionPacket_1Sheet",
    "before": "\tuint8_t line_feeds = wPrinterNumberLineFeeds;\n\twPrinterNumberLineFeeds = 0x00u;",
    "after": "\tuint8_t line_feeds = wPrinterNumberLineFeeds;\n\twPrinterNumberLineFeeds = 0x01u;",
    "case_ids": ["SendPrinterInstructionPacket_1Sheet-0", "SendPrinterInstructionPacket_1Sheet-1"],
}
# <<< factory-mutation SendPrinterInstructionPacket_1Sheet
# >>> factory-completion SendPrinterInstructionPacket_1Sheet
# $315D is SendPrinterPacket.wait_printer_packet_transmission (home/printer.asm),
# the DoFrame loop the reference can never leave without a printer answering on
# the serial line. legacy_to_schema always emits completion "return", so the
# split is applied after migration.
for _record in SCHEMA2_CASES["SendPrinterInstructionPacket_1Sheet"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion SendPrinterInstructionPacket_1Sheet
# >>> factory-mutation _PreparePrinterConnection
MUTATIONS["_PreparePrinterConnection"] = {
    "source_symbol": "_PreparePrinterConnection",
    "before": "PreparePrinterConnectionResult _PreparePrinterConnection(uint16_t hl)\n{\n\tSendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_DATA, FALSE, hl);",
    "after": "PreparePrinterConnectionResult _PreparePrinterConnection(uint16_t hl)\n{\n\tSendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_DATA, FALSE, (uint16_t)(hl + 1u));",
    "case_ids": ["_PreparePrinterConnection-0", "_PreparePrinterConnection-1"],
}
# <<< factory-mutation _PreparePrinterConnection
# >>> factory-completion _PreparePrinterConnection
# $315D is SendPrinterPacket.wait_printer_packet_transmission (home/printer.asm),
# the DoFrame loop the reference can never leave without a printer answering on
# the serial line. legacy_to_schema always emits completion "return", so the
# split is applied after migration.
for _record in SCHEMA2_CASES["_PreparePrinterConnection"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion _PreparePrinterConnection

# >>> factory-mutation SendTilesToPrinter
MUTATIONS["SendTilesToPrinter"] = {
    "source_symbol": "SendTilesToPrinter",
    "before": "\t\thl = (uint16_t)(hl + 32u);",
    "after": "\t\thl = (uint16_t)(hl + 31u);",
    "case_ids": ["SendTilesToPrinter-3"],
}
# <<< factory-mutation SendTilesToPrinter

# >>> factory-completion SendTilesToPrinter
for _record in SCHEMA2_CASES["SendTilesToPrinter"]:
    if _record.get("evidence") == "primary":
        _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion SendTilesToPrinter

# >>> factory-mutation SendPrinterInstructionPacket_1Sheet_3LineFeeds
MUTATIONS["SendPrinterInstructionPacket_1Sheet_3LineFeeds"] = {
    "source_symbol": "SendPrinterInstructionPacket_1Sheet_3LineFeeds",
    "before": "\t\tSendPrinterInstructionPacket(0x0301u, contrast.hl);",
    "after": "\t\tSendPrinterInstructionPacket(0x0301u, (uint16_t)(contrast.hl + 1u));",
    "case_ids": ["SendPrinterInstructionPacket_1Sheet_3LineFeeds-2"],
}
# <<< factory-mutation SendPrinterInstructionPacket_1Sheet_3LineFeeds
# >>> factory-completion SendPrinterInstructionPacket_1Sheet_3LineFeeds
# $315D is SendPrinterPacket.wait_printer_packet_transmission (home/printer.asm),
# the DoFrame loop the reference can never leave without a printer answering on
# the serial line. legacy_to_schema always emits completion "return", so the
# split is applied after migration to the primary records only.
for _record in SCHEMA2_CASES["SendPrinterInstructionPacket_1Sheet_3LineFeeds"]:
    if _record["evidence"] == "primary":
        _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion SendPrinterInstructionPacket_1Sheet_3LineFeeds

# >>> factory-mutation LoadGfxBufferForPrinter
MUTATIONS["LoadGfxBufferForPrinter"] = {
    "source_symbol": "LoadGfxBufferForPrinter",
    "before": "return (LoadGfxBufferForPrinterResult){init.a, init.f, hl};",
    "after": "return (LoadGfxBufferForPrinterResult){1u, init.f, hl};",
    "case_ids": ["LoadGfxBufferForPrinter-0", "LoadGfxBufferForPrinter-1"],
}
# <<< factory-mutation LoadGfxBufferForPrinter
# >>> factory-mutation AddToPrinterGfxBuffer
MUTATIONS["AddToPrinterGfxBuffer"] = {
    "source_symbol": "AddToPrinterGfxBuffer",
    "before": "\tgb_write8(addr, (uint8_t)(gb_read8(addr) + 2u));",
    "after": "\tgb_write8(addr, (uint8_t)(gb_read8(addr) + 3u));",
    "case_ids": ["AddToPrinterGfxBuffer-0"],
}
# <<< factory-mutation AddToPrinterGfxBuffer
# >>> factory-mutation SendCardListToPrinter
MUTATIONS["SendCardListToPrinter"] = {"source_symbol": "SendCardListToPrinter", "before": "SendCardListToPrinterResult SendCardListToPrinter(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t offset = wPrinterHorizontalOffset;\n\tif (offset != 1u) {\n\t\tLoadGfxBufferForPrinterResult loaded = LoadGfxBufferForPrinter(hl);\n\t\tif ((loaded.f & 0x10u) != 0u)\n\t\t\treturn (SendCardListToPrinterResult){loaded.a, loaded.f, b, c, d, e, loaded.hl};\n\t\thl = loaded.hl;\n\t}\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) != 0u)", "after": "SendCardListToPrinterResult SendCardListToPrinter(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)\n{\n\tuint8_t offset = wPrinterHorizontalOffset;\n\tif (offset != 1u) {\n\t\tLoadGfxBufferForPrinterResult loaded = LoadGfxBufferForPrinter(hl);\n\t\tif ((loaded.f & 0x10u) != 0u)\n\t\t\treturn (SendCardListToPrinterResult){loaded.a, loaded.f, b, c, d, e, loaded.hl};\n\t\thl = loaded.hl;\n\t}\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) == 0u)", "case_ids": ["SendCardListToPrinter-0", "SendCardListToPrinter-1", "SendCardListToPrinter-2"]}
# <<< factory-mutation SendCardListToPrinter
# >>> factory-mutation Func_19f87
MUTATIONS["Func_19f87"] = {
    "source_symbol": "Func_19f87",
    "before": "Func_19f87Result Func_19f87(void)\n{\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) != 0u)",
    "after": "Func_19f87Result Func_19f87(void)\n{\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) == 0u)",
    "case_ids": ["Func_19f87-0", "Func_19f87-1"],
}
# <<< factory-mutation Func_19f87
# >>> factory-mutation Func_1a011
MUTATIONS["Func_1a011"] = {
    "source_symbol": "Func_1a011",
    "before": "Func_1a011Result Func_1a011(void)\n{\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) != 0u)",
    "after": "Func_1a011Result Func_1a011(void)\n{\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) == 0u)",
    "case_ids": ["Func_1a011-0", "Func_1a011-1"],
}
# <<< factory-mutation Func_1a011
# >>> factory-mutation Func_19f99
MUTATIONS["Func_19f99"] = {
    "source_symbol": "Func_19f99",
    "before": "Func_19f99Result Func_19f99(void)\n{\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) != 0u)\n\t\treturn (Func_19f99Result){init.a, init.f};",
    "after": "Func_19f99Result Func_19f99(void)\n{\n\tTryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();\n\tif ((init.f & 0x10u) != 0u)\n\t\treturn (Func_19f99Result){init.a, 0x80u};",
    "case_ids": ["Func_19f99-0", "Func_19f99-1"],
}
# <<< factory-mutation Func_19f99
# >>> factory-mutation _PrintDeckConfiguration
MUTATIONS["_PrintDeckConfiguration"] = {"source_symbol": "_PrintDeckConfiguration", "before": "\tCopyDataHLtoDE(&hl, &de, DECK_STRUCT_SIZE);", "after": "\tCopyDataHLtoDE(&hl, &de, (uint16_t)(DECK_STRUCT_SIZE - 1u));", "case_ids": ["_PrintDeckConfiguration-0", "_PrintDeckConfiguration-1"]}
# <<< factory-mutation _PrintDeckConfiguration
# >>> factory-completion _PrintDeckConfiguration
for _record in SCHEMA2_CASES["_PrintDeckConfiguration"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion _PrintDeckConfiguration
# >>> factory-mutation Func_1a080
MUTATIONS["Func_1a080"] = {
    "source_symbol": "Func_1a080",
    "before": "Func_1a080Result Func_1a080(uint16_t hl)\n{\n\tSendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_NUL, FALSE, hl);",
    "after": "Func_1a080Result Func_1a080(uint16_t hl)\n{\n\tSendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_NUL, FALSE, (uint16_t)(hl + 1u));",
    "case_ids": ["Func_1a080-0", "Func_1a080-1"],
}
# <<< factory-mutation Func_1a080
# >>> factory-completion Func_1a080
# $315D is SendPrinterPacket.wait_printer_packet_transmission (home/printer.asm),
# the DoFrame loop the reference can never leave without a printer answering on
# the serial line. legacy_to_schema always emits completion "return", so the
# split is applied after migration.
for _record in SCHEMA2_CASES["Func_1a080"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion Func_1a080
# >>> factory-mutation _RequestToPrintCard
MUTATIONS["_RequestToPrintCard"] = {
    "source_symbol": "_RequestToPrintCard",
    "before": "RequestToPrintCardResult _RequestToPrintCard(uint8_t a)\n{\n\tLoadCardDataToBuffer1_FromCardID(a);",
    "after": "RequestToPrintCardResult _RequestToPrintCard(uint8_t a)\n{\n\tLoadCardDataToBuffer1_FromCardID((uint8_t)(a + 1u));",
    "case_ids": ["_RequestToPrintCard-0", "_RequestToPrintCard-1"],
}
# <<< factory-mutation _RequestToPrintCard
# >>> factory-completion _RequestToPrintCard
# $315D is SendPrinterPacket.wait_printer_packet_transmission
# (home/printer.asm), the DoFrame loop the reference can never leave without a
# printer answering on the serial line. legacy_to_schema always emits
# completion "return", so the split is applied after migration.
for _record in SCHEMA2_CASES["_RequestToPrintCard"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion _RequestToPrintCard
# >>> factory-mutation _PrintCardList
MUTATIONS["_PrintCardList"] = {
    "source_symbol": "_PrintCardList",
    "before": "\twPrintOnlyStarRarity = star_only;",
    "after": "\twPrintOnlyStarRarity = (uint8_t)(star_only + 1u);",
    "case_ids": ["_PrintCardList-0", "_PrintCardList-1"],
}
# <<< factory-mutation _PrintCardList
# >>> factory-completion _PrintCardList
# $315D is SendPrinterPacket.wait_printer_packet_transmission
# (poketcg/src/home/printer.asm), the DoFrame loop the reference can never leave
# without a printer answering on the serial line. legacy_to_schema always emits
# completion "return", so the split is applied after migration.
for _record in SCHEMA2_CASES["_PrintCardList"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion _PrintCardList
# >>> factory-mutation PrinterMenu_CardList
MUTATIONS["PrinterMenu_CardList"] = {
    "source_symbol": "PrinterMenu_CardList",
    "before": "\tuint16_t params = PRINTER_CARD_LIST_SELECTION_PARAMS_ADDR;\n\t(void)InitCardSelectionParams(0x01u, &params);",
    "after": "\tuint16_t params = (uint16_t)(PRINTER_CARD_LIST_SELECTION_PARAMS_ADDR + 1u);\n\t(void)InitCardSelectionParams(0x01u, &params);",
    "case_ids": ["PrinterMenu_CardList-0", "PrinterMenu_CardList-1"],
}
# <<< factory-mutation PrinterMenu_CardList
# >>> factory-mutation PrinterMenu_PokemonCards
MUTATIONS["PrinterMenu_PokemonCards"] = {
    "source_symbol": "PrinterMenu_PokemonCards",
    "before": "void PrinterMenu_PokemonCards(void)\n{\n\t(void)WriteCardListsTerminatorBytes();\n\tPrintPlayersCardsHeaderInfo();\n\n\twCardListVisibleOffset = 0u;\n\twCurCardTypeFilter = 0u;\n\tPrintFilteredCardSelectionList(0u, 0x80u, 0u, 0u, 0u, 0u, wCardListCoords_ADDR);\n\tEnableLCD();\n\n\tuint16_t filter_params = FILTERS_CARD_SELECTION_PARAMS_ADDR;",
    "after": "void PrinterMenu_PokemonCards(void)\n{\n\t(void)WriteCardListsTerminatorBytes();\n\tPrintPlayersCardsHeaderInfo();\n\n\twCardListVisibleOffset = 0u;\n\twCurCardTypeFilter = 0u;\tPrintFilteredCardSelectionList(0u, 0x80u, 0u, 0u, 0u, 0u, wCardListCoords_ADDR);\n\tEnableLCD();\n\n\tuint16_t filter_params = (uint16_t)(FILTERS_CARD_SELECTION_PARAMS_ADDR + 1u);",
    "case_ids": ["PrinterMenu_PokemonCards-0", "PrinterMenu_PokemonCards-1"],
}
# <<< factory-mutation PrinterMenu_PokemonCards
# >>> factory-mutation HandlePrinterMenu
MUTATIONS["HandlePrinterMenu"] = {"source_symbol": "HandlePrinterMenu", "before": "void HandlePrinterMenu(void)\n{\n\t(void)0;", "after": "void HandlePrinterMenu(void)\n{\n\t(void)0;\n\twSelectedPrinterMenuItem = 1u;", "case_ids": ["HandlePrinterMenu-0", "HandlePrinterMenu-1"]}
# <<< factory-mutation HandlePrinterMenu
# >>> factory-completion HandlePrinterMenu
# >>> factory-completion HandlePrinterMenu
for _record in SCHEMA2_CASES["HandlePrinterMenu"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x315D}
# <<< factory-completion HandlePrinterMenu
# >>> factory-mutation PrinterMenu_PrintQuality
MUTATIONS["PrinterMenu_PrintQuality"] = {"source_symbol": "PrinterMenu_PrintQuality", "before": "\t\t\tsPrinterContrastLevel = selected;", "after": "\t\t\tsPrinterContrastLevel = (uint8_t)(selected + 1u);", "case_ids": ["PrinterMenu_PrintQuality-0", "PrinterMenu_PrintQuality-1"]}
# <<< factory-mutation PrinterMenu_PrintQuality
# >>> factory-completion PrinterMenu_PrintQuality
# >>> factory-completion PrinterMenu_PrintQuality
for _record in SCHEMA2_CASES["PrinterMenu_PrintQuality"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x6DE2, "bank": 2}
# <<< factory-completion PrinterMenu_PrintQuality
