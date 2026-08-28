"""Oracle-diff cases for _PauseMenu_Exit (engine/menus/give_booster_pack.asm:113).

_PauseMenu_Exit is a bare ret: it reads nothing, writes nothing, and preserves
all registers.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    # All registers are preserved by a bare ret.
    "_PauseMenu_Exit": ("a", "f", "b", "c", "d", "e", "hl"),
}

CASES = {
    "_PauseMenu_Exit": [
        # All-zero baseline, including an untouched WRAM byte.
        {"wram": {0xC000: b"\x5A"}, "read": {0xC000: 1}},
        # Poisoned registers and untouched WRAM must survive unchanged.
        dict(POISON, wram={0xC000: b"\xA5"}, read={0xC000: 1}),
    ],
}
# >>> factory-cases-statics
# give_booster_pack.asm:1-56 (GiveBoosterPack). Addresses only; the C side uses
# the generated bare labels.
GBP_wLCDC = 0xCABB
GBP_wTxRam2 = 0xCE3F
GBP_wTxRam3 = 0xCE43
GBP_wAnotherBoosterPack = 0xD117

# FlashWhiteScreen calls EnableLCD, so real frames elapse from that point on and
# the VBlank handler runs every frame: CopyDMAFunction installs hDMAFunction,
# which InitMenuScreen's wVBlankOAMCopyToggle = TRUE makes the handler call, and
# without it the handler runs junk, never clears wReentrancyFlag, and every
# later WaitForVBlank halts forever at pc $0271. SetupText warms the glyph cache
# the text page ahead of the cutpoint walks.
GBP_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# wLCDC clear on entry keeps the leading DisableLCD on its `ret z` assert path
# and every WaitForVBlank ahead of FlashWhiteScreen a no-op. wAnotherBoosterPack
# selects which of the two received-pack texts the reference prints before it
# reaches the cutpoint, so it is pinned per case: $00 takes the `jr nz` to
# .first_booster, $01 falls through to AndAnotherBoosterPackText. Neither path
# touches an observed byte, so both must land on the same TxRam pair.
GBP_SEED_FIRST = {GBP_wLCDC: b"\x00", GBP_wAnotherBoosterPack: b"\x00"}
GBP_SEED_ANOTHER = {GBP_wLCDC: b"\x00", GBP_wAnotherBoosterPack: b"\x01"}
# B, not A: the reference has to clear one scrollable text page before it can
# reach the wait, and WaitForButtonAorB reads edge-triggered hKeysPressed, so
# the key has to be a cycled list -- a held button is newly pressed once and is
# invisible to a wait that starts after the first frame.
GBP_KEYS = [0x00, 0x02]
# Only the two TxRam slots this routine's own asm writes are observed.
# wTextBoxFrameType is written twice by the full routine, and
# wVBlankOAMCopyToggle is a byte the VBlank handler clears, so neither is
# comparable here.
GBP_READ = {GBP_wTxRam2: 2, GBP_wTxRam3: 2}
# A scene load, a white flash, a generated booster and a full page of
# letter-delayed text, at 70224 cycles per DMG frame, with the WaitForVBlank
# halt retiring few instructions per cycle.
GBP_INSTRUCTIONS = 60000000
GBP_CYCLES = 240000000
# <<< factory-cases-statics

# >>> factory GiveBoosterPack
# The reference is mid-flight at the pre-ret cutpoint declared below, so no
# register is comparable; the two TxRam slots the routine writes are.
CONTRACT["GiveBoosterPack"] = {"compare": (), "preserve": ()}
CASES["GiveBoosterPack"] = [
    # BOOSTER_COLOSSEUM_NEUTRAL ($00): type 0, SCENE_COLOSSEUM_BOOSTER ($01),
    # ColosseumBoosterText ($03A8). Row 0 of both tables.
    {"a": 0x00, "keys": GBP_KEYS, "setup": GBP_SETUP,
     "wram": dict(GBP_SEED_FIRST), "read": dict(GBP_READ),
     "instruction_budget": GBP_INSTRUCTIONS, "cycle_budget": GBP_CYCLES},
    # BOOSTER_EVOLUTION_GRASS ($08): type 1, SCENE_EVOLUTION_BOOSTER ($02),
    # EvolutionBoosterText ($03A9). The first id whose type is non-zero, so the
    # doubled-twice row index actually has to move.
    {"a": 0x08, "keys": GBP_KEYS, "setup": GBP_SETUP,
     "wram": dict(GBP_SEED_FIRST), "read": dict(GBP_READ),
     "instruction_budget": GBP_INSTRUCTIONS, "cycle_budget": GBP_CYCLES},
    # BOOSTER_LABORATORY_PSYCHIC ($17): type 3, SCENE_LABORATORY_BOOSTER ($04),
    # LaboratoryBoosterText ($03AB) -- the top row. wAnotherBoosterPack = TRUE
    # sends the reference down the AndAnotherBoosterPackText branch on its way
    # to the cutpoint.
    {"a": 0x17, "keys": GBP_KEYS, "setup": GBP_SETUP,
     "wram": dict(GBP_SEED_ANOTHER), "read": dict(GBP_READ),
     "instruction_budget": GBP_INSTRUCTIONS, "cycle_budget": GBP_CYCLES},
    # Poisoned entry registers with a real booster id in a: f/b/c/d/e/hl are all
    # dead on entry -- only `a` selects anything -- and $0E is
    # BOOSTER_MYSTERY_NEUTRAL, type 2, SCENE_MYSTERY_BOOSTER ($03),
    # MysteryBoosterText ($03AA).
    dict(POISON, a=0x0E, keys=GBP_KEYS, setup=GBP_SETUP,
         wram=dict(GBP_SEED_FIRST), read=dict(GBP_READ),
         instruction_budget=GBP_INSTRUCTIONS, cycle_budget=GBP_CYCLES),
]
# <<< factory GiveBoosterPack

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "_PauseMenu_Exit": {
        "source_symbol": "_PauseMenu_Exit",
        "before": "void _PauseMenu_Exit(void)\n{\n}",
        "after": "void _PauseMenu_Exit(void)\n{\n\tgb_write8(0xC000, 0x01);\n}",
        "case_ids": ["_PauseMenu_Exit-0", "_PauseMenu_Exit-1"],
    },
}
# >>> factory-mutation GiveBoosterPack
MUTATIONS["GiveBoosterPack"] = {"source_symbol": "GiveBoosterPack", "before": "\twTxRam3 = scene;\n\tgb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);", "after": "\twTxRam3 = (uint8_t)(scene + 1u);\n\tgb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);", "case_ids": ["GiveBoosterPack-0", "GiveBoosterPack-1", "GiveBoosterPack-3"]}
# <<< factory-mutation GiveBoosterPack
# >>> factory-completion GiveBoosterPack
# The reference never returns: asm:49 `call WaitForSongToFinish` loops on
# AssertSongFinished, which only reports finished once the timer ISR has walked
# the booster jingle to its `music_end`, and the call-level runner arms VBlank
# alone. That is a genuine spin, not a small budget, so completion is declared
# pre-ret at AssertSongFinished itself (poketcg.sym 00:378A, ROM0 and therefore
# bank-independent), exactly as the landed ShowMedalReceivedScreen and
# _ShowPromotionalCardScreen cases do. Nothing ahead of the wait calls
# AssertSongFinished -- DisableLCD, InitMenuScreen, LoadBoosterGfx,
# FlashWhiteScreen, PauseSong, PlaySong, GenerateBoosterPack and
# PrintScrollableText_NoTextBoxLabel do not -- so the first hit is the wait
# itself, after both observed TxRam slots have been written.
# legacy_to_schema always emits completion "return", so the split is applied
# after migration.
for _record in SCHEMA2_CASES["GiveBoosterPack"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x378A}
# <<< factory-completion GiveBoosterPack
