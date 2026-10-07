/* --- factory DrawPlayersPrizeAndBenchCards */
/* >>> part probe_entries_duel_menus */
const ProbeEntry probe_entries_duel_menus[] = {
	{ "DrawPlayAreaToPlacePrizeCards", adapt_DrawPlayAreaToPlacePrizeCards },
	{ "DrawYourOrOppPlayAreaScreen_Bank0", adapt_DrawYourOrOppPlayAreaScreen_Bank0 },
	{ "DrawAIPeekScreen", adapt_DrawAIPeekScreen },
	{ "SelectPrizeCards", adapt_SelectPrizeCards },
	{ "HandlePeekSelection", adapt_HandlePeekSelection },
	{ "OpenDuelCheckMenu", adapt_OpenDuelCheckMenu },
	{ "OpenInPlayAreaScreen_FromSelectButton", adapt_OpenInPlayAreaScreen_FromSelectButton },
	{ NULL, NULL },
};
/* <<< part probe_entries_duel_menus */
