"""Oracle-diff cases for poketcg/src/scripts/water_club.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wActiveGameEvent = 0xD0C2
wPlayerXCoord = 0xD330
wPlayerYCoord = 0xD331
wLoadNPCXPos = 0xD3AC
wd3d0 = 0xD3D0

CONTRACT = {
    "Preload_Amy": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "Preload_Amy": [
        {"wram": {wActiveGameEvent: b"\x00", wd3d0: b"\xaa"}},
        dict(POISON, wram={wActiveGameEvent: b"\x01", wPlayerXCoord: b"\x14",
                           wPlayerYCoord: b"\x06", wLoadNPCXPos: b"\xee", wd3d0: b"\xaa"}),
        {"wram": {wActiveGameEvent: b"\x01", wPlayerXCoord: b"\x13",
                  wPlayerYCoord: b"\x06", wLoadNPCXPos: b"\xee", wd3d0: b"\xaa"}},
        {"wram": {wActiveGameEvent: b"\xff", wPlayerXCoord: b"\x14",
                  wPlayerYCoord: b"\x05", wLoadNPCXPos: b"\xdd", wd3d0: b"\xaa"}, "keys": 0xA5},
    ],
}

SCHEMA2_CASES = {
    "Preload_Amy": [
        {
            "id": "Preload_Amy-zero",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0},
            "bus": {},
            "seeds": {"wram": {wActiveGameEvent: b"\x00", wd3d0: b"\xaa"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "Preload_Amy-poison",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
            "bus": {},
            "seeds": {"wram": {wActiveGameEvent: b"\x01", wPlayerXCoord: b"\x14",
                                wPlayerYCoord: b"\x06", wLoadNPCXPos: b"\xee", wd3d0: b"\xaa"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "Preload_Amy-boundary",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0},
            "bus": {},
            "seeds": {"wram": {wActiveGameEvent: b"\xff", wPlayerXCoord: b"\x14",
                                wPlayerYCoord: b"\x05", wLoadNPCXPos: b"\xdd", wd3d0: b"\xaa"}},
            "setup": [],
            "input_events": [{"keys": 0xA5}],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
    ],
}

MUTATIONS = {
    "Preload_Amy": {
        "source_symbol": "Preload_Amy",
        "before": "if (x != 0x14u)",
        "after": "if (x == 0x14u)",
        "case_ids": ["Preload_Amy-zero", "Preload_Amy-poison", "Preload_Amy-boundary"],
    },
}
