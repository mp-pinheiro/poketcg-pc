"""Oracle-diff cases for poketcg/src/engine/overworld/npc_data.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory GetNPCHeaderPointer
CONTRACT["GetNPCHeaderPointer"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["GetNPCHeaderPointer"] = [
    {"a": 0x00},
    {"a": 0x01},
    {"a": 0x7F},
    {"a": 0x80},
    dict(POISON),
]
# <<< factory GetNPCHeaderPointer

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wOpponentName = 0xCC16
wOpponentPortrait = 0xCC15

wCurrentNPCNameTx = 0xD0C8
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wConsole = 0xCAB4
wTempNPC = 0xD3AB
wNPCSpriteID = 0xD3B3
wNPCAnim = 0xD3B1
wNPCAnimFlags = 0xD3B2
NPC_OUTPUT = {wTempNPC: 1, wNPCSpriteID: 1, wNPCAnim: 1, wNPCAnimFlags: 1}

wNPCDuelDeckID = 0xCC19
wNPCDuelPrizes = 0xCC18
wOpponentName = 0xCC16
wOpponentPortrait = 0xCC15

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wCurMap = 0xD32F
wMatchStartTheme = 0xD113
# <<< factory-cases-statics

# >>> factory SetNPCOpponentNameAndPortrait
CONTRACT["SetNPCOpponentNameAndPortrait"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNPCOpponentNameAndPortrait"] = [
    {"a": 0x00, "wram": {wOpponentName: b"\xFF\xFF", wOpponentPortrait: b"\xFF"}, "read": {wOpponentName: 2, wOpponentPortrait: 1}},
    dict(POISON, a=0x02, wram={wOpponentName: b"\xEE\xEE", wOpponentPortrait: b"\xEE"}, read={wOpponentName: 2, wOpponentPortrait: 1}),
    {"a": 0x7F, "wram": {wOpponentName: b"\x00\x00", wOpponentPortrait: b"\x00"}, "read": {wOpponentName: 2, wOpponentPortrait: 1}},
    {"a": 0xFF, "wram": {wOpponentName: b"\x11\x22", wOpponentPortrait: b"\x33"}, "read": {wOpponentName: 2, wOpponentPortrait: 1}},
]
# <<< factory SetNPCOpponentNameAndPortrait

# >>> factory GetNPCNameAndScript
CONTRACT["GetNPCNameAndScript"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("d", "e", "hl"), "wram_out": True}
CASES["GetNPCNameAndScript"] = [
    {"a": 0x00, "read": {wCurrentNPCNameTx: 2}},
    {"a": 0x01, "read": {wCurrentNPCNameTx: 2}},
    {"a": 0x02, "read": {wCurrentNPCNameTx: 2}},
    {"a": 0x03, "read": {wCurrentNPCNameTx: 2}},
    dict(POISON, a=0x00, read={wCurrentNPCNameTx: 2}),
]
# <<< factory GetNPCNameAndScript

# >>> factory LoadNPCSpriteData
CONTRACT["LoadNPCSpriteData"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["LoadNPCSpriteData"] = [
    {"a": 0x00, "wram": {wConsole: b"\x00"}, "read": NPC_OUTPUT},
    {"a": 0x01, "b": 0x12, "c": 0x34, "d": 0x56, "e": 0x78, "hl": 0x2468, "wram": {wConsole: b"\x02"}, "read": NPC_OUTPUT},
    {"a": 0x08, "b": 0xA5, "c": 0x5A, "d": 0x3C, "e": 0xC3, "hl": 0x9ABC, "wram": {wConsole: b"\x01"}, "read": NPC_OUTPUT},
    dict(POISON, a=0x00, wram={wConsole: b"\x02"}, read=NPC_OUTPUT),
]
# <<< factory LoadNPCSpriteData

# >>> factory _GetNPCDuelConfigurations
CONTRACT["_GetNPCDuelConfigurations"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["_GetNPCDuelConfigurations"] = [
    {"wram": {wNPCDuelDeckID: b"\x00"}},
    {"wram": {wNPCDuelDeckID: b"\x01"}},
    {"wram": {wNPCDuelDeckID: b"\x03"}},
    dict(POISON, wram={wNPCDuelDeckID: b"\x01"}),
]
# <<< factory _GetNPCDuelConfigurations

# >>> factory SetNPCDeckIDAndDuelTheme
CONTRACT["SetNPCDeckIDAndDuelTheme"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["SetNPCDeckIDAndDuelTheme"] = [
    {"a": 0x00, "wram": {0xCC19: b"\x00", 0xCC1A: b"\x00"}, "read": {0xCC19: 1, 0xCC1A: 1}},
    dict(POISON, a=0x02, wram={0xCC19: b"\x00", 0xCC1A: b"\x00"}, read={0xCC19: 1, 0xCC1A: 1}),
    {"a": 0x7F, "wram": {0xCC19: b"\x00", 0xCC1A: b"\x00"}, "read": {0xCC19: 1, 0xCC1A: 1}},
]
# <<< factory SetNPCDeckIDAndDuelTheme

# >>> factory _GetChallengeMachineDuelConfigurations
CONTRACT["_GetChallengeMachineDuelConfigurations"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e")}
CASES["_GetChallengeMachineDuelConfigurations"] = [
    {"wram": {0xCC19: b"\x00"}},
    {"wram": {0xCC19: b"\xFE"}},
    dict(POISON, wram={0xCC19: b"\x00"}),
]
# <<< factory _GetChallengeMachineDuelConfigurations

# >>> factory SetNPCDialogName
CONTRACT["SetNPCDialogName"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["SetNPCDialogName"] = [
    {"a": 0x00, "b": 0xBB, "c": 0xCC, "hl": 0x1234, "wram": {0xD0C8: b"\x00\x00"}, "read": {0xD0C8: 2}},
    {"a": 0x01, "b": 0x11, "c": 0x22, "hl": 0xC500, "wram": {0xD0C8: b"\x00\x00"}, "read": {0xD0C8: 2}},
    dict(POISON, a=0x00, wram={0xD0C8: b"\x00\x00"}, read={0xD0C8: 2}),
]
# <<< factory SetNPCDialogName

# >>> factory SetNPCMatchStartTheme
CONTRACT["SetNPCMatchStartTheme"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNPCMatchStartTheme"] = [
    {"a": 0x00, "wram": {wCurMap: b"\x00", wMatchStartTheme: b"\xFF"}, "read": {wMatchStartTheme: 1}, "expect_regs": {"a": 0x00, "f": 0x70}},
    {"a": 0x02, "wram": {wCurMap: b"\x00", wMatchStartTheme: b"\xFF"}, "read": {wMatchStartTheme: 1}, "expect_regs": {"a": 0x00, "f": 0x50}},
    {"a": 0x02, "wram": {wCurMap: b"\x20", wMatchStartTheme: b"\xFF"}, "read": {wMatchStartTheme: 1}, "expect_regs": {"a": 0x17, "f": 0xC0}, "expect": {wMatchStartTheme: b"\x17"}},
    dict(POISON, a=0xAA, wram={wCurMap: b"\x00"}, expect_regs={"a": 0xAA, "f": 0x40}),
]
# <<< factory SetNPCMatchStartTheme

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation GetNPCHeaderPointer
MUTATIONS["GetNPCHeaderPointer"] = {"source_symbol": "GetNPCHeaderPointer", "before": "const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, table_address);", "after": "const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, (uint16_t)(table_address + 1u));", "case_ids": ["GetNPCHeaderPointer-0", "GetNPCHeaderPointer-1", "GetNPCHeaderPointer-2", "GetNPCHeaderPointer-3"]}
# <<< factory-mutation GetNPCHeaderPointer
# >>> factory-mutation SetNPCOpponentNameAndPortrait
MUTATIONS["SetNPCOpponentNameAndPortrait"] = {"source_symbol": "SetNPCOpponentNameAndPortrait", "before": "const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, (uint16_t)(result.hl + NPC_DATA_NAME_TEXT));", "after": "const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, (uint16_t)(result.hl + NPC_DATA_NAME_TEXT + 1u));", "case_ids": ["SetNPCOpponentNameAndPortrait-0", "SetNPCOpponentNameAndPortrait-1", "SetNPCOpponentNameAndPortrait-2", "SetNPCOpponentNameAndPortrait-3"]}
# <<< factory-mutation SetNPCOpponentNameAndPortrait
# >>> factory-mutation GetNPCNameAndScript
MUTATIONS["GetNPCNameAndScript"] = {"source_symbol": "GetNPCNameAndScript", "before": "\tuint16_t cursor = (uint16_t)(header.hl + NPC_DATA_SCRIPT_PTR);", "after": "\tuint16_t cursor = (uint16_t)(header.hl + NPC_DATA_SCRIPT_PTR + 1u);", "case_ids": ["GetNPCNameAndScript-0", "GetNPCNameAndScript-1", "GetNPCNameAndScript-2", "GetNPCNameAndScript-3", "GetNPCNameAndScript-4"]}
# <<< factory-mutation GetNPCNameAndScript
# >>> factory-mutation LoadNPCSpriteData
MUTATIONS["LoadNPCSpriteData"] = {"source_symbol": "LoadNPCSpriteData", "before": "\tconst uint8_t *entry = rom_ptr(NPC_DATA_BANK, header.hl);", "after": "\tconst uint8_t *entry = rom_ptr(NPC_DATA_BANK, (uint16_t)(header.hl + 1u));", "case_ids": ["LoadNPCSpriteData-0", "LoadNPCSpriteData-1", "LoadNPCSpriteData-2", "LoadNPCSpriteData-3"]}
# <<< factory-mutation LoadNPCSpriteData
# >>> factory-mutation _GetNPCDuelConfigurations
MUTATIONS["_GetNPCDuelConfigurations"] = {"source_symbol": "_GetNPCDuelConfigurations", "before": "\treturn (_GetNPCDuelDuelConfigurationsResult){a, f, b, c, d, e, hl};", "after": "\treturn (_GetNPCDuelDuelConfigurationsResult){0u, f, b, c, d, e, hl};", "case_ids": ["_GetNPCDuelConfigurations-1", "_GetNPCDuelConfigurations-2", "_GetNPCDuelConfigurations-3"]}
# <<< factory-mutation _GetNPCDuelConfigurations
# >>> factory-mutation SetNPCDeckIDAndDuelTheme
MUTATIONS["SetNPCDeckIDAndDuelTheme"] = {"source_symbol": "SetNPCDeckIDAndDuelTheme", "before": "\tconst uint8_t *entry = rom_ptr(NPC_DATA_BANK, (uint16_t)(header.hl + NPC_DATA_DECK_ID));", "after": "\tconst uint8_t *entry = rom_ptr(NPC_DATA_BANK, (uint16_t)(header.hl + NPC_DATA_DECK_ID + 1u));", "case_ids": ["SetNPCDeckIDAndDuelTheme-1", "SetNPCDeckIDAndDuelTheme-2"]}
# <<< factory-mutation SetNPCDeckIDAndDuelTheme
# >>> factory-mutation _GetChallengeMachineDuelConfigurations
MUTATIONS["_GetChallengeMachineDuelConfigurations"] = {"source_symbol": "_GetChallengeMachineDuelConfigurations", "before": "a = entry[5];", "after": "a = entry[4];", "case_ids": ["_GetChallengeMachineDuelConfigurations-0", "_GetChallengeMachineDuelConfigurations-1"]}
# <<< factory-mutation _GetChallengeMachineDuelConfigurations
# >>> factory-mutation SetNPCDialogName
MUTATIONS["SetNPCDialogName"] = {"source_symbol": "SetNPCDialogName", "before": "wCurrentNPCNameTx = lo;", "after": "wCurrentNPCNameTx = (uint8_t)(lo + 1u);", "case_ids": ["SetNPCDialogName-0", "SetNPCDialogName-1"]}
# <<< factory-mutation SetNPCDialogName
# >>> factory-mutation SetNPCMatchStartTheme
MUTATIONS["SetNPCMatchStartTheme"] = {
    "source_symbol": "SetNPCMatchStartTheme",
    "before": "\tif (a != NPC_RONALD1)\n\t\treturn (SetNPCMatchStartThemeResult){a, f1, b, c, d, e, hl};",
    "after": "\tif (a != 0xFFu)\n\t\treturn (SetNPCMatchStartThemeResult){a, f1, b, c, d, e, hl};",
    "case_ids": ["SetNPCMatchStartTheme-2", "SetNPCMatchStartTheme-0", "SetNPCMatchStartTheme-1"],
}
# <<< factory-mutation SetNPCMatchStartTheme
