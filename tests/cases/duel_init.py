"""Oracle-diff cases for poketcg/src/engine/menus/duel_init.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
DI_WLCDC = 0xCABB
DI_HW = 0xFF40
DI_WD291 = 0xD291
DI_FRAME = 0xCCF3
DI_TXRAM2 = 0xCE3F
DI_TXRAM2_B = 0xCE41
DI_DECK_ID = 0xCC19
DI_OPP_NAME = 0xCC16
DI_PORTRAIT = 0xCC15
DI_THEME = 0xD113
DI_CUR_SONG = 0xDD80
# duel_init.asm:19-38 copies the title and deck-name text ids out of
# OpponentTitlesAndDeckNames at four bytes per deck, and skips the deck-name
# label when both of its bytes are zero, so the deck id selects the branch.
# The start theme is out of range, so music1.asm:36-39 leaves wCurSongID at the
# seeded $80 and WaitForSongToFinish returns on its first pass; a real song id
# never reaches $80 and the routine would never return.
DI_READ = {DI_FRAME: 1, DI_TXRAM2: 2, DI_TXRAM2_B: 2, DI_WD291: 1}
DI_KEYS = [0x00, 0x01]
DI_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
DI_BUDGET = 60000000
DI_CYCLES = 240000000


def _di_wram(deck_id):
    return {DI_WLCDC: b"\x00", DI_HW: b"\x80", DI_WD291: b"\x41",
            DI_DECK_ID: bytes([deck_id]), DI_OPP_NAME: b"\x76\x00",
            DI_PORTRAIT: b"\x01", DI_THEME: b"\xFF", DI_CUR_SONG: b"\x80",
            DI_TXRAM2: b"\x00\x00", DI_TXRAM2_B: b"\x00\x00"}
# <<< factory-cases-statics

# >>> factory Duel_Init
CONTRACT["Duel_Init"] = {"compare": (), "preserve": ()}
CASES["Duel_Init"] = [
    {"f": 0x00, "keys": DI_KEYS, "setup": DI_SETUP, "wram": _di_wram(0),
     "read": dict(DI_READ), "instruction_budget": DI_BUDGET,
     "cycle_budget": DI_CYCLES},
    {"f": 0x00, "keys": DI_KEYS, "setup": DI_SETUP, "wram": _di_wram(1),
     "read": dict(DI_READ), "instruction_budget": DI_BUDGET,
     "cycle_budget": DI_CYCLES},
    dict(POISON, keys=DI_KEYS, setup=DI_SETUP, wram=_di_wram(0),
         read=dict(DI_READ), instruction_budget=DI_BUDGET,
         cycle_budget=DI_CYCLES),
    dict(POISON, keys=DI_KEYS, setup=DI_SETUP, wram=_di_wram(1),
         read=dict(DI_READ), instruction_budget=DI_BUDGET,
         cycle_budget=DI_CYCLES),
]
# <<< factory Duel_Init

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Duel_Init
MUTATIONS["Duel_Init"] = {"source_symbol": "Duel_Init", "before": "\twTextBoxFrameType = 4u;", "after": "\twTextBoxFrameType = 5u;", "case_ids": ["Duel_Init-0", "Duel_Init-1", "Duel_Init-2", "Duel_Init-3"]}
# <<< factory-mutation Duel_Init
