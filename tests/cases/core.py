"""Oracle-diff cases for poketcg/src/engine/duel/core.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory SetLineSeparation
CONTRACT["SetLineSeparation"] = {"compare": ("a",), "preserve": ()}
wLineSeparation = 0xCD08
CASES["SetLineSeparation"] = [
	{"a": 0, "wram": {wLineSeparation: b"\xff"}},
	{"a": 1, "wram": {wLineSeparation: b"\x00"}},
	dict(POISON, a=0x20, wram={wLineSeparation: b"\x00"}),
]
# <<< factory SetLineSeparation

# >>> factory PlayAreaScreenMenuFunction
CONTRACT["PlayAreaScreenMenuFunction"] = {"compare": ("f",), "preserve": ()}
CASES["PlayAreaScreenMenuFunction"] = [
    {"keys": 0},
    {"keys": 0x01},
    {"keys": 0x02},
    {"keys": 0x08},
    dict(POISON, keys=0x02),
    dict(POISON, keys=0x00),
]
# <<< factory PlayAreaScreenMenuFunction

# >>> factory SwitchAttackPage
CONTRACT["SwitchAttackPage"] = {"compare": (), "preserve": ()}
CASES["SwitchAttackPage"] = [
	{"wram": {0xCC04: b"\x00"}, "read": {0xCC04: 1}},
	{"wram": {0xCC04: b"\x01"}, "read": {0xCC04: 1}},
	dict(POISON, wram={0xCC04: b"\xff"}, read={0xCC04: 1}),
]
# <<< factory SwitchAttackPage

# >>> factory CopyCGBCardPalette
CONTRACT["CopyCGBCardPalette"] = {"compare": (), "preserve": ()}
CASES["CopyCGBCardPalette"] = [
    {"wram": {0xCE23: bytes(range(8))}, "read": {0xCAF0: 8}},
    dict(POISON, a=2, wram={0xCE23: bytes(range(0x10, 0x18))},
         read={0xCAF0 + 16: 8}),
]
# <<< factory CopyCGBCardPalette

# >>> factory CreateCardAttrBlkPacket_DataSet
CONTRACT["CreateCardAttrBlkPacket_DataSet"] = {"compare": ("hl",), "preserve": (), "wram_out": True}
CASES["CreateCardAttrBlkPacket_DataSet"] = [
    {"hl": 0xC100, "a": 0, "d": 0, "e": 0, "wram": {0xC100: b"\x00" * 6}, "read": {0xC100: 6}},
    dict(POISON, hl=0xC100, wram={0xC100: b"\x00" * 6}, read={0xC100: 6}),
    {"hl": 0xC100, "a": 0x12, "d": 0x30, "e": 0x40, "wram": {0xC100: b"\x00" * 6}, "read": {0xC100: 6}},
]
# <<< factory CreateCardAttrBlkPacket_DataSet

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation SetLineSeparation
MUTATIONS["SetLineSeparation"] = {
	"source_symbol": "SetLineSeparation",
	"before": "wLineSeparation = a;",
	"after": "wLineSeparation = (uint8_t)(a + 1u);",
	"case_ids": ["SetLineSeparation-0", "SetLineSeparation-1"],
}
# <<< factory-mutation SetLineSeparation
# >>> factory-mutation PlayAreaScreenMenuFunction
MUTATIONS["PlayAreaScreenMenuFunction"] = {
    "source_symbol": "PlayAreaScreenMenuFunction",
    "before": "return 0xA0u;",
    "after": "return 0x80u;",
    "case_ids": ["PlayAreaScreenMenuFunction-0", "PlayAreaScreenMenuFunction-5"],
}
# <<< factory-mutation PlayAreaScreenMenuFunction
# >>> factory-mutation SwitchAttackPage
MUTATIONS["SwitchAttackPage"] = {
	"source_symbol": "SwitchAttackPage",
	"before": "wAttackPageNumber ^ 0x01u",
	"after": "wAttackPageNumber & 0x01u",
	"case_ids": ["SwitchAttackPage-0", "SwitchAttackPage-1"],
}
# <<< factory-mutation SwitchAttackPage
# >>> factory-mutation CopyCGBCardPalette
MUTATIONS["CopyCGBCardPalette"] = {
    "source_symbol": "CopyCGBCardPalette",
    "before": "wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE)",
    "after": "wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE) + 1u",
    "case_ids": ["CopyCGBCardPalette-0", "CopyCGBCardPalette-1"],
}
# <<< factory-mutation CopyCGBCardPalette
# >>> factory-mutation CreateCardAttrBlkPacket_DataSet
MUTATIONS["CreateCardAttrBlkPacket_DataSet"] = {
    "source_symbol": "CreateCardAttrBlkPacket_DataSet",
    "before": "gb_write8(hl++, (uint8_t)(d + 7u));",
    "after": "gb_write8(hl++, (uint8_t)(d + 8u));",
    "case_ids": ["CreateCardAttrBlkPacket_DataSet-2"],
}
# <<< factory-mutation CreateCardAttrBlkPacket_DataSet
