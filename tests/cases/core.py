"""Oracle-diff cases for poketcg/src/engine/duel/core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory SetLineSeparation
CONTRACT["SetLineSeparation"] = {"compare": ("a",), "preserve": ()}
wLineSeparation = 0xCD08
CASES["SetLineSeparation"] = [
	{"a": 0, "wram": {wLineSeparation: b"\xff"}},
	{"a": 1, "wram": {wLineSeparation: b"\x00"}},
	dict(POISON, a=0x20, wram={wLineSeparation: b"\x00"}),
]
# <<< factory SetLineSeparation

# >>> factory PlayAreaScreenMenuFunction
CONTRACT["PlayAreaScreenMenuFunction"] = {"compare": ("f",), "preserve": ()}
CASES["PlayAreaScreenMenuFunction"] = [
    {"keys": 0},
    {"keys": 0x01},
    {"keys": 0x02},
    {"keys": 0x08},
    dict(POISON, keys=0x02),
    dict(POISON, keys=0x00),
]
# <<< factory PlayAreaScreenMenuFunction

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation SetLineSeparation
MUTATIONS["SetLineSeparation"] = {
	"source_symbol": "SetLineSeparation",
	"before": "wLineSeparation = a;",
	"after": "wLineSeparation = (uint8_t)(a + 1u);",
	"case_ids": ["SetLineSeparation-0", "SetLineSeparation-1"],
}
# <<< factory-mutation SetLineSeparation
# >>> factory-mutation PlayAreaScreenMenuFunction
MUTATIONS["PlayAreaScreenMenuFunction"] = {
    "source_symbol": "PlayAreaScreenMenuFunction",
    "before": "return 0xA0u;",
    "after": "return 0x80u;",
    "case_ids": ["PlayAreaScreenMenuFunction-0", "PlayAreaScreenMenuFunction-5"],
}
# <<< factory-mutation PlayAreaScreenMenuFunction
