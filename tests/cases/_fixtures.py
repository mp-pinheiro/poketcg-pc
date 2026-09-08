"""Live game states captured from the reference for fixture-backed cases.

A fixture is `tools/completion/session.py capture NAME --routine R`: the
reference's registers, SP, WRAM, HRAM and VRAM bank 0 at R's entry while it
replays a recorded session. Seeded whole, a routine runs exactly as the game
does, and `keys` taps A through every text box it opens. The observations
cover both duelists' variables, the damage/effect working area and the
redrawn BG map.

`practice-win-attack-entry.json` is session `practice-win` at DoFrame 35383,
the entry of PlayAttackAnimation_DealAttackDamage: Goldeen's Horn Attack on
Sam's Machop in turn 1 of the practice duel.
"""
import json
from pathlib import Path

# Bytes the two reference lanes cannot agree on with the native lane, left
# unseeded and uncompared. wIE ($CAB7) mirrors rIE, which each lane arms for
# itself. wVBlankCounter ($CAB8), wCursorBlinkCounter ($CD0F) and
# wCheckMenuCursorBlinkCounter ($CEA3) count frames spent in key waits, which
# the PyBoy lane runs many DoFrames per tick (it skips the VBlank halt).
# wFlushPaletteFlags ($CABF) and wVBlankOAMCopyToggle ($CAC0) are consumed by
# the VBlank ISR. Do not widen this for a byte the game computes.
# $CFF0-$CFF5 and $DC30-$DCFF are the PyBoy oracle's synthesized call frame
# (tools/oracle/pyboy_oracle.py RESERVED); $DD80+ is the sound driver's.
_HOLES = (0xCAB7, 0xCAB8, 0xCABF, 0xCAC0, 0xCD0F, 0xCEA3)
_SPANS = ((0xC000, 0xCFF0), (0xD000, 0xDC30), (0xDD00, 0xDD80))
# The joypad snapshot hDPadRepeat..hKeysPressed ($FF8D-$FF91) is the `keys`
# timeline as each lane injects it: the probe advances it per completed poll,
# PyBoy per frame, so a routine that polls inside its own DoFrame loop
# (ExecuteNPCMovement) exits on different entries. The game state the polls
# drove is compared through WRAM; the snapshot itself is not.
_HRAM_HOLES = (0xFF8D, 0xFF8E, 0xFF8F, 0xFF90, 0xFF91)


class Fixture:
    """One captured state (`session.py capture NAME --routine R`) as a case
    builder: `Fixture("practice-win-attack-entry").case(**{"C3C8": b"\\x00"})`."""

    def __init__(self, name: str):
        data = json.load(open(Path(__file__).resolve().parent.parent / "fixtures" / f"{name}.json"))
        self.name = name
        self.ordinal = data["ordinal"]
        self.entry = data["entry"]
        self.regs = data["regs"]
        self.sp = data["sp"]
        self.wram = bytes.fromhex(data["wram"])
        self.hram = bytes.fromhex(data["hram"])
        self.vram = bytes.fromhex(data["vram0"])

    def case(self, vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
        """The captured state with `changes` ({"C3C8": bytes} hex addresses)
        patched in, as a case body. `vram=False` leaves VRAM unseeded and
        uncompared, for a routine that returns mid-frame: the gbref lane's PPU
        answers $FF to a VRAM read during mode 3. `bank` seeds hBankROM for a
        banked routine: the reference leaves the routine's own bank selected at
        its `ret` and the probe's bank guard restores the entry value, so
        seeding the routine's bank is the one value both lanes exit with. A home
        routine keeps the captured value; PyBoy needs the shadow consistent
        with the mapped bank or the first bank restore maps garbage."""
        wram = bytearray(self.wram)
        hram = bytearray(self.hram)
        for addr, data in changes.items():
            address = int(addr, 16)
            if address >= 0xFF80:
                hram[address - 0xFF80:address - 0xFF80 + len(data)] = data
            else:
                wram[address - 0xC000:address - 0xC000 + len(data)] = data
        if bank is not None:
            hram[0] = bank
        spans = {}
        for start, end in _SPANS:
            cursor = start
            for hole in sorted(_HOLES):
                if start <= hole < end:
                    spans[cursor] = bytes(wram[cursor - 0xC000:hole - 0xC000])
                    cursor = hole + 1
            spans[cursor] = bytes(wram[cursor - 0xC000:end - 0xC000])
        # $FFB8-$FFFE is the unused HRAM tail (hram.asm `ds $38`); the gbref
        # runner's setup calls run on a stack up there.
        cursor = 0xFF80
        for hole in _HRAM_HOLES:
            spans[cursor] = bytes(hram[cursor - 0xFF80:hole - 0xFF80])
            cursor = hole + 1
        spans[cursor] = bytes(hram[cursor - 0xFF80:0x38])
        if vram:
            spans[0x8000] = self.vram
        # rLCDC from the game's own wLCDC mirror: the gbref lane runs a real PPU,
        # and with the LCD off its first `halt` would wait for a VBlank forever.
        spans[0xFF40] = bytes([self.wram[0xCABB - 0xC000]])
        # The game's own SP: the gbref lane otherwise parks the stack at $FFFE, and
        # a deep call plus real interrupt frames would grow it down through
        # hKeysHeld and the rest of HRAM.
        case = {"wram": spans, "entry_sp": self.sp,
                "read": {0xC200: 0x200, 0xCC00: 0x100},
                "keys": [0x00, 0x01], "instruction_budget": 40000000, "cycle_budget": 160000000}
        if vram:
            case["vread"] = {0: {0x9800: 0x400}}
        return case


ATTACK = Fixture("practice-win-attack-entry")
ATTACK_REGS = ATTACK.regs
# Func_c141's entry after the practice duel: wActiveGameEvent = GAME_EVENT_DUEL,
# Dr. Mason's lab loaded, Sam's after-duel script about to be dispatched.
AFTER_DUEL = Fixture("practice-win-after-duel-entry")
AFTER_DUEL_REGS = AFTER_DUEL.regs
# Func_c9b8's entry at the game's start: wCurMap = OVERWORLD_MAP, so the
# LOAD_MAP slot is LoadOverworld (Func_d4fb, then Script_BeginGame).
LOAD_MAP = Fixture("practice-win-load-map-entry")
LOAD_MAP_REGS = LOAD_MAP.regs
# AIProcessEnergyCards' entry in the AI-versus-AI session ai-duel-02 at DoFrame
# 24437: the second duelist's turn, an energy card in hand, the reference
# attaches it and the port did not.
AI_ENERGY = Fixture("ai-duel-02-energy-entry")
AI_ENERGY_REGS = AI_ENERGY.regs
# CheckIfDefendingPokemonCanKnockOut's entry inside that same AIProcessEnergyCards
# call, scoring the arena card.
AI_DEFENDING_KO = Fixture("ai-duel-02-defending-ko-entry")
AI_DEFENDING_KO_REGS = AI_DEFENDING_KO.regs
# AITryToPlayEnergyCard's entry in that call: the arena card chosen, the
# energy list built, one basic energy of the arena card's color in hand.
AI_TRY_ENERGY = Fixture("ai-duel-02-try-energy-entry")
AI_TRY_ENERGY_REGS = AI_TRY_ENERGY.regs
# CheckIfEvolutionNeedsEnergyForAttack's entry at DoFrame 33500 of the same
# session: neither of the arena card's attacks needs energy, so
# AITryToPlayEnergyCard asks whether its evolution would.
AI_EVOLUTION_ENERGY = Fixture("ai-duel-02-evolution-energy-entry")
AI_EVOLUTION_ENERGY_REGS = AI_EVOLUTION_ENERGY.regs
# The same AI turn after the energy attach, DoFrame 24548: AIDecidePlayPokemonCard's
# second call and AIProcessAndTryToUseAttack's entry (AIProcessAttacks shares it).
AI_PLAY_POKEMON = Fixture("ai-duel-02-play-pokemon-entry")
AI_PLAY_POKEMON_REGS = AI_PLAY_POKEMON.regs
AI_EVOLUTION = Fixture("ai-duel-02-evolution-entry")
AI_EVOLUTION_REGS = AI_EVOLUTION.regs
AI_ATTACK = Fixture("ai-duel-02-attack-entry")
AI_ATTACK_REGS = AI_ATTACK.regs
# GetAIScoreOfAttack's entry for the first attack in that same call.
AI_ATTACK_SCORE = Fixture("ai-duel-02-attack-score-entry")
AI_ATTACK_SCORE_REGS = AI_ATTACK_SCORE.regs
# EstimateDamage_VersusDefendingCard's entry from AIProcessAttacks.execute in
# that same turn: the chosen attack's damage against the player's arena card.
AI_ESTIMATE = Fixture("ai-duel-02-estimate-entry")
AI_ESTIMATE_REGS = AI_ESTIMATE.regs
# AIDecide_Bill's entry at DoFrame 25589, phase 4 of the trainer-card pass with
# eleven cards left in the deck: the parameter byte is the count the cp leaves.
AI_BILL = Fixture("ai-duel-02-bill-entry")
AI_BILL_REGS = AI_BILL.regs
# AIDecideBenchPokemonToSwitchTo's entry at DoFrame 26540: the AI's arena card
# was just knocked out and it picks the bench card to promote.
AI_KO_SWITCH = Fixture("ai-duel-02-ko-switch-entry")
AI_KO_SWITCH_REGS = AI_KO_SWITCH.regs
# The retreat phase of the AI turn at DoFrame 28004: deciding to retreat, the
# bench card to switch to, and the retreat itself (a = 2, the chosen bench slot).
AI_RETREAT_DECISION = Fixture("ai-duel-02-retreat-decision-entry")
AI_RETREAT_DECISION_REGS = AI_RETREAT_DECISION.regs
AI_RETREAT_SWITCH = Fixture("ai-duel-02-retreat-switch-entry")
AI_RETREAT_SWITCH_REGS = AI_RETREAT_SWITCH.regs
AI_TRY_RETREAT = Fixture("ai-duel-02-try-retreat-entry")
AI_TRY_RETREAT_REGS = AI_TRY_RETREAT.regs
# Back in the lab after the AI duel, DoFrame 37028: the after-duel script's
# MOVE_ACTIVE_NPC, from the script command through the first movement step.
NPC_EXECUTE = Fixture("ai-duel-02-npc-execute-entry")
NPC_EXECUTE_REGS = NPC_EXECUTE.regs
NPC_START = Fixture("ai-duel-02-npc-start-entry")
NPC_START_REGS = NPC_START.regs
NPC_MOVE = Fixture("ai-duel-02-npc-move-entry")
NPC_MOVE_REGS = NPC_MOVE.regs
# The TAS route's DisplayPlayAreaScreenToUsePkmnPower at DoFrame 35174: the
# player opens the play area to use a Pokemon Power; the case's B press cancels.
POWER_SCREEN = Fixture("tas-5530s-pkmn-power-screen-entry")
POWER_SCREEN_REGS = POWER_SCREEN.regs
# The TAS route's B press out of the In Play Area screen (DoFrame 61557): the
# exit must leave wCheckMenuCursorBlinkCounter as the frame found it.
IN_PLAY_AREA_B_EXIT = Fixture("tas-5530s-in-play-area-b-exit-entry")
IN_PLAY_AREA_B_EXIT_REGS = IN_PLAY_AREA_B_EXIT.regs
# The fighting-club route's first walk (DoFrame 99702): DOWN held, one pixel of
# the step left, so the step and its arrival (Func_c6dc) both run this frame.
MOVE_STEP = Fixture("fighting-club-move-step-entry")
MOVE_STEP_REGS = MOVE_STEP.regs
# The rock-club route's B press on the Potion target screen (DoFrame 118590):
# HandleMenuInput under PlayAreaScreenMenuFunction must report the cancel.
PLAY_AREA_B = Fixture("rock-club-play-area-b-entry")
PLAY_AREA_B_REGS = PLAY_AREA_B.regs
# andrew-duel at DoFrame 163975: the AI's Tentacool uses Cowardice with more
# Pokemon in play, so the scan restarts from the arena.
COWARDICE = Fixture("andrew-duel-cowardice-entry")
COWARDICE_REGS = COWARDICE.regs
# ryan-duel at DoFrame 210731: Ryan's AI weighs a retreat and decides against it.
RETREAT_STAY = Fixture("ryan-duel-retreat-decision-entry")
RETREAT_STAY_REGS = RETREAT_STAY.regs


def attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ATTACK.case(vram=vram, bank=bank, **changes)


def after_duel_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AFTER_DUEL.case(vram=vram, bank=bank, **changes)


def load_map_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return LOAD_MAP.case(vram=vram, bank=bank, **changes)


def ai_energy_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ENERGY.case(vram=vram, bank=bank, **changes)


def ai_defending_ko_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_DEFENDING_KO.case(vram=vram, bank=bank, **changes)


def ai_try_energy_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_TRY_ENERGY.case(vram=vram, bank=bank, **changes)


def ai_evolution_energy_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_EVOLUTION_ENERGY.case(vram=vram, bank=bank, **changes)


def ai_play_pokemon_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_PLAY_POKEMON.case(vram=vram, bank=bank, **changes)


def ai_evolution_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_EVOLUTION.case(vram=vram, bank=bank, **changes)


def ai_attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ATTACK.case(vram=vram, bank=bank, **changes)


def ai_attack_score_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ATTACK_SCORE.case(vram=vram, bank=bank, **changes)


def ai_estimate_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ESTIMATE.case(vram=vram, bank=bank, **changes)


def ai_bill_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_BILL.case(vram=vram, bank=bank, **changes)


def ai_ko_switch_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_KO_SWITCH.case(vram=vram, bank=bank, **changes)


def ai_retreat_decision_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_RETREAT_DECISION.case(vram=vram, bank=bank, **changes)


def ai_retreat_switch_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_RETREAT_SWITCH.case(vram=vram, bank=bank, **changes)


def ai_try_retreat_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_TRY_RETREAT.case(vram=vram, bank=bank, **changes)


def npc_execute_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NPC_EXECUTE.case(vram=vram, bank=bank, **changes)


def npc_start_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NPC_START.case(vram=vram, bank=bank, **changes)


def npc_move_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NPC_MOVE.case(vram=vram, bank=bank, **changes)


def power_screen_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return POWER_SCREEN.case(vram=vram, bank=bank, **changes)


def in_play_area_b_exit_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return IN_PLAY_AREA_B_EXIT.case(vram=vram, bank=bank, **changes)


def move_step_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return MOVE_STEP.case(vram=vram, bank=bank, **changes)


def play_area_b_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return PLAY_AREA_B.case(vram=vram, bank=bank, **changes)


def cowardice_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return COWARDICE.case(vram=vram, bank=bank, **changes)


def retreat_stay_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return RETREAT_STAY.case(vram=vram, bank=bank, **changes)
