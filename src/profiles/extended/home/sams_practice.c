/* >>> factory AIPerformScriptedTurn */
SamsPracticeResult AIPerformScriptedTurn(uint8_t a, uint8_t f, uint8_t b,
					uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t scripted_turn = (uint8_t)(wDuelTurns >> 1);
	switch (scripted_turn) {
	case 0: {
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(MACHOP, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = MACHOP;
		e = FIGHTING_ENERGY;
		break;
	}
	case 1: {
		CoreCardListResult hand = LookForCardIDInHandList_Bank5(RATTATA);
		hTemp_ffa0 = hand.a;
		AIMakeDecisionResult decision =
			AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e);
		b = decision.b;
		c = decision.c;
		d = decision.d;
		e = decision.e;
		f = decision.f;
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(RATTATA, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = RATTATA;
		e = FIGHTING_ENERGY;
		break;
	}
	case 2: {
		LookResult found = LookForCardIDInPlayArea_Bank5(RATTATA, PLAY_AREA_ARENA);
		hTempPlayAreaLocation_ffa1 = found.a;
		CoreCardListResult hand = LookForCardIDInHandList_Bank5(RATICATE);
		hTemp_ffa0 = hand.a;
		AIMakeDecisionResult decision =
			AIMakeDecision(OPPACTION_EVOLVE_PKMN, b, c, d, e);
		b = decision.b;
		c = decision.c;
		d = decision.d;
		e = decision.e;
		f = decision.f;
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(RATICATE, LIGHTNING_ENERGY);
		a = result.a;
		f = result.f;
		d = RATICATE;
		e = LIGHTNING_ENERGY;
		break;
	}
	case 3: {
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(RATICATE, LIGHTNING_ENERGY);
		a = result.a;
		f = result.f;
		d = RATICATE;
		e = LIGHTNING_ENERGY;
		break;
	}
	case 4: {
		CoreCardListResult hand = LookForCardIDInHandList_Bank5(MACHOP);
		hTemp_ffa0 = hand.a;
		AIMakeDecisionResult decision =
			AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e);
		b = decision.b;
		c = decision.c;
		d = decision.d;
		e = decision.e;
		f = decision.f;
		AIAttachEnergyInHandToCardInBenchResult result =
			AIAttachEnergyInHandToCardInBench(MACHOP, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = MACHOP;
		e = FIGHTING_ENERGY;
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		CardId arena_card = GetCardIDFromDeckIndex(arena.a);
		uint8_t retreat_a = PLAY_AREA_BENCH_1;
		uint8_t retreat_f;
		if (arena_card == MACHOP) {
			retreat_a = PLAY_AREA_BENCH_2;
			retreat_f = 0u;
		} else {
			retreat_f = 0x40u;
			if ((arena_card & 0x0Fu) < (MACHOP & 0x0Fu))
				retreat_f = (uint8_t)(retreat_f | 0x20u);
			if (arena_card < MACHOP)
				retreat_f = (uint8_t)(retreat_f | 0x10u);
		}
		AITryToRetreatResult retreat = AITryToRetreat(retreat_a, retreat_f);
		a = retreat.a;
		f = retreat.f;
		break;
	}
	case 5:
	case 6: {
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(MACHOP, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = MACHOP;
		e = FIGHTING_ENERGY;
		break;
	}
	default:
		break;
	}

	a = 0u;
	f = 0x80u;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(a, f, b, c, d, e, hl);
	a = unusable.a;
	f = unusable.f;
	b = unusable.b;
	c = unusable.c;
	d = unusable.d;
	e = unusable.e;
	hl = unusable.hl;
	if ((f & 0x10u) == 0u) {
		AITryUseAttackResult attack = AITryUseAttack(b);
		f = attack.f;
		return (SamsPracticeResult){a, f, b, c, d, e, hl};
	}
	AIMakeDecisionResult decision =
		AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	b = decision.b;
	c = decision.c;
	d = decision.d;
	e = decision.e;
	f = decision.f;
	a = (uint8_t)(wDuelFinished | 1u);
	return (SamsPracticeResult){a, f, b, c, d, e, hl};
}
/* <<< factory AIPerformScriptedTurn */
/* === factory GetPlayAreaLocationOfRaticateOrRattata */
/* === factory SetSamsStartingPlayArea */
