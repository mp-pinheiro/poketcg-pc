"""Oracle-diff cases for _PauseMenu_Exit (engine/menus/give_booster_pack.asm:113).

_PauseMenu_Exit is a bare ret: it reads nothing, writes nothing, and preserves
all registers.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    # All registers are preserved by a bare ret.
    "_PauseMenu_Exit": ("a", "f", "b", "c", "d", "e", "hl"),
}

CASES = {
    "_PauseMenu_Exit": [
        # All-zero baseline, including an untouched WRAM byte.
        {"wram": {0xC000: b"\x5A"}, "read": {0xC000: 1}},
        # Poisoned registers and untouched WRAM must survive unchanged.
        dict(POISON, wram={0xC000: b"\xA5"}, read={0xC000: 1}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "_PauseMenu_Exit": {
        "source_symbol": "_PauseMenu_Exit",
        "before": "void _PauseMenu_Exit(void)\n{\n}",
        "after": "void _PauseMenu_Exit(void)\n{\n\tgb_write8(0xC000, 0x01);\n}",
        "case_ids": ["_PauseMenu_Exit-0", "_PauseMenu_Exit-1"],
    },
}
