"""Oracle-diff cases for poketcg/src/scripts/ishiharas_house.asm."""
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}
CONTRACT = {}
CASES = {}
# >>> factory Preload_NikkiInIshiharasHouse
CONTRACT["Preload_NikkiInIshiharasHouse"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_NikkiInIshiharasHouse"] = [{"wram": {0xD3DD: b"\x00"}}, {"wram": {0xD3DD: b"\x01"}}, dict(POISON, wram={0xD3DD: b"\x01"})]
# <<< factory Preload_NikkiInIshiharasHouse
# >>> factory Preload_IshiharaInIshiharasHouse
CONTRACT["Preload_IshiharaInIshiharasHouse"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_IshiharaInIshiharasHouse"] = [{"wram": {0xD3D7: b"\x00"}}, {"wram": {0xD3D7: b"\x40"}}, dict(POISON, wram={0xD3D7: b"\x48"})]
# <<< factory Preload_IshiharaInIshiharasHouse
# >>> factory Preload_Ronald1InIshiharasHouse
CONTRACT["Preload_Ronald1InIshiharasHouse"] = {"compare": ("a", "f"), "preserve": ()}
CASES["Preload_Ronald1InIshiharasHouse"] = [{"wram": {0xD3D8: b"\x00"}}, {"wram": {0xD3D8: b"\x02"}}, dict(POISON, wram={0xD3D8: b"\x02"})]
# <<< factory Preload_Ronald1InIshiharasHouse
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
MUTATIONS = {}
# >>> factory-mutation Preload_NikkiInIshiharasHouse
MUTATIONS["Preload_NikkiInIshiharasHouse"] = {"source_symbol": "Preload_NikkiInIshiharasHouse", "before": "uint8_t f = (a == NIKKI_IN_ISHIHARAS_HOUSE) ? 0x90u", "after": "uint8_t f = (a == 0x02u) ? 0x90u", "case_ids": ["Preload_NikkiInIshiharasHouse-1"]}
# <<< factory-mutation Preload_NikkiInIshiharasHouse
# >>> factory-mutation Preload_IshiharaInIshiharasHouse
MUTATIONS["Preload_IshiharaInIshiharasHouse"] = {"source_symbol": "Preload_IshiharaInIshiharasHouse", "before": "cp_flags(a, ISHIHARA_LEFT)", "after": "cp_flags(a, 0x09u)", "case_ids": ["Preload_IshiharaInIshiharasHouse-2"]}
# <<< factory-mutation Preload_IshiharaInIshiharasHouse
# >>> factory-mutation Preload_Ronald1InIshiharasHouse
MUTATIONS["Preload_Ronald1InIshiharasHouse"] = {"source_symbol": "Preload_Ronald1InIshiharasHouse", "before": "ccf_cp_flags(a, TRUE)", "after": "cp_flags(a, TRUE)", "case_ids": ["Preload_Ronald1InIshiharasHouse-1"]}
# <<< factory-mutation Preload_Ronald1InIshiharasHouse
