#include "home/effect_functions.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/bg_map.h"
/* >>> factory statics */
#include "home/duel.h"
#include "home/effect_functions.h"

#define DUELIST_TYPE_PLAYER               0x00u
#define POISONED                          0x80u
#define DOUBLE_POISONED                   0xc0u
#define DUELVARS_DUELIST_TYPE             0xf1u
#define DUELVARS_ARENA_CARD_STATUS        0xf0u
#define DUELVARS_ARENA_CARD_SUBSTATUS1    0xe7u

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
#include "home/random.h"

#include "home/substatus.h"

#define CLEFAIRY_DOLL 0xCBu
#define EFFECT_FAILED_UNSUCCESSFUL 0x02u
#define MYSTERIOUS_FOSSIL 0xCCu
#define PLAY_AREA_ARENA 0x00u
#define SNORLAX 0xBEu

#define DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE 0xEDu
#define DUELVARS_DECK_CARDS 0x7Eu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu
#define DECK_SIZE 60u
#define TYPE_ENERGY 0x08u
#define TYPE_ENERGY_DOUBLE_COLORLESS 0x0Eu
#define TYPE_TRAINER 0x10u
#define TX_ThereAreNoTrainerCardsInDiscardPileText 0x00C4u
#define TX_NoCardsLeftInTheDeckText 0x00B1u
#define NotEnoughWaterEnergyText 0x00C3u
#define NoDamageCountersText 0x00ADu

#define SUBSTATUS1_REDUCE_BY_20 0x13u

#include "home/effect_functions.h"

#define CONFUSED   0x01u
#define PARALYZED  0x03u
#define PSN_DBLPSN 0xf0u

#define PSN_DBLPSN 0xf0u
#define PARALYZED  0x03u
#define CONFUSED   0x01u

#include "home/damage.h"
#include "home/duel.h"

#define PLAY_AREA_ARENA 0x00u

#define DUELVARS_ARENA_CARD       0xBBu
#define DUELVARS_ARENA_CARD_HP    0xC8u
#define DUELVARS_ARENA_CARD_STAGE 0xCEu
#define POKEMON_POWER             0x04u

#define CONFUSED   0x01u
#define PARALYZED  0x03u
#define PSN_DBLPSN 0xf0u
#define CNF_SLP_PRZ 0x0fu

#define COLOR_TEXT_FIRE      0x48u
#define COLOR_TEXT_GRASS     0x47u
#define COLOR_TEXT_LIGHTNING 0x4au
#define COLOR_TEXT_WATER     0x49u
#define COLOR_TEXT_FIGHTING  0x4bu
#define COLOR_TEXT_PSYCHIC   0x4cu

static const uint8_t color_to_text[] = {
	COLOR_TEXT_FIRE,
	COLOR_TEXT_GRASS,
	COLOR_TEXT_LIGHTNING,
	COLOR_TEXT_WATER,
	COLOR_TEXT_FIGHTING,
	COLOR_TEXT_PSYCHIC,
};

#define DUELVARS_BENCH1_CARD_HP 0xC9u

#include "home/math.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"

#define KRABBY 0x4fu
#define SUBSTATUS3_HEADACHE_F 1u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"

#define FIRE 0x00u
#define NotEnoughFireEnergyText 0x00c1u

#define DUELVARS_ARENA_CARD_FLAGS 0xC2u
#define USED_PKMN_POWER_THIS_TURN 0x20u
#define WATER 0x03u

#include "home/damage.h"
#include "home/duel.h"
#include "home/math.h"

#define ASLEEP    0x02u

#include "home/duel.h"
#include "home/card_data.h"
#define DUELVARS_CARD_LOCATIONS 0x00u
#define CARD_LOCATION_ARENA    0x10u

#define DUELVARS_ARENA_CARD_CHANGED_TYPE 0xD4u

#define NoCardsLeftInTheDeckText 0x00b1u

#define ATK_ANIM_NONE 0x00u

#define PSYCHIC 0x05u
#define NotEnoughPsychicEnergyText 0x00c2u
#define OpponentIsNotAsleepText 0x00d3u

#define SUBSTATUS1_REDUCE_BY_10 0x1eu

#include "home/duel.h"
#include "home/card_data.h"
#define CARD_LOCATION_PLAY_AREA_F 4u

#define ThereAreNoCardsInTheDiscardPileText 0x00bbu

#define DUELVARS_HAND 0x42u
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xeeu

#define ThereAreNoStage1PokemonText 0x00BCu

#define SUBSTATUS1_PREVENT_LESS_THAN_40 0x0eu
#define EffectNoPokemonOnTheBenchText 0x00b7u

#define SUBSTATUS1_HALVE_DAMAGE 0x15u

#define CARD_LOCATION_PLAY_AREA 0x10u
#define TYPE_ENERGY_GRASS 0x09u

#define UNAFFECTED_BY_WEAKNESS_RESISTANCE_F 0x07u

#include "generated/hram.h"

#define USED_LEEK_SLAP_THIS_DUEL_F 0x06u

#define NoResistanceText 0x00c9u
#define NoWeaknessText 0x00c8u

#include "home/math.h"
#include "home/damage.h"
#include "home/duel.h"

#define NotAffectedByPoisonSleepParalysisOrConfusionText 0x00b5u
#define NotEnoughCardsInHandText 0x00b6u

#define NoGrassEnergyText 0x00CEu

#include "home/menus.h"
#include "home/print_text.h"
#include "home/duel.h"

#define OnlyOncePerTurnText 0x00CAu

#define NotEnoughEnergyCardsText 0x00C0u

#include "home/duel.h"

#define ThereAreNoBasicEnergyCardsInDiscardPileText 0x00b0u

#include "home/duel.h"
#include "generated/hram.h"

#define DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER 0xe0u

static uint8_t effect_compare(uint8_t lhs, uint8_t rhs)
{
	uint8_t f = 0x40u;
	if (lhs == rhs)
		f |= 0x80u;
	if ((lhs & 0x0fu) < (rhs & 0x0fu))
		f |= 0x20u;
	if (lhs < rhs)
		f |= 0x10u;
	return f;
}

#include "home/effect_functions.h"
#define NoAttackMayBeChoosenText 0x00c5u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/effect_functions.h"
#include "mem.h"

#define TYPE_ENERGY_PSYCHIC 0x0du

#include "generated/hram.h"
#include "home/duel.h"

#define NoEnergyAttachedToOpponentsActiveText 0x00aeu

#define NoPokemonWithDamageCountersText 0x00acu

#include "home/duel.h"
#include "home/substatus.h"

#define ConditionsForEvolvingToStage2NotFulfilledText 0x00b9u
#define ThereAreNoCardsInHandThatYouCanChangeText 0x00bau

#define MAX_PLAY_AREA_POKEMON 0x06u
#define NoSpaceOnTheBenchText 0x00b2u

#define DUELVARS_ARENA_CARD_LAST_TURN_EFFECT 0xf8u
#define LAST_TURN_EFFECT_DISCARD_ENERGY 0x01u

#define ThereAreNoTrainerCardsInDiscardPileText 0x00c4u

#define ThereAreNoEnergyCardsInDiscardPileText 0x00afu

#include "home/random.h"

#define ATK_ANIM_GLOW_EFFECT 0x5bu

#include "mem.h"

#include "generated/wram.h"
#include "home/card_color.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/effect_functions.h"
#include "mem.h"
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define SECOND_ATTACK 0x01u

#include "generated/hram.h"
#include "home/duel.h"
#include "home/effect_functions.h"
#define LAST_TURN_EFFECT_AMNESIA 0x02u

#include "home/duel.h"
#include "home/effect_functions.h"

#include "home/duel.h"
#include "home/effect_functions.h"

#include "generated/wram.h"
#include "mem.h"

#define SUBSTATUS1_DESTINY_BOND 0x16u

#include "home/effect_functions.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/effect_functions.h"

#include "home/effect_functions.h"
#include "generated/hram.h"

#include "generated/hram.h"
#include "home/effect_functions.h"

#include "home/effect_functions.h"

#include "home/effect_functions.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/damage.h"
#include "home/duel.h"
#include "home/effect_functions.h"

#define ThereIsNoEnergyCardAttachedText 0x00cdu
#include "home/effect_functions.h"

#define ThereAreNoPokemonInDiscardPileText 0x00b8u

#include "home/effect_functions.h"
#include "home/duel.h"
#include "generated/hram.h"

#include "home/effect_functions.h"
#include "home/substatus.h"
#include "home/duel.h"
#include "generated/hram.h"
#define CannotUseSinceTheresOnly1PkmnText 0x00cfu

#include "home/effect_functions.h"

#include "home/effect_functions.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define TYPE_ENERGY_WATER 0x0Bu

#include "home/effect_functions.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "home/effect_functions.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "home/effect_functions.h"
#include "home/substatus.h"
#include "generated/hram.h"

#include "home/effect_functions.h"
#include "home/duel.h"

#include "home/effect_functions.h"
#include "home/menus.h"
#include "home/duel.h"
#include "generated/hram.h"
#define HAS_CHANGED_COLOR 0x80u
#define USED_PKMN_POWER_THIS_TURN_F 0x05u
#define ChangedTheColorOfText 0x0116u

#include "home/effect_functions.h"
#include "mem.h"

#include "home/effect_functions.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "mem.h"
/* <<< factory statics */

/* >>> factory SleepEffect */
/* effect_functions.asm:14-16 */
QueueStatusConditionResult SleepEffect(void)
{
	return QueueStatusCondition(PSN_DBLPSN, ASLEEP);
}
/* <<< factory SleepEffect */

/* >>> factory SetDefiniteDamage */
/* effect_functions.asm:...? */
void SetDefiniteDamage(uint8_t a)
{
	gb_write8(wDamage_ADDR, a);
	gb_write8(wAIMinDamage_ADDR, a);
	gb_write8(wAIMaxDamage_ADDR, a);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);
}
/* <<< factory SetDefiniteDamage */





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

/* >>> factory CreateTrainerCardListFromDiscardPile */
/* effect_functions.asm:537-596 */
CreateTrainerCardListFromDiscardPileResult CreateTrainerCardListFromDiscardPile(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t b = r.a;
	uint16_t hl = (uint16_t)((r.hl & 0xFF00u) | (uint8_t)(r.a + DUELVARS_DECK_CARDS));
	uint16_t de = wDuelTempList_ADDR;
	b = (uint8_t)(b + 1u);

	while (b != 0u) {
		uint8_t l = (uint8_t)hl;
		uint8_t card = gb_read8(hl);
		(void)LoadCardDataToBuffer2_FromDeckIndex(card);
		if (gb_read8(wLoadedCard2Type_ADDR) == TYPE_TRAINER) {
			gb_write8(de, card);
			de++;
		}
		l--;
		hl = (uint16_t)((hl & 0xFF00u) | l);
		b--;
	}

	gb_write8(de, 0xFFu);
	if (gb_read8(wDuelTempList_ADDR) == 0xFFu)
		return (CreateTrainerCardListFromDiscardPileResult){TX_ThereAreNoTrainerCardsInDiscardPileText, 0x90u};
	uint8_t first = gb_read8(wDuelTempList_ADDR);
	return (CreateTrainerCardListFromDiscardPileResult){0, (uint8_t)((first == 0u) ? 0x80u : 0x00u)};
}
/* <<< factory CreateTrainerCardListFromDiscardPile */

/* >>> factory CreateEnergyCardListFromDiscardPile */
/* effect_functions.asm:597-654 */
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile(uint8_t c)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t count = r.a;
	uint8_t h = (uint8_t)(r.hl >> 8);
	uint8_t l = (uint8_t)(DUELVARS_DECK_CARDS + count);
	uint16_t de = wDuelTempList_ADDR;
	uint8_t b = (uint8_t)(count + 1u);
	for (;;) {
		l--;
		b--;
		if (b == 0u)
			break;
		uint8_t idx = gb_read8((uint16_t)((uint16_t)h << 8 | l));
		LoadCardDataToBuffer2_FromDeckIndex(idx);
		uint8_t type = gb_read8(wLoadedCard2Type_ADDR);
		if ((type & TYPE_ENERGY) == 0u)
			continue;
		if (c != 0u && type == TYPE_ENERGY_DOUBLE_COLORLESS)
			continue;
		gb_write8(de++, idx);
	}
	gb_write8(de, 0xFFu);
	uint8_t first = gb_read8(wDuelTempList_ADDR);
	uint16_t hl_out = (uint16_t)((uint16_t)h << 8 | l);
	uint8_t f = (first == 0xFFu) ? 0x90u : 0x00u;
	return (CreateEnergyCardListFromDiscardPileResult){hl_out, f};
}
/* <<< factory CreateEnergyCardListFromDiscardPile */


/* >>> factory GetAttackName */
/* effect_functions.asm:877-894 */
uint16_t GetAttackName(uint8_t d, uint8_t e)
{
	LoadCardDataToBuffer1_FromDeckIndex(d);
	uint16_t addr = (e == 0u) ? wLoadedCard1Atk1Name_ADDR : wLoadedCard1Atk2Name_ADDR;
	uint8_t lo = gb_read8(addr);
	uint8_t hi = gb_read8((uint16_t)(addr + 1u));
	return (uint16_t)(lo | (uint16_t)hi << 8);
}
/* <<< factory GetAttackName */


/* >>> factory ClefableMinimizeEffect */
/* effect_functions.asm:7973-7976 */
uint16_t ClefableMinimizeEffect(void)
{
	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_20);
}
/* <<< factory ClefableMinimizeEffect */

/* >>> factory HandleAIMetronomeEffect */
/* effect_functions.asm:8168-8169 */
void HandleAIMetronomeEffect(void)
{
	(void)0;
}
/* <<< factory HandleAIMetronomeEffect */

/* >>> factory ParalysisEffect */
/* effect_functions.asm:19-21 */
QueueStatusConditionResult ParalysisEffect(void)
{
	return QueueStatusCondition(PSN_DBLPSN, PARALYZED);
}
/* <<< factory ParalysisEffect */

/* >>> factory ConfusionEffect */
/* effect_functions.asm:28-30 */
QueueStatusConditionResult ConfusionEffect(void)
{
	return QueueStatusCondition(PSN_DBLPSN, CONFUSED);
}
/* <<< factory ConfusionEffect */

/* >>> factory InvisibleWallEffect */
/* effect_functions.asm:4999-5001. scf: sets carry, clears N/H, keeps Z. */
uint8_t InvisibleWallEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory InvisibleWallEffect */

/* >>> factory CheckIfDefendingPokemonHasAnyAttack */
/* effect_functions.asm:893-916 */
CheckAttackResult CheckIfDefendingPokemonHasAnyAttack(void)
{
	SwapTurn();
	uint8_t index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	LoadCardDataToBuffer2_FromDeckIndex(index);

	uint8_t f;
	uint8_t category = gb_read8(wLoadedCard2Atk1Category_ADDR);
	if (category != POKEMON_POWER) {
		f = (category == 0u) ? 0x80u : 0x00u;
	} else {
		uint8_t lo = gb_read8(wLoadedCard2Atk2Name_ADDR);
		uint8_t hi = gb_read8((uint16_t)(wLoadedCard2Atk2Name_ADDR + 1u));
		f = ((uint8_t)(lo | hi) != 0u) ? 0x00u : 0x90u;
	}

	SwapTurn();
	return (CheckAttackResult){f};
}
/* <<< factory CheckIfDefendingPokemonHasAnyAttack */

/* >>> factory UpdateDevolvedCardHPAndStage */
/* effect_functions.asm:919-947 */
void UpdateDevolvedCardHPAndStage(uint8_t a)
{
	uint8_t e = hTempPlayAreaLocation_ff9d;
	uint8_t damage = GetCardDamageAndMaxHP(e).a;

	uint16_t arena_addr = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).hl;
	gb_write8(arena_addr, a);

	LoadCardDataToBuffer2_FromDeckIndex(a);

	uint16_t hp_addr = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).hl;
	uint8_t new_max_hp = gb_read8(wLoadedCard2HP_ADDR);
	uint8_t new_hp = (new_max_hp < damage) ? 0u : (uint8_t)(new_max_hp - damage);
	gb_write8(hp_addr, new_hp);

	uint16_t stage_addr = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_STAGE + e)).hl;
	gb_write8(stage_addr, gb_read8(wLoadedCard2Stage_ADDR));
}
/* <<< factory UpdateDevolvedCardHPAndStage */


/* >>> factory DodrioRage_DamageBoostEffect */
/* effect_functions.asm:7866-7869 */
void DodrioRage_DamageBoostEffect(void)
{
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	AddToDamage(r.a);
}
/* <<< factory DodrioRage_DamageBoostEffect */

/* >>> factory DragonairSlam_AIEffect */
/* effect_functions.asm:7890-7893 */
void DragonairSlam_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory DragonairSlam_AIEffect */



/* >>> factory CheckIfPlayAreaHasAnyDamage */
/* effect_functions.asm:517-531. Zero-means-max: the count is post-tested
 * (dec+jr nz after the call), so an 8-bit count of 0 runs 256 times. */
CheckIfPlayAreaHasAnyDamageResult CheckIfPlayAreaHasAnyDamage(void)
{
	/* DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA = 0xEFu (duel_constants.asm);
	 * not the local macro of the same name, which is defined wrong above. */
	DuelistVarResult count = GetTurnDuelistVariable(0xEFu);
	uint32_t n = count.a ? count.a : 0x100u;
	uint8_t e = PLAY_AREA_ARENA;
	for (uint32_t i = 0; i < n; i++) {
		if (GetCardDamageAndMaxHP(e).a != 0u)
			return (CheckIfPlayAreaHasAnyDamageResult){0x00u, count.hl};
		e++;
	}
	return (CheckIfPlayAreaHasAnyDamageResult){0x90u, count.hl};
}
/* <<< factory CheckIfPlayAreaHasAnyDamage */

/* >>> factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
/* effect_functions.asm:581-583 */
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile_OnlyBasic(void)
{
	return CreateEnergyCardListFromDiscardPile(0x01u);
}
/* <<< factory CreateEnergyCardListFromDiscardPile_OnlyBasic */

/* >>> factory KabutoArmorEffect */
/* effect_functions.asm:5939-5941. scf: sets carry, clears N/H, keeps Z. */
uint8_t KabutoArmorEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory KabutoArmorEffect */

/* >>> factory CuboneRage_DamageBoostEffect */
/* effect_functions.asm:5970-5974 */
void CuboneRage_DamageBoostEffect(void)
{
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	AddToDamage(r.a);
}
/* <<< factory CuboneRage_DamageBoostEffect */

/* >>> factory PoisonEffect */
/* effect_functions.asm:6-8 */
QueueStatusConditionResult PoisonEffect(void)
{
	return QueueStatusCondition(CNF_SLP_PRZ, POISONED);
}
/* <<< factory PoisonEffect */

/* >>> factory DoublePoisonEffect */
/* effect_functions.asm:10-12 */
QueueStatusConditionResult DoublePoisonEffect(void)
{
	return QueueStatusCondition(CNF_SLP_PRZ, DOUBLE_POISONED);
}
/* <<< factory DoublePoisonEffect */




/* >>> factory LoadCardNameAndInputColor */
/* effect_functions.asm:1345-1371 */
void LoadCardNameAndInputColor(uint8_t a, uint8_t d, uint8_t e)
{
	uint8_t color = color_to_text[a];
	uint8_t name_lo = gb_read8(wLoadedCard1Name_ADDR);
	uint8_t name_hi = gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u));

	wTxRam2 = name_lo;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), name_hi);
	wTxRam2_b = color;
	gb_write8((uint16_t)(wTxRam2_b_ADDR + 1u), 0u);
}
/* <<< factory LoadCardNameAndInputColor */




/* >>> factory AIPickEnergyCardToDiscardFromDefendingPokemon */
/* effect_functions.asm:1053-1140 */
AIPickEnergyCardToDiscardResult AIPickEnergyCardToDiscardFromDefendingPokemon(void)
{
	SwapTurn();
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	HandListResult list = CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);
	if (list.f & 0x10u) {
		SwapTurn();
		return (AIPickEnergyCardToDiscardResult){0xFFu};
	}

	uint8_t color = 0x07u;
	uint8_t colorless = gb_read8((uint16_t)(wAttachedEnergies_ADDR + 7u));
	if (colorless == 0u) {
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		LoadCardDataToBuffer1_FromDeckIndex(arena.a);
		color = wLoadedCard1Type;
		if (color >= 0x07u ||
		    gb_read8((uint16_t)(wAttachedEnergies_ADDR + color)) == 0u)
			color = 0xFFu;
	}

	uint16_t cursor = wDuelTempList_ADDR;
	if (color != 0xFFu) {
		for (;;) {
			uint8_t entry = gb_read8(cursor++);
			if (entry == 0xFFu)
				break;
			LoadCardDataToBuffer2_FromDeckIndex(entry);
			if ((wLoadedCard2Type & 0x07u) == color) {
				SwapTurn();
				return (AIPickEnergyCardToDiscardResult){entry};
			}
		}
	}
	TempListResult count = CountCardsInDuelTempList();
	(void)ShuffleCards(count.a, wDuelTempList_ADDR);
	SwapTurn();
	return (AIPickEnergyCardToDiscardResult){gb_read8(wDuelTempList_ADDR)};
}
/* <<< factory AIPickEnergyCardToDiscardFromDefendingPokemon */




/* >>> factory AIFindTargetForBenchAttack */
/* effect_functions.asm:1141-1176 */
AIFindTargetForBenchAttackResult AIFindTargetForBenchAttack(void)
{
	SwapTurn();
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t target = PLAY_AREA_ARENA;
	uint8_t best = 0xFFu;
	uint8_t slot = 1u;
	while (--count != 0u) {
		uint8_t hp = GetTurnDuelistVariable(
			(uint8_t)(DUELVARS_BENCH1_CARD_HP + slot - 1u)).a;
		if (best >= hp) {
			best = hp;
			target = slot;
		}
		slot++;
	}
	SwapTurn();
	return (AIFindTargetForBenchAttackResult){target};
}
/* <<< factory AIFindTargetForBenchAttack */




/* >>> factory ApplyExtraWaterEnergyDamageBonus */
void ApplyExtraWaterEnergyDamageBonus(uint8_t b, uint8_t c)
{
	if (wMetronomeEnergyCost) {
		c = wMetronomeEnergyCost;
		b = 0u;
	}
	GetPlayAreaCardAttachedEnergies(hTempPlayAreaLocation_ff9d);
	uint16_t water_addr = (uint16_t)(wAttachedEnergies_ADDR + WATER);
	uint8_t water = gb_read8(water_addr);
	if (c && wTotalAttachedEnergies == water)
		b = (uint8_t)(c + b);
	uint8_t extra = (uint8_t)(water - b);
	if (water >= b && extra >= 1u) {
		if (extra > 2u) extra = 2u;
		AddToDamage(ATimes10(extra));
	}
	wAIMinDamage = wDamage;
	wAIMaxDamage = wDamage;
}
/* <<< factory ApplyExtraWaterEnergyDamageBonus */



/* >>> factory OmastarSpikeCannon_AIEffect */
/* effect_functions.asm:8045-8052. */
void OmastarSpikeCannon_AIEffect(void)
{
	SetExpectedAIDamage((uint8_t)30u, 0u, 60u);
}
/* <<< factory OmastarSpikeCannon_AIEffect */



/* >>> factory ClairvoyanceEffect */
/* effect_functions.asm:8058-8059. scf: sets carry, clears N/H, keeps Z. */
uint8_t ClairvoyanceEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory ClairvoyanceEffect */

/* >>> factory KrabbyCallForFamily_AISelectEffect */
/* effect_functions.asm:2946-2966 */
void KrabbyCallForFamily_AISelectEffect(uint8_t c, uint16_t de)
{
	(void)CreateDeckCardList(c, de);

	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		hTemp_ffa0 = card;
		if (card == 0xffu)
			return;
		uint16_t card_id = GetCardIDFromDeckIndex(card);
		if ((uint8_t)card_id == KRABBY)
			return;
	}
}
/* <<< factory KrabbyCallForFamily_AISelectEffect */


/* >>> factory CreateListOfEnergyAttachedToArena */
CreateListOfEnergyAttachedToArenaResult CreateListOfEnergyAttachedToArena(uint8_t a)
{
	uint8_t count = 0;
	uint16_t locations = GetTurnDuelistVariable(0x00u).hl;
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t index = 0; index < DECK_SIZE; index++) {
		if (gb_read8((uint16_t)(locations + index)) != 0x10u)
			continue;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(index);
		if (GetCardType(card_id) != a)
			continue;
		gb_write8(dst++, index);
		count++;
	}
	gb_write8(dst, 0xFFu);
	return (CreateListOfEnergyAttachedToArenaResult){
		count, count, (uint16_t)(locations + DECK_SIZE), 0xC0u};
}
/* <<< factory CreateListOfEnergyAttachedToArena */


/* >>> factory HandleNoDamageOrEffect */
HandleNoDamageOrEffectResult HandleNoDamageOrEffect(uint16_t hl)
{
	NoDamageOrEffectCheckResult check = CheckNoDamageOrEffect(hl);
	if ((check.f & 0x10u) == 0u)
		return (HandleNoDamageOrEffectResult){check.f, check.hl};
	return (HandleNoDamageOrEffectResult){(uint8_t)(0x10u | (check.hl == 0u ? 0x80u : 0x00u)), check.hl};
}
/* <<< factory HandleNoDamageOrEffect */

/* >>> factory ArcanineFlamethrower_CheckEnergy */
/* effect_functions.asm:3533-3546 */
ArcanineFlamethrowerCheckEnergyResult ArcanineFlamethrower_CheckEnergy(void)
{
	uint8_t energy;
	uint8_t f;
	uint16_t hl = NotEnoughFireEnergyText;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	energy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	f = 0x40u;
	if (energy == 1u)
		f |= 0x80u;
	if ((energy & 0x0fu) == 0u)
		f |= 0x20u;
	if (energy == 0u)
		f |= 0x10u;
	return (ArcanineFlamethrowerCheckEnergyResult){energy, f, 0u, hl};
}
/* <<< factory ArcanineFlamethrower_CheckEnergy */

/* >>> factory ArcanineFlamethrower_DiscardEffect */
/* effect_functions.asm:3549-3554 */
uint8_t ArcanineFlamethrower_DiscardEffect(void)
{
	uint8_t card = gb_read8(hTemp_ffa0_ADDR);
	PutCardInDiscardPile(card);
	return card;
}
/* <<< factory ArcanineFlamethrower_DiscardEffect */


/* >>> factory PoisonWhip_AIEffect */
void PoisonWhip_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);
}
/* <<< factory PoisonWhip_AIEffect */


/* >>> factory SolarPower_CheckUse */
SolarPowerCheckUseResult SolarPower_CheckUse(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	DuelistVarResult flags = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location));
	if (flags.a & USED_PKMN_POWER_THIS_TURN)
		return (SolarPowerCheckUseResult){0x10u, 0x00CAu};
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	if (incapable.f & 0x10u)
		return (SolarPowerCheckUseResult){incapable.f, incapable.hl};
	DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	if (status.a)
		return (SolarPowerCheckUseResult){0x00u, status.hl};
	status = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	if (status.a)
		return (SolarPowerCheckUseResult){0x00u, status.hl};
	return (SolarPowerCheckUseResult){0x90u, 0x00B5u};
}
/* <<< factory SolarPower_CheckUse */


/* >>> factory DevolutionBeam_LoadAnimation */
/* effect_functions.asm:5232-5236 */
void DevolutionBeam_LoadAnimation(void)
{
	wLoadedAttackAnimation = ATK_ANIM_NONE;
}
/* <<< factory DevolutionBeam_LoadAnimation */


/* >>> factory CheckIfTurnDuelistHasEvolvedCards */
CheckAttackResult CheckIfTurnDuelistHasEvolvedCards(void)
{
	DuelistVarResult cards = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint16_t stage = (uint16_t)((cards.hl & 0xFF00u) | DUELVARS_ARENA_CARD_STAGE);
	for (;;) {
		uint8_t card = gb_read8(cards.hl++);
		if (card == 0xFFu)
			return (CheckAttackResult){0x90u};
		uint8_t stage_value = gb_read8(stage++);
		if (stage_value != 0u)
			return (CheckAttackResult){0x00u};
	}
}
/* <<< factory CheckIfTurnDuelistHasEvolvedCards */


/* >>> factory FindFirstNonBasicCardInPlayArea */
FindFirstNonBasicCardInPlayAreaResult FindFirstNonBasicCardInPlayArea(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint32_t n = count.a ? count.a : 0x100u;
	uint16_t stage = (uint16_t)((count.hl & 0xFF00u) | DUELVARS_ARENA_CARD_STAGE);
	uint8_t slot = PLAY_AREA_ARENA;
	for (uint32_t i = 0; i < n; i++) {
		if (gb_read8(stage++) != 0u)
			return (FindFirstNonBasicCardInPlayAreaResult){slot, 0x10u};
		slot++;
	}
	return (FindFirstNonBasicCardInPlayAreaResult){0x00u, 0x80u};
}
/* <<< factory FindFirstNonBasicCardInPlayArea */

/* >>> factory Wildfire_AISelectEffect */
/* effect_functions.asm:3780-3783 */
WildfireAISelectEffectResult Wildfire_AISelectEffect(void)
{
	uint8_t a = 0x00u;
	hTempList = a;
	return (WildfireAISelectEffectResult){a, 0x80u};
}
/* <<< factory Wildfire_AISelectEffect */

/* >>> factory FireBlast_CheckEnergy */
/* effect_functions.asm:3691-3704 */
FireBlastCheckEnergyResult FireBlast_CheckEnergy(void)
{
	uint8_t a;
	uint8_t flags = 0x40u;

	GetPlayAreaCardAttachedEnergies(0u);
	a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	if ((a & 0x0fu) == 0u)
		flags |= 0x20u;
	if (a == 1u)
		flags |= 0x80u;
	if (a < 1u)
		flags |= 0x10u;
	return (FireBlastCheckEnergyResult){a, flags, NotEnoughFireEnergyText};
}
/* <<< factory FireBlast_CheckEnergy */

/* >>> factory BigEggsplosion_AIEffect */
/* effect_functions.asm:1814-1844 */
void BigEggsplosion_AIEffect(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	GetPlayAreaCardAttachedEnergies(location);
	SetDamageToATimes20(wTotalAttachedEnergies);

	uint16_t damage = (uint16_t)((uint16_t)wTotalAttachedEnergies * 20u);
	if ((uint8_t)(damage >> 8) == 0xFFu)
		damage = (uint16_t)((damage & 0xFF00u) | 0x00FFu);

	wAIMaxDamage = (uint8_t)damage;
	wDamage = (uint8_t)(wAIMaxDamage >> 1);
	wAIMinDamage = 0u;
}
/* <<< factory BigEggsplosion_AIEffect */

/* >>> factory Thrash_AIEffect */
/* effect_functions.asm:1863-1870 */
void Thrash_AIEffect(void)
{
	SetExpectedAIDamage(35u, 30u, 40u);
}
/* <<< factory Thrash_AIEffect */

/* >>> factory Prophecy_CheckDeck */
/* effect_functions.asm:4705-4729 */
ProphecyCheckDeckResult Prophecy_CheckDeck(void)
{
	DuelistVarResult turn = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (turn.a < DECK_SIZE)
		return (ProphecyCheckDeckResult){
			turn.a,
			(uint8_t)(turn.a == 0u ? 0x80u : 0x00u),
			turn.hl
		};

	DuelistVarResult nonturn = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (nonturn.a < DECK_SIZE)
		return (ProphecyCheckDeckResult){
			nonturn.a,
			(uint8_t)(nonturn.a == 0u ? 0x80u : 0x00u),
			nonturn.hl
		};

	return (ProphecyCheckDeckResult){nonturn.a, 0x10u, NoCardsLeftInTheDeckText};
}
/* <<< factory Prophecy_CheckDeck */

/* >>> factory TryGiveDamageCounter_DamageSwap */
/* effect_functions.asm:5134-5158 */
TryGiveDamageCounter_DamageSwapResult TryGiveDamageCounter_DamageSwap(void)
{
	uint8_t target = (uint8_t)(hPlayAreaEffectTarget + DUELVARS_ARENA_CARD_HP);
	DuelistVarResult result = GetTurnDuelistVariable(target);
	uint8_t remaining = (uint8_t)(result.a - 10u);

	if (remaining == 0u)
		return (TryGiveDamageCounter_DamageSwapResult){0u, 0x10u, result.hl};

	gb_write8(result.hl, remaining);

	uint8_t source = (uint8_t)(hTempPlayAreaLocation_ffa1 + DUELVARS_ARENA_CARD_HP);
	uint16_t source_hp = (uint16_t)((result.hl & 0xff00u) | source);
	uint8_t new_hp = (uint8_t)(10u + gb_read8(source_hp));
	gb_write8(source_hp, new_hp);

	return (TryGiveDamageCounter_DamageSwapResult){
		new_hp,
		(uint8_t)(new_hp == 0u ? 0x80u : 0u),
		source_hp
	};
}
/* <<< factory TryGiveDamageCounter_DamageSwap */

/* >>> factory TransparencyEffect */
/* effect_functions.asm:4699-4700 */
uint8_t TransparencyEffect(void)
{
	return 0x10u;
}
/* <<< factory TransparencyEffect */

/* >>> factory Barrier_CheckEnergy */
/* effect_functions.asm:5395-5408 */
BarrierCheckEnergyResult Barrier_CheckEnergy(void)
{
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	uint8_t a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + PSYCHIC));
	uint8_t f = 0x40u;

	if (a == 1u)
		f |= 0x80u;
	if ((a & 0x0fu) < 1u)
		f |= 0x20u;
	if (a < 1u)
		f |= 0x10u;

	return (BarrierCheckEnergyResult){a, f, NotEnoughPsychicEnergyText};
}
/* <<< factory Barrier_CheckEnergy */

/* >>> factory ResetDevolvedCardStatus */
/* effect_functions.asm:1026-1050 */
uint8_t ResetDevolvedCardStatus(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	if (location == PLAY_AREA_ARENA)
		ClearAllStatusConditions();

	DuelistVarResult changed = GetTurnDuelistVariable(
		(uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + location));
	gb_write8(changed.hl, 0u);
	DuelistVarResult flags = GetTurnDuelistVariable(
		(uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location));
	gb_write8(flags.hl, 0u);
	return (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location);
}
/* <<< factory ResetDevolvedCardStatus */

/* >>> factory EeveeQuickAttack_AIEffect */
void EeveeQuickAttack_AIEffect(void)
{
	SetExpectedAIDamage(20u, 10u, 30u);
}
/* <<< factory EeveeQuickAttack_AIEffect */

/* >>> factory MirrorMove_AIEffect */
void MirrorMove_AIEffect(void)
{
	DuelistVarResult damage = GetTurnDuelistVariable(0xF3u);
	wAIMinDamage = gb_read8(damage.hl);
	wAIMaxDamage = wAIMinDamage;
}
/* <<< factory MirrorMove_AIEffect */

/* >>> factory MirrorMove_InitialEffect1 */
MirrorMoveInitialEffect1Result MirrorMove_InitialEffect1(void)
{
	DuelistVarResult damage = GetTurnDuelistVariable(0xF3u);
	uint16_t hl = damage.hl;
	uint8_t value = gb_read8(hl++);
	value |= gb_read8(hl);
	hl++;
	value |= gb_read8(hl);
	hl++;
	if (value != 0u)
		return (MirrorMoveInitialEffect1Result){0x00u, hl};
	value = gb_read8(hl++);
	if (value != 0u)
		return (MirrorMoveInitialEffect1Result){0x00u, hl};
	return (MirrorMoveInitialEffect1Result){0x90u, 0x00C6u};
}
/* <<< factory MirrorMove_InitialEffect1 */

/* >>> factory FuryAttack_AIEffect */
/* effect_functions.asm:...? */
void FuryAttack_AIEffect(void)
{
	SetExpectedAIDamage(10u, 0u, 20u);
}
/* <<< factory FuryAttack_AIEffect */

/* >>> factory RetreatAidEffect */
/* effect_functions.asm:...? */
uint8_t RetreatAidEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory RetreatAidEffect */

/* >>> factory FriendshipSong_BenchCheck */
FriendshipSongBenchCheckResult FriendshipSong_BenchCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t f = (uint8_t)(count.a >= 6u ? 0x10u : 0u);
	if (count.a == 6u)
		f |= 0x80u;
	return (FriendshipSongBenchCheckResult){count.a, f, 0x00B2u};
}
/* <<< factory FriendshipSong_BenchCheck */

/* >>> factory ExpandEffect */
void ExpandEffect(void)
{
	(void)ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_10);
}
/* <<< factory ExpandEffect */

/* >>> factory CheckIfThereAreAnyEnergyCardsAttached */
CheckIfThereAreAnyEnergyCardsAttachedResult CheckIfThereAreAnyEnergyCardsAttached(void)
{
	DuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);
	for (uint8_t index = 0; index < DECK_SIZE; index++) {
		uint8_t location = gb_read8((uint16_t)(locations.hl + index));
		if (!(location & (1u << CARD_LOCATION_PLAY_AREA_F)))
			continue;
		(void)LoadCardDataToBuffer2_FromDeckIndex(index);
		uint8_t type = gb_read8(wLoadedCard2Type_ADDR);
		if (type == TYPE_TRAINER)
			continue;
		if (type >= TYPE_ENERGY)
			return (CheckIfThereAreAnyEnergyCardsAttachedResult){0x00u};
	}
	return (CheckIfThereAreAnyEnergyCardsAttachedResult){0x90u};
}
/* <<< factory CheckIfThereAreAnyEnergyCardsAttached */

/* >>> factory PokeBall_DeckCheck */
/* effect_functions.asm:10462-10473 */
PokeBall_DeckCheckResult PokeBall_DeckCheck(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t z = (uint8_t)(r.a == DECK_SIZE);
	uint8_t borrow = (uint8_t)(r.a < DECK_SIZE);
	uint8_t f = z ? 0x80u : 0x00u;
	if (!borrow)
		f = (uint8_t)(f | 0x10u);
	return (PokeBall_DeckCheckResult){r.a, (uint16_t)NoCardsLeftInTheDeckText, f};
}
/* <<< factory PokeBall_DeckCheck */

/* >>> factory Recycle_DiscardPileCheck */
/* effect_functions.asm:10548-10558 */
Recycle_DiscardPileCheckResult Recycle_DiscardPileCheck(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t z = (uint8_t)(r.a == 1u);
	uint8_t h = (uint8_t)((r.a & 0x0fu) < 1u);
	uint8_t borrow = (uint8_t)(r.a < 1u);
	uint8_t f = 0x40u;
	if (z)
		f = (uint8_t)(f | 0x80u);
	if (h)
		f = (uint8_t)(f | 0x20u);
	if (borrow)
		f = (uint8_t)(f | 0x10u);
	return (Recycle_DiscardPileCheckResult){(uint16_t)ThereAreNoCardsInTheDiscardPileText, f};
}
/* <<< factory Recycle_DiscardPileCheck */


/* >>> factory CreateBasicPokemonCardListFromDiscardPile */
CreateBasicPokemonCardListFromDiscardPileResult CreateBasicPokemonCardListFromDiscardPile(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t b = (uint8_t)(count.a + 1u);
	uint16_t hl = (uint16_t)((count.hl & 0xFF00u) |
		(uint8_t)(count.a + DUELVARS_DECK_CARDS));
	uint16_t de = wDuelTempList_ADDR;
	while (b != 0u) {
		uint8_t card = gb_read8(hl);
		LoadCardDataToBuffer2_FromDeckIndex(card);
		if (gb_read8(wLoadedCard2Type_ADDR) < TYPE_ENERGY &&
			gb_read8(wLoadedCard2Stage_ADDR) == 0u)
			gb_write8(de++, card);
		hl = (uint16_t)((hl & 0xFF00u) | (uint8_t)((uint8_t)hl - 1u));
		b--;
	}
	gb_write8(de, 0xFFu);
	if (gb_read8(wDuelTempList_ADDR) == 0xFFu)
		return (CreateBasicPokemonCardListFromDiscardPileResult){0x90u};
	return (CreateBasicPokemonCardListFromDiscardPileResult){0x00u};
}
/* <<< factory CreateBasicPokemonCardListFromDiscardPile */

/* >>> factory CreatePokemonCardListFromHand */
CreatePokemonCardListFromHandResult CreatePokemonCardListFromHand(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	uint8_t count = r.a;
	uint16_t hl = (uint16_t)((r.hl & 0xFF00u) | DUELVARS_HAND);
	uint16_t de = wDuelTempList_ADDR;

	for (;;) {
		uint8_t card = gb_read8(hl);
		LoadCardDataToBuffer2_FromDeckIndex(card);
		if (gb_read8(wLoadedCard2Type_ADDR) < TYPE_ENERGY)
			gb_write8(de++, card);
		hl = (uint16_t)((hl & 0xFF00u) | (uint8_t)((uint8_t)hl + 1u));
		count--;
		if (count == 0u)
			break;
	}
	gb_write8(de, 0xFFu);
	uint8_t first = gb_read8(wDuelTempList_ADDR);
	uint8_t result_f = (first == 0xFFu) ? 0x90u : (uint8_t)(first == 0u ? 0x80u : 0x00u);
	return (CreatePokemonCardListFromHandResult){first, result_f, 0u,
		(uint8_t)(de >> 8), (uint8_t)de};
}
/* <<< factory CreatePokemonCardListFromHand */

/* >>> factory Pokedex_DeckCheck */
PokedexDeckCheckResult Pokedex_DeckCheck(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t f = (count < DECK_SIZE) ? 0x00u : (uint8_t)(count == DECK_SIZE ? 0x90u : 0x10u);
	return (PokedexDeckCheckResult){count, f, NoCardsLeftInTheDeckText};
}
/* <<< factory Pokedex_DeckCheck */

/* >>> factory Pokedex_OrderDeckCardsEffect */

PokedexOrderDeckCardsEffectResult Pokedex_OrderDeckCardsEffect(void)
{
	uint16_t hl = hTempList_ADDR;
	uint8_t c = 0u;
	uint8_t a = 0u;

	for (;;) {
		a = gb_read8(hl++);
		if (a == 0xffu)
			break;
		SearchCardInDeckAndAddToHand(a);
		c = (uint8_t)(c + 1u);
	}

	hl = (uint16_t)(hl - 2u);
	do {
		a = gb_read8(hl--);
		ReturnCardToDeck(a);
		c = (uint8_t)(c - 1u);
	} while (c != 0u);

	return (PokedexOrderDeckCardsEffectResult){a, c, 0xc0u, hl};
}
/* <<< factory Pokedex_OrderDeckCardsEffect */

/* >>> factory Maintenance_HandCheck */
MaintenanceHandCheckResult Maintenance_HandCheck(void)
{
	DuelistVarResult hand = GetTurnDuelistVariable(0xeeu);
	uint8_t result = (uint8_t)(hand.a - 3u);
	uint8_t f = 0x40u;

	if (result == 0u)
		f |= 0x80u;
	if ((hand.a & 0x0fu) < 3u)
		f |= 0x20u;
	if (hand.a < 3u)
		f |= 0x10u;

	return (MaintenanceHandCheckResult){hand.a, f, 0x00b6u};
}
/* <<< factory Maintenance_HandCheck */

/* >>> factory DevolutionSpray_PlayAreaEvolutionCheck */
DevolutionSprayPlayAreaEvolutionCheckResult DevolutionSpray_PlayAreaEvolutionCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint16_t hl = (uint16_t)((count.hl & 0xFF00u) | DUELVARS_ARENA_CARD);
	uint16_t n = count.a ? count.a : 0x100u;
	do {
		LoadCardDataToBuffer2_FromDeckIndex(gb_read8(hl++));
		if (gb_read8(wLoadedCard2Stage_ADDR) != 0u)
			return (DevolutionSprayPlayAreaEvolutionCheckResult){0x0000u, 0x00u};
	} while (--n != 0u);
	return (DevolutionSprayPlayAreaEvolutionCheckResult){
		ThereAreNoStage1PokemonText, 0x90u
	};
}
/* <<< factory DevolutionSpray_PlayAreaEvolutionCheck */

/* >>> factory SpitPoison_AIEffect */
/* effect_functions.asm:1435-1438 */
void SpitPoison_AIEffect(void)
{
	SetExpectedAIDamage(5u, 0u, 10u);
}
/* <<< factory SpitPoison_AIEffect */

/* >>> factory GloomPoisonPowder_AIEffect */
void GloomPoisonPowder_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);
}
/* <<< factory GloomPoisonPowder_AIEffect */

/* >>> factory FoulOdorEffect */
QueueStatusConditionResult FoulOdorEffect(void)
{
	QueueStatusConditionResult r;
	(void)ConfusionEffect();
	SwapTurn();
	r = ConfusionEffect();
	SwapTurn();
	return r;
}
/* <<< factory FoulOdorEffect */


/* >>> factory KakunaPoisonPowder_AIEffect */
void KakunaPoisonPowder_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory KakunaPoisonPowder_AIEffect */


/* >>> factory SwordsDanceEffect */
uint16_t SwordsDanceEffect(void)
{
	if (gb_read8(0xCCC3u) != 0x2Eu)
		return 0u;
	return ApplySubstatus1ToAttackingCard(0x19u);
}
/* <<< factory SwordsDanceEffect */


/* >>> factory Twineedle_AIEffect */
void Twineedle_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory Twineedle_AIEffect */


/* >>> factory BeedrillPoisonSting_AIEffect */
void BeedrillPoisonSting_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory BeedrillPoisonSting_AIEffect */


/* >>> factory FoulGas_AIEffect */
void FoulGas_AIEffect(void)
{
	UpdateExpectedAIDamage(5u, 0u, 10u);
}
/* <<< factory FoulGas_AIEffect */


/* >>> factory Sprout_AISelectEffect */
#define ODDISH 0x1cu
void Sprout_AISelectEffect(uint8_t c, uint16_t de)
{
	(void)CreateDeckCardList(c, de);

	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		hTemp_ffa0 = card;
		if (card == 0xffu)
			return;
		if ((uint8_t)GetCardIDFromDeckIndex(card) == ODDISH)
			return;
	}
}
/* <<< factory Sprout_AISelectEffect */


/* >>> factory Teleport_CheckBench */
TeleportCheckBenchResult Teleport_CheckBench(void)
{
    DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
    uint8_t f = 0x40u;
    if (count.a == 2u) f |= 0x80u;
    if ((count.a & 0x0fu) < 2u) f |= 0x20u;
    if (count.a < 2u) f |= 0x10u;
    return (TeleportCheckBenchResult){count.a, f, 0x00d2u};
}
/* <<< factory Teleport_CheckBench */


/* >>> factory Teleport_AISelectEffect */
TeleportAISelectEffectResult Teleport_AISelectEffect(void)
{
    DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
    uint8_t a = Random(count.a);
    hTemp_ffa0 = a;
    return (TeleportAISelectEffectResult){a, count.hl};
}
/* <<< factory Teleport_AISelectEffect */


/* >>> factory HornHazard_AIEffect */
/* effect_functions.asm:2050-2053 */
void HornHazard_AIEffect(void)
{
	SetExpectedAIDamage(15u, 0u, 30u);
}
/* <<< factory HornHazard_AIEffect */


/* >>> factory NidorinaDoubleKick_AIEffect */
/* effect_functions.asm:2073-2076 */
void NidorinaDoubleKick_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory NidorinaDoubleKick_AIEffect */

/* >>> factory NidorinoDoubleKick_AIEffect */
/* effect_functions.asm:...? */
void NidorinoDoubleKick_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory NidorinoDoubleKick_AIEffect */

/* >>> factory WeedlePoisonSting_AIEffect */
/* effect_functions.asm:...? */
void WeedlePoisonSting_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory WeedlePoisonSting_AIEffect */

/* >>> factory BellsproutCallForFamily_AISelectEffect */
#define BELLSPROUT 0x23u
void BellsproutCallForFamily_AISelectEffect(uint8_t c, uint16_t de)
{
	(void)CreateDeckCardList(c, de);

	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		hTemp_ffa0 = card;
		if (card == 0xffu)
			return;
		if ((uint8_t)GetCardIDFromDeckIndex(card) == BELLSPROUT)
			return;
	}
}
/* <<< factory BellsproutCallForFamily_AISelectEffect */

/* >>> factory WeezingSmog_AIEffect */
void WeezingSmog_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory WeezingSmog_AIEffect */


/* >>> factory NidoranFFurySwipes_AIEffect */
#define NIDORANF 0x14u
#define NIDORANM 0x17u
void NidoranFFurySwipes_AIEffect(void)
{
	SetExpectedAIDamage(30u / 2u, 0u, 30u);
}
/* <<< factory NidoranFFurySwipes_AIEffect */


/* >>> factory NidoranFCallForFamily_AISelectEffect */
void NidoranFCallForFamily_AISelectEffect(uint8_t c, uint16_t de)
{
	(void)CreateDeckCardList(c, de);
	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		hTemp_ffa0 = card;
		if (card == 0xffu)
			return;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(card);
		if ((uint8_t)card_id == NIDORANF || (uint8_t)card_id == NIDORANM)
			return;
	}
}
/* <<< factory NidoranFCallForFamily_AISelectEffect */


/* >>> factory ToxicGasEffect */
uint8_t ToxicGasEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory ToxicGasEffect */


/* >>> factory Sludge_AIEffect */
void Sludge_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory Sludge_AIEffect */

/* >>> factory KadabraRecover_DiscardEffect */
/* effect_functions.asm:5774-5779 */
uint8_t KadabraRecover_DiscardEffect(void)
{
	uint8_t a = hTemp_ffa0;
	PutCardInDiscardPile(a);
	return a;
}
/* <<< factory KadabraRecover_DiscardEffect */

/* >>> factory PrimeapeFurySwipes_AIEffect */
/* effect_functions.asm:5907-5914 */
PrimeapeFurySwipesAIResult PrimeapeFurySwipes_AIEffect(void)
{
	SetExpectedAIDamage(0x1eu, 0x00u, 0x3cu);
	return (PrimeapeFurySwipesAIResult){0x3cu, 0x80u, 0x00u, 0x3cu};
}
/* <<< factory PrimeapeFurySwipes_AIEffect */

/* >>> factory StretchKick_CheckBench */
/* effect_functions.asm:6186-6196 */
StretchKickCheckBenchResult StretchKick_CheckBench(void)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t f = 0x40u;

	if (r.a == 2u)
		f |= 0x80u;
	if ((r.a & 0x0fu) < 2u)
		f |= 0x20u;
	if (r.a < 2u)
		f |= 0x10u;

	return (StretchKickCheckBenchResult){r.a, f, EffectNoPokemonOnTheBenchText};
}
/* <<< factory StretchKick_CheckBench */

/* >>> factory StarmieRecover_CheckEnergyHP */
/* effect_functions.asm:5782-5804 */
StarmieRecoverCheckEnergyHPResult StarmieRecover_CheckEnergyHP(void)
{
	uint8_t energy;
	uint8_t a;
	uint8_t f;
	CardDamageResult damage;
	uint16_t hl = NotEnoughWaterEnergyText;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	energy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER));
	f = 0x40u;
	if (energy == 1u)
		f |= 0x80u;
	if ((energy & 0x0fu) < 1u)
		f |= 0x20u;
	if (energy < 1u)
		f |= 0x10u;
	if (energy < 1u)
		return (StarmieRecoverCheckEnergyHPResult){energy, f, 0u, 0u, hl};

	damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	a = damage.a;
	hl = NoDamageCountersText;
	f = 0x40u;
	if (a == 10u)
		f |= 0x80u;
	if ((a & 0x0fu) < 10u)
		f |= 0x20u;
	if (a < 10u)
		f |= 0x10u;
	return (StarmieRecoverCheckEnergyHPResult){a, f, damage.c, 1u, hl};
}
/* <<< factory StarmieRecover_CheckEnergyHP */


/* >>> factory StarmieRecover_DiscardEffect */
/* effect_functions.asm:5807-5812 */
uint8_t StarmieRecover_DiscardEffect(void)
{
	uint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR));
	PutCardInDiscardPile(card);
	return card;
}
/* <<< factory StarmieRecover_DiscardEffect */


/* >>> factory LightScreenEffect */
/* effect_functions.asm:6436-6441 */
uint16_t LightScreenEffect(void)
{
	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_HALVE_DAMAGE);
}
/* <<< factory LightScreenEffect */


/* >>> factory Cowardice_CheckUseAndBench */
/* effect_functions.asm:3391-3425 */
#define CAN_EVOLVE_THIS_TURN 0x10u
#define CannotBeUsedInTurnWhichWasPlayedText 0x00b6u
CowardiceCheckUseAndBenchResult Cowardice_CheckUseAndBench(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	if (incapable.f & 0x10u)
		return (CowardiceCheckUseAndBenchResult){incapable.f, incapable.hl};

	DuelistVarResult count = GetTurnDuelistVariable(
		DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (count.a < 2u)
		return (CowardiceCheckUseAndBenchResult){0x70u, EffectNoPokemonOnTheBenchText};

	DuelistVarResult flags = GetTurnDuelistVariable(
		(uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location));
	if ((flags.a & CAN_EVOLVE_THIS_TURN) == 0u)
		return (CowardiceCheckUseAndBenchResult){0x10u,
			CannotBeUsedInTurnWhichWasPlayedText};
	return (CowardiceCheckUseAndBenchResult){0x00u, flags.hl};
}
/* <<< factory Cowardice_CheckUseAndBench */



/* >>> factory Cowardice_ReturnToHandEffect */
/* effect_functions.asm:3428-3467 */
void Cowardice_ReturnToHandEffect(void)
{
	uint8_t location = hTemp_ffa0;
	uint8_t card = GetTurnDuelistVariable(
		(uint8_t)(DUELVARS_ARENA_CARD + location)).a;
	(void)MovePlayAreaCardToDiscardPile(location);
	if (location == PLAY_AREA_ARENA)
		(void)SwapArenaWithBenchPokemon(hAIPkmnPowerEffectParam);
	(void)MoveDiscardPileCardToHand(card);
	AddCardToHand(card);
	(void)ShiftAllPokemonToFirstPlayAreaSlots();
	wDuelDisplayedScreen = 0u;
}
/* <<< factory Cowardice_ReturnToHandEffect */

/* >>> factory CheckIfCardHasGrassEnergyAttached */
/* effect_functions.asm:2303-2340 */
CheckIfCardHasGrassEnergyAttachedResult CheckIfCardHasGrassEnergyAttached(uint8_t a)
{
	uint8_t e = (uint8_t)(a | CARD_LOCATION_PLAY_AREA);
	DuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);
	for (uint8_t index = 0; index < DECK_SIZE; index++) {
		if (gb_read8((uint16_t)(locations.hl + index)) != e)
			continue;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(index);
		if (GetCardType(card_id) != TYPE_ENERGY_GRASS)
			continue;
		return (CheckIfCardHasGrassEnergyAttachedResult){
			index, index == 0u ? 0x80u : 0x00u, e, (uint16_t)(locations.hl + index)};
	}
	return (CheckIfCardHasGrassEnergyAttachedResult){DECK_SIZE, 0x90u, e,
		(uint16_t)(locations.hl + DECK_SIZE)};
}
/* <<< factory CheckIfCardHasGrassEnergyAttached */

/* >>> factory GrimerMinimizeEffect */
/* effect_functions.asm:...? */
uint16_t GrimerMinimizeEffect(void)
{
	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_REDUCE_BY_20);
}
/* <<< factory GrimerMinimizeEffect */


/* >>> factory Quickfreeze_InitialEffect */
/* effect_functions.asm:3463-3465. scf: sets carry, clears N/H, keeps Z. */
uint8_t Quickfreeze_InitialEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory Quickfreeze_InitialEffect */


/* >>> factory FocusEnergyEffect */
/* effect_functions.asm:3509-3520 */
void FocusEnergyEffect(void)
{
	if (gb_read8(0xCCC3u) != 0x5Au)
		return;
	(void)ApplySubstatus1ToAttackingCard(0x19u);
}
/* <<< factory FocusEnergyEffect */

/* >>> factory MagnetonSonicboom_UnaffectedByColorEffect */
/* effect_functions.asm:7060-7064 */
void MagnetonSonicboom_UnaffectedByColorEffect(void)
{
	uint8_t flags = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	gb_write8((uint16_t)(wDamage_ADDR + 1u),
		(uint8_t)(flags | (uint8_t)(1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F)));
}
/* <<< factory MagnetonSonicboom_UnaffectedByColorEffect */

/* >>> factory MagnetonSonicboom_NullEffect */
/* effect_functions.asm:7065-7065 */
void MagnetonSonicboom_NullEffect(void)
{
	/* null effect */
}
/* <<< factory MagnetonSonicboom_NullEffect */

/* >>> factory ElectrodeSonicboom_UnaffectedByColorEffect */
/* effect_functions.asm:7278-7283 */
uint16_t ElectrodeSonicboom_UnaffectedByColorEffect(void)
{
	uint16_t hl = (uint16_t)(wDamage_ADDR + 1u);
	uint8_t value = gb_read8(hl);
	gb_write8(hl, (uint8_t)(value | (uint8_t)(1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F)));
	return hl;
}
/* <<< factory ElectrodeSonicboom_UnaffectedByColorEffect */

/* >>> factory EnergySpike_AISelectEffect */
/* effect_functions.asm:7365-7369 */
void EnergySpike_AISelectEffect(void)
{
	hTemp_ffa0 = 0xffu;
}
/* <<< factory EnergySpike_AISelectEffect */

/* >>> factory CometPunch_AIEffect */
/* effect_functions.asm:7794-7801 */
void CometPunch_AIEffect(void)
{
	SetExpectedAIDamage(0x28u, 0x00u, 0x50u);
}
/* <<< factory CometPunch_AIEffect */

/* >>> factory Conversion1_WeaknessCheck */
/* effect_functions.asm:8228-8251 */
Conversion1WeaknessCheckResult Conversion1_WeaknessCheck(void)
{
	DuelistVarResult result;
	uint8_t weakness;

	SwapTurn();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	LoadCardDataToBuffer2_FromDeckIndex(result.a);
	SwapTurn();

	weakness = wLoadedCard2Weakness;
	if (weakness == 0u)
		return (Conversion1WeaknessCheckResult){0u, 0x90u, NoWeaknessText};
	return (Conversion1WeaknessCheckResult){weakness, 0u, result.hl};
}
/* <<< factory Conversion1_WeaknessCheck */

/* >>> factory Conversion2_ResistanceCheck */
/* effect_functions.asm:8277-8294 */
Conversion2ResistanceCheckResult Conversion2_ResistanceCheck(void)
{
	DuelistVarResult result;
	uint8_t resistance;

	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	LoadCardDataToBuffer2_FromDeckIndex(result.a);

	resistance = wLoadedCard2Resistance;
	if (resistance == 0u)
		return (Conversion2ResistanceCheckResult){0u, 0x90u, NoResistanceText};
	return (Conversion2ResistanceCheckResult){resistance, 0u, result.hl};
}
/* <<< factory Conversion2_ResistanceCheck */

/* >>> factory ElectrodeSonicboom_NullEffect */
/* effect_functions.asm:7283-7283 */
void ElectrodeSonicboom_NullEffect(void)
{
	uint8_t null_effect_value = hTemp_ffa0;
	hTemp_ffa0 = null_effect_value;
}
/* <<< factory ElectrodeSonicboom_NullEffect */

/* >>> factory FirstAid_DamageCheck */
/* effect_functions.asm:8180-8190 */
FirstAidDamageCheckResult FirstAid_DamageCheck(void)
{
	uint8_t hp = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
	uint8_t flags = 0x40u;

	if (hp == 10u)
		flags |= 0x80u;
	if (hp < 10u)
		flags |= 0x10u;
	if ((hp & 0x0fu) < 0x0au)
		flags |= 0x20u;

	return (FirstAidDamageCheckResult){NoDamageCountersText, flags};
}
/* <<< factory FirstAid_DamageCheck */

/* >>> factory DoTheWaveEffect */
/* effect_functions.asm:8171-8183 */
void DoTheWaveEffect(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t amount = ATimes10((uint8_t)(r.a - 1u));
	AddToDamage(amount);
}
/* <<< factory DoTheWaveEffect */

/* >>> factory FullHeal_StatusCheck */
/* effect_functions.asm:9404-9415 */
FullHealStatusCheckResult FullHeal_StatusCheck(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	uint8_t status = r.a;

	if (status != 0u)
		return (FullHealStatusCheckResult){status, 0x00u, r.hl};

	return (FullHealStatusCheckResult){
		0x00u,
		(uint8_t)(0x80u | 0x10u),
		NotAffectedByPoisonSleepParalysisOrConfusionText
	};
}
/* <<< factory FullHeal_StatusCheck */

/* >>> factory PoisonFang_AIEffect */
/* effect_functions.asm:1485 */
void PoisonFang_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);
}
/* <<< factory PoisonFang_AIEffect */

/* >>> factory WeepinbellPoisonPowder_AIEffect */
/* effect_functions.asm:1490 */
void WeepinbellPoisonPowder_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory WeepinbellPoisonPowder_AIEffect */

/* >>> factory Toxic_AIEffect */
void Toxic_AIEffect(void)
{
	UpdateExpectedAIDamage(20u, 20u, 20u);
}
/* <<< factory Toxic_AIEffect */

/* >>> factory BoyfriendsEffect */
#define NIDOKING 0x19u
void BoyfriendsEffect(void)
{
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint16_t hl = arena.hl;
	uint8_t c = PLAY_AREA_ARENA;
	while (gb_read8(hl) != 0xffu) {
		uint16_t id = GetCardIDFromDeckIndex(gb_read8(hl));
		if ((uint8_t)id == NIDOKING && (uint8_t)(id >> 8) == 0u)
			c++;
		hl++;
	}
	AddToDamage(ATimes10((uint8_t)(c << 1)));
}
/* <<< factory BoyfriendsEffect */

/* >>> factory IvysaurPoisonPowder_AIEffect */
void IvysaurPoisonPowder_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);
}
/* <<< factory IvysaurPoisonPowder_AIEffect */

/* >>> factory EnergyTrans_CheckPlayArea */
EnergyTransCheckPlayAreaResult EnergyTrans_CheckPlayArea(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	if (incapable.f & 0x10u)
		return (EnergyTransCheckPlayAreaResult){location, incapable.f, incapable.hl, 0u};

	DuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);
	for (uint8_t index = 0; index < DECK_SIZE; index++) {
		uint16_t entry = (uint16_t)(locations.hl + index);
		if ((gb_read8(entry) & CARD_LOCATION_PLAY_AREA) == 0u)
			continue;
		uint16_t card_id = GetCardIDFromDeckIndex(index);
		uint8_t card_type = GetCardType((uint8_t)card_id);
		if (card_type == TYPE_ENERGY_GRASS)
			return (EnergyTransCheckPlayAreaResult){card_type, 0xC0u, entry, card_id};
	}
	return (EnergyTransCheckPlayAreaResult){DECK_SIZE, 0x90u, NoGrassEnergyText, 0u};
}
/* <<< factory EnergyTrans_CheckPlayArea */


/* >>> factory Firegiver_InitialEffect */
uint8_t Firegiver_InitialEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory Firegiver_InitialEffect */


/* >>> factory MoltresLv37DiveBomb_AIEffect */
void MoltresLv37DiveBomb_AIEffect(void)
{
	SetExpectedAIDamage(35u, 0u, 70u);
}
/* <<< factory MoltresLv37DiveBomb_AIEffect */


/* >>> factory GetEnergyAttachedMultiplierDamage */
uint16_t GetEnergyAttachedMultiplierDamage(void)
{
	SwapTurn();
	DuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);
	uint8_t count = 0u;
	for (uint8_t i = 0u; i < DECK_SIZE; i++) {
		if (gb_read8((uint16_t)(locations.hl + i)) != CARD_LOCATION_ARENA)
			continue;
		if ((GetCardType((uint8_t)GetCardIDFromDeckIndex(i)) & TYPE_ENERGY) != 0u)
			count++;
	}
	SwapTurn();
	return (uint16_t)(count * 10u);
}
/* <<< factory GetEnergyAttachedMultiplierDamage */
/* >>> factory Fly_AIEffect */
void Fly_AIEffect(void)
{
	SetExpectedAIDamage(15u, 0u, 30u);
}
/* <<< factory Fly_AIEffect */
/* >>> factory Gigashock_AISelectEffect */
void Gigashock_AISelectEffect(void)
{
	uint8_t count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint16_t list = hTempList_ADDR;
	if (count < 4u) {
		for (uint8_t slot = 1u; slot < count; slot++)
			gb_write8(list++, slot);
		gb_write8(list, 0xffu);
		return;
	}
	SwapTurn();
	for (uint8_t slot = 1u; slot < count; slot++)
		gb_write8(list++, slot);
	gb_write8(list, 0u);
	for (uint8_t offset = 0u; gb_read8((uint16_t)(hTempList_ADDR + offset)) != 0u; offset++) {
		uint16_t current_addr = (uint16_t)(hTempList_ADDR + offset);
		uint8_t current = gb_read8(current_addr);
		uint8_t current_hp =
			GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + current)).a;
		for (uint8_t next = (uint8_t)(offset + 1u);
		     gb_read8((uint16_t)(hTempList_ADDR + next)) != 0u; next++) {
			uint16_t next_addr = (uint16_t)(hTempList_ADDR + next);
			uint8_t candidate = gb_read8(next_addr);
			uint8_t candidate_hp =
				GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + candidate)).a;
			if (candidate_hp >= current_hp) {
				current_hp = candidate_hp;
				gb_write8(current_addr, candidate);
				gb_write8(next_addr, current);
				current = candidate;
			}
		}
	}
	gb_write8((uint16_t)(hTempList_ADDR + 3u), 0xffu);
	SwapTurn();
}
/* <<< factory Gigashock_AISelectEffect */

/* >>> factory Wildfire_DiscardDeckEffect */
void Wildfire_DiscardDeckEffect(void)
{
	uint8_t count = hTemp_ffa0;
	SwapTurn();
	DuelistVarResult remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t cards_left = (uint8_t)(DECK_SIZE - remaining.a);
	if (cards_left < count)
		count = cards_left;
	for (uint8_t i = 0u; i < count; i++) {
		DrawCardResult draw = DrawCardFromDeck();
		if ((draw.f & 0x10u) == 0u)
			PutCardInDiscardPile(draw.a);
	}
	LoadTxRam3(count);
	(void)DrawWideTextBox_PrintText(0x0174u);
	SwapTurn();
}
/* <<< factory Wildfire_DiscardDeckEffect */

/* >>> factory MoltresLv35DiveBomb_AIEffect */
void MoltresLv35DiveBomb_AIEffect(void)
{
	SetExpectedAIDamage(40u, 0u, 80u);
}
/* <<< factory MoltresLv35DiveBomb_AIEffect */

/* >>> factory ClefairyDoll_BenchCheck */
ClefairyDollBenchCheckResult ClefairyDoll_BenchCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(0xEFu);
	uint8_t f = (uint8_t)(count.a >= 6u ? 0x10u : 0x00u);
	if (count.a == 6u)
		f |= 0x80u;
	return (ClefairyDollBenchCheckResult){count.a, f, 0x00B2u};
}
/* <<< factory ClefairyDoll_BenchCheck */

/* >>> factory ClefairyDoll_PlaceInPlayAreaEffect */
void ClefairyDoll_PlaceInPlayAreaEffect(void)
{
	(void)PutHandPokemonCardInPlayArea(hTempCardIndex_ff9f, 0x00u);
}
/* <<< factory ClefairyDoll_PlaceInPlayAreaEffect */

/* >>> factory EnergyBurnCheck_Unreferenced */
/* effect_functions.asm:4018-4041 */
EnergyBurnCheckResult EnergyBurnCheck_Unreferenced(void)
{
    PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(PLAY_AREA_ARENA);
    if (incapable.f & 0x10u)
        return (EnergyBurnCheckResult){0x00u, incapable.f};
    DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
    uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(arena.a);
    if (card_id == 0x32u)
        return (EnergyBurnCheckResult){card_id, 0x00u};
    return (EnergyBurnCheckResult){card_id, 0x10u};
}
/* <<< factory EnergyBurnCheck_Unreferenced */

/* >>> factory FlareonRage_DamageBoostEffect */
/* effect_functions.asm:4018-4026 */
void FlareonRage_DamageBoostEffect(void)
{
    CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
    AddToDamage(r.a);
}
/* <<< factory FlareonRage_DamageBoostEffect */

/* >>> factory Shift_OncePerTurnCheck */
/* effect_functions.asm:2472-2501 */
ShiftOncePerTurnCheckResult Shift_OncePerTurnCheck(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	DuelistVarResult flags = GetTurnDuelistVariable(
		(uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location));
	if (flags.a & USED_PKMN_POWER_THIS_TURN)
		return (ShiftOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	return (ShiftOncePerTurnCheckResult){incapable.f, incapable.hl};
}
/* <<< factory Shift_OncePerTurnCheck */

/* >>> factory VenomPowder_AIEffect */
void VenomPowder_AIEffect(void)
{
	UpdateExpectedAIDamage(5u, 0u, 10u);
}
/* <<< factory VenomPowder_AIEffect */

/* >>> factory TangelaPoisonPowder_AIEffect */
/* effect_functions.asm:2572-2575 */
void TangelaPoisonPowder_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory TangelaPoisonPowder_AIEffect */

/* >>> factory PetalDance_AIEffect */
/* effect_functions.asm:2653-2656 */
void PetalDance_AIEffect(void)
{
	SetExpectedAIDamage(60u, 0u, 120u);
}
/* <<< factory PetalDance_AIEffect */

/* >>> factory RainDanceEffect */
/* effect_functions.asm:8058-8059. scf: sets carry, clears N/H, keeps Z. */
uint8_t RainDanceEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory RainDanceEffect */

/* >>> factory PsyduckFurySwipes_AIEffect */
void PsyduckFurySwipes_AIEffect(void)
{
	SetExpectedAIDamage((uint8_t)(30u / 2u), 0u, 30u);
}
/* <<< factory PsyduckFurySwipes_AIEffect */

/* >>> factory VaporeonQuickAttack_AIEffect */
void VaporeonQuickAttack_AIEffect(void)
{
	SetExpectedAIDamage((10u + 30u) / 2u, 10u, 30u);
}
/* <<< factory VaporeonQuickAttack_AIEffect */

/* >>> factory JellyfishSting_AIEffect */
/* effect_functions.asm:3176-3179 */
void JellyfishSting_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(10u, 10u, 10u);
}
/* <<< factory JellyfishSting_AIEffect */

/* >>> factory PoliwhirlAmnesia_CheckAttacks */
/* effect_functions.asm:3182-3219 */
PoliwhirlAmnesiaCheckAttacksResult PoliwhirlAmnesia_CheckAttacks(void)
{
	SwapTurn();
	uint8_t index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	(void)LoadCardDataToBuffer2_FromDeckIndex(index);
	uint8_t category = gb_read8(wLoadedCard2Atk1Category_ADDR);
	if (category == POKEMON_POWER) {
		uint8_t lo = gb_read8(wLoadedCard2Atk2Name_ADDR);
		uint8_t hi = gb_read8((uint16_t)(wLoadedCard2Atk2Name_ADDR + 1u));
		if ((uint8_t)(lo | hi) == 0u) {
			SwapTurn();
			return (PoliwhirlAmnesiaCheckAttacksResult){0x90u, 0x00C5u};
		}
		SwapTurn();
		return (PoliwhirlAmnesiaCheckAttacksResult){0x00u, 0u};
	}
	SwapTurn();
	return (PoliwhirlAmnesiaCheckAttacksResult){
		(uint8_t)(category == 0u ? 0x80u : 0x00u), 0u};
}
/* <<< factory PoliwhirlAmnesia_CheckAttacks */

/* >>> factory HeadacheEffect */
void HeadacheEffect(void)
{
	DuelistVarResult substatus = GetNonTurnDuelistVariable(0xEBu);
	gb_write8(substatus.hl, (uint8_t)(substatus.a | (1u << SUBSTATUS3_HEADACHE_F)));
}
/* <<< factory HeadacheEffect */

/* >>> factory ArcanineQuickAttack_AIEffect */
void ArcanineQuickAttack_AIEffect(void)
{
	SetExpectedAIDamage((10u + 30u) / 2u, 10u, 30u);
}
/* <<< factory ArcanineQuickAttack_AIEffect */

/* >>> factory FlamesOfRage_CheckEnergy */
FlamesOfRageCheckEnergyResult FlamesOfRage_CheckEnergy(void)
{
	uint8_t a;
	uint8_t f = 0x40u;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	if (a == 2u)
		f |= 0x80u;
	if (a < 2u)
		f |= 0x10u;
	if ((a & 0x0fu) < 2u)
		f |= 0x20u;
	return (FlamesOfRageCheckEnergyResult){a, f, PLAY_AREA_ARENA,
		NotEnoughFireEnergyText};
}
/* <<< factory FlamesOfRage_CheckEnergy */

/* >>> factory MagmarFlamethrower_DiscardEffect */
/* effect_functions.asm:3913-3918 */
uint8_t MagmarFlamethrower_DiscardEffect(void)
{
	uint8_t card = gb_read8(hTemp_ffa0_ADDR);
	PutCardInDiscardPile(card);
	return card;
}
/* <<< factory MagmarFlamethrower_DiscardEffect */

/* >>> factory MagmarSmog_AIEffect */
/* effect_functions.asm:3921-3928 */
void MagmarSmog_AIEffect(void)
{
	UpdateExpectedAIDamage_AccountForPoison(5u, 0u, 10u);
}
/* <<< factory MagmarSmog_AIEffect */

/* >>> factory Wildfire_CheckEnergy */
/* effect_functions.asm:3735-3748 */
WildfireCheckEnergyResult Wildfire_CheckEnergy(void)
{
	uint8_t energy;
	uint8_t f = 0x40u;
	uint16_t hl = NotEnoughFireEnergyText;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	energy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	if (energy == 1u)
		f |= 0x80u;
	if ((energy & 0x0fu) == 0u)
		f |= 0x20u;
	if (energy == 0u)
		f |= 0x10u;
	return (WildfireCheckEnergyResult){energy, f, PLAY_AREA_ARENA, hl};
}
/* <<< factory Wildfire_CheckEnergy */

/* >>> factory MrMimeMeditate_DamageBoostEffect */
void MrMimeMeditate_DamageBoostEffect(void)
{
	SwapTurn();
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	SwapTurn();
	AddToDamage(r.a);
}
/* <<< factory MrMimeMeditate_DamageBoostEffect */

/* >>> factory DancingEmbers_AIEffect */
/* effect_functions.asm:4111-4114 */
void DancingEmbers_AIEffect(void)
{
	SetExpectedAIDamage(80u / 2u, 0u, 80u);
}
/* <<< factory DancingEmbers_AIEffect */

/* >>> factory FlareonFlamethrower_DiscardEffect */
/* effect_functions.asm:3891-3896 */
uint8_t FlareonFlamethrower_DiscardEffect(void)
{
	uint8_t card = gb_read8((uint16_t)(hTemp_ffa0_ADDR));
	PutCardInDiscardPile(card);
	return card;
}
/* <<< factory FlareonFlamethrower_DiscardEffect */

/* >>> factory MagmarFlamethrower_CheckEnergy */
/* effect_functions.asm:3899-3912 */
MagmarFlamethrowerCheckEnergyResult MagmarFlamethrower_CheckEnergy(void)
{
	uint8_t a;
	uint8_t flags = 0x40u;
	uint16_t magmar_hl = NotEnoughFireEnergyText;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	if ((a & 0x0fu) == 0u)
		flags |= 0x20u;
	if (a == 1u)
		flags |= 0x80u;
	if (a < 1u)
		flags |= 0x10u;
	return (MagmarFlamethrowerCheckEnergyResult){a, flags, magmar_hl};
}
/* <<< factory MagmarFlamethrower_CheckEnergy */

/* >>> factory FlamesOfRage_DiscardEffect */
/* effect_functions.asm:...? */
void FlamesOfRage_DiscardEffect(void)
{
	PutCardInDiscardPile(gb_read8(hTempList_ADDR));
	PutCardInDiscardPile(gb_read8((uint16_t)(hTempList_ADDR + 1u)));
}
/* <<< factory FlamesOfRage_DiscardEffect */

/* >>> factory FlamesOfRage_DamageBoostEffect */
/* effect_functions.asm:...? */
void FlamesOfRage_DamageBoostEffect(void)
{
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	AddToDamage(r.a);
}
/* <<< factory FlamesOfRage_DamageBoostEffect */

/* >>> factory CharmeleonFlamethrower_CheckEnergy */
/* effect_functions.asm:3929-3942 */
CharmeleonFlamethrowerCheckEnergyResult CharmeleonFlamethrower_CheckEnergy(void)
{
	uint8_t energy;
	uint8_t f;
	uint16_t hl = NotEnoughFireEnergyText;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	energy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	f = 0x40u;
	if (energy == 1u)
		f |= 0x80u;
	if ((energy & 0x0fu) == 0u)
		f |= 0x20u;
	if (energy == 0u)
		f |= 0x10u;
	return (CharmeleonFlamethrowerCheckEnergyResult){energy, f, 0u, hl};
}
/* <<< factory CharmeleonFlamethrower_CheckEnergy */

/* >>> factory CharmeleonFlamethrower_DiscardEffect */
/* effect_functions.asm:3945-3950 */
uint8_t CharmeleonFlamethrower_DiscardEffect(void)
{
	uint8_t card = gb_read8(hTemp_ffa0_ADDR);
	PutCardInDiscardPile(card);
	return card;
}
/* <<< factory CharmeleonFlamethrower_DiscardEffect */

/* >>> factory EnergyBurnEffect */
EnergyBurnEffectResult EnergyBurnEffect(uint8_t f)
{
	return (EnergyBurnEffectResult){(uint8_t)((f & 0x80u) | 0x10u)};
}
/* <<< factory EnergyBurnEffect */

/* >>> factory FireSpin_CheckEnergy */
FireSpinCheckEnergyResult FireSpin_CheckEnergy(void)
{
	(void)CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);
	uint8_t count = CountCardsInDuelTempList().a;
	uint8_t f = 0x40u;
	if ((count & 0x0fu) < 2u)
		f |= 0x20u;
	if (count < 2u)
		f |= 0x10u;
	if (count == 2u)
		f |= 0x80u;
	return (FireSpinCheckEnergyResult){count, f, NotEnoughEnergyCardsText};
}
/* <<< factory FireSpin_CheckEnergy */

/* >>> factory FlareonQuickAttack_AIEffect */
/* effect_functions.asm:3859-3866 */
void FlareonQuickAttack_AIEffect(void)
{
	SetExpectedAIDamage((uint8_t)(40u / 2u), 10u, 30u);
}
/* <<< factory FlareonQuickAttack_AIEffect */

/* >>> factory FlareonFlamethrower_CheckEnergy */
/* effect_functions.asm:3875-3888 */
FlareonFlamethrowerCheckEnergyResult FlareonFlamethrower_CheckEnergy(void)
{
	uint8_t a;
	uint8_t f = 0x40u;

	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + FIRE));
	if ((a & 0x0fu) < 1u)
		f |= 0x20u;
	if (a < 1u)
		f |= 0x10u;
	if (a == 1u)
		f |= 0x80u;
	return (FlareonFlamethrowerCheckEnergyResult){a, f, PLAY_AREA_ARENA,
		NotEnoughFireEnergyText};
}
/* <<< factory FlareonFlamethrower_CheckEnergy */

/* >>> factory Prophecy_AISelectEffect */
/* effect_functions.asm:4756-4760 */
ProphecyAISelectEffectResult Prophecy_AISelectEffect(void)
{
	hTemp_ffa0 = 0xffu;
	return (ProphecyAISelectEffectResult){0xffu};
}
/* <<< factory Prophecy_AISelectEffect */

/* >>> factory Prophecy_ReorderDeckEffect */
/* effect_functions.asm:4763-4815 */
ProphecyReorderDeckEffectResult Prophecy_ReorderDeckEffect(void)
{
	uint16_t hl = hTempList_ADDR;
	uint8_t a = gb_read8(hl++);
	if (a == 0xffu)
		return (ProphecyReorderDeckEffectResult){a, 0u, 0x00u, hl};
	if (a != 0u)
		SwapTurn();

	uint8_t c = 0u;
	for (;;) {
		a = gb_read8(hl++);
		if (a == 0xffu)
			break;
		SearchCardInDeckAndAddToHand(a);
		c = (uint8_t)(c + 1u);
	}
	hl = (uint16_t)(hl - 2u);
	do {
		a = gb_read8(hl--);
		ReturnCardToDeck(a);
		c = (uint8_t)(c - 1u);
	} while (c != 0u);

	IsPlayerTurnResult turn = IsPlayerTurn();
	if (!(turn.f & 0x10u)) {
		WaitResult wait = DrawWideTextBox_WaitForInput(0x0184u);
		if (a == 0u)
			a = turn.a;
		return (ProphecyReorderDeckEffectResult){a, c, wait.f, hl};
	}
	return (ProphecyReorderDeckEffectResult){turn.a, c, turn.f, turn.hl};
}
/* <<< factory Prophecy_ReorderDeckEffect */

/* >>> factory SuperEnergyRetrieval_HandEnergyCheck */
/* effect_functions.asm:10979-10996 */
SuperEnergyRetrievalHandEnergyCheckResult SuperEnergyRetrieval_HandEnergyCheck(void)
{
	DuelistVarResult hand = GetTurnDuelistVariable(0xeeu);
	if (hand.a < 3u)
		return (SuperEnergyRetrievalHandEnergyCheckResult){NotEnoughCardsInHandText, 0x70u};

	CreateEnergyCardListFromDiscardPileResult energy =
		CreateEnergyCardListFromDiscardPile_OnlyBasic();
	return (SuperEnergyRetrievalHandEnergyCheckResult){
		ThereAreNoBasicEnergyCardsInDiscardPileText, energy.f
	};
}
/* <<< factory SuperEnergyRetrieval_HandEnergyCheck */

/* >>> factory GetNextPositionInTempList_TrainerEffects */
/* effect_functions.asm:11065-11079 */
uint16_t GetNextPositionInTempList_TrainerEffects(void)
{
	uint8_t selection = hCurSelectionItem;
	hCurSelectionItem = (uint8_t)(selection + 1u);
	return (uint16_t)(hTempList_ADDR + selection);
}
/* <<< factory GetNextPositionInTempList_TrainerEffects */

/* >>> factory NinetalesLure_AISelectEffect */
/* effect_functions.asm:3674-3679 */
uint8_t NinetalesLure_AISelectEffect(void)
{
	AIFindTargetForBenchAttackResult r = AIFindTargetForBenchAttack();
	hTemp_ffa0 = r.a;
	return r.a;
}
/* <<< factory NinetalesLure_AISelectEffect */

/* >>> factory Ember_CheckEnergy */
/* effect_functions.asm:3713-3726 */
EmberCheckEnergyResult Ember_CheckEnergy(void)
{
	GetPlayAreaCardAttachedEnergies(0u);
	uint8_t fire = wAttachedEnergies;
	uint8_t flags = 0x40u;

	if (fire == 1u)
		flags = (uint8_t)(flags | 0x80u);
	if (fire < 1u)
		flags = (uint8_t)(flags | 0x30u);
	if (fire != 0u && (fire & 0x0fu) == 0u)
		flags = (uint8_t)(flags | 0x20u);

	return (EmberCheckEnergyResult){fire, flags, NotEnoughFireEnergyText};
}
/* <<< factory Ember_CheckEnergy */

/* >>> factory DestinyBond_CheckEnergy */
/* effect_functions.asm:4593-4606 */
IsPlayerTurnResult DestinyBond_CheckEnergy(void)
{
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	uint8_t a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + PSYCHIC));
	uint16_t hl = NotEnoughPsychicEnergyText;
	uint8_t f = 0x40u;

	if ((a & 0x0fu) < 1u)
		f |= 0x20u;
	if (a < 1u)
		f |= 0x10u;
	if (a == 1u)
		f |= 0x80u;

	return (IsPlayerTurnResult){a, f, hl};
}
/* <<< factory DestinyBond_CheckEnergy */

/* >>> factory ComputerSearch_HandDeckCheck */
/* effect_functions.asm:9455-9477 */
ComputerSearchHandDeckCheckResult ComputerSearch_HandDeckCheck(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (r.a < 3u)
		return (ComputerSearchHandDeckCheckResult){
			r.a, (uint8_t)(effect_compare(r.a, 3u)), NotEnoughCardsInHandText
		};

	r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	return (ComputerSearchHandDeckCheckResult){
		r.a,
		(uint8_t)(effect_compare(r.a, DECK_SIZE) ^ 0x10u),
		NoCardsLeftInTheDeckText
	};
}
/* <<< factory ComputerSearch_HandDeckCheck */

/* >>> factory MrFuji_BenchCheck */
/* effect_functions.asm:9516-9526 */
MrFujiBenchCheckResult MrFuji_BenchCheck(void)
{
	DuelistVarResult r = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	return (MrFujiBenchCheckResult){
		r.a,
		effect_compare(r.a, 2u),
		EffectNoPokemonOnTheBenchText
	};
}
/* <<< factory MrFuji_BenchCheck */
/* >>> factory StepIn_BenchCheck */
/* effect_functions.asm:7708-7718 */
SolarPowerCheckUseResult StepIn_BenchCheck(void)
{
	if (hTempPlayAreaLocation_ff9d == PLAY_AREA_ARENA)
		return (SolarPowerCheckUseResult){0x90u, 0x00D1u};
	return (SolarPowerCheckUseResult){0x80u, 0x00D4u};
}
/* <<< factory StepIn_BenchCheck */
/* >>> factory Peek_OncePerTurnCheck */
/* effect_functions.asm:6254-6277 */
SolarPowerCheckUseResult Peek_OncePerTurnCheck(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	DuelistVarResult flags = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_FLAGS + location));
	if (flags.a & USED_PKMN_POWER_THIS_TURN)
		return (SolarPowerCheckUseResult){0x10u, 0x00CAu};
	PkmnPowerIncapableResult r = CheckIsIncapableOfUsingPkmnPower(location);
	return (SolarPowerCheckUseResult){r.f, r.hl};
}
/* <<< factory Peek_OncePerTurnCheck */

/* >>> factory Wail_BenchCheck */
/* effect_functions.asm:6339-6363 */
MrFujiBenchCheckResult Wail_BenchCheck(void)
{
	DuelistVarResult turn = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (turn.a < 6u)
		return (MrFujiBenchCheckResult){turn.a, turn.a == 0u ? 0x80u : 0u, turn.hl};
	DuelistVarResult nonturn = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (nonturn.a < 6u)
		return (MrFujiBenchCheckResult){nonturn.a, nonturn.a == 0u ? 0x80u : 0u, nonturn.hl};
	return (MrFujiBenchCheckResult){nonturn.a, 0x10u, 0x00B2u};
}
/* <<< factory Wail_BenchCheck */

/* >>> factory StepIn_SwitchEffect */
/* effect_functions.asm:7719-7732 */
void StepIn_SwitchEffect(void)
{
	SwapAreaResult r = SwapArenaWithBenchPokemon(hTemp_ffa0);
	(void)r;
	DuelistVarResult flags = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_FLAGS);
	gb_write8(flags.hl, (uint8_t)(gb_read8(flags.hl) | USED_PKMN_POWER_THIS_TURN));
}
/* <<< factory StepIn_SwitchEffect */

/* >>> factory ThickSkinnedEffect */
/* effect_functions.asm:7745-7746 */
uint8_t ThickSkinnedEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory ThickSkinnedEffect */

/* >>> factory HealingWind_InitialEffect */
/* effect_functions.asm:8489-8490 */
uint8_t HealingWind_InitialEffect(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory HealingWind_InitialEffect */

/* >>> factory PickRandomBasicCardFromDeck */
/* effect_functions.asm:8712-8750 */
uint8_t PickRandomBasicCardFromDeck(void)
{
	CardListResult list = CreateDeckCardList(0u, 0u);
	if (list.f & 0x10u)
		return 0xFFu;
	(void)ShuffleCards(0u, wDuelTempList_ADDR);
	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t index = gb_read8(hl++);
		hTempCardIndex_ff98 = index;
		if (index == 0xFFu)
			return 0xFFu;
		LoadCardDataToBuffer2_FromDeckIndex(index);
		if (wLoadedCard2Type >= TYPE_ENERGY || wLoadedCard2Stage != 0u)
			continue;
		return index;
	}
}
/* <<< factory PickRandomBasicCardFromDeck */

/* >>> factory DreamEaterEffect */
/* effect_functions.asm:4688-4702 */
DreamEaterEffectResult DreamEaterEffect(void)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	uint8_t masked = (uint8_t)(r.a & CNF_SLP_PRZ);

	if (masked == ASLEEP)
		return (DreamEaterEffectResult){masked, 0xc0u, r.hl};

	return (DreamEaterEffectResult){masked, 0x10u, OpponentIsNotAsleepText};
}
/* <<< factory DreamEaterEffect */

/* >>> factory JynxMeditate_DamageBoostEffect */
/* effect_functions.asm:5806-5818 */
void JynxMeditate_DamageBoostEffect(void)
{
	SwapTurn();
	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	SwapTurn();
	AddToDamage(damage.a);
}
/* <<< factory JynxMeditate_DamageBoostEffect */

/* >>> factory KadabraRecover_CheckEnergyHP */
/* effect_functions.asm:5744-5766 */
KadabraRecoverCheckEnergyHPResult KadabraRecover_CheckEnergyHP(void)
{
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	uint8_t energy = gb_read8((uint16_t)(wAttachedEnergies_ADDR + PSYCHIC));
	uint8_t f = 0x40u;
	uint16_t hl = NotEnoughPsychicEnergyText;
	if (energy == 1u)
		f |= 0x80u;
	if ((energy & 0x0fu) < 1u)
		f |= 0x20u;
	if (energy < 1u)
		f |= 0x10u;
	if (energy < 1u)
		return (KadabraRecoverCheckEnergyHPResult){energy, f, 0u, 0u, hl};
	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	f = 0x40u;
	hl = NoDamageCountersText;
	if (damage.a == 10u)
		f |= 0x80u;
	if ((damage.a & 0x0fu) < 10u)
		f |= 0x20u;
	if (damage.a < 10u)
		f |= 0x10u;
	return (KadabraRecoverCheckEnergyHPResult){damage.a, f, damage.c, 1u, hl};
}
/* <<< factory KadabraRecover_CheckEnergyHP */

/* >>> factory MewtwoAltEnergyAbsorption_AddToHandEffect */
/* effect_functions.asm:5461-5479 */
void MewtwoAltEnergyAbsorption_AddToHandEffect(void)
{
	for (uint8_t i = 0u;; i++) {
		uint8_t card = gb_read8((uint16_t)(hTempList_ADDR + i));
		if (card == 0xffu)
			return;
		(void)MoveDiscardPileCardToHand(card);
		DuelistVarResult location = GetTurnDuelistVariable(
			(uint8_t)(DUELVARS_CARD_LOCATIONS + card));
		gb_write8(location.hl, CARD_LOCATION_ARENA);
	}
}
/* <<< factory MewtwoAltEnergyAbsorption_AddToHandEffect */

/* >>> factory MewtwoEnergyAbsorption_AddToHandEffect */
/* effect_functions.asm:5503-5521 */
void MewtwoEnergyAbsorption_AddToHandEffect(void)
{
	MewtwoAltEnergyAbsorption_AddToHandEffect();
}
/* <<< factory MewtwoEnergyAbsorption_AddToHandEffect */

/* >>> factory NeutralizingShieldEffect */
/* effect_functions.asm:5375-5377 */
uint8_t NeutralizingShieldEffect(void)
{
	return 0x10u;
}
/* <<< factory NeutralizingShieldEffect */

/* >>> factory PealOfThunder_InitialEffect */
/* effect_functions.asm:7087-7089 */
uint8_t PealOfThunder_InitialEffect(void)
{
	return 0x10u;
}
/* <<< factory PealOfThunder_InitialEffect */

/* >>> factory PrehistoricPowerEffect */
/* effect_functions.asm:6249-6251 */
uint8_t PrehistoricPowerEffect(void)
{
	return 0x10u;
}
/* <<< factory PrehistoricPowerEffect */

/* >>> factory Scavenge_DiscardEffect */
/* effect_functions.asm:5694-5697 */
uint8_t Scavenge_DiscardEffect(void)
{
	uint8_t card = gb_read8(hTemp_ffa0_ADDR);
	PutCardInDiscardPile(card);
	return card;
}
/* <<< factory Scavenge_DiscardEffect */

/* >>> factory DrawSymbolOnPlayAreaCursor */
/* effect_functions.asm:1401-1413 */
void DrawSymbolOnPlayAreaCursor(uint8_t a, uint8_t b)
{
	uint8_t row = (uint8_t)(a * 3u + 2u);
	WriteByteToBGMap0(b, 0u, row);
}
/* <<< factory DrawSymbolOnPlayAreaCursor */
/* >>> factory Func_2c6d9 */
/* effect_functions.asm:1414-1417 */
WaitResult Func_2c6d9(void)
{
	return DrawWideTextBox_WaitForInput(0x0031u);
}
/* <<< factory Func_2c6d9 */


/* >>> factory MarowakCallForFamily_AISelectEffect */
/* effect_functions.asm:6072-6100 */
void MarowakCallForFamily_AISelectEffect(void)
{
	(void)CreateDeckCardList(0u, 0u);
	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		hTemp_ffa0 = card;
		if (card == 0xffu)
			return;
		LoadCardDataToBuffer2_FromDeckIndex(card);
		if (gb_read8(wLoadedCard2Type_ADDR) != 0x02u)
			continue;
		if (gb_read8(wLoadedCard2Stage_ADDR) == 0u)
			return;
	}
}
/* <<< factory MarowakCallForFamily_AISelectEffect */

/* >>> factory GustOfWind_BenchCheck */
/* effect_functions.asm:11131-11141 */
IsPlayerTurnResult GustOfWind_BenchCheck(void)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(
		DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t flags = 0x40u;
	uint8_t value = r.a;
	if (value < 2u)
		flags |= 0x10u;
	if ((value & 0x0fu) < 2u)
		flags |= 0x20u;
	if (value == 2u)
		flags |= 0x80u;
	return (IsPlayerTurnResult){value, flags, EffectNoPokemonOnTheBenchText};
}
/* <<< factory GustOfWind_BenchCheck */
#define NoSpaceOnTheBenchText 0x00b2u

/* >>> factory VictreebelLure_AssertPokemonInBench */
/* effect_functions.asm:1496-1501 */
VictreebelLureAssertPokemonInBenchResult VictreebelLure_AssertPokemonInBench(void)
{
	DuelistVarResult count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	return (VictreebelLureAssertPokemonInBenchResult){
		count.a, effect_compare(count.a, 2u), EffectNoPokemonOnTheBenchText
	};
}
/* <<< factory VictreebelLure_AssertPokemonInBench */

/* >>> factory NinetalesLure_CheckBench */
/* effect_functions.asm:3654-3659 */
NinetalesLureCheckBenchResult NinetalesLure_CheckBench(void)
{
	DuelistVarResult count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	return (NinetalesLureCheckBenchResult){
		count.a, effect_compare(count.a, 2u), EffectNoPokemonOnTheBenchText
	};
}
/* <<< factory NinetalesLure_CheckBench */

/* >>> factory ThunderboltEffect */
/* effect_functions.asm:6491-6501 */
void ThunderboltEffect(void)
{
	(void)CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);
	for (uint8_t i = 0;; i++) {
		uint8_t card = gb_read8((uint16_t)(wDuelTempList_ADDR + i));
		if (card == 0xffu)
			break;
		PutCardInDiscardPile(card);
	}
}
/* <<< factory ThunderboltEffect */

/* >>> factory TrainerCardAsPokemon_BenchCheck */
/* effect_functions.asm:8453-8460 */
TrainerCardAsPokemonBenchCheckResult TrainerCardAsPokemon_BenchCheck(void)
{
	hTemp_ffa0 = hTempPlayAreaLocation_ff9d;
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	return (TrainerCardAsPokemonBenchCheckResult){
		count.a, effect_compare(count.a, 2u), EffectNoPokemonOnTheBenchText
	};
}
/* <<< factory TrainerCardAsPokemon_BenchCheck */

/* >>> factory TrainerCardAsPokemon_DiscardEffect */
/* effect_functions.asm:8475-8487 */
void TrainerCardAsPokemon_DiscardEffect(void)
{
	uint8_t location = hTemp_ffa0;
	(void)MovePlayAreaCardToDiscardPile(location);
	if (location == PLAY_AREA_ARENA)
		(void)SwapArenaWithBenchPokemon(hTempPlayAreaLocation_ffa1);
	(void)ShiftAllPokemonToFirstPlayAreaSlots();
}
/* <<< factory TrainerCardAsPokemon_DiscardEffect */

/* >>> factory MysteriousFossil_BenchCheck */
/* effect_functions.asm:9390-9396 */
MysteriousFossilBenchCheckResult MysteriousFossil_BenchCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t f = count.a == 6u ? 0x90u : (count.a > 6u ? 0x10u : 0u);
	return (MysteriousFossilBenchCheckResult){count.a, f, NoSpaceOnTheBenchText};
}
/* <<< factory MysteriousFossil_BenchCheck */

/* >>> factory MysteriousFossil_PlaceInPlayAreaEffect */
/* effect_functions.asm:9398-9401 */
void MysteriousFossil_PlaceInPlayAreaEffect(void)
{
	(void)PutHandPokemonCardInPlayArea(hTempCardIndex_ff9f, 0x00u);
}
/* <<< factory MysteriousFossil_PlaceInPlayAreaEffect */

/* >>> factory ScoopUp_BenchCheck */
/* effect_functions.asm:9905-9910 */
ScoopUpBenchCheckResult ScoopUp_BenchCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	return (ScoopUpBenchCheckResult){
		count.a, effect_compare(count.a, 2u), EffectNoPokemonOnTheBenchText
	};
}
/* <<< factory ScoopUp_BenchCheck */
/* >>> factory CreateListOfFireEnergyAttachedToArena */
/* effect_functions.asm:340-341 */
CreateListOfEnergyAttachedToArenaResult CreateListOfFireEnergyAttachedToArena(void)
{
	return CreateListOfEnergyAttachedToArena(0x08u);
}
/* <<< factory CreateListOfFireEnergyAttachedToArena */

/* >>> factory CreateEnergyCardListFromDiscardPile_AllEnergy */
/* effect_functions.asm:588-589 */
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile_AllEnergy(void)
{
	return CreateEnergyCardListFromDiscardPile(0x00u);
}
/* <<< factory CreateEnergyCardListFromDiscardPile_AllEnergy */

/* >>> factory CheckIfDeckIsEmpty */
/* effect_functions.asm:658-669 */
CheckIfDeckIsEmptyResult CheckIfDeckIsEmpty(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(
		DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t f = count.a >= DECK_SIZE ? 0x10u : 0x00u;
	if (count.a == DECK_SIZE)
		f |= 0x80u;
	return (CheckIfDeckIsEmptyResult){count.a, TX_NoCardsLeftInTheDeckText, f};
}
/* <<< factory CheckIfDeckIsEmpty */


/* >>> factory Toxic_DoublePoisonEffect */
/* effect_functions.asm:1892-1894 */
QueueStatusConditionResult Toxic_DoublePoisonEffect(void)
{
	return DoublePoisonEffect();
}
/* <<< factory Toxic_DoublePoisonEffect */
/* >>> factory LeekSlap_OncePerDuelCheck */
/* effect_functions.asm:7755-7763 */
uint8_t LeekSlap_OncePerDuelCheck(void)
{
	DuelistVarResult flags = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_FLAGS);
	if ((gb_read8(flags.hl) & (uint8_t)(1u << USED_LEEK_SLAP_THIS_DUEL_F)) == 0u)
		return 0xA0u;
	return 0x30u;
}
/* <<< factory LeekSlap_OncePerDuelCheck */

/* >>> factory LeekSlap_SetUsedThisDuelFlag */
/* effect_functions.asm:7765-7769 */
void LeekSlap_SetUsedThisDuelFlag(void)
{
	DuelistVarResult flags = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_FLAGS);
	gb_write8(flags.hl, (uint8_t)(gb_read8(flags.hl) | (uint8_t)(1u << USED_LEEK_SLAP_THIS_DUEL_F)));
}
/* <<< factory LeekSlap_SetUsedThisDuelFlag */

/* >>> factory PlusPowerEffect */
/* effect_functions.asm:9589-9599 */
void PlusPowerEffect(void)
{
	(void)PutHandCardInPlayArea(hTempCardIndex_ff9f, PLAY_AREA_ARENA);
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER);
	gb_write8(count.hl, (uint8_t)(gb_read8(count.hl) + 1u));
}
/* <<< factory PlusPowerEffect */

/* >>> factory StrikesBackEffect */
/* effect_functions.asm:5935-5937 */
uint8_t StrikesBackEffect(void)
{
	return 0x10u;
}
/* <<< factory StrikesBackEffect */

/* >>> factory Switch_BenchCheck */
/* effect_functions.asm:9602-9607 */
MrFujiBenchCheckResult Switch_BenchCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	return (MrFujiBenchCheckResult){count.a, effect_compare(count.a, 2u), EffectNoPokemonOnTheBenchText};
}
/* <<< factory Switch_BenchCheck */

/* >>> factory Switch_SwitchEffect */
/* effect_functions.asm:9618-9622 */
void Switch_SwitchEffect(void)
{
	(void)SwapArenaWithBenchPokemon(hTemp_ffa0);
}
/* <<< factory Switch_SwitchEffect */
/* >>> factory TryGiveDamageCounter_StrangeBehavior */
/* effect_functions.asm:5605-5623 */
TryGiveDamageCounter_StrangeBehaviorResult TryGiveDamageCounter_StrangeBehavior(void)
{
	uint8_t source = gb_read8((uint16_t)hTemp_ffa0_ADDR);
	uint8_t target = gb_read8((uint16_t)hTempPlayAreaLocation_ffa1_ADDR);
	DuelistVarResult source_hp =
		GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + source));
	uint8_t remaining = (uint8_t)(source_hp.a - 10u);
	if (remaining == 0u)
		return (TryGiveDamageCounter_StrangeBehaviorResult){0u, 0x10u, source_hp.hl};
	gb_write8(source_hp.hl, remaining);
	DuelistVarResult target_hp =
		GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + target));
	uint8_t new_hp = (uint8_t)(10u + target_hp.a);
	gb_write8(target_hp.hl, new_hp);
	return (TryGiveDamageCounter_StrangeBehaviorResult){
		new_hp, (uint8_t)(new_hp == 0u ? 0x80u : 0u), target_hp.hl
	};
}
/* <<< factory TryGiveDamageCounter_StrangeBehavior */

/* >>> factory SpacingOut_CheckDamage */
/* effect_functions.asm:5626-5630 */
SpacingOutCheckDamageResult SpacingOut_CheckDamage(void)
{
	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	return (SpacingOutCheckDamageResult){
		damage.a, effect_compare(damage.a, 10u), damage.c, 0u, NoDamageCountersText
	};
}
/* <<< factory SpacingOut_CheckDamage */

/* >>> factory SpacingOut_HealEffect */
/* effect_functions.asm:5642-5654 */
SpacingOutHealEffectResult SpacingOut_HealEffect(void)
{
	uint8_t coin = gb_read8((uint16_t)hTemp_ffa0_ADDR);
	if (coin == 0u)
		return (SpacingOutHealEffectResult){0u, 0x80u, 0u, 0u};
	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	if (damage.a == 0u)
		return (SpacingOutHealEffectResult){0u, 0x80u, 0u, 0u};
	DuelistVarResult hp =
		GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t new_hp = (uint8_t)(10u + hp.a);
	uint8_t f = 0u;
	if (new_hp == 0u)
		f |= 0x80u;
	if ((hp.a & 0x0fu) + 10u > 0x0fu)
		f |= 0x20u;
	if ((uint16_t)hp.a + 10u > 0xffu)
		f |= 0x10u;
	gb_write8(hp.hl, new_hp);
	return (SpacingOutHealEffectResult){new_hp, f, hp.hl, 1u};
}
/* <<< factory SpacingOut_HealEffect */
/* >>> factory CopyPlayAreaHPToBackup_Unreferenced */
void CopyPlayAreaHPToBackup_Unreferenced(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint16_t n = count.a ? count.a : 0x100u;
	for (uint16_t i = 0; i < n; i++)
		gb_write8((uint16_t)(wBackupPlayerAreaHP_ADDR + i), gb_read8((uint16_t)(hp.hl + i)));
}
/* <<< factory CopyPlayAreaHPToBackup_Unreferenced */
void CopyPlayAreaHPFromBackup_Unreferenced(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint16_t n = count.a ? count.a : 0x100u;
	for (uint16_t i = 0; i < n; i++)
		gb_write8((uint16_t)(hp.hl + i), gb_read8((uint16_t)(wBackupPlayerAreaHP_ADDR + i)));
}
/* <<< factory CopyPlayAreaHPFromBackup_Unreferenced */

/* >>> factory Gale_LoadAnimation */
void Gale_LoadAnimation(void)
{
	wLoadedAttackAnimation = 0x87u;
}
/* <<< factory Gale_LoadAnimation */

/* >>> factory EnergySearch_DeckCheck */
uint8_t EnergySearch_DeckCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (count.a == DECK_SIZE)
		return 0x90u;
	return (count.a > DECK_SIZE) ? 0x10u : 0x00u;
}
/* <<< factory EnergySearch_DeckCheck */

/* >>> factory CheckIfCardIsBasicEnergy */
uint8_t CheckIfCardIsBasicEnergy(uint8_t a)
{
	LoadCardDataToBuffer2_FromDeckIndex(a);
	uint8_t type = gb_read8(wLoadedCard2Type_ADDR);
	if (type < TYPE_ENERGY)
		return 0x10u;
	if (type >= TYPE_ENERGY_DOUBLE_COLORLESS)
		return type == TYPE_ENERGY_DOUBLE_COLORLESS ? 0x90u : 0x10u;
	return 0x00u;
}
/* <<< factory CheckIfCardIsBasicEnergy */

/* >>> factory CreatePlayableStage2PokemonCardListFromHand */
uint8_t CreatePlayableStage2PokemonCardListFromHand(void)
{
	HandListResult hand = CreateHandCardList(0u);
	if (hand.f & 0x10u)
		return 0x90u;
	uint16_t src = wDuelTempList_ADDR;
	uint16_t dst = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(src++);
		if (card == 0xffu)
			break;
		LoadCardDataToBuffer2_FromDeckIndex(card);
		if (gb_read8(wLoadedCard2Type_ADDR) >= TYPE_ENERGY ||
			gb_read8(wLoadedCard2Stage_ADDR) != 2u)
			continue;
		DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		uint8_t eligible = 0u;
		for (uint8_t slot = 0; slot < count.a; slot++) {
			if (!(CheckIfCanEvolveInto_BasicToStage2(card, slot).f & 0x10u)) {
				eligible = 1u;
				break;
			}
		}
		if (eligible)
			gb_write8(dst++, card);
	}
	gb_write8(dst, 0xffu);
	return gb_read8(wDuelTempList_ADDR) == 0xffu ? 0x90u : 0x00u;
}
/* <<< factory CreatePlayableStage2PokemonCardListFromHand */

/* >>> factory Barrier_DiscardEffect */
/* effect_functions.asm:5422-5427 */
uint8_t Barrier_DiscardEffect(void)
{
	uint8_t value = hTemp_ffa0;
	PutCardInDiscardPile(value);
	return value;
}
/* <<< factory Barrier_DiscardEffect */
/* >>> factory DestinyBond_DiscardEffect */
void DestinyBond_DiscardEffect(void) { PutCardInDiscardPile(gb_read8(hTempList_ADDR)); }
/* <<< factory DestinyBond_DiscardEffect */
/* >>> factory Ember_DiscardEffect */
void Ember_DiscardEffect(void) { PutCardInDiscardPile(hTemp_ffa0); }
/* <<< factory Ember_DiscardEffect */
/* >>> factory FireBlast_DiscardEffect */
void FireBlast_DiscardEffect(void) { PutCardInDiscardPile(hTemp_ffa0); }
/* <<< factory FireBlast_DiscardEffect */
/* >>> factory FireSpin_AISelectEffect */
void FireSpin_AISelectEffect(void)
{
	(void)CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);
	gb_write8(hTempList_ADDR, gb_read8(wDuelTempList_ADDR));
	gb_write8((uint16_t)(hTempList_ADDR + 1u), gb_read8((uint16_t)(wDuelTempList_ADDR + 1u)));
}
/* <<< factory FireSpin_AISelectEffect */
/* >>> factory FireSpin_DiscardEffect */
void FireSpin_DiscardEffect(void)
{
	PutCardInDiscardPile(gb_read8(hTempList_ADDR));
	PutCardInDiscardPile(gb_read8((uint16_t)(hTempList_ADDR + 1u)));
}
/* <<< factory FireSpin_DiscardEffect */
/* >>> factory PidgeottoMirrorMove_InitialEffect1 */
/* effect_functions.asm:8047-8049 */
MirrorMoveInitialEffect1Result PidgeottoMirrorMove_InitialEffect1(void)
{
	return MirrorMove_InitialEffect1();
}
/* <<< factory PidgeottoMirrorMove_InitialEffect1 */

/* >>> factory ClefairyMetronome_CheckAttacks */
/* effect_functions.asm:8071-8077 */
ClefairyMetronomeCheckAttacksResult ClefairyMetronome_CheckAttacks(void)
{
	CheckAttackResult r = CheckIfDefendingPokemonHasAnyAttack();
	return (ClefairyMetronomeCheckAttacksResult){r.f, NoAttackMayBeChoosenText};
}
/* <<< factory ClefairyMetronome_CheckAttacks */

/* >>> factory Psychic_DamageBoostEffect */
/* effect_functions.asm:5383-5395 */
void Psychic_DamageBoostEffect(void)
{
	uint16_t damage = (uint16_t)(gb_read8(wDamage_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wDamage_ADDR + 1u)) << 8));
	uint16_t bonus = GetEnergyAttachedMultiplierDamage();
	uint16_t sum = (uint16_t)(damage + bonus);

	gb_write8(wDamage_ADDR, (uint8_t)sum);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), (uint8_t)(sum >> 8));
}
/* <<< factory Psychic_DamageBoostEffect */

/* >>> factory Barrier_AISelectEffect */
/* effect_functions.asm:5414-5424 */
void Barrier_AISelectEffect(void)
{
	CreateListOfEnergyAttachedToArena(TYPE_ENERGY_PSYCHIC);
	uint8_t value = gb_read8(wDuelTempList_ADDR);
	gb_write8(hTemp_ffa0_ADDR, value);
}
/* <<< factory Barrier_AISelectEffect */

/* >>> factory Whirlpool_AISelectEffect */
/* effect_functions.asm:3308-3312. AI side of Whirlpool: picks an Energy card
 * attached to the defending Pokemon and stashes its index in hTemp_ffa0 for
 * Whirlpool_DiscardEffect ($ff = none selected). The picked index is also
 * left in a at ret, mirroring the asm tail. */
uint8_t Whirlpool_AISelectEffect(void)
{
	uint8_t a = AIPickEnergyCardToDiscardFromDefendingPokemon().a;
	hTemp_ffa0 = a;
	return a;
}
/* <<< factory Whirlpool_AISelectEffect */

/* >>> factory Whirlpool_DiscardEffect */
/* effect_functions.asm:3313-3331. Whirlpool's "discard 1 Energy from the Defending
 * Pokemon" follow-up. Bails out early (leaving hl as HandleNoDamageOrEffect left it)
 * if the attack had no effect (carry from HandleNoDamageOrEffect) or no energy card
 * was selected (hTemp_ffa0 == $ff); otherwise SwapTurn makes the defending side the
 * turn side, the selected card is put in that side's discard pile via
 * PutCardInDiscardPile, and the turn is swapped back. The
 * DUELVARS_ARENA_CARD_LAST_TURN_EFFECT := LAST_TURN_EFFECT_DISCARD_ENERGY update is
 * commented out in the original, so it is absent here as well. SwapTurn and
 * PutCardInDiscardPile preserve every register, so hl at ret still holds
 * HandleNoDamageOrEffect's exit value on every path. */
uint16_t Whirlpool_DiscardEffect(uint16_t hl)
{
	HandleNoDamageOrEffectResult noeff = HandleNoDamageOrEffect(hl);
	if (noeff.f & 0x10u)
		return noeff.hl;
	uint8_t whirlpool_card = hTemp_ffa0;
	if (whirlpool_card == 0xFFu)
		return noeff.hl;
	SwapTurn();
	PutCardInDiscardPile(whirlpool_card);
	SwapTurn();
	return noeff.hl;
}
/* <<< factory Whirlpool_DiscardEffect */

/* >>> factory EnergyRemoval_EnergyCheck */
/* effect_functions.asm:9010-9022 */
EnergyRemovalEnergyCheckResult EnergyRemoval_EnergyCheck(void)
{
	SwapTurn();
	CheckIfThereAreAnyEnergyCardsAttachedResult r = CheckIfThereAreAnyEnergyCardsAttached();
	SwapTurn();
	return (EnergyRemovalEnergyCheckResult){r.f, NoEnergyAttachedToOpponentsActiveText};
}
/* <<< factory EnergyRemoval_EnergyCheck */

/* >>> factory EnergyRemoval_AISelection */
/* effect_functions.asm:9025-9028 */
uint8_t EnergyRemoval_AISelection(void)
{
	return AIPickEnergyCardToDiscardFromDefendingPokemon().a;
}
/* <<< factory EnergyRemoval_AISelection */

/* >>> factory EnergyRetrieval_HandEnergyCheck */
/* effect_functions.asm:9046-9063. cp 2 with a hand count below 2 always leaves
 * N|H|C set and Z clear (the count is 0 or 1, so the half-borrow is guaranteed),
 * which is the exact flag byte the caller sees on the early ret c path; the
 * fall-through path inherits the list-builder's exit flags untouched by ldtx. */
EnergyRetrievalHandEnergyCheckResult EnergyRetrieval_HandEnergyCheck(void)
{
	uint8_t n = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (n < 2u)
		return (EnergyRetrievalHandEnergyCheckResult){NotEnoughCardsInHandText, 0x70u};
	uint8_t f = CreateEnergyCardListFromDiscardPile_OnlyBasic().f;
	return (EnergyRetrievalHandEnergyCheckResult){ThereAreNoBasicEnergyCardsInDiscardPileText, f};
}
/* <<< factory EnergyRetrieval_HandEnergyCheck */

/* >>> factory MrMimeMeditate_AIEffect */
/* effect_functions.asm:5003-5008. Applies the Meditate damage boost, then
 * tail-jumps into SetDefiniteAIDamage (a plain call here: the jp only saves
 * a stack frame, which the C ABI handles itself). */
void MrMimeMeditate_AIEffect(void)
{
	MrMimeMeditate_DamageBoostEffect();
	SetDefiniteAIDamage();
}
/* <<< factory MrMimeMeditate_AIEffect */

/* >>> factory PsywaveEffect */
/* effect_functions.asm:5154-5163. Stores the energy-multiplier damage (the de
 * pair returned by GetEnergyAttachedMultiplierDamage) little-endian into
 * wDamage; hl ends advanced one past the low byte, exactly as the asm leaves
 * it. */
uint16_t PsywaveEffect(void)
{
	uint16_t de = GetEnergyAttachedMultiplierDamage();
	uint16_t hl = wDamage_ADDR;
	gb_write8(hl++, (uint8_t)de);
	gb_write8(hl, (uint8_t)(de >> 8));
	return hl;
}
/* <<< factory PsywaveEffect */

/* >>> factory PokemonCenter_DamageCheck */
/* effect_functions.asm:9624-9627 */
PokemonCenterDamageCheckResult PokemonCenter_DamageCheck(void)
{
	CheckIfPlayAreaHasAnyDamageResult r = CheckIfPlayAreaHasAnyDamage();
	return (PokemonCenterDamageCheckResult){r.f, NoPokemonWithDamageCountersText};
}
/* <<< factory PokemonCenter_DamageCheck */

/* >>> factory PokemonBreeder_HandPlayAreaCheck */
/* effect_functions.asm:9735-9743 */
PokemonBreederHandPlayAreaCheckResult PokemonBreeder_HandPlayAreaCheck(uint16_t hl)
{
	uint8_t f = CreatePlayableStage2PokemonCardListFromHand();
	if (f & 0x10u)
		return (PokemonBreederHandPlayAreaCheckResult){
			(uint8_t)((f & 0x80u) | 0x10u),
			ConditionsForEvolvingToStage2NotFulfilledText
		};
	PrehistoricPowerResult r = IsPrehistoricPowerActive(hl);
	return (PokemonBreederHandPlayAreaCheckResult){r.f, r.hl};
}
/* <<< factory PokemonBreeder_HandPlayAreaCheck */

/* >>> factory PokemonTrader_HandDeckCheck */
/* effect_functions.asm:10016-10024 */
PokemonTraderHandDeckCheckResult PokemonTrader_HandDeckCheck(void)
{
	DuelistVarResult var = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	uint16_t message = ThereAreNoCardsInHandThatYouCanChangeText;
	if (var.a < 2u) {
		uint8_t f = 0x40u;
		if (var.a == 0u)
			f |= 0x20u;
		f |= 0x10u;
		return (PokemonTraderHandDeckCheckResult){
			var.a, f, 0u, 0u, 0u, message, 0u
		};
	}
	CreatePokemonCardListFromHandResult list = CreatePokemonCardListFromHand();
	return (PokemonTraderHandDeckCheckResult){
		list.a, list.f, list.c, list.d, list.e, message, 1u
	};
}
/* <<< factory PokemonTrader_HandDeckCheck */

/* >>> factory VictreebelLure_GetBenchPokemonWithLowestHP */
/* effect_functions.asm:1520-1523 */
void VictreebelLure_GetBenchPokemonWithLowestHP(void)
{
	AIFindTargetForBenchAttackResult target = AIFindTargetForBenchAttack();
	hTemp_ffa0 = target.a;
}
/* <<< factory VictreebelLure_GetBenchPokemonWithLowestHP */

/* >>> factory Sprout_CheckDeckAndPlayArea */
/* effect_functions.asm:1674-1682 */
CheckIfDeckIsEmptyResult Sprout_CheckDeckAndPlayArea(void)
{
	CheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();
	if (deck.f & 0x10u)
		return deck;

	DuelistVarResult vars = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t sprout_flags = vars.a >= MAX_PLAY_AREA_POKEMON ? 0x10u : 0x00u;
	if (vars.a == MAX_PLAY_AREA_POKEMON)
		sprout_flags |= 0x80u;
	return (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText, sprout_flags};
}
/* <<< factory Sprout_CheckDeckAndPlayArea */

/* >>> factory NidoranFCallForFamily_CheckDeckAndPlayArea */
/* effect_functions.asm:1939-1947 */
CheckIfDeckIsEmptyResult NidoranFCallForFamily_CheckDeckAndPlayArea(void)
{
	CheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();
	if (deck.f & 0x10u)
		return deck;

	DuelistVarResult vars = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t family_flags = vars.a >= MAX_PLAY_AREA_POKEMON ? 0x10u : 0x00u;
	if (vars.a == MAX_PLAY_AREA_POKEMON)
		family_flags |= 0x80u;
	return (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText, family_flags};
}
/* <<< factory NidoranFCallForFamily_CheckDeckAndPlayArea */

/* >>> factory DragonairHyperBeam_AISelectEffect */
/* effect_functions.asm:7911-7914 */
void DragonairHyperBeam_AISelectEffect(void)
{
	AIPickEnergyCardToDiscardResult r = AIPickEnergyCardToDiscardFromDefendingPokemon();
	hTemp_ffa0 = r.a;
}
/* <<< factory DragonairHyperBeam_AISelectEffect */

/* >>> factory ClefableMetronome_CheckAttacks */
/* effect_functions.asm:7959-7963 */
ClefableMetronomeCheckAttacksResult ClefableMetronome_CheckAttacks(void)
{
	CheckAttackResult r = CheckIfDefendingPokemonHasAnyAttack();
	return (ClefableMetronomeCheckAttacksResult){r.f, NoAttackMayBeChoosenText};
}
/* <<< factory ClefableMetronome_CheckAttacks */

/* >>> factory Scavenge_CheckDiscardPile */
/* effect_functions.asm:5659-5667 */
ScavengeCheckDiscardPileResult Scavenge_CheckDiscardPile(void)
{
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	uint8_t psychic = gb_read8((uint16_t)(wAttachedEnergies_ADDR + PSYCHIC));
	if (psychic < 1u)
		return (ScavengeCheckDiscardPileResult){NotEnoughPsychicEnergyText, 0x70u};
	CreateTrainerCardListFromDiscardPileResult r = CreateTrainerCardListFromDiscardPile();
	return (ScavengeCheckDiscardPileResult){ThereAreNoTrainerCardsInDiscardPileText, r.f};
}
/* <<< factory Scavenge_CheckDiscardPile */

/* >>> factory Scavenge_AISelectEffect */
/* effect_functions.asm:5682-5693 */
void Scavenge_AISelectEffect(void)
{
	(void)CreateListOfEnergyAttachedToArena(TYPE_ENERGY_PSYCHIC);
	hTemp_ffa0 = wDuelTempList;
	(void)CreateTrainerCardListFromDiscardPile();
	hTempPlayAreaLocation_ffa1 = wDuelTempList;
}
/* <<< factory Scavenge_AISelectEffect */

/* >>> factory SlowpokeAmnesia_CheckAttacks */
/* effect_functions.asm:5724-5727 */
SlowpokeAmnesiaCheckAttacksResult SlowpokeAmnesia_CheckAttacks(void)
{
	CheckAttackResult r = CheckIfDefendingPokemonHasAnyAttack();
	return (SlowpokeAmnesiaCheckAttacksResult){r.f, NoAttackMayBeChoosenText};
}
/* <<< factory SlowpokeAmnesia_CheckAttacks */

/* >>> factory DevolutionBeam_CheckPlayArea */
/* effect_functions.asm:5163-5169 */
DevolutionBeamCheckPlayAreaResult DevolutionBeam_CheckPlayArea(void)
{
	CheckAttackResult r = CheckIfTurnDuelistHasEvolvedCards();
	if ((r.f & 0x10u) == 0u)
		return (DevolutionBeamCheckPlayAreaResult){r.f, 0x01u, 0x02u, 0x00efu};

	SwapTurn();
	r = CheckIfTurnDuelistHasEvolvedCards();
	SwapTurn();
	return (DevolutionBeamCheckPlayAreaResult){
		r.f,
		0x01u,
		0x02u,
		ThereAreNoStage1PokemonText
	};
}
/* <<< factory DevolutionBeam_CheckPlayArea */

/* >>> factory DevolutionBeam_AISelectEffect */
/* effect_functions.asm:5218-5230 */
void DevolutionBeam_AISelectEffect(void)
{
	hTemp_ffa0 = 0x01u;
	SwapTurn();
	FindFirstNonBasicCardInPlayAreaResult r = FindFirstNonBasicCardInPlayArea();
	SwapTurn();
	if (!(r.f & 0x10u)) {
		hTemp_ffa0 = 0x00u;
		r = FindFirstNonBasicCardInPlayArea();
	}
	hTempPlayAreaLocation_ffa1 = r.a;
}
/* <<< factory DevolutionBeam_AISelectEffect */

/* >>> factory MewtwoAltEnergyAbsorption_CheckDiscardPile */
/* effect_functions.asm:5432-5435 */
CreateEnergyCardListFromDiscardPileResult MewtwoAltEnergyAbsorption_CheckDiscardPile(void)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile_AllEnergy();
	return (CreateEnergyCardListFromDiscardPileResult){ThereAreNoEnergyCardsInDiscardPileText, r.f};
}
/* <<< factory MewtwoAltEnergyAbsorption_CheckDiscardPile */

/* >>> factory MewtwoAltEnergyAbsorption_AISelectEffect */
/* effect_functions.asm:5442-5459 */
MewtwoAltEnergyAbsorptionAISelectEffectResult MewtwoAltEnergyAbsorption_AISelectEffect(void)
{
	(void)CreateEnergyCardListFromDiscardPile_AllEnergy();
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = hTempList_ADDR;
	uint8_t c = 2u;

	for (;;) {
		uint8_t a = gb_read8(hl++);
		if (a == 0xffu)
			break;
		gb_write8(de++, a);
		c--;
		if (c == 0u)
			break;
	}
	gb_write8(de, (uint8_t)0xffu);
	return (MewtwoAltEnergyAbsorptionAISelectEffectResult){
		0xffu, 0xc0u, 0u, c, de, hl
	};
}
/* <<< factory MewtwoAltEnergyAbsorption_AISelectEffect */

/* >>> factory MewtwoEnergyAbsorption_CheckDiscardPile */
/* effect_functions.asm:5474-5477 */
MewtwoEnergyAbsorptionCheckDiscardPileResult MewtwoEnergyAbsorption_CheckDiscardPile(void)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile_AllEnergy();
	return (MewtwoEnergyAbsorptionCheckDiscardPileResult){
		ThereAreNoEnergyCardsInDiscardPileText, r.f, 0u, 0u, wDuelTempList_ADDR
	};
}
/* <<< factory MewtwoEnergyAbsorption_CheckDiscardPile */

/* >>> factory MewtwoEnergyAbsorption_AISelectEffect */
/* effect_functions.asm:5484-5501 */
MewtwoEnergyAbsorptionAISelectEffectResult MewtwoEnergyAbsorption_AISelectEffect(void)
{
	(void)CreateEnergyCardListFromDiscardPile_AllEnergy();
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = hTempList_ADDR;
	uint8_t c = 2u;

	for (;;) {
		uint8_t a = gb_read8(hl++);
		if (a == 0xffu)
			break;
		gb_write8(de++, a);
		c--;
		if (c == 0u)
			break;
	}
	gb_write8(de, 0xffu);
	return (MewtwoEnergyAbsorptionAISelectEffectResult){
		0xffu, 0xc0u, 0u, c, de, hl
	};
}
/* <<< factory MewtwoEnergyAbsorption_AISelectEffect */

/* >>> factory JynxMeditate_AIEffect */
/* effect_functions.asm:5802-5804 */
void JynxMeditate_AIEffect(void)
{
	JynxMeditate_DamageBoostEffect();
	SetDefiniteAIDamage();
}
/* <<< factory JynxMeditate_AIEffect */

/* >>> factory MysteryAttack_RandomEffect */
/* effect_functions.asm:5820-5858 */
void MysteryAttack_RandomEffect(void)
{
	SetDefiniteDamage(10u);

	uint8_t effect = (uint8_t)(UpdateRNGSources() & 0x07u);
	hTemp_ffa0 = effect;

	switch (effect) {
	case 0u:
		(void)ParalysisEffect();
		break;
	case 1u:
		(void)PoisonEffect();
		break;
	case 2u:
		(void)SleepEffect();
		break;
	case 3u:
		(void)ConfusionEffect();
		break;
	case 4u:
	case 5u:
		break;
	case 6u:
		SetDefiniteDamage(20u);
		break;
	case 7u:
		wLoadedAttackAnimation = ATK_ANIM_GLOW_EFFECT;
		SetDefiniteDamage(0u);
		SetNoEffectFromStatus();
		break;
	}
}
/* <<< factory MysteryAttack_RandomEffect */

/* >>> factory MarowakCallForFamily_CheckDeckAndPlayArea */
/* effect_functions.asm:5995-6003 */
CheckIfDeckIsEmptyResult MarowakCallForFamily_CheckDeckAndPlayArea(void)
{
	CheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();
	if (deck.f & 0x10u)
		return deck;
	DuelistVarResult v = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	/* cp MAX_PLAY_AREA_POKEMON followed by ccf: N and H are cleared by ccf,
	 * Z survives from the compare, carry is the inverted borrow. */
	uint8_t f = (uint8_t)((v.a == MAX_PLAY_AREA_POKEMON ? 0x80u : 0x00u)
		| (v.a >= MAX_PLAY_AREA_POKEMON ? 0x10u : 0x00u));
	CheckIfDeckIsEmptyResult r;
	r.a = v.a;
	r.hl = NoSpaceOnTheBenchText;
	r.f = f;
	return r;
}
/* <<< factory MarowakCallForFamily_CheckDeckAndPlayArea */

/* >>> factory IceBreath_ZeroDamage */
/* effect_functions.asm:3495-3499 */
uint8_t IceBreath_ZeroDamage(void)
{
	uint8_t ice_breath_damage = 0u;
	SetDefiniteDamage(ice_breath_damage);
	return ice_breath_damage;
}
/* <<< factory IceBreath_ZeroDamage */

/* >>> factory AIPickFireEnergyCardToDiscard */
/* effect_functions.asm:3526-3531 */
void AIPickFireEnergyCardToDiscard(void)
{
	CreateListOfFireEnergyAttachedToArena();
	hTemp_ffa0 = gb_read8(wDuelTempList_ADDR);
}
/* <<< factory AIPickFireEnergyCardToDiscard */

/* >>> factory FlamesOfRage_AIEffect */
/* effect_functions.asm:3618-3620 */
void FlamesOfRage_AIEffect(void)
{
	FlamesOfRage_DamageBoostEffect();
	SetDefiniteAIDamage();
}
/* <<< factory FlamesOfRage_AIEffect */

/* >>> factory ArcanineFlamethrower_AISelectEffect */
/* effect_functions.asm:3545-3548 */
void ArcanineFlamethrower_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory ArcanineFlamethrower_AISelectEffect */

/* >>> factory FlamesOfRage_AISelectEffect */
/* effect_functions.asm:3605-3613 */
void FlamesOfRage_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
	gb_write8((uint16_t)(hTempList_ADDR + 1u), gb_read8((uint16_t)(wDuelTempList_ADDR + 1u)));
}
/* <<< factory FlamesOfRage_AISelectEffect */

/* >>> factory FireBlast_AISelectEffect */
/* effect_functions.asm:3703-3706 */
void FireBlast_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory FireBlast_AISelectEffect */

/* >>> factory EnergyConversion_CheckEnergy */
/* effect_functions.asm:4632-4638 */
EnergyConversionCheckEnergyResult EnergyConversion_CheckEnergy(void)
{
	CreateEnergyCardListFromDiscardPileResult r =
		CreateEnergyCardListFromDiscardPile_AllEnergy();
	return (EnergyConversionCheckEnergyResult){ThereAreNoEnergyCardsInDiscardPileText, r.f};
}
/* <<< factory EnergyConversion_CheckEnergy */

/* >>> factory EnergyConversion_AISelectEffect */
/* effect_functions.asm:4642-4666 */
void EnergyConversion_AISelectEffect(void)
{
	uint16_t src = wDuelTempList_ADDR;
	uint16_t dst = hTempList_ADDR;
	uint8_t count = 2u;

	(void)CreateEnergyCardListFromDiscardPile_AllEnergy();
	for (;;) {
		uint8_t value = gb_read8(src);
		src = (uint16_t)(src + 1u);
		if (value == 0xffu) {
			gb_write8(dst, 0xffu);
			return;
		}
		gb_write8(dst, value);
		dst = (uint16_t)(dst + 1u);
		count = (uint8_t)(count - 1u);
		if (count == 0u)
			break;
	}
	gb_write8(dst, 0xffu);
}
/* <<< factory EnergyConversion_AISelectEffect */

/* >>> factory HypnoDarkMind_AISelectEffect */
/* effect_functions.asm:4976-4993 */
void HypnoDarkMind_AISelectEffect(void)
{
	gb_write8(hTemp_ffa0_ADDR, 0xffu);

	DuelistVarResult r =
		GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t count = r.a;
	if (count < 2u)
		return;

	AIFindTargetForBenchAttackResult target = AIFindTargetForBenchAttack();
	gb_write8(hTemp_ffa0_ADDR, target.a);
}
/* <<< factory HypnoDarkMind_AISelectEffect */

/* >>> factory AIPickAttackForAmnesia */
uint8_t AIPickAttackForAmnesia(void)
{
	uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER;
	SwapTurn();
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	HandleEnergyBurn();
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	LoadCardDataToBuffer2_FromDeckIndex(arena);
	if ((uint16_t)wLoadedCard2Atk1Name_ADDR == 0u)
		goto chosen;
	{
		CheckIfEnoughEnergiesForGivenAttackResult check =
			CheckIfEnoughEnergiesForGivenAttack(arena, SECOND_ATTACK);
		if (check.f & 0x10u) {
			attack = SECOND_ATTACK;
			goto chosen;
		}
	}
	if (wLoadedCard2Atk1Category != POKEMON_POWER)
		attack = FIRST_ATTACK_OR_PKMN_POWER;
	else
		attack = SECOND_ATTACK;
chosen:
	SwapTurn();
	return attack;
}
/* <<< factory AIPickAttackForAmnesia */

/* >>> factory MirrorMove_AISelection */
void MirrorMove_AISelection(void)
{
	hTemp_ffa0 = 0xFFu;
	uint8_t effect = GetTurnDuelistVariable(
		DUELVARS_ARENA_CARD_LAST_TURN_EFFECT).a;
	if (effect == 0u)
		return;
	if (effect == LAST_TURN_EFFECT_DISCARD_ENERGY) {
		AIPickEnergyCardToDiscardResult result =
			AIPickEnergyCardToDiscardFromDefendingPokemon();
		hTemp_ffa0 = result.a;
		return;
	}
	if (effect == LAST_TURN_EFFECT_AMNESIA) {
		hTemp_ffa0 = AIPickAttackForAmnesia();
	}
}
/* <<< factory MirrorMove_AISelection */

/* >>> factory KinglerFlail_HPCheck */
void KinglerFlail_HPCheck(void)
{
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	SetDefiniteDamage(r.a);
}
/* <<< factory KinglerFlail_HPCheck */

/* >>> factory MagikarpFlail_HPCheck */
void MagikarpFlail_HPCheck(void)
{
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	SetDefiniteDamage(r.a);
}
/* <<< factory MagikarpFlail_HPCheck */

/* >>> factory SuperFang_HalfHPEffect */
void SuperFang_HalfHPEffect(void)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t damage = (uint8_t)(r.a >> 1);
	if ((damage & 1u) != 0u)
		damage = (uint8_t)(damage + 5u);
	SetDefiniteDamage(damage);
}
/* <<< factory SuperFang_HalfHPEffect */

/* >>> factory KarateChop_DamageSubtractionEffect */
void KarateChop_DamageSubtractionEffect(void)
{
	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	uint16_t damage_value = (uint16_t)(gb_read8(wDamage_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wDamage_ADDR + 1u)) << 8));
	uint16_t remaining = (uint16_t)(damage_value - (uint16_t)damage.a);
	gb_write8(wDamage_ADDR, (uint8_t)remaining);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), (uint8_t)(remaining >> 8));
	if (damage_value < damage.a)
		SetDefiniteDamage(0u);
}
/* <<< factory KarateChop_DamageSubtractionEffect */

/* >>> factory SpearowMirrorMove_AISelection */
void SpearowMirrorMove_AISelection(void)
{
	MirrorMove_AISelection();
}
/* <<< factory SpearowMirrorMove_AISelection */

/* >>> factory CharmeleonFlamethrower_AISelectEffect */
void CharmeleonFlamethrower_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory CharmeleonFlamethrower_AISelectEffect */

/* >>> factory ClefableMetronome_AISelectEffect */
void ClefableMetronome_AISelectEffect(void)
{
	HandleAIMetronomeEffect();
}
/* <<< factory ClefableMetronome_AISelectEffect */

/* >>> factory Ember_AISelectEffect */
void Ember_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory Ember_AISelectEffect */

/* >>> factory FlareonFlamethrower_AISelectEffect */
void FlareonFlamethrower_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory FlareonFlamethrower_AISelectEffect */

/* >>> factory DestinyBond_DestinyBondEffect */
uint16_t DestinyBond_DestinyBondEffect(void)
{
	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_DESTINY_BOND);
}
/* <<< factory DestinyBond_DestinyBondEffect */

/* >>> factory FlareonRage_AIEffect */
void FlareonRage_AIEffect(void)
{
	FlareonRage_DamageBoostEffect();
	SetDefiniteAIDamage();
}
/* <<< factory FlareonRage_AIEffect */

/* >>> factory GolduckHyperBeam_AISelectEffect */
void GolduckHyperBeam_AISelectEffect(void)
{
	AIPickEnergyCardToDiscardResult result = AIPickEnergyCardToDiscardFromDefendingPokemon();
	gb_write8(hTemp_ffa0_ADDR, result.a);
}
/* <<< factory GolduckHyperBeam_AISelectEffect */

/* >>> factory OnixHardenEffect */
uint16_t OnixHardenEffect(void)
{
	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_PREVENT_LESS_THAN_40);
}
/* <<< factory OnixHardenEffect */

/* >>> factory PoliwhirlAmnesia_AISelectEffect */
void PoliwhirlAmnesia_AISelectEffect(void)
{
	uint8_t result = AIPickAttackForAmnesia();
	hTemp_ffa0 = result;
}
/* <<< factory PoliwhirlAmnesia_AISelectEffect */

/* >>> factory StretchKick_AISelectEffect */
void StretchKick_AISelectEffect(void)
{
	AIFindTargetForBenchAttackResult result = AIFindTargetForBenchAttack();
	hTemp_ffa0 = result.a;
}
/* <<< factory StretchKick_AISelectEffect */

/* >>> factory VaporeonWaterGunEffect */
void VaporeonWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(2u, 1u);
}
/* <<< factory VaporeonWaterGunEffect */

/* >>> factory Potion_DamageCheck */
PotionDamageCheckResult Potion_DamageCheck(void)
{
	CheckIfPlayAreaHasAnyDamageResult r = CheckIfPlayAreaHasAnyDamage();
	return (PotionDamageCheckResult){r.f, NoPokemonWithDamageCountersText};
}
/* <<< factory Potion_DamageCheck */

/* >>> factory CloysterSpikeCannon_AIEffect */
void CloysterSpikeCannon_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory CloysterSpikeCannon_AIEffect */

/* >>> factory JolteonDoubleKick_AIEffect */
void JolteonDoubleKick_AIEffect(void)
{
	SetExpectedAIDamage(20u, 0u, 40u);
}
/* <<< factory JolteonDoubleKick_AIEffect */

/* >>> factory RapidashStomp_AIEffect */
void RapidashStomp_AIEffect(void)
{
	SetExpectedAIDamage(25u, 20u, 30u);
}
/* <<< factory RapidashStomp_AIEffect */

/* >>> factory StoneBarrage_AIEffect */
void StoneBarrage_AIEffect(void)
{
	SetExpectedAIDamage(10u, 0u, 100u);
}
/* <<< factory StoneBarrage_AIEffect */

/* >>> factory DestinyBond_AISelectEffect */
void DestinyBond_AISelectEffect(void)
{
	CreateListOfEnergyAttachedToArenaResult result = CreateListOfEnergyAttachedToArena(0x0Du);
	(void)result;
	hTempList = wDuelTempList;
}
/* <<< factory DestinyBond_AISelectEffect */

/* >>> factory Rampage_AIEffect */
void Rampage_AIEffect(void)
{
	CardDamageResult r = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	AddToDamage(r.a);
	SetDefiniteAIDamage();
}
/* <<< factory Rampage_AIEffect */

/* >>> factory SuperPotion_DamageEnergyCheck */
SuperPotionDamageEnergyCheckResult SuperPotion_DamageEnergyCheck(void)
{
	CheckIfPlayAreaHasAnyDamageResult damage = CheckIfPlayAreaHasAnyDamage();
	if ((damage.f & 0x10u) != 0u)
		return (SuperPotionDamageEnergyCheckResult){damage.f, NoPokemonWithDamageCountersText};
	CheckIfThereAreAnyEnergyCardsAttachedResult energy = CheckIfThereAreAnyEnergyCardsAttached();
	return (SuperPotionDamageEnergyCheckResult){energy.f, ThereIsNoEnergyCardAttachedText};
}
/* <<< factory SuperPotion_DamageEnergyCheck */

/* >>> factory KrabbyCallForFamily_CheckDeckAndPlayArea */
CheckIfDeckIsEmptyResult KrabbyCallForFamily_CheckDeckAndPlayArea(void)
{
	CheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();
	if (deck.f & 0x10u)
		return deck;
	DuelistVarResult vars = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t f = (vars.a == MAX_PLAY_AREA_POKEMON ? 0x80u : 0x00u)
		| (vars.a >= MAX_PLAY_AREA_POKEMON ? 0x10u : 0x00u);
	return (CheckIfDeckIsEmptyResult){vars.a, NoSpaceOnTheBenchText, f};
}
/* <<< factory KrabbyCallForFamily_CheckDeckAndPlayArea */

/* >>> factory Revive_BenchCheck */
ReviveBenchCheckResult Revive_BenchCheck(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (count.a >= MAX_PLAY_AREA_POKEMON) {
		uint8_t f = (uint8_t)((count.a == MAX_PLAY_AREA_POKEMON ? 0x80u : 0u) | 0x10u);
		return (ReviveBenchCheckResult){f, NoSpaceOnTheBenchText};
	}
	CreateBasicPokemonCardListFromDiscardPileResult list = CreateBasicPokemonCardListFromDiscardPile();
	return (ReviveBenchCheckResult){list.f, ThereAreNoPokemonInDiscardPileText};
}
/* <<< factory Revive_BenchCheck */

/* >>> factory DragonairHyperBeam_DiscardEffect */
uint16_t DragonairHyperBeam_DiscardEffect(uint16_t hl)
{
	HandleNoDamageOrEffectResult no_effect = HandleNoDamageOrEffect(hl);
	if (no_effect.f & 0x10u)
		return no_effect.hl;
	uint8_t card = hTemp_ffa0;
	if (card == 0xffu)
		return no_effect.hl;
	SwapTurn();
	PutCardInDiscardPile(card);
	DuelistVarResult result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_LAST_TURN_EFFECT);
	gb_write8(result.hl, LAST_TURN_EFFECT_DISCARD_ENERGY);
	SwapTurn();
	return result.hl;
}
/* <<< factory DragonairHyperBeam_DiscardEffect */

/* >>> factory MirrorMove_ExecuteStatusEffect */
MirrorMoveExecuteStatusEffectResult MirrorMove_ExecuteStatusEffect(uint8_t a)
{
	uint8_t c = a;
	if ((a & PSN_DBLPSN) != 0u) {
		if (a == DOUBLE_POISONED)
			(void)DoublePoisonEffect();
		if (a == POISONED)
			(void)PoisonEffect();
	}
	if ((c & CNF_SLP_PRZ) == 0u)
		return (MirrorMoveExecuteStatusEffectResult){0xa0u};
	if (c == CONFUSED) {
		QueueStatusConditionResult r = ConfusionEffect();
		return (MirrorMoveExecuteStatusEffectResult){r.f};
	}
	if (c == ASLEEP) {
		QueueStatusConditionResult r = SleepEffect();
		return (MirrorMoveExecuteStatusEffectResult){r.f};
	}
	if (c == PARALYZED) {
		QueueStatusConditionResult r = ParalysisEffect();
		return (MirrorMoveExecuteStatusEffectResult){r.f};
	}
	return (MirrorMoveExecuteStatusEffectResult){0x00u};
}
/* <<< factory MirrorMove_ExecuteStatusEffect */

/* >>> factory Curse_CheckDamageAndBench */
CurseCheckDamageAndBenchResult Curse_CheckDamageAndBench(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	DuelistVarResult flags = GetTurnDuelistVariable(
		(uint8_t)(location + DUELVARS_ARENA_CARD_FLAGS));
	if ((flags.a & USED_PKMN_POWER_THIS_TURN) != 0u)
		return (CurseCheckDamageAndBenchResult){0x10u, OnlyOncePerTurnText};

	SwapTurn();
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	SwapTurn();
	if (count.a < 2u)
		return (CurseCheckDamageAndBenchResult){0x10u, CannotUseSinceTheresOnly1PkmnText};

	SwapTurn();
	CheckIfPlayAreaHasAnyDamageResult damage = CheckIfPlayAreaHasAnyDamage();
	SwapTurn();
	if ((damage.f & 0x10u) != 0u)
		return (CurseCheckDamageAndBenchResult){0x10u, NoPokemonWithDamageCountersText};

	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	return (CurseCheckDamageAndBenchResult){incapable.f, incapable.hl};
}
/* <<< factory Curse_CheckDamageAndBench */

/* >>> factory SpearowMirrorMove_AIEffect */
void SpearowMirrorMove_AIEffect(void)
{
	MirrorMove_AIEffect();
}
/* <<< factory SpearowMirrorMove_AIEffect */

/* >>> factory SpearowMirrorMove_InitialEffect1 */
MirrorMoveInitialEffect1Result SpearowMirrorMove_InitialEffect1(void)
{
	return MirrorMove_InitialEffect1();
}
/* <<< factory SpearowMirrorMove_InitialEffect1 */

/* >>> factory PidgeottoMirrorMove_AIEffect */
void PidgeottoMirrorMove_AIEffect(void)
{
	MirrorMove_AIEffect();
}
/* <<< factory PidgeottoMirrorMove_AIEffect */

/* >>> factory PidgeottoMirrorMove_AISelection */
void PidgeottoMirrorMove_AISelection(void)
{
	MirrorMove_AISelection();
}
/* <<< factory PidgeottoMirrorMove_AISelection */

/* >>> factory ClefairyMetronome_AISelectEffect */
void ClefairyMetronome_AISelectEffect(void)
{
	HandleAIMetronomeEffect();
}
/* <<< factory ClefairyMetronome_AISelectEffect */

/* >>> factory EnergySpike_DeckCheck */
CheckIfDeckIsEmptyResult EnergySpike_DeckCheck(void)
{
	return CheckIfDeckIsEmpty();
}
/* <<< factory EnergySpike_DeckCheck */

/* >>> factory MagmarFlamethrower_AISelectEffect */
void MagmarFlamethrower_AISelectEffect(void)
{
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory MagmarFlamethrower_AISelectEffect */

/* >>> factory OmastarWaterGunEffect */
void OmastarWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(1u, 1u);
}
/* <<< factory OmastarWaterGunEffect */

/* >>> factory CuboneRage_AIEffect */
void CuboneRage_AIEffect(void)
{
	CuboneRage_DamageBoostEffect();
	SetDefiniteAIDamage();
}
/* <<< factory CuboneRage_AIEffect */

/* >>> factory GravelerHardenEffect */
uint16_t GravelerHardenEffect(void)
{
	return ApplySubstatus1ToAttackingCard(SUBSTATUS1_PREVENT_LESS_THAN_40);
}
/* <<< factory GravelerHardenEffect */

/* >>> factory KarateChop_AIEffect */
void KarateChop_AIEffect(void)
{
	KarateChop_DamageSubtractionEffect();
	SetDefiniteAIDamage();
}
/* <<< factory KarateChop_AIEffect */

/* >>> factory LaprasWaterGunEffect */
void LaprasWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(1u, 0u);
}
/* <<< factory LaprasWaterGunEffect */

/* >>> factory OmanyteWaterGunEffect */
void OmanyteWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(1u, 0u);
}
/* <<< factory OmanyteWaterGunEffect */

/* >>> factory PoliwrathWaterGunEffect */
void PoliwrathWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(2u, 1u);
}
/* <<< factory PoliwrathWaterGunEffect */

/* >>> factory SeadraWaterGunEffect */
void SeadraWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(1u, 1u);
}
/* <<< factory SeadraWaterGunEffect */

/* >>> factory SuperFang_AIEffect */
void SuperFang_AIEffect(void)
{
	SuperFang_HalfHPEffect();
	SetDefiniteAIDamage();
}
/* <<< factory SuperFang_AIEffect */

/* >>> factory DragoniteLv41Slam_AIEffect */
void DragoniteLv41Slam_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory DragoniteLv41Slam_AIEffect */

/* >>> factory ElectabuzzQuickAttack_AIEffect */
void ElectabuzzQuickAttack_AIEffect(void)
{
	SetExpectedAIDamage(20u, 10u, 30u);
}
/* <<< factory ElectabuzzQuickAttack_AIEffect */

/* >>> factory JolteonQuickAttack_AIEffect */
void JolteonQuickAttack_AIEffect(void)
{
	SetExpectedAIDamage(20u, 10u, 30u);
}
/* <<< factory JolteonQuickAttack_AIEffect */

/* >>> factory LeekSlap_AIEffect */
void LeekSlap_AIEffect(void)
{
	SetExpectedAIDamage(15u, 0u, 30u);
}
/* <<< factory LeekSlap_AIEffect */

/* >>> factory PinMissile_AIEffect */
void PinMissile_AIEffect(void)
{
	SetExpectedAIDamage(40u, 0u, 80u);
}
/* <<< factory PinMissile_AIEffect */

/* >>> factory SandslashFurySwipes_AIEffect */
void SandslashFurySwipes_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory SandslashFurySwipes_AIEffect */

/* >>> factory Thunderpunch_AIEffect */
void Thunderpunch_AIEffect(void)
{
	SetExpectedAIDamage(35u, 30u, 40u);
}
/* <<< factory Thunderpunch_AIEffect */

/* >>> factory StarmieRecover_AISelectEffect */
StarmieRecoverAISelectEffectResult StarmieRecover_AISelectEffect(void)
{
	CreateListOfEnergyAttachedToArenaResult result = CreateListOfEnergyAttachedToArena(TYPE_ENERGY_WATER);
	uint8_t a = wDuelTempList;
	hTemp_ffa0 = a;
	return (StarmieRecoverAISelectEffectResult){a, result.f};
}
/* <<< factory StarmieRecover_AISelectEffect */

/* >>> factory BellsproutCallForFamily_CheckDeckAndPlayArea */
BellsproutCallForFamilyCheckDeckAndPlayAreaResult BellsproutCallForFamily_CheckDeckAndPlayArea(void)
{
	CheckIfDeckIsEmptyResult deck = CheckIfDeckIsEmpty();
	if (deck.f & 0x10u)
		return (BellsproutCallForFamilyCheckDeckAndPlayAreaResult){deck.a, deck.hl, deck.f};
	DuelistVarResult var = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint16_t hl = NoSpaceOnTheBenchText;
	uint8_t z = (var.a == MAX_PLAY_AREA_POKEMON) ? 0x80u : 0u;
	uint8_t c = (var.a >= MAX_PLAY_AREA_POKEMON) ? 0x10u : 0u;
	uint8_t f = (uint8_t)(z | c);
	return (BellsproutCallForFamilyCheckDeckAndPlayAreaResult){var.a, hl, f};
}
/* <<< factory BellsproutCallForFamily_CheckDeckAndPlayArea */

/* >>> factory Spark_AISelectEffect */
SparkAISelectEffectResult Spark_AISelectEffect(void)
{
	hTemp_ffa0 = 0xFFu;
	DuelistVarResult var = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (var.a < 2u)
		return (SparkAISelectEffectResult){var.a};
	AIFindTargetForBenchAttackResult target = AIFindTargetForBenchAttack();
	hTemp_ffa0 = target.a;
	return (SparkAISelectEffectResult){target.a};
}
/* <<< factory Spark_AISelectEffect */

/* >>> factory DamageSwap_CheckDamage */
DamageSwapCheckDamageResult DamageSwap_CheckDamage(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	CheckIfPlayAreaHasAnyDamageResult has_damage = CheckIfPlayAreaHasAnyDamage();
	if (has_damage.f & 0x10u) {
		uint8_t f = (uint8_t)((has_damage.f & 0x80u) | 0x10u);
		return (DamageSwapCheckDamageResult){f, NoPokemonWithDamageCountersText};
	}
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(hTempPlayAreaLocation_ff9d);
	return (DamageSwapCheckDamageResult){incapable.f, incapable.hl};
}
/* <<< factory DamageSwap_CheckDamage */

/* >>> factory PokemonFlute_BenchCheck */
PokemonFluteBenchCheckResult PokemonFlute_BenchCheck(void)
{
	DuelistVarResult count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (count.a >= MAX_PLAY_AREA_POKEMON) {
		uint8_t f = (uint8_t)(((count.a == MAX_PLAY_AREA_POKEMON) ? 0x80u : 0u) | 0x10u);
		return (PokemonFluteBenchCheckResult){f, NoSpaceOnTheBenchText};
	}
	SwapTurn();
	CreateBasicPokemonCardListFromDiscardPileResult basics = CreateBasicPokemonCardListFromDiscardPile();
	SwapTurn();
	return (PokemonFluteBenchCheckResult){basics.f, ThereAreNoPokemonInDiscardPileText};
}
/* <<< factory PokemonFlute_BenchCheck */

/* >>> factory Heal_OncePerTurnCheck */
HealOncePerTurnCheckResult Heal_OncePerTurnCheck(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTemp_ffa0 = location;
	DuelistVarResult flags = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_FLAGS));
	if (flags.a & USED_PKMN_POWER_THIS_TURN)
		return (HealOncePerTurnCheckResult){0x10u, OnlyOncePerTurnText};
	CheckIfPlayAreaHasAnyDamageResult has_damage = CheckIfPlayAreaHasAnyDamage();
	if (has_damage.f & 0x10u)
		return (HealOncePerTurnCheckResult){has_damage.f, NoPokemonWithDamageCountersText};
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(hTempPlayAreaLocation_ff9d);
	return (HealOncePerTurnCheckResult){incapable.f, incapable.hl};
}
/* <<< factory Heal_OncePerTurnCheck */

/* >>> factory Shift_ChangeColorEffect */
Shift_ChangeColorEffectResult Shift_ChangeColorEffect(uint8_t d, uint8_t e)
{
	uint8_t location = hTemp_ffa0;
	DuelistVarResult arena_card = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena_card.a);

	DuelistVarResult flags = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_FLAGS));
	gb_write8(flags.hl, (uint8_t)(gb_read8(flags.hl) | (1u << USED_PKMN_POWER_THIS_TURN_F)));

	DuelistVarResult changed_type = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_CHANGED_TYPE));
	uint8_t new_type = (uint8_t)(hAIPkmnPowerEffectParam | HAS_CHANGED_COLOR);
	gb_write8(changed_type.hl, new_type);

	LoadCardNameAndInputColor(new_type, d, e);
	WaitResult result = DrawWideTextBox_WaitForInput(ChangedTheColorOfText);
	return (Shift_ChangeColorEffectResult){result.f};
}
/* <<< factory Shift_ChangeColorEffect */

/* >>> factory MagikarpFlail_AIEffect */
void MagikarpFlail_AIEffect(void)
{
	MagikarpFlail_HPCheck();
	SetDefiniteAIDamage();
}
/* <<< factory MagikarpFlail_AIEffect */

/* >>> factory PoliwagWaterGunEffect */
void PoliwagWaterGunEffect(void)
{
	ApplyExtraWaterEnergyDamageBonus(1u, 0u);
}
/* <<< factory PoliwagWaterGunEffect */

/* >>> factory TaurosStomp_AIEffect */
void TaurosStomp_AIEffect(void)
{
	SetExpectedAIDamage(25u, 20u, 30u);
}
/* <<< factory TaurosStomp_AIEffect */

/* >>> factory DodrioRage_AIEffect */
void DodrioRage_AIEffect(void)
{
	DodrioRage_DamageBoostEffect();
	SetDefiniteAIDamage();
}
/* <<< factory DodrioRage_AIEffect */

/* >>> factory DragoniteLv45Slam_AIEffect */
void DragoniteLv45Slam_AIEffect(void)
{
	SetExpectedAIDamage(40u, 0u, 80u);
}
/* <<< factory DragoniteLv45Slam_AIEffect */

/* >>> factory GengarDarkMind_AISelectEffect */
void GengarDarkMind_AISelectEffect(void)
{
	hTemp_ffa0 = 0xFFu;
	DuelistVarResult r = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (r.a < 2u)
		return;
	AIFindTargetForBenchAttackResult t = AIFindTargetForBenchAttack();
	hTemp_ffa0 = t.a;
}
/* <<< factory GengarDarkMind_AISelectEffect */

/* >>> factory PoliwhirlDoubleslap_AIEffect */
void PoliwhirlDoubleslap_AIEffect(void)
{
	SetExpectedAIDamage(30u, 0u, 60u);
}
/* <<< factory PoliwhirlDoubleslap_AIEffect */
