/* >>> factory TwoByteNumberToText_CountLeadingZeros */
/* Contract fields are b, c, d, e, hl. b is preserved on both paths; c and de are
 * preserved on the full-width path only, so they come in to be echoed back out. */
LeadingZerosResult TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint8_t c, uint16_t de)
{
	/* `jp z` is a tail call, and TwoByteNumberToTxSymbol_TrimLeadingZeros pushes and pops both bc and de. */
	if (wFontWidth == 0)
		return (LeadingZerosResult){c, de, TwoByteNumberToTxSymbol_TrimLeadingZeros(value).hl};

	de = wStringBuffer_ADDR;
	TwoByteNumberToText(value, &de); /* leaves de on the TX_END slot, five bytes along */

	uint16_t hl = wStringBuffer_ADDR;

	c = 4;
	while (gb_read8(hl) == '0') {
		hl++;
		if (--c == 0)
			break;
	}
	return (LeadingZerosResult){c, de, hl};
}
/* <<< factory TwoByteNumberToText_CountLeadingZeros */
