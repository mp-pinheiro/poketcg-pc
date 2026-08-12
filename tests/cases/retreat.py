"""Oracle-diff cases for SetAIRetreatFlags (engine/duel/ai/retreat.asm:440-460)."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

W_WHOSE_TURN = 0xCC05
W_LOADED_ATTACK_CATEGORY = 0xCCB1
W_AI_RETREAT_FLAGS = 0xCDDA
W_AI_TRIED_ATTACK = 0xCDDB
PLAYER_TURN = 0xC2
OPPONENT_TURN = 0xC3

CONTRACT = {
    "SetAIRetreatFlags": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "SetAIRetreatFlags": [
        # All-zero player-turn baseline: a non-Pokémon-Power attack sets the flag.
        {"wram": {W_WHOSE_TURN: bytes([PLAYER_TURN]),
                   W_LOADED_ATTACK_CATEGORY: b"\x00"},
         "read": {W_AI_RETREAT_FLAGS: 1}},
        # Poisoned registers and the Pokémon Power early return leave the flag clear.
        dict(POISON,
             wram={W_WHOSE_TURN: bytes([PLAYER_TURN]),
                   W_LOADED_ATTACK_CATEGORY: b"\x04"},
             read={W_AI_RETREAT_FLAGS: 1}),
        # Category boundaries around POKEMON_POWER exercise both player branches.
        {"wram": {W_WHOSE_TURN: bytes([PLAYER_TURN]),
                   W_LOADED_ATTACK_CATEGORY: b"\x03"},
         "read": {W_AI_RETREAT_FLAGS: 1}},
        {"wram": {W_WHOSE_TURN: bytes([PLAYER_TURN]),
                   W_LOADED_ATTACK_CATEGORY: b"\x05"},
         "read": {W_AI_RETREAT_FLAGS: 1}},
        # Opponent with no tried attack sets the flag; a tried attack returns early.
        {"wram": {W_WHOSE_TURN: bytes([OPPONENT_TURN]),
                   W_AI_TRIED_ATTACK: b"\x00"},
         "read": {W_AI_RETREAT_FLAGS: 1}},
        dict(POISON,
             wram={W_WHOSE_TURN: bytes([OPPONENT_TURN]),
                   W_AI_TRIED_ATTACK: b"\xff"},
             read={W_AI_RETREAT_FLAGS: 1},
             keys=0),
        # The target byte is exact: adjacent bytes must remain untouched.
        {"wram": {W_WHOSE_TURN: bytes([PLAYER_TURN]),
                   W_LOADED_ATTACK_CATEGORY: b"\x00",
                   W_AI_RETREAT_FLAGS - 1: b"\x11",
                   W_AI_RETREAT_FLAGS: b"\xaa",
                   W_AI_RETREAT_FLAGS + 1: b"\x22"},
         "read": {W_AI_RETREAT_FLAGS - 1: 1, W_AI_RETREAT_FLAGS: 1,
                  W_AI_RETREAT_FLAGS + 1: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema

MUTATIONS = {
    "SetAIRetreatFlags": {
        "source_symbol": "SetAIRetreatFlags",
        "before": "gb_write8(wAIRetreatFlags_ADDR, 0);",
        "after": "gb_write8(wAIRetreatFlags_ADDR, 0xFF);",
        "case_ids": [f"SetAIRetreatFlags-{i}" for i in range(len(CASES["SetAIRetreatFlags"]))],
    },
}

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
