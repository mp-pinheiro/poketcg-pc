"""Oracle-diff cases for poketcg/src/engine/sequences/intro_sequence_commands.asm."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory AnimateRandomTitleScreenOrb
CONTRACT["AnimateRandomTitleScreenOrb"] = {"compare": ("a", "b"), "preserve": ("b",)}
CASES["AnimateRandomTitleScreenOrb"] = [
    {"wram": {0xD635: b"\x01", 0xCAB4: b"\x00"}, "read": {0xD4CF: 1}},
    {"wram": {0xD635: b"\x3F", 0xCAB4: b"\x00"}, "read": {0xD4CF: 1}},
    {"wram": {0xD635: b"\xFF", 0xCAB4: b"\x00"}, "read": {0xD4CF: 1}},
    {"wram": {0xD635: b"\x01", 0xCAB4: b"\x02", 0xD629: b"\x00\x01\x02\x03\x04\x05\x06"},
     "read": {0xD4CF: 1}},
    dict(POISON, wram={0xD635: b"\x3F", 0xCAB4: b"\x02", 0xD629: b"\x06\x05\x04\x03\x02\x01\x00"},
         read={0xD4CF: 1}),
]
# <<< factory AnimateRandomTitleScreenOrb

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation AnimateRandomTitleScreenOrb
MUTATIONS["AnimateRandomTitleScreenOrb"] = {
    "source_symbol": "AnimateRandomTitleScreenOrb",
    "before": "\tuint8_t a = (uint8_t)(wTitleScreenOrbCounter & ORB_COUNTER_MASK);",
    "after": "\tuint8_t a = (uint8_t)(wTitleScreenOrbCounter & 0x1fu);",
    "case_ids": ["AnimateRandomTitleScreenOrb-1", "AnimateRandomTitleScreenOrb-2", "AnimateRandomTitleScreenOrb-4"],
}
# <<< factory-mutation AnimateRandomTitleScreenOrb
