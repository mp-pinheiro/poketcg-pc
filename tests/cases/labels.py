from tests.cases._symbols import HRAM_START, sym
SRC = sym("wDecompressionSecondaryBufferStart") + 0x11
HFFB0 = sym("hffb0")

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "PrintLabels": {
        # b/c are clobbered mid-flight by the text engine on any real label
        # entry and hold no defined exit value (init/print residue), so only
        # the defined exits are pinned.
        "compare": ("d", "e", "hl"),
        "preserve": (),
    },
}

# print_text.py's proven text-id-1 primaries: SetupText primes the engine,
# CACHE_READ covers the glyph LRU tables, VRAM_READ the generated tiles.
SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CACHE_READ = {sym("wc600") + 0x20: 4, sym("wc700") + 0x20: 4, sym("wc800") + 0x20: 4, sym("wc900") + 0x20: 4, sym("wCurTextTile"): 2, sym("wFontWidth"): 1}
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES = {
    "PrintLabels": [
        {"hl": SRC, "d": 0, "e": 0, "wram": {SRC: b"\x80", HFFB0: b"\x02"},
         "read": {SRC: 1, HFFB0: 1}},
        dict(POISON, hl=SRC, d=0, e=0, wram={SRC: b"\x80", HFFB0: b"\x02"},
             read={SRC: 1, HFFB0: 1}),
        {"hl": SRC, "d": 0x12, "e": 0x34,
         "oracle": False,
         "why": "text printing reaches banked text data outside the standalone label oracle contract",
         "wram": {SRC: b"\x01\x00\x00\x00\x80", HFFB0: b"\x02", sym("wLCDC"): b"\x00"},
         "expect": {HFFB0: b"\x02", sym("hTextBGMap0Address"): b"\x01\x98", sym("hTextHorizontalAlign"): b"\x01"},
         "expect_regs": {"b": 0, "c": 0, "d": 0x80, "e": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x16}},
        dict(POISON, hl=SRC, d=0x12, e=0x34,
             oracle=False,
             why="text printing reaches banked text data outside the standalone label oracle contract",
             wram={SRC: b"\x01\x00\x00\x00\x80", HFFB0: b"\x02", sym("wLCDC"): b"\x00"},
             expect={HFFB0: b"\x02", sym("hTextBGMap0Address"): b"\x01\x98", sym("hTextHorizontalAlign"): b"\x01"},
             expect_regs={"b": 0xBB, "c": 0xCC, "d": 0x80, "e": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x16}),
        {"hl": HRAM_START + 0x7C, "d": 0x12, "e": 0x34,
         "oracle": False,
         "why": "the two-pass label scan wraps its list pointer from $FFFF to $0000, outside the oracle snapshot",
         "wram": {HRAM_START + 0x7C: b"\x01\x00\x00\x00", 0x0000: b"\x80", HFFB0: b"\x02", sym("wLCDC"): b"\x00"},
         "expect": {HFFB0: b"\x02"},
         "read": {HRAM_START + 0x7C: 4, 0x0000: 1, HFFB0: 1, sym("wLCDC"): 1}},
        # A real label entry drives the text engine twice: once under the
        # stored hffb0=$02 (pass 1) and once under the restored value (pass
        # 2), so both the second-pass rewind and the reprint are exercised.
        # The trailing $80 sentinel keeps a skipped rewind inside seeded
        # memory, and the probes cover the glyph LRU chain, the generated
        # tiles, and the exit list pointer -- the observable state of both
        # passes.
        {"hl": SRC, "d": 0, "e": 0,
         "setup": SETUP,
         "wram": {SRC: b"\x00\x00\x01\x00\x80\x80", HFFB0: b"\x02"},
         "read": {**CACHE_READ, SRC: 6, HFFB0: 1},
         "vread": VRAM_READ,
         "instruction_budget": 1000000, "cycle_budget": 4000000},
    ],
}
# >>> factory InitAndPrintMenu
CONTRACT["InitAndPrintMenu"] = {"compare": (), "preserve": (), "wram_out": True}
CASES["InitAndPrintMenu"] = [
    {"hl": sym("wNameBuffer"), "a": 0x05, "wram": {sym("wNameBuffer"): b"\x00\x00\x04\x04\x80"},
     "read": {sym("wCurMenuItem"): 1}},
    dict(POISON, hl=sym("wNameBuffer"), wram={sym("wNameBuffer"): b"\x00\x00\x04\x04\x80"}),
]
# <<< factory InitAndPrintMenu

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "PrintLabels": {
        "source_symbol": "PrintLabels",
        "before": "\thl = start;",
        "after": "\thl = (uint16_t)(hl + 0u);",
        "case_ids": ["PrintLabels-5", "PrintLabels-2", "PrintLabels-0", "PrintLabels-1", "PrintLabels-3", "PrintLabels-4"],
    },
}
# >>> factory-mutation InitAndPrintMenu
MUTATIONS["InitAndPrintMenu"] = {"source_symbol": "InitAndPrintMenu", "before": "InitializeMenuParameters(a, &menu_hl);", "after": "InitializeMenuParameters((uint8_t)(a + 1u), &menu_hl);", "case_ids": ["InitAndPrintMenu-0"]}
# <<< factory-mutation InitAndPrintMenu
