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
    "Func_2057": {"compare": ("a", "b", "c", "d", "e", "hl"),
                  "preserve": ("b", "c", "d", "e", "hl")},
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
    "Func_2057": [
        {"read": {MAP: 1}},
        dict(POISON, a=0xA5, b=9, c=6, d=4,
             read={MAP + 4 * 32 + 15: 1}),
        {"a": 0x5A, "b": 0xFF, "c": 1, "d": 0,
         "read": {MAP: 1}},
        {"a": 0x3C, "b": 31, "c": 0, "d": 31,
         "read": {MAP + 31 * 32 + 31: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "FillRectangle": {
        "source_symbol": "FillRectangle",
        "before": "uint8_t col_step = (uint8_t)(hl >> 8);",
        "after": "uint8_t col_step = (uint8_t)hl;",
        "case_ids": ["FillRectangle-1", "FillRectangle-2", "FillRectangle-3", "FillRectangle-4"],
    },
    "Func_2057": {
        "source_symbol": "Func_2057",
        "before": "\tuint8_t c = (uint8_t)(x + offset);",
        "after": "\tuint8_t c = (uint8_t)(x - offset);",
        "case_ids": ["Func_2057-1", "Func_2057-2"],
    },
}
