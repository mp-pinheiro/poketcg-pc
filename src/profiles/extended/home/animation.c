/* >>> factory DoMapOWFrame */
void DoMapOWFrame(void)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(MapOWFramesetPointers_BANK);
	uint8_t map = gb_read8(wCurMap_ADDR);
	uint8_t c = (uint8_t)(map * 2u);

	const uint8_t *p = rom_ptr(MAP_OW_FRAMESET_POINTERS_BANK,
		(uint16_t)(MAP_OW_FRAMESET_POINTERS_ADDR + c));
	uint16_t hl = (uint16_t)(p[0] | (uint16_t)p[1] << 8);
	ProcessOWFrameset(hl);
	BankswitchROM(saved_bank);
}
/* <<< factory DoMapOWFrame */
