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
	{ "OneByteNumberToTxSymbol_TrimLeadingZeros", adapt_OneByteNumberToTxSymbol_TrimLeadingZeros },
/* <<< part probe_entries_menus */
