"""Oracle-diff cases for poketcg/src/engine/menus/naming.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory-cases-statics
wNameBuffer = 0xC500
sPlayerName = 0xA010
wRNG1 = 0xCACA
wRNG2 = 0xCACB
wRNGCounter = 0xCACC

# DisplayPlayerNamingScreen farcalls InputPlayerName, whose InitializeInputName
# clears $CFE7-$CFFE and wipes the oracle call frame at $CFF0-$CFF5; after the
# pre-ret capture the PyBoy audit parks the CPU on the wiped stub and decodes
# live WRAM. The naming screen leaves ten bytes at $D000-$D009 whose last
# opcode (`ld bc,d16`) swallows $D00A, so the slide resumes at $D00B:
# `18 fe 00` spins at every alignment and keeps the park harmless. Nothing in
# this routine's call graph writes $D00A-$D015.
DPNS_PARK = b"\x18\xfe\x00" * 4

# CopyDMAFunction installs hDMAFunction (VBlankHandler calls it once
# wVBlankOAMCopyToggle is set); SetupText zeroes the glyph cache the naming
# screen's text printing walks. Holding UP|A ($41) exits InputPlayerName on
# the first pass with an empty name, so wNameBuffer[0] is TX_END and the
# routine falls through to its default-name branch.
DPNS_SETUP = [{"fn": "CopyDMAFunction"}, {"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory DisplayPlayerNamingScreen
CONTRACT["DisplayPlayerNamingScreen"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ()}
CASES["DisplayPlayerNamingScreen"] = [
	{"rom_bank": 4, "keys": 0x41,
	 "wram": {wNameBuffer: b"\xff" * 16, 0xFF90: b"\x00", 0xD00A: DPNS_PARK,
		  wRNG1: b"\x5A", wRNG2: b"\xC3", wRNGCounter: b"\x00"},
	 "sram": {0: {}},
	 "sread": {0: {sPlayerName: 16}},
	 "setup": DPNS_SETUP,
	 "instruction_budget": 20000000, "cycle_budget": 80000000},
	dict(POISON, rom_bank=4, keys=0x41,
	     wram={wNameBuffer: b"\xff" * 16, 0xFF90: b"\x00", 0xD00A: DPNS_PARK,
		   wRNG1: b"\xB7", wRNG2: b"\x2E", wRNGCounter: b"\xFD"},
	     sram={0: {}},
	     sread={0: {sPlayerName: 16}},
	     setup=DPNS_SETUP,
	     instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory DisplayPlayerNamingScreen

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation DisplayPlayerNamingScreen
MUTATIONS["DisplayPlayerNamingScreen"] = {
	"source_symbol": "DisplayPlayerNamingScreen",
	"before": "\t\t\tgb_write8((uint16_t)(sPlayerName_ADDR + i), name[i]);",
	"after": "\t\t\tgb_write8((uint16_t)(sPlayerName_ADDR + i + 1u), name[i]);",
	"case_ids": ["DisplayPlayerNamingScreen-0", "DisplayPlayerNamingScreen-1"],
}
# <<< factory-mutation DisplayPlayerNamingScreen
# >>> factory-completion DisplayPlayerNamingScreen
# InputPlayerName's InitializeInputName clears $CFE7-$CFFE, which wipes the
# oracle call frame at $CFF0-$CFF5, so the default completion hook never fires
# and the run dies on the watchdog. $68EA is this routine's own `ret`:
# `04:68a9 DisplayPlayerNamingScreen` plus its 66 code bytes end at `04:68eb
# .default_name`, and every store the contract observes -- the 16-byte
# sPlayerName copy and both RNG checksum bytes -- has already run there.
for _rec in SCHEMA2_CASES["DisplayPlayerNamingScreen"]:
    _rec["completion"] = {"mode": "pre-ret", "pc": 0x68EA}
# <<< factory-completion DisplayPlayerNamingScreen
