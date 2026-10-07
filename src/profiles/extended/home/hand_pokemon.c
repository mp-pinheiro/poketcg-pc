#include "home/hand_pokemon.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/common.h"
#include "home/substatus.h"
#include "home/duel.h"
#include "home/card_id_bus.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
#define INVINCIBLE_RONALD_DECK_ID 0x1Au
#define LEGENDARY_DRAGONITE_DECK_ID 0x0Fu
#define LEGENDARY_RONALD_DECK_ID 0x1Bu

#include "home/retreat.h"

#define LEGENDARY_ARTICUNO_DECK_ID 0x0Eu
#define LEGENDARY_ZAPDOS_DECK_ID 0x0Du
#define DUELVARS_ARENA_CARD 0xBBu
#define DUELVARS_ARENA_CARD_HP 0xC8u
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/core.h"
#include "home/duel.h"
#define PIKACHU_DECK_ID 0x25u
/* <<< factory statics */

/* >>> factory AIDecideSpecialEvolutions */
void AIDecideSpecialEvolutions(void)
{
	uint8_t deck = wOpponentDeckID;
	if (deck == LEGENDARY_DRAGONITE_DECK_ID) {
		CardId card = card_id_read_at(wLoadedCard2ID_ADDR);
		if (card == CHARMELEON) {
			uint8_t location = hTempPlayAreaLocation_ff9d;
			CountNumberOfEnergyCardsAttachedResult attached =
				CountNumberOfEnergyCardsAttached(location);
			if (attached.a < 3u) {
				AIDiscourage(10u);
				return;
			}
			CountOppEnergyResult hand = CountOppEnergyCardsInHand(0u, 0u);
			if ((uint8_t)(attached.a + hand.a) < 6u)
				AIDiscourage(10u);
			else
				(void)AIEncourage(3u);
			return;
		}
		if (card == MAGIKARP) {
			uint8_t location = hTempPlayAreaLocation_ff9d;
			if (location == 0u)
				return;
			CountNumberOfEnergyCardsAttachedResult attached =
				CountNumberOfEnergyCardsAttached(location);
			if (attached.a >= 2u)
				(void)AIEncourage(3u);
			return;
		}
		if (card != DRAGONAIR)
			return;
	} else if (deck == INVINCIBLE_RONALD_DECK_ID) {
		if (card_id_read_at(wLoadedCard2ID_ADDR) != GRIMER)
			return;
		if (hTempPlayAreaLocation_ff9d == 0u)
			return;
		(void)AIEncourage(10u);
		return;
	} else if (deck != LEGENDARY_RONALD_DECK_ID
		|| card_id_read_at(wLoadedCard2ID_ADDR) != DRAGONAIR) {
		return;
	}

	uint8_t location = hTempPlayAreaLocation_ff9d;
	if (location != 0u) {
		uint8_t count = GetTurnDuelistVariable(
			DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t total = 0u;
		while (count != 0u) {
			--count;
			CardDamageResult damage = GetCardDamageAndMaxHP(count);
			total = (uint8_t)(total + damage.a);
		}
		if (total <= 70u) {
			AIDiscourage(10u);
			return;
		}
		PkmnPowerCountResult muk =
			CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if ((muk.f & 0x10u) != 0u) {
			AIDiscourage(10u);
			return;
		}
		(void)AIEncourage(10u);
		return;
	}

	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	if (damage.a < 50u) {
		AIDiscourage(10u);
		return;
	}
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	if (wTotalAttachedEnergies < 3u) {
		AIDiscourage(10u);
		return;
	}
	PkmnPowerCountResult muk =
		CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if ((muk.f & 0x10u) != 0u)
		AIDiscourage(10u);
	else
		(void)AIEncourage(10u);
}
/* <<< factory AIDecideSpecialEvolutions */

/* >>> factory AIDecideEvolution */
/* hand_pokemon.asm:104-391. For every evolution card in hand and every play
 * area card it can evolve, score the evolution against 128 and play it at 133. */
uint8_t AIDecideEvolution(void)
{
	(void)CreateHandCardList(0u);
	{
		uint16_t src = wDuelTempList_ADDR;
		uint16_t dst = wHandTempList_ADDR;
		(void)CopyListWithFFTerminatorFromHLToDE_Bank5(&src, &dst);
	}
	uint16_t hand = wHandTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hand++);
		if (card == 0xFFu)
			break;
		wTempAIPokemonCard = card;
		if (IsPrehistoricPowerActive(hand).f & 0x10u)
			continue;
		(void)LoadCardDataToBuffer1_FromDeckIndex(card);
		if (wLoadedCard1Type >= TYPE_ENERGY || wLoadedCard1Stage == 0u)
			continue;
		uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		for (uint8_t loc = 0u; count != 0u; ++loc, --count) {
			if (CheckIfCanEvolveInto(card, loc).f & 0x10u)
				continue;
			wTempAI = loc;
			hTempPlayAreaLocation_ff9d = loc;
			wEvolutionHPDifference = (uint8_t)(wLoadedCard1HP - wLoadedCard2HP);
			wAIScore = 0x80u;
			AIDecideSpecialEvolutions();
			wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
			uint8_t can_attack = (CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u;
			if (!can_attack) {
				wSelectedAttack = SECOND_ATTACK;
				can_attack = (CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u;
			}
			if (can_attack) {
				wCurCardCanAttack = 1u;
				if ((CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) != 0u
				    && (CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u)
					wCurCardCanKO = 1u;
			} else {
				wCurCardCanAttack = 0u;
				wCurCardCanKO = 0u;
			}
			DuelistVarResult slot = GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD));
			uint8_t original = slot.a;
			gb_write8(slot.hl, card);
			wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
			uint8_t evolution_can_attack =
				(CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u;
			if (!evolution_can_attack) {
				wSelectedAttack = SECOND_ATTACK;
				evolution_can_attack =
					(CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u;
			}
			if (evolution_can_attack) {
				(void)AIEncourage(5u);
			} else if (wCurCardCanAttack != 0u) {
				AIDiscourage(2u);
				if (wAlreadyPlayedEnergy == 0u && (LookForEnergyNeededInHand() & 0x10u) != 0u)
					(void)AIEncourage(7u);
			}
			if (wCurCardCanAttack != 0u && wTempAI == 0u) {
				if ((CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) != 0u
				    && (CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u)
					(void)AIEncourage(5u);
				else if (wCurCardCanKO != 0u)
					AIDiscourage(20u);
			}
			if (wTempAI == 0u) {
				hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
				DuelistVarResult hp =
					GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
				uint8_t old_hp = hp.a;
				gb_write8(hp.hl, (uint8_t)(old_hp + wEvolutionHPDifference));
				if (CheckIfDefendingPokemonCanKnockOut(
					0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u)
					AIDiscourage(5u);
				gb_write8(hp.hl, old_hp);
			}
			if ((CheckDamageToMrMime(wTempAI, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u)
				AIDiscourage(20u);
			slot = GetTurnDuelistVariable((uint8_t)(wTempAI + DUELVARS_ARENA_CARD));
			gb_write8(slot.hl, original);
			if (wTempAI == 0u) {
				hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
				if (CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u)
					(void)AIEncourage(5u);
				if (GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a != 0u)
					(void)AIEncourage(4u);
			}
			if (CheckForEvolutionInList(card, 0u, 0u, 0u).f & 0x10u)
				(void)AIEncourage(2u);
			else if (CheckForEvolutionInDeck(card, 0u).f & 0x10u)
				(void)AIEncourage(1u);
			CardDamageResult damage = GetCardDamageAndMaxHP(wTempAI);
			if (damage.a != 0u)
				AIDiscourage(ConvertHPToDamageCounters_Bank5((uint8_t)(damage.a >> 2)).a);
			slot = GetTurnDuelistVariable((uint8_t)(wTempAI + DUELVARS_ARENA_CARD));
			(void)LoadCardDataToBuffer1_FromDeckIndex(slot.a);
			CardId loaded_id = card_id_read_at(wLoadedCard1ID_ADDR);
			if (loaded_id == MYSTERIOUS_FOSSIL)
				(void)AIEncourage(5u);
			else if ((wLoadedCard1AIInfo & 0x0Fu) == AI_INFO_ENCOURAGE_EVO)
				(void)AIEncourage(2u);
			if (wOpponentDeckID == PIKACHU_DECK_ID) {
				if (loaded_id == PIKACHU_LV12 || loaded_id == PIKACHU_LV14
				    || loaded_id == PIKACHU_LV16 || loaded_id == PIKACHU_ALT_LV16)
					AIDiscourage(3u);
			}
			if (wAIScore >= 133u) {
				hTempPlayAreaLocation_ffa1 = wTempAI;
				hTemp_ffa0 = wTempAIPokemonCard;
				(void)AIMakeDecision(OPPACTION_EVOLVE_PKMN, 0u, 0u, 0u, 0u);
				if (wTempAI == 0u)
					wPreviousAIFlags = (uint8_t)(wPreviousAIFlags
						& (uint8_t)~AI_FLAG_USED_PLUSPOWER);
				break;
			}
		}
	}
	return 0xFFu;
}
/* <<< factory AIDecideEvolution */

/* >>> factory AIDecidePlayLegendaryBirds */
void AIDecidePlayLegendaryBirds(void)
{
	uint8_t deck = wOpponentDeckID;
	if (deck != LEGENDARY_ZAPDOS_DECK_ID &&
		deck != LEGENDARY_ARTICUNO_DECK_ID &&
		deck != LEGENDARY_RONALD_DECK_ID)
		return;

	CardId card = card_id_read_at(wLoadedCard1ID_ADDR);
	if (card == ARTICUNO_LV37) {
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a < 2u)
			return;
		CheckIfActiveCardCanKnockOutResult knock =
			CheckIfActiveCardCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((knock.f & 0x10u) != 0u) {
			AIDiscourage(100u);
			return;
		}
		CheckIfActivePokemonCanUseAnyNonResidualAttackResult attack =
			CheckIfActivePokemonCanUseAnyNonResidualAttack(knock.a, knock.f, knock.b, knock.c,
				knock.d, knock.e, knock.hl);
		if ((attack.f & 0x10u) == 0u) {
			AIDiscourage(100u);
			return;
		}
		AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat(0u);
		if ((retreat.f & 0x10u) != 0u) {
			AIDiscourage(100u);
			return;
		}
		if ((GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ) != 0u) {
			AIDiscourage(100u);
			return;
		}
		SwapTurn();
		uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		(void)CopyAttackDataAndDamage_FromDeckIndex(arena, FIRST_ATTACK_OR_PKMN_POWER);
		SwapTurn();
		if (wLoadedAttackCategory == POKEMON_POWER)
			goto check_muk_and_snorlax;
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a >= MAX_BENCH_POKEMON)
			return;

	check_muk_and_snorlax:
		if ((CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) != 0u) {
			AIDiscourage(100u);
			return;
		}
		uint8_t opponent_arena =
			GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		SwapTurn();
		CardId opponent_card = GetCardIDFromDeckIndex(opponent_arena);
		SwapTurn();
		if (opponent_card == SNORLAX) {
			AIDiscourage(100u);
			return;
		}
		(void)AIEncourage(70u);
		return;
	}
	if (card == MOLTRES_LV37) {
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a >= 56u)
			AIDiscourage(100u);
		return;
	}
	if (card == ZAPDOS_LV68 &&
		(CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) != 0u)
		AIDiscourage(100u);
}
/* <<< factory AIDecidePlayLegendaryBirds */

/* >>> factory AIDecidePlayPokemonCard */
AIDecidePlayPokemonCardResult AIDecidePlayPokemonCard(void)
{
	(void)CreateHandCardList(0u);
	(void)SortTempHandByIDList(0u, 0u, 0u, 0u, 0u);
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = wHandTempList_ADDR;
	(void)CopyListWithFFTerminatorFromHLToDE_Bank5(&hl, &de);
	hl = wHandTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		if (card == 0xFFu) {
			/* hand_pokemon.asm:14 `jp z, AIDecideEvolution`: its `.done` is `or a / ret`. */
			uint8_t last = AIDecideEvolution();
			return (AIDecidePlayPokemonCardResult){last, (uint8_t)(last == 0u ? 0x80u : 0u)};
		}
		wTempAIPokemonCard = card;
		uint16_t saved_hl = hl;
		(void)LoadCardDataToBuffer1_FromDeckIndex(card);
		if (wLoadedCard1Type >= TYPE_ENERGY || wLoadedCard1Stage != 0u) {
			hl = saved_hl;
			continue;
		}
		wAIScore = 130u;
		AIDecidePlayLegendaryBirds();
		DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (count.a >= 4u)
			AIDiscourage(20u);
		else
			(void)AIEncourage(50u);
		hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
		CheckIfDefendingPokemonCanKnockOutResult ko =
			CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if (ko.f & 0x10u)
			(void)AIEncourage(20u);
		EnergyCostBitsResult cost = GetAttacksEnergyCostBits(wTempAIPokemonCard);
		EnergyFlagsResult energy = CheckEnergyFlagsNeededInList(cost.a);
		if (energy.carry)
			(void)AIEncourage(20u);
		CheckForEvolutionInListResult hand_evo =
			CheckForEvolutionInList(wTempAIPokemonCard, 0u, 0u, 0u);
		if (hand_evo.f & 0x10u)
			(void)AIEncourage(20u);
		CheckForEvolutionInDeckResult deck_evo =
			CheckForEvolutionInDeck(wTempAIPokemonCard, 0u);
		if (deck_evo.f & 0x10u)
			(void)AIEncourage(10u);
		if (wAIScore < 180u) {
			hl = saved_hl;
			continue;
		}
		hTemp_ffa0 = wTempAIPokemonCard;
		CheckIfCardCanBePlayedResult playable = CheckIfCardCanBePlayed(wTempAIPokemonCard, 0u);
		if (playable.f & 0x10u) {
			hl = saved_hl;
			continue;
		}
		AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, 0u, 0u, 0u, 0u);
		if (decision.f & 0x10u)
			return (AIDecidePlayPokemonCardResult){decision.a, decision.f}; /* turn ended */
		hl = saved_hl;
	}
}
/* <<< factory AIDecidePlayPokemonCard */
