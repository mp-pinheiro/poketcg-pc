"""Oracle-diff cases for poketcg/src/home/ai.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
PLAYER_TURN = 0xC2
OPPONENT_TURN = 0xC3

wOpponentDeckID = 0xCC0E
wIsPracticeDuel = 0xCC13
wRNG1 = 0xCACA
wRNG2 = 0xCACB
wRNGCounter = 0xCACC
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wDeckName = 0xCCE9
wPlayerDuelistType = 0xC2F1
wOpponentDuelistType = 0xC3F1

CONTRACT = {
    "LoadOpponentDeck": {"compare": ("a", "hl"), "preserve": ()},
}

CASES = {
    "LoadOpponentDeck": [
        # Sam-normal (deck id 2): forces PRACTICE_PLAYER_DECK onto the OTHER
        # duelist via a swap-load-swap, reseeds the RNG, then loads
        # SAMS_PRACTICE_DECK for the current turn holder.
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x02"},
         "read": {wIsPracticeDuel: 1, wOpponentDeckID: 1, wRNG1: 1, wRNG2: 1,
                  wRNGCounter: 1, wOpponentDeck: 60, wPlayerDeck: 60,
                  wDeckName: 2, wPlayerDuelistType: 1}},
        # Sam-practice (deck id 0): same shape, wIsPracticeDuel ends up 1.
        {"wram": {hWhoseTurn: bytes((OPPONENT_TURN,)), wOpponentDeckID: b"\x00"},
         "read": {wIsPracticeDuel: 1, wOpponentDeckID: 1, wRNG1: 1, wRNG2: 1,
                  wRNGCounter: 1, wOpponentDeck: 60, wPlayerDeck: 60,
                  wDeckName: 2, wOpponentDuelistType: 1}},
        # Plain deck id (not 0 or 2): no Sam handling, no RNG reseed, deck
        # loaded straight onto the current turn holder at deck_id+2.
        {"wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x05"},
         "read": {wIsPracticeDuel: 1, wOpponentDeckID: 1, wPlayerDeck: 60,
                  wDeckName: 2, wPlayerDuelistType: 1}},
        # Right at the boundary (deck_id == NUM_DECK_IDS): DeckPointers[55] is
        # NULL in the real ROM, so LoadDeck no-ops (carry, no copy) -- safe to
        # run, and proves the clamp does NOT fire at 53 (53 < NUM_DECK_IDS+1).
        {"wram": {hWhoseTurn: bytes((OPPONENT_TURN,)), wOpponentDeckID: b"\x35"},
         "read": {wOpponentDeckID: 1, wOpponentDuelistType: 1}},
        dict(POISON, wram={hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x09"},
             read={wIsPracticeDuel: 1, wOpponentDeckID: 1, wPlayerDeck: 60,
                   wDeckName: 2, wPlayerDuelistType: 1}),
        # NUM_DECK_IDS+1 clamp (deck_id=54): oracle-unsafe to run for real --
        # DeckPointers[56] (deck_id+2) is a non-NULL pointer into fixed bank 0
        # ($0614), landing on raw code bytes. copy_deck_data's unbounded
        # (quantity, card-id) loop never finds a terminating zero within a
        # sane distance there (traced by hand: 40+ pairs summing past 4700
        # bytes with no end in sight), so it would scribble across most of
        # WRAM on real hardware too. Verified only against the C port's own
        # clamp logic, never against the oracle.
        {"oracle": False,
         "why": "deck_id=54 clamp forces a LoadDeck(56) read of raw code as "
                "deck data (DeckPointers[56]=$0614, fixed bank 0) -- an "
                "unbounded copy loop that would corrupt WRAM broadly on real "
                "hardware too, not something safe to run through the oracle.",
         "wram": {hWhoseTurn: bytes((PLAYER_TURN,)), wOpponentDeckID: b"\x36"},
         "expect": {wOpponentDeckID: b"\x01", wPlayerDuelistType: b"\x81"},
         "expect_regs": {"a": 0x81}},
    ],
}
# >>> factory-cases-statics
wOpponentDeckID = 0xCC0E
hWhoseTurn = 0xFF97
hTempPlayAreaLocation_ff9d = 0xFF9D

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hTemp_ffa0 = 0xFFA0
# <<< factory-cases-statics

# >>> factory AIDoAction
CONTRACT["AIDoAction"] = {"compare": ("a",), "preserve": ()}
CASES["AIDoAction"] = [
    {"a": 0x03,
     "wram": {wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
     "read": {hTempPlayAreaLocation_ff9d: 1}},
    {"a": 0x04,
     "wram": {wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
     "read": {hTempPlayAreaLocation_ff9d: 1}},
    dict(POISON, a=0x03,
         wram={wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
         read={hTempPlayAreaLocation_ff9d: 1}),
]
# <<< factory AIDoAction

# >>> factory AIDoAction_ForcedSwitch
CONTRACT["AIDoAction_ForcedSwitch"] = {"compare": ("a",), "preserve": ()}
CASES["AIDoAction_ForcedSwitch"] = [
    {"wram": {wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
     "read": {hTempPlayAreaLocation_ff9d: 1}},
    dict(POISON,
         wram={wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
         read={hTempPlayAreaLocation_ff9d: 1}),
]
# <<< factory AIDoAction_ForcedSwitch

# >>> factory AIDoAction_KOSwitch
CONTRACT["AIDoAction_KOSwitch"] = {"compare": ("a",), "preserve": ()}
CASES["AIDoAction_KOSwitch"] = [
    {"wram": {wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
     "read": {hTemp_ffa0: 1}},
    dict(POISON,
         wram={wOpponentDeckID: b"\x01", hWhoseTurn: b"\xC2"},
         read={hTemp_ffa0: 1}),
]
# <<< factory AIDoAction_KOSwitch

# >>> factory AIDoAction_StartDuel
CONTRACT["AIDoAction_StartDuel"] = {"compare": ("a",), "preserve": ()}
CASES["AIDoAction_StartDuel"] = [
    {"wram": {0xCC0E: b"\x01", 0xFF97: b"\xC2", 0xC2BA: b"\x00"},
     "expect_regs": {"a": 0xFF}},
    dict(POISON,
         wram={0xCC0E: b"\x01", 0xFF97: b"\xC2", 0xC2BA: b"\x00"},
         expect_regs={"a": 0xFF}),
]
# <<< factory AIDoAction_StartDuel

# >>> factory AIDoAction_TakePrize
CONTRACT["AIDoAction_TakePrize"] = {"compare": ("a",), "preserve": ()}
CASES["AIDoAction_TakePrize"] = [
    {"wram": {0xFF97: b"\xC3", 0xCCC8: b"\x01", 0xC3EC: b"\x3F", 0xC3EE: b"\x00",
               0xC33C: b"\x00\x00\x00\x00\x00\x00", 0xCC0E: b"\x01"},
     "read": {0xC3EC: 1, 0xC3EE: 1, 0xC342: 1},
     "expect_regs": {"a": 0x05},
     "instruction_budget": 20000000,
     "cycle_budget": 80000000},
    dict(POISON,
         wram={0xFF97: b"\xC3", 0xCCC8: b"\x01", 0xC3EC: b"\x3F", 0xC3EE: b"\x00",
               0xC33C: b"\x00\x00\x00\x00\x00\x00", 0xCC0E: b"\x01"},
         read={0xC3EC: 1, 0xC3EE: 1, 0xC342: 1},
         expect_regs={"a": 0x05},
         instruction_budget=20000000,
         cycle_budget=80000000),
]
# <<< factory AIDoAction_TakePrize

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "LoadOpponentDeck": {
        "source_symbol": "LoadOpponentDeck",
        "before": "\t\t\twIsPracticeDuel = 1;",
        "after": "\t\t\twIsPracticeDuel = 0;",
        "case_ids": ["LoadOpponentDeck-1", "LoadOpponentDeck-4"],
    },
}
# >>> factory-mutation AIDoAction
MUTATIONS["AIDoAction"] = {"source_symbol": "AIDoAction", "before": "\t\t} else if (action == 3u || action == 4u) {", "after": "\t\t} else if (action == 4u) {", "case_ids": ["AIDoAction-0"]}
# <<< factory-mutation AIDoAction
# >>> factory-mutation AIDoAction_ForcedSwitch
MUTATIONS["AIDoAction_ForcedSwitch"] = {"source_symbol": "AIDoAction_ForcedSwitch", "before": "uint8_t AIDoAction_ForcedSwitch(void)\n{\n\tuint8_t result = AIDoAction(0x03u);\n\thTempPlayAreaLocation_ff9d = result;", "after": "uint8_t AIDoAction_ForcedSwitch(void)\n{\n\tuint8_t result = AIDoAction(0x03u);\n\thTempPlayAreaLocation_ff9d = (uint8_t)(result ^ 0xFFu);", "case_ids": ["AIDoAction_ForcedSwitch-0"]}
# <<< factory-mutation AIDoAction_ForcedSwitch
# >>> factory-mutation AIDoAction_KOSwitch
MUTATIONS["AIDoAction_KOSwitch"] = {"source_symbol": "AIDoAction_KOSwitch", "before": "uint8_t AIDoAction_KOSwitch(void)\n{\n\tuint8_t result = AIDoAction(AIACTION_KO_SWITCH);\n\thTemp_ffa0 = result;", "after": "uint8_t AIDoAction_KOSwitch(void)\n{\n\tuint8_t result = AIDoAction(AIACTION_KO_SWITCH);\n\thTemp_ffa0 = (uint8_t)(result ^ 0xFFu);", "case_ids": ["AIDoAction_KOSwitch-0"]}
# <<< factory-mutation AIDoAction_KOSwitch
# >>> factory-mutation AIDoAction_StartDuel
MUTATIONS["AIDoAction_StartDuel"] = {"source_symbol": "AIDoAction_StartDuel", "before": "uint8_t AIDoAction_StartDuel(void)\n{\n\treturn AIDoAction(0x02u);", "after": "uint8_t AIDoAction_StartDuel(void)\n{\n\treturn AIDoAction(0x01u);", "case_ids": ["AIDoAction_StartDuel-0"]}
# <<< factory-mutation AIDoAction_StartDuel
# >>> factory-mutation AIDoAction_TakePrize
MUTATIONS["AIDoAction_TakePrize"] = {"source_symbol": "AIDoAction_TakePrize", "before": "uint8_t AIDoAction_TakePrize(void)\n{\n\treturn AIDoAction(AIACTION_TAKE_PRIZE);", "after": "uint8_t AIDoAction_TakePrize(void)\n{\n\treturn AIDoAction(0x03u);", "case_ids": ["AIDoAction_TakePrize-0"]}
# <<< factory-mutation AIDoAction_TakePrize
