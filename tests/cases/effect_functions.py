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


# >>> factory IsPlayerTurn
CONTRACT["IsPlayerTurn"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["IsPlayerTurn"] = [
    {},
    dict(POISON),
    {"b": 1, "c": 2, "d": 3, "e": 4},
]
# <<< factory IsPlayerTurn


# >>> factory UpdateExpectedAIDamage_AccountForPoison
CONTRACT["UpdateExpectedAIDamage_AccountForPoison"] = {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["UpdateExpectedAIDamage_AccountForPoison"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    {"a": 0x05, "d": 0x01, "e": 0x0A, "wram": {0xCCB9: b"\x14"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
    dict(POISON, a=0x03, d=0x07, e=0x11, wram={0xCCB9: b"\x30"}, read={0xCCB9: 1, 0xCCBB: 2}),
    {"a": 0xFF, "d": 0xFF, "e": 0x00, "wram": {0xCCB9: b"\xFF"}, "read": {0xCCB9: 1, 0xCCBB: 2}},
]
# <<< factory UpdateExpectedAIDamage_AccountForPoison

# >>> factory ApplySubstatus1ToAttackingCard
CONTRACT["ApplySubstatus1ToAttackingCard"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["ApplySubstatus1ToAttackingCard"] = [
    {},
    {"a": 1},
    {"a": 0xFF},
    dict(POISON, a=0x20),
]
# <<< factory ApplySubstatus1ToAttackingCard


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
# >>> factory-mutation IsPlayerTurn
MUTATIONS["IsPlayerTurn"] = {
    "source_symbol": "IsPlayerTurn",
    "before": "\tDuelistVarResult r = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);",
    "after": "\tDuelistVarResult r = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);",
    "case_ids": ["IsPlayerTurn-0", "IsPlayerTurn-1", "IsPlayerTurn-2"],
}
# <<< factory-mutation IsPlayerTurn
# >>> factory-mutation UpdateExpectedAIDamage_AccountForPoison
MUTATIONS["UpdateExpectedAIDamage_AccountForPoison"] = {
    "source_symbol": "UpdateExpectedAIDamage_AccountForPoison",
    "before": "\t\tUpdateExpectedAIDamage(a, d, e);",
    "after": "\t\tUpdateExpectedAIDamage(a, e, d);",
    "case_ids": ["UpdateExpectedAIDamage_AccountForPoison-1", "UpdateExpectedAIDamage_AccountForPoison-2"],
}
# <<< factory-mutation UpdateExpectedAIDamage_AccountForPoison
# >>> factory-mutation ApplySubstatus1ToAttackingCard
MUTATIONS["ApplySubstatus1ToAttackingCard"] = {
    "source_symbol": "ApplySubstatus1ToAttackingCard",
    "before": "\treturn (uint16_t)(r.hl + 1u);",
    "after": "\treturn r.hl;",
    "case_ids": ["ApplySubstatus1ToAttackingCard-0", "ApplySubstatus1ToAttackingCard-1", "ApplySubstatus1ToAttackingCard-2", "ApplySubstatus1ToAttackingCard-3"],
}
# <<< factory-mutation ApplySubstatus1ToAttackingCard
