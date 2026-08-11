"""Oracle-diff cases for special_attacks.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
wPlayerCardLocations = 0xC200
wPlayerDeck = 0xC400

CONTRACT = {
    "CheckIfAnyBasicPokemonInDeck": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d"),
    },
}

CASES = {
    "CheckIfAnyBasicPokemonInDeck": [
        {},
        {
            "wram": {
                hWhoseTurn: bytes((PLAYER_TURN,)),
                wPlayerCardLocations: b"\x01" * 60,
            },
        },
        {
            "wram": {
                hWhoseTurn: bytes((PLAYER_TURN,)),
                wPlayerCardLocations: b"\x00\x01" + b"\x01" * 58,
                wPlayerDeck: b"\x08",
            },
        },
        {
            "wram": {
                hWhoseTurn: bytes((PLAYER_TURN,)),
                wPlayerCardLocations: b"\x00\x00" + b"\x01" * 58,
                wPlayerDeck: b"\x09\x08",
            },
        },
        {
            "wram": {
                hWhoseTurn: bytes((PLAYER_TURN,)),
                wPlayerCardLocations: b"\x01" * 59 + b"\x00",
                wPlayerDeck: b"\x00" * 59 + b"\x08",
            },
        },
        dict(
            POISON,
            wram={
                hWhoseTurn: bytes((PLAYER_TURN,)),
                wPlayerCardLocations: b"\x01" + b"\x00" + b"\x01" * 58,
                wPlayerDeck: b"\x01\x08",
            },
        ),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "CheckIfAnyBasicPokemonInDeck": {
        "source_symbol": "CheckIfAnyBasicPokemonInDeck",
        "before": "if (a < TYPE_ENERGY && gb_read8(wLoadedCard2Stage_ADDR) == 0)",
        "after": "if (a >= TYPE_ENERGY && gb_read8(wLoadedCard2Stage_ADDR) == 0)",
        "case_ids": ["CheckIfAnyBasicPokemonInDeck-2", "CheckIfAnyBasicPokemonInDeck-4"],
    },
}
