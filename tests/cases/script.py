POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCurMap = 0xD32F

CONTRACT = {
    "GetMapScriptPointer": {"compare": ("a", "b", "c", "d", "e", "f", "hl"), "preserve": ("b", "c", "d", "e")},
}

CASES = {
    # The oracle resolves MapScripts (04:562A) from the real ROM, so these seed
    # only the map id and script selector; the pointer and its flags are diffed.
    "GetMapScriptPointer": [
        {"hl": 0x0004, "wram": {wCurMap: b"\x00"}},
        {"hl": 0x0006, "wram": {wCurMap: b"\x00"}},
        {"hl": 0x0004, "wram": {wCurMap: b"\x01"}},
        {"hl": 0x0006, "wram": {wCurMap: b"\x02"}},
        dict(POISON, hl=0x0004, wram={wCurMap: b"\x03"}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "GetMapScriptPointer": {
        "source_symbol": "GetMapScriptPointer",
        "before": "(uint16_t)(MAP_SCRIPTS + (uint16_t)wCurMap * 16u + l)",
        "after":  "(uint16_t)(MAP_SCRIPTS + (uint16_t)wCurMap * 15u + l)",
        "case_ids": ["GetMapScriptPointer-0", "GetMapScriptPointer-1", "GetMapScriptPointer-2", "GetMapScriptPointer-3", "GetMapScriptPointer-4"],
    },
}
