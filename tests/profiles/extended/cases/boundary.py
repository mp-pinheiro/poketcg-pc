EXTENDED_BOUNDARY_CASES = [
    {"name": "lookup-00fe", "card_id": 0x00FE, "valid": True},
    {"name": "lookup-00ff", "card_id": 0x00FF, "valid": True},
    {"name": "lookup-0100", "card_id": 0x0100, "valid": True},
    {"name": "lookup-01ff", "card_id": 0x01FF, "valid": True},
    {"name": "lookup-0200", "card_id": 0x0200, "valid": False},
    {"name": "collection-counts", "card_ids": [0x00FE, 0x00FF, 0x0100, 0x01FF]},
    {"name": "deck-compress-roundtrip", "card_ids": [0x00FE, 0x00FF, 0x0100, 0x01FF]},
    {"name": "deck-save-roundtrip", "card_ids": [0x00FE, 0x00FF, 0x0100, 0x01FF]},
    {"name": "card-page-graphics", "card_id": 0x01FF},
    {"name": "duel-high-card", "card_id": 0x01FF},
]
