/* >>> factory LoadTitleScreenSprites */
void LoadTitleScreenSprites(void)
{
    static const uint8_t sprites[] = {
        SPRITE_GRASS, SPRITE_FIRE, SPRITE_WATER, SPRITE_COLORLESS,
        SPRITE_LIGHTNING, SPRITE_PSYCHIC, SPRITE_FIGHTING
    };
    uint16_t destination = wTitleScreenSprites_ADDR;

    gb_write8(wWhichOBP_ADDR, 0);
    gb_write8(wWhichOBPalIndex_ADDR, 0);
    LoadOBPalette(PALETTE_30);

    for (uint8_t index = 0; index < sizeof(sprites); index++) {
        CreateSpriteAndAnimBufferEntry(sprites[index], 0);
        gb_write8(destination, gb_read8(wWhichSprite_ADDR));
        destination++;
        uint16_t property = GetFirstSpriteAnimBufferProperty();
        property++;
        gb_write8(property, (uint8_t)(gb_read8(property) | index));
    }
}
/* <<< factory LoadTitleScreenSprites */
/* >>> factory PlayIntroSequence */
void PlayIntroSequence(void)
{
	(void)InitMenuScreen();
	EnableAndClearSpriteAnimations();
	(void)SetDoFrameFunction(HANDLE_ALL_SPRITE_ANIMATIONS);
	LoadTitleScreenSprites();

	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)(INTRO_SEQUENCE & 0xffu));
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u), (uint8_t)(INTRO_SEQUENCE >> 8));
	wd317 = 0u;
	wIntroSequencePalsNeedUpdate = 0u;
	wSequenceDelay = 0u;
	(void)FlashWhiteScreen();
	if (!frame_boundary_is_installed()) {
		DoFrameIfLCDEnabled();
		EnableLCD();
		return;
	}

	for (;;) {
		DoFrameIfLCDEnabled();
		(void)UpdateRNGSources();
		if ((hKeysPressed & (PAD_A | PAD_START)) != 0u) {
			if (AssertSongFinished() == 0u) {
				DisableLCD();
				PlaySong(MUSIC_TITLESCREEN);
				/* intro.asm:45-47 is the home LoadScene, not the
				 * sequence command LoadOpeningScene: that one also
				 * whites the palettes through Func_10d17 and advances
				 * wSequenceCmdPtr, neither of which the skip does. */
				(void)LoadScene(SCENE_TITLE_SCREEN, 0u, 0u, 0u, 0u, 0u, 0u);
				IntroSequenceEmptyFunc();
			}
			break;
		}
		if (wIntroSequencePalsNeedUpdate != 0u)
			Func_10d74();
		uint8_t saved_bank = hBankROM;
		BankswitchROM(7u);
		(void)ExecuteIntroSequenceCmd();
		BankswitchROM(saved_bank);
		if (wSequenceDelay == 0xFFu)
			break;
	}
	EnableAndClearSpriteAnimations();
	ShowPressStart(); /* intro.asm:51 .ShowPressStart */
	EnableLCD();
}
/* <<< factory PlayIntroSequence */
