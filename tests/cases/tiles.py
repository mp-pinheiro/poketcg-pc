SRC = 0xC100
DST = 0x8000
MAP = 0x9800
PAT = bytes((i * 37 + 11) & 0xFF for i in range(1024))
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wConsole = 0xCAB4
CONSOLE_DMG = 0x01
CONSOLE_CGB = 0x02
wLoadedCard1Type = 0xCC24
TYPE_TRAINER = 0x10

V0_TILES0 = 0x8000
V0_TILES1 = 0x8800
V0_TILES2 = 0x9000
S_GFX_BUFFER1 = 0xA400
S_GFX_BUFFER4 = 0xB000

SYMBOLS_FONT_FAR = 0x2968
DUEL_CARD_HEADER_GFX_FAR = 0x2ce8
DUEL_OTHER_GFX = 0x4008

CONTRACT = {
    "FillRectangle": {"compare": ("d", "e"), "preserve": ("d", "e")},
    "Copy1bppTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "CopyFontsOrDuelGraphicsTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadSymbolsFont": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadCardSet2Tiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDuelDrawCardsScreenTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadCardOrDuelMenuBorderTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadCardTypeHeaderTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDuelCardSymbolTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDuelCardSymbolTiles2": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDuelFaceDownCardTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDuelCheckPokemonScreenTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadPlacingThePrizesScreenTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDeckAndDiscardPileIcons": {"compare": ("d", "e", "hl"), "preserve": ()},
    "LoadDuelCoinTossResultTiles": {"compare": ("d", "e", "hl"), "preserve": ()},
    "Func_212f": {"compare": ("d", "e", "hl"), "preserve": ()},
    "DrawDuelBoxMessage": {"compare": (), "preserve": ()},
    "LoadFullWidthFontTiles": {"compare": (), "preserve": ()},
}

CASES = {
    "FillRectangle": [
        {"oracle": False, "why": "256 by 256 writes exceed the oracle frame budget.",
         "expect": {MAP: b"\0"}},
        dict(POISON, a=0x12, b=1, c=1, d=3, e=2, hl=0x0201,
             read={MAP: 0x400}),
        {"a": 0x40, "b": 0, "c": 1, "d": 0, "e": 0, "hl": 0x0101,
         "oracle": False, "why": "256 columns exceed the oracle frame budget.",
         "expect": {MAP + 255: b"\x3f"}},
        # h != l with b > 1, c > 1: distinguishes column step (h) from row step
        # (l). A port that swaps them still passes every other case here because
        # b=1/c=1 cases have no increment and hl=0x0101 is symmetric.
        {"a": 0x10, "b": 2, "c": 2, "d": 0, "e": 0, "hl": 0x0201,
         "read": {MAP: 1, MAP + 1: 1, MAP + 32: 1, MAP + 33: 1}},
    ],
    "Copy1bppTiles": [
        {},
        dict(POISON, hl=DST, d=SRC >> 8, e=SRC & 0xff,
             wram={SRC: PAT}, read={DST: 2048}),
    ],
    "CopyFontsOrDuelGraphicsTiles": [
        {},
        # extraction=0: hl < $4000 selects BANK_FONTS itself (0x1d).
        dict(POISON, hl=DUEL_CARD_HEADER_GFX_FAR, d=V0_TILES1 >> 8, e=0, b=1,
             vread={0: {V0_TILES1: 16}}),
        # extraction=1: hl >= $4000 selects BANK_FONTS+1 (0x1e).
        {"hl": DUEL_OTHER_GFX, "d": V0_TILES1 >> 8, "e": 0x40, "b": 1,
         "vread": {0: {V0_TILES1 + 0x40: 16}}},
        # b=0 boundary: 256 blocks, fills v0Tiles0 and v0Tiles1 entirely.
        {"hl": SYMBOLS_FONT_FAR, "d": V0_TILES0 >> 8, "e": 0, "b": 0,
         "vread": {0: {V0_TILES0: 4096}}},
    ],
    "LoadSymbolsFont": [
        {"vread": {0: {V0_TILES2: 896}}},
        dict(POISON, vread={0: {V0_TILES2: 896}}),
    ],
    "LoadCardSet2Tiles": [
        # PRO/NONE (index 0): no icon, destination stays untouched.
        {"vread": {0: {V0_TILES1 + 0x7C0: 64}}},
        {"a": 1, "vread": {0: {V0_TILES1 + 0x7C0: 64}}},  # JUNGLE, offset 0
        {"a": 2, "vread": {0: {V0_TILES1 + 0x7C0: 64}}},  # FOSSIL, offset 0x40
        {"a": 7, "vread": {0: {V0_TILES1 + 0x7C0: 64}}},  # GB, offset 0x80
        dict(POISON, a=1, vread={0: {V0_TILES1 + 0x7C0: 64}}),
        dict(POISON, a=3, vread={0: {V0_TILES1 + 0x7C0: 64}}),  # no icon
    ],
    "LoadDuelDrawCardsScreenTiles": [
        {"vread": {0: {V0_TILES1 + 0x740: 128}}},
        dict(POISON, vread={0: {V0_TILES1 + 0x740: 128}}),
    ],
    "LoadCardOrDuelMenuBorderTiles": [
        {"vread": {0: {V0_TILES1 + 0x500: 128}}},
        dict(POISON, vread={0: {V0_TILES1 + 0x500: 128}}),
    ],
    "LoadCardTypeHeaderTiles": [
        {"vread": {0: {V0_TILES1 + 0x600: 256}}},
        {"a": 1, "vread": {0: {V0_TILES1 + 0x600: 256}}},
        {"a": 2, "vread": {0: {V0_TILES1 + 0x600: 256}}},
        dict(POISON, a=1, vread={0: {V0_TILES1 + 0x600: 256}}),
    ],
    "LoadDuelCardSymbolTiles": [
        {"wram": {wConsole: bytes([CONSOLE_DMG])},
         "vread": {0: {V0_TILES1 + 0x500: 768}}},
        {"wram": {wConsole: bytes([CONSOLE_CGB])},
         "vread": {0: {V0_TILES1 + 0x500: 768}}},
        dict(POISON, wram={wConsole: bytes([CONSOLE_CGB])},
             vread={0: {V0_TILES1 + 0x500: 768}}),
    ],
    "LoadDuelCardSymbolTiles2": [
        {"wram": {wConsole: bytes([CONSOLE_DMG])},
         "vread": {0: {V0_TILES1 + 0x540: 192}}},
        {"wram": {wConsole: bytes([CONSOLE_CGB])},
         "vread": {0: {V0_TILES1 + 0x540: 192}}},
        dict(POISON, wram={wConsole: bytes([CONSOLE_CGB])},
             vread={0: {V0_TILES1 + 0x540: 192}}),
    ],
    "LoadDuelFaceDownCardTiles": [
        {"wram": {wConsole: bytes([CONSOLE_DMG])},
         "vread": {0: {V0_TILES1 + 0x500: 256}}},
        {"wram": {wConsole: bytes([CONSOLE_CGB])},
         "vread": {0: {V0_TILES1 + 0x500: 256}}},
        dict(POISON, wram={wConsole: bytes([CONSOLE_CGB])},
             vread={0: {V0_TILES1 + 0x500: 256}}),
    ],
    "LoadDuelCheckPokemonScreenTiles": [
        {"wram": {wConsole: bytes([CONSOLE_DMG])},
         "vread": {0: {V0_TILES1 + 0x500: 576}}},
        {"wram": {wConsole: bytes([CONSOLE_CGB])},
         "vread": {0: {V0_TILES1 + 0x500: 576}}},
        dict(POISON, wram={wConsole: bytes([CONSOLE_CGB])},
             vread={0: {V0_TILES1 + 0x500: 576}}),
    ],
    "LoadPlacingThePrizesScreenTiles": [
        # Falls through into LoadDeckAndDiscardPileIcons (port-contract.md's
        # fallthrough list): both copies must land.
        {"wram": {wConsole: bytes([CONSOLE_DMG])},
         "vread": {0: {V0_TILES1 + 0x200: 208, V0_TILES1 + 0x500: 768}}},
        {"wram": {wConsole: bytes([CONSOLE_CGB])},
         "vread": {0: {V0_TILES1 + 0x200: 208, V0_TILES1 + 0x500: 768}}},
        dict(POISON, wram={wConsole: bytes([CONSOLE_CGB])},
             vread={0: {V0_TILES1 + 0x200: 208, V0_TILES1 + 0x500: 768}}),
    ],
    "LoadDeckAndDiscardPileIcons": [
        {"wram": {wConsole: bytes([CONSOLE_DMG])},
         "vread": {0: {V0_TILES1 + 0x500: 768}}},
        {"wram": {wConsole: bytes([CONSOLE_CGB])},
         "vread": {0: {V0_TILES1 + 0x500: 768}}},
        dict(POISON, wram={wConsole: bytes([CONSOLE_CGB])},
             vread={0: {V0_TILES1 + 0x500: 768}}),
    ],
    "LoadDuelCoinTossResultTiles": [
        {"vread": {0: {V0_TILES2 + 0x300: 128}}},
        dict(POISON, vread={0: {V0_TILES2 + 0x300: 128}}),
    ],
    "Func_212f": [
        {"wram": {wLoadedCard1Type: bytes([TYPE_TRAINER])},
         "sram": {1: {S_GFX_BUFFER1: b"\0"}}, "ramg": True,
         "read": {S_GFX_BUFFER1: 768, S_GFX_BUFFER1 + 0x300: 128,
                  S_GFX_BUFFER1 + 0x380: 64, S_GFX_BUFFER4: 768}},
        dict(POISON, wram={wLoadedCard1Type: bytes([TYPE_TRAINER])},
             sram={1: {S_GFX_BUFFER1: b"\0"}}, ramg=True,
             read={S_GFX_BUFFER1: 768, S_GFX_BUFFER1 + 0x300: 128,
                   S_GFX_BUFFER1 + 0x380: 64, S_GFX_BUFFER4: 768}),
    ],
    "DrawDuelBoxMessage": [
        {"vread": {0: {V0_TILES1 + 0x200: 640}},
         "read": {0x9885: 10, 0x98A5: 10, 0x98C5: 10, 0x98E5: 10}},
        {"a": 6, "vread": {0: {V0_TILES1 + 0x200: 640}},
         "read": {0x9885: 10, 0x98A5: 10, 0x98C5: 10, 0x98E5: 10}},
        dict(POISON, a=3, vread={0: {V0_TILES1 + 0x200: 640}},
             read={0x9885: 10, 0x98A5: 10, 0x98C5: 10, 0x98E5: 10}),
    ],
    "LoadFullWidthFontTiles": [
        {"vread": {0: {V0_TILES0: 1024, V0_TILES1: 1024, V0_TILES2: 1024}}},
        dict(POISON,
             vread={0: {V0_TILES0: 1024, V0_TILES1: 1024, V0_TILES2: 1024}}),
    ],
}
# >>> factory Func_2057
CONTRACT["Func_2057"] = {"compare": ("d", "e"), "preserve": ("d",)}
CASES["Func_2057"] = [
        {"vread": {0: {MAP: 1}}},
        {"hl": SRC, "wram": {SRC: b"\x99"}, "vread": {0: {MAP: 1}}},
        dict(POISON,
             oracle=False,
             why="a/b/c stand in for Func_1f96's not-yet-ported local frame "
                 "(sp+2/sp+6/sp+7); a live call can only supply the "
                 "harness's own zeroed $CF00-$CFFF window there, never "
                 "these poison bytes, so the frame arithmetic is asm-"
                 "derived rather than oracle-run.",
             expect_regs={"e": 0xFF, "d": 0xDD}),
    ]
# <<< factory Func_2057

# >>> factory Func_2051
CONTRACT["Func_2051"] = {"compare": ("d", "e"), "preserve": ("d",)}
CASES["Func_2051"] = [
    {"hl": SRC, "wram": {SRC: b"\x00", SRC + 1: b"\x42"}, "vread": {0: {MAP: 1}}},
    dict(POISON,
         hl=SRC, wram={SRC: b"\x99"},
         oracle=False,
         why=("Func_2051 overwrites hl via `ld hl, sp+9` before falling through into Func_2057, and Func_2057 itself re-derives frame_c/frame_lo/frame_hi from sp+2/sp+6/sp+7 -- every one of those addresses lands in the harness's own synthesized call frame when this routine is invoked in isolation (both the PyBoy oracle's zeroed $CF00-$CFFF window and GBRT's own return-address frame), so a live call can only exercise the all-zero path. Non-zero frame content -- what Func_1f96, once ported, would supply through its own real local-frame bytes -- is asm-derived rather than oracle-run."),
         expect_regs={"e": 0x99, "d": 0xDD}),
    dict(POISON,
         oracle=False,
         why=("Func_2051 overwrites hl via `ld hl, sp+9` before falling through into Func_2057, and Func_2057 itself re-derives frame_c/frame_lo/frame_hi from sp+2/sp+6/sp+7 -- every one of those addresses lands in the harness's own synthesized call frame when this routine is invoked in isolation (both the PyBoy oracle's zeroed $CF00-$CFFF window and GBRT's own return-address frame), so a live call can only exercise the all-zero path. Non-zero frame content -- what Func_1f96, once ported, would supply through its own real local-frame bytes -- is asm-derived rather than oracle-run."),
         expect_regs={"e": 0xFF, "d": 0xDD}),
]
# <<< factory Func_2051

# >>> factory Func_2055
CONTRACT["Func_2055"] = {"compare": ("d", "e"), "preserve": ("d",)}
CASES["Func_2055"] = [
    {"hl": SRC, "wram": {SRC: b"\x00", SRC + 1: b"\x42"}, "vread": {0: {MAP: 1}}},
    dict(POISON,
         hl=SRC, wram={SRC: b"\x99"},
         oracle=False,
         why=("Func_2055 overwrites hl via `ld hl, sp+8` before falling through into Func_2057, and Func_2057 itself re-derives frame_c/frame_lo/frame_hi from sp+2/sp+6/sp+7 -- every one of those addresses lands in the harness's own synthesized call frame when this routine is invoked in isolation (both the PyBoy oracle's zeroed $CF00-$CFFF window and GBRT's own return-address frame), so a live call can only exercise the all-zero path. Non-zero frame content -- what Func_1f96, once ported, would supply through its own real local-frame bytes -- is asm-derived rather than oracle-run."),
         expect_regs={"e": 0x99, "d": 0xDD}),
    dict(POISON,
         oracle=False,
         why=("Func_2055 overwrites hl via `ld hl, sp+8` before falling through into Func_2057, and Func_2057 itself re-derives frame_c/frame_lo/frame_hi from sp+2/sp+6/sp+7 -- every one of those addresses lands in the harness's own synthesized call frame when this routine is invoked in isolation (both the PyBoy oracle's zeroed $CF00-$CFFF window and GBRT's own return-address frame), so a live call can only exercise the all-zero path. Non-zero frame content -- what Func_1f96, once ported, would supply through its own real local-frame bytes -- is asm-derived rather than oracle-run."),
         expect_regs={"e": 0xFF, "d": 0xDD}),
]
# <<< factory Func_2055

# >>> factory Func_2046
CONTRACT["Func_2046"] = {"compare": (), "preserve": ()}
CASES["Func_2046"] = [
    {"d": 0xC1, "e": 0x00, "hl": 0xC200,
     "wram": {0xC201: b"\x42"},
     "vread": {0: {MAP: 1}}},
    {"d": 0xC3, "e": 0x00,
     "wram": {0xC300: b"\x07"},
     "oracle": False,
     "why": "counter_addr stands in for Func_1f96's not-yet-ported sp+3 "
            "local; a live call always sees that frame byte as 0 (the "
            "harness's own zeroed/return-address frame), so a nonzero "
            "low nibble -- the early-return path -- can only be driven "
            "through an asm-derived case.",
     "expect": {0xC300: b"\x08"}},
    {"d": 0xC3, "e": 0x01, "hl": 0xC302, "a": 0x05, "b": 0x02, "c": 0x01,
     "wram": {0xC301: b"\x00", 0xC302: b"\x77"},
     "oracle": False,
     "why": "frame_c/frame_lo/frame_hi stand in for sp+2/sp+6/sp+7 of the "
            "same not-yet-ported frame; a live call always sees them (and "
            "sp+3/sp+8) as 0, so nonzero row/column arithmetic through the "
            "Func_2055 branch can only be driven through an asm-derived "
            "case.",
     "expect": {0xC301: b"\x01"},
     "expect_vram": {0: {0x98E1: b"\x77"}}},
    {"d": 0xC3, "e": 0x03, "hl": 0xC304, "a": 0x03, "b": 0x04, "c": 0x00,
     "wram": {0xC303: b"\x10", 0xC304: b"\x99", 0xC305: b"\x55"},
     "oracle": False,
     "why": "old=0x10 selects the Func_2051 branch (bit 4 of the "
            "incremented counter set); the real counter frame byte is "
            "always 0 on an isolated call, so this branch -- and its "
            "hl8+1 (sp+9) dereference -- can only be driven through an "
            "asm-derived case.",
     "expect": {0xC303: b"\x11"},
     "expect_vram": {0: {0x98E0: b"\x55"}}},
    dict(POISON,
         wram={0xDDEE: b"\x11"},
         oracle=False,
         why="Poisoned frame_c/frame_lo/frame_hi/hl8 alongside a nonzero "
             "counter low nibble at counter_addr (=de=0xDDEE): proves the "
             "early return is taken -- and nothing else is touched -- even "
             "under maximally hostile register state; the counter frame is "
             "never live-driveable to a nonzero low nibble.",
         expect={0xDDEE: b"\x12"}),
]
# <<< factory Func_2046

# >>> factory Func_1f96
CONTRACT["Func_1f96"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_1f96"] = [
    {"a": 0x00, "d": 0xC1, "e": 0x00,
     "wram": {0xC100: b"\x00\x00\x00\x00\x00\x00\x00", 0xCABB: b"\x00"},
     "keys": [0x00, 0x01]},
    dict(POISON, d=0xC1, e=0x00,
         wram={0xC100: b"\x00\x00\x00\x00\x00\x00\x00", 0xCABB: b"\x00"},
         keys=[0x00, 0x01]),
]
# <<< factory Func_1f96

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "FillRectangle": {
        "source_symbol": "FillRectangle",
        "before": "uint8_t col_step = (uint8_t)(hl >> 8);",
        "after": "uint8_t col_step = (uint8_t)hl;",
        "case_ids": ["FillRectangle-3", "FillRectangle-1", "FillRectangle-2", "FillRectangle-4"],
    },
}
# >>> factory-mutation Func_2057
MUTATIONS["Func_2057"] = {
        "source_symbol": "Func_2057",
        "before": "uint8_t value = gb_read8(hl);",
        "after": "uint8_t value = gb_read8((uint16_t)(hl + 1u));",
        "case_ids": ["Func_2057-1"],
    }
# <<< factory-mutation Func_2057
# >>> factory-mutation Func_2051
MUTATIONS["Func_2051"] = {
    "source_symbol": "Func_2051",
    "before": "uint8_t Func_2051(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)\n{\n\treturn Func_2057(hl, frame_c, frame_lo, frame_hi);",
    "after": "uint8_t Func_2051(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)\n{\n\treturn Func_2057((uint16_t)(hl + 1u), frame_c, frame_lo, frame_hi);",
    "case_ids": ["Func_2051-0"],
}
# <<< factory-mutation Func_2051
# >>> factory-mutation Func_2055
MUTATIONS["Func_2055"] = {
    "source_symbol": "Func_2055",
    "before": "uint8_t Func_2055(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)\n{\n\treturn Func_2057(hl, frame_c, frame_lo, frame_hi);",
    "after": "uint8_t Func_2055(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)\n{\n\treturn Func_2057((uint16_t)(hl + 1u), frame_c, frame_lo, frame_hi);",
    "case_ids": ["Func_2055-0"],
}
# <<< factory-mutation Func_2055
# >>> factory-mutation Func_2046
MUTATIONS["Func_2046"] = {
    "source_symbol": "Func_2046",
    "before": "Func_2055(hl8, frame_c, frame_lo, frame_hi);",
    "after": "Func_2055((uint16_t)(hl8 + 1u), frame_c, frame_lo, frame_hi);",
    "case_ids": ["Func_2046-0"],
}
# <<< factory-mutation Func_2046
# >>> factory-mutation Func_1f96
MUTATIONS["Func_1f96"] = {
    "source_symbol": "Func_1f96",
    "before": "Func1f96Result Func_1f96(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl)\n{\n\tuint16_t table = de;\n\tuint8_t selected = a;",
    "after": "Func1f96Result Func_1f96(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl)\n{\n\tuint16_t table = de;\n\tuint8_t selected = (uint8_t)(a + 1u);",
    "case_ids": ["Func_1f96-0"]
}
# <<< factory-mutation Func_1f96
