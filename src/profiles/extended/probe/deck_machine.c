/* --- factory EmptyScreenAndDrawTextBox */
/* --- factory PrintCardToSendText */
/* --- factory PrintReceivedTheseCardsText */
/* --- factory Func_b568 */
/* --- factory ShowReceivedCardsList */
/* --- factory Func_b088 */
/* --- factory PrinterMenu_DeckConfiguration */
/* --- factory GiftCenter_ReceiveCard */
/* --- factory GiftCenter_ReceiveDeck */
/* --- factory GiftCenter_SendCard */
/* --- factory GiftCenter_SendDeck */
/* --- factory HandleGiftCenter */
/* >>> part probe_entries_deck_machine */
const ProbeEntry probe_entries_deck_machine[] = {
	{ "CheckIfSelectedDeckMachineEntryIsEmpty", adapt_CheckIfSelectedDeckMachineEntryIsEmpty },
	{ "SafelySwitchToSRAM1", adapt_SafelySwitchToSRAM1 },
	{ "SafelySwitchToTempSRAMBank", adapt_SafelySwitchToTempSRAMBank },
	{ "CheckIfHasEnoughCardsToBuildDeck", adapt_CheckIfHasEnoughCardsToBuildDeck },
	{ "GetSavedDeckPointers", adapt_GetSavedDeckPointers },
	{ "GetSavedDeckCount", adapt_GetSavedDeckCount },
	{ "GetSelectedSavedDeckPtr", adapt_GetSelectedSavedDeckPtr },
	{ "SafelySwitchToSRAM0", adapt_SafelySwitchToSRAM0 },
	{ "DrawListScrollArrows", adapt_DrawListScrollArrows },
	{ "SetDeckMachineTitleText", adapt_SetDeckMachineTitleText },
	{ "FindFirstEmptyDeckSlot", adapt_FindFirstEmptyDeckSlot },
	{ "PrintNumSavedDecks", adapt_PrintNumSavedDecks },
	{ "CheckIfCanBuildSavedDeck", adapt_CheckIfCanBuildSavedDeck },
	{ "PrintDeckMachineEntry", adapt_PrintDeckMachineEntry },
	{ "TryDeleteSavedDeck", adapt_TryDeleteSavedDeck },
	{ "HandleDeckMissingCardsList", adapt_HandleDeckMissingCardsList },
	{ "HandleDismantleDeckToMakeSpace", adapt_HandleDismantleDeckToMakeSpace },
	{ "PrintVisibleDeckMachineEntries", adapt_PrintVisibleDeckMachineEntries },
	{ "ClearScreenAndDrawDeckMachineScreen", adapt_ClearScreenAndDrawDeckMachineScreen },
	{ "DrawDeckMachineScreen", adapt_DrawDeckMachineScreen },
	{ "HandleDeckMachineSelection", adapt_HandleDeckMachineSelection },
	{ "UpdateDeckMachineScrollArrowsAndEntries", adapt_UpdateDeckMachineScrollArrowsAndEntries },
	{ "SaveDeckInDeckSaveMachine", adapt_SaveDeckInDeckSaveMachine },
	{ "TryBuildDeckMachineDeck", adapt_TryBuildDeckMachineDeck },
	{ "HandleAutoDeckMenu", adapt_HandleAutoDeckMenu },
	{ "InitDeckMachineDrawingParams", adapt_InitDeckMachineDrawingParams },
	{ "HandleDeckSaveMachineMenu", adapt_HandleDeckSaveMachineMenu },
	{ NULL, NULL },
};
/* <<< part probe_entries_deck_machine */
