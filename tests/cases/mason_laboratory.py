"""Oracle-diff cases for poketcg/src/scripts/mason_laboratory.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wEventVars = 0xD3D2
wLoadNPCXPos = 0xD3AC
wLoadNPCYPos = 0xD3AD
EVENT_MASON_LAB_STATE_BYTE = wEventVars + 0x0D

def npc_pos(state_byte, x=0x55, y=0x66):
    return {EVENT_MASON_LAB_STATE_BYTE: bytes((state_byte,)),
            wLoadNPCXPos: bytes((x,)), wLoadNPCYPos: bytes((y,))}

NPC_POS_READ = {EVENT_MASON_LAB_STATE_BYTE: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1}

wDuelResult = 0xD0C3
wNPCDuelist = 0xD0C4
wTempNPC = 0xD3AB
wLoadedNPCs = 0xD34A
wLoadedNPCTempIndex = 0xD3AA
wScriptNPC = 0xD3B6
wPlayerDirection = 0xD334
wOverworldNPCFlags = 0xD0C1
wNextScript = 0xD0C6
wOverworldMode = 0xD0BF

wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
wCurTilemap = 0xD131
wConsole = 0xCAB4
wPermissionMap = 0xD133
# <<< factory-cases-statics

# >>> factory Preload_DrMason
CONTRACT["Preload_DrMason"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["Preload_DrMason"] = [
    {"wram": npc_pos(0x00), "read": NPC_POS_READ},
    dict(POISON, wram=npc_pos(0xFF), read=NPC_POS_READ),
    {"wram": npc_pos(0x02), "read": NPC_POS_READ},
    dict(POISON, wram=npc_pos(0xF2), read=NPC_POS_READ),
    {"wram": npc_pos(0x04), "read": NPC_POS_READ},
]
# <<< factory Preload_DrMason

# >>> factory Preload_Sam
# EVENT_MASON_LAB_STATE is wEventVars+$0D bits 1-3; the macro leaves that
# mask ($0E) in wLoadedEventBits. State 0 moves Sam to ($0a,$08) facing south
# and returns a=SOUTH; state 1 is the `cp` Z path (f=$90); anything higher
# leaves the map data alone.
wLoadNPCDirection = 0xD3AE
wLoadedEventBits = 0xD3D1

def sam_pos(state_byte, x=0x55, y=0x66, direction=0x77):
    return {EVENT_MASON_LAB_STATE_BYTE: bytes((state_byte,)),
            wLoadNPCXPos: bytes((x,)), wLoadNPCYPos: bytes((y,)),
            wLoadNPCDirection: bytes((direction,)), wLoadedEventBits: b"\x00"}

SAM_READ = {EVENT_MASON_LAB_STATE_BYTE: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1,
            wLoadNPCDirection: 1, wLoadedEventBits: 1}

CONTRACT["Preload_Sam"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e", "hl"),
}
CASES["Preload_Sam"] = [
    {"wram": sam_pos(0x00), "read": SAM_READ},
    dict(POISON, wram=sam_pos(0xF1), read=SAM_READ),
    {"wram": sam_pos(0x02), "read": SAM_READ},
    dict(POISON, wram=sam_pos(0xF3), read=SAM_READ),
    {"wram": sam_pos(0x04), "read": SAM_READ},
    dict(POISON, wram=sam_pos(0x0E), read=SAM_READ),
]
# <<< factory Preload_Sam

# >>> factory Preload_Tech5
# EVENT_RECEIVED_LEGENDARY_CARDS is wEventVars+$06 bit 1 (mask $02). Set, the
# technician's X advances by two and hl is left on wLoadNPCXPos; clear, the
# `or a` Z path returns f=$90 with hl untouched.
EVENT_LEGENDARY_BYTE = wEventVars + 0x06

def tech5_pos(event_byte, x=0x55):
    return {EVENT_LEGENDARY_BYTE: bytes((event_byte,)), wLoadNPCXPos: bytes((x,)),
            wLoadedEventBits: b"\x00"}

TECH5_READ = {EVENT_LEGENDARY_BYTE: 1, wLoadNPCXPos: 1, wLoadedEventBits: 1}

CONTRACT["Preload_Tech5"] = {
    "compare": ("a", "f", "b", "c", "d", "e", "hl"),
    "preserve": ("b", "c", "d", "e"),
}
CASES["Preload_Tech5"] = [
    {"wram": tech5_pos(0x00), "read": TECH5_READ},
    dict(POISON, wram=tech5_pos(0xFD), read=TECH5_READ),
    {"wram": tech5_pos(0x02), "read": TECH5_READ},
    dict(POISON, wram=tech5_pos(0xFF, x=0xFE), read=TECH5_READ),
]
# <<< factory Preload_Tech5

# >>> factory MasonLaboratoryAfterDuel
CONTRACT["MasonLaboratoryAfterDuel"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": (), "wram_out": True}
CASES["MasonLaboratoryAfterDuel"] = [
    {"wram": {wDuelResult: b"\x01", wNPCDuelist: b"\x99"}},
    {"wram": {
        wDuelResult: b"\x00",
        wNPCDuelist: b"\x07",
        wLoadedNPCs: b"\x07" + b"\x00" * 95,
        wLoadedNPCTempIndex: b"\xEE",
        wScriptNPC: b"\xAA",
        wPlayerDirection: b"\x01",
        wOverworldNPCFlags: b"\x00",
        wNextScript: b"\xFF\xFF",
        wOverworldMode: b"\x00",
    }, "expect": {wTempNPC: b"\x07", wScriptNPC: b"\x00", wOverworldMode: b"\x03"}},
    dict(POISON, wram={wDuelResult: b"\x01", wNPCDuelist: b"\x99"}),
]
# <<< factory MasonLaboratoryAfterDuel

# >>> factory MasonLabCloseTextBox
CONTRACT["MasonLabCloseTextBox"] = {"compare": (), "preserve": ()}
CASES["MasonLabCloseTextBox"] = [
    {"wram": {wOWMapEvents + 9: b"\x00\x01\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents + 9: 3, wPermissionMap: 256}},
    {"wram": {wOWMapEvents + 9: b"\x00\x02\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents + 9: 3, wPermissionMap: 256}},
    dict(POISON, wram={wOWMapEvents + 9: b"\x00\x03\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
         read={wWriteBGMapToSRAM: 1, wOWMapEvents + 9: 3, wPermissionMap: 256}),
]
# <<< factory MasonLabCloseTextBox

# >>> factory MasonLabLoadMap
# mason_laboratory.asm:21-29. EVENT_MASON_LAB_STATE is wEventVars+$0D bits 1-3
# (scripting.asm EventVarMasks), so the state is seeded shifted left one.
_LAB_STATE_BYTE = wEventVars + 0x0D
CONTRACT["MasonLabLoadMap"] = {"compare": (), "preserve": ()}
CASES["MasonLabLoadMap"] = [
    # State 0: Dr Mason is looked up and the first-visit script is queued.
    {"wram": {_LAB_STATE_BYTE: b"\x00", wTempNPC: b"\x00", wNextScript: b"\x00\x00"},
     "read": {wTempNPC: 1, wNextScript: 2}},
    # State 3 == MASON_LAB_RECEIVED_STARTER_DECK: `ret nc`, nothing written.
    {"wram": {_LAB_STATE_BYTE: b"\x06", wTempNPC: b"\x00", wNextScript: b"\x00\x00"},
     "read": {wTempNPC: 1, wNextScript: 2}},
    # State 4: above the threshold, same early exit.
    {"wram": {_LAB_STATE_BYTE: b"\x08", wTempNPC: b"\x00", wNextScript: b"\x00\x00"},
     "read": {wTempNPC: 1, wNextScript: 2}},
    dict(POISON, wram={_LAB_STATE_BYTE: b"\x00", wTempNPC: b"\x00", wNextScript: b"\x00\x00"},
         read={wTempNPC: 1, wNextScript: 2}),
]
# <<< factory MasonLabLoadMap

# >>> factory MasonLabPressedA
# mason_laboratory.asm:31-37. EVENT_RECEIVED_LEGENDARY_CARDS is wEventVars+$06
# bit 1. ChallengeMachineObjectTable ($03:5572) holds (x, y, direction) triples
# 10,4,NORTH and 12,4,NORTH, matched against the player's own position
# (fire_club_lobby.asm:26-42).
_LEGENDARY_BYTE = wEventVars + 0x06
wPlayerXCoord = 0xD330
wPlayerYCoord = 0xD331
wPlayerDirection = 0xD334

def _pressed_a(legendary, x, y, direction):
    return {_LEGENDARY_BYTE: bytes((legendary,)),
            wPlayerXCoord: bytes((x,)), wPlayerYCoord: bytes((y,)),
            wPlayerDirection: bytes((direction,)),
            wNextScript: b"\x00\x00"}

_PRESSED_A_READ = {wNextScript: 2}
CONTRACT["MasonLabPressedA"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ()}
CASES["MasonLabPressedA"] = [
    # Legendary cards not received: `or a / ret z` before any search.
    {"wram": _pressed_a(0x00, 10, 4, 0x00), "read": dict(_PRESSED_A_READ)},
    # Received, standing at the first table entry: the search reports found.
    {"wram": _pressed_a(0x02, 10, 4, 0x00), "read": dict(_PRESSED_A_READ)},
    # Received, standing at the second entry.
    {"wram": _pressed_a(0x02, 12, 4, 0x00), "read": dict(_PRESSED_A_READ)},
    # Received but facing the wrong way: walks the table to its terminator.
    {"wram": _pressed_a(0x02, 10, 4, 0x02), "read": dict(_PRESSED_A_READ)},
    # Received, nowhere near either entry.
    {"wram": _pressed_a(0x02, 0x33, 0x44, 0x00), "read": dict(_PRESSED_A_READ)},
    dict(POISON, wram=_pressed_a(0x02, 10, 4, 0x00), read=dict(_PRESSED_A_READ)),
]
# <<< factory MasonLabPressedA

from tests.cases._schema_migration import legacy_to_schema

# >>> factory Script_Tech1
# mason_laboratory.asm:58-90. Two paths, each ending in its own `rst $20`, so
# each case declares the completion pc its seed reaches:
#   total >= 10 -> the `start_script` rst at $5597
#   total <  10 -> .low_on_energies grants 10 of each of the six energy cards,
#                  then the rst at $55B5
# The pc is derived from each case's own seeded counts, so the two cannot drift.
#
# Collection slots are CARD_SLOT(sCardCollection, id) = 0xA100 | id, so the six
# energy cards (EnergyCardList 03:55C4 = 01..06) sit at 0xA101..0xA106 and the
# count is the low 7 bits. The low path grants +10 per card, which the sread span
# observes directly (01 -> 0x0B).
#
# Index 0 is the EXACT cp boundary, total == 10: widening `>= 10` to `> 10` is
# invisible at every other total, so only this case reds the mutation.
_TECH1_COLL = 0xA100
_TECH1_BUDGET = {"instruction_budget": 60000000, "cycle_budget": 240000000}
_TECH1_RST = {True: 0x5597, False: 0x55B5}  # keyed by "total >= 10"
_TECH1_SEEDS = (
    (2, 2, 2, 2, 1, 1),   # total 10 -- the exact cp boundary, high path
    (2, 2, 2, 2, 2, 2),   # total 12 -- high path
    (1, 1, 1, 1, 1, 1),   # total 6 -- low path, grants 60 cards
    (2, 2, 2, 1, 1, 1),   # total 9 -- one below the boundary, low path
    (2, 2, 2, 2, 2, 2),   # POISON registers, high path
)

def _tech1_page(counts):
    page = bytearray(256)
    for _i, _n in enumerate(counts, start=1):
        page[_i] = _n
    return bytes(page)

CONTRACT["Script_Tech1"] = {"compare": ("a", "b", "c", "hl"), "preserve": ()}
CASES["Script_Tech1"] = []
for _i, _counts in enumerate(_TECH1_SEEDS):
    _base = dict(POISON) if _i == 4 else {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}
    _base["sram"] = {0: {_TECH1_COLL: _tech1_page(_counts)}}
    _base["sread"] = {0: {_TECH1_COLL: 8}}
    _base.update(_TECH1_BUDGET)
    CASES["Script_Tech1"].append(_base)
# <<< factory Script_Tech1

SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-completion Script_Tech1
# One completion pc per case, derived from that case's own seeded total.
for _rec, _counts in zip(SCHEMA2_CASES["Script_Tech1"], _TECH1_SEEDS):
    _rec["completion"] = {"mode": "pre-ret", "pc": _TECH1_RST[sum(_counts) >= 10]}
# <<< factory-completion Script_Tech1

MUTATIONS = {}
# >>> factory-mutation Preload_DrMason
MUTATIONS["Preload_DrMason"] = {
    "source_symbol": "Preload_DrMason",
    "before": "if (state == MASON_LAB_IN_PRACTICE_DUEL) {",
    "after": "if (state != MASON_LAB_IN_PRACTICE_DUEL) {",
    "case_ids": ["Preload_DrMason-0", "Preload_DrMason-1", "Preload_DrMason-2",
                 "Preload_DrMason-3", "Preload_DrMason-4"],
}
# <<< factory-mutation Preload_DrMason
# >>> factory-mutation Preload_Sam
MUTATIONS["Preload_Sam"] = {
    "source_symbol": "Preload_Sam",
    "before": "if (state < MASON_LAB_IN_PRACTICE_DUEL) {",
    "after": "if (state >= MASON_LAB_IN_PRACTICE_DUEL) {",
    "case_ids": ["Preload_Sam-0", "Preload_Sam-1", "Preload_Sam-2",
                 "Preload_Sam-3", "Preload_Sam-4", "Preload_Sam-5"],
}
# <<< factory-mutation Preload_Sam
# >>> factory-mutation Preload_Tech5
MUTATIONS["Preload_Tech5"] = {
    "source_symbol": "Preload_Tech5",
    "before": "uint8_t moved = (uint8_t)(gb_read8(hl) + 2u);",
    "after": "uint8_t moved = (uint8_t)(gb_read8(hl) + 1u);",
    "case_ids": ["Preload_Tech5-0", "Preload_Tech5-1", "Preload_Tech5-2",
                 "Preload_Tech5-3"],
}
# <<< factory-mutation Preload_Tech5
# >>> factory-mutation MasonLaboratoryAfterDuel
MUTATIONS["MasonLaboratoryAfterDuel"] = {"source_symbol": "MasonLaboratoryAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(MasonLaboratoryAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(MasonLaboratoryAfterDuelTable + 1u));", "case_ids": ["MasonLaboratoryAfterDuel-0"]}
# <<< factory-mutation MasonLaboratoryAfterDuel
# >>> factory-mutation MasonLabCloseTextBox
MUTATIONS["MasonLabCloseTextBox"] = {"source_symbol": "MasonLabCloseTextBox", "before": "\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_CHALLENGE_MACHINE);", "after": "\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_CHALLENGE_MACHINE + 1u));", "case_ids": ["MasonLabCloseTextBox-0", "MasonLabCloseTextBox-1"]}
# <<< factory-mutation MasonLabCloseTextBox
# >>> factory-mutation Script_Tech1
MUTATIONS["Script_Tech1"] = {"source_symbol": "Script_Tech1", "before": "\tif (a >= 10u)", "after": "\tif (a > 10u)", "case_ids": ["Script_Tech1-0"]}
# <<< factory-mutation Script_Tech1
