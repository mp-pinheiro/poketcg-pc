#include "home/legendary_ronald.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/attacks.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/energy.h"
#include "home/general.h"
#include "home/hand_pokemon.h"
#include "home/init.h"
#include "home/substatus.h"
#define AI_FLAG_USED_PROFESSOR_OAK 0x04u
#define AI_TRAINER_CARD_PHASE_01 0x01u
#define AI_TRAINER_CARD_PHASE_02 0x02u
#define AI_TRAINER_CARD_PHASE_04 0x04u
#define AI_TRAINER_CARD_PHASE_05 0x05u
#define AI_TRAINER_CARD_PHASE_07 0x07u
#define AI_TRAINER_CARD_PHASE_10 0x0au
#define AI_TRAINER_CARD_PHASE_15 0x0fu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xbau
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define DECK_SIZE 0x3cu
#define MAX_PLAY_AREA_POKEMON 0x06u
#define MOLTRES_LV37 0x40u
#define MUK 0x27u
#define OPPACTION_FINISH_NO_ATTACK 0x05u
#define OPPACTION_PLAY_BASIC_PKMN 0x01u
/* <<< factory statics */

/* >>> factory AIDoTurn_LegendaryRonald */
AIDoTurn_LegendaryRonaldResult AIDoTurn_LegendaryRonald(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	InitAITurnVars();
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_04);

	DuelistVarResult play_area = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (play_area.a < MAX_PLAY_AREA_POKEMON) {
		DuelistVarResult cards = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
		if (cards.a < (DECK_SIZE - 9u)) {
			PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
			if ((muk.f & 0x10u) == 0u) {
				CoreCardListResult moltres = LookForCardIDInHandList_Bank5(MOLTRES_LV37);
				if ((moltres.f & 0x10u) != 0u) {
					hTemp_ffa0 = moltres.a;
					AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e);
					(void)decision;
				}
			}
		}
	}
	AIDecidePlayPokemonCard();
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);
	AIProcessRetreat();
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);
	if (wAlreadyPlayedEnergy == 0u)
		AIProcessAndTryToPlayEnergy();
	AIDecidePlayPokemonCard();
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_15);
	if ((wPreviousAIFlags & AI_FLAG_USED_PROFESSOR_OAK) != 0u) {
		AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
		AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
		AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_04);

		play_area = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (play_area.a < MAX_PLAY_AREA_POKEMON) {
			DuelistVarResult cards = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
			if (cards.a < (DECK_SIZE - 9u)) {
				PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
				if ((muk.f & 0x10u) == 0u) {
					CoreCardListResult moltres = LookForCardIDInHandList_Bank5(MOLTRES_LV37);
					if ((moltres.f & 0x10u) != 0u) {
						hTemp_ffa0 = moltres.a;
						AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e);
						(void)decision;
					}
				}
			}
		}
	}
	AIDecidePlayPokemonCard();
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07);
	AIProcessRetreat();
	AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);
	if (wAlreadyPlayedEnergy == 0u)
		AIProcessAndTryToPlayEnergy();
	AIDecidePlayPokemonCard();
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u)
		return (AIDoTurn_LegendaryRonaldResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIDoTurn_LegendaryRonaldResult){decision.f};
}
/* <<< factory AIDoTurn_LegendaryRonald */
