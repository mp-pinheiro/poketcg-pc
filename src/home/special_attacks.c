#include "home/special_attacks.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/damage_calculation.h"
#define ATTACK_FLAG2_ADDRESS 0x08u
#define DUELVARS_ARENA_CARD 0xBBu
#define DUELVARS_ARENA_CARD_HP 0xC8u
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define HEAL_USER_F 0x01u
#define NULLIFY_OR_WEAKEN_ATTACK_F 0x02u
#define PLAY_AREA_ARENA 0x00u
#define SECOND_ATTACK 0x01u
/* <<< factory statics */

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

/* >>> factory CheckWhetherToSwitchToFirstAttack */
void CheckWhetherToSwitchToFirstAttack(void)
{
	uint8_t first_score = wFirstAttackAIScore;
	if (first_score < 0x50u) {
		wSelectedAttack = SECOND_ATTACK;
		return;
	}
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	(void)EstimateDamage_VersusDefendingCard(FIRST_ATTACK_OR_PKMN_POWER);
	DuelistVarResult hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t remaining = (uint8_t)(hp.a - wDamage);
	if (remaining != 0u && hp.a >= wDamage) {
		wSelectedAttack = SECOND_ATTACK;
		return;
	}
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	(void)CopyAttackDataAndDamage_FromDeckIndex(arena.a, SECOND_ATTACK);
	AttackFlagResult heal = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS | HEAL_USER_F));
	if ((heal.f & 0x10u) != 0u) {
		wSelectedAttack = SECOND_ATTACK;
		return;
	}
	AttackFlagResult weaken = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS | NULLIFY_OR_WEAKEN_ATTACK_F));
	if ((weaken.f & 0x10u) != 0u) {
		wSelectedAttack = SECOND_ATTACK;
		return;
	}
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
}
/* <<< factory CheckWhetherToSwitchToFirstAttack */
