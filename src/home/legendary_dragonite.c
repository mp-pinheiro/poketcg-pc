#include "home/legendary_dragonite.h"

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
#define AI_FLAG_USED_PROFESSOR_OAK 0x04u
#define AI_TRAINER_CARD_PHASE_01 0x01u
#define AI_TRAINER_CARD_PHASE_02 0x02u
#define AI_TRAINER_CARD_PHASE_07 0x07u
#define AI_TRAINER_CARD_PHASE_10 0x0au
#define AI_TRAINER_CARD_PHASE_11 0x0bu
#define AI_TRAINER_CARD_PHASE_15 0x0fu
#define DUELVARS_ARENA_CARD 0xbbu
#define KANGASKHAN 0xb9u
#define OPPACTION_FINISH_NO_ATTACK 0x05u
#define PLAY_AREA_ARENA 0x00u
/* <<< factory statics */

/* >>> factory AIDoTurn_LegendaryDragonite */
AIDoTurn_LegendaryDragoniteResult AIDoTurn_LegendaryDragonite(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	InitAITurnVars();
	AIProcessHandTrainerCardsWrapResult trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
	a = trainer.a;
	f = trainer.f;
	HandleAIAntiMewtwoDeckStrategyResult anti = HandleAIAntiMewtwoDeckStrategy(a, f, b, c, d, e, hl);
	a = anti.a;
	f = anti.f;
	if ((f & 0x10u) != 0u) {
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
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
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_11);
		a = trainer.a;
		f = trainer.f;
		if (wAlreadyPlayedEnergy == 0u) {
			DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
			uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
			uint8_t skip_energy = 0u;
			if ((uint8_t)card_id == KANGASKHAN) {
				CoreCardListResult energy_list = CreateEnergyCardListFromHand(arena.a);
				if ((energy_list.f & 0x10u) != 0u) {
					skip_energy = 1u;
				} else {
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
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_15);
		a = trainer.a;
		f = trainer.f;
		if ((wPreviousAIFlags & AI_FLAG_USED_PROFESSOR_OAK) != 0u) {
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
			a = trainer.a;
			f = trainer.f;
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
			a = trainer.a;
			f = trainer.f;
			AIDecidePlayPokemonCard();
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);
			a = trainer.a;
			f = trainer.f;
			retreat = AIProcessRetreat();
			a = retreat.a;
			f = retreat.f;
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);
			a = trainer.a;
			f = trainer.f;
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_11);
			a = trainer.a;
			f = trainer.f;
			if (wAlreadyPlayedEnergy == 0u)
				AIProcessAndTryToPlayEnergy();
			AIDecidePlayPokemonCard();
		}
	}
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u)
		return (AIDoTurn_LegendaryDragoniteResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIDoTurn_LegendaryDragoniteResult){decision.f};
}
/* <<< factory AIDoTurn_LegendaryDragonite */
