POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
QUEUE = 0xD423
BUFFER = 0xD42C
WDO_FRAME_FN = 0xCAD3
UPDATE_LO = 0xA2
UPDATE_HI = 0x3B
CONTRACT = {
    "_ResetAnimationQueue": {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")},
    "PlayLoadedDuelAnimation": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")},
    "LoadDuelAnimationToBuffer": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "_UpdateQueuedAnimations": {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ()},
    "ClearAndDisableQueuedAnimations": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
}
CASES = {
    "_ResetAnimationQueue": [
        {"wram": {QUEUE: b"\x00" * 7, 0xD4AC: b"\x7f\x7f\x7f"}},
        dict(POISON, wram={QUEUE: b"\x01" * 7, 0xD4AC: b"\xaa\xbb\xcc"}),
    ],
    "PlayLoadedDuelAnimation": [
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x00"}},
        dict(POISON, wram={WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x00"}, expect={0xD4BF: b"\x00"}),
        dict(POISON, wram={WDO_FRAME_FN: b"\xa2\x00", 0xD422: b"\x01", QUEUE: b"\xff"}, read={QUEUE: 1}),
    ],
    "LoadDuelAnimationToBuffer": [
        {"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x00", 0xD422: b"\x01", 0xD4AE: b"\x02", 0xD4AF: b"\x01", 0xD4B0: b"\x05", 0xD4B1: b"4\x12", 0xD4B3: b"\x03", 0xD4BE: b"\x07"}, "read": {BUFFER: 8}},
        dict(POISON, wram={0xD4AC: b"\x08", 0xD4AD: b"\x78", 0xD422: b"\x02", 0xD4AE: b"\x00", 0xD4AF: b"\x00", 0xD4B0: b"\x00", 0xD4B1: b"\x01\x00", 0xD4B3: b"\x00", 0xD4BE: b"\x00"}, read={BUFFER + 0x78: 8}),
        {"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x78"}, "read": {BUFFER: 8}},
    ],
    "_UpdateQueuedAnimations": [
        {"wram": {0xD42A: b"\xff", 0xD4C0: b"\x00"}, "expect_regs": {"a": 0}},
        dict(POISON, wram={0xD42A: b"\xff", 0xD4C0: b"\x80", 0xD4AC: b"\x00\x00"}, expect={0xD4C0: b"\xff"}, expect_regs={"a": 0}),
        {"wram": {0xD42A: b"\xff", 0xD4C0: b"\x01", QUEUE: b"\x01\xff\xff\xff\xff\xff\xff", 0xD4E0: b"\x01", 0xD4EE: b"\xff"}, "read": {QUEUE: 1, 0xD4E0: 1}, "expect_regs": {"a": 1, "hl": 0xD42A}},
    ],
    "ClearAndDisableQueuedAnimations": [
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD42A: b"\xff", QUEUE: b"\x01\xff\xff\xff\xff\xff\xff", 0xD4E0: b"\x01"}, "read": {QUEUE: 1, 0xD4E0: 1}, "expect": {QUEUE: b"\xff", 0xD4AC: b"\x00\x00", 0xD4E0: b"\x00"}},
        dict(POISON, wram={WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD42A: b"\xff", QUEUE: b"\xff" * 7, 0xD4AC: b"\xaa\xbb"}, expect={QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}),
        {"wram": {WDO_FRAME_FN: b"\x01\x00", 0xD42A: b"\xff", QUEUE: b"\x01" * 7, 0xD4AC: b"\x01\x02"}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
_SCHEMA_ZERO = {"id": "", "hardware": "cgb", "mapper": {"rom_bank": 7, "ram_bank": 0, "vram_bank": 0, "ram_enable": False}, "registers": {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}, "bus": {}, "setup": [], "input_events": [], "instruction_budget": 1000, "cycle_budget": 10000, "completion": {"mode": "return"}, "evidence": "primary"}
_SCHEMA_POISON = dict(_SCHEMA_ZERO, registers=dict(POISON), instruction_budget=10000, cycle_budget=100000)
def _case(base, identifier, seeds, bus=None):
    return dict(base, id=identifier, seeds={"wram": seeds}, bus=bus or {})
SCHEMA2_CASES["PlayLoadedDuelAnimation"].extend([
    _case(_SCHEMA_ZERO, "PlayLoadedDuelAnimation-zero", {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x00"}),
    _case(_SCHEMA_POISON, "PlayLoadedDuelAnimation-poison", {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x00"}),
])
_special_boundary = _case(
    _SCHEMA_ZERO,
    "PlayLoadedDuelAnimation-special-boundary",
    {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x96"},
)
_special_boundary["evidence"] = "dependency-blocked"
_special_boundary["reason"] = "DUEL_SPECIAL_ANIMS dispatches to Func_1ce03 and the screen-animation dependency graph is not ported."
SCHEMA2_CASES["PlayLoadedDuelAnimation"].append(_special_boundary)
SCHEMA2_CASES["LoadDuelAnimationToBuffer"].extend([
    _case(_SCHEMA_ZERO, "LoadDuelAnimationToBuffer-zero", {0xD4AC: b"\x00", 0xD4AD: b"\x00", 0xD422: b"\x01", 0xD4AE: b"\x02", 0xD4AF: b"\x01", 0xD4B0: b"\x05", 0xD4B1: b"4\x12", 0xD4B3: b"\x03", 0xD4BE: b"\x07"}, {BUFFER: 8}),
    _case(_SCHEMA_POISON, "LoadDuelAnimationToBuffer-poison", {0xD4AC: b"\x08", 0xD4AD: b"\x78", 0xD422: b"\x02", 0xD4AE: b"\x00", 0xD4AF: b"\x00", 0xD4B0: b"\x00", 0xD4B1: b"\x01\x00", 0xD4B3: b"\x00", 0xD4BE: b"\x00"}, {BUFFER + 0x78: 8}),
    _case(_SCHEMA_ZERO, "LoadDuelAnimationToBuffer-boundary", {0xD4AC: b"\x00", 0xD4AD: b"\x78"}, {BUFFER: 8}),
])
SCHEMA2_CASES["_UpdateQueuedAnimations"].extend([
    _case(_SCHEMA_ZERO, "_UpdateQueuedAnimations-zero", {0xD42A: b"\xff", 0xD4C0: b"\x00"}),
    _case(_SCHEMA_POISON, "_UpdateQueuedAnimations-poison", {0xD42A: b"\xff", 0xD4C0: b"\x80", 0xD4AC: b"\x00\x00"}),
    _case(_SCHEMA_ZERO, "_UpdateQueuedAnimations-boundary", {0xD42A: b"\xff", 0xD4C0: b"\x01", QUEUE: b"\xff" * 7}),
])
SCHEMA2_CASES["ClearAndDisableQueuedAnimations"].extend([
    _case(_SCHEMA_ZERO, "ClearAndDisableQueuedAnimations-zero", {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}),
    _case(_SCHEMA_POISON, "ClearAndDisableQueuedAnimations-poison", {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), QUEUE: b"\xff" * 7, 0xD4AC: b"\xaa\xbb"}),
    _case(_SCHEMA_ZERO, "ClearAndDisableQueuedAnimations-boundary", {WDO_FRAME_FN: b"\x01\x00", QUEUE: b"\x01" * 7, 0xD4AC: b"\x01\x02"}),
])
MUTATIONS = {
    "_ResetAnimationQueue": {"source_symbol": "_ResetAnimationQueue", "before": "for (uint8_t i = 0; i < QUEUE_LENGTH; i++)\n        write((uint16_t)(QUEUE_ADDR + i), 0xff);", "after": "for (uint8_t i = 0; i < QUEUE_LENGTH; i++)\n        write((uint16_t)(QUEUE_ADDR + i), 0xfe);", "case_ids": ["_ResetAnimationQueue-0", "_ResetAnimationQueue-1"]},
    "PlayLoadedDuelAnimation": {"source_symbol": "PlayLoadedDuelAnimation", "before": "if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))\n        return;", "after": "if (lo != (uint8_t)UPDATE_ADDR && hi != (uint8_t)(UPDATE_ADDR >> 8))\n        return;", "case_ids": ["PlayLoadedDuelAnimation-2"]},
    "LoadDuelAnimationToBuffer": {"source_symbol": "LoadDuelAnimationToBuffer", "before": "if (next != cur) {", "after": "if (next == cur) {", "case_ids": ["LoadDuelAnimationToBuffer-0", "LoadDuelAnimationToBuffer-zero"]},
    "_UpdateQueuedAnimations": {"source_symbol": "_UpdateQueuedAnimations", "before": "if (GetSpriteAnimCounter() == 0xff) {\n                DisableCurSpriteAnim();\n                write(queue_addr, 0xff);", "after": "if (GetSpriteAnimCounter() == 0xff) {\n                /* disabled */\n                write(queue_addr, 0xff);", "case_ids": ["_UpdateQueuedAnimations-0"]},
    "ClearAndDisableQueuedAnimations": {"source_symbol": "ClearAndDisableQueuedAnimations", "before": "write(wWhichSprite_ADDR, sprite);\n            DisableCurSpriteAnim();\n            write(queue_addr, 0xff);", "after": "write(wWhichSprite_ADDR, sprite);\n            /* disabled */\n            write(queue_addr, 0xff);", "case_ids": ["ClearAndDisableQueuedAnimations-0"]},
}
