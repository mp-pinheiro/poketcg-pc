POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
HEADER = 0xCE2B
BUFFER = 0xCAA0

CONTRACT = {
    "GetTextOffsetFromTextID": ("b", "c", "d", "e", "hl"),
    "GetPointerToTextHeader": ("b", "c", "hl"),
    "ReadTextHeader": ("b", "c", "hl"),
    "WriteToTextHeader": ("b", "c", "hl"),
    "WriteToTextHeader_MoveToNext": ("b", "c", "hl"),
    "ResetTxRam_WriteToTextHeader": ("b", "c", "hl"),
    "TwoByteNumberToText_CountLeadingZeros": ("b", "c", "d", "e", "hl"),
    "CopyText": ("b", "c", "d", "e", "hl"),
    "CountLinesOfTextFromID": ("a", "b", "c", "d", "e", "hl"),
    "LoadTxRam2": ("b", "c", "d", "e", "hl"),
    "LoadTxRam3": ("b", "c", "d", "e", "hl"),
    "ProcessTextHeader": ("a", "d", "e", "f", "hl"),
    "HandleTxRam2Or3": ("a", "b", "c", "d", "e", "hl"),
    "CopyTextData_FromTextID": ("a", "d", "e", "hl"),
    "CopyPlayerNameOrTurnDuelistName": ("a", "b", "c", "d", "e", "hl"),
    # These four end in ProcessText, whose own CONTRACT is ("hl",): its exit d/e are
    # path-dependent residue, clobbered by Func_22ca on the half-width path and left
    # alone when wFontWidth is FULL_WIDTH. They inherit that, so d/e stay out.
    "InitTextPrinting_ProcessTextFromID": ("b", "c", "hl"),
    "InitTextPrinting_ProcessTextFromPointerToID": ("b", "c", "hl"),
    "ProcessTextFromID": ("b", "c", "hl"),
    "ProcessTextFromPointerToID": ("b", "c", "hl"),
    "PlaceTextItems": ("d", "hl"),
    "PrintText": ("hl",),
    "PrintTextNoDelay": ("hl",),
    "DrawTextReadyLabeledOrRegularTextBox": ("a", "d", "e", "hl"),
}

CASES = {
    "GetTextOffsetFromTextID": [{"hl": 1}, dict(POISON, hl=1)],
    # hl = wTextHeader1 + wWhichTextHeader * 5, and the routine writes no memory at
    # all -- so `expect` alone cannot fail it and the output has to be pinned with
    # `expect_regs`. Selector 1 lands on $CE30, which is wTextHeader2 in poketcg.sym,
    # cross-checking the stride against the symbol table rather than against the port.
    "GetPointerToTextHeader": [
        {"wram": {0xCE48: b"\x00"}, "read": {0xCE48: 1}},
        {"wram": {0xCE48: b"\x01"}, "read": {0xCE48: 1}},
        dict(POISON, wram={0xCE48: b"\x03"}, read={0xCE48: 1}),
    ],
    # Oracle-run: the synthesized frame now sits in $CF00-$CFFF, so the text-header
    # block at $CE2B is seedable and diffable against the real ROM.
    "ReadTextHeader": [
        {"wram": {HEADER: b"\x0f\x00\x01\x00\x40"},
         "read": {HEADER: 5, 0xFF80: 1}},
        dict(POISON, wram={HEADER: b"\x06\x01\x02\x34\x56"},
             read={HEADER: 5, 0xFF80: 1}),
    ],
    "WriteToTextHeader": [
        {"hl": 0x4000, "wram": {0xCE48: b"\x00", HEADER: b"\0" * 5},
         "read": {HEADER: 5, 0xCE48: 1}},
        dict(POISON, hl=0x5678, wram={0xCE48: b"\x03", HEADER: b"\0" * 5},
             read={HEADER: 5, 0xCE3A: 5, 0xCE48: 1}),
    ],
    "WriteToTextHeader_MoveToNext": [
        {"hl": 0x4000, "wram": {0xCE48: b"\x00", HEADER: b"\0" * 5},
         "read": {HEADER: 5, 0xCE48: 1}},
        dict(POISON, hl=0x5678, wram={0xCE48: b"\x02", HEADER: b"\0" * 5},
             read={HEADER: 5, 0xCE35: 5, 0xCE48: 1}),
    ],
    "ResetTxRam_WriteToTextHeader": [
        {"hl": 0x4000, "wram": {0xCE48: b"\x03", HEADER: b"\0" * 5,
                                0xCE49: b"\x01", 0xCE4A: b"\x02"},
         "read": {HEADER: 5, 0xCE3A: 5, 0xCE48: 1, 0xCE49: 1, 0xCE4A: 1}},
        dict(POISON, hl=0x5678, wram={0xCE48: b"\x02", HEADER: b"\0" * 5,
                                      0xCE49: b"\x01", 0xCE4A: b"\x02"},
             read={HEADER: 5, 0xCE35: 5, 0xCE48: 1, 0xCE49: 1, 0xCE4A: 1}),
    ],
    "TwoByteNumberToText_CountLeadingZeros": [
        {"hl": 0, "wram": {0xCD0A: b"\x01"}, "read": {BUFFER: 6}},
        {"hl": 1, "wram": {0xCD0A: b"\x01"}, "read": {BUFFER: 6}},
        dict(POISON, hl=0xFFFF, wram={0xCD0A: b"\x01"}, read={BUFFER: 6}),
        {"hl": 0, "wram": {0xCD0A: b"\x00"}, "read": {BUFFER: 11}},
    ],
    "CopyText": [
        {"hl": 1, "d": 0xC1, "e": 0x00, "read": {0xC100: 32}},
        {"hl": 0, "d": 0xC1, "e": 0x00, "wram": {0xFF97: b"\x00"},
         "sram": {0: {0xA010: b"\x21\x00"}}, "read": {0xC100: 2}},
        {"hl": 0, "d": 0xC1, "e": 0x20, "wram": {0xFF97: b"\x01", 0xC500: b"\x31\x00"},
         "read": {0xC120: 2}},
    ],
    "CountLinesOfTextFromID": [{"hl": 1}, dict(POISON, hl=1)],
    # wTxRam2 is $CE3F and the asm writes it and $CE40. wTxRam2_b is a DIFFERENT
    # symbol at $CE41 and must stay untouched -- the third read byte pins that.
    # Oracle-run now that the synthesized frame moved out to $CF00-$CFFF.
    "LoadTxRam2": [
        {"hl": 1, "wram": {0xCE3F: b"\xff\xff\xff"}, "read": {0xCE3F: 3}},
        dict(POISON, hl=0x1234, wram={0xCE3F: b"\xff\xff\xff"}, read={0xCE3F: 3}),
    ],
    "LoadTxRam3": [
        {"hl": 0, "wram": {0xCE43: b"\xff\xff\xff"}, "read": {0xCE43: 3}},
        dict(POISON, hl=0xFFFF, wram={0xCE43: b"\xff\xff\xff"}, read={0xCE43: 3}),
    ],
}

CASES.update({
    # No text engine involved: a bounded copy of at most a tiles, so this runs on the
    # oracle against the real ROM. e comes back as the actual character count.
    "CopyTextData_FromTextID": [
        {"a": 8, "hl": 1, "d": 0xC1, "e": 0x00, "read": {0xC100: 10}},
        {"a": 2, "hl": 1, "d": 0xC1, "e": 0x00, "read": {0xC100: 4}},
        dict(POISON, a=8, hl=1, d=0xC1, e=0x00, read={0xC100: 10}),
    ],
    # hWhoseTurn selects the callee; hl always comes back as the buffer the asm
    # pushed and popped, whichever name was copied.
    "CopyPlayerNameOrTurnDuelistName": [
        {"wram": {0xFF97: b"\x00"}, "sram": {0: {0xA010: b"\x41\x42\x00"}},
         "read": {BUFFER: 4}},
        # OPPONENT_TURN is HIGH(wOpponentDuelVariables) = $C3. With no text ID at
        # wOpponentName the opponent path falls back to the name buffer.
        {"wram": {0xFF97: b"\xC3", 0xCC16: b"\x00\x00", 0xC500: b"\x43\x44\x00"},
         "read": {BUFFER: 4}},
        dict(POISON, wram={0xFF97: b"\x00"}, sram={0: {0xA010: b"\x45\x00"}},
             read={BUFFER: 3}),
    ],
    # Text ID 0 resolves to an immediately terminated text, so ProcessText returns
    # without generating tiles. The multi-pair half-width case (id 1, "Hand") is
    # appended after CACHE_READ is defined -- it needs a SetupText prelude so the
    # cache is acyclic and the oracle returns.
    "ProcessTextFromID": [
        {"hl": 0, "wram": {0xCABB: b"\x00"}},
        dict(POISON, hl=0, wram={0xCABB: b"\x00"}),
    ],
    "InitTextPrinting_ProcessTextFromID": [
        {"hl": 0, "d": 0, "e": 0, "wram": {0xCABB: b"\x00"}},
        dict(POISON, hl=0, d=1, e=2, wram={0xCABB: b"\x00"}),
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
         "wram": {HEADER: b"\x0f\x00\x01\x00\xC1", 0xCE48: b"\x00",
                  0xC100: b"\x00"},
         "read": {HEADER: 5, 0xCE48: 1, 0xC100: 1}},
        # A pending header level is popped and the routine re-runs one level up:
        # wWhichTextHeader selects the header, five bytes per level.
        {"d": 5, "e": 6,
         "wram": {HEADER: b"\x0f\x00\x01\x00\xC1",
                  HEADER + 5: b"\x0f\x00\x01\x00\xC1",
                  0xCE48: b"\x01", 0xC100: b"\x00"},
         "read": {HEADER: 10, 0xCE48: 1, 0xC100: 1}},
    ],
    # The zero-ID early exit returns before any text processing, so it is the one
    # path of this pair the emulator can run end to end.
    "InitTextPrinting_ProcessTextFromPointerToID": [
        {"hl": 0xC100, "d": 0, "e": 0, "wram": {0xC100: b"\x00\x00"},
         "read": {0xC100: 2}},
        dict(POISON, hl=0xC100, d=0, e=0, wram={0xC100: b"\x00\x00"},
             read={0xC100: 2}),
    ],

    "HandleTxRam2Or3": [
        # The asm ends `ld a, [hli] / ld h, [hl] / ld l, a`, so hl is the 16-bit value
        # held in the slot, not the slot address. Index 0 reads the first slot.
        {"hl": 0xCE49, "d": 0xCE, "e": 0x3F, "wram": {0xCE49: b"\x00", 0xCE3F: b"\x34\x12"},
         "oracle": False, "why": "text buffers are in the synthesized call frame",
         "expect": {0xCE49: b"\x01"}, "expect_regs": {"hl": 0x1234}},
        # Index 2 selects the third slot: `add a` doubles it, so the offset is 4.
        {"hl": 0xCE49, "d": 0xCE, "e": 0x3F,
         "wram": {0xCE49: b"\x02", 0xCE43: b"\x78\x56"},
         "oracle": False, "why": "text buffers are in the synthesized call frame",
         "expect": {0xCE49: b"\x03"}, "expect_regs": {"hl": 0x5678}},
        # `add a` is 8-bit, so an index of $80 doubles to 0 and wraps onto slot 0.
        {"hl": 0xCE49, "d": 0xCE, "e": 0x3F,
         "wram": {0xCE49: b"\x80", 0xCE3F: b"\xCD\xAB"},
         "oracle": False, "why": "text buffers are in the synthesized call frame",
         "expect": {0xCE49: b"\x81"}, "expect_regs": {"hl": 0xABCD}},
    ],
    "ProcessTextFromPointerToID": [
        {"hl": 0xC100, "wram": {0xC100: b"\x00\x00"}, "oracle": False,
         "why": "the zero text ID path is independent of the ROM text table",
         "expect": {0xC100: b"\x00\x00"}, "expect_regs": {"hl": 0xC101}},
    ],
})

# Real text id 1 ("\x06Hand\x00") drives the half-width tile cache across two
# character pairs, so the whole cache -- key1 $C6xx, key2 $C7xx, next $C8xx,
# prev $C9xx -- is diffed against the oracle. wCurTextTile ($CD05) and
# wFontWidth ($CD0A) pin the placed tile id and the half-width mode.
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
# InitTextPrinting's whole observable effect is the print cursor: hTextBGMap0Address
# ($FFAA-$FFAB, the BG-map destination DECoordToBGMap0Address derives from d/e) and
# hTextHorizontalAlign ($FFAD, d itself). Without these a routine that places items
# at the wrong coordinates still passes -- swapping InitTextPrinting(d, e) to (e, d)
# was verified green before they were added.
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES.update({
    # Item format is [x][y][text-id lo][text-id hi] per item, bit 7 of x terminates.
    "PlaceTextItems": [
        {"hl": 0xC100, "wram": {0xC100: b"\x80"}},
        dict(POISON, hl=0xC100, wram={0xC100: b"\x80"}),
        {"hl": 0xC100, "wram": {0xC100: b"\x01\x02\x01\x00\x80"},
         "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
    ],
    # Non-labeled branch draws a 20x6 box at BG-map row 12 ($9980 under zero scroll)
    # then arms text printing at (1,14). wIsTextBoxLabeled lives in the synthesized
    # frame ($CE4B) so the labeled branch cannot be oracle-driven and is left to the C.
    "DrawTextReadyLabeledOrRegularTextBox": [
        {"hl": 0xC100, "read": {0x9980: 64}},
        dict(POISON, hl=0xC100, read={0x9980: 64}),
    ],
    # hl == 0 takes the wDefaultText path (no bank save/restore); a zero first byte
    # is TX_END so the body exits after one ProcessTextHeader. wTextSpeed ($CE47)
    # is inside the synthesized frame and cannot be seeded, so it stays 0: the
    # DoFrame delay loop runs zero iterations. Seeding hKeysHeld=PAD_B takes the
    # B-skip branch (TEXT_SPEED_4 path); at speed 0 its output matches the no-B
    # case because both skip every DoFrame, but it exercises the hKeysHeld read.
    "PrintText": [
        {"hl": 0, "d": 0, "e": 0, "wram": {0xC590: b"\x00"}},
        dict(POISON, hl=0, wram={0xC590: b"\x00"}),
        {"hl": 1, "d": 0, "e": 0, "setup": SETUP, "read": dict(CACHE_READ),
         "vread": VRAM_READ},
        {"hl": 1, "d": 0, "e": 0, "wram": {0xFF90: b"\x02"},
         "setup": SETUP, "read": dict(CACHE_READ), "vread": VRAM_READ},
    ],
    # No hl==0 shortcut: hl is always a text id. id 0 resolves to an immediate
    # TX_END; id 1 ("Hand") runs the engine.
    "PrintTextNoDelay": [
        {"hl": 0, "d": 0, "e": 0},
        {"hl": 1, "d": 0, "e": 0, "setup": SETUP, "read": dict(CACHE_READ),
         "vread": VRAM_READ},
        dict(POISON, hl=1, d=0, e=0, setup=SETUP, read=dict(CACHE_READ), vread=VRAM_READ),
    ],
})
# GenerateTextTile's product is the tile itself, copied into VRAM. Without a vread
# the cache keys are checked but the generated tile is not: swapping its d/e
# arguments was verified green before this span was added.
CASES["ProcessTextFromID"].append(
    {"hl": 1, "setup": SETUP, "read": dict(CACHE_READ), "vread": VRAM_READ})

# WaitForPlayerToAdvanceText, PrintScrollableText and its three wrappers are NOT
# registered. WaitForPlayerToAdvanceText -> WaitForButtonAorB spins on hKeysPressed
# waiting for A or B; nothing under the oracle advances it, so it never returns.
# This is a genuine input wait, not the hBankROM/farcall hang: the wait chain
# (SetCursorParametersForTextBox, WaitForButtonAorB -> DoFrame/RefreshMenuCursor)
# contains no BankswitchROM and no farcall, so an unset hBankROM cannot divert it.
# The wrappers transitively reach the same wait, and their C bodies additionally
# depend on the unported menu routines SetCursorParametersForTextBox /
# WaitForButtonAorB / RefreshMenuCursor / EraseCursor, which are outside this
# slice's files. Blocking on a harness input-injection facility (the oracle runs
# with no_input=True and exposes no per-frame button seed).
