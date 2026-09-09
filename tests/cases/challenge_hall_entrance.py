"""Oracle-diff cases for poketcg/src/scripts/challenge_hall_entrance.asm."""
from tests.cases._fixtures import clerk9_fixture as _clerk9_fixture, CLERK9_REGS as _CLERK9_REGS

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

CONTRACT = {}
CASES = {}

# >>> factory Preload_Clerk9
CONTRACT["Preload_Clerk9"] = {"compare": ("a", "f", "b", "c", "d", "e", "hl"), "preserve": ("b", "d", "e")}
CASES["Preload_Clerk9"] = [
    {"a": 0x00, "f": 0x00, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x4567, "expect_regs": {"a": 0x00, "f": 0x90, "b": 0x11, "c": 0x22, "d": 0x33, "e": 0x44, "hl": 0x4567}},
    {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234, "expect_regs": {"a": 0x00, "f": 0x90, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}},
    # challenge-hall 635772: five medals with cup 2 not started; .five_medals readies cup 2
    # and falls into .four_medals, which closes cup 1 (wEventVars+$0e ends $E4).
    dict(_clerk9_fixture(vram=False, bank=3), **_CLERK9_REGS, read={0xD3E0: 1, 0xD3E2: 1, 0xD3E6: 1}),
    # The same entry with the medal flags changed: three medals ready cup 1 (.three_medals),
    # four close it (.four_medals), six close both (.more_than_five_medals), none takes the
    # .less_than_three_medals row, and all eight give the packs and take the same row.
    dict(_clerk9_fixture(vram=False, bank=3, **{"D3D2": b"\x0b"}), **_CLERK9_REGS, read={0xD3E0: 1, 0xD3E2: 1, 0xD3E6: 1}),
    dict(_clerk9_fixture(vram=False, bank=3, **{"D3D2": b"\x1b"}), **_CLERK9_REGS, read={0xD3E0: 1, 0xD3E2: 1, 0xD3E6: 1}),
    dict(_clerk9_fixture(vram=False, bank=3, **{"D3D2": b"\x7b"}), **_CLERK9_REGS, read={0xD3E0: 1, 0xD3E2: 1, 0xD3E6: 1}),
    dict(_clerk9_fixture(vram=False, bank=3, **{"D3D2": b"\x00"}), **_CLERK9_REGS, read={0xD3E0: 1, 0xD3E2: 1, 0xD3E6: 1}),
    dict(_clerk9_fixture(vram=False, bank=3, **{"D3D2": b"\xff"}), **_CLERK9_REGS, read={0xD3E0: 1, 0xD3E2: 1, 0xD3E6: 1}),
]
# <<< factory Preload_Clerk9

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {}
# >>> factory-mutation Preload_Clerk9
MUTATIONS["Preload_Clerk9"] = {"source_symbol": "Preload_Clerk9", "before": "\t\t\tresult.c = CHALLENGE_CUP_OVER;\n\t\t\tSetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);\n\t\t} else if (medals == 4u) {", "after": "\t\t} else if (medals == 4u) {", "case_ids": ["Preload_Clerk9-2"]}
# <<< factory-mutation Preload_Clerk9
