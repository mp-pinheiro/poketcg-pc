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
