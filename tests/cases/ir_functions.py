"""Oracle-diff cases for poketcg/src/engine/link/ir_functions.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCurSongID = 0xDD80

CONTRACT = {
    "PlayCardPopSong": {"compare": ("hl",), "preserve": ("hl",)},
}

CASES = {
    "PlayCardPopSong": [
        # The routine has no inputs; all registers start at zero.
        {"read": {wCurSongID: 1}},
        # Entry registers are ignored except for the return contract.
        dict(POISON, read={wCurSongID: 1}),
        # Existing song state is replaced by the card-pop song ID.
        {"wram": {wCurSongID: b"\xff"}, "read": {wCurSongID: 1}},
    ],
}

# >>> factory InitIRCommunications
wOwnIRCommunicationParams = 0xC5EB
wIRCommunicationErrorCode = 0xC5EA
hWhoseTurn = 0xFF97
wNameBuffer = 0xC500
wOpponentName = 0xCC16
wDefaultText = 0xC590
sPlayerName = 0xA010
NAME_BUFFER_LENGTH = 0x10

CONTRACT["InitIRCommunications"] = {"compare": (), "preserve": ()}
CASES["InitIRCommunications"] = [
	{"a": 0,
	 "wram": {wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF",
	          wIRCommunicationErrorCode: b"\x00", hWhoseTurn: b"\x00",
	          wNameBuffer: b"\xFF", wOpponentName: b"\xFF\xFF",
	          wDefaultText: b"\xFF" * NAME_BUFFER_LENGTH},
	 "sram": {0: {sPlayerName: bytes(NAME_BUFFER_LENGTH)}},
	 "read": {wOwnIRCommunicationParams: 4, wIRCommunicationErrorCode: 1,
	          hWhoseTurn: 1, wNameBuffer: 1, wOpponentName: 2,
	          wDefaultText: NAME_BUFFER_LENGTH}},
	dict(POISON,
	     wram={wOwnIRCommunicationParams: b"\x00\x00\x00\x00",
	           wIRCommunicationErrorCode: b"\xAB", hWhoseTurn: b"\xAB",
	           wNameBuffer: b"\x00", wOpponentName: b"\x00\x00",
	           wDefaultText: b"\x00" * NAME_BUFFER_LENGTH},
	     sram={0: {sPlayerName: bytes(range(0x50, 0x50 + NAME_BUFFER_LENGTH))}},
	     read={wOwnIRCommunicationParams: 4, wIRCommunicationErrorCode: 1,
	           hWhoseTurn: 1, wNameBuffer: 1, wOpponentName: 2,
	           wDefaultText: NAME_BUFFER_LENGTH}),
	{"a": 0x02,
	 "wram": {wOwnIRCommunicationParams: b"\x00\x00\x00\x00",
	          wIRCommunicationErrorCode: b"\x00", hWhoseTurn: b"\x00",
	          wNameBuffer: b"\xEE", wOpponentName: b"\xEE\xEE",
	          wDefaultText: b"\xEE" * NAME_BUFFER_LENGTH},
	 "sram": {0: {sPlayerName: bytes(range(1, 1 + NAME_BUFFER_LENGTH))}},
	 "read": {wOwnIRCommunicationParams: 4, wIRCommunicationErrorCode: 1,
	          hWhoseTurn: 1, wNameBuffer: 1, wOpponentName: 2,
	          wDefaultText: NAME_BUFFER_LENGTH}},
]
# <<< factory InitIRCommunications


# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
WRAM_SEED = {0xCAB4: b"\x00", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00"}
SCENE_READ = {0xCAB4: 1, 0xCABC: 1, 0xD131: 1, 0xD291: 1, 0xD61C: 1, 0xD61D: 1, 0xD620: 2, 0xD622: 2}
TEXT_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4, 0xCD05: 2, 0xCD0A: 1}
# <<< factory-cases-statics

# >>> factory LoadLinkConnectingScene
CONTRACT["LoadLinkConnectingScene"] = {"compare": (), "preserve": ()}
CASES["LoadLinkConnectingScene"] = [
    {"hl": 0x0000, "wram": WRAM_SEED, "sram": {0: {}}, "setup": SETUP_TEXT, "read": {**SCENE_READ, **TEXT_READ}, "instruction_budget": 8000000, "cycle_budget": 32000000},
    dict(POISON, wram=WRAM_SEED, sram={0: {}}, setup=SETUP_TEXT, read={**SCENE_READ, **TEXT_READ}, instruction_budget=8000000, cycle_budget=32000000),
]
# <<< factory LoadLinkConnectingScene

# >>> factory ClearRPAndRestoreVBlankFunction
CONTRACT["ClearRPAndRestoreVBlankFunction"] = {"compare": ("a", "f"), "preserve": ("a", "f")}
CASES["ClearRPAndRestoreVBlankFunction"] = [
    {"a": 0x42, "wram": {0xCE8D: b"\x34\x12", 0xFF56: b"\x01"}, "read": {0xFF56: 1, 0xCAD1: 2}},
    dict(POISON, wram={0xCE8D: b"\x78\x56", 0xFF56: b"\x01"}, read={0xFF56: 1, 0xCAD1: 2}),
    {"a": 0x00, "wram": {0xCE8D: b"\x00\x00"}, "read": {0xFF56: 1, 0xCAD1: 2}},
]
# <<< factory ClearRPAndRestoreVBlankFunction

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _case, _name in zip(SCHEMA2_CASES["PlayCardPopSong"], ("zero", "poison", "boundary")):
    _case["id"] = f"PlayCardPopSong-{_name}"

MUTATIONS = {
    "PlayCardPopSong": {
        "source_symbol": "PlayCardPopSong",
        "before": "Music1_PlaySong(MUSIC_CARD_POP);",
        "after": "Music1_PlaySong((uint8_t)(MUSIC_CARD_POP + 1u));",
        "case_ids": [
            "PlayCardPopSong-zero",
            "PlayCardPopSong-poison",
            "PlayCardPopSong-boundary",
        ],
    },
}
# >>> factory-mutation InitIRCommunications
MUTATIONS["InitIRCommunications"] = {
	"source_symbol": "InitIRCommunications",
	"before": "i < NAME_BUFFER_LENGTH; i++)",
	"after": "i < (uint8_t)(NAME_BUFFER_LENGTH - 1u); i++)",
	"case_ids": ["InitIRCommunications-0", "InitIRCommunications-1", "InitIRCommunications-2"],
}
# <<< factory-mutation InitIRCommunications
# >>> factory-mutation LoadLinkConnectingScene
MUTATIONS["LoadLinkConnectingScene"] = {"source_symbol": "LoadLinkConnectingScene", "before": "\tLoadScene(SCENE_GAMEBOY_LINK_CONNECTING, 0u, 0u, 0u, 0u, 0u, saved_hl);", "after": "\tLoadScene(0u, 0u, 0u, 0u, 0u, 0u, saved_hl);", "case_ids": ["LoadLinkConnectingScene-0", "LoadLinkConnectingScene-1"]}
# <<< factory-mutation LoadLinkConnectingScene

# >>> factory-mutation ClearRPAndRestoreVBlankFunction
MUTATIONS["ClearRPAndRestoreVBlankFunction"] = {
    "source_symbol": "ClearRPAndRestoreVBlankFunction",
    "before": "\tClearRP();\n\tRestoreVBlankFunction();",
    "after": "\tClearRP();",
    "case_ids": ["ClearRPAndRestoreVBlankFunction-0", "ClearRPAndRestoreVBlankFunction-1"],
}
# <<< factory-mutation ClearRPAndRestoreVBlankFunction
