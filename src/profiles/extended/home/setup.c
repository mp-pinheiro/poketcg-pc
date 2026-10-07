/* >>> factory SetupPalettes */
SetupPalettesResult SetupPalettes(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	uint8_t a = 0xE4u; /* ldgbpal a, SHADE_WHITE, SHADE_LIGHT, SHADE_DARK, SHADE_BLACK */

	gb_write8(rBGP, a);
	gb_write8(wBGP_ADDR, a);
	gb_write8(rOBP0, a);
	gb_write8(rOBP1, a);
	gb_write8(wOBP0_ADDR, a);
	gb_write8(wOBP1_ADDR, a);
	gb_write8(wFlushPaletteFlags_ADDR, 0);

	if (gb_read8(wConsole_ADDR) != CONSOLE_CGB)
		return (SetupPalettesResult){b, c, d, e, 0xCABEu};

	uint16_t de = wBackgroundPalettesCGB_ADDR;
	for (uint8_t i = 16; i != 0; i--) {
		for (uint8_t j = 0; j < PAL_SIZE; j++)
			gb_write8(de++, gb_read8((uint16_t)(INITIAL_PALETTE_ADDR + j)));
	}
	FlushAllCGBPalettesResult r = FlushAllCGBPalettes();
	return (SetupPalettesResult){r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory SetupPalettes */
/* === factory DetectConsole */
