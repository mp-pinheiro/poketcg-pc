POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
QUEUE = 0xD423
BUFFER = 0xD42C
WDO_FRAME_FN = 0xCAD3
UPDATE_LO = 0xA2
UPDATE_HI = 0x3B
CONTRACT = {
    "_ResetAnimationQueue": {
        "compare": ("b", "c", "hl"),
        "preserve": ("b", "c", "hl"),
    },
    "PlayLoadedDuelAnimation": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "LoadDuelAnimationToBuffer": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "_UpdateQueuedAnimations": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": (),
    },
    "ClearAndDisableQueuedAnimations": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}
CASES = {
    "_ResetAnimationQueue": [
        {"wram": {QUEUE: b"\x00" * 7, 0xD4AC: b"\x7f\x7f\x7f"}},
        dict(POISON, wram={QUEUE: b"\x01" * 7, 0xD4AC: b"\xaa\xbb\xcc"}),
    ],
    "PlayLoadedDuelAnimation": [
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x00", 0xD421: b"\x00"}},
        dict(POISON, wram={WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x01", 0xD421: b"\x00"},
             expect={0xD4BF: b"\x01"}),
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x01", 0xD421: b"\x01"},
         "expect": {0xD4BF: b"\x01"}},
    ],
    "LoadDuelAnimationToBuffer": [
        {"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x00", 0xD422: b"\x01", 0xD4AE: b"\x02",
                  0xD4AF: b"\x01", 0xD4B0: b"\x05", 0xD4B1: b"4\x12",
                  0xD4B3: b"\x03", 0xD4BE: b"\x07"}, "read": {BUFFER: 8}},
        dict(POISON, wram={0xD4AC: b"\x08", 0xD4AD: b"\x78", 0xD422: b"\x02",
                           0xD4AE: b"\x00", 0xD4AF: b"\x00", 0xD4B0: b"\x00",
                           0xD4B1: b"\x01\x00", 0xD4B3: b"\x00", 0xD4BE: b"\x00"},
             read={BUFFER + 0x78: 8}),
        {"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x08"}, "read": {BUFFER: 8}},
    ],
    "_UpdateQueuedAnimations": [
        {"wram": {0xD42A: b"\xff", 0xD4C0: b"\xff",
                  QUEUE: b"\x00\x01\x02\x03\x04\x05\x06"},
         "expect": {QUEUE: b"\xff\x01\x02\x03\x04\x05\x06"},
         "expect_regs": {"a": 0}},
        dict(POISON, wram={0xD42A: b"\xff", 0xD4C0: b"\x80",
                           QUEUE: b"\x01\xff\x02\xff\x03\xff\x04"},
             expect={0xD4C0: b"\xff", QUEUE: b"\x01\xff\x02\xff\x03\xff\x04"},
             expect_regs={"a": 0xff}),
    ],
    "ClearAndDisableQueuedAnimations": [
        {"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD42A: b"\xFF",
                  QUEUE: b"\x00" * 7, 0xD4AC: b"\x01\x02"},
         "expect": {QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}},
        dict(POISON, wram={WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD42A: b"\xFF",
                           QUEUE: b"\x01\xff\x02\xff\x03\xff\x04", 0xD4AC: b"\xaa\xbb"},
             expect={QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}),
        {"wram": {WDO_FRAME_FN: b"\x01\x00", 0xD42A: b"\xFF", QUEUE: b"\x01" * 7,
                  0xD4AC: b"\x01\x02"}},
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
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x00",
                     0xD421: b"\x00"}})
_pl_poison = dict(_SCHEMA_POISON, id="PlayLoadedDuelAnimation-poison",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]), 0xD422: b"\x01",
                     0xD421: b"\x00"}})
_pl_boundary = dict(_SCHEMA_ZERO, id="PlayLoadedDuelAnimation-boundary",
    seeds={"wram": {WDO_FRAME_FN: b"\x00\x00", 0xD422: b"\x01"}})
_lb_zero = dict(_SCHEMA_ZERO, id="LoadDuelAnimationToBuffer-zero",
    seeds={"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x00", 0xD422: b"\x01",
                     0xD4AE: b"\x02", 0xD4AF: b"\x01", 0xD4B0: b"\x05",
                     0xD4B1: b"4\x12", 0xD4B3: b"\x03", 0xD4BE: b"\x07"}},
    bus={BUFFER: 8})
_lb_poison = dict(_SCHEMA_POISON, id="LoadDuelAnimationToBuffer-poison",
    seeds={"wram": {0xD4AC: b"\x08", 0xD4AD: b"\x78", 0xD422: b"\x02",
                     0xD4AE: b"\x00", 0xD4AF: b"\x00", 0xD4B0: b"\x00",
                     0xD4B1: b"\x01\x00", 0xD4B3: b"\x00", 0xD4BE: b"\x00"}},
    bus={BUFFER + 0x78: 8})
_lb_boundary = dict(_SCHEMA_ZERO, id="LoadDuelAnimationToBuffer-boundary",
    seeds={"wram": {0xD4AC: b"\x00", 0xD4AD: b"\x08"}},
    bus={BUFFER: 8})
_up_zero = dict(_SCHEMA_ZERO, id="_UpdateQueuedAnimations-zero",
    seeds={"wram": {0xD42A: b"\xff", 0xD4C0: b"\x00"}})
_up_poison = dict(_SCHEMA_POISON, id="_UpdateQueuedAnimations-poison",
    seeds={"wram": {0xD42A: b"\xff", 0xD4C0: b"\x80"}})
_up_boundary = dict(_SCHEMA_ZERO, id="_UpdateQueuedAnimations-boundary",
    seeds={"wram": {0xD42A: b"\x00", QUEUE: b"\xff" * 7}})
_cl_zero = dict(_SCHEMA_ZERO, id="ClearAndDisableQueuedAnimations-zero",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]),
                     QUEUE: b"\xff" * 7, 0xD4AC: b"\x00\x00"}})
_cl_poison = dict(_SCHEMA_POISON, id="ClearAndDisableQueuedAnimations-poison",
    seeds={"wram": {WDO_FRAME_FN: bytes([UPDATE_LO, UPDATE_HI]),
                     QUEUE: b"\x01\xff\x02\xff\x03\xff\x04", 0xD4AC: b"\xaa\xbb"}})
_cl_boundary = dict(_SCHEMA_ZERO, id="ClearAndDisableQueuedAnimations-boundary",
    seeds={"wram": {WDO_FRAME_FN: b"\x01\x00", QUEUE: b"\x01" * 7,
                     0xD4AC: b"\x01\x02"}})
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
        "before": "if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))\n        return;",
        "after": "if (lo != (uint8_t)UPDATE_ADDR && hi != (uint8_t)(UPDATE_ADDR >> 8))\n        return;",
        "case_ids": ["PlayLoadedDuelAnimation-0", "PlayLoadedDuelAnimation-zero"],
    },
    "LoadDuelAnimationToBuffer": {
        "source_symbol": "LoadDuelAnimationToBuffer",
        "before": "if (next != cur) {",
        "after": "if (next == cur) {",
        "case_ids": ["LoadDuelAnimationToBuffer-0", "LoadDuelAnimationToBuffer-zero"],
    },
    "_UpdateQueuedAnimations": {
        "source_symbol": "_UpdateQueuedAnimations",
        "before": "DisableCurSpriteAnim();",
        "after": "/* disabled */",
        "case_ids": ["_UpdateQueuedAnimations-0", "_UpdateQueuedAnimations-zero"],
    },
    "ClearAndDisableQueuedAnimations": {
        "source_symbol": "ClearAndDisableQueuedAnimations",
        "before": "DisableCurSpriteAnim();",
        "after": "/* disabled */",
        "case_ids": ["ClearAndDisableQueuedAnimations-0", "ClearAndDisableQueuedAnimations-zero"],
    },
}
