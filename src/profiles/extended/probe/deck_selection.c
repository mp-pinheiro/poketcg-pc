/* --- factory CopyDeckFromSRAM */
/* --- factory Func_9001 */
/* >>> part probe_entries_deck_selection */
const ProbeEntry probe_entries_deck_selection[] = {
	{ "GetPointerToDeckCards", adapt_GetPointerToDeckCards },
	{ "ResetCheckMenuCursorPositionAndBlink", adapt_ResetCheckMenuCursorPositionAndBlink },
	{ "GetPointerToDeckName", adapt_GetPointerToDeckName },
	{ "InitDeckBuildingParams", adapt_InitDeckBuildingParams },
	{ "CheckIfCurDeckIsValid", adapt_CheckIfCurDeckIsValid },
	{ "CancelDeckSelectionSubMenu", adapt_CancelDeckSelectionSubMenu },
	{ "LoadHandCardsIcon", adapt_LoadHandCardsIcon },
	{ "InitPromotionalCardAndDeckCounterSaveData", adapt_InitPromotionalCardAndDeckCounterSaveData },
	{ "PrepareMenuGraphics", adapt_PrepareMenuGraphics },
	{ "EmptyScreenAndLoadFontDuelAndHandCardsIcons", adapt_EmptyScreenAndLoadFontDuelAndHandCardsIcons },
	{ "PrintThereIsNoDeckHereText", adapt_PrintThereIsNoDeckHereText },
	{ "WriteCardListsTerminatorBytes", adapt_WriteCardListsTerminatorBytes },
	{ "OpenDeckConfirmationMenu", adapt_OpenDeckConfirmationMenu },
	{ "HandleStartButtonInDeckSelectionMenu", adapt_HandleStartButtonInDeckSelectionMenu },
	{ "InputCurDeckName", adapt_InputCurDeckName },
	{ "DeckSelectionMenu", adapt_DeckSelectionMenu },
	{ "DeckSelectionSubMenu", adapt_DeckSelectionSubMenu },
	{ "DeckSelectionSubMenu_SelectOrCancel", adapt_DeckSelectionSubMenu_SelectOrCancel },
	{ NULL, NULL },
};
/* <<< part probe_entries_deck_selection */
