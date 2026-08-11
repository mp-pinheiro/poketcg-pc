POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wTxRam2 = 0xCE3F
wMultichoiceTextboxResult_ChooseDeckToDuelAgainst = 0xD695
wLoadedEventBits = 0xD3D1
wEventVars = 0xD3D2
EVENT_AARON_BOOSTER_REWARD = wEventVars + 0x1A

CONTRACT = {
    "Func_d96c": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("d", "e"),
    },
    "Script_BeatAaron": {
        "compare": (),
        "preserve": (),
    },
}

CASES = {
    "Func_d96c": [
        {"a": 0, "wram": {wTxRam2: b"\xff\xff\xff"}, "read": {wTxRam2: 3}},
        {"a": 2, "wram": {wTxRam2: b"\xff\xff\xff"}, "read": {wTxRam2: 3}},
        dict(POISON, a=2, wram={wTxRam2: b"\xff\xff\xff"}, read={wTxRam2: 3}),
        {"a": 9, "wram": {wTxRam2: b"\xff\xff\xff"}, "read": {wTxRam2: 3}},
        dict(POISON, a=0xFF, wram={wTxRam2: b"\xff\xff\xff"}, read={wTxRam2: 3}),
    ],
    "Script_BeatAaron": [
        {
            "wram": {wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\x00", EVENT_AARON_BOOSTER_REWARD: b"\xff"},
            "oracle": False,
            "why": "script command engine and booster generation are outside the probe ABI",
            "expect": {wLoadedEventBits: b"\x03", EVENT_AARON_BOOSTER_REWARD: b"\x00"},
        },
        {
            **POISON,
            "wram": {wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\xaa", EVENT_AARON_BOOSTER_REWARD: b"\xff"},
            "oracle": False,
            "why": "script command engine and booster generation are outside the probe ABI",
            "expect": {wLoadedEventBits: b"\x03", EVENT_AARON_BOOSTER_REWARD: b"\x02"},
        },
        {
            "a": 3,
            "wram": {wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\x03", EVENT_AARON_BOOSTER_REWARD: b"\x00"},
            "oracle": False,
            "why": "script command engine and booster generation are outside the probe ABI",
            "expect": {wLoadedEventBits: b"\x03", EVENT_AARON_BOOSTER_REWARD: b"\x03"},
        },
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Func_d96c": {
        "source_symbol": "Func_d96c",
        "before": "uint8_t offset = (uint8_t)((uint8_t)(a - 2u) << 1);",
        "after": "uint8_t offset = (uint8_t)((uint8_t)(a - 1u) << 1);",
        "case_ids": ["Func_d96c-1", "Func_d96c-2", "Func_d96c-3"],
    },
    "Script_BeatAaron": {
        "source_symbol": "Script_BeatAaron",
        "before": "value & EVENT_AARON_BOOSTER_REWARD_MASK",
        "after": "(uint8_t)(value + 1u) & EVENT_AARON_BOOSTER_REWARD_MASK",
        "case_ids": ["Script_BeatAaron-0", "Script_BeatAaron-1", "Script_BeatAaron-2"],
    },
}
