/* >>> factory HandleEnergyBurn */
void HandleEnergyBurn(void)
{
	CardId card_id = deck_card_id(turn_duel_var(DUELVARS_ARENA_CARD));
	if (card_id != CHARIZARD)
		return;
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(0);
	if (incapable.f & 0x10u)
		return;
	for (uint8_t i = 0; i < NUM_COLORED_TYPES; i++)
		gb_write8((uint16_t)(wAttachedEnergies_ADDR + i), 0);
	gb_write8((uint16_t)(wAttachedEnergies_ADDR + FIRE), wTotalAttachedEnergies);
}
/* <<< factory HandleEnergyBurn */
