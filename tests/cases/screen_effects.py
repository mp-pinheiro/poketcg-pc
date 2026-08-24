"""Oracle-diff cases for poketcg/src/engine/duel/animations/screen_effects.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory DecrementScreenAnimDuration
CONTRACT["DecrementScreenAnimDuration"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e")}
CASES["DecrementScreenAnimDuration"] = [
	# all-zero: 0 -> 0xff, Z clear, half-borrow set, carry clear -> f=0x60
	{},
	# entry carry passes through untouched (0 -> 0xff) -> f=0x70
	{"f": 0x10},
	# boundary 1 -> 0: Z set, H clear; poison proves a/b/c/d/e/hl preserved and C carried -> f=0xd0
	dict(POISON, wram={0xD4BB: b"\x01"}),
	# half-borrow boundary 0x10 -> 0x0f; entry Z/N/H bits must not leak into f -> f=0x60
	{"f": 0xE0, "wram": {0xD4BB: b"\x10"}},
	# plain decrement, no flags produced by dec -> f=0x40
	{"wram": {0xD4BB: b"\xff"}},
	# 2 -> 1: result nonzero, no half-borrow -> f=0x40
	{"wram": {0xD4BB: b"\x02"}},
]
# <<< factory DecrementScreenAnimDuration

# >>> factory UpdateShakeOffset
CONTRACT["UpdateShakeOffset"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["UpdateShakeOffset"] = [
	{},
	{"wram": {0xD4BB: b"\x00", 0xD4BC: b"\x00\xC1", 0xC100: b"\x15\x02"}, "read": {0xD4BC: 2, 0xC100: 1}},
	{"wram": {0xD4BB: b"\x15", 0xD4BC: b"\x00\xC1", 0xC100: b"\x15\x02"}, "read": {0xD4BC: 2, 0xC100: 1}},
	{"wram": {0xD4BB: b"\x20", 0xD4BC: b"\x00\xC1", 0xC100: b"\x15\x02"}, "read": {0xD4BC: 2, 0xC100: 1}},
	dict(POISON, wram={0xD4BB: b"\x01", 0xD4BC: b"\x00\xC1", 0xC100: b"\x01\xFF"}, read={0xD4BC: 2, 0xC100: 1}),
]
# <<< factory UpdateShakeOffset

# >>> factory-cases-statics
wActiveScreenAnim = 0xD42A
wScreenAnimUpdatePtr = 0xD4B9
hSCX = 0xFF92
rSCX = 0xFF43
hSCY = 0xFF93
rSTAT = 0xFF41
rIE = 0xFFFF

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wScreenAnimDuration = 0xD4BB
wScreenAnimUpdatePtr = 0xD4B9

wDuelAnimDamage = 0xD4B1
WD4C0 = 0xD4C0
WDUEL_ANIM_RETURN_BANK = 0xD4BE
# <<< factory-cases-statics

# >>> factory DefaultScreenAnimationUpdate
CONTRACT["DefaultScreenAnimationUpdate"] = {"compare": (), "preserve": ()}
CASES["DefaultScreenAnimationUpdate"] = [
    {"wram": {0xD42A: b"\x00", 0xD4B9: b"\x00\x00"}, "hram": {0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, "expect": {0xD42A: b"\xFF", 0xD4B9: b"\xBC\x4C", 0xFF92: b"\x00", 0xFF93: b"\x00", 0xFF41: b"\xBF", 0xFF43: b"\x00", 0xFFFF: b"\xFD"}},
    dict(POISON, wram={0xD42A: b"\x12", 0xD4B9: b"\x34\x56"}, hram={0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, expect={0xD42A: b"\xFF", 0xD4B9: b"\xBC\x4C", 0xFF92: b"\x00", 0xFF93: b"\x00", 0xFF41: b"\xBF", 0xFF43: b"\x00", 0xFFFF: b"\xFD"}),
]
# <<< factory DefaultScreenAnimationUpdate

# >>> factory DoScreenAnimationUpdate
CONTRACT["DoScreenAnimationUpdate"] = {"compare": (), "preserve": ()}
CASES["DoScreenAnimationUpdate"] = [
    {"wram": {wScreenAnimUpdatePtr: b"\xBC\x4C", wScreenAnimDuration: b"\x00"}, "read": {wScreenAnimDuration: 1, wScreenAnimUpdatePtr: 2}},
    dict(POISON, wram={wScreenAnimUpdatePtr: b"\xBC\x4C", wScreenAnimDuration: b"\xFF"}, read={wScreenAnimDuration: 1, wScreenAnimUpdatePtr: 2}),
]
# <<< factory DoScreenAnimationUpdate

# >>> factory LoadDefaultScreenAnimationUpdateWhenFinished
CONTRACT["LoadDefaultScreenAnimationUpdateWhenFinished"] = {"compare": (), "preserve": ()}
CASES["LoadDefaultScreenAnimationUpdateWhenFinished"] = [
    {"wram": {0xD4BB: b"\x00", 0xD42A: b"\x00", 0xD4B9: b"\x00\x00"}, "hram": {0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, "read": {0xD42A: 1, 0xD4B9: 2, 0xFF92: 1, 0xFF93: 1, 0xFF41: 1, 0xFF43: 1, 0xFFFF: 1}},
    dict(POISON, wram={0xD4BB: b"\x01", 0xD42A: b"\x12", 0xD4B9: b"\x34\x56"}, hram={0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, read={0xD42A: 1, 0xD4B9: 2, 0xFF92: 1, 0xFF93: 1, 0xFF41: 1, 0xFF43: 1, 0xFFFF: 1}),
]
# <<< factory LoadDefaultScreenAnimationUpdateWhenFinished

# >>> factory ShakeScreenX
CONTRACT["ShakeScreenX"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenX"] = [
    {"wram": {0xD4B9: b"\x00\x00", 0xD4BC: b"\x00\x00"}, "read": {0xD4B9: 2, 0xD4BC: 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xD4B9: b"\x56\x34", 0xD4BC: b"\x78\x9A"}, "read": {0xD4B9: 2, 0xD4BC: 2}},
]
# <<< factory ShakeScreenX

# >>> factory Func_1ce03
CONTRACT["Func_1ce03"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_1ce03"] = [
    {"a": 0x9E, "wram": {WD4C0: b"\x00", WDUEL_ANIM_RETURN_BANK: b"\x00", wDuelAnimDamage: b"\x34\x12"}, "expect": {WD4C0: b"\x80"}, "read": {WD4C0: 1}},
    dict(POISON, a=0x9E, wram={WD4C0: b"\x00", WDUEL_ANIM_RETURN_BANK: b"\x00", wDuelAnimDamage: b"\x78\x56"}, expect={WD4C0: b"\x80"}, read={WD4C0: 1}),
]
# <<< factory Func_1ce03

# >>> factory ShakeScreenX_Big
CONTRACT["ShakeScreenX_Big"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenX_Big"] = [
    {"wram": {0xD4B9: b"\x00\x00", 0xD4BC: b"\x00\x00"}, "read": {0xD4B9: 2, 0xD4BC: 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xD4B9: b"\x56\x78", 0xD4BC: b"\x9A\xBC"}, "read": {0xD4B9: 2, 0xD4BC: 2}},
]
# <<< factory ShakeScreenX_Big

# >>> factory ShakeScreenX_Small
CONTRACT["ShakeScreenX_Small"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenX_Small"] = [
    {"wram": {0xD4B9: b"\x00\x00", 0xD4BC: b"\x00\x00"}, "read": {0xD4B9: 2, 0xD4BC: 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {0xD4B9: b"\x56\x78", 0xD4BC: b"\x9A\xBC"}, "read": {0xD4B9: 2, 0xD4BC: 2}},
]
# <<< factory ShakeScreenX_Small

# >>> factory DistortScreen
CONTRACT["DistortScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DistortScreen"] = [
    {"wram": {0xD4BB: b"\x03"},
     "read": {0xD4B9: 2, 0xD667: 1, 0xCACE: 2, 0xD666: 1, 0xD4BB: 1}},
    dict(POISON, wram={0xD4BB: b"\x10"},
         read={0xD4B9: 2, 0xD667: 1, 0xCACE: 2, 0xD666: 1, 0xD4BB: 1}),
]
# <<< factory DistortScreen

# >>> factory WhiteFlashScreen
CONTRACT["WhiteFlashScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["WhiteFlashScreen"] = [
    {"wram": {0xD4BB: b"\x00", 0xCABC: b"\x11"},
     "read": {0xD4B9: 2, 0xD4BC: 1, 0xCAF0: 8, 0xD297: 8, 0xD4BB: 1}},
    dict(POISON, wram={0xD4BB: b"\x05", 0xCABC: b"\x22"},
         read={0xD4B9: 2, 0xD4BC: 1, 0xCAF0: 8, 0xD297: 8, 0xD4BB: 1}),
]
# <<< factory WhiteFlashScreen

# >>> factory ShakeScreenY
CONTRACT["ShakeScreenY"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ShakeScreenY"] = [
    {"hl": 0x4D61, "wram": {0xD4BC: b"\x00\x00", 0xD4B9: b"\x00\x00"},
     "expect": {0xD4BC: b"\x61\x4D", 0xD4B9: b"\x2B\x4D"}},
    dict(POISON, wram={0xD4BC: b"\x00\x00", 0xD4B9: b"\x00\x00"}),
]
# <<< factory ShakeScreenY

# >>> factory ShakeScreenY_Big
CONTRACT["ShakeScreenY_Big"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenY_Big"] = [
    {"read": {0xD4B9: 2, 0xD4BC: 2}},
    dict(POISON, read={0xD4B9: 2, 0xD4BC: 2}),
]
# <<< factory ShakeScreenY_Big

# >>> factory ShakeScreenY_Small
CONTRACT["ShakeScreenY_Small"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenY_Small"] = [
    {"read": {0xD4B9: 2, 0xD4BC: 2}},
    dict(POISON, read={0xD4B9: 2, 0xD4BC: 2}),
]
# <<< factory ShakeScreenY_Small

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DecrementScreenAnimDuration
MUTATIONS["DecrementScreenAnimDuration"] = {
	"source_symbol": "DecrementScreenAnimDuration",
	"before": "(v == 0u ? 0x80u : 0u)",
	"after": "(v == 0u ? 0x00u : 0x80u)",
	"case_ids": ["DecrementScreenAnimDuration-0", "DecrementScreenAnimDuration-1", "DecrementScreenAnimDuration-2", "DecrementScreenAnimDuration-3", "DecrementScreenAnimDuration-4", "DecrementScreenAnimDuration-5"],
}
# <<< factory-mutation DecrementScreenAnimDuration
# >>> factory-mutation UpdateShakeOffset
MUTATIONS["UpdateShakeOffset"] = {"source_symbol": "UpdateShakeOffset", "before": "\tif (duration >= timer)", "after": "\tif (duration > timer)", "case_ids": ["UpdateShakeOffset-2", "UpdateShakeOffset-4"]}
# <<< factory-mutation UpdateShakeOffset
# >>> factory-mutation DefaultScreenAnimationUpdate
MUTATIONS["DefaultScreenAnimationUpdate"] = {
    "source_symbol": "DefaultScreenAnimationUpdate",
    "before": "gb_write8(wActiveScreenAnim_ADDR, 0xffu);",
    "after": "gb_write8(wActiveScreenAnim_ADDR, 0xfeu);",
    "case_ids": ["DefaultScreenAnimationUpdate-0", "DefaultScreenAnimationUpdate-1"],
}
# <<< factory-mutation DefaultScreenAnimationUpdate
# >>> factory-mutation DoScreenAnimationUpdate
MUTATIONS["DoScreenAnimationUpdate"] = {"source_symbol": "DoScreenAnimationUpdate", "before": "	wScreenAnimDuration = 1u;", "after": "	wScreenAnimDuration = 2u;", "case_ids": ["DoScreenAnimationUpdate-0", "DoScreenAnimationUpdate-1"]}
# <<< factory-mutation DoScreenAnimationUpdate
# >>> factory-mutation LoadDefaultScreenAnimationUpdateWhenFinished
MUTATIONS["LoadDefaultScreenAnimationUpdateWhenFinished"] = {"source_symbol": "LoadDefaultScreenAnimationUpdateWhenFinished", "before": "\tif (wScreenAnimDuration != 0u)\n\t\treturn;", "after": "\tif (wScreenAnimDuration == 0u)\n\t\treturn;", "case_ids": ["LoadDefaultScreenAnimationUpdateWhenFinished-0", "LoadDefaultScreenAnimationUpdateWhenFinished-1"]}
# <<< factory-mutation LoadDefaultScreenAnimationUpdateWhenFinished
# >>> factory-mutation ShakeScreenX
MUTATIONS["ShakeScreenX"] = {"source_symbol": "ShakeScreenX", "before": "\tgb_write8(wScreenAnimUpdatePtr_ADDR, (uint8_t)SHAKE_SCREEN_X_UPDATE_FUNC_ADDR);", "after": "\tgb_write8(wScreenAnimUpdatePtr_ADDR, (uint8_t)(SHAKE_SCREEN_X_UPDATE_FUNC_ADDR + 1u));", "case_ids": ["ShakeScreenX-0", "ShakeScreenX-1"]}
# <<< factory-mutation ShakeScreenX
# >>> factory-mutation Func_1ce03
MUTATIONS["Func_1ce03"] = {"source_symbol": "Func_1ce03", "before": "\tFunc_3bb5();", "after": "\treturn;", "case_ids": ["Func_1ce03-0", "Func_1ce03-1"]}
# <<< factory-mutation Func_1ce03
# >>> factory-mutation ShakeScreenX_Big
MUTATIONS["ShakeScreenX_Big"] = {"source_symbol": "ShakeScreenX_Big", "before": "\tShakeScreenX(0x4d61u);", "after": "\tShakeScreenX(0x4d62u);", "case_ids": ["ShakeScreenX_Big-0", "ShakeScreenX_Big-1"]}
# <<< factory-mutation ShakeScreenX_Big
# >>> factory-mutation ShakeScreenX_Small
MUTATIONS["ShakeScreenX_Small"] = {"source_symbol": "ShakeScreenX_Small", "before": "void ShakeScreenX_Small(void)\n{\n\tShakeScreenX(0x4d55u);\n}", "after": "void ShakeScreenX_Small(void)\n{\n\tShakeScreenX(0x4d56u);\n}", "case_ids": ["ShakeScreenX_Small-0", "ShakeScreenX_Small-1"]}
# <<< factory-mutation ShakeScreenX_Small
# >>> factory-mutation DistortScreen
MUTATIONS["DistortScreen"] = {"source_symbol": "DistortScreen", "before": "static const uint8_t BGScrollModData[8] = {4u, 3u, 2u, 1u, 1u, 1u, 1u, 2u};", "after": "static const uint8_t BGScrollModData[8] = {5u, 3u, 2u, 1u, 1u, 1u, 1u, 2u};", "case_ids": ["DistortScreen-0", "DistortScreen-1"]}
# <<< factory-mutation DistortScreen
# >>> factory-mutation WhiteFlashScreen
MUTATIONS["WhiteFlashScreen"] = {"source_symbol": "WhiteFlashScreen", "before": "wTempWhiteFlashBGP = wBGP;", "after": "wTempWhiteFlashBGP = (uint8_t)(wBGP + 1u);", "case_ids": ["WhiteFlashScreen-0", "WhiteFlashScreen-1"]}
# <<< factory-mutation WhiteFlashScreen
# >>> factory-mutation ShakeScreenY
MUTATIONS["ShakeScreenY"] = {"source_symbol": "ShakeScreenY", "before": "gb_write8(wScreenAnimUpdatePtr_ADDR, (uint8_t)SHAKE_SCREEN_Y_UPDATE_FUNC_ADDR);", "after": "gb_write8(wScreenAnimUpdatePtr_ADDR, (uint8_t)(SHAKE_SCREEN_Y_UPDATE_FUNC_ADDR + 1u));", "case_ids": ["ShakeScreenY-0"]}
# <<< factory-mutation ShakeScreenY
# >>> factory-mutation ShakeScreenY_Big
MUTATIONS["ShakeScreenY_Big"] = {"source_symbol": "ShakeScreenY_Big", "before": "ShakeScreenY(0x4D61u);", "after": "ShakeScreenY(0x4D10u);", "case_ids": ["ShakeScreenY_Big-0"]}
# <<< factory-mutation ShakeScreenY_Big
# >>> factory-mutation ShakeScreenY_Small
MUTATIONS["ShakeScreenY_Small"] = {"source_symbol": "ShakeScreenY_Small", "before": "ShakeScreenY(0x4D55u);", "after": "ShakeScreenY(0x4D61u);", "case_ids": ["ShakeScreenY_Small-0"]}
# <<< factory-mutation ShakeScreenY_Small
