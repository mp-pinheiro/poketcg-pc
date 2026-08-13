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
#define DUELVARS_ARENA_CARD_STATUS        0xf0u
#define DUELVARS_ARENA_CARD_SUBSTATUS1    0xcbu

#define DUELVARS_DUELIST_TYPE          0xf1u
#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xe7u
#define DUELIST_TYPE_PLAYER            0x00u

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

#define SUBSTATUS1_REDUCE_BY_10 0x1eu

#include "home/duel.h"
#include "home/card_data.h"
#define CARD_LOCATION_PLAY_AREA_F 4u

#define ThereAreNoCardsInTheDiscardPileText 0x00bbu

#define DUELVARS_HAND 0x42u
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xeeu

#define ThereAreNoStage1PokemonText 0x00BCu
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
void ApplyExtraWaterEnergyDamageBonus(void)
{
	uint8_t c = 0u;
	uint8_t b = 0u;
	if (wMetronomeEnergyCost) { c = wMetronomeEnergyCost; }
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
	return (uint8_t)((f & 0x80u) | (uint8_t)0x10u);
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
