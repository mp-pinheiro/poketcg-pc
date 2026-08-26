"""Oracle-diff cases for poketcg/src/scripts/fire_club_lobby.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory FindExtraInteractableObjects
CONTRACT["FindExtraInteractableObjects"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()}
CASES["FindExtraInteractableObjects"] = [
    {"hl": 0xC500, "wram": {0xC500: b"\x00"}},
    {"hl": 0xC500, "wram": {
        0xC500: b"\xAA\x00\x00\x00\x00" + b"\x05\x06\x00\xBC\x9A" + b"\x00",
        0xD330: b"\x05", 0xD331: b"\x06", 0xD334: b"\x00"}},
    dict(POISON, hl=0x1234, wram={0xD330: b"\x05", 0xD331: b"\x06", 0xD334: b"\x00"}),
]
# <<< factory FindExtraInteractableObjects

# >>> factory FireClubPressedA
CONTRACT["FireClubPressedA"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()}
CASES["FireClubPressedA"] = [
    {"wram": {0xD330: b"\x10", 0xD331: b"\x02", 0xD334: b"\x00"}, "rom_bank": 3},
    {"wram": {0xD330: b"\x63", 0xD331: b"\x02", 0xD334: b"\x00"}, "rom_bank": 3},
    dict(POISON, wram={0xD330: b"\x10", 0xD331: b"\x02", 0xD334: b"\x00"}, rom_bank=3),
]
# <<< factory FireClubPressedA

# >>> factory FireClubLobbyAfterDuel
CONTRACT["FireClubLobbyAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["FireClubLobbyAfterDuel"] = [
    {"wram": {0xD0C3: b"\x00", 0xD0C4: b"\x19"}, "rom_bank": 3},
    {"wram": {0xD0C3: b"\x01", 0xD0C4: b"\x19"}, "rom_bank": 3},
    dict(POISON, wram={0xD0C3: b"\x00", 0xD0C4: b"\x19"}, rom_bank=3),
]
# <<< factory FireClubLobbyAfterDuel

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation FindExtraInteractableObjects
MUTATIONS["FindExtraInteractableObjects"] = {"source_symbol": "FindExtraInteractableObjects", "before": "if (gb_read8(wPlayerXCoord_ADDR) == gb_read8(cursor)) {", "after": "if (gb_read8(wPlayerXCoord_ADDR) != gb_read8(cursor)) {", "case_ids": ["FindExtraInteractableObjects-1"]}
# <<< factory-mutation FindExtraInteractableObjects
# >>> factory-mutation FireClubPressedA
MUTATIONS["FireClubPressedA"] = {"source_symbol": "FireClubPressedA", "before": "FindExtraInteractableObjectsResult r = FindExtraInteractableObjects(SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520);", "after": "FindExtraInteractableObjectsResult r = FindExtraInteractableObjects((uint16_t)(SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520 + 5u));", "case_ids": ["FireClubPressedA-0", "FireClubPressedA-1"]}
# <<< factory-mutation FireClubPressedA
# >>> factory-mutation FireClubLobbyAfterDuel
MUTATIONS["FireClubLobbyAfterDuel"] = {"source_symbol": "FireClubLobbyAfterDuel", "before": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(AFTER_DUEL_TABLE_830);", "after": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(AFTER_DUEL_TABLE_830 + 1u));", "case_ids": ["FireClubLobbyAfterDuel-0"]}
# <<< factory-mutation FireClubLobbyAfterDuel
