/* >>> factory AIDoTurn_LegendaryMoltres */
/* rgbasm mixed shift/add: (2 << 0) + (2 << 2) = 0x0a. */
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
		AIDecidePlayPokemonCardResult played = AIDecidePlayPokemonCard();
		if ((played.f & 0x10u) != 0u)
			return (AIDoTurn_LegendaryMoltresResult){played.f}; /* turn ended */
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05); a = trainer.a; f = trainer.f;
		AIProcessRetreatResult retreat = AIProcessRetreat(); a = retreat.a; f = retreat.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_11); a = trainer.a; f = trainer.f;
		if (wAlreadyPlayedEnergy == 0u) {
			DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
			uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
			if (card_id == MAGMAR_LV31) {
				CoreCardListResult energy = CreateEnergyCardListFromHand(arena.a);
				if ((energy.f & 0x10u) == 0u) {
					CountNumberOfEnergyCardsAttachedResult attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA);
					if (attached.a == 0u) { hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA; if ((AITryToPlayEnergyCard().f & 0x10u) == 0u) AIProcessAndTryToPlayEnergy(); }
					else AIProcessAndTryToPlayEnergy();
				}
			} else AIProcessAndTryToPlayEnergy();
		}
		(void)AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_13); a = trainer.a; f = trainer.f;
	}
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u) return (AIDoTurn_LegendaryMoltresResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIDoTurn_LegendaryMoltresResult){decision.f};
}
/* <<< factory AIDoTurn_LegendaryMoltres */
