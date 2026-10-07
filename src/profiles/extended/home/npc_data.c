/* >>> factory GetNPCHeaderPointer */
GetNPCHeaderPointerResult GetNPCHeaderPointer(uint8_t a)
{
	uint8_t rotated = (uint8_t)((a << 1) | (a >> 7));
	uint8_t low_address = (uint8_t)(NPC_HEADER_POINTERS_ADDR + rotated);
	uint8_t base_high = (uint8_t)(NPC_HEADER_POINTERS_ADDR >> 8);
	uint8_t carry = (uint8_t)(low_address < (uint8_t)NPC_HEADER_POINTERS_ADDR);
	uint8_t high_address = (uint8_t)(base_high + carry);
	uint16_t table_address = (uint16_t)(((uint16_t)high_address << 8) | low_address);
	const uint8_t *entry = rom_ptr(NPC_HEADER_POINTERS_BANK, table_address);
	uint8_t pointer_low = entry[0];
	uint8_t pointer_high = entry[1];
	uint16_t pointer = (uint16_t)(pointer_low | ((uint16_t)pointer_high << 8));
	uint8_t f = 0;
	if (high_address == 0u)
		f |= 0x80u;
	if ((uint8_t)((base_high & 0x0Fu) + carry) > 0x0Fu)
		f |= 0x20u;
	if ((uint16_t)base_high + carry > (uint16_t)0xFFu)
		f |= 0x10u;
	return (GetNPCHeaderPointerResult){pointer, pointer_low, f};
}
/* <<< factory GetNPCHeaderPointer */
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
