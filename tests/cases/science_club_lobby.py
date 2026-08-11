wRNG1 = 0xCACA
wTxRam2 = 0xCE3F

CONTRACT = {
    "Script_Specs2": {"compare": (), "preserve": ()},
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
STATE = {
    "wram": [[0xC000, 4096], [0xD000, 4096]],
    "sram": [[bank, addr, 4096] for bank in range(4) for addr in (0xA000, 0xB000)],
    "vram": [[bank, addr, 4096] for bank in range(2) for addr in (0x8000, 0x9000)],
}

CASES = {
    "Script_Specs2": [
        {"wram": {wRNG1: b"\x00\x00\x00", wTxRam2: b"\xff\xff"},
         "read": {wRNG1: 3, wTxRam2: 2}},
        dict(POISON, wram={wRNG1: b"\x12\x34\x56", wTxRam2: b"\x00\x00"},
             read={wRNG1: 3, wTxRam2: 2}),
        dict(POISON, wram={wRNG1: b"\xff\xff\xff", wTxRam2: b"\xaa\xaa"},
             read={wRNG1: 3, wTxRam2: 2}),
    ],
}

SCHEMA2_CASES = {
    "Script_Specs2": [
        {
            "id": "Script_Specs2-zero",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {r: 0 for r in POISON},
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\x00\x00\x00", wTxRam2: b"\xff\xff"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "Script_Specs2-poison",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\x12\x34\x56", wTxRam2: b"\x00\x00"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "Script_Specs2-boundary",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\xff\xff\xff", wTxRam2: b"\xaa\xaa"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
    ],
}

MUTATIONS = {
    "Script_Specs2": {
        "source_symbol": "Script_Specs2",
        "before": "uint8_t card = science_club_cards[UpdateRNGSources() & 3u];",
        "after": "uint8_t card = science_club_cards[(UpdateRNGSources() + 1u) & 3u];",
        "case_ids": ["Script_Specs2-zero", "Script_Specs2-poison", "Script_Specs2-boundary"],
    },
}
