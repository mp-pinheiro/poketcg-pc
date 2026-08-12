#include "home/core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x2eu
#define DUELVARS_ARENA_CARD_HP 0x01u
#define MENU_CANCEL 0xFFu
#define PAD_A     0x01u
#define PAD_B     0x02u
#define PAD_START 0x08u
#define B_PAD_B_BIT 0x02u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x12u
#define DUELVARS_ARENA_CARD_HP                  0x08u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x1Au
/* <<< factory statics */

/* >>> factory SetLineSeparation */
/* core.asm:4772-4774 */
void SetLineSeparation(uint8_t a)
{
	wLineSeparation = a;
}
/* <<< factory SetLineSeparation */

/* >>> factory PlayAreaScreenMenuFunction */
/* core.asm:5040-5054 */
uint8_t PlayAreaScreenMenuFunction(void)
{
	uint8_t keys = (uint8_t)(hKeysPressed & (PAD_A | PAD_B | PAD_START));
	if (keys == 0u)
		return 0xA0u;
	if (keys & PAD_B) {
		hCurMenuItem = MENU_CANCEL;
		return 0x10u;
	}
	return 0x90u;
}
/* <<< factory PlayAreaScreenMenuFunction */
