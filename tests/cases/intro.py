POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

W_TITLE_SCREEN_SPRITES = 0xD629
W_SPRITE_ANIM_BUFFER = 0xD4D0
READS = {
    W_TITLE_SCREEN_SPRITES: 7,
    W_SPRITE_ANIM_BUFFER + 1: 1,
    W_SPRITE_ANIM_BUFFER + 4: 1,
    W_SPRITE_ANIM_BUFFER + 17: 1,
    W_SPRITE_ANIM_BUFFER + 20: 1,
    W_SPRITE_ANIM_BUFFER + 33: 1,
    W_SPRITE_ANIM_BUFFER + 36: 1,
    W_SPRITE_ANIM_BUFFER + 49: 1,
    W_SPRITE_ANIM_BUFFER + 52: 1,
    W_SPRITE_ANIM_BUFFER + 65: 1,
    W_SPRITE_ANIM_BUFFER + 68: 1,
    W_SPRITE_ANIM_BUFFER + 81: 1,
    W_SPRITE_ANIM_BUFFER + 84: 1,
    W_SPRITE_ANIM_BUFFER + 97: 1,
    W_SPRITE_ANIM_BUFFER + 100: 1,
}

CONTRACT = {
    "LoadTitleScreenSprites": {"compare": (), "preserve": ()},
}

CASES = {
    "LoadTitleScreenSprites": [
        {"read": READS},
        dict(POISON, read=READS),
    ],
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "LoadTitleScreenSprites": {
        "source_symbol": "LoadTitleScreenSprites",
        "before": "gb_write8(property, (uint8_t)(gb_read8(property) | index));",
        "after": "gb_write8(property, (uint8_t)(gb_read8(property) | (uint8_t)(index + 1u)));",
        "case_ids": ["LoadTitleScreenSprites-0", "LoadTitleScreenSprites-1"],
    },
}
