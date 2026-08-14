# >>> factory-cases-statics
wScriptPointer = 0xD413
wLoadedEventBits = 0xD3D1
wEventVars = 0xD3D2

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics







CONTRACT = {}
CASES = {}

# >>> factory IncreaseScriptPointer
CONTRACT["IncreaseScriptPointer"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "d", "e", "hl"),
}
CASES["IncreaseScriptPointer"] = [
    {"a": 0, "wram": {wScriptPointer: b"\x00\x00"},
     "read": {wScriptPointer: 2}},
    dict(POISON, a=1, wram={wScriptPointer: b"\x00\xC1"},
         read={wScriptPointer: 2}),
    {"a": 0xFF, "wram": {wScriptPointer: b"\xFF\xFF"},
     "read": {wScriptPointer: 2}},
    {"a": 1, "wram": {wScriptPointer: b"\xFF\xFF"},
     "read": {wScriptPointer: 2}},
]
# <<< factory IncreaseScriptPointer


# >>> factory SetScriptPointer
CONTRACT["SetScriptPointer"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "f", "b", "c", "d", "e"),
}
CASES["SetScriptPointer"] = [
    {"b": 0, "c": 0, "wram": {wScriptPointer: b"\xFF\xFF"},
     "read": {wScriptPointer: 2}},
    dict(POISON, b=0xBB, c=0xCC,
         wram={wScriptPointer: b"\x11\x22"}, read={wScriptPointer: 2}),
    {"b": 0xFF, "c": 0xFF, "wram": {wScriptPointer: b"\x00\x00"},
     "read": {wScriptPointer: 2}},
]
# <<< factory SetScriptPointer


# >>> factory GetScriptArgsAfterPointer
CONTRACT["GetScriptArgsAfterPointer"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("d", "e", "hl"),
}
CASES["GetScriptArgsAfterPointer"] = [
    {"a": 0, "wram": {wScriptPointer: b"\x00\xC1",
                        0xC100: b"\x34\x12"}},
    dict(POISON, a=1, wram={wScriptPointer: b"\x00\xC1",
                            0xC101: b"\x56\x78"}),
    {"a": 0xFF, "wram": {wScriptPointer: b"\x00\xC1",
                           0xC1FF: b"\x00\x00"}},
    {"a": 1, "wram": {wScriptPointer: b"\xFF\xC1",
                        0xC200: b"\xAA\xBB"}},
]
# <<< factory GetScriptArgsAfterPointer


# >>> factory GetEventVar
CONTRACT["GetEventVar"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e"),
}
CASES["GetEventVar"] = [
    {"a": 0, "read": {wLoadedEventBits: 1}},
    dict(POISON, a=1, read={wLoadedEventBits: 1}),
    {"a": 0x7F, "read": {wLoadedEventBits: 1}},
    {"a": 0x80, "read": {wLoadedEventBits: 1}},
    {"a": 0xFF, "read": {wLoadedEventBits: 1}},
]
# <<< factory GetEventVar


# >>> factory IncreaseScriptPointerBy1
CONTRACT["IncreaseScriptPointerBy1"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy1"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy1

# >>> factory IncreaseScriptPointerBy2
CONTRACT["IncreaseScriptPointerBy2"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy2"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy2

# >>> factory IncreaseScriptPointerBy4
CONTRACT["IncreaseScriptPointerBy4"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy4"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy4

# >>> factory IncreaseScriptPointerBy3
CONTRACT["IncreaseScriptPointerBy3"] = {"compare": ("a", "f", "c"), "preserve": ()}
CASES["IncreaseScriptPointerBy3"] = [
	{},
	dict(POISON),
]
# <<< factory IncreaseScriptPointerBy3

# >>> factory GetScriptArgs5AfterPointer
CONTRACT["GetScriptArgs5AfterPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl")}
CASES["GetScriptArgs5AfterPointer"] = [
	# All-zero entry state. The setup is mandatory warmth: with the script
	# pointer left at $0000 the routine reads bus addresses the oracle's RAM
	# snapshot cannot capture (previous round's ValueError), so every case
	# points the script pointer at scratch WRAM via the ported SetScriptPointer.
	# The first two seeded bytes spell the pointer little-endian so the pointer
	# is $C1xx under either reading of SetScriptPointer's bc operand.
	{"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x00}], "read": {0xC100: 16}},
	dict(POISON, setup=[{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x00}],
	     wram={0xC100: b"\x00\xc1\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\x0f"}),
	{"setup": [{"fn": "SetScriptPointer", "b": 0xC1, "c": 0x40}],
	 "wram": {0xC140: b"\x40\xc1\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\x0f"},
	 "read": {0xC140: 16}},
	{"setup": [{"fn": "SetScriptPointer", "b": 0xC9, "c": 0xF0}],
	 "wram": {0xC9F0: b"\xf0\xc9\x7e\x81\xfe\x01\xc3\x3c"}},
]
# <<< factory GetScriptArgs5AfterPointer

# >>> factory SetScriptControlByteFail
CONTRACT["SetScriptControlByteFail"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetScriptControlByteFail"] = [
	{},
	{"a": 0x5A, "wram": {0xD415: b"\x80"}},
	{"f": 0x50, "wram": {0xD415: b"\xff"}},
	dict(POISON, wram={0xD415: b"\xff"}),
]
# <<< factory SetScriptControlByteFail

# >>> factory IncreaseScriptPointerBy5
CONTRACT["IncreaseScriptPointerBy5"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["IncreaseScriptPointerBy5"] = [
	{},
	dict(POISON),
	dict(POISON, wram={0xC100: b"\x11\x22\x33\x44"}),
]
# <<< factory IncreaseScriptPointerBy5

# >>> factory IncreaseScriptPointerBy6
CONTRACT["IncreaseScriptPointerBy6"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["IncreaseScriptPointerBy6"] = [
	{},
	dict(POISON),
	dict(POISON, wram={0xC100: b"\x11\x22\x33\x44"}),
]
# <<< factory IncreaseScriptPointerBy6

# >>> factory IncreaseScriptPointerBy7
CONTRACT["IncreaseScriptPointerBy7"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e", "hl")}
CASES["IncreaseScriptPointerBy7"] = [
	{},
	dict(POISON),
	dict(POISON, wram={0xC100: b"\x11\x22\x33\x44"}),
]
# <<< factory IncreaseScriptPointerBy7

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}

# >>> factory-mutation IncreaseScriptPointer
MUTATIONS["IncreaseScriptPointer"] = {
    "source_symbol": "IncreaseScriptPointer",
    "before": "uint16_t low_sum = (uint16_t)low + a;",
    "after": "uint16_t low_sum = (uint16_t)low + (uint8_t)(a << 1);",
    "case_ids": ["IncreaseScriptPointer-1", "IncreaseScriptPointer-2"],
}
# <<< factory-mutation IncreaseScriptPointer

# >>> factory-mutation SetScriptPointer
MUTATIONS["SetScriptPointer"] = {
    "source_symbol": "SetScriptPointer",
    "before": "gb_write8(wScriptPointer_ADDR, (uint8_t)bc);",
    "after": "gb_write8(wScriptPointer_ADDR, (uint8_t)(bc ^ 0xFFu));",
    "case_ids": ["SetScriptPointer-1", "SetScriptPointer-2"],
}
# <<< factory-mutation SetScriptPointer

# >>> factory-mutation GetScriptArgsAfterPointer
MUTATIONS["GetScriptArgsAfterPointer"] = {
    "source_symbol": "GetScriptArgsAfterPointer",
    "before": "uint16_t target = (uint16_t)(pointer + a);",
    "after": "uint16_t target = (uint16_t)(pointer + (uint8_t)(a + 1u));",
    "case_ids": ["GetScriptArgsAfterPointer-1", "GetScriptArgsAfterPointer-3"],
}
# <<< factory-mutation GetScriptArgsAfterPointer

# >>> factory-mutation GetEventVar
MUTATIONS["GetEventVar"] = {
    "source_symbol": "GetEventVar",
    "before": "uint16_t bc = (uint16_t)a * 2u;",
    "after": "uint16_t bc = (uint16_t)a * 4u;",
    "case_ids": ["GetEventVar-1", "GetEventVar-3", "GetEventVar-4"],
}
# <<< factory-mutation GetEventVar
# >>> factory-mutation IncreaseScriptPointerBy1
MUTATIONS["IncreaseScriptPointerBy1"] = {"source_symbol": "IncreaseScriptPointerBy1", "before": "return IncreaseScriptPointer(1u);", "after": "return IncreaseScriptPointer(2u);", "case_ids": ["IncreaseScriptPointerBy1-0", "IncreaseScriptPointerBy1-1"]}
# <<< factory-mutation IncreaseScriptPointerBy1
# >>> factory-mutation IncreaseScriptPointerBy2
MUTATIONS["IncreaseScriptPointerBy2"] = {"source_symbol": "IncreaseScriptPointerBy2", "before": "return IncreaseScriptPointer(2u);", "after": "return IncreaseScriptPointer(1u);", "case_ids": ["IncreaseScriptPointerBy2-0", "IncreaseScriptPointerBy2-1"]}
# <<< factory-mutation IncreaseScriptPointerBy2
# >>> factory-mutation IncreaseScriptPointerBy4
MUTATIONS["IncreaseScriptPointerBy4"] = {"source_symbol": "IncreaseScriptPointerBy4", "before": "return IncreaseScriptPointer(4u);", "after": "return IncreaseScriptPointer(1u);", "case_ids": ["IncreaseScriptPointerBy4-0", "IncreaseScriptPointerBy4-1"]}
# <<< factory-mutation IncreaseScriptPointerBy4
# >>> factory-mutation IncreaseScriptPointerBy3
MUTATIONS["IncreaseScriptPointerBy3"] = {
	"source_symbol": "IncreaseScriptPointerBy3",
	"before": "return IncreaseScriptPointer(3u);",
	"after": "return IncreaseScriptPointer(4u);",
	"case_ids": ["IncreaseScriptPointerBy3-0", "IncreaseScriptPointerBy3-1"],
}
# <<< factory-mutation IncreaseScriptPointerBy3
# >>> factory-mutation GetScriptArgs5AfterPointer
MUTATIONS["GetScriptArgs5AfterPointer"] = {
	"source_symbol": "GetScriptArgs5AfterPointer",
	"before": "\treturn GetScriptArgsAfterPointer(5u);",
	"after": "\treturn GetScriptArgsAfterPointer(4u);",
	"case_ids": ["GetScriptArgs5AfterPointer-1", "GetScriptArgs5AfterPointer-2", "GetScriptArgs5AfterPointer-3"],
}
# <<< factory-mutation GetScriptArgs5AfterPointer
# >>> factory-mutation SetScriptControlByteFail
MUTATIONS["SetScriptControlByteFail"] = {
	"source_symbol": "SetScriptControlByteFail",
	"before": "\treturn (SetScriptControlByteFailResult){0x00u, 0x80u};",
	"after": "\treturn (SetScriptControlByteFailResult){0x00u, 0x90u};",
	"case_ids": ["SetScriptControlByteFail-0", "SetScriptControlByteFail-1", "SetScriptControlByteFail-2", "SetScriptControlByteFail-3"],
}
# <<< factory-mutation SetScriptControlByteFail
# >>> factory-mutation IncreaseScriptPointerBy5
MUTATIONS["IncreaseScriptPointerBy5"] = {
	"source_symbol": "IncreaseScriptPointerBy5",
	"before": "\treturn IncreaseScriptPointer(5u);",
	"after": "\treturn IncreaseScriptPointer(6u);",
	"case_ids": ["IncreaseScriptPointerBy5-0", "IncreaseScriptPointerBy5-1", "IncreaseScriptPointerBy5-2"],
}
# <<< factory-mutation IncreaseScriptPointerBy5
# >>> factory-mutation IncreaseScriptPointerBy6
MUTATIONS["IncreaseScriptPointerBy6"] = {
	"source_symbol": "IncreaseScriptPointerBy6",
	"before": "\treturn IncreaseScriptPointer(6u);",
	"after": "\treturn IncreaseScriptPointer(5u);",
	"case_ids": ["IncreaseScriptPointerBy6-0", "IncreaseScriptPointerBy6-1", "IncreaseScriptPointerBy6-2"],
}
# <<< factory-mutation IncreaseScriptPointerBy6
# >>> factory-mutation IncreaseScriptPointerBy7
MUTATIONS["IncreaseScriptPointerBy7"] = {
	"source_symbol": "IncreaseScriptPointerBy7",
	"before": "\treturn IncreaseScriptPointer(7u);",
	"after": "\treturn IncreaseScriptPointer(6u);",
	"case_ids": ["IncreaseScriptPointerBy7-0", "IncreaseScriptPointerBy7-1", "IncreaseScriptPointerBy7-2"],
}
# <<< factory-mutation IncreaseScriptPointerBy7
