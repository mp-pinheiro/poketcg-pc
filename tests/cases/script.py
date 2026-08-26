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
# >>> factory ResetAnimationQueue
_HBANK_ROM = 0xFF80
_WDO_FRAME_FN = 0xCAD3
CONTRACT["ResetAnimationQueue"] = {"compare": (), "preserve": ()}
CASES["ResetAnimationQueue"] = [
	{"wram": {_HBANK_ROM: b"\x04", _WDO_FRAME_FN: b"\x00\x00"},
	 "read": {_HBANK_ROM: 1, _WDO_FRAME_FN: 2}},
	dict(POISON, wram={_HBANK_ROM: b"\x07", _WDO_FRAME_FN: b"\xff\xff"},
	     read={_HBANK_ROM: 1, _WDO_FRAME_FN: 2}),
]
# <<< factory ResetAnimationQueue

# >>> factory FinishQueuedAnimations
_HBANK_ROM = 0xFF80
_WDO_FRAME_FN = 0xCAD3
_WVBL_TOGGLE = 0xCAC0
_WANIM_QUEUE = 0xD423
_WBUF_POS = 0xD4AC
CONTRACT["FinishQueuedAnimations"] = {"compare": (), "preserve": ()}
CASES["FinishQueuedAnimations"] = [
	{"wram": {_HBANK_ROM: b"\x04", _WDO_FRAME_FN: b"\x11\x22"},
	 "read": {_HBANK_ROM: 1, _WDO_FRAME_FN: 2, _WVBL_TOGGLE: 1}},
	{"wram": {_HBANK_ROM: b"\x04", _WDO_FRAME_FN: b"\xA2\x3B",
	          _WANIM_QUEUE: b"\xff" * 7, _WBUF_POS: b"\x00\x00"},
	 "read": {_HBANK_ROM: 1, _WDO_FRAME_FN: 2, _WVBL_TOGGLE: 1}},
	dict(POISON, wram={_HBANK_ROM: b"\x07", _WDO_FRAME_FN: b"\x33\x44"},
	     read={_HBANK_ROM: 1, _WDO_FRAME_FN: 2, _WVBL_TOGGLE: 1}),
]
# <<< factory FinishQueuedAnimations

# >>> factory GetNPCDuelConfigurations
CONTRACT["GetNPCDuelConfigurations"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetNPCDuelConfigurations"] = [
    {},
    dict(POISON),
]
# <<< factory GetNPCDuelConfigurations

# >>> factory-cases-statics
wCurMap = 0xD32F
wPlayerXCoord = 0xD330
wPlayerYCoord = 0xD331
wPlayerDirection = 0xD334
hBankROM = 0xFF80
wNextScript = 0xD0C6
wDefaultObjectText = 0xD0CA
wCurrentNPCNameTx = 0xD0C8
# <<< factory-cases-statics

# >>> factory HandleMoveModeAPress
CONTRACT["HandleMoveModeAPress"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("e",)}
CASES["HandleMoveModeAPress"] = [
    {
        "a": 0x11, "f": 0x00, "b": 0x22, "c": 0x33, "d": 0x44, "e": 0x55, "hl": 0x4567,
        "wram": {wCurMap: b"\x01", wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x04", wPlayerDirection: b"\x00", hBankROM: b"\x01"},
        "read": {wNextScript: 2, wDefaultObjectText: 2, wCurrentNPCNameTx: 2}
    },
    dict(POISON, wram={wCurMap: b"\x01", wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x04", wPlayerDirection: b"\x00", hBankROM: b"\x01"}, read={wNextScript: 2, wDefaultObjectText: 2, wCurrentNPCNameTx: 2})
]
# <<< factory HandleMoveModeAPress

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
# >>> factory-mutation ResetAnimationQueue
MUTATIONS["ResetAnimationQueue"] = {
	"source_symbol": "ResetAnimationQueue",
	"before": "void ResetAnimationQueue(void)\n{\n\tuint8_t bank = gb_read8(hBankROM_ADDR);\n\tBankswitchROM(BANK_ANIMATION_CORE);\n\t_ResetAnimationQueue();\n\tBankswitchROM(bank);\n}",
	"after": "void ResetAnimationQueue(void)\n{\n\tuint8_t bank = gb_read8(hBankROM_ADDR);\n\tBankswitchROM(BANK_ANIMATION_CORE);\n\t_ResetAnimationQueue();\n\tBankswitchROM((uint8_t)(bank + 1u));\n}",
	"case_ids": ["ResetAnimationQueue-0", "ResetAnimationQueue-1"],
}
# <<< factory-mutation ResetAnimationQueue
# >>> factory-mutation FinishQueuedAnimations
MUTATIONS["FinishQueuedAnimations"] = {
	"source_symbol": "FinishQueuedAnimations",
	"before": "if (!(r.f & 0x10u)) {",
	"after": "if ((r.f & 0x10u)) {",
	"case_ids": ["FinishQueuedAnimations-0", "FinishQueuedAnimations-1"],
}
# <<< factory-mutation FinishQueuedAnimations
# >>> factory-mutation GetNPCDuelConfigurations
MUTATIONS["GetNPCDuelConfigurations"] = {"source_symbol": "GetNPCDuelConfigurations", "before": "\t_GetNPCDuelDuelConfigurationsResult result = _GetNPCDuelConfigurations(a, f, b, c, d, e, hl);", "after": "\t_GetNPCDuelDuelConfigurationsResult result = _GetNPCDuelConfigurations(a, f, b, c, d, 0u, hl);", "case_ids": ["GetNPCDuelConfigurations-1"]}
# <<< factory-mutation GetNPCDuelConfigurations
# >>> factory-mutation HandleMoveModeAPress
MUTATIONS["HandleMoveModeAPress"] = {"source_symbol": "HandleMoveModeAPress", "before": "\tuint8_t object_direction = wPlayerDirection;", "after": "\tuint8_t object_direction = 0xffu;", "case_ids": ["HandleMoveModeAPress-0", "HandleMoveModeAPress-1"]}
# <<< factory-mutation HandleMoveModeAPress
