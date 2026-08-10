"""Oracle-diff cases for poketcg/src/home/coin_toss.asm.

TossCoin and TossCoinATimes are not registered: both bank1call _TossCoin
(engine/duel/core.asm:7847), the full coin-toss animation/RNG sequence, which is
not ported and whose video/RNG side effects the differ cannot reproduce.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "CompareDEtoBC": {
        "compare": ("f", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "CompareDEtoBC": [
        {"d": 0x12, "e": 0x34, "b": 0x12, "c": 0x34},
        {"d": 0x10, "e": 0x00, "b": 0x20, "c": 0x00},
        {"d": 0x20, "e": 0x00, "b": 0x10, "c": 0x00},
        {"d": 0x12, "e": 0xAA, "b": 0x12, "c": 0x00},
        {"d": 0x12, "e": 0x00, "b": 0x23, "c": 0x00},
        dict(POISON, d=0x05, e=0x09, b=0x21, c=0x80),
    ],
}

SCHEMA2_CASES = {
    "CompareDEtoBC": [
        {
            "id": "CompareDEtoBC-equal",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {"d": 0x12, "e": 0x34, "b": 0x12, "c": 0x34},
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
            "id": "CompareDEtoBC-less",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {"d": 0x10, "e": 0, "b": 0x20, "c": 0},
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
            "id": "CompareDEtoBC-poison",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, d=5, e=9, b=0x21, c=0x80),
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
    "CompareDEtoBC": {
        "source_symbol": "CompareDEtoBC",
        "before": "if (d != b)",
        "after": "if (d == b)",
        "case_ids": ["CompareDEtoBC-equal", "CompareDEtoBC-less", "CompareDEtoBC-poison"],
    },
}
