"""The one seed that drives a duel to a reachable exit.

HandleDuelSetup returns only through core.asm:1836-1840 `scf / ret`, reached
when ChooseInitialArenaAndBenchPokemon fails at core.asm:1770. Every other path
waits on arena, bench and prize input, and the case schema caps input_events at
16 frames, so no case can drive them. Both duelvar pages therefore declare
DUELIST_TYPE_LINK_OPP and both decks hold a single non-basic card, which sends
core.asm:1920-1931 into its serial-exchange error.

Shared by tests/cases/core.py and tests/cases/map.py: any routine reaching
StartDuel needs this exact seed to reach a `ret` on either lane.
"""
from tests.cases._symbols import STACK_TOP, card_id_bytes, sym, sym_pointer

DUEL_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]

# The animation queue and its source pointer, parked so the shuffle-and-draw
# animation does not read unseeded card data.
DUEL_ANIM_SAFE = {
    sym("wActiveScreenAnim"): b"\xff", sym("wd4c0"): b"\xff", sym("wAnimationQueue"): b"\xff" * 7,
    sym("wDoFrameFunction"): sym_pointer("UpdateQueuedAnimations"), sym("wDuelAnimBufferCurPos"): b"\x00", sym("wDuelAnimBufferSize"): b"\x08",
}

DUEL_WRAM = {
    sym("wNPCDuelPrizes"): b"\x06", sym("wDuelTheme"): b"\x01",
    sym("hWhoseTurn"): b"\xC2", sym("wPlayerDuelistType"): b"\x80", sym("wOpponentDuelistType"): b"\x80",
    sym("wDuelType"): b"\x80", sym("wBoosterCardsDrawn"): card_id_bytes(0x08) * 0x3C,
    sym("wOpponentDeck"): card_id_bytes(0x08) * 0x3C,
    sym("wLCDC"): b"\x00", sym("wSkipDelayAllowed"): b"\x01",
    **DUEL_ANIM_SAFE,
}

# One press: the error path needs a single A, and a held key raises no further
# edge, so a longer timeline would change nothing.
# hKeysHeld ($FF90) is deliberately not seeded. Every joypad poll latches it
# and the timeline cycles modulo its entry count, so its value at a stop point
# inside the run is parity-dependent, and seeding it would make a
# non-deterministic byte a compared output.
DUEL_KEYS = [0x00, 0x01]

DUEL_INSTRUCTION_BUDGET = 200000000
DUEL_CYCLE_BUDGET = 800000000
DUEL_ENTRY_SP = STACK_TOP - 2
