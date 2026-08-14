"""Oracle-diff cases for poketcg/src/engine/overworld/npc_core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory CheckIfNPCIsRonald
CONTRACT["CheckIfNPCIsRonald"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("a", "b", "c", "d", "e", "hl")}
CASES["CheckIfNPCIsRonald"] = [
	{},
	{"a": 0x00},
	{"a": 0x01},
	{"a": 0x02},
	{"a": 0x71},
	{"a": 0x72},
	{"a": 0x73},
	{"a": 0xFF},
	dict(POISON, a=0x02),
	dict(POISON, a=0x71),
	dict(POISON, a=0x72),
	dict(POISON, a=0x00),
	dict(POISON, a=0xFF),
]
# <<< factory CheckIfNPCIsRonald

# >>> factory UpdateNPCAnimation
CONTRACT["UpdateNPCAnimation"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ("f", "b", "c", "hl")}
CASES["UpdateNPCAnimation"] = [
	{},
	{"wram": {0xD3AA: b"\x03"}},
	dict(POISON, wram={0xD4CF: b"\x37"}),
	{"wram": {0xC100: bytes(range(0x10, 0x20)) * 0xE0, 0xD000: (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], 0xD3AA: b"\x00", 0xD3AB: (bytes(range(0x10, 0x20)) * 0x100)[:0xC55]}},
	{"wram": {0xC100: bytes(range(0x20, 0x30)) * 0xE0, 0xD000: (bytes(range(0x20, 0x30)) * 0x100)[:0x3AA], 0xD3AA: b"\x01", 0xD3AB: (bytes(range(0x20, 0x30)) * 0x100)[:0xC55]}},
	dict(POISON, wram={0xC100: bytes(range(0x10, 0x20)) * 0xE0, 0xD000: (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], 0xD3AA: b"\x02", 0xD3AB: (bytes(range(0x10, 0x20)) * 0x100)[:0xC55]}),
]
# <<< factory UpdateNPCAnimation

# >>> factory ApplyRandomCountToNPCAnim
CONTRACT["ApplyRandomCountToNPCAnim"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ("f", "b", "c", "hl")}
CASES["ApplyRandomCountToNPCAnim"] = [
	{},
	{"wram": {0xD3AA: b"\x01"}},
	dict(POISON, wram={0xD4CF: b"\x64"}),
	{"wram": {0xC100: bytes(range(0x10, 0x20)) * 0xE0, 0xD000: (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], 0xD3AA: b"\x00", 0xD3AB: (bytes(range(0x10, 0x20)) * 0x100)[:0xC55]}},
	{"wram": {0xC100: bytes(range(0x20, 0x30)) * 0xE0, 0xD000: (bytes(range(0x20, 0x30)) * 0x100)[:0x3AA], 0xD3AA: b"\x02", 0xD3AB: (bytes(range(0x20, 0x30)) * 0x100)[:0xC55]}},
	dict(POISON, wram={0xC100: bytes(range(0x10, 0x20)) * 0xE0, 0xD000: (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], 0xD3AA: b"\x01", 0xD3AB: (bytes(range(0x10, 0x20)) * 0x100)[:0xC55]}),
	{"wram": {0xC100: b"\xff" * 0xE00, 0xD000: b"\xff" * 0x3AA, 0xD3AA: b"\x00", 0xD3AB: b"\xff" * 0xC55}},
]
# <<< factory ApplyRandomCountToNPCAnim

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation CheckIfNPCIsRonald
MUTATIONS["CheckIfNPCIsRonald"] = {"source_symbol": "CheckIfNPCIsRonald", "before": "a == NPC_RONALD3", "after": "a == NPC_RONALD1", "case_ids": ["CheckIfNPCIsRonald-5", "CheckIfNPCIsRonald-10"]}
# <<< factory-mutation CheckIfNPCIsRonald
# >>> factory-mutation UpdateNPCAnimation
MUTATIONS["UpdateNPCAnimation"] = {"source_symbol": "UpdateNPCAnimation", "before": "NPC_FLAG_DIRECTIONLESS_F)) == 0", "after": "NPC_FLAG_DIRECTIONLESS_F)) != 0", "case_ids": ["UpdateNPCAnimation-3", "UpdateNPCAnimation-4", "UpdateNPCAnimation-5"]}
# <<< factory-mutation UpdateNPCAnimation
# >>> factory-mutation ApplyRandomCountToNPCAnim
MUTATIONS["ApplyRandomCountToNPCAnim"] = {"source_symbol": "ApplyRandomCountToNPCAnim", "before": "gb_write8(counter, (uint8_t)(count - r));", "after": "gb_write8((uint16_t)(counter + 1u), (uint8_t)(count - r));", "case_ids": ["ApplyRandomCountToNPCAnim-3", "ApplyRandomCountToNPCAnim-4", "ApplyRandomCountToNPCAnim-5"]}
# <<< factory-mutation ApplyRandomCountToNPCAnim
