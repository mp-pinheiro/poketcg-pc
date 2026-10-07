from tests.cases._symbols import sym
from tests.cases._fixtures import queued_animations_fixture as _queued_animations_fixture, QUEUED_ANIMATIONS_REGS as _QUEUED_ANIMATIONS_REGS
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
QUEUE = sym("wAnimationQueue")
BUFFER = sym("wDuelAnim1ID")
WDO_FRAME_FN = sym("wDoFrameFunction")
UPDATE_LO = 0xA2
UPDATE_HI = 0x3B
CONTRACT = {
    "_ResetAnimationQueue": {
        "compare": ("b", "c", "hl"),
        "preserve": ("b", "c", "hl"),
    },
    # The sprite path pushes and pops bc/de/hl; the special path (`jp
    # Func_1cb5e`, animations $61+) does not, and no caller reads them.
    "PlayLoadedDuelAnimation": {
        "compare": (),
        "preserve": (),
    },
    "LoadDuelAnimationToBuffer": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "_UpdateQueuedAnimations": {
        "compare": ("a", "b", "c", "hl"),
        "preserve": (),
    },
    "ClearAndDisableQueuedAnimations": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}
CASES = {
    "_ResetAnimationQueue": [
        {"wram": {QUEUE: b"\x00" * 7, sym("wDuelAnimBufferCurPos"): b"\x7f\x7f\x7f"}},
        dict(POISON, wram={QUEUE: b"\x01" * 7, sym("wDuelAnimBufferCurPos"): b"\xaa\xbb\xcc"}),
    ],
    "PlayLoadedDuelAnimation": [
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wTempAnimation"): b"\x00", sym("wAnimationsDisabled"): b"\x00"}},
        dict(POISON, wram={WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wTempAnimation"): b"\x01", sym("wAnimationsDisabled"): b"\x00"},
             expect={sym("wd4bf"): b"\x01"}),
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wTempAnimation"): b"\x01", sym("wAnimationsDisabled"): b"\x01"},
         "expect": {sym("wd4bf"): b"\x01"}},
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, 0x00]), sym("wTempAnimation"): b"\x01", sym("wAnimationsDisabled"): b"\x00"},
         "expect": {sym("wd4bf"): b"\x00"}, "read": {sym("wd4bf"): 1}},
        # DUEL_ANIM_SMALL_SHAKE_X ($61) is a screen animation, not a sprite
        # table row: it registers ShakeScreenX's update and a 24-frame duration.
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wTempAnimation"): b"\x61", sym("wAnimationsDisabled"): b"\x00",
                  sym("wActiveScreenAnim"): b"\xff", sym("wScreenAnimUpdatePtr"): b"\x00\x00\x00\x00\x00"},
         "read": {sym("wActiveScreenAnim"): 1, sym("wScreenAnimUpdatePtr"): 5}},
    ],
    "LoadDuelAnimationToBuffer": [
        {"wram": {sym("wDuelAnimBufferCurPos"): b"\x00", sym("wDuelAnimBufferSize"): b"\x00", sym("wTempAnimation"): b"\x01", sym("wDuelAnimationScreen"): b"\x02",
                  sym("wDuelAnimDuelistSide"): b"\x01", sym("wDuelAnimLocationParam"): b"\x05", sym("wDuelAnimDamage"): b"4\x12",
                  sym("wDuelAnimEffectiveness"): b"\x03", sym("wDuelAnimReturnBank"): b"\x07"}, "read": {BUFFER: 8}},
        dict(POISON, wram={sym("wDuelAnimBufferCurPos"): b"\x08", sym("wDuelAnimBufferSize"): b"\x78", sym("wTempAnimation"): b"\x02",
                           sym("wDuelAnimationScreen"): b"\x00", sym("wDuelAnimDuelistSide"): b"\x00", sym("wDuelAnimLocationParam"): b"\x00",
                           sym("wDuelAnimDamage"): b"\x01\x00", sym("wDuelAnimEffectiveness"): b"\x00", sym("wDuelAnimReturnBank"): b"\x00"},
             read={BUFFER + 0x78: 8}),
        {"wram": {sym("wDuelAnimBufferCurPos"): b"\x00", sym("wDuelAnimBufferSize"): b"\x08"}, "read": {BUFFER: 8}},
    ],
    "_UpdateQueuedAnimations": [
        {"wram": {sym("wActiveScreenAnim"): b"\xff", sym("wd4c0"): b"\xff",
                  QUEUE: b"\x00\x01\x02\x03\x04\x05\x06"},
         "expect": {QUEUE: b"\xff\x01\x02\x03\x04\x05\x06"},
         "expect_regs": {"a": 0}},
        {"wram": {sym("wActiveScreenAnim"): b"\xff", sym("wd4c0"): b"\x01", sym("wWhichSprite"): b"\x00",
                  sym("wSprite1Enabled"): b"\x01", sym("wSprite1Counter"): b"\xff", sym("wAllSpriteAnimationsDisabled"): b"\x00",
                  QUEUE: b"\x00" * 7},
         "read": {sym("wSprite1Enabled"): 1, QUEUE: 7},
         "expect_regs": {"a": 0}},
        dict(POISON, wram={sym("wActiveScreenAnim"): b"\xff", sym("wd4c0"): b"\x80",
                           QUEUE: b"\x01\xff\x02\xff\x03\xff\x04"},
             expect={sym("wd4c0"): b"\xff", QUEUE: b"\x01\xff\x02\xff\x03\xff\x04"},
             expect_regs={"a": 0xff}),
        # A running shake ($61, ShakeScreenX's update at 06:4CFF) on its last
        # frame: the update ends it, wActiveScreenAnim goes back to $ff and the
        # empty buffer leaves a = $ff.
        {"wram": {sym("wActiveScreenAnim"): b"\x61", sym("wd4c0"): b"\xff", sym("wScreenAnimUpdatePtr"): b"\xff\x4c\x01\x55\x4d",
                  sym("hBankROM"): b"\x06", sym("hSCX"): b"\x00", sym("wDuelAnimBufferCurPos"): b"\x00\x00", QUEUE: b"\xff" * 7},
         "read": {sym("wActiveScreenAnim"): 1, sym("wScreenAnimUpdatePtr"): 5, sym("hSCX"): 1}},

        dict(_queued_animations_fixture(vram=False), **_QUEUED_ANIMATIONS_REGS),
    ],
    "ClearAndDisableQueuedAnimations": [
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wActiveScreenAnim"): b"\xFF",
                  QUEUE: b"\x00" * 7, sym("wDuelAnimBufferCurPos"): b"\x01\x02"},
         "expect": {QUEUE: b"\xff" * 7, sym("wDuelAnimBufferCurPos"): b"\x00\x00"},
         "read": {sym("wd4c0"): 1}},
        dict(POISON, wram={WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wActiveScreenAnim"): b"\xFF",
                           QUEUE: b"\x01\xff\x02\xff\x03\xff\x04", sym("wDuelAnimBufferCurPos"): b"\xaa\xbb"},
             expect={QUEUE: b"\xff" * 7, sym("wDuelAnimBufferCurPos"): b"\x00\x00"}),
        {"wram": {WDO_FRAME_FN: b"\x01\x00", sym("wActiveScreenAnim"): b"\xFF", QUEUE: b"\x01" * 7,
                  sym("wDuelAnimBufferCurPos"): b"\x01\x02"}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
_SCHEMA_ZERO = {
    "id": "",
    "hardware": "cgb",
    "mapper": {"rom_bank": 7, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
    "registers": {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0},
    "bus": {},
    "setup": [],
    "input_events": [],
    "instruction_budget": 1000,
    "cycle_budget": 10000,
    "completion": {"mode": "return"},
    "evidence": "primary",
}
_SCHEMA_POISON = {
    "id": "",
    "hardware": "cgb",
    "mapper": {"rom_bank": 7, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
    "registers": dict(POISON),
    "bus": {},
    "setup": [],
    "input_events": [],
    "instruction_budget": 10000,
    "cycle_budget": 100000,
    "completion": {"mode": "return"},
    "evidence": "primary",
}
_pl_zero = dict(_SCHEMA_ZERO, id="PlayLoadedDuelAnimation-zero",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wTempAnimation"): b"\x00",
                     sym("wAnimationsDisabled"): b"\x00"}})
_pl_poison = dict(_SCHEMA_POISON, id="PlayLoadedDuelAnimation-poison",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), sym("wTempAnimation"): b"\x01",
                     sym("wAnimationsDisabled"): b"\x00"}})
_pl_boundary = dict(_SCHEMA_ZERO, id="PlayLoadedDuelAnimation-boundary",
    seeds={"wram": {WDO_FRAME_FN: b"\x00\x00", sym("wTempAnimation"): b"\x01"}})
_lb_zero = dict(_SCHEMA_ZERO, id="LoadDuelAnimationToBuffer-zero",
    seeds={"wram": {sym("wDuelAnimBufferCurPos"): b"\x00", sym("wDuelAnimBufferSize"): b"\x00", sym("wTempAnimation"): b"\x01",
                     sym("wDuelAnimationScreen"): b"\x02", sym("wDuelAnimDuelistSide"): b"\x01", sym("wDuelAnimLocationParam"): b"\x05",
                     sym("wDuelAnimDamage"): b"4\x12", sym("wDuelAnimEffectiveness"): b"\x03", sym("wDuelAnimReturnBank"): b"\x07"}},
    bus={BUFFER: 8})
_lb_poison = dict(_SCHEMA_POISON, id="LoadDuelAnimationToBuffer-poison",
    seeds={"wram": {sym("wDuelAnimBufferCurPos"): b"\x08", sym("wDuelAnimBufferSize"): b"\x78", sym("wTempAnimation"): b"\x02",
                     sym("wDuelAnimationScreen"): b"\x00", sym("wDuelAnimDuelistSide"): b"\x00", sym("wDuelAnimLocationParam"): b"\x00",
                     sym("wDuelAnimDamage"): b"\x01\x00", sym("wDuelAnimEffectiveness"): b"\x00", sym("wDuelAnimReturnBank"): b"\x00"}},
    bus={BUFFER + 0x78: 8})
_lb_boundary = dict(_SCHEMA_ZERO, id="LoadDuelAnimationToBuffer-boundary",
    seeds={"wram": {sym("wDuelAnimBufferCurPos"): b"\x00", sym("wDuelAnimBufferSize"): b"\x08"}},
    bus={BUFFER: 8})
_up_zero = dict(_SCHEMA_ZERO, id="_UpdateQueuedAnimations-zero",
    seeds={"wram": {sym("wActiveScreenAnim"): b"\xff", sym("wd4c0"): b"\x00"}})
_up_poison = dict(_SCHEMA_POISON, id="_UpdateQueuedAnimations-poison",
    seeds={"wram": {sym("wActiveScreenAnim"): b"\xff", sym("wd4c0"): b"\x80"}})
_up_boundary = dict(_SCHEMA_ZERO, id="_UpdateQueuedAnimations-boundary",
    seeds={"wram": {sym("wActiveScreenAnim"): b"\x00", QUEUE: b"\xff" * 7}})
_cl_zero = dict(_SCHEMA_ZERO, id="ClearAndDisableQueuedAnimations-zero",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]),
                     QUEUE: b"\xff" * 7, sym("wDuelAnimBufferCurPos"): b"\x00\x00"}})
_cl_poison = dict(_SCHEMA_POISON, id="ClearAndDisableQueuedAnimations-poison",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]),
                     QUEUE: b"\x01\xff\x02\xff\x03\xff\x04", sym("wDuelAnimBufferCurPos"): b"\xaa\xbb"}})
_cl_boundary = dict(_SCHEMA_ZERO, id="ClearAndDisableQueuedAnimations-boundary",
    seeds={"wram": {WDO_FRAME_FN: b"\x01\x00", QUEUE: b"\x01" * 7,
                     sym("wDuelAnimBufferCurPos"): b"\x01\x02"}})
SCHEMA2_CASES["PlayLoadedDuelAnimation"].extend([_pl_zero, _pl_poison, _pl_boundary])
SCHEMA2_CASES["LoadDuelAnimationToBuffer"].extend([_lb_zero, _lb_poison, _lb_boundary])
SCHEMA2_CASES["_UpdateQueuedAnimations"].extend([_up_zero, _up_poison, _up_boundary])
SCHEMA2_CASES["ClearAndDisableQueuedAnimations"].extend([_cl_zero, _cl_poison, _cl_boundary])
MUTATIONS = {
    "_ResetAnimationQueue": {
        "source_symbol": "_ResetAnimationQueue",
        "before": "for (uint8_t i = 0; i < QUEUE_LENGTH; i++)\n        write((uint16_t)(QUEUE_ADDR + i), 0xff);",
        "after": "for (uint8_t i = 0; i < QUEUE_LENGTH; i++)\n        write((uint16_t)(QUEUE_ADDR + i), 0xfe);",
        "case_ids": ["_ResetAnimationQueue-0", "_ResetAnimationQueue-1"],
    },
    "PlayLoadedDuelAnimation": {
        "source_symbol": "PlayLoadedDuelAnimation",
        "before": "if (animation >= DUEL_SPECIAL_ANIMS) {",
        "after": "if (animation >= 0x96u) {",
        "case_ids": ["PlayLoadedDuelAnimation-4"],
    },
    "LoadDuelAnimationToBuffer": {
        "source_symbol": "LoadDuelAnimationToBuffer",
        "before": "if (next != cur) {",
        "after": "if (next == cur) {",
        "case_ids": ["LoadDuelAnimationToBuffer-0", "LoadDuelAnimationToBuffer-zero"],
    },
    "_UpdateQueuedAnimations": {
        "source_symbol": "_UpdateQueuedAnimations",
        "before": "        uint16_t hl = CallScreenAnimationUpdate();\n        active = read(wActiveScreenAnim_ADDR);",
        "after": "        uint16_t hl = (uint16_t)(wScreenAnimUpdatePtr_ADDR + 1u);\n        active = read(wActiveScreenAnim_ADDR);",
        "case_ids": ["_UpdateQueuedAnimations-3"],
    },
    "ClearAndDisableQueuedAnimations": {"source_symbol": "ClearAndDisableQueuedAnimations", "before": "    write(wd4c0_ADDR, 0xff);\n    if (read(wActiveScreenAnim_ADDR) != 0xff)", "after": "    write(wd4c0_ADDR, 0x00);\n    if (read(wActiveScreenAnim_ADDR) != 0xff)", "case_ids": ["ClearAndDisableQueuedAnimations-0", "ClearAndDisableQueuedAnimations-zero"]},
}
