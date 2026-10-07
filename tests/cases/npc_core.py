from tests.cases._symbols import STACK_WINDOW, sym
from tests.cases._fixtures import npc_start_fixture as _npc_start_fixture, NPC_START_REGS as _NPC_START_REGS, npc_move_fixture as _npc_move_fixture, NPC_MOVE_REGS as _NPC_MOVE_REGS
"""Oracle-diff cases for poketcg/src/engine/overworld/npc_core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

def _observable_npc_tail(payload):
	pre = STACK_WINDOW.start - sym("wTempNPC")
	post = STACK_WINDOW.stop - sym("wTempNPC")
	return {sym("wTempNPC"): payload[:pre], STACK_WINDOW.stop: payload[post:]}


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
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x03"}},
	dict(POISON, wram={sym("wWhichSprite"): b"\x37"}),
	{"wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(range(0x10, 0x20)) * 0xE0, sym("wNamingScreenDestPointer"): (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], sym("wLoadedNPCTempIndex"): b"\x00", **_observable_npc_tail((bytes(range(0x10, 0x20)) * 0x100)[:0xC55])}},
	{"wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(range(0x20, 0x30)) * 0xE0, sym("wNamingScreenDestPointer"): (bytes(range(0x20, 0x30)) * 0x100)[:0x3AA], sym("wLoadedNPCTempIndex"): b"\x01", **_observable_npc_tail((bytes(range(0x20, 0x30)) * 0x100)[:0xC55])}},
	dict(POISON, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(range(0x10, 0x20)) * 0xE0, sym("wNamingScreenDestPointer"): (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], sym("wLoadedNPCTempIndex"): b"\x02", **_observable_npc_tail((bytes(range(0x10, 0x20)) * 0x100)[:0xC55])}),
]
# <<< factory UpdateNPCAnimation

# >>> factory ApplyRandomCountToNPCAnim
CONTRACT["ApplyRandomCountToNPCAnim"] = {"compare": ("a", "f", "b", "c", "hl"), "preserve": ("f", "b", "c", "hl")}
CASES["ApplyRandomCountToNPCAnim"] = [
	{},
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x01"}},
	dict(POISON, wram={sym("wWhichSprite"): b"\x64"}),
	{"wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(range(0x10, 0x20)) * 0xE0, sym("wNamingScreenDestPointer"): (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], sym("wLoadedNPCTempIndex"): b"\x00", **_observable_npc_tail((bytes(range(0x10, 0x20)) * 0x100)[:0xC55])}},
	{"wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(range(0x20, 0x30)) * 0xE0, sym("wNamingScreenDestPointer"): (bytes(range(0x20, 0x30)) * 0x100)[:0x3AA], sym("wLoadedNPCTempIndex"): b"\x02", **_observable_npc_tail((bytes(range(0x20, 0x30)) * 0x100)[:0xC55])}},
	dict(POISON, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: bytes(range(0x10, 0x20)) * 0xE0, sym("wNamingScreenDestPointer"): (bytes(range(0x10, 0x20)) * 0x100)[:0x3AA], sym("wLoadedNPCTempIndex"): b"\x01", **_observable_npc_tail((bytes(range(0x10, 0x20)) * 0x100)[:0xC55])}),
	{"wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xff" * 0xE00, sym("wNamingScreenDestPointer"): b"\xff" * 0x3AA, sym("wLoadedNPCTempIndex"): b"\x00", **_observable_npc_tail(b"\xff" * 0xC55)}},
]
# <<< factory ApplyRandomCountToNPCAnim

# >>> factory SetNPCAnimation
CONTRACT["SetNPCAnimation"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["SetNPCAnimation"] = [
    {"a": 0, "wram": {sym("wLoadedNPCTempIndex"): b"\x00"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x100}},
    {"a": 1, "wram": {sym("wLoadedNPCTempIndex"): b"\x01"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x100}},
    {"a": 0xFF, "wram": {sym("wLoadedNPCTempIndex"): b"\x02"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x100}},
    dict(POISON, a=0x33, wram={sym("wLoadedNPCTempIndex"): b"\x01"}, read={sym("wTempObjectPalettesCGB") + 0x29: 0x100}),
]
# <<< factory SetNPCAnimation

# >>> factory SetNPCDirection
CONTRACT["SetNPCDirection"] = {"compare": ("a", "hl"), "preserve": ("hl",)}
CASES["SetNPCDirection"] = [
    {"a": 0, "wram": {sym("wLoadedNPCTempIndex"): b"\x00"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x100}},
    {"a": 1, "wram": {sym("wLoadedNPCTempIndex"): b"\x01"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x100}},
    {"a": 0xFF, "wram": {sym("wLoadedNPCTempIndex"): b"\x02"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x100}},
    dict(POISON, a=0x02, wram={sym("wLoadedNPCTempIndex"): b"\x01"}, read={sym("wTempObjectPalettesCGB") + 0x29: 0x100}),
]
# <<< factory SetNPCDirection

# >>> factory StartNPCMovement
# wLoadedNPCTempIndex = 0xD3AA; movement scripts live in scratch WRAM ($C100-$CA00),
# where GetNextNPCMovementByte's bus read at $Cxxx hits WRAM regardless of bank.
SCRATCH = sym("wDecompressionSecondaryBufferStart") + 0x11
wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
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
	{"b": 0xC1, "c": 0x82, "wram": {sym("wDecompressionSecondaryBufferStart") + 0x14: b"\x06", sym("wDecompressionSecondaryBufferStart") + 0x93: b"\xf3\x80"}, "read": {sym("wDecompressionSecondaryBufferStart") + 0x14: 1, sym("wDecompressionSecondaryBufferStart") + 0x93: 2}},  # jump -$80, 16-bit wraparound
	dict(POISON, b=0xC1, c=0x00, wram={SCRATCH: b"\x01"}, read={SCRATCH: 1}),  # proves hl preserved, bc unchanged
	dict(POISON, b=0xC1, c=0x02, wram={sym("wDecompressionSecondaryBufferStart") + 0x13: b"\x81\x05"}, read={sym("wDecompressionSecondaryBufferStart") + 0x13: 2}),  # preservation through rotation path
	dict(POISON, b=0xC1, c=0x00, wram={SCRATCH: b"\xff"}, read={SCRATCH: 1}),  # preservation through stop path,
    dict(_npc_start_fixture(vram=False, bank=7), **_NPC_START_REGS),
]
# <<< factory StartNPCMovement

# >>> factory Func_1c5e9
CONTRACT["Func_1c5e9"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Func_1c5e9"] = [
    {"read": {sym("wTempObjectPalettesCGB") + 0x29: 0x200}},
    {"wram": {sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x00"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x200}},
    dict(POISON, wram={sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x01"}, read={sym("wTempObjectPalettesCGB") + 0x29: 0x200}),
]
# <<< factory Func_1c5e9

# >>> factory UpdateNPCPosition
CONTRACT["UpdateNPCPosition"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
# The routine indexes wLoadedNPCs ($D34A; id, sprite, x, y, direction, ...)
# through wLoadedNPCTempIndex, so the observed span has to be the NPC slot:
# the earlier span over wTempNPC ($D3AB) never saw the coordinates move, which
# is how a +-1 transcription of PlayerMovementOffsetTable_Tiles (steps are
# +-2, map.asm:227-231) shipped green.
CASES["UpdateNPCPosition"] = [
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x00" * 8}, "read": {sym("wLoadedNPC1ID"): 8}},
	dict(POISON, wram={sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x11\x22\x30\x40\x00\x00\x00\x00"}, read={sym("wLoadedNPC1ID"): 8}),
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x11\x22\x30\x40\x01\x00\x00\x00"}, "read": {sym("wLoadedNPC1ID"): 8}},
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x11\x22\x30\x40\x02\x00\x00\x00"}, "read": {sym("wLoadedNPC1ID"): 8}},
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x11\x22\x30\x40\x03\x00\x00\x00"}, "read": {sym("wLoadedNPC1ID"): 8}},
	# second slot, so the index arithmetic is observed as well
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC1ID"): b"\x00" * 12 + b"\x11\x22\x30\x40\x01\x00\x00\x00"}, "read": {sym("wLoadedNPC1ID"): 20}},
]
# <<< factory UpdateNPCPosition

# >>> factory UpdateNPCSpritePosition
CONTRACT["UpdateNPCSpritePosition"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UpdateNPCSpritePosition"] = [
	{"hl": sym("wTempNPC"), "wram": {sym("wLoadNPCYPos"): b"\x01\x02", sym("wLoadNPCFunction") + 1: b"\x00", sym("wWhichSprite"): b"\x00"}, "hram": {sym("hSCX"): b"\x20", sym("hSCY"): b"\x30"}, "read": {sym("wLoadNPCFunction") + 1: 1, sym("hSCX"): 1, sym("hSCY"): 1, sym("wWhichSprite"): 1, sym("wLoadNPCYPos"): 1, sym("wLoadNPCDirection"): 1}},
	dict(POISON, hl=sym("wTempNPC"), wram={sym("wLoadNPCYPos"): b"\x10\x20", sym("wLoadNPCFunction"): b"\x01", sym("wLoadNPCFunction") + 1: b"\x20", sym("wNPCSpriteID"): b"\x08", sym("wWhichSprite"): b"\x00"}, hram={sym("hSCX"): b"\x20", sym("hSCY"): b"\x30"}, read={sym("wLoadNPCFunction") + 1: 1, sym("wLoadNPCFunction"): 1, sym("wNPCSpriteID"): 1, sym("hSCX"): 1, sym("hSCY"): 1, sym("wWhichSprite"): 1, sym("wLoadNPCYPos"): 1, sym("wLoadNPCDirection"): 1}),
]
# <<< factory UpdateNPCSpritePosition

# >>> factory CheckIsAnNPCMoving
CONTRACT["CheckIsAnNPCMoving"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["CheckIsAnNPCMoving"] = [
	{"wram": {sym("wIsAnNPCMoving"): b"\x00"}},
	{"wram": {sym("wIsAnNPCMoving"): b"\x01"}},
	{"wram": {sym("wIsAnNPCMoving"): b"\x20"}},
	{"wram": {sym("wIsAnNPCMoving"): b"\x21"}},
	dict(POISON, wram={sym("wIsAnNPCMoving"): b"\x20"}),
]
# <<< factory CheckIsAnNPCMoving

# >>> factory UpdateNPCsTilePermission
CONTRACT["UpdateNPCsTilePermission"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["UpdateNPCsTilePermission"] = [
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1CoordX"): b"\x00\x00", sym("wBoosterViableCardList"): b"\xFF"}, "expect": {sym("wBoosterViableCardList"): b"\xBF"}, "expect_regs": {"a": 0xBF}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC2ID"): b"\x04\x06", sym("wBoosterViableCardList") + 0x32: b"\x40"}, "expect": {sym("wBoosterViableCardList") + 0x32: b"\x00"}, "expect_regs": {"a": 0x00}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x07", sym("wLoadedNPC7Field0x0a"): b"\x0E\x10", sym("wBoosterViableCardList") + 0x87: b"\x7F"}, "expect": {sym("wBoosterViableCardList") + 0x87: b"\x3F"}, "expect_regs": {"a": 0x3F}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x08", sym("wLoadedNPC1CoordX"): b"\x02\x04", sym("wBoosterViableCardList") + 0x21: b"\xFF"}, "expect": {sym("wBoosterViableCardList") + 0x21: b"\xBF"}, "expect_regs": {"a": 0xBF}},
    dict(POISON, wram={sym("wLoadedNPCTempIndex"): b"\xAA", sym("wLoadedNPC1CoordX"): b"\x08\x0A", sym("wBoosterViableCardList") + 0x50: b"\xFF"}, expect={sym("wBoosterViableCardList") + 0x50: b"\xBF"}, expect_regs={"a": 0xBF}),
]
# <<< factory UpdateNPCsTilePermission

# >>> factory SetNPCsTilePermission
CONTRACT["SetNPCsTilePermission"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNPCsTilePermission"] = [
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1CoordX"): b"\x00\x00", sym("wBoosterViableCardList"): b"\xFF"}, "expect": {sym("wBoosterViableCardList"): b"\x40"}, "expect_regs": {"a": 0x40}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC2ID"): b"\x04\x06", sym("wBoosterViableCardList") + 0x32: b"\x40"}, "expect": {sym("wBoosterViableCardList") + 0x32: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x07", sym("wLoadedNPC7Field0x0a"): b"\x0E\x10", sym("wBoosterViableCardList") + 0x87: b"\x7F"}, "expect": {sym("wBoosterViableCardList") + 0x87: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x08", sym("wLoadedNPC1CoordX"): b"\x02\x04", sym("wBoosterViableCardList") + 0x21: b"\xFF"}, "expect": {sym("wBoosterViableCardList") + 0x21: b"\x40"}, "expect_regs": {"a": 0x40}},
    dict(POISON, wram={sym("wLoadedNPCTempIndex"): b"\xAA", sym("wLoadedNPC1CoordX"): b"\x08\x0A", sym("wBoosterViableCardList") + 0x50: b"\xFF"}, expect={sym("wBoosterViableCardList") + 0x50: b"\x40"}, expect_regs={"a": 0x40}),
]
# <<< factory SetNPCsTilePermission

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")

wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wIsAnNPCMoving = sym("wIsAnNPCMoving")
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
wTempNPC = sym("wTempNPC")
wLoadedNPCs = sym("wLoadedNPCs")
NPC_TABLE = bytes(range(1, 97))
NPC_READ = {wLoadedNPCs: 96}
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wLoadedNPCs = sym("wLoadedNPCs")
wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
wRonaldIsInMap = sym("wRonaldIsInMap")

wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")
wPlayerDirection = sym("wPlayerDirection")
wCurrentNPCNameTx = sym("wCurrentNPCNameTx")
wOverworldNPCFlags = sym("wOverworldNPCFlags")
NPC_BASE = sym("wLoadedNPC1ID")
NPC_DATA = b"\x00" * 96
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wLoadedNPCTempIndex = sym("wLoadedNPCTempIndex")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wIsAnNPCMoving = sym("wIsAnNPCMoving")
wNumLoadedNPCs = sym("wNumLoadedNPCs")
wLoadedNPCs = sym("wLoadedNPCs")
wWhichSprite = sym("wWhichSprite")
wPermissionMap = sym("wPermissionMap")
SPRITE_BUFFER = sym("wSprite1Enabled")
hSCX = sym("hSCX")
hSCY = sym("hSCY")
def npc_entry(npc_id, sprite_id, x, y, direction=0, flags=0, step=0):
    e = bytearray(12)
    e[0] = npc_id
    e[1] = sprite_id
    e[2] = x
    e[3] = y
    e[4] = direction
    e[5] = flags
    e[8] = step
    return bytes(e)
# <<< factory-cases-statics

# >>> factory SetNPCPosition
CONTRACT["SetNPCPosition"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetNPCPosition"] = [
    {"b": 0x04, "c": 0x06, "wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1CoordX"): b"\x00\x00", sym("wBoosterViableCardList"): b"\xFF", sym("wBoosterViableCardList") + 0x32: b"\x00"}, "expect": {sym("wBoosterViableCardList"): b"\xBF", sym("wBoosterViableCardList") + 0x32: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"b": 0x0E, "c": 0x10, "wram": {sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC2ID"): b"\x04\x06", sym("wBoosterViableCardList") + 0x32: b"\xFF", sym("wBoosterViableCardList") + 0x87: b"\x7F"}, "expect": {sym("wBoosterViableCardList") + 0x32: b"\xBF", sym("wBoosterViableCardList") + 0x87: b"\x40"}, "expect_regs": {"a": 0x40}},
    {"b": 0x02, "c": 0x04, "wram": {sym("wLoadedNPCTempIndex"): b"\x07", sym("wLoadedNPC7Field0x0a"): b"\x0E\x10", sym("wBoosterViableCardList") + 0x87: b"\xFF", sym("wBoosterViableCardList") + 0x21: b"\x00"}, "expect": {sym("wBoosterViableCardList") + 0x87: b"\xBF", sym("wBoosterViableCardList") + 0x21: b"\x40"}, "expect_regs": {"a": 0x40}},
    dict(POISON, b=0x12, c=0x14, wram={sym("wLoadedNPCTempIndex"): b"\xAA", sym("wLoadedNPC1CoordX"): b"\x08\x0A", sym("wBoosterViableCardList") + 0x50: b"\xFF", sym("wBoosterViableCardList") + 0xA9: b"\x00"}, expect={sym("wBoosterViableCardList") + 0x50: b"\xBF", sym("wBoosterViableCardList") + 0xA9: b"\x40"}, expect_regs={"a": 0x40, "b": 0x12, "c": 0x14, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory SetNPCPosition

# >>> factory Func_1c53f
CONTRACT["Func_1c53f"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")};
CASES["Func_1c53f"] = [
    {"wram": {sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x00"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x200}},
    {"wram": {sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x01"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x200}},
    dict(POISON, wram={sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x02"}, read={sym("wTempObjectPalettesCGB") + 0x29: 0x200}),
]
# <<< factory Func_1c53f

# >>> factory GetNPCDirection
CONTRACT["GetNPCDirection"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["GetNPCDirection"] = [
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1Direction"): b"\x2A"}, "read": {sym("wLoadedNPC1Direction"): 1}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x07", sym("wLoadedNPC8Direction"): b"\x91"}, "read": {sym("wLoadedNPC8Direction"): 1}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "wram": {sym("wLoadedNPCTempIndex"): b"\x08", sym("wLoadedNPC1Direction"): b"\x7E"}, "read": {sym("wLoadedNPC1Direction"): 1}},
]
# <<< factory GetNPCDirection

# >>> factory GetNPCPosition
CONTRACT["GetNPCPosition"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("hl",)}
CASES["GetNPCPosition"] = [
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1CoordX"): b"\x12\x34"}, "read": {sym("wLoadedNPC1CoordX"): 2}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC2CoordX"): b"\x56\x78"}, "read": {sym("wLoadedNPC2CoordX"): 2}},
    {"wram": {sym("wLoadedNPCTempIndex"): b"\x07", sym("wLoadedNPC8Direction"): b"\x9A\xBC"}, "read": {sym("wLoadedNPC8Direction"): 2}},
    dict(POISON, wram={sym("wLoadedNPCTempIndex"): b"\x07", sym("wLoadedNPC8Direction"): b"\xDE\xF0"}, read={sym("wLoadedNPC8Direction"): 2}),
]
# <<< factory GetNPCPosition

# >>> factory UpdateIsAnNPCMovingFlag
CONTRACT["UpdateIsAnNPCMovingFlag"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["UpdateIsAnNPCMovingFlag"] = [
    {"hl": sym("wNameBuffer"), "wram": {wIsAnNPCMoving: b"\x00", sym("wNameBuffer") + 5: b"\x00"}, "expect": {wIsAnNPCMoving: b"\x00"}, "expect_regs": {"a": 0x00, "f": 0x80}},
    {"hl": sym("wNameBuffer"), "wram": {wIsAnNPCMoving: b"\x01", sym("wNameBuffer") + 5: b"\x02"}, "expect": {wIsAnNPCMoving: b"\x03"}, "expect_regs": {"a": 0x03, "f": 0x00}},
    {"hl": sym("wNameBuffer"), "wram": {wIsAnNPCMoving: b"\x80", sym("wNameBuffer") + 5: b"\x01"}, "expect": {wIsAnNPCMoving: b"\x81"}, "expect_regs": {"a": 0x81, "f": 0x00}},
    dict(POISON, hl=sym("wNameBuffer"), wram={wIsAnNPCMoving: b"\x20", sym("wNameBuffer") + 5: b"\x04"}, expect={wIsAnNPCMoving: b"\x24"}, expect_regs={"a": 0x24, "f": 0x00}),
]
# <<< factory UpdateIsAnNPCMovingFlag

# >>> factory ClearNPCs
CONTRACT["ClearNPCs"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")};
CASES["ClearNPCs"] = [
	{"wram": {sym("wLoadedNPC1ID"): b"\xFF" * 0x60, sym("wNumLoadedNPCs"): b"\x7F", sym("wRonaldIsInMap"): b"\x01"}, "expect": {sym("wLoadedNPC1ID"): b"\x00" * 0x60, sym("wNumLoadedNPCs"): b"\x00", sym("wRonaldIsInMap"): b"\x00"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	{"wram": {sym("wLoadedNPC1ID"): bytes(range(0x60)), sym("wNumLoadedNPCs"): b"\xAA", sym("wRonaldIsInMap"): b"\xBB"}, "expect": {sym("wLoadedNPC1ID"): b"\x00" * 0x60, sym("wNumLoadedNPCs"): b"\x00", sym("wRonaldIsInMap"): b"\x00"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	dict(POISON, wram={sym("wLoadedNPC1ID"): b"\xA5" * 0x60, sym("wNumLoadedNPCs"): b"\x5A", sym("wRonaldIsInMap"): b"\xC3"}, expect={sym("wLoadedNPC1ID"): b"\x00" * 0x60, sym("wNumLoadedNPCs"): b"\x00", sym("wRonaldIsInMap"): b"\x00"}, expect_regs={"a": 0x00, "f": 0xC0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}),
]
# <<< factory ClearNPCs

# >>> factory SetAllNPCTilePermissions
CONTRACT["SetAllNPCTilePermissions"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["SetAllNPCTilePermissions"] = [
	{"wram": {sym("wLoadedNPC1ID"): b"\x01\x00\x00\x00" + b"\x00" * 92, sym("wBoosterViableCardList"): b"\xFF"}, "expect": {sym("wBoosterViableCardList"): b"\x40"}, "expect_regs": {"a": 0x00, "f": 0xC0}},
	{"wram": {sym("wLoadedNPC1ID"): b"\x00" * 84 + b"\x01\x00\x0E\x10" + b"\x00" * 8, sym("wBoosterViableCardList") + 0x87: b"\x7F"}, "expect": {sym("wBoosterViableCardList") + 0x87: b"\x40"}, "expect_regs": {"a": 0x40, "f": 0xC0}},
	dict(POISON, wram={sym("wLoadedNPC1ID"): b"\x00" * 96, sym("wLoadedNPCTempIndex"): b"\x77"}, expect_regs={"a": 0x00, "f": 0xC0}),
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
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x01\x02\x00\x00", sym("wNumLoadedNPCs"): b"\x03"}, "expect": {sym("wLoadedNPC1ID"): b"\x00\x02", sym("wNumLoadedNPCs"): b"\x02"}},
	{"wram": {sym("wLoadedNPCTempIndex"): b"\x00", sym("wLoadedNPC1ID"): b"\x71\x03\x00\x00", sym("wNumLoadedNPCs"): b"\x02", sym("wRonaldIsInMap"): b"\x01"}, "expect": {sym("wLoadedNPC1ID"): b"\x00\x03", sym("wNumLoadedNPCs"): b"\x01", sym("wRonaldIsInMap"): b"\x00"}},
	dict(POISON, wram={sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC2ID"): b"\x01\x04\x00\x00", sym("wNumLoadedNPCs"): b"\x05"}, expect={sym("wLoadedNPC2ID"): b"\x00\x04", sym("wNumLoadedNPCs"): b"\x04"}),
	dict(POISON, wram={sym("wLoadedNPCTempIndex"): b"\x01", sym("wLoadedNPC2ID"): b"\x72\x07\x00\x00", sym("wNumLoadedNPCs"): b"\x01", sym("wRonaldIsInMap"): b"\x01"}, expect={sym("wLoadedNPC2ID"): b"\x00\x07", sym("wNumLoadedNPCs"): b"\x00", sym("wRonaldIsInMap"): b"\x00"}),
]
# <<< factory UnloadNPC

# >>> factory Func_1c52e
CONTRACT["Func_1c52e"] = {"compare": ("a", "b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Func_1c52e"] = [
    {"a": 0x00, "wram": {sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x00"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x200}, "expect": {sym("wTempObjectPalettesCGB") + 0x30: b"\x00"}},
    {"a": 0x7F, "wram": {sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x01"}, "read": {sym("wTempObjectPalettesCGB") + 0x29: 0x200}, "expect": {sym("wTempObjectPalettesCGB") + 0x3C: b"\x7F"}},
    dict(POISON, a=0x33, wram={sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x00"}, read={sym("wTempObjectPalettesCGB") + 0x29: 0x200}, expect={sym("wTempObjectPalettesCGB") + 0x30: b"\x33"}),
    dict(POISON, a=0xFF, wram={sym("wTempObjectPalettesCGB") + 0x29: bytes(range(256)) * 2, sym("wLoadedNPCTempIndex"): b"\x01"}, read={sym("wTempObjectPalettesCGB") + 0x29: 0x200}, expect={sym("wTempObjectPalettesCGB") + 0x3C: b"\xFF"}),
]
# <<< factory Func_1c52e

# >>> factory UpdateNPCMovementStep
CONTRACT["UpdateNPCMovementStep"] = {"compare": ("a", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl"), "wram_out": True}
CASES["UpdateNPCMovementStep"] = [
    {"a": 0x17, "hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer") + 5: b"\x00", sym("wNameBuffer") + 8: b"\x0F"}, "expect": {sym("wNameBuffer") + 8: b"\x0F"}, "expect_regs": {"a": 0x17}},
    {"a": 0x42, "hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer") + 5: b"\x20", sym("wNameBuffer") + 8: b"\x00"}, "expect": {sym("wNameBuffer") + 8: b"\x01"}, "expect_regs": {"a": 0x42}},
    {"a": 0x99, "hl": sym("wNameBuffer"), "wram": {sym("wNameBuffer") + 5: b"\x20", sym("wNameBuffer") + 8: b"\x0E"}, "expect": {sym("wNameBuffer") + 8: b"\x0F"}, "expect_regs": {"a": 0x99}},
    dict(POISON, hl=sym("wNameBuffer"), wram={sym("wNameBuffer") + 5: b"\x20", sym("wNameBuffer") + 8: b"\x0E"}, expect={sym("wNameBuffer") + 8: b"\x0F"}, expect_regs={"a": 0xAA}),
]
# <<< factory UpdateNPCMovementStep

# >>> factory FindNPCAtLocation
CONTRACT["FindNPCAtLocation"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")}
CASES["FindNPCAtLocation"] = [
    {"b": 0x05, "c": 0x07, "d": 0x11, "e": 0x22, "hl": 0x3344,
     "wram": {sym("wLoadedNPC1Sprite"): b"\x01", sym("wLoadedNPC1CoordX"): b"\x05\x07", sym("wLoadedNPC1Field0x05"): b"\x00"}},
    dict(POISON, b=0x09, c=0x0A,
         wram={sym("wLoadedNPC2Sprite"): b"\x01", sym("wLoadedNPC2CoordX"): b"\x09\x0A", sym("wLoadedNPC2Field0x05"): b"\x00",
               sym("wLoadedNPC1CoordX"): b"\x00\x00"}),
    {"b": 0xFF, "c": 0x00, "d": 0x11, "e": 0x22, "hl": 0x3344},
]
# <<< factory FindNPCAtLocation

# >>> factory HandleAllNPCMovement
CONTRACT["HandleAllNPCMovement"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["HandleAllNPCMovement"] = [
    {"wram": {wIsAnNPCMoving: b"\xFF", wNumLoadedNPCs: b"\x00"},
     "read": {wIsAnNPCMoving: 1}},
    {"wram": {wIsAnNPCMoving: b"\xFF", wNumLoadedNPCs: b"\x01",
              wLoadedNPCs: npc_entry(0, 0, 0, 0)},
     "read": {wIsAnNPCMoving: 1, wLoadedNPCs: 12}},
    dict(POISON, wram={wIsAnNPCMoving: b"\x00", wNumLoadedNPCs: b"\x01",
                       wLoadedNPCs: npc_entry(5, 3, 0x0A, 0x0B),
                       wPermissionMap + 0x55: b"\x10",
                       SPRITE_BUFFER + 3 * 16 + 1: b"\x00",
                       SPRITE_BUFFER + 3 * 16 + 2: b"\x00",
                       SPRITE_BUFFER + 3 * 16 + 3: b"\x00",
                       SPRITE_BUFFER + 3 * 16 + 15: b"\x00",
                       hSCX: b"\x00", hSCY: b"\x00"},
         read={wIsAnNPCMoving: 1, wLoadedNPCs: 12, wWhichSprite: 1,
               SPRITE_BUFFER + 3 * 16 + 1: 3, SPRITE_BUFFER + 3 * 16 + 15: 1}),
    dict(_npc_move_fixture(bank=7), **_NPC_MOVE_REGS),
]
# <<< factory HandleAllNPCMovement

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
# >>> factory-mutation FindNPCAtLocation
MUTATIONS["FindNPCAtLocation"] = {"source_symbol": "FindNPCAtLocation", "before": "if (active != 0u) {", "after": "if (active == 0u) {", "case_ids": ["FindNPCAtLocation-0", "FindNPCAtLocation-1"]}
# <<< factory-mutation FindNPCAtLocation
# >>> factory-mutation HandleAllNPCMovement
MUTATIONS["HandleAllNPCMovement"] = {"source_symbol": "HandleAllNPCMovement", "before": "wWhichSprite = a;", "after": "wWhichSprite = 0u;", "case_ids": ["HandleAllNPCMovement-2"]}
# <<< factory-mutation HandleAllNPCMovement
