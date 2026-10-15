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
/* >>> factory GetNPCNameAndScript */
GetNPCNameAndScriptResult GetNPCNameAndScript(uint8_t a)
{
	GetNPCHeaderPointerResult header = GetNPCHeaderPointer(a);
	uint16_t cursor = (uint16_t)(header.hl + NPC_DATA_SCRIPT_PTR);
	const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, cursor);
	uint8_t script_low = entry[0];
	uint8_t script_high = entry[1];
	uint8_t name_low = entry[2];
	uint8_t name_high = entry[3];
	gb_write8(wCurrentNPCNameTx_ADDR, name_low);
	gb_write8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u), name_high);
	uint8_t f = (uint8_t)(header.f & 0x80u);
	if (((uint16_t)(header.hl & 0x0FFFu) + NPC_DATA_SCRIPT_PTR) > 0x0FFFu)
		f |= 0x20u;
	if ((uint32_t)header.hl + NPC_DATA_SCRIPT_PTR > 0xFFFFu)
		f |= 0x10u;
	return (GetNPCNameAndScriptResult){rom_ptr(NPC_HEADER_POINTERS_BANK, header.hl)[4], f, script_high, script_low};
}
/* <<< factory GetNPCNameAndScript */
