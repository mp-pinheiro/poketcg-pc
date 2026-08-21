"""Oracle-diff cases for poketcg/src/engine/link/ir_core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory StoreRegistersInIRDataBuffer
CONTRACT["StoreRegistersInIRDataBuffer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "f", "b", "c", "d", "e")}
CASES["StoreRegistersInIRDataBuffer"] = [
    {"wram": {0xCE85: b"\xaa" * 8}},
    dict(POISON, wram={0xCE85: b"\x00" * 8}),
]
# <<< factory StoreRegistersInIRDataBuffer

# >>> factory LoadRegistersFromIRDataBuffer
CONTRACT["LoadRegistersFromIRDataBuffer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["LoadRegistersFromIRDataBuffer"] = [
    {"read": {0xCE85: 8}},
    dict(POISON, wram={0xCE85: b"\xf0\x11\x22\x33\x44\x55\x66\x77"}),
    {"wram": {0xCE85: b"\xaf\x12\x34\x56\x78\x9a\xbc\xde"}},
]
# <<< factory LoadRegistersFromIRDataBuffer

# >>> factory ReturnZFlagUnsetAndCarryFlagSet
CONTRACT["ReturnZFlagUnsetAndCarryFlagSet"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ReturnZFlagUnsetAndCarryFlagSet"] = [
	{},
	dict(POISON),
]
# <<< factory ReturnZFlagUnsetAndCarryFlagSet

# >>> factory TransmitIRBit
CONTRACT["TransmitIRBit"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["TransmitIRBit"] = [
	{"f": 0x00, "hl": 0xFF56, "expect": {0xFF56: b"\xC0"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	{"f": 0x10, "hl": 0xFF56, "expect": {0xFF56: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0xD0}},
	dict(POISON, f=0x00, hl=0xFF56, expect={0xFF56: b"\xC0"}, expect_regs={"a": 0x00, "f": 0xC0}),
	dict(POISON, f=0x10, hl=0xFF56, expect={0xFF56: b"\x00"}, expect_regs={"a": 0x00, "f": 0xD0}),
]
# <<< factory TransmitIRBit

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation StoreRegistersInIRDataBuffer
MUTATIONS["StoreRegistersInIRDataBuffer"] = {"source_symbol": "StoreRegistersInIRDataBuffer", "before": "\tgb_write8(addr++, f);", "after": "\tgb_write8(addr++, a);", "case_ids": ["StoreRegistersInIRDataBuffer-1"]}
# <<< factory-mutation StoreRegistersInIRDataBuffer
# >>> factory-mutation LoadRegistersFromIRDataBuffer
MUTATIONS["LoadRegistersFromIRDataBuffer"] = {"source_symbol": "LoadRegistersFromIRDataBuffer", "before": "\tr.f = (uint8_t)(gb_read8(addr++) & 0xf0u);", "after": "\tr.f = (uint8_t)(gb_read8(addr++) & 0xe0u);", "case_ids": ["LoadRegistersFromIRDataBuffer-1"]}
# <<< factory-mutation LoadRegistersFromIRDataBuffer
# >>> factory-mutation ReturnZFlagUnsetAndCarryFlagSet
MUTATIONS["ReturnZFlagUnsetAndCarryFlagSet"] = {"source_symbol": "ReturnZFlagUnsetAndCarryFlagSet", "before": "return (ReturnZFlagUnsetAndCarryFlagSetResult){0xFFu, 0x10u};", "after": "return (ReturnZFlagUnsetAndCarryFlagSetResult){0xFEu, 0x10u};", "case_ids": ["ReturnZFlagUnsetAndCarryFlagSet-0", "ReturnZFlagUnsetAndCarryFlagSet-1"]}
# <<< factory-mutation ReturnZFlagUnsetAndCarryFlagSet
# >>> factory-mutation TransmitIRBit
MUTATIONS["TransmitIRBit"] = {"source_symbol": "TransmitIRBit", "before": "if ((f & 0x10u) != 0u)", "after": "if ((f & 0x10u) == 0u)", "case_ids": ["TransmitIRBit-0", "TransmitIRBit-1", "TransmitIRBit-2", "TransmitIRBit-3"]}
# <<< factory-mutation TransmitIRBit
