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

rSTAT = 0xFF41
rLCDC = 0xFF40
rLYC = 0xFF45
rWX = 0xFF4B
rIE = 0xFFFF

CONTRACT = {
	"ApplyBackgroundScroll": {
		"compare": ("a", "f", "b", "c", "d", "e", "hl"),
		"preserve": ("a", "f", "b", "c", "d", "e", "hl"),
	},
}

CASES = {
	"ApplyBackgroundScroll": [
		{"oracle": False,
		 "why": "The leaf oracle does not advance the PPU LY register.",
		 "wram": {rLY: b"\x00", wApplyBGScroll: b"\x00"},
		 "expect": {rSTAT: b"\x40", rIE: b"\x02", rSCX: b"\x00",
		            rLYC: b"\x00", hSCX: b"\x00",
		            wApplyBGScroll: b"\x00", wNextScrollLY: b"\x60"}},
		dict(POISON, wram={rLY: b"\x00", wApplyBGScroll: b"\x01"},
		     read={rSTAT: 1, rIE: 1, wApplyBGScroll: 1}),
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
	"ApplyBackgroundScroll": {
		"source_symbol": "ApplyBackgroundScroll",
		"before": "if (gb_read8(wApplyBGScroll_ADDR) != 0)",
		"after": "if (gb_read8(wApplyBGScroll_ADDR) == 0)",
		"case_ids": ["ApplyBackgroundScroll-0", "ApplyBackgroundScroll-1", "ApplyBackgroundScroll-2", "ApplyBackgroundScroll-3"],
	},
}
