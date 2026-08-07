"""Oracle-diff cases for poketcg/src/home/copy.asm."""

SRC = 0xC100
DST = 0xC500
wLCDC = 0xCABB
VRAM_DST = 0x8000
OAM_DST = 0xFE00

# $DDEE is where the d=$DD/e=$EE poison lands: real WRAM, clear of the oracle's
# $CE00-$CFFF frame, so the poisoned registers can be used verbatim as a
# destination and hl=$1234 verbatim as a (ROM) source.
POISON_DST = 0xDDEE
POISON_SRC = 0x1234

PAT = bytes((i * 7 + 3) & 0xFF for i in range(512))

CONTRACT = {
    # b ends at 0 and a holds the last byte copied: both are loop residue.
    # c survives the push bc / pop bc around every block.
    "CopyGfxData": ("c", "d", "e", "hl"),
    # bc ends at 0 and a at 0 (`ld a, c / or b`): residue, not outputs.
    "CopyDataHLtoDE": ("d", "e", "hl"),
    # "preserves all registers except af" — copy.asm:37.
    "CopyDataHLtoDE_SaveRegisters": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "CopyGfxData": [
        # b=0, c=0: 256 blocks of 256 bytes, hl=de=0, i.e. a 64 KiB self-copy.
        {},
        {"a": 0xAA, "f": 0xF0, "b": 4, "c": 3, "d": 0xDD, "e": 0xEE, "hl": POISON_SRC,
         "read": {POISON_DST: 16}},
        # b=0 is 256 blocks, not zero blocks.
        {"b": 0, "c": 1, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:256]}, "read": {DST: 260}},
        # c=0 is 256 bytes per block, not zero bytes.
        {"b": 1, "c": 0, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:256]}, "read": {DST: 260}},
        {"b": 2, "c": 0, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:512]}, "read": {DST: 516}},
        {"b": 1, "c": 1, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:4]}, "read": {DST: 4}},
        {"b": 3, "c": 0x10, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:0x30]}, "read": {DST: 0x34}},
        # wLCDC bit 7 set takes .hblank_copy in the asm; the C has one path.
        {"b": 4, "c": 8, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {wLCDC: b"\x80", SRC: PAT[:32]}, "read": {DST: 36}},
        # WRAM -> VRAM ($8000); reads back through the VRAM window, not WRAM.
        {"b": 3, "c": 0x10, "hl": SRC, "d": VRAM_DST >> 8, "e": VRAM_DST & 0xFF,
         "wram": {SRC: PAT[:0x30]}, "read": {VRAM_DST: 0x34}},
        # c=0 is 256 bytes/block into VRAM, not zero.
        {"b": 1, "c": 0, "hl": SRC, "d": VRAM_DST >> 8, "e": VRAM_DST & 0xFF,
         "wram": {SRC: PAT[:256]}, "read": {VRAM_DST: 260}},
        # OAM ($FE00) destination; reads back through the OAM capture.
        {"b": 1, "c": 4, "hl": SRC, "d": OAM_DST >> 8, "e": OAM_DST & 0xFF,
         "wram": {SRC: PAT[:4]}, "read": {OAM_DST: 8}},
    ],
    "CopyDataHLtoDE": [
        {},
        {"a": 0xAA, "f": 0xF0, "b": 0x00, "c": 0x10, "d": 0xDD, "e": 0xEE,
         "hl": POISON_SRC, "read": {POISON_DST: 20}},
        {"b": 0, "c": 1, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:4]}, "read": {DST: 4}},
        {"b": 1, "c": 0, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:256]}, "read": {DST: 260}},
        # 257 is where a port that only decrements c stops early.
        {"b": 1, "c": 1, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:257]}, "read": {DST: 260}},
        {
            "b": 0, "c": 0, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
            "wram": {SRC: b"\xde\xad\xbe\xef"},
            "oracle": False,
            "why": "bc=0 is 65536 bytes, which sweeps the whole address space "
                   "and would bury the oracle's synthesized call frame.",
            # de trails hl by $400, so from iteration $400 on the loop re-reads
            # what it just wrote and the four seed bytes smear across memory at
            # a $400 stride. $C500 is the first write; $D900 is $1400 bytes in,
            # both surviving the $E000 echo pass because $2000 is a multiple of
            # the stride. A no-op or an 8-bit count leaves them zero.
            "expect": {DST: b"\xde\xad\xbe\xef", 0xD900: b"\xde\xad\xbe\xef"},
        },
    ],
    "CopyDataHLtoDE_SaveRegisters": [
        {},
        {"a": 0xAA, "f": 0xF0, "b": 0x00, "c": 0x10, "d": 0xDD, "e": 0xEE,
         "hl": POISON_SRC, "read": {POISON_DST: 20}},
        {"b": 0, "c": 1, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:4]}, "read": {DST: 4}},
        {"b": 1, "c": 1, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
         "wram": {SRC: PAT[:257]}, "read": {DST: 260}},
        # The all-zero case above is a degenerate self-copy that an empty body also
        # passes; this is the bc=0 boundary with the data actually moving.
        {
            "b": 0, "c": 0, "hl": SRC, "d": DST >> 8, "e": DST & 0xFF,
            "wram": {SRC: b"\xde\xad\xbe\xef"},
            "oracle": False,
            "why": "bc=0 is 65536 bytes, which sweeps the whole address space "
                   "and would bury the oracle's synthesized call frame.",
            "expect": {DST: b"\xde\xad\xbe\xef", 0xD900: b"\xde\xad\xbe\xef"},
        },
    ],
}
