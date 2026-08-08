POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

WCONSOLE = 0xCAB4
WLCDC = 0xCABB
WBGP = 0xCABC
WOBP0 = 0xCABD
WOBP1 = 0xCABE
WFLAG = 0xCABF
WVBL = 0xCAC0
WBG = 0xCAF0
WOBJ = 0xCB30
WTEXT = 0xCCF3
OAM = 0xCA00
HBANK = 0xFF80
HSCROLL = 0xFF92

OAM_SEED = b"\xff\x00\x00\x00" * 40

CONTRACT = {
    "SetDefaultPalettes": ("b", "c", "d", "e", "hl"),
    "Func_12871": ("b", "d", "e"),
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
