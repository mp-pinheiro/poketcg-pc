/* >>> factory GetFullWidthFontTileOffset */
static void adapt_GetFullWidthFontTileOffset(ProbeState *s)
{
	FullWidthOffsetResult out = GetFullWidthFontTileOffset(s->d, s->e);
	s->a = out.a;
	s->b = out.b;
	s->c = out.c;
	s->d = out.d;
	s->e = out.e;
	s->hl = out.hl;
}
/* <<< factory GetFullWidthFontTileOffset */
/* --- factory TwoByteNumberToTxSymbol_PadSpace */
/* === factory GenerateTextTile */
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
static void adapt_TwoByteNumberToTxSymbol_TrimLeadingZeros(ProbeState *s)
{
	NumberTextResult out = TwoByteNumberToTxSymbol_TrimLeadingZeros(s->hl);
	s->a = out.a;
	s->hl = out.hl;
}
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
/* --- part adapt_InitTextPrinting_ProcessText_decl */
/* >>> part probe_entries_process_text */
	{ "TwoByteNumberToTxSymbol_TrimLeadingZeros", adapt_TwoByteNumberToTxSymbol_TrimLeadingZeros },
/* <<< part probe_entries_process_text */
/* --- part InitTextPrinting_ProcessText */
