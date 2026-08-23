POISON={"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234}
wTxRam2=0xCE3F;wMultichoiceTextboxResult_ChooseDeckToDuelAgainst=0xD695;wLoadedEventBits=0xD3D1;wEventVars=0xD3D2;EVENT_AARON_BOOSTER_REWARD=wEventVars+0x1A
CONTRACT={"Func_d96c":{"compare":("a","b","c","d","e","hl"),"preserve":("d","e")}}
CASES={"Func_d96c":[{"a":0,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},{"a":2,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},dict(POISON,a=2,wram={wTxRam2:b"\xff\xff\xff"},read={wTxRam2:3}),{"a":9,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},dict(POISON,a=0xFF,wram={wTxRam2:b"\xff\xff\xff"},read={wTxRam2:3})]}
# >>> factory-cases-statics
wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
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

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES=legacy_to_schema(CASES,CONTRACT)
MUTATIONS={"Func_d96c":{"source_symbol":"Func_d96c","before":"uint8_t offset=(uint8_t)((uint8_t)(a-2u)<<1);","after":"uint8_t offset=(uint8_t)((uint8_t)(a-1u)<<1);","case_ids":["Func_d96c-1","Func_d96c-2","Func_d96c-3"]}}
# >>> factory-mutation DeckMachineRoomCloseTextBox
MUTATIONS["DeckMachineRoomCloseTextBox"] = {"source_symbol": "DeckMachineRoomCloseTextBox", "before": "\tfor (uint8_t a = MAP_EVENT_FIGHTING_DECK_MACHINE; a <= MAP_EVENT_FIRE_DECK_MACHINE; a++)", "after": "\tfor (uint8_t a = MAP_EVENT_FIGHTING_DECK_MACHINE; a < MAP_EVENT_FIRE_DECK_MACHINE; a++)", "case_ids": ["DeckMachineRoomCloseTextBox-0", "DeckMachineRoomCloseTextBox-1"]}
# <<< factory-mutation DeckMachineRoomCloseTextBox
