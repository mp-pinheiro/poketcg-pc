"""Oracle-diff cases for poketcg/src/scripts/gift_center.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Preload_GiftCenterClerk
CONTRACT["Preload_GiftCenterClerk"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
wConsole = 0xCAB4
wLoadNPCDirection = 0xD3AE
CONSOLE_CGB = 0x02
CASES["Preload_GiftCenterClerk"] = [
    {"wram": {wConsole: b"\x00", wLoadNPCDirection: b"\x55"},
     "read": {wConsole: 1, wLoadNPCDirection: 1}},
    dict(POISON,
         wram={wConsole: b"\x00", wLoadNPCDirection: b"\x55"},
         read={wConsole: 1, wLoadNPCDirection: 1}),
    {"wram": {wConsole: bytes((CONSOLE_CGB,)), wLoadNPCDirection: b"\x55"},
     "read": {wConsole: 1, wLoadNPCDirection: 1}},
    dict(POISON,
         wram={wConsole: bytes((CONSOLE_CGB,)), wLoadNPCDirection: b"\x55"},
         read={wConsole: 1, wLoadNPCDirection: 1}),
    {"wram": {wConsole: b"\x01", wLoadNPCDirection: b"\x55"},
     "read": {wConsole: 1, wLoadNPCDirection: 1}},
]
# <<< factory Preload_GiftCenterClerk

# >>> factory-cases-statics
# GiftCenterMenu (gift_center.asm:31) seeds and observations.
wLCDC = 0xCABB
wTxRam2 = 0xCE3F
wSelectedGiftCenterMenuItem = 0xD0BA
wOverworldNPCFlags = 0xD0C1
wGiftCenterChoice = 0xD10E
wPermissionMap = 0xD133
rLCDC = 0xFF40
hDPadHeld = 0xFF8F
hKeysPressed = 0xFF91
hCurMenuItem = 0xFFB1
PAD_A = 0x01
PAD_B = 0x02
# <<< factory-cases-statics

# >>> factory GiftCenterMenu
CONTRACT["GiftCenterMenu"] = {"compare": ("a", "f"), "preserve": ()}
# The routine's single exit is `pop af` / `ret`, and the two frame calls that
# straddle the dispatch are void, so a and f are the whole register contract.
#
# Every case runs with the LCD off (wLCDC and rLCDC both $00). DoFrameIfLCDEnabled
# is then a no-op on both sides, so no frame elapses, nothing calls ReadJoypad,
# and the seeded hKeysPressed survives into the first HandleMenuInput poll -- the
# input loop takes exactly one turn. On the A exit HandleMenuInput sets
# hCurMenuItem = wCurMenuItem = e, so `cp e` is always Z (f = $C0) and the choice
# is the seeded menu item; on the B exit hCurMenuItem is $ff, the compare misses
# and the choice becomes GIFT_CENTER_MENU_EXIT.
#
# wTxRam2 is seeded $AA $BB so the four dispatching choices prove the text-pointer
# write happened and the GIFT_CENTER_MENU_EXIT cases prove `.stub` wrote nothing.
# wPermissionMap is seeded exactly as the landed CloseTextBox cases do, to pin
# down the LoadTilemap_ToSRAM that CloseTextBox reaches.
CASES["GiftCenterMenu"] = [
    {"wram": {wLCDC: b"\x00", rLCDC: b"\x00", hDPadHeld: b"\x00",
              hKeysPressed: bytes((PAD_A,)),
              wSelectedGiftCenterMenuItem: b"\x00", wOverworldNPCFlags: b"\x00",
              wTxRam2: b"\xAA\xBB", wPermissionMap: b"\x00" * 0x100},
     "read": {wGiftCenterChoice: 1, wTxRam2: 2, hCurMenuItem: 1,
              wSelectedGiftCenterMenuItem: 1, wOverworldNPCFlags: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wLCDC: b"\x00", rLCDC: b"\x00", hDPadHeld: b"\x00",
              hKeysPressed: bytes((PAD_A,)),
              wSelectedGiftCenterMenuItem: b"\x02", wOverworldNPCFlags: b"\x00",
              wTxRam2: b"\xAA\xBB", wPermissionMap: b"\x00" * 0x100},
     "read": {wGiftCenterChoice: 1, wTxRam2: 2, hCurMenuItem: 1,
              wSelectedGiftCenterMenuItem: 1, wOverworldNPCFlags: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"wram": {wLCDC: b"\x00", rLCDC: b"\x00", hDPadHeld: b"\x00",
              hKeysPressed: bytes((PAD_A,)),
              wSelectedGiftCenterMenuItem: b"\x04", wOverworldNPCFlags: b"\x00",
              wTxRam2: b"\xAA\xBB", wPermissionMap: b"\x00" * 0x100},
     "read": {wGiftCenterChoice: 1, wTxRam2: 2, hCurMenuItem: 1,
              wSelectedGiftCenterMenuItem: 1, wOverworldNPCFlags: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON,
         wram={wLCDC: b"\x00", rLCDC: b"\x00", hDPadHeld: b"\x00",
               hKeysPressed: bytes((PAD_B,)),
               wSelectedGiftCenterMenuItem: b"\x01", wOverworldNPCFlags: b"\x02",
               wTxRam2: b"\xAA\xBB", wPermissionMap: b"\xFF" * 0x100},
         read={wGiftCenterChoice: 1, wTxRam2: 2, hCurMenuItem: 1,
               wSelectedGiftCenterMenuItem: 1, wOverworldNPCFlags: 1},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}],
         instruction_budget=20000000, cycle_budget=80000000),
    {"wram": {wLCDC: b"\x00", rLCDC: b"\x00", hDPadHeld: b"\x00",
              hKeysPressed: bytes((PAD_A,)),
              wSelectedGiftCenterMenuItem: b"\x03", wOverworldNPCFlags: b"\x00",
              wTxRam2: b"\xAA\xBB", wPermissionMap: b"\x00" * 0x100},
     "read": {wGiftCenterChoice: 1, wTxRam2: 2, hCurMenuItem: 1,
              wSelectedGiftCenterMenuItem: 1, wOverworldNPCFlags: 1},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory GiftCenterMenu

from tests.cases._schema_migration import legacy_to_schema

# >>> factory gift-center event-value statics
wGiftCenterChoice = 0xD10E
wLoadedEventBits = 0xD3D1
wEventVars = 0xD3D2
# <<< factory gift-center event-value statics

# >>> factory Func_fc7a
# gift_center.asm: `ld a, [wConsole]` / `ld c, a` / set_event_value, 8 bytes of
# code, then `rst $20` at $7C82 starts the script bytecode; completion is
# declared pre-ret there. SetEventValue writes
#   (~mask & [hl]) | ((value << tz(mask)) & mask)
# with (offset, mask) = (0x1B, 0xFF) from EventVarMasks, verified against
# the ROM 2026-08-26.
# mask 0xFF replaces the whole byte; seeding the var to 0xFF proves the write
# happened rather than coinciding with a zeroed default.
CONTRACT["Func_fc7a"] = {"compare": ("a", "c"), "preserve": ("b", "d", "e", "hl")}
CASES["Func_fc7a"] = [
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wConsole: b"\x02", wEventVars + 0x1B: b"\xFF"},
     "read": {wLoadedEventBits: 1, wEventVars + 0x1B: 1}},
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wConsole: b"\x00", wEventVars + 0x1B: b"\xFF"},
     "read": {wLoadedEventBits: 1, wEventVars + 0x1B: 1}},
    dict(POISON,
         wram={wConsole: b"\xFF", wEventVars + 0x1B: b"\x00"},
         read={wLoadedEventBits: 1, wEventVars + 0x1B: 1}),
]
# <<< factory Func_fc7a

# >>> factory Func_fcad
# gift_center.asm: `ld a, [wGiftCenterChoice]` / `ld c, a` / set_event_value, 8 bytes of
# code, then `rst $20` at $7CB5 starts the script bytecode; completion is
# declared pre-ret there. SetEventValue writes
#   (~mask & [hl]) | ((value << tz(mask)) & mask)
# with (offset, mask) = (0x1A, 0xFC) from EventVarMasks, verified against
# the ROM 2026-08-26.
# tz=2, so this is the first landed routine where the shift-alignment loop
# actually runs. The event shares byte 0x1A with EVENT_AARON_BOOSTER_REWARD
# (mask 0x03): seeding the var to 0xFF proves the low bits survive.
CONTRACT["Func_fcad"] = {"compare": ("a", "c"), "preserve": ("b", "d", "e", "hl")}
CASES["Func_fcad"] = [
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wGiftCenterChoice: b"\x02", wEventVars + 0x1A: b"\xFF"},
     "read": {wLoadedEventBits: 1, wEventVars + 0x1A: 1}},
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wGiftCenterChoice: b"\x00", wEventVars + 0x1A: b"\xFF"},
     "read": {wLoadedEventBits: 1, wEventVars + 0x1A: 1}},
    dict(POISON,
         wram={wGiftCenterChoice: b"\xFF", wEventVars + 0x1A: b"\x00"},
         read={wLoadedEventBits: 1, wEventVars + 0x1A: 1}),
]
# <<< factory Func_fcad

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-completion gift-center event-value entries
# legacy_to_schema always emits completion "return"; both routines end at their
# `rst $20`, so the split is applied after migration.
for _fn, _pc in (
        ("Func_fc7a", 0x7C82),
        ("Func_fcad", 0x7CB5),
):
    for _rec in SCHEMA2_CASES[_fn]:
        _rec["completion"] = {"mode": "pre-ret", "pc": _pc}
# <<< factory-completion gift-center event-value entries

MUTATIONS = {}
# >>> factory-mutation Preload_GiftCenterClerk
MUTATIONS["Preload_GiftCenterClerk"] = {
    "source_symbol": "Preload_GiftCenterClerk",
    "before": "if (console == CONSOLE_CGB)",
    "after": "if (console != CONSOLE_CGB)",
    "case_ids": ["Preload_GiftCenterClerk-0", "Preload_GiftCenterClerk-1",
                 "Preload_GiftCenterClerk-2", "Preload_GiftCenterClerk-3",
                 "Preload_GiftCenterClerk-4"],
}
# <<< factory-mutation Preload_GiftCenterClerk
# >>> factory-mutation Func_fc7a
MUTATIONS["Func_fc7a"] = {"source_symbol": "Func_fc7a", "before": "\twritten = (uint8_t)((event & (uint8_t)~0xFFu) | (value & 0xFFu));", "after": "\twritten = (uint8_t)((event & (uint8_t)0xFFu) | (value & 0xFFu));", "case_ids": ["Func_fc7a-0", "Func_fc7a-1", "Func_fc7a-2"]}
# <<< factory-mutation Func_fc7a
# >>> factory-mutation Func_fcad
MUTATIONS["Func_fcad"] = {"source_symbol": "Func_fcad", "before": "\twritten = (uint8_t)((event & (uint8_t)~0xFCu) | ((uint8_t)(value << 2u) & 0xFCu));", "after": "\twritten = (uint8_t)((event & (uint8_t)~0xFCu) | ((uint8_t)(value << 1u) & 0xFCu));", "case_ids": ["Func_fcad-0", "Func_fcad-1", "Func_fcad-2"]}
# <<< factory-mutation Func_fcad
# >>> factory-mutation GiftCenterMenu
MUTATIONS["GiftCenterMenu"] = {
    "source_symbol": "GiftCenterMenu",
    "before": "\tuint8_t selected = wSelectedGiftCenterMenuItem;\n\tInitAndPrintMenu(GIFT_CENTER_MENU_PARAMS, selected);",
    "after": "\tuint8_t selected = wSelectedGiftCenterMenuItem;\n\tInitAndPrintMenu(GIFT_CENTER_MENU_PARAMS, (uint8_t)(selected ^ 1u));",
    "case_ids": ["GiftCenterMenu-0", "GiftCenterMenu-1", "GiftCenterMenu-4"],
}
# <<< factory-mutation GiftCenterMenu
