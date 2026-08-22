POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
ACTIVE = 0xD42A
WD4C0 = 0xD4C0
QUEUE = 0xD423
DO_FRAME_FUNCTION = 0xCAD3

CONTRACT = {
    "CheckAnyAnimationPlaying": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "SetDoFrameFunction": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("f", "b", "c", "d", "e", "hl"),
    },
    "ResetDoFrameFunction": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("f", "b", "c", "d", "e", "hl"),
    },
}

ALL_FF = {ACTIVE: b"\xff", WD4C0: b"\xff", QUEUE: b"\xff" * 7}
ONE_ACTIVE = {ACTIVE: b"\xff", WD4C0: b"\xff", QUEUE: b"\xff\xff\xff\xff\xff\xff\xfe"}

CASES = {
    "CheckAnyAnimationPlaying": [
        {"wram": ALL_FF},
        dict(POISON, wram=ONE_ACTIVE),
    ],
    "SetDoFrameFunction": [
        {"hl": 0x1234, "read": {DO_FRAME_FUNCTION: 2}},
        dict(POISON, hl=0x0000, read={DO_FRAME_FUNCTION: 2}),
    ],
    "ResetDoFrameFunction": [
        {"hl": 0x5678, "read": {DO_FRAME_FUNCTION: 2}},
        dict(POISON, hl=0xABCD, read={DO_FRAME_FUNCTION: 2}),
    ],
# PlayDuelAnimation, UpdateQueuedAnimations, and Func_3bb5 remain unregistered:
# each farcalls the unported duel-animation engine or sprite-animation dispatcher.
# The runnable status and DoFrame-function leaves above are kept separate from
# those orchestrators rather than represented by no-op adapters.
}
# >>> factory PlayDuelAnimation
CONTRACT["PlayDuelAnimation"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("f", "b", "c", "d", "e", "hl"),
}

WDO_FRAME_FN = 0xCAD3
UPDATE_LO = 0xA2
UPDATE_HI = 0x3B
WD4AC = 0xD4AC
WD4AD = 0xD4AD
WD4BE = 0xD4BE
WD4BF = 0xD4BF

CASES["PlayDuelAnimation"] = [
    {"a": 0, "read": {WD4AD: 1, WD4BE: 1, WD4BF: 1}},
    dict(POISON, read={WD4AD: 1, WD4BF: 1}),
    {"a": 1, "wram": {ACTIVE: b"\xff", WD4C0: b"\xff", QUEUE: b"\xff" * 7,
                       WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]),
                       WD4AC: b"\x00", WD4AD: b"\x08"},
     "read": {WD4AD: 1, WD4BF: 1}},
    {"a": 1, "wram": {**ONE_ACTIVE, WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI])},
     "read": {WD4AD: 1, WD4BF: 1}},
    {"a": 1, "wram": {ACTIVE: b"\xff", WD4C0: b"\xff", QUEUE: b"\xff" * 7,
                       WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI])},
     "read": {WD4AD: 1, WD4BF: 1}},
]
# <<< factory PlayDuelAnimation

# >>> factory UpdateQueuedAnimations
CONTRACT["UpdateQueuedAnimations"] = {
    "compare": ("a", "f", "hl"),
    "preserve": ("f",),
}

CUR_POS = 0xD4AC
BUF_SIZE = 0xD4AD

CASES["UpdateQueuedAnimations"] = [
    {"wram": {ACTIVE: b"\xff", WD4C0: b"\x00"}},
    dict(POISON, wram={ACTIVE: b"\xff", WD4C0: b"\x80", CUR_POS: b"\x00", BUF_SIZE: b"\x00"},
         read={WD4C0: 1}),
    {"hl": 0xABCD, "wram": {ACTIVE: b"\xff", WD4C0: b"\x00"}},
    {"hl": 0x1234, "wram": {ACTIVE: b"\xff", WD4C0: b"\xff", QUEUE: b"\xff" * 7,
                             CUR_POS: b"\x00", BUF_SIZE: b"\x00"},
     "read": {QUEUE: 7, WD4C0: 1}},
]
# <<< factory UpdateQueuedAnimations

# >>> factory-cases-statics
WD4C0 = 0xD4C0
hBankROM = 0xFF80
wDuelAnimReturnBank = 0xD4BE
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory Func_3bb5
CONTRACT["Func_3bb5"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_3bb5"] = [
    {"wram": {wDuelAnimReturnBank: b"\x02", WD4C0: b"\x00"},
     "hram": {hBankROM: b"\x01"},
     "read": {WD4C0: 1, hBankROM: 1}},
    dict(POISON,
         wram={wDuelAnimReturnBank: b"\x03", WD4C0: b"\x55"},
         hram={hBankROM: b"\x07"},
         read={WD4C0: 1, hBankROM: 1}),
]
# <<< factory Func_3bb5

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "CheckAnyAnimationPlaying": {
        "source_symbol": "CheckAnyAnimationPlaying",
        "before": "\tif (value == 0xffu)",
        "after": "\tif (value != 0xffu)",
        "case_ids": ["CheckAnyAnimationPlaying-0", "CheckAnyAnimationPlaying-1"],
    },
}
# >>> factory-mutation PlayDuelAnimation
MUTATIONS["PlayDuelAnimation"] = {
    "source_symbol": "PlayDuelAnimation",
    "before": "&& !(CheckAnyAnimationPlaying().f & 0x10u)) {",
    "after": "&& (CheckAnyAnimationPlaying().f & 0x10u)) {",
    "case_ids": ["PlayDuelAnimation-3", "PlayDuelAnimation-4"],
}
# <<< factory-mutation PlayDuelAnimation
# >>> factory-mutation UpdateQueuedAnimations
MUTATIONS["UpdateQueuedAnimations"] = {
    "source_symbol": "UpdateQueuedAnimations",
    "before": "_UpdateQueuedAnimations(hl)",
    "after": "_UpdateQueuedAnimations(0)",
    "case_ids": ["UpdateQueuedAnimations-1", "UpdateQueuedAnimations-2"],
}
# <<< factory-mutation UpdateQueuedAnimations
# >>> factory-mutation Func_3bb5
MUTATIONS["Func_3bb5"] = {
    "source_symbol": "Func_3bb5",
    "before": "gb_write8(wd4c0_ADDR, 0x80u);",
    "after": "gb_write8(wd4c0_ADDR, 0x00u);",
    "case_ids": ["Func_3bb5-0", "Func_3bb5-1"],
}
# <<< factory-mutation Func_3bb5
