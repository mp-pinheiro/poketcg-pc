/* >>> factory GetAIScoreOfAttack */
/* attacks.asm .check_if_kos_bench: how many of the turn holder's benched
 * Pokemon `bench_damage` knocks out, plus `initial`, reaches the prize count
 * the other duelist still needs. Returns carry as the asm does, and the count
 * in d so .count_own_ko_bench can subtract it. */
typedef struct {
	uint8_t d;
	uint8_t carry;
} BenchKnockouts;

static BenchKnockouts check_if_kos_bench(uint8_t initial, uint8_t bench_damage)
{
	uint8_t d = initial;
	uint16_t hl = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
	for (uint8_t e = PLAY_AREA_ARENA + 1u;; e++) {
		if (gb_read8(hl++) == 0xFFu)
			break;
		uint8_t hp = GetTurnDuelistVariable((uint8_t)(e + DUELVARS_ARENA_CARD_HP)).a;
		if (hp <= bench_damage)
			d++;
	}
	SwapTurn();
	uint8_t prizes = CountPrizes();
	SwapTurn();
	return (BenchKnockouts){d, prizes <= d};
}

void GetAIScoreOfAttack(uint8_t a)
{
	wSelectedAttack = a;
	wAIScore = 0x50u;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) {
	unusable:
		wAIScore = 0u;
		return;
	}
	CardId turn_card_id = GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	uint16_t temp_turn_id = wTempTurnDuelistCardID_ADDR;
	card_id_write(&temp_turn_id, turn_card_id);
	SwapTurn();
	CardId non_turn_card_id = GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	uint16_t temp_non_turn_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_non_turn_id, non_turn_card_id);
	NoDamageOrEffectResult no_damage = HandleNoDamageOrEffectSubstatus(0u, 0u, 0u);
	SwapTurn();
	if (no_damage.f & 0x10u) {
		wAICannotDamage = 1u;
		(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
		uint8_t category = wLoadedAttackCategory;
		if (category == POKEMON_POWER)
			goto unusable;
		if ((category & RESIDUAL) == 0u
		    && (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | DAMAGE_TO_OPPONENT_BENCH_F).f & 0x10u) == 0u)
			goto unusable;
	}
	/* .check_if_can_ko */
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	if (GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a <= wDamage)
		(void)AIEncourage(20u);
	/* .check_damage */
	wAIAttackIsNonDamaging = 0u;
	uint8_t damage = wDamage;
	wTempAI = damage;
	if (damage != 0u) {
		(void)AIEncourage(ConvertHPToDamageCounters_Bank5(damage).a);
	} else {
		wAIAttackIsNonDamaging = 1u;
		AIDiscourage(1u);
		if (wAIMaxDamage != 0u) {
			(void)AIEncourage(2u);
			wAIAttackIsNonDamaging = 0u;
		}
		if (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | DAMAGE_TO_OPPONENT_BENCH_F).f & 0x10u)
			(void)AIEncourage(2u);
	}
	/* .check_recoil */
	if ((CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | LOW_RECOIL_F).f & 0x10u) != 0u
	    || (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | HIGH_RECOIL_F).f & 0x10u) != 0u) {
		uint8_t recoil = wLoadedAttackEffectParam;
		if (recoil == 0u)
			goto check_defending_can_ko;
		wDamage = recoil;
		uint8_t self_damage = (uint8_t)ApplyDamageModifiers_DamageToSelf();
		AIDiscourage(ConvertHPToDamageCounters_Bank5(self_damage).a);
		if ((CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | HIGH_RECOIL_F).f & 0x10u) == 0u) {
			/* LOW_RECOIL: only its self knockout matters. */
			if (GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a > self_damage)
				goto check_defending_can_ko;
			AIDiscourage(10u);
		}
		/* .high_recoil */
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a < 2u)
			goto dismiss_high_recoil_atk;
		uint8_t deck = wOpponentDeckID;
		if (deck == ROCK_CRUSHER_DECK_ID) {
			if (CountPrizes() >= 4u)
				goto dismiss_high_recoil_atk;
			SwapTurn();
			BenchKnockouts kos = check_if_kos_bench(0u, 20u);
			SwapTurn();
			if (kos.carry)
				goto encourage_high_recoil_atk;
			goto high_recoil_generic_checks;
		}
		if (deck == ZAPPING_SELFDESTRUCT_DECK_ID) {
			if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a >= 31u)
				goto high_recoil_generic_checks;
			CardDamageResult arena = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
			if ((uint8_t)(arena.a << 1) < arena.c)
				goto high_recoil_generic_checks;
			uint8_t bench_damage = 10u;
			if (GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a) != MAGNEMITE_LV13)
				bench_damage = 20u;
			if (check_if_kos_bench(1u, bench_damage).carry)
				goto dismiss_high_recoil_atk;
			goto encourage_high_recoil_atk;
		}
		if (deck == BOOM_BOOM_SELFDESTRUCT_DECK_ID)
			goto encourage_high_recoil_atk;
		if (deck == POWER_GENERATOR_DECK_ID) {
		dismiss_high_recoil_atk:
			wAIScore = 0u;
			return;
		}
	high_recoil_generic_checks:
		{
			CardId id = GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
			uint8_t bench_damage = 20u;
			if (id == CHANSEY)
				bench_damage = 0u;
			else if (id == MAGNEMITE_LV13 || id == WEEZING)
				bench_damage = 10u;
			SwapTurn();
			BenchKnockouts player = check_if_kos_bench(0u, bench_damage);
			SwapTurn();
			if (player.carry) {
			encourage_high_recoil_atk:
				(void)AIEncourage(20u);
				return;
			}
			BenchKnockouts own = check_if_kos_bench(1u, bench_damage);
			if (own.carry) {
				wAIScore = 0u;
				return;
			}
			/* .count_own_ko_bench: d counts the active card too. */
			if (own.d != 0u)
				AIDiscourage((uint8_t)(own.d - 1u));
			(void)AIEncourage(player.d);
		}
	}
check_defending_can_ko:
	{
		uint8_t attack = wSelectedAttack;
		uint8_t can_ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u;
		wSelectedAttack = attack;
		if (can_ko) {
			(void)AIEncourage(5u);
			if (wAIAttackIsNonDamaging != 0u)
				AIDiscourage(5u);
		}
	}
	/* .check_discard */
	(void)CopyAttackDataAndDamage_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a, wSelectedAttack);
	if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | DISCARD_ENERGY_F).f & 0x10u) {
		AIDiscourage(1u);
		AIDiscourage(wLoadedAttackEffectParam);
	}
	if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | ENCOURAGE_THIS_ATTACK_F).f & 0x10u)
		(void)AIEncourage(wLoadedAttackEffectParam);
	if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | NULLIFY_OR_WEAKEN_ATTACK_F).f & 0x10u)
		(void)AIEncourage(1u);
	if (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | DRAW_CARD_F).f & 0x10u)
		(void)AIEncourage(1u);
	if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | HEAL_USER_F).f & 0x10u) {
		uint8_t heal;
		if (wLoadedAttackEffectParam == HEALING_EQUALS_10_HP) {
			heal = HEALING_EQUALS_10_HP;
		} else {
			uint8_t counters = ConvertHPToDamageCounters_Bank5(wTempAI).a;
			if (wLoadedAttackEffectParam != HEALING_EQUALS_DAMAGE_DEALT)
				counters = (uint8_t)((counters >> 1) + (counters & 1u));
			heal = ConvertHPToDamageCounters_Bank5(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a).a;
			if (heal >= counters)
				heal = counters;
		}
		/* .tally_heal_score: never more than the damage there is to heal. */
		uint8_t taken = ConvertHPToDamageCounters_Bank5(GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a).a;
		if (taken >= heal)
			taken = heal;
		(void)AIEncourage(taken);
	}
	/* .check_status_effect */
	{
		uint8_t defender = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		SwapTurn();
		CardId defender_id = GetCardIDFromDeckIndex(defender);
		SwapTurn();
		if (defender_id == SNORLAX)
			goto handle_special_atks;
	}
	{
		uint8_t status = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
		wTempAI = status;
		if (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | INFLICT_POISON_F).f & 0x10u) {
			if ((status & DOUBLE_POISONED) == 0u)
				(void)AIEncourage(2u);
			else if ((status & 0x40u) != 0u
				 && (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | ENCOURAGE_THIS_ATTACK_F).f & 0x10u) != 0u)
				AIDiscourage(2u);
		}
		if (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | INFLICT_SLEEP_F).f & 0x10u) {
			if ((status & CNF_SLP_PRZ) != ASLEEP)
				(void)AIEncourage(1u);
		}
		if (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | INFLICT_PARALYSIS_F).f & 0x10u) {
			if ((status & CNF_SLP_PRZ) == ASLEEP)
				AIDiscourage(1u);
			else
				(void)AIEncourage(1u);
		}
		if (CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | INFLICT_CONFUSION_F).f & 0x10u) {
			if ((status & CNF_SLP_PRZ) == ASLEEP)
				AIDiscourage(1u);
			else if ((status & CNF_SLP_PRZ) != CONFUSED)
				(void)AIEncourage(1u);
		}
		if ((GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ) == CONFUSED)
			AIDiscourage(1u);
	}
handle_special_atks:
	if (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | SPECIAL_AI_HANDLING_F).f & 0x10u) {
		uint8_t score = HandleSpecialAIAttacks().a;
		if (score >= 0x80u)
			(void)AIEncourage((uint8_t)(score - 0x80u));
		else
			AIDiscourage((uint8_t)(0x80u - score));
	}
}
/* <<< factory GetAIScoreOfAttack */
/* === factory AIProcessAttacks */
