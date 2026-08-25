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
MUTATIONS["PlayAttackAnimationCommands_NextCommand"] = {"source_symbol": "PlayAttackAnimationCommands_NextCommand", "before": "return (PlayAttackAnimationCommands_NextCommandResult){(uint8_t)(de >> 8), (uint8_t)de};", "after": "return (PlayAttackAnimationCommands_NextCommandResult){(uint8_t)(de >> 8), (uint8_t)(de + 1u)};", "case_ids": ["PlayAttackAnimationCommands_NextCommand-0", "PlayAttackAnimationCommands_NextCommand-1", "PlayAttackAnimationCommands_NextCommand-2", "PlayAttackAnimationCommands_NextCommand-3", "PlayAttackAnimationCommands_NextCommand-4"]}
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
