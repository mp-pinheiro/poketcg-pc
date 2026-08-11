POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sCardCollection = 0xA100
wEventVars = 0xD3D2
wOWMapEvents = 0xD323
wWriteBGMapToSRAM = 0xD292
wLoadNPCXPos = 0xD3AC
wLoadNPCYPos = 0xD3AD

CONTRACT = {
    "Script_Tech1": {"compare": (), "preserve": ()},
    "Preload_DrMason": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Script_Tech1": [
        {"sram": {0: {sCardCollection: b"\x00" * 256}},
         "sread": {0: {sCardCollection: 6}}},
        dict(POISON, sram={0: {sCardCollection: b"\x00" * 256}},
             sread={0: {sCardCollection: 6}}),
        {"sram": {0: {sCardCollection: bytes(9 if i == 1 else 0 for i in range(256))}},
         "sread": {0: {sCardCollection: 6}}},
        {"sram": {0: {sCardCollection: bytes(10 if i == 1 else 0 for i in range(256))}},
         "sread": {0: {sCardCollection: 6}}},
    ],
    "Preload_DrMason": [
        {"wram": {wEventVars + 6: b"\x00", wEventVars + 0x0D: b"\x00",
                  wLoadNPCXPos: b"\xAA", wLoadNPCYPos: b"\xBB",
                  wOWMapEvents: b"\x00" * 11, wWriteBGMapToSRAM: b"\xAA"},
         "read": {wOWMapEvents + 0x0A: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1,
                  wWriteBGMapToSRAM: 1, wEventVars - 1: 1},
         "a": 0, "f": 0xF0},
        dict(POISON,
             wram={wEventVars + 6: b"\x02", wEventVars + 0x0D: b"\x02",
                   wLoadNPCXPos: b"\xAA", wLoadNPCYPos: b"\xBB",
                   wOWMapEvents: b"\x00" * 11, wWriteBGMapToSRAM: b"\xAA"},
             read={wOWMapEvents + 0x0A: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1,
                   wWriteBGMapToSRAM: 1, wEventVars - 1: 1}),
        {"wram": {wEventVars + 6: b"\x02", wEventVars + 0x0D: b"\x00",
                  wLoadNPCXPos: b"\xAA", wLoadNPCYPos: b"\xBB",
                  wOWMapEvents: b"\x00" * 11, wWriteBGMapToSRAM: b"\xAA"},
         "read": {wOWMapEvents + 0x0A: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1,
                  wWriteBGMapToSRAM: 1, wEventVars - 1: 1}},
        {"wram": {wEventVars + 6: b"\x00", wEventVars + 0x0D: b"\x04",
                  wLoadNPCXPos: b"\xAA", wLoadNPCYPos: b"\xBB",
                  wOWMapEvents: b"\x00" * 11, wWriteBGMapToSRAM: b"\xAA"},
         "read": {wOWMapEvents + 0x0A: 1, wLoadNPCXPos: 1, wLoadNPCYPos: 1,
                  wWriteBGMapToSRAM: 1, wEventVars - 1: 1}},
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Script_Tech1": {
        "source_symbol": "Script_Tech1",
        "before": "if (total >= 10)",
        "after": "if (total >= 9)",
        "case_ids": ["Script_Tech1-2", "Script_Tech1-3"],
    },
    "Preload_DrMason": {
        "source_symbol": "Preload_DrMason",
        "before": "if (state == 1)",
        "after": "if (state == 2)",
        "case_ids": ["Preload_DrMason-1", "Preload_DrMason-2"],
    },
}
