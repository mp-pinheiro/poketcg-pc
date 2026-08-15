"""Oracle-diff cases for poketcg/src/engine/menus/unknown.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Func_18661
hDPadHeld = 0xFF8F
wCheckMenuCursorBlinkCounter = 0xCEA3
wCheckMenuCursorXY = 0xCEAF
CONTRACT["Func_18661"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Func_18661"] = [
	# all-zero: phase 0 -> counter 0->1, bit 4 clear -> cursor tile $0f
	# written at column 1, row 14 ($99c1); exits a=$0f, f=$00.
	{"read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# poisoned entry registers prove the routine is memory-only; LEFT held
	# (seeded both via keys and hDPadHeld to be independent of the harness
	# key plumbing): blank $00 at old (0,0), cursor $0f at new (1,0).
	dict(POISON, keys=0x20, wram={hDPadHeld: b"\x20"},
	     read={wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	     vread={0: {0x99C0: 0x50}}),
	# phase 1 -> ret nz with a=1, f=$20 (and sets H), counter becomes 2.
	{"wram": {wCheckMenuCursorBlinkCounter: b"\x01"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# phase 0, new count 16 has bit 4 set -> blank tile $00 drawn; a=0, f=$80.
	{"wram": {wCheckMenuCursorBlinkCounter: b"\x0f"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# phase 0 with nonzero counter, new count 33 has bit 4 clear ->
	# cursor tile $0f drawn; a=$0f, f=$00.
	{"wram": {wCheckMenuCursorBlinkCounter: b"\x20"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# counter wraps 255 -> 0 in RAM while phase 15 returns nz: a=$0f, f=$20.
	{"wram": {wCheckMenuCursorBlinkCounter: b"\xff"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# RIGHT held: x 0->1, blank at old (0,0), SFX, cursor at new (1,0)
	# ($99cb); hKeysPressed only matters for A/B, so dpad bits are inert.
	{"keys": 0x10, "wram": {hDPadHeld: b"\x10"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# UP held: y 0->1, cursor lands at column 1, row 16 ($9a01).
	{"keys": 0x40, "wram": {hDPadHeld: b"\x40"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# DOWN held: same target as UP, distinct asm bit path.
	{"keys": 0x80, "wram": {hDPadHeld: b"\x80"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
	# LEFT+UP held: left/right wins and y stays 0 -- catches a port that
	# swaps the branch priority between the axis checks.
	{"keys": 0x60, "wram": {hDPadHeld: b"\x60"},
	 "read": {wCheckMenuCursorBlinkCounter: 1, wCheckMenuCursorXY: 2},
	 "vread": {0: {0x99C0: 0x50}}},
]
# <<< factory Func_18661

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Func_18661
MUTATIONS["Func_18661"] = {
	"source_symbol": "Func_18661",
	"before": "? SYM_SPACE : SYM_CURSOR_R;",
	"after": "? SYM_CURSOR_R : SYM_SPACE;",
	"case_ids": ["Func_18661-0", "Func_18661-1", "Func_18661-3", "Func_18661-4",
	             "Func_18661-6", "Func_18661-7", "Func_18661-8", "Func_18661-9"],
}
# <<< factory-mutation Func_18661
