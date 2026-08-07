"""Oracle-diff cases for ClearSRAMBGMaps (gfx/load_gfx.asm:293-308)."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hBankSRAM = 0xFF81

# sGfxBuffer0 + sGfxBuffer1: $800 bytes at $A000 in SRAM bank 1.
GFX_FILL = 0xA000
GFX_FILL_LEN = 0x800

CONTRACT = {
    # a is the SRAM bank restored from hBankSRAM; f, b, c, d, e, hl are preserved.
    "ClearSRAMBGMaps": ("a", "f", "b", "c", "d", "e", "hl"),
}

CASES = {
    "ClearSRAMBGMaps": [
        # Poisoned first: an empty port leaves the $AA seed and the diff fails.
        {"wram": {hBankSRAM: b"\x01"},
         "sram": {0x01: {GFX_FILL: b"\xaa" * GFX_FILL_LEN}},
         "read": {GFX_FILL: GFX_FILL_LEN}},
        dict(POISON,
             wram={hBankSRAM: b"\x01"},
             sram={0x01: {GFX_FILL: b"\xaa" * GFX_FILL_LEN}},
             read={GFX_FILL: GFX_FILL_LEN}),
        # hBankSRAM differs from the fill bank, so exit a must be 2, not 1. No SRAM read:
        # the selected bank at RET is 2, whose storage is unseeded.
        {"wram": {hBankSRAM: b"\x02"}},
    ],
}
