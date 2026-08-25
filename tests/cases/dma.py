"""Oracle-diff cases for poketcg/src/home/dma.asm."""

WOAM = 0xCA00
OAM = 0xFE00
PAT = bytes((i * 7 + 3) & 0xFF for i in range(160))

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {
    "DMA": {"compare": ("a", "f", "b", "c", "d", "e", "hl"),
            "preserve": ("b", "c", "d", "e", "hl")},
}

CASES = {
    "DMA": [
        {"wram": {WOAM: PAT}, "read": {OAM: 160}},
        dict(POISON, wram={WOAM: PAT}, read={OAM: 160}),
    ],
}
# >>> factory CopyDMAFunction
CONTRACT["CopyDMAFunction"] = {"compare": (), "preserve": ()}
CASES["CopyDMAFunction"] = [
    {"read": {0xFF83: 10}},
    dict(POISON, read={0xFF83: 10}),
]
# <<< factory CopyDMAFunction

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)


MUTATIONS = {
    "DMA": {
        "source_symbol": "DMA",
        "before": "for (uint16_t i = 0; i < 0xA0u; i++)",
        "after": "for (uint16_t i = 0xA0u; i > 0; i--)",
        "case_ids": ["DMA-0", "DMA-1"],
    },
}
# >>> factory-mutation CopyDMAFunction
MUTATIONS["CopyDMAFunction"] = {"source_symbol": "CopyDMAFunction", "before": "void CopyDMAFunction(void)\n{\n\tconst uint8_t *stub = rom_ptr(0u, DMA_ROM_ADDR);", "after": "void CopyDMAFunction(void)\n{\n\tconst uint8_t *stub = rom_ptr(0u, (uint16_t)(DMA_ROM_ADDR + 1u));", "case_ids": ["CopyDMAFunction-0", "CopyDMAFunction-1"]}
# <<< factory-mutation CopyDMAFunction
