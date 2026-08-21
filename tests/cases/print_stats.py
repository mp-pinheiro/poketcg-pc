"""Oracle-diff cases for poketcg/src/engine/menus/print_stats.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DrawPauseMenuPlayerPortrait
CONTRACT["DrawPauseMenuPlayerPortrait"] = {"compare": (), "preserve": ()}
CASES["DrawPauseMenuPlayerPortrait"] = [
    {"wram": {0xD61E: b"\x00"}, "read": {0xD61E: 1}},
    dict(POISON, wram={0xD61E: b"\xFF"}, read={0xD61E: 1}),
]
# <<< factory DrawPauseMenuPlayerPortrait

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DrawPauseMenuPlayerPortrait
MUTATIONS["DrawPauseMenuPlayerPortrait"] = {
    "source_symbol": "DrawPauseMenuPlayerPortrait",
    "before": "\tDrawPlayerPortrait();",
    "after": "\t(void)0;",
    "case_ids": ["DrawPauseMenuPlayerPortrait-0", "DrawPauseMenuPlayerPortrait-1"],
}
# <<< factory-mutation DrawPauseMenuPlayerPortrait
