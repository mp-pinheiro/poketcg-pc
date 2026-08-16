"""Oracle-diff cases for poketcg/src/engine/scenes.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory SetBoosterLogoOAM
CONTRACT["SetBoosterLogoOAM"] = {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetBoosterLogoOAM"] = [
	{},
	{"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE,
	 "hl": 0x1234,
	 "wram": {
		 0xCAB4: b"\x02",
		 0xCAC0: b"\x7F",
		 0xD4CA: b"\x55",
		 0xD4CB: b"\x66",
		 0xD61C: b"\x20",
		 0xD61D: b"\x30",
		 0xFF92: b"\x04",
		 0xFF93: b"\x08",
	 },
	 "read": {0xC000: 0x100}},
	{"wram": {
		 0xCAB4: b"\x01",
		 0xCAC0: b"\xFF",
		 0xD4CA: b"\xA5",
		 0xD4CB: b"\xA6",
		 0xD61C: b"\x40",
		 0xD61D: b"\x40",
		 0xFF92: b"\x10",
		 0xFF93: b"\x20",
	 }}
]
# <<< factory SetBoosterLogoOAM

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation SetBoosterLogoOAM
MUTATIONS["SetBoosterLogoOAM"] = {"source_symbol": "SetBoosterLogoOAM", "before": "wWhichVRAMBank = 0u;", "after": "wWhichVRAMBank = 1u;", "case_ids": ["SetBoosterLogoOAM-1", "SetBoosterLogoOAM-2"]}
# <<< factory-mutation SetBoosterLogoOAM
