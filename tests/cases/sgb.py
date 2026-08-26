"""Oracle-diff cases for poketcg/src/home/sgb.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "Wait": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("hl",),
    },
}

_ZERO_RESULT = {"a": 0, "f": 0x80, "b": 0, "c": 0, "d": 0, "e": 0}

CASES = {
    "Wait": [
        {"oracle": False,
         "why": "bc=0 expands to 65536 delay iterations and exceeds the oracle budget",
         "expect_regs": _ZERO_RESULT},
        dict(POISON, b=0, c=1, expect_regs=_ZERO_RESULT),
        {"b": 0, "c": 2},
        {"oracle": False, "b": 1, "c": 0,
         "why": "256 outer delay passes exceed the live PyBoy frame budget",
         "expect_regs": _ZERO_RESULT},
        {"oracle": False, "b": 1, "c": 1,
         "why": "257 outer delay passes exceed the live PyBoy frame budget",
         "expect_regs": _ZERO_RESULT},
    ],
}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory SendSGB
CONTRACT["SendSGB"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["SendSGB"] = [
    {"a": 0x00, "hl": 0xC500, "wram": {0xC500: b"\x00"}, "sram": {0: {}},
     "expect_regs": {"a": 0x00, "f": 0xA0, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0xC500},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"hl": 0xC500, "wram": {0xC500: b"\x01" + b"\x00" * 16}, "sram": {0: {}},
     "expect_regs": {"a": 0x00, "f": 0x80, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0xC510},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, hl=0xC500, wram={0xC500: b"\x00"}, sram={0: {}},
         expect_regs={"a": 0x00, "f": 0xA0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0xC500},
         instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory SendSGB

# >>> factory InitSGB
CONTRACT["InitSGB"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["InitSGB"] = [
    {"sram": {0: {}}, "instruction_budget": 4000000, "cycle_budget": 20000000},
    dict(POISON, sram={0: {}}, instruction_budget=4000000, cycle_budget=20000000),
]
# <<< factory InitSGB

# >>> factory DetectSGB
CONTRACT["DetectSGB"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["DetectSGB"] = [
    {"instruction_budget": 4000000, "cycle_budget": 20000000},
    dict(POISON, instruction_budget=4000000, cycle_budget=20000000),
]
# <<< factory DetectSGB

# >>> factory Func_0bcb
CONTRACT["Func_0bcb"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["Func_0bcb"] = [
    {"hl": 0xA000, "ramg": True, "sram": {0: {0xA000: bytes(range(256)) * 16}}, "wram": {0xCABB: b"\xC3", 0xFF40: b"\x80"}, "vread": {0: {0x8800: 0x1000, 0x9800: 0x1A0}}, "instruction_budget": 500000, "cycle_budget": 2000000},
    dict(POISON, hl=0xA000, ramg=True, sram={0: {0xA000: bytes(range(256)) * 16}}, wram={0xCABB: b"\xC3", 0xFF40: b"\x80"}, vread={0: {0x8800: 0x1000, 0x9800: 0x1A0}}, instruction_budget=500000, cycle_budget=2000000),
]
# <<< factory Func_0bcb

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Wait": {
        "source_symbol": "Wait",
        "before": "\treturn (SGBWaitResult){0, 0x80u, 0, 0, 0, 0};",
        "after": "\treturn (SGBWaitResult){1, 0x80u, 0, 0, 0, 0};",
        "case_ids": ["Wait-0", "Wait-1", "Wait-2"],
    },
}
# >>> factory-mutation SendSGB
MUTATIONS["SendSGB"] = {
    "source_symbol": "SendSGB",
    "before": "\t\treturn (SendSGBResult){0u, 0xA0u, b, c, d, e, hl};",
    "after": "\t\treturn (SendSGBResult){0u, 0x80u, b, c, d, e, hl};",
    "case_ids": ["SendSGB-0", "SendSGB-2", "SendSGB-1"],
}
# <<< factory-mutation SendSGB
# >>> factory-mutation InitSGB
MUTATIONS["InitSGB"] = {
    "source_symbol": "InitSGB",
    "before": "\tr = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AE0u); /* MaskEnPacket_Cancel */",
    "after": "\tr = SendSGB(r.a, r.f, r.b, r.c, r.d, r.e, 0x0AD0u); /* MaskEnPacket_Cancel (mutated) */",
    "case_ids": ["InitSGB-0", "InitSGB-1"],
}
# <<< factory-mutation InitSGB
# >>> factory-mutation DetectSGB
MUTATIONS["DetectSGB"] = {
    "source_symbol": "DetectSGB",
    "before": "\treturn (DetectSGBResult){ok.a, (uint8_t)(ok.a == 0u ? 0x80u : 0x00u), ok.b, ok.c, ok.d, ok.e, ok.hl};",
    "after": "\treturn (DetectSGBResult){ok.a, (uint8_t)(ok.a == 0u ? 0x00u : 0x80u), ok.b, ok.c, ok.d, ok.e, ok.hl};",
    "case_ids": ["DetectSGB-0", "DetectSGB-1"],
}
# <<< factory-mutation DetectSGB
# >>> factory-mutation Func_0bcb
MUTATIONS["Func_0bcb"] = {
    "source_symbol": "Func_0bcb",
    "before": "\t\tuint8_t value = gb_read8((uint16_t)(hl + i));",
    "after": "\t\tuint8_t value = gb_read8((uint16_t)(hl + i + 1u));",
    "case_ids": ["Func_0bcb-0"],
}
# <<< factory-mutation Func_0bcb
