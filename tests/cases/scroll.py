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
rLY = 0xFF44
rSCX = 0xFF43
hSCX = 0xFF92
wApplyBGScroll = 0xD667
wNextScrollLY = 0xD668

rLCDC = 0xFF40
rSTAT = 0xFF41
rLYC = 0xFF45
rWX = 0xFF4B
rIE = 0xFFFF

CONTRACT = {
	"Func_3e44": {
		"compare": ("a", "f", "b", "c", "d", "e", "hl"),
		"preserve": ("a", "f", "b", "c", "d", "e", "hl"),
	},
	"GetNextBackgroundScroll": {
		"compare": ("a", "d", "e"),
		"preserve": ("d", "e"),
	},
	"EnableInt_LYCoincidence": {
		"compare": ("b", "c", "d", "e", "hl"),
		"preserve": ("b", "c", "d", "e", "hl"),
	},
	"DisableInt_LYCoincidence": {
		"compare": ("b", "c", "d", "e", "hl"),
		"preserve": ("b", "c", "d", "e", "hl"),
	},
	"ApplyBackgroundScroll": {
		"compare": ("a", "f", "b", "c", "d", "e", "hl"),
		"preserve": ("a", "f", "b", "c", "d", "e", "hl"),
	},
}

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
	"ApplyBackgroundScroll": [
		dict(POISON, wram={rLY: b"\x00", wApplyBGScroll: b"\x01"},
		     read={rSTAT: 1, rIE: 1, wApplyBGScroll: 1}),
		{"oracle": False,
		 "why": "The leaf oracle does not advance the PPU LY register.",
		 "wram": {rLY: b"\x00", wApplyBGScroll: b"\x00"},
		 "expect": {rSTAT: b"\x40", rIE: b"\x02", rSCX: b"\x00",
		            rLYC: b"\x00", hSCX: b"\x00",
		            wApplyBGScroll: b"\x00", wNextScrollLY: b"\x60"}},
		{"oracle": False,
		 "why": "The leaf oracle does not advance the PPU LY register.",
		 "wram": {rLY: b"\x00", wApplyBGScroll: b"\x01"},
		 "expect": {rSTAT: b"\x00", rIE: b"\x00", wApplyBGScroll: b"\x01"}},
		{"oracle": False,
		 "why": "The leaf oracle does not advance the PPU LY register.",
		 "wram": {rLY: b"\x00", wApplyBGScroll: b"\x00",
		          wVBlankCounter: b"\x00", wBGScrollMod: b"\x01"},
		 "expect": {hSCX: b"\x00", wNextScrollLY: b"\x60"}},
	],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Func_3e44": {
        "source_symbol": "Func_3e44",
        "before": "if (guard & 0x01)",
        "after":  "if (guard & 0x02)",
        "case_ids": ["Func_3e44-0", "Func_3e44-1", "Func_3e44-2", "Func_3e44-3", "Func_3e44-4", "Func_3e44-5", "Func_3e44-6"],
    },
	"ApplyBackgroundScroll": {
		"source_symbol": "ApplyBackgroundScroll",
		"before": "if (gb_read8(wApplyBGScroll_ADDR) != 0)",
		"after": "if (gb_read8(wApplyBGScroll_ADDR) == 0)",
		"case_ids": ["ApplyBackgroundScroll-0", "ApplyBackgroundScroll-1", "ApplyBackgroundScroll-2", "ApplyBackgroundScroll-3"],
	},
}
