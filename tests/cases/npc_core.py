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

# >>> factory SetNPCAnimation
CONTRACT["SetNPCAnimation"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["SetNPCAnimation"] = [
    {"a": 0, "wram": {0xD3AA: b"\x00"}, "read": {0xD300: 0x100}},
    {"a": 1, "wram": {0xD3AA: b"\x01"}, "read": {0xD300: 0x100}},
    {"a": 0xFF, "wram": {0xD3AA: b"\x02"}, "read": {0xD300: 0x100}},
    dict(POISON, a=0x33, wram={0xD3AA: b"\x01"}, read={0xD300: 0x100}),
]
# <<< factory SetNPCAnimation

# >>> factory SetNPCDirection
CONTRACT["SetNPCDirection"] = {"compare": ("a", "hl"), "preserve": ("hl",)}
CASES["SetNPCDirection"] = [
    {"a": 0, "wram": {0xD3AA: b"\x00"}, "read": {0xD300: 0x100}},
    {"a": 1, "wram": {0xD3AA: b"\x01"}, "read": {0xD300: 0x100}},
    {"a": 0xFF, "wram": {0xD3AA: b"\x02"}, "read": {0xD300: 0x100}},
    dict(POISON, a=0x02, wram={0xD3AA: b"\x01"}, read={0xD300: 0x100}),
]
# <<< factory SetNPCDirection

# >>> factory StartNPCMovement
# wLoadedNPCTempIndex = 0xD3AA; movement scripts live in scratch WRAM ($C100-$CA00),
# where GetNextNPCMovementByte's bus read at $Cxxx hits WRAM regardless of bank.
SCRATCH = 0xC100
wLoadedNPCTempIndex = 0xD3AA
# compare excludes f (loop/callee residue on the stop path, not a produced contract)
# and d/e (never read here; callee clobber not modeled). bc is an advanced pointer
# (the routine's own `inc bc` after callees proves they preserve it), so b/c are outputs.
CONTRACT["StartNPCMovement"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("hl",)}
CASES["StartNPCMovement"] = [
	{"b": 0, "c": 0},  # all-zero: bc = $0000 walks ROM bank 0 from the rst vectors
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\x02"}, "read": {SCRATCH: 1}},  # plain direction, immediate exit
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\x81\x00"}, "read": {SCRATCH: 2}},  # rotation (bit 7 set), then exit
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\xf5\x02\x00\x00\x03"}, "read": {SCRATCH: 5}},  # jump +2 forward
	{"b": 0xC1, "c": 0x01, "wram": {SCRATCH: b"\x00\xf5\xfe"}, "read": {SCRATCH: 3}},  # jump -2 backward
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\xff", wLoadedNPCTempIndex: b"\x02"}, "read": {SCRATCH: 1}},  # $ff stop, NPC index 2
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\xef\x7f"}, "read": {SCRATCH: 2}},  # boundary: $ef rotation, $7f max direction
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\xf0\x01\x02"}, "read": {SCRATCH: 3}},  # boundary: $f0 minimal jump command
	{"b": 0xC1, "c": 0x00, "wram": {SCRATCH: b"\xf1\x7f" + b"\x00" * 0x7E + b"\x01"}, "read": {SCRATCH: 0x81}},  # jump +$7f max positive
	{"b": 0xC1, "c": 0x82, "wram": {0xC103: b"\x06", 0xC182: b"\xf3\x80"}, "read": {0xC103: 1, 0xC182: 2}},  # jump -$80, 16-bit wraparound
	dict(POISON, b=0xC1, c=0x00, wram={SCRATCH: b"\x01"}, read={SCRATCH: 1}),  # proves hl preserved, bc unchanged
	dict(POISON, b=0xC1, c=0x02, wram={0xC102: b"\x81\x05"}, read={0xC102: 2}),  # preservation through rotation path
	dict(POISON, b=0xC1, c=0x00, wram={SCRATCH: b"\xff"}, read={SCRATCH: 1}),  # preservation through stop path
]
# <<< factory StartNPCMovement

# >>> factory Func_1c5e9
CONTRACT["Func_1c5e9"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Func_1c5e9"] = [
    {"read": {0xD300: 0x200}},
    {"wram": {0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x00"}, "read": {0xD300: 0x200}},
    dict(POISON, wram={0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x01"}, read={0xD300: 0x200}),
]
# <<< factory Func_1c5e9

# >>> factory UpdateNPCPosition
CONTRACT["UpdateNPCPosition"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["UpdateNPCPosition"] = [
	{"wram": {0xD3AA: b"\x00", 0xD3AB: b"\x00\x00\x00\x00\x00"}, "read": {0xD3AB: 5}},
	dict(POISON, wram={0xD3AA: b"\x00", 0xD3AB: b"\x11\x22\x30\x40\x00"}, read={0xD3AB: 5}),
	{"wram": {0xD3AA: b"\x00", 0xD3AB: b"\x11\x22\x30\x40\x01"}, "read": {0xD3AB: 5}},
	{"wram": {0xD3AA: b"\x00", 0xD3AB: b"\x11\x22\x30\x40\x02"}, "read": {0xD3AB: 5}},
	{"wram": {0xD3AA: b"\x00", 0xD3AB: b"\x11\x22\x30\x40\x03"}, "read": {0xD3AB: 5}},
]
# <<< factory UpdateNPCPosition

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
# >>> factory-mutation SetNPCAnimation
MUTATIONS["SetNPCAnimation"] = {
    "source_symbol": "SetNPCAnimation",
    "before": "GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_ANIM);",
    "after": "GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);",
    "case_ids": ["SetNPCAnimation-1", "SetNPCAnimation-2", "SetNPCAnimation-3"],
}
# <<< factory-mutation SetNPCAnimation
# >>> factory-mutation SetNPCDirection
MUTATIONS["SetNPCDirection"] = {
    "source_symbol": "SetNPCDirection",
    "before": "GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);\n\tgb_write8(r.hl, a);",
    "after": "GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION_BACKUP);\n\tgb_write8(r.hl, a);",
    "case_ids": ["SetNPCDirection-1", "SetNPCDirection-2", "SetNPCDirection-3"],
}
# <<< factory-mutation SetNPCDirection
# >>> factory-mutation StartNPCMovement
MUTATIONS["StartNPCMovement"] = {
	"source_symbol": "StartNPCMovement",
	"before": "if (cmd >= MOVEMENT_CMD_SPECIAL)",
	"after": "if (cmd > MOVEMENT_CMD_SPECIAL)",
	"case_ids": ["StartNPCMovement-7"],
}
# <<< factory-mutation StartNPCMovement
# >>> factory-mutation Func_1c5e9
MUTATIONS["Func_1c5e9"] = {"source_symbol": "Func_1c5e9", "before": "uint16_t hl = (uint16_t)(r.hl + (uint16_t)(LOADED_NPC_DIRECTION - LOADED_NPC_DIRECTION_BACKUP));", "after": "uint16_t hl = (uint16_t)(r.hl + 0u);", "case_ids": ["Func_1c5e9-1", "Func_1c5e9-2"]}
# <<< factory-mutation Func_1c5e9
# >>> factory-mutation UpdateNPCPosition
MUTATIONS["UpdateNPCPosition"] = {"source_symbol": "UpdateNPCPosition", "before": "uint8_t x = (uint8_t)(gb_read8(hl) + x_offset);", "after": "uint8_t x = (uint8_t)(gb_read8(hl) + y_offset);", "case_ids": ["UpdateNPCPosition-1", "UpdateNPCPosition-2", "UpdateNPCPosition-3", "UpdateNPCPosition-4"]}
# <<< factory-mutation UpdateNPCPosition
