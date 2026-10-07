/* === factory LoadDeck */
/* >>> factory CompressDeckToSRAM */
void CompressDeckToSRAM(uint16_t de, uint16_t hl)
{
	uint16_t source = de;
	uint16_t destination = hl;
	for (uint8_t block = 0u; block < 7u; block++) {
		uint8_t command = 0u;
		uint16_t look = source;
		for (uint8_t bit = 0u; bit < 8u; bit++) {
			uint8_t high = gb_read8((uint16_t)(look + 1u));
			look = (uint16_t)(look + 2u);
			command = (uint8_t)((command << 1) | (high & 0x01u));
		}
		gb_write8(destination++, command);
		for (uint8_t card = 0u; card < 8u; card++) {
			gb_write8(destination++, gb_read8(source));
			source = (uint16_t)(source + 2u);
		}
	}
	uint8_t command = 0u;
	uint16_t look = source;
	for (uint8_t bit = 0u; bit < 4u; bit++) {
		uint8_t high = gb_read8((uint16_t)(look + 1u));
		look = (uint16_t)(look + 2u);
		command = (uint8_t)((command << 1) | (high & 0x01u));
	}
	gb_write8(destination++, (uint8_t)(command << 4));
	for (uint8_t card = 0u; card < 4u; card++) {
		gb_write8(destination++, gb_read8(source));
		source = (uint16_t)(source + 2u);
	}
}
/* <<< factory CompressDeckToSRAM */
/* >>> factory DecompressSRAMDeck */
void DecompressSRAMDeck(uint16_t de, uint16_t hl)
{
	uint16_t source = de;
	uint16_t destination = hl;
	wDecompSavedDeckCount = DECK_SIZE;
	for (;;) {
		uint8_t command = gb_read8(source++);
		for (uint8_t bit = 0u; bit < 8u; bit++) {
			gb_write8(destination++, gb_read8(source++));
			gb_write8(destination++, (uint8_t)(command >> 7));
			command = (uint8_t)(command << 1);
			wDecompSavedDeckCount = (uint8_t)(wDecompSavedDeckCount - 1u);
			if (wDecompSavedDeckCount == 0u)
				return;
		}
	}
}
/* <<< factory DecompressSRAMDeck */
