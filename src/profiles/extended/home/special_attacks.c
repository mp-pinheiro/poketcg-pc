/* >>> factory HandleSpecialAIAttacks */
#define DUELVARS_BENCH 0xBCu
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xEEu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu

static uint8_t special_cp_flags(uint8_t a, uint8_t n)
{
	return (uint8_t)(0x40u | (a == n ? 0x80u : 0u)
		| ((a & 0x0Fu) < (n & 0x0Fu) ? 0x20u : 0u) | (a < n ? 0x10u : 0u));
}

static HandleSpecialAIAttacksResult special_zero_score(void)
{
	return (HandleSpecialAIAttacksResult){0u, 0x80u};
}

static HandleSpecialAIAttacksResult special_bench_slots_score(uint8_t limit)
{
	DuelistVarResult n = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (n.a >= limit)
		return special_zero_score();
	return (HandleSpecialAIAttacksResult){(uint8_t)(0x80u + limit - n.a), 0x00u};
}

static uint8_t special_in_deck(CardId card)
{
	return (uint8_t)(LookForCardIDInLocation_Bank5(CARD_LOCATION_DECK, card).f & 0x10u);
}

HandleSpecialAIAttacksResult HandleSpecialAIAttacks(void)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	DuelistVarResult arena = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	CardId card = GetCardIDFromDeckIndex(arena.a);

	switch (card) {
	case NIDORANF:
		if (!special_in_deck(NIDORANM) && !special_in_deck(NIDORANF))
			return special_zero_score();
		return special_bench_slots_score(MAX_PLAY_AREA_POKEMON);
	case ODDISH:
	case BELLSPROUT:
	case KRABBY:
		if (!special_in_deck(card))
			return special_zero_score();
		return special_bench_slots_score(MAX_BENCH_POKEMON);
	case MAROWAK_LV26:
		if (!special_in_deck(GEODUDE) && !special_in_deck(ONIX)
		    && !special_in_deck(CUBONE) && !special_in_deck(RHYHORN))
			return special_zero_score();
		return special_bench_slots_score(MAX_BENCH_POKEMON);
	case JIGGLYPUFF_LV13:
		if (!(CheckIfAnyBasicPokemonInDeck().f & 0x10u))
			return special_zero_score();
		return special_bench_slots_score(MAX_PLAY_AREA_POKEMON);
	case EXEGGUTOR: {
		AIDecideWhetherToRetreatResult r = AIDecideWhetherToRetreat(0u);
		if (!(r.f & 0x10u))
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x8Au, r.f};
	}
	case SCYTHER:
	case VAPOREON_LV29: {
		if (wAICannotDamage != 0u)
			return (HandleSpecialAIAttacksResult){0x85u, 0x00u};
		wSelectedAttack = SECOND_ATTACK;
		CheckIfSelectedAttackIsUnusableResult u =
			CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, 0u, 0u, 0u, 0u, 0u, 0u);
		if (u.f & 0x10u)
			return (HandleSpecialAIAttacksResult){0x85u, u.f};
		(void)EstimateDamage_VersusDefendingCard(SECOND_ATTACK);
		if (gb_read8(wDamage_ADDR) != 0u)
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x85u, 0x80u};
	}
	case ELECTRODE_LV42: {
		SwapTurn();
		uint8_t color = GetArenaCardColor();
		SwapTurn();
		uint16_t hl = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
		for (;;) {
			uint8_t index = gb_read8(hl++);
			if (index == 0xFFu)
				return (HandleSpecialAIAttacksResult){0x82u, 0xC0u};
			if (GetCardType(GetCardIDFromDeckIndex(index)) == color)
				return special_zero_score();
		}
	}
	case MEW_LV23: {
		LookForCardThatIsKnockedOutOnDevolutionResult r = LookForCardThatIsKnockedOutOnDevolution(0u);
		if (!(r.f & 0x10u))
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x85u, r.f};
	}
	case PORYGON: {
		uint8_t status = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
		if (status == CONFUSED)
			return special_zero_score();
		uint8_t set_up = CountNumberOfSetUpBenchPokemon(0u, 0u, 0u, 0u, 0u, 0u, 0u).a;
		uint8_t f = special_cp_flags(set_up, 2u);
		uint8_t high = wSelectedAttack == 0u ? (uint8_t)(set_up >= 2u) : (uint8_t)(set_up < 2u);
		return (HandleSpecialAIAttacksResult){high ? 0x82u : 0x81u, f};
	}
	case MEWTWO_ALT_LV60:
	case MEWTWO_LV60: {
		LookForCardIDInLocationResult r =
			LookForCardIDInLocation_Bank5(CARD_LOCATION_DISCARD_PILE, PSYCHIC_ENERGY);
		if (!(r.f & 0x10u))
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x82u, r.f};
	}
	case NINETALES_LV35: {
		if (GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a == 0u)
			return special_zero_score();
		uint8_t roll = Random(3u);
		if (roll == 0u)
			return (HandleSpecialAIAttacksResult){0x83u, 0x80u};
		if (roll == 1u)
			return (HandleSpecialAIAttacksResult){0u, 0xC0u};
		SwapTurn();
		HandListResult hand = CreateHandCardList(0u);
		SwapTurn();
		if (hand.a == 0u)
			return special_zero_score();
		if (GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a < 3u) {
			uint8_t basics = 0u;
			for (uint16_t hl = wDuelTempList_ADDR;; hl++) {
				uint8_t index = gb_read8(hl);
				if (index == 0xFFu)
					break;
				SwapTurn();
				(void)LoadCardDataToBuffer2_FromDeckIndex(index);
				SwapTurn();
				if (gb_read8(wLoadedCard2Type_ADDR) >= TYPE_ENERGY)
					continue;
				if (gb_read8(wLoadedCard2Stage_ADDR) != 0u)
					continue;
				basics++;
			}
			if (basics >= 2u)
				return (HandleSpecialAIAttacksResult){0x83u, special_cp_flags(basics, 2u)};
		}
		uint16_t hl = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).hl;
		for (;;) {
			uint8_t index = gb_read8(hl++);
			if (index == 0xFFu)
				return special_zero_score();
			SwapTurn();
			CheckForEvolutionInListResult r = CheckForEvolutionInList(index, 0u, 0u, 0u);
			SwapTurn();
			if (r.f & 0x10u)
				return (HandleSpecialAIAttacksResult){0x83u, r.f};
		}
	}
	case ZAPDOS_LV68:
		return (HandleSpecialAIAttacksResult){0x83u, 0xC0u};
	case KANGASKHAN: {
		uint8_t used = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
		if (used >= 41u)
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x80u, special_cp_flags(used, 41u)};
	}
	case DUGTRIO: {
		uint16_t hl = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
		uint8_t d = 0u;
		uint8_t e = (uint8_t)(PLAY_AREA_BENCH_1 - 1u);
		for (;;) {
			e++;
			uint8_t index = gb_read8(hl++);
			if (index == 0xFFu)
				break;
			DuelistVarResult hp = GetTurnDuelistVariable((uint8_t)(e + DUELVARS_ARENA_CARD_HP));
			if (hp.a >= 20u)
				continue;
			d++;
		}
		SwapTurn();
		uint8_t prizes = CountPrizes();
		SwapTurn();
		if (prizes <= d)
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x80u, special_cp_flags(prizes, d)};
	}
	case ELECTRODE_LV35: {
		if (!special_in_deck(LIGHTNING_ENERGY))
			return special_zero_score();
		AIEnergyResult r = AIProcessButDontPlayEnergy_SkipEvolution();
		if (!(r.f & 0x10u))
			return special_zero_score();
		return (HandleSpecialAIAttacksResult){0x83u, r.f};
	}
	case GOLDUCK:
	case DRAGONAIR: {
		SwapTurn();
		uint8_t attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
		SwapTurn();
		if (attached == 0u)
			return (HandleSpecialAIAttacksResult){0x80u, 0x80u};
		return (HandleSpecialAIAttacksResult){0x83u, 0x00u};
	}
	default:
		return special_zero_score();
	}
}
/* <<< factory HandleSpecialAIAttacks */
