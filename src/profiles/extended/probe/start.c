/* --- factory ShowCardPopCGBDisclaimer */
/* >>> part probe_entries_start */
const ProbeEntry probe_entries_start[] = {
	{ "CheckIfHasSaveData", adapt_CheckIfHasSaveData },
	{ "PrintStartMenuDescriptionText", adapt_PrintStartMenuDescriptionText },
	{ "AskToContinueFromDiaryWithDuelData", adapt_AskToContinueFromDiaryWithDuelData },
	{ "HandleStartMenu", adapt_HandleStartMenu },
	{ "DrawPlayerPortraitAndPrintNewGameText", adapt_DrawPlayerPortraitAndPrintNewGameText },
	{ "DeleteSaveDataForNewGame", adapt_DeleteSaveDataForNewGame },
	{ "HandleTitleScreen", adapt_HandleTitleScreen },
	{ "Start", adapt_Start },
	{ NULL, NULL },
};
/* <<< part probe_entries_start */
