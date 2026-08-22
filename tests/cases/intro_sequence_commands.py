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
