"""Oracle-diff cases for poketcg/src/engine/link/ir_functions.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCurSongID = 0xDD80

CONTRACT = {
    "PlayCardPopSong": {"compare": ("hl",), "preserve": ("hl",)},
}

CASES = {
    "PlayCardPopSong": [
        # The routine has no inputs; all registers start at zero.
        {"read": {wCurSongID: 1}},
        # Entry registers are ignored except for the return contract.
        dict(POISON, read={wCurSongID: 1}),
        # Existing song state is replaced by the card-pop song ID.
        {"wram": {wCurSongID: b"\xff"}, "read": {wCurSongID: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _case, _name in zip(SCHEMA2_CASES["PlayCardPopSong"], ("zero", "poison", "boundary")):
    _case["id"] = f"PlayCardPopSong-{_name}"

MUTATIONS = {
    "PlayCardPopSong": {
        "source_symbol": "PlayCardPopSong",
        "before": "PlaySong(MUSIC_CARD_POP);",
        "after": "PlaySong((uint8_t)(MUSIC_CARD_POP + 1u));",
        "case_ids": [
            "PlayCardPopSong-zero",
            "PlayCardPopSong-poison",
            "PlayCardPopSong-boundary",
        ],
    },
}
