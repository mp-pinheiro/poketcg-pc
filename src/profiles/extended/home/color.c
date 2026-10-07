/* --- part wConsolePaletteData_ADDR */
/* --- factory LoadConsolePaletteData */
/* >>> factory SetWhitePalettes */
void SetWhitePalettes(void)
{
	gb_write8(wBGP_ADDR, 0u);
	gb_write8(wOBP0_ADDR, 0u);
	gb_write8(wOBP1_ADDR, 0u);
	white_cgb(wBackgroundPalettesCGB_ADDR, 128u);
}
/* <<< factory SetWhitePalettes */
/* >>> factory FadePalIntoAnother_GetFadedColor */
FadeColorResult FadePalIntoAnother_GetFadedColor(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
    uint8_t red = fade_component((uint8_t)(c & 0x1f), (uint8_t)(e & 0x1f));
    uint8_t green = fade_component((uint8_t)(((c >> 5) & 7) | ((b & 3) << 3)), (uint8_t)(((e >> 5) & 7) | ((d & 3) << 3)));
    uint8_t blue = fade_component((uint8_t)((b >> 2) & 0x1f), (uint8_t)((d >> 2) & 0x1f));
    if (c != e || b != d) {
        /* color.asm:297,322 -- .unequal parks the faded red and the top two
         * green bits in HRAM scratch; a colour already at its target skips
         * the block and leaves both bytes as they were. */
        gb_write8(0xFFB6u, red);
        gb_write8(0xFFB7u, (uint8_t)((green >> 3) & 3));
    }
    FadeColorResult result;
    result.a = (uint8_t)(((green >> 3) & 3) | (blue << 2));
    result.c = (uint8_t)(red | ((green & 7) << 5));
    return result;
}
/* <<< factory FadePalIntoAnother_GetFadedColor */
/* >>> factory FadeScreenToWhite */
void FadeScreenToWhite(void)
{
	if (gb_read8(wLCDC_ADDR) & 0x80u) {
		gb_write8(wTempBGP_ADDR, 0u);
		gb_write8(wTempOBP0_ADDR, 0u);
		gb_write8(wTempOBP1_ADDR, 0u);
		white_cgb(wTempBackgroundPalettesCGB_ADDR, 128u);
		RestoreFirstColorInOBPals();
		FadeScreenToTempPals();
		DisableLCD();
		return;
	}
	gb_write8(wBGP_ADDR, 0u);
	gb_write8(wOBP0_ADDR, 0u);
	gb_write8(wOBP1_ADDR, 0u);
	white_cgb(wBackgroundPalettesCGB_ADDR, 128u);
	FlushAllPalettes();
}
/* <<< factory FadeScreenToWhite */
/* >>> factory Func_10d17 */
void Func_10d17(void)
{
	gb_write8(wTempBGP_ADDR, gb_read8(wBGP_ADDR));
	gb_write8(wTempOBP0_ADDR, gb_read8(wOBP0_ADDR));
	gb_write8(wTempOBP1_ADDR, gb_read8(wOBP1_ADDR));
	for (uint16_t i = 0u; i < 128u; i++)
		gb_write8((uint16_t)(wTempBackgroundPalettesCGB_ADDR + i),
			  gb_read8((uint16_t)(wBackgroundPalettesCGB_ADDR + i)));
	gb_write8(wBGP_ADDR, 0u);
	white_cgb(wBackgroundPalettesCGB_ADDR, 64u);
	FlushAllPalettes();
	gb_write8(wd317_ADDR, 0x10u);
}
/* <<< factory Func_10d17 */
/* >>> factory Func_10d50 */
void Func_10d50(void)
{
	gb_write8(wTempBGP_ADDR, 0u);
	gb_write8(wTempOBP0_ADDR, gb_read8(wOBP0_ADDR));
	gb_write8(wTempOBP1_ADDR, gb_read8(wOBP1_ADDR));
	white_cgb(wTempBackgroundPalettesCGB_ADDR, 64u);
	gb_write8(wd317_ADDR, 0x10u);
}
/* <<< factory Func_10d50 */
/* === factory FadeDMGPalettes */
