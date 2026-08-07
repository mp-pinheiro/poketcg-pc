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
}

CASES = {
    "GetTextOffsetFromTextID": [{"hl": 1}, dict(POISON, hl=1)],
    # hl = wTextHeader1 + wWhichTextHeader * 5, and the routine writes no memory at
    # all -- so `expect` alone cannot fail it and the output has to be pinned with
    # `expect_regs`. Selector 1 lands on $CE30, which is wTextHeader2 in poketcg.sym,
    # cross-checking the stride against the symbol table rather than against the port.
    "GetPointerToTextHeader": [
        {"wram": {0xCE48: b"\x00"}, "oracle": False,
         "why": "header selector and the headers themselves are in the synthesized call frame",
         "expect": {0xCE48: b"\x00"}, "expect_regs": {"hl": 0xCE2B}},
        {"wram": {0xCE48: b"\x01"}, "oracle": False,
         "why": "header selector and the headers themselves are in the synthesized call frame",
         "expect": {0xCE48: b"\x01"}, "expect_regs": {"hl": 0xCE30}},
        dict(POISON, wram={0xCE48: b"\x03"}, oracle=False,
             why="header selector and the headers themselves are in the synthesized call frame",
             expect={0xCE48: b"\x03"},
             expect_regs={"hl": 0xCE3A, "b": 0xBB, "c": 0xCC}),
    ],
    "ReadTextHeader": [
        {"wram": {HEADER: b"\x0f\x00\x01\x00\x40"},
         "oracle": False, "why": "text headers occupy the synthesized call frame",
         "expect": {0xFF80: b"\x01"}},
        dict(POISON, wram={HEADER: b"\x06\x01\x02\x34\x56"}, oracle=False,
             why="text headers occupy the synthesized call frame",
             expect={0xFF80: b"\x02"}),
    ],
    "WriteToTextHeader": [
        {"hl": 0x4000, "wram": {0xCE48: b"\x00", HEADER: b"\0" * 5},
         "oracle": False, "why": "text headers occupy the synthesized call frame",
         "expect": {HEADER: b"\0\0\0\0\x40"}},
        dict(POISON, hl=0x5678, wram={0xCE48: b"\x03", HEADER: b"\0" * 5},
             oracle=False, why="text headers occupy the synthesized call frame",
             expect={0xCE3A: b"\0\0\0\x78\x56"}),
    ],
    "WriteToTextHeader_MoveToNext": [
        {"hl": 0x4000, "wram": {0xCE48: b"\x00", HEADER: b"\0" * 5},
         "oracle": False, "why": "text headers occupy the synthesized call frame",
         "expect": {HEADER: b"\0\0\0\0\x40"}},
        dict(POISON, hl=0x5678, wram={0xCE48: b"\x02", HEADER: b"\0" * 5},
             oracle=False, why="text headers occupy the synthesized call frame",
             expect={0xCE35: b"\0\0\0\x78\x56"}),
    ],
    "ResetTxRam_WriteToTextHeader": [
        {"hl": 0x4000, "wram": {0xCE48: b"\x03", HEADER: b"\0" * 5,
                                    0xCE49: b"\x01", 0xCE4A: b"\x02"},
         "oracle": False, "why": "text headers occupy the synthesized call frame",
         "expect": {HEADER: b"\x0f\0\0\0\x40", 0xCE48: b"\0", 0xCE49: b"\0", 0xCE4A: b"\0"}},
        dict(POISON, hl=0x5678, wram={0xCE48: b"\x02", HEADER: b"\0" * 5,
                                      0xCE49: b"\x01", 0xCE4A: b"\x02"},
             oracle=False, why="text headers occupy the synthesized call frame",
             expect={HEADER: b"\x0f\0\0\x78\x56", 0xCE48: b"\0", 0xCE49: b"\0", 0xCE4A: b"\0"}),
    ],
    "TwoByteNumberToText_CountLeadingZeros": [
        {"hl": 0, "wram": {0xCD0A: b"\x01"}, "read": {BUFFER: 6}},
        {"hl": 1, "wram": {0xCD0A: b"\x01"}, "read": {BUFFER: 6}},
        dict(POISON, hl=0xFFFF, wram={0xCD0A: b"\x01"}, read={BUFFER: 6}),
        {"hl": 0, "wram": {0xCD0A: b"\x00"}, "read": {BUFFER: 11}},
    ],
    "CopyText": [
        {"hl": 1, "d": 0xC1, "e": 0x00, "read": {0xC100: 32}},
        dict(POISON, hl=1, d=0xC1, e=0x40, read={0xC140: 32}),
    ],
    "CountLinesOfTextFromID": [{"hl": 1}, dict(POISON, hl=1)],
    "LoadTxRam2": [{"hl": 1}, dict(POISON, hl=0x1234)],
    "LoadTxRam3": [{"hl": 0}, dict(POISON, hl=0xFFFF)],
}
