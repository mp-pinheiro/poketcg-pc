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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

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
