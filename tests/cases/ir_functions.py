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

wCurSongID = 0xDD80
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

# >>> factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain
CONTRACT["LoadLinkNotConnectedSceneAndAskWhetherToTryAgain"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LoadLinkNotConnectedSceneAndAskWhetherToTryAgain"] = [
    {"hl": 0x0000,"wram": {**WRAM_SEED, 0xCABB: b"\x00"},"sram": {0: {}},"setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],"keys": [0x00, 0x01],"read": {**SCENE_READ, **TEXT_READ},"instruction_budget": 20000000,"cycle_budget": 80000000},
    dict(POISON, hl=0x0000, wram={**WRAM_SEED, 0xCABB: b"\x00"}, sram={0: {}}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], read={**SCENE_READ, **TEXT_READ}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain

# >>> factory SetIRCommunicationErrorCode_NoError
CONTRACT["SetIRCommunicationErrorCode_NoError"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SetIRCommunicationErrorCode_NoError"] = [
    {"oracle": False, "evidence": "primary", "why": "The deterministic native CGB infrared peer drives the receive request; clearing the own-communication parameter and the error return are asserted.", "a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": 0x81, "ir_peer": True, "setup": [{"fn": "CopyDMAFunction"}], "wram": {0xCAB4: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC5EB: b"\xFF"}, "read": {0xC5EB: 1}, "expect": {0xC5EB: b"\x00"}, "expect_regs": {"a": 0xFF, "f": 0x10}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The deterministic native CGB infrared peer drives the receive request with poisoned registers; clearing the own-communication parameter and the error return are asserted.", keys=0x81, ir_peer=True, setup=[{"fn": "CopyDMAFunction"}], wram={0xCAB4: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC5EB: b"\xFF"}, read={0xC5EB: 1}, expect={0xC5EB: b"\x00"}, expect_regs={"a": 0xFF, "f": 0x10}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SetIRCommunicationErrorCode_NoError

# >>> factory SetIRCommunicationErrorCode_Error
CONTRACT["SetIRCommunicationErrorCode_Error"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SetIRCommunicationErrorCode_Error"] = [
    {"oracle": False, "evidence": "primary", "why": "Infrared peer hardware is unavailable to the reference runner; the native peer path verifies the error-code write and communication shutdown.", "keys": 0x81, "ir_peer": True, "setup": [{"fn": "CopyDMAFunction"}], "wram": {0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, "read": {0xC5EA: 1}, "expect": {0xC5EA: b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x10}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="Infrared peer hardware is unavailable to the reference runner; the native peer path verifies the error-code write and communication shutdown with poisoned registers.", keys=0x81, ir_peer=True, setup=[{"fn": "CopyDMAFunction"}], wram={0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, read={0xC5EA: 1}, expect={0xC5EA: b"\x01"}, expect_regs={"a": 0x01, "f": 0x10}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SetIRCommunicationErrorCode_Error

# >>> factory TryReceiveCardOrDeckConfigurationThroughIR
CONTRACT["TryReceiveCardOrDeckConfigurationThroughIR"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TryReceiveCardOrDeckConfigurationThroughIR"] = [
    {"oracle": False, "evidence": "primary", "why": "The deterministic CGB infrared peer supplies the request and then the receive-command frame; the communication error byte and carry return are asserted.", "a": 0x02, "keys": 0x81, "ir_peer": True, "wram": {0xCAB4: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC510: b"\xFF", 0xC5EA: b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}], "read": {0xC510: 1, 0xC5EA: 1}, "expect": {0xC510: b"\x00", 0xC5EA: b"\xFF"}, "expect_regs": {"a": 0x00, "f": 0x90}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The deterministic CGB infrared peer supplies the request and then the receive-command frame; the communication error byte and carry return are asserted with poisoned registers.", keys=0x81, ir_peer=True, wram={0xCAB4: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", 0xC510: b"\xFF", 0xC5EA: b"\x00"}, setup=[{"fn": "CopyDMAFunction"}], read={0xC510: 1, 0xC5EA: 1}, expect={0xC510: b"\x00", 0xC5EA: b"\xFF"}, expect_regs={"a": 0x00, "f": 0x90}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TryReceiveCardOrDeckConfigurationThroughIR

# >>> factory ExchangeIRCommunicationParameters
CONTRACT["ExchangeIRCommunicationParameters"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ExchangeIRCommunicationParameters"] = [
    {"oracle": False, "evidence": "primary", "why": "The deterministic native CGB infrared peer drives the parameter exchange into its communication-error path; the received parameter block and carry return are asserted.", "a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": 0x80, "ir_peer": True, "setup": [{"fn": "CopyDMAFunction"}], "wram": {0xCAB4: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, "read": {0xC5EF: 4}, "expect": {0xC5EF: b"\x00\x00\x00\x00"}, "expect_regs": {"a": 0x00, "f": 0x90}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The deterministic native CGB infrared peer drives the parameter exchange into its communication-error path with poisoned registers; the received parameter block and carry return are asserted.", keys=0x80, ir_peer=True, setup=[{"fn": "CopyDMAFunction"}], wram={0xCAB4: b"\x02", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, read={0xC5EF: 4}, expect={0xC5EF: b"\x00\x00\x00\x00"}, expect_regs={"a": 0x00, "f": 0x90}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ExchangeIRCommunicationParameters

# >>> factory _ReceiveCard
CONTRACT["_ReceiveCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_ReceiveCard"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block is observed.", "keys": [0x82, 0x10, 0x01], "wram": {0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wOwnIRCommunicationParams: 4}, "expect": {wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block is observed.", keys=[0x82, 0x10, 0x01], wram={0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wOwnIRCommunicationParams: 4}, expect={wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _ReceiveCard

# >>> factory _ReceiveDeckConfiguration
CONTRACT["_ReceiveDeckConfiguration"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_ReceiveDeckConfiguration"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block is observed.", "keys": [0x82, 0x10, 0x01], "wram": {0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wOwnIRCommunicationParams: 4}, "expect": {wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block is observed.", keys=[0x82, 0x10, 0x01], wram={0xCAB4: b"\x02", 0xC590: b"\x00", 0xD131: b"\x00", 0xD291: b"\x00", 0xD5D7: b"\x00", 0xCABB: b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wOwnIRCommunicationParams: 4}, expect={wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _ReceiveDeckConfiguration

# >>> factory PrepareSendCardOrDeckConfigurationThroughIR
CONTRACT["PrepareSendCardOrDeckConfigurationThroughIR"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PrepareSendCardOrDeckConfigurationThroughIR"] = [
    {"keys": 0x02, "sram": {0: {}}, "wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "setup": [{"fn": "CopyDMAFunction"}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=0x02, sram={0: {}}, wram={0xCABB: b"\x80", 0xFF40: b"\x80"}, setup=[{"fn": "CopyDMAFunction"}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrepareSendCardOrDeckConfigurationThroughIR

# >>> factory _SendCard
CONTRACT["_SendCard"] = {"compare": (), "preserve": ()}
CASES["_SendCard"] = [
    {"oracle": False, "evidence": "primary", "why": "The bounded prefix stops after the routine initial music shutdown before the scene and infrared handshake; the music state is asserted.", "read": {wCurSongID: 1}, "expect": {wCurSongID: b"\x00"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"oracle": False, "evidence": "primary", "why": "The bounded prefix stops after the routine initial music shutdown with poisoned registers; the music state is asserted.", "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "read": {wCurSongID: 1}, "expect": {wCurSongID: b"\x00"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
]
# <<< factory _SendCard

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
# >>> factory-mutation LoadLinkNotConnectedSceneAndAskWhetherToTryAgain
MUTATIONS["LoadLinkNotConnectedSceneAndAskWhetherToTryAgain"] = {"source_symbol": "LoadLinkNotConnectedSceneAndAskWhetherToTryAgain", "before": "\t(void)LoadScene(SCENE_GAMEBOY_LINK_NOT_CONNECTED, 0u, 0u, 0u, 0u, 0u, saved_hl);", "after": "\t(void)LoadScene(0u, 0u, 0u, 0u, 0u, 0u, saved_hl);", "case_ids": ["LoadLinkNotConnectedSceneAndAskWhetherToTryAgain-0", "LoadLinkNotConnectedSceneAndAskWhetherToTryAgain-1"]}
# <<< factory-mutation LoadLinkNotConnectedSceneAndAskWhetherToTryAgain
# >>> factory-mutation SetIRCommunicationErrorCode_NoError
MUTATIONS["SetIRCommunicationErrorCode_NoError"] = {
    "source_symbol": "SetIRCommunicationErrorCode_NoError",
    "before": "\twOwnIRCommunicationParams = 0u;",
    "after": "\twOwnIRCommunicationParams = 1u;",
    "case_ids": ["SetIRCommunicationErrorCode_NoError-0", "SetIRCommunicationErrorCode_NoError-1"]
}
# <<< factory-mutation SetIRCommunicationErrorCode_NoError
# >>> factory-mutation SetIRCommunicationErrorCode_Error
MUTATIONS["SetIRCommunicationErrorCode_Error"] = {
    "source_symbol": "SetIRCommunicationErrorCode_Error",
    "before": "SetIRCommunicationErrorCode_ErrorResult SetIRCommunicationErrorCode_Error(uint8_t a, uint8_t f, uint8_t b)\n{\n\twIRCommunicationErrorCode = 0x01u;",
    "after": "SetIRCommunicationErrorCode_ErrorResult SetIRCommunicationErrorCode_Error(uint8_t a, uint8_t f, uint8_t b)\n{\n\twIRCommunicationErrorCode = 0x00u;",
    "case_ids": ["SetIRCommunicationErrorCode_Error-0", "SetIRCommunicationErrorCode_Error-1"]
}
# <<< factory-mutation SetIRCommunicationErrorCode_Error
# >>> factory-mutation TryReceiveCardOrDeckConfigurationThroughIR
MUTATIONS["TryReceiveCardOrDeckConfigurationThroughIR"] = {
    "source_symbol": "TryReceiveCardOrDeckConfigurationThroughIR",
    "before": "TryReceiveCardOrDeckConfigurationThroughIRResult TryReceiveCardOrDeckConfigurationThroughIR(uint8_t a)\n{\n\tInitIRCommunications(a);\n\tfor (;;) {\n\t\twDuelTempList = 0u;",
    "after": "TryReceiveCardOrDeckConfigurationThroughIRResult TryReceiveCardOrDeckConfigurationThroughIR(uint8_t a)\n{\n\tInitIRCommunications(a);\n\tfor (;;) {\n\t\twDuelTempList = 1u;",
    "case_ids": ["TryReceiveCardOrDeckConfigurationThroughIR-0", "TryReceiveCardOrDeckConfigurationThroughIR-1"]
}
# <<< factory-mutation TryReceiveCardOrDeckConfigurationThroughIR
# >>> factory-mutation ExchangeIRCommunicationParameters
MUTATIONS["ExchangeIRCommunicationParameters"] = {
    "source_symbol": "ExchangeIRCommunicationParameters",
    "before": "error:\n\treturn (ExchangeIRCommunicationParametersResult){0u, 0x90u};",
    "after": "error:\n\treturn (ExchangeIRCommunicationParametersResult){0u, 0x00u};",
    "case_ids": ["ExchangeIRCommunicationParameters-0", "ExchangeIRCommunicationParameters-1"]
}
# <<< factory-mutation ExchangeIRCommunicationParameters
# >>> factory-mutation _ReceiveCard
MUTATIONS["_ReceiveCard"] = {"source_symbol": "_ReceiveCard", "before": "_ReceiveCardResult _ReceiveCard(void)\n{\n\tfor (;;) {\n\t\tStopMusic();\n\t\tLoadLinkConnectingScene(ReceivingACardText);\n\t\tTryReceiveCardOrDeckConfigurationThroughIRResult received =\n\t\t\tTryReceiveCardOrDeckConfigurationThroughIR(IRPARAM_SEND_CARDS);\n\t\tgb_write8((uint16_t)(wOwnIRCommunicationParams_ADDR + 1u), 0x4Fu);", "after": "_ReceiveCardResult _ReceiveCard(void)\n{\n\tfor (;;) {\n\t\tStopMusic();\n\t\tLoadLinkConnectingScene(ReceivingACardText);\n\t\tTryReceiveCardOrDeckConfigurationThroughIRResult received =\n\t\t\tTryReceiveCardOrDeckConfigurationThroughIR(IRPARAM_SEND_CARDS);\n\t\tgb_write8((uint16_t)(wOwnIRCommunicationParams_ADDR + 1u), 0x00u);", "case_ids": ["_ReceiveCard-0", "_ReceiveCard-1"]}
# <<< factory-mutation _ReceiveCard
# >>> factory-mutation _ReceiveDeckConfiguration
MUTATIONS["_ReceiveDeckConfiguration"] = {
    "source_symbol": "_ReceiveDeckConfiguration",
    "before": "\t\tTryReceiveCardOrDeckConfigurationThroughIRResult received = TryReceiveCardOrDeckConfigurationThroughIR(IRPARAM_SEND_DECK);",
    "after": "\t\tTryReceiveCardOrDeckConfigurationThroughIRResult received = TryReceiveCardOrDeckConfigurationThroughIR(0x00u);",
    "case_ids": ["_ReceiveDeckConfiguration-0", "_ReceiveDeckConfiguration-1"]
}
# <<< factory-mutation _ReceiveDeckConfiguration
# >>> factory-mutation PrepareSendCardOrDeckConfigurationThroughIR
MUTATIONS["PrepareSendCardOrDeckConfigurationThroughIR"] = {
    "source_symbol": "PrepareSendCardOrDeckConfigurationThroughIR",
    "before": "if ((hKeysPressed & 0x02u) != 0u)\n\t\t\treturn (PrepareSendCardOrDeckConfigurationThroughIRResult){1u, 0x10u};",
    "after": "if ((hKeysPressed & 0x02u) != 0u)\n\t\t\treturn (PrepareSendCardOrDeckConfigurationThroughIRResult){0u, 0x10u};",
    "case_ids": ["PrepareSendCardOrDeckConfigurationThroughIR-0", "PrepareSendCardOrDeckConfigurationThroughIR-1"],
}
# <<< factory-mutation PrepareSendCardOrDeckConfigurationThroughIR
# >>> factory-mutation _SendCard
MUTATIONS["_SendCard"] = {"source_symbol": "_SendCard", "before": "void _SendCard(void)\n{\n\tStopMusic();\n}", "after": "void _SendCard(void)\n{\n\tPlayCardPopSong();\n}", "case_ids": ["_SendCard-0", "_SendCard-1"]}
# <<< factory-mutation _SendCard
# >>> factory-completion _SendCard
for _record in SCHEMA2_CASES["_SendCard"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x5A1F}
# <<< factory-completion _SendCard
