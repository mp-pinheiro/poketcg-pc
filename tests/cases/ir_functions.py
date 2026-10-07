"""Oracle-diff cases for poketcg/src/engine/link/ir_functions.asm."""
from tests.cases._symbols import STACK_TOP, sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wCurSongID = sym("wCurSongID")

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
wOwnIRCommunicationParams = sym("wOwnIRCommunicationParams")
wIRCommunicationErrorCode = sym("wIRCommunicationErrorCode")
hWhoseTurn = sym("hWhoseTurn")
wNameBuffer = sym("wNameBuffer")
wOpponentName = sym("wOpponentName")
wDefaultText = sym("wDefaultText")
sPlayerName = sym("sPlayerName")
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
WRAM_SEED = {sym("wConsole"): b"\x00", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00"}
SCENE_READ = {sym("wConsole"): 1, sym("wBGP"): 1, sym("wCurTilemap"): 1, sym("wd291"): 1, sym("wSceneBaseX"): 1, sym("wSceneBaseY"): 1, sym("wSceneSGBPacketPtr"): 2, sym("wSceneSGBRoutinePtr"): 2}
TEXT_READ = {sym("wc600") + 0x20: 4, sym("wc700") + 0x20: 4, sym("wc800") + 0x20: 4, sym("wc900") + 0x20: 4, sym("wCurTextTile"): 2, sym("wFontWidth"): 1}

wCurSongID = sym("wCurSongID")
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
    {"a": 0x42, "wram": {sym("wVBlankFunctionTrampolineBackup"): b"\x34\x12", 0xFF56: b"\x01"}, "read": {0xFF56: 1, sym("wVBlankFunctionTrampoline") + 1: 2}},
    dict(POISON, wram={sym("wVBlankFunctionTrampolineBackup"): b"\x78\x56", 0xFF56: b"\x01"}, read={0xFF56: 1, sym("wVBlankFunctionTrampoline") + 1: 2}),
    {"a": 0x00, "wram": {sym("wVBlankFunctionTrampolineBackup"): b"\x00\x00"}, "read": {0xFF56: 1, sym("wVBlankFunctionTrampoline") + 1: 2}},
]
# <<< factory ClearRPAndRestoreVBlankFunction

# >>> factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain
CONTRACT["LoadLinkNotConnectedSceneAndAskWhetherToTryAgain"] = {"compare": ("a", "f"), "preserve": ()}
CASES["LoadLinkNotConnectedSceneAndAskWhetherToTryAgain"] = [
    {"hl": 0x0000,"wram": {**WRAM_SEED, sym("wLCDC"): b"\x00"},"sram": {0: {}},"setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}],"keys": [0x00, 0x01],"read": {**SCENE_READ, **TEXT_READ},"instruction_budget": 20000000,"cycle_budget": 80000000},
    dict(POISON, hl=0x0000, wram={**WRAM_SEED, sym("wLCDC"): b"\x00"}, sram={0: {}}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], keys=[0x00, 0x01], read={**SCENE_READ, **TEXT_READ}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory LoadLinkNotConnectedSceneAndAskWhetherToTryAgain

# >>> factory SetIRCommunicationErrorCode_NoError
CONTRACT["SetIRCommunicationErrorCode_NoError"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SetIRCommunicationErrorCode_NoError"] = [
    {"oracle": False, "evidence": "primary", "why": "The deterministic native CGB infrared peer drives the receive request; clearing the own-communication parameter and the error return are asserted.", "a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": 0x81, "ir_peer": True, "setup": [{"fn": "CopyDMAFunction"}], "wram": {sym("wConsole"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", sym("wOwnIRCommunicationParams"): b"\xFF"}, "read": {sym("wOwnIRCommunicationParams"): 1}, "expect": {sym("wOwnIRCommunicationParams"): b"\x00"}, "expect_regs": {"a": 0xFF, "f": 0x10}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The deterministic native CGB infrared peer drives the receive request with poisoned registers; clearing the own-communication parameter and the error return are asserted.", keys=0x81, ir_peer=True, setup=[{"fn": "CopyDMAFunction"}], wram={sym("wConsole"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", sym("wOwnIRCommunicationParams"): b"\xFF"}, read={sym("wOwnIRCommunicationParams"): 1}, expect={sym("wOwnIRCommunicationParams"): b"\x00"}, expect_regs={"a": 0xFF, "f": 0x10}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SetIRCommunicationErrorCode_NoError

# >>> factory SetIRCommunicationErrorCode_Error
CONTRACT["SetIRCommunicationErrorCode_Error"] = {"compare": ("a", "f"), "preserve": ()}
CASES["SetIRCommunicationErrorCode_Error"] = [
    {"oracle": False, "evidence": "primary", "why": "Infrared peer hardware is unavailable to the reference runner; the native peer path verifies the error-code write and communication shutdown.", "keys": 0x81, "ir_peer": True, "setup": [{"fn": "CopyDMAFunction"}], "wram": {sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, "read": {sym("wIRCommunicationErrorCode"): 1}, "expect": {sym("wIRCommunicationErrorCode"): b"\x01"}, "expect_regs": {"a": 0x01, "f": 0x10}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="Infrared peer hardware is unavailable to the reference runner; the native peer path verifies the error-code write and communication shutdown with poisoned registers.", keys=0x81, ir_peer=True, setup=[{"fn": "CopyDMAFunction"}], wram={sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, read={sym("wIRCommunicationErrorCode"): 1}, expect={sym("wIRCommunicationErrorCode"): b"\x01"}, expect_regs={"a": 0x01, "f": 0x10}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory SetIRCommunicationErrorCode_Error

# >>> factory TryReceiveCardOrDeckConfigurationThroughIR
CONTRACT["TryReceiveCardOrDeckConfigurationThroughIR"] = {"compare": ("a", "f"), "preserve": ()}
CASES["TryReceiveCardOrDeckConfigurationThroughIR"] = [
    {"oracle": False, "evidence": "primary", "why": "The deterministic CGB infrared peer supplies the request and then the receive-command frame; the communication error byte and carry return are asserted.", "a": 0x02, "keys": 0x81, "ir_peer": True, "wram": {sym("wConsole"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", sym("wDuelTempList"): b"\xFF", sym("wIRCommunicationErrorCode"): b"\x00"}, "setup": [{"fn": "CopyDMAFunction"}], "read": {sym("wDuelTempList"): 1, sym("wIRCommunicationErrorCode"): 1}, "expect": {sym("wDuelTempList"): b"\x00", sym("wIRCommunicationErrorCode"): b"\xFF"}, "expect_regs": {"a": 0x00, "f": 0x90}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The deterministic CGB infrared peer supplies the request and then the receive-command frame; the communication error byte and carry return are asserted with poisoned registers.", keys=0x81, ir_peer=True, wram={sym("wConsole"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", sym("wDuelTempList"): b"\xFF", sym("wIRCommunicationErrorCode"): b"\x00"}, setup=[{"fn": "CopyDMAFunction"}], read={sym("wDuelTempList"): 1, sym("wIRCommunicationErrorCode"): 1}, expect={sym("wDuelTempList"): b"\x00", sym("wIRCommunicationErrorCode"): b"\xFF"}, expect_regs={"a": 0x00, "f": 0x90}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory TryReceiveCardOrDeckConfigurationThroughIR

# >>> factory ExchangeIRCommunicationParameters
CONTRACT["ExchangeIRCommunicationParameters"] = {"compare": ("a", "f"), "preserve": ()}
CASES["ExchangeIRCommunicationParameters"] = [
    {"oracle": False, "evidence": "primary", "why": "The deterministic native CGB infrared peer drives the parameter exchange into its communication-error path; the received parameter block and carry return are asserted.", "a": 0x00, "f": 0x00, "b": 0x00, "c": 0x00, "d": 0x00, "e": 0x00, "hl": 0x0000, "keys": 0x80, "ir_peer": True, "setup": [{"fn": "CopyDMAFunction"}], "wram": {sym("wConsole"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, "read": {sym("wOtherIRCommunicationParams"): 4}, "expect": {sym("wOtherIRCommunicationParams"): b"\x00\x00\x00\x00"}, "expect_regs": {"a": 0x00, "f": 0x90}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The deterministic native CGB infrared peer drives the parameter exchange into its communication-error path with poisoned registers; the received parameter block and carry return are asserted.", keys=0x80, ir_peer=True, setup=[{"fn": "CopyDMAFunction"}], wram={sym("wConsole"): b"\x02", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00"}, read={sym("wOtherIRCommunicationParams"): 4}, expect={sym("wOtherIRCommunicationParams"): b"\x00\x00\x00\x00"}, expect_regs={"a": 0x00, "f": 0x90}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory ExchangeIRCommunicationParameters

# >>> factory _ReceiveCard
CONTRACT["_ReceiveCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_ReceiveCard"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block is observed.", "keys": [0x82, 0x10, 0x01], "wram": {sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wOwnIRCommunicationParams: 4}, "expect": {wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block is observed.", keys=[0x82, 0x10, 0x01], wram={sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wOwnIRCommunicationParams: 4}, expect={wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _ReceiveCard

# >>> factory _ReceiveDeckConfiguration
CONTRACT["_ReceiveDeckConfiguration"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_ReceiveDeckConfiguration"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block is observed.", "keys": [0x82, 0x10, 0x01], "wram": {sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wOwnIRCommunicationParams: 4}, "expect": {wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The disconnected CGB infrared path deterministically reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block is observed.", keys=[0x82, 0x10, 0x01], wram={sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wOwnIRCommunicationParams: 4}, expect={wOwnIRCommunicationParams: b"\x02\x4F\x4B\x31"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _ReceiveDeckConfiguration

# >>> factory PrepareSendCardOrDeckConfigurationThroughIR
CONTRACT["PrepareSendCardOrDeckConfigurationThroughIR"] = {"compare": ("a", "f"), "preserve": ()}
CASES["PrepareSendCardOrDeckConfigurationThroughIR"] = [
    {"keys": 0x02, "sram": {0: {}}, "wram": {sym("wLCDC"): b"\x80", 0xFF40: b"\x80"}, "setup": [{"fn": "CopyDMAFunction"}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=0x02, sram={0: {}}, wram={sym("wLCDC"): b"\x80", 0xFF40: b"\x80"}, setup=[{"fn": "CopyDMAFunction"}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PrepareSendCardOrDeckConfigurationThroughIR

# >>> factory _SendCard
CONTRACT["_SendCard"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_SendCard"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically cancels the send with B, reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block and the card-pop song are observed.", "keys": [0x02, 0x00, 0x01, 0x00, 0x10, 0x00, 0x01], "entry_sp": STACK_TOP - 2, "wram": {sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wOwnIRCommunicationParams: 4, wCurSongID: 1}, "expect": {wOwnIRCommunicationParams: b"\x02\x50\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The disconnected CGB infrared path deterministically cancels the send with B, reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block and the card-pop song are observed.", keys=[0x02, 0x00, 0x01, 0x00, 0x10, 0x00, 0x01], entry_sp=STACK_TOP - 2, wram={sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wOwnIRCommunicationParams: 4, wCurSongID: 1}, expect={wOwnIRCommunicationParams: b"\x02\x50\x4B\x31"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _SendCard

# >>> factory _SendDeckConfiguration
CONTRACT["_SendDeckConfiguration"] = {"compare": ("a", "f"), "preserve": ()}
CASES["_SendDeckConfiguration"] = [
    {"oracle": False, "evidence": "primary", "why": "The disconnected CGB infrared path deterministically cancels the send with B, reaches the retry screen and returns through its no-retry carry exit; the own communication parameter block and the card-pop song are observed.", "keys": [0x02, 0x00, 0x01, 0x00, 0x10, 0x00, 0x01], "entry_sp": STACK_TOP - 2, "wram": {sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "read": {wOwnIRCommunicationParams: 4, wCurSongID: 1}, "expect": {wOwnIRCommunicationParams: b"\x03\x50\x4B\x31"}, "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, oracle=False, evidence="primary", why="The disconnected CGB infrared path deterministically cancels the send with B, reaches the retry screen and returns through its no-retry carry exit with poisoned registers; the own communication parameter block and the card-pop song are observed.", keys=[0x02, 0x00, 0x01, 0x00, 0x10, 0x00, 0x01], entry_sp=STACK_TOP - 2, wram={sym("wConsole"): b"\x02", sym("wCurDeckCardChanges"): b"\x00", sym("wCurTilemap"): b"\x00", sym("wd291"): b"\x00", sym("wAllSpriteAnimationsDisabled"): b"\x00", sym("wLCDC"): b"\x80", 0xFF40: b"\x80", 0xFF4D: b"\x00", wOwnIRCommunicationParams: b"\xFF\xFF\xFF\xFF"}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], read={wOwnIRCommunicationParams: 4, wCurSongID: 1}, expect={wOwnIRCommunicationParams: b"\x03\x50\x4B\x31"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory _SendDeckConfiguration

from tests.cases._schema_migration import legacy_to_schema

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
for _case, _name in zip(SCHEMA2_CASES["PlayCardPopSong"], ("zero", "poison", "boundary")):
    _case["id"] = f"PlayCardPopSong-{_name}"

MUTATIONS = {
    "PlayCardPopSong": {
        "source_symbol": "PlayCardPopSong",
        "before": "PlaySong(MUSIC_CARD_POP);",
        "after": "PlaySong((uint8_t)(MUSIC_CARD_POP + 1u));",
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
MUTATIONS["_SendCard"] = {"source_symbol": "_SendCard", "before": "PrepareSendCardOrDeckConfigurationThroughIR(IRPARAM_SEND_CARDS, 0x20u,", "after": "PrepareSendCardOrDeckConfigurationThroughIR(IRPARAM_SEND_DECK, 0x20u,", "case_ids": ["_SendCard-0", "_SendCard-1"]}
# <<< factory-mutation _SendCard
# >>> factory-mutation _SendDeckConfiguration
MUTATIONS["_SendDeckConfiguration"] = {"source_symbol": "_SendDeckConfiguration", "before": "PrepareSendCardOrDeckConfigurationThroughIR(IRPARAM_SEND_DECK, 0x20u,", "after": "PrepareSendCardOrDeckConfigurationThroughIR(IRPARAM_SEND_CARDS, 0x20u,", "case_ids": ["_SendDeckConfiguration-0", "_SendDeckConfiguration-1"]}
# <<< factory-mutation _SendDeckConfiguration
