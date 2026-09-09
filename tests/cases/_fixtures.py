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
        self._load(name, data)

    @classmethod
    def from_capture(cls, data: dict) -> "Fixture":
        """A capture that never touched disk: the sweep's in-memory entries."""
        fixture = cls.__new__(cls)
        fixture._load(data.get("entry", "?"), data)
        return fixture

    def _load(self, name: str, data: dict) -> None:
        self.name = name
        self.ordinal = data["ordinal"]
        self.entry = data["entry"]
        self.regs = data["regs"]
        self.sp = data["sp"]
        self.wram = bytes.fromhex(data["wram"])
        self.hram = bytes.fromhex(data["hram"])
        self.vram = bytes.fromhex(data["vram0"])
        self.sram = bytes.fromhex(data["sram"]) if "sram" in data else None
        self.rom_bank = data.get("rom_bank")

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
        # The mapped ROM bank is the one gambatte had in the $4000-$7FFF window,
        # which a capture records; the probe otherwise forces the routine's own
        # symbol bank and a home routine then reads bank 0 for its caller's data.
        # hBankROM is only the game's shadow of it and can disagree at boot.
        case = {"wram": spans, "entry_sp": self.sp,
                "rom_bank": bank if bank is not None else (self.rom_bank if self.rom_bank is not None else hram[0]),
                "read": {0xC200: 0x200, 0xCC00: 0x100},
                "keys": [0x00, 0x01], "instruction_budget": 40000000, "cycle_budget": 160000000}
        if vram:
            case["vread"] = {0: {0x9800: 0x400}}
        if self.sram is not None:
            # A capture taken with --sram seeds the two save banks against the
            # game's own save. SRAM2/SRAM3 are gfx scratch (sram.asm:370,392)
            # and would push the gbref request past its 64 KB field.
            case["sram"] = {bank: {0xA000: self.sram[bank * 0x2000:(bank + 1) * 0x2000]} for bank in range(2)}
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
# gene-duel at DoFrame 224056: Gene's AI weighs a retreat with a fully powered
# evolution line in hand.
RETREAT_GENE = Fixture("gene-duel-retreat-decision-entry")
RETREAT_GENE_REGS = RETREAT_GENE.regs
# gene-duel at DoFrame 224056: Gene's AI picks an energy for its arena card and
# shuffles the candidates before choosing one.
AI_ENERGY_PLAY = Fixture("gene-duel-ai-energy-entry")
AI_ENERGY_PLAY_REGS = AI_ENERGY_PLAY.regs
AI_ENERGY_SCORING = Fixture("gene-duel-ai-energy-scoring-entry")
AI_ENERGY_SCORING_REGS = AI_ENERGY_SCORING.regs
# gene-duel at DoFrame 224056: the AI's trainer phase 5 (Energy Removal) with
# the player's Machop energised; the ROM decides not to play it.
AI_TRAINER_PHASE5 = Fixture("gene-duel-trainer-phase5-entry")
AI_TRAINER_PHASE5_REGS = AI_TRAINER_PHASE5.regs
# gene-duel at DoFrame 224056: the Energy Removal decision with the player's
# arena Machop energised but short of an attack; the ROM's .default fallback
# inspects the terminal (empty) slot and declines.
ENERGY_REMOVAL = Fixture("gene-duel-energy-removal-entry")
ENERGY_REMOVAL_REGS = ENERGY_REMOVAL.regs
# gene-duel at DoFrame 224056: Gene's arena card above half HP with an
# evolution flagged, so the evolution search runs on the arena deck index.
FULLY_POWERED = Fixture("gene-duel-fully-powered-entry")
FULLY_POWERED_REGS = FULLY_POWERED.regs
# jennifer-duel at DoFrame 259030: Jennifer's bench of three Pikachu, the
# first at full HP with its Raichu in hand, so the set-up count must search
# evolutions by the bench deck index rather than the HP just read.
BENCH_COUNT = Fixture("jennifer-duel-bench-count-entry")
BENCH_COUNT_REGS = BENCH_COUNT.regs
# lightning-2 at DoFrame 310249: Koffing's Foul Gas against the player; the
# ROM's coin lands tails here, so the confusion branch runs.
FOUL_GAS = Fixture("lightning-2-foul-gas-entry")
FOUL_GAS_REGS = FOUL_GAS.regs
# lightning-2 at DoFrame 313096: Weezing's AI weighs Smog against Selfdestruct
# with three energies attached and the player's Machop in the arena.
# lightning-2 at DoFrame 313096: Weezing's AI scores Smog (a=0) and then
# Selfdestruct (a=1) with three energies attached and the player's Machop
# in the arena.
ATTACK_SCORE_SMOG = Fixture("lightning-2-attack-score-smog-entry")
ATTACK_SCORE_SMOG_REGS = ATTACK_SCORE_SMOG.regs
ATTACK_SCORE_SELFDESTRUCT = Fixture("lightning-2-attack-score-selfdestruct-entry")
ATTACK_SCORE_SELFDESTRUCT_REGS = ATTACK_SCORE_SELFDESTRUCT.regs
# lightning-2 at DoFrame 313673: Weezing's Selfdestruct after-damage effect,
# with Weezing at 60 HP and one benched Pokemon on each side.
SELFDESTRUCT = Fixture("lightning-2-selfdestruct-entry")
SELFDESTRUCT_REGS = SELFDESTRUCT.regs
# ai-duel-13 at DoFrame 25772: the AI's Energy Trans check for its second
# attack with a bench but no Venusaur Lv67, so the Venusaur count is the exit.
ENERGY_TRANS = Fixture("ai-duel-13-energy-trans-entry")
ENERGY_TRANS_REGS = ENERGY_TRANS.regs
# ai-duel-13 at DoFrame 28796: after a knockout the AI picks which of its
# three benched Pokemon to bring out.
BENCH_SWITCH = Fixture("ai-duel-13-bench-switch-entry")
BENCH_SWITCH_REGS = BENCH_SWITCH.regs
# ai-duel-1b at DoFrame 25685: Legendary Ronald's whole AI turn, from
# InitAITurnVars through the attack. Professor Oak is not in this hand.
RONALD_TURN = Fixture("ai-duel-1b-turn-entry")
RONALD_TURN_REGS = RONALD_TURN.regs
# boot-deck-machine at DoFrame 91322: the lab PC's Card Album opens on the
# starter collection.
CARD_ALBUM = Fixture("boot-deck-machine-card-album-entry")
CARD_ALBUM_REGS = CARD_ALBUM.regs
# boot-deck-machine at DoFrame 91671: the Evolution file's first page, seven
# rows of owned names and "-------------" placeholders.
CARD_SET_LIST = Fixture("boot-deck-machine-card-set-list-entry")
CARD_SET_LIST_REGS = CARD_SET_LIST.regs
# boot-deck-machine at DoFrame 91672: the first list poll after
# InitCardSelectionParams reset the blink counter; the cursor must appear.
CARD_LIST_SELECT = Fixture("boot-deck-machine-card-list-select-entry")
CARD_LIST_SELECT_REGS = CARD_LIST_SELECT.regs
# boot-deck-machine at DoFrame 96034: the deck save machine prints slot 1, a
# saved starter deck the player cannot build even by dismantling (SRAM seeded).
DECK_ENTRY = Fixture("boot-deck-machine-deck-entry-entry")
DECK_ENTRY_REGS = DECK_ENTRY.regs
# boot-deck-machine at DoFrame 98631: the deck build screen lists the grass
# filter of the player's collection (SRAM seeded).
FILTERED_LIST = Fixture("boot-deck-machine-filtered-list-entry")
FILTERED_LIST_REGS = FILTERED_LIST.regs
# boot-deck-machine at DoFrame 100325: the deck confirmation screen's header,
# with the starter deck loaded and its 60 cards counted (SRAM seeded).
DECK_INFO_HEADER = Fixture("boot-deck-machine-deck-info-header-entry")
DECK_INFO_HEADER_REGS = DECK_INFO_HEADER.regs
# boot-deck-machine at DoFrame 100325: the confirmation list prints the deck's
# 29 unique cards from row 5 at align 3, scroll cursor on the last row.
CONFIRM_LIST = Fixture("boot-deck-machine-confirm-list-entry")
CONFIRM_LIST_REGS = CONFIRM_LIST.regs
# lightning-3 at DoFrame 0: the boot tile copy, 0x38 blocks of 0x10 bytes from
# the caller's banked gfx table into VRAM $9000.
BOOT_GFX = Fixture("lightning-3-boot-gfx-entry")
BOOT_GFX_REGS = BOOT_GFX.regs
# lightning-3 at DoFrame 515: the naming screen builds one full-width font tile
# out of the font bank into wTextTileBuffer.
FONT_TILE = Fixture("lightning-3-font-tile-entry")
FONT_TILE_REGS = FONT_TILE.regs
# lightning-3 at DoFrame 516: the naming screen draws the cursor with the LCD
# on, so WriteByteToBGMap0 stages the byte and hands back a = 0.
NAME_CURSOR = Fixture("lightning-3-name-cursor-entry")
NAME_CURSOR_REGS = NAME_CURSOR.regs
# lightning-3 at DoFrame 593: A is pressed on a keyboard character, so the
# routine transforms it and appends it to wNamingScreenBuffer.
NAME_INPUT = Fixture("lightning-3-name-input-entry")
NAME_INPUT_REGS = NAME_INPUT.regs
# lightning-3 at DoFrame 735: "End" is chosen, so the finished name is copied
# out of wNamingScreenBuffer into the caller's destination buffer.
NAME_FINAL = Fixture("lightning-3-name-final-entry")
NAME_FINAL_REGS = NAME_FINAL.regs
SCROLL_TEXT = Fixture("lightning-3-scroll-text-entry")
SCROLL_TEXT_REGS = SCROLL_TEXT.regs
TITLE_ORB = Fixture("lightning-3-title-orb-entry")
TITLE_ORB_REGS = TITLE_ORB.regs
ADVANCE_TEXT = Fixture("boot-deck-machine-advance-text-entry")
ADVANCE_TEXT_REGS = ADVANCE_TEXT.regs
BUTTON_AB = Fixture("boot-deck-machine-button-ab-entry")
BUTTON_AB_REGS = BUTTON_AB.regs
YES_NO = Fixture("boot-deck-machine-yes-no-entry")
YES_NO_REGS = YES_NO.regs
CARD_LIST_INPUT = Fixture("isaac-duel-card-list-input-entry")
CARD_LIST_INPUT_REGS = CARD_LIST_INPUT.regs
CHECK_CURSOR = Fixture("boot-deck-machine-check-cursor-entry")
CHECK_CURSOR_REGS = CHECK_CURSOR.regs
DM_ENTRIES = Fixture("boot-deck-machine-visible-entries-entry")
DM_ENTRIES_REGS = DM_ENTRIES.regs
HIGH_RECOIL = Fixture("lightning-3-high-recoil-entry")
HIGH_RECOIL_REGS = HIGH_RECOIL.regs
SAND_ATTACK = Fixture("lightning-3-sand-attack-entry")
SAND_ATTACK_REGS = SAND_ATTACK.regs
DAMAGE_REDUCTION = Fixture("lightning-3-damage-reduction-entry")
DAMAGE_REDUCTION_REGS = DAMAGE_REDUCTION.regs
AI_PKMN_POWERS = Fixture("lightning-3-ai-pkmn-powers-entry")
AI_PKMN_POWERS_REGS = AI_PKMN_POWERS.regs
ZAPDOS_RECOIL = Fixture("lightning-3-zapdos-recoil-entry")
ZAPDOS_RECOIL_REGS = ZAPDOS_RECOIL.regs
MAP_SCRIPT = Fixture("lightning-3-map-script-entry")
MAP_SCRIPT_REGS = MAP_SCRIPT.regs
SPECIAL_ATTACK = Fixture("water-master-special-attack-entry")
SPECIAL_ATTACK_REGS = SPECIAL_ATTACK.regs
SCROLL_LABEL = Fixture("lightning-3-scroll-label-entry")
SCROLL_LABEL_REGS = SCROLL_LABEL.regs
WAIT_KEYS = Fixture("boot-deck-machine-wait-keys-entry")
WAIT_KEYS_REGS = WAIT_KEYS.regs



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


def retreat_gene_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return RETREAT_GENE.case(vram=vram, bank=bank, **changes)


def ai_energy_play_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ENERGY_PLAY.case(vram=vram, bank=bank, **changes)


def ai_energy_scoring_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ENERGY_SCORING.case(vram=vram, bank=bank, **changes)


def ai_trainer_phase5_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_TRAINER_PHASE5.case(vram=vram, bank=bank, **changes)


def energy_removal_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ENERGY_REMOVAL.case(vram=vram, bank=bank, **changes)


def fully_powered_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return FULLY_POWERED.case(vram=vram, bank=bank, **changes)


def bench_count_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return BENCH_COUNT.case(vram=vram, bank=bank, **changes)


def foul_gas_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return FOUL_GAS.case(vram=vram, bank=bank, **changes)


def attack_score_smog_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ATTACK_SCORE_SMOG.case(vram=vram, bank=bank, **changes)


def attack_score_selfdestruct_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ATTACK_SCORE_SELFDESTRUCT.case(vram=vram, bank=bank, **changes)


def selfdestruct_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return SELFDESTRUCT.case(vram=vram, bank=bank, **changes)


def energy_trans_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ENERGY_TRANS.case(vram=vram, bank=bank, **changes)


def bench_switch_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return BENCH_SWITCH.case(vram=vram, bank=bank, **changes)


def ronald_turn_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return RONALD_TURN.case(vram=vram, bank=bank, **changes)


def card_album_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CARD_ALBUM.case(vram=vram, bank=bank, **changes)


def card_set_list_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CARD_SET_LIST.case(vram=vram, bank=bank, **changes)


def card_list_select_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CARD_LIST_SELECT.case(vram=vram, bank=bank, **changes)


def deck_entry_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DECK_ENTRY.case(vram=vram, bank=bank, **changes)


def filtered_list_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return FILTERED_LIST.case(vram=vram, bank=bank, **changes)


def deck_info_header_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DECK_INFO_HEADER.case(vram=vram, bank=bank, **changes)


def confirm_list_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CONFIRM_LIST.case(vram=vram, bank=bank, **changes)


def boot_gfx_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return BOOT_GFX.case(vram=vram, bank=bank, **changes)


def font_tile_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return FONT_TILE.case(vram=vram, bank=bank, **changes)


def name_cursor_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NAME_CURSOR.case(vram=vram, bank=bank, **changes)


def name_input_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NAME_INPUT.case(vram=vram, bank=bank, **changes)


def name_final_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NAME_FINAL.case(vram=vram, bank=bank, **changes)


def scroll_text_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return SCROLL_TEXT.case(vram=vram, bank=bank, **changes)


def title_orb_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return TITLE_ORB.case(vram=vram, bank=bank, **changes)


def advance_text_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ADVANCE_TEXT.case(vram=vram, bank=bank, **changes)


def button_ab_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return BUTTON_AB.case(vram=vram, bank=bank, **changes)


def yes_no_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return YES_NO.case(vram=vram, bank=bank, **changes)


def card_list_input_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CARD_LIST_INPUT.case(vram=vram, bank=bank, **changes)


def check_cursor_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CHECK_CURSOR.case(vram=vram, bank=bank, **changes)


def dm_entries_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DM_ENTRIES.case(vram=vram, bank=bank, **changes)


def high_recoil_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return HIGH_RECOIL.case(vram=vram, bank=bank, **changes)


def sand_attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return SAND_ATTACK.case(vram=vram, bank=bank, **changes)


def damage_reduction_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DAMAGE_REDUCTION.case(vram=vram, bank=bank, **changes)


def ai_pkmn_powers_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_PKMN_POWERS.case(vram=vram, bank=bank, **changes)


def zapdos_recoil_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ZAPDOS_RECOIL.case(vram=vram, bank=bank, **changes)


def map_script_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return MAP_SCRIPT.case(vram=vram, bank=bank, **changes)


def special_attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return SPECIAL_ATTACK.case(vram=vram, bank=bank, **changes)


def scroll_label_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return SCROLL_LABEL.case(vram=vram, bank=bank, **changes)


def wait_keys_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return WAIT_KEYS.case(vram=vram, bank=bank, **changes)


PKMN_POWER = Fixture("water-2-pkmnpower-entry")
PKMN_POWER_REGS = PKMN_POWER.regs


def pkmn_power_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return PKMN_POWER.case(vram=vram, bank=bank, **changes)


NPC_COORDS = Fixture("water-master-npc-coords-entry")
NPC_COORDS_REGS = NPC_COORDS.regs


def npc_coords_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return NPC_COORDS.case(vram=vram, bank=bank, **changes)


ENERGY_SEARCH = Fixture("grass-club-energy-search-entry")
ENERGY_SEARCH_REGS = ENERGY_SEARCH.regs


def energy_search_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ENERGY_SEARCH.case(vram=vram, bank=bank, **changes)


PROFESSOR_OAK = Fixture("psychic-club-professor-oak-entry")
PROFESSOR_OAK_REGS = PROFESSOR_OAK.regs


def professor_oak_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return PROFESSOR_OAK.case(vram=vram, bank=bank, **changes)


GRASS_RETREAT = Fixture("grass-club-retreat-entry")
GRASS_RETREAT_REGS = GRASS_RETREAT.regs


def grass_retreat_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return GRASS_RETREAT.case(vram=vram, bank=bank, **changes)


GRASS_RETREAT_2 = Fixture("grass-club-retreat-entry-2")
GRASS_RETREAT_2_REGS = GRASS_RETREAT_2.regs


def grass_retreat_2_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return GRASS_RETREAT_2.case(vram=vram, bank=bank, **changes)


AI_DUEL_RETREAT = Fixture("ai-duel-12-retreat-entry")
AI_DUEL_RETREAT_REGS = AI_DUEL_RETREAT.regs


def ai_duel_retreat_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_DUEL_RETREAT.case(vram=vram, bank=bank, **changes)


BEGIN_USE_ATTACK = Fixture("psychic-club-begin-use-attack-entry")
BEGIN_USE_ATTACK_REGS = BEGIN_USE_ATTACK.regs


def begin_use_attack_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return BEGIN_USE_ATTACK.case(vram=vram, bank=bank, **changes)


AI_GUST_OF_WIND = Fixture("ai-duel-19-gust-of-wind-entry")
AI_GUST_OF_WIND_REGS = AI_GUST_OF_WIND.regs


def ai_gust_of_wind_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_GUST_OF_WIND.case(vram=vram, bank=bank, **changes)


AI_ENERGY_RETRIEVAL = Fixture("ai-duel-2d-energy-retrieval-entry")
AI_ENERGY_RETRIEVAL_REGS = AI_ENERGY_RETRIEVAL.regs


def ai_energy_retrieval_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_ENERGY_RETRIEVAL.case(vram=vram, bank=bank, **changes)


AI_POWER_EFFECT = Fixture("ai-duel-24-power-effect-entry")
AI_POWER_EFFECT_REGS = AI_POWER_EFFECT.regs


def ai_power_effect_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return AI_POWER_EFFECT.case(vram=vram, bank=bank, **changes)


DOME_RONALD = Fixture("ronald-3-dome-ronald-entry")
DOME_RONALD_REGS = DOME_RONALD.regs


def dome_ronald_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DOME_RONALD.case(vram=vram, bank=bank, **changes)


CLERK9 = Fixture("challenge-hall-clerk9-entry")
CLERK9_REGS = CLERK9.regs


def clerk9_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CLERK9.case(vram=vram, bank=bank, **changes)


DOME_LOAD_MAP = Fixture("dome-1-load-map-entry")
DOME_LOAD_MAP_REGS = DOME_LOAD_MAP.regs


def dome_load_map_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DOME_LOAD_MAP.case(vram=vram, bank=bank, **changes)


DOME_AFTER_DUEL = Fixture("dome-1-after-duel-entry")
DOME_AFTER_DUEL_REGS = DOME_AFTER_DUEL.regs


def dome_after_duel_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return DOME_AFTER_DUEL.case(vram=vram, bank=bank, **changes)


PEAL_OF_THUNDER = Fixture("dome-2-peal-of-thunder-entry")
PEAL_OF_THUNDER_REGS = PEAL_OF_THUNDER.regs


def peal_of_thunder_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return PEAL_OF_THUNDER.case(vram=vram, bank=bank, **changes)


BENCH_HALF_HP = Fixture("dome-3-bench-half-hp-entry")
BENCH_HALF_HP_REGS = BENCH_HALF_HP.regs


def bench_half_hp_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return BENCH_HALF_HP.case(vram=vram, bank=bank, **changes)


ARTICUNO_TURN = Fixture("dome-3-articuno-turn-entry")
ARTICUNO_TURN_REGS = ARTICUNO_TURN.regs


def articuno_turn_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ARTICUNO_TURN.case(vram=vram, bank=bank, **changes)


ARTICUNO_SCORING = Fixture("dome-3-articuno-scoring-entry")
ARTICUNO_SCORING_REGS = ARTICUNO_SCORING.regs


def articuno_scoring_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return ARTICUNO_SCORING.case(vram=vram, bank=bank, **changes)


CREDITS_SCROLL_TABLE = Fixture("credits-1-scroll-table-entry")
CREDITS_SCROLL_TABLE_REGS = CREDITS_SCROLL_TABLE.regs


def credits_scroll_table_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return CREDITS_SCROLL_TABLE.case(vram=vram, bank=bank, **changes)


SPECIAL_ATTACK_PARAMS = Fixture("challenge-hall-special-attack-params-entry")
SPECIAL_ATTACK_PARAMS_REGS = SPECIAL_ATTACK_PARAMS.regs


def special_attack_params_fixture(vram: bool = True, bank: int | None = None, **changes: bytes) -> dict:
    return SPECIAL_ATTACK_PARAMS.case(vram=vram, bank=bank, **changes)
