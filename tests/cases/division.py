"""Oracle-diff cases for poketcg/src/home/division.asm."""

CONTRACT = {
    "DivideBCbyDE": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("d", "e"),
    },
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}


def _case(bc, de, **kw):
    return dict(kw, b=bc >> 8, c=bc & 0xFF, d=de >> 8, e=de & 0xFF)


CASES = {
    "DivideBCbyDE": [
        # All-zero: divisor 0, so quotient $FFFF and remainder = dividend = 0.
        {},
        # Poisoned registers: proves d/e survive and hl is overwritten, not
        # combined with its entry value. $BBCC / $DDEE -> quotient 0.
        dict(POISON),
        # de=0 with a real dividend: quotient $FFFF, remainder = dividend.
        _case(0x1234, 0x0000, a=0xAA, hl=0x5678),
        _case(0xFFFF, 0x0000),
        # Exact division: 1000 / 10 = 100 remainder 0.
        _case(1000, 10),
        # With a remainder: 1000 / 7 = 142 remainder 6.
        _case(1000, 7),
        # bc < de: quotient 0, remainder = dividend.
        _case(5, 100),
        _case(0xFFFE, 0xFFFF),
        _case(0xFFFF, 0x0001),
        _case(0xFFFF, 0xFFFF),
        # Divisor above $8000 drives the remainder to its maximum ($7FFF)
        # before the final shift, the one place a 17th bit could go missing.
        _case(0xFFFF, 0x8000),
        _case(0xFFFF, 0xC000),
        _case(0x8000, 0x8001),
        _case(1, 1),
        _case(0x0000, 0x0001),
        # Entry carry must not reach the quotient or the remainder: the same
        # division with carry set and clear has to give the same answer.
        _case(10000, 100, a=0xAA, f=0xF0, hl=0x1234),
        _case(10000, 100, a=0xAA, f=0x00, hl=0x1234),
        # Divisor with a zero low byte, exercising the `sbc d` path alone.
        _case(0xABCD, 0x0100),
        # Divisor with a zero high byte and a borrow out of the low byte.
        _case(0xABCD, 0x00FF),
    ],
}
SCHEMA2_CASES = {
    "DivideBCbyDE": [
        {
            "id": "DivideBCbyDE-zero",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": {r: 0 for r in POISON},
            "bus": {},
            "seeds": {},
            "setup": [],
            "input_events": [],
            "instruction_budget": 10000,
            "cycle_budget": 100000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "DivideBCbyDE-poison",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": dict(POISON),
            "bus": {},
            "seeds": {},
            "setup": [],
            "input_events": [],
            "instruction_budget": 10000,
            "cycle_budget": 100000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
        {
            "id": "DivideBCbyDE-divisor-zero",
            "hardware": "cgb",
            "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
            "registers": _case(0x1234, 0),
            "bus": {},
            "seeds": {},
            "setup": [],
            "input_events": [],
            "instruction_budget": 10000,
            "cycle_budget": 100000,
            "completion": {"mode": "return"},
            "evidence": "primary",
        },
    ],
}
MUTATIONS = {
    "DivideBCbyDE": {
        "source_symbol": "DivideBCbyDE",
        "before": "bc = (uint16_t)(bc << 1);",
        "after": "bc = (uint16_t)(bc << 1 | 1u);",
        "case_ids": ["DivideBCbyDE-zero", "DivideBCbyDE-poison", "DivideBCbyDE-divisor-zero"],
    },
}
