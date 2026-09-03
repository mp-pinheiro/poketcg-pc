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

DUEL_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]

# The animation queue and its source pointer, parked so the shuffle-and-draw
# animation does not read unseeded card data.
DUEL_ANIM_SAFE = {
    0xD42A: b"\xff", 0xD4C0: b"\xff", 0xD423: b"\xff" * 7,
    0xCAD3: bytes([0xA2, 0x3B]), 0xD4AC: b"\x00", 0xD4AD: b"\x08",
}

DUEL_WRAM = {
    0xCC18: b"\x06", 0xCC1A: b"\x01",
    0xFF97: b"\xC2", 0xC2F1: b"\x80", 0xC3F1: b"\x80",
    0xCC09: b"\x80", 0xC400: b"\x08" * 0x3C, 0xC480: b"\x08" * 0x3C,
    0xCABB: b"\x00", 0xCCF2: b"\x01",
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
