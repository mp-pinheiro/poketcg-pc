/* --- factory OneByteNumberToTxSymbol_PadSpace */
/* --- factory OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign */
/* === factory OneByteNumberToTxSymbol */
/* >>> factory OneByteNumberToTxSymbol_TrimLeadingZeros */
static void adapt_OneByteNumberToTxSymbol_TrimLeadingZeros(ProbeState *s)
{
	TxSymbolResult result = OneByteNumberToTxSymbol_TrimLeadingZeros(s->a);
	s->a = result.a;
	s->hl = result.hl;
}
/* <<< factory OneByteNumberToTxSymbol_TrimLeadingZeros */
/* >>> factory GetCardSymbolData */
static void adapt_GetCardSymbolData(ProbeState *s)
{
	uint8_t id = CardTypeToSymbolID();
	s->a = GetCardSymbolData();
	s->b = 0;
	s->c = (uint8_t)(id * 2);
	s->hl = (uint16_t)(0x20C5u + id * 2u);
}
/* <<< factory GetCardSymbolData */
/* --- part DrawWideTextBox_PrintTextNoDelay_Wait */
/* --- part DrawNarrowTextBox_WaitForInput */
/* --- factory Func_2827 */
/* --- factory ContinueDuel */
/* >>> part probe_entries_menus */
const ProbeEntry probe_entries_menus[] = {
	{ "InitializeCardListParameters", adapt_InitializeCardListParameters },
	{ "InitializeMenuParameters", adapt_InitializeMenuParameters },
	{ "SetMenuItem", adapt_SetMenuItem },
	{ "OneByteNumberToTxSymbol", adapt_OneByteNumberToTxSymbol },
	{ "OneByteNumberToTxSymbol_TrimLeadingZeros", adapt_OneByteNumberToTxSymbol_TrimLeadingZeros },
	{ "CardTypeToSymbolID", adapt_CardTypeToSymbolID },
	{ "GetCardSymbolData", adapt_GetCardSymbolData },
	{ "SetCursorParametersForTextBox", adapt_SetCursorParametersForTextBox },
	{ "SetCursorParametersForTextBox_Default", adapt_SetCursorParametersForTextBox_Default },
	{ "DrawCursor", adapt_DrawCursor },
	{ "EraseCursor", adapt_EraseCursor },
	{ "DrawCursor2", adapt_DrawCursor2 },
	{ "RefreshMenuCursor", adapt_RefreshMenuCursor },
	{ "DrawCardSymbol", adapt_DrawCardSymbol },
	{ "DrawNarrowTextBox", adapt_DrawNarrowTextBox },
	{ "DrawWideTextBox", adapt_DrawWideTextBox },
	{ "DrawNarrowTextBox_PrintTextNoDelay", adapt_DrawNarrowTextBox_PrintTextNoDelay },
	{ "DrawWideTextBox_PrintTextNoDelay", adapt_DrawWideTextBox_PrintTextNoDelay },
	{ "DrawWideTextBox_PrintText", adapt_DrawWideTextBox_PrintText },
	{ "PrintYesOrNoItems", adapt_PrintYesOrNoItems },
	{ "WaitForButtonAorB", adapt_WaitForButtonAorB },
	{ "DrawWideTextBox_WaitForInput", adapt_DrawWideTextBox_WaitForInput },
	{ "WaitForWideTextBoxInput", adapt_WaitForWideTextBoxInput },
	{ "RefreshMenuCursor_CheckPlaySFX", adapt_RefreshMenuCursor_CheckPlaySFX },
	{ "PlayOpenOrExitScreenSFX", adapt_PlayOpenOrExitScreenSFX },
	{ "DrawTextBox_PrintTextNoDelay", adapt_DrawTextBox_PrintTextNoDelay },
	{ "HandleYesOrNoMenu", adapt_HandleYesOrNoMenu },
	{ "CopyCardNameAndLevel", adapt_CopyCardNameAndLevel },
	{ "ReloadCardListItems", adapt_ReloadCardListItems },
	{ "PrintCardListItems", adapt_PrintCardListItems },
	{ "CardListMenuFunction", adapt_CardListMenuFunction },
	{ "HandleMenuInput", adapt_HandleMenuInput },
	{ "HandleCardListInput", adapt_HandleCardListInput },
	{ "HandleDuelMenuInput", adapt_HandleDuelMenuInput },
	{ "TwoItemHorizontalMenu", adapt_TwoItemHorizontalMenu },
	{ "YesOrNoMenu", adapt_YesOrNoMenu },
	{ "YesOrNoMenuWithText", adapt_YesOrNoMenuWithText },
	{ "YesOrNoMenuWithText_SetCursorToYes", adapt_YesOrNoMenuWithText_SetCursorToYes },
	{ "YesOrNoMenuWithText_LeftAligned", adapt_YesOrNoMenuWithText_LeftAligned },
	{ NULL, NULL },
};
/* <<< part probe_entries_menus */
