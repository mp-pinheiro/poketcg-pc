"""Oracle-diff cases for poketcg/src/scripts/pokemon_dome_entrance.asm."""
from tests.cases._fixtures import dome_ronald_fixture as _dome_ronald_fixture, DOME_RONALD_REGS as _DOME_RONALD_REGS

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
wCurTilemap = 0xD131
wConsole = 0xCAB4
wPermissionMap = 0xD133
# <<< factory-cases-statics
# >>> factory PokemonDomeEntranceLoadMap
wEventVarByte_Dome = 0xD3E9
wEventVarByte_NPC = 0xD3EA
wReceivedLegendary = 0xD3D8
wEventVarByte_Ronald = 0xD3EB
CONTRACT["PokemonDomeEntranceLoadMap"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["PokemonDomeEntranceLoadMap"] = [
    {"wram": {wEventVarByte_Dome: b"\xFF", wEventVarByte_NPC: b"\xFF", wEventVarByte_Ronald: b"\xFF", wReceivedLegendary: b"\x00"}},
    {"wram": {wEventVarByte_Dome: b"\x08", wEventVarByte_NPC: b"\xFF", wEventVarByte_Ronald: b"\xFF", wReceivedLegendary: b"\x02"}},
    dict(POISON, wram={wEventVarByte_Dome: b"\x00", wEventVarByte_NPC: b"\xFF", wEventVarByte_Ronald: b"\xFF", wReceivedLegendary: b"\x00"}),
]
# <<< factory PokemonDomeEntranceLoadMap

# >>> factory PokemonDomeEntranceCloseTextBox
CONTRACT["PokemonDomeEntranceCloseTextBox"] = {"compare": (), "preserve": ()}
CASES["PokemonDomeEntranceCloseTextBox"] = [
    {"wram": {wOWMapEvents: b"\xFF\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents: 2, wPermissionMap: 256}},
    {"wram": {wOWMapEvents: b"\x02\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
     "read": {wWriteBGMapToSRAM: 1, wOWMapEvents: 2, wPermissionMap: 256}},
    dict(POISON, wram={wOWMapEvents: b"\x03\x00", wCurTilemap: b"\x00", wConsole: b"\x00"},
         read={wWriteBGMapToSRAM: 1, wOWMapEvents: 2, wPermissionMap: 256}),
]
# <<< factory PokemonDomeEntranceCloseTextBox

# >>> factory Script_f631.ows_f63c
# The code portion of Script_f631's .ows_f63c local, entered by `jp hl` from
# EnterScript after `set_next_npc_and_script NPC_RONALD1, .ows_f63c`; its
# `start_script` rst at $7651 ends the code, so every case completes pre-ret
# there (the split applied after migration, below). Compared: a and f at the
# rst (`xor a`), the medal count and its successor written to wTxRam3 and
# wTxRam3_b, and EVENT_MEDAL_COUNT's byte refreshed by TryGiveMedalPCPacks.
wTxRam3 = 0xCE43
wEventVarByte_MedalCount = 0xD3DC
CONTRACT["Script_f631.ows_f63c"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Script_f631.ows_f63c"] = [
    # ronald-3 632724: the live entry, five medals (Mitch, Gene, Amy, Isaac, Ken poked).
    dict(_dome_ronald_fixture(vram=False, bank=3), **_DOME_RONALD_REGS,
         read={wTxRam3: 4, wEventVarByte_MedalCount: 1}),
    # No medals at all: the count and its successor are 0 and 1.
    dict(_dome_ronald_fixture(vram=False, bank=3, **{"D3D2": b"\x00"}), **_DOME_RONALD_REGS,
         read={wTxRam3: 4, wEventVarByte_MedalCount: 1}),
    # Eight medals: the count refresh gives every pack, and the successor is 9.
    dict(_dome_ronald_fixture(vram=False, bank=3, **{"D3D2": b"\xff"}), **_DOME_RONALD_REGS,
         read={wTxRam3: 4, wEventVarByte_MedalCount: 1}),
]
# <<< factory Script_f631.ows_f63c

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-completion Script_f631.ows_f63c
for _rec in SCHEMA2_CASES["Script_f631.ows_f63c"]:
    _rec["completion"] = {"mode": "pre-ret", "pc": 0x7651}
# <<< factory-completion Script_f631.ows_f63c

MUTATIONS = {}
# >>> factory-mutation PokemonDomeEntranceCloseTextBox
MUTATIONS["PokemonDomeEntranceCloseTextBox"] = {"source_symbol": "PokemonDomeEntranceCloseTextBox", "before": "\tApplyOWMapEventChangeIfEventSet(MAP_EVENT_POKEMON_DOME_DOOR);", "after": "\tApplyOWMapEventChangeIfEventSet((uint8_t)(MAP_EVENT_POKEMON_DOME_DOOR + 1u));", "case_ids": ["PokemonDomeEntranceCloseTextBox-0", "PokemonDomeEntranceCloseTextBox-1"]}
# <<< factory-mutation PokemonDomeEntranceCloseTextBox
# >>> factory-mutation PokemonDomeEntranceLoadMap
MUTATIONS["PokemonDomeEntranceLoadMap"] = {"source_symbol": "PokemonDomeEntranceLoadMap", "before": "ZeroOutEventValue(EVENT_POKEMON_DOME_STATE", "after": "ZeroOutEventValue(EVENT_HALL_OF_HONOR_DOORS_OPEN", "case_ids": ["PokemonDomeEntranceLoadMap-0"]}
# <<< factory-mutation PokemonDomeEntranceLoadMap
# >>> factory-mutation Script_f631.ows_f63c
MUTATIONS["Script_f631.ows_f63c"] = {"source_symbol": "Script_f631_ows_f63c", "before": "\twTxRam3_b = (uint8_t)(count + 1u);", "after": "\twTxRam3_b = count;", "case_ids": ["Script_f631.ows_f63c-0", "Script_f631.ows_f63c-1", "Script_f631.ows_f63c-2"]}
# <<< factory-mutation Script_f631.ows_f63c
