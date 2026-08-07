"""Oracle-diff cases for poketcg/src/home/dma.asm."""

WOAM = 0xCA00
OAM = 0xFE00
PAT = bytes((i * 7 + 3) & 0xFF for i in range(160))

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DMA": ("b", "c", "d", "e", "hl"),
}

CASES = {
    "DMA": [
        {"wram": {WOAM: PAT}, "read": {OAM: 160}},
        dict(POISON, wram={WOAM: PAT}, read={OAM: 160}),
    ],
}
