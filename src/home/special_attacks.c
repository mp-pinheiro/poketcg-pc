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

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/energy.h"
#include "home/retreat.h"
#include "home/damage_calculation.h"
#include "home/card_color.h"
#include "home/card_data.h"
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
#define CARD_LOCATION_DECK 0x00u
#define MAX_BENCH_POKEMON 0x05u
#define MAX_PLAY_AREA_POKEMON 0x06u
#define NIDORANF 0x14u
#define NIDORANM 0x17u
#define ODDISH 0x1Cu
#define BELLSPROUT 0x23u
#define EXEGGUTOR 0x29u
#define SCYTHER 0x2Eu
#define KRABBY 0x4Fu
#define VAPOREON_LV29 0x5Au
#define ELECTRODE_LV42 0x6Fu
#define DUGTRIO 0x7Au
#define GEODUDE 0x80u
#define ONIX 0x83u
#define CUBONE 0x84u
#define MAROWAK_LV26 0x85u
#define RHYHORN 0x89u
#define MEW_LV23 0xA2u
#define JIGGLYPUFF_LV13 0xAEu
#define KANGASKHAN 0xB9u
#define DRAGONAIR 0xC0u
#define NINETALES_LV35 0x35u
#define MEWTWO_ALT_LV60 0x9Fu
#define MEWTWO_LV60 0x9Eu
#define ZAPDOS_LV68 0x76u
#define ELECTRODE_LV35 0x6Eu
#define GOLDUCK 0x45u
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

/* >>> factory HandleSpecialAIAttacks */
HandleSpecialAIAttacksResult HandleSpecialAIAttacks(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	DuelistVarResult arena = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	uint8_t card = (uint8_t)GetCardIDFromDeckIndex(arena.a);
	uint8_t score = 0u;
	uint8_t flags = 0x80u;
	if (card == EXEGGUTOR) {
		AIDecideWhetherToRetreatResult r = AIDecideWhetherToRetreat();
		if (r.f & 0x10u) { score = 0x8Au; flags = 0u; }
	} else if (card == SCYTHER || card == VAPOREON_LV29) {
		if (wAICannotDamage != 0u) { score = 0x85u; flags = 0u; }
		else {
			wSelectedAttack = SECOND_ATTACK;
			CheckIfSelectedAttackIsUnusableResult r = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
			if (r.f & 0x10u || wDamage == 0u) { score = 0x85u; flags = 0u; }
		}
	} else if (card == MEW_LV23) {
		if (LookForCardThatIsKnockedOutOnDevolution(0u).f & 0x10u) { score = 0x85u; flags = 0u; }
	} else if (card == NIDORANF || card == ODDISH || card == BELLSPROUT || card == KRABBY || card == MAROWAK_LV26) {
		LookForCardIDInLocationResult r = LookForCardIDInLocation_Bank5(CARD_LOCATION_DECK, card == NIDORANF ? NIDORANM : GEODUDE);
		if (r.f & 0x10u) {
			DuelistVarResult n = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
			uint8_t limit = card == NIDORANF ? MAX_PLAY_AREA_POKEMON : MAX_BENCH_POKEMON;
			if (n.a < limit) { score = (uint8_t)(0x80u + limit - n.a); flags = 0u; }
		}
	} else if (card == JIGGLYPUFF_LV13) {
		if (CheckIfAnyBasicPokemonInDeck().f & 0x10u) { score = 0x85u; flags = 0u; }
	} else if (card == ZAPDOS_LV68 || card == KANGASKHAN || card == DUGTRIO || card == ELECTRODE_LV35 || card == GOLDUCK || card == DRAGONAIR) {
		score = (card == KANGASKHAN || card == DUGTRIO) ? 0x80u : 0x83u;
		flags = 0u;
	}
	return (HandleSpecialAIAttacksResult){score, flags};
}
/* <<< factory HandleSpecialAIAttacks */
