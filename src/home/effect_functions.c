#include "home/effect_functions.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define DUELVARS_DUELIST_TYPE 0x10u
#define DUELIST_TYPE_PLAYER   0x00u

#define DUELVARS_DUELIST_TYPE 0x00u
#include "home/effect_functions.h"

#define DUELIST_TYPE_PLAYER               0x00u
#define POISONED                          0x80u
#define DOUBLE_POISONED                   0xc0u
#define DUELVARS_DUELIST_TYPE             0xf2u
#define DUELVARS_ARENA_CARD_STATUS        0xcdu
#define DUELVARS_ARENA_CARD_SUBSTATUS1    0xcbu

#define DUELVARS_DUELIST_TYPE          0xf1u
#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xe7u
#define DUELIST_TYPE_PLAYER            0x00u
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


/* >>> factory IsPlayerTurn */
/* effect_functions.asm:157-165 */
IsPlayerTurnResult IsPlayerTurn(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	if (r.a == DUELIST_TYPE_PLAYER)
		return (IsPlayerTurnResult){r.a, 0x90u, r.hl};
	return (IsPlayerTurnResult){r.a, 0x00u, r.hl};
}
/* <<< factory IsPlayerTurn */

/* >>> factory UpdateExpectedAIDamage_AccountForPoison */
/* effect_functions.asm:177-187 */
void UpdateExpectedAIDamage_AccountForPoison(uint8_t a, uint8_t d, uint8_t e)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	if ((r.a & (POISONED | DOUBLE_POISONED)) == 0u) {
		UpdateExpectedAIDamage(a, d, e);
		return;
	}
	uint8_t dmg = wDamage;
	wAIMinDamage = dmg;
	wAIMaxDamage = dmg;
}
/* <<< factory UpdateExpectedAIDamage_AccountForPoison */


/* >>> factory ApplySubstatus1ToAttackingCard */
/* effect_functions.asm:264-270 */
uint16_t ApplySubstatus1ToAttackingCard(uint8_t a)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	gb_write8(r.hl, a);
	return (uint16_t)(r.hl + 1u);
}
/* <<< factory ApplySubstatus1ToAttackingCard */
