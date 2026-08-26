"""Oracle-diff cases for poketcg/src/engine/menus/card_album.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetFirstOwnedCardIndex
OWNED_LIST = 0xCF68
NOT_OWNED = 0x80

CONTRACT["GetFirstOwnedCardIndex"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("c", "d", "e")}
CASES["GetFirstOwnedCardIndex"] = [
    {},
    dict(POISON),
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 3, "a": NOT_OWNED}]},
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 64, "a": NOT_OWNED}]},
    {"setup": [{"fn": "FillMemoryWithA", "hl": OWNED_LIST, "b": 0, "c": 1, "a": NOT_OWNED},
               {"fn": "FillMemoryWithA", "hl": OWNED_LIST + 1, "b": 0, "c": 1, "a": 0x81}]},
]
# <<< factory GetFirstOwnedCardIndex

# >>> factory-cases-statics
wCardListCoords = 0xCED0
wCardListVisibleOffset = 0xCEA1
wFilteredCardList = 0xCEDA
wNumVisibleCardListEntries = 0xCECB
wUnableToScrollDown = 0xCECD
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hDPadHeld = 0xFF8F
wCardListCursorPos = 0xCEA4
wCardListNumCursorPositions = 0xCEA9
wCurCardListPtr = 0xCFD8
wFirstOwnedCardIndex = 0xCFE5
wMenuInputSFX = 0xCFE3
wOwnedCardsCountList = 0xCF68
wTempCardListCursorPos = 0xCED4
wVBlankOAMCopyToggle = 0xCAC0
wced2 = 0xCED2

hCurMenuItem = 0xFFB1
wLCDC = 0xCABB
# <<< factory-cases-statics

# >>> factory PrintCardSetListEntries
CONTRACT["PrintCardSetListEntries"] = {"compare": ("hl",), "preserve": ()}
CASES["PrintCardSetListEntries"] = [
    {"wram": {wCardListCoords: b"\x10\x08", wCardListVisibleOffset: b"\x00", wNumVisibleCardListEntries: b"\x00", wFilteredCardList: b"\x00\x00"}, "read": {wUnableToScrollDown: 1, wFilteredCardList: 2}},
    dict(POISON, wram={wCardListCoords: b"\x10\x08", wCardListVisibleOffset: b"\x00", wNumVisibleCardListEntries: b"\x00", wFilteredCardList: b"\x00\x00"}, read={wUnableToScrollDown: 1, wFilteredCardList: 2}),
]
# <<< factory PrintCardSetListEntries

# >>> factory CreateCardSetList
CONTRACT["CreateCardSetList"] = {"compare": ("a", "f"), "preserve": ()}
CASES["CreateCardSetList"] = [
    {"a": 0x00, "wram": {0xC000: b"\x80" * 0xE5}, "read": {0xCEDA: 60, 0xCF68: 60, 0xCEAE: 1, 0xCFE2: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0x02, "wram": {0xC000: b"\x80" * 0xE5}, "read": {0xCEDA: 60, 0xCF68: 60, 0xCEAE: 1, 0xCFE2: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xC000: b"\x80" * 0xE5}, "read": {0xCEDA: 60, 0xCF68: 60, 0xCEAE: 1, 0xCFE2: 1}, "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory CreateCardSetList

# >>> factory HandleCardAlbumCardPage
# The bounded path: the entry under the cursor is CARD_NOT_OWNED, so the card
# page (and every frame-driven callee behind it) is skipped, and hDPadHeld holds
# a PAD_BUTTONS bit, so .handle_input exits on its first test. No call, no frame,
# no VBlank -- the reference leaves rLCDC at the runner's 0 and never services an
# interrupt, so wVBlankOAMCopyToggle is safe to observe.
CONTRACT["HandleCardAlbumCardPage"] = {"compare": ("a", "f"), "preserve": ()}
CASES["HandleCardAlbumCardPage"] = [
    {"d": 0x00, "e": 0x00,
     "wram": {wCardListCursorPos: b"\x03", wCardListVisibleOffset: b"\x02",
              wOwnedCardsCountList + 0x05: b"\x80", hDPadHeld: b"\x01"},
     "read": {wVBlankOAMCopyToggle: 1, wTempCardListCursorPos: 1},
     "instruction_budget": 200000, "cycle_budget": 800000},
    dict(POISON,
         wram={wCardListCursorPos: b"\x05", wCardListVisibleOffset: b"\x00",
               wOwnedCardsCountList + 0x05: b"\x80", hDPadHeld: b"\x0F"},
         read={wVBlankOAMCopyToggle: 1, wTempCardListCursorPos: 1},
         instruction_budget=200000, cycle_budget=800000),
    {"d": 0xDD, "e": 0xEE,
     "wram": {wCardListCursorPos: b"\x00", wCardListVisibleOffset: b"\x00",
              wOwnedCardsCountList: b"\x80", hDPadHeld: b"\x08"},
     "read": {wVBlankOAMCopyToggle: 1, wTempCardListCursorPos: 1},
     "instruction_budget": 200000, "cycle_budget": 800000},
]
# <<< factory HandleCardAlbumCardPage

# >>> factory CreateCardSetListAndInitListCoords
CONTRACT["CreateCardSetListAndInitListCoords"] = {"compare": ("a", "f"), "preserve": ("a", "f")}
CASES["CreateCardSetListAndInitListCoords"] = [
    {"a": 0x04, "sram": {0: {0xA100: bytes(0xFF)}}, "read": {0xC000: 0xFF, 0xCECB: 1, 0xCED0: 2, 0xCFB9: 2}, "instruction_budget": 2000000, "cycle_budget": 8000000},
    dict(POISON, a=0x03, sram={0: {0xA100: bytes(0xFF)}}, read={0xC000: 0xFF, 0xCECB: 1, 0xCED0: 2, 0xCFB9: 2}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory CreateCardSetListAndInitListCoords

# >>> factory CardAlbum
CONTRACT["CardAlbum"] = {"compare": (), "preserve": ()}
CASES["CardAlbum"] = [
    {
        "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234,
        "keys": [0x02],
        "wram": {0xFFB1: b"\xFF", 0xCABB: b"\x00"},
        "read": {0xCABB: 1},
        "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],
        "instruction_budget": 20000000,
        "cycle_budget": 80000000,
    },
    dict(POISON, keys=[0x02], wram={0xFFB1: b"\xFF", 0xCABB: b"\x00"}, read={0xCABB: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory CardAlbum

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetFirstOwnedCardIndex
MUTATIONS["GetFirstOwnedCardIndex"] = {
    "source_symbol": "GetFirstOwnedCardIndex",
    "before": "index++;",
    "after": "",
    "case_ids": ["GetFirstOwnedCardIndex-2", "GetFirstOwnedCardIndex-3", "GetFirstOwnedCardIndex-4"],
}
# <<< factory-mutation GetFirstOwnedCardIndex
# >>> factory-mutation PrintCardSetListEntries
MUTATIONS["PrintCardSetListEntries"] = {"source_symbol": "PrintCardSetListEntries", "before": "gb_write8(wUnableToScrollDown_ADDR, TRUE);", "after": "gb_write8(wUnableToScrollDown_ADDR, FALSE);", "case_ids": ["PrintCardSetListEntries-0", "PrintCardSetListEntries-1"]}
# <<< factory-mutation PrintCardSetListEntries
# >>> factory-mutation CreateCardSetList
MUTATIONS["CreateCardSetList"] = {"source_symbol": "CreateCardSetList", "before": "void CreateCardSetList(uint8_t a)\n{\n\tuint8_t set = a;", "after": "void CreateCardSetList(uint8_t a)\n{\n\tuint8_t set = 0u;", "case_ids": ["CreateCardSetList-1"]}
# <<< factory-mutation CreateCardSetList
# >>> factory-mutation HandleCardAlbumCardPage
MUTATIONS["HandleCardAlbumCardPage"] = {
    "source_symbol": "HandleCardAlbumCardPage",
    "before": "wVBlankOAMCopyToggle = TRUE;\n\ta = wCardListCursorPos;\n\twTempCardListCursorPos = a;",
    "after": "wVBlankOAMCopyToggle = FALSE;\n\ta = wCardListCursorPos;\n\twTempCardListCursorPos = (uint8_t)(a + 1u);",
    "case_ids": ["HandleCardAlbumCardPage-0", "HandleCardAlbumCardPage-1",
                 "HandleCardAlbumCardPage-2"],
}
# <<< factory-mutation HandleCardAlbumCardPage
# >>> factory-mutation CreateCardSetListAndInitListCoords
MUTATIONS["CreateCardSetListAndInitListCoords"] = {
    "source_symbol": "CreateCardSetListAndInitListCoords",
    "before": "\tgb_write8(wCardListCoords_ADDR, 0x04u);\n\tgb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x02u);",
    "after": "\tgb_write8(wCardListCoords_ADDR, 0x03u);\n\tgb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x02u);",
    "case_ids": ["CreateCardSetListAndInitListCoords-0", "CreateCardSetListAndInitListCoords-1"],
}
# <<< factory-mutation CreateCardSetListAndInitListCoords
# >>> factory-mutation CardAlbum
MUTATIONS["CardAlbum"] = {
    "source_symbol": "CardAlbum",
    "before": "if ((uint8_t)(item + 1u) == 0u)",
    "after": "if ((uint8_t)(item + 2u) == 0u)",
    "case_ids": ["CardAlbum-0", "CardAlbum-1"],
}
# <<< factory-mutation CardAlbum
