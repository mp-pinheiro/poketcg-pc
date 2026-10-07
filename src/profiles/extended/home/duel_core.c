/* >>> factory ConvertSpecialTrainerCardToPokemon */
/* core.asm:7123-7163. Entry: a = deck index (a duelvar offset), hl = wLoadedCard*
 * buffer, de = the card id. Overwrites a trainer card in the play area with a
 * generic colorless Pokemon (56 bytes from .trainer_to_pkmn_data). Exit contracts:
 *  - not a trainer:          a = card type, hl/de preserved
 *  - not in the play area:   a = 0, hl/de preserved
 *  - wrong id high byte:     a = d, hl/de preserved
 *  - overwrite:              a = last table byte, hl = buffer + $40, de preserved,
 *                            c = 0
 */
TrainerConvertResult ConvertSpecialTrainerCardToPokemon(uint8_t a, uint16_t hl, uint16_t de)
{
	uint8_t card_type = gb_read8(hl);
	if (card_type != TYPE_TRAINER)
		return (TrainerConvertResult){card_type, a, hl};

	uint8_t location = gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | a)) &
			   CARD_LOCATION_PLAY_AREA;
	if (!location)
		return (TrainerConvertResult){0, a, hl};

	uint8_t id_hi = (uint8_t)(de >> 8);
	uint8_t id_lo = (uint8_t)de;
	uint8_t mismatch;
	if (id_hi != (uint8_t)(MYSTERIOUS_FOSSIL >> 8))
		mismatch = id_hi;
	else
		mismatch = id_lo;
	if (de == MYSTERIOUS_FOSSIL)
		goto overwrite;
	if (de != CLEFAIRY_DOLL) {
		if (id_hi != (uint8_t)(CLEFAIRY_DOLL >> 8))
			mismatch = id_hi;
		else
			mismatch = id_lo;
		return (TrainerConvertResult){mismatch, a, hl};
	}
overwrite:

	const uint8_t *table = trainer_to_pkmn_data();
	gb_write8(hl, TYPE_PKMN_COLORLESS);
	for (uint8_t i = 0; i < (uint8_t)(CARD_DATA_AI_INFO - CARD_DATA_HP); i++)
		gb_write8((uint16_t)(hl + CARD_DATA_HP + i), table[i]);
	return (TrainerConvertResult){table[CARD_DATA_AI_INFO - CARD_DATA_HP - 1u],
				      0, (uint16_t)(hl + CARD_DATA_AI_INFO)};
}
/* <<< factory ConvertSpecialTrainerCardToPokemon */
/* >>> factory SetDefaultConsolePalettes */
void SetDefaultConsolePalettes(void)
{
	gb_write8(wTextBoxFrameType_ADDR, 1u);
	const uint8_t *src = rom_ptr(CGBDefaultPalettes_BANK, CGBDefaultPalettes_ADDR);
	for (uint8_t i = 0u; i < 40u; i++)
		gb_write8((uint16_t)(wBackgroundPalettesCGB_ADDR + i), src[i]);
	for (uint8_t i = 0u; i < 8u; i++)
		gb_write8((uint16_t)(wObjectPalettesCGB_ADDR + i), src[i]);
	FlushAllPalettes();
}
/* <<< factory SetDefaultConsolePalettes */
