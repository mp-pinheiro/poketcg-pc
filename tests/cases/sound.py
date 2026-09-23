"""Oracle-diff cases for poketcg/src/home/sound.asm's tile-plane converters.

Func_37c5 processes exactly 768 source bytes (8x6x8x2) and touches roughly
3266 bytes of destination (de sweeps ~3072 bytes, plus the +$c0/+$c2 write
offsets ahead of it), so every case reads a wide `sread` window. Destinations
sit in SRAM (the real caller, engine/link/printer.asm, targets sGfxBuffer2 =
$a800) so there is no reserved-WRAM collision to worry about. Source `hl`
points into the default-active ROM bank 1 ($4000-$7fff); the routine never
bank-switches itself, so both sides read the same real ROM bytes there.
"""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

SREAD_LEN = 3280

CONTRACT = {
    "Func_37c5": {"compare": ("a", "d", "e", "hl"), "preserve": ()},
    "Func_37a5": {"compare": ("a", "f", "d", "e", "hl"), "preserve": ("f",)},
}

CASES = {
    "Func_37c5": [
        # All-zero: carry_in clear (f=0), a=0.
        {"hl": 0x4000, "d": 0xA8, "e": 0x00, "ramg": True,
         "sread": {0: {0xA800: SREAD_LEN}}},
        # Same source/dest, carry_in SET this time -- proves the entry carry
        # (undocumented but real, threaded with no reset anywhere in the
        # routine) actually reaches the computed tile data.
        {"hl": 0x4000, "d": 0xAC, "e": 0x00, "f": 0x10, "ramg": True,
         "sread": {0: {0xAC00: SREAD_LEN}}},
        # Different source region and a nonzero starting accumulator.
        {"hl": 0x4200, "d": 0xB0, "e": 0x00, "a": 0x5A, "ramg": True,
         "sread": {0: {0xB000: SREAD_LEN}}},
        dict(POISON, hl=0x4100, d=0xA8, e=0x00, ramg=True,
             sread={0: {0xA800: SREAD_LEN}}),
    ],
    "Func_37a5": [
        # hl's top 3 bits select the CardGraphics bank offset (0 here); the
        # low bits get <<3'd and normalized into $4000-$7fff for Func_37c5.
        {"hl": 0x02A7, "d": 0xA8, "e": 0x00, "ramg": True,
         "sread": {0: {0xA800: SREAD_LEN}}},
        {"hl": 0x1800, "d": 0xA0, "e": 0x00, "ramg": True,
         "sread": {0: {0xA000: SREAD_LEN}}},
        dict(POISON, hl=0x1234, d=0xA8, e=0x00, ramg=True,
             sread={0: {0xA800: SREAD_LEN}}),
    ],
}

# Audio wrapper CONTRACT + CASES — home/sound.asm farcall trampolines
# Wrappers dissolve to direct C calls into Music1_* routines.
# CONTRACT matches the underlying Music1_* routine.
wCurSongID = 0xDD80

CONTRACT.update({
    "SetupSound": {"compare": (), "preserve": ()},
    "StopMusic": {"compare": ("hl",), "preserve": ("hl",)},
    "PlaySong": {"compare": ("hl",), "preserve": ("hl",)},
    "AssertSongFinished": {"compare": ("a",), "preserve": ()},
    "AssertSFXFinished": {"compare": ("a",), "preserve": ()},
    "PlaySFX_InvalidChoice": {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")},
    "PlaySFX": {"compare": ("b", "c", "hl"), "preserve": ("b", "c", "hl")},
    "PauseSong": {"compare": (), "preserve": ()},
    "ResumeSong": {"compare": (), "preserve": ()},
})

CASES.update({
    "SetupSound": [
        {"read": {wCurSongID: 1}},
        dict(POISON, read={wCurSongID: 1}),
    ],
    "StopMusic": [
        {"read": {wCurSongID: 1}},
    ],
    "PlaySong": [
        {"a": 0, "read": {wCurSongID: 1}},
        {"a": 30, "read": {wCurSongID: 1}},
        dict(POISON, a=15, read={wCurSongID: 1}),
    ],
    "AssertSongFinished": [
        {"wram": {wCurSongID: b"\x80"}},
        {"wram": {wCurSongID: b"\x00"}},
        dict(POISON, wram={wCurSongID: b"\x80"}),
    ],
    "AssertSFXFinished": [
        {"wram": {0xDD82: b"\x80"}},
        {"wram": {0xDD82: b"\x00"}},
        dict(POISON, wram={0xDD82: b"\x80"}),
    ],
    "PlaySFX_InvalidChoice": [
        {"read": {0xDD82: 1, 0xDD83: 1}},
    ],
    "PlaySFX": [
        {"a": 0, "read": {0xDD82: 1, 0xDD83: 1}},
        {"a": 1, "read": {0xDD82: 1, 0xDD83: 1}},
        dict(POISON, a=5, read={0xDD82: 1, 0xDD83: 1}),
    ],
    "PauseSong": [
        {"wram": {wCurSongID: b"\x01"}, "read": {wCurSongID: 1}},
    ],
    "ResumeSong": [
        {"wram": {wCurSongID: b"\x01"}, "read": {wCurSongID: 1}},
    ],
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "Func_37c5": {
        "source_symbol": "Func_37c5",
        "before": "for (uint8_t outer = 0; outer < 8; outer++)",
        "after": "for (uint8_t outer = 0; outer < 7; outer++)",
        "case_ids": ["Func_37c5-0", "Func_37c5-1", "Func_37c5-2", "Func_37c5-3"],
    },
}
for _rec in SCHEMA2_CASES["PauseSong"]:
    _rec.setdefault("bus", {}).update({0xDD80: 0x165})
for _rec in SCHEMA2_CASES["StopMusic"]:
    _rec.setdefault("bus", {}).update({0xDD80: 0x165})
MUTATIONS["Func_37a5"] = {
    "source_symbol": "Func_37a5",
    "before": "\tshifted = (uint16_t)((shifted & (uint16_t)~0x8000u) | 0x4000u);",
    "after": "\tshifted = (uint16_t)((shifted & (uint16_t)~0x7FFFu) | 0x4000u);",
    "case_ids": ["Func_37a5-0"],
}
MUTATIONS["AssertSFXFinished"] = {
    "source_symbol": "AssertSFXFinished",
    "before": "\tuint8_t result = Music1_AssertSFXFinished();\n\n\tBankswitchROM(saved);\n\treturn result;",
    "after": "\tuint8_t result = Music1_AssertSFXFinished();\n\n\tBankswitchROM(saved);\n\treturn 1u + result;",
    "case_ids": ["AssertSFXFinished-0"],
}
MUTATIONS["AssertSongFinished"] = {
    "source_symbol": "AssertSongFinished",
    "before": "\tuint8_t result = Music1_AssertSongFinished();\n\n\tBankswitchROM(saved);\n\treturn result;",
    "after": "\tuint8_t result = Music1_AssertSongFinished();\n\n\tBankswitchROM(saved);\n\treturn 1u + result;",
    "case_ids": ["AssertSongFinished-0"],
}
MUTATIONS["PlaySFX"] = {
    "source_symbol": "PlaySFX",
    "before": "\tMusic1_PlaySFX(a);",
    "after": "\t;",
    "case_ids": ["PlaySFX-1"],
}
MUTATIONS["PlaySFX_InvalidChoice"] = {
    "source_symbol": "PlaySFX_InvalidChoice",
    "before": "\tPlaySFX(SFX_DENIED);",
    "after": "\t;",
    "case_ids": ["PlaySFX_InvalidChoice-0"],
}
MUTATIONS["PlaySong"] = {
    "source_symbol": "PlaySong",
    "before": "\tMusic1_PlaySong(a);",
    "after": "\t;",
    "case_ids": ["PlaySong-1"],
}
MUTATIONS["ResumeSong"] = {
    "source_symbol": "ResumeSong",
    "before": "\tMusic1_ResumeSong();",
    "after": "\t;",
    "case_ids": ["ResumeSong-0"],
}
MUTATIONS["SetupSound"] = {
    "source_symbol": "SetupSound",
    "before": "\tMusic1_Init();",
    "after": "\t;",
    "case_ids": ["SetupSound-0"],
}
MUTATIONS["PauseSong"] = {
    "source_symbol": "PauseSong",
    "before": "\tMusic1_PauseSong();",
    "after": "\t;",
    "case_ids": ["PauseSong-0"],
}
MUTATIONS["StopMusic"] = {
    "source_symbol": "StopMusic",
    "before": "\tMusic1_PlaySong(0);",
    "after": "\tMusic1_PlaySong(1);",
    "case_ids": ["StopMusic-0"],
}
