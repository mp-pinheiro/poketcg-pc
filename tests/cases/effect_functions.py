"""Oracle-diff cases for poketcg/src/engine/duel/effect_functions.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}




# >>> factory UpdateExpectedAIDamage
CONTRACT["UpdateExpectedAIDamage"] = {"compare": (), "preserve": ()}
CASES["UpdateExpectedAIDamage"] = [
	{"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0x05, "d": 0x03, "e": 0x07, "wram": {0xCCB9: b"\x10"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0xFF, "d": 0xFF, "e": 0xFF, "wram": {0xCCB9: b"\xFF"}, "read": {0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}},
	dict(POISON, wram={0xCCB9: b"\x22"}, read={0xCCB9: 1, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory UpdateExpectedAIDamage


# >>> factory SetExpectedAIDamage
CONTRACT["SetExpectedAIDamage"] = {"compare": (), "preserve": ()}
CASES["SetExpectedAIDamage"] = [
	{"wram": {0xCCB9: b"\x00\x00"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0x05, "d": 0x03, "e": 0x07, "wram": {0xCCB9: b"\xAA\xBB"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
	{"a": 0xFF, "d": 0xFF, "e": 0xFF, "wram": {0xCCB9: b"\x01\x02"}, "read": {0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}},
	dict(POISON, wram={0xCCB9: b"\x33\x44"}, read={0xCCB9: 2, 0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory SetExpectedAIDamage


from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation UpdateExpectedAIDamage
MUTATIONS["UpdateExpectedAIDamage"] = {
	"source_symbol": "UpdateExpectedAIDamage",
	"before": "gb_write8(wDamage_ADDR, (uint8_t)(a + hl));",
	"after": "gb_write8(wDamage_ADDR, (uint8_t)(a + hl + 1u));",
	"case_ids": ["UpdateExpectedAIDamage-0", "UpdateExpectedAIDamage-1", "UpdateExpectedAIDamage-2", "UpdateExpectedAIDamage-3"],
}
# <<< factory-mutation UpdateExpectedAIDamage
# >>> factory-mutation SetExpectedAIDamage
MUTATIONS["SetExpectedAIDamage"] = {
	"source_symbol": "SetExpectedAIDamage",
	"before": "gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);",
	"after": "gb_write8((uint16_t)(wDamage_ADDR + 1u), 1u);",
	"case_ids": ["SetExpectedAIDamage-0", "SetExpectedAIDamage-1", "SetExpectedAIDamage-2", "SetExpectedAIDamage-3"],
}
# <<< factory-mutation SetExpectedAIDamage
