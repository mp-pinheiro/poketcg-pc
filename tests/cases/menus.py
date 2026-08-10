SRC = 0xC100
CURSOR_STATE = 0xCD0F

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}


CONTRACT = {
    "InitializeCardListParameters": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "InitializeMenuParameters": {"compare": ("c", "hl"), "preserve": ("c",)},
    "SetMenuItem": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "OneByteNumberToTxSymbol": {"compare": ("a", "hl"), "preserve": ()},
    "OneByteNumberToTxSymbol_PadSpace": {"compare": ("a", "hl"), "preserve": ()},
    "OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign": {"compare": ("b", "c", "d", "hl"), "preserve": ("b", "c", "d")},
    "CardTypeToSymbolID": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetCardSymbolData": {"compare": ("d", "e", "hl"), "preserve": ("d", "e")},
    "SetCursorParametersForTextBox": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("d", "e")},
    "SetCursorParametersForTextBox_Default": {"compare": ("d", "e", "f"), "preserve": ("d", "e")},
}

PARAMS8 = bytes(range(8))
PARAMS9 = bytes(range(9))
CASES = {
    "InitializeCardListParameters": [
        {"hl": SRC, "wram": {SRC: PARAMS9}},
        dict(POISON, a=7, d=3, e=2, hl=SRC, wram={SRC: PARAMS9}),
    ],
    "InitializeMenuParameters": [
        {"hl": SRC, "wram": {SRC: PARAMS8}},
        dict(POISON, a=4, hl=SRC, wram={SRC: PARAMS8}),
    ],
    "SetMenuItem": [
        {},
        dict(POISON, a=5),
    ],
    "OneByteNumberToTxSymbol": [
        {"read": {0xC590: 3}},
        dict(POISON, a=9, read={0xC590: 3}),
        {"a": 10, "read": {0xC590: 3}},
        {"a": 99, "read": {0xC590: 3}},
        {"a": 255, "read": {0xC590: 3}},
    ],
    "OneByteNumberToTxSymbol_PadSpace": [
        {"read": {0xC590: 3}},
        {"a": 9, "read": {0xC590: 3}},
        dict(POISON, a=42, read={0xC590: 3}),
        {"a": 10, "read": {0xC590: 3}},
        {"a": 99, "read": {0xC590: 3}},
        {"a": 255, "read": {0xC590: 3}},
    ],
    "OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign": [
        {"read": {0xC590: 3}},
        {"a": 9, "read": {0xC590: 3}},
        dict(POISON, a=7, read={0xC590: 3}),
        {"a": 10, "read": {0xC590: 3}},
        {"a": 99, "read": {0xC590: 3}},
        {"a": 255, "read": {0xC590: 3}},
    ],
    "CardTypeToSymbolID": [
        {"wram": {0xCC24: b"\x00"}},
        dict(POISON, wram={0xCC24: b"\x07"}),
        {"wram": {0xCC24: b"\x08"}},
        {"wram": {0xCC24: b"\x0f"}},
        {"wram": {0xCC24: b"\x10", 0xCC2D: b"\x03"}},
    ],
    "GetCardSymbolData": [
        {"wram": {0xCC24: b"\x00", 0xCC2D: b"\x00"}},
        dict(POISON, wram={0xCC24: b"\x10", 0xCC2D: b"\x02"}),
        {"wram": {0xCC24: b"\x08"}},
    ],
    "SetCursorParametersForTextBox": [
        {"d": 3, "e": 4, "b": 0x12, "c": 0x34},
        dict(POISON, d=7, e=8, b=0x56, c=0x78),
        {"d": 3, "e": 4, "b": 0x12, "c": 0x34, "oracle": False,
         "why": "cursor state is inside the synthesized frame",
		"expect": {CURSOR_STATE: bytes([0, 0, 3, 4, 0, 1, 0x12, 0x34])}},
    ],
    # The label intentionally falls through into WaitForButtonAorB after the
    # setup call (menus.asm:709-716), so a standalone oracle invocation waits
    # forever. SYM_CURSOR_R is resolved from charmaps.asm:444 as $0F.
    "SetCursorParametersForTextBox_Default": [
        {"d": 2, "e": 5, "keys": 0x01,
         "read": {CURSOR_STATE: 8}},
        dict(POISON, d=9, e=1, keys=0x01,
             read={CURSOR_STATE: 8}),
    ],
}

def menu_state(counter=0, item=0, xoff=0, yoff=0, ysep=0, vis=0, invis=0):
    return {
        0xCD0F: bytes([counter]),
        0xCD10: bytes([item]),
        0xCD11: bytes([xoff]),
        0xCD12: bytes([yoff]),
        0xCD13: bytes([ysep]),
        0xCD15: bytes([vis]),
        0xCD16: bytes([invis]),
    }


CONTRACT.update({
    "DrawCursor": {"compare": (), "preserve": ()},
    "EraseCursor": {"compare": (), "preserve": ()},
    "DrawCursor2": {"compare": (), "preserve": ()},
    "RefreshMenuCursor": {"compare": (), "preserve": ()},
    "DrawCardSymbol": {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")},
    "DrawNarrowTextBox": {"compare": ("hl",), "preserve": ()},
    "DrawWideTextBox": {"compare": ("hl",), "preserve": ()},
    "DrawNarrowTextBox_PrintTextNoDelay": {"compare": ("hl",), "preserve": ()},
    "DrawWideTextBox_PrintTextNoDelay": {"compare": ("hl",), "preserve": ()},
    "DrawWideTextBox_PrintText": {"compare": ("hl",), "preserve": ()},
    "PrintYesOrNoItems": {"compare": ("b", "c", "hl"), "preserve": ("b", "c")},
    "DrawWideTextBox_PrintTextNoDelay_Wait": {"compare": (), "preserve": ()},
    "DrawNarrowTextBox_WaitForInput": {"compare": (), "preserve": ()},
    "DrawWideTextBox_WaitForInput": {"compare": (), "preserve": ()},
    "WaitForWideTextBoxInput": {"compare": (), "preserve": ()},
    "WaitForButtonAorB": {"compare": ("f",), "preserve": ()},
})

BOX_READ = {0x9980: 192}  # BG-map row 12, 6 rows x 32 cols, zero scroll
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
PLACEMENT_READ = {0xFFAA: 2, 0xFFAD: 1, 0xFFAE: 1}
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800, 0x9980: 192}, 1: {0x9980: 192}}

CASES.update({
    "DrawCursor": [
        {"a": 5, "wram": menu_state(), "vread": {0: {0x9800: 1}, 1: {0x9800: 1}}},
        dict(POISON, a=0xAA, wram=menu_state(item=3, xoff=5, yoff=7, ysep=4),
             vread={0: {0x9a65: 1}, 1: {0x9a65: 1}}),
        # low byte of item*ysep, plus yoff, both wrap mod 256 before landing
        # in a valid VRAM address: 250*1 mod 256 = 250, +10 mod 256 = 4.
        {"a": 7, "wram": menu_state(item=250, xoff=15, yoff=10, ysep=1),
         "vread": {0: {0x988f: 1}}},
    ],
    "EraseCursor": [
        {"wram": menu_state(item=1, xoff=2, yoff=3, ysep=2, invis=7),
         "vread": {0: {0x98a2: 1}, 1: {0x98a2: 1}}},
        dict(POISON, wram=menu_state(item=6, xoff=9, yoff=11, ysep=5, invis=0x2A),
             vread={0: {0x9d29: 1}}),
    ],
    "DrawCursor2": [
        {"wram": menu_state(item=2, xoff=1, yoff=1, ysep=3, vis=9),
         "vread": {0: {0x98e1: 1}, 1: {0x98e1: 1}}},
        dict(POISON, wram=menu_state(item=8, xoff=4, yoff=6, ysep=7, vis=0x3B),
             vread={0: {0x9fc4: 1}}),
    ],
    "RefreshMenuCursor": [
        # old&0xf == 5 != 0 -> early return; DrawCursor2 (setup) plants a
        # sentinel tile at the same cursor position first, so a buggy
        # implementation that draws anyway is caught, not just a wrong count.
        {"wram": menu_state(counter=5, item=3, xoff=1, yoff=1, ysep=2, vis=0xAB),
         "setup": [{"fn": "DrawCursor2"}], "read": {0x98e1: 1}},
        # old == 0 -> new&0x10 == 0 -> draws the visible tile.
        {"wram": menu_state(counter=0, item=3, xoff=2, yoff=2, ysep=1, vis=0x11),
         "read": {0x98a2: 1}},
        # old == 16 -> new&0x10 != 0 -> falls into EraseCursor (invisible tile).
        {"wram": menu_state(counter=16, item=4, xoff=2, yoff=1, ysep=5, invis=0x22),
         "read": {0x9aa2: 1}},
        # old == 255: low nibble 0xf != 0 -> early return, and the counter
        # itself wraps 255 -> 0 (checked automatically via the wram readback).
        dict(POISON, wram=menu_state(counter=255, item=9, xoff=10, yoff=2, ysep=6, vis=0x44),
             setup=[{"fn": "DrawCursor2"}], read={0x9f0a: 1}),
    ],
    "DrawCardSymbol": [
        # DMG, pokemon basic (type=0 -> id = stage+8 = 8, tile $d0).
        {"d": 5, "e": 5, "vread": {0: {0x9883: 2, 0x98a3: 2}, 1: {0x9883: 2, 0x98a3: 2}}},
        # CGB, trainer (type>=TYPE_TRAINER -> id=11, tile $dc, attr $02).
        {"d": 10, "e": 10, "wram": {0xCAB4: b"\x02", 0xCC24: b"\x10"},
         "vread": {0: {0x9928: 2, 0x9948: 2}, 1: {0x9928: 2, 0x9948: 2}}},
        # poisoned b/c/hl (must survive the whole push/pop body unchanged) plus
        # d=0,e=1, wrapping x to $fe while y stays 0; energy type=$09 -> id=1, tile $e4.
        dict(POISON, d=0, e=1, wram={0xCC24: b"\x09"},
             vread={0: {0x98fe: 2, 0x991e: 2}}),
        # type == TYPE_ENERGY exactly -> id = type&7 = 0, tile $e0.
        {"d": 20, "e": 3, "wram": {0xCC24: b"\x08"},
         "vread": {0: {0x9852: 2, 0x9872: 2}}},
    ],
    "DrawNarrowTextBox": [
        {"vread": {0: BOX_READ}},
        {"wram": {0xCAB4: b"\x02"}, "vread": {1: {0x9980: 192}}},
        dict(POISON, vread={0: BOX_READ}),
    ],
    "DrawWideTextBox": [
        {"vread": {0: BOX_READ}},
        {"wram": {0xCAB4: b"\x02"}, "vread": {1: {0x9980: 192}}},
        dict(POISON, vread={0: BOX_READ}),
    ],
    "DrawNarrowTextBox_PrintTextNoDelay": [
        {"hl": 0, "vread": {0: BOX_READ}},
        {"hl": 1, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
        dict(POISON, hl=1, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ},
             vread=VRAM_READ),
    ],
    "DrawWideTextBox_PrintTextNoDelay": [
        {"hl": 0, "vread": {0: BOX_READ}},
        {"hl": 1, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
        dict(POISON, hl=1, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ},
             vread=VRAM_READ),
    ],
    "DrawWideTextBox_PrintText": [
        {"hl": 0, "wram": {0xC590: b"\x00"}, "vread": {0: BOX_READ}},
        {"hl": 1, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
        dict(POISON, hl=1, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ},
             vread=VRAM_READ),
    ],
    "PrintYesOrNoItems": [
        {"d": 7, "e": 16, "setup": SETUP, "read": {**CACHE_READ, **PLACEMENT_READ},
         "vread": VRAM_READ},
        dict(POISON, d=3, e=16, setup=SETUP, read={**CACHE_READ, **PLACEMENT_READ},
             vread=VRAM_READ),
    ],
})

# WaitForButtonAorB returns carry set (f=$90) if B, clear (f=$00) if A, and
# erases the cursor on both paths. The erased tile must be diffed, not just the
# flag, or a dropped EraseCursor call stays green.
CASES.update({
    "WaitForButtonAorB": [
        {"keys": 0x01, "wram": menu_state(counter=5, item=1, xoff=4, yoff=1,
         ysep=0, invis=0x11), "vread": {0: {0x9884: 1}}},
        {"keys": 0x02, "wram": menu_state(counter=5, item=1, xoff=4, yoff=1,
         ysep=0, invis=0x11), "vread": {0: {0x9884: 1}}},
        dict(POISON, keys=0x01, wram=menu_state(counter=0, item=2, xoff=1, yoff=2,
             ysep=0, invis=0x33), vread={0: {0x9841: 1}}),
    ],
    "DrawWideTextBox_PrintTextNoDelay_Wait": [
        {"hl": 0, "keys": 0x01,
         "wram": {**menu_state(counter=5, item=1, xoff=4, invis=0x22)},
         "read": {0xCD0F: 1, 0xCD10: 1, 0xCD16: 1},
         "vread": {0: {0x9980: 1, 0x9A32: 1}}},
    ],
    "DrawNarrowTextBox_WaitForInput": [
        {"hl": 0, "keys": 0x01,
         "wram": {**menu_state(counter=5, item=1, xoff=4, invis=0x22)},
         "read": {0xCD0F: 1, 0xCD10: 1, 0xCD16: 1},
         "vread": {0: {0x9980: 1}}},
    ],
    "DrawWideTextBox_WaitForInput": [
        {"hl": 0, "keys": 0x01,
         "wram": {0xC590: b"\x00", **menu_state(counter=5, item=1, xoff=4, invis=0x22)},
         "read": {0xCD0F: 1, 0xCD10: 1, 0xCD16: 1},
         "vread": {0: {0x9980: 1, 0x9A32: 1}}},
    ],
    "WaitForWideTextBoxInput": [
        {"keys": 0x01, "wram": menu_state(counter=5, item=0, xoff=2, yoff=3,
         ysep=0, invis=0x22),
         "vread": {0: {0x9A32: 1}}},
    ],
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "OneByteNumberToTxSymbol": {
        "source_symbol": "OneByteNumberToTxSymbol",
        "before": "return tx_symbol_core(a);",
        "after": "return tx_symbol_core((uint8_t)(a + 1u));",
        "case_ids": ["OneByteNumberToTxSymbol-0", "OneByteNumberToTxSymbol-1", "OneByteNumberToTxSymbol-2", "OneByteNumberToTxSymbol-3", "OneByteNumberToTxSymbol-4"],
    },
}
