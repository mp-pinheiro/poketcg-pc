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
		AIDecidePlayPokemonCardResult played = AIDecidePlayPokemonCard();
		if ((played.f & 0x10u) != 0u)
			return (AIDoTurn_LegendaryZapdosResult){played.f}; /* turn ended */
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
			uint8_t attach_to_arena = card_id == ELECTABUZZ_LV35;
			if (card_id == VOLTORB)
				attach_to_arena = (LookForCardIDInHandList_Bank5(ELECTRODE_LV35).f & 0x10u) != 0u;
			if (attach_to_arena) {
				CoreCardListResult energy = CreateEnergyCardListFromHand(arena.a);
				if ((energy.f & 0x10u) != 0u)
					skip_energy = 1u;
				else {
					CountNumberOfEnergyCardsAttachedResult attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA);
					if (attached.a == 0u) {
						hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
						if ((AITryToPlayEnergyCard().f & 0x10u) != 0u)
							skip_energy = 1u;
					}
				}
			}
			if (skip_energy == 0u)
				AIProcessAndTryToPlayEnergy();
		}
		played = AIDecidePlayPokemonCard();
		if ((played.f & 0x10u) != 0u)
			return (AIDoTurn_LegendaryZapdosResult){played.f}; /* turn ended */
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
