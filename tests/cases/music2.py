"""Oracle-diff cases for music2.asm (bank $3e) -- audio music engine."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# -- existing 14 routines -------------------------------------------------

CONTRACT["Music2_EmptyFunc"] = {"compare": (), "preserve": ()}
CASES["Music2_EmptyFunc"] = [{}, POISON]

CONTRACT["Music2_f404e"] = {"compare": (), "preserve": ()}
CASES["Music2_f404e"] = [
    {"a": 0x42, "read": {0xDDF0: 1}},
    dict(POISON, read={0xDDF0: 1}),
]

CONTRACT["Music2_f4066"] = {"compare": (), "preserve": ()}
CASES["Music2_f4066"] = [
    {"wram": {0xDDF2: b"\x00"}},
    {"wram": {0xDDF2: b"\x01"}},
    {"wram": {0xDDF2: b"\xFF"}},
    dict(POISON, wram={0xDDF2: b"\x05"}),
]

CONTRACT["Music2_f406f"] = {"compare": ("b", "c"), "preserve": ("b", "c")}
CASES["Music2_f406f"] = [
    {"a": 0x00, "read": {0xDDF1: 1}},
    {"a": 0x07, "read": {0xDDF1: 1}},
    {"a": 0x77, "read": {0xDDF1: 1}},
    {"a": 0xFF, "read": {0xDDF1: 1}},
    dict(POISON, read={0xDDF1: 1}),
]

CONTRACT["Music2_PlaySong"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["Music2_PlaySong"] = [
    {"a": 0x00, "read": {0xDD80: 1}},
    {"a": 0x1E, "read": {0xDD80: 1}},
    {"a": 0x1F, "read": {0xDD80: 1}},
    {"a": 0xFF, "read": {0xDD80: 1}},
    dict(POISON, read={0xDD80: 1}),
]

CONTRACT["Music2_PlaySFX"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Music2_PlaySFX"] = [
    {"a": 0x00, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "wram": {0xDD83: b"\x0A", 0xDD82: b"\x05"}},
    {"a": 0x01, "wram": {0xDD83: b"\x05", 0xDD82: b"\x80"}},
    dict(POISON, read={0xDD83: 1, 0xDD82: 1}),
]

CONTRACT["Music2_AssertSongFinished"] = {"compare": ("a",), "preserve": ()}
CASES["Music2_AssertSongFinished"] = [
    {"wram": {0xDD80: b"\x80"}},
    {"wram": {0xDD80: b"\x00"}},
    {"wram": {0xDD80: b"\x7F"}},
    dict(POISON, wram={0xDD80: b"\xFF"}),
]

CONTRACT["Music2_AssertSFXFinished"] = {"compare": ("a",), "preserve": ()}
CASES["Music2_AssertSFXFinished"] = [
    {"wram": {0xDD82: b"\x80"}},
    {"wram": {0xDD82: b"\x00"}},
    dict(POISON, wram={0xDD82: b"\x55"}),
]

CONTRACT["Music2_CheckForEndOfSong"] = {"compare": (), "preserve": ()}
CASES["Music2_CheckForEndOfSong"] = [
    {"wram": {0xDD8D: b"\x01\x01\x01\x01"}},
    {"wram": {0xDD8D: b"\x00\x00\x00\x00", 0xDD80: b"\x05"}},
    {"wram": {0xDD8D: b"\x00\x00\x00\x01", 0xDD80: b"\x05"}},
    dict(POISON, wram={0xDD8D: b"\x00\x00\x00\x00", 0xDD80: b"\x05"}),
]

CONTRACT["Music2_f4980"] = {"compare": (), "preserve": ()}
CASES["Music2_f4980"] = [
    {"wram": {0xDD8C: b"\x00"}},
    {"wram": {0xDD8C: b"\x0F"}},
    dict(POISON, wram={0xDD8C: b"\x00"}),
]

CONTRACT["Music2_CopyData"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["Music2_CopyData"] = [
    {"a": 0, "hl": 0xC100, "d": 0xC2, "e": 0x00, "read": {0xC200: 0}},
    {"a": 5, "hl": 0xC100, "d": 0xC2, "e": 0x00,
     "wram": {0xC100: b"\x01\x02\x03\x04\x05"}, "read": {0xC200: 5}},
    dict(POISON, a=3, hl=0xC100, d=0xC2, e=0x00,
         wram={0xC100: b"\xAA\xBB\xCC"}, read={0xC200: 3}),
]

CONTRACT["Music2_Init"] = {"compare": (), "preserve": ()}
CASES["Music2_Init"] = [
    {"read": {0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4, 0xDDB3: 4,
              0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1, 0xDDF3: 8, 0xDDF0: 1,
              0xDDF2: 1, 0xDD8C: 1, 0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}},
    dict(POISON, read={0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4,
                       0xDDB3: 4, 0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1,
                       0xDDF3: 8, 0xDDF0: 1, 0xDDF2: 1, 0xDD8C: 1,
                       0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}),
]

CONTRACT["Music2_StopAllChannels"] = {"compare": (), "preserve": ()}
CASES["Music2_StopAllChannels"] = [
    {"wram": {0xDD8C: b"\x00"}, "read": {0xDD8D: 4}},
    {"wram": {0xDD8C: b"\x0F"}, "read": {0xDD8D: 4}},
    {"wram": {0xDD8C: b"\x05"}, "read": {0xDD8D: 4}},
    dict(POISON, wram={0xDD8C: b"\x00"}, read={0xDD8D: 4}),
]

CONTRACT["Music2_BeginSong"] = {"compare": (), "preserve": ()}
CASES["Music2_BeginSong"] = [
    {"a": 0x00, "read": {0xDD81: 1, 0xDD95: 8, 0xDD9D: 8, 0xDDBB: 4,
                          0xDD8D: 4, 0xDD91: 4, 0xDDEA: 4, 0xDDBF: 4,
                          0xDDDF: 4, 0xDDCB: 4, 0xDDF3: 8, 0xDDC7: 4,
                          0xDDF2: 1}},
    {"a": 0x01, "read": {0xDD81: 1, 0xDD95: 8, 0xDD8D: 4, 0xDDF2: 1}},
    dict(POISON, a=0x01, read={0xDD81: 1, 0xDD95: 8, 0xDD8D: 4, 0xDDF2: 1}),
]

# -- Stack helpers --------------------------------------------------------

CONTRACT["Music2_GetChannelStackPointer"] = {"compare": ("hl", "c"), "preserve": ("c",)}
CASES["Music2_GetChannelStackPointer"] = [
    {"c": 0, "wram": {0xDDF3: b"\x00\xC1"}, "read": {0xDDF3: 8}},
    {"c": 1, "wram": {0xDDF3: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4"}, "read": {0xDDF3: 8}},
    {"c": 3, "wram": {0xDDF3: b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4"},
     "read": {0xDDF3: 8}},
    dict(POISON, b=0, c=2, wram={0xDDF3: b"\x34\x12\x78\x56\xBC\x9A\xF0\xDE"},
         read={0xDDF3: 8}),
]

CONTRACT["Music2_SetChannelStackPointer"] = {"compare": ("c",), "preserve": ("c",)}
CASES["Music2_SetChannelStackPointer"] = [
    {"c": 0, "hl": 0xC100, "read": {0xDDF3: 2}},
    {"c": 2, "hl": 0xC200, "read": {0xDDF3: 8}},
    {"c": 3, "hl": 0xC300,
     "wram": {0xDDF3: b"\x00\x00\x00\x00\x00\x00\x00\x00"},
     "read": {0xDDF3: 8}},
    dict(POISON, b=0, c=1, hl=0xC1FF, read={0xDDF3: 8}),
]

# -- Channel output routines ----------------------------------------------

CONTRACT["Music2_f4714"] = {"compare": (), "preserve": ()}
CASES["Music2_f4714"] = [
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

CONTRACT["Music2_f475a"] = {"compare": (), "preserve": ()}
CASES["Music2_f475a"] = [
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

CONTRACT["Music2_f479c"] = {"compare": (), "preserve": ()}
CASES["Music2_f479c"] = [
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

CONTRACT["Music2_f480a"] = {"compare": (), "preserve": ()}
CASES["Music2_f480a"] = [
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

CONTRACT["Music2_f4839"] = {"compare": (), "preserve": ()}
CASES["Music2_f4839"] = [
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

CONTRACT["Music2_LoadWaveInstrument"] = {"compare": (), "preserve": ()}
CASES["Music2_LoadWaveInstrument"] = [
    {"wram": {0xDD8A: b"\x00", 0xDD8B: b"\x01"},
     "read": {0xDD8B: 1}},
    {"wram": {0xDD8A: b"\x01", 0xDD8B: b"\x01"},
     "read": {0xDD8B: 1}},
    dict(POISON, wram={0xDD8A: b"\x02", 0xDD8B: b"\x01"},
         read={0xDD8B: 1}),
]

# -- Vibrato --------------------------------------------------------------

CONTRACT["Music2_UpdateVibrato"] = {"compare": ("d", "e", "c"), "preserve": ("c",)}
CASES["Music2_UpdateVibrato"] = [
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

CONTRACT["Music2_f490b"] = {"compare": (), "preserve": ()}
CASES["Music2_f490b"] = [
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

CONTRACT["Music2_f4967"] = {"compare": ("d", "e", "c"), "preserve": ("c",)}
CASES["Music2_f4967"] = [
    {"c": 0, "d": 0x00, "e": 0x2C, "wram": {0xDDEA: b"\x00"}},
    {"c": 0, "d": 0x00, "e": 0x2C, "wram": {0xDDEA: b"\x10"}},
    {"c": 0, "d": 0x03, "e": 0x00, "wram": {0xDDEA: b"\x80"}},
    {"c": 1, "d": 0x00, "e": 0x2C, "wram": {0xDDEB: b"\x20"}},
    dict(POISON, b=0, c=2, d=0x03, e=0x00, wram={0xDDEC: b"\xFF"}),
]

CONTRACT["Music2_f485a"] = {"compare": (), "preserve": ()}
CASES["Music2_f485a"] = [
    {"a": 0, "wram": {0xDDDF: b"\x00", 0xDD8C: b"\x00",
                       0xDDA5: b"\x2C\x00"}},
    {"a": 1, "wram": {0xDDE0: b"\x00", 0xDD8C: b"\x00",
                       0xDDA7: b"\x2C\x00"}},
    dict(POISON, a=0, wram={0xDDDF: b"\x01", 0xDD8C: b"\x00",
                             0xDDA5: b"\x9C\x00"}),
]

# -- Panning / output select ----------------------------------------------

CONTRACT["Music2_f4866"] = {"compare": (), "preserve": ()}
CASES["Music2_f4866"] = [
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

CONTRACT["Music2_UpdateChannel1"] = {"compare": (), "preserve": ()}
CASES["Music2_UpdateChannel1"] = [
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

CONTRACT["Music2_UpdateChannel2"] = {"compare": (), "preserve": ()}
CASES["Music2_UpdateChannel2"] = [
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

CONTRACT["Music2_UpdateChannel3"] = {"compare": (), "preserve": ()}
CASES["Music2_UpdateChannel3"] = [
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

CONTRACT["Music2_UpdateChannel4"] = {"compare": (), "preserve": ()}
CASES["Music2_UpdateChannel4"] = [
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

CONTRACT["Music2_PauseSong"] = {"compare": (), "preserve": ()}
CASES["Music2_PauseSong"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x00",
              0xDD8D: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x0F",
                       0xDD8D: b"\x01\x01\x01\x01"}),
]

CONTRACT["Music2_ResumeSong"] = {"compare": (), "preserve": ()}
CASES["Music2_ResumeSong"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x00",
              0xDE55: b"\x80", 0xDE56: b"\x3D",
              0xDD8D: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x0F",
                       0xDE55: b"\x81", 0xDE56: b"\x3E",
                       0xDD8D: b"\x01\x01\x01\x01"}),
]

CONTRACT["Music2_BackupSong"] = {"compare": (), "preserve": ()}
CASES["Music2_BackupSong"] = [
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

CONTRACT["Music2_LoadBackup"] = {"compare": (), "preserve": ()}
CASES["Music2_LoadBackup"] = [
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

CONTRACT["Music2_CheckForNewSound"] = {"compare": (), "preserve": ()}
CASES["Music2_CheckForNewSound"] = [
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

CONTRACT["Music2_Update"] = {"compare": (), "preserve": ()}
CASES["Music2_Update"] = [
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
# >>> factory Music2_f400c_2
CONTRACT["Music2_f400c_2"] = {"compare": (), "preserve": ()};
CASES["Music2_f400c_2"] = [
    {"a": 0x42, "read": {0xDDF0: 1}},
    dict(POISON, read={0xDDF0: 1}, wram={0xC103: b"\x00"}),
]
# <<< factory Music2_f400c_2

# >>> factory Music2_f4018_2
CONTRACT["Music2_f4018_2"] = {"compare": (), "preserve": ()};
CASES["Music2_f4018_2"] = [
    {"a": 0x42, "read": {0xDDF1: 1}},
    dict(POISON, read={0xDDF1: 1}),
]
# <<< factory Music2_f4018_2

# >>> factory _AssertSFXFinished_2
CONTRACT["_AssertSFXFinished_2"] = {"compare": ("a",), "preserve": ()};
CASES["_AssertSFXFinished_2"] = [
    {"wram": {0xDD82: b"\x80", 0xDD80: b"\x00"}},
    {"wram": {0xDD82: b"\x00", 0xDD80: b"\x80"}},
    dict(POISON, wram={0xDD82: b"\x55", 0xDD80: b"\xFF"}),
]
# <<< factory _AssertSFXFinished_2

# >>> factory _AssertSongFinished_2
CONTRACT["_AssertSongFinished_2"] = {"compare": ("a",), "preserve": ()};
CASES["_AssertSongFinished_2"] = [
    {"wram": {0xDD80: b"\x80"}},
    {"wram": {0xDD80: b"\x00"}},
    dict(POISON, wram={0xDD80: b"\x55"}),
]
# <<< factory _AssertSongFinished_2

# >>> factory _PauseSong_2
CONTRACT["_PauseSong_2"] = {"compare": (), "preserve": ()}
CASES["_PauseSong_2"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x00",
              0xDD8D: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x0F",
                       0xDD8D: b"\x01\x01\x01\x01"}),
]
# <<< factory _PauseSong_2

# >>> factory _PlaySFX_2
CONTRACT["_PlaySFX_2"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")};
CASES["_PlaySFX_2"] = [
    {"a": 0x00, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "wram": {0xDD83: b"\x0A", 0xDD82: b"\x05"}},
    {"a": 0x01, "wram": {0xDD83: b"\x05", 0xDD82: b"\x80"}},
    dict(POISON, read={0xDD83: 1, 0xDD82: 1}),
]
# <<< factory _PlaySFX_2

# >>> factory _PlaySong_2
CONTRACT["_PlaySong_2"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")};
CASES["_PlaySong_2"] = [
    {"a": 0x00, "wram": {0xDD80: b"\x55"}, "expect_wram": {0xDD80: b"\x00"}},
    {"a": 0x01, "wram": {0xDD80: b"\x55"}, "expect_wram": {0xDD80: b"\x01"}},
    {"a": 0x1E, "wram": {0xDD80: b"\x55"}, "expect_wram": {0xDD80: b"\x1E"}},
    {"a": 0x1F, "wram": {0xDD80: b"\x55"}, "expect_wram": {0xDD80: b"\x55"}},
    dict(POISON, wram={0xDD80: b"\x55"}, expect_wram={0xDD80: b"\x55"}),
]
# <<< factory _PlaySong_2

# >>> factory _ResumeSong_2
CONTRACT["_ResumeSong_2"] = {"compare": (), "preserve": ()}
CASES["_ResumeSong_2"] = [
    {"wram": {0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x00",
              0xDD8D: b"\x00\x00\x00\x00"}},
    dict(POISON, wram={0xDD80: b"\x80", 0xDD81: b"\x3D", 0xDD8C: b"\x0F",
                       0xDD8D: b"\x01\x01\x01\x01"}),
]
# <<< factory _ResumeSong_2

# >>> factory Music2_f4015_2
CONTRACT["Music2_f4015_2"] = {"compare": (), "preserve": ()}
CASES["Music2_f4015_2"] = [
    {"wram": {0xDDF2: b"\x00"}, "read": {0xDDF2: 1}},
    {"wram": {0xDDF2: b"\x01"}, "read": {0xDDF2: 1}},
    {"wram": {0xDDF2: b"\xFF"}, "read": {0xDDF2: 1}},
    dict(POISON, wram={0xDDF2: b"\x05"}, read={0xDDF2: 1}),
]
# <<< factory Music2_f4015_2

# >>> factory _SetupSound_2
CONTRACT["_SetupSound_2"] = {"compare": (), "preserve": ()}
CASES["_SetupSound_2"] = [
    {"read": {0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4, 0xDDB3: 4,
              0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1, 0xDDF3: 8, 0xDDF0: 1,
              0xDDF2: 1, 0xDD8C: 1, 0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}},
    dict(POISON, read={0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4,
                       0xDDB3: 4, 0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1,
                       0xDDF3: 8, 0xDDF0: 1, 0xDDF2: 1, 0xDD8C: 1,
                       0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}),
]
# <<< factory _SetupSound_2

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Music2_CopyData": {
        "source_symbol": "Music2_CopyData",
        "before": "\tdo { gb_write8((*de)++, gb_read8((*hl)++)); } while (--c);",
        "after": "\tdo { gb_write8((*de)++, gb_read8((*hl)++)); } while (c--);",
        "case_ids": ["Music2_CopyData-0", "Music2_CopyData-1", "Music2_CopyData-2"],
    },
}
# >>> factory-mutation Music2_f400c_2
MUTATIONS["Music2_f400c_2"] = {"source_symbol": "Music2_f400c_2", "before": "Music2_f404e(a);", "after": "Music2_f404e(a), gb_write8(0xC103u, 0x01u);", "case_ids": ["Music2_f400c_2-1"]}
# <<< factory-mutation Music2_f400c_2
# >>> factory-mutation Music2_f4018_2
MUTATIONS["Music2_f4018_2"] = {"source_symbol": "Music2_f4018_2", "before": "Music2_f406f(a);", "after": "Music2_f406f((uint8_t)(a ^ 1u));", "case_ids": ["Music2_f4018_2-1"]}
# <<< factory-mutation Music2_f4018_2
# >>> factory-mutation _AssertSFXFinished_2
MUTATIONS["_AssertSFXFinished_2"] = {"source_symbol": "_AssertSFXFinished_2", "before": "return Music2_AssertSFXFinished();", "after": "return Music2_AssertSongFinished();", "case_ids": ["_AssertSFXFinished_2-0", "_AssertSFXFinished_2-1", "_AssertSFXFinished_2-2"]}
# <<< factory-mutation _AssertSFXFinished_2
# >>> factory-mutation _AssertSongFinished_2
MUTATIONS["_AssertSongFinished_2"] = {"source_symbol": "_AssertSongFinished_2", "before": "return Music2_AssertSongFinished();", "after": "return (uint8_t)(Music2_AssertSongFinished() ^ 0x01u);", "case_ids": ["_AssertSongFinished_2-0", "_AssertSongFinished_2-1", "_AssertSongFinished_2-2"]}
# <<< factory-mutation _AssertSongFinished_2
# >>> factory-mutation _PauseSong_2
MUTATIONS["_PauseSong_2"] = {"source_symbol": "_PauseSong_2", "before": "Music2_PauseSong();", "after": "Music2_ResumeSong();", "case_ids": ["_PauseSong_2-0", "_PauseSong_2-1"]}
# <<< factory-mutation _PauseSong_2
# >>> factory-mutation _PlaySFX_2
MUTATIONS["_PlaySFX_2"] = {"source_symbol": "_PlaySFX_2", "before": "Music2_PlaySFX(a);", "after": "Music2_PlaySFX((uint8_t)(a ^ 1u));", "case_ids": ["_PlaySFX_2-0", "_PlaySFX_2-1", "_PlaySFX_2-2", "_PlaySFX_2-3", "_PlaySFX_2-4"]};
# <<< factory-mutation _PlaySFX_2
# >>> factory-mutation _PlaySong_2
MUTATIONS["_PlaySong_2"] = {"source_symbol": "_PlaySong_2", "before": "Music2_PlaySong(a);", "after": "Music2_PlaySong((uint8_t)(a ^ 1u));", "case_ids": ["_PlaySong_2-0", "_PlaySong_2-1", "_PlaySong_2-2", "_PlaySong_2-3", "_PlaySong_2-4"]};
# <<< factory-mutation _PlaySong_2
# >>> factory-mutation _ResumeSong_2
MUTATIONS["_ResumeSong_2"] = {"source_symbol": "_ResumeSong_2", "before": "Music2_ResumeSong();", "after": "Music2_PauseSong();", "case_ids": ["_ResumeSong_2-0", "_ResumeSong_2-1"]}
# <<< factory-mutation _ResumeSong_2
# >>> factory-mutation Music2_f4015_2
MUTATIONS["Music2_f4015_2"] = {"source_symbol": "Music2_f4015_2", "before": "\tMusic2_f4066();", "after": "\tMusic2_EmptyFunc();", "case_ids": ["Music2_f4015_2-0", "Music2_f4015_2-1", "Music2_f4015_2-2", "Music2_f4015_2-3"]};
# <<< factory-mutation Music2_f4015_2
# >>> factory-mutation _SetupSound_2
MUTATIONS["_SetupSound_2"] = {"source_symbol": "_SetupSound_2", "before": "\tMusic2_Init();", "after": "\tMusic2_EmptyFunc();", "case_ids": ["_SetupSound_2-0", "_SetupSound_2-1"]}
# <<< factory-mutation _SetupSound_2
