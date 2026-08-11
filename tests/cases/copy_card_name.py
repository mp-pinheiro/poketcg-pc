"""Oracle-diff cases for engine/copy_card_name.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDefaultText = 0xC590
wLoadedCard1Type = 0xCC24
wLoadedCard1Level = 0xCC5D
wCardNameLength = 0xCD9B

CONTRACT = {
    "_CopyCardNameAndLevel_HalfwidthText": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e"),
    },
}

CASES = {
    "_CopyCardNameAndLevel_HalfwidthText": [
        # All-zero input: an empty half-width name gets one padding space.
        {"read": {wDefaultText: 2}},
        # The routine has no register inputs; all register poison must survive
        # except for the returned a and hl values.
        dict(POISON, read={wDefaultText: 2}),
        # Energy cards do not receive a level suffix.
        {"wram": {wCardNameLength: b"\x04", wLoadedCard1Type: b"\x08",
                   wLoadedCard1Level: b"\x0a", wDefaultText: b"\x06AB\x00"},
         "read": {wDefaultText: 9}},
        # One-digit and two-digit levels both use the full four-byte suffix.
        {"wram": {wCardNameLength: b"\x04", wLoadedCard1Type: b"\x00",
                   wLoadedCard1Level: b"\x01", wDefaultText: b"\x06AB\x00"},
         "read": {wDefaultText: 9}},
        {"wram": {wCardNameLength: b"\x04", wLoadedCard1Type: b"\x00",
                   wLoadedCard1Level: b"\x0a", wDefaultText: b"\x06AB\x00"},
         "read": {wDefaultText: 9}},
        # Length one leaves exactly two half-width padding slots.
        {"wram": {wCardNameLength: b"\x01", wLoadedCard1Type: b"\x08",
                   wDefaultText: b"\x06\x00"}, "read": {wDefaultText: 5}},
        # 127 doubles to 256 and wraps the eight-bit counter to zero; the
        # post-test fill therefore writes 255 spaces, not no spaces.
        {"wram": {wCardNameLength: b"\x7f", wLoadedCard1Type: b"\x08",
                   wDefaultText: b"\x00"}, "read": {wDefaultText: 257}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "_CopyCardNameAndLevel_HalfwidthText": {
        "source_symbol": "_CopyCardNameAndLevel_HalfwidthText",
        "before": "if (wLoadedCard1Type < TYPE_ENERGY && wLoadedCard1Level != 0) {",
        "after": "if (wLoadedCard1Type <= TYPE_ENERGY && wLoadedCard1Level != 0) {",
        "case_ids": ["_CopyCardNameAndLevel_HalfwidthText-2",
                     "_CopyCardNameAndLevel_HalfwidthText-3",
                     "_CopyCardNameAndLevel_HalfwidthText-4"],
    },
}
