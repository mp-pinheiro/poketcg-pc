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


# >>> factory SetNoEffectFromStatus
CONTRACT["SetNoEffectFromStatus"] = {"compare": (), "preserve": ()}
CASES["SetNoEffectFromStatus"] = [
    {"read": {0xCCED: 1}},
    dict(POISON, read={0xCCED: 1}),
]
# <<< factory SetNoEffectFromStatus

# >>> factory SetDefiniteAIDamage
CONTRACT["SetDefiniteAIDamage"] = {"compare": (), "preserve": ()}
CASES["SetDefiniteAIDamage"] = [
    {"wram": {0xCCB9: b"\x00"}, "read": {0xCCBB: 1, 0xCCBC: 1}},
    {"wram": {0xCCB9: b"\x42"}, "read": {0xCCBB: 1, 0xCCBC: 1}},
    dict(POISON, wram={0xCCB9: b"\x99"}, read={0xCCBB: 1, 0xCCBC: 1}),
]
# <<< factory SetDefiniteAIDamage

# >>> factory PickRandomPlayAreaCard
CONTRACT["PickRandomPlayAreaCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PickRandomPlayAreaCard"] = [
	{"a": 0},
	{"a": 1},
	dict(POISON, a=0x40),
]
# <<< factory PickRandomPlayAreaCard

# >>> factory GetNextPositionInTempList
CONTRACT["GetNextPositionInTempList"] = {"compare": ("hl", "d", "e"), "preserve": ("d", "e")}
CASES["GetNextPositionInTempList"] = [
	{"wram": {0xFFB2: b"\x00"}, "read": {0xFFB2: 1}},
	{"wram": {0xFFB2: b"\x01"}, "read": {0xFFB2: 1}},
	dict(POISON, wram={0xFFB2: b"\xFF"}, read={0xFFB2: 1}),
]
# <<< factory GetNextPositionInTempList

# >>> factory QueueStatusCondition
wStatusConditionQueue = 0xCCCE
wStatusConditionQueueIndex = 0xCCCD
wTempNonTurnDuelistCardID = 0xCCC4
wWhoseTurn = 0xCC05
hWhoseTurn = 0xFF97
wNoEffectFromWhichStatus = 0xCCF1
wEffectFailed = 0xCCED

CONTRACT["QueueStatusCondition"] = {"compare": ("f",), "preserve": ()}
CASES["QueueStatusCondition"] = [
    {"b": 1, "c": 2, "wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x01"},
     "read": {wStatusConditionQueue: 3, wStatusConditionQueueIndex: 1}},
    {"b": 1, "c": 2, "wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x00", wTempNonTurnDuelistCardID: b"\xcb"},
     "read": {wNoEffectFromWhichStatus: 1, wEffectFailed: 1}},
    {"b": 1, "c": 2, "wram": {hWhoseTurn: b"\x00", wWhoseTurn: b"\x00", wTempNonTurnDuelistCardID: b"\xcc"},
     "read": {wNoEffectFromWhichStatus: 1, wEffectFailed: 1}},
    dict(POISON, b=1, c=2, wram={hWhoseTurn: b"\x01", wWhoseTurn: b"\x00"},
         read={wStatusConditionQueue: 3, wStatusConditionQueueIndex: 1}),
    {"b": 3, "c": 4, "wram": {hWhoseTurn: b"\x02", wWhoseTurn: b"\x02", wStatusConditionQueueIndex: b"\x00"},
     "read": {wStatusConditionQueue: 3, wStatusConditionQueueIndex: 1}},
]
# <<< factory QueueStatusCondition

# >>> factory CommentedOut_2c086
CONTRACT["CommentedOut_2c086"] = {"compare": ("a",), "preserve": ("a",)}
CASES["CommentedOut_2c086"] = [
    {"a": 0},
    dict(POISON, a=0xAA),
    {"a": 1},
    {"a": 255},
]
# <<< factory CommentedOut_2c086

# >>> factory SetWasUnsuccessful
wEffectFailed = 0xCCED

CONTRACT["SetWasUnsuccessful"] = {"compare": (), "preserve": ()}
CASES["SetWasUnsuccessful"] = [
    {"wram": {wEffectFailed: b"\x00"}, "read": {wEffectFailed: 1}},
    dict(POISON, wram={wEffectFailed: b"\xFF"}, read={wEffectFailed: 1}),
]
# <<< factory SetWasUnsuccessful

# >>> factory Teleport_SwitchEffect
CONTRACT["Teleport_SwitchEffect"] = {"compare": (), "preserve": ()}
hTemp_ffa0 = 0xFFA0
wDuelDisplayedScreen = 0xCAC2
CASES["Teleport_SwitchEffect"] = [
    {"wram": {hTemp_ffa0: b"\x00", wDuelDisplayedScreen: b"\x05"}},
    {"wram": {hTemp_ffa0: b"\x01", wDuelDisplayedScreen: b"\xFF"}},
    dict(POISON, wram={hTemp_ffa0: b"\x02", wDuelDisplayedScreen: b"\x03"}),
]
# <<< factory Teleport_SwitchEffect

# >>> factory SetDamageToATimes20
CONTRACT["SetDamageToATimes20"] = {"compare": (), "preserve": ()}
wDamage = 0xCCB9
CASES["SetDamageToATimes20"] = [
    {"a": 0, "read": {wDamage: 2}},
    {"a": 1, "read": {wDamage: 2}},
    {"a": 10, "read": {wDamage: 2}},
    {"a": 255, "read": {wDamage: 2}},
    dict(POISON, a=5, read={wDamage: 2}),
]
# <<< factory SetDamageToATimes20

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
# >>> factory-mutation SetNoEffectFromStatus
MUTATIONS["SetNoEffectFromStatus"] = {"source_symbol": "SetNoEffectFromStatus", "before": "gb_write8(0xCCEDu, 0x01u);", "after": "gb_write8(0xCCEDu, 0x02u);", "case_ids": ["SetNoEffectFromStatus-0", "SetNoEffectFromStatus-1"]}
# <<< factory-mutation SetNoEffectFromStatus
# >>> factory-mutation SetDefiniteAIDamage
MUTATIONS["SetDefiniteAIDamage"] = {"source_symbol": "SetDefiniteAIDamage", "before": "gb_write8(0xCCBBu, a);", "after": "gb_write8(0xCCBBu, 0x00u);", "case_ids": ["SetDefiniteAIDamage-1", "SetDefiniteAIDamage-0", "SetDefiniteAIDamage-2"]}
# <<< factory-mutation SetDefiniteAIDamage
# >>> factory-mutation PickRandomPlayAreaCard
MUTATIONS["PickRandomPlayAreaCard"] = {
	"source_symbol": "PickRandomPlayAreaCard",
	"before": "return (PickRandomPlayAreaCardResult){a, (uint8_t)(a == 0 ? 0x80u : 0u)};",
	"after": "return (PickRandomPlayAreaCardResult){a, (uint8_t)(a == 0 ? 0x00u : 0u)};",
	"case_ids": ["PickRandomPlayAreaCard-0"],
}
# <<< factory-mutation PickRandomPlayAreaCard
# >>> factory-mutation GetNextPositionInTempList
MUTATIONS["GetNextPositionInTempList"] = {
	"source_symbol": "GetNextPositionInTempList",
	"before": "return (uint16_t)(hTempList_ADDR + a);",
	"after": "return (uint16_t)(hTempList_ADDR + a + 1u);",
	"case_ids": ["GetNextPositionInTempList-0", "GetNextPositionInTempList-1"],
}
# <<< factory-mutation GetNextPositionInTempList
# >>> factory-mutation QueueStatusCondition
MUTATIONS["QueueStatusCondition"] = {
    "source_symbol": "QueueStatusCondition",
    "before": "return (QueueStatusConditionResult){0x10u};",
    "after": "return (QueueStatusConditionResult){0x00u};",
    "case_ids": ["QueueStatusCondition-0", "QueueStatusCondition-3", "QueueStatusCondition-4"],
}
# <<< factory-mutation QueueStatusCondition
# >>> factory-mutation CommentedOut_2c086
MUTATIONS["CommentedOut_2c086"] = {
    "source_symbol": "CommentedOut_2c086",
    "before": "\treturn a;",
    "after": "\treturn (uint8_t)(a + 1u);",
    "case_ids": ["CommentedOut_2c086-0", "CommentedOut_2c086-1", "CommentedOut_2c086-2", "CommentedOut_2c086-3"],
}
# <<< factory-mutation CommentedOut_2c086
# >>> factory-mutation SetWasUnsuccessful
MUTATIONS["SetWasUnsuccessful"] = {
    "source_symbol": "SetWasUnsuccessful",
    "before": "wEffectFailed = EFFECT_FAILED_UNSUCCESSFUL;",
    "after": "wEffectFailed = 0x00u;",
    "case_ids": ["SetWasUnsuccessful-0", "SetWasUnsuccessful-1"],
}
# <<< factory-mutation SetWasUnsuccessful
# >>> factory-mutation Teleport_SwitchEffect
MUTATIONS["Teleport_SwitchEffect"] = {
    "source_symbol": "Teleport_SwitchEffect",
    "before": "wDuelDisplayedScreen = 0u;",
    "after": "wDuelDisplayedScreen = 1u;",
    "case_ids": ["Teleport_SwitchEffect-0", "Teleport_SwitchEffect-1"],
}
# <<< factory-mutation Teleport_SwitchEffect
# >>> factory-mutation SetDamageToATimes20
MUTATIONS["SetDamageToATimes20"] = {
    "source_symbol": "SetDamageToATimes20",
    "before": "hl = (uint16_t)(hl + de);",
    "after": "hl = (uint16_t)(hl - de);",
    "case_ids": ["SetDamageToATimes20-1", "SetDamageToATimes20-2", "SetDamageToATimes20-3"],
}
# <<< factory-mutation SetDamageToATimes20
