#include "home/legendary_zapdos.h"

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
#define AI_TRAINER_CARD_PHASE_01 0x01u
#define AI_TRAINER_CARD_PHASE_04 0x04u
#define AI_TRAINER_CARD_PHASE_07 0x07u
#define AI_TRAINER_CARD_PHASE_10 0x0au
#define AI_TRAINER_CARD_PHASE_13 0x0du
#define DUELVARS_ARENA_CARD 0xbbu
#define ELECTABUZZ_LV35 0x71u
#define ELECTRODE_LV35 0x6eu
#define OPPACTION_FINISH_NO_ATTACK 0x05u
#define PLAY_AREA_ARENA 0x00u
#define VOLTORB 0x6du
/* <<< factory statics */

/* >>> factory AIDoTurn_LegendaryZapdos */
AIDoTurn_LegendaryZapdosResult AIDoTurn_LegendaryZapdos(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	InitAITurnVars();
	HandleAIAntiMewtwoDeckStrategyResult anti = HandleAIAntiMewtwoDeckStrategy(a, f, b, c, d, e, hl);
	a = anti.a;
	f = anti.f;
	if ((f & 0x10u) != 0u) {
		AIProcessHandTrainerCardsWrapResult trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
		a = trainer.a;
		f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_04);
		a = trainer.a;
		f = trainer.f;
		AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);
		a = trainer.a;
		f = trainer.f;
		AIProcessRetreatResult retreat = AIProcessRetreat();
		a = retreat.a;
		f = retreat.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);
		a = trainer.a;
		f = trainer.f;
		if (wAlreadyPlayedEnergy == 0u) {
			DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
			uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
			uint8_t skip_energy = 0u;
			if ((uint8_t)card_id == VOLTORB) {
				CoreCardListResult found = LookForCardIDInHandList_Bank5(ELECTRODE_LV35);
				if ((found.f & 0x10u) != 0u)
					card_id = VOLTORB;
				else
					skip_energy = 0u;
			}
			if ((uint8_t)card_id == VOLTORB || (uint8_t)card_id == ELECTABUZZ_LV35) {
				CoreCardListResult energy = CreateEnergyCardListFromHand(arena.a);
				if ((energy.f & 0x10u) != 0u)
					skip_energy = 1u;
				else {
					CountNumberOfEnergyCardsAttachedResult attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA);
					if (attached.a == 0u) {
						hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
						if (AITryToPlayEnergyCard() != 0u)
							skip_energy = 1u;
					}
				}
			}
			if (skip_energy == 0u)
				AIProcessAndTryToPlayEnergy();
		}
		AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_13);
		a = trainer.a;
		f = trainer.f;
	}
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u)
		return (AIDoTurn_LegendaryZapdosResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIDoTurn_LegendaryZapdosResult){decision.f};
}
/* <<< factory AIDoTurn_LegendaryZapdos */
