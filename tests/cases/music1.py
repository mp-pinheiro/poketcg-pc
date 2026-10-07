"""Oracle-diff cases for music1.asm (bank $3d) -- audio music engine."""
from tests.cases._symbols import STACK_CANARY, sym

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# -- existing 14 routines -------------------------------------------------

CONTRACT["Music1_EmptyFunc"] = {"compare": (), "preserve": ()}
CASES["Music1_EmptyFunc"] = [{}, POISON]

CONTRACT["Music1_f404e"] = {"compare": (), "preserve": ()}
CASES["Music1_f404e"] = [
    {"a": 0x42, "read": {sym("wddf0"): 1}},
    dict(POISON, read={sym("wddf0"): 1}),
]

CONTRACT["Music1_f4066"] = {"compare": (), "preserve": ()}
CASES["Music1_f4066"] = [
    {"wram": {sym("wddf2"): b"\x00"}},
    {"wram": {sym("wddf2"): b"\x01"}},
    {"wram": {sym("wddf2"): b"\xFF"}},
    dict(POISON, wram={sym("wddf2"): b"\x05"}),
]

CONTRACT["Music1_f406f"] = {"compare": ("b", "c"), "preserve": ("b", "c")}
CASES["Music1_f406f"] = [
    {"a": 0x00, "read": {sym("wMusicPanning"): 1}},
    {"a": 0x07, "read": {sym("wMusicPanning"): 1}},
    {"a": 0x77, "read": {sym("wMusicPanning"): 1}},
    {"a": 0xFF, "read": {sym("wMusicPanning"): 1}},
    dict(POISON, read={sym("wMusicPanning"): 1}),
]

CONTRACT["Music1_PlaySong"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["Music1_PlaySong"] = [
    {"a": 0x00, "read": {sym("wCurSongID"): 1}},
    {"a": 0x1E, "read": {sym("wCurSongID"): 1}},
    {"a": 0x1F, "read": {sym("wCurSongID"): 1}},
    {"a": 0xFF, "read": {sym("wCurSongID"): 1}},
    dict(POISON, read={sym("wCurSongID"): 1}),
]

CONTRACT["Music1_PlaySFX"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["Music1_PlaySFX"] = [
    {"a": 0x00, "read": {sym("wSfxPriority"): 1, sym("wCurSfxID"): 1}},
    {"a": 0x01, "read": {sym("wSfxPriority"): 1, sym("wCurSfxID"): 1}},
    {"a": 0x01, "wram": {sym("wSfxPriority"): b"\x0A", sym("wCurSfxID"): b"\x05"}},
    {"a": 0x01, "wram": {sym("wSfxPriority"): b"\x05", sym("wCurSfxID"): b"\x80"}},
    dict(POISON, read={sym("wSfxPriority"): 1, sym("wCurSfxID"): 1}),
]

CONTRACT["Music1_AssertSongFinished"] = {"compare": ("a",), "preserve": ()}
CASES["Music1_AssertSongFinished"] = [
    {"wram": {sym("wCurSongID"): b"\x80"}},
    {"wram": {sym("wCurSongID"): b"\x00"}},
    {"wram": {sym("wCurSongID"): b"\x7F"}},
    dict(POISON, wram={sym("wCurSongID"): b"\xFF"}),
]

CONTRACT["Music1_AssertSFXFinished"] = {"compare": ("a",), "preserve": ()}
CASES["Music1_AssertSFXFinished"] = [
    {"wram": {sym("wCurSfxID"): b"\x80"}},
    {"wram": {sym("wCurSfxID"): b"\x00"}},
    dict(POISON, wram={sym("wCurSfxID"): b"\x55"}),
]

CONTRACT["Music1_CheckForEndOfSong"] = {"compare": (), "preserve": ()}
CASES["Music1_CheckForEndOfSong"] = [
    {"wram": {sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"}},
    {"wram": {sym("wMusicIsPlaying"): b"\x00\x00\x00\x00", sym("wCurSongID"): b"\x05"}},
    {"wram": {sym("wMusicIsPlaying"): b"\x00\x00\x00\x01", sym("wCurSongID"): b"\x05"}},
    dict(POISON, wram={sym("wMusicIsPlaying"): b"\x00\x00\x00\x00", sym("wCurSongID"): b"\x05"}),
]

CONTRACT["Music1_f4980"] = {"compare": (), "preserve": ()}
CASES["Music1_f4980"] = [
    {"wram": {sym("wdd8c"): b"\x00"}},
    {"wram": {sym("wdd8c"): b"\x0F"}},
    dict(POISON, wram={sym("wdd8c"): b"\x00"}),
]

CONTRACT["Music1_CopyData"] = {"compare": ("hl", "d", "e"), "preserve": ()}
CASES["Music1_CopyData"] = [
    {"a": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "d": 0xC2, "e": 0x00, "read": {sym("wPlayerCardLocations"): 0}},
    {"a": 5, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "d": 0xC2, "e": 0x00,
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x01\x02\x03\x04\x05"}, "read": {sym("wPlayerCardLocations"): 5}},
    dict(POISON, a=3, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, d=0xC2, e=0x00,
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xAA\xBB\xCC"}, read={sym("wPlayerCardLocations"): 3}),
]

CONTRACT["Music1_Init"] = {"compare": (), "preserve": ()}
CASES["Music1_Init"] = [
    {"read": {sym("wCurSongID"): 1, sym("wCurSfxID"): 1, sym("wMusicIsPlaying"): 4, sym("wMusicTie"): 4, sym("wddb3"): 4,
              sym("wMusicPitchOffset"): 4, sym("wMusicCutoff"): 4, sym("wMusicPanning"): 1, sym("wMusicChannelStackPointers"): 8, sym("wddf0"): 1,
              sym("wddf2"): 1, sym("wdd8c"): 1, sym("wMusicStereoPanning"): 1, sym("wCurSongBank"): 1, sym("wddef"): 1}},
    dict(POISON, read={sym("wCurSongID"): 1, sym("wCurSfxID"): 1, sym("wMusicIsPlaying"): 4, sym("wMusicTie"): 4,
                       sym("wddb3"): 4, sym("wMusicPitchOffset"): 4, sym("wMusicCutoff"): 4, sym("wMusicPanning"): 1,
                       sym("wMusicChannelStackPointers"): 8, sym("wddf0"): 1, sym("wddf2"): 1, sym("wdd8c"): 1,
                       sym("wMusicStereoPanning"): 1, sym("wCurSongBank"): 1, sym("wddef"): 1}),
]

CONTRACT["Music1_StopAllChannels"] = {"compare": (), "preserve": ()}
CASES["Music1_StopAllChannels"] = [
    {"wram": {sym("wdd8c"): b"\x00"}, "read": {sym("wMusicIsPlaying"): 4}},
    {"wram": {sym("wdd8c"): b"\x0F"}, "read": {sym("wMusicIsPlaying"): 4}},
    {"wram": {sym("wdd8c"): b"\x05"}, "read": {sym("wMusicIsPlaying"): 4}},
    dict(POISON, wram={sym("wdd8c"): b"\x00"}, read={sym("wMusicIsPlaying"): 4}),
]

CONTRACT["Music1_BeginSong"] = {"compare": (), "preserve": ()}
CASES["Music1_BeginSong"] = [
    {"a": 0x00, "read": {sym("wCurSongBank"): 1, sym("wMusicChannelPointers"): 8, sym("wMusicMainLoopStart"): 8, sym("wddbb"): 4,
                          sym("wMusicIsPlaying"): 4, sym("wMusicTie"): 4, sym("wMusicFrequencyOffset"): 4, sym("wMusicCutoff"): 4,
                          sym("wMusicVibratoDelay"): 4, sym("wMusicPitchOffset"): 4, sym("wMusicChannelStackPointers"): 8, sym("wMusicEcho"): 4,
                          sym("wddf2"): 1}},
    {"a": 0x01, "read": {sym("wCurSongBank"): 1, sym("wMusicChannelPointers"): 8, sym("wMusicIsPlaying"): 4, sym("wddf2"): 1}},
    dict(POISON, a=0x01, read={sym("wCurSongBank"): 1, sym("wMusicChannelPointers"): 8, sym("wMusicIsPlaying"): 4, sym("wddf2"): 1}),
]

# -- Stack helpers --------------------------------------------------------

CONTRACT["Music1_GetChannelStackPointer"] = {"compare": ("hl", "c"), "preserve": ("c",)}
CASES["Music1_GetChannelStackPointer"] = [
    {"c": 0, "wram": {sym("wMusicChannelStackPointers"): b"\x00\xC1"}, "read": {sym("wMusicChannelStackPointers"): 8}},
    {"c": 1, "wram": {sym("wMusicChannelStackPointers"): b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4"}, "read": {sym("wMusicChannelStackPointers"): 8}},
    {"c": 3, "wram": {sym("wMusicChannelStackPointers"): b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4"},
     "read": {sym("wMusicChannelStackPointers"): 8}},
    dict(POISON, b=0, c=2, wram={sym("wMusicChannelStackPointers"): b"\x34\x12\x78\x56\xBC\x9A\xF0\xDE"},
         read={sym("wMusicChannelStackPointers"): 8}),
]

CONTRACT["Music1_SetChannelStackPointer"] = {"compare": ("c",), "preserve": ("c",)}
CASES["Music1_SetChannelStackPointer"] = [
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11, "read": {sym("wMusicChannelStackPointers"): 2}},
    {"c": 2, "hl": sym("wPlayerCardLocations"), "read": {sym("wMusicChannelStackPointers"): 8}},
    {"c": 3, "hl": sym("wOpponentCardLocations"),
     "wram": {sym("wMusicChannelStackPointers"): b"\x00\x00\x00\x00\x00\x00\x00\x00"},
     "read": {sym("wMusicChannelStackPointers"): 8}},
    dict(POISON, b=0, c=1, hl=sym("wDecompressionSecondaryBufferStart") + 0x110, read={sym("wMusicChannelStackPointers"): 8}),
]

# -- Channel output routines ----------------------------------------------

CONTRACT["Music1_f4714"] = {"compare": (), "preserve": ()}
CASES["Music1_f4714"] = [
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb7"): b"\x00", sym("wMusicTie"): b"\x00"},
     "read": {sym("wMusicTie"): 1}},
    {"wram": {sym("wdd8c"): b"\x01", sym("wddb7"): b"\x00"},
     "read": {sym("wMusicTie"): 1, sym("wddb7"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb7"): b"\x10", sym("wMusicTie"): b"\x80",
              sym("wMusicVolume"): b"\x77", sym("wMusicDuty1"): b"\xC0", sym("wMusicCh1CurPitch"): b"\x2C", sym("wMusicCh1CurOctave"): b"\x80"},
     "read": {sym("wMusicTie"): 1, sym("wddb7"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb7"): b"\x10", sym("wMusicTie"): b"\x02",
              sym("wMusicVolume"): b"\x55", sym("wMusicDuty1"): b"\x40", sym("wMusicCh1CurPitch"): b"\x9C", sym("wMusicCh1CurOctave"): b"\x00"},
     "read": {sym("wMusicTie"): 1, sym("wddb7"): 1}},
    dict(POISON, wram={sym("wdd8c"): b"\x00", sym("wddb7"): b"\x10", sym("wMusicTie"): b"\x03",
                       sym("wMusicVolume"): b"\x33", sym("wMusicDuty1"): b"\x80", sym("wMusicCh1CurPitch"): b"\x2C",
                       sym("wMusicCh1CurOctave"): b"\x80"},
         read={sym("wMusicTie"): 1, sym("wddb7"): 1}),
]

CONTRACT["Music1_f475a"] = {"compare": (), "preserve": ()}
CASES["Music1_f475a"] = [
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb8"): b"\x00", sym("wMusicTie") + 1: b"\x00"},
     "read": {sym("wMusicTie") + 1: 1}},
    {"wram": {sym("wdd8c"): b"\x02", sym("wddb8"): b"\x00"},
     "read": {sym("wMusicTie") + 1: 1, sym("wddb8"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb8"): b"\x10", sym("wMusicTie") + 1: b"\x80",
              sym("wMusicVolume") + 1: b"\x77", sym("wMusicDuty2"): b"\xC0", sym("wMusicCh2CurPitch"): b"\x2C", sym("wMusicCh2CurOctave"): b"\x80"},
     "read": {sym("wMusicTie") + 1: 1, sym("wddb8"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb8"): b"\x10", sym("wMusicTie") + 1: b"\x02",
              sym("wMusicVolume") + 1: b"\x55", sym("wMusicDuty2"): b"\x40", sym("wMusicCh2CurPitch"): b"\x9C", sym("wMusicCh2CurOctave"): b"\x00"},
     "read": {sym("wMusicTie") + 1: 1, sym("wddb8"): 1}},
    dict(POISON, wram={sym("wdd8c"): b"\x00", sym("wddb8"): b"\x10", sym("wMusicTie") + 1: b"\x03",
                       sym("wMusicVolume") + 1: b"\x33", sym("wMusicDuty2"): b"\x80", sym("wMusicCh2CurPitch"): b"\x2C",
                       sym("wMusicCh2CurOctave"): b"\x80"},
         read={sym("wMusicTie") + 1: 1, sym("wddb8"): 1}),
]

CONTRACT["Music1_f479c"] = {"compare": (), "preserve": ()}
CASES["Music1_f479c"] = [
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb9"): b"\x00", sym("wMusicWaveChange"): b"\x00", sym("wMusicTie") + 2: b"\x00"},
     "read": {sym("wMusicTie") + 2: 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb9"): b"\x00", sym("wMusicWaveChange"): b"\x00",
              sym("wMusicTie"): b"\x55", sym("wMusicTie") + 2: b"\x01"},
     "read": {sym("wMusicTie"): 1, sym("wMusicTie") + 2: 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb9"): b"\x00", sym("wMusicWaveChange"): b"\x01",
              sym("wMusicTie"): b"\x55", sym("wMusicTie") + 2: b"\x01"},
     "read": {sym("wMusicTie"): 1, sym("wMusicTie") + 2: 1, sym("wMusicWaveChange"): 1}},
    {"wram": {sym("wdd8c"): b"\x04", sym("wddb9"): b"\x00"},
     "read": {sym("wMusicTie") + 2: 1, sym("wddb9"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb9"): b"\x10", sym("wMusicTie") + 2: b"\x80",
              sym("wMusicWaveChange"): b"\x00", sym("wMusicVolume") + 2: b"\x77", sym("wMusicCh3CurPitch"): b"\x2C", sym("wMusicCh3CurOctave"): b"\x80"},
     "read": {sym("wMusicTie") + 2: 1, sym("wddb9"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddb9"): b"\x10", sym("wMusicTie") + 2: b"\x02",
              sym("wMusicWaveChange"): b"\x00", sym("wMusicVolume") + 2: b"\x55", sym("wMusicCh3CurPitch"): b"\x9C", sym("wMusicCh3CurOctave"): b"\x00"},
     "read": {sym("wMusicTie") + 2: 1, sym("wddb9"): 1}},
    dict(POISON, wram={sym("wdd8c"): b"\x00", sym("wddb9"): b"\x10", sym("wMusicTie") + 2: b"\x03",
                       sym("wMusicWaveChange"): b"\x00", sym("wMusicVolume") + 2: b"\x33", sym("wMusicCh3CurPitch"): b"\x2C",
                       sym("wMusicCh3CurOctave"): b"\x80"},
         read={sym("wMusicTie") + 2: 1, sym("wddb9"): 1}),
]

CONTRACT["Music1_f480a"] = {"compare": (), "preserve": ()}
CASES["Music1_f480a"] = [
    {"wram": {sym("wdd8c"): b"\x00", sym("wddba"): b"\x00"},
     "read": {sym("wddef"): 1, sym("wddab"): 4}},
    {"wram": {sym("wdd8c"): b"\x08", sym("wddba"): b"\x05"},
     "read": {sym("wddba"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wddba"): b"\x01", sym("wddab"): b"\x01\x02\x03\x04"},
     "read": {sym("wddab"): 4}},
    dict(POISON, wram={sym("wdd8c"): b"\x00", sym("wddba"): b"\xA5",
                       sym("wddab"): b"\xAA\xBB\xCC\xDD"},
         read={sym("wddab"): 4}),
]

CONTRACT["Music1_f4839"] = {"compare": (), "preserve": ()}
CASES["Music1_f4839"] = [
    {"wram": {sym("wdd8c"): b"\x08", sym("wddef"): b"\x01"},
     "read": {sym("wddef"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wdded"): b"\x00\xC1",
              sym("wddef"): b"\x01", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x03"},
     "read": {sym("wdded"): 2, sym("wddef"): 1}},
    {"wram": {sym("wdd8c"): b"\x00", sym("wdded"): b"\x00\xC1",
              sym("wddef"): b"\x01", sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
     "read": {sym("wdded"): 2, sym("wddef"): 1}},
    dict(POISON, wram={sym("wdd8c"): b"\x00", sym("wdded"): b"\x50\xC1",
                       sym("wddef"): b"\x01", sym("wDecompressionSecondaryBufferStart") + 0x61: b"\x07"},
         read={sym("wdded"): 2, sym("wddef"): 1}),
]

CONTRACT["Music1_LoadWaveInstrument"] = {"compare": (), "preserve": ()}
CASES["Music1_LoadWaveInstrument"] = [
    {"wram": {sym("wMusicWave"): b"\x00", sym("wMusicWaveChange"): b"\x01"},
     "read": {sym("wMusicWaveChange"): 1}},
    {"wram": {sym("wMusicWave"): b"\x01", sym("wMusicWaveChange"): b"\x01"},
     "read": {sym("wMusicWaveChange"): 1}},
    dict(POISON, wram={sym("wMusicWave"): b"\x02", sym("wMusicWaveChange"): b"\x01"},
         read={sym("wMusicWaveChange"): 1}),
]

# -- Vibrato --------------------------------------------------------------

CONTRACT["Music1_UpdateVibrato"] = {"compare": ("d", "e", "c"), "preserve": ("c",)}
CASES["Music1_UpdateVibrato"] = [
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x00", sym("wMusicCh1CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh1CurPitch"): 2}},
    {"c": 1, "wram": {sym("wMusicVibratoDelay") + 1: b"\x00", sym("wMusicCh2CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh2CurPitch"): 2}},
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x05", sym("wdde3"): b"\x04",
                       sym("wMusicVibratoType"): b"\x00", sym("wdddb"): b"\x00",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh1CurPitch"): 2, sym("wdde3"): 1, sym("wdddb"): 1}},
    dict(POISON, b=0, c=2, wram={sym("wMusicVibratoDelay") + 2: b"\x00", sym("wMusicCh3CurPitch"): b"\x2C\x00"},
         read={sym("wMusicCh3CurPitch"): 2}),
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdde3"): b"\x01",
                       sym("wMusicVibratoType"): b"\x01", sym("wdddb"): b"\x01",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh1CurPitch"): 2, sym("wMusicVibratoType"): 1, sym("wdddb"): 1}},
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdde3"): b"\x01",
                       sym("wMusicVibratoType"): b"\x01", sym("wdddb"): b"\x05",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh1CurPitch"): 2, sym("wMusicVibratoType"): 1, sym("wdddb"): 1}},
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdde3"): b"\x01",
                       sym("wMusicVibratoType"): b"\x01", sym("wdddb"): b"\x00",
                       sym("wMusicCh1CurPitch"): b"\xFF\x0C"},
     "read": {sym("wMusicCh1CurPitch"): 2, sym("wMusicVibratoType"): 1, sym("wdddb"): 1}},
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdde3"): b"\x01",
                       sym("wMusicVibratoType"): b"\x02", sym("wdddb"): b"\x0C",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh1CurPitch"): 2, sym("wMusicVibratoType"): 1, sym("wdddb"): 1}},
    {"c": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdde3"): b"\x01",
                       sym("wMusicVibratoType"): b"\x01", sym("wdddb"): b"\x08",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"},
     "read": {sym("wMusicCh1CurPitch"): 2, sym("wMusicVibratoType"): 1, sym("wdddb"): 1}},
    {"c": 1, "wram": {sym("wMusicVibratoDelay") + 1: b"\x01", sym("wdde3") + 1: b"\x01",
                       sym("wMusicVibratoType") + 1: b"\x01", sym("wdddb") + 1: b"\x05",
                       sym("wMusicCh2CurPitch"): b"\x00\x01"},
     "read": {sym("wMusicCh2CurPitch"): 2, sym("wMusicVibratoType") + 1: 1, sym("wdddb") + 1: 1}},
]

CONTRACT["Music1_f490b"] = {"compare": (), "preserve": ()}
CASES["Music1_f490b"] = [
    {"a": 0, "wram": {sym("wMusicVibratoDelay"): b"\x00", sym("wdd8c"): b"\x00",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"}},
    {"a": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdd8c"): b"\x01"},
     "read": {sym("wMusicCh1CurPitch"): 2}},
    {"a": 0, "wram": {sym("wMusicVibratoDelay"): b"\x01", sym("wdd8c"): b"\x00",
                       sym("wMusicCh1CurPitch"): b"\x9C\x00"}},
    {"a": 1, "wram": {sym("wMusicVibratoDelay") + 1: b"\x00", sym("wdd8c"): b"\x00",
                       sym("wMusicCh2CurPitch"): b"\x2C\x00"}},
    {"a": 1, "wram": {sym("wMusicVibratoDelay") + 1: b"\x01", sym("wdd8c"): b"\x02"},
     "read": {sym("wMusicCh2CurPitch"): 2}},
    {"a": 1, "wram": {sym("wMusicVibratoDelay") + 1: b"\x01", sym("wdd8c"): b"\x00",
                       sym("wMusicCh2CurPitch"): b"\x9C\x00"}},
    {"a": 2, "wram": {sym("wMusicVibratoDelay") + 2: b"\x00", sym("wdd8c"): b"\x00",
                       sym("wMusicCh3CurPitch"): b"\x2C\x00"}},
    {"a": 2, "wram": {sym("wMusicVibratoDelay") + 2: b"\x01", sym("wdd8c"): b"\x04"},
     "read": {sym("wMusicCh3CurPitch"): 2}},
    {"a": 2, "wram": {sym("wMusicVibratoDelay") + 2: b"\x01", sym("wdd8c"): b"\x00",
                       sym("wMusicCh3CurPitch"): b"\x9C\x00"}},
    {"a": 3, "wram": {sym("wdd8c"): b"\x00", sym("wMusicCh1CurPitch"): b"\x2C\x00"}},
    dict(POISON, a=0, wram={sym("wMusicVibratoDelay"): b"\x01", sym("wdd8c"): b"\x00",
                             sym("wMusicCh1CurPitch"): b"\x06\x03"}),
]

CONTRACT["Music1_f4967"] = {"compare": ("d", "e", "c"), "preserve": ("c",)}
CASES["Music1_f4967"] = [
    {"c": 0, "d": 0x00, "e": 0x2C, "wram": {sym("wMusicFrequencyOffset"): b"\x00"}},
    {"c": 0, "d": 0x00, "e": 0x2C, "wram": {sym("wMusicFrequencyOffset"): b"\x10"}},
    {"c": 0, "d": 0x03, "e": 0x00, "wram": {sym("wMusicFrequencyOffset"): b"\x80"}},
    {"c": 1, "d": 0x00, "e": 0x2C, "wram": {sym("wMusicFrequencyOffset") + 1: b"\x20"}},
    dict(POISON, b=0, c=2, d=0x03, e=0x00, wram={sym("wMusicFrequencyOffset") + 2: b"\xFF"}),
]

CONTRACT["Music1_f485a"] = {"compare": (), "preserve": ()}
CASES["Music1_f485a"] = [
    {"a": 0, "wram": {sym("wMusicVibratoDelay"): b"\x00", sym("wdd8c"): b"\x00",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"}},
    {"a": 1, "wram": {sym("wMusicVibratoDelay") + 1: b"\x00", sym("wdd8c"): b"\x00",
                       sym("wMusicCh2CurPitch"): b"\x2C\x00"}},
    dict(POISON, a=0, wram={sym("wMusicVibratoDelay"): b"\x01", sym("wdd8c"): b"\x00",
                             sym("wMusicCh1CurPitch"): b"\x9C\x00"}),
]

# -- Panning / output select ----------------------------------------------

CONTRACT["Music1_f4866"] = {"compare": (), "preserve": ()}
CASES["Music1_f4866"] = [
    {"wram": {sym("wMusicPanning"): b"\x77", sym("wdd8c"): b"\x00", sym("wMusicStereoPanning"): b"\xFF",
              sym("wddf0"): b"\x00"}},
    {"wram": {sym("wMusicPanning"): b"\x77", sym("wdd8c"): b"\x0F", sym("wMusicStereoPanning"): b"\xFF",
              sym("wdd85"): b"\xFF", sym("wddf0"): b"\x00"}},
    {"wram": {sym("wMusicPanning"): b"\x77", sym("wdd8c"): b"\x03", sym("wMusicStereoPanning"): b"\xCC",
              sym("wdd85"): b"\x33", sym("wddf0"): b"\xFF"}},
    dict(POISON, wram={sym("wMusicPanning"): b"\x77", sym("wdd8c"): b"\x05", sym("wMusicStereoPanning"): b"\xAA",
                       sym("wdd85"): b"\x55", sym("wddf0"): b"\x0F"}),
]

# -- Channel updaters -----------------------------------------------------

CONTRACT["Music1_UpdateChannel1"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel1"] = [
    {"wram": {sym("wMusicIsPlaying"): b"\x00", sym("wdd8c"): b"\x00",
              sym("wMusicChannelPointers"): b"\x00\xC1",
              sym("wddb7"): b"\x00", sym("wddbb"): b"\x01", sym("wMusicVibratoDelay"): b"\x00",
              sym("wMusicCh1CurPitch"): b"\x2C\x00"}},
    {"wram": {sym("wMusicIsPlaying"): b"\x01", sym("wdd8c"): b"\x00",
              sym("wddbb"): b"\x01", sym("wMusicVibratoDelay"): b"\x00",
              sym("wddb7"): b"\x10", sym("wddc3"): b"\x01",
              sym("wMusicChannelPointers"): b"\x00\xC1",
              sym("wMusicVolume"): b"\x77", sym("wMusicDuty1"): b"\xC0",
              sym("wMusicCh1CurPitch"): b"\x9C\x00", sym("wMusicCh1CurOctave"): b"\x00"}},
    dict(POISON, wram={sym("wMusicIsPlaying"): b"\x01", sym("wdd8c"): b"\x00",
                       sym("wddbb"): b"\x01", sym("wMusicVibratoDelay"): b"\x00",
                       sym("wMusicChannelPointers"): b"\x00\xC1",
                       sym("wddb7"): b"\x00", sym("wddc3"): b"\x01",
                       sym("wMusicCh1CurPitch"): b"\x2C\x00"}),
    # echo counter wraps $00 -> $FF; music1.asm:392-395 decrements
    # unconditionally, with no zero guard before the store.
    {"wram": {sym("wMusicIsPlaying"): b"\x01", sym("wdd8c"): b"\x00",
              sym("wddb7"): b"\x10", sym("wddbb"): b"\x05",
              sym("wddc3"): b"\x00", sym("wMusicVibratoDelay"): b"\x00"}},
]

CONTRACT["Music1_UpdateChannel2"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel2"] = [
    {"wram": {sym("wMusicIsPlaying") + 1: b"\x00", sym("wdd8c"): b"\x00",
              sym("wMusicChannelPointers") + 2: b"\x00\xC1",
              sym("wddb8"): b"\x00", sym("wddbb") + 1: b"\x01", sym("wMusicVibratoDelay") + 1: b"\x00",
              sym("wMusicCh2CurPitch"): b"\x2C\x00"}},
    {"wram": {sym("wMusicIsPlaying") + 1: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddbb") + 1: b"\x01", sym("wMusicVibratoDelay") + 1: b"\x00",
              sym("wddb8"): b"\x10", sym("wddc3") + 1: b"\x01",
              sym("wMusicChannelPointers") + 2: b"\x00\xC1",
              sym("wMusicVolume") + 1: b"\x77", sym("wMusicDuty2"): b"\xC0",
              sym("wMusicCh2CurPitch"): b"\x9C\x00", sym("wMusicCh2CurOctave"): b"\x00"}},
    dict(POISON, wram={sym("wMusicIsPlaying") + 1: b"\x01", sym("wdd8c"): b"\x00",
                       sym("wddbb") + 1: b"\x01", sym("wMusicVibratoDelay") + 1: b"\x00",
                       sym("wMusicChannelPointers") + 2: b"\x00\xC1",
                       sym("wddb8"): b"\x00", sym("wddc3") + 1: b"\x01",
                       sym("wMusicCh2CurPitch"): b"\x2C\x00"}),
    # echo counter wraps $00 -> $FF (music1.asm:445-448).
    {"wram": {sym("wMusicIsPlaying") + 1: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddb8"): b"\x10", sym("wddbb") + 1: b"\x05",
              sym("wddc3") + 1: b"\x00", sym("wMusicVibratoDelay") + 1: b"\x00"}},
]

CONTRACT["Music1_UpdateChannel3"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel3"] = [
    {"wram": {sym("wMusicIsPlaying") + 2: b"\x00", sym("wdd8c"): b"\x00",
              sym("wMusicChannelPointers") + 4: b"\x00\xC1",
              sym("wddb9"): b"\x00", sym("wddbb") + 2: b"\x01", sym("wMusicVibratoDelay") + 2: b"\x00",
              sym("wMusicCh3CurPitch"): b"\x2C\x00", sym("wMusicWaveChange"): b"\x00"}},
    {"wram": {sym("wMusicIsPlaying") + 2: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddbb") + 2: b"\x01", sym("wMusicVibratoDelay") + 2: b"\x00",
              sym("wddb9"): b"\x10", sym("wddc3") + 2: b"\x01",
              sym("wMusicChannelPointers") + 4: b"\x00\xC1",
              sym("wMusicVolume") + 2: b"\x77", sym("wMusicCh3CurPitch"): b"\x9C\x00", sym("wMusicCh3CurOctave"): b"\x00",
              sym("wMusicWaveChange"): b"\x00"}},
    dict(POISON, wram={sym("wMusicIsPlaying") + 2: b"\x01", sym("wdd8c"): b"\x00",
                       sym("wddbb") + 2: b"\x01", sym("wMusicVibratoDelay") + 2: b"\x00",
                       sym("wMusicChannelPointers") + 4: b"\x00\xC1",
                       sym("wddb9"): b"\x00", sym("wddc3") + 2: b"\x01",
                       sym("wMusicCh3CurPitch"): b"\x2C\x00", sym("wMusicWaveChange"): b"\x00"}),
    # echo counter wraps $00 -> $FF (music1.asm:498-501).
    {"wram": {sym("wMusicIsPlaying") + 2: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddb9"): b"\x10", sym("wddbb") + 2: b"\x05",
              sym("wddc3") + 2: b"\x00", sym("wMusicVibratoDelay") + 2: b"\x00"}},
]

CONTRACT["Music1_UpdateChannel4"] = {"compare": (), "preserve": ()}
CASES["Music1_UpdateChannel4"] = [
    {"wram": {sym("wMusicIsPlaying") + 3: b"\x00", sym("wdd8c"): b"\x00",
              sym("wMusicChannelPointers") + 6: b"\x00\xC1",
              sym("wddba"): b"\x00", sym("wddbb") + 3: b"\x01", sym("wddef"): b"\x00"}},
    {"wram": {sym("wMusicIsPlaying") + 3: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddbb") + 3: b"\x01", sym("wddef"): b"\x00",
              sym("wMusicOctave"): b"\x05",
              sym("wMusicChannelPointers") + 6: b"\x00\xC1",
              sym("wddba"): b"\x01",
              sym("wdded"): b"\x00\xC1",
              sym("wddab"): b"\x01\x02\x03\x04"}},
    dict(POISON, wram={sym("wMusicIsPlaying") + 3: b"\x01", sym("wdd8c"): b"\x00",
                       sym("wddbb") + 3: b"\x01", sym("wddef"): b"\x00",
                       sym("wMusicChannelPointers") + 6: b"\x00\xC1",
                       sym("wddba"): b"\x00"}),
    # channel 4 has no echo counter: wddc3+3 must never move, unlike
    # channels 1-3 (music1.asm:540-577 has no wddc3 reference at all).
    {"wram": {sym("wMusicIsPlaying") + 3: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddba"): b"\x10", sym("wddbb") + 3: b"\x05",
              sym("wddef"): b"\x00", sym("wddc3") + 3: b"\x42"}},
    # music1.asm:1122-1127 (Music1_end): the popped stream pointer is
    # discarded via `pop hl; ret`, never stored to wMusicChannelPointers.
    # A note whose stream immediately hits an end command ($DA) must leave
    # wMusicChannelPointers at the command byte's own address, not the
    # post-increment position past it.
    {"wram": {sym("wMusicIsPlaying") + 3: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddbb") + 3: b"\x01", sym("wddef"): b"\x00",
              sym("wMusicChannelPointers") + 6: b"\x00\xC3",
              sym("wOpponentCardLocations"): b"\xDA"}},
    # channel 4 never reaches Music1_f485a/UpdateVibrato (music1.asm:
    # 559-564): a nonzero vibrato delay must not advance wdde3+3.
    {"wram": {sym("wMusicIsPlaying") + 3: b"\x01", sym("wdd8c"): b"\x00",
              sym("wddbb") + 3: b"\x05", sym("wddef"): b"\x00",
              sym("wMusicVibratoDelay") + 3: b"\x05", sym("wdde3") + 3: b"\x33"}},
]

# -- Pause / Resume / Backup / LoadBackup ---------------------------------

CONTRACT["Music1_PauseSong"] = {"compare": (), "preserve": ()}
CASES["Music1_PauseSong"] = [
    {"wram": {sym("wCurSongID"): b"\x80", sym("wCurSongBank"): b"\x3D", sym("wdd8c"): b"\x00",
              sym("wMusicIsPlaying"): b"\x00\x00\x00\x00"}},
    dict(POISON, wram={sym("wCurSongID"): b"\x80", sym("wCurSongBank"): b"\x3D", sym("wdd8c"): b"\x0F",
                       sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"}),
]

CONTRACT["Music1_ResumeSong"] = {"compare": (), "preserve": ()}
CASES["Music1_ResumeSong"] = [
    {"wram": {sym("wCurSongID"): b"\x80", sym("wCurSongBank"): b"\x3D", sym("wdd8c"): b"\x00",
              sym("wCurSongIDBackup"): b"\x80", sym("wCurSongBankBackup"): b"\x3D",
              sym("wMusicIsPlaying"): b"\x00\x00\x00\x00"}},
    dict(POISON, wram={sym("wCurSongID"): b"\x80", sym("wCurSongBank"): b"\x3D", sym("wdd8c"): b"\x0F",
                       sym("wCurSongIDBackup"): b"\x81", sym("wCurSongBankBackup"): b"\x3E",
                       sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"}),
]

CONTRACT["Music1_BackupSong"] = {"compare": (), "preserve": ()}
CASES["Music1_BackupSong"] = [
    {"wram": {sym("wCurSongID"): b"\x05", sym("wCurSongBank"): b"\x3D",
              sym("wMusicStereoPanning"): b"\xFF", sym("wMusicDuty1"): b"\x01\x02\x03\x04",
              sym("wMusicWave"): b"\x03", sym("wMusicWaveChange"): b"\x00",
              sym("wMusicIsPlaying"): b"\x01\x01\x01\x01",
              sym("wMusicTie"): b"\x01\x01\x01\x01",
              sym("wMusicChannelPointers"): b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              sym("wMusicMainLoopStart"): b"\x00\xD1\x00\xD2\x00\xD3\x00\xD4",
              sym("wddab"): b"\xAA\xBB",
              sym("wMusicOctave"): b"\x02\x02\x02\x02",
              sym("wddb3"): b"\x03\x03\x03\x03",
              sym("wddb7"): b"\x10\x10\x10\x10",
              sym("wddbb"): b"\x04\x04\x04\x04",
              sym("wMusicCutoff"): b"\x05\x05\x05\x05",
              sym("wddc3"): b"\x06\x06\x06\x06",
              sym("wMusicEcho"): b"\x07\x07\x07\x07",
              sym("wMusicPitchOffset"): b"\x08\x08\x08\x08",
              sym("wMusicSpeed"): b"\x09\x09\x09\x09",
              sym("wMusicVibratoType2"): b"\x0A\x0A\x0A\x0A",
              sym("wMusicVibratoDelay"): b"\x0B\x0B\x0B\x0B",
              sym("wMusicVolume"): b"\x77\x77\x77",
              sym("wMusicFrequencyOffset"): b"\x00\x00\x00",
              sym("wdded"): b"\x50\xC1",
              sym("wMusicChannelStackPointers"): b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              sym("wMusicCh1Stack"): b"\x00" * 48},
     "read": {sym("wCurSongIDBackup"): 2}},
    dict(POISON, wram={sym("wCurSongID"): b"\x05", sym("wCurSongBank"): b"\x3E",
                       sym("wMusicStereoPanning"): b"\xAA", sym("wMusicDuty1"): b"\x40\x00\x80\xC0",
                       sym("wMusicWave"): b"\x00", sym("wMusicWaveChange"): b"\x01",
                       sym("wMusicIsPlaying"): b"\x00\x00\x00\x01",
                       sym("wMusicTie"): b"\x00\x00\x00\x01",
                       sym("wMusicChannelPointers"): b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       sym("wMusicMainLoopStart"): b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       sym("wddab"): b"\x00\x00",
                       sym("wMusicOctave"): b"\x00\x00\x00\x00",
                       sym("wddb3"): b"\x00\x00\x00\x00",
                       sym("wddb7"): b"\x00\x00\x00\x00",
                       sym("wddbb"): b"\x00\x00\x00\x00",
                       sym("wMusicCutoff"): b"\x00\x00\x00\x00",
                       sym("wddc3"): b"\x00\x00\x00\x00",
                       sym("wMusicEcho"): b"\x00\x00\x00\x00",
                       sym("wMusicPitchOffset"): b"\x00\x00\x00\x00",
                       sym("wMusicSpeed"): b"\x00\x00\x00\x00",
                       sym("wMusicVibratoType2"): b"\x00\x00\x00\x00",
                       sym("wMusicVibratoDelay"): b"\x00\x00\x00\x00",
                       sym("wMusicVolume"): b"\x00\x00\x00",
                       sym("wMusicFrequencyOffset"): b"\x00\x00\x00",
                       sym("wdded"): b"\x00\x00",
                       sym("wMusicChannelStackPointers"): b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       sym("wMusicCh1Stack"): b"\x00" * 48}),
]

CONTRACT["Music1_LoadBackup"] = {"compare": (), "preserve": ()}
CASES["Music1_LoadBackup"] = [
    {"wram": {sym("wCurSongID"): b"\x80", sym("wCurSongBank"): b"\x3D",
              sym("wCurSongIDBackup"): b"\x05", sym("wCurSongBankBackup"): b"\x3E",
              sym("wMusicStereoPanningBackup"): b"\xFF",
              sym("wMusicDuty1Backup"): b"\x01\x02\x03\x04",
              sym("wMusicWaveBackup"): b"\x03", sym("wMusicWaveChangeBackup"): b"\x00",
              sym("wMusicIsPlayingBackup"): b"\x01\x01\x01\x01",
              sym("wMusicTieBackup"): b"\x01\x01\x01\x01",
              sym("wMusicChannelPointersBackup"): b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              sym("wMusicMainLoopStartBackup"): b"\x00\xD1\x00\xD2\x00\xD3\x00\xD4",
              sym("wde76"): b"\xAA", sym("wde77"): b"\xBB",
              sym("wMusicOctaveBackup"): b"\x02\x02\x02\x02",
              sym("wde7c"): b"\x03\x03\x03\x03",
              sym("wde80"): b"\x10\x10\x10\x10",
              sym("wde84"): b"\x04\x04\x04\x04",
              sym("wMusicCutoffBackup"): b"\x05\x05\x05\x05",
              sym("wde8c"): b"\x06\x06\x06\x06",
              sym("wMusicEchoBackup"): b"\x07\x07\x07\x07",
              sym("wMusicPitchOffsetBackup"): b"\x08\x08\x08\x08",
              sym("wMusicSpeedBackup"): b"\x09\x09\x09\x09",
              sym("wMusicVibratoType2Backup"): b"\x0A\x0A\x0A\x0A",
              sym("wMusicVibratoDelayBackup"): b"\x0B\x0B\x0B\x0B",
              sym("wMusicVolumeBackup"): b"\x77\x77\x77",
              sym("wMusicFrequencyOffsetBackup"): b"\x00\x00\x00",
              sym("wdeaa"): b"\x50\xC1",
              sym("wdeac"): b"\x00",
              sym("wMusicChannelStackPointersBackup"): b"\x00\xC1\x00\xC2\x00\xC3\x00\xC4",
              sym("wMusicCh1StackBackup"): b"\x00" * 48}},
    dict(POISON, wram={sym("wCurSongID"): b"\x80", sym("wCurSongBank"): b"\x3D",
                       sym("wCurSongIDBackup"): b"\x00", sym("wCurSongBankBackup"): b"\x3D",
                       sym("wMusicStereoPanningBackup"): b"\xAA",
                       sym("wMusicDuty1Backup"): b"\x40\x00\x80\xC0",
                       sym("wMusicWaveBackup"): b"\x00", sym("wMusicWaveChangeBackup"): b"\x01",
                       sym("wMusicIsPlayingBackup"): b"\x00\x00\x00\x01",
                       sym("wMusicTieBackup"): b"\x00\x00\x00\x01",
                       sym("wMusicChannelPointersBackup"): b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       sym("wMusicMainLoopStartBackup"): b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       sym("wde76"): b"\x00", sym("wde77"): b"\x00",
                       sym("wMusicOctaveBackup"): b"\x00\x00\x00\x00",
                       sym("wde7c"): b"\x00\x00\x00\x00",
                       sym("wde80"): b"\x00\x00\x00\x00",
                       sym("wde84"): b"\x00\x00\x00\x00",
                       sym("wMusicCutoffBackup"): b"\x00\x00\x00\x00",
                       sym("wde8c"): b"\x00\x00\x00\x00",
                       sym("wMusicEchoBackup"): b"\x00\x00\x00\x00",
                       sym("wMusicPitchOffsetBackup"): b"\x00\x00\x00\x00",
                       sym("wMusicSpeedBackup"): b"\x00\x00\x00\x00",
                       sym("wMusicVibratoType2Backup"): b"\x00\x00\x00\x00",
                       sym("wMusicVibratoDelayBackup"): b"\x00\x00\x00\x00",
                       sym("wMusicVolumeBackup"): b"\x00\x00\x00",
                       sym("wMusicFrequencyOffsetBackup"): b"\x00\x00\x00",
                       sym("wdeaa"): b"\x00\x00",
                       sym("wdeac"): b"\x00",
                       sym("wMusicChannelStackPointersBackup"): b"\x00\x00\x00\x00\x00\x00\x00\x00",
                       sym("wMusicCh1StackBackup"): b"\x00" * 48}),
]

# -- High-level -----------------------------------------------------------

CONTRACT["Music1_CheckForNewSound"] = {"compare": (), "preserve": ()}
CASES["Music1_CheckForNewSound"] = [
    {"wram": {sym("wCurSongID"): b"\x80", sym("wCurSfxID"): b"\x80"}},
    {"wram": {sym("wCurSongID"): b"\x00", sym("wCurSfxID"): b"\x80",
              sym("wCurSongBank"): b"\x3D",
              sym("wMusicIsPlaying"): b"\x00\x00\x00\x00"},
     "read": {sym("wCurSongID"): 1}},
    dict(POISON, wram={sym("wCurSongID"): b"\x05", sym("wCurSfxID"): b"\x00",
                       sym("wCurSongBank"): b"\x3D",
                       sym("wMusicIsPlaying"): b"\x00\x00\x00\x00"},
         read={sym("wCurSongID"): 1, sym("wCurSfxID"): 1}),
]

CONTRACT["Music1_Update"] = {"compare": (), "preserve": ()}
CASES["Music1_Update"] = [
    {"wram": {sym("wCurSongBank"): b"\x3D", sym("wddf2"): b"\x01",
              sym("wdd8c"): b"\x0F", sym("wCurSongID"): b"\x80",
              sym("wCurSfxID"): b"\x80"},
     "read": {sym("wMusicIsPlaying"): 4}},
    {"wram": {sym("wCurSongBank"): b"\x3D", sym("wddf2"): b"\x00",
              sym("wdd8c"): b"\x00", sym("wCurSongID"): b"\x80",
              sym("wCurSfxID"): b"\x80",
              sym("wMusicIsPlaying"): b"\x00\x00\x00\x00",
              sym("wddbb"): b"\x01\x01\x01\x01",
              sym("wddb7"): b"\x00\x00\x00\x00",
              sym("wddef"): b"\x00",
              sym("wMusicChannelPointers"): b"\x00\xC1\x00\xC1\x00\xC1\x00\xC1",
              sym("wMusicVibratoDelay"): b"\x00\x00\x00\x00",
              sym("wMusicCh1CurPitch"): b"\x2C\x00",
              sym("wMusicCh2CurPitch"): b"\x2C\x00",
              sym("wMusicCh3CurPitch"): b"\x2C\x00",
              sym("wMusicPanning"): b"\x77",
              sym("wMusicStereoPanning"): b"\xFF", sym("wdd85"): b"\x00",
              sym("wddf0"): b"\x00"},
     "read": {sym("wMusicIsPlaying"): 4}},
    dict(POISON, wram={sym("wCurSongBank"): b"\x3D", sym("wddf2"): b"\x01",
                       sym("wdd8c"): b"\x0F", sym("wCurSongID"): b"\x80",
                       sym("wCurSfxID"): b"\x80"},
         read={sym("wMusicIsPlaying"): 4}),
    # wCurSongBank ($DD81) = $3E banks in the music2 driver, and music1.asm's
    # `call Music1_UpdateChannel1` then resolves to 3e:40e9's copy instead of
    # 3d's. Every other case here sets $3D, so the whole music2 dispatch was
    # unobserved; the reference takes it on 208 of its 2,001 audio ticks over
    # the boot timeline.
    {"wram": {sym("wCurSongBank"): b"\x3E", sym("wddf2"): b"\x00",
              sym("wdd8c"): b"\x00", sym("wCurSongID"): b"\x80",
              sym("wCurSfxID"): b"\x80",
              sym("wMusicIsPlaying"): b"\x01\x01\x01\x01",
              sym("wddbb"): b"\x01\x01\x01\x01",
              sym("wddb7"): b"\x00\x00\x00\x00",
              sym("wddef"): b"\x00",
              sym("wMusicChannelPointers"): b"\x00\xC1\x00\xC1\x00\xC1\x00\xC1",
              sym("wMusicVibratoDelay"): b"\x00\x00\x00\x00",
              sym("wMusicCh1CurPitch"): b"\x2C\x00",
              sym("wMusicCh2CurPitch"): b"\x2C\x00",
              sym("wMusicCh3CurPitch"): b"\x2C\x00",
              sym("wMusicPanning"): b"\x77",
              sym("wMusicStereoPanning"): b"\xFF", sym("wdd85"): b"\x00",
              sym("wddf0"): b"\x00"},
     "read": {sym("wMusicIsPlaying"): 4, sym("wddbb"): 4, sym("wddc3"): 4}},
]
# >>> factory _PauseSong
CONTRACT["_PauseSong"] = {"compare": (), "preserve": ()}
CASES["_PauseSong"] = [{}, dict(POISON, wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00"})]
# <<< factory _PauseSong

# >>> factory _ResumeSong
CONTRACT["_ResumeSong"] = {"compare": (), "preserve": ()}
CASES["_ResumeSong"] = [{}, dict(POISON, wram={sym("wDecompressionSecondaryBufferStart") + 0x12: b"\x00"})]
# <<< factory _ResumeSong

# >>> factory Music1_f400c
CONTRACT["Music1_f400c"] = {"compare": (), "preserve": ()}
CASES["Music1_f400c"] = [
    {"a": 0x42, "read": {sym("wddf0"): 1}},
    dict(POISON, read={sym("wddf0"): 1}, wram={sym("wDecompressionSecondaryBufferStart") + 0x14: b"\x00"}),
]
# <<< factory Music1_f400c

# >>> factory Music1_f4018
CONTRACT["Music1_f4018"] = {"compare": ("b", "c"), "preserve": ("b", "c")};
CASES["Music1_f4018"] = [
    {"a": 0x00, "read": {sym("wMusicPanning"): 1}},
    {"a": 0x07, "read": {sym("wMusicPanning"): 1}},
    {"a": 0x77, "read": {sym("wMusicPanning"): 1}},
    dict(POISON, read={sym("wMusicPanning"): 1}),
]
# <<< factory Music1_f4018

# >>> factory _AssertSFXFinished
CONTRACT["_AssertSFXFinished"] = {"compare": ("a",), "preserve": ()}
CASES["_AssertSFXFinished"] = [
    {"wram": {sym("wCurSfxID"): b"\x80"}},
    {"wram": {sym("wCurSfxID"): b"\x00"}},
    dict(POISON, wram={sym("wCurSfxID"): b"\x55"}),
]
# <<< factory _AssertSFXFinished

# >>> factory _AssertSongFinished
CONTRACT["_AssertSongFinished"] = {"compare": ("a",), "preserve": ()}
CASES["_AssertSongFinished"] = [
    {"wram": {sym("wCurSongID"): b"\x80"}},
    {"wram": {sym("wCurSongID"): b"\x00"}},
    {"wram": {sym("wCurSongID"): b"\x7F"}},
    dict(POISON, wram={sym("wCurSongID"): b"\xFF"}),
]
# <<< factory _AssertSongFinished

# >>> factory _PlaySFX
CONTRACT["_PlaySFX"] = {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")}
CASES["_PlaySFX"] = [
    {"a": 0x00, "read": {sym("wSfxPriority"): 1, sym("wCurSfxID"): 1}},
    {"a": 0x01, "read": {sym("wSfxPriority"): 1, sym("wCurSfxID"): 1}},
    {"a": 0x01, "wram": {sym("wSfxPriority"): b"\x0A", sym("wCurSfxID"): b"\x05"}},
    {"a": 0x01, "wram": {sym("wSfxPriority"): b"\x05", sym("wCurSfxID"): b"\x80"}},
    dict(POISON, read={sym("wSfxPriority"): 1, sym("wCurSfxID"): 1}),
]
# <<< factory _PlaySFX

# >>> factory _PlaySong
CONTRACT["_PlaySong"] = {"compare": ("hl",), "preserve": ("hl",)}
CASES["_PlaySong"] = [
    {"a": 0x00, "read": {sym("wCurSongID"): 1}},
    {"a": 0x1E, "read": {sym("wCurSongID"): 1}},
    {"a": 0x1F, "read": {sym("wCurSongID"): 1}},
    {"a": 0xFF, "read": {sym("wCurSongID"): 1}},
    dict(POISON, read={sym("wCurSongID"): 1}),
]
# <<< factory _PlaySong

# >>> factory _SetupSound
CONTRACT["_SetupSound"] = {"compare": (), "preserve": ()}
CASES["_SetupSound"] = [
    {"read": {sym("wCurSongID"): 1, sym("wCurSfxID"): 1, sym("wMusicIsPlaying"): 4, sym("wMusicTie"): 4, sym("wddb3"): 4,
              sym("wMusicPitchOffset"): 4, sym("wMusicCutoff"): 4, sym("wMusicPanning"): 1, sym("wMusicChannelStackPointers"): 8, sym("wddf0"): 1,
              sym("wddf2"): 1, sym("wdd8c"): 1, sym("wMusicStereoPanning"): 1, sym("wCurSongBank"): 1, sym("wddef"): 1}},
    dict(POISON, read={sym("wCurSongID"): 1, sym("wCurSfxID"): 1, sym("wMusicIsPlaying"): 4, sym("wMusicTie"): 4,
                       sym("wddb3"): 4, sym("wMusicPitchOffset"): 4, sym("wMusicCutoff"): 4, sym("wMusicPanning"): 1,
                       sym("wMusicChannelStackPointers"): 8, sym("wddf0"): 1, sym("wddf2"): 1, sym("wdd8c"): 1,
                       sym("wMusicStereoPanning"): 1, sym("wCurSongBank"): 1, sym("wddef"): 1}),
]
# <<< factory _SetupSound

# >>> factory SoundTimerHandler
CONTRACT["SoundTimerHandler"] = {"compare": (), "preserve": ()}
CASES["SoundTimerHandler"] = [
    {"wram": {sym("wCurSongID"): b"\x00", sym("wCurSfxID"): b"\x80"}, "read": {sym("wCurSongID"): 1}},
    dict(POISON, wram={sym("wCurSongID"): b"\x00", sym("wCurSfxID"): b"\x80"}, read={sym("wCurSongID"): 1}),
]
# <<< factory SoundTimerHandler

# >>> factory Music1_f4015
CONTRACT["Music1_f4015"] = {"compare": (), "preserve": ()}
CASES["Music1_f4015"] = [
    {"wram": {sym("wddf2"): b"\x00"}, "expect": {sym("wddf2"): b"\x01"}},
    {"wram": {sym("wddf2"): b"\x01"}, "expect": {sym("wddf2"): b"\x00"}},
    dict(POISON, wram={sym("wddf2"): b"\x05"}, expect={sym("wddf2"): b"\x04"}),
]
# <<< factory Music1_f4015

# >>> factory Music1_duty
CONTRACT["Music1_duty"] = {"compare": (), "preserve": ()}
CASES["Music1_duty"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicDuty1"): 1}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x3F\xFF"}, "read": {sym("wMusicDuty2"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x80\xFF"}, "read": {sym("wMusicDuty2") + 2: 1}},
    dict(POISON, b=0, c=2, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"},
         read={sym("wMusicDuty2") + 1: 1}),
]
# <<< factory Music1_duty

# >>> factory Music1_speed
CONTRACT["Music1_speed"] = {"compare": (), "preserve": ()}
CASES["Music1_speed"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF"}, "read": {sym("wMusicSpeed"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"}, "read": {sym("wMusicSpeed"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicSpeed") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"},
         read={sym("wMusicSpeed") + 1: 1}),
]
# <<< factory Music1_speed

# >>> factory Music1_inc_octave
CONTRACT["Music1_inc_octave"] = {"compare": (), "preserve": ()}
CASES["Music1_inc_octave"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave"): b"\x00"},
     "read": {sym("wMusicOctave"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave"): b"\xFF"},
     "read": {sym("wMusicOctave"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave") + 3: b"\x07"},
     "read": {sym("wMusicOctave") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave") + 1: b"\x10"},
         read={sym("wMusicOctave") + 1: 1}),
]
# <<< factory Music1_inc_octave

# >>> factory Music1_dec_octave
CONTRACT["Music1_dec_octave"] = {"compare": (), "preserve": ()}
CASES["Music1_dec_octave"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave"): b"\x01"},
     "read": {sym("wMusicOctave"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave"): b"\x00"},
     "read": {sym("wMusicOctave"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave") + 3: b"\x07"},
     "read": {sym("wMusicOctave") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicOctave") + 1: b"\x10"},
         read={sym("wMusicOctave") + 1: 1}),
]
# <<< factory Music1_dec_octave

# >>> factory Music1_tie
CONTRACT["Music1_tie"] = {"compare": (), "preserve": ()}
CASES["Music1_tie"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicTie"): b"\x00"},
     "read": {sym("wMusicTie"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicTie") + 3: b"\xFF"},
     "read": {sym("wMusicTie") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicTie") + 1: b"\x7F"},
         read={sym("wMusicTie") + 1: 1}),
]
# <<< factory Music1_tie

# >>> factory Music1_stereo_panning
CONTRACT["Music1_stereo_panning"] = {"compare": (), "preserve": ()}
CASES["Music1_stereo_panning"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x11\xFF", sym("wMusicStereoPanning"): b"\x00"},
     "read": {sym("wMusicStereoPanning"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF", sym("wMusicStereoPanning"): b"\xFF"},
     "read": {sym("wMusicStereoPanning"): 1}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x11\xFF", sym("wMusicStereoPanning"): b"\x00"},
     "read": {sym("wMusicStereoPanning"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x81\xFF", sym("wMusicStereoPanning"): b"\x00"},
     "read": {sym("wMusicStereoPanning"): 1}},
    dict(POISON, b=0, c=2, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x11\xFF", sym("wMusicStereoPanning"): b"\xAA"},
         read={sym("wMusicStereoPanning"): 1}),
]
# <<< factory Music1_stereo_panning

# >>> factory Music1_MainLoop
CONTRACT["Music1_MainLoop"] = {"compare": (), "preserve": ()}
CASES["Music1_MainLoop"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"}, "read": {sym("wMusicMainLoopStart"): 2}},
    {"c": 3, "stack": [sym("wPlayerCardLocations")], "wram": {sym("wPlayerCardLocations"): b"\xFF"}, "read": {sym("wMusicMainLoopStart") + 6: 2}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
         read={sym("wMusicMainLoopStart") + 2: 2}),
]
# <<< factory Music1_MainLoop

# >>> factory Music1_Loop
CONTRACT["Music1_Loop"] = {"compare": (), "preserve": ()}
CASES["Music1_Loop"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x03\xFF", sym("wMusicChannelStackPointers"): b"\x00\xC2"},
     "read": {sym("wPlayerCardLocations"): 3, sym("wMusicChannelStackPointers"): 2}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x01\xFF", sym("wMusicChannelStackPointers") + 2: b"\x00\xC3"},
     "read": {sym("wOpponentCardLocations"): 3, sym("wMusicChannelStackPointers") + 2: 2}},
    dict(POISON, b=0, c=2, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF", sym("wMusicChannelStackPointers") + 4: b"\x10\xC2"},
         read={sym("wPlayerCardLocations") + 0x10: 3, sym("wMusicChannelStackPointers") + 4: 2}),
]
# <<< factory Music1_Loop

# >>> factory Music1_call
CONTRACT["Music1_call"] = {"compare": (), "preserve": ()}
CASES["Music1_call"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xC2", sym("wPlayerCardLocations"): b"\xFF", sym("wMusicChannelStackPointers"): b"\x00\xC3"},
     "read": {sym("wOpponentCardLocations"): 2, sym("wMusicChannelStackPointers"): 2}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x21],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x21: b"\x00\xC2", sym("wPlayerCardLocations"): b"\xFF", sym("wMusicChannelStackPointers") + 2: b"\x20\xC3"},
     "read": {sym("wOpponentCardLocations") + 0x20: 2, sym("wMusicChannelStackPointers") + 2: 2}},
    dict(POISON, b=0, c=3, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xC2", sym("wPlayerCardLocations"): b"\xFF", sym("wMusicChannelStackPointers") + 6: b"\x40\xC3"},
         read={sym("wOpponentPrizeCards") + 4: 2, sym("wMusicChannelStackPointers") + 6: 2}),
]
# <<< factory Music1_call

# >>> factory Music1_ret
CONTRACT["Music1_ret"] = {"compare": (), "preserve": ()}
CASES["Music1_ret"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wMusicChannelStackPointers"): b"\x02\xC3", sym("wOpponentCardLocations"): b"\x00\xC2", sym("wPlayerCardLocations") + 2: b"\xFF"},
     "read": {sym("wMusicChannelStackPointers"): 2}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wMusicChannelStackPointers") + 2: b"\x22\xC3", sym("wOpponentCardLocations") + 0x20: b"\x00\xC2", sym("wPlayerCardLocations") + 2: b"\xFF"},
     "read": {sym("wMusicChannelStackPointers") + 2: 2}},
    dict(POISON, b=0, c=3, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wMusicChannelStackPointers") + 6: b"\x42\xC3", sym("wOpponentPrizeCards") + 4: b"\x00\xC2", sym("wPlayerCardLocations") + 2: b"\xFF"},
         read={sym("wMusicChannelStackPointers") + 6: 2}),
]
# <<< factory Music1_ret

# >>> factory Music1_frequency_offset
CONTRACT["Music1_frequency_offset"] = {"compare": (), "preserve": ()}
CASES["Music1_frequency_offset"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF"}, "read": {sym("wMusicFrequencyOffset"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"}, "read": {sym("wMusicFrequencyOffset"): 1}},
    {"c": 2, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicFrequencyOffset") + 2: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"},
         read={sym("wMusicFrequencyOffset") + 1: 1}),
]
# <<< factory Music1_frequency_offset

# >>> factory Music1_volume
CONTRACT["Music1_volume"] = {"compare": (), "preserve": ()}
CASES["Music1_volume"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"}, "read": {sym("wMusicVolume"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"}, "read": {sym("wMusicVolume"): 1}},
    {"c": 2, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicVolume") + 2: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x11\xFF"},
         read={sym("wMusicVolume") + 1: 1}),
]
# <<< factory Music1_volume

# >>> factory Music1_wave
CONTRACT["Music1_wave"] = {"compare": (), "preserve": ()}
CASES["Music1_wave"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x05\xFF", sym("wMusicWave"): b"\x00\x00"},
     "read": {sym("wMusicWave"): 2}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF", sym("wMusicWave"): b"\xFF\xFF"},
     "read": {sym("wMusicWave"): 2}},
    dict(POISON, b=0, c=2, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF", sym("wMusicWave"): b"\x00\x00"}, read={sym("wMusicWave"): 2}),
]
# <<< factory Music1_wave

# >>> factory Music1_cutoff
CONTRACT["Music1_cutoff"] = {"compare": (), "preserve": ()}
CASES["Music1_cutoff"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF"}, "read": {sym("wMusicCutoff"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"}, "read": {sym("wMusicCutoff"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicCutoff") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"},
         read={sym("wMusicCutoff") + 1: 1}),
]
# <<< factory Music1_cutoff

# >>> factory Music1_echo
CONTRACT["Music1_echo"] = {"compare": (), "preserve": ()}
CASES["Music1_echo"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF"}, "read": {sym("wMusicEcho"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"}, "read": {sym("wMusicEcho"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicEcho") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"},
         read={sym("wMusicEcho") + 1: 1}),
]
# <<< factory Music1_echo

# >>> factory Music1_vibrato_type
CONTRACT["Music1_vibrato_type"] = {"compare": (), "preserve": ()}
CASES["Music1_vibrato_type"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF"},
     "read": {sym("wMusicVibratoType"): 1, sym("wMusicVibratoType2"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"},
     "read": {sym("wMusicVibratoType"): 1, sym("wMusicVibratoType2"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"},
     "read": {sym("wMusicVibratoType") + 3: 1, sym("wMusicVibratoType2") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"},
         read={sym("wMusicVibratoType") + 1: 1, sym("wMusicVibratoType2") + 1: 1}),
]
# <<< factory Music1_vibrato_type

# >>> factory Music1_vibrato_delay
CONTRACT["Music1_vibrato_delay"] = {"compare": (), "preserve": ()}
CASES["Music1_vibrato_delay"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF"}, "read": {sym("wMusicVibratoDelay"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF"}, "read": {sym("wMusicVibratoDelay"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF"}, "read": {sym("wMusicVibratoDelay") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF"},
         read={sym("wMusicVibratoDelay") + 1: 1}),
]
# <<< factory Music1_vibrato_delay

# >>> factory Music1_pitch_offset
CONTRACT["Music1_pitch_offset"] = {"compare": (), "preserve": ()}
CASES["Music1_pitch_offset"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x40\xFF", sym("wMusicPitchOffset"): b"\x00"},
     "read": {sym("wMusicPitchOffset"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF", sym("wMusicPitchOffset"): b"\xAA"},
     "read": {sym("wMusicPitchOffset"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF\xFF", sym("wMusicPitchOffset") + 3: b"\x00"},
     "read": {sym("wMusicPitchOffset") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7F\xFF", sym("wMusicPitchOffset") + 1: b"\x11"},
         read={sym("wMusicPitchOffset") + 1: 1}),
]
# <<< factory Music1_pitch_offset

# >>> factory Music1_adjust_pitch_offset
CONTRACT["Music1_adjust_pitch_offset"] = {"compare": (), "preserve": ()}
CASES["Music1_adjust_pitch_offset"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x05\xFF", sym("wMusicPitchOffset"): b"\x10"},
     "read": {sym("wMusicPitchOffset"): 1}},
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x02\xFF", sym("wMusicPitchOffset"): b"\xFF"},
     "read": {sym("wMusicPitchOffset"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x00\xFF", sym("wMusicPitchOffset") + 3: b"\x7F"},
     "read": {sym("wMusicPitchOffset") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x11\xFF", sym("wMusicPitchOffset") + 1: b"\x22"},
         read={sym("wMusicPitchOffset") + 1: 1}),
]
# <<< factory Music1_adjust_pitch_offset

# >>> factory Music1_end
CONTRACT["Music1_end"] = {"compare": (), "preserve": ()}
CASES["Music1_end"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wMusicIsPlaying"): b"\x01"}, "read": {sym("wMusicIsPlaying"): 1}},
    {"c": 3, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wMusicIsPlaying") + 3: b"\xFF"}, "read": {sym("wMusicIsPlaying") + 3: 1}},
    dict(POISON, b=0, c=1, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wMusicIsPlaying") + 1: b"\x7F"},
         read={sym("wMusicIsPlaying") + 1: 1}),
]
# <<< factory Music1_end

# >>> factory Music1_EndLoop
# Exhausted-path cases only: the taken branch's sole observable is where the
# dispatcher resumes, and Music1_PlayNextNote's command mapping is defective
# (see the note above it). Reaching zero pops the frame, which is observable
# through the channel stack pointer without executing any command.
CONTRACT["Music1_EndLoop"] = {"compare": (), "preserve": ()}
CASES["Music1_EndLoop"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicChannelStackPointers"): b"\x03\xC2", sym("wPlayerCardLocations"): b"\x00\xC3\x01"},
     "read": {sym("wMusicChannelStackPointers"): 2, sym("wPlayerCardLocations") + 2: 1}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicChannelStackPointers") + 2: b"\x03\xC2", sym("wPlayerCardLocations"): b"\x00\xC3\x01"},
     "read": {sym("wMusicChannelStackPointers") + 2: 2, sym("wPlayerCardLocations") + 2: 1}},
    dict(POISON, b=0, c=2, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF", sym("wMusicChannelStackPointers") + 4: b"\x13\xC2", sym("wPlayerCardLocations") + 0x10: b"\x00\xC3\x01"},
         read={sym("wMusicChannelStackPointers") + 4: 2, sym("wPlayerCardLocations") + 0x12: 1}),
]
# <<< factory Music1_EndLoop

# >>> factory Music1_octave
# The octave value comes from the command byte in `a` ($D1-$D6), not the stream.
CONTRACT["Music1_octave"] = {"compare": (), "preserve": ()}
CASES["Music1_octave"] = [
    {"a": 0xD1, "c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
     "read": {sym("wMusicOctave"): 1}},
    {"a": 0xD6, "c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
     "read": {sym("wMusicOctave"): 1}},
    {"a": 0xD3, "c": 2, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
     "read": {sym("wMusicOctave") + 2: 1}},
    {"a": 0xD1, "c": 2, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11], "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
     "read": {sym("wMusicOctave") + 2: 1}},
    dict(POISON, a=0xD4, b=0, c=3, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11], wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xFF"},
         read={sym("wMusicOctave") + 3: 1}),
]
# <<< factory Music1_octave

# >>> factory Music1_EndMainLoop
# The only observable is where the dispatcher resumes, so the loop-start points
# at a $E6 (volume, table index 22) command followed by $FF to terminate: the
# volume byte lands only if the resume address was read correctly.
CONTRACT["Music1_EndMainLoop"] = {"compare": (), "preserve": ()}
CASES["Music1_EndMainLoop"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wMusicMainLoopStart"): b"\x10\xC1", sym("wDecompressionSecondaryBufferStart") + 0x21: b"\xE6\x5A\xFF",
              sym("wMusicVolume"): b"\x00\x00\x00\x00", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"},
     "read": {sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wMusicMainLoopStart") + 2: b"\x18\xC1", sym("wDecompressionSecondaryBufferStart") + 0x29: b"\xE6\x77\xFF",
              sym("wMusicVolume"): b"\x00\x00\x00\x00", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"},
     "read": {sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}},
    dict(POISON, b=0, c=0, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wMusicMainLoopStart"): b"\x10\xC1", sym("wDecompressionSecondaryBufferStart") + 0x21: b"\xE6\xA5\xFF",
               sym("wMusicVolume"): b"\xFF\xFF\xFF\xFF", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"},
         read={sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}),
]
# <<< factory Music1_EndMainLoop

# >>> factory Music1_jp
CONTRACT["Music1_jp"] = {"compare": (), "preserve": ()}
CASES["Music1_jp"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x10\xC1", sym("wDecompressionSecondaryBufferStart") + 0x21: b"\xE6\x5A\xFF",
              sym("wMusicVolume"): b"\x00\x00\x00\x00", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"},
     "read": {sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}},
    {"c": 1, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x18\xC1", sym("wDecompressionSecondaryBufferStart") + 0x29: b"\xE6\x77\xFF",
              sym("wMusicVolume"): b"\x00\x00\x00\x00", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"},
     "read": {sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}},
    dict(POISON, b=0, c=0, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x10\xC1", sym("wDecompressionSecondaryBufferStart") + 0x21: b"\xE6\xA5\xFF",
               sym("wMusicVolume"): b"\xFF\xFF\xFF\xFF", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"},
         read={sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}),
]
# <<< factory Music1_jp

# >>> factory Music1_PlayNextNote
# Channel arrives in c; hl is the stream pointer, read with `ld a,[hli]`.
# Every stream ends in $FF (index 47 -> end) so the dispatcher loop terminates.
# Case 6 uses $DA, which is index 10 -> end: the pre-2026-08-26 mapping ran an
# inc_octave there instead, so that case pins the table alignment.
_PNN_IDLE = {sym("wMusicIsPlaying"): b"\x01\x01\x01\x01"}
# A cmd below $D0 is a note: high nibble selects the instrument, low nibble the
# duration index. Its operand byte is peeked, never consumed, so the stream
# pointer stored to wMusicChannelPointers is the operand's own address.
_NOTE_SEED = {sym("wMusicSpeed"): b"\x03\x03\x03\x03", sym("wMusicTie"): b"\x00\x00\x00\x00",
              sym("wMusicCutoff"): b"\x08\x08\x08\x08", sym("wMusicOctave"): b"\x00\x00\x00\x00",
              sym("wMusicPitchOffset"): b"\x00\x00\x00\x00", sym("wMusicFrequencyOffset"): b"\x00\x00\x00\x00",
              sym("wMusicVibratoType2"): b"\x11\x22\x33\x44"}
_NOTE_READ = {sym("wMusicStereoPanning"): 1, sym("wMusicTie"): 4, sym("wMusicChannelPointers"): 8, sym("wMusicCh1CurPitch"): 8, sym("wddab"): 4,
              sym("wddb7"): 4, sym("wddbb"): 4, sym("wddc3"): 4, sym("wMusicVibratoType"): 4, sym("wdddb"): 4,
              sym("wdde3"): 4, sym("wdded"): 2, sym("wddef"): 1}
CONTRACT["Music1_PlayNextNote"] = {"compare": (), "preserve": ()}
CASES["Music1_PlayNextNote"] = [
    # $D0 speed
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD0\x2A\xFF", sym("wMusicSpeed"): b"\x00\x00\x00\x00"},
     "read": {sym("wMusicSpeed"): 4, sym("wMusicIsPlaying"): 4}},
    # $D3 octave: (cmd & 7) - 1
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD3\xFF", sym("wMusicOctave"): b"\x00\x00\x00\x00"},
     "read": {sym("wMusicOctave"): 4, sym("wMusicIsPlaying"): 4}},
    # $D3 octave on channel 2, which gets the decrement back
    {"c": 2, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD3\xFF", sym("wMusicOctave"): b"\x00\x00\x00\x00"},
     "read": {sym("wMusicOctave"): 4, sym("wMusicIsPlaying"): 4}},
    # $D7 inc_octave
    {"c": 1, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD7\xFF", sym("wMusicOctave"): b"\x05\x05\x05\x05"},
     "read": {sym("wMusicOctave"): 4, sym("wMusicIsPlaying"): 4}},
    # $D8 dec_octave
    {"c": 1, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD8\xFF", sym("wMusicOctave"): b"\x05\x05\x05\x05"},
     "read": {sym("wMusicOctave"): 4, sym("wMusicIsPlaying"): 4}},
    # $D9 tie
    {"c": 3, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD9\xFF", sym("wMusicTie"): b"\x00\x00\x00\x00"},
     "read": {sym("wMusicTie"): 4, sym("wMusicIsPlaying"): 4}},
    # $DA end
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xDA", sym("wMusicOctave"): b"\x07\x07\x07\x07"},
     "read": {sym("wMusicIsPlaying"): 4, sym("wMusicOctave"): 4}},
    # $DC stereo_panning, rotated once for channel 1
    {"c": 1, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xDC\x35\xFF", sym("wMusicStereoPanning"): b"\x00"},
     "read": {sym("wMusicStereoPanning"): 1, sym("wMusicIsPlaying"): 4}},
    # $DD MainLoop records the byte before the continuation
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xDD\xFF",
                                sym("wMusicMainLoopStart"): b"\x00\x00\x00\x00\x00\x00\x00\x00"},
     "read": {sym("wMusicMainLoopStart"): 8, sym("wMusicIsPlaying"): 4}},
    # every one-operand writer in a single stream
    {"c": 2, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, 
         sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xE4\x11\xE5\xC3\xE6\x5A\xE7\x77\xE8\x33\xE9\x22"
                 b"\xEA\x44\xEB\x66\xEC\x88\xED\x02\xFF"},
     "read": {sym("wMusicDuty1"): 4, sym("wMusicWave"): 1, sym("wMusicWaveChange"): 1, sym("wMusicIsPlaying"): 4, sym("wMusicCutoff"): 4,
              sym("wMusicEcho"): 4, sym("wMusicPitchOffset"): 4, sym("wMusicVibratoType"): 4, sym("wMusicVibratoType2"): 4, sym("wMusicVibratoDelay"): 4,
              sym("wMusicVolume"): 4, sym("wMusicFrequencyOffset"): 4}},
    dict(POISON, b=0, c=1, hl=sym("wDecompressionSecondaryBufferStart") + 0x11,
         wram={**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD0\x2A\xE6\x5A\xFF",
                                 sym("wMusicSpeed"): b"\xFF\xFF\xFF\xFF",
                                 sym("wMusicVolume"): b"\xFF\xFF\xFF\xFF"},
         read={sym("wMusicSpeed"): 4, sym("wMusicVolume"): 4, sym("wMusicIsPlaying"): 4}),
    # instrument 0 takes neither lookup but still stores the stream pointer
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x05\x40"},
     "read": _NOTE_READ},
    # pitch lookup with a non-zero octave and pitch offset
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\x40",
              sym("wMusicOctave"): b"\x02\x02\x02\x02", sym("wMusicPitchOffset"): b"\x01\x01\x01\x01"},
     "read": _NOTE_READ},
    # operand $D9 skips the cutoff scaling, so cutoff 2 must not be applied
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\xD9",
              sym("wMusicCutoff"): b"\x02\x02\x02\x02"},
     "read": _NOTE_READ},
    # cutoff 0 is not a skip: the counter wraps to 256 additions
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\x40",
              sym("wMusicCutoff"): b"\x00\x00\x00\x00"},
     "read": _NOTE_READ},
    # cutoff above 8 also scales
    {"c": 1, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\x40",
              sym("wMusicCutoff"): b"\x09\x09\x09\x09", sym("wMusicOctave"): b"\x01\x01\x01\x01"},
     "read": _NOTE_READ},
    # channel 3 takes the noise-instrument table
    {"c": 3, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\x40",
              sym("wMusicOctave"): b"\x01\x01\x01\x01", sym("wMusicStereoPanning"): b"\x00"},
     "read": _NOTE_READ},
    # a tie already latched at $80 skips the vibrato/flag reset
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\x40",
              sym("wMusicTie"): b"\x80\x80\x80\x80"},
     "read": _NOTE_READ},
    # a negative frequency offset subtracts ~fo rather than negating it
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x35\x40",
              sym("wMusicFrequencyOffset"): b"\x80\x80\x80\x80"},
     "read": _NOTE_READ},
    dict(POISON, b=0, c=2, hl=sym("wDecompressionSecondaryBufferStart") + 0x11,
         wram={**_PNN_IDLE, **_NOTE_SEED, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\x7A\x40",
               sym("wMusicOctave"): b"\x03\x03\x03\x03"},
         read=_NOTE_READ),
    # $E2 call pushes the raw operand address, not operand+2
    # (music1.asm:976-992: the popped stream pointer is stored unmodified,
    # before it is used to read the 2-byte target).
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xE2\x00\xC2", sym("wPlayerCardLocations"): b"\xFF",
              sym("wMusicChannelStackPointers"): b"\x00\xC3"},
     "read": {sym("wOpponentCardLocations"): 2}},
    dict(POISON, b=0, c=1, hl=sym("wDecompressionSecondaryBufferStart") + 0x21,
         wram={**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x21: b"\xE2\x00\xC2", sym("wPlayerCardLocations"): b"\xFF",
               sym("wMusicChannelStackPointers") + 2: b"\x00\xC3"},
         read={sym("wOpponentCardLocations"): 2}),
    # $E3 ret resumes at the popped stack value + 2, not the raw value
    # (music1.asm:994-1005 `inc de` twice after the pop): landing on $DA
    # (end) at the +2 target rather than $D7 (inc_octave) at the raw one.
    {"c": 0, "hl": sym("wDecompressionSecondaryBufferStart") + 0x11,
     "wram": {**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xE3", sym("wMusicOctave"): b"\x05\x05\x05\x05",
              sym("wMusicChannelStackPointers"): b"\x00\xC3", sym("wPlayerArenaCardLastTurnEffect") + 6: b"\x50\xC1",
              sym("wDecompressionSecondaryBufferStart") + 0x61: b"\xD7\xFF", sym("wDecompressionSecondaryBufferStart") + 0x63: b"\xDA"}},
    dict(POISON, b=0, c=1, hl=sym("wDecompressionSecondaryBufferStart") + 0x11,
         wram={**_PNN_IDLE, sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xE3", sym("wMusicOctave"): b"\x05\x05\x05\x05",
               sym("wMusicChannelStackPointers") + 2: b"\x00\xC3", sym("wPlayerArenaCardLastTurnEffect") + 6: b"\x50\xC1",
               sym("wDecompressionSecondaryBufferStart") + 0x61: b"\xD7\xFF", sym("wDecompressionSecondaryBufferStart") + 0x63: b"\xDA"}),
]
# <<< factory Music1_PlayNextNote

# >>> factory Music1_note
# music1.asm:648 is reached by `jr c` from the dispatcher, which has already
# done `ld a,[hli]` / `push hl` / `push af`. The runner pushes `stack` in list
# order, so the deepest word comes first: [advanced_stream_ptr, command_word].
# `pop af` (asm:732) takes the command word's high byte as the instrument
# nibble, and `pop de` (asm:833) takes the stream pointer that the common exit
# stores to wMusicChannelPointers.
CONTRACT["Music1_note"] = {"compare": (), "preserve": ()}
CASES["Music1_note"] = [
    {"a": 0x05, "b": 0, "c": 0, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x0500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40"}, "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 0, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40",
              sym("wMusicOctave"): b"\x02\x02\x02\x02", sym("wMusicPitchOffset"): b"\x01\x01\x01\x01"},
     "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 0, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\xD9", sym("wMusicCutoff"): b"\x02\x02\x02\x02"},
     "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 0, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40", sym("wMusicCutoff"): b"\x00\x00\x00\x00"},
     "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 1, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40", sym("wMusicCutoff"): b"\x09\x09\x09\x09",
              sym("wMusicOctave"): b"\x01\x01\x01\x01"},
     "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 3, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40",
              sym("wMusicOctave"): b"\x01\x01\x01\x01", sym("wMusicStereoPanning"): b"\x00"},
     "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 0, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40", sym("wMusicTie"): b"\x80\x80\x80\x80"},
     "read": _NOTE_READ},
    {"a": 0x35, "b": 0, "c": 0, "hl": sym("wPlayerCardLocations"), "stack": [sym("wPlayerCardLocations"), 0x3500],
     "wram": {**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40", sym("wMusicFrequencyOffset"): b"\x80\x80\x80\x80"},
     "read": _NOTE_READ},
    dict(POISON, a=0x7A, b=0, c=2, hl=sym("wPlayerCardLocations"), stack=[sym("wPlayerCardLocations"), 0x7A00],
         wram={**_NOTE_SEED, sym("wPlayerCardLocations"): b"\x40", sym("wMusicOctave"): b"\x03\x03\x03\x03"},
         read=_NOTE_READ),
]
# <<< factory Music1_note

# >>> factory Music1_PlayNextNote_pop
CONTRACT["Music1_PlayNextNote_pop"] = {"compare": (), "preserve": ()}
CASES["Music1_PlayNextNote_pop"] = [
    {"c": 0, "stack": [sym("wDecompressionSecondaryBufferStart") + 0x11],
     "wram": {sym("wDecompressionSecondaryBufferStart") + 0x11: b"\xD0\x2A\xFF", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01",
              sym("wMusicSpeed"): b"\x00\x00\x00\x00"},
     "read": {sym("wMusicSpeed"): 4, sym("wMusicIsPlaying"): 4}},
    {"c": 1, "stack": [sym("wPlayerCardLocations")],
     "wram": {sym("wPlayerCardLocations"): b"\xD0\x35\xFF", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01",
              sym("wMusicSpeed"): b"\x00\x00\x00\x00"},
     "read": {sym("wMusicSpeed"): 4, sym("wMusicIsPlaying"): 4}},
    dict(POISON, b=0, c=0, stack=[sym("wOpponentCardLocations")],
         wram={sym("wOpponentCardLocations"): b"\xD0\x2A\xFF", sym("wMusicIsPlaying"): b"\x01\x01\x01\x01",
               sym("wMusicSpeed"): b"\xFF\xFF\xFF\xFF"},
         read={sym("wMusicSpeed"): 4, sym("wMusicIsPlaying"): 4}),
]
# <<< factory Music1_PlayNextNote_pop

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
# >>> factory-mutation Music1_EndLoop
MUTATIONS["Music1_EndLoop"] = {"source_symbol": "Music1_EndLoop", "before": "\t\tMusic1_SetChannelStackPointer(ch, (uint16_t)(sp - 3u));", "after": "\t\tMusic1_SetChannelStackPointer(ch, (uint16_t)(sp - 2u));", "case_ids": ["Music1_EndLoop-0", "Music1_EndLoop-1"]}
# <<< factory-mutation Music1_EndLoop
# >>> factory-mutation Music1_octave
MUTATIONS["Music1_octave"] = {"source_symbol": "Music1_octave", "before": "\tif (ch == 2u)", "after": "\tif (ch == 3u)", "case_ids": ["Music1_octave-2", "Music1_octave-3"]}
# <<< factory-mutation Music1_octave
# >>> factory-mutation Music1_EndMainLoop
MUTATIONS["Music1_EndMainLoop"] = {"source_symbol": "Music1_EndMainLoop", "before": "void Music1_EndMainLoop(uint16_t caller_stream, uint8_t ch)\n{\n\t(void)caller_stream;\n\tuint16_t addr = (uint16_t)(wMusicMainLoopStart_ADDR + (uint16_t)ch * 2u);", "after": "void Music1_EndMainLoop(uint16_t caller_stream, uint8_t ch)\n{\n\t(void)caller_stream;\n\tuint16_t addr = (uint16_t)(wMusicMainLoopStart_ADDR + (uint16_t)ch * 2u + 1u);", "case_ids": ["Music1_EndMainLoop-0", "Music1_EndMainLoop-1"]}
# <<< factory-mutation Music1_EndMainLoop
# >>> factory-mutation Music1_jp
MUTATIONS["Music1_jp"] = {"source_symbol": "Music1_jp", "before": "void Music1_jp(uint16_t caller_stream, uint8_t ch)\n{\n\tuint16_t hl = (uint16_t)(gb_read8(caller_stream)", "after": "void Music1_jp(uint16_t caller_stream, uint8_t ch)\n{\n\tuint16_t hl = (uint16_t)(gb_read8((uint16_t)(caller_stream + 1u))", "case_ids": ["Music1_jp-0", "Music1_jp-1"]}
# <<< factory-mutation Music1_jp
# >>> factory-mutation Music1_PlayNextNote
MUTATIONS["Music1_PlayNextNote"] = {"source_symbol": "Music1_PlayNextNote", "before": "\t\t\twMusicSpeed_PTR[ch] = gb_read8((*hl)++);", "after": "\t\t\twMusicSpeed_PTR[ch] = (uint8_t)(gb_read8((*hl)++) + 1u);", "case_ids": ["Music1_PlayNextNote-0", "Music1_PlayNextNote-10"]}
# <<< factory-mutation Music1_PlayNextNote
# >>> factory-mutation Music1_PlayNextNote_pop
MUTATIONS["Music1_PlayNextNote_pop"] = {"source_symbol": "Music1_PlayNextNote_pop", "before": "void Music1_PlayNextNote_pop(uint16_t caller_stream, uint8_t ch)\n{\n\tuint16_t hl = caller_stream;\n\tMusic1_PlayNextNote(&hl, ch);", "after": "void Music1_PlayNextNote_pop(uint16_t caller_stream, uint8_t ch)\n{\n\tuint16_t hl = caller_stream;\n\tMusic1_PlayNextNote(&hl, (uint8_t)(ch + 1u));", "case_ids": ["Music1_PlayNextNote_pop-0", "Music1_PlayNextNote_pop-2"]}
# <<< factory-mutation Music1_PlayNextNote_pop
# >>> factory-mutation Music1_note
MUTATIONS["Music1_note"] = {"source_symbol": "Music1_note", "before": "void Music1_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch)\n{\n\t(void)instrument;\n\tpnn_note(hl, note, ch);", "after": "void Music1_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch)\n{\n\t(void)instrument;\n\tpnn_note(hl, (uint8_t)(note ^ 0x01u), ch);", "case_ids": ["Music1_note-1", "Music1_note-3"]}
# <<< factory-mutation Music1_note
MUTATIONS["Music1_UpdateVibrato"] = {"source_symbol": "Music1_UpdateVibrato", "before": "\t\treturn (uint16_t)((uint16_t)(hi & 0x07u) << 8 | lo);", "after": "\t\treturn (uint16_t)((uint16_t)(hi & 0x0Fu) << 8 | lo);", "case_ids": ["Music1_UpdateVibrato-6"]}
MUTATIONS["Music1_f479c"] = {"source_symbol": "Music1_f479c", "before": "\t\t\twMusicTie_PTR[0] = 0;\n\t\t\tgb_write8(APU_AUD3ENA, 0);", "after": "\t\t\twMusicTie_PTR[2] = 0;\n\t\t\tgb_write8(APU_AUD3ENA, 0);", "case_ids": ["Music1_f479c-1"]}
MUTATIONS["Music1_CheckForNewSound"] = {"source_symbol": "Music1_CheckForNewSound", "before": "\t\twCurSongID = (uint8_t)(wCurSongID | 0x80u);", "after": "\t\twCurSongID = (uint8_t)(wCurSongID | 0x40u);", "case_ids": ["Music1_CheckForNewSound-1"]}
for _rec in SCHEMA2_CASES["Music1_BackupSong"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongIDBackup"): 1, sym("wCurSongBankBackup"): 1, sym("wMusicStereoPanningBackup"): 1, sym("wMusicWaveBackup"): 1, sym("wMusicWaveChangeBackup"): 1, sym("wde76"): 1, sym("wde77"): 1, sym("wdeac"): 1})
for _rec in SCHEMA2_CASES["Music1_LoadBackup"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 1, sym("wCurSongBank"): 1, sym("wMusicStereoPanning"): 1, sym("wMusicWave"): 1, sym("wMusicWaveChange"): 1, sym("wddab"): 1, sym("wddac"): 1, sym("wddef"): 1})
for _rec in SCHEMA2_CASES["Music1_f404e"]:
    _rec.setdefault("bus", {}).update({sym("wddf0"): 1})
for _rec in SCHEMA2_CASES["Music1_f4066"]:
    _rec.setdefault("bus", {}).update({sym("wddf2"): 1})
for _rec in SCHEMA2_CASES["Music1_f480a"]:
    _rec.setdefault("bus", {}).update({sym("wddef"): 1})
for _rec in SCHEMA2_CASES["Music1_f485a"]:
    _rec.setdefault("bus", {}).update({sym("wMusicVibratoDelay"): 1, sym("wMusicVibratoDelay") + 1: 1, sym("wMusicVibratoDelay") + 2: 1})
for _rec in SCHEMA2_CASES["Music1_f490b"]:
    _rec.setdefault("bus", {}).update({sym("wMusicVibratoDelay"): 1, sym("wMusicVibratoDelay") + 1: 1, sym("wMusicVibratoDelay") + 2: 1})
for _rec in SCHEMA2_CASES["Music1_BackupSong"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_EmptyFunc"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_LoadBackup"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_UpdateChannel1"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_UpdateChannel2"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_UpdateChannel3"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_UpdateChannel4"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f404e"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f4066"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f4714"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f475a"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f480a"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f485a"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f4866"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f490b"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
for _rec in SCHEMA2_CASES["Music1_f4980"]:
    _rec.setdefault("bus", {}).update({sym("wCurSongID"): 0x165})
MUTATIONS["Music1_AssertSFXFinished"] = {
    "source_symbol": "Music1_AssertSFXFinished",
    "before": "\treturn (wCurSfxID != 0x80) ? 1 : 0;",
    "after": "\treturn (wCurSfxID == 0x80) ? 1 : 0;",
    "case_ids": ["Music1_AssertSFXFinished-0"],
}
MUTATIONS["Music1_AssertSongFinished"] = {
    "source_symbol": "Music1_AssertSongFinished",
    "before": "\treturn (wCurSongID != 0x80) ? 1 : 0;",
    "after": "\treturn (wCurSongID == 0x80) ? 1 : 0;",
    "case_ids": ["Music1_AssertSongFinished-0"],
}
MUTATIONS["Music1_BeginSong"] = {
    "source_symbol": "Music1_BeginSong",
    "before": "\tbank = gb_read8(ADR_SongBanks1 + a);",
    "after": "\tbank = gb_read8(ADR_SongBanks1 - a);",
    "case_ids": ["Music1_BeginSong-1"],
}
MUTATIONS["Music1_CheckForEndOfSong"] = {
    "source_symbol": "Music1_CheckForEndOfSong",
    "before": "\tif (sum == 0) wCurSongID = 0x80;",
    "after": "\tif (sum != 0) wCurSongID = 0x80;",
    "case_ids": ["Music1_CheckForEndOfSong-1"],
}
MUTATIONS["Music1_Init"] = {
    "source_symbol": "Music1_Init",
    "before": "\t\tgb_write8(wMusicChannelStackPointers_ADDR + i,",
    "after": "\t\tgb_write8(wMusicChannelStackPointers_ADDR - i,",
    "case_ids": ["Music1_Init-0"],
}
MUTATIONS["Music1_PlaySFX"] = {
    "source_symbol": "Music1_PlaySFX",
    "before": "\tif (a != 0u) {",
    "after": "\tif (a == 0u) {",
    "case_ids": ["Music1_PlaySFX-1"],
}
MUTATIONS["Music1_PlaySong"] = {
    "source_symbol": "Music1_PlaySong",
    "before": "\tif (a >= gb_read8(ADR_NumberOfSongs1)) return;",
    "after": "\tif (a > gb_read8(ADR_NumberOfSongs1)) return;",
    "case_ids": ["Music1_PlaySong-2"],
}
MUTATIONS["Music1_ResumeSong"] = {
    "source_symbol": "Music1_ResumeSong",
    "before": "\tMusic1_LoadBackup();",
    "after": "\t;",
    "case_ids": ["Music1_ResumeSong-1"],
}
MUTATIONS["Music1_SetChannelStackPointer"] = {
    "source_symbol": "Music1_SetChannelStackPointer",
    "before": "\tgb_write8(addr + 1, (uint8_t)(sp >> 8));",
    "after": "\tgb_write8(addr - 1, (uint8_t)(sp >> 8));",
    "case_ids": ["Music1_SetChannelStackPointer-0"],
}
MUTATIONS["Music1_Update"] = {
    "source_symbol": "Music1_Update",
    "before": "\t\tif (wddf2 != 0) {",
    "after": "\t\tif (wddf2 == 0) {",
    "case_ids": ["Music1_Update-3"],
}
MUTATIONS["Music1_f406f"] = {
    "source_symbol": "Music1_f406f",
    "before": "\tuint8_t lo = a & 0x07;",
    "after": "\tuint8_t lo = a | 0x07;",
    "case_ids": ["Music1_f406f-0"],
}
MUTATIONS["Music1_f4839"] = {
    "source_symbol": "Music1_f4839",
    "before": "\t\tif (v == 0xFF) {",
    "after": "\t\tif (v != 0xFF) {",
    "case_ids": ["Music1_f4839-1"],
}
MUTATIONS["Music1_f4967"] = {
    "source_symbol": "Music1_f4967",
    "before": "\tde = (uint16_t)wMusicCh1CurPitch_PTR[ch * 2 + 1] << 8",
    "after": "\tde = (uint16_t)wMusicCh1CurPitch_PTR[ch * 2 - 1] << 8",
    "case_ids": ["Music1_f4967-2"],
}
MUTATIONS["Music1_GetChannelStackPointer"] = {
    "source_symbol": "Music1_GetChannelStackPointer",
    "before": "uint16_t Music1_GetChannelStackPointer(uint8_t ch)\n{\n\tuint16_t addr = wMusicChannelStackPointers_ADDR + ((uint16_t)ch << 1);",
    "after": "uint16_t Music1_GetChannelStackPointer(uint8_t ch)\n{\n\tuint16_t addr = wMusicChannelStackPointers_ADDR - ((uint16_t)ch << 1);",
    "case_ids": ["Music1_GetChannelStackPointer-1"],
}
MUTATIONS["Music1_LoadWaveInstrument"] = {
    "source_symbol": "Music1_LoadWaveInstrument",
    "before": "\t}\n\twMusicWaveChange = 0;",
    "after": "\t}\n\twMusicWaveChange = (0) ^ 1u;",
    "case_ids": ["Music1_LoadWaveInstrument-0"],
}
MUTATIONS["Music1_PauseSong"] = {
    "source_symbol": "Music1_PauseSong",
    "before": "\tMusic1_BackupSong();\n\tMusic1_StopAllChannels();",
    "after": "\tMusic1_BackupSong();\n\t;",
    "case_ids": ["Music1_PauseSong-1"],
}
MUTATIONS["Music1_StopAllChannels"] = {
    "source_symbol": "Music1_StopAllChannels",
    "before": "\twMusicIsPlaying_PTR[0] = 0;",
    "after": "\twMusicIsPlaying_PTR[0] = (0) ^ 1u;",
    "case_ids": ["Music1_StopAllChannels-0"],
}
MUTATIONS["Music1_UpdateChannel1"] = {
    "source_symbol": "Music1_UpdateChannel1",
    "before": "void Music1_UpdateChannel1(void) { g_rom_bank = MUSIC1_BANK; update_channel(0); }",
    "after": "void Music1_UpdateChannel1(void) { g_rom_bank = MUSIC1_BANK; update_channel(1); }",
    "case_ids": ["Music1_UpdateChannel1-1"],
}
MUTATIONS["Music1_UpdateChannel2"] = {
    "source_symbol": "Music1_UpdateChannel2",
    "before": "void Music1_UpdateChannel2(void) { g_rom_bank = MUSIC1_BANK; update_channel(1); }",
    "after": "void Music1_UpdateChannel2(void) { g_rom_bank = MUSIC1_BANK; update_channel(2); }",
    "case_ids": ["Music1_UpdateChannel2-1"],
}
MUTATIONS["Music1_UpdateChannel3"] = {
    "source_symbol": "Music1_UpdateChannel3",
    "before": "void Music1_UpdateChannel3(void) { g_rom_bank = MUSIC1_BANK; update_channel(2); }",
    "after": "void Music1_UpdateChannel3(void) { g_rom_bank = MUSIC1_BANK; update_channel(3); }",
    "case_ids": ["Music1_UpdateChannel3-1"],
}
MUTATIONS["Music1_UpdateChannel4"] = {
    "source_symbol": "Music1_UpdateChannel4",
    "before": "void Music1_UpdateChannel4(void) { g_rom_bank = MUSIC1_BANK; update_channel(3); }",
    "after": "void Music1_UpdateChannel4(void) { g_rom_bank = MUSIC1_BANK; update_channel(4); }",
    "case_ids": ["Music1_UpdateChannel4-1"],
}
MUTATIONS["Music1_f4714"] = {
    "source_symbol": "Music1_f4714",
    "before": "void Music1_f4714(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(0); }",
    "after": "void Music1_f4714(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(1); }",
    "case_ids": ["Music1_f4714-2"],
}
MUTATIONS["Music1_f475a"] = {
    "source_symbol": "Music1_f475a",
    "before": "void Music1_f475a(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(1); }",
    "after": "void Music1_f475a(void) { g_rom_bank = MUSIC1_BANK; update_ch_output(2); }",
    "case_ids": ["Music1_f475a-2"],
}
MUTATIONS["Music1_f404e"] = {
    "source_symbol": "Music1_f404e",
    "before": "void Music1_f404e(uint8_t a)         { g_rom_bank = MUSIC1_BANK; wddf0 = a; }",
    "after": "void Music1_f404e(uint8_t a)         { g_rom_bank = MUSIC1_BANK; wddf0 = (a) ^ 1u; }",
    "case_ids": ["Music1_f404e-0"],
}
MUTATIONS["Music1_f4066"] = {
    "source_symbol": "Music1_f4066",
    "before": "void Music1_f4066(void)              { g_rom_bank = MUSIC1_BANK; wddf2 ^= 1; }",
    "after": "void Music1_f4066(void)              { g_rom_bank = MUSIC1_BANK; wddf2 ^= (1) ^ 1u; }",
    "case_ids": ["Music1_f4066-0"],
}
for _rec in SCHEMA2_CASES["Music1_BackupSong"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_BackupSong"] = {
    "source_symbol": "Music1_BackupSong",
    "before": "void Music1_BackupSong(void)\n{",
    "after": "void Music1_BackupSong(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_BackupSong-0"],
}
for _rec in SCHEMA2_CASES["Music1_LoadBackup"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_LoadBackup"] = {
    "source_symbol": "Music1_LoadBackup",
    "before": "void Music1_LoadBackup(void)\n{",
    "after": "void Music1_LoadBackup(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_LoadBackup-0"],
}
for _rec in SCHEMA2_CASES["Music1_f480a"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_f480a"] = {
    "source_symbol": "Music1_f480a",
    "before": "void Music1_f480a(void)\n{",
    "after": "void Music1_f480a(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_f480a-0"],
}
for _rec in SCHEMA2_CASES["Music1_f485a"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_f485a"] = {
    "source_symbol": "Music1_f485a",
    "before": "void Music1_f485a(uint8_t ch)\n{",
    "after": "void Music1_f485a(uint8_t ch)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_f485a-0"],
}
for _rec in SCHEMA2_CASES["Music1_f4866"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_f4866"] = {
    "source_symbol": "Music1_f4866",
    "before": "void Music1_f4866(void)\n{",
    "after": "void Music1_f4866(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_f4866-0"],
}
for _rec in SCHEMA2_CASES["Music1_f490b"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_f490b"] = {
    "source_symbol": "Music1_f490b",
    "before": "void Music1_f490b(uint8_t ch, uint16_t de)\n{",
    "after": "void Music1_f490b(uint8_t ch, uint16_t de)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_f490b-0"],
}
for _rec in SCHEMA2_CASES["Music1_f4980"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_f4980"] = {
    "source_symbol": "Music1_f4980",
    "before": "void Music1_f4980(void)\n{",
    "after": "void Music1_f4980(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);",
    "case_ids": ["Music1_f4980-0"],
}
for _rec in SCHEMA2_CASES["Music1_EmptyFunc"]:
    _rec.setdefault("bus", {}).update({STACK_CANARY: 1})
MUTATIONS["Music1_EmptyFunc"] = {
    "source_symbol": "Music1_EmptyFunc",
    "before": "void Music1_EmptyFunc(void)          { g_rom_bank = MUSIC1_BANK; }",
    "after": "void Music1_EmptyFunc(void)          { gb_write8(0xdff0u, 0xFFu); g_rom_bank = MUSIC1_BANK; }",
    "case_ids": ["Music1_EmptyFunc-0"],
}
