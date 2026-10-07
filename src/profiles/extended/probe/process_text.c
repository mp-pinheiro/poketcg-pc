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
const ProbeEntry probe_entries_process_text[] = {
	{"InitTextFormat", adapt_InitTextFormat},
	{"CaseHalfWidthLetter", adapt_CaseHalfWidthLetter},
	{"ClassifyTextCharacterPair", adapt_ClassifyTextCharacterPair},
	{"GetTextLengthInHalfTiles", adapt_GetTextLengthInHalfTiles},
	{"GetTextLengthInTiles", adapt_GetTextLengthInTiles},
	{"GetFullWidthFontTileOffset", adapt_GetFullWidthFontTileOffset},
	{"ConvertTileNumberToTileDataAddress", adapt_ConvertTileNumberToTileDataAddress},
	{"CopyHalfWidthCharacterToDE", adapt_CopyHalfWidthCharacterToDE},
	{"CreateHalfWidthFontTile", adapt_CreateHalfWidthFontTile},
	{"CreateFullWidthFontTile", adapt_CreateFullWidthFontTile},
	{"CreateFullWidthFontTile_ConvertToTileDataAddress", adapt_CreateFullWidthFontTile_ConvertToTileDataAddress},
	{"GenerateTextTile", adapt_GenerateTextTile},
	{"TwoByteNumberToTxSymbol_TrimLeadingZeros", adapt_TwoByteNumberToTxSymbol_TrimLeadingZeros},
	{"ProcessText", adapt_ProcessText},
	{"SetupText", adapt_SetupText},
	{"InitTextPrinting", adapt_InitTextPrinting},
	{"InitTextPrintingInTextbox", adapt_InitTextPrintingInTextbox},
	{"PlaceNextTextTile", adapt_PlaceNextTextTile},
	{"ProcessSpecialTextCharacter", adapt_ProcessSpecialTextCharacter},
	{"TerminateHalfWidthText", adapt_TerminateHalfWidthText},
	{"Func_235e", adapt_Func_235e},
	{"Func_2325", adapt_Func_2325},
	{"Func_22ca", adapt_Func_22ca},
	{"CopyTextData", adapt_CopyTextData},
	{NULL, NULL},
};
/* <<< part probe_entries_process_text */
/* --- part InitTextPrinting_ProcessText */
