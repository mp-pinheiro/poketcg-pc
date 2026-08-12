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

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x02u
#include "home/random.h"

#include "home/substatus.h"

#define CLEFAIRY_DOLL 0xCBu
#define EFFECT_FAILED_UNSUCCESSFUL 0x02u
#define MYSTERIOUS_FOSSIL 0xCCu
#define PLAY_AREA_ARENA 0x00u
#define SNORLAX 0xBEu

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

/* >>> factory SetNoEffectFromStatus */
void SetNoEffectFromStatus(void)
{
	gb_write8(0xCCEDu, 0x01u);
}
/* <<< factory SetNoEffectFromStatus */

/* >>> factory SetDefiniteAIDamage */
void SetDefiniteAIDamage(void)
{
	uint8_t a = gb_read8(0xCCB9u);
	gb_write8(0xCCBBu, a);
	gb_write8(0xCCBCu, a);
}
/* <<< factory SetDefiniteAIDamage */

/* >>> factory PickRandomPlayAreaCard */
/* effect_functions.asm:316-321 */
PickRandomPlayAreaCardResult PickRandomPlayAreaCard(void)
{
	DuelistVarResult v = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t a = Random(v.a);
	return (PickRandomPlayAreaCardResult){a, (uint8_t)(a == 0 ? 0x80u : 0u)};
}
/* <<< factory PickRandomPlayAreaCard */

/* >>> factory GetNextPositionInTempList */
/* effect_functions.asm:326-334 */
uint16_t GetNextPositionInTempList(void)
{
	uint8_t a = hCurSelectionItem;
	hCurSelectionItem = (uint8_t)(a + 1u);
	return (uint16_t)(hTempList_ADDR + a);
}
/* <<< factory GetNextPositionInTempList */

/* >>> factory QueueStatusCondition */
/* effect_functions.asm:41-73 */
QueueStatusConditionResult QueueStatusCondition(uint8_t b, uint8_t c)
{
	uint8_t who = gb_read8(hWhoseTurn_ADDR);
	uint8_t turn = wWhoseTurn;
	uint8_t can_induce = 1u;

	if (who == turn) {
		uint8_t cardid = wTempNonTurnDuelistCardID;
		if (cardid == CLEFAIRY_DOLL || cardid == MYSTERIOUS_FOSSIL) {
			can_induce = 0u;
		} else if (cardid == SNORLAX) {
			SwapTurn();
			PkmnPowerIncapableResult r = CheckIsIncapableOfUsingPkmnPower(PLAY_AREA_ARENA);
			SwapTurn();
			can_induce = (r.f & 0x10u) ? 1u : 0u;
		} else {
			can_induce = 1u;
		}
	}

	if (!can_induce) {
		wNoEffectFromWhichStatus = c;
		SetNoEffectFromStatus();
		return (QueueStatusConditionResult){0x00u};
	}

	uint16_t idxaddr = wStatusConditionQueueIndex_ADDR;
	uint8_t idx = gb_read8(idxaddr);
	uint16_t qhl = (uint16_t)(wStatusConditionQueue_ADDR + idx);

	SwapTurn();
	uint8_t whoNew = gb_read8(hWhoseTurn_ADDR);
	gb_write8(qhl, whoNew);
	qhl++;
	SwapTurn();

	gb_write8(qhl, b);
	qhl++;
	gb_write8(qhl, c);

	gb_write8(idxaddr, (uint8_t)(idx + 3u));

	return (QueueStatusConditionResult){0x10u};
}
/* <<< factory QueueStatusCondition */

/* >>> factory CommentedOut_2c086 */
/* effect_functions.asm:98-98 */
uint8_t CommentedOut_2c086(uint8_t a)
{
	return a;
}
/* <<< factory CommentedOut_2c086 */

/* >>> factory SetWasUnsuccessful */
/* effect_functions.asm:131-136 */
void SetWasUnsuccessful(void)
{
	wEffectFailed = EFFECT_FAILED_UNSUCCESSFUL;
}
/* <<< factory SetWasUnsuccessful */

/* >>> factory Teleport_SwitchEffect */
/* effect_functions.asm:1806-1812 */
void Teleport_SwitchEffect(void)
{
	uint8_t e = hTemp_ffa0;
	SwapArenaWithBenchPokemon(e);
	wDuelDisplayedScreen = 0u;
}
/* <<< factory Teleport_SwitchEffect */

/* >>> factory SetDamageToATimes20 */
/* effect_functions.asm:1847-1861 */
void SetDamageToATimes20(uint8_t a)
{
	uint16_t hl = a;
	uint16_t de = hl;
	hl = (uint16_t)(hl + hl);
	hl = (uint16_t)(hl + hl);
	hl = (uint16_t)(hl + de);
	hl = (uint16_t)(hl + hl);
	hl = (uint16_t)(hl + hl);
	gb_write8(wDamage_ADDR, (uint8_t)(hl & 0xFFu));
	gb_write8((uint16_t)(wDamage_ADDR + 1u), (uint8_t)(hl >> 8));
}
/* <<< factory SetDamageToATimes20 */
