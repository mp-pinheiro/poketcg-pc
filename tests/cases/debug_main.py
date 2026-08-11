"""Oracle-diff cases for poketcg/src/engine/menus/debug_main.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
HCUR_MENU_ITEM = 0xFFB1

CONTRACT = {
    "Func_126b3": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

# Item 10 selects DebugQuit, the sole table target with a bounded return
# without depending on another unported debug routine.
CASES = {
    "Func_126b3": [
        {"wram": {HCUR_MENU_ITEM: b"\x0a"}, "read": {HCUR_MENU_ITEM: 1}},
        dict(POISON, wram={HCUR_MENU_ITEM: b"\x0a"}, read={HCUR_MENU_ITEM: 1}),
        {"a": 0xFF, "f": 0xFF, "wram": {HCUR_MENU_ITEM: b"\x0a"},
         "read": {HCUR_MENU_ITEM: 1}},
    ],
}

MUTATIONS = {
    "Func_126b3": {
        "source_symbol": "Func_126b3",
        "before": "a == 0 ? 0x80u : 0x00u",
        "after": "a == 0 ? 0x00u : 0x00u",
        "case_ids": ["Func_126b3-0", "Func_126b3-1", "Func_126b3-2"],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
