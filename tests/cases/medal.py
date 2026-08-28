"""Oracle-diff cases for poketcg/src/engine/menus/medal.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wConsole = 0xCAB4
wLCDC = 0xCABB
wTxRam2 = 0xCE3F
wMedalScreenYOffset = 0xD114
wWhichMedal = 0xD115
wMedalDisplayTimer = 0xD116

# FlashWhiteScreen calls EnableLCD, so real frames elapse from that point on and
# the VBlank handler runs: CopyDMAFunction installs hDMAFunction, which
# InitMenuScreen's wVBlankOAMCopyToggle = 1 makes the handler call every frame.
# SetupText warms the glyph cache PrintScrollableText walks.
MEDAL_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# wLCDC clear on entry keeps DisableLCD on its `ret z` assert path and every
# WaitForVBlank before FlashWhiteScreen a no-op; both sides leave $CABB at $80
# afterwards because both run EnableLCD. wConsole = CONSOLE_DMG is what makes the
# reference's `farcall SetMainSGBBorder` return at its first compare, which is
# the path the C body reproduces.
MEDAL_SEED = {wLCDC: b"\x00", wConsole: b"\x00"}
# $D114-$D116 is wMedalScreenYOffset/wWhichMedal/wMedalDisplayTimer in one span;
# $CE3F is the two-byte wTxRam2 medal-name pointer. Nothing the VBlank handler
# touches is observed.
MEDAL_READ = {wMedalScreenYOffset: 3, wTxRam2: 2}
# 225 flashing frames plus the letter-delay frames of the text page, at 70224
# cycles per DMG frame, with the halt in WaitForVBlank retiring few instructions
# per cycle.
MEDAL_INSTRUCTIONS = 60000000
MEDAL_CYCLES = 240000000
MEDAL_KEYS = [0x00, 0x01]
# <<< factory-cases-statics

# >>> factory ShowMedalReceivedScreen
# The reference is mid-flight at the completion point declared below, so no
# register is comparable; the medal screen's own WRAM writes are.
CONTRACT["ShowMedalReceivedScreen"] = {"compare": (), "preserve": ()}
CASES["ShowMedalReceivedScreen"] = [
    # Medal 0 (Grass): wWhichMedal = $00, wTxRam2 = GrassClubMapName ($0336).
    {"a": 0x08, "keys": MEDAL_KEYS, "setup": MEDAL_SETUP,
     "wram": dict(MEDAL_SEED), "read": dict(MEDAL_READ),
     "instruction_budget": MEDAL_INSTRUCTIONS, "cycle_budget": MEDAL_CYCLES},
    # Last medal ($0F -> index 7, FightingClubMapName $0332): the top of the
    # table, so an off-by-one in the `sub $8` or in the doubled index shows here.
    {"a": 0x0F, "keys": MEDAL_KEYS, "setup": MEDAL_SETUP,
     "wram": dict(MEDAL_SEED), "read": dict(MEDAL_READ),
     "instruction_budget": MEDAL_INSTRUCTIONS, "cycle_budget": MEDAL_CYCLES},
    # Poisoned entry registers with a real medal id in a: f/b/c/d/e/hl are all
    # dead on entry -- only `a` selects anything -- and $0A is medal 2 (Fire).
    dict(POISON, a=0x0A, keys=MEDAL_KEYS, setup=MEDAL_SETUP,
         wram=dict(MEDAL_SEED), read=dict(MEDAL_READ),
         instruction_budget=MEDAL_INSTRUCTIONS, cycle_budget=MEDAL_CYCLES),
]
# <<< factory ShowMedalReceivedScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation ShowMedalReceivedScreen
MUTATIONS["ShowMedalReceivedScreen"] = {"source_symbol": "ShowMedalReceivedScreen", "before": "\twMedalScreenYOffset = (uint8_t)-6;", "after": "\twMedalScreenYOffset = (uint8_t)-5;", "case_ids": ["ShowMedalReceivedScreen-0", "ShowMedalReceivedScreen-1", "ShowMedalReceivedScreen-2"]}
# <<< factory-mutation ShowMedalReceivedScreen
# >>> factory-completion ShowMedalReceivedScreen
# The reference never returns: WaitForSongToFinish loops on AssertSongFinished,
# which only reports finished once wCurSongID reads $80, and nothing but the
# timer ISR's Music1_Update puts it there while the call-level runner arms VBlank
# alone. That is a genuine spin, not a small budget, so completion is declared
# pre-ret at AssertSongFinished itself (poketcg.sym 00:378A, ROM0 and therefore
# bank-independent), exactly as the landed _ShowPromotionalCardScreen and
# PreparePrinterConnection cases do. Nothing ahead of the wait calls
# AssertSongFinished -- PauseSong, PlaySong, InitMenuScreen, DrawCollectedMedals,
# FlashWhiteScreen, FlashReceivedMedal and PrintScrollableText_NoTextBoxLabel do
# not -- so the first hit is the wait itself, after every observed byte has been
# written. legacy_to_schema always emits completion "return", so the split is
# applied after migration.
for _record in SCHEMA2_CASES["ShowMedalReceivedScreen"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x378A}
# <<< factory-completion ShowMedalReceivedScreen
