"""Oracle-diff cases for poketcg/src/home/damage.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wDamage = 0xCCB9

CONTRACT = {
    "AddToDamage": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
    "SubtractFromDamage": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
}

CASES = {
    "AddToDamage": [
        {"a": 0, "wram": {wDamage: b"\x00\x00"}},
        {"a": 0x40, "wram": {wDamage: b"\xC0\x00"}},
        {"a": 0x10, "wram": {wDamage: b"\x05\x01"}},
        dict(POISON, a=0xFF, wram={wDamage: b"\x01\x80"}),
    ],
    "SubtractFromDamage": [
        {"a": 0, "wram": {wDamage: b"\x00\x00"}},
        {"a": 0x40, "wram": {wDamage: b"\xC0\x00"}},
        {"a": 0x10, "wram": {wDamage: b"\x05\x01"}},
        {"a": 0x01, "wram": {wDamage: b"\x00\x00"}},
        dict(POISON, a=0xFF, wram={wDamage: b"\x01\x80"}),
    ],
}

def _schema_case(identifier, registers):
    seed = registers.pop("_damage")
    return {
        "id": identifier,
        "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
        "registers": registers,
        "bus": {},
        "seeds": {"wram": {wDamage: seed}},
        "setup": [],
        "input_events": [],
        "instruction_budget": 1000,
        "cycle_budget": 10000,
        "completion": {"mode": "return"},
        "evidence": "primary",
    }

SCHEMA2_CASES = {
    "AddToDamage": [
        _schema_case("AddToDamage-zero", {"a": 0, "_damage": b"\x00\x00"}),
        _schema_case("AddToDamage-boundary", {"a": 0xFF, "_damage": b"\x01\x80"}),
    ],
    "SubtractFromDamage": [
        _schema_case("SubtractFromDamage-zero", {"a": 0, "_damage": b"\x00\x00"}),
        _schema_case("SubtractFromDamage-boundary", {"a": 1, "_damage": b"\x00\x00"}),
    ],
}
