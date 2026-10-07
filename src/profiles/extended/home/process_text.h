/* === factory GetTextLengthInTiles */
/* >>> part FullWidthOffsetResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} FullWidthOffsetResult;
/* <<< part FullWidthOffsetResult */
/* >>> factory GetFullWidthFontTileOffset */
FullWidthOffsetResult GetFullWidthFontTileOffset(uint8_t d, uint8_t e);
/* <<< factory GetFullWidthFontTileOffset */
/* --- factory TwoByteNumberToTxSymbol_PadSpace */
/* === part NumberTextResult */
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
NumberTextResult TwoByteNumberToTxSymbol_TrimLeadingZeros(uint16_t hl);
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
/* --- part InitTextPrinting_ProcessText */
