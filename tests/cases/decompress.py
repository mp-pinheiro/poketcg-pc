"""Oracle-diff cases for poketcg/src/home/decompress.asm.

The nine pieces of decompressor state sit consecutively at $CAD6, so a case seeds
them as one 10-byte span. InitDataDecompression is the only way the game reaches
that state, but a probe call is a single routine call, so the streaming routines
get the post-Init state (and any mid-stream state) seeded directly instead.
"""

STATE = 0xCAD6  # source ptr LE, bits left, command byte, repeat toggle, lengths,
                # bytes to repeat, buffer page, repeat offset, buffer low
PAGE = 0xC0     # secondary buffer page used by the game (wDecompressionSecondaryBuffer)
BUF = PAGE << 8
START_LOW = 0xEF  # LOW(wDecompressionSecondaryBufferStart)

SRC = 0xC200
OUT = 0xC300
SRC_LIT = 0xC400
OUT_LIT = 0xC600

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    # bc and de are read but never written; hl and a are clobbered.
    "InitDataDecompression": {"compare": ("b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")},
    # push hl / push de ... pop de / pop hl. bc ends at 0 and a at 0 as loop residue.
    "DecompressData": {"compare": ("d", "e", "hl"), "preserve": ("d", "e", "hl")},
    # returns the byte in a, clobbers bc and hl; d/e are untouched.
    "DecompressData.Decompress": {"compare": ("a", "d", "e"), "preserve": ("d", "e")},
}


def state(src, bits=1, cmd=0x00, toggle=0, lengths=0x00, nbytes=0,
          page=PAGE, offset=0x00, low=START_LOW):
    return bytes([src & 0xFF, src >> 8, bits, cmd, toggle, lengths, nbytes,
                  page, offset, low])


def page_bytes(at_low, data):
    return bytes(at_low) + bytes(data) + bytes(0x100 - at_low - len(data))


# One command byte followed by 2 literals and 6 repeat commands, then a second
# command byte, for 34 output bytes total. Hand-traced against decompress.asm:
#   $11 $22 | $11 $22 $11 | $11 $22 $11 $22 $11 | $11 $22 | $11 $22 |
#   $22 $11 $22 $11 $11 $22 $11 $22 $11 $11 $22 $11 $22 $22 $11 $22 $11 |
#   $11 $11 | $99
RICH = bytes([
    0xC0,  # command bits, MSB first: literal, literal, then six repeats
    0x11,  # literal
    0x22,  # literal
    0xEF,  # repeat from $EF
    0x13,  # high nybble 1 -> 3 bytes; low nybble 3 is kept for the next repeat
    0xEF,  # repeat from $EF, toggle on -> reuses low nybble 3 -> 5 bytes
    0xEF,  # repeat from $EF, toggle off -> a lengths byte follows
    0x00,  # high nybble 0 -> 2 bytes
    0xF1,  # repeat from $F1, toggle on -> low nybble 0 -> 2 bytes
    0xF0,  # repeat from $F0, toggle off
    0xF0,  # high nybble F -> 17 bytes, wrapping the page low byte past $FF
    0x00,  # repeat from $00, toggle on -> low nybble 0 -> 2 bytes; eighth command bit
    0x80,  # command byte refill: literal, then seven repeats
    0x99,  # literal
])

# State and buffer after the first 5 of those bytes, so a second call continues the
# same stream. Feeding this 5 more bytes must produce outputs 6..10 of RICH.
MID5 = state(src=SRC + 5, bits=6, cmd=0x00, toggle=1, lengths=0x13, nbytes=0,
             offset=0xF2, low=0xF4)
MID5_BUF = page_bytes(START_LOW, [0x11, 0x22, 0x11, 0x22, 0x11])

# Mid-repeat: the same stream three bytes in, with two repeat bytes still owed.
MID3 = state(src=SRC + 5, bits=6, cmd=0x00, toggle=1, lengths=0x13, nbytes=2,
             offset=0xF0, low=0xF2)
MID3_BUF = page_bytes(START_LOW, [0x11, 0x22, 0x11])

# 33 all-literal command bytes, 8 literals each: 264 bytes of output, enough for the
# 256/257 boundary where a port that only decrements the low byte of bc stops early.
LITERAL = b"".join(bytes([0xFF]) + bytes((i * 8 + k) & 0xFF for k in range(8))
                   for i in range(33))

# bc == 0 means 65536 output bytes, which sweeps the whole address space and cannot
# run on the oracle. Seeding every byte the decompressor can read with $AA makes the
# run a fixed point: a literal copies $AA out of the source, a repeat copies $AA out
# of the secondary buffer, and each output byte written back into memory is $AA
# again. That survives the sweep walking over the state block at $CAD6: the source
# pointer, the buffer page and every length field become $AA too, and $AAxx is still
# inside the seeded window.
#
# Writes below $8000 are live MBC5 register writes, so the output start address
# decides how long the fixed point lasts. $AA into $0000-$1FFF is not $0A, so it
# turns SRAM off and every later source read in $A000-$BFFF is open bus. Starting at
# $2000 puts that region last: output bytes 1..57344 cover $2000-$FFFF, and only
# bytes 57345..65536 land on RAMG, where nothing is stored. Measured: the first
# non-$AA output byte is 57345, writing to $0001.
#
# Two more consequences of the live decode. $2000-$2FFF selects ROM bank $AA % 64,
# which is never read: the source pointer's measured reach is $8000-$C371 and it
# never drops below $8000. $4000-$5FFF selects SRAM bank ($AA & $F) % 4 = 2, which is
# why all four banks are seeded and not just the one live at entry. $C000-$C3FF is
# seeded so the source's WRAM tail does not depend on the sweep having overwritten it
# first.
AA_SEED = {at: b"\xaa" * 0x800 for at in range(0x8000, 0xA000, 0x800)}
AA_SEED[BUF] = b"\xaa" * 0x400
AA_SEED[STATE] = state(src=0x8000)
# Witnesses: neither address is ever read (the source stops at $C371 and the buffer
# page is $C0 then $AA), so $55 can only become $AA by being written. $D000 is output
# byte 45057 and $FF80 is 57217, both far past the 256 an 8-bit counter would stop at.
AA_SEED[0xD000] = b"\x55"
AA_SEED[0xFF80] = b"\x55"
AA_SRAM = {bank: {at: b"\xaa" * 0x800 for at in range(0xA000, 0xC000, 0x800)}
           for bank in range(4)}
# The state block itself is not checked: the sweep does overwrite it, but every later
# .Decompress call writes its own fields again, so its final value is not derivable.

CASES = {
    "InitDataDecompression": [
        # b = 0 clears $0000-$00FF, where writes are MBC register writes and land
        # nowhere; only the state block is observable.
        {"wram": {STATE: bytes(10)}},
        # de is stored, never dereferenced, so the poison value goes in unchanged.
        # $C0FF and $C200 are guards: the clear is exactly the $C1 page.
        dict(POISON, b=0xC1,
             wram={STATE: bytes(10), 0xC100: b"\xff" * 0x100,
                   0xC0FF: b"\xff", 0xC200: b"\xff"}),
        # Page overlapping the state block: the asm writes the state first and then
        # clears, so the state is wiped again.
        dict(POISON, b=0xCA, d=0xC2, e=0x34, wram={STATE: b"\xff" * 10}),
        # LE store of a source pointer with both halves distinct and high.
        dict(POISON, b=PAGE, d=0xFF, e=0xFE,
             wram={STATE: bytes(10), BUF: b"\xff" * 0x100}),
        # Seeding the state block with zeros hides the five stores that write zero
        # ($CAD9 command byte, $CADA toggle, $CADB lengths, $CADC bytes-to-repeat,
        # $CADE offset). Poison it, and clear a page that does not overlap it.
        dict(POISON, b=0xC1, d=0x12, e=0x34,
             wram={STATE: b"\xa5" * 10, 0xC100: b"\xff" * 0x100},
             read={STATE: 10}),
    ],
    "DecompressData": [
        # Single byte: the first command byte is pulled and one literal copied.
        {"b": 0x00, "c": 0x01, "d": OUT >> 8, "e": OUT & 0xFF,
         "wram": {SRC: RICH, STATE: state(src=SRC)}, "read": {OUT: 1, BUF: 0x100}},
        # First half of RICH, then the second half from the state the first left
        # behind: the two together must match the single 10-byte call below.
        {"b": 0x00, "c": 0x05, "d": OUT >> 8, "e": OUT & 0xFF,
         "wram": {SRC: RICH, STATE: state(src=SRC)}, "read": {OUT: 5, BUF: 0x100}},
        {"b": 0x00, "c": 0x05, "d": OUT >> 8, "e": OUT & 0xFF,
         "wram": {SRC: RICH, STATE: MID5, BUF: MID5_BUF},
         "read": {OUT: 5, BUF: 0x100}},
        {"b": 0x00, "c": 0x0A, "d": OUT >> 8, "e": OUT & 0xFF,
         "wram": {SRC: RICH, STATE: state(src=SRC)}, "read": {OUT: 10, BUF: 0x100}},
        # Resuming mid-repeat, with two bytes still owed before a command is read.
        {"b": 0x00, "c": 0x08, "d": OUT >> 8, "e": OUT & 0xFF,
         "wram": {SRC: RICH, STATE: MID3, BUF: MID3_BUF},
         "read": {OUT: 8, BUF: 0x100}},
        # All 34 bytes: both command-bit branches, both toggle states, the 17-byte
        # run that wraps the page low byte, and the command byte refill.
        dict(POISON, b=0x00, c=0x22, d=OUT >> 8, e=OUT & 0xFF,
             wram={SRC: RICH, STATE: state(src=SRC)},
             read={OUT: 34, BUF: 0x100}),
        # Same stream against a secondary buffer page other than the game's.
        dict(POISON, b=0x00, c=0x22, d=OUT >> 8, e=OUT & 0xFF,
             wram={SRC: RICH, STATE: state(src=SRC, page=0xC1),
                   0xC100: bytes(0x100), 0xC0FF: b"\x5a", 0xC200 + len(RICH): b"\x5a"},
             read={OUT: 34, 0xC100: 0x100}),
        {"b": 0x01, "c": 0x00, "d": OUT_LIT >> 8, "e": OUT_LIT & 0xFF,
         "wram": {SRC_LIT: LITERAL, STATE: state(src=SRC_LIT)},
         "read": {OUT_LIT: 0x100, BUF: 0x100}},
        {"b": 0x01, "c": 0x01, "d": OUT_LIT >> 8, "e": OUT_LIT & 0xFF,
         "wram": {SRC_LIT: LITERAL, STATE: state(src=SRC_LIT)},
         "read": {OUT_LIT: 0x101, BUF: 0x100}},
        {"b": 0x00, "c": 0x00, "d": 0x20, "e": 0x00, "oracle": False,
         "why": "bc == 0 is 65536 output bytes: it overwrites the whole address "
                "space, including the oracle's synthesized call frame and stack, "
                "so no emulator run can survive it",
         "wram": AA_SEED,
         "sram": AA_SRAM,
         "expect": {
             0xD000: b"\xaa",  # seeded $55; written as output byte 45057
             0xFF80: b"\xaa",  # seeded $55; written as output byte 57217
         }},
    ],
    "DecompressData.Decompress": [
        # All-zero state: bits left 0 decrements to $FF without refilling, the zero
        # command byte selects repeat mode, and the source and buffer pages are both
        # $0000, so the offset byte, the lengths byte and the repeated byte all come
        # out of ROM and the buffer write lands on an MBC register.
        {"wram": {STATE: bytes(10)}},
        dict(POISON, wram={SRC: RICH, STATE: state(src=SRC)}, read={BUF: 0x100}),
        # Toggle on: the run length is the low nybble of the byte kept last time,
        # and no lengths byte is read.
        dict(POISON, wram={SRC: RICH, STATE: MID5, BUF: MID5_BUF},
             read={BUF: 0x100}),
        # Still repeating: no command bit and no source byte are consumed.
        dict(POISON, wram={SRC: RICH, STATE: MID3, BUF: MID3_BUF},
             read={BUF: 0x100}),
        # Last owed byte of a run: wDecompNumBytesToRepeat reaches 0.
        dict(POISON,
             wram={SRC: RICH,
                   STATE: state(src=SRC + 5, bits=6, toggle=1, lengths=0x13,
                                nbytes=1, offset=0xF1, low=0xF3),
                   BUF: MID5_BUF},
             read={BUF: 0x100}),
        # Maximum run length: lengths nybble $F puts $10 in wDecompNumBytesToRepeat.
        dict(POISON, wram={SRC: b"\x00\xef\xff", STATE: state(src=SRC),
                           BUF: page_bytes(START_LOW, [0x11, 0x22, 0x11])},
             read={BUF: 0x100}),
        # Read and write low bytes both at $FF: the read happens first, then the
        # write to the same address, and both wrap to $00 for the next call.
        dict(POISON, wram={SRC: RICH,
                           STATE: state(src=SRC, nbytes=3, offset=0xFF, low=0xFF),
                           BUF: page_bytes(0xFC, [0x1A, 0x2B, 0x3C, 0x4D])},
             read={BUF: 0x100}),
        # Write wraps to the start of the page while the read does not.
        dict(POISON, wram={SRC: RICH,
                           STATE: state(src=SRC, nbytes=3, offset=0x7F, low=0x00),
                           BUF: page_bytes(0x7F, [0x5E, 0x6F])},
             read={BUF: 0x100}),
        # A page other than the game's, with a literal copy landing in it.
        dict(POISON, wram={SRC: RICH, STATE: state(src=SRC, page=0xC1),
                           0xC100: bytes(0x100)},
             read={0xC100: 0x100}),
    ],
}

MUTATIONS = {
    "DecompressData": {
        "source_symbol": "DecompressData",
        "before": "de = (uint16_t)(de + 1);",
        "after": "de = (uint16_t)(de + 2);",
        "case_ids": ["DecompressData-0", "DecompressData-1", "DecompressData-2", "DecompressData-3", "DecompressData-4", "DecompressData-5", "DecompressData-6", "DecompressData-7", "DecompressData-8", "DecompressData-9"],
    },
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
