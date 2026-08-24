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

# >>> factory ReturnZFlagUnsetAndCarryFlagSet2
CONTRACT["ReturnZFlagUnsetAndCarryFlagSet2"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")};
CASES["ReturnZFlagUnsetAndCarryFlagSet2"] = [
	{},
	dict(POISON),
]
# <<< factory ReturnZFlagUnsetAndCarryFlagSet2

# >>> factory ReceiveByteThroughIR
CONTRACT["ReceiveByteThroughIR"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["ReceiveByteThroughIR"] = [
    {"wram": {0xFF56: b"\x3E"}},
    dict(POISON, wram={0xFF56: b"\x3E"}),
    dict(POISON, wram={0xFF56: b"\x3C"},
         oracle=False,
         why="rRP is a real hardware IR port register; the reference oracle ignores memory seeds there and always reads back the idle value, so the light-received (bit1-clear) branch is only reachable in the native harness, not against real hardware",
         expect_regs={"a": 0x00, "f": 0x80}),
]
# <<< factory ReceiveByteThroughIR

# >>> factory ReceiveByteThroughIR_ZeroIfUnsuccessful
CONTRACT["ReceiveByteThroughIR_ZeroIfUnsuccessful"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ReceiveByteThroughIR_ZeroIfUnsuccessful"] = [
    {"wram": {0xFF56: b"\x3E"}},
    dict(POISON, wram={0xFF56: b"\x3E"}),
]
# <<< factory ReceiveByteThroughIR_ZeroIfUnsuccessful

# >>> factory ReceiveNBytesToHLThroughIR
CONTRACT["ReceiveNBytesToHLThroughIR"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["ReceiveNBytesToHLThroughIR"] = [
    {"hl": 0xC500, "c": 0x03, "wram": {0xFF56: b"\x3E", 0xC500: b"\xFF\xFF\xFF"}, "read": {0xC500: 3}},
    dict(POISON, hl=0xC500, c=0x03, wram={0xFF56: b"\x3E", 0xC500: b"\xFF\xFF\xFF"}, read={0xC500: 3}),
]
# <<< factory ReceiveNBytesToHLThroughIR

# >>> factory TransmitByteThroughIR
CONTRACT["TransmitByteThroughIR"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["TransmitByteThroughIR"] = [
    {"a": 0x00, "keys": 0x02},
    {"a": 0xA5, "keys": 0x02},
    {"a": 0xFF, "keys": 0x02},
    dict(POISON, a=0xAA, keys=0x02),
]
# <<< factory TransmitByteThroughIR

# >>> factory Func_1971e
CONTRACT["Func_1971e"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_1971e"] = [
    {"keys": 0x02},
    dict(POISON, keys=0x02),
]
# <<< factory Func_1971e

# >>> factory TransmitNBytesFromHLThroughIR
CONTRACT["TransmitNBytesFromHLThroughIR"] = {"compare": ("a", "f", "hl"), "preserve": ()}
CASES["TransmitNBytesFromHLThroughIR"] = [
    {"hl": 0xC500, "c": 0x01, "keys": 0x02, "wram": {0xC500: b"\x11"}},
    dict(POISON, hl=0xC500, c=0x01, keys=0x02, wram={0xC500: b"\x11"}),
]
# <<< factory TransmitNBytesFromHLThroughIR

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
# >>> factory-mutation ReturnZFlagUnsetAndCarryFlagSet2
MUTATIONS["ReturnZFlagUnsetAndCarryFlagSet2"] = {"source_symbol": "ReturnZFlagUnsetAndCarryFlagSet2", "before": "return result;", "after": "result.a ^= 1u;\n\treturn result;", "case_ids": ["ReturnZFlagUnsetAndCarryFlagSet2-0", "ReturnZFlagUnsetAndCarryFlagSet2-1"]}
# <<< factory-mutation ReturnZFlagUnsetAndCarryFlagSet2
# >>> factory-mutation ReceiveByteThroughIR
MUTATIONS["ReceiveByteThroughIR"] = {"source_symbol": "ReceiveByteThroughIR", "before": "if ((rp & (1u << B_RP_DATA_IN_470)) == 0u)\n\t\t\tbreak;", "after": "if ((rp & (1u << B_RP_DATA_IN_470)) != 0u)\n\t\t\tbreak;", "case_ids": ["ReceiveByteThroughIR-0"]}
# <<< factory-mutation ReceiveByteThroughIR
# >>> factory-mutation ReceiveByteThroughIR_ZeroIfUnsuccessful
MUTATIONS["ReceiveByteThroughIR_ZeroIfUnsuccessful"] = {"source_symbol": "ReceiveByteThroughIR_ZeroIfUnsuccessful", "before": "if (r.f & 0x10u)\n\t\treturn (ReceiveByteThroughIRResult){0u, 0x80u};", "after": "if (r.f & 0x10u)\n\t\treturn (ReceiveByteThroughIRResult){1u, 0x00u};", "case_ids": ["ReceiveByteThroughIR_ZeroIfUnsuccessful-0"]}
# <<< factory-mutation ReceiveByteThroughIR_ZeroIfUnsuccessful
# >>> factory-mutation ReceiveNBytesToHLThroughIR
MUTATIONS["ReceiveNBytesToHLThroughIR"] = {"source_symbol": "ReceiveNBytesToHLThroughIR", "before": "\t\tif (r.f & 0x10u) {", "after": "\t\tif (r.f & 0x20u) {", "case_ids": ["ReceiveNBytesToHLThroughIR-0", "ReceiveNBytesToHLThroughIR-1"]}
# <<< factory-mutation ReceiveNBytesToHLThroughIR
# >>> factory-mutation TransmitByteThroughIR
MUTATIONS["TransmitByteThroughIR"] = {
    "source_symbol": "TransmitByteThroughIR",
    "before": "\tif ((joyp & P11) == 0u) {",
    "after": "\tif ((joyp & P11) != 0u) {",
    "case_ids": ["TransmitByteThroughIR-0", "TransmitByteThroughIR-1"],
}
# <<< factory-mutation TransmitByteThroughIR
# >>> factory-mutation Func_1971e
MUTATIONS["Func_1971e"] = {
    "source_symbol": "Func_1971e",
    "before": "\t\t\treturn (Func_1971eResult){err.a, err.f};",
    "after": "\t\t\treturn (Func_1971eResult){(uint8_t)(err.a + 1u), err.f};",
    "case_ids": ["Func_1971e-0", "Func_1971e-1"],
}
# <<< factory-mutation Func_1971e
# >>> factory-mutation TransmitNBytesFromHLThroughIR
MUTATIONS["TransmitNBytesFromHLThroughIR"] = {
    "source_symbol": "TransmitNBytesFromHLThroughIR",
    "before": "\t\tb = (uint8_t)(b + byte);\n\t\thl = (uint16_t)(hl + 1u);",
    "after": "\t\tb = (uint8_t)(b + byte);\n\t\thl = (uint16_t)(hl + 2u);",
    "case_ids": ["TransmitNBytesFromHLThroughIR-0", "TransmitNBytesFromHLThroughIR-1"],
}
# <<< factory-mutation TransmitNBytesFromHLThroughIR
