POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDefaultText = 0xC590
wLoadedCard1Type = 0xCC24
wLoadedCard1Level = 0xCC5D
wCardNameLength = 0xCD9B

# `stack` declares the words the caller pushed below the return address, in push
# order. _CopyCardNameAndLevel does `push bc` then `push de` before jumping here,
# so stack[0] is the saved bc that this label's `pop bc` restores and stack[1] the
# saved de its `pop de` restores. Without them the synthesized frame holds only a
# return address and the epilogue pops whatever preceded it.
_SAVED_BC = 0xBBCC
_SAVED_DE = 0xDDEE

# wCardNameLength=4 pads to 2 * (4 + 1) = 10 tiles, and the name copy that ran in
# the caller left "AB" + TX_END at wDefaultText.
_NAME = b"AB\x00"


def _seed(card_type, level):
    return {wDefaultText: _NAME, wLoadedCard1Type: bytes([card_type]),
            wLoadedCard1Level: bytes([level]), wCardNameLength: b"\x04"}


CONTRACT = {
    "_CopyCardNameAndLevel_HalfwidthText": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": (),
    },
    "_CopyCardNameAndLevel": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": (),
    },
}

CASES = {
    "_CopyCardNameAndLevel_HalfwidthText": [
        # Energy card: `cp TYPE_ENERGY` takes `jr nc`, so no level is appended and
        # the pad loop fills the remaining seven tiles.
        {"wram": _seed(0x08, 0x00), "stack": [_SAVED_BC, _SAVED_DE],
         "read": {wDefaultText: 10}},
        # Same shape with every entry register poisoned: all seven are dead on
        # entry here, so any of them reaching the exit is a leak.
        dict(POISON, wram=_seed(0x08, 0x00), stack=[_SAVED_BC, _SAVED_DE],
             read={wDefaultText: 10}),
        # Pokemon card at level 12: exercises the two-digit branch, whose tens
        # loop brackets its counter in push bc / pop bc.
        {"wram": _seed(0x00, 0x0C), "stack": [_SAVED_BC, _SAVED_DE],
         "read": {wDefaultText: 10}},
    ],
    # The parent runs against real card data: the setup call populates
    # wLoadedCard1Name/Type/Level, then CopyText expands the name into
    # wDefaultText and the TX_HALFWIDTH check tail-jumps into the label above.
    # Entry a is the pad width in tiles; bc and de must survive the round trip.
    "_CopyCardNameAndLevel": [
        # Blastoise: a Pokemon at level 52, so the halfwidth path appends " Lv52"
        # through its two-digit branch.
        {"a": 0x0D, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE,
         "setup": [{"fn": "LoadCardDataToBuffer1_FromCardID", "e": 0x43}],
         "read": {wDefaultText: 32}},
        # Water Energy: type >= TYPE_ENERGY, so no level is appended.
        {"a": 0x0D, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE,
         "setup": [{"fn": "LoadCardDataToBuffer1_FromCardID", "e": 0x03}],
         "read": {wDefaultText: 32}},
        # Poisoned entry registers, real pad width: f/b/c/d/e/hl carry the poison
        # values, so a leak of any of them shows up in the exit contract.
        dict(POISON, a=0x0D,
             setup=[{"fn": "LoadCardDataToBuffer1_FromCardID", "e": 0x43}],
             read={wDefaultText: 32}),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
MUTATIONS["_CopyCardNameAndLevel_HalfwidthText"] = {
    "source_symbol": "_CopyCardNameAndLevel_HalfwidthText",
    "before": "\tuint8_t b = (uint8_t)((uint8_t)(wCardNameLength + 1u) << 1);",
    "after": "\tuint8_t b = (uint8_t)((uint8_t)(wCardNameLength + 2u) << 1);",
    "case_ids": ["_CopyCardNameAndLevel_HalfwidthText-0",
                 "_CopyCardNameAndLevel_HalfwidthText-2"],
}
MUTATIONS["_CopyCardNameAndLevel"] = {
    "source_symbol": "_CopyCardNameAndLevel",
    "before": "\tif (gb_read8(wDefaultText_ADDR) == TX_HALFWIDTH)",
    "after": "\tif (gb_read8(wDefaultText_ADDR) != TX_HALFWIDTH)",
    "case_ids": ["_CopyCardNameAndLevel-0", "_CopyCardNameAndLevel-1"],
}
