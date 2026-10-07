/* >>> part MasonLaboratoryAfterDuelTable */
#define MasonLaboratoryAfterDuelTable (MasonLaboratoryAfterDuel_ADDR + 0x06u)
/* <<< part MasonLaboratoryAfterDuelTable */
/* >>> factory Script_Tech1 */
/* mason_laboratory.asm:58-90. Two paths, each ending in its own `rst $20`:
 *   total >= 10 -> the `start_script` rst at $5597
 *   total <  10 -> .low_on_energies adds 10 of each of the six energy cards,
 *                  then reaches the rst at $55B5
 * The cases declare one completion pc each. Both paths are implemented here --
 * verifying only the counting prefix would be a simplification, not a port.
 *
 * EnergyCardList (03:55C4, six bytes 01..06) is walked by `ld a, [hli]`, so hl
 * ends at EnergyCardList.end = $55CA on both paths. The count loop keeps the
 * running total in b (`add b` / `ld b, a`) and is a do/while: `dec c` / `jr nz`
 * sits at the bottom, and c starts at 6.
 *
 * On the low path `push af` / `pop af` around AddCardToCollection restores the
 * card id every iteration, so `a` ends holding the LAST card id (6), while both
 * loop counters land on zero. */
ScriptTech1Result Script_Tech1(void)
{
	uint8_t b = 0u;
	uint8_t c = ENERGY_CARD_LIST_LEN;
	uint16_t hl = ENERGY_CARD_LIST;
	uint8_t a;

	do {
		const uint8_t *entry = rom_ptr(ENERGY_CARD_LIST_BANK, hl);
		CardId id = (CardId)(entry[0] | ((uint16_t)entry[1] << 8));
		hl = (uint16_t)(hl + 2u);
		a = GetCardCountInCollection(id).a;
		a = (uint8_t)(a + b);
		b = a;
		c--;
	} while (c != 0u);

	a = b;
	if (a >= 10u)
		return (ScriptTech1Result){a, b, c, hl};

	c = ENERGY_CARD_LIST_LEN;
	hl = ENERGY_CARD_LIST;
	do {
		b = 10u;
		const uint8_t *entry = rom_ptr(ENERGY_CARD_LIST_BANK, hl);
		CardId id = (CardId)(entry[0] | ((uint16_t)entry[1] << 8));
		hl = (uint16_t)(hl + 2u);
		a = (uint8_t)id;
		do {
			AddCardToCollection(id);
			b--;
		} while (b != 0u);
		c--;
	} while (c != 0u);
	return (ScriptTech1Result){a, b, c, hl};
}
/* <<< factory Script_Tech1 */
