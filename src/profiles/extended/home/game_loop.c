
/* >>> factory GameLoop */
void GameLoop(void)
{
	uint8_t interrupt_enable = gb_read8(rIE);
	gb_write8(rIE, (uint8_t)(interrupt_enable | IE_VBLANK));
	interrupt_enable = gb_read8(rIE);
	gb_write8(rIE, (uint8_t)(interrupt_enable | IE_TIMER));
	EnableSRAM();
	wTextSpeed = sTextSpeed;
	wSkipDelayAllowed = sSkipDelayAllowed;
	DisableSRAM();
	wUppercaseHalfWidthLetters = 1u;
	if (wConsole != 2u)
		CGBDisclaimer();
	if (hKeysHeld != (PAD_A | PAD_B)) {
		for (;;)
			_GameLoop();
	}

	SetupResetBackUpRamScreen();
	EmptyScreen();
	HandleYesOrNoMenuResult menu = YesOrNoMenuWithText(ResetBackUpRamText);
	if ((menu.f & 0x10u) == 0u) {
		EnableSRAM();
		s0a000 = 0u;
		DisableSRAM();
	}
	(void)Reset(); /* .reset_game: jp Reset (game_loop.asm:35-36) */
}
/* <<< factory GameLoop */
/* === factory SetupResetBackUpRamScreen */

/* >>> factory CGBDisclaimer */
void CGBDisclaimer(void)
{
	wTileMapFill = 0u;
	DisableLCD();
	(void)LoadSymbolsFont();
	SetDefaultPalettes();
	(void)SetupText(0x38u, 0x7Fu);
	EmptyScreen();
	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 7u, 0u, 11u);
	InitTextPrinting(4u, 13u);
	(void)PrintTextNoDelay(ExclusiveToGameBoyColorsText, 4u, 13u);
	EnableLCD();
	for (;;)
		DoFrame();
}
/* <<< factory CGBDisclaimer */
