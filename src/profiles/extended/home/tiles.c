/* --- factory Copy1bppTiles */
/* --- part V0_TILES0 */
/* --- part S_GFX_BUFFER1 */
/* --- part S_GFX_BUFFER4 */
/* --- part DUEL_DMG_SGB_SYMBOL_GFX_FAR */
/* --- part LOAD_FULL_WIDTH_FONT_TILES_SRC */
/* >>> factory LoadDuelCardSymbolTiles */
TileCopyResult LoadDuelCardSymbolTiles(void)
{
	uint16_t hl = DUEL_CGB_SYMBOL_GFX_FAR;
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x30u);
	return (TileCopyResult){hl, de};
}
/* <<< factory LoadDuelCardSymbolTiles */
/* >>> factory LoadDuelCardSymbolTiles2 */
TileCopyResult LoadDuelCardSymbolTiles2(void)
{
	uint16_t hl = (uint16_t)(DUEL_CGB_SYMBOL_GFX_FAR + 0x40u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x540u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x0Cu);
	return (TileCopyResult){hl, de};
}
/* <<< factory LoadDuelCardSymbolTiles2 */
/* >>> part load_duel_check_pokemon_tiles */
static TileCopyResult load_duel_check_pokemon_tiles(uint8_t b)
{
	uint16_t hl = (uint16_t)(DUEL_CGB_SYMBOL_GFX_FAR + 0x300u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, b);
	return (TileCopyResult){hl, de};
}
/* <<< part load_duel_check_pokemon_tiles */
/* >>> part load_deck_and_discard_pile_icons */
static TileCopyResult load_deck_and_discard_pile_icons(void)
{
	uint16_t hl = (uint16_t)(DUEL_CGB_SYMBOL_GFX_FAR + 0x540u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x30u);
	return (TileCopyResult){hl, de};
}
/* <<< part load_deck_and_discard_pile_icons */
/* --- factory Func_212f */
/* --- factory LoadFullWidthFontTiles */
/* --- factory Func_2057 */
/* --- factory Func_2051 */
/* --- factory Func_2055 */
/* --- factory Func_2046 */
/* --- factory Func_1f96 */
/* === factory LoadDeckAndDiscardPileIcons */
/* === factory LoadDuelCheckPokemonScreenTiles */
