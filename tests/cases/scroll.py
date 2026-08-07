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
		{"oracle": False,
		 "why": "rWX/rLCDC/rLYC are IO ($FF40-$FF7F), outside the oracle snapshot",
		 "wram": {wd657: b"\x00", wd658: b"\x00", wd64b: b"\xb0", wd651: b"\x50",
		          rLCDC: b"\x00"},
		 "expect": {rWX: b"\xb0", rLCDC: b"\x02", rLYC: b"\x50", wd658: b"\x01"}},
		{"oracle": False,
		 "why": "rWX/rLCDC/rLYC are IO ($FF40-$FF7F), outside the oracle snapshot",
		 "wram": {wd657: b"\x00", wd658: b"\x00", wd64b: b"\x50", wd651: b"\x90",
		          wd665: b"\x00", rLCDC: b"\xff"},
		 "expect": {rWX: b"\x50", rLCDC: b"\xfd", rLYC: b"\x00", wd658: b"\x00"}},
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
		{"oracle": False,
		 "why": "rSTAT is IO ($FF41), outside the oracle snapshot",
		 "wram": {rSTAT: b"\x00", rIE: b"\x00"},
		 "expect": {rSTAT: b"\x40", rIE: b"\x02"}},
		{"oracle": False,
		 "why": "rSTAT is IO ($FF41), outside the oracle snapshot",
		 "wram": {rSTAT: b"\x80", rIE: b"\x00"},
		 "expect": {rSTAT: b"\xc0", rIE: b"\x02"}},
	],
	"DisableInt_LYCoincidence": [
		{"wram": {rIE: b"\x00"}},
		dict(POISON, wram={rIE: b"\x00"}),
		{"wram": {rIE: b"\x02"}},
		{"wram": {rIE: b"\x0f"}},
		{"oracle": False,
		 "why": "rSTAT is IO ($FF41), outside the oracle snapshot",
		 "wram": {rSTAT: b"\x40", rIE: b"\x02"},
		 "expect": {rSTAT: b"\x00", rIE: b"\x00"}},
	],
}
