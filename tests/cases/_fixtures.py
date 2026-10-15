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
import os
from pathlib import Path

from tests.cases._symbols import CALL_FRAME, HRAM_START, SRAM_START, STACK_WINDOW, WRAM_START, WRAMX_START, card_id_size, card_max_hp, frame_callback_pointer, profile_symbols, sym

# Bytes the two reference lanes cannot agree on with the native lane, left
# unseeded and uncompared. wIE ($CAB7) mirrors rIE, which each lane arms for
# itself. wVBlankCounter ($CAB8), wCursorBlinkCounter ($CD0F) and
# wCheckMenuCursorBlinkCounter ($CEA3) count frames spent in key waits, which
# the PyBoy lane runs many DoFrames per tick (it skips the VBlank halt).
# wFlushPaletteFlags ($CABF) and wVBlankOAMCopyToggle ($CAC0) are consumed by
# the VBlank ISR. Do not widen this for a byte the game computes.
# $CFF0-$CFF5 and $DC30-$DCFF are the PyBoy oracle's synthesized call frame
# (tools/oracle/pyboy_oracle.py RESERVED); $DD80+ is the sound driver's.
_HOLES = tuple(sym(name) for name in (
    "wIE", "wVBlankCounter", "wFlushPaletteFlags", "wVBlankOAMCopyToggle",
    "wCursorBlinkCounter", "wCheckMenuCursorBlinkCounter"))

_ROOT = Path(__file__).resolve().parents[2]
_PROFILE_CATALOG = json.loads((_ROOT / "profiles" / "profiles.json").read_text())
_DEFAULT_PROFILE = _PROFILE_CATALOG["default"]


def _source_profile(directory: Path | None) -> str:
    if directory is None:
        return _DEFAULT_PROFILE
    try:
        parts = directory.resolve().relative_to(_ROOT).parts
    except ValueError:
        return _DEFAULT_PROFILE
    if len(parts) >= 4 and parts[:2] == ("tests", "profiles") and parts[3] == "fixtures":
        return parts[2]
    return _DEFAULT_PROFILE


def _cut(start: int, end: int, holes: tuple[int, ...]) -> list[tuple[int, int]]:
    pieces = []
    cursor = start
    for hole in sorted(holes):
        if start <= hole < end:
            pieces.append((cursor, hole))
            cursor = hole + 1
    pieces.append((cursor, end))
    return pieces


def _without(start: int, end: int, window: range) -> tuple[tuple[int, int], ...]:
    return tuple((a, b) for a, b in ((start, min(end, window.start)), (max(start, window.stop), end)) if a < b)


_SPANS = ((WRAM_START, CALL_FRAME.start), *_without(WRAMX_START, sym("wCurSongID"), STACK_WINDOW))
# The joypad snapshot hDPadRepeat..hKeysPressed ($FF8D-$FF91) is the `keys`
# timeline as each lane injects it: the probe advances it per completed poll,
# PyBoy per frame, so a routine that polls inside its own DoFrame loop
# (ExecuteNPCMovement) exits on different entries. The game state the polls
# drove is compared through WRAM; the snapshot itself is not.
_HRAM_HOLES = tuple(sym(name) for name in ("hDPadRepeat", "hKeysReleased", "hDPadHeld", "hKeysHeld", "hKeysPressed"))


class Fixture:
    """One captured state (`session.py capture NAME --routine R`) as a case
    builder: `Fixture("practice-win-attack-entry").case({sym("wOpponentArenaCardHP"): b"\\x00"})`."""

    def __init__(self, name: str, directory: Path | None = None, holes: tuple[int, ...] = _HOLES,
                 lcdc: int | None = None):
        folder = directory if directory is not None else Path(__file__).resolve().parent.parent / "fixtures"
        self.source_profile = _source_profile(directory)
        self.source_variant = None
        with (folder / f"{name}.json").open() as stream:
            data = json.load(stream)
        self._load(name, data)
        self.holes = holes
        self.lcdc = sym("wLCDC") if lcdc is None else lcdc

    @classmethod
    def from_capture(cls, data: dict) -> "Fixture":
        """A capture that never touched disk: the sweep's in-memory entries."""
        fixture = cls.__new__(cls)
        fixture._load(data.get("entry", "?"), data)
        fixture.source_profile = os.environ.get("POKETCG_PROFILE") or _DEFAULT_PROFILE
        fixture.source_variant = os.environ.get("POKETCG_PROFILE_VARIANT")
        fixture.holes = _HOLES
        fixture.lcdc = sym("wLCDC")
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

    def case(self, changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
             **named: bytes) -> dict:
        """The captured state with `changes` ({address: bytes}, or hex-string
        keywords such as C3C8=b"...") patched in, as a case body. `vram=False` leaves VRAM unseeded and
        uncompared, for a routine that returns mid-frame: the gbref lane's PPU
        answers $FF to a VRAM read during mode 3. `bank` seeds hBankROM for a
        banked routine: the reference leaves the routine's own bank selected at
        its `ret` and the probe's bank guard restores the entry value, so
        seeding the routine's bank is the one value both lanes exit with. A home
        routine keeps the captured value; PyBoy needs the shadow consistent
        with the mapped bank or the first bank restore maps garbage."""
        wram = bytearray(self.wram)
        hram = bytearray(self.hram)
        patches = dict(changes or {})
        patches.update((int(address, 16), data) for address, data in named.items())
        source_callback = profile_symbols(self.source_profile).get("wDoFrameFunction")
        target_callback = sym("wDoFrameFunction")
        if source_callback is not None and target_callback not in patches:
            source_address = source_callback[1]
            if source_address != target_callback:
                raise ValueError(f"{self.name} moves wDoFrameFunction from {source_address:04X} to {target_callback:04X}")
            offset = source_address - WRAM_START
            value = self.wram[offset:offset + 2]
            if len(value) == 2:
                pointer = frame_callback_pointer(int.from_bytes(value, "little"), self.source_profile,
                                                 self.rom_bank, self.source_variant)
                if pointer != value:
                    patches[target_callback] = pointer
        for address, data in patches.items():
            if address >= HRAM_START:
                hram[address - HRAM_START:address - HRAM_START + len(data)] = data
            else:
                wram[address - WRAM_START:address - WRAM_START + len(data)] = data
        if bank is not None:
            hram[0] = bank
        spans = {}
        for start, end in _SPANS:
            for piece, stop in _cut(start, end, self.holes):
                spans[piece] = bytes(wram[piece - WRAM_START:stop - WRAM_START])
        # $FFB8-$FFFE is the unused HRAM tail (hram.asm `ds $38`); the gbref
        # runner's setup calls run on a stack up there.
        cursor = HRAM_START
        for hole in _HRAM_HOLES:
            spans[cursor] = bytes(hram[cursor - HRAM_START:hole - HRAM_START])
            cursor = hole + 1
        spans[cursor] = bytes(hram[cursor - HRAM_START:0x38])
        if vram:
            spans[0x8000] = self.vram
        # rLCDC from the game's own wLCDC mirror: the gbref lane runs a real PPU,
        # and with the LCD off its first `halt` would wait for a VBlank forever.
        spans[0xFF40] = bytes([self.wram[self.lcdc - WRAM_START]])
        # The game's own SP: the gbref lane otherwise parks the stack at $FFFE, and
        # a deep call plus real interrupt frames would grow it down through
        # hKeysHeld and the rest of HRAM.
        # The mapped ROM bank is the one gambatte had in the $4000-$7FFF window,
        # which a capture records; the probe otherwise forces the routine's own
        # symbol bank and a home routine then reads bank 0 for its caller's data.
        # hBankROM is only the game's shadow of it and can disagree at boot.
        reads = {}
        for name, length in (("wPlayerDuelVariables", 0x200), ("wPracticeDuelTurn", 0x100)):
            start = sym(name)
            reads.update((piece, stop - piece) for piece, stop in _cut(start, start + length, self.holes) if stop > piece)
        case = {"wram": spans, "entry_sp": self.sp,
                "rom_bank": bank if bank is not None else (self.rom_bank if self.rom_bank is not None else hram[0]),
                "read": reads,
                "keys": [0x00, 0x01], "instruction_budget": 40000000, "cycle_budget": 160000000}
        if vram:
            case["vread"] = {0: {0x9800: 0x400}}
        if self.sram is not None:
            # A capture taken with --sram seeds the two save banks against the
            # game's own save. SRAM2/SRAM3 are gfx scratch (sram.asm:370,392)
            # and would push the gbref request past its 64 KB field.
            case["sram"] = {bank: {SRAM_START: self.sram[bank * 0x2000:(bank + 1) * 0x2000]} for bank in range(2)}
        return case

def profile_fixture(names: dict[str, str], *, holes: tuple[int, ...] = _HOLES,
                    lcdc: int | None = None) -> Fixture:
    profile = os.environ.get("POKETCG_PROFILE") or _DEFAULT_PROFILE
    name = names.get(profile, names[_DEFAULT_PROFILE])
    case_namespace = _PROFILE_CATALOG["profiles"][profile]["evidence"]["case_namespace"]
    profile_directory = _ROOT / Path(case_namespace).parent / "fixtures"
    directory = (
        profile_directory
        if (profile_directory / f"{name}.json").is_file()
        else _ROOT / "tests" / "fixtures"
    )
    return Fixture(name, directory=directory, holes=holes, lcdc=lcdc)


ATTACK = profile_fixture({
    "vanilla": "practice-win-attack-entry",
    "extended": "practice-horn-attack-entry",
})
ATTACK_REGS = ATTACK.regs
OPEN_CARD_PAGE_CHECK_PLAY_AREA = profile_fixture({
    "vanilla": "practice-win-attack-entry",
    "extended": "practice-horn-attack-open-card-page-check-play-area-entry",
})


def open_card_page_check_play_area_fixture(changes: dict[int, bytes] | None = None,
                                          vram: bool = True, bank: int | None = None,
                                          **named: bytes) -> dict:
    return OPEN_CARD_PAGE_CHECK_PLAY_AREA.case(changes, vram=vram, bank=bank, **named)


# Func_c141's entry after the practice duel: wActiveGameEvent = GAME_EVENT_DUEL,
# Dr. Mason's lab loaded, Sam's after-duel script about to be dispatched.
AFTER_DUEL = profile_fixture({
    "vanilla": "practice-win-after-duel-entry",
    "extended": "starter-deck-after-duel-entry",
})
AFTER_DUEL_REGS = AFTER_DUEL.regs
# Func_c9b8's entry at the game's start: wCurMap = OVERWORLD_MAP, so the
# LOAD_MAP slot is LoadOverworld (Func_d4fb, then Script_BeginGame).
LOAD_MAP = profile_fixture({
    "vanilla": "practice-win-load-map-entry",
    "extended": "starter-deck-load-map-entry",
})
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
AI_PLAY_POKEMON = profile_fixture({
    "vanilla": "ai-duel-02-play-pokemon-entry",
    "extended": "ai-duel-fire-charge-aidecideplaypokemoncard-entry",
})
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
AI_ESTIMATE = profile_fixture({
    "vanilla": "ai-duel-02-estimate-entry",
    "extended": "ai-duel-fire-charge-ai-estimate-entry",
})
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
NPC_EXECUTE = profile_fixture({
    "vanilla": "ai-duel-02-npc-execute-entry",
    "extended": "starter-deck-npc-execute-entry",
})
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
MOVE_STEP = profile_fixture({
    "vanilla": "fighting-club-move-step-entry",
    "extended": "multi-bank-scripts-move-step-entry",
})
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
ENERGY_REMOVAL = profile_fixture({
    "vanilla": "gene-duel-energy-removal-entry",
    "extended": "ai-duel-fighting-carriers-energy-removal-entry",
})
ENERGY_REMOVAL_REGS = ENERGY_REMOVAL.regs
# gene-duel at DoFrame 224056: Gene's arena card above half HP with an
# evolution flagged, so the evolution search runs on the arena deck index.
FULLY_POWERED = Fixture("gene-duel-fully-powered-entry")
FULLY_POWERED_REGS = FULLY_POWERED.regs
# jennifer-duel at DoFrame 259030: Jennifer's bench of three Pikachu, the
# first at full HP with its Raichu in hand, so the set-up count must search
# evolutions by the bench deck index rather than the HP just read.
BENCH_COUNT = profile_fixture({
    "vanilla": "jennifer-duel-bench-count-entry",
    "extended": "ai-duel-fire-charge-bench-count-entry",
})
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
FULL_HEAL_TRAINER = Fixture("full-heal-trainer-entry")
FULL_HEAL_TRAINER_REGS = FULL_HEAL_TRAINER.regs
DECK_ENTRY = Fixture("boot-deck-machine-deck-entry-entry")
DECK_ENTRY_REGS = DECK_ENTRY.regs
# boot-deck-machine at DoFrame 98631: the deck build screen lists the grass
# filter of the player's collection (SRAM seeded).
FILTERED_LIST = Fixture("boot-deck-machine-filtered-list-entry")
FILTERED_LIST_REGS = FILTERED_LIST.regs
# boot-deck-machine at DoFrame 100325: the deck confirmation screen's header,
# with the starter deck loaded and its 60 cards counted (SRAM seeded).
DECK_INFO_HEADER = profile_fixture({
    "vanilla": "boot-deck-machine-deck-info-header-entry",
    "extended": "deck-confirmation-showdeckinfoheader-entry",
})
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
SCROLL_TEXT = profile_fixture({
    "vanilla": "lightning-3-scroll-text-entry",
    "extended": "practice-menu-scroll-text-entry",
})
SCROLL_TEXT_REGS = SCROLL_TEXT.regs
TITLE_ORB = Fixture("lightning-3-title-orb-entry")
TITLE_ORB_REGS = TITLE_ORB.regs
ADVANCE_TEXT = profile_fixture({
    "vanilla": "boot-deck-machine-advance-text-entry",
    "extended": "practice-menu-advance-text-entry",
})
ADVANCE_TEXT_REGS = ADVANCE_TEXT.regs
BUTTON_AB = profile_fixture({
    "vanilla": "boot-deck-machine-button-ab-entry",
    "extended": "practice-menu-button-ab-entry",
})
BUTTON_AB_REGS = BUTTON_AB.regs
YES_NO = profile_fixture({
    "vanilla": "boot-deck-machine-yes-no-entry",
    "extended": "practice-menu-yes-no-entry",
})
YES_NO_REGS = YES_NO.regs
CARD_LIST_INPUT = Fixture("isaac-duel-card-list-input-entry")
CARD_LIST_INPUT_REGS = CARD_LIST_INPUT.regs
CHECK_CURSOR = Fixture("boot-deck-machine-check-cursor-entry")
CHECK_CURSOR_REGS = CHECK_CURSOR.regs
DM_ENTRIES = profile_fixture({
    "vanilla": "boot-deck-machine-visible-entries-entry",
    "extended": "deck-ui-visible-deck-machine-entries-entry",
})
DM_ENTRIES_REGS = DM_ENTRIES.regs
HIGH_RECOIL = Fixture("lightning-3-high-recoil-entry")
HIGH_RECOIL_REGS = HIGH_RECOIL.regs
SAND_ATTACK = profile_fixture({
    "vanilla": "lightning-3-sand-attack-entry",
    "extended": "practice-horn-attack-entry",
})
SAND_ATTACK_REGS = SAND_ATTACK.regs
DAMAGE_REDUCTION = Fixture("lightning-3-damage-reduction-entry")
DAMAGE_REDUCTION_REGS = DAMAGE_REDUCTION.regs
AI_PKMN_POWERS = profile_fixture({
    "vanilla": "lightning-3-ai-pkmn-powers-entry",
    "extended": "ai-heal-carrier-pkmn-powers-handler-entry",
})
AI_PKMN_POWERS_REGS = AI_PKMN_POWERS.regs
ZAPDOS_RECOIL = Fixture("lightning-3-zapdos-recoil-entry")
ZAPDOS_RECOIL_REGS = ZAPDOS_RECOIL.regs
MAP_SCRIPT = Fixture("lightning-3-map-script-entry")
MAP_SCRIPT_REGS = MAP_SCRIPT.regs
SPECIAL_ATTACK = Fixture("water-master-special-attack-entry")
SPECIAL_ATTACK_REGS = SPECIAL_ATTACK.regs
SCROLL_LABEL = profile_fixture({
    "vanilla": "lightning-3-scroll-label-entry",
    "extended": "practice-menu-scroll-label-entry",
})
SCROLL_LABEL_REGS = SCROLL_LABEL.regs
WAIT_KEYS = profile_fixture({
    "vanilla": "boot-deck-machine-wait-keys-entry",
    "extended": "status-screen-wait-keys-entry",
})
WAIT_KEYS_REGS = WAIT_KEYS.regs
FIND_NPC = profile_fixture({
    "vanilla": "water-club-findnpc-entry",
    "extended": "multi-bank-scripts-find-npc-entry",
})
FIND_NPC_REGS = FIND_NPC.regs
TEXT_TILE = Fixture("water-master-placenexttexttile-entry")
TEXT_TILE_REGS = TEXT_TILE.regs
HALF_WIDTH_END = Fixture("grass-club-terminate-halfwidth-entry")
HALF_WIDTH_END_REGS = HALF_WIDTH_END.regs
MAP_WARP = Fixture("ronald-1-handlemapwarp-entry")
MAP_WARP_REGS = MAP_WARP.regs



def attack_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                   **named: bytes) -> dict:
    return ATTACK.case(changes, vram=vram, bank=bank, **named)


def after_duel_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return AFTER_DUEL.case(changes, vram=vram, bank=bank, **named)


def load_map_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                     **named: bytes) -> dict:
    return LOAD_MAP.case(changes, vram=vram, bank=bank, **named)


def ai_energy_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return AI_ENERGY.case(changes, vram=vram, bank=bank, **named)


def ai_defending_ko_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return AI_DEFENDING_KO.case(changes, vram=vram, bank=bank, **named)


def ai_try_energy_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return AI_TRY_ENERGY.case(changes, vram=vram, bank=bank, **named)


def ai_evolution_energy_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return AI_EVOLUTION_ENERGY.case(changes, vram=vram, bank=bank, **named)


def ai_play_pokemon_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return AI_PLAY_POKEMON.case(changes, vram=vram, bank=bank, **named)


def ai_evolution_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return AI_EVOLUTION.case(changes, vram=vram, bank=bank, **named)


def ai_attack_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return AI_ATTACK.case(changes, vram=vram, bank=bank, **named)


def ai_attack_score_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return AI_ATTACK_SCORE.case(changes, vram=vram, bank=bank, **named)


def ai_estimate_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return AI_ESTIMATE.case(changes, vram=vram, bank=bank, **named)


def ai_bill_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                    **named: bytes) -> dict:
    return AI_BILL.case(changes, vram=vram, bank=bank, **named)


def ai_ko_switch_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return AI_KO_SWITCH.case(changes, vram=vram, bank=bank, **named)


def ai_retreat_decision_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return AI_RETREAT_DECISION.case(changes, vram=vram, bank=bank, **named)


def ai_retreat_switch_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return AI_RETREAT_SWITCH.case(changes, vram=vram, bank=bank, **named)


def ai_try_retreat_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return AI_TRY_RETREAT.case(changes, vram=vram, bank=bank, **named)


def npc_execute_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return NPC_EXECUTE.case(changes, vram=vram, bank=bank, **named)


def npc_start_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return NPC_START.case(changes, vram=vram, bank=bank, **named)


def npc_move_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                     **named: bytes) -> dict:
    return NPC_MOVE.case(changes, vram=vram, bank=bank, **named)


def power_screen_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return POWER_SCREEN.case(changes, vram=vram, bank=bank, **named)


def in_play_area_b_exit_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return IN_PLAY_AREA_B_EXIT.case(changes, vram=vram, bank=bank, **named)


def move_step_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return MOVE_STEP.case(changes, vram=vram, bank=bank, **named)


def play_area_b_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return PLAY_AREA_B.case(changes, vram=vram, bank=bank, **named)


def cowardice_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return COWARDICE.case(changes, vram=vram, bank=bank, **named)


def retreat_stay_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return RETREAT_STAY.case(changes, vram=vram, bank=bank, **named)


def retreat_gene_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return RETREAT_GENE.case(changes, vram=vram, bank=bank, **named)


def ai_energy_play_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return AI_ENERGY_PLAY.case(changes, vram=vram, bank=bank, **named)


def ai_energy_scoring_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return AI_ENERGY_SCORING.case(changes, vram=vram, bank=bank, **named)


def ai_trainer_phase5_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return AI_TRAINER_PHASE5.case(changes, vram=vram, bank=bank, **named)


def energy_removal_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return ENERGY_REMOVAL.case(changes, vram=vram, bank=bank, **named)


def fully_powered_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return FULLY_POWERED.case(changes, vram=vram, bank=bank, **named)


def bench_count_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return BENCH_COUNT.case(changes, vram=vram, bank=bank, **named)


def foul_gas_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                     **named: bytes) -> dict:
    return FOUL_GAS.case(changes, vram=vram, bank=bank, **named)


def attack_score_smog_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return ATTACK_SCORE_SMOG.case(changes, vram=vram, bank=bank, **named)


def attack_score_selfdestruct_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                      **named: bytes) -> dict:
    return ATTACK_SCORE_SELFDESTRUCT.case(changes, vram=vram, bank=bank, **named)


def selfdestruct_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return SELFDESTRUCT.case(changes, vram=vram, bank=bank, **named)


def energy_trans_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return ENERGY_TRANS.case(changes, vram=vram, bank=bank, **named)


def bench_switch_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return BENCH_SWITCH.case(changes, vram=vram, bank=bank, **named)


def ronald_turn_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return RONALD_TURN.case(changes, vram=vram, bank=bank, **named)


def card_album_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return CARD_ALBUM.case(changes, vram=vram, bank=bank, **named)


def card_set_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return CARD_SET_LIST.case(changes, vram=vram, bank=bank, **named)


def card_list_select_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return CARD_LIST_SELECT.case(changes, vram=vram, bank=bank, **named)


def full_heal_trainer_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return FULL_HEAL_TRAINER.case(changes, vram=vram, bank=bank, **named)


def deck_entry_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return DECK_ENTRY.case(changes, vram=vram, bank=bank, **named)


def filtered_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return FILTERED_LIST.case(changes, vram=vram, bank=bank, **named)


def deck_info_header_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return DECK_INFO_HEADER.case(changes, vram=vram, bank=bank, **named)


def confirm_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return CONFIRM_LIST.case(changes, vram=vram, bank=bank, **named)


def boot_gfx_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                     **named: bytes) -> dict:
    return BOOT_GFX.case(changes, vram=vram, bank=bank, **named)


def font_tile_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return FONT_TILE.case(changes, vram=vram, bank=bank, **named)


def name_cursor_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return NAME_CURSOR.case(changes, vram=vram, bank=bank, **named)


def name_input_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return NAME_INPUT.case(changes, vram=vram, bank=bank, **named)


def name_final_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return NAME_FINAL.case(changes, vram=vram, bank=bank, **named)


def scroll_text_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return SCROLL_TEXT.case(changes, vram=vram, bank=bank, **named)


def title_orb_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return TITLE_ORB.case(changes, vram=vram, bank=bank, **named)


def advance_text_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return ADVANCE_TEXT.case(changes, vram=vram, bank=bank, **named)


def button_ab_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return BUTTON_AB.case(changes, vram=vram, bank=bank, **named)


def yes_no_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                   **named: bytes) -> dict:
    return YES_NO.case(changes, vram=vram, bank=bank, **named)


def card_list_input_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return CARD_LIST_INPUT.case(changes, vram=vram, bank=bank, **named)


def check_cursor_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return CHECK_CURSOR.case(changes, vram=vram, bank=bank, **named)


def dm_entries_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return DM_ENTRIES.case(changes, vram=vram, bank=bank, **named)


def high_recoil_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return HIGH_RECOIL.case(changes, vram=vram, bank=bank, **named)


def sand_attack_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return SAND_ATTACK.case(changes, vram=vram, bank=bank, **named)


def damage_reduction_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return DAMAGE_REDUCTION.case(changes, vram=vram, bank=bank, **named)


def ai_pkmn_powers_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return AI_PKMN_POWERS.case(changes, vram=vram, bank=bank, **named)


def zapdos_recoil_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return ZAPDOS_RECOIL.case(changes, vram=vram, bank=bank, **named)


def map_script_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return MAP_SCRIPT.case(changes, vram=vram, bank=bank, **named)


def special_attack_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return SPECIAL_ATTACK.case(changes, vram=vram, bank=bank, **named)


def scroll_label_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return SCROLL_LABEL.case(changes, vram=vram, bank=bank, **named)


def wait_keys_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return WAIT_KEYS.case(changes, vram=vram, bank=bank, **named)


def find_npc_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                     **named: bytes) -> dict:
    return FIND_NPC.case(changes, vram=vram, bank=bank, **named)


def text_tile_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                      **named: bytes) -> dict:
    return TEXT_TILE.case(changes, vram=vram, bank=bank, **named)


def half_width_end_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return HALF_WIDTH_END.case(changes, vram=vram, bank=bank, **named)


def map_warp_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                     **named: bytes) -> dict:
    return MAP_WARP.case(changes, vram=vram, bank=bank, **named)


PKMN_POWER = Fixture("water-2-pkmnpower-entry")
PKMN_POWER_REGS = PKMN_POWER.regs


def pkmn_power_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return PKMN_POWER.case(changes, vram=vram, bank=bank, **named)


NPC_COORDS = Fixture("water-master-npc-coords-entry")
NPC_COORDS_REGS = NPC_COORDS.regs


def npc_coords_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return NPC_COORDS.case(changes, vram=vram, bank=bank, **named)


ENERGY_SEARCH = Fixture("grass-club-energy-search-entry")
ENERGY_SEARCH_REGS = ENERGY_SEARCH.regs


def energy_search_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return ENERGY_SEARCH.case(changes, vram=vram, bank=bank, **named)


PROFESSOR_OAK = Fixture("psychic-club-professor-oak-entry")
PROFESSOR_OAK_REGS = PROFESSOR_OAK.regs


def professor_oak_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return PROFESSOR_OAK.case(changes, vram=vram, bank=bank, **named)


GRASS_RETREAT = Fixture("grass-club-retreat-entry")
GRASS_RETREAT_REGS = GRASS_RETREAT.regs


def grass_retreat_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return GRASS_RETREAT.case(changes, vram=vram, bank=bank, **named)


GRASS_RETREAT_2 = Fixture("grass-club-retreat-entry-2")
GRASS_RETREAT_2_REGS = GRASS_RETREAT_2.regs


def grass_retreat_2_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return GRASS_RETREAT_2.case(changes, vram=vram, bank=bank, **named)


AI_DUEL_RETREAT = Fixture("ai-duel-12-retreat-entry")
AI_DUEL_RETREAT_REGS = AI_DUEL_RETREAT.regs


def ai_duel_retreat_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return AI_DUEL_RETREAT.case(changes, vram=vram, bank=bank, **named)


BEGIN_USE_ATTACK = Fixture("psychic-club-begin-use-attack-entry")
BEGIN_USE_ATTACK_REGS = BEGIN_USE_ATTACK.regs


def begin_use_attack_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return BEGIN_USE_ATTACK.case(changes, vram=vram, bank=bank, **named)


AI_GUST_OF_WIND = Fixture("ai-duel-19-gust-of-wind-entry")
AI_GUST_OF_WIND_REGS = AI_GUST_OF_WIND.regs


def ai_gust_of_wind_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return AI_GUST_OF_WIND.case(changes, vram=vram, bank=bank, **named)


AI_ENERGY_RETRIEVAL = Fixture("ai-duel-2d-energy-retrieval-entry")
AI_ENERGY_RETRIEVAL_REGS = AI_ENERGY_RETRIEVAL.regs


def ai_energy_retrieval_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return AI_ENERGY_RETRIEVAL.case(changes, vram=vram, bank=bank, **named)


EFFECT_DISPATCH = Fixture("ai-duel-2b-tryexecuteeffectcommandfunction-entry")
EFFECT_DISPATCH_REGS = EFFECT_DISPATCH.regs


def effect_dispatch_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return EFFECT_DISPATCH.case(changes, vram=vram, bank=bank, **named)


MASON_PRELOAD = Fixture("challenge-machine-preload-drmason-entry")
MASON_PRELOAD_REGS = MASON_PRELOAD.regs


def mason_preload_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return MASON_PRELOAD.case(changes, vram=vram, bank=bank, **named)


DISCARD_BASIC_LIST = Fixture("effect-revive-discardlist-entry")
DISCARD_BASIC_LIST_REGS = DISCARD_BASIC_LIST.regs


def discard_basic_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                               **named: bytes) -> dict:
    return DISCARD_BASIC_LIST.case(changes, vram=vram, bank=bank, **named)


COLOR_NAME = Fixture("effect-venomoth-1-colorname-entry")
COLOR_NAME_REGS = COLOR_NAME.regs


def color_name_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return COLOR_NAME.case(changes, vram=vram, bank=bank, **named)


AI_HEAL = profile_fixture({
    "vanilla": "effect-vileplume-1-aiheal-entry",
    "extended": "ai-heal-carrier-aiheal-entry",
})
AI_HEAL_REGS = AI_HEAL.regs


def ai_heal_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                    **named: bytes) -> dict:
    return AI_HEAL.case(changes, vram=vram, bank=bank, **named)


CLUB_MAP_NAME = Fixture("deck-machine-clubname-entry")
CLUB_MAP_NAME_REGS = CLUB_MAP_NAME.regs


def club_map_name_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return CLUB_MAP_NAME.case(changes, vram=vram, bank=bank, **named)


CARD_ENERGIES = Fixture("charizard-energies-entry")
CARD_ENERGIES_REGS = CARD_ENERGIES.regs


def card_energies_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return CARD_ENERGIES.case(changes, vram=vram, bank=bank, **named)


ATTACK_LIST = Fixture("charizard-attacklist-entry")
ATTACK_LIST_REGS = ATTACK_LIST.regs


def attack_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return ATTACK_LIST.case(changes, vram=vram, bank=bank, **named)


TRAINER_DISCARD_LIST = Fixture("scavenge-trainerlist-entry")
TRAINER_DISCARD_LIST_REGS = TRAINER_DISCARD_LIST.regs


def trainer_discard_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                 **named: bytes) -> dict:
    return TRAINER_DISCARD_LIST.case(changes, vram=vram, bank=bank, **named)


AI_POWER_EFFECT = Fixture("ai-duel-24-power-effect-entry")
AI_POWER_EFFECT_REGS = AI_POWER_EFFECT.regs


def ai_power_effect_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return AI_POWER_EFFECT.case(changes, vram=vram, bank=bank, **named)


DOME_RONALD = Fixture("ronald-3-dome-ronald-entry")
DOME_RONALD_REGS = DOME_RONALD.regs


def dome_ronald_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                        **named: bytes) -> dict:
    return DOME_RONALD.case(changes, vram=vram, bank=bank, **named)


CLERK9 = Fixture("challenge-hall-clerk9-entry")
CLERK9_REGS = CLERK9.regs


def clerk9_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                   **named: bytes) -> dict:
    return CLERK9.case(changes, vram=vram, bank=bank, **named)


DOME_LOAD_MAP = Fixture("dome-1-load-map-entry")
DOME_LOAD_MAP_REGS = DOME_LOAD_MAP.regs


def dome_load_map_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return DOME_LOAD_MAP.case(changes, vram=vram, bank=bank, **named)


DOME_AFTER_DUEL = Fixture("dome-1-after-duel-entry")
DOME_AFTER_DUEL_REGS = DOME_AFTER_DUEL.regs


def dome_after_duel_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return DOME_AFTER_DUEL.case(changes, vram=vram, bank=bank, **named)


PEAL_OF_THUNDER = Fixture("dome-2-peal-of-thunder-entry")
PEAL_OF_THUNDER_REGS = PEAL_OF_THUNDER.regs


def peal_of_thunder_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                            **named: bytes) -> dict:
    return PEAL_OF_THUNDER.case(changes, vram=vram, bank=bank, **named)


BENCH_HALF_HP = Fixture("dome-3-bench-half-hp-entry")
BENCH_HALF_HP_REGS = BENCH_HALF_HP.regs


def bench_half_hp_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return BENCH_HALF_HP.case(changes, vram=vram, bank=bank, **named)


ARTICUNO_TURN = Fixture("dome-3-articuno-turn-entry")
ARTICUNO_TURN_REGS = ARTICUNO_TURN.regs


def articuno_turn_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return ARTICUNO_TURN.case(changes, vram=vram, bank=bank, **named)


ARTICUNO_SCORING = Fixture("dome-3-articuno-scoring-entry")
ARTICUNO_SCORING_REGS = ARTICUNO_SCORING.regs


def articuno_scoring_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return ARTICUNO_SCORING.case(changes, vram=vram, bank=bank, **named)


CREDITS_SCROLL_TABLE = Fixture("credits-1-scroll-table-entry")
CREDITS_SCROLL_TABLE_REGS = CREDITS_SCROLL_TABLE.regs


def credits_scroll_table_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                 **named: bytes) -> dict:
    return CREDITS_SCROLL_TABLE.case(changes, vram=vram, bank=bank, **named)


SPECIAL_ATTACK_PARAMS = Fixture("challenge-hall-special-attack-params-entry")
SPECIAL_ATTACK_PARAMS_REGS = SPECIAL_ATTACK_PARAMS.regs


def special_attack_params_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                  **named: bytes) -> dict:
    return SPECIAL_ATTACK_PARAMS.case(changes, vram=vram, bank=bank, **named)


AI_PKMN_POWERS_MASTER = profile_fixture({
    "vanilla": "water-master-ai-pkmn-powers-entry",
    "extended": "ai-heal-carrier-pkmn-powers-loop-entry",
})
AI_PKMN_POWERS_MASTER_REGS = AI_PKMN_POWERS_MASTER.regs


def ai_pkmn_powers_master_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                  **named: bytes) -> dict:
    return AI_PKMN_POWERS_MASTER.case(changes, vram=vram, bank=bank, **named)


EVOLUTION_IN_LIST = profile_fixture({
    "vanilla": "dome-5-evolution-in-list-entry",
    "extended": "ai-duel-fire-charge-evolution-in-list-entry",
})
EVOLUTION_IN_LIST_REGS = EVOLUTION_IN_LIST.regs


def evolution_in_list_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return EVOLUTION_IN_LIST.case(changes, vram=vram, bank=bank, **named)


CARD_CAN_BE_PLAYED = Fixture("water-club-card-can-be-played-entry")
CARD_CAN_BE_PLAYED_REGS = CARD_CAN_BE_PLAYED.regs


def card_can_be_played_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                               **named: bytes) -> dict:
    return CARD_CAN_BE_PLAYED.case(changes, vram=vram, bank=bank, **named)


ALIVE_IN_PLAY_AREA = Fixture("dome-5-alive-in-play-area-entry")
ALIVE_IN_PLAY_AREA_REGS = ALIVE_IN_PLAY_AREA.regs


def alive_in_play_area_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                               **named: bytes) -> dict:
    return ALIVE_IN_PLAY_AREA.case(changes, vram=vram, bank=bank, **named)


ENERGY_NEEDED_IN_HAND = Fixture("grass-club-energy-needed-in-hand-entry")
ENERGY_NEEDED_IN_HAND_REGS = ENERGY_NEEDED_IN_HAND.regs


def energy_needed_in_hand_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                  **named: bytes) -> dict:
    return ENERGY_NEEDED_IN_HAND.case(changes, vram=vram, bank=bank, **named)


SPECIAL_AI_ATTACKS = Fixture("water-master-special-ai-attacks-entry")
SPECIAL_AI_ATTACKS_REGS = SPECIAL_AI_ATTACKS.regs


def special_ai_attacks_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                               **named: bytes) -> dict:
    return SPECIAL_AI_ATTACKS.case(changes, vram=vram, bank=bank, **named)


STRIKES_BACK_RESIDUAL = Fixture("dome-5-strikes-back-residual-entry")
STRIKES_BACK_RESIDUAL_REGS = STRIKES_BACK_RESIDUAL.regs


def strikes_back_residual_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                  **named: bytes) -> dict:
    return STRIKES_BACK_RESIDUAL.case(changes, vram=vram, bank=bank, **named)


SORT_TEMP_HAND = Fixture("water-master-sort-temp-hand-entry")
SORT_TEMP_HAND_REGS = SORT_TEMP_HAND.regs


def sort_temp_hand_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                           **named: bytes) -> dict:
    return SORT_TEMP_HAND.case(changes, vram=vram, bank=bank, **named)


CARD_DESCRIPTION = Fixture("credits-1-card-description-entry")
CARD_DESCRIPTION_REGS = CARD_DESCRIPTION.regs


def card_description_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return CARD_DESCRIPTION.case(changes, vram=vram, bank=bank, **named)


CARD_PAGE_ENERGY = Fixture("dome-4-card-page-energy-entry")
CARD_PAGE_ENERGY_REGS = CARD_PAGE_ENERGY.regs
CARD_PAGE_TRAINER = Fixture("dome-5-card-page-trainer-entry")
CARD_PAGE_TRAINER_REGS = CARD_PAGE_TRAINER.regs
ENERGY_OR_TRAINER_PAGE = Fixture("dome-5-energy-or-trainer-page-entry")
ENERGY_OR_TRAINER_PAGE_REGS = ENERGY_OR_TRAINER_PAGE.regs


def card_page_energy_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return CARD_PAGE_ENERGY.case(changes, vram=vram, bank=bank, **named)


def card_page_trainer_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return CARD_PAGE_TRAINER.case(changes, vram=vram, bank=bank, **named)


def energy_or_trainer_page_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                   **named: bytes) -> dict:
    return ENERGY_OR_TRAINER_PAGE.case(changes, vram=vram, bank=bank, **named)


ATTACK_INFORMATION = Fixture("credits-1-attack-information-entry")
ATTACK_INFORMATION_REGS = ATTACK_INFORMATION.regs


def attack_information_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                               **named: bytes) -> dict:
    return ATTACK_INFORMATION.case(changes, vram=vram, bank=bank, **named)


PLAY_AREA_CARD_INFO = Fixture("water-master-play-area-card-info-entry")
PLAY_AREA_CARD_INFO_REGS = PLAY_AREA_CARD_INFO.regs


def play_area_card_info_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return PLAY_AREA_CARD_INFO.case(changes, vram=vram, bank=bank, **named)


ATTACK_ANIMATION_COMMANDS = Fixture("dome-2-attack-animation-commands-entry")
ATTACK_ANIMATION_COMMANDS_REGS = ATTACK_ANIMATION_COMMANDS.regs


def attack_animation_commands_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                      **named: bytes) -> dict:
    return ATTACK_ANIMATION_COMMANDS.case(changes, vram=vram, bank=bank, **named)


ANIMATION_NEXT_COMMAND = Fixture("dome-2-animation-next-command-entry")
ANIMATION_NEXT_COMMAND_REGS = ANIMATION_NEXT_COMMAND.regs


def animation_next_command_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                   **named: bytes) -> dict:
    return ANIMATION_NEXT_COMMAND.case(changes, vram=vram, bank=bank, **named)


FIRST_OR_NEXT_PAGE = profile_fixture({
    "vanilla": "water-club-first-or-next-page-entry",
    "extended": "trainer-card-page-displayfirstornextcardpage-entry",
})
FIRST_OR_NEXT_PAGE_REGS = FIRST_OR_NEXT_PAGE.regs


def first_or_next_page_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                               **named: bytes) -> dict:
    return FIRST_OR_NEXT_PAGE.case(changes, vram=vram, bank=bank, **named)


ENERGY_RETRIEVAL = Fixture("ai-ghost-energy-retrieval-entry")
ENERGY_RETRIEVAL_REGS = ENERGY_RETRIEVAL.regs


def energy_retrieval_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             **named: bytes) -> dict:
    return ENERGY_RETRIEVAL.case(changes, vram=vram, bank=bank, **named)


ENERGY_SEARCH_FLOWER = Fixture("ai-flower-energy-search-entry")
ENERGY_SEARCH_FLOWER_REGS = ENERGY_SEARCH_FLOWER.regs


def energy_search_flower_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                 **named: bytes) -> dict:
    return ENERGY_SEARCH_FLOWER.case(changes, vram=vram, bank=bank, **named)


STRANGE_BEHAVIOR = profile_fixture({
    "vanilla": "ai-ghost-strange-behavior-entry",
    "extended": "ai-slowbro-carrier-strange-behavior-entry",
})
STRANGE_BEHAVIOR_REGS = STRANGE_BEHAVIOR.regs


def strange_behavior_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                             damage: int | None = None, **named: bytes) -> dict:
    patches = dict(changes or {})
    if damage is not None:
        turn = STRANGE_BEHAVIOR.hram[sym("hWhoseTurn") - HRAM_START]
        side = "Player" if turn == 0xC2 else "Opponent"
        index = STRANGE_BEHAVIOR.wram[sym(f"w{side}ArenaCard") - WRAM_START]
        width = card_id_size()
        offset = sym(f"w{side}Deck") - WRAM_START + index * width
        card_id = int.from_bytes(STRANGE_BEHAVIOR.wram[offset:offset + width], "little")
        patches[sym(f"w{side}ArenaCardHP")] = bytes((card_max_hp(card_id) - damage,))
    return STRANGE_BEHAVIOR.case(patches, vram=vram, bank=bank, **named)


COUNT_CARD_ID = Fixture("ai-ghost-count-card-id-entry")
COUNT_CARD_ID_REGS = COUNT_CARD_ID.regs


def count_card_id_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                          **named: bytes) -> dict:
    return COUNT_CARD_ID.case(changes, vram=vram, bank=bank, **named)


QUEUED_ANIMATIONS = Fixture("ai-science-queued-animations-entry")
QUEUED_ANIMATIONS_REGS = QUEUED_ANIMATIONS.regs


def queued_animations_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return QUEUED_ANIMATIONS.case(changes, vram=vram, bank=bank, **named)


DAMAGE_NUMBER_CHARS = Fixture("water-master-damage-number-chars-entry")
DAMAGE_NUMBER_CHARS_REGS = DAMAGE_NUMBER_CHARS.regs


def damage_number_chars_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return DAMAGE_NUMBER_CHARS.case(changes, vram=vram, bank=bank, **named)


DIGIT_CHAR = Fixture("water-master-digit-char-entry")
DIGIT_CHAR_REGS = DIGIT_CHAR.regs


def digit_char_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                       **named: bytes) -> dict:
    return DIGIT_CHAR.case(changes, vram=vram, bank=bank, **named)


PROCESS_TEXT_HEADER = Fixture("water-master-process-text-header-entry")
PROCESS_TEXT_HEADER_REGS = PROCESS_TEXT_HEADER.regs


def process_text_header_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                **named: bytes) -> dict:
    return PROCESS_TEXT_HEADER.case(changes, vram=vram, bank=bank, **named)


INIT_DUELVAR = Fixture("practice-win-init-duelvar-entry")
INIT_DUELVAR_REGS = INIT_DUELVAR.regs


def init_duelvar_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return INIT_DUELVAR.case(changes, vram=vram, bank=bank, **named)


SWAP_DUELVAR = Fixture("practice-win-swap-duelvar-entry")
SWAP_DUELVAR_REGS = SWAP_DUELVAR.regs


def swap_duelvar_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                         **named: bytes) -> dict:
    return SWAP_DUELVAR.case(changes, vram=vram, bank=bank, **named)


CARD_PAGE_ATTACK2 = Fixture("deck-explore-cardpage-attack2-entry")
CARD_PAGE_ATTACK2_REGS = CARD_PAGE_ATTACK2.regs


def card_page_attack2_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                              **named: bytes) -> dict:
    return CARD_PAGE_ATTACK2.case(changes, vram=vram, bank=bank, **named)


GIFT_CENTER_SEND_CARD = Fixture("gift-center-send-card-entry")
GIFT_CENTER_SEND_CARD_REGS = GIFT_CENTER_SEND_CARD.regs


def gift_center_send_card_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                  **named: bytes) -> dict:
    return GIFT_CENTER_SEND_CARD.case(changes, vram=vram, bank=bank, **named)


GIFT_CENTER_SEND_DECK = Fixture("gift-center-send-deck-entry")
GIFT_CENTER_SEND_DECK_REGS = GIFT_CENTER_SEND_DECK.regs


def gift_center_send_deck_fixture(changes: dict[int, bytes] | None = None, vram: bool = True, bank: int | None = None,
                                  **named: bytes) -> dict:
    return GIFT_CENTER_SEND_DECK.case(changes, vram=vram, bank=bank, **named)


def lass_hand_fixture(player_cards: tuple[int, ...], opponent_cards: tuple[int, ...],
                      *, ai_turn: bool = False, duel_type: int = 0) -> dict:
    from tests.cases._symbols import const, deck_bytes, sym

    turn = "Opponent" if ai_turn else "Player"
    seeds = {
        sym("hWhoseTurn"): bytes([sym(f"w{turn}DuelVariables") >> 8]),
        sym("wDuelType"): bytes([duel_type]),
        sym("hTempCardIndex_ff9f"): b"\x00",
        sym("wLCDC"): b"\x00",
        sym("wRNG1"): b"\x01\x02\x03",
        sym("wPlayerArenaCard"): b"\xFF", sym("wOpponentArenaCard"): b"\xFF",
        sym("wPlayerBench"): b"\xFF", sym("wOpponentBench"): b"\xFF",
    }
    reads = {sym("hWhoseTurn"): 1, sym("wNoItemSelectionMenuKeys"): 1}
    for prefix, cards in (("Player", player_cards), ("Opponent", opponent_cards)):
        seeds[sym(f"w{prefix}Deck")] = deck_bytes(list(cards) + [const("GRASS_ENERGY")] * (60 - len(cards)))
        seeds[sym(f"w{prefix}Hand")] = bytes(range(len(cards)))
        seeds[sym(f"w{prefix}NumberOfCardsInHand")] = bytes([len(cards)])
        seeds[sym(f"w{prefix}NumberOfCardsInDiscardPile")] = b"\x00"
        seeds[sym(f"w{prefix}NumberOfCardsNotInDeck")] = bytes([len(cards)])
        seeds[sym(f"w{prefix}CardLocations")] = b"\x01" * len(cards) + bytes(60 - len(cards))
        seeds[sym(f"w{prefix}DeckCards")] = bytes(range(60))
        reads[sym(f"w{prefix}NumberOfCardsInHand")] = 1
        reads[sym(f"w{prefix}CardLocations")] = len(cards)
    return {
        "wram": seeds, "read": reads,
        "keys": [0, 1, 0, 2] * 4,
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "instruction_budget": 20000000, "cycle_budget": 80000000,
    }
