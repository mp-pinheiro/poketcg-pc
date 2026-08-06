"""Oracle-diff cases for poketcg/src/home/random.asm."""

wRNG1 = 0xCACA  # wRNG1, wRNG2, wRNGCounter are consecutive

CONTRACT = {
    "UpdateRNGSources": ("a", "b", "c", "d", "e", "hl"),
    # HtimesL's exit a is always 0 (loop residue), so it is not part of the contract.
    "HtimesL": ("b", "c", "d", "e", "hl"),
    "Random": ("a", "b", "c", "d", "e", "hl"),
}

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CASES = {
    "UpdateRNGSources": [
        # Hand-traced from the asm: $12/$34/$56 -> $88/$4C/$57 with A=$C4.
        dict(POISON, wram={wRNG1: b"\x12\x34\x56"}),
        {"wram": {wRNG1: b"\x00\x00\x00"}},
        dict(POISON, wram={wRNG1: b"\xff\xff\xff"}),
        # Counter wrap: $FF -> $00 must not carry into wRNG2.
        dict(POISON, wram={wRNG1: b"\x80\x01\xff"}),
        # Exercises both feedback inputs: bit6(wRNG2) set, bit0(wRNG1) clear.
        dict(POISON, wram={wRNG1: b"\x02\x40\x00"}),
        # bit7(ctr ^ r1) == 1: the only case where `rl e` hands a set carry to `rl d`.
        # Every other seed has that carry 0, so dropping the term still diffs clean.
        dict(POISON, wram={wRNG1: b"\x01\x00\x80"}),
    ],
    "HtimesL": [
        {},
        # Poisoned: hl=$1234 -> $12 * $34 = $3A8, bc/de must survive the push/pop.
        dict(POISON),
        {"hl": 0x00FF},  # h=0 -> 0
        {"hl": 0xFF00},  # l=0 -> 0
        {"hl": 0xFFFF},  # 255 * 255 = $FE01, the widest product
        # a=$80: the only set bit is consumed on the iteration where a reaches 0,
        # so a port that tests `nz` before adding loses the whole product.
        {"hl": 0x8003},
        dict(POISON, hl=0x0180),  # h=1: single carry iteration, a hits 0 with it
        dict(POISON, hl=0x0101),
        dict(POISON, hl=0x02FF),  # de shifted left once before the add
        dict(POISON, hl=0xA55A),
    ],
    "Random": [
        {"wram": {wRNG1: b"\x00\x00\x00"}},
        dict(POISON, wram={wRNG1: b"\x12\x34\x56"}),
        # a=0 boundary: h=0 so the product is 0 regardless of the RNG byte, but
        # the RNG state must still advance.
        dict(POISON, a=0, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=0, wram={wRNG1: b"\xde\xad\xbe"}),
        dict(POISON, a=1, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=1, wram={wRNG1: b"\xff\xff\xff"}),
        dict(POISON, a=10, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=10, wram={wRNG1: b"\x80\x01\xff"}),
        dict(POISON, a=255, wram={wRNG1: b"\x12\x34\x56"}),
        dict(POISON, a=255, wram={wRNG1: b"\x02\x40\x00"}),
        # Seeds where bit7(wRNGCounter ^ wRNG1) == 1, so the rl e -> rl d carry
        # reaches both the returned byte and the diffed wRNG2.
        dict(POISON, wram={wRNG1: b"\x00\xff\x80"}),
        dict(POISON, a=10, wram={wRNG1: b"\x01\x00\x80"}),
    ],
}
