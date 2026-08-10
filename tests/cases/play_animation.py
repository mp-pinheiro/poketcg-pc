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
