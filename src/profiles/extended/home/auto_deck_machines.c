/* >>> factory ReadAutoDeckConfiguration */
void ReadAutoDeckConfiguration(void)
{
	EnableSRAM();
	uint8_t machine = wCurAutoDeckMachine;
	uint16_t hl = (uint16_t)(HtimesL((uint16_t)(((uint16_t)(6u * NUM_DECK_MACHINE_SLOTS) << 8) | machine)) + AUTO_DECK_MACHINE_ENTRIES);

	for (uint8_t b = 0u; b < NUM_DECK_MACHINE_SLOTS; b++) {
		uint16_t deck_de = (uint16_t)(HtimesL((uint16_t)(((uint16_t)DECK_COMPRESSED_STRUCT_SIZE << 8) | b)) + sAutoDecks_ADDR);
		const uint8_t *entry_ptr = rom_ptr(AUTO_DECK_MACHINES_BANK, hl);
		uint16_t src_de = (uint16_t)(entry_ptr[0] | ((uint16_t)entry_ptr[1] << 8));
		uint16_t cards = wCurDeckCards_ADDR;
		for (;;) {
			uint8_t count = rom_ptr(AUTO_DECK_MACHINES_BANK, src_de++)[0];
			if (count == 0u)
				break;
			uint8_t low = rom_ptr(AUTO_DECK_MACHINES_BANK, src_de++)[0];
			uint8_t high = rom_ptr(AUTO_DECK_MACHINES_BANK, src_de++)[0];
			while (count-- != 0u) {
				gb_write8(cards++, low);
				gb_write8(cards++, high);
			}
		}
		gb_write8(cards++, 0u);
		gb_write8(cards, 0u);
		CompressDeckToSRAM(wCurDeckCards_ADDR,
			(uint16_t)(deck_de + DECK_NAME_SIZE));
		hl = (uint16_t)(hl + 2u);

		entry_ptr = rom_ptr(AUTO_DECK_MACHINES_BANK, hl);
		uint16_t text_id = (uint16_t)(entry_ptr[0] | ((uint16_t)entry_ptr[1] << 8));
		(void)CopyText(text_id, wDismantledDeckName_ADDR);
		uint16_t name_hl = deck_de;
		uint16_t name_de = wDismantledDeckName_ADDR;
		for (;;) {
			uint8_t ch = gb_read8(name_de);
			gb_write8(name_hl++, ch);
			if (ch == 0u)
				break;
			name_de++;
		}
		hl = (uint16_t)(hl + 2u);

		entry_ptr = rom_ptr(AUTO_DECK_MACHINES_BANK, hl);
		uint16_t desc_addr = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR + (uint16_t)b * 2u);
		gb_write8(desc_addr, entry_ptr[0]);
		gb_write8((uint16_t)(desc_addr + 1u), entry_ptr[1]);
		hl = (uint16_t)(hl + 2u);
	}

	DisableSRAM();
}
/* <<< factory ReadAutoDeckConfiguration */
