/* >>> factory FindExtraInteractableObjects */
FindExtraInteractableObjectsResult FindExtraInteractableObjects(uint16_t hl)
{
	uint16_t de = 6u;
	for (;;) {
		uint8_t a = gb_read8(hl);
		if (a == 0u)
			return (FindExtraInteractableObjectsResult){
				hl, 0u, 0u, (uint8_t)(de >> 8), (uint8_t)de, 0u};
		uint16_t entry_start = hl;
		if (gb_read8(wPlayerXCoord_ADDR) != gb_read8(hl))
			goto next;
		hl = (uint16_t)(hl + 1u);
		if (gb_read8(wPlayerYCoord_ADDR) != gb_read8(hl))
			goto next;
		hl = (uint16_t)(hl + 1u);
		if (gb_read8(wPlayerDirection_ADDR) != gb_read8(hl))
			goto next;
		hl = (uint16_t)(hl + 1u);
		uint8_t c = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t b = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t bank = gb_read8(hl);
		uint16_t next_hl = SetNextScript(bank, (uint16_t)(((uint16_t)b << 8) | c));
		return (FindExtraInteractableObjectsResult){
			next_hl, b, c, (uint8_t)(de >> 8), (uint8_t)de, 1u};
	next:
		hl = (uint16_t)(entry_start + de);
	}
}
/* <<< factory FindExtraInteractableObjects */
