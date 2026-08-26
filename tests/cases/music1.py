"""Oracle-diff cases for music1.asm (bank $3d) -- audio music engine."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# -- existing 14 routines -------------------------------------------------

CONTRACT["Music1_EmptyFunc"] = {"compare": (), "preserve": ()}
CASES["Music1_EmptyFunc"] = [{}, POISON]

CONTRACT["Music1_f404e"] = {"compare": (), "preserve": ()}
CASES["Music1_f404e"] = [
    {"a": 0x42, "read": {0xDDF0: 1}},
    dict(POISON, read={0xDDF0: 1}),
]

CONTRACT["Music1_f4066"] = {"compare": (), "preserve": ()}
CASES["Music1_f4066"] = [
    {"wram": {0xDDF2: b"\x00"}},
    {"wram": {0xDDF2: b"\x01"}},
    {"wram": {0xDDF2: b"\xFF"}},
    dict(POISON, wram={0xDDF2: b"\x05"}),
]

CONTRACT["Music1_f406f"] = {"compare": ("b", "c"), "preserve": ("b", "c")}
CASES["Music1_f406f"] = [
    {"a": 0x00, "read": {0xDDF1: 1}},
    {"a": 0x07, "read": {0xDDF1: 1}},
    {"a": 0x77, "read": {0xDDF1: 1}},
    {"a": 0xFF, "read": {0xDDF1: 1}},
    dict(POISON, read={0xDDF1: 1}),
]

CONTRACT["Music1_PlaySong"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["Music1_PlaySong"] = [
    {"a": 0x00, "read": {0xDD80: 1}},
    {"a": 0x1E, "read": {0xDD80: 1}},
    {"a": 0x1F, "read": {0xDD80: 1}},
    {"a": 0xFF, "read": {0xDD80: 1}},
    dict(POISON, read={0xDD80: 1}),
]

CONTRACT["Music1_PlaySFX"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Music1_PlaySFX"] = [
    {"a": 0x00, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "wram": {0xDD83: b"\x0A", 0xDD82: b"\x05"}},
    {"a": 0x01, "wram": {0xDD83: b"\x05", 0xDD82: b"\x80"}},
    dict(POISON, read={0xDD83: 1, 0xDD82: 1}),
]

CONTRACT["Music1_AssertSongFinished"] = {"compare": ("a",), "preserve": ()}
CASES["Music1_AssertSongFinished"] = [
    {"wram": {0xDD80: b"\x80"}},
    {"wram": {0xDD80: b"\x00"}},
    {"wram": {0xDD80: b"\x7F"}},
    dict(POISON, wram={0xDD80: b"\xFF"}),
]

CONTRACT["Music1_AssertSFXFinished"] = {"compare": ("a",), "preserve": ()}
CASES["Music1_AssertSFXFinished"] = [
    {"wram": {0xDD82: b"\x80"}},
    {"wram": {0xDD82: b"\x00"}},
    dict(POISON, wram={0xDD82: b"\x55"}),
]

CONTRACT["Music1_CheckForEndOfSong"] = {"compare": (), "preserve": ()}
CASES["Music1_CheckForEndOfSong"] = [
    {"wram": {0xDD8D: b"\x01\x01\x01\x01"}},
    {"wram": {0xDD8D: b"\x00\x00\x00\x00", 0xDD80: b"\x05"}},
    {"wram": {0xDD8D: b"\x00\x00\x00\x01", 0xDD80: b"\x05"}},
    dict(POISON, wram={0xDD8D: b"\x00\x00\x00\x00", 0xDD80: b"\x05"}),
]

CONTRACT["Music1_f4980"] = {"compare": (), "preserve": ()}
CASES["Music1_f4980"] = [
    {"wram": {0xDD8C: b"\x00"}},
    {"wram": {0xDD8C: b"\x0F"}},
    dict(POISON, wram={0xDD8C: b"\x00"}),
]

CONTRACT["Music1_CopyData"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["Music1_CopyData"] = [
    {"a": 0, "hl": 0xC100, "d": 0xC2, "e": 0x00, "read": {0xC200: 0}},
    {"a": 5, "hl": 0xC100, "d": 0xC2, "e": 0x00,
     "wram": {0xC100: b"\x01\x02\x03\x04\x05"}, "read": {0xC200: 5}},
    dict(POISON, a=3, hl=0xC100, d=0xC2, e=0x00,
         wram={0xC100: b"\xAA\xBB\xCC"}, read={0xC200: 3}),
]

CONTRACT["Music1_Init"] = {"compare": (), "preserve": ()}
CASES["Music1_Init"] = [
    {"read": {0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4, 0xDDB3: 4,
              0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1, 0xDDF3: 8, 0xDDF0: 1,
              0xDDF2: 1, 0xDD8C: 1, 0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}},
    dict(POISON, read={0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4,
                       0xDDB3: 4, 0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1,
                       0xDDF3: 8, 0xDDF0: 1, 0xDDF2: 1, 0xDD8C: 1,
                       0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}),
]

CONTRACT["Music1_StopAllChannels"] = {"compare": (), "preserve": ()}
CASES["Music1_StopAllChannels"] = [
    {"wram": {0xDD8C: b"\x00"}, "read": {0xDD8D: 4}},
    {"wram": {0xDD8C: b"\x0F"}, "read": {0xDD8D: 4}},
    {"wram": {0xDD8C: b"\x05"}, "read": {0xDD8D: 4}},
    dict(POISON, wram={0xDD8C: b"\x00"}, read={0xDD8D: 4}),
]

CONTRACT["Music1_BeginSong"] = {"compare": (), "preserve": ()}
CASES["Music1_BeginSong"] = [
    {"a": 0x00, "read": {0xDD81: 1, 0xDD95: 8, 0xDD9D: 8, 0xDDBB: 4,
                          0xDD8D: 4, 0xDD91: 4, 0xDDEA: 4, 0xDDBF: 4,
                          0xDDDF: 4, 0xDDCB: 4, 0xDDF3: 8, 0xDDC7: 4,
                          0xDDF2: 1}},
    {"a": 0x01, "read": {0xDD81: 1, 0xDD95: 8, 0xDD8D: 4, 0xDDF2: 1}},
    dict(POISON, a=0x01, read={0xDD81: 1, 0xDD95: 8, 0xDD8D: 4, 0xDDF2: 1}),
]

# -- Stack helpers --------------------------------------------------------

CONTRACT["Music1_GetChannelStackPointer"] = {"compare": ("hl", "c"), "preserve": ("c",)}
CASES["Music1_GetChannelStackPointer"] = [
    {"c": 0, "wram": {0xDDF3: b"\x00\xC1"}, "read": {0xDDF3: 8}},
    {"c": 1, "wram": {0xDDF3: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4"}, "read": {0xDDF3: 8}},
    {"c": 3, "wram": {0xDDF3: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4"},
     "read": {0xDDF3: 8}},
    dict(POISON, b=0, c=2, wram={0xDDF3: b"\x34\x12\x78\x56\xBC\x9A\xF0\xDE"},
         read={0xDDF3: 8}),
]

CONTRACT["Music1_SetChannelStackPointer"] = {"compare": ("c",), "preserve": ("c",)}
CASES["Music1_SetChannelStackPointer"] = [
    {"c": 0, "hl": 0xC100, "read": {0xDDF3: 2}},
    {"c": 2, "hl": 0xC200, "read": {0xDDF3: 8}},
    {"c": 3, "hl": 0xC300,
     "wram": {0xDDF3: b"\x00\x00\x00\x00\x00\x00\x00\x00"},
     "read": {0xDDF3: 8}},
    dict(POISON, b=0, c=1, hl=0xC1FF, read={0xDDF3: 8}),
]

# -- Channel output routines ----------------------------------------------

CONTRACT["Music1_f4714"] = {"compare": (), "preserve": ()}
CASES["Music1_f4714"] = [
    {"wram": {0xDD8C: b"\x00", 0xDDB7: b"\x00", 0xDD91: b"\x00"},
     "read": {0xDD91: 1}},
    {"wram": {0xDD8C: b"\x01", 0xDDB7: b"\x00"},
     "read": {0xDD91: 1, 0xDDB7: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDB7: b"\x10", 0xDD91: b"\x80",
              0xDDE7: b"\x77", 0xDD86: b"\xC0", 0xDDA5: b"\x2C", 0xDDA6: b"\x80"},
     "read": {0xDD91: 1, 0xDDB7: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDB7: b"\x10", 0xDD91: b"\x02",
              0xDDE7: b"\x55", 0xDD86: b"\x40", 0xDDA5: b"\x9C", 0xDDA6: b"\x00"},
     "read": {0xDD91: 1, 0xDDB7: 1}},
    dict(POISON, wram={0xDD8C: b"\x00", 0xDDB7: b"\x10", 0xDD91: b"\x03",
                       0xDDE7: b"\x33", 0xDD86: b"\x80", 0xDDA5: b"\x2C",
                       0xDDA6: b"\x80"},
         read={0xDD91: 1, 0xDDB7: 1}),
]

CONTRACT["Music1_f475a"] = {"compare": (), "preserve": ()}
CASES["Music1_f475a"] = [
    {"wram": {0xDD8C: b"\x00", 0xDDB8: b"\x00", 0xDD92: b"\x00"},
     "read": {0xDD92: 1}},
    {"wram": {0xDD8C: b"\x02", 0xDDB8: b"\x00"},
     "read": {0xDD92: 1, 0xDDB8: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDB8: b"\x10", 0xDD92: b"\x80",
              0xDDE8: b"\x77", 0xDD87: b"\xC0", 0xDDA7: b"\x2C", 0xDDA8: b"\x80"},
     "read": {0xDD92: 1, 0xDDB8: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDB8: b"\x10", 0xDD92: b"\x02",
              0xDDE8: b"\x55", 0xDD87: b"\x40", 0xDDA7: b"\x9C", 0xDDA8: b"\x00"},
     "read": {0xDD92: 1, 0xDDB8: 1}},
    dict(POISON, wram={0xDD8C: b"\x00", 0xDDB8: b"\x10", 0xDD92: b"\x03",
                       0xDDE8: b"\x33", 0xDD87: b"\x80", 0xDDA7: b"\x2C",
                       0xDDA8: b"\x80"},
         read={0xDD92: 1, 0xDDB8: 1}),
]

CONTRACT["Music1_f479c"] = {"compare": (), "preserve": ()}
CASES["Music1_f479c"] = [
    {"wram": {0xDD8C: b"\x00", 0xDDB9: b"\x00", 0xDD8B: b"\x00", 0xDD93: b"\x00"},
     "read": {0xDD93: 1}},
    {"wram": {0xDD8C: b"\x04", 0xDDB9: b"\x00"},
     "read": {0xDD93: 1, 0xDDB9: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDB9: b"\x10", 0xDD93: b"\x80",
              0xDD8B: b"\x00", 0xDDE9: b"\x77", 0xDDA9: b"\x2C", 0xDDAA: b"\x80"},
     "read": {0xDD93: 1, 0xDDB9: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDB9: b"\x10", 0xDD93: b"\x02",
              0xDD8B: b"\x00", 0xDDE9: b"\x55", 0xDDA9: b"\x9C", 0xDDAA: b"\x00"},
     "read": {0xDD93: 1, 0xDDB9: 1}},
    dict(POISON, wram={0xDD8C: b"\x00", 0xDDB9: b"\x10", 0xDD93: b"\x03",
                       0xDD8B: b"\x00", 0xDDE9: b"\x33", 0xDDA9: b"\x2C",
                       0xDDAA: b"\x80"},
         read={0xDD93: 1, 0xDDB9: 1}),
]

CONTRACT["Music1_f480a"] = {"compare": (), "preserve": ()}
CASES["Music1_f480a"] = [
    {"wram": {0xDD8C: b"\x00", 0xDDBA: b"\x00"},
     "read": {0xDDEF: 1, 0xDDAB: 4}},
    {"wram": {0xDD8C: b"\x08", 0xDDBA: b"\x05"},
     "read": {0xDDBA: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDBA: b"\x01", 0xDDAB: b"\x01\x02\x03\x04"},
     "read": {0xDDAB: 4}},
    dict(POISON, wram={0xDD8C: b"\x00", 0xDDBA: b"\xA5",
                       0xDDAB: b"\xAA\xBB\xCC\xDD"},
         read={0xDDAB: 4}),
]

CONTRACT["Music1_f4839"] = {"compare": (), "preserve": ()}
CASES["Music1_f4839"] = [
    {"wram": {0xDD8C: b"\x08", 0xDDEF: b"\x01"},
     "read": {0xDDEF: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDED: b"\x00\xC1",
              0xDDEF: b"\x01", 0xC100: b"\x03"},
     "read": {0xDDED: 2, 0xDDEF: 1}},
    {"wram": {0xDD8C: b"\x00", 0xDDED: b"\x00\xC1",
              0xDDEF: b"\x01", 0xC100: b"\xFF"},
     "read": {0xDDED: 2, 0xDDEF: 1}},
    dict(POISON, wram={0xDD8C: b"\x00", 0xDDED: b"\x50\xC1",
                       0xDDEF: b"\x01", 0xC150: b"\x07"},
         read={0xDDED: 2, 0xDDEF: 1}),
]

CONTRACT["Music1_LoadWaveInstrument"] = {"compare": (), "preserve": ()}
CASES["Music1_LoadWaveInstrument"] = [
    {"wram": {0xDD8A: b"\x00", 0xDD8B: b"\x01"},
     "read": {0xDD8B: 1}},
    {"wram": {0xDD8A: b"\x01", 0xDD8B: b"\x01"},
     "read": {0xDD8B: 1}},
    dict(POISON, wram={0xDD8A: b"\x02", 0xDD8B: b"\x01"},
         read={0xDD8B: 1}),
]

# -- Vibrato --------------------------------------------------------------

CONTRACT["Music1_UpdateVibrato"] = {"compare": ("d", "e", "c"), "preserve": ("c",)}
CASES["Music1_UpdateVibrato"] = [
    {"c": 0, "wram": {0xDDDF: b"\x00", 0xDDA5: b"\x2C\x00"},
     "read": {0xDDA5: 2}},
    {"c": 1, "wram": {0xDDE0: b"\x00", 0xDDA7: b"\x2C\x00"},
     "read": {0xDDA7: 2}},
    {"c": 0, "wram": {0xDDDF: b"\x05", 0xDDE3: b"\x04",
                       0xDDD3: b"\x00", 0xDDDB: b"\x00",
                       0xDDA5: b"\x2C\x00"},
     "read": {0xDDA5: 2, 0xDDE3: 1, 0xDDDB: 1}},
    dict(POISON, b=0, c=2, wram={0xDDE1: b"\x00", 0xDDA9: b"\x2C\x00"},
         read={0xDDA9: 2}),
]

CONTRACT["Music1_f490b"] = {"compare": (), "preserve": ()}
CASES["Music1_f490b"] = [
    {"a": 0, "wram": {0xDDDF: b"\x00", 0xDD8C: b"\x00",
                       0xDDA5: b"\x2C\x00"}},
    {"a": 0, "wram": {0xDDDF: b"\x01", 0xDD8C: b"\x01"},
     "read": {0xDDA5: 2}},
    {"a": 0, "wram": {0xDDDF: b"\x01", 0xDD8C: b"\x00",
                       0xDDA5: b"\x9C\x00"}},
    {"a": 1, "wram": {0xDDE0: b"\x00", 0xDD8C: b"\x00",
                       0xDDA7: b"\x2C\x00"}},
    {"a": 1, "wram": {0xDDE0: b"\x01", 0xDD8C: b"\x02"},
     "read": {0xDDA7: 2}},
    {"a": 1, "wram": {0xDDE0: b"\x01", 0xDD8C: b"\x00",
                       0xDDA7: b"\x9C\x00"}},
    {"a": 2, "wram": {0xDDE1: b"\x00", 0xDD8C: b"\x00",
                       0xDDA9: b"\x2C\x00"}},
    {"a": 2, "wram": {0xDDE1: b"\x01", 0xDD8C: b"\x04"},
     "read": {0xDDA9: 2}},
    {"a": 2, "wram": {0xDDE1: b"\x01", 0xDD8C: b"\x00",
                       0xDDA9: b"\x9C\x00"}},
    {"a": 3, "wram": {0xDD8C: b"\x00", 0xDDA5: b"\x2C\x00"}},
    dict(POISON, a=0, wram={0xDDDF: b"\x01", 0xDD8C: b"\x00",
                             0xDDA5: b"\x06\x03"}),
]

CONTRACT["Music1_f4967"] = {"compare": ("d", "e", "c"), "preserve": ("c",)}
CASES["Music1_f4967"] = [
    {"c": 0, "d": 0x00, "e": 0x2C, "wram": {0xDDEA: b"\x00"}},
    {"c": 0, "d": 0x00, "e": 0x2C, "wram": {0xDDEA: b"\x10"}},
    {"c": 0, "d": 0x03, "e": 0x00, "wram": {0xDDEA: b"\x80"}},
    {"c": 1, "d": 0x00, "e": 0x2C, "wram": {0xDDEB: b"\x20"}},
    dict(POISON, b=0, c=2, d=0x03, e=0x00, wram={0xDDEC: b"\xFF"}),
]

CONTRACT["Music1_f485a"] = {"compare": (), "preserve": ()}
CASES["Music1_f485a"] = [
    {"a": 0, "wram": {0xDDDF: b"\x00", 0xDD8C: b"\x00",
                       0xDDA5: b"\x2C\x00"}},
    {"a": 1, "wram": {0xDDE0: b"\x00", 0xDD8C: b"\x00",
                       0xDDA7: b"\x2C\x00"}},
    dict(POISON, a=0, wram={0xDDDF: b"\x01", 0xDD8C: b"\x00",
                             0xDDA5: b"\x9C\x00"}),
]

# -- Panning / output select ----------------------------------------------

CONTRACT["Music1_f4866"] = {"compare": (), "preserve": ()}
CASES["Music1_f4866"] = [
    {"wram": {0xDDF1: b"\x77", 0xDD8C: b"\x00", 0xDD84: b"\xFF",
              0xDDF0: b"\x00"}},
    {"wram": {0xDDF1: b"\x77", 0xDD8C: b"\x0F", 0xDD84: b"\xFF",
              0xDD85: b"\xFF", 0xDDF0: b"\x00"}},
    {"wram": {0xDDF1: b"\x77", 0xDD8C: b"\x03", 0xDD84: b"\xCC",
              0xDD85: b"\x33", 0xDDF0: b"\xFF"}},
    dict(POISON, wram={0xDDF1: b"\x77", 0xDD8C: b"\x05", 0xDD84: b"\xAA",
                       0xDD85: b"\x55", 0xDDF0: b"\x0F"}),
]

# -- Channel updaters -----------------------------------------------------

CONTRACT["Music1_UpdateChannel1"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel1"] = [
    {"wram": {0xDD8D: b"\x00", 0xDD8C: b"\x00",
              0xDD95: b"\x00\xC1",
              0xDDB7: b"\x00", 0xDDBB: b"\x01", 0xDDDF: b"\x00",
              0xDDA5: b"\x2C\x00"}},
    {"wram": {0xDD8D: b"\x01", 0xDD8C: b"\x00",
              0xDDBB: b"\x01", 0xDDDF: b"\x00",
              0xDDB7: b"\x10", 0xDDC3: b"\x01",
              0xDD95: b"\x00\xC1",
              0xDDE7: b"\x77", 0xDD86: b"\xC0",
              0xDDA5: b"\x9C\x00", 0xDDA6: b"\x00"}},
    dict(POISON, wram={0xDD8D: b"\x01", 0xDD8C: b"\x00",
                       0xDDBB: b"\x01", 0xDDDF: b"\x00",
                       0xDD95: b"\x00\xC1",
                       0xDDB7: b"\x00", 0xDDC3: b"\x01",
                       0xDDA5: b"\x2C\x00"}),
]

CONTRACT["Music1_UpdateChannel2"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel2"] = [
    {"wram": {0xDD8E: b"\x00", 0xDD8C: b"\x00",
              0xDD97: b"\x00\xC1",
              0xDDB8: b"\x00", 0xDDBC: b"\x01", 0xDDE0: b"\x00",
              0xDDA7: b"\x2C\x00"}},
    {"wram": {0xDD8E: b"\x01", 0xDD8C: b"\x00",
              0xDDBC: b"\x01", 0xDDE0: b"\x00",
              0xDDB8: b"\x10", 0xDDC4: b"\x01",
              0xDD97: b"\x00\xC1",
              0xDDE8: b"\x77", 0xDD87: b"\xC0",
              0xDDA7: b"\x9C\x00", 0xDDA8: b"\x00"}},
    dict(POISON, wram={0xDD8E: b"\x01", 0xDD8C: b"\x00",
                       0xDDBC: b"\x01", 0xDDE0: b"\x00",
                       0xDD97: b"\x00\xC1",
                       0xDDB8: b"\x00", 0xDDC4: b"\x01",
                       0xDDA7: b"\x2C\x00"}),
]

CONTRACT["Music1_UpdateChannel3"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel3"] = [
    {"wram": {0xDD8F: b"\x00", 0xDD8C: b"\x00",
              0xDD99: b"\x00\xC1",
              0xDDB9: b"\x00", 0xDDBD: b"\x01", 0xDDE1: b"\x00",
              0xDDA9: b"\x2C\x00", 0xDD8B: b"\x00"}},
    {"wram": {0xDD8F: b"\x01", 0xDD8C: b"\x00",
              0xDDBD: b"\x01", 0xDDE1: b"\x00",
              0xDDB9: b"\x10", 0xDDC5: b"\x01",
              0xDD99: b"\x00\xC1",
              0xDDE9: b"\x77", 0xDDA9: b"\x9C\x00", 0xDDAA: b"\x00",
              0xDD8B: b"\x00"}},
    dict(POISON, wram={0xDD8F: b"\x01", 0xDD8C: b"\x00",
                       0xDDBD: b"\x01", 0xDDE1: b"\x00",
                       0xDD99: b"\x00\xC1",
                       0xDDB9: b"\x00", 0xDDC5: b"\x01",
                       0xDDA9: b"\x2C\x00", 0xDD8B: b"\x00"}),
]

CONTRACT["Music1_UpdateChannel4"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel4"] = [
    {"wram": {0xDD90: b"\x00", 0xDD8C: b"\x00",
              0xDD9B: b"\x00\xC1",
              0xDDBA: b"\x00", 0xDDBE: b"\x01", 0xDDEF: b"\x00"}},
    {"wram": {0xDD90: b"\x01", 0xDD8C: b"\x00",
              0xDDBE: b"\x01", 0xDDEF: b"\x00",
              0xDDAF: b"\x05",
              0xDD9B: b"\x00\xC1",
              0xDDBA: b"\x01",
              0xDDED: b"\x00\xC1",
              0xDDAB: b"\x01\x02\x03\x04"}},
    dict(POISON, wram={0xDD90: b"\x01", 0xDD8C: b"\x00",
                       0xDDBE: b"\x01", 0xDDEF: b"\x00",
                       0xDD9B: b"\x00\xC1",
                       0xDDBA: b"\x00"}),
]

# -- Pause / Resume / Backup / LoadBackup ---------------------------------

CONTRACT["Music1_PauseSong"] = {"compare": (), "preserve": ()}
CASES["Music1_PauseSong"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x00",
              0xDD8D: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x0F",
                       0xDD8D: b"\x01\x01\x01\x01"}),
]

CONTRACT["Music1_ResumeSong"] = {"compare": (), "preserve": ()}
CASES["Music1_ResumeSong"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x00",
              0xDE55: b"\x80", 0xDE56: b"\x3D",
              0xDD8D: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x0F",
                       0xDE55: b"\x81", 0xDE56: b"\x3E",
                       0xDD8D: b"\x01\x01\x01\x01"}),
]

CONTRACT["Music1_BackupSong"] = {"compare": (), "preserve": ()}
CASES["Music1_BackupSong"] = [
    {"wram": {0xDD80: b"\x05", 0xDD81: b"\x3D",
              0xDD84: b"\xFF", 0xDD86: b"\x01\x02\x03\x04",
              0xDD8A: b"\x03", 0xDD8B: b"\x00",
              0xDD8D: b"\x01\x01\x01\x01",
              0xDD91: b"\x01\x01\x01\x01",
              0xDD95: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              0xDD9D: b"\x00\xD1\x00\xD2\x00\xD3\x00\xD4",
              0xDDAB: b"\xAA\xBB",
              0xDDAF: b"\x02\x02\x02\x02",
              0xDDB3: b"\x03\x03\x03\x03",
              0xDDB7: b"\x10\x10\x10\x10",
              0xDDBB: b"\x04\x04\x04\x04",
              0xDDBF: b"\x05\x05\x05\x05",
              0xDDC3: b"\x06\x06\x06\x06",
              0xDDC7: b"\x07\x07\x07\x07",
              0xDDCB: b"\x08\x08\x08\x08",
              0xDDCF: b"\x09\x09\x09\x09",
              0xDDD7: b"\x0A\x0A\x0A\x0A",
              0xDDDF: b"\x0B\x0B\x0B\x0B",
              0xDDE7: b"\x77\x77\x77",
              0xDDEA: b"\x00\x00\x00",
              0xDDED: b"\x50\xC1",
              0xDDF3: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              0xDDFB: b"\x00" * 48},
     "read": {0xDE55: 2}},
    dict(POISON, wram={0xDD80: b"\x05", 0xDD81: b"\x3E",
                       0xDD84: b"\xAA", 0xDD86: b"\x40\x00\x80\xC0",
                       0xDD8A: b"\x00", 0xDD8B: b"\x01",
                       0xDD8D: b"\x00\x00\x00\x01",
                       0xDD91: b"\x00\x00\x00\x01",
                       0xDD95: b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       0xDD9D: b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       0xDDAB: b"\x00\x00",
                       0xDDAF: b"\x00\x00\x00\x00",
                       0xDDB3: b"\x00\x00\x00\x00",
                       0xDDB7: b"\x00\x00\x00\x00",
                       0xDDBB: b"\x00\x00\x00\x00",
                       0xDDBF: b"\x00\x00\x00\x00",
                       0xDDC3: b"\x00\x00\x00\x00",
                       0xDDC7: b"\x00\x00\x00\x00",
                       0xDDCB: b"\x00\x00\x00\x00",
                       0xDDCF: b"\x00\x00\x00\x00",
                       0xDDD7: b"\x00\x00\x00\x00",
                       0xDDDF: b"\x00\x00\x00\x00",
                       0xDDE7: b"\x00\x00\x00",
                       0xDDEA: b"\x00\x00\x00",
                       0xDDED: b"\x00\x00",
                       0xDDF3: b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       0xDDFB: b"\x00" * 48}),
]

CONTRACT["Music1_LoadBackup"] = {"compare": (), "preserve": ()}
CASES["Music1_LoadBackup"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D",
              0xDE55: b"\x05", 0xDE56: b"\x3E",
              0xDE57: b"\xFF",
              0xDE58: b"\x01\x02\x03\x04",
              0xDE5C: b"\x03", 0xDE5D: b"\x00",
              0xDE5E: b"\x01\x01\x01\x01",
              0xDE62: b"\x01\x01\x01\x01",
              0xDE66: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              0xDE6E: b"\x00\xD1\x00\xD2\x00\xD3\x00\xD4",
              0xDE76: b"\xAA", 0xDE77: b"\xBB",
              0xDE78: b"\x02\x02\x02\x02",
              0xDE7C: b"\x03\x03\x03\x03",
              0xDE80: b"\x10\x10\x10\x10",
              0xDE84: b"\x04\x04\x04\x04",
              0xDE88: b"\x05\x05\x05\x05",
              0xDE8C: b"\x06\x06\x06\x06",
              0xDE90: b"\x07\x07\x07\x07",
              0xDE94: b"\x08\x08\x08\x08",
              0xDE98: b"\x09\x09\x09\x09",
              0xDE9C: b"\x0A\x0A\x0A\x0A",
              0xDEA0: b"\x0B\x0B\x0B\x0B",
              0xDEA4: b"\x77\x77\x77",
              0xDEA7: b"\x00\x00\x00",
              0xDEAA: b"\x50\xC1",
              0xDEAC: b"\x00",
              0xDEAD: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              0xDEB5: b"\x00" * 48}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D",
                       0xDE55: b"\x00", 0xDE56: b"\x3D",
                       0xDE57: b"\xAA",
                       0xDE58: b"\x40\x00\x80\xC0",
                       0xDE5C: b"\x00", 0xDE5D: b"\x01",
                       0xDE5E: b"\x00\x00\x00\x01",
                       0xDE62: b"\x00\x00\x00\x01",
                       0xDE66: b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       0xDE6E: b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       0xDE76: b"\x00", 0xDE77: b"\x00",
                       0xDE78: b"\x00\x00\x00\x00",
                       0xDE7C: b"\x00\x00\x00\x00",
                       0xDE80: b"\x00\x00\x00\x00",
                       0xDE84: b"\x00\x00\x00\x00",
                       0xDE88: b"\x00\x00\x00\x00",
                       0xDE8C: b"\x00\x00\x00\x00",
                       0xDE90: b"\x00\x00\x00\x00",
                       0xDE94: b"\x00\x00\x00\x00",
                       0xDE98: b"\x00\x00\x00\x00",
                       0xDE9C: b"\x00\x00\x00\x00",
                       0xDEA0: b"\x00\x00\x00\x00",
                       0xDEA4: b"\x00\x00\x00",
                       0xDEA7: b"\x00\x00\x00",
                       0xDEAA: b"\x00\x00",
                       0xDEAC: b"\x00",
                       0xDEAD: b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       0xDEB5: b"\x00" * 48}),
]

# -- High-level -----------------------------------------------------------

CONTRACT["Music1_CheckForNewSound"] = {"compare": (), "preserve": ()}
CASES["Music1_CheckForNewSound"] = [
    {"wram": {0xDD80: b"\x80", 0xDD82: b"\x80"}},
    {"wram": {0xDD80: b"\x00", 0xDD82: b"\x80",
              0xDD81: b"\x3D",
              0xDD8D: b"\x00\x00\x00\x00"},
     "read": {0xDD80: 1}},
    dict(POISON, wram={0xDD80: b"\x05", 0xDD82: b"\x00",
                       0xDD81: b"\x3D",
                       0xDD8D: b"\x00\x00\x00\x00"},
         read={0xDD80: 1, 0xDD82: 1}),
]

CONTRACT["Music1_Update"] = {"compare": (), "preserve": ()}
CASES["Music1_Update"] = [
    {"wram": {0xDD81: b"\x3D", 0xDDF2: b"\x01",
              0xDD8C: b"\x0F", 0xDD80: b"\x80",
              0xDD82: b"\x80"},
     "read": {0xDD8D: 4}},
    {"wram": {0xDD81: b"\x3D", 0xDDF2: b"\x00",
              0xDD8C: b"\x00", 0xDD80: b"\x80",
              0xDD82: b"\x80",
              0xDD8D: b"\x00\x00\x00\x00",
              0xDDBB: b"\x01\x01\x01\x01",
              0xDDB7: b"\x00\x00\x00\x00",
              0xDDEF: b"\x00",
              0xDD95: b"\x00\xC1\x00\xC1\x00\xC1\x00\xC1",
              0xDDDF: b"\x00\x00\x00\x00",
              0xDDA5: b"\x2C\x00",
              0xDDA7: b"\x2C\x00",
              0xDDA9: b"\x2C\x00",
              0xDDF1: b"\x77",
              0xDD84: b"\xFF", 0xDD85: b"\x00",
              0xDDF0: b"\x00"},
     "read": {0xDD8D: 4}},
    dict(POISON, wram={0xDD81: b"\x3D", 0xDDF2: b"\x01",
                       0xDD8C: b"\x0F", 0xDD80: b"\x80",
                       0xDD82: b"\x80"},
         read={0xDD8D: 4}),
]
# >>> factory _PauseSong
CONTRACT["_PauseSong"] = {"compare": (), "preserve": ()}
CASES["_PauseSong"] = [{}, dict(POISON, wram={0xC100: b"\x00"})]
# <<< factory _PauseSong

# >>> factory _ResumeSong
CONTRACT["_ResumeSong"] = {"compare": (), "preserve": ()}
CASES["_ResumeSong"] = [{}, dict(POISON, wram={0xC101: b"\x00"})]
# <<< factory _ResumeSong

# >>> factory Music1_f400c
CONTRACT["Music1_f400c"] = {"compare": (), "preserve": ()}
CASES["Music1_f400c"] = [
    {"a": 0x42, "read": {0xDDF0: 1}},
    dict(POISON, read={0xDDF0: 1}, wram={0xC103: b"\x00"}),
]
# <<< factory Music1_f400c

# >>> factory Music1_f4018
CONTRACT["Music1_f4018"] = {"compare": ("b", "c"), "preserve": ("b", "c")};
CASES["Music1_f4018"] = [
    {"a": 0x00, "read": {0xDDF1: 1}},
    {"a": 0x07, "read": {0xDDF1: 1}},
    {"a": 0x77, "read": {0xDDF1: 1}},
    dict(POISON, read={0xDDF1: 1}),
]
# <<< factory Music1_f4018

# >>> factory _AssertSFXFinished
CONTRACT["_AssertSFXFinished"] = {"compare": ("a",), "preserve": ()}
CASES["_AssertSFXFinished"] = [
    {"wram": {0xDD82: b"\x80"}},
    {"wram": {0xDD82: b"\x00"}},
    dict(POISON, wram={0xDD82: b"\x55"}),
]
# <<< factory _AssertSFXFinished

# >>> factory _AssertSongFinished
CONTRACT["_AssertSongFinished"] = {"compare": ("a",), "preserve": ()}
CASES["_AssertSongFinished"] = [
    {"wram": {0xDD80: b"\x80"}},
    {"wram": {0xDD80: b"\x00"}},
    {"wram": {0xDD80: b"\x7F"}},
    dict(POISON, wram={0xDD80: b"\xFF"}),
]
# <<< factory _AssertSongFinished

# >>> factory _PlaySFX
CONTRACT["_PlaySFX"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["_PlaySFX"] = [
    {"a": 0x00, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "wram": {0xDD83: b"\x0A", 0xDD82: b"\x05"}},
    {"a": 0x01, "wram": {0xDD83: b"\x05", 0xDD82: b"\x80"}},
    dict(POISON, read={0xDD83: 1, 0xDD82: 1}),
]
# <<< factory _PlaySFX

# >>> factory _PlaySong
CONTRACT["_PlaySong"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["_PlaySong"] = [
    {"a": 0x00, "read": {0xDD80: 1}},
    {"a": 0x1E, "read": {0xDD80: 1}},
    {"a": 0x1F, "read": {0xDD80: 1}},
    {"a": 0xFF, "read": {0xDD80: 1}},
    dict(POISON, read={0xDD80: 1}),
]
# <<< factory _PlaySong

# >>> factory _SetupSound
CONTRACT["_SetupSound"] = {"compare": (), "preserve": ()}
CASES["_SetupSound"] = [
    {"read": {0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4, 0xDDB3: 4,
              0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1, 0xDDF3: 8, 0xDDF0: 1,
              0xDDF2: 1, 0xDD8C: 1, 0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}},
    dict(POISON, read={0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4,
                       0xDDB3: 4, 0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1,
                       0xDDF3: 8, 0xDDF0: 1, 0xDDF2: 1, 0xDD8C: 1,
                       0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}),
]
# <<< factory _SetupSound

# >>> factory SoundTimerHandler
CONTRACT["SoundTimerHandler"] = {"compare": (), "preserve": ()}
CASES["SoundTimerHandler"] = [
    {"wram": {0xDD80: b"\x00", 0xDD82: b"\x80"}, "read": {0xDD80: 1}},
    dict(POISON, wram={0xDD80: b"\x00", 0xDD82: b"\x80"}, read={0xDD80: 1}),
]
# <<< factory SoundTimerHandler

# >>> factory Music1_f4015
CONTRACT["Music1_f4015"] = {"compare": (), "preserve": ()}
CASES["Music1_f4015"] = [
    {"wram": {0xDDF2: b"\x00"}, "expect": {0xDDF2: b"\x01"}},
    {"wram": {0xDDF2: b"\x01"}, "expect": {0xDDF2: b"\x00"}},
    dict(POISON, wram={0xDDF2: b"\x05"}, expect={0xDDF2: b"\x04"}),
]
# <<< factory Music1_f4015

# >>> factory Music1_duty
CONTRACT["Music1_duty"] = {"compare": (), "preserve": ()}
CASES["Music1_duty"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDD86: 1}},
    {"c": 1, "stack": [0xC100], "wram": {0xC100: b"\x3F\xFF"}, "read": {0xDD87: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\x80\xFF"}, "read": {0xDD89: 1}},
    dict(POISON, b=0, c=2, stack=[0xC100], wram={0xC100: b"\xFF\xFF"},
         read={0xDD88: 1}),
]
# <<< factory Music1_duty

# >>> factory Music1_speed
CONTRACT["Music1_speed"] = {"compare": (), "preserve": ()}
CASES["Music1_speed"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF"}, "read": {0xDDCF: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"}, "read": {0xDDCF: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDDD2: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF"},
         read={0xDDD0: 1}),
]
# <<< factory Music1_speed

# >>> factory Music1_inc_octave
CONTRACT["Music1_inc_octave"] = {"compare": (), "preserve": ()}
CASES["Music1_inc_octave"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDDAF: b"\x00"},
     "read": {0xDDAF: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDDAF: b"\xFF"},
     "read": {0xDDAF: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDDB2: b"\x07"},
     "read": {0xDDB2: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\xFF", 0xDDB0: b"\x10"},
         read={0xDDB0: 1}),
]
# <<< factory Music1_inc_octave

# >>> factory Music1_dec_octave
CONTRACT["Music1_dec_octave"] = {"compare": (), "preserve": ()}
CASES["Music1_dec_octave"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDDAF: b"\x01"},
     "read": {0xDDAF: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDDAF: b"\x00"},
     "read": {0xDDAF: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDDB2: b"\x07"},
     "read": {0xDDB2: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\xFF", 0xDDB0: b"\x10"},
         read={0xDDB0: 1}),
]
# <<< factory Music1_dec_octave

# >>> factory Music1_tie
CONTRACT["Music1_tie"] = {"compare": (), "preserve": ()}
CASES["Music1_tie"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDD91: b"\x00"},
     "read": {0xDD91: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF", 0xDD94: b"\xFF"},
     "read": {0xDD94: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\xFF", 0xDD92: b"\x7F"},
         read={0xDD92: 1}),
]
# <<< factory Music1_tie

# >>> factory Music1_stereo_panning
CONTRACT["Music1_stereo_panning"] = {"compare": (), "preserve": ()}
CASES["Music1_stereo_panning"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x11\xFF", 0xDD84: b"\x00"},
     "read": {0xDD84: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF", 0xDD84: b"\xFF"},
     "read": {0xDD84: 1}},
    {"c": 1, "stack": [0xC100], "wram": {0xC100: b"\x11\xFF", 0xDD84: b"\x00"},
     "read": {0xDD84: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\x81\xFF", 0xDD84: b"\x00"},
     "read": {0xDD84: 1}},
    dict(POISON, b=0, c=2, stack=[0xC100], wram={0xC100: b"\x11\xFF", 0xDD84: b"\xAA"},
         read={0xDD84: 1}),
]
# <<< factory Music1_stereo_panning

# >>> factory Music1_MainLoop
CONTRACT["Music1_MainLoop"] = {"compare": (), "preserve": ()}
CASES["Music1_MainLoop"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\xFF"}, "read": {0xDD9D: 2}},
    {"c": 3, "stack": [0xC200], "wram": {0xC200: b"\xFF"}, "read": {0xDDA3: 2}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\xFF"},
         read={0xDD9F: 2}),
]
# <<< factory Music1_MainLoop

# >>> factory Music1_Loop
CONTRACT["Music1_Loop"] = {"compare": (), "preserve": ()}
CASES["Music1_Loop"] = [
    {"c": 0, "stack": [0xC100],
     "wram": {0xC100: b"\x03\xFF", 0xDDF3: b"\x00\xC2"},
     "read": {0xC200: 3, 0xDDF3: 2}},
    {"c": 1, "stack": [0xC100],
     "wram": {0xC100: b"\x01\xFF", 0xDDF5: b"\x00\xC3"},
     "read": {0xC300: 3, 0xDDF5: 2}},
    dict(POISON, b=0, c=2, stack=[0xC100],
         wram={0xC100: b"\xFF\xFF", 0xDDF7: b"\x10\xC2"},
         read={0xC210: 3, 0xDDF7: 2}),
]
# <<< factory Music1_Loop

# >>> factory Music1_call
CONTRACT["Music1_call"] = {"compare": (), "preserve": ()}
CASES["Music1_call"] = [
    {"c": 0, "stack": [0xC100],
     "wram": {0xC100: b"\x00\xC2", 0xC200: b"\xFF", 0xDDF3: b"\x00\xC3"},
     "read": {0xC300: 2, 0xDDF3: 2}},
    {"c": 1, "stack": [0xC110],
     "wram": {0xC110: b"\x00\xC2", 0xC200: b"\xFF", 0xDDF5: b"\x20\xC3"},
     "read": {0xC320: 2, 0xDDF5: 2}},
    dict(POISON, b=0, c=3, stack=[0xC100],
         wram={0xC100: b"\x00\xC2", 0xC200: b"\xFF", 0xDDF9: b"\x40\xC3"},
         read={0xC340: 2, 0xDDF9: 2}),
]
# <<< factory Music1_call

# >>> factory Music1_ret
CONTRACT["Music1_ret"] = {"compare": (), "preserve": ()}
CASES["Music1_ret"] = [
    {"c": 0, "stack": [0xC100],
     "wram": {0xDDF3: b"\x02\xC3", 0xC300: b"\x00\xC2", 0xC202: b"\xFF"},
     "read": {0xDDF3: 2}},
    {"c": 1, "stack": [0xC100],
     "wram": {0xDDF5: b"\x22\xC3", 0xC320: b"\x00\xC2", 0xC202: b"\xFF"},
     "read": {0xDDF5: 2}},
    dict(POISON, b=0, c=3, stack=[0xC100],
         wram={0xDDF9: b"\x42\xC3", 0xC340: b"\x00\xC2", 0xC202: b"\xFF"},
         read={0xDDF9: 2}),
]
# <<< factory Music1_ret

# >>> factory Music1_frequency_offset
CONTRACT["Music1_frequency_offset"] = {"compare": (), "preserve": ()}
CASES["Music1_frequency_offset"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF"}, "read": {0xDDEA: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"}, "read": {0xDDEA: 1}},
    {"c": 2, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDDEC: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF"},
         read={0xDDEB: 1}),
]
# <<< factory Music1_frequency_offset

# >>> factory Music1_volume
CONTRACT["Music1_volume"] = {"compare": (), "preserve": ()}
CASES["Music1_volume"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x7F\xFF"}, "read": {0xDDE7: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"}, "read": {0xDDE7: 1}},
    {"c": 2, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDDE9: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x11\xFF"},
         read={0xDDE8: 1}),
]
# <<< factory Music1_volume

# >>> factory Music1_wave
CONTRACT["Music1_wave"] = {"compare": (), "preserve": ()}
CASES["Music1_wave"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x05\xFF", 0xDD8A: b"\x00\x00"},
     "read": {0xDD8A: 2}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF", 0xDD8A: b"\xFF\xFF"},
     "read": {0xDD8A: 2}},
    dict(POISON, b=0, c=2, stack=[0xC100],
         wram={0xC100: b"\xFF\xFF", 0xDD8A: b"\x00\x00"}, read={0xDD8A: 2}),
]
# <<< factory Music1_wave

# >>> factory Music1_cutoff
CONTRACT["Music1_cutoff"] = {"compare": (), "preserve": ()}
CASES["Music1_cutoff"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF"}, "read": {0xDDBF: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"}, "read": {0xDDBF: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDDC2: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF"},
         read={0xDDC0: 1}),
]
# <<< factory Music1_cutoff

# >>> factory Music1_echo
CONTRACT["Music1_echo"] = {"compare": (), "preserve": ()}
CASES["Music1_echo"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF"}, "read": {0xDDC7: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"}, "read": {0xDDC7: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDDCA: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF"},
         read={0xDDC8: 1}),
]
# <<< factory Music1_echo

# >>> factory Music1_vibrato_type
CONTRACT["Music1_vibrato_type"] = {"compare": (), "preserve": ()}
CASES["Music1_vibrato_type"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF"},
     "read": {0xDDD3: 1, 0xDDD7: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"},
     "read": {0xDDD3: 1, 0xDDD7: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"},
     "read": {0xDDD6: 1, 0xDDDA: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF"},
         read={0xDDD4: 1, 0xDDD8: 1}),
]
# <<< factory Music1_vibrato_type

# >>> factory Music1_vibrato_delay
CONTRACT["Music1_vibrato_delay"] = {"compare": (), "preserve": ()}
CASES["Music1_vibrato_delay"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF"}, "read": {0xDDDF: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF"}, "read": {0xDDDF: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF"}, "read": {0xDDE2: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF"},
         read={0xDDE0: 1}),
]
# <<< factory Music1_vibrato_delay

# >>> factory Music1_pitch_offset
CONTRACT["Music1_pitch_offset"] = {"compare": (), "preserve": ()}
CASES["Music1_pitch_offset"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x40\xFF", 0xDDCB: b"\x00"},
     "read": {0xDDCB: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF", 0xDDCB: b"\xAA"},
     "read": {0xDDCB: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\xFF\xFF", 0xDDCE: b"\x00"},
     "read": {0xDDCE: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x7F\xFF", 0xDDCC: b"\x11"},
         read={0xDDCC: 1}),
]
# <<< factory Music1_pitch_offset

# >>> factory Music1_adjust_pitch_offset
CONTRACT["Music1_adjust_pitch_offset"] = {"compare": (), "preserve": ()}
CASES["Music1_adjust_pitch_offset"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x05\xFF", 0xDDCB: b"\x10"},
     "read": {0xDDCB: 1}},
    {"c": 0, "stack": [0xC100], "wram": {0xC100: b"\x02\xFF", 0xDDCB: b"\xFF"},
     "read": {0xDDCB: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xC100: b"\x00\xFF", 0xDDCE: b"\x7F"},
     "read": {0xDDCE: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xC100: b"\x11\xFF", 0xDDCC: b"\x22"},
         read={0xDDCC: 1}),
]
# <<< factory Music1_adjust_pitch_offset

# >>> factory Music1_end
CONTRACT["Music1_end"] = {"compare": (), "preserve": ()}
CASES["Music1_end"] = [
    {"c": 0, "stack": [0xC100], "wram": {0xDD8D: b"\x01"}, "read": {0xDD8D: 1}},
    {"c": 3, "stack": [0xC100], "wram": {0xDD90: b"\xFF"}, "read": {0xDD90: 1}},
    dict(POISON, b=0, c=1, stack=[0xC100], wram={0xDD8E: b"\x7F"},
         read={0xDD8E: 1}),
]
# <<< factory Music1_end

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Music1_CopyData": {
        "source_symbol": "Music1_CopyData",
        "before": "\tdo { gb_write8((*de)++, gb_read8((*hl)++)); } while (--c);",
        "after": "\tdo { gb_write8((*de)++, gb_read8((*hl)++)); } while (c--);",
        "case_ids": ["Music1_CopyData-0", "Music1_CopyData-1", "Music1_CopyData-2"],
    },
}
# >>> factory-mutation _PauseSong
MUTATIONS["_PauseSong"] = {"source_symbol": "_PauseSong", "before": "Music1_PauseSong();", "after": "Music1_PauseSong(), gb_write8(0xC100u, 0x01u);", "case_ids": ["_PauseSong-1"]}
# <<< factory-mutation _PauseSong
# >>> factory-mutation _ResumeSong
MUTATIONS["_ResumeSong"] = {"source_symbol": "_ResumeSong", "before": "Music1_ResumeSong();", "after": "Music1_ResumeSong(), gb_write8(0xC101u, 0x01u);", "case_ids": ["_ResumeSong-1"]}
# <<< factory-mutation _ResumeSong
# >>> factory-mutation Music1_f400c
MUTATIONS["Music1_f400c"] = {"source_symbol": "Music1_f400c", "before": "Music1_f404e(a);", "after": "Music1_f404e(a), gb_write8(0xC103u, 0x01u);", "case_ids": ["Music1_f400c-1"]}
# <<< factory-mutation Music1_f400c
# >>> factory-mutation Music1_f4018
MUTATIONS["Music1_f4018"] = {"source_symbol": "Music1_f4018", "before": "\tMusic1_f406f(a);", "after": "\tMusic1_f406f((uint8_t)(a ^ 1u));", "case_ids": ["Music1_f4018-0", "Music1_f4018-1", "Music1_f4018-2", "Music1_f4018-3"]}
# <<< factory-mutation Music1_f4018
# >>> factory-mutation Music1_duty
MUTATIONS["Music1_duty"] = {"source_symbol": "Music1_duty", "before": "\tuint8_t value = (uint8_t)(gb_read8(caller_stream) & 0xC0u);", "after": "\tuint8_t value = (uint8_t)(gb_read8(caller_stream) & 0x3Fu);", "case_ids": ["Music1_duty-0", "Music1_duty-2"]}
# <<< factory-mutation Music1_duty
# >>> factory-mutation Music1_speed
MUTATIONS["Music1_speed"] = {"source_symbol": "Music1_speed", "before": "\tgb_write8((uint16_t)(wMusicSpeed_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicSpeed_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_speed-0", "Music1_speed-2"]}
# <<< factory-mutation Music1_speed
# >>> factory-mutation Music1_inc_octave
MUTATIONS["Music1_inc_octave"] = {"source_symbol": "Music1_inc_octave", "before": "\tgb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));", "after": "\tgb_write8(addr, (uint8_t)(gb_read8(addr) + 2u));", "case_ids": ["Music1_inc_octave-0", "Music1_inc_octave-2"]}
# <<< factory-mutation Music1_inc_octave
# >>> factory-mutation Music1_dec_octave
MUTATIONS["Music1_dec_octave"] = {"source_symbol": "Music1_dec_octave", "before": "\tgb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));", "after": "\tgb_write8(addr, (uint8_t)(gb_read8(addr) - 2u));", "case_ids": ["Music1_dec_octave-0", "Music1_dec_octave-2"]}
# <<< factory-mutation Music1_dec_octave
# >>> factory-mutation Music1_tie
MUTATIONS["Music1_tie"] = {"source_symbol": "Music1_tie", "before": "\tgb_write8((uint16_t)(wMusicTie_ADDR + ch), 0x80u);", "after": "\tgb_write8((uint16_t)(wMusicTie_ADDR + ch), 0x40u);", "case_ids": ["Music1_tie-0", "Music1_tie-1"]}
# <<< factory-mutation Music1_tie
# >>> factory-mutation Music1_stereo_panning
MUTATIONS["Music1_stereo_panning"] = {"source_symbol": "Music1_stereo_panning", "before": "\tuint8_t mask = 0xEEu;", "after": "\tuint8_t mask = 0xFFu;", "case_ids": ["Music1_stereo_panning-1", "Music1_stereo_panning-4"]}
# <<< factory-mutation Music1_stereo_panning
# >>> factory-mutation Music1_MainLoop
MUTATIONS["Music1_MainLoop"] = {"source_symbol": "Music1_MainLoop", "before": "\tuint16_t target = (uint16_t)(caller_stream - 1u);", "after": "\tuint16_t target = (uint16_t)(caller_stream - 2u);", "case_ids": ["Music1_MainLoop-0", "Music1_MainLoop-1"]}
# <<< factory-mutation Music1_MainLoop
# >>> factory-mutation Music1_Loop
MUTATIONS["Music1_Loop"] = {"source_symbol": "Music1_Loop", "before": "\tgb_write8((uint16_t)(sp + 2u), count);", "after": "\tgb_write8((uint16_t)(sp + 2u), (uint8_t)(count + 1u));", "case_ids": ["Music1_Loop-0", "Music1_Loop-1"]}
# <<< factory-mutation Music1_Loop
# >>> factory-mutation Music1_call
MUTATIONS["Music1_call"] = {"source_symbol": "Music1_call", "before": "\tMusic1_SetChannelStackPointer(ch, (uint16_t)(sp + 2u));", "after": "\tMusic1_SetChannelStackPointer(ch, (uint16_t)(sp + 3u));", "case_ids": ["Music1_call-0", "Music1_call-1"]}
# <<< factory-mutation Music1_call
# >>> factory-mutation Music1_ret
MUTATIONS["Music1_ret"] = {"source_symbol": "Music1_ret", "before": "\tMusic1_SetChannelStackPointer(ch, (uint16_t)(sp - 2u));", "after": "\tMusic1_SetChannelStackPointer(ch, (uint16_t)(sp - 1u));", "case_ids": ["Music1_ret-0", "Music1_ret-1"]}
# <<< factory-mutation Music1_ret
# >>> factory-mutation Music1_frequency_offset
MUTATIONS["Music1_frequency_offset"] = {"source_symbol": "Music1_frequency_offset", "before": "\tgb_write8((uint16_t)(wMusicFrequencyOffset_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicFrequencyOffset_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_frequency_offset-0", "Music1_frequency_offset-2"]}
# <<< factory-mutation Music1_frequency_offset
# >>> factory-mutation Music1_volume
MUTATIONS["Music1_volume"] = {"source_symbol": "Music1_volume", "before": "\tgb_write8((uint16_t)(wMusicVolume_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicVolume_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_volume-0", "Music1_volume-2"]}
# <<< factory-mutation Music1_volume
# >>> factory-mutation Music1_wave
MUTATIONS["Music1_wave"] = {"source_symbol": "Music1_wave", "before": "\tgb_write8(wMusicWaveChange_ADDR, 0x01u);", "after": "\tgb_write8(wMusicWaveChange_ADDR, 0x00u);", "case_ids": ["Music1_wave-0", "Music1_wave-1"]}
# <<< factory-mutation Music1_wave
# >>> factory-mutation Music1_cutoff
MUTATIONS["Music1_cutoff"] = {"source_symbol": "Music1_cutoff", "before": "\tgb_write8((uint16_t)(wMusicCutoff_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicCutoff_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_cutoff-0", "Music1_cutoff-2"]}
# <<< factory-mutation Music1_cutoff
# >>> factory-mutation Music1_echo
MUTATIONS["Music1_echo"] = {"source_symbol": "Music1_echo", "before": "\tgb_write8((uint16_t)(wMusicEcho_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicEcho_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_echo-0", "Music1_echo-2"]}
# <<< factory-mutation Music1_echo
# >>> factory-mutation Music1_vibrato_type
MUTATIONS["Music1_vibrato_type"] = {"source_symbol": "Music1_vibrato_type", "before": "\tgb_write8((uint16_t)(wMusicVibratoType2_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicVibratoType2_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_vibrato_type-0", "Music1_vibrato_type-2"]}
# <<< factory-mutation Music1_vibrato_type
# >>> factory-mutation Music1_vibrato_delay
MUTATIONS["Music1_vibrato_delay"] = {"source_symbol": "Music1_vibrato_delay", "before": "\tgb_write8((uint16_t)(wMusicVibratoDelay_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicVibratoDelay_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_vibrato_delay-0", "Music1_vibrato_delay-2"]}
# <<< factory-mutation Music1_vibrato_delay
# >>> factory-mutation Music1_pitch_offset
MUTATIONS["Music1_pitch_offset"] = {"source_symbol": "Music1_pitch_offset", "before": "\tgb_write8((uint16_t)(wMusicPitchOffset_ADDR + ch), value);", "after": "\tgb_write8((uint16_t)(wMusicPitchOffset_ADDR + ch), (uint8_t)(value ^ 1u));", "case_ids": ["Music1_pitch_offset-0", "Music1_pitch_offset-2"]}
# <<< factory-mutation Music1_pitch_offset
# >>> factory-mutation Music1_adjust_pitch_offset
MUTATIONS["Music1_adjust_pitch_offset"] = {"source_symbol": "Music1_adjust_pitch_offset", "before": "\tgb_write8(addr, (uint8_t)(value + gb_read8(addr)));", "after": "\tgb_write8(addr, value);", "case_ids": ["Music1_adjust_pitch_offset-0", "Music1_adjust_pitch_offset-1"]}
# <<< factory-mutation Music1_adjust_pitch_offset
# >>> factory-mutation Music1_end
MUTATIONS["Music1_end"] = {"source_symbol": "Music1_end", "before": "\tgb_write8((uint16_t)(wMusicIsPlaying_ADDR + ch), 0x00u);", "after": "\tgb_write8((uint16_t)(wMusicIsPlaying_ADDR + ch), 0x01u);", "case_ids": ["Music1_end-0", "Music1_end-1"]}
# <<< factory-mutation Music1_end
# >>> factory-mutation _AssertSFXFinished
MUTATIONS["_AssertSFXFinished"] = {"source_symbol": "_AssertSFXFinished", "before": "return Music1_AssertSFXFinished();", "after": "return (uint8_t)(Music1_AssertSFXFinished() ^ 1u);", "case_ids": ["_AssertSFXFinished-0", "_AssertSFXFinished-1", "_AssertSFXFinished-2"]};
# <<< factory-mutation _AssertSFXFinished
# >>> factory-mutation _AssertSongFinished
MUTATIONS["_AssertSongFinished"] = {"source_symbol": "_AssertSongFinished", "before": "return Music1_AssertSongFinished();", "after": "return (uint8_t)(Music1_AssertSongFinished() ^ 1u);", "case_ids": ["_AssertSongFinished-0", "_AssertSongFinished-1", "_AssertSongFinished-2", "_AssertSongFinished-3"]}
# <<< factory-mutation _AssertSongFinished
# >>> factory-mutation _PlaySFX
MUTATIONS["_PlaySFX"] = {"source_symbol": "_PlaySFX", "before": "Music1_PlaySFX(a);", "after": "Music1_PlaySFX((uint8_t)(a ^ 1u));", "case_ids": ["_PlaySFX-0", "_PlaySFX-1", "_PlaySFX-2", "_PlaySFX-3", "_PlaySFX-4"]};
# <<< factory-mutation _PlaySFX
# >>> factory-mutation _PlaySong
MUTATIONS["_PlaySong"] = {"source_symbol": "_PlaySong", "before": "Music1_PlaySong(a);", "after": "Music1_PlaySong((uint8_t)(a ^ 1u));", "case_ids": ["_PlaySong-0", "_PlaySong-1", "_PlaySong-2", "_PlaySong-3", "_PlaySong-4"]};
# <<< factory-mutation _PlaySong
# >>> factory-mutation _SetupSound
MUTATIONS["_SetupSound"] = {"source_symbol": "_SetupSound", "before": "Music1_Init();", "after": "Music1_EmptyFunc();", "case_ids": ["_SetupSound-0", "_SetupSound-1"]};
# <<< factory-mutation _SetupSound
# >>> factory-mutation SoundTimerHandler
MUTATIONS["SoundTimerHandler"] = {"source_symbol": "SoundTimerHandler", "before": "\tMusic1_Update();", "after": "\tMusic1_EmptyFunc();", "case_ids": ["SoundTimerHandler-0", "SoundTimerHandler-1"]}
# <<< factory-mutation SoundTimerHandler
# >>> factory-mutation Music1_f4015
MUTATIONS["Music1_f4015"] = {"source_symbol": "Music1_f4015", "before": "\tMusic1_f4066();", "after": "\tMusic1_EmptyFunc();", "case_ids": ["Music1_f4015-0", "Music1_f4015-1", "Music1_f4015-2"]}
# <<< factory-mutation Music1_f4015
