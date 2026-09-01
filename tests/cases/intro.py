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

# >>> factory-cases-statics
POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}
wd317 = 0xD317
wSequenceCmdPtr = 0xD631
wSequenceDelay = 0xD633
wIntroSequencePalsNeedUpdate = 0xD634
# <<< factory-cases-statics

# >>> factory PlayIntroSequence
CONTRACT["PlayIntroSequence"] = {"compare": (), "preserve": ()}
CASES["PlayIntroSequence"] = [
    dict(oracle=False, evidence="primary", why="The bounded intro prefix performs LCD/menu/palette setup, installs the intro command pointer, clears intro state, and stops immediately before the interactive command-frame loop.", wram={wSequenceCmdPtr: b"\x00\x00", wd317: b"\xFF", wIntroSequencePalsNeedUpdate: b"\xFF", wSequenceDelay: b"\xFF"}, read={wSequenceCmdPtr: 2, wd317: 1, wIntroSequencePalsNeedUpdate: 1, wSequenceDelay: 1}, expect={wSequenceCmdPtr: b"\x9D\x55", wd317: b"\x00", wIntroSequencePalsNeedUpdate: b"\x00", wSequenceDelay: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
    dict(POISON, oracle=False, evidence="primary", why="The bounded intro prefix writes the same command pointer and cleared state from poisoned entry registers before returning ahead of input handling.", wram={wSequenceCmdPtr: b"\x00\x00", wd317: b"\xFF", wIntroSequencePalsNeedUpdate: b"\xFF", wSequenceDelay: b"\xFF"}, read={wSequenceCmdPtr: 2, wd317: 1, wIntroSequencePalsNeedUpdate: 1, wSequenceDelay: 1}, expect={wSequenceCmdPtr: b"\x9D\x55", wd317: b"\x00", wIntroSequencePalsNeedUpdate: b"\x00", wSequenceDelay: b"\x00"}, instruction_budget=20000000, cycle_budget=80000000),
]
# <<< factory PlayIntroSequence

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
# >>> factory-mutation PlayIntroSequence
MUTATIONS["PlayIntroSequence"] = {"source_symbol": "PlayIntroSequence", "before": "void PlayIntroSequence(void)\n{\n\tDisableLCD();\n\tLoadConsolePaletteData();\n\t(void)InitMenuScreen();\n\tEnableAndClearSpriteAnimations();\n\tPlaySong(MUSIC_TITLESCREEN);", "after": "void PlayIntroSequence(void)\n{\n\tDisableLCD();\n\tLoadConsolePaletteData();\n\t(void)InitMenuScreen();\n\tEnableAndClearSpriteAnimations();\n\tPlaySong(0x00u);", "case_ids": ["PlayIntroSequence-0", "PlayIntroSequence-1"]}
# <<< factory-mutation PlayIntroSequence
# >>> factory-completion PlayIntroSequence
for _record in SCHEMA2_CASES["PlayIntroSequence"]:
    _record["completion"] = {"mode": "pre-ret", "pc": 0x5364, "bank": 7}
# <<< factory-completion PlayIntroSequence
