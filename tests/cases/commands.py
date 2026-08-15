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

# >>> factory AnimationCommand_AnimEnd2
CONTRACT["AnimationCommand_AnimEnd2"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("a", "f", "b", "c", "d", "e", "hl"),
}
CASES["AnimationCommand_AnimEnd2"] = [
    {"read": {wDuelAnimationScreen: 1}},
    dict(POISON, read={wDuelAnimationScreen: 1}),
]
# <<< factory AnimationCommand_AnimEnd2


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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}

# >>> factory-mutation AnimationCommand_AnimEnd2
MUTATIONS["AnimationCommand_AnimEnd2"] = {
    "source_symbol": "AnimationCommand_AnimEnd2",
    "before": "void AnimationCommand_AnimEnd2(void)\n{\n\treturn;",
    "after": "void AnimationCommand_AnimEnd2(void)\n{\n\tgb_write8(wDuelAnimationScreen_ADDR, 0xFFu);\n\treturn;",
    "case_ids": ["AnimationCommand_AnimEnd2-1"],
}
# <<< factory-mutation AnimationCommand_AnimEnd2

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
