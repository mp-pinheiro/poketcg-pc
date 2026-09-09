from tests.cases._fixtures import play_area_b_fixture as _play_area_b_fixture, PLAY_AREA_B_REGS as _PLAY_AREA_B_REGS
from tests.cases._fixtures import CARD_LIST_INPUT_REGS as _CARD_LIST_INPUT_REGS, card_list_input_fixture as _card_list_input_fixture
from tests.cases._fixtures import BUTTON_AB_REGS as _BUTTON_AB_REGS, button_ab_fixture as _button_ab_fixture
from tests.cases._fixtures import YES_NO_REGS as _YES_NO_REGS, yes_no_fixture as _yes_no_fixture
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
        dict(_button_ab_fixture(vram=False), **_BUTTON_AB_REGS, keys=[0x00, 0x01]),
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
# >>> factory RefreshMenuCursor_CheckPlaySFX
CONTRACT["RefreshMenuCursor_CheckPlaySFX"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["RefreshMenuCursor_CheckPlaySFX"] = [
    {"wram": {0xCD99: b"\x00"}},
    {"wram": {0xCD99: b"\x12", 0xDD83: b"\x00"}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xCD99: b"\x34", 0xDD83: b"\x00"}},
]
# <<< factory RefreshMenuCursor_CheckPlaySFX

# >>> factory PlayOpenOrExitScreenSFX
CONTRACT["PlayOpenOrExitScreenSFX"] = {"compare": ("a", "f"), "preserve": ("a", "f"), "wram_out": True}
CASES["PlayOpenOrExitScreenSFX"] = [
    {"a": 0x11, "f": 0x00, "wram": {0xFFB1: b"\xFF"}, "read": {0xDD82: 1}},
    dict(POISON, wram={0xFFB1: b"\x02"}, read={0xDD82: 1}),
]
# <<< factory PlayOpenOrExitScreenSFX

# >>> factory-cases-statics
hCurMenuItem = 0xFFB1
hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
wCurMenuItem = 0xCD10
wCursorBlinkCounter = 0xCD0F
wDefaultYesOrNo = 0xCD9A
wLeftmostItemCursorX = 0xCD98
wMenuCursorXOffset = 0xCD11

wDuelTempList = 0xC510
wListScrollOffset = 0xCD19
wMenuCursorYOffset = 0xCD12
wNumMenuItems = 0xCD14
wNumListItems = 0xCD1B
wListItemXPosition = 0xCD1A
wListItemNameMaxLength = 0xCD1C
wDefaultText = 0xC590

hffb0 = 0xFFB0
wDuelTempList = 0xC510
wListScrollOffset = 0xCD19
wMenuCursorYOffset = 0xCD12
wNumMenuItems = 0xCD14
wNumListItems = 0xCD1B

hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
hCurMenuItem = 0xFFB1
wCurMenuItem = 0xCD10
wNumMenuItems = 0xCD14
wListScrollOffset = 0xCD19
wNumListItems = 0xCD1B
wListFunctionPointer = 0xCD1D
wCardListIndicatorYPosition = 0xCD97
wRefreshMenuCursorSFX = 0xCD99
wDefaultText = 0xC590

wCurMenuItem = 0xCD10
wLeftmostItemCursorX = 0xCD98
wDefaultYesOrNo = 0xCD9A
wMenuCursorXOffset = 0xCD11
wCursorBlinkCounter = 0xCD0F
hCurMenuItem = 0xFFB1

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wDuelReturnAddress = 0xCBE5
wDuelFinished = 0xCC07
wDuelTheme = 0xCC1A
# <<< factory-cases-statics

# >>> factory HandleYesOrNoMenu
CONTRACT["HandleYesOrNoMenu"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleYesOrNoMenu"] = [
    {"d": 0x20, "e": 0x10, "b": 0xAA, "c": 0xBB, "keys": 0x01,
     "wram": {wDefaultYesOrNo: b"\x00"},
     "expect": {wDefaultYesOrNo: b"\x00", hCurMenuItem: b"\x01", wCurMenuItem: b"\x01"},
     "expect_regs": {"a": 0x01, "f": 0x90},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, d=0x20, e=0x10, keys=0x01,
         wram={wDefaultYesOrNo: b"\x01"},
         expect={wDefaultYesOrNo: b"\x00", hCurMenuItem: b"\x00", wCurMenuItem: b"\x00"},
         expect_regs={"a": 0x00, "f": 0x80},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory HandleYesOrNoMenu

# >>> factory CopyCardNameAndLevel
# The home-bank entry point 19 callers use. The setup call loads real card data,
# so CopyText expands an actual name into wDefaultText and the callee's halfwidth
# path appends the level; entry a is the pad width in tiles.
CONTRACT["CopyCardNameAndLevel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
                                    "preserve": ()}
CASES["CopyCardNameAndLevel"] = [
    {"a": 0x0D, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE,
     "setup": [{"fn": "LoadCardDataToBuffer1_FromCardID", "e": 0x43}],
     "read": {0xC590: 32}},
    {"a": 0x0D, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE,
     "setup": [{"fn": "LoadCardDataToBuffer1_FromCardID", "e": 0x03}],
     "read": {0xC590: 32}},
    dict(POISON, a=0x0D,
         setup=[{"fn": "LoadCardDataToBuffer1_FromCardID", "e": 0x43}],
         read={0xC590: 32}),
]
# <<< factory CopyCardNameAndLevel

# >>> factory ReloadCardListItems
CONTRACT["ReloadCardListItems"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ReloadCardListItems"] = [
    {"wram": {wListScrollOffset: b"\x00", wMenuCursorYOffset: b"\x0a", wNumMenuItems: b"\x03", wNumListItems: b"\x03", wDuelTempList: b"\xff"}, "read": {0x9932: 1, 0x99d2: 1}},
    dict(POISON, wram={wListScrollOffset: b"\x01", wMenuCursorYOffset: b"\x0a", wNumMenuItems: b"\x02", wNumListItems: b"\x05", wDuelTempList + 1: b"\xff"}, read={0x9932: 1, 0x99b2: 1}),
]
# <<< factory ReloadCardListItems

# >>> factory Func_2827
CONTRACT["Func_2827"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["Func_2827"] = [
    {"wram": {wListScrollOffset: b"\x00", wMenuCursorYOffset: b"\x0a", wNumMenuItems: b"\x03", wNumListItems: b"\x03", wDuelTempList: b"\xff"}, "read": {hffb0: 1, 0x9932: 1, 0x99d2: 1}},
    dict(POISON, wram={wListScrollOffset: b"\x01", wMenuCursorYOffset: b"\x0a", wNumMenuItems: b"\x02", wNumListItems: b"\x05", wDuelTempList + 1: b"\xff"}, read={hffb0: 1, 0x9932: 1, 0x99b2: 1}),
]
# <<< factory Func_2827

# >>> factory PrintCardListItems
CONTRACT["PrintCardListItems"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["PrintCardListItems"] = [
    {"a": 0x01, "d": 0x00, "e": 0x00, "hl": 0xC500, "wram": {0xC500: b"\x01\x02\x03\x04\x01\x20\x21\x00\x00", 0xC510: b"\xFF"}, "read": {0xCD13: 1, 0xCD17: 2, 0xCD97: 1}, "vread": {0: {0x9832: 1, 0x9872: 1}}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0x1234, wram={0xC5ED: b"\xFF"}, read={0xCD13: 1, 0xCD17: 2, 0xCD97: 1}, vread={0: {0x9832: 1, 0x9872: 1}}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory PrintCardListItems

# >>> factory CardListMenuFunction
CONTRACT["CardListMenuFunction"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CardListMenuFunction"] = [
    {"keys": 0x00, "wram": {wCurMenuItem: b"\x00", wNumMenuItems: b"\x02", wListScrollOffset: b"\x00", wNumListItems: b"\x04", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x77"}, "read": {hCurMenuItem: 1}},
    {"keys": 0x00, "wram": {wCurMenuItem: b"\x01", wNumMenuItems: b"\x03", wListScrollOffset: b"\x02", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x12"}, "read": {hCurMenuItem: 1}},
    {"keys": 0x02, "wram": {wCurMenuItem: b"\x01", wNumMenuItems: b"\x03", wListScrollOffset: b"\x02", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\xAA"}, "read": {hCurMenuItem: 1}},
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x01", wNumMenuItems: b"\x03", wListScrollOffset: b"\x02", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x55"}, read={hCurMenuItem: 1}),
    # menus.asm:573-581 `jp hl` on wListFunctionPointer = CardListFunction
    # ($01:5719): START pressed (hKeysPressed $FF91) is the list function's
    # own carry exit, B its MENU_CANCEL write to hCurMenuItem, neither an A/B
    # decision of this routine. Bank 1 mapped by hBankROM ($FF80).
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x01", wNumMenuItems: b"\x03", wListScrollOffset: b"\x02", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x19\x57", wRefreshMenuCursorSFX: b"\x55", 0xFF91: b"\x08", 0xFF80: b"\x01"}, read={hCurMenuItem: 1}),
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x01", wNumMenuItems: b"\x03", wListScrollOffset: b"\x02", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x19\x57", wRefreshMenuCursorSFX: b"\x55", 0xFF91: b"\x02", 0xFF80: b"\x01"}, read={hCurMenuItem: 1}),
    # menus.asm:436-481 `.no_more_items`: hDPadHeld ($FF8F) UP with the cursor
    # wrapped to the last visible item and no page above (scroll 0), and DOWN
    # wrapped to the first item with no page below (scroll + items == list),
    # both clear the buffered cursor SFX (wRefreshMenuCursorSFX, seeded 1 as
    # HandleMenuInput leaves it) instead of scrolling.
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x02", wNumMenuItems: b"\x03", wListScrollOffset: b"\x00", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x01", 0xFF8F: b"\x40"}, read={hCurMenuItem: 1, wCurMenuItem: 1, wListScrollOffset: 1}),
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x00", wNumMenuItems: b"\x03", wListScrollOffset: b"\x02", wNumListItems: b"\x05", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x01", 0xFF8F: b"\x80"}, read={hCurMenuItem: 1, wCurMenuItem: 1, wListScrollOffset: 1}),
    # menus.asm:495-508 LEFT from a page less than one page down (scroll 2 of
    # 5 visible, 7 items) with the cursor on absolute item 6: the first page
    # is shown with the cursor at 6 - 5 = 1, not at 6. menus.asm:530-546 RIGHT
    # onto the last page from scroll 0, cursor 0: scroll becomes 2 and the
    # cursor 0 - 2 + 5 = 3.
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x04", wNumMenuItems: b"\x05", wListScrollOffset: b"\x02", wNumListItems: b"\x07", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x01", 0xFF8F: b"\x20"}, read={hCurMenuItem: 1, wCurMenuItem: 1, wListScrollOffset: 1}),
    dict(POISON, keys=0x00, wram={wCurMenuItem: b"\x00", wNumMenuItems: b"\x05", wListScrollOffset: b"\x00", wNumListItems: b"\x07", wCardListIndicatorYPosition: b"\xFF", wListFunctionPointer: b"\x00\x00", wRefreshMenuCursorSFX: b"\x01", 0xFF8F: b"\x10"}, read={hCurMenuItem: 1, wCurMenuItem: 1, wListScrollOffset: 1}),
]
# <<< factory CardListMenuFunction

# >>> factory HandleMenuInput
CONTRACT["HandleMenuInput"] = {"compare": ("a", "e", "f"), "preserve": ()}
_PLAY_AREA_B = _play_area_b_fixture(bank=1)
_PLAY_AREA_B["wram"] = {**_PLAY_AREA_B["wram"], 0xFF8F: b"\x02", 0xFF90: b"\x02", 0xFF91: b"\x02"}
_PLAY_AREA_B["read"] = {**_PLAY_AREA_B["read"], 0xFF92: 1, 0xCD10: 1}
CASES["HandleMenuInput"] = [
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x01", 0xCD17: b"\x00\x00", 0xCD10: b"\x02", 0xCD14: b"\x04", 0xFFB1: b"\x02", 0xCD15: b"\x00", 0xCD99: b"\x99"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD99: 1}},
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x02", 0xCD17: b"\x00\x00", 0xCD10: b"\x03", 0xCD14: b"\x04", 0xFFB1: b"\x03", 0xCD15: b"\x00", 0xCD99: b"\x2A"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD99: 1}},
    dict(POISON, wram={0xFF8F: b"\x00", 0xFF91: b"\x02", 0xCD17: b"\x00\x00", 0xCD10: b"\x01", 0xCD14: b"\x04", 0xFFB1: b"\x01", 0xCD15: b"\x00", 0xCD99: b"\x77"}, read={0xFFB1: 1, 0xCD10: 1, 0xCD99: 1}),
    # menus.asm:79-104: hDPadHeld PAD_UP with a nonzero cursor position takes
    # the up/down branch, which overwrites wRefreshMenuCursorSFX with $1
    # (buffered cursor SFX) after the unconditional entry clear -- seeded
    # nonzero here to prove both writes land, not just the entry clear.
    {"wram": {0xFF8F: b"\x40", 0xFF91: b"\x00", 0xCD17: b"\x00\x00", 0xCD10: b"\x02", 0xCD14: b"\x04", 0xFFB1: b"\x02", 0xCD15: b"\x00", 0xCD99: b"\x99"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD99: 1}},
    # menus.asm:113-122 `call CallHL` on wMenuUpdateFunc ($CD17). With
    # PlayAreaScreenMenuFunction ($01:60CE, hBankROM $FF80 = 1) installed,
    # START is that function's carry exit -- A-pressed epilogue, blink counter
    # ($CD0F) untouched -- and no button is its nc exit into RefreshMenuCursor,
    # which advances the counter. A port that runs CardListMenuFunction for
    # every update function, or that refreshes the cursor before the update
    # function decides, differs on the counter or the flags.
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x08", 0xCD17: b"\xCE\x60", 0xCD10: b"\x02", 0xCD14: b"\x04", 0xFFB1: b"\x02", 0xCD15: b"\x00", 0xCD99: b"\x99", 0xCD0F: b"\x05", 0xFF80: b"\x01"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD99: 1, 0xCD0F: 1}},
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x00", 0xCD17: b"\xCE\x60", 0xCD10: b"\x02", 0xCD14: b"\x04", 0xFFB1: b"\x02", 0xCD15: b"\x00", 0xCD99: b"\x00", 0xCD0F: b"\x05", 0xFF80: b"\x01"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD99: 1, 0xCD0F: 1}},
    dict(_PLAY_AREA_B, **_PLAY_AREA_B_REGS),
]
# <<< factory HandleMenuInput

# >>> factory HandleCardListInput
CONTRACT["HandleCardListInput"] = {"compare": ("a", "d", "e", "f"), "preserve": ()}
CASES["HandleCardListInput"] = [
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x01", 0xCD17: b"\x00\x00", 0xCD10: b"\x02", 0xCD14: b"\x04", 0xFFB1: b"\x02", 0xCD15: b"\x00", 0xCD19: b"\x03"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD19: 1}},
    {"wram": {0xFF8F: b"\x00", 0xFF91: b"\x02", 0xCD17: b"\x00\x00", 0xCD10: b"\x03", 0xCD14: b"\x04", 0xFFB1: b"\x03", 0xCD15: b"\x00", 0xCD19: b"\x01"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD19: 1}},
    dict(POISON, wram={0xFF8F: b"\x00", 0xFF91: b"\x02", 0xCD17: b"\x00\x00", 0xCD10: b"\x01", 0xCD14: b"\x04", 0xFFB1: b"\x01", 0xCD15: b"\x00", 0xCD19: b"\x07"}, read={0xFFB1: 1, 0xCD10: 1, 0xCD19: 1}),
    dict(_card_list_input_fixture(vram=False), **_CARD_LIST_INPUT_REGS),
]
# <<< factory HandleCardListInput

# >>> factory HandleDuelMenuInput
CONTRACT["HandleDuelMenuInput"] = {"compare": ("a", "e", "f"), "preserve": ()}
CASES["HandleDuelMenuInput"] = [
    {"e": 0x00, "wram": {0xFF8F: b"\x01", 0xCD10: b"\x02", 0xFFB1: b"\x02", 0xCD0F: b"\x00"}, "read": {0xFFB1: 1, 0xCD10: 1}},
    {"e": 0x00, "wram": {0xFF8F: b"\x40", 0xCD10: b"\x00", 0xFFB1: b"\x00", 0xCD0F: b"\x00"}, "read": {0xFFB1: 1, 0xCD10: 1, 0xCD0F: 1}, "vread": {0: {0x9800 + 32 * 14 + 2: 1}}},
    dict(POISON, wram={0xFF8F: b"\x00", 0xCD10: b"\x00", 0xFFB1: b"\x00", 0xCD0F: b"\x01"}, read={0xCD0F: 1}),
]
# <<< factory HandleDuelMenuInput

# >>> factory YesOrNoMenuWithText_LeftAligned
CONTRACT["YesOrNoMenuWithText_LeftAligned"] = {"compare": ("a", "f"), "preserve": ()}
CASES["YesOrNoMenuWithText_LeftAligned"] = [
    {"hl": 1, "b": 0x12, "c": 0x34, "keys": 0x01,
     "setup": SETUP,
     "wram": {**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x00"},
     "read": {**CACHE_READ, **PLACEMENT_READ},
     "vread": VRAM_READ,
     "expect_regs": {"a": 0x01, "f": 0x90},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=1, keys=0x01,
         setup=SETUP,
         wram={**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x01"},
         read={**CACHE_READ, **PLACEMENT_READ},
         vread=VRAM_READ,
         expect_regs={"a": 0x00, "f": 0x80},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory YesOrNoMenuWithText_LeftAligned

# >>> factory TwoItemHorizontalMenu
CONTRACT["TwoItemHorizontalMenu"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TwoItemHorizontalMenu"] = [
    {"hl": 0, "keys": 0x01, "wram": {0xFF97: b"\xC2"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "expect_regs": {"a": 0, "f": 0x80}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0, keys=0x01, wram={0xFF97: b"\xC2"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], expect_regs={"a": 0, "f": 0x80}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory TwoItemHorizontalMenu

# >>> factory YesOrNoMenu
CONTRACT["YesOrNoMenu"] = {"compare": ("a", "f"), "preserve": ()}
CASES["YesOrNoMenu"] = [
    {"keys": 0x01,
     "setup": SETUP,
     "wram": {**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x00"},
     "read": {**CACHE_READ, **PLACEMENT_READ},
     "vread": VRAM_READ,
     "expect_regs": {"a": 0x01, "f": 0x90},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, keys=0x01,
         setup=SETUP,
         wram={**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x01"},
         read={**CACHE_READ, **PLACEMENT_READ},
         vread=VRAM_READ,
         expect_regs={"a": 0x00, "f": 0x80},
         instruction_budget=2000000, cycle_budget=8000000),
    dict(_yes_no_fixture(vram=False), **_YES_NO_REGS, keys=[0x00, 0x01]),
]
# <<< factory YesOrNoMenu

# >>> factory YesOrNoMenuWithText
CONTRACT["YesOrNoMenuWithText"] = {"compare": ("a", "f"), "preserve": ()}
CASES["YesOrNoMenuWithText"] = [
    {"hl": 1, "keys": 0x01,
     "setup": SETUP,
     "wram": {**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x00"},
     "read": {**CACHE_READ, **PLACEMENT_READ},
     "vread": VRAM_READ,
     "expect_regs": {"a": 0x01, "f": 0x90},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=1, keys=0x01,
         setup=SETUP,
         wram={**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x01"},
         read={**CACHE_READ, **PLACEMENT_READ},
         vread=VRAM_READ,
         expect_regs={"a": 0x00, "f": 0x80},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory YesOrNoMenuWithText

# >>> factory YesOrNoMenuWithText_SetCursorToYes
CONTRACT["YesOrNoMenuWithText_SetCursorToYes"] = {"compare": ("a", "f"), "preserve": ()}
CASES["YesOrNoMenuWithText_SetCursorToYes"] = [
    {"hl": 1, "keys": 0x01,
     "setup": SETUP,
     "wram": {**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x00"},
     "read": {**CACHE_READ, **PLACEMENT_READ},
     "vread": VRAM_READ,
     "expect_regs": {"a": 0x01, "f": 0x90},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=1, keys=0x01,
         setup=SETUP,
         wram={**menu_state(counter=5, item=1, xoff=2, invis=0x22), wDefaultYesOrNo: b"\x00"},
         read={**CACHE_READ, **PLACEMENT_READ},
         vread=VRAM_READ,
         expect_regs={"a": 0x01, "f": 0x90},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory YesOrNoMenuWithText_SetCursorToYes

# >>> factory DrawTextBox_PrintTextNoDelay
CONTRACT["DrawTextBox_PrintTextNoDelay"] = {"compare": ("hl",), "preserve": ()}
CASES["DrawTextBox_PrintTextNoDelay"] = [
    {"a": 11, "stack": [0], "setup": SETUP,
     "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": VRAM_READ},
    {"a": 11, "stack": [1], "setup": SETUP,
     "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": VRAM_READ},
    {"a": 19, "stack": [1], "setup": SETUP,
     "read": {**CACHE_READ, **PLACEMENT_READ}, "vread": VRAM_READ},
    dict(POISON, a=19, stack=[1], setup=SETUP,
         read={**CACHE_READ, **PLACEMENT_READ}, vread=VRAM_READ),
]
# <<< factory DrawTextBox_PrintTextNoDelay

# >>> factory ContinueDuel
CONTRACT["ContinueDuel"] = {"compare": (), "preserve": ()}
CASES["ContinueDuel"] = [
    {"entry_sp": 0xFFFC,
     "wram": {wDuelReturnAddress: b"\xAA\xBB", wDuelFinished: b"\xCC", wDuelTheme: b"\x01"},
     "read": {wDuelReturnAddress: 2, wDuelFinished: 1},
     "expect": {wDuelReturnAddress: b"\xFC\xFF", wDuelFinished: b"\x00"},
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, entry_sp=0xFFFC,
         wram={wDuelReturnAddress: b"\xAA\xBB", wDuelFinished: b"\xCC", wDuelTheme: b"\x01"},
         read={wDuelReturnAddress: 2, wDuelFinished: 1},
         expect={wDuelReturnAddress: b"\xFC\xFF", wDuelFinished: b"\x00"},
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ContinueDuel

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
# >>> factory-mutation RefreshMenuCursor_CheckPlaySFX
MUTATIONS["RefreshMenuCursor_CheckPlaySFX"] = {"source_symbol": "RefreshMenuCursor_CheckPlaySFX", "before": "\t\tPlaySFX(a);", "after": "\t\tPlaySFX(0u);", "case_ids": ["RefreshMenuCursor_CheckPlaySFX-1", "RefreshMenuCursor_CheckPlaySFX-2"]}
# <<< factory-mutation RefreshMenuCursor_CheckPlaySFX
# >>> factory-mutation PlayOpenOrExitScreenSFX
MUTATIONS["PlayOpenOrExitScreenSFX"] = {
    "source_symbol": "PlayOpenOrExitScreenSFX",
    "before": "if ((uint8_t)(item + 1u) == 0u)",
    "after": "if ((uint8_t)(item + 2u) == 0u)",
    "case_ids": ["PlayOpenOrExitScreenSFX-0", "PlayOpenOrExitScreenSFX-1"],
}
# <<< factory-mutation PlayOpenOrExitScreenSFX
# >>> factory-mutation HandleYesOrNoMenu
MUTATIONS["HandleYesOrNoMenu"] = {
    "source_symbol": "HandleYesOrNoMenu",
    "before": "\twCurMenuItem = (uint8_t)(wDefaultYesOrNo ^ 1u);",
    "after": "\twCurMenuItem = (uint8_t)(wDefaultYesOrNo ^ 0u);",
    "case_ids": ["HandleYesOrNoMenu-0", "HandleYesOrNoMenu-1"],
}
# <<< factory-mutation HandleYesOrNoMenu

# >>> factory-mutation CopyCardNameAndLevel
MUTATIONS["CopyCardNameAndLevel"] = {
    "source_symbol": "CopyCardNameAndLevel",
    "before": "\treturn _CopyCardNameAndLevel(a, b, c, d, e);",
    "after": "\treturn _CopyCardNameAndLevel((uint8_t)(a + 1u), b, c, d, e);",
    "case_ids": ["CopyCardNameAndLevel-0", "CopyCardNameAndLevel-1"],
}
# <<< factory-mutation CopyCardNameAndLevel
# >>> factory-mutation ReloadCardListItems
MUTATIONS["ReloadCardListItems"] = {
    "source_symbol": "ReloadCardListItems",
    "before": "uint8_t up = SYM_SPACE;",
    "after": "uint8_t up = SYM_CURSOR_U;",
    "case_ids": ["ReloadCardListItems-0", "ReloadCardListItems-1"],
}
# <<< factory-mutation ReloadCardListItems
# >>> factory-mutation Func_2827
MUTATIONS["Func_2827"] = {
    "source_symbol": "Func_2827",
    "before": "\tgb_write8(hffb0_ADDR, 0x00u);",
    "after": "\tgb_write8(hffb0_ADDR, 0x01u);",
    "case_ids": ["Func_2827-0", "Func_2827-1"],
}
# <<< factory-mutation Func_2827
# >>> factory-mutation PrintCardListItems
MUTATIONS["PrintCardListItems"] = {
    "source_symbol": "PrintCardListItems",
    "before": "\twMenuYSeparation = 2u;",
    "after": "\twMenuYSeparation = 3u;",
    "case_ids": ["PrintCardListItems-0", "PrintCardListItems-1"],
}
# <<< factory-mutation PrintCardListItems
# >>> factory-mutation CardListMenuFunction
MUTATIONS["CardListMenuFunction"] = {"source_symbol": "CardListMenuFunction", "before": "\tif (list_fn == CARD_LIST_FUNCTION) {\n\t\tCardListFunctionResult r = CardListFunction();\n\t\treturn (CardListMenuFunctionResult){r.a, r.f};\n\t}", "after": "\tif (list_fn == CARD_LIST_FUNCTION)\n\t\treturn (CardListMenuFunctionResult){0u, 0x00u};", "case_ids": ["CardListMenuFunction-4", "CardListMenuFunction-5"]}
# <<< factory-mutation CardListMenuFunction
# >>> factory-mutation HandleMenuInput
MUTATIONS["HandleMenuInput"] = {"source_symbol": "HandleMenuInput", "before": "\t\t} else if (update == PLAY_AREA_SCREEN_MENU_FUNCTION) {\n\t\t\tupdate_f = PlayAreaScreenMenuFunction();", "after": "\t\t} else if (update == PLAY_AREA_SCREEN_MENU_FUNCTION) {\n\t\t\tupdate_f = CardListMenuFunction().f;", "case_ids": ["HandleMenuInput-4"]}
# <<< factory-mutation HandleMenuInput
# >>> factory-mutation HandleCardListInput
MUTATIONS["HandleCardListInput"] = {
    "source_symbol": "HandleCardListInput",
    "before": "\tHandleCardListInputResult result = {input.a, input.d, input.e, input.f};",
    "after": "\tHandleCardListInputResult result = {input.a, 0u, input.e, input.f};",
    "case_ids": ["HandleCardListInput-3"],
}
# <<< factory-mutation HandleCardListInput
# >>> factory-mutation YesOrNoMenuWithText_LeftAligned
MUTATIONS["YesOrNoMenuWithText_LeftAligned"] = {
    "source_symbol": "YesOrNoMenuWithText_LeftAligned",
    "before": "\treturn HandleYesOrNoMenu(2u, 16u, b, c);",
    "after": "\treturn (HandleYesOrNoMenuResult){0u, 0x80u};",
    "case_ids": ["YesOrNoMenuWithText_LeftAligned-0", "YesOrNoMenuWithText_LeftAligned-1"],
}
# <<< factory-mutation YesOrNoMenuWithText_LeftAligned
# >>> factory-mutation TwoItemHorizontalMenu
MUTATIONS["TwoItemHorizontalMenu"] = {"source_symbol": "TwoItemHorizontalMenu", "before": "\tEnableLCD();\n\t/* jp target lands inside .refresh_menu, whose own xor $1 flips */\n\t/* wCurMenuItem unconditionally before the wait loop begins. */\n\twCurMenuItem = (uint8_t)(wCurMenuItem ^ 1u);", "after": "\tEnableLCD();\n\t/* jp target lands inside .refresh_menu, whose own xor $1 flips */\n\t/* wCurMenuItem unconditionally before the wait loop begins. */\n", "case_ids": ["TwoItemHorizontalMenu-0", "TwoItemHorizontalMenu-1"]}
# <<< factory-mutation TwoItemHorizontalMenu
# >>> factory-mutation YesOrNoMenu
MUTATIONS["YesOrNoMenu"] = {"source_symbol": "YesOrNoMenu", "before": "\treturn HandleYesOrNoMenu(6u, 16u, 0u, 0u);", "after": "\treturn HandleYesOrNoMenu(7u, 16u, 0u, 0u);", "case_ids": ["YesOrNoMenu-0", "YesOrNoMenu-1"]}
# <<< factory-mutation YesOrNoMenu
# >>> factory-mutation YesOrNoMenuWithText
MUTATIONS["YesOrNoMenuWithText"] = {
    "source_symbol": "YesOrNoMenuWithText",
    "before": "HandleYesOrNoMenuResult YesOrNoMenuWithText(uint16_t hl)\n{\n\t(void)DrawWideTextBox_PrintText(hl);",
    "after": "HandleYesOrNoMenuResult YesOrNoMenuWithText(uint16_t hl)\n{\n\t(void)DrawWideTextBox_PrintText(0u);",
    "case_ids": ["YesOrNoMenuWithText-0", "YesOrNoMenuWithText-1"],
}
# <<< factory-mutation YesOrNoMenuWithText
# >>> factory-mutation YesOrNoMenuWithText_SetCursorToYes
MUTATIONS["YesOrNoMenuWithText_SetCursorToYes"] = {"source_symbol": "YesOrNoMenuWithText_SetCursorToYes", "before": "HandleYesOrNoMenuResult YesOrNoMenuWithText_SetCursorToYes(uint16_t hl)\n{\n\twDefaultYesOrNo = 1u;", "after": "HandleYesOrNoMenuResult YesOrNoMenuWithText_SetCursorToYes(uint16_t hl)\n{\n\twDefaultYesOrNo = 0u;", "case_ids": ["YesOrNoMenuWithText_SetCursorToYes-0", "YesOrNoMenuWithText_SetCursorToYes-1"]}
# <<< factory-mutation YesOrNoMenuWithText_SetCursorToYes
# >>> factory-mutation DrawTextBox_PrintTextNoDelay
MUTATIONS["DrawTextBox_PrintTextNoDelay"] = {"source_symbol": "DrawTextBox_PrintTextNoDelay", "before": "\tInitTextPrintingInTextbox(a, d, e);", "after": "\tInitTextPrintingInTextbox(a, d, (uint8_t)(e + 1u));", "case_ids": ["DrawTextBox_PrintTextNoDelay-1", "DrawTextBox_PrintTextNoDelay-2"]}
# <<< factory-mutation DrawTextBox_PrintTextNoDelay
# >>> factory-mutation ContinueDuel
MUTATIONS["ContinueDuel"] = {"source_symbol": "ContinueDuel", "before": "void ContinueDuel(void)\n{\n\tBankswitchROM(CONTINUE_DUEL_BANK);\n\t_ContinueDuel();", "after": "void ContinueDuel(void)\n{\n\tBankswitchROM(CONTINUE_DUEL_BANK);", "case_ids": ["ContinueDuel-0", "ContinueDuel-1"]}
# <<< factory-mutation ContinueDuel
# >>> factory-completion ContinueDuel
# _ContinueDuel (duel/core.asm:9-21) tail-jumps into MainDuelLoop and never
# returns; the recorded 0x2382 was a text-cache `ret` the reference happened to
# stop on. Both lanes stop at the duel interface call, after the two writes
# this case observes.
for _record in SCHEMA2_CASES["ContinueDuel"]:
    _record["completion"] = {"mode": "entry", "pc": 0x426D, "bank": 1,
                             "routine": "DuelMainInterface"}
# <<< factory-completion ContinueDuel
