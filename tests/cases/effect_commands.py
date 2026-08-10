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
    "CheckMatchingCommand": ("f", "b", "c", "d", "e", "hl"),
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
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
