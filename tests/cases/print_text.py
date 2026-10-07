from tests.cases._symbols import STACK_CANARY, sym
from tests.cases._fixtures import (ADVANCE_TEXT_REGS, PROCESS_TEXT_HEADER_REGS,
                                   SCROLL_LABEL_REGS, SCROLL_TEXT_REGS,
                                   advance_text_fixture, process_text_header_fixture,
                                   scroll_label_fixture, scroll_text_fixture)

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
HEADER = sym("wTextHeader1")
BUFFER = sym("wStringBuffer")
BOX_READ = {0x9980: 192}
CURSOR_STATE = {sym("wCursorBlinkCounter"): bytes([5]), sym("wCurMenuItem"): bytes([0]), sym("wMenuCursorXOffset"): bytes([18]),
                sym("wMenuCursorYOffset"): bytes([17]), sym("wMenuYSeparation"): bytes([0]), sym("wNumMenuItems"): bytes([1]),
                sym("wMenuVisibleCursorTile"): bytes([0x0F]), sym("wMenuInvisibleCursorTile"): bytes([0x00])}

CONTRACT = {
    "GetTextOffsetFromTextID": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
    "GetPointerToTextHeader": {"compare": ("b", "c", "hl"), "preserve": ()},
    "ReadTextHeader": {"compare": ("b", "c", "hl"), "preserve": ()},
    "WriteToTextHeader": {"compare": ("b", "c", "hl"), "preserve": ()},
    "WriteToTextHeader_MoveToNext": {"compare": ("b", "c", "hl"), "preserve": ()},
    "ResetTxRam_WriteToTextHeader": {"compare": ("b", "c", "hl"), "preserve": ()},
    "TwoByteNumberToText_CountLeadingZeros": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
    "CopyText": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
    "CountLinesOfTextFromID": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "LoadTxRam2": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
    "LoadTxRam3": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()},
    "ProcessTextHeader": {"compare": ("a", "d", "e", "f", "hl"), "preserve": ()},
    "HandleTxRam2Or3": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "CopyTextData_FromTextID": {"compare": ("d", "e", "hl"), "preserve": ()},
    "CopyPlayerNameOrTurnDuelistName": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "InitTextPrinting_ProcessTextFromID": {"compare": ("b", "c", "hl"), "preserve": ()},
    "InitTextPrinting_ProcessTextFromPointerToID": {"compare": ("b", "c", "hl"), "preserve": ()},
    "ProcessTextFromID": {"compare": ("b", "c", "hl"), "preserve": ()},
    "ProcessTextFromPointerToID": {"compare": ("b", "c", "hl"), "preserve": ()},
    "PlaceTextItems": {"compare": ("d", "hl"), "preserve": ()},
    "PrintText": {"compare": ("hl",), "preserve": ()},
    "PrintTextNoDelay": {"compare": ("hl",), "preserve": ()},
    "DrawTextReadyLabeledOrRegularTextBox": {"compare": ("a", "d", "e", "hl"), "preserve": ()},
    "WaitForPlayerToAdvanceText": {"compare": ("f",), "preserve": ()},
    "PrintScrollableText": {"compare": ("d", "e", "hl"), "preserve": ()},
    "PrintScrollableText_NoTextBoxLabel": {"compare": ("f",), "preserve": ()},
    "PrintScrollableText_WithTextBoxLabel_NoWait": {"compare": ("a", "d", "e", "hl"), "preserve": ()},
    "PrintScrollableText_WithTextBoxLabel": {"compare": ("f",), "preserve": ()},
}

CASES = {
    "GetTextOffsetFromTextID": [{"hl": 1}, dict(POISON, hl=1)],
    # hl = wTextHeader1 + wWhichTextHeader * 5, and the routine writes no memory at
    # all -- so `expect` alone cannot fail it and the output has to be pinned with
    # `expect_regs`. Selector 1 lands on $CE30, which is wTextHeader2 in poketcg.sym,
    # cross-checking the stride against the symbol table rather than against the port.
    "GetPointerToTextHeader": [
        {"wram": {sym("wWhichTextHeader"): b"\x00"}, "read": {sym("wWhichTextHeader"): 1}},
        {"wram": {sym("wWhichTextHeader"): b"\x01"}, "read": {sym("wWhichTextHeader"): 1}},
        dict(POISON, wram={sym("wWhichTextHeader"): b"\x03"}, read={sym("wWhichTextHeader"): 1}),
    ],
    # Oracle-run: the synthesized frame now sits in $CF00-$CFFF, so the text-header
    # block at $CE2B is seedable and diffable against the real ROM.
    "ReadTextHeader": [
        {"wram": {HEADER: b"\x0f\x00\x01\x00\x40"},
         "read": {HEADER: 5, sym("hBankROM"): 1}},
        dict(POISON, wram={HEADER: b"\x06\x01\x02\x34\x56"},
             read={HEADER: 5, sym("hBankROM"): 1}),
    ],
    "WriteToTextHeader": [
        {"hl": 0x4000, "wram": {sym("wWhichTextHeader"): b"\x00", HEADER: b"\0" * 5},
         "read": {HEADER: 5, sym("wWhichTextHeader"): 1}},
        dict(POISON, hl=0x5678, wram={sym("wWhichTextHeader"): b"\x03", HEADER: b"\0" * 5},
             read={HEADER: 5, sym("wTextHeader4"): 5, sym("wWhichTextHeader"): 1}),
    ],
    "WriteToTextHeader_MoveToNext": [
        {"hl": 0x4000, "wram": {sym("wWhichTextHeader"): b"\x00", HEADER: b"\0" * 5},
         "read": {HEADER: 5, sym("wWhichTextHeader"): 1}},
        dict(POISON, hl=0x5678, wram={sym("wWhichTextHeader"): b"\x02", HEADER: b"\0" * 5},
             read={HEADER: 5, sym("wTextHeader3"): 5, sym("wWhichTextHeader"): 1}),
    ],
    "ResetTxRam_WriteToTextHeader": [
        {"hl": 0x4000, "wram": {sym("wWhichTextHeader"): b"\x03", HEADER: b"\0" * 5,
                                sym("wWhichTxRam2"): b"\x01", sym("wWhichTxRam3"): b"\x02"},
         "read": {HEADER: 5, sym("wTextHeader4"): 5, sym("wWhichTextHeader"): 1, sym("wWhichTxRam2"): 1, sym("wWhichTxRam3"): 1}},
        dict(POISON, hl=0x5678, wram={sym("wWhichTextHeader"): b"\x02", HEADER: b"\0" * 5,
                                      sym("wWhichTxRam2"): b"\x01", sym("wWhichTxRam3"): b"\x02"},
             read={HEADER: 5, sym("wTextHeader3"): 5, sym("wWhichTextHeader"): 1, sym("wWhichTxRam2"): 1, sym("wWhichTxRam3"): 1}),
    ],
    "TwoByteNumberToText_CountLeadingZeros": [
        {"hl": 0, "wram": {sym("wFontWidth"): b"\x01"}, "read": {BUFFER: 6}},
        {"hl": 1, "wram": {sym("wFontWidth"): b"\x01"}, "read": {BUFFER: 6}},
        dict(POISON, hl=0xFFFF, wram={sym("wFontWidth"): b"\x01"}, read={BUFFER: 6}),
        {"hl": 0, "wram": {sym("wFontWidth"): b"\x00"}, "read": {BUFFER: 11}},
    ],
    "CopyText": [
        {"hl": 1, "d": 0xC1, "e": 0x00, "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 32}},
        {"hl": 0, "d": 0xC1, "e": 0x00, "wram": {sym("hWhoseTurn"): b"\x00"},
         "sram": {0: {sym("sPlayerName"): b"\x21\x00"}}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 2}},
        {"hl": 0, "d": 0xC1, "e": 0x20, "wram": {sym("hWhoseTurn"): b"\x01", sym("wNameBuffer"): b"\x31\x00"},
         "read": {sym("wDecompressionSecondaryBufferStart") + 0x31: 2}},
    ],
    "CountLinesOfTextFromID": [{"hl": 1}, dict(POISON, hl=1)],
    # wTxRam2 is $CE3F and the asm writes it and $CE40. wTxRam2_b is a DIFFERENT
    # symbol at $CE41 and must stay untouched -- the third read byte pins that.
    # Oracle-run now that the synthesized frame moved out to $CF00-$CFFF.
    "LoadTxRam2": [
        {"hl": 1, "wram": {sym("wTxRam2"): b"\xff\xff\xff"}, "read": {sym("wTxRam2"): 3}},
        dict(POISON, hl=0x1234, wram={sym("wTxRam2"): b"\xff\xff\xff"}, read={sym("wTxRam2"): 3}),
    ],
    "LoadTxRam3": [
        {"hl": 0, "wram": {sym("wTxRam3"): b"\xff\xff\xff"}, "read": {sym("wTxRam3"): 3}},
        dict(POISON, hl=0xFFFF, wram={sym("wTxRam3"): b"\xff\xff\xff"}, read={sym("wTxRam3"): 3}),
    ],
}

CASES.update({
    # No text engine involved: a bounded copy of at most a tiles, so this runs on the
    # oracle against the real ROM. e comes back as the actual character count.
    # hff96 ($FF96) holds the count across GetTextOffsetFromTextID.
    "CopyTextData_FromTextID": [
        {"a": 8, "hl": 1, "d": 0xC1, "e": 0x00, "wram": {sym("hff96"): b"\x55"}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 10}},
        {"a": 2, "hl": 1, "d": 0xC1, "e": 0x00, "wram": {sym("hff96"): b"\x55"}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 4}},
        dict(POISON, a=8, hl=1, d=0xC1, e=0x00, wram={sym("hff96"): b"\x55"}, read={sym("wDecompressionSecondaryBufferStart") + 0x11: 10}),
    ],
    # hWhoseTurn selects the callee; hl always comes back as the buffer the asm
    # pushed and popped, whichever name was copied.
    "CopyPlayerNameOrTurnDuelistName": [
        {"wram": {sym("hWhoseTurn"): b"\x00"}, "sram": {0: {sym("sPlayerName"): b"\x41\x42\x00"}},
         "read": {BUFFER: 4}},
        # OPPONENT_TURN is HIGH(wOpponentDuelVariables) = $C3. With no text ID at
        # wOpponentName the opponent path falls back to the name buffer.
        {"wram": {sym("hWhoseTurn"): b"\xC3", sym("wOpponentName"): b"\x00\x00", sym("wNameBuffer"): b"\x43\x44\x00"},
         "read": {BUFFER: 4}},
        dict(POISON, wram={sym("hWhoseTurn"): b"\x00"}, sram={0: {sym("sPlayerName"): b"\x45\x00"}},
             read={BUFFER: 3}),
    ],
    # Text ID 0 resolves to an immediately terminated text, so ProcessText returns
    # without generating tiles. The multi-pair half-width case (id 1, "Hand") is
    # appended after CACHE_READ is defined -- it needs a SetupText prelude so the
    # cache is acyclic and the oracle returns.
    "ProcessTextFromID": [
        {"hl": 0, "wram": {sym("wLCDC"): b"\x00"}},
        dict(POISON, hl=0, wram={sym("wLCDC"): b"\x00"}),
    ],
    "InitTextPrinting_ProcessTextFromID": [
        {"hl": 0, "d": 0, "e": 0, "wram": {sym("wLCDC"): b"\x00"}},
        dict(POISON, hl=0, d=1, e=2, wram={sym("wLCDC"): b"\x00"}),
    ],
    # ReadTextHeader resolves inside wTextHeader1 ($CE2B), which lives in the
    # oracle's synthesized call frame, so these are asm-derived rather than run.
    # TX_END with no pending header level: TerminateHalfWidthText returns at once
    # when wFontWidth is FULL_WIDTH, then `scf` makes carry the only flag output.
    # ReadTextHeader resolves inside wTextHeader1 ($CE2B), which lives in the
    # oracle's synthesized call frame, so these are derived from the asm.
    # A header is five bytes: syllabary, font width, bank, text lo, text hi.
    # With FULL_WIDTH set, TerminateHalfWidthText returns at once and leaves d, e
    # and hl alone, so `scf` makes carry the only flag the TX_END path produces.
    "ProcessTextHeader": [
        {"d": 3, "e": 4,
         "wram": {HEADER: b"\x0f\x00\x01\x00\xC1", sym("wWhichTextHeader"): b"\x00",
                  sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00"},
         "read": {HEADER: 5, sym("wWhichTextHeader"): 1, sym("wDecompressionSecondaryBufferStart") + 0x11: 1}},
        # A pending header level is popped and the routine re-runs one level up:
        # wWhichTextHeader selects the header, five bytes per level.
        {"d": 5, "e": 6,
         "wram": {HEADER: b"\x0f\x00\x01\x00\xC1",
                  HEADER + 5: b"\x0f\x00\x01\x00\xC1",
                  sym("wWhichTextHeader"): b"\x01", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00"},
         "read": {HEADER: 10, sym("wWhichTextHeader"): 1, sym("wDecompressionSecondaryBufferStart") + 0x11: 1}},
        # TX_SYMBOL is a two-byte sequence (print_text.asm:292-293 writes back
        # the handler's advanced pointer): one call consumes both, places the
        # symbol tile at the text position and leaves the header on the space.
        {"d": 0, "e": 0,
         "wram": {HEADER: b"\x0f\x00\x01\x00\xC1", sym("wWhichTextHeader"): b"\x00",
                  sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x05\x07\x20\x6d\x00", sym("hffb0"): b"\x00"},
         "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}, {"fn": "InitTextPrinting", "d": 2, "e": 3}],
         "read": {HEADER: 5, sym("wDecompressionSecondaryBufferStart") + 0x11: 5}, "vread": {0: {0x9800: 0x400}}},

        dict(process_text_header_fixture(vram=False), **PROCESS_TEXT_HEADER_REGS,
             read={HEADER: 5}),
    ],
    # The zero-ID early exit returns before any text processing, so it is the one
    # path of this pair the emulator can run end to end.
    "InitTextPrinting_ProcessTextFromPointerToID": [
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "d": 0, "e": 0, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\x00"},
         "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 2}},
        dict(POISON, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, d=0, e=0, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\x00"},
             read={sym("wDecompressionSecondaryBufferStart") + 0x11: 2}),
    ],

    "HandleTxRam2Or3": [
        # The asm ends `ld a, [hli] / ld h, [hl] / ld l, a`, so hl is the 16-bit value
        # held in the slot, not the slot address. Index 0 reads the first slot.
        {"hl": sym("wWhichTxRam2"), "d": 0xCE, "e": 0x3F, "wram": {sym("wWhichTxRam2"): b"\x00", sym("wTxRam2"): b"\x34\x12"},
         "read": {sym("wWhichTxRam2"): 1, sym("wTxRam2"): 2}},
        # Index 2 selects the third slot: `add a` doubles it, so the offset is 4.
        {"hl": sym("wWhichTxRam2"), "d": 0xCE, "e": 0x3F,
         "wram": {sym("wWhichTxRam2"): b"\x02", sym("wTxRam3"): b"\x78\x56"},
         "read": {sym("wWhichTxRam2"): 1, sym("wTxRam3"): 2}},
        # `add a` is 8-bit, so an index of $80 doubles to 0 and wraps onto slot 0.
        {"hl": sym("wWhichTxRam2"), "d": 0xCE, "e": 0x3F,
         "wram": {sym("wWhichTxRam2"): b"\x80", sym("wTxRam2"): b"\xCD\xAB"},
         "read": {sym("wWhichTxRam2"): 1, sym("wTxRam2"): 2}},
    ],
    "ProcessTextFromPointerToID": [
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\x00"}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x11: 2}},
    ],
})

# Real text id 1 ("\x06Hand\x00") drives the half-width tile cache across two
# character pairs, so the whole cache -- key1 $C6xx, key2 $C7xx, next $C8xx,
# prev $C9xx -- is diffed against the oracle. wCurTextTile ($CD05) and
# wFontWidth ($CD0A) pin the placed tile id and the half-width mode.
CACHE_READ = {sym("wc600") + 0x20: 4, sym("wc700") + 0x20: 4, sym("wc800") + 0x20: 4, sym("wc900") + 0x20: 4, sym("wCurTextTile"): 2, sym("wFontWidth"): 1}
# InitTextPrinting's whole observable effect is the print cursor: hTextBGMap0Address
# ($FFAA-$FFAB, the BG-map destination DECoordToBGMap0Address derives from d/e) and
# hTextHorizontalAlign ($FFAD, d itself). Without these a routine that places items
# at the wrong coordinates still passes -- swapping InitTextPrinting(d, e) to (e, d)
# was verified green before they were added.
PLACEMENT_READ = {sym("hTextBGMap0Address"): 2, sym("hTextHorizontalAlign"): 1}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES.update({
    # Item format is [x][y][text-id lo][text-id hi] per item, bit 7 of x terminates.
    "PlaceTextItems": [
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x80"}},
        dict(POISON, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x80"}),
        {"hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x01\x02\x01\x00\x80"},
         "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
    ],
    # hl == 0 takes the wDefaultText path (no bank save/restore); a zero first byte
    # is TX_END so the body exits after one ProcessTextHeader. wTextSpeed ($CE47)
    # is inside the synthesized frame and cannot be seeded, so it stays 0: the
    # DoFrame delay loop runs zero iterations. Seeding hKeysHeld=PAD_B takes the
    # B-skip branch (TEXT_SPEED_4 path); at speed 0 its output matches the no-B
    # case because both skip every DoFrame, but it exercises the hKeysHeld read.
    "PrintText": [
        {"hl": 0, "d": 0, "e": 0, "wram": {sym("wCurDeckCardChanges"): b"\x00"}},
        dict(POISON, hl=0, wram={sym("wCurDeckCardChanges"): b"\x00"}),
        {"hl": 1, "d": 0, "e": 0, "setup": SETUP, "read": dict(CACHE_READ),
         "vread": VRAM_READ},
        {"hl": 1, "d": 0, "e": 0, "wram": {sym("hKeysHeld"): b"\x02"},
         "setup": SETUP, "read": dict(CACHE_READ), "vread": VRAM_READ},
        {"hl": 1, "d": 0x12, "e": 0x34, "setup": SETUP,
         "read": dict(CACHE_READ), "vread": VRAM_READ},
    ],
    # No hl==0 shortcut: hl is always a text id. id 0 resolves to an immediate
    # TX_END; id 1 ("Hand") runs the engine.
    "PrintTextNoDelay": [
        {"hl": 0, "d": 0, "e": 0},
        {"hl": 1, "d": 0, "e": 0, "setup": SETUP, "read": dict(CACHE_READ),
         "vread": VRAM_READ},
        dict(POISON, hl=1, d=0, e=0, setup=SETUP, read=dict(CACHE_READ), vread=VRAM_READ),
    ],
    "DrawTextReadyLabeledOrRegularTextBox": [
        {"hl": 0, "vread": {0: BOX_READ}},
        {"hl": 1, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
    ],
    "WaitForPlayerToAdvanceText": [
        {"keys": 0x01, "vread": {0: {0x9A32: 1}}},
        {"keys": 0x02, "vread": {0: {0x9A32: 1}}},
        dict(POISON, keys=0x01, vread={0: {0x9A32: 1}}),
        dict(advance_text_fixture(vram=False), **ADVANCE_TEXT_REGS, keys=[0x00, 0x01]),
    ],
    "PrintScrollableText": [
        {"a": 0, "hl": 0, "keys": 0x01,
         "wram": {sym("wCurDeckCardChanges"): b"\x00"}, "vread": {0: BOX_READ}},
        {"a": 0, "hl": 1, "keys": 0x02, "setup": SETUP,
         "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
        dict(scroll_text_fixture(vram=False), **SCROLL_TEXT_REGS, keys=[0x00, 0x01]),
    ],
    "PrintScrollableText_NoTextBoxLabel": [
        {"hl": 0, "keys": 0x01,
         "wram": {sym("wCurDeckCardChanges"): b"\x00", sym("wIsTextBoxLabeled"): b"\xff", sym("wCursorBlinkCounter"): b"\x05",
                  sym("wCurMenuItem"): b"\x04", sym("wMenuInvisibleCursorTile"): b"\x22"},
         "read": {sym("wIsTextBoxLabeled"): 1, sym("wCursorBlinkCounter"): 1, sym("wCurMenuItem"): 1, sym("wMenuInvisibleCursorTile"): 1},
         "vread": {0: {0x9A32: 1}}},
        dict(scroll_text_fixture(vram=False), **SCROLL_TEXT_REGS, keys=[0x00, 0x01]),
    ],
    "PrintScrollableText_WithTextBoxLabel_NoWait": [
        {"hl": 0, "d": 0x34, "e": 0x12,
         "wram": {sym("wCurDeckCardChanges"): b"\x00", sym("wIsTextBoxLabeled"): b"\xff", sym("wTextBoxLabel"): b"\xff\xff"},
         "read": {sym("wIsTextBoxLabeled"): 1, sym("wTextBoxLabel"): 2}, "vread": {0: {0x9980: 1}}},
    ],
    "PrintScrollableText_WithTextBoxLabel": [
        {"hl": 0, "d": 0x34, "e": 0x12, "keys": 0x01,
         "wram": {sym("wCurDeckCardChanges"): b"\x00", sym("wIsTextBoxLabeled"): b"\xff", sym("wTextBoxLabel"): b"\xff\xff",
                  sym("wCursorBlinkCounter"): b"\x05", sym("wCurMenuItem"): b"\x04", sym("wMenuInvisibleCursorTile"): b"\x22"},
         "read": {sym("wIsTextBoxLabeled"): 1, sym("wTextBoxLabel"): 2, sym("wCursorBlinkCounter"): 1, sym("wCurMenuItem"): 1, sym("wMenuInvisibleCursorTile"): 1},
         "vread": {0: {0x9980: 1}}},
        dict(scroll_label_fixture(vram=False, changes={sym("wDoFrameFunction"): b"\x00\x00"}), **SCROLL_LABEL_REGS, keys=[0x00, 0x01]),
    ],
})
# GenerateTextTile's product is the tile itself, copied into VRAM. Without a vread
# the cache keys are checked but the generated tile is not: swapping its d/e
# arguments was verified green before this span was added.
CASES["ProcessTextFromID"].append(
    {"hl": 1, "setup": SETUP, "read": dict(CACHE_READ), "vread": VRAM_READ})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {
    "ProcessTextHeader": {
        "source_symbol": "ProcessTextHeader",
        "before": "\treturn header_result(hBankROM, printed.d, printed.e,\n\t\t\t     (uint8_t)(hBankROM == 0u ? 0x80u : 0x00u), done.hl);",
        "after": "\treturn header_result(hBankROM, d, e,\n\t\t\t     (uint8_t)(hBankROM == 0u ? 0x80u : 0x00u), done.hl);",
        "case_ids": ["ProcessTextHeader-3"],
    },
    "CopyTextData_FromTextID": {
        "source_symbol": "CopyTextData_FromTextID",
        "before": "\tgb_write8(hff96_ADDR, a);\n\tuint16_t source = GetTextOffsetFromTextID(hl);",
        "after": "\tuint16_t source = GetTextOffsetFromTextID(hl);",
        "case_ids": ["CopyTextData_FromTextID-0", "CopyTextData_FromTextID-1", "CopyTextData_FromTextID-2"],
    },
    "PrintText": {
        "source_symbol": "PrintText",
        "before": "if (hl == 0) {",
        "after": "if (hl != 0) {",
        "case_ids": ["PrintText-0", "PrintText-1", "PrintText-2", "PrintText-3", "PrintText-4"],
    },
}
MUTATIONS["CopyPlayerNameOrTurnDuelistName"] = {
    "source_symbol": "CopyPlayerNameOrTurnDuelistName",
    "before": "\tCopyTextResult result = hWhoseTurn == OPPONENT_TURN ? CopyOpponentName(de)",
    "after": "\tCopyTextResult result = hWhoseTurn != OPPONENT_TURN ? CopyOpponentName(de)",
    "case_ids": ["CopyPlayerNameOrTurnDuelistName-0"],
}
MUTATIONS["CopyText"] = {
    "source_symbol": "CopyText",
    "before": "\t\tif (hWhoseTurn == OPPONENT_TURN)",
    "after": "\t\tif (hWhoseTurn != OPPONENT_TURN)",
    "case_ids": ["CopyText-1"],
}
MUTATIONS["CountLinesOfTextFromID"] = {
    "source_symbol": "CountLinesOfTextFromID",
    "before": "\t\tif (value == 0x0a)",
    "after": "\t\tif (value != 0x0a)",
    "case_ids": ["CountLinesOfTextFromID-0"],
}
MUTATIONS["DrawTextReadyLabeledOrRegularTextBox"] = {
    "source_symbol": "DrawTextReadyLabeledOrRegularTextBox",
    "before": "\t\tDrawRegularTextBox(&box, wIsTextBoxLabeled, b, c, d, e);",
    "after": "\t\tDrawRegularTextBox(&box, wIsTextBoxLabeled, (uint8_t)(b ^ 1u), c, d, e);",
    "case_ids": ["DrawTextReadyLabeledOrRegularTextBox-0"],
}
MUTATIONS["GetTextOffsetFromTextID"] = {
    "source_symbol": "GetTextOffsetFromTextID",
    "before": "\tuint16_t index = (uint16_t)(text_id * 3u);",
    "after": "\tuint16_t index = (uint16_t)(text_id * 4u);",
    "case_ids": ["GetTextOffsetFromTextID-0"],
}
MUTATIONS["HandleTxRam2Or3"] = {
    "source_symbol": "HandleTxRam2Or3",
    "before": "\tuint8_t offset = (uint8_t)(index * 2u);",
    "after": "\tuint8_t offset = (uint8_t)(index * 3u);",
    "case_ids": ["HandleTxRam2Or3-1"],
}
MUTATIONS["GetPointerToTextHeader"] = {
    "source_symbol": "GetPointerToTextHeader",
    "before": "\treturn text_header();",
    "after": "\treturn (text_header()) ^ 1u;",
    "case_ids": ["GetPointerToTextHeader-0"],
}
MUTATIONS["LoadTxRam2"] = {
    "source_symbol": "LoadTxRam2",
    "before": "\tgb_write8((uint16_t)(wTxRam2_ADDR + 1), (uint8_t)(text_id >> 8));",
    "after": "\tgb_write8((uint16_t)(wTxRam2_ADDR - 1), (uint8_t)(text_id >> 8));",
    "case_ids": ["LoadTxRam2-0"],
}
MUTATIONS["LoadTxRam3"] = {
    "source_symbol": "LoadTxRam3",
    "before": "\tgb_write8((uint16_t)(wTxRam3_ADDR + 1), (uint8_t)(value >> 8));",
    "after": "\tgb_write8((uint16_t)(wTxRam3_ADDR - 1), (uint8_t)(value >> 8));",
    "case_ids": ["LoadTxRam3-0"],
}
MUTATIONS["PlaceTextItems"] = {
    "source_symbol": "PlaceTextItems",
    "before": "\t\tif (d & 0x80u)",
    "after": "\t\tif (d & 0x81u)",
    "case_ids": ["PlaceTextItems-2"],
}
MUTATIONS["PrintScrollableText"] = {
    "source_symbol": "PrintScrollableText",
    "before": "\t\tuint8_t c = (uint8_t)(speed + 1u);",
    "after": "\t\tuint8_t c = (uint8_t)(speed - 1u);",
    "case_ids": ["PrintScrollableText-0"],
}
MUTATIONS["PrintScrollableText_NoTextBoxLabel"] = {
    "source_symbol": "PrintScrollableText_NoTextBoxLabel",
    "before": "\t(void)PrintScrollableText(0, hl);",
    "after": "\t;",
    "case_ids": ["PrintScrollableText_NoTextBoxLabel-0"],
}
MUTATIONS["PrintScrollableText_WithTextBoxLabel"] = {
    "source_symbol": "PrintScrollableText_WithTextBoxLabel",
    "before": "\t(void)PrintScrollableText_WithTextBoxLabel_NoWait(hl, de);",
    "after": "\t;",
    "case_ids": ["PrintScrollableText_WithTextBoxLabel-0"],
}
MUTATIONS["PrintScrollableText_WithTextBoxLabel_NoWait"] = {
    "source_symbol": "PrintScrollableText_WithTextBoxLabel_NoWait",
    "before": "\tgb_write8(wTextBoxLabel_ADDR, (uint8_t)de);",
    "after": "\tgb_write8(wTextBoxLabel_ADDR, (uint8_t)(uint16_t)(de ^ 1u));",
    "case_ids": ["PrintScrollableText_WithTextBoxLabel_NoWait-0"],
}
MUTATIONS["PrintTextNoDelay"] = {
    "source_symbol": "PrintTextNoDelay",
    "before": "\tResetTxRam_WriteToTextHeader(text);",
    "after": "\t;",
    "case_ids": ["PrintTextNoDelay-0"],
}
MUTATIONS["ProcessTextFromID"] = {
    "source_symbol": "ProcessTextFromID",
    "before": "\tProcessText(&text);",
    "after": "\t;",
    "case_ids": ["ProcessTextFromID-0"],
}
MUTATIONS["ProcessTextFromPointerToID"] = {
    "source_symbol": "ProcessTextFromPointerToID",
    "before": "\t\treturn header_result(0, 0, 0, 0, hl);",
    "after": "\t\treturn header_result(0, 0, 0, 0, (uint16_t)(hl ^ 1u));",
    "case_ids": ["ProcessTextFromPointerToID-0"],
}
MUTATIONS["ReadTextHeader"] = {
    "source_symbol": "ReadTextHeader",
    "before": "\treturn text;",
    "after": "\treturn 1u + text;",
    "case_ids": ["ReadTextHeader-0"],
}
MUTATIONS["TwoByteNumberToText_CountLeadingZeros"] = {
    "source_symbol": "TwoByteNumberToText_CountLeadingZeros",
    "before": "\tif (wFontWidth == 0)",
    "after": "\tif (wFontWidth != 0)",
    "case_ids": ["TwoByteNumberToText_CountLeadingZeros-0"],
}
MUTATIONS["WaitForPlayerToAdvanceText"] = {
    "source_symbol": "WaitForPlayerToAdvanceText",
    "before": "\tSetCursorParametersForTextBox(18, 17, SYM_CURSOR_D, SYM_BOX_BOTTOM);",
    "after": "\t;",
    "case_ids": ["WaitForPlayerToAdvanceText-0"],
}
MUTATIONS["ResetTxRam_WriteToTextHeader"] = {
    "source_symbol": "ResetTxRam_WriteToTextHeader",
    "before": "\twWhichTextHeader = 0;",
    "after": "\twWhichTextHeader = (0) ^ 1u;",
    "case_ids": ["ResetTxRam_WriteToTextHeader-0"],
}
MUTATIONS["WriteToTextHeader_MoveToNext"] = {
    "source_symbol": "WriteToTextHeader_MoveToNext",
    "before": "\tout.hl = wWhichTextHeader_ADDR;",
    "after": "\tout.hl = (wWhichTextHeader_ADDR) ^ 1u;",
    "case_ids": ["WriteToTextHeader_MoveToNext-0"],
}
for _rec in SCHEMA2_CASES["InitTextPrinting_ProcessTextFromID"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["InitTextPrinting_ProcessTextFromID"] = {
    "source_symbol": "InitTextPrinting_ProcessTextFromID",
    "before": "ProcessTextHeaderResult InitTextPrinting_ProcessTextFromID(uint8_t d, uint8_t e, uint16_t hl)\n{",
    "after": "ProcessTextHeaderResult InitTextPrinting_ProcessTextFromID(uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["InitTextPrinting_ProcessTextFromID-0"],
}
for _rec in SCHEMA2_CASES["InitTextPrinting_ProcessTextFromPointerToID"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["InitTextPrinting_ProcessTextFromPointerToID"] = {
    "source_symbol": "InitTextPrinting_ProcessTextFromPointerToID",
    "before": "ProcessTextHeaderResult InitTextPrinting_ProcessTextFromPointerToID(uint8_t d, uint8_t e, uint16_t hl)\n{",
    "after": "ProcessTextHeaderResult InitTextPrinting_ProcessTextFromPointerToID(uint8_t d, uint8_t e, uint16_t hl)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["InitTextPrinting_ProcessTextFromPointerToID-0"],
}
for _rec in SCHEMA2_CASES["WriteToTextHeader"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["WriteToTextHeader"] = {
    "source_symbol": "WriteToTextHeader",
    "before": "TextHeaderWrite WriteToTextHeader(uint16_t text)\n{",
    "after": "TextHeaderWrite WriteToTextHeader(uint16_t text)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["WriteToTextHeader-0"],
}
