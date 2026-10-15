/* >>> part GETCARDPTR_BOUND */
#define GETCARDPTR_BOUND ((uint16_t)(CARD_POINTERS + 3u * (NUM_CARDS + 1u)))
/* <<< part GETCARDPTR_BOUND */
/* >>> part get_card_pointer */
static CardPtrResult get_card_pointer(CardId cardid)
{
	uint16_t entry = (uint16_t)(CARD_POINTERS + (uint16_t)cardid * 3u);
	if (entry >= GETCARDPTR_BOUND)
		return (CardPtrResult){entry, 1u, 0u};
	uint8_t saved = hBankROM;
	BankswitchROM(BANK_CARD_DATA);
	uint8_t lo = gb_read8(entry);
	uint8_t hi = gb_read8((uint16_t)(entry + 1u));
	uint8_t bank = gb_read8((uint16_t)(entry + 2u));
	BankswitchROM(saved);
	return (CardPtrResult){(uint16_t)(lo | (uint16_t)hi << 8), 0u, bank};
}
/* <<< part get_card_pointer */
/* >>> factory GetCardType */
/* card_data.asm:84-96 */
uint8_t GetCardType(CardId e)
{
	CardPtrResult pointer = get_card_pointer(e);
	if (pointer.carry)
		return hBankROM;
	return rom_ptr(pointer.bank, pointer.hl)[CARD_DATA_TYPE];
}
/* <<< factory GetCardType */
/* >>> factory GetCardName */
uint16_t GetCardName(CardId e)
{
	CardPtrResult pointer = get_card_pointer(e);
	if (pointer.carry)
		return e;
	const uint8_t *p = rom_ptr(pointer.bank, pointer.hl) + CARD_DATA_NAME;
	return (uint16_t)(p[0] | (uint16_t)p[1] << 8);
}
/* <<< factory GetCardName */
/* >>> factory GetCardTypeRarityAndSet */
CardTRS GetCardTypeRarityAndSet(CardId a)
{
	CardPtrResult pointer = get_card_pointer(a);
	if (pointer.carry)
		return (CardTRS){hBankROM, 0u, 0u, 1u};
	const uint8_t *p = rom_ptr(pointer.bank, pointer.hl);
	return (CardTRS){p[CARD_DATA_TYPE], p[CARD_DATA_RARITY], p[CARD_DATA_SET], 0u};
}
/* <<< factory GetCardTypeRarityAndSet */
/* --- factory CopyFontsOrDuelGraphicsTiles2 */
/* === factory GetCardPointer */
/* === factory LoadCardDataToBuffer1_FromName */
/* === factory LoadCardDataToHL_FromCardID */
/* === factory LoadCardGfx */
