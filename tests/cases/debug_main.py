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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
