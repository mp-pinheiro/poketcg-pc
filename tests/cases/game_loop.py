POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

WCONSOLE = 0xCAB4
WTILE_MAP_FILL = 0xCAB6
WLCDC = 0xCABB
WBGP = 0xCABC
WOBP0 = 0xCABD
WOBP1 = 0xCABE
WFLUSH_PALETTE_FLAGS = 0xCABF

READ = {
    WTILE_MAP_FILL: 1,
    WLCDC: 1,
    WBGP: 1,
    0xCAB7: 1,
    0xFFFF: 1,
    WOBP0: 1,
    WOBP1: 1,
    WFLUSH_PALETTE_FLAGS: 1,
    0xCD04: 1,
    0xFF40: 1,
    0xFF47: 1,
    0xFF48: 1,
    0xFF49: 1,
    0xFFA8: 1,
    0xFFA9: 1,
    0xFFB0: 1,
    0xC600: 0x100,
}

CONTRACT = {
    "SetupResetBackUpRamScreen": {"compare": (), "preserve": ()},
}

CASES = {
    "SetupResetBackUpRamScreen": [
        {"wram": {WCONSOLE: b"\x00", WTILE_MAP_FILL: b"\x00",
                  WLCDC: b"\x00", WBGP: b"\x00", WOBP0: b"\x00",
                  WOBP1: b"\x00", WFLUSH_PALETTE_FLAGS: b"\x00",
                  0xFF47: b"\xFC", 0xFF48: b"\xFF", 0xFF49: b"\xFF"},
         "read": READ, "vread": {0: {0x9000: 896}}},
        dict(POISON,
             wram={WCONSOLE: b"\x00", WTILE_MAP_FILL: b"\xA5",
                   WLCDC: b"\x80", WBGP: b"\x11", WOBP0: b"\x22",
                   WOBP1: b"\x33", WFLUSH_PALETTE_FLAGS: b"\x44",
                   0xFF47: b"\xFC", 0xFF48: b"\xFF", 0xFF49: b"\xFF"},
             read=READ, vread={0: {0x9000: 896}}),
    ],
}

# >>> factory-cases-statics
hWhoseTurn = 0xFF97
wUppercaseHalfWidthLetters = 0xCD0D
sCardCollection = 0xA100

hKeysHeld = 0xFF90
sTextSpeed = 0xA006
sSkipDelayAllowed = 0xA009
wTextSpeed = 0xCE47
wSkipDelayAllowed = 0xCCF2
# <<< factory-cases-statics

# >>> factory InitSaveDataAndSetUppercase
CONTRACT["InitSaveDataAndSetUppercase"] = {"compare": (), "preserve": ()}
CASES["InitSaveDataAndSetUppercase"] = [
    {"wram": {hWhoseTurn: b"\xFF", wUppercaseHalfWidthLetters: b"\x00"},
     "read": {wUppercaseHalfWidthLetters: 1},
     "sread": {0: {sCardCollection: 32}}},
    dict(POISON, wram={hWhoseTurn: b"\xFF", wUppercaseHalfWidthLetters: b"\x00"},
         read={wUppercaseHalfWidthLetters: 1},
         sread={0: {sCardCollection: 32}}),
]
# <<< factory InitSaveDataAndSetUppercase

# >>> factory GameLoop
CONTRACT["GameLoop"] = {"compare": (), "preserve": ()}
CASES["GameLoop"] = [
    dict(oracle=True, evidence="primary", why="The no-button path performs GameLoop's bounded setup and then reaches the non-returning _GameLoop dispatch; copied text settings and the uppercase-width flag are observed before that dispatch.", wram={hKeysHeld: b"\x00", wTextSpeed: b"\xFF", wSkipDelayAllowed: b"\xFF", wUppercaseHalfWidthLetters: b"\xFF"}, sram={0: {sTextSpeed: b"\x02", sSkipDelayAllowed: b"\x01"}}, read={wTextSpeed: 1, wSkipDelayAllowed: 1, wUppercaseHalfWidthLetters: 1}, expect={wTextSpeed: b"\x02", wSkipDelayAllowed: b"\x01", wUppercaseHalfWidthLetters: b"\x01"}, instruction_budget=2000000, cycle_budget=8000000),
    dict(POISON, oracle=True, evidence="primary", why="With poisoned entry registers, the no-button setup still copies the selected SRAM settings and sets uppercase half-width letters before the non-returning _GameLoop dispatch.", wram={hKeysHeld: b"\x00", wTextSpeed: b"\xFF", wSkipDelayAllowed: b"\xFF", wUppercaseHalfWidthLetters: b"\xFF"}, sram={0: {sTextSpeed: b"\x06", sSkipDelayAllowed: b"\x00"}}, read={wTextSpeed: 1, wSkipDelayAllowed: 1, wUppercaseHalfWidthLetters: 1}, expect={wTextSpeed: b"\x06", wSkipDelayAllowed: b"\x00", wUppercaseHalfWidthLetters: b"\x01"}, instruction_budget=2000000, cycle_budget=8000000),
]
# <<< factory GameLoop

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "SetupResetBackUpRamScreen": {
        "source_symbol": "SetupResetBackUpRamScreen",
        "before": "wTileMapFill = 0;",
        "after": "wTileMapFill = 0xFF;",
        "case_ids": ["SetupResetBackUpRamScreen-0", "SetupResetBackUpRamScreen-1"],
    },
}
# >>> factory-mutation InitSaveDataAndSetUppercase
MUTATIONS["InitSaveDataAndSetUppercase"] = {"source_symbol": "InitSaveDataAndSetUppercase", "before": "\twUppercaseHalfWidthLetters = 1u;", "after": "\twUppercaseHalfWidthLetters = 0u;", "case_ids": ["InitSaveDataAndSetUppercase-0", "InitSaveDataAndSetUppercase-1"]}
# <<< factory-mutation InitSaveDataAndSetUppercase
# >>> factory-mutation GameLoop
MUTATIONS["GameLoop"] = {"source_symbol": "GameLoop", "before": "void GameLoop(void)\n{\n\tResetSerial();\n\tuint8_t interrupt_enable = gb_read8(rIE);\n\tgb_write8(rIE, (uint8_t)(interrupt_enable | IE_VBLANK));\n\tinterrupt_enable = gb_read8(rIE);\n\tgb_write8(rIE, (uint8_t)(interrupt_enable | IE_TIMER));\n\tEnableSRAM();\n\twTextSpeed = sTextSpeed;\n\twSkipDelayAllowed = sSkipDelayAllowed;\n\tDisableSRAM();\n\twUppercaseHalfWidthLetters = 1u;", "after": "void GameLoop(void)\n{\n\tResetSerial();\n\tuint8_t interrupt_enable = gb_read8(rIE);\n\tgb_write8(rIE, (uint8_t)(interrupt_enable | IE_VBLANK));\n\tinterrupt_enable = gb_read8(rIE);\n\tgb_write8(rIE, (uint8_t)(interrupt_enable | IE_TIMER));\n\tEnableSRAM();\n\twTextSpeed = sTextSpeed;\n\twSkipDelayAllowed = sSkipDelayAllowed;\n\tDisableSRAM();\n\twUppercaseHalfWidthLetters = 0u;", "case_ids": ["GameLoop-0", "GameLoop-1"]}
# <<< factory-mutation GameLoop
# >>> factory-completion GameLoop
for _record in SCHEMA2_CASES["GameLoop"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x66D1, "bank": 4}
# <<< factory-completion GameLoop
