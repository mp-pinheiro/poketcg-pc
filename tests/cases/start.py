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

# >>> factory-cases-statics
def _header_for(payload):
    checksum = sum(payload) & 0xFFFF
    return bytes([0x08, 0x00, len(payload) & 0xFF, len(payload) >> 8,
                  checksum & 0xFF, checksum >> 8])

def _build_image(payload):
    return _header_for(payload) + b"\x00\x00" + payload

_VALID_PAYLOAD = bytes(179)
_VALID_IMAGE = _build_image(_VALID_PAYLOAD)
_INVALID_IMAGE = (bytes([0x08 ^ 0xFF, 0x00 ^ 0xFF]) + _header_for(_VALID_PAYLOAD)[2:]
                  + b"\x00\x00" + _VALID_PAYLOAD)

wCurHighlightedStartMenuItem = 0xD626
wCurMenuItem = 0xCD10
wHasSaveData = 0xD624
wCurOverworldMap = 0xD3CB
wMedalCount = 0xD3CC
wTotalNumCardsCollected = 0xD3CD
wTotalNumCardsToCollect = 0xD3CE
wTxRam2 = 0xCE3F
wTxRam3 = 0xCE43
SETUP_TEXT = [{"fn": "SetupText", "d": 0x20, "e": 0x40}]
# <<< factory-cases-statics

# >>> factory CheckIfHasSaveData
CONTRACT["CheckIfHasSaveData"] = {"compare": ("a", "f"), "preserve": (), "wram_out": True}
CASES["CheckIfHasSaveData"] = [
    {"wram": {0xFF81: b"\x03"}, "ramg": True,
     "sram": {2: {0xB800: _VALID_IMAGE}, 0: {0xBC03: b"\x00", 0xBC00: b"\x00" * 0x100}},
     "read": {0xD624: 1, 0xD625: 1}},
    dict(POISON, wram={0xFF81: b"\x03"}, ramg=True,
         sram={2: {0xB800: _INVALID_IMAGE}},
         read={0xD624: 1, 0xD625: 1}),
    {"wram": {0xFF81: b"\x03"}, "ramg": True,
     "sram": {2: {0xB800: _INVALID_IMAGE}},
     "read": {0xD624: 1, 0xD625: 1}},
]
# <<< factory CheckIfHasSaveData

# >>> factory PrintStartMenuDescriptionText
CONTRACT["PrintStartMenuDescriptionText"] = {"compare": ("a", "f", "b", "c", "d", "e"), "preserve": ("b", "c", "d", "e")}
CASES["PrintStartMenuDescriptionText"] = [
    {"wram": {wCurMenuItem: b"\x02", wCurHighlightedStartMenuItem: b"\x02", wHasSaveData: b"\x01"}},
    dict(POISON, a=0xAA, f=0xF0, b=0xBB, c=0xCC, d=0xDD, e=0xEE, hl=0x1234,
         wram={wCurMenuItem: b"\x03", wCurHighlightedStartMenuItem: b"\x03", wHasSaveData: b"\x00"})
]
# <<< factory PrintStartMenuDescriptionText

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
# >>> factory-mutation CheckIfHasSaveData
MUTATIONS["CheckIfHasSaveData"] = {"source_symbol": "CheckIfHasSaveData", "before": "\tuint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;", "after": "\tuint8_t has_save = (first.f & 0x10u) ? FALSE : TRUE;", "case_ids": ["CheckIfHasSaveData-0", "CheckIfHasSaveData-2"]}
# <<< factory-mutation CheckIfHasSaveData
# >>> factory-mutation PrintStartMenuDescriptionText
MUTATIONS["PrintStartMenuDescriptionText"] = {"source_symbol": "PrintStartMenuDescriptionText", "before": "\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;", "after": "\tuint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0x80u : f;", "case_ids": ["PrintStartMenuDescriptionText-0", "PrintStartMenuDescriptionText-1"]}
# <<< factory-mutation PrintStartMenuDescriptionText
