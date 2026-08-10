"""Oracle-diff cases for poketcg/src/home/math.asm."""

CONTRACT = {
    "ATimes10": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CASES = {
    "ATimes10": [
        {},
        dict(POISON),
        dict(POISON, a=1),
        # 25 is the last input whose product fits in 8 bits; 26 is the first that wraps.
        dict(POISON, a=25),
        dict(POISON, a=26),
        dict(POISON, a=100),
        # 128 * 10 == 1280, a multiple of 256: the result is 0 without the input being 0.
        dict(POISON, a=128),
        dict(POISON, a=0x33),
        dict(POISON, a=255),
    ],
}

STATE = {
    "wram": [[0xC000, 4096], [0xD000, 4096]],
    "sram": [[bank, addr, 4096] for bank in range(4) for addr in (0xA000, 0xB000)],
    "vram": [[bank, addr, 4096] for bank in range(2) for addr in (0x8000, 0x9000)],
}
SCHEMA2_CASES = {
    "ATimes10": [
        {
            "id": "ATimes10-zero",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {r: 0 for r in POISON},
            "bus": {},
            "seeds": {},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "ATimes10-poison-25",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, a=25),
            "bus": {},
            "seeds": {},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "ATimes10-wrap",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, a=255),
            "bus": {},
            "seeds": {},
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
    "ATimes10": {
        "source_symbol": "ATimes10",
        "before": "a = (uint8_t)(a + e);",
        "after": "a = (uint8_t)(a + (uint8_t)(e + 1u));",
        "case_ids": ["ATimes10-zero", "ATimes10-poison-25", "ATimes10-wrap"],
    },
}
