"""Oracle-diff cases for poketcg/src/engine/menus/debug_main.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
HCUR_MENU_ITEM = 0xFFB1

CONTRACT = {
    "Func_126b3": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e"),
    },
}

# Item 10 selects DebugQuit, the sole table target with a bounded return
# without depending on another unported debug routine.
CASES = {
    "Func_126b3": [
        {"setup": [{"fn": "SetMenuItem", "a": 10}],
         "wram": {HCUR_MENU_ITEM: b"\x0a"}, "read": {HCUR_MENU_ITEM: 1}},
        dict(POISON, setup=[{"fn": "SetMenuItem", "a": 10}],
             wram={HCUR_MENU_ITEM: b"\x0a"}, read={HCUR_MENU_ITEM: 1}),
        {"a": 0xFF, "f": 0xFF, "setup": [{"fn": "SetMenuItem", "a": 10}],
         "wram": {HCUR_MENU_ITEM: b"\x0a"}, "read": {HCUR_MENU_ITEM: 1}},
    ],
}

MUTATIONS = {
    "Func_126b3": {
        "source_symbol": "Func_126b3",
        "before": "menu == 10u",
        "after": "menu == 11u",
        "case_ids": ["Func_126b3-0", "Func_126b3-1", "Func_126b3-2"],
    },
}

# >>> factory-cases-statics
DM_hCurMenuItem = 0xFFB1
DM_wConsole = 0xCAB4
DM_wTileMapFill = 0xCAB6
DM_wVBlankFunctionTrampoline = 0xCAD0
DM_wLineSeparation = 0xCD08
DM_wDebugMenuSelection = 0xD418
DM_wDebugSGBBorder = 0xD419
DM_wDebugBoosterSelection = 0xD41A
# The body's own EnableLCD makes real frames elapse, so the reference VBlank
# handler runs: CopyDMAFunction installs hDMAFunction (Func_12871 sets
# wVBlankOAMCopyToggle, so the handler calls it), and SetupText primes the glyph
# cache the menu text walks.
DM_FRAME_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# One idle frame, then UP+A together ($40|$01). The menu has 11 items and the
# body forces the cursor to item 0, so a single UP wraps it to item 10 and the
# same HandleMenuInput call sees A newly pressed and confirms it. Pressing both
# on one frame makes the pair phase-insensitive: whichever entry the reference
# observes first, the only frame that can leave the loop selects item 10.
DM_KEYS = [0x00, 0x41]
# wVBlankFunctionTrampoline holds a bare `ret` for the reference handler's
# `call wVBlankFunctionTrampoline`; wConsole picks CONSOLE_DMG for
# SetDefaultConsolePalettes. Neither side writes either byte.
DM_SEED = {DM_wConsole: b"\x00", DM_wVBlankFunctionTrampoline: b"\xc9"}
# Only bytes this routine's own asm writes, plus the menu item it dispatches on.
DM_READ = {DM_wTileMapFill: 1, DM_wLineSeparation: 1, DM_wDebugMenuSelection: 1,
           DM_wDebugSGBBorder: 1, DM_wDebugBoosterSelection: 1, DM_hCurMenuItem: 1}
DM_BUDGET = {"instruction_budget": 20000000, "cycle_budget": 80000000}
# <<< factory-cases-statics

# >>> factory Func_12661
CONTRACT["Func_12661"] = {"compare": ("a", "f", "hl"), "preserve": ()}
# Item 10 is DebugQuit (`or a; ret`), the only entry of Unknown_126bb that
# returns nc, which is what lets the outer rebuild loop reach its `ret`.
# rom_bank 4 is the routine's own bank, where Unknown_128f7 lives.
CASES["Func_12661"] = [
    dict(rom_bank=4, keys=DM_KEYS, wram=DM_SEED, setup=DM_FRAME_SETUP,
         read=DM_READ, **DM_BUDGET),
    dict(POISON, rom_bank=4, keys=DM_KEYS, wram=DM_SEED, setup=DM_FRAME_SETUP,
         read=DM_READ, **DM_BUDGET),
]
# <<< factory Func_12661

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation Func_12661
MUTATIONS["Func_12661"] = {
    "source_symbol": "Func_12661",
    "before": "wDebugSGBBorder = 3u;",
    "after": "wDebugSGBBorder = 4u;",
    "case_ids": ["Func_12661-0", "Func_12661-1"],
}
# <<< factory-mutation Func_12661
