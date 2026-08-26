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

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ffa1 = 0xFFA1
wPlayerDuelVariables = 0xC200
wPlayerDeck = 0xC400
wAIPlayEnergyCardForRetreat = 0xCDD7
DUELVARS_ARENA_CARD = 0xBB
DUELVARS_ARENA_CARD_STATUS = 0xF0
DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA = 0xEF
# <<< factory-cases-statics

# >>> factory AITryToRetreat
# Every AIMakeDecision exit of this routine dispatches a bank:1 OppActionTable
# handler, and the reference spins there forever: AIMakeDecision's .delay_loop
# calls DoFrame (pc $0542) and waits on wVBlankCounter, which no VBlank ever
# bumps with the LCD off. So each primary case lands on one of the two
# .set_carry exits -- the Asleep/Paralyzed status gate and the Mysterious
# Fossil / Clefairy Doll route with an empty bench. Between them they pin the
# wAIPlayEnergyCardForRetreat gate, the arena-card id lookup, the
# hTempPlayAreaLocation_ffa1 write of the caller's `pop af`, and both shapes of
# the carry exit (Z from the matching `cp`, Z from the caller's own flags).
CONTRACT["AITryToRetreat"] = {"compare": ("a", "f"), "preserve": ()}
CASES["AITryToRetreat"] = [
    # Asleep arena Pokemon: exit a = status & CNF_SLP_PRZ, carry set, and the
    # popped entry a lands in hTempPlayAreaLocation_ffa1.
    {"a": 0x03,
     "wram": {hWhoseTurn: bytes([PLAYER_TURN]),
              wAIPlayEnergyCardForRetreat: b"\x00",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
              wPlayerDeck: b"\x01",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_STATUS: b"\x02"},
     "read": {hTempPlayAreaLocation_ffa1: 1},
     "instruction_budget": 200000, "cycle_budget": 800000},
    # Poisoned registers, Paralyzed: the second `cp` is the one that matches.
    dict(POISON,
         wram={hWhoseTurn: bytes([PLAYER_TURN]),
               wAIPlayEnergyCardForRetreat: b"\x00",
               wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x00",
               wPlayerDeck: b"\x01",
               wPlayerDuelVariables + DUELVARS_ARENA_CARD_STATUS: b"\x03"},
         read={hTempPlayAreaLocation_ffa1: 1},
         instruction_budget=200000, cycle_budget=800000),
    # Double Poisoned + Paralyzed: only the CNF_SLP_PRZ nibble may decide, and
    # the untouched byte still reaches hTemp_ffa0's `ld b, a` path.
    {"a": 0x2A, "f": 0xB0, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x89AB,
     "wram": {hWhoseTurn: bytes([PLAYER_TURN]),
              wAIPlayEnergyCardForRetreat: b"\x00",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x1e",
              wPlayerDeck + 0x1E: b"\x22",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_STATUS: b"\xc3"},
     "read": {hTempPlayAreaLocation_ffa1: 1},
     "instruction_budget": 200000, "cycle_budget": 800000},
    # Mysterious Fossil with a single Pokemon in play: no bench, so `pop af`
    # restores the caller's a and Z and `scf` only adds carry. Nothing is
    # written on this path, so the case observes registers alone.
    dict(POISON,
         wram={hWhoseTurn: bytes([PLAYER_TURN]),
               wAIPlayEnergyCardForRetreat: b"\x00",
               wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x07",
               wPlayerDeck + 0x07: b"\xcc",
               wPlayerDuelVariables + DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA: b"\x01"},
         instruction_budget=200000, cycle_budget=800000),
    # Clefairy Doll with an empty play area, entry Z clear: the exit f must be
    # carry alone, which is what distinguishes a restored `pop af` from a
    # synthesized $90.
    {"a": 0x5C, "f": 0x40, "b": 0x9E, "c": 0x7D, "d": 0x6C, "e": 0x5B, "hl": 0x4A39,
     "wram": {hWhoseTurn: bytes([PLAYER_TURN]),
              wAIPlayEnergyCardForRetreat: b"\x00",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x3b",
              wPlayerDeck + 0x3B: b"\xcb",
              wPlayerDuelVariables + DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA: b"\x00"},
     "instruction_budget": 200000, "cycle_budget": 800000},
    # Poisoned + Asleep, a different deck slot and an $ff entry a, so the
    # hTempPlayAreaLocation_ffa1 write is pinned to the caller's byte rather
    # than to any play-area constant.
    {"a": 0xFF, "f": 0xF0, "b": 0x01, "c": 0x02, "d": 0x04, "e": 0x08, "hl": 0x0F0F,
     "wram": {hWhoseTurn: bytes([PLAYER_TURN]),
              wAIPlayEnergyCardForRetreat: b"\x00",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD: b"\x2d",
              wPlayerDeck + 0x2D: b"\x0c",
              wPlayerDuelVariables + DUELVARS_ARENA_CARD_STATUS: b"\x82"},
     "read": {hTempPlayAreaLocation_ffa1: 1},
     "instruction_budget": 200000, "cycle_budget": 800000},
]
# <<< factory AITryToRetreat

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
# >>> factory-mutation AITryToRetreat
MUTATIONS["AITryToRetreat"] = {
    "source_symbol": "AITryToRetreat",
    "before": "\thTempPlayAreaLocation_ffa1 = entry_a;",
    "after": "\thTempPlayAreaLocation_ffa1 = 0u;",
    "case_ids": ["AITryToRetreat-0", "AITryToRetreat-1", "AITryToRetreat-2",
                 "AITryToRetreat-5"],
}
# <<< factory-mutation AITryToRetreat
