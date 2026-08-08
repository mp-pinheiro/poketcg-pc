#include "home/duel_core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#define TYPE_TRAINER 0x10u
#define TYPE_PKMN_COLORLESS 0x06u
#define CARD_LOCATION_PLAY_AREA 0x10u
#define CARD_DATA_HP 0x08u
#define CARD_DATA_AI_INFO 0x40u
#define TRAINER_TO_PKMN_DATA 0x6db9u /* bank 1 */
#define MYSTERIOUS_FOSSIL 0xccu
#define CLEFAIRY_DOLL 0xcbu

static const uint8_t *trainer_to_pkmn_data(void)
{
	return rom_ptr(1u, TRAINER_TO_PKMN_DATA);
}

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

	/* core.asm:7136-7148. `cp` never modifies a, so the fossil check falls through
	 * with a = e; the second `cp CLEFAIRY_DOLL; ret nz` exits with a = e whenever
	 * e is neither doll nor fossil. Only the fossil-with-nonzero-high path exits
	 * with a = d. */
	uint8_t id_hi = (uint8_t)(de >> 8);
	uint8_t id_lo = (uint8_t)de;
	if (id_lo == MYSTERIOUS_FOSSIL) {
		if (id_hi != 0)
			return (TrainerConvertResult){id_hi, a, hl};
	} else {
		if (id_lo != CLEFAIRY_DOLL)
			return (TrainerConvertResult){id_lo, a, hl};
		if (id_hi != 0)
			return (TrainerConvertResult){id_hi, a, hl};
	}

	const uint8_t *table = trainer_to_pkmn_data();
	gb_write8(hl, TYPE_PKMN_COLORLESS);
	for (uint8_t i = 0; i < (uint8_t)(CARD_DATA_AI_INFO - CARD_DATA_HP); i++)
		gb_write8((uint16_t)(hl + CARD_DATA_HP + i), table[i]);
	return (TrainerConvertResult){table[CARD_DATA_AI_INFO - CARD_DATA_HP - 1u],
				      0, (uint16_t)(hl + CARD_DATA_AI_INFO)};
}
