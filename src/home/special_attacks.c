#include "home/special_attacks.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"

#define DUELVARS_CARD_LOCATIONS 0x00u
#define TYPE_ENERGY 0x08u
#define DECK_SIZE 60u

BasicPokemonDeckResult CheckIfAnyBasicPokemonInDeck(void)
{
	uint8_t e = 0;
	uint16_t hl = 0;
	for (; e < DECK_SIZE; e++) {
		DuelistVarResult locations = GetTurnDuelistVariable(
			(uint8_t)(DUELVARS_CARD_LOCATIONS + e));
		hl = locations.hl;
		if (locations.a != 0x00u)
			continue;
		(void)LoadCardDataToBuffer2_FromDeckIndex(e);
		if (gb_read8(wLoadedCard2Type_ADDR) >= TYPE_ENERGY)
			continue;
		if (gb_read8(wLoadedCard2Stage_ADDR) != 0)
			continue;
		return (BasicPokemonDeckResult){0, e, 0x90u, hl};
	}
	return (BasicPokemonDeckResult){DECK_SIZE, DECK_SIZE, 0, hl};
}
