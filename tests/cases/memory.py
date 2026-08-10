"""Oracle-diff cases for poketcg/src/home/memory.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hBankROM = 0xFF80
wDecompSourcePosPtr = 0xCAD6
wTempPointer = 0xD4C4
wTempPointerBank = 0xD4C6
wDecompressionSecondaryBuffer = 0xC000


def decomp_state(src, buf_high=0xC0):
    """The 10 bytes InitDataDecompression leaves at $CAD6 for source pointer `src`."""
    return bytes([src & 0xFF, src >> 8, 1, 0, 0, 0, 0, buf_high, 0, 0xEF])


def banked_src(src, bank):
    """wTempPointer + wTempPointerBank, which are contiguous at $D4C4."""
    return bytes([src & 0xFF, src >> 8, bank])


CONTRACT = {
    # BankswitchROM leaves A as the restored bank; DecompressData clobbers AF.
    "DecompressDataFromBank": {"compare": ("d", "e", "hl"), "preserve": ("d", "e", "hl")},
    # CopyDataHLtoDE_SaveRegisters preserves BC/DE/HL, but clobbers AF.
    "CopyBankedDataToDE": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    # Both fills preserve bc/de/hl. Exit a==0 and F=Z are loop residue.
    "FillMemoryWithA": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "FillMemoryWithDE": {"compare": ("b", "c", "d", "e", "hl"), "preserve": ("b", "c", "d", "e", "hl")},
    "GetFarByte": {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("f", "b", "c", "d", "e", "hl")},
}

CASES = {
    "DecompressDataFromBank": [
        # Closest runnable baseline to all-zero. A literal bc=0 case is absent on
        # purpose: 65536 decompressed bytes sweep the whole address space, so the
        # oracle's call frame dies (it hangs out at 240 frames) and the byte values
        # cannot be hand-derived for an `expect` map either. Everything else here is
        # zero, so the source pointer, the secondary buffer page and the output
        # pointer all sit at $0000.
        {"c": 0x01, "read": {wDecompSourcePosPtr: 10, hBankROM: 1}},
        dict(POISON, b=0x00, c=0x10, d=0xC2, e=0x00,
             wram={wDecompSourcePosPtr: decomp_state(0x4000),
                   wTempPointerBank: b"\x01", hBankROM: b"\x05"},
             read={0xC200: 0x12, wDecompressionSecondaryBuffer: 0x100}),
        {"c": 0x01, "d": 0xC2, "e": 0x00,
         "wram": {wDecompSourcePosPtr: decomp_state(0x5000), wTempPointerBank: b"\x02"},
         "read": {0xC200: 3, wDecompressionSecondaryBuffer: 0x100}},
        {"b": 0x01, "c": 0x00, "d": 0xC2, "e": 0x00,
         "wram": {wDecompSourcePosPtr: decomp_state(0x4000), wTempPointerBank: b"\x03",
                  hBankROM: b"\x11"},
         "read": {0xC200: 0x102, wDecompressionSecondaryBuffer: 0x100}},
        {"b": 0x01, "c": 0x01, "d": 0xC2, "e": 0x00,
         "wram": {wDecompSourcePosPtr: decomp_state(0x4000), wTempPointerBank: b"\x04"},
         "read": {0xC200: 0x104, wDecompressionSecondaryBuffer: 0x100}},
        # Resumed mid-stream: 3 bytes still to repeat, toggle on, partial command byte
        # and a seeded secondary buffer, so the repeat path runs on real data.
        {"c": 0x20, "d": 0xC2, "e": 0x00,
         "wram": {wDecompSourcePosPtr: bytes([0x00, 0x60, 5, 0xA5, 1, 0x37, 3, 0xC0, 0x20, 0x40]),
                  wTempPointerBank: b"\x05", hBankROM: b"\x0a",
                  wDecompressionSecondaryBuffer: bytes((i * 7 + 3) & 0xFF for i in range(256))},
         "read": {0xC200: 0x22}},
        # Source below $4000: hardware ignores the bank there.
        {"c": 0x10, "d": 0xC2, "e": 0x00,
         "wram": {wDecompSourcePosPtr: decomp_state(0x0134), wTempPointerBank: b"\x0a"},
         "read": {0xC200: 0x12, wDecompressionSecondaryBuffer: 0x100}},
        {"c": 0x08, "d": 0xC2, "e": 0x00,
         "wram": {wDecompSourcePosPtr: decomp_state(0x4000), wTempPointerBank: b"\x01",
                  hBankROM: b"\x3f"},
         "read": {0xC200: 0x0A, wDecompressionSecondaryBuffer: 0x100}},
    ],
    "CopyBankedDataToDE": [
        # bc=0 is 65536 bytes, so this sweep overwrites the oracle call frame.
        {"oracle": False,
         "why": "bc=0 copies 65536 bytes and sweeps the whole address space, "
                "burying the oracle's synthesized call frame.",
         "wram": {0xC100: b"\x5a\xa5\x5a\xa5"},
         "expect": {hBankROM: b"\x00"},
         "expect_regs": {"b": 0, "c": 0, "d": 0xC1, "e": 0x00, "hl": 0}},
        dict(POISON, b=0x00, c=0x20, d=0xC1, e=0x00,
             wram={wTempPointer: banked_src(0x4000, 2), hBankROM: b"\x05",
                   0xC100: b"\x11" * 0x22}),
        {"c": 0x01, "d": 0xC2, "e": 0x00,
         "wram": {wTempPointer: banked_src(0x4000, 1), 0xC200: b"\x11" * 3}},
        {"b": 0x01, "c": 0x00, "d": 0xC2, "e": 0x00,
         "wram": {wTempPointer: banked_src(0x5000, 3), hBankROM: b"\x11",
                  0xC200: b"\x11" * 258}},
        {"b": 0x01, "c": 0x01, "d": 0xC2, "e": 0x00,
         "wram": {wTempPointer: banked_src(0x4000, 0x3F), 0xC200: b"\x11" * 260}},
        # Source below $4000: hardware ignores the bank there.
        {"c": 0x10, "d": 0xC3, "e": 0x00,
         "wram": {wTempPointer: banked_src(0x0134, 0x0A), hBankROM: b"\x3f",
                  0xC300: b"\x11" * 0x12}},
        {"c": 0x10, "d": 0xC3, "e": 0x00,
         "wram": {wTempPointer: banked_src(0x4000, 0), 0xC300: b"\x11" * 0x12}},
    ],
    "FillMemoryWithA": [
        {
            "oracle": False,
            "why": "all-zero registers means bc=0, i.e. 65536 bytes from $0000, which "
                   "sweeps the oracle's synthesized call frame at $CE00-$CFFF",
            "wram": {0xC100: b"\xff\xff", 0xC800: b"\xff", 0xDFFF: b"\xff",
                     hBankROM: b"\xff"},
            "expect": {0xC100: b"\x00\x00", 0xC800: b"\x00", 0xDFFF: b"\x00",
                       hBankROM: b"\x00"},
        },
        dict(POISON, hl=0xC100, b=0x00, c=0x40, wram={0xC100: b"\x11" * 0x42}),
        {"a": 0x5A, "b": 0, "c": 1, "hl": 0xC200, "wram": {0xC200: b"\x11" * 3}},
        {"a": 0x77, "b": 1, "c": 0, "hl": 0xC300, "wram": {0xC300: b"\x11" * 258}},
        {"a": 0x99, "b": 1, "c": 1, "hl": 0xC400, "wram": {0xC400: b"\x22" * 260}},
        {
            "a": 0x5A, "hl": 0xC100,
            "oracle": False,
            "why": "bc=0 is 65536 bytes, one full wrap of the address space; it "
                   "overwrites the synthesized call frame, so only the C side can run it",
            # Last byte written is $C0FF, so $C000 proves the wrap happened.
            "expect": {0xC000: b"\x5a", 0xC100: b"\x5a", 0xD000: b"\x5a",
                       0xDFFF: b"\x5a", hBankROM: b"\x5a"},
        },
    ],
    "FillMemoryWithDE": [
        {
            "oracle": False,
            "why": "all-zero registers means bc=0, i.e. 65536 pairs = 131072 bytes, "
                   "which sweeps the oracle's synthesized call frame at $CE00-$CFFF",
            "wram": {0xC100: b"\xff\xff", 0xD000: b"\xff", 0xDFFF: b"\xff"},
            "expect": {0xC100: b"\x00\x00", 0xD000: b"\x00", 0xDFFF: b"\x00"},
        },
        dict(POISON, hl=0xC500, b=0x00, c=0x08, wram={0xC500: b"\x11" * 18}),
        {"d": 0x12, "e": 0x34, "b": 0, "c": 1, "hl": 0xC600, "wram": {0xC600: b"\x11" * 4}},
        {"d": 0xAB, "e": 0xCD, "b": 1, "c": 0, "hl": 0xC700, "wram": {0xC700: b"\x11" * 514}},
        {"d": 0x01, "e": 0x02, "b": 1, "c": 1, "hl": 0xC000, "wram": {0xC000: b"\x33" * 516}},
        {
            "d": 0x5A, "e": 0xA5, "hl": 0xC100,
            "oracle": False,
            "why": "bc=0 is 65536 pairs = 131072 bytes, two full wraps of the address "
                   "space; it overwrites the synthesized call frame",
            # Pairs start on the even address $C100, so even addresses hold e and odd d.
            "expect": {0xC000: b"\xa5\x5a", 0xC100: b"\xa5\x5a", 0xD000: b"\xa5\x5a",
                       0xDFFE: b"\xa5\x5a", hBankROM: b"\xa5\x5a"},
        },
    ],
    "GetFarByte": [
        {"read": {hBankROM: 1}},
        dict(POISON, wram={hBankROM: b"\x07"}),
        {"a": 0x00, "hl": 0x0134, "read": {hBankROM: 1}},
        {"a": 0x00, "hl": 0x4000, "read": {hBankROM: 1}},
        {"a": 0x01, "hl": 0x4000, "read": {hBankROM: 1}},
        {"a": 0x02, "hl": 0x4000, "wram": {hBankROM: b"\x1f"}},
        {"a": 0x3F, "hl": 0x4002, "read": {hBankROM: 1}},
        # A non-zero bank with an address below $4000: hardware ignores the bank.
        {"a": 0x3F, "hl": 0x0134, "read": {hBankROM: 1}},
        {"a": 0x0A, "hl": 0x1FFF, "read": {hBankROM: 1}},
        # `ld a, [hl]` is a bus read, so an address at or above $8000 must reach RAM,
        # not the ROM image. rom_ptr alone answers $CE for the first of these.
        {"a": 0x02, "hl": 0xC200, "wram": {0xC200: b"\x5a", hBankROM: b"\x04"}},
        {"a": 0x11, "hl": 0xFF90, "wram": {0xFF90: b"\x77"}, "read": {hBankROM: 1}},
        {"a": 0x05, "hl": 0xDFFF, "wram": {0xDFFF: b"\xa3"}, "read": {hBankROM: 1}},
        # $A000 with SRAM disabled at power-on: the bus read is open bus, $FF.
        {"a": 0x02, "hl": 0xA000, "wram": {hBankROM: b"\x04"}, "read": {hBankROM: 1}},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "FillMemoryWithA": {
        "source_symbol": "FillMemoryWithA",
        "before": "gb_write8(hl++, a);",
        "after": "gb_write8(hl, a);",
        "case_ids": ["FillMemoryWithA-0", "FillMemoryWithA-1", "FillMemoryWithA-2", "FillMemoryWithA-3", "FillMemoryWithA-4", "FillMemoryWithA-5"],
    },
}
