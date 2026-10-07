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
	if (hKeysHeld != (PAD_A | PAD_B)) {
		for (;;)
			_GameLoop(); /* game_loop.asm:22-23 */
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
/* === factory CGBDisclaimer */
/* === factory SetupResetBackUpRamScreen */
