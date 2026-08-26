"""Oracle-diff cases for duel animation command routines."""

wDuelAnimLocationParam = 0xD4B0
wDuelAnimationScreen = 0xD4AE
wDuelAnimSetScreen = 0xD4B3
wDuelType = 0xCC09
wWhoseTurn = 0xCC05

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory AnimationCommand_AnimEnd
CONTRACT["AnimationCommand_AnimEnd"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["AnimationCommand_AnimEnd"] = [{"wram": {0xC100: b"\x00"}}, dict(POISON, wram={0xC100: b"\xAA"})]
# <<< factory AnimationCommand_AnimEnd




# >>> factory UpdateDuelAnimationScreen
CONTRACT["UpdateDuelAnimationScreen"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e"),
}
CASES["UpdateDuelAnimationScreen"] = [
    {"wram": {wDuelAnimSetScreen: b"\x00"},
     "read": {wDuelAnimationScreen: 1}},
    {"hl": 0xC100, "wram": {wDuelAnimSetScreen: b"\x01"},
     "read": {wDuelAnimationScreen: 1}},
    {"hl": 0xC101, "wram": {wDuelAnimSetScreen: b"\x02"},
     "read": {wDuelAnimationScreen: 0}},
    dict(POISON, hl=0xC102, wram={wDuelAnimSetScreen: b"\xFF"},
         read={wDuelAnimationScreen: 0}),
    {"hl": 0xC200,
     "wram": {wDuelAnimSetScreen: b"\x04", wDuelAnimLocationParam: b"\x00",
              wWhoseTurn: b"\xC2", wDuelType: b"\x00"},
     "read": {wDuelAnimationScreen: 1}},
    {"hl": 0xC201,
     "wram": {wDuelAnimSetScreen: b"\x04", wDuelAnimLocationParam: b"\x80",
              wWhoseTurn: b"\xC2", wDuelType: b"\x00"},
     "read": {wDuelAnimationScreen: 1}},
    {"hl": 0xC202,
     "wram": {wDuelAnimSetScreen: b"\x04", wDuelAnimLocationParam: b"\x00",
              wWhoseTurn: b"\xC3", wDuelType: b"\x00"},
     "read": {wDuelAnimationScreen: 1}},
    dict(POISON, hl=0xC203,
         wram={wDuelAnimSetScreen: b"\x04", wDuelAnimLocationParam: b"\x80",
               wWhoseTurn: b"\xC3", wDuelType: b"\x01"},
         read={wDuelAnimationScreen: 1}),
]
# <<< factory UpdateDuelAnimationScreen


# >>> factory DuelAnim153
CONTRACT["DuelAnim153"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["DuelAnim153"] = [
    {"wram": {0xC100: b"\x00\x00"}},
    dict(POISON, wram={0xC100: b"\x5A\xA5"}),
    {"a": 1, "hl": 0xC100, "wram": {0xC100: b"\xFF\xFF"}},
]
# <<< factory DuelAnim153

# >>> factory AnimationCommand_AnimEnd2
CONTRACT["AnimationCommand_AnimEnd2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")}
CASES["AnimationCommand_AnimEnd2"] = [
    {},
    dict(POISON),
]
# <<< factory AnimationCommand_AnimEnd2

# >>> factory DuelAnim154
CONTRACT["DuelAnim154"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["DuelAnim154"] = [{}, dict(POISON), {"wram": {0xC100: b"\x00"}}]
# <<< factory DuelAnim154

# >>> factory DuelAnim155
CONTRACT["DuelAnim155"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["DuelAnim155"] = [{}, dict(POISON), {"wram": {0xC100: b"\x00"}}]
# <<< factory DuelAnim155

# >>> factory DuelAnim156
CONTRACT["DuelAnim156"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["DuelAnim156"] = [{}, dict(POISON), {"wram": {0xC100: b"\x00"}}]
# <<< factory DuelAnim156

# >>> factory-cases-statics
wDamageAnimEffectiveness = 0xCE81
wNoDamageOrEffect = 0xCCC7
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDamageAnimAmount = 0xCE7F
wLoadedAttackAnimation = 0xCCB8
wTempNonTurnDuelistCardID = 0xCCC4
wTxRam2 = 0xCE3F
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDuelDisplayedScreen = 0xCAC2
hWhoseTurn = 0xFF97
HUD_TILE = 0x996F
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory GetDamageText
CONTRACT["GetDamageText"] = {"compare": ("hl",), "preserve": ()}
CASES["GetDamageText"] = [
    {"hl": 0x2345, "wram": {wDamageAnimEffectiveness: b"\x00"}, "expect_regs": {"hl": 0x003A}},
    {"hl": 0x2345, "wram": {wDamageAnimEffectiveness: b"\x02"}, "expect_regs": {"hl": 0x0037}},
    {"hl": 0x2345, "wram": {wDamageAnimEffectiveness: b"\x04"}, "expect_regs": {"hl": 0x0036}},
    {"hl": 0x2345, "wram": {wDamageAnimEffectiveness: b"\x06"}, "expect_regs": {"hl": 0x0038}},
    {"hl": 0x0000, "wram": {wNoDamageOrEffect: b"\x00", wDamageAnimEffectiveness: b"\x00"}, "expect_regs": {"hl": 0x003B}},
    {"hl": 0x0000, "wram": {wNoDamageOrEffect: b"\x00", wDamageAnimEffectiveness: b"\x04"}, "expect_regs": {"hl": 0x0039}},
    {"hl": 0x0000, "wram": {wNoDamageOrEffect: b"\x80", wDamageAnimEffectiveness: b"\x04"}, "expect_regs": {"hl": 0x0000}},
    dict(POISON, wram={wDamageAnimEffectiveness: b"\x06"}, expect_regs={"hl": 0x0038}),
]
# <<< factory GetDamageText

# >>> factory PlayAttackAnimationCommands_NextCommand
CONTRACT["PlayAttackAnimationCommands_NextCommand"] = {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c")}
CASES["PlayAttackAnimationCommands_NextCommand"] = [
    dict(POISON, a=8),
    dict(POISON, a=9),
    dict(POISON, a=10),
    dict(POISON, a=11),
    dict(POISON, a=12),
]
# <<< factory PlayAttackAnimationCommands_NextCommand

# >>> factory DuelAnim157
CONTRACT["DuelAnim157"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["DuelAnim157"] = [{}, dict(POISON), {"wram": {0xC100: b"\x00"}}]
# <<< factory DuelAnim157

# >>> factory PrintDamageText
CONTRACT["PrintDamageText"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["PrintDamageText"] = [
    {"hl": 0xC100, "wram": {wLoadedAttackAnimation: b"\x00", wTempNonTurnDuelistCardID: b"\x08", wDamageAnimAmount: b"\x01\x00", 0xCAD3: b"\x48\x03", wTxRam2: b"\xAA\x55"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wTxRam2: 2}, "instruction_budget": 1000000, "cycle_budget": 4000000},
    dict(POISON, wram={wLoadedAttackAnimation: b"\x00", wTempNonTurnDuelistCardID: b"\x08", wDamageAnimAmount: b"\x01\x00", 0xCAD3: b"\x48\x03", wTxRam2: b"\x12\x34"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wTxRam2: 2}, instruction_budget=1000000, cycle_budget=4000000),
    {"b": 1, "c": 2, "d": 3, "e": 4, "hl": 0xC101, "wram": {wLoadedAttackAnimation: b"\x79", wTxRam2: b"\xAA\x55"}, "read": {wTxRam2: 2}},
    dict(POISON, wram={wLoadedAttackAnimation: b"\x86", wTxRam2: b"\x12\x34"}, read={wTxRam2: 2}),
]
# <<< factory PrintDamageText

# >>> factory UpdateMainSceneHUD
CONTRACT["UpdateMainSceneHUD"] = {"compare": (), "preserve": ()}
CASES["UpdateMainSceneHUD"] = [
    {"wram": {wDuelDisplayedScreen: b"\x00"}},
    {"wram": {wDuelDisplayedScreen: b"\x01", hWhoseTurn: b"\xC2", 0xC2BB: b"\xFF", 0xC3BB: b"\xFF", 0xC2F1: b"\x00", 0xC2F0: b"\x00", 0xC3F1: b"\x00", 0xC3F0: b"\x00", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC3EC: b"\x00", 0xC3EF: b"\x00"}, "vread": {0: {HUD_TILE: 1}}},
    dict(POISON, wram={wDuelDisplayedScreen: b"\x01", hWhoseTurn: b"\xC2", 0xC2BB: b"\xFF", 0xC3BB: b"\xFF", 0xC2F1: b"\x00", 0xC2F0: b"\x00", 0xC3F1: b"\x00", 0xC3F0: b"\x00", 0xC2EC: b"\x00", 0xC2EF: b"\x00", 0xC3EC: b"\x00", 0xC3EF: b"\x00"}, vread={0: {HUD_TILE: 1}}),
]
# <<< factory UpdateMainSceneHUD

# >>> factory SetScreenForDuelAnimation
CONTRACT["SetScreenForDuelAnimation"] = {"compare": (), "preserve": ()}
CASES["SetScreenForDuelAnimation"] = [
    {"hl": 0xC100, "wram": {wDuelAnimSetScreen: b"\x00", wDuelDisplayedScreen: b"\x00"}, "read": {wDuelDisplayedScreen: 0}},
    {"hl": 0xC101, "wram": {wDuelAnimSetScreen: b"\x01", wDuelDisplayedScreen: b"\x01"}, "read": {wDuelAnimationScreen: 0}},
    {"hl": 0xC102, "wram": {wDuelAnimSetScreen: b"\x04", wDuelAnimLocationParam: b"\x00", wWhoseTurn: b"\xC2", wDuelType: b"\x00", wDuelDisplayedScreen: b"\x00", 0xCABB: b"\x00"}, "setup": [{"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wDuelDisplayedScreen: 4}, "instruction_budget": 60000000, "cycle_budget": 240000000},
    dict(POISON, hl=0xC103, wram={wDuelAnimSetScreen: b"\x04", wDuelAnimLocationParam: b"\x00", wWhoseTurn: b"\xC2", wDuelType: b"\x00", wDuelDisplayedScreen: b"\x00", 0xCABB: b"\x00"}, setup=[{"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wDuelDisplayedScreen: 4}, instruction_budget=60000000, cycle_budget=240000000),
]
# <<< factory SetScreenForDuelAnimation


# >>> factory AnimationCommand_AnimNormal
wDamageAnimPlayAreaLocation = 0xCE82
# de points at the animation id; the chain then reads a terminating END (0).
_hWhoseTurn = 0xFF97
_wDuelAnimDuelistSide = 0xD4AF
_wDuelAnimDamage = 0xD4B1
_wDuelAnimEffectiveness = 0xD4B3
_wDuelDisplayedScreen = 0xCAC2
_STREAM = 0xC100
CONTRACT["AnimationCommand_AnimNormal"] = {"compare": ("d", "e"), "preserve": ()}
CASES["AnimationCommand_AnimNormal"] = [
    # plain id -> played as-is
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, "read": {_STREAM: 2}},
    # SHAKE1 on the player's turn -> small shake X
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\xFA\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, "read": {_STREAM: 2}},
    # SHAKE1 on the opponent's turn with a link duel -> small shake Y
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\xFA\x00", _hWhoseTurn: b"\xC3",
        wDuelType: b"\x01"}, "read": {_STREAM: 2}},
    # SHAKE3 swaps the pair
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\xFC\x00", _hWhoseTurn: b"\xC3",
        wDuelType: b"\x01"}, "read": {_STREAM: 2}},
    dict(POISON, d=0xC1, e=0x00, wram={_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, read={_STREAM: 2}),
    # SHOW_DAMAGE: copies the damage pair and effectiveness into the anim state
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x09\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimAmount: b"\x2A\x01",
        wDamageAnimEffectiveness: b"\x03", _wDuelDisplayedScreen: b"\x01"},
     "read": {_STREAM: 2, _wDuelAnimDamage: 2}},
]
# <<< factory AnimationCommand_AnimNormal

# >>> factory AnimationCommand_AnimPlayer
CONTRACT["AnimationCommand_AnimPlayer"] = {"compare": ("d", "e"), "preserve": ()}
CASES["AnimationCommand_AnimPlayer"] = [
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, "read": {_STREAM: 2, _wDuelAnimDuelistSide: 1}},
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC3",
        wDuelType: b"\x01"}, "read": {_STREAM: 2, _wDuelAnimDuelistSide: 1}},
    dict(POISON, d=0xC1, e=0x00, wram={_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, read={_STREAM: 2, _wDuelAnimDuelistSide: 1}),
]
# <<< factory AnimationCommand_AnimPlayer

# >>> factory AnimationCommand_AnimOpponent
CONTRACT["AnimationCommand_AnimOpponent"] = {"compare": ("d", "e"), "preserve": ()}
CASES["AnimationCommand_AnimOpponent"] = [
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, "read": {_STREAM: 2, _wDuelAnimDuelistSide: 1}},
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC3",
        wDuelType: b"\x01"}, "read": {_STREAM: 2, _wDuelAnimDuelistSide: 1}},
    dict(POISON, d=0xC1, e=0x00, wram={_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00"}, read={_STREAM: 2, _wDuelAnimDuelistSide: 1}),
]
# <<< factory AnimationCommand_AnimOpponent

# >>> factory AnimationCommand_AnimPlayArea
CONTRACT["AnimationCommand_AnimPlayArea"] = {"compare": ("d", "e"), "preserve": ()}
CASES["AnimationCommand_AnimPlayArea"] = [
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimPlayAreaLocation: b"\x83"},
     "read": {_STREAM: 2, wDuelAnimLocationParam: 1}},
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimPlayAreaLocation: b"\x05"},
     "read": {_STREAM: 2, wDuelAnimLocationParam: 1}},
    dict(POISON, d=0xC1, e=0x00, wram={_STREAM: b"\x20\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimPlayAreaLocation: b"\xFF"},
        read={_STREAM: 2, wDuelAnimLocationParam: 1}),
]
# <<< factory AnimationCommand_AnimPlayArea

# >>> factory AnimationCommand_AnimScreen
CONTRACT["AnimationCommand_AnimScreen"] = {"compare": ("d", "e"), "preserve": ()}
CASES["AnimationCommand_AnimScreen"] = [
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x01\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimPlayAreaLocation: b"\x00"},
     "read": {_STREAM: 2, wDuelAnimSetScreen: 1, wDuelAnimLocationParam: 1}},
    {"d": 0xC1, "e": 0x00, "wram": {_STREAM: b"\x04\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimPlayAreaLocation: b"\x00"},
     "read": {_STREAM: 2, wDuelAnimSetScreen: 1, wDuelAnimLocationParam: 1}},
    dict(POISON, d=0xC1, e=0x00, wram={_STREAM: b"\x00\x00", _hWhoseTurn: b"\xC2",
        wDuelType: b"\x00", wDamageAnimPlayAreaLocation: b"\x00"},
        read={_STREAM: 2, wDuelAnimSetScreen: 1, wDuelAnimLocationParam: 1}),
]
# <<< factory AnimationCommand_AnimScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}

# >>> factory-mutation AnimationCommand_AnimEnd
MUTATIONS["AnimationCommand_AnimEnd"] = {"source_symbol": "AnimationCommand_AnimEnd", "before": "\treturn;", "after": "\tgb_write8(0xC100u, 0x01u);", "case_ids": ["AnimationCommand_AnimEnd-0", "AnimationCommand_AnimEnd-1"]}
# <<< factory-mutation AnimationCommand_AnimEnd

# >>> factory-mutation UpdateDuelAnimationScreen
MUTATIONS["UpdateDuelAnimationScreen"] = {
    "source_symbol": "UpdateDuelAnimationScreen",
    "before": "uint8_t set_screen = gb_read8(wDuelAnimSetScreen_ADDR);",
    "after": "uint8_t set_screen = (uint8_t)(gb_read8(wDuelAnimSetScreen_ADDR) ^ 1u);",
    "case_ids": ["UpdateDuelAnimationScreen-1", "UpdateDuelAnimationScreen-4"],
}
# <<< factory-mutation UpdateDuelAnimationScreen
# >>> factory-mutation DuelAnim153
MUTATIONS["DuelAnim153"] = {
    "source_symbol": "DuelAnim153",
    "before": "void DuelAnim153(void)\n{\n}",
    "after": "void DuelAnim153(void)\n{\n\tgb_write8(0xC100u, 0xFFu);\n}",
    "case_ids": ["DuelAnim153-0", "DuelAnim153-1"],
}
# <<< factory-mutation DuelAnim153
# >>> factory-mutation AnimationCommand_AnimEnd2
MUTATIONS["AnimationCommand_AnimEnd2"] = {
    "source_symbol": "AnimationCommand_AnimEnd2",
    "before": "uint8_t AnimationCommand_AnimEnd2(uint8_t a)\n{\n\treturn a;\n}",
    "after": "uint8_t AnimationCommand_AnimEnd2(uint8_t a)\n{\n\treturn (uint8_t)(a + 1u);\n}",
    "case_ids": ["AnimationCommand_AnimEnd2-0", "AnimationCommand_AnimEnd2-1"],
}
# <<< factory-mutation AnimationCommand_AnimEnd2
# >>> factory-mutation DuelAnim154
MUTATIONS["DuelAnim154"] = {"source_symbol": "DuelAnim154", "before": "\treturn; /* DuelAnim154 */", "after": "\tgb_write8(0xC100u, 1u); /* DuelAnim154 */", "case_ids": ["DuelAnim154-2"]}
# <<< factory-mutation DuelAnim154
# >>> factory-mutation DuelAnim155
MUTATIONS["DuelAnim155"] = {"source_symbol": "DuelAnim155", "before": "\treturn; /* DuelAnim155 */", "after": "\tgb_write8(0xC100u, 1u); /* DuelAnim155 */", "case_ids": ["DuelAnim155-2"]}
# <<< factory-mutation DuelAnim155
# >>> factory-mutation DuelAnim156
MUTATIONS["DuelAnim156"] = {"source_symbol": "DuelAnim156", "before": "\treturn; /* DuelAnim156 */", "after": "\tgb_write8(0xC100u, 1u); /* DuelAnim156 */", "case_ids": ["DuelAnim156-2"]}
# <<< factory-mutation DuelAnim156
# >>> factory-mutation GetDamageText
MUTATIONS["GetDamageText"] = {
    "source_symbol": "GetDamageText",
    "before": "\tif (hl == 0u) {",
    "after": "\tif (hl != 0u) {",
    "case_ids": ["GetDamageText-0", "GetDamageText-4", "GetDamageText-5", "GetDamageText-6"],
}
# <<< factory-mutation GetDamageText
# >>> factory-mutation PlayAttackAnimationCommands_NextCommand
MUTATIONS["PlayAttackAnimationCommands_NextCommand"] = {"source_symbol": "PlayAttackAnimationCommands_NextCommand", "before": "\tuint8_t opcode = gb_read8(de);\n\tde++;", "after": "\tuint8_t opcode = gb_read8(de);\n\tde += 2u;", "case_ids": ["PlayAttackAnimationCommands_NextCommand-0", "PlayAttackAnimationCommands_NextCommand-1", "PlayAttackAnimationCommands_NextCommand-2", "PlayAttackAnimationCommands_NextCommand-3", "PlayAttackAnimationCommands_NextCommand-4"]}
# <<< factory-mutation PlayAttackAnimationCommands_NextCommand
# >>> factory-mutation DuelAnim157
MUTATIONS["DuelAnim157"] = {"source_symbol": "DuelAnim157", "before": "\treturn; /* DuelAnim157 */", "after": "\tgb_write8(0xC100u, 1u); /* DuelAnim157 */", "case_ids": ["DuelAnim157-2"]}
# <<< factory-mutation DuelAnim157
# >>> factory-mutation PrintDamageText
MUTATIONS["PrintDamageText"] = {
    "source_symbol": "PrintDamageText",
    "before": "\tgb_write8(wTxRam2_ADDR, 0u);",
    "after": "\tgb_write8(wTxRam2_ADDR, 1u);",
    "case_ids": ["PrintDamageText-0", "PrintDamageText-1"],
}
# <<< factory-mutation PrintDamageText
# >>> factory-mutation UpdateMainSceneHUD
MUTATIONS["UpdateMainSceneHUD"] = {"source_symbol": "UpdateMainSceneHUD", "before": "if (displayed_screen == DUEL_MAIN_SCENE) {", "after": "if (displayed_screen != DUEL_MAIN_SCENE) {", "case_ids": ["UpdateMainSceneHUD-1", "UpdateMainSceneHUD-2"]}
# <<< factory-mutation UpdateMainSceneHUD
# >>> factory-mutation SetScreenForDuelAnimation
MUTATIONS["SetScreenForDuelAnimation"] = {"source_symbol": "SetScreenForDuelAnimation", "before": "\t\tgb_write8(wDuelDisplayedScreen_ADDR, saved_screen);", "after": "\t\tgb_write8(wDuelDisplayedScreen_ADDR, (uint8_t)(saved_screen ^ 1u));", "case_ids": ["SetScreenForDuelAnimation-2", "SetScreenForDuelAnimation-3"]}
# <<< factory-mutation SetScreenForDuelAnimation
# >>> factory-mutation AnimationCommand_AnimNormal
MUTATIONS["AnimationCommand_AnimNormal"] = {"source_symbol": "AnimationCommand_AnimNormal", "before": "\t\tgb_write8(wDuelAnimDamage_ADDR, gb_read8(wDamageAnimAmount_ADDR));", "after": "\t\tgb_write8(wDuelAnimDamage_ADDR, (uint8_t)(gb_read8(wDamageAnimAmount_ADDR) + 1u));", "case_ids": ["AnimationCommand_AnimNormal-5"]}
# <<< factory-mutation AnimationCommand_AnimNormal
# >>> factory-mutation AnimationCommand_AnimPlayer
MUTATIONS["AnimationCommand_AnimPlayer"] = {"source_symbol": "AnimationCommand_AnimPlayer", "before": "\t\tgb_write8(wDuelAnimDuelistSide_ADDR, PLAYER_TURN);", "after": "\t\tgb_write8(wDuelAnimDuelistSide_ADDR, OPPONENT_TURN);", "case_ids": ["AnimationCommand_AnimPlayer-0", "AnimationCommand_AnimPlayer-1", "AnimationCommand_AnimPlayer-2"]}
# <<< factory-mutation AnimationCommand_AnimPlayer
# >>> factory-mutation AnimationCommand_AnimOpponent
MUTATIONS["AnimationCommand_AnimOpponent"] = {"source_symbol": "AnimationCommand_AnimOpponent", "before": "\t\tgb_write8(wDuelAnimDuelistSide_ADDR, OPPONENT_TURN);", "after": "\t\tgb_write8(wDuelAnimDuelistSide_ADDR, PLAYER_TURN);", "case_ids": ["AnimationCommand_AnimOpponent-0", "AnimationCommand_AnimOpponent-1", "AnimationCommand_AnimOpponent-2"]}
# <<< factory-mutation AnimationCommand_AnimOpponent
# >>> factory-mutation AnimationCommand_AnimPlayArea
MUTATIONS["AnimationCommand_AnimPlayArea"] = {"source_symbol": "AnimationCommand_AnimPlayArea", "before": "& 0x7Fu);", "after": "& 0xFFu);", "case_ids": ["AnimationCommand_AnimPlayArea-0", "AnimationCommand_AnimPlayArea-1", "AnimationCommand_AnimPlayArea-2"]}
# <<< factory-mutation AnimationCommand_AnimPlayArea
# >>> factory-mutation AnimationCommand_AnimScreen
MUTATIONS["AnimationCommand_AnimScreen"] = {"source_symbol": "AnimationCommand_AnimScreen", "before": "\tgb_write8(wDuelAnimSetScreen_ADDR, screen);", "after": "\tgb_write8(wDuelAnimSetScreen_ADDR, (uint8_t)(screen + 1u));", "case_ids": ["AnimationCommand_AnimScreen-0", "AnimationCommand_AnimScreen-1", "AnimationCommand_AnimScreen-2"]}
# <<< factory-mutation AnimationCommand_AnimScreen
