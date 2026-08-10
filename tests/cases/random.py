"""Oracle-diff cases for poketcg/src/home/random.asm."""

wRNG1 = 0xCACA  # wRNG1, wRNG2, wRNGCounter are consecutive

CONTRACT = {
    "UpdateRNGSources": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "HtimesL": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e"),
    },
    "Random": {
        "compare": ("a", "b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
STATE = {
    "wram": [[0xC000, 4096], [0xD000, 4096]],
    "sram": [[bank, addr, 4096] for bank in range(4) for addr in (0xA000, 0xB000)],
    "vram": [[bank, addr, 4096] for bank in range(2) for addr in (0x8000, 0x9000)],
}

CASES = {
    "UpdateRNGSources": [
        # Hand-traced from the asm: $12/$34/$56 -> $88/$4C/$57 with A=$C4.
        dict(POISON, wram={wRNG1: b"\x12\x34\x56"}),
        {"wram": {wRNG1: b"\x00\x00\x00"}},
        dict(POISON, wram={wRNG1: b"\xff\xff\xff"}),
        # Counter wrap: $FF -> $00 must not carry into wRNG2.
        dict(POISON, wram={wRNG1: b"\x80\x01\xff"}),
        # Exercises both feedback inputs: bit6(wRNG2) set, bit0(wRNG1) clear.
        dict(POISON, wram={wRNG1: b"\x02\x40\x00"}),
        # bit7(ctr ^ r1) == 1: the only case where `rl e` hands a set carry to `rl d`.
        # Every other seed has that carry 0, so dropping the term still diffs clean.
        dict(POISON, wram={wRNG1: b"\x01\x00\x80"}),
    ],
    "HtimesL": [
        {},
        # Poisoned: hl=$1234 -> $12 * $34 = $3A8, bc/de must survive the push/pop.
        dict(POISON),
        {"hl": 0x00FF},  # h=0 -> 0
        {"hl": 0xFF00},  # l=0 -> 0
        {"hl": 0xFFFF},  # 255 * 255 = $FE01, the widest product
        # a=$80: the only set bit is consumed on the iteration where a reaches 0,
        # so a port that tests `nz` before adding loses the whole product.
        {"hl": 0x8003},
        dict(POISON, hl=0x0180),  # h=1: single carry iteration, a hits 0 with it
        dict(POISON, hl=0x0101),
        dict(POISON, hl=0x02FF),  # de shifted left once before the add
        dict(POISON, hl=0xA55A),
    ],
    "Random": [
        {"wram": {wRNG1: b"\x00\x00\x00"}},
        dict(POISON, wram={wRNG1: b"\x12\x34\x56"}),
        # a=0 boundary: h=0 so the product is 0 regardless of the RNG byte, but
        # the RNG state must still advance.
        dict(POISON, a=0, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=0, wram={wRNG1: b"\xde\xad\xbe"}),
        dict(POISON, a=1, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=1, wram={wRNG1: b"\xff\xff\xff"}),
        dict(POISON, a=10, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=10, wram={wRNG1: b"\x80\x01\xff"}),
        dict(POISON, a=255, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=255, wram={wRNG1: b"\x02\x40\x00"}),
        # Seeds where bit7(wRNGCounter ^ wRNG1) == 1, so the rl e -> rl d carry
        # reaches both the returned byte and the diffed wRNG2.
        dict(POISON, wram={wRNG1: b"\x00\xff\x80"}),
        dict(POISON, a=10, wram={wRNG1: b"\x01\x00\x80"}),
    ],
}

SCHEMA2_CASES = {
    "HtimesL": [
        {
            "id": "HtimesL-zero",
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
            "id": "HtimesL-poison",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
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
            "id": "HtimesL-max",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, hl=0xffff),
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
    "UpdateRNGSources": [
        {
            "id": "UpdateRNGSources-zero",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {r: 0 for r in POISON},
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\x00\x00\x00"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "UpdateRNGSources-poison",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\x12\x34\x56"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "UpdateRNGSources-boundary",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\xff\xff\xff"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
    ],
    "Random": [
        {
            "id": "Random-zero",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, a=0),
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\x12\x34\x56"}},
            "setup": [],
            "input_events": [],
            "instruction_budget": 1000,
            "cycle_budget": 10000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "Random-one",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON, a=1),
            "bus": {},
            "seeds": {"wram": {wRNG1: b"\xff\xff\xff"}},
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
    "UpdateRNGSources": {
        "source_symbol": "UpdateRNGSources",
        "before": "uint8_t feedback = (uint8_t)(((r2 >> 6) ^ r1) & 1);",
        "after": "uint8_t feedback = (uint8_t)((((r2 >> 6) ^ r1) & 1) ^ 1u);",
        "case_ids": ["UpdateRNGSources-zero", "UpdateRNGSources-poison", "UpdateRNGSources-boundary"],
    },
    "HtimesL": {
        "source_symbol": "HtimesL",
        "before": "acc = (uint16_t)(acc + de);",
        "after": "acc = (uint16_t)(acc + (uint16_t)(de + 1u));",
        "case_ids": ["HtimesL-zero", "HtimesL-poison", "HtimesL-max"],
    },
    "Random": {
        "source_symbol": "Random",
        "before": "return (uint8_t)(HtimesL((uint16_t)(a << 8 | l)) >> 8);",
        "after": "return (uint8_t)(HtimesL((uint16_t)(a << 8 | (uint8_t)(l + 1u))) >> 8);",
        "case_ids": ["Random-zero", "Random-one"],
    },
}
