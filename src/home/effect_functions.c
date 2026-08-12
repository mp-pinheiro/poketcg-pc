#include "home/effect_functions.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define DUELVARS_DUELIST_TYPE 0x10u
#define DUELIST_TYPE_PLAYER   0x00u

#define DUELVARS_DUELIST_TYPE 0x00u
/* <<< factory statics */





/* >>> factory UpdateExpectedAIDamage */
/* effect_functions.asm:193-206 */
void UpdateExpectedAIDamage(uint8_t a, uint8_t d, uint8_t e)
{
	uint8_t hl = gb_read8(wDamage_ADDR);
	gb_write8(wAIMinDamage_ADDR, (uint8_t)(hl + d));
	gb_write8(wAIMaxDamage_ADDR, (uint8_t)(hl + e));
	gb_write8(wDamage_ADDR, (uint8_t)(a + hl));
}
/* <<< factory UpdateExpectedAIDamage */


/* >>> factory SetExpectedAIDamage */
/* effect_functions.asm:213-221 */
void SetExpectedAIDamage(uint8_t a, uint8_t d, uint8_t e)
{
	gb_write8(wDamage_ADDR, a);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);
	gb_write8(wAIMinDamage_ADDR, d);
	gb_write8(wAIMaxDamage_ADDR, e);
}
/* <<< factory SetExpectedAIDamage */
