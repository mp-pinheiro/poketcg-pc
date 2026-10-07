from tests.cases._symbols import sym
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

WCONSOLE = sym("wConsole")
WLCDC = sym("wLCDC")
WBGP = sym("wBGP")
WOBP0 = sym("wOBP0")
WOBP1 = sym("wOBP1")
WFLAG = sym("wFlushPaletteFlags")
WVBL = sym("wVBlankOAMCopyToggle")
WBG = sym("wBackgroundPalettesCGB")
WOBJ = sym("wObjectPalettesCGB")
WTEXT = sym("wTextBoxFrameType")
OAM = sym("wOAM")
HBANK = sym("hBankROM")
HSCROLL = sym("hSCX")

OAM_SEED = b"\xff\x00\x00\x00" * 40

CONTRACT = {
    "SetDefaultPalettes": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "Func_12871": {"compare": ("b", "d", "e"), "preserve": ("b", "d", "e")},
}

CASES = {
    "SetDefaultPalettes": [
        {"wram": {WCONSOLE: b"\x00", HBANK: b"\x04",
                  WBGP: b"\x00", WOBP0: b"\x00", WOBP1: b"\x00",
                  WTEXT: b"\x00", 0xFF47: b"\xfc", 0xFF48: b"\xff",
                  0xFF49: b"\xff"},
         "read": {WBGP: 1, WOBP0: 1, WOBP1: 1, WTEXT: 1, HBANK: 1,
                  WFLAG: 1, 0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
        dict(POISON,
             wram={WCONSOLE: b"\x00", HBANK: b"\x04",
                   WBGP: b"\x11", WOBP0: b"\x22", WOBP1: b"\x33",
                   WTEXT: b"\x55", 0xFF47: b"\xfc", 0xFF48: b"\xff",
                   0xFF49: b"\xff"},
             read={WBGP: 1, WOBP0: 1, WOBP1: 1, WTEXT: 1, HBANK: 1,
                   WFLAG: 1, 0xFF47: 1, 0xFF48: 1, 0xFF49: 1}),
        {"a": 0x01, "wram": {WCONSOLE: b"\x02", HBANK: b"\x04",
                               WBG: b"\x00" * 40, WOBJ: b"\x00" * 8},
         "read": {WBG: 40, WOBJ: 8, WTEXT: 1, HBANK: 1, WFLAG: 1,
                  0xFF47: 1, 0xFF48: 1, 0xFF49: 1}},
    ],
    "Func_12871": [
        {"wram": {WCONSOLE: b"\x00", HBANK: b"\x04", OAM: OAM_SEED, WVBL: b"\x00",
                  WLCDC: b"\x00", HSCROLL: b"\xaa\xbb\xcc\xdd"},
         "read": {OAM: 160, WVBL: 1, WLCDC: 1, HSCROLL: 4,
                  0xFF42: 2, 0xFF4A: 2}},
        dict(POISON,
             wram={WCONSOLE: b"\x00", HBANK: b"\x04", OAM: OAM_SEED, WVBL: b"\x00",
                   WLCDC: b"\x00", HSCROLL: b"\x11\x22\x33\x44"},
             read={OAM: 160, WVBL: 1, WLCDC: 1, HSCROLL: 4,
                   0xFF42: 2, 0xFF4A: 2}),
    ],
}

MUTATIONS = {
    "SetDefaultPalettes": {
        "source_symbol": "SetDefaultPalettes",
        "before": "gb_write8(wTextBoxFrameType_ADDR, 4);",
        "after": "gb_write8(wTextBoxFrameType_ADDR, 5);",
        "case_ids": ["SetDefaultPalettes-0", "SetDefaultPalettes-1", "SetDefaultPalettes-2"],
    },
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS["Func_12871"] = {
    "source_symbol": "Func_12871",
    "before": "\tZeroObjectPositions();",
    "after": "\t;",
    "case_ids": ["Func_12871-0"],
}
