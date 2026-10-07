/* >>> factory SetDefaultPalettes */
void SetDefaultPalettes(void)
{
	gb_write8(wBGP_ADDR, 0xE4u);
	gb_write8(wOBP0_ADDR, 0xE4u);
	gb_write8(wOBP1_ADDR, 0xE4u);
	gb_write8(wTextBoxFrameType_ADDR, 1);
	uint8_t bank = gb_read8(hBankROM_ADDR);
	BankswitchROM(1);
	SetDefaultConsolePalettes();
	BankswitchROM(bank);
	FlushAllPalettes();
}
/* <<< factory SetDefaultPalettes */
