/* --- factory Copy1bppTiles */
/* --- factory Func_212f */
/* --- factory LoadFullWidthFontTiles */
/* --- factory Func_2057 */
/* --- factory Func_2051 */
/* --- factory Func_2055 */
/* --- factory Func_2046 */
/* --- factory Func_1f96 */
/* >>> part probe_entries_tiles */
const ProbeEntry probe_entries_tiles[] = {
	{ "FillRectangle", adapt_FillRectangle },
	{ "CopyFontsOrDuelGraphicsTiles", adapt_CopyFontsOrDuelGraphicsTiles },
	{ "LoadSymbolsFont", adapt_LoadSymbolsFont },
	{ "LoadCardSet2Tiles", adapt_LoadCardSet2Tiles },
	{ "LoadDuelDrawCardsScreenTiles", adapt_LoadDuelDrawCardsScreenTiles },
	{ "LoadCardOrDuelMenuBorderTiles", adapt_LoadCardOrDuelMenuBorderTiles },
	{ "LoadCardTypeHeaderTiles", adapt_LoadCardTypeHeaderTiles },
	{ "LoadDuelCardSymbolTiles", adapt_LoadDuelCardSymbolTiles },
	{ "LoadDuelCardSymbolTiles2", adapt_LoadDuelCardSymbolTiles2 },
	{ "LoadDuelFaceDownCardTiles", adapt_LoadDuelFaceDownCardTiles },
	{ "LoadDuelCheckPokemonScreenTiles", adapt_LoadDuelCheckPokemonScreenTiles },
	{ "LoadPlacingThePrizesScreenTiles", adapt_LoadPlacingThePrizesScreenTiles },
	{ "LoadDeckAndDiscardPileIcons", adapt_LoadDeckAndDiscardPileIcons },
	{ "LoadDuelCoinTossResultTiles", adapt_LoadDuelCoinTossResultTiles },
	{ "DrawDuelBoxMessage", adapt_DrawDuelBoxMessage },
	{ NULL, NULL },
};
/* <<< part probe_entries_tiles */
