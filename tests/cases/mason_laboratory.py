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
# >>> factory-mutation MasonLaboratoryAfterDuel
MUTATIONS["MasonLaboratoryAfterDuel"] = {"source_symbol": "MasonLaboratoryAfterDuel", "before": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript(MasonLaboratoryAfterDuelTable);", "after": "	FindEndOfDuelScriptResult r = FindEndOfDuelScript((uint16_t)(MasonLaboratoryAfterDuelTable + 1u));", "case_ids": ["MasonLaboratoryAfterDuel-0"]}
# <<< factory-mutation MasonLaboratoryAfterDuel
# >>> factory-mutation MasonLabCloseTextBox
MUTATIONS["MasonLabCloseTextBox"] = {"source_symbol": "MasonLabCloseTextBox", "before": "\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_CHALLENGE_MACHINE);", "after": "\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_CHALLENGE_MACHINE + 1u));", "case_ids": ["MasonLabCloseTextBox-0", "MasonLabCloseTextBox-1"]}
# <<< factory-mutation MasonLabCloseTextBox
# >>> factory-mutation Script_Tech1
MUTATIONS["Script_Tech1"] = {"source_symbol": "Script_Tech1", "before": "\tif (a >= 10u)", "after": "\tif (a > 10u)", "case_ids": ["Script_Tech1-0"]}
# <<< factory-mutation Script_Tech1
