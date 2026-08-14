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
