"""Oracle-diff cases for poketcg/src/home/math.asm."""

CONTRACT = {
    "ATimes10": ("a", "b", "c", "d", "e", "hl"),
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

SCHEMA2_CASES = {
    "ATimes10": [{
        "id": "ATimes10-poison-25",
        "fn": "ATimes10",
        "entry": 0x0C4B,
        "completion": "return",
        "instruction_budget": 1000,
        "cycle_budget": 10000,
        "mapper": {"rom_bank": 1, "ram_bank": 0, "ram_enable": False},
        "registers": dict(POISON, a=25),
        "bus": {},
        "sram": {},
        "vram": {},
        "setup": [],
        "input_events": [],
        "evidence": "primary",
    }],
}
