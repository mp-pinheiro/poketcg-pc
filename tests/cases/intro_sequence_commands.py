"""Oracle-diff cases for poketcg/src/engine/sequences/intro_sequence_commands.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory AnimateRandomTitleScreenOrb
CONTRACT["AnimateRandomTitleScreenOrb"] = {"compare": ("a", "b"), "preserve": ("b",)}
CASES["AnimateRandomTitleScreenOrb"] = [
    {"wram": {0xD635: b"\x01", 0xCAB4: b"\x00"}, "read": {0xD4CF: 1}},
    {"wram": {0xD635: b"\x3F", 0xCAB4: b"\x00"}, "read": {0xD4CF: 1}},
    {"wram": {0xD635: b"\xFF", 0xCAB4: b"\x00"}, "read": {0xD4CF: 1}},
    {"wram": {0xD635: b"\x01", 0xCAB4: b"\x02", 0xD629: b"\x00\x01\x02\x03\x04\x05\x06"},
     "read": {0xD4CF: 1}},
    dict(POISON, wram={0xD635: b"\x3F", 0xCAB4: b"\x02", 0xD629: b"\x06\x05\x04\x03\x02\x01\x00"},
         read={0xD4CF: 1}),
]
# <<< factory AnimateRandomTitleScreenOrb

# >>> factory-cases-statics
wSequenceCmdPtr = 0xD631

wSequenceCmdPtr = 0xD631
wIntroSequencePalsNeedUpdate = 0xD634

wSequenceDelay = 0xD633
wSequenceCmdPtr = 0xD631

wIntroSequencePalsNeedUpdate = 0xD634
# <<< factory-cases-statics

# >>> factory AdvanceIntroSequenceCmdPtr
CONTRACT["AdvanceIntroSequenceCmdPtr"] = {"compare": ("a", "f"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceIntroSequenceCmdPtr"] = [
	{"a": 0x05, "wram": {wSequenceCmdPtr: b"\x10\x20"}, "expect_regs": {"a": 0x20, "f": 0x00}, "expect": {wSequenceCmdPtr: b"\x15\x20"}},
	{"a": 0x01, "wram": {wSequenceCmdPtr: b"\xFF\x20"}, "expect_regs": {"a": 0x21, "f": 0x00}, "expect": {wSequenceCmdPtr: b"\x00\x21"}},
	dict(POISON, a=0x01, wram={wSequenceCmdPtr: b"\xFF\xFF"}, expect_regs={"a": 0x00, "f": 0xB0}, expect={wSequenceCmdPtr: b"\x00\x00"}),
]
# <<< factory AdvanceIntroSequenceCmdPtr

# >>> factory AdvanceIntroSequenceCmdPtrBy2
CONTRACT["AdvanceIntroSequenceCmdPtrBy2"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceIntroSequenceCmdPtrBy2"] = [
	{"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
	dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
	{"wram": {wSequenceCmdPtr: bytes([254, 0x00])}, "read": {wSequenceCmdPtr: 2}},
	{"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceIntroSequenceCmdPtrBy2

# >>> factory AdvanceIntroSequenceCmdPtrBy4
CONTRACT["AdvanceIntroSequenceCmdPtrBy4"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceIntroSequenceCmdPtrBy4"] = [
	{"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
	dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
	{"wram": {wSequenceCmdPtr: bytes([254, 0x00])}, "read": {wSequenceCmdPtr: 2}},
	{"wram": {wSequenceCmdPtr: b"\xFF\xFF"}, "read": {wSequenceCmdPtr: 2}},
]
# <<< factory AdvanceIntroSequenceCmdPtrBy4

# >>> factory IntroSequenceEmptyFunc
CONTRACT["IntroSequenceEmptyFunc"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e", "hl")}
CASES["IntroSequenceEmptyFunc"] = [
    {"wram": {0xC500: b"\x00"}, "expect": {0xC500: b"\x00"}},
    dict(POISON, wram={0xC500: b"\x00"}, expect={0xC500: b"\x00"}),
]
# <<< factory IntroSequenceEmptyFunc

# >>> factory IntroSequenceCmd_FadeIn
CONTRACT["IntroSequenceCmd_FadeIn"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["IntroSequenceCmd_FadeIn"] = [
    {"wram": {0xD631: b"\x00\x00"}, "read": {0xD631: 2}},
    {"wram": {0xD631: b"\x00\x05"}, "read": {0xD631: 2}},
    dict(POISON, wram={0xD631: b"\x00\x00"}, read={0xD631: 2}),
]
# <<< factory IntroSequenceCmd_FadeIn

# >>> factory IntroSequenceCmd_WaitSFX
CONTRACT["IntroSequenceCmd_WaitSFX"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["IntroSequenceCmd_WaitSFX"] = [
    {"wram": {0xDD82: b"\x80", 0xD631: b"\x00\x00"}, "read": {0xD631: 2}},
    {"wram": {0xDD82: b"\x05", 0xD631: b"\x00\x00"}, "read": {0xD631: 2}},
    dict(POISON, wram={0xDD82: b"\x80", 0xD631: b"\x00\x00"}, read={0xD631: 2}),
]
# <<< factory IntroSequenceCmd_WaitSFX

# >>> factory IntroSequenceCmd_WaitOrbsAnimation
CONTRACT["IntroSequenceCmd_WaitOrbsAnimation"] = {"compare": ("a", "f"), "preserve": ()}
CASES["IntroSequenceCmd_WaitOrbsAnimation"] = [
    {"wram": {0xD629: bytes([0,1,2,3,4,5,6]), 0xD4D0 + 0*16 + 14: b"\x05"}},
    dict(POISON, wram={0xD629: bytes([0,1,2,3,4,5,6]),
         0xD4D0 + 0*16 + 14: b"\xFF", 0xD4D0 + 1*16 + 14: b"\xFF", 0xD4D0 + 2*16 + 14: b"\xFF",
         0xD4D0 + 3*16 + 14: b"\xFF", 0xD4D0 + 4*16 + 14: b"\xFF", 0xD4D0 + 5*16 + 14: b"\xFF",
         0xD4D0 + 6*16 + 14: b"\xFF"}),
    {"wram": {0xD629: bytes([0,1,2,3,4,5,6]),
        0xD4D0 + 0*16 + 14: b"\xFF", 0xD4D0 + 1*16 + 14: b"\xFF", 0xD4D0 + 2*16 + 14: b"\xFF",
        0xD4D0 + 3*16 + 14: b"\xFF", 0xD4D0 + 4*16 + 14: b"\xFF", 0xD4D0 + 5*16 + 14: b"\xFF",
        0xD4D0 + 6*16 + 14: b"\x00"}},
]
# <<< factory IntroSequenceCmd_WaitOrbsAnimation

# >>> factory IntroSequenceCmd_SetOrbsAnimations
CONTRACT["IntroSequenceCmd_SetOrbsAnimations"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b",), "wram_out": True}
CASES["IntroSequenceCmd_SetOrbsAnimations"] = [
    {"b": 0xC5, "c": 0x00, "wram": {0xD629: bytes([0,1,2,3,4,5,6]), 0xC500: bytes([0,0,0,0,0,0,0])}},
    dict(POISON, b=0xC5, c=0x00, wram={0xD629: bytes([0,1,2,3,4,5,6]), 0xC500: bytes([0,0,0,0,0,0,0])}),
]
# <<< factory IntroSequenceCmd_SetOrbsAnimations

# >>> factory IntroSequenceCmd_SetOrbsCoordinates
CONTRACT["IntroSequenceCmd_SetOrbsCoordinates"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b",), "wram_out": True}
CASES["IntroSequenceCmd_SetOrbsCoordinates"] = [
    {"b": 0xC5, "c": 0x00, "wram": {0xD629: bytes([0,1,2,3,4,5,6]), 0xC500: bytes(range(1, 15))}},
    dict(POISON, b=0xC5, c=0x00, wram={0xD629: bytes([0,1,2,3,4,5,6]), 0xC500: bytes(range(1, 15))}),
]
# <<< factory IntroSequenceCmd_SetOrbsCoordinates

# >>> factory IntroSequenceCmd_PlayTitleScreenMusic
CONTRACT["IntroSequenceCmd_PlayTitleScreenMusic"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["IntroSequenceCmd_PlayTitleScreenMusic"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceCmdPtr: 2}},
    {"wram": {wSequenceCmdPtr: b"\x00\x05"}, "read": {wSequenceCmdPtr: 2}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00"}, read={wSequenceCmdPtr: 2}),
]
# <<< factory IntroSequenceCmd_PlayTitleScreenMusic

# >>> factory IntroSequenceCmd_FadeOut
CONTRACT["IntroSequenceCmd_FadeOut"] = {"compare": ("a", "f"), "preserve": ()}
CASES["IntroSequenceCmd_FadeOut"] = [
    {"wram": {wSequenceCmdPtr: b"\x00\x00", wIntroSequencePalsNeedUpdate: b"\x00"},
     "read": {wSequenceCmdPtr: 2, wIntroSequencePalsNeedUpdate: 1}},
    {"wram": {wSequenceCmdPtr: b"\x00\x05", wIntroSequencePalsNeedUpdate: b"\x00"},
     "read": {wSequenceCmdPtr: 2, wIntroSequencePalsNeedUpdate: 1}},
    dict(POISON, wram={wSequenceCmdPtr: b"\x00\x00", wIntroSequencePalsNeedUpdate: b"\x00"},
         read={wSequenceCmdPtr: 2, wIntroSequencePalsNeedUpdate: 1}),
]
# <<< factory IntroSequenceCmd_FadeOut

# >>> factory AdvanceIntroSequenceCmdPtrBy3
CONTRACT["AdvanceIntroSequenceCmdPtrBy3"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["AdvanceIntroSequenceCmdPtrBy3"] = [
    {"wram": {0xD631: b"\x00\x00"}, "read": {0xD631: 2}},
    {"wram": {0xD631: b"\x10\x20"}, "read": {0xD631: 2}},
    {"wram": {0xD631: b"\xFD\xFF"}, "read": {0xD631: 2}},
    dict(POISON, wram={0xD631: b"\x00\x00"}, read={0xD631: 2}),
    {"wram": {0xD631: b"\xFF\xFF"}, "read": {0xD631: 2}},
]
# <<< factory AdvanceIntroSequenceCmdPtrBy3

# >>> factory IntroSequenceCmd_Wait
CONTRACT["IntroSequenceCmd_Wait"] = {"compare": ("a", "f"), "preserve": ()}
CASES["IntroSequenceCmd_Wait"] = [
    {"c": 0x00, "wram": {wSequenceDelay: b"\x00", wSequenceCmdPtr: b"\x00\x00"}, "read": {wSequenceDelay: 1, wSequenceCmdPtr: 2}},
    {"c": 0x7F, "wram": {wSequenceDelay: b"\xFF", wSequenceCmdPtr: b"\xFF\x20"}, "read": {wSequenceDelay: 1, wSequenceCmdPtr: 2}},
    dict(POISON, c=0xCC, wram={wSequenceDelay: b"\x12", wSequenceCmdPtr: b"\x10\x20"}, read={wSequenceDelay: 1, wSequenceCmdPtr: 2}),
]
# <<< factory IntroSequenceCmd_Wait

# >>> factory IntroSequenceCmd_PlaySFX
CONTRACT["IntroSequenceCmd_PlaySFX"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["IntroSequenceCmd_PlaySFX"] = [
    {"c": 0x00, "wram": {0xD631: b"\x00\x00"}, "read": {0xD631: 2}},
    {"c": 0x7F, "wram": {0xD631: b"\x00\x05"}, "read": {0xD631: 2}},
    dict(POISON, c=0xCC, wram={0xD631: b"\x00\x00"}, read={0xD631: 2}),
]
# <<< factory IntroSequenceCmd_PlaySFX

# >>> factory LoadOpeningScene
CONTRACT["LoadOpeningScene"] = {"compare": (), "preserve": ()}
CASES["LoadOpeningScene"] = [
    {"a": 0x00, "b": 0x00, "c": 0x00,
     "wram": {wIntroSequencePalsNeedUpdate: b"\xAA"},
     "expect": {wIntroSequencePalsNeedUpdate: b"\x00"},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, a=0x01, b=0x02, c=0x03,
         wram={wIntroSequencePalsNeedUpdate: b"\xFF"},
         expect={wIntroSequencePalsNeedUpdate: b"\x00"},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory LoadOpeningScene

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AnimateRandomTitleScreenOrb
MUTATIONS["AnimateRandomTitleScreenOrb"] = {
    "source_symbol": "AnimateRandomTitleScreenOrb",
    "before": "\tuint8_t a = (uint8_t)(wTitleScreenOrbCounter & ORB_COUNTER_MASK);",
    "after": "\tuint8_t a = (uint8_t)(wTitleScreenOrbCounter & 0x1fu);",
    "case_ids": ["AnimateRandomTitleScreenOrb-1", "AnimateRandomTitleScreenOrb-2", "AnimateRandomTitleScreenOrb-4"],
}
# <<< factory-mutation AnimateRandomTitleScreenOrb
# >>> factory-mutation AdvanceIntroSequenceCmdPtr
MUTATIONS["AdvanceIntroSequenceCmdPtr"] = {"source_symbol": "AdvanceIntroSequenceCmdPtr", "before": "uint8_t high_before = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));", "after": "uint8_t high_before = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 2u));", "case_ids": ["AdvanceIntroSequenceCmdPtr-0", "AdvanceIntroSequenceCmdPtr-1", "AdvanceIntroSequenceCmdPtr-2"]}
# <<< factory-mutation AdvanceIntroSequenceCmdPtr
# >>> factory-mutation AdvanceIntroSequenceCmdPtrBy2
MUTATIONS["AdvanceIntroSequenceCmdPtrBy2"] = {"source_symbol": "AdvanceIntroSequenceCmdPtrBy2", "before": "\tAdvanceIntroSequenceCmdPtr(2u);", "after": "\tAdvanceIntroSequenceCmdPtr(3u);", "case_ids": ["AdvanceIntroSequenceCmdPtrBy2-0", "AdvanceIntroSequenceCmdPtrBy2-1", "AdvanceIntroSequenceCmdPtrBy2-2", "AdvanceIntroSequenceCmdPtrBy2-3"]}
# <<< factory-mutation AdvanceIntroSequenceCmdPtrBy2
# >>> factory-mutation AdvanceIntroSequenceCmdPtrBy4
MUTATIONS["AdvanceIntroSequenceCmdPtrBy4"] = {"source_symbol": "AdvanceIntroSequenceCmdPtrBy4", "before": "\tAdvanceIntroSequenceCmdPtr(4u);", "after": "\tAdvanceIntroSequenceCmdPtr(5u);", "case_ids": ["AdvanceIntroSequenceCmdPtrBy4-0", "AdvanceIntroSequenceCmdPtrBy4-1", "AdvanceIntroSequenceCmdPtrBy4-2", "AdvanceIntroSequenceCmdPtrBy4-3"]}
# <<< factory-mutation AdvanceIntroSequenceCmdPtrBy4
# >>> factory-mutation IntroSequenceEmptyFunc
MUTATIONS["IntroSequenceEmptyFunc"] = {"source_symbol": "IntroSequenceEmptyFunc", "before": "\t(void)0;", "after": "\tgb_write8(0xC500, 1u);", "case_ids": ["IntroSequenceEmptyFunc-0", "IntroSequenceEmptyFunc-1"]}
# <<< factory-mutation IntroSequenceEmptyFunc
# >>> factory-mutation IntroSequenceCmd_FadeIn
MUTATIONS["IntroSequenceCmd_FadeIn"] = {"source_symbol": "IntroSequenceCmd_FadeIn", "before": "\tuint8_t hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));", "after": "\tuint8_t hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 0u));", "case_ids": ["IntroSequenceCmd_FadeIn-0", "IntroSequenceCmd_FadeIn-1"]}
# <<< factory-mutation IntroSequenceCmd_FadeIn
# >>> factory-mutation IntroSequenceCmd_WaitSFX
MUTATIONS["IntroSequenceCmd_WaitSFX"] = {"source_symbol": "IntroSequenceCmd_WaitSFX", "before": "\tuint8_t a = AssertSFXFinished();\n\tif (a == 0u) {", "after": "\tuint8_t a = AssertSFXFinished();\n\tif (a != 0u) {", "case_ids": ["IntroSequenceCmd_WaitSFX-0", "IntroSequenceCmd_WaitSFX-1"]}
# <<< factory-mutation IntroSequenceCmd_WaitSFX
# >>> factory-mutation IntroSequenceCmd_WaitOrbsAnimation
MUTATIONS["IntroSequenceCmd_WaitOrbsAnimation"] = {"source_symbol": "IntroSequenceCmd_WaitOrbsAnimation", "before": "\t\tif (counter != 0xFFu) {", "after": "\t\tif (counter != 0xFEu) {", "case_ids": ["IntroSequenceCmd_WaitOrbsAnimation-1", "IntroSequenceCmd_WaitOrbsAnimation-2"]}
# <<< factory-mutation IntroSequenceCmd_WaitOrbsAnimation
# >>> factory-mutation IntroSequenceCmd_SetOrbsAnimations
MUTATIONS["IntroSequenceCmd_SetOrbsAnimations"] = {"source_symbol": "IntroSequenceCmd_SetOrbsAnimations", "before": "\t\tStartSpriteAnimation(anim);\n\t\tde = (uint16_t)(de + 1u);", "after": "\t\tStartSpriteAnimation(anim);\n\t\tde = (uint16_t)(de + 2u);", "case_ids": ["IntroSequenceCmd_SetOrbsAnimations-0", "IntroSequenceCmd_SetOrbsAnimations-1"]}
# <<< factory-mutation IntroSequenceCmd_SetOrbsAnimations
# >>> factory-mutation IntroSequenceCmd_SetOrbsCoordinates
MUTATIONS["IntroSequenceCmd_SetOrbsCoordinates"] = {
    "source_symbol": "IntroSequenceCmd_SetOrbsCoordinates",
    "before": "gb_write8((uint16_t)(prop_addr + 1u), y);\n\t\tde = (uint16_t)(de + 1u);",
    "after": "gb_write8((uint16_t)(prop_addr + 1u), y);\n\t\tde = (uint16_t)(de + 2u);",
    "case_ids": ["IntroSequenceCmd_SetOrbsCoordinates-0", "IntroSequenceCmd_SetOrbsCoordinates-1"],
}
# <<< factory-mutation IntroSequenceCmd_SetOrbsCoordinates
# >>> factory-mutation IntroSequenceCmd_PlayTitleScreenMusic
MUTATIONS["IntroSequenceCmd_PlayTitleScreenMusic"] = {"source_symbol": "IntroSequenceCmd_PlayTitleScreenMusic", "before": "uint8_t exit_f = (uint8_t)((ptr_hi == 0u ? 0x80u : 0x00u) | 0x10u);", "after": "uint8_t exit_f = 0x10u;", "case_ids": ["IntroSequenceCmd_PlayTitleScreenMusic-0", "IntroSequenceCmd_PlayTitleScreenMusic-1"]}
# <<< factory-mutation IntroSequenceCmd_PlayTitleScreenMusic
# >>> factory-mutation IntroSequenceCmd_FadeOut
MUTATIONS["IntroSequenceCmd_FadeOut"] = {"source_symbol": "IntroSequenceCmd_FadeOut", "before": "wIntroSequencePalsNeedUpdate = TRUE;", "after": "wIntroSequencePalsNeedUpdate = 0u;", "case_ids": ["IntroSequenceCmd_FadeOut-0", "IntroSequenceCmd_FadeOut-1"]}
# <<< factory-mutation IntroSequenceCmd_FadeOut
# >>> factory-mutation AdvanceIntroSequenceCmdPtrBy3
MUTATIONS["AdvanceIntroSequenceCmdPtrBy3"] = {"source_symbol": "AdvanceIntroSequenceCmdPtrBy3", "before": "\tAdvanceIntroSequenceCmdPtr(3u);", "after": "\tAdvanceIntroSequenceCmdPtr(4u);", "case_ids": ["AdvanceIntroSequenceCmdPtrBy3-0", "AdvanceIntroSequenceCmdPtrBy3-1", "AdvanceIntroSequenceCmdPtrBy3-2", "AdvanceIntroSequenceCmdPtrBy3-3", "AdvanceIntroSequenceCmdPtrBy3-4"]}
# <<< factory-mutation AdvanceIntroSequenceCmdPtrBy3
# >>> factory-mutation IntroSequenceCmd_Wait
MUTATIONS["IntroSequenceCmd_Wait"] = {"source_symbol": "IntroSequenceCmd_Wait", "before": "\tuint8_t f = (uint8_t)((adv.f & 0x80u) | 0x10u);", "after": "\tuint8_t f = (uint8_t)((adv.f & 0x80u) | 0x00u);", "case_ids": ["IntroSequenceCmd_Wait-0", "IntroSequenceCmd_Wait-1", "IntroSequenceCmd_Wait-2"]}
# <<< factory-mutation IntroSequenceCmd_Wait
# >>> factory-mutation IntroSequenceCmd_PlaySFX
MUTATIONS["IntroSequenceCmd_PlaySFX"] = {"source_symbol": "IntroSequenceCmd_PlaySFX", "before": "\tuint8_t f = (uint8_t)((a == 0u ? 0x80u : 0u) | 0x10u);", "after": "\tuint8_t f = (uint8_t)((a == 0u ? 0x80u : 0u) | 0x00u);", "case_ids": ["IntroSequenceCmd_PlaySFX-0", "IntroSequenceCmd_PlaySFX-1", "IntroSequenceCmd_PlaySFX-2"]}
# <<< factory-mutation IntroSequenceCmd_PlaySFX
# >>> factory-mutation LoadOpeningScene
MUTATIONS["LoadOpeningScene"] = {
    "source_symbol": "LoadOpeningScene",
    "before": "\tgb_write8(wIntroSequencePalsNeedUpdate_ADDR, 0u);",
    "after": "\tgb_write8(wIntroSequencePalsNeedUpdate_ADDR, 1u);",
    "case_ids": ["LoadOpeningScene-0", "LoadOpeningScene-1"],
}
# <<< factory-mutation LoadOpeningScene
