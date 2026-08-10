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
    "CopyGfxData": {
        "compare": ("c", "d", "e", "hl"),
        "preserve": ("c",),
    },
    "CopyDataHLtoDE": {
        "compare": ("d", "e", "hl"),
        "preserve": (),
    },
    "CopyDataHLtoDE_SaveRegisters": {
        "compare": ("b", "c", "d", "e", "hl"),
        "preserve": ("b", "c", "d", "e", "hl"),
    },
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
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
SCHEMA2_CASES["CopyDataHLtoDE"] = [{
    "id": "CopyDataHLtoDE-primary-4",
    "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
    "registers": {
        "a": 0, "f": 0, "b": 0, "c": 1,
        "d": DST >> 8, "e": DST & 0xFF, "hl": SRC,
    },
    "bus": {},
    "seeds": {"wram": {SRC: PAT[:4], DST: b"\x00" * 4}},
    "setup": [],
    "input_events": [],
    "instruction_budget": 10000,
    "cycle_budget": 40000,
    "completion": {"mode": "return"},
    "evidence": "primary",
}]

SCHEMA2_CASES["CopyGfxData"] = [{
    "id": "CopyGfxData-primary-1",
    "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
    "registers": {
        "a": 0, "f": 0, "b": 1, "c": 1,
        "d": DST >> 8, "e": DST & 0xFF, "hl": SRC,
    },
    "bus": {},
    "seeds": {"wram": {SRC: PAT[:1], DST: b"\x00"}},
    "setup": [],
    "input_events": [],
    "instruction_budget": 10000,
    "cycle_budget": 40000,
    "completion": {"mode": "return"},
    "evidence": "primary",
}]
SCHEMA2_CASES["CopyDataHLtoDE_SaveRegisters"] = [{
    "id": "CopyDataHLtoDE_SaveRegisters-primary-257",
    "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
    "registers": {
        "a": 0, "f": 0, "b": 1, "c": 1,
        "d": DST >> 8, "e": DST & 0xFF, "hl": SRC,
    },
    "bus": {},
    "seeds": {"wram": {SRC: PAT[:257], DST: b"\x00" * 257}},
    "setup": [],
    "input_events": [],
    "instruction_budget": 20000,
    "cycle_budget": 80000,
    "completion": {"mode": "return"},
    "evidence": "primary",
}]

def _copy_primary(identifier, registers, seeds, budget=10000, completion=None, evidence="primary"):
    return {
        "id": identifier,
        "mapper": {"rom_bank": 1, "ram_bank": 0, "vram_bank": 0, "ram_enable": False},
        "registers": registers,
        "bus": {},
        "seeds": seeds,
        "setup": [],
        "input_events": [],
        "instruction_budget": budget,
        "cycle_budget": budget * 16,
        "completion": completion or {"mode": "return"},
        "evidence": evidence,
    }

SCHEMA2_CASES["CopyGfxData"].extend([
    _copy_primary("CopyGfxData-zero", {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}, {}, 20_000_000, {"mode": "pre-ret", "pc": 0x0731}, "native-stress"),
    _copy_primary(
        "CopyGfxData-poison",
        {"a": 0xAA, "f": 0xF0, "b": 4, "c": 3, "d": 0xDD, "e": 0xEE, "hl": 0x1234},
        {"wram": {0xDDEE: b"\x00" * 12}},
    ),
    _copy_primary(
        "CopyGfxData-c-zero",
        {"a": 0, "f": 0, "b": 1, "c": 0, "d": DST >> 8, "e": DST & 0xFF, "hl": SRC},
        {"wram": {SRC: PAT[:256], DST: b"\x00" * 256}},
    ),
])
SCHEMA2_CASES["CopyDataHLtoDE"].extend([
    _copy_primary("CopyDataHLtoDE-zero", {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}, {}, 2_000_000, {"mode": "pre-ret", "pc": 0x0744}, "native-stress"),
    _copy_primary(
        "CopyDataHLtoDE-poison",
        {"a": 0xAA, "f": 0xF0, "b": 0, "c": 16, "d": 0xDD, "e": 0xEE, "hl": 0x1234},
        {"wram": {0xDDEE: b"\x00" * 16}},
    ),
    _copy_primary(
        "CopyDataHLtoDE-one",
        {"a": 0, "f": 0, "b": 0, "c": 1, "d": DST >> 8, "e": DST & 0xFF, "hl": SRC},
        {"wram": {SRC: PAT[:1], DST: b"\x00"}},
    ),
])
SCHEMA2_CASES["CopyDataHLtoDE_SaveRegisters"].extend([
    _copy_primary("CopyDataHLtoDE_SaveRegisters-zero", {"a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}, {}, 2_000_000, {"mode": "pre-ret", "pc": 0x073b}, "dependency-blocked"),
    _copy_primary(
        "CopyDataHLtoDE_SaveRegisters-poison",
        {"a": 0xAA, "f": 0xF0, "b": 0, "c": 16, "d": 0xDD, "e": 0xEE, "hl": 0x1234},
        {"wram": {0xDDEE: b"\x00" * 16}},
    ),
    _copy_primary(
        "CopyDataHLtoDE_SaveRegisters-one",
        {"a": 0, "f": 0, "b": 0, "c": 1, "d": DST >> 8, "e": DST & 0xFF, "hl": SRC},
        {"wram": {SRC: PAT[:1], DST: b"\x00"}},
    ),
])

MUTATIONS = {
    "CopyDataHLtoDE": {
        "source_symbol": "CopyDataHLtoDE",
        "before": "\tdo {\n\t\tgb_write8(dst++, gb_read8(src++));",
        "after": "\tdo {\n\t\tgb_write8(dst++, gb_read8(src++));\n\t\tgb_write8(dst++, gb_read8(src++));",
        "case_ids": ["CopyDataHLtoDE-primary-4"],
    },
}
