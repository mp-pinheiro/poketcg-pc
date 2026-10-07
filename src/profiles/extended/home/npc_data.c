/* >>> factory LoadNPCSpriteData */
LoadNPCSpriteDataResult LoadNPCSpriteData(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	GetNPCHeaderPointerResult header = GetNPCHeaderPointer(a);
	const uint8_t *entry = rom_ptr(NPC_DATA_BANK, header.hl);
	wTempNPC = entry[0];
	wNPCSpriteID = entry[1];
	wNPCAnim = entry[2];
	wNPCAnimFlags = entry[3];
	return (LoadNPCSpriteDataResult){entry[3], header.f, b, c, d, e, hl};
}
/* <<< factory LoadNPCSpriteData */
/* --- factory _GetNPCDuelConfigurations */
/* === factory GetNPCNameAndScript */
