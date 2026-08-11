POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
WCONSOLE = 0xCAB4

CONTRACT = {
    "ShowCardPopCGBDisclaimer": {"compare": ("f",), "preserve": ()},
}

SETUP = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
CACHE_READ = {0xC620: 4, 0xC720: 4, 0xC820: 4, 0xC920: 4,
              0xCD05: 2, 0xCD0A: 1, 0xFFAA: 2, 0xFFAD: 1}
VRAM_READ = {0: {0x8000: 0x1000, 0x9000: 0x800}}

CASES = {
    "ShowCardPopCGBDisclaimer": [
        {"wram": {WCONSOLE: b"\x02"}},
        {"wram": {WCONSOLE: b"\x00"}, "keys": 0x01,
         "setup": SETUP, "read": CACHE_READ, "vread": VRAM_READ},
        {"wram": {WCONSOLE: b"\x00"}, "keys": 0x02,
         "setup": SETUP, "read": CACHE_READ, "vread": VRAM_READ},
        dict(POISON, wram={WCONSOLE: b"\x00"}, keys=0x01,
             setup=SETUP, read=CACHE_READ, vread=VRAM_READ),
    ],
}

MUTATIONS = {
    "ShowCardPopCGBDisclaimer": {
        "source_symbol": "ShowCardPopCGBDisclaimer",
        "before": "if (wConsole == CONSOLE_CGB)",
        "after": "if (wConsole != CONSOLE_CGB)",
        "case_ids": [
            "ShowCardPopCGBDisclaimer-0",
            "ShowCardPopCGBDisclaimer-1",
            "ShowCardPopCGBDisclaimer-2",
            "ShowCardPopCGBDisclaimer-3",
        ],
    },
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
