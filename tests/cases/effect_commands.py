"""Oracle-diff cases for poketcg/src/engine/duel/effect_commands.asm.

Real EffectCommands table data (bank 6, from the linked ROM), so the pointer
values returned on a match are exactly what the oracle's ROM read produces --
no need to hand-derive them. EkansSpitPoisonEffectCommands @ $46f7:
  $46f7: type=$03 (EFFECTCMDTYPE_BEFORE_DAMAGE), ptr=$46f8
  $46fa: type=$09 (EFFECTCMDTYPE_AI),            ptr=$46f0
  $46fd: $00 terminator
EkansWrapEffectCommands (the next table) starts at $46fe.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wEffectFunctionsBank = 0xCE22
LIST = 0x46F7
EFFECTCMDTYPE_BEFORE_DAMAGE = 0x03
EFFECTCMDTYPE_AI = 0x09
EFFECTCMDTYPE_INITIAL_EFFECT_1 = 0x01

CONTRACT = {
    "CheckMatchingCommand": {
        "compare": ("f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "d", "e"),
    },
}

CASES = {
    "CheckMatchingCommand": [
        # NULL list: carry, hl echoes the 0 input untouched, no bank switch at all.
        {"a": 0, "hl": 0},
        # Match on the first entry.
        {"a": EFFECTCMDTYPE_BEFORE_DAMAGE, "hl": LIST, "read": {wEffectFunctionsBank: 1}},
        # Match on the second entry.
        {"a": EFFECTCMDTYPE_AI, "hl": LIST, "read": {wEffectFunctionsBank: 1}},
        # Miss: list exhausted, exit hl lands right after the terminator byte.
        {"a": EFFECTCMDTYPE_INITIAL_EFFECT_1, "hl": LIST, "read": {wEffectFunctionsBank: 1}},
        # Poisoned: b/d/e must survive untouched, c must become the entry command
        # type (not stay poisoned), matching a real match.
        dict(POISON, a=EFFECTCMDTYPE_AI, hl=LIST, read={wEffectFunctionsBank: 1}),
        # Poisoned NULL: carry, hl==0, preservation still holds.
        dict(POISON, a=EFFECTCMDTYPE_AI, hl=0),
    ],
}
# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
hBankROM = 0xFF80
wEffectFunctionsBank = 0xCE22
wLoadedAttackEffectCommands = 0xCCB2
# <<< factory-cases-statics

# >>> factory TryExecuteEffectCommandFunction
CONTRACT["TryExecuteEffectCommandFunction"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["TryExecuteEffectCommandFunction"] = [
    {"a": 0x05, "hram": {hBankROM: b"\x01"}, "wram": {wLoadedAttackEffectCommands: b"\xE8\xC0", 0xC0E8: b"\x00", wEffectFunctionsBank: b"\x00"},
     "sram": {0: {}}, "expect_regs": {"a": 0x01, "f": 0x00, "c": 0x05, "hl": 0xC0E9},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    {"a": 0x00, "hram": {hBankROM: b"\x06"}, "wram": {wLoadedAttackEffectCommands: b"\x00\x00"},
     "sram": {0: {}}, "expect_regs": {"a": 0x00, "f": 0x80, "c": 0x00, "hl": 0x0000},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, a=0xAA, hram={hBankROM: b"\x01"}, wram={wLoadedAttackEffectCommands: b"\xE8\xC0", 0xC0E8: b"\x00", wEffectFunctionsBank: b"\x00"},
         sram={0: {}}, expect_regs={"a": 0x01, "f": 0x00, "c": 0xAA, "hl": 0xC0E9},
         instruction_budget=2000000, cycle_budget=8000000),
    {"a": 0x05, "b": 0x12, "d": 0x34, "e": 0x56,
     "hram": {hBankROM: b"\x01", 0xFF97: b"\xC2"},
     "wram": {wLoadedAttackEffectCommands: b"\xE8\xC0", 0xC0E8: b"\x05\xC7\x40\x00", 0xC2F1: b"\x00", wEffectFunctionsBank: b"\x00"},
     "sram": {0: {}}, "expect_regs": {"a": 0x00, "f": 0x90, "b": 0x00, "c": 0x90, "d": 0x34, "e": 0x56, "hl": 0xC2F1},
     "instruction_budget": 2000000, "cycle_budget": 8000000},
]
# <<< factory TryExecuteEffectCommandFunction

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "CheckMatchingCommand": {
        "source_symbol": "CheckMatchingCommand",
        "before": "if (type == a)",
        "after": "if (type != a)",
        "case_ids": ["CheckMatchingCommand-1", "CheckMatchingCommand-2", "CheckMatchingCommand-4", "CheckMatchingCommand-5"],
    },
}
# >>> factory-mutation TryExecuteEffectCommandFunction
MUTATIONS["TryExecuteEffectCommandFunction"] = {
    "source_symbol": "TryExecuteEffectCommandFunction",
    "before": "\tfunction(&state);",
    "after": "\tstate.d = (uint8_t)(state.d + 1u);\n\tfunction(&state);",
    "case_ids": ["TryExecuteEffectCommandFunction-3"],
}
# <<< factory-mutation TryExecuteEffectCommandFunction
