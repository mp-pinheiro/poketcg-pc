#include "home/common.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"

#define CARD_LIST_TERMINATOR 0xFFu
#define F_Z 0x80u
#define F_C 0x10u
/* <<< factory statics */

/* >>> factory CountOppEnergyCardsInHand */
/* common.asm:434-452 */
CountOppEnergyResult CountOppEnergyCardsInHand(uint8_t a, uint8_t b)
{
	CoreCardListResult r = CreateEnergyCardListFromHand(a);
	if (r.f & F_C)
		return (CountOppEnergyResult){r.a, r.f, b};
	uint8_t count = 0u;
	uint16_t hl = wDuelTempList_ADDR;
	while (gb_read8(hl) != CARD_LIST_TERMINATOR) {
		hl = (uint16_t)(hl + 1u);
		count++;
	}
	return (CountOppEnergyResult){count, (uint8_t)(count ? 0x00u : F_Z), count};
}
/* <<< factory CountOppEnergyCardsInHand */

/* >>> factory ConvertHPToDamageCounters_Bank8 */
/* common.asm:454-466 */
uint8_t ConvertHPToDamageCounters_Bank8(uint8_t a)
{
	return (uint8_t)(a / 10u);
}
/* <<< factory ConvertHPToDamageCounters_Bank8 */

/* >>> factory CalculateWordTensDigit */
/* common.asm:468-481 */
uint16_t CalculateWordTensDigit(uint16_t hl)
{
	return (uint16_t)(hl / 10u);
}
/* <<< factory CalculateWordTensDigit */
