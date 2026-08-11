POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_STATUS = 0xC2F0
OPPONENT_STATUS = 0xC3F0
PLAYER_PLUSPOWER = 0xC2E0
OPPONENT_PLUSPOWER = 0xC3E0
PLAYER_DEFENDER = 0xC2DA
OPPONENT_DEFENDER = 0xC3DA
PLAYER_DISCARD_COUNT = 0xC2ED
OPPONENT_DISCARD_COUNT = 0xC3ED
PLAYER_DECK = 0xC400
OPPONENT_DECK = 0xC480

CONTRACT = {
    "IsArenaPokemonAsleepOrPoisoned": {
        "compare": ("a", "f", "hl"),
        "preserve": (),
    },
    "DiscardAttachedPlusPowers": {
        "compare": ("a", "b", "c", "f", "hl"),
        "preserve": (),
    },
    "DiscardAttachedDefenders": {
        "compare": ("a", "b", "c", "f", "hl"),
        "preserve": (),
    },
}

CASES = {
    "IsArenaPokemonAsleepOrPoisoned": [
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_STATUS: b"\x00"}},
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_STATUS: b"\x02"}},
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_STATUS: b"\x80"}},
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_STATUS: b"\x03"}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", OPPONENT_STATUS: b"\xC0"}),
    ],
    "DiscardAttachedPlusPowers": [
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_PLUSPOWER: b"\x01\x02\x03\x04\x05\x06",
                  PLAYER_DISCARD_COUNT: b"\x00", 0xC200: b"\x10", PLAYER_DECK: b"\xD8"}},
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_PLUSPOWER: b"\x01\x01\x01\x01\x01\x01",
                  PLAYER_DISCARD_COUNT: b"\x00", 0xC200: b"\x00"}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", OPPONENT_PLUSPOWER: b"\x06\x05\x04\x03\x02\x01",
                           OPPONENT_DISCARD_COUNT: b"\x00", 0xC300: b"\x10", OPPONENT_DECK: b"\xD8"}),
    ],
    "DiscardAttachedDefenders": [
        {"wram": {hWhoseTurn: b"\xC2", PLAYER_DEFENDER: b"\x06\x05\x04\x03\x02\x01",
                  PLAYER_DISCARD_COUNT: b"\x00", 0xC200: b"\x10", PLAYER_DECK: b"\xD9"}},
        dict(POISON, wram={hWhoseTurn: b"\xC3", OPPONENT_DEFENDER: b"\x01\x02\x03\x04\x05\x06",
                           OPPONENT_DISCARD_COUNT: b"\x00", 0xC300: b"\x10", OPPONENT_DECK: b"\xD9"}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "IsArenaPokemonAsleepOrPoisoned": {
        "source_symbol": "IsArenaPokemonAsleepOrPoisoned",
        "before": "value &= (POISONED | DOUBLE_POISONED);",
        "after": "value &= (DOUBLE_POISONED);",
        "case_ids": ["IsArenaPokemonAsleepOrPoisoned-0", "IsArenaPokemonAsleepOrPoisoned-1", "IsArenaPokemonAsleepOrPoisoned-2", "IsArenaPokemonAsleepOrPoisoned-3", "IsArenaPokemonAsleepOrPoisoned-4"],
    },
}
