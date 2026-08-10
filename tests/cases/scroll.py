"""Oracle-diff cases for scroll.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

wd64b = 0xD64B
wd651 = 0xD651
wd657 = 0xD657
wd658 = 0xD658
wd659 = 0xD659
wd65f = 0xD65F
wd665 = 0xD665
wVBlankCounter = 0xCAB8
wBGScrollMod = 0xD666

rLCDC = 0xFF40
rSTAT = 0xFF41
rLYC = 0xFF45
rWX = 0xFF4B
rIE = 0xFFFF

CONTRACT = {
	"Func_3e44": ("a", "f", "b", "c", "d", "e", "hl"),
	"GetNextBackgroundScroll": ("a", "d", "e"),
	"EnableInt_LYCoincidence": ("b", "c", "d", "e", "hl"),
	"DisableInt_LYCoincidence": ("b", "c", "d", "e", "hl"),
}

# ApplyBackgroundScroll (scroll.asm:60) is intentionally absent: its .wait_ly
# loop polls rLY ($FF44), which only advances on a PPU tick, and the leaf oracle
# drives no PPU ticks -- so it spins past MAX_FRAMES and never returns. Its only
# helper not already covered, GetNextBackgroundScroll, IS ported on its own.

CASES = {
	"Func_3e44": [
		{"wram": {wd657: b"\x00", wd658: b"\x00", wd64b: b"\x00" * 6,
		          wd651: b"\x00" * 6, wd665: b"\x00"}},
		dict(POISON,
		     wram={wd657: b"\x00", wd658: b"\x00", wd64b: b"\x00" * 6,
		           wd651: b"\x00" * 6, wd665: b"\x00"}),
		{"wram": {wd657: b"\x00", wd658: b"\x00",
		          wd64b: b"\x11\x22\x33\x44\x55\x66",
		          wd651: b"\x8f\x00\x00\x00\x00\x00",
		          wd659: b"\xaa\xbb\xcc\xdd\xee\xff",
		          wd65f: b"\x01\x02\x03\x04\x05\x06",
		          wd665: b"\x01"}},
		{"wram": {wd657: b"\x00", wd658: b"\x05",
		          wd651: b"\x00\x00\x00\x00\x00\x90",
		          wd665: b"\x00"}},
		{"wram": {wd657: b"\x01", wd658: b"\x42"}},
		{"wram": {wd657: b"\x00", wd658: b"\x00", wd64b: b"\xb0", wd651: b"\x50",
		          rLCDC: b"\x00"},
		 "read": {rWX: 1, rLCDC: 1, rLYC: 1, wd658: 1}},
		{"wram": {wd657: b"\x00", wd658: b"\x00", wd64b: b"\x50", wd651: b"\x90",
		          wd665: b"\x00", rLCDC: b"\xff"},
		 "read": {rWX: 1, rLCDC: 1, rLYC: 1, wd658: 1}},
	],
	"GetNextBackgroundScroll": [
		{"wram": {wVBlankCounter: b"\x00", wBGScrollMod: b"\x00"}},
		dict(POISON, wram={wVBlankCounter: b"\x00", wBGScrollMod: b"\x01"}),
		{"a": 0x30, "wram": {wVBlankCounter: b"\x00", wBGScrollMod: b"\x01"}},
		{"a": 0x30, "wram": {wVBlankCounter: b"\x00", wBGScrollMod: b"\x02"}},
		{"a": 0x30, "wram": {wVBlankCounter: b"\x00", wBGScrollMod: b"\x03"}},
		{"a": 0x30, "wram": {wVBlankCounter: b"\x00", wBGScrollMod: b"\x00"}},
		{"a": 0x30, "wram": {wVBlankCounter: b"\x00", wBGScrollMod: b"\x04"}},
		{"a": 0x40, "wram": {wVBlankCounter: b"\x3f", wBGScrollMod: b"\x01"}},
	],
	"EnableInt_LYCoincidence": [
		{"wram": {rIE: b"\x00"}},
		dict(POISON, wram={rIE: b"\x00"}),
		{"wram": {rIE: b"\x02"}},
		{"wram": {rIE: b"\x01"}},
		{"wram": {rSTAT: b"\x00", rIE: b"\x00"},
		 "read": {rSTAT: 1, rIE: 1}},
		{"wram": {rSTAT: b"\x80", rIE: b"\x00"},
		 "read": {rSTAT: 1, rIE: 1}},
	],
	"DisableInt_LYCoincidence": [
		{"wram": {rIE: b"\x00"}},
		dict(POISON, wram={rIE: b"\x00"}),
		{"wram": {rIE: b"\x02"}},
		{"wram": {rIE: b"\x0f"}},
		{"wram": {rSTAT: b"\x40", rIE: b"\x02"},
		 "read": {rSTAT: 1, rIE: 1}},
	],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
