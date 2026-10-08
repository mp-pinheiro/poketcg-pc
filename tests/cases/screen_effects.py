"""Oracle-diff cases for poketcg/src/engine/duel/animations/screen_effects.asm."""
from tests.cases._symbols import const, sym, sym_pointer

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
	dict(POISON, wram={sym("wScreenAnimDuration"): b"\x01"}),
	# half-borrow boundary 0x10 -> 0x0f; entry Z/N/H bits must not leak into f -> f=0x60
	{"f": 0xE0, "wram": {sym("wScreenAnimDuration"): b"\x10"}},
	# plain decrement, no flags produced by dec -> f=0x40
	{"wram": {sym("wScreenAnimDuration"): b"\xff"}},
	# 2 -> 1: result nonzero, no half-borrow -> f=0x40
	{"wram": {sym("wScreenAnimDuration"): b"\x02"}},
]
# <<< factory DecrementScreenAnimDuration

# >>> factory UpdateShakeOffset
CONTRACT["UpdateShakeOffset"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["UpdateShakeOffset"] = [
	{},
	{"wram": {sym("wScreenAnimDuration"): b"\x00", sym("wScreenShakeOffsetsPtr"): b"\x00\xC1", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x15\x02"}, "read": {sym("wScreenShakeOffsetsPtr"): 2, sym("wDecompressionSecondaryBufferStart") + 0x11: 1}},
	{"wram": {sym("wScreenAnimDuration"): b"\x15", sym("wScreenShakeOffsetsPtr"): b"\x00\xC1", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x15\x02"}, "read": {sym("wScreenShakeOffsetsPtr"): 2, sym("wDecompressionSecondaryBufferStart") + 0x11: 1}},
	{"wram": {sym("wScreenAnimDuration"): b"\x20", sym("wScreenShakeOffsetsPtr"): b"\x00\xC1", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x15\x02"}, "read": {sym("wScreenShakeOffsetsPtr"): 2, sym("wDecompressionSecondaryBufferStart") + 0x11: 1}},
	dict(POISON, wram={sym("wScreenAnimDuration"): b"\x01", sym("wScreenShakeOffsetsPtr"): b"\x00\xC1", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x01\xFF"}, read={sym("wScreenShakeOffsetsPtr"): 2, sym("wDecompressionSecondaryBufferStart") + 0x11: 1}),
]
# <<< factory UpdateShakeOffset

# >>> factory-cases-statics
wActiveScreenAnim = sym("wActiveScreenAnim")
wScreenAnimUpdatePtr = sym("wScreenAnimUpdatePtr")
hSCX = sym("hSCX")
rSCX = 0xFF43
hSCY = sym("hSCY")
rSTAT = 0xFF41
rIE = 0xFFFF

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wScreenAnimDuration = sym("wScreenAnimDuration")
wScreenAnimUpdatePtr = sym("wScreenAnimUpdatePtr")

wDuelAnimDamage = sym("wDuelAnimDamage")
WD4C0 = sym("wd4c0")
WDUEL_ANIM_RETURN_BANK = sym("wDuelAnimReturnBank")

wAnimationsDisabled = sym("wAnimationsDisabled")
wTempAnimation = sym("wTempAnimation")
wScreenShakeOffsetsPtr = sym("wScreenShakeOffsetsPtr")
wTempWhiteFlashBGP = sym("wTempWhiteFlashBGP")
wBGP = sym("wBGP")
wLCDCFunctionTrampoline = sym("wLCDCFunctionTrampoline")
wBackgroundPalettesCGB = sym("wBackgroundPalettesCGB")
wTempBackgroundPalettesCGB = sym("wTempBackgroundPalettesCGB")
wBGScrollMod = sym("wBGScrollMod")
wApplyBGScroll = sym("wApplyBGScroll")
# <<< factory-cases-statics

# >>> factory DefaultScreenAnimationUpdate
CONTRACT["DefaultScreenAnimationUpdate"] = {"compare": (), "preserve": ()}
CASES["DefaultScreenAnimationUpdate"] = [
    {"wram": {sym("wActiveScreenAnim"): b"\x00", sym("wScreenAnimUpdatePtr"): b"\x00\x00"}, "hram": {0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, "expect": {sym("wActiveScreenAnim"): b"\xFF", sym("wScreenAnimUpdatePtr"): b"\xBC\x4C", sym("hSCX"): b"\x00", sym("hSCY"): b"\x00", 0xFF41: b"\xBF", 0xFF43: b"\x00", 0xFFFF: b"\xFD"}},
    dict(POISON, wram={sym("wActiveScreenAnim"): b"\x12", sym("wScreenAnimUpdatePtr"): b"\x34\x56"}, hram={0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, expect={sym("wActiveScreenAnim"): b"\xFF", sym("wScreenAnimUpdatePtr"): b"\xBC\x4C", sym("hSCX"): b"\x00", sym("hSCY"): b"\x00", 0xFF41: b"\xBF", 0xFF43: b"\x00", 0xFFFF: b"\xFD"}),
]
# <<< factory DefaultScreenAnimationUpdate

# >>> factory DoScreenAnimationUpdate
CONTRACT["DoScreenAnimationUpdate"] = {"compare": (), "preserve": ()}
CASES["DoScreenAnimationUpdate"] = [
    {"wram": {wScreenAnimUpdatePtr: sym_pointer("DefaultScreenAnimationUpdate"), wScreenAnimDuration: b"\x00"}, "read": {wScreenAnimDuration: 1, wScreenAnimUpdatePtr: 2}},
    dict(POISON, wram={wScreenAnimUpdatePtr: sym_pointer("DefaultScreenAnimationUpdate"), wScreenAnimDuration: b"\xFF"}, read={wScreenAnimDuration: 1, wScreenAnimUpdatePtr: 2}),
]
# <<< factory DoScreenAnimationUpdate

# >>> factory LoadDefaultScreenAnimationUpdateWhenFinished
CONTRACT["LoadDefaultScreenAnimationUpdateWhenFinished"] = {"compare": (), "preserve": ()}
CASES["LoadDefaultScreenAnimationUpdateWhenFinished"] = [
    {"wram": {sym("wScreenAnimDuration"): b"\x00", sym("wActiveScreenAnim"): b"\x00", sym("wScreenAnimUpdatePtr"): b"\x00\x00"}, "hram": {0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, "read": {sym("wActiveScreenAnim"): 1, sym("wScreenAnimUpdatePtr"): 2, sym("hSCX"): 1, sym("hSCY"): 1, 0xFF41: 1, 0xFF43: 1, 0xFFFF: 1}},
    dict(POISON, wram={sym("wScreenAnimDuration"): b"\x01", sym("wActiveScreenAnim"): b"\x12", sym("wScreenAnimUpdatePtr"): b"\x34\x56"}, hram={0xFF41: b"\xFF", 0xFFFF: b"\xFF"}, read={sym("wActiveScreenAnim"): 1, sym("wScreenAnimUpdatePtr"): 2, sym("hSCX"): 1, sym("hSCY"): 1, 0xFF41: 1, 0xFF43: 1, 0xFFFF: 1}),
]
# <<< factory LoadDefaultScreenAnimationUpdateWhenFinished

# >>> factory ShakeScreenX
CONTRACT["ShakeScreenX"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenX"] = [
    {"wram": {sym("wScreenAnimUpdatePtr"): b"\x00\x00", sym("wScreenShakeOffsetsPtr"): b"\x00\x00"}, "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {sym("wScreenAnimUpdatePtr"): b"\x56\x34", sym("wScreenShakeOffsetsPtr"): b"\x78\x9A"}, "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
]
# <<< factory ShakeScreenX

# >>> factory Func_1ce03
CONTRACT["Func_1ce03"] = {"compare": ("a", "f"), "preserve": ()}
# screen_effects.asm:258-286: a - $96 indexes .pointer_table. $98 runs
# UpdateMainSceneHUD (the HUD text row is read back), $97 runs PrintDamageText
# (wTxRam2 receives the damage, hl parked as the caller leaves it), $9B is one
# of the empty DuelAnim15x routines. The return bank ($CE21) is the caller's.
CASES["Func_1ce03"] = [
    {"a": 0x98, "wram": {WD4C0: b"\x00", WDUEL_ANIM_RETURN_BANK: b"\x06", sym("hWhoseTurn"): b"\xC2", sym("wPlayerArenaCard"): b"\x00", sym("wPlayerNumberOfPokemonInPlayArea"): b"\x01", sym("wBoosterCardsDrawn"): b"\x08", sym("wPlayerCardLocations"): b"\x10", sym("wLCDC"): b"\x00", sym("wPlayerArenaCardHP"): b"\x28"},
     "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {WD4C0: 1}, "vread": {0: {0x9800: 0x400}},
     "instruction_budget": 4000000, "cycle_budget": 16000000},
    dict(POISON, a=0x97, wram={WD4C0: b"\x00", WDUEL_ANIM_RETURN_BANK: b"\x06", sym("wLoadedAttackAnimation"): b"\x00", sym("wTempNonTurnDuelistCardID"): b"\x08", sym("wDamageAnimAmount"): b"\x14\x00", sym("wDoFrameFunction"): sym_pointer("NoOp"), sym("wTxRam2"): b"\xAA\x55"},
         setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={WD4C0: 1, sym("wTxRam2"): 2}, vread={0: {0x9800: 0x400}},
         instruction_budget=4000000, cycle_budget=16000000),
    dict(POISON, a=0x9B, wram={WD4C0: b"\x00", WDUEL_ANIM_RETURN_BANK: b"\x06"}, read={WD4C0: 1}),
]
# <<< factory Func_1ce03

# >>> factory ShakeScreenX_Big
CONTRACT["ShakeScreenX_Big"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenX_Big"] = [
    {"wram": {sym("wScreenAnimUpdatePtr"): b"\x00\x00", sym("wScreenShakeOffsetsPtr"): b"\x00\x00"}, "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {sym("wScreenAnimUpdatePtr"): b"\x56\x78", sym("wScreenShakeOffsetsPtr"): b"\x9A\xBC"}, "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
]
# <<< factory ShakeScreenX_Big

# >>> factory ShakeScreenX_Small
CONTRACT["ShakeScreenX_Small"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenX_Small"] = [
    {"wram": {sym("wScreenAnimUpdatePtr"): b"\x00\x00", sym("wScreenShakeOffsetsPtr"): b"\x00\x00"}, "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
     "wram": {sym("wScreenAnimUpdatePtr"): b"\x56\x78", sym("wScreenShakeOffsetsPtr"): b"\x9A\xBC"}, "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
]
# <<< factory ShakeScreenX_Small

# >>> factory DistortScreen
CONTRACT["DistortScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["DistortScreen"] = [
    {"wram": {sym("wScreenAnimDuration"): b"\x03"},
     "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wApplyBGScroll"): 1, sym("wLCDCFunctionTrampoline") + 1: 2, sym("wBGScrollMod"): 1, sym("wScreenAnimDuration"): 1}},
    dict(POISON, wram={sym("wScreenAnimDuration"): b"\x10"},
         read={sym("wScreenAnimUpdatePtr"): 2, sym("wApplyBGScroll"): 1, sym("wLCDCFunctionTrampoline") + 1: 2, sym("wBGScrollMod"): 1, sym("wScreenAnimDuration"): 1}),
]
# <<< factory DistortScreen

# >>> factory WhiteFlashScreen
CONTRACT["WhiteFlashScreen"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["WhiteFlashScreen"] = [
    {"wram": {sym("wScreenAnimDuration"): b"\x00", sym("wBGP"): b"\x11"},
     "read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 1, sym("wBackgroundPalettesCGB"): 8, sym("wTempBackgroundPalettesCGB"): 8, sym("wScreenAnimDuration"): 1}},
    dict(POISON, wram={sym("wScreenAnimDuration"): b"\x05", sym("wBGP"): b"\x22"},
         read={sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 1, sym("wBackgroundPalettesCGB"): 8, sym("wTempBackgroundPalettesCGB"): 8, sym("wScreenAnimDuration"): 1}),
]
# <<< factory WhiteFlashScreen

# >>> factory ShakeScreenY
CONTRACT["ShakeScreenY"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["ShakeScreenY"] = [
    {"hl": 0x4D61, "wram": {sym("wScreenShakeOffsetsPtr"): b"\x00\x00", sym("wScreenAnimUpdatePtr"): b"\x00\x00"},
     "expect": {sym("wScreenShakeOffsetsPtr"): b"\x61\x4D", sym("wScreenAnimUpdatePtr"): b"\x2B\x4D"}},
    dict(POISON, wram={sym("wScreenShakeOffsetsPtr"): b"\x00\x00", sym("wScreenAnimUpdatePtr"): b"\x00\x00"}),
]
# <<< factory ShakeScreenY

# >>> factory ShakeScreenY_Big
CONTRACT["ShakeScreenY_Big"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenY_Big"] = [
    {"read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
    dict(POISON, read={sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}),
]
# <<< factory ShakeScreenY_Big

# >>> factory ShakeScreenY_Small
CONTRACT["ShakeScreenY_Small"] = {"compare": (), "preserve": ()}
CASES["ShakeScreenY_Small"] = [
    {"read": {sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}},
    dict(POISON, read={sym("wScreenAnimUpdatePtr"): 2, sym("wScreenShakeOffsetsPtr"): 2}),
]
# <<< factory ShakeScreenY_Small

# >>> factory InitScreenAnimation
CONTRACT["InitScreenAnimation"] = {"compare": (), "preserve": ()}
CASES["InitScreenAnimation"] = [
    dict(POISON, wram={wAnimationsDisabled: b"\x00", wTempAnimation: const("DUEL_ANIM_SMALL_SHAKE_X").to_bytes(1, "little")},
         read={wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wScreenShakeOffsetsPtr: 2}),
    {"wram": {wAnimationsDisabled: b"\x01", wTempAnimation: const("DUEL_ANIM_SMALL_SHAKE_X").to_bytes(1, "little"),
                     wActiveScreenAnim: b"\x55", wScreenAnimUpdatePtr: b"\x34\x12",
                     wScreenAnimDuration: b"\x77", wScreenShakeOffsetsPtr: b"\x88\x99"},
     "read": {wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wScreenShakeOffsetsPtr: 2}},
    {"wram": {wAnimationsDisabled: b"\x00", wTempAnimation: const("DUEL_ANIM_BIG_SHAKE_X").to_bytes(1, "little")},
     "read": {wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wScreenShakeOffsetsPtr: 2}},
    {"wram": {wAnimationsDisabled: b"\x00", wTempAnimation: const("DUEL_ANIM_SMALL_SHAKE_Y").to_bytes(1, "little")},
     "read": {wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wScreenShakeOffsetsPtr: 2}},
    {"wram": {wAnimationsDisabled: b"\x00", wTempAnimation: const("DUEL_ANIM_BIG_SHAKE_Y").to_bytes(1, "little")},
     "read": {wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wScreenShakeOffsetsPtr: 2}},
    {"wram": {wAnimationsDisabled: b"\x00", wTempAnimation: const("DUEL_ANIM_FLASH").to_bytes(1, "little"), wBGP: b"\x11"},
     "read": {wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wTempWhiteFlashBGP: 1, wBackgroundPalettesCGB: 8,
               wTempBackgroundPalettesCGB: 8, wBGP: 1}},
    {"wram": {wAnimationsDisabled: b"\x00", wTempAnimation: const("DUEL_ANIM_DISTORT").to_bytes(1, "little")},
     "read": {wActiveScreenAnim: 1, wScreenAnimUpdatePtr: 2, wScreenAnimDuration: 1,
               wBGScrollMod: 1, wApplyBGScroll: 1, wLCDCFunctionTrampoline: 2}},
]
# <<< factory InitScreenAnimation

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
MUTATIONS["Func_1ce03"] = {"source_symbol": "Func_1ce03", "before": "\tFunc_3bb5(effects[(uint8_t)(a - 0x96u)]);", "after": "\tFunc_3bb5(DuelAnim153);", "case_ids": ["Func_1ce03-1"]}
# <<< factory-mutation Func_1ce03
# >>> factory-mutation ShakeScreenX_Big
MUTATIONS["ShakeScreenX_Big"] = {"source_symbol": "ShakeScreenX_Big", "before": "\tShakeScreenX(BigShakeOffsets_ADDR);", "after": "\tShakeScreenX((uint16_t)(BigShakeOffsets_ADDR + 1u));", "case_ids": ["ShakeScreenX_Big-0", "ShakeScreenX_Big-1"]}
# <<< factory-mutation ShakeScreenX_Big
# >>> factory-mutation ShakeScreenX_Small
MUTATIONS["ShakeScreenX_Small"] = {"source_symbol": "ShakeScreenX_Small", "before": "\tShakeScreenX(SmallShakeOffsets_ADDR);", "after": "\tShakeScreenX((uint16_t)(SmallShakeOffsets_ADDR + 1u));", "case_ids": ["ShakeScreenX_Small-0", "ShakeScreenX_Small-1"]}
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
MUTATIONS["ShakeScreenY_Big"] = {"source_symbol": "ShakeScreenY_Big", "before": "\tShakeScreenY(BigShakeOffsets_ADDR);", "after": "\tShakeScreenY((uint16_t)(BigShakeOffsets_ADDR + 1u));", "case_ids": ["ShakeScreenY_Big-0"]}
# <<< factory-mutation ShakeScreenY_Big
# >>> factory-mutation ShakeScreenY_Small
MUTATIONS["ShakeScreenY_Small"] = {"source_symbol": "ShakeScreenY_Small", "before": "\tShakeScreenY(SmallShakeOffsets_ADDR);", "after": "\tShakeScreenY((uint16_t)(SmallShakeOffsets_ADDR + 1u));", "case_ids": ["ShakeScreenY_Small-0"]}
# <<< factory-mutation ShakeScreenY_Small
# >>> factory-mutation InitScreenAnimation
MUTATIONS["InitScreenAnimation"] = {
    "source_symbol": "InitScreenAnimation",
    "before": "void InitScreenAnimation(void)\n{\n\ttypedef void (*ScreenAnimationHandler)(void);\n\ttypedef struct {\n\t\tScreenAnimationHandler handler;\n\t\tuint8_t duration;\n\t} ScreenAnimationEntry;\n\tstatic const ScreenAnimationEntry screen_animation_functions[6] = {\n\t\t{ShakeScreenX_Small, 24u},",
    "after": "void InitScreenAnimation(void)\n{\n\ttypedef void (*ScreenAnimationHandler)(void);\n\ttypedef struct {\n\t\tScreenAnimationHandler handler;\n\t\tuint8_t duration;\n\t} ScreenAnimationEntry;\n\tstatic const ScreenAnimationEntry screen_animation_functions[6] = {\n\t\t{ShakeScreenX_Big, 24u},",
    "case_ids": ["InitScreenAnimation-0"]
}
# <<< factory-mutation InitScreenAnimation
