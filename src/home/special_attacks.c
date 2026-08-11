#include "home/special_attacks.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"

#define CARD_LOCATION_DECK 0x00u
#define DUELVARS_CARD_LOCATIONS 0x00u
#define DECK_SIZE 60u
#define TYPE_ENERGY 0x08u

CheckIfAnyBasicPokemonInDeckResult CheckIfAnyBasicPokemonInDeck(uint8_t b,
										uint8_t c,
										uint8_t d)
{
	uint8_t e = 0;
	for (;;) {
		DuelistVarResult location = GetTurnDuelistVariable(
			(uint8_t)(DUELVARS_CARD_LOCATIONS + e));
		uint8_t a;

		if (location.a == CARD_LOCATION_DECK) {
			(void)LoadCardDataToBuffer2_FromDeckIndex(e);
			a = gb_read8(wLoadedCard2Type_ADDR);
			if (a < TYPE_ENERGY && gb_read8(wLoadedCard2Stage_ADDR) == 0)
				return (CheckIfAnyBasicPokemonInDeckResult){0, 0x90u, b, c, d,
								 e, location.hl};
		}
		e = (uint8_t)(e + 1u);
		a = DECK_SIZE;
		if (a == e)
			return (CheckIfAnyBasicPokemonInDeckResult){a, 0x00u, b, c, d, e,
								location.hl};
	}
}
