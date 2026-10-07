/* >>> factory CheckSpecificDecksToAttachDoubleColorless */
static CardId CheckSpecificDecksToAttachDoubleColorless_GetID(void)
{
	uint8_t loc = hTempPlayAreaLocation_ff9d;
	DuelistVarResult v = GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD));
	return GetCardIDFromDeckIndex(v.a);
}

CheckSpecificDecksToAttachDoubleColorlessResult CheckSpecificDecksToAttachDoubleColorless(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t deck_id = wOpponentDeckID;
	uint8_t a = deck_id;
	uint8_t check_colorless = 0u;

	if (deck_id == LEGENDARY_DRAGONITE_DECK_ID) {
		CardId card_id = CheckSpecificDecksToAttachDoubleColorless_GetID();
		a = (uint8_t)(card_id >> 8);
		if (a == 0u)
			a = (uint8_t)card_id;
		if (card_id == CHARMANDER || card_id == DRATINI)
			check_colorless = 1u;
	} else if (deck_id == FIRE_CHARGE_DECK_ID) {
		CardId card_id = CheckSpecificDecksToAttachDoubleColorless_GetID();
		a = (uint8_t)(card_id >> 8);
		if (a == 0u)
			a = (uint8_t)card_id;
		if (card_id == GROWLITHE)
			check_colorless = 1u;
	} else if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		CardId card_id = CheckSpecificDecksToAttachDoubleColorless_GetID();
		a = (uint8_t)(card_id >> 8);
		if (a == 0u)
			a = (uint8_t)card_id;
		if (card_id == DRATINI)
			check_colorless = 1u;
	}

	if (check_colorless) {
		uint8_t loc = hTempPlayAreaLocation_ff9d;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + COLORLESS));
		if (a == 0u) {
			CoreCardListResult r = LookForCardIDInHand(DOUBLE_COLORLESS_ENERGY);
			if (!(r.f & 0x10u)) {
				hTemp_ffa0 = r.a;
				return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x10u, b, c, d, e, hl};
			}
			a = r.a;
		}
	}
	return (CheckSpecificDecksToAttachDoubleColorlessResult){a, (uint8_t)(a == 0u ? 0x80u : 0u), b, c, d, e, hl};
}
/* <<< factory CheckSpecificDecksToAttachDoubleColorless */
/* >>> factory GetEnergyCardForDiscardOrEnergyBoostAttack */
GetEnergyCardForDiscardOrEnergyBoostAttackResult GetEnergyCardForDiscardOrEnergyBoostAttack(uint8_t c_in)
{
	DuelistVarResult dv = GetTurnDuelistVariable((uint8_t)(hTempPlayAreaLocation_ff9d + DUELVARS_ARENA_CARD));
	(void)LoadCardDataToBuffer2_FromDeckIndex(dv.a);
	CardId loaded_id = card_id_read_at(wLoadedCard2ID_ADDR);
	uint8_t a = (uint8_t)loaded_id;
	uint8_t b = a;
	uint16_t hl;
	a = wSelectedAttack;
	if (a == 0u) {
		hl = wLoadedCard2Atk1EnergyCost_ADDR;
	} else {
		a = b;
		if (loaded_id == ZAPDOS_LV64)
			return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, b, c_in, 0u, 0x00u};
		if (loaded_id == CHARIZARD || loaded_id == EXEGGUTOR)
			return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, FALSE, TRUE, 0u, 0x90u};
		hl = wLoadedCard2Atk2EnergyCost_ADDR;
	}

	uint8_t e;
	uint8_t f;
	a = gb_read8(hl); hl = (uint16_t)(hl + 1u);
	b = a;
	a = (uint8_t)(a & 0xF0u);
	if (a != 0u) {
		e = FIRE_ENERGY;
		f = 0x10u;
	} else {
		a = b;
		a = (uint8_t)(a & 0x0Fu);
		if (a != 0u) {
			e = GRASS_ENERGY;
			f = 0x10u;
		} else {
			a = gb_read8(hl); hl = (uint16_t)(hl + 1u);
			b = a;
			a = (uint8_t)(a & 0xF0u);
			if (a != 0u) {
				e = LIGHTNING_ENERGY;
				f = 0x10u;
			} else {
				a = b;
				a = (uint8_t)(a & 0x0Fu);
				if (a != 0u) {
					e = WATER_ENERGY;
					f = 0x10u;
				} else {
					a = gb_read8(hl); hl = (uint16_t)(hl + 1u);
					b = a;
					a = (uint8_t)(a & 0xF0u);
					if (a != 0u) {
						e = FIGHTING_ENERGY;
						f = 0x10u;
					} else {
						e = PSYCHIC_ENERGY;
						f = 0x90u;
					}
				}
			}
		}
	}
	return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, TRUE, FALSE, e, f};
}
/* <<< factory GetEnergyCardForDiscardOrEnergyBoostAttack */
/* >>> factory AITryToPlayEnergyCard */
AITryToPlayEnergyCardResult AITryToPlayEnergyCard(void)
{
	uint8_t pending;
	uint8_t attack;
	uint8_t need_b;
	uint8_t need_c;
	uint8_t need_e;

	gb_write8(wTempAI_ADDR, 0u);
	gb_write8(wSelectedAttack_ADDR, FIRST_ATTACK_OR_PKMN_POWER_600);
	CheckEnergyNeededForAttackResult r1 = CheckEnergyNeededForAttack();
	if (r1.f & 0x10u) {
		if (r1.b != 0u || r1.c != 0u) {
			need_b = r1.b;
			need_c = r1.c;
			need_e = r1.e;
			goto check_deck;
		}
	}

second_attack:
	gb_write8(wSelectedAttack_ADDR, SECOND_ATTACK_600);
	CheckEnergyNeededForAttackResult r2 = CheckEnergyNeededForAttack();
	if (r2.f & 0x10u) {
		if (r2.b != 0u || r2.c != 0u) {
			need_b = r2.b;
			need_c = r2.c;
			need_e = r2.e;
			goto check_deck;
		}
	}

	{
		gb_write8(wTempAI_ADDR, 1u);
		gb_write8(wSelectedAttack_ADDR, FIRST_ATTACK_OR_PKMN_POWER_600);
		(void)CheckEnergyNeededForAttack();
		AttackFlagResult f1a = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | ATTACHED_ENERGY_BOOST_F_600));
		if (f1a.f & 0x10u)
			goto energy_boost_or_discard_energy;
		AttackFlagResult f1b = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | DISCARD_ENERGY_F_600));
		if (f1b.f & 0x10u)
			goto energy_boost_or_discard_energy;

		gb_write8(wSelectedAttack_ADDR, SECOND_ATTACK_600);
		(void)CheckEnergyNeededForAttack();
		AttackFlagResult f2a = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | ATTACHED_ENERGY_BOOST_F_600));
		if (f2a.f & 0x10u)
			goto energy_boost_or_discard_energy;
		AttackFlagResult f2b = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | DISCARD_ENERGY_F_600));
		if (f2b.f & 0x10u)
			goto energy_boost_or_discard_energy;

		CheckIfEvolutionNeedsEnergyForAttackResult evo =
			CheckIfEvolutionNeedsEnergyForAttack(0u, 0u, 0u, 0u, 0u);
		if ((evo.f & 0x10u) == 0u)
			return (AITryToPlayEnergyCardResult){evo.a, evo.f};
		(void)CreateEnergyCardListFromHand(evo.a);
		need_b = evo.b;
		need_c = evo.c;
		need_e = evo.e;
		goto check_deck;
	}

energy_boost_or_discard_energy:
	{
		GetEnergyCardForDiscardOrEnergyBoostAttackResult g =
			GetEnergyCardForDiscardOrEnergyBoostAttack(0u);
		if ((g.f & 0x10u) == 0u)
			return (AITryToPlayEnergyCardResult){g.a, g.f};
		need_b = g.b;
		need_c = g.c;
		need_e = g.e;
	}

check_deck:
	{
		CheckSpecificDecksToAttachDoubleColorlessResult sd =
			CheckSpecificDecksToAttachDoubleColorless(need_b, need_c, 0u, need_e, 0u);
		if (sd.f & 0x10u)
			goto play_energy_card;

		if (need_b != 0u) {
			CoreCardListResult look = LookForCardIDInHand(need_e);
			gb_write8(hTemp_ffa0_ADDR, look.a);
			if ((look.f & 0x10u) == 0u)
				goto play_energy_card;
		}

		if (gb_read8(hTempPlayAreaLocation_ff9d_ADDR) != 0u)
			goto look_for_any_energy;
		if (need_c == 0u)
			goto check_if_done;
		if (need_c != 2u)
			goto look_for_any_energy;

		{
			uint16_t hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl = (uint16_t)(hl + 1u);
				if (v == 0xFFu)
					goto look_for_any_energy;
				gb_write8(hTemp_ffa0_ADDR, v);
				CardId id = GetCardIDFromDeckIndex(v);
				if (id == DOUBLE_COLORLESS_ENERGY_600)
					goto play_energy_card;
			}
		}

	look_for_any_energy:
		{
			uint16_t hl = wDuelTempList_ADDR;
			(void)ShuffleCards(CountCardsInDuelTempList().a, hl);
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl = (uint16_t)(hl + 1u);
				if (v == 0xFFu)
					goto check_if_done;
				CheckIfOpponentHasBossDeckIDResult boss = CheckIfOpponentHasBossDeckID(v);
				uint8_t load;
				if (boss.carry == 0u) {
					load = v;
				} else {
					CardId id = GetCardIDFromDeckIndex(v);
					if (id == DOUBLE_COLORLESS_ENERGY_600)
						continue;
					load = boss.a;
				}
				gb_write8(hTemp_ffa0_ADDR, load);
				break;
			}
		}
	}

play_energy_card:
	{
		uint8_t loc = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
		gb_write8(hTempPlayAreaLocation_ffa1_ADDR, loc);
		AIMakeDecisionResult played =
			AIMakeDecision(OPPACTION_PLAY_ENERGY_600, 0u, 0u, 0u, 0u);

		return (AITryToPlayEnergyCardResult){played.a, 0x10u};
	}

check_if_done:
	pending = gb_read8(wTempAI_ADDR);
	if (pending != 0u)
		return (AITryToPlayEnergyCardResult){pending, 0x00u};
	attack = gb_read8(wSelectedAttack_ADDR);
	if (attack == 0u)
		goto second_attack;
	return (AITryToPlayEnergyCardResult){attack, 0x00u};
}
/* <<< factory AITryToPlayEnergyCard */
/* >>> factory DetermineAIScoreOfAttackEnergyRequirement */
/* energy.asm .asm_166cd: the surplus-energy verdict came back "play more",
 * and an ATTACHED_ENERGY_BOOST attack that one more energy would turn into a
 * knockout is worth a lot more. */
static void encourage_energy_boost_knockout(void)
{
	(void)AIEncourage(2u);
	if ((CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | ATTACHED_ENERGY_BOOST_F).f & 0x10u) == 0u)
		return;
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = gb_read8(wDamage_ADDR);
	if (hp <= damage)
		return;
	uint8_t boosted = (uint8_t)(damage + 10u);
	if (hp > boosted)
		return;
	(void)AIEncourage(20u);
	if (hTempPlayAreaLocation_ff9d == 0u)
		(void)AIEncourage(10u);
}

void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)
{
	wSelectedAttack = a;
	CheckEnergyNeededForAttackResult energy = CheckEnergyNeededForAttack();
	if (energy.f & 0x10u) {
		if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F).f & 0x10u)
			AIDiscourage(5u);
		uint8_t color_in_hand = energy.b != 0u
			&& (LookForCardIDInHand(energy.e).f & 0x10u) == 0u;
		if (color_in_hand) {
			(void)AIEncourage(4u);
		} else {
			if (energy.c == 0u)
				goto check_evolution;
			(void)AIEncourage(3u);
		}
		if ((uint8_t)(energy.b + energy.c - 1u) != 0u)
			goto check_evolution;
		(void)AIEncourage(3u);
		(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
		if (GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a > gb_read8(wDamage_ADDR))
			goto check_evolution;
		(void)AIEncourage(20u);
		if (hTempPlayAreaLocation_ff9d != 0u)
			goto check_evolution;
		(void)AIEncourage(10u);
	} else if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | ATTACHED_ENERGY_BOOST_F).f & 0x10u) {
		uint8_t param = wLoadedAttackEffectParam;
		if (param != MAX_ENERGY_BOOST_IS_LIMITED) {
			(void)AIEncourage(param);
		} else {
			CheckIfNoSurplusEnergyResult surplus = CheckIfNoSurplusEnergyForAttack();
			if ((surplus.f & 0x10u) != 0u || surplus.a < 3u)
				encourage_energy_boost_knockout();
			else
				AIDiscourage(5u);
		}
	} else if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | DISCARD_ENERGY_F).f & 0x10u) {
		if (card_id_read_at(wLoadedCard1ID_ADDR) != ZAPDOS_LV64) {
			if (CheckIfNoSurplusEnergyForAttack().f & 0x10u)
				encourage_energy_boost_knockout();
			else
				AIDiscourage(5u);
		}
	}

check_evolution:
	{
		uint8_t evolution = wTempAI;
		if (evolution == 0xFFu)
			return;
		uint8_t location = hTempPlayAreaLocation_ff9d;
		DuelistVarResult slot = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
		uint8_t original = slot.a;
		gb_write8(slot.hl, evolution);
		CheckEnergyNeededForAttackResult evo_energy = CheckEnergyNeededForAttack();
		if ((evo_energy.f & 0x10u) != 0u
		    && (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F).f & 0x10u) == 0u) {
			if (evo_energy.b != 0u && (LookForCardIDInHand(evo_energy.e).f & 0x10u) == 0u)
				(void)AIEncourage(2u);
			else if (evo_energy.c != 0u)
				(void)AIEncourage(1u);
		}
		gb_write8(slot.hl, original);
	}
}
/* <<< factory DetermineAIScoreOfAttackEnergyRequirement */
/* >>> factory AIProcessEnergyCards */
AIEnergyResult AIProcessEnergyCards(void)
{
	for (uint8_t i = 0; i < MAX_PLAY_AREA_POKEMON; ++i)
		gb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + i), 0x80u);
	HandleLegendaryArticunoEnergyScoring();
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (uint8_t loc = 0; count != 0u; ++loc, --count) {
		hTempPlayAreaLocation_ff9d = loc;
		wAIScore = 0x80u;
		wTempAI = 0xFFu;
		if ((wAIEnergyAttachLogicFlags & AI_ENERGY_FLAG_SKIP_EVOLUTION) == 0u) {
			(void)CreateHandCardList(0u);
			wCurCardCanAttack = GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD)).a;
			EnergyFlagsResult need =
				CheckEnergyFlagsNeededInList(GetAttacksEnergyCostBits(wCurCardCanAttack).a);
			/* energy.asm:149: a card whose energy is not in hand keeps the
			 * neutral score; nothing below is evaluated for it. */
			if (!need.carry)
				goto store_score;
			CheckForEvolutionInListResult in_hand = CheckForEvolutionInList(wCurCardCanAttack, 0u, 0u, 0u);
			if (in_hand.f & 0x10u) {
				wTempAI = in_hand.a;
				(void)AIEncourage(2u);
			} else if (CheckForEvolutionInDeck(wCurCardCanAttack, 0u).f & 0x10u) {
				(void)AIEncourage(1u);
			}
		}
		/* .check_venusaur */
		if ((CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) == 0u
		    && (CountTurnDuelistPokemonWithActivePkmnPower(VENUSAUR_LV67).f & 0x10u) != 0u)
			(void)AIEncourage(1u);
		if (loc == 0u) {
			/* .check_bench is reached when poison will KO the arena card
			 * or the defending Pokemon can. */
			uint8_t threatened;
			if (wAIBarrierFlagCounter & (1u << AI_MEWTWO_MILL_F)) {
				AIDiscourage(5u);
				threatened = 0u;
			} else {
				(void)AIEncourage(4u);
				uint8_t hp = ConvertHPToDamageCounters_Bank5(
					GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a).a;
				threatened = hp < 3u
					&& (GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a
					    & (hp == 2u ? DOUBLE_POISONED : POISONED)) != 0u;
			}
			if (!threatened)
				threatened = (CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) != 0u;
			if (threatened) {
				AIDiscourage(10u);
				if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a == 1u)
					(void)AIEncourage(6u);
			}
		} else {
			uint8_t hp = ConvertHPToDamageCounters_Bank5(
				GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD_HP)).a).a;
			if (hp < 3u)
				AIDiscourage((uint8_t)(3u - hp));
		}
		/* .ai_score_bonus: the deck's (card ID, energy target, score) list. */
		if (gb_read8(wAICardListEnergyBonus_ADDR + 1u) != 0u) {
			uint16_t list = (uint16_t)(gb_read8(wAICardListEnergyBonus_ADDR)
					| (gb_read8(wAICardListEnergyBonus_ADDR + 1u) << 8));
			CardId id = GetCardIDFromDeckIndex(GetTurnDuelistVariable(
				(uint8_t)(loc + DUELVARS_ARENA_CARD)).a);
			for (;;) {
				CardId entry = card_id_read(&list);
				if (entry == 0u)
					break;
				if (entry != id) {
					list = (uint16_t)(list + 2u);
					continue;
				}
				uint8_t target = gb_read8(list++);
				(void)GetPlayAreaCardAttachedEnergies(loc);
				if (wTotalAttachedEnergies >= target) {
					/* energy.asm:242: `jr .store_score`, skipping the
					 * rest of the scoring (the asm's own noted bug). */
					AIDiscourage(10u);
					goto store_score;
				}
				uint8_t score = gb_read8(list);
				if (score >= 0x80u)
					(void)AIEncourage((uint8_t)(score - 0x80u));
				else
					AIDiscourage((uint8_t)(0x80u - score));
				break;
			}
		}
		/* .check_boss_deck */
		if (CheckIfNotABossDeckID().carry == 0u) {
			(void)HandleAIEnergyScoringForRepeatedBenchPokemon();
			uint8_t v = gb_read8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + loc));
			if (v >= 0x80u)
				(void)AIEncourage((uint8_t)(v - 0x80u));
			else
				AIDiscourage((uint8_t)(0x80u - v));
		}
		(void)AIEncourage(1u);
		DetermineAIScoreOfAttackEnergyRequirement(FIRST_ATTACK_OR_PKMN_POWER_600);
		DetermineAIScoreOfAttackEnergyRequirement(SECOND_ATTACK_600);
	store_score:
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + loc), wAIScore);
	}
	/* energy.asm:265-285. RetrievePlayAreaAIScoreFromBackup1 is push af ...
	 * pop af (:71-85), so the carry each tail jump carries is this routine's:
	 * `scf` when a card was found under logic flags, clear otherwise, and
	 * AITryToPlayEnergyCard's own carry on the no-flags path -- which its
	 * 1/0 return already is, set only on `.play_energy_card` (:138-145). */
	AIScoreResult best = FindPlayAreaCardWithHighestAIScore(0, 0, 0, 0, 0);

	uint8_t logic = wAIEnergyAttachLogicFlags;

	if ((best.f & 0x10u) != 0u) {
		if (logic != 0u) {
			(void)RetrievePlayAreaAIScoreFromBackup1();
			return (AIEnergyResult){logic, 0x10u};
		}
		(void)CreateEnergyCardListFromHand(best.a);
		AITryToPlayEnergyCardResult played = AITryToPlayEnergyCard();

		return (AIEnergyResult){played.a, played.f};
	}
	if (logic != 0u)
		(void)RetrievePlayAreaAIScoreFromBackup1();
	return (AIEnergyResult){logic, 0x00u};
}
/* <<< factory AIProcessEnergyCards */
/* >>> factory AIProcessAndTryToPlayEnergy */
AIEnergyResult AIProcessAndTryToPlayEnergy(void)
{
	wAIEnergyAttachLogicFlags = 0u;
	CoreCardListResult list = CreateEnergyCardListFromHand(0u);
	if ((list.f & 0x10u) == 0u)
		return AIProcessEnergyCards();
	if (wAIEnergyAttachLogicFlags != 0u) {
		(void)RetrievePlayAreaAIScoreFromBackup1();
		return (AIEnergyResult){wAIEnergyAttachLogicFlags, 0u};
	}
	return (AIEnergyResult){0u, 0x80u};
}
/* <<< factory AIProcessAndTryToPlayEnergy */
/* --- factory Func_16488 */
