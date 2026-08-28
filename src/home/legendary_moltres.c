#include "home/legendary_moltres.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/attacks.h"
#include "home/common.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/energy.h"
#include "home/general.h"
#include "home/hand_pokemon.h"
#include "home/init.h"
#include "home/substatus.h"
#define AI_TRAINER_CARD_PHASE_02 0x02u
#define AI_TRAINER_CARD_PHASE_04 0x04u
#define AI_TRAINER_CARD_PHASE_05 0x05u
#define AI_TRAINER_CARD_PHASE_10 0x0au
#define AI_TRAINER_CARD_PHASE_11 0x0bu
#define AI_TRAINER_CARD_PHASE_13 0x0du
#define DECK_SIZE 0x3cu
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xbau
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define MAGMAR_LV31 0x3cu
#define MAX_PLAY_AREA_POKEMON 0x06u
#define MOLTRES_LV37 0x40u
#define MUK 0x27u
#define OPPACTION_FINISH_NO_ATTACK 0x05u
#define OPPACTION_PLAY_BASIC_PKMN 0x01u
#define PLAY_AREA_ARENA 0x00u
/* rgbasm mixed shift/add: (2 << 0) + (2 << 2) = 0x0a. */
/* <<< factory statics */

/* >>> factory AIDoTurn_LegendaryMoltres */
AIDoTurn_LegendaryMoltresResult AIDoTurn_LegendaryMoltres(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	InitAITurnVars();
	HandleAIAntiMewtwoDeckStrategyResult anti = HandleAIAntiMewtwoDeckStrategy(a, f, b, c, d, e, hl);
	a = anti.a; f = anti.f;
	if ((f & 0x10u) != 0u) {
		AIProcessHandTrainerCardsWrapResult trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
		a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_04); a = trainer.a; f = trainer.f;
		DuelistVarResult play_area = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (play_area.a < MAX_PLAY_AREA_POKEMON) {
			DuelistVarResult deck_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
			if (deck_count.a < (uint8_t)(DECK_SIZE - 9u)) {
				PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
				if ((muk.f & 0x10u) == 0u) {
					CoreCardListResult moltres = LookForCardIDInHandList_Bank5(MOLTRES_LV37);
					if ((moltres.f & 0x10u) != 0u) { hTemp_ffa0 = moltres.a; AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e); a = decision.b; f = decision.f; }
				}
			}
		}
		AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05); a = trainer.a; f = trainer.f;
		AIProcessRetreatResult retreat = AIProcessRetreat(); a = retreat.a; f = retreat.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_11); a = trainer.a; f = trainer.f;
		if (wAlreadyPlayedEnergy == 0u) {
			DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
			uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
			if ((uint8_t)card_id == MAGMAR_LV31) {
				CoreCardListResult energy = CreateEnergyCardListFromHand(arena.a);
				if ((energy.f & 0x10u) == 0u) {
					CountNumberOfEnergyCardsAttachedResult attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA);
					if (attached.a == 0u) { hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA; if (AITryToPlayEnergyCard() == 0u) AIProcessAndTryToPlayEnergy(); }
					else AIProcessAndTryToPlayEnergy();
				}
			} else AIProcessAndTryToPlayEnergy();
		}
		AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_13); a = trainer.a; f = trainer.f;
	}
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u) return (AIDoTurn_LegendaryMoltresResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIDoTurn_LegendaryMoltresResult){decision.f};
}
/* <<< factory AIDoTurn_LegendaryMoltres */
