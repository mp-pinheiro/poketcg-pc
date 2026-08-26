POISON={"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234}
wTxRam2=0xCE3F;wMultichoiceTextboxResult_ChooseDeckToDuelAgainst=0xD695;wLoadedEventBits=0xD3D1;wEventVars=0xD3D2;EVENT_AARON_BOOSTER_REWARD=wEventVars+0x1A
CONTRACT={"Func_d96c":{"compare":("a","b","c","d","e","hl"),"preserve":("d","e")}}
CASES={"Func_d96c":[{"a":0,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},{"a":2,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},dict(POISON,a=2,wram={wTxRam2:b"\xff\xff\xff"},read={wTxRam2:3}),{"a":9,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},dict(POISON,a=0xFF,wram={wTxRam2:b"\xff\xff\xff"},read={wTxRam2:3})]}
# >>> factory-cases-statics
wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292

wDuelResult = 0xCC08
wNPCDuelist = 0xCC07

wEventVars = 0xD3D2
wLCDC = 0xCABB
wTxRam2 = 0xCE3F
POISON={"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234}
# <<< factory-cases-statics

# >>> factory DeckMachineRoomCloseTextBox
CONTRACT["DeckMachineRoomCloseTextBox"] = {"compare": (), "preserve": ()}
CASES["DeckMachineRoomCloseTextBox"] = [
    {"wram": {wOWMapEvents + 1: bytes([0xFF] * 10)},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents + 1: 10}},
    {"wram": {wOWMapEvents + 1: bytes([0x22] * 10)},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents + 1: 10}},
    dict(POISON, wram={wOWMapEvents + 1: bytes([0x33] * 10)},
         read={wWriteBGMapToSRAM: 1, wOWMapEvents + 1: 10}),
]
# <<< factory DeckMachineRoomCloseTextBox

# >>> factory DeckMachineRoomAfterDuel
CONTRACT["DeckMachineRoomAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["DeckMachineRoomAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {wDuelResult: b"\x00", wNPCDuelist: b"\x63"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory DeckMachineRoomAfterDuel

# >>> factory Script_da76
CONTRACT["Script_da76"] = {"compare": (), "preserve": ()}
CASES["Script_da76"] = [
    {"keys": [0x00, 0x01], "wram": {0xCABB: b"\x80", 0xFF40: b"\x80"}, "read": {0xCABB: 1, 0xCE3F: 3}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xCABB: b"\x80", 0xFF40: b"\x80"}, read={0xCABB: 1, 0xCE3F: 3}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Script_da76

# >>> factory Script_da1c
CONTRACT["Script_da1c"] = {"compare": (), "preserve": ()}
CASES["Script_da1c"] = [
    {"keys": [0x00, 0x01], "wram": {0xCABB: b"\x00", 0xFF40: b"\x00", 0xCE3F: b"\xFF\xFF\xFF"}, "read": {0xCE3F: 3, 0xFF40: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    {"keys": [0x00, 0x01], "wram": {0xCABB: b"\x00", 0xFF40: b"\x00", 0xCE3F: b"\xFF\xFF\xFF"}, "read": {0xCE3F: 3, 0xFF40: 1}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01], wram={0xCABB: b"\x00", 0xFF40: b"\x00", 0xCE3F: b"\xFF\xFF\xFF"}, read={0xCE3F: 3, 0xFF40: 1}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000)]
# <<< factory Script_da1c

# >>> factory Script_d9c2
CONTRACT["Script_d9c2"] = {"compare": (), "preserve": ()}
CASES["Script_d9c2"] = [
    {"keys": [0x00, 0x01, 0x00, 0x01], "wram": {wEventVars: b"\x00" * 0x40, wLCDC: b"\x00", wTxRam2: b"\x00\x00\x00"}, "read": {wEventVars: 0x40, wLCDC: 1, wTxRam2: 3}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01, 0x00, 0x01], wram={wEventVars: b"\x00" * 0x40, wLCDC: b"\x00", wTxRam2: b"\x00\x00\x00"}, read={wEventVars: 0x40, wLCDC: 1, wTxRam2: 3}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Script_d9c2

# >>> factory Script_d9ef
CONTRACT["Script_d9ef"] = {"compare": (), "preserve": ()}
CASES["Script_d9ef"] = [
    {"keys": [0x00, 0x01, 0x00, 0x01], "wram": {wEventVars: b"\x00" * 0x40, wLCDC: b"\x00", wTxRam2: b"\x00\x00\x00"}, "read": {wEventVars: 0x40, wLCDC: 1, wTxRam2: 3}, "setup": [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], "instruction_budget": 20000000, "cycle_budget": 80000000},
    dict(POISON, keys=[0x00, 0x01, 0x00, 0x01], wram={wEventVars: b"\x00" * 0x40, wLCDC: b"\x00", wTxRam2: b"\x00\x00\x00"}, read={wEventVars: 0x40, wLCDC: 1, wTxRam2: 3}, setup=[{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}], instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory Script_d9ef

# >>> factory Script_BeatAaron
# The routine's code is 8 bytes; `set_event_value` is `call SetStackEventValue` +
# `db $73`, and the callee returns PAST the db to the `rst $20` at $590B that
# starts the script bytecode. $590B is therefore the end of this routine's code,
# and every case declares completion pre-ret there. Running past the rst enters
# the overworld script interpreter, which needs ambient scene state a per-routine
# probed call cannot supply -- that is scene-level replay, not a port.
#
# SetEventValue writes (~mask & [hl]) | ((c << tz(mask)) & mask). Verified against
# the ROM 2026-08-26: EventVarMasks[0x73] = (offset 0x1A, mask 0x03), so the
# shift-alignment loop runs zero times. Cases cover both mask bits, the all-clear
# value, the 0xFF truncation, and a pre-set neighbour nibble so the ~mask
# preservation of the untouched bits is actually observed.
CONTRACT["Script_BeatAaron"] = {"compare": ("a", "c"), "preserve": ("b", "d", "e", "hl")}
CASES["Script_BeatAaron"] = [
    # Index 0 must seed the untouched bits NON-ZERO, or the mutation flipping
    # `& ~mask` to `& mask` is invisible: with the event var at 0x00 both forms
    # yield 0 and the corrupted routine passes.
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\x03",
              EVENT_AARON_BOOSTER_REWARD: b"\xFC"},
     "read": {wLoadedEventBits: 1, EVENT_AARON_BOOSTER_REWARD: 1}},
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\x02",
              EVENT_AARON_BOOSTER_REWARD: b"\x00"},
     "read": {wLoadedEventBits: 1, EVENT_AARON_BOOSTER_REWARD: 1}},
    {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
     "wram": {wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\x00",
              EVENT_AARON_BOOSTER_REWARD: b"\x03"},
     "read": {wLoadedEventBits: 1, EVENT_AARON_BOOSTER_REWARD: 1}},
    dict(POISON,
         wram={wMultichoiceTextboxResult_ChooseDeckToDuelAgainst: b"\xFF",
               EVENT_AARON_BOOSTER_REWARD: b"\xF0"},
         read={wLoadedEventBits: 1, EVENT_AARON_BOOSTER_REWARD: 1}),
]
# <<< factory Script_BeatAaron

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES=legacy_to_schema(CASES,CONTRACT)
# >>> factory-completion Script_BeatAaron
# $590B is the `rst $20` that begins Script_BeatAaron's script bytecode; the
# routine's code ends there. legacy_to_schema always emits completion "return",
# so the split is applied after migration.
for _rec in SCHEMA2_CASES["Script_BeatAaron"]:
    _rec["completion"] = {"mode": "pre-ret", "pc": 0x590B}
# <<< factory-completion Script_BeatAaron
MUTATIONS={"Func_d96c":{"source_symbol":"Func_d96c","before":"uint8_t offset=(uint8_t)((uint8_t)(a-2u)<<1);","after":"uint8_t offset=(uint8_t)((uint8_t)(a-1u)<<1);","case_ids":["Func_d96c-1","Func_d96c-2","Func_d96c-3"]}}
# >>> factory-mutation DeckMachineRoomCloseTextBox
MUTATIONS["DeckMachineRoomCloseTextBox"] = {"source_symbol": "DeckMachineRoomCloseTextBox", "before": "\tfor (uint8_t a = MAP_EVENT_FIGHTING_DECK_MACHINE; a <= MAP_EVENT_FIRE_DECK_MACHINE; a++)", "after": "\tfor (uint8_t a = MAP_EVENT_FIGHTING_DECK_MACHINE; a < MAP_EVENT_FIRE_DECK_MACHINE; a++)", "case_ids": ["DeckMachineRoomCloseTextBox-0", "DeckMachineRoomCloseTextBox-1"]}
# <<< factory-mutation DeckMachineRoomCloseTextBox
# >>> factory-mutation DeckMachineRoomAfterDuel
MUTATIONS["DeckMachineRoomAfterDuel"] = {"source_symbol": "DeckMachineRoomAfterDuel", "before": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript(DeckMachineRoomAfterDuelTable);", "after": "\tFindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(DeckMachineRoomAfterDuelTable + 1u));", "case_ids": ["DeckMachineRoomAfterDuel-0", "DeckMachineRoomAfterDuel-1"]}
# <<< factory-mutation DeckMachineRoomAfterDuel
# >>> factory-mutation Script_da76
MUTATIONS["Script_da76"] = {"source_symbol": "Script_da76", "before": "\tuint8_t copy_length = PKMN_CARD_DATA_LENGTH;", "after": "\tuint8_t copy_length = 0x40u;", "case_ids": ["Script_da76-0", "Script_da76-1"]}
# <<< factory-mutation Script_da76
# >>> factory-mutation Script_da1c
MUTATIONS["Script_da1c"] = {"source_symbol": "Script_da1c", "before": "\tFuncD96cResult result = Func_d96c(0x06u);", "after": "\tFuncD96cResult result = Func_d96c(0x07u);", "case_ids": ["Script_da1c-0", "Script_da1c-1", "Script_da1c-2"]}
# <<< factory-mutation Script_da1c
# >>> factory-mutation Script_d9c2
MUTATIONS["Script_d9c2"] = {"source_symbol": "Script_d9c2", "before": "\tFuncD96cResult card = Func_d96c(4u);", "after": "\tFuncD96cResult card = Func_d96c(3u);", "case_ids": ["Script_d9c2-0", "Script_d9c2-1"]}
# <<< factory-mutation Script_d9c2
# >>> factory-mutation Script_d9ef
MUTATIONS["Script_d9ef"] = {"source_symbol": "Script_d9ef", "before": "void Script_d9ef(void)\n{\n\tFuncD96cResult card = Func_d96c(5u);", "after": "void Script_d9ef(void)\n{\n\tFuncD96cResult card = Func_d96c(6u);", "case_ids": ["Script_d9ef-0", "Script_d9ef-1"]}
# <<< factory-mutation Script_d9ef
# >>> factory-mutation Script_BeatAaron
MUTATIONS["Script_BeatAaron"] = {
    "source_symbol": "Script_BeatAaron",
    "before": "\twritten = (uint8_t)((event & (uint8_t)~EVENT_AARON_BOOSTER_REWARD_MASK)",
    "after": "\twritten = (uint8_t)((event & (uint8_t)EVENT_AARON_BOOSTER_REWARD_MASK)",
    "case_ids": ["Script_BeatAaron-0", "Script_BeatAaron-1", "Script_BeatAaron-2"],
}
# <<< factory-mutation Script_BeatAaron
