"""Oracle-diff cases for music1.asm (bank $3d) — audio music engine."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

CONTRACT["Music1_EmptyFunc"] = ()
CASES["Music1_EmptyFunc"] = [{}, POISON]

CONTRACT["Music1_f404e"] = ()
CASES["Music1_f404e"] = [
    {"a": 0x42, "read": {0xDDF0: 1}},
    dict(POISON, read={0xDDF0: 1}),
]

CONTRACT["Music1_f4066"] = ()
CASES["Music1_f4066"] = [
    {"wram": {0xDDF2: b"\x00"}},
    {"wram": {0xDDF2: b"\x01"}},
    {"wram": {0xDDF2: b"\xFF"}},
    dict(POISON, wram={0xDDF2: b"\x05"}),
]

CONTRACT["Music1_f406f"] = ("b", "c")
CASES["Music1_f406f"] = [
    {"a": 0x00, "read": {0xDDF1: 1}},
    {"a": 0x07, "read": {0xDDF1: 1}},
    {"a": 0x77, "read": {0xDDF1: 1}},
    {"a": 0xFF, "read": {0xDDF1: 1}},
    dict(POISON, read={0xDDF1: 1}),
]

CONTRACT["Music1_PlaySong"] = ("hl",)
CASES["Music1_PlaySong"] = [
    {"a": 0x00, "read": {0xDD80: 1}},
    {"a": 0x1E, "read": {0xDD80: 1}},
    {"a": 0x1F, "read": {0xDD80: 1}},
    {"a": 0xFF, "read": {0xDD80: 1}},
    dict(POISON, read={0xDD80: 1}),
]

CONTRACT["Music1_PlaySFX"] = ("b", "c", "hl")
CASES["Music1_PlaySFX"] = [
    {"a": 0x00, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "read": {0xDD83: 1, 0xDD82: 1}},
    {"a": 0x01, "wram": {0xDD83: b"\x0A", 0xDD82: b"\x05"}},
    {"a": 0x01, "wram": {0xDD83: b"\x05", 0xDD82: b"\x80"}},
    dict(POISON, read={0xDD83: 1, 0xDD82: 1}),
]

CONTRACT["Music1_AssertSongFinished"] = ("a",)
CASES["Music1_AssertSongFinished"] = [
    {"wram": {0xDD80: b"\x80"}},
    {"wram": {0xDD80: b"\x00"}},
    {"wram": {0xDD80: b"\x7F"}},
    dict(POISON, wram={0xDD80: b"\xFF"}),
]

CONTRACT["Music1_AssertSFXFinished"] = ("a",)
CASES["Music1_AssertSFXFinished"] = [
    {"wram": {0xDD82: b"\x80"}},
    {"wram": {0xDD82: b"\x00"}},
    dict(POISON, wram={0xDD82: b"\x55"}),
]

CONTRACT["Music1_CheckForEndOfSong"] = ()
CASES["Music1_CheckForEndOfSong"] = [
    {"wram": {0xDD8D: b"\x01\x01\x01\x01"}},
    {"wram": {0xDD8D: b"\x00\x00\x00\x00", 0xDD80: b"\x05"}},
    {"wram": {0xDD8D: b"\x00\x00\x00\x01", 0xDD80: b"\x05"}},
    dict(POISON, wram={0xDD8D: b"\x00\x00\x00\x00", 0xDD80: b"\x05"}),
]

CONTRACT["Music1_f4980"] = ()
CASES["Music1_f4980"] = [
    {"wram": {0xDD8C: b"\x00"}},
    {"wram": {0xDD8C: b"\x0F"}},
    dict(POISON, wram={0xDD8C: b"\x00"}),
]

CONTRACT["Music1_CopyData"] = ("hl", "d", "e")
CASES["Music1_CopyData"] = [
    {"a": 0, "hl": 0xC100, "d": 0xC2, "e": 0x00, "read": {0xC200: 0}},
    {"a": 5, "hl": 0xC100, "d": 0xC2, "e": 0x00,
     "wram": {0xC100: b"\x01\x02\x03\x04\x05"}, "read": {0xC200: 5}},
    dict(POISON, a=3, hl=0xC100, d=0xC2, e=0x00,
         wram={0xC100: b"\xAA\xBB\xCC"}, read={0xC200: 3}),
]

# Init: WRAM-only readback. APU regs are touched but the oracle and C probe
# have different power-on APU states; we verify the WRAM side comprehensively.
CONTRACT["Music1_Init"] = ()
CASES["Music1_Init"] = [
    {"read": {0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4, 0xDDB3: 4,
              0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1, 0xDDF3: 8, 0xDDF0: 1,
              0xDDF2: 1, 0xDD8C: 1, 0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}},
    dict(POISON, read={0xDD80: 1, 0xDD82: 1, 0xDD8D: 4, 0xDD91: 4,
                       0xDDB3: 4, 0xDDCB: 4, 0xDDBF: 4, 0xDDF1: 1,
                       0xDDF3: 8, 0xDDF0: 1, 0xDDF2: 1, 0xDD8C: 1,
                       0xDD84: 1, 0xDD81: 1, 0xDDEF: 1}),
]

CONTRACT["Music1_StopAllChannels"] = ()
CASES["Music1_StopAllChannels"] = [
    {"wram": {0xDD8C: b"\x00"}, "read": {0xDD8D: 4}},
    {"wram": {0xDD8C: b"\x0F"}, "read": {0xDD8D: 4}},
    {"wram": {0xDD8C: b"\x05"}, "read": {0xDD8D: 4}},
    dict(POISON, wram={0xDD8C: b"\x00"}, read={0xDD8D: 4}),
]

CONTRACT["Music1_BeginSong"] = ()
CASES["Music1_BeginSong"] = [
    {"a": 0x00, "read": {0xDD81: 1, 0xDD95: 8, 0xDD9D: 8, 0xDDBB: 4,
                          0xDD8D: 4, 0xDD91: 4, 0xDDEA: 4, 0xDDBF: 4,
                          0xDDDF: 4, 0xDDCB: 4, 0xDDF3: 8, 0xDDC7: 4,
                          0xDDF2: 1}},
    {"a": 0x01, "read": {0xDD81: 1, 0xDD95: 8, 0xDD8D: 4, 0xDDF2: 1}},
    dict(POISON, a=0x01, read={0xDD81: 1, 0xDD95: 8, 0xDD8D: 4, 0xDDF2: 1}),
]
