"""Oracle-diff cases for poketcg/src/engine/promotional_card.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wLoadedCard1Name = 0xCC27
hWhoseTurn = 0xFF97
# <<< factory-cases-statics

# >>> factory _ShowPromotionalCardScreen
CONTRACT["_ShowPromotionalCardScreen"] = {"compare": (), "preserve": ()}
# a != 0 in every case: with a == 0 the ROM re-enters its own tail four times
# and the pre-ret stop below would land on the first pass while the port ran
# all four, so the legendary branch is not comparable at this completion point.
# 0x1E is VILEPLUME (ReceivedCardText); POISON's 0xAA takes the promotional
# fallback. keys=[0x00, 0x02] taps B, which is what WaitForWideTextBoxInput
# reads inside _DisplayCardDetailScreen; a measured reference run reaches the
# wait loop with exactly this shape. CopyDMAFunction installs hDMAFunction for
# the VBlank handler; the routine calls SetupText itself, so the glyph cache is
# initialised without a second setup entry.
CASES["_ShowPromotionalCardScreen"] = [
    {"a": 0x1E, "keys": [0x00, 0x02],
     "read": {wLoadedCard1Name: 2, hWhoseTurn: 1},
     "setup": [{"fn": "CopyDMAFunction"}],
     "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x02],
         read={wLoadedCard1Name: 2, hWhoseTurn: 1},
         setup=[{"fn": "CopyDMAFunction"}],
         instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _ShowPromotionalCardScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation _ShowPromotionalCardScreen
MUTATIONS["_ShowPromotionalCardScreen"] = {
    "source_symbol": "_ShowPromotionalCardScreen",
    "before": "\t\tLoadCardDataToBuffer1_FromCardID(card);\n\t\tPauseSong();",
    "after": "\t\tLoadCardDataToBuffer1_FromCardID((uint8_t)(card + 1u));\n\t\tPauseSong();",
    "case_ids": ["_ShowPromotionalCardScreen-0", "_ShowPromotionalCardScreen-1"],
}
# <<< factory-mutation _ShowPromotionalCardScreen
# >>> factory-completion _ShowPromotionalCardScreen
# $6680 is _ShowPromotionalCardScreen.loop (poketcg.sym 06:6680), the
# `call AssertSongFinished` / `or a` / `jr nz` wait. The reference can never
# leave it: AssertSongFinished only reports done once wCurSongID reads $80, and
# nothing but the timer ISR's Music1_Update can put it there, while the
# call-level runner arms VBlank alone. That is a genuine spin, not a small
# budget, so completion is declared pre-ret at the loop head exactly as the
# landed PreparePrinterConnection cases do. legacy_to_schema always emits
# completion "return", so the split is applied after migration.
for _record in SCHEMA2_CASES["_ShowPromotionalCardScreen"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x6680}
# <<< factory-completion _ShowPromotionalCardScreen
