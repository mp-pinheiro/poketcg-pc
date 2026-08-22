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

# >>> factory UpdateNPCSpritePosition
CONTRACT["UpdateNPCSpritePosition"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UpdateNPCSpritePosition"] = [
	{"hl": 0xD3AB, "wram": {0xD3AD: b"\x01\x02", 0xD3B0: b"\x00", 0xD4CF: b"\x00"}, "hram": {0xFF92: b"\x20", 0xFF93: b"\x30"}, "read": {0xD3B0: 1, 0xFF92: 1, 0xFF93: 1, 0xD4CF: 1, 0xD3AD: 1, 0xD3AE: 1}},
	dict(POISON, hl=0xD3AB, wram={0xD3AD: b"\x10\x20", 0xD3AF: b"\x01", 0xD3B0: b"\x20", 0xD3B3: b"\x08", 0xD4CF: b"\x00"}, hram={0xFF92: b"\x20", 0xFF93: b"\x30"}, read={0xD3B0: 1, 0xD3AF: 1, 0xD3B3: 1, 0xFF92: 1, 0xFF93: 1, 0xD4CF: 1, 0xD3AD: 1, 0xD3AE: 1}),
]
# <<< factory UpdateNPCSpritePosition

# >>> factory CheckIsAnNPCMoving
CONTRACT["CheckIsAnNPCMoving"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckIsAnNPCMoving"] = [
	{"wram": {0xD3B7: b"\x00"}},
	{"wram": {0xD3B7: b"\x01"}},
	{"wram": {0xD3B7: b"\x20"}},
	{"wram": {0xD3B7: b"\x21"}},
	dict(POISON, wram={0xD3B7: b"\x20"}),
]
# <<< factory CheckIsAnNPCMoving

# >>> factory UpdateNPCsTilePermission
CONTRACT["UpdateNPCsTilePermission"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UpdateNPCsTilePermission"] = [
    {"wram": {0xD3AA: b"\x00", 0xD34C: b"\x00\x00", 0xD133: b"\xFF"}, "expect": {0xD133: b"\xBF"}, "expect_regs": {"a": 0xBF}},
    {"wram": {0xD3AA: b"\x01", 0xD356: b"\x04\x06", 0xD165: b"\x40"}, "expect": {0xD165: b"\x00"}, "expect_regs": {"a": 0x00}},
    {"wram": {0xD3AA: b"\x07", 0xD39C: b"\x0E\x10", 0xD1BA: b"\x7F"}, "expect": {0xD1BA: b"\x3F"}, "expect_regs": {"a": 0x3F}},
    {"wram": {0xD3AA: b"\x08", 0xD34C: b"\x02\x04", 0xD154: b"\xFF"}, "expect": {0xD154: b"\xBF"}, "expect_regs": {"a": 0xBF}},
    dict(POISON, wram={0xD3AA: b"\xAA", 0xD34C: b"\x08\x0A", 0xD183: b"\xFF"}, expect={0xD183: b"\xBF"}, expect_regs={"a": 0xBF}),
]
# <<< factory UpdateNPCsTilePermission

# >>> factory SetNPCsTilePermission
CONTRACT["SetNPCsTilePermission"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNPCsTilePermission"] = [
    {"wram": {0xD3AA: b"\x00", 0xD34C: b"\x00\x00", 0xD133: b"\xFF"}, "expect": {0xD133: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"wram": {0xD3AA: b"\x01", 0xD356: b"\x04\x06", 0xD165: b"\x40"}, "expect": {0xD165: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"wram": {0xD3AA: b"\x07", 0xD39C: b"\x0E\x10", 0xD1BA: b"\x7F"}, "expect": {0xD1BA: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"wram": {0xD3AA: b"\x08", 0xD34C: b"\x02\x04", 0xD154: b"\xFF"}, "expect": {0xD154: b"\x40"}, "expect_regs": {"a": 0x40}},
    dict(POISON, wram={0xD3AA: b"\xAA", 0xD34C: b"\x08\x0A", 0xD183: b"\xFF"}, expect={0xD183: b"\x40"}, expect_regs={"a": 0x40}),
]
# <<< factory SetNPCsTilePermission

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wLoadedNPCTempIndex = 0xD3AA

wLoadedNPCTempIndex = 0xD3AA
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wIsAnNPCMoving = 0xD3B7
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadedNPCTempIndex = 0xD3AA
wTempNPC = 0xD3AB
wLoadedNPCs = 0xD34A
NPC_TABLE = bytes(range(1, 97))
NPC_READ = {wLoadedNPCs: 96}
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wLoadedNPCs = 0xD34A
wLoadedNPCTempIndex = 0xD3AA
wRonaldIsInMap = 0xD3B8

wLoadedNPCTempIndex = 0xD3AA
wPlayerDirection = 0xD334
wCurrentNPCNameTx = 0xD0C8
wOverworldNPCFlags = 0xD0C1
NPC_BASE = 0xD34A
NPC_DATA = b"\x00" * 96
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadedNPCTempIndex = 0xD3AA

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
# <<< factory-cases-statics

# >>> factory SetNPCPosition
CONTRACT["SetNPCPosition"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNPCPosition"] = [
    {"b": 0x04, "c": 0x06, "wram": {0xD3AA: b"\x00", 0xD34C: b"\x00\x00", 0xD133: b"\xFF", 0xD165: b"\x00"}, "expect": {0xD133: b"\xBF", 0xD165: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"b": 0x0E, "c": 0x10, "wram": {0xD3AA: b"\x01", 0xD356: b"\x04\x06", 0xD165: b"\xFF", 0xD1BA: b"\x7F"}, "expect": {0xD165: b"\xBF", 0xD1BA: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"b": 0x02, "c": 0x04, "wram": {0xD3AA: b"\x07", 0xD39C: b"\x0E\x10", 0xD1BA: b"\xFF", 0xD154: b"\x00"}, "expect": {0xD1BA: b"\xBF", 0xD154: b"\x40"}, "expect_regs": {"a": 0x40}},
    dict(POISON, b=0x12, c=0x14, wram={0xD3AA: b"\xAA", 0xD34C: b"\x08\x0A", 0xD183: b"\xFF", 0xD1DC: b"\x00"}, expect={0xD183: b"\xBF", 0xD1DC: b"\x40"}, expect_regs={"a": 0x40, "b": 0x12, "c": 0x14, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory SetNPCPosition

# >>> factory Func_1c53f
CONTRACT["Func_1c53f"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")};
CASES["Func_1c53f"] = [
    {"wram": {0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x00"}, "read": {0xD300: 0x200}},
    {"wram": {0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x01"}, "read": {0xD300: 0x200}},
    dict(POISON, wram={0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x02"}, read={0xD300: 0x200}),
]
# <<< factory Func_1c53f

# >>> factory GetNPCDirection
CONTRACT["GetNPCDirection"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetNPCDirection"] = [
    {"wram": {0xD3AA: b"\x00", 0xD34E: b"\x2A"}, "read": {0xD34E: 1}},
    {"wram": {0xD3AA: b"\x07", 0xD3A2: b"\x91"}, "read": {0xD3A2: 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {0xD3AA: b"\x08", 0xD34E: b"\x7E"}, "read": {0xD34E: 1}},
]
# <<< factory GetNPCDirection

# >>> factory GetNPCPosition
CONTRACT["GetNPCPosition"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("hl",)}
CASES["GetNPCPosition"] = [
    {"wram": {0xD3AA: b"\x00", 0xD34C: b"\x12\x34"}, "read": {0xD34C: 2}},
    {"wram": {0xD3AA: b"\x01", 0xD358: b"\x56\x78"}, "read": {0xD358: 2}},
    {"wram": {0xD3AA: b"\x07", 0xD3A2: b"\x9A\xBC"}, "read": {0xD3A2: 2}},
    dict(POISON, wram={0xD3AA: b"\x07", 0xD3A2: b"\xDE\xF0"}, read={0xD3A2: 2}),
]
# <<< factory GetNPCPosition

# >>> factory UpdateIsAnNPCMovingFlag
CONTRACT["UpdateIsAnNPCMovingFlag"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["UpdateIsAnNPCMovingFlag"] = [
    {"hl": 0xC500, "wram": {wIsAnNPCMoving: b"\x00", 0xC505: b"\x00"}, "expect": {wIsAnNPCMoving: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80}},
    {"hl": 0xC500, "wram": {wIsAnNPCMoving: b"\x01", 0xC505: b"\x02"}, "expect": {wIsAnNPCMoving: b"\x03"}, "expect_regs": {"a": 0x03, "f": 0x00}},
    {"hl": 0xC500, "wram": {wIsAnNPCMoving: b"\x80", 0xC505: b"\x01"}, "expect": {wIsAnNPCMoving: b"\x81"}, "expect_regs": {"a": 0x81, "f": 0x00}},
    dict(POISON, hl=0xC500, wram={wIsAnNPCMoving: b"\x20", 0xC505: b"\x04"}, expect={wIsAnNPCMoving: b"\x24"}, expect_regs={"a": 0x24, "f": 0x00}),
]
# <<< factory UpdateIsAnNPCMovingFlag

# >>> factory ClearNPCs
CONTRACT["ClearNPCs"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")};
CASES["ClearNPCs"] = [
	{"wram": {0xD34A: b"\xFF" * 0x60, 0xD349: b"\x7F", 0xD3B8: b"\x01"}, "expect": {0xD34A: b"\x00" * 0x60, 0xD349: b"\x00", 0xD3B8: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	{"wram": {0xD34A: bytes(range(0x60)), 0xD349: b"\xAA", 0xD3B8: b"\xBB"}, "expect": {0xD34A: b"\x00" * 0x60, 0xD349: b"\x00", 0xD3B8: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	dict(POISON, wram={0xD34A: b"\xA5" * 0x60, 0xD349: b"\x5A", 0xD3B8: b"\xC3"}, expect={0xD34A: b"\x00" * 0x60, 0xD349: b"\x00", 0xD3B8: b"\x00"}, expect_regs={"a": 0x00, "f": 0xC0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory ClearNPCs

# >>> factory SetAllNPCTilePermissions
CONTRACT["SetAllNPCTilePermissions"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetAllNPCTilePermissions"] = [
	{"wram": {0xD34A: b"\x01\x00\x00\x00" + b"\x00" * 92, 0xD133: b"\xFF"}, "expect": {0xD133: b"\x40"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	{"wram": {0xD34A: b"\x00" * 84 + b"\x01\x00\x0E\x10" + b"\x00" * 8, 0xD1BA: b"\x7F"}, "expect": {0xD1BA: b"\x40"}, "expect_regs": {"a": 0x40, "f": 0xC0}},
	dict(POISON, wram={0xD34A: b"\x00" * 96, 0xD3AA: b"\x77"}, expect_regs={"a": 0x00, "f": 0xC0}),
]
# <<< factory SetAllNPCTilePermissions

# >>> factory Func_1c557
CONTRACT["Func_1c557"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["Func_1c557"] = [
    {"a": 0xF0, "wram": {wLoadedNPCTempIndex: b"\x07", wTempNPC: b"\x44", wLoadedNPCs: NPC_TABLE}, "read": NPC_READ},
    {"a": 0x12, "wram": {wLoadedNPCTempIndex: b"\x07", wTempNPC: b"\x44", wLoadedNPCs: bytes(range(1, 13)) + b"\x12\x22\x23\x24\x37\x26\x27\x28\x29\x2A\x2B\x2C" + bytes(range(25, 97))}, "read": NPC_READ, "expect": {wLoadedNPCs + 19: b"\x37", wLoadedNPCTempIndex: b"\x07", wTempNPC: b"\x44"}},
    {"a": 0x60, "wram": {wLoadedNPCTempIndex: b"\x00", wTempNPC: b"\x01", wLoadedNPCs: bytes(range(1, 97))}, "read": NPC_READ},
    dict(POISON, wram={wLoadedNPCTempIndex: b"\x03", wTempNPC: b"\x55", wLoadedNPCs: NPC_TABLE}, read=NPC_READ),
]
# <<< factory Func_1c557

# >>> factory LoadNPC
CONTRACT["LoadNPC"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["LoadNPC"] = [
    {"wram": {wLoadedNPCs: b"\x01" * 0x60}, "expect": {wLoadedNPCTempIndex: b"\x00"}, "expect_regs": {"a": 0x01}},
    dict(POISON, wram={wLoadedNPCs: b"\x01" * 0x60, wLoadedNPCTempIndex: b"\xAA"}, expect={wLoadedNPCTempIndex: b"\x00"}, expect_regs={"a": 0x01, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory LoadNPC

# >>> factory SetNewScriptNPC
CONTRACT["SetNewScriptNPC"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ("hl",), "wram_out": True}
CASES["SetNewScriptNPC"] = [
    {"hl": 0x4567, "wram": {wLoadedNPCTempIndex: b"\x00", wPlayerDirection: b"\x01", wOverworldNPCFlags: b"\x00", NPC_BASE: NPC_DATA}, "expect": {NPC_BASE + 4: b"\x03", wOverworldNPCFlags: b"\x02"}, "read": {wCurrentNPCNameTx: 2}},
    {"hl": 0x0000, "wram": {wLoadedNPCTempIndex: b"\x01", wPlayerDirection: b"\x03", wOverworldNPCFlags: b"\x80", NPC_BASE: NPC_DATA}, "expect": {NPC_BASE + 12 + 4: b"\x01", wOverworldNPCFlags: b"\x82"}, "read": {wCurrentNPCNameTx: 2}},
    dict(POISON, wram={wLoadedNPCTempIndex: b"\x00", wPlayerDirection: b"\x02", wOverworldNPCFlags: b"\x04", NPC_BASE: NPC_DATA}, expect={NPC_BASE + 4: b"\x00", wOverworldNPCFlags: b"\x06"}, read={wCurrentNPCNameTx: 2}),
]
# <<< factory SetNewScriptNPC

# >>> factory UnloadNPC
CONTRACT["UnloadNPC"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UnloadNPC"] = [
	{},
	{"wram": {0xD3AA: b"\x00", 0xD34A: b"\x01\x02\x00\x00", 0xD349: b"\x03"}, "expect": {0xD34A: b"\x00\x02", 0xD349: b"\x02"}},
	{"wram": {0xD3AA: b"\x00", 0xD34A: b"\x71\x03\x00\x00", 0xD349: b"\x02", 0xD3B8: b"\x01"}, "expect": {0xD34A: b"\x00\x03", 0xD349: b"\x01", 0xD3B8: b"\x00"}},
	dict(POISON, wram={0xD3AA: b"\x01", 0xD356: b"\x01\x04\x00\x00", 0xD349: b"\x05"}, expect={0xD356: b"\x00\x04", 0xD349: b"\x04"}),
	dict(POISON, wram={0xD3AA: b"\x01", 0xD356: b"\x72\x07\x00\x00", 0xD349: b"\x01", 0xD3B8: b"\x01"}, expect={0xD356: b"\x00\x07", 0xD349: b"\x00", 0xD3B8: b"\x00"}),
]
# <<< factory UnloadNPC

# >>> factory Func_1c52e
CONTRACT["Func_1c52e"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Func_1c52e"] = [
    {"a": 0x00, "wram": {0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x00"}, "read": {0xD300: 0x200}, "expect": {0xD307: b"\x00"}},
    {"a": 0x7F, "wram": {0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x01"}, "read": {0xD300: 0x200}, "expect": {0xD313: b"\x7F"}},
    dict(POISON, a=0x33, wram={0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x00"}, read={0xD300: 0x200}, expect={0xD307: b"\x33"}),
    dict(POISON, a=0xFF, wram={0xD300: bytes(range(256)) * 2, 0xD3AA: b"\x01"}, read={0xD300: 0x200}, expect={0xD313: b"\xFF"}),
]
# <<< factory Func_1c52e

# >>> factory UpdateNPCMovementStep
CONTRACT["UpdateNPCMovementStep"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["UpdateNPCMovementStep"] = [
    {"a": 0x17, "hl": 0xC500, "wram": {0xC505: b"\x00", 0xC508: b"\x0F"}, "expect": {0xC508: b"\x0F"}, "expect_regs": {"a": 0x17}},
    {"a": 0x42, "hl": 0xC500, "wram": {0xC505: b"\x20", 0xC508: b"\x00"}, "expect": {0xC508: b"\x01"}, "expect_regs": {"a": 0x42}},
    {"a": 0x99, "hl": 0xC500, "wram": {0xC505: b"\x20", 0xC508: b"\x0E"}, "expect": {0xC508: b"\x0F"}, "expect_regs": {"a": 0x99}},
    dict(POISON, hl=0xC500, wram={0xC505: b"\x20", 0xC508: b"\x0E"}, expect={0xC508: b"\x0F"}, expect_regs={"a": 0xAA}),
]
# <<< factory UpdateNPCMovementStep

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
# >>> factory-mutation UpdateNPCSpritePosition
MUTATIONS["UpdateNPCSpritePosition"] = {"source_symbol": "UpdateNPCSpritePosition", "before": "uint8_t y = (uint8_t)(y_base * 8u + 0x10u);", "after": "uint8_t y = (uint8_t)(y_base * 8u + 0x08u);", "case_ids": ["UpdateNPCSpritePosition-0", "UpdateNPCSpritePosition-1"]}
# <<< factory-mutation UpdateNPCSpritePosition
# >>> factory-mutation CheckIsAnNPCMoving
MUTATIONS["CheckIsAnNPCMoving"] = {"source_symbol": "CheckIsAnNPCMoving", "before": "uint8_t a = (uint8_t)(wIsAnNPCMoving & NPC_FLAG_MOVING);", "after": "uint8_t a = wIsAnNPCMoving;", "case_ids": ["CheckIsAnNPCMoving-1", "CheckIsAnNPCMoving-2", "CheckIsAnNPCMoving-3", "CheckIsAnNPCMoving-4"]}
# <<< factory-mutation CheckIsAnNPCMoving
# >>> factory-mutation UpdateNPCsTilePermission
MUTATIONS["UpdateNPCsTilePermission"] = {"source_symbol": "UpdateNPCsTilePermission", "before": "uint8_t result = UpdatePermissionOfMapPosition(0x40u, x, y);", "after": "uint8_t result = UpdatePermissionOfMapPosition(0x20u, x, y);", "case_ids": ["UpdateNPCsTilePermission-0", "UpdateNPCsTilePermission-1", "UpdateNPCsTilePermission-2", "UpdateNPCsTilePermission-3", "UpdateNPCsTilePermission-4"]}
# <<< factory-mutation UpdateNPCsTilePermission
# >>> factory-mutation SetNPCsTilePermission
MUTATIONS["SetNPCsTilePermission"] = {"source_symbol": "SetNPCsTilePermission", "before": "SetPermissionOfMapPosition(0x40u, x, y);", "after": "SetPermissionOfMapPosition(0x20u, x, y);", "case_ids": ["SetNPCsTilePermission-0", "SetNPCsTilePermission-1", "SetNPCsTilePermission-2", "SetNPCsTilePermission-3", "SetNPCsTilePermission-4"]}
# <<< factory-mutation SetNPCsTilePermission
# >>> factory-mutation SetNPCPosition
MUTATIONS["SetNPCPosition"] = {
    "source_symbol": "SetNPCPosition",
    "before": "gb_write8((uint16_t)(entry.hl + 1u), c);",
    "after": "gb_write8((uint16_t)(entry.hl + 2u), c);",
    "case_ids": ["SetNPCPosition-0", "SetNPCPosition-1", "SetNPCPosition-2", "SetNPCPosition-3"],
}
# <<< factory-mutation SetNPCPosition
# >>> factory-mutation Func_1c53f
MUTATIONS["Func_1c53f"] = {"source_symbol": "Func_1c53f", "before": "uint16_t backup = (uint16_t)(r.hl + (LOADED_NPC_DIRECTION_BACKUP - LOADED_NPC_DIRECTION));", "after": "uint16_t backup = (uint16_t)(r.hl + 4u);", "case_ids": ["Func_1c53f-0", "Func_1c53f-1", "Func_1c53f-2"]}
# <<< factory-mutation Func_1c53f
# >>> factory-mutation GetNPCDirection
MUTATIONS["GetNPCDirection"] = {
    "source_symbol": "GetNPCDirection",
    "before": "	return gb_read8(r.hl);",
    "after": "	return (uint8_t)(gb_read8(r.hl) + 1u);",
    "case_ids": ["GetNPCDirection-0", "GetNPCDirection-1", "GetNPCDirection-2"],
}
# <<< factory-mutation GetNPCDirection
# >>> factory-mutation GetNPCPosition
MUTATIONS["GetNPCPosition"] = {
    "source_symbol": "GetNPCPosition",
    "before": "\tuint8_t y = gb_read8((uint16_t)(r.hl + 1u));",
    "after": "\tuint8_t y = gb_read8((uint16_t)(r.hl + 2u));",
    "case_ids": ["GetNPCPosition-0", "GetNPCPosition-1", "GetNPCPosition-2", "GetNPCPosition-3"],
}
# <<< factory-mutation GetNPCPosition
# >>> factory-mutation UpdateIsAnNPCMovingFlag
MUTATIONS["UpdateIsAnNPCMovingFlag"] = {"source_symbol": "UpdateIsAnNPCMovingFlag", "before": "uint8_t a = (uint8_t)(wIsAnNPCMoving | gb_read8((uint16_t)(hl + LOADED_NPC_FLAGS)));", "after": "uint8_t a = wIsAnNPCMoving;", "case_ids": ["UpdateIsAnNPCMovingFlag-1", "UpdateIsAnNPCMovingFlag-2", "UpdateIsAnNPCMovingFlag-3"]}
# <<< factory-mutation UpdateIsAnNPCMovingFlag
# >>> factory-mutation ClearNPCs
MUTATIONS["ClearNPCs"] = {"source_symbol": "ClearNPCs", "before": "wLoadedNPCs_PTR[i] = 0x00u;", "after": "wLoadedNPCs_PTR[i + 1u] = 0x00u;", "case_ids": ["ClearNPCs-0", "ClearNPCs-1", "ClearNPCs-2"]};
# <<< factory-mutation ClearNPCs
# >>> factory-mutation SetAllNPCTilePermissions
MUTATIONS["SetAllNPCTilePermissions"] = {"source_symbol": "SetAllNPCTilePermissions", "before": "\t\tif (wLoadedNPCs_PTR[(uint16_t)i * LOADED_NPC_LENGTH] != 0u) {", "after": "\t\tif (wLoadedNPCs_PTR[(uint16_t)i * LOADED_NPC_LENGTH] == 0u) {", "case_ids": ["SetAllNPCTilePermissions-0", "SetAllNPCTilePermissions-1", "SetAllNPCTilePermissions-2"]}
# <<< factory-mutation SetAllNPCTilePermissions
# >>> factory-mutation Func_1c557
MUTATIONS["Func_1c557"] = {"source_symbol": "Func_1c557", "before": "\tif ((found.f & 0x10u) == 0u)", "after": "\tif ((found.f & 0x10u) != 0u)", "case_ids": ["Func_1c557-0", "Func_1c557-1", "Func_1c557-2", "Func_1c557-3"]}
# <<< factory-mutation Func_1c557
# >>> factory-mutation LoadNPC
MUTATIONS["LoadNPC"] = {"source_symbol": "LoadNPC", "before": "remaining != 0u", "after": "remaining == 0u", "case_ids": ["LoadNPC-0", "LoadNPC-1"]}
# <<< factory-mutation LoadNPC
# >>> factory-mutation SetNewScriptNPC
MUTATIONS["SetNewScriptNPC"] = {"source_symbol": "SetNewScriptNPC", "before": "gb_write8(direction.hl, (uint8_t)(wPlayerDirection ^ 0x02u));", "after": "gb_write8(direction.hl, wPlayerDirection);", "case_ids": ["SetNewScriptNPC-0", "SetNewScriptNPC-1", "SetNewScriptNPC-2"]}
# <<< factory-mutation SetNewScriptNPC
# >>> factory-mutation UnloadNPC
MUTATIONS["UnloadNPC"] = {"source_symbol": "UnloadNPC", "before": "gb_write8(npc.hl, 0u);", "after": "gb_write8((uint16_t)(npc.hl + 1u), 0u);", "case_ids": ["UnloadNPC-1", "UnloadNPC-2", "UnloadNPC-3", "UnloadNPC-4"]}
# <<< factory-mutation UnloadNPC
# >>> factory-mutation Func_1c52e
MUTATIONS["Func_1c52e"] = {"source_symbol": "Func_1c52e", "before": "PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,\n\t\tLOADED_NPC_DIRECTION_BACKUP);\n\tgb_write8(r.hl, a);", "after": "PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,\n\t\tLOADED_NPC_DIRECTION_BACKUP);\n\tgb_write8((uint16_t)(r.hl + 1u), a);", "case_ids": ["Func_1c52e-0", "Func_1c52e-1", "Func_1c52e-2", "Func_1c52e-3"]}
# <<< factory-mutation Func_1c52e
# >>> factory-mutation UpdateNPCMovementStep
MUTATIONS["UpdateNPCMovementStep"] = {"source_symbol": "UpdateNPCMovementStep", "before": "\tgb_write8(step, (uint8_t)(gb_read8(step) + 1u));", "after": "\tgb_write8(step, (uint8_t)(gb_read8(step) + 2u));", "case_ids": ["UpdateNPCMovementStep-1", "UpdateNPCMovementStep-2", "UpdateNPCMovementStep-3"]}
# <<< factory-mutation UpdateNPCMovementStep
