/* === part DUELVARS_ARENA_CARD */
/* >>> part DUELVARS_ARENA_CARD_FLAGS */
#define DUELVARS_ARENA_CARD_FLAGS          0xc2u
/* <<< part DUELVARS_ARENA_CARD_FLAGS */
/* >>> part check_turn_duelist_has_color */
/* pkmn_powers.asm:618-729 (.CheckWhetherTurnDuelistHasColor). Returns 1 with
 * carry set if the turn duelist has a card in play whose color matches the
 * weakness WR mask in b: walks the play area slots starting at the arena card
 * variable until an $ff terminator. push bc around the card lookups keeps b
 * alive across the calls. Exit flags: 0x30 on a hit (and b sets H, scf sets C),
 * 0x00 on the terminator (or a with a = $ff). */
static uint8_t check_turn_duelist_has_color(uint8_t b, uint8_t *f)
{
	uint16_t hl = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).hl;
	uint8_t c = PLAY_AREA_ARENA;
	for (;;) {
		uint8_t idx = gb_read8(hl++);
		if (idx == 0xffu) {
			*f = 0x00u;
			return 0xffu;
		}
		uint8_t wr = TranslateColorToWR(GetPlayAreaCardColor(c));
		uint8_t overlap = (uint8_t)(wr & b);
		if (overlap != 0u) {
			*f = 0x30u;
			return overlap;
		}
		c++;
	}
}
/* <<< part check_turn_duelist_has_color */
/* >>> part OPPACTION_DUEL_MAIN_SCENE_269 */
#define OPPACTION_DUEL_MAIN_SCENE_269 OPPACTION_DUEL_MAIN_SCENE
/* <<< part OPPACTION_DUEL_MAIN_SCENE_269 */
/* >>> factory HandleAIShift */
/* pkmn_powers.asm:618-729. AI handler for Venomoth's Shift power. c is the
 * Play Area location of Venomoth (0 = Arena card); any nonzero location
 * returns immediately. The c==0 path stores the defending Pokemon's weakness
 * to wAIDefendingPokemonWeakness and, when a usable color exists, runs the
 * OPPACTION_USE_PKMN_POWER / _EXECUTE_PKMN_POWER_EFFECT / _DUEL_MAIN_SCENE
 * sequence through AIMakeDecision. Produces a/f at every exit; b, c, d, e, hl
 * are preserved on the early paths. */
AIShiftResult HandleAIShift(uint8_t c)
{
	if (c != 0u) /* ld a,c ; or a ; ret nz */
		return (AIShiftResult){c, 0x00u};

	hTemp_ffa0 = 0u;
	uint8_t wr = TranslateColorToWR(GetArenaCardColor());
	SwapTurn();
	uint8_t weakness = GetArenaCardWeakness();
	wAIDefendingPokemonWeakness = weakness;
	SwapTurn();
	if (weakness == 0u) /* or a ; ret z */
		return (AIShiftResult){weakness, 0x80u};
	uint8_t overlap = (uint8_t)(weakness & wr);
	if (overlap != 0u) /* and b ; ret nz (and always sets H) */
		return (AIShiftResult){overlap, 0x20u};
	uint8_t f = 0u;
	uint8_t found = check_turn_duelist_has_color(weakness, &f);
	if (!(f & 0x10u)) {
		SwapTurn();
		found = check_turn_duelist_has_color(weakness, &f);
		SwapTurn();
		if (!(f & 0x10u))
			return (AIShiftResult){found, f};
	}
	/* .found: dispatch the Shift Pkmn Power sequence */
	hTempCardIndex_ff9f = gb_read8(WCE08_ADDR);
	(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER, 0u, 0u, 0u, 0u);

	/* converts WR_* back to a color index: rotate left until bit 7 is set */
	uint8_t color = 0u;
	uint8_t rot = wAIDefendingPokemonWeakness;
	while (!(rot & 0x80u)) {
		color = (uint8_t)(color + 1u);
		rot = (uint8_t)((rot << 1u) | (rot >> 7u));
	}

	hAIPkmnPowerEffectParam = color;
	(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT, 0u, 0u, 0u, 0u);
	AIMakeDecisionResult r = AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE, 0u, 0u, 0u, 0u);
	return (AIShiftResult){OPPACTION_DUEL_MAIN_SCENE, r.f};
}
/* <<< factory HandleAIShift */
/* >>> factory HandleAIDamageSwap */
/* pkmn_powers.asm .CheckForDamageSwapTargetInBench. Looks through the bench for
 * a Chansey, Kangaskhan, Snorlax or Mr. Mime with at least 20 HP, preferring
 * one with no energy attached. Returns carry when there is none; otherwise a
 * is the target's play area location with Z clear. */
static HandleAIDamageSwapResult HandleAIDamageSwap_CheckForTargetInBench(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t with_energy = 0xffu;
	uint8_t without_energy = 0xffu;
	for (uint8_t location = PLAY_AREA_BENCH_1; location != count; location++) {
		uint8_t index = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD)).a;
		CardId id = GetCardIDFromDeckIndex(index);
		if (id != CHANSEY && id != KANGASKHAN && id != SNORLAX && id != MR_MIME)
			continue;
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + location)).a < 20u)
			continue;
		with_energy = location;
		if (CountNumberOfEnergyCardsAttached(location).a != 0u)
			continue;
		without_energy = location;
	}
	if (without_energy != 0xffu)
		return (HandleAIDamageSwapResult){without_energy, 0x00u};
	if (with_energy != 0xffu)
		return (HandleAIDamageSwapResult){with_energy, 0x00u};
	return (HandleAIDamageSwapResult){0xffu, 0x90u};
}

HandleAIDamageSwapResult HandleAIDamageSwap(uint8_t f)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t bench_count = (uint8_t)(count.a - 1u);
	if (bench_count == 0u)
		return (HandleAIDamageSwapResult){0u, (uint8_t)(0xc0u | (f & 0x10u))};

	AIChooseRandomlyNotToDoActionResult skip = AIChooseRandomlyNotToDoAction();
	if (skip.f & 0x10u)
		return (HandleAIDamageSwapResult){skip.a, skip.f};
	PkmnPowerCountResult alakazam = CountTurnDuelistPokemonWithActivePkmnPower(ALAKAZAM);
	if (!(alakazam.f & 0x10u))
		return (HandleAIDamageSwapResult){alakazam.a, alakazam.f};
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return (HandleAIDamageSwapResult){muk.a, muk.f};
	uint8_t arena_index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	CardId arena_id = GetCardIDFromDeckIndex(arena_index);
	if (arena_id != ALAKAZAM && arena_id != KADABRA && arena_id != ABRA && arena_id != MR_MIME) {
		uint8_t half_borrow = (uint8_t)((arena_id & 0x0fu) < (MR_MIME & 0x0fu));
		uint8_t borrow = (uint8_t)(arena_id < MR_MIME);
		return (HandleAIDamageSwapResult){(uint8_t)arena_id, (uint8_t)(0x40u | (half_borrow << 5) | (borrow << 4))};
	}
	CardDamageResult arena = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	if (arena.a == 0u)
		return (HandleAIDamageSwapResult){0u, 0x80u};
	gb_write8(WCE06_ADDR, ConvertHPToDamageCounters_Bank8(arena.a));
	LookResult alakazam_at = LookForCardIDInPlayArea_Bank5(ALAKAZAM, PLAY_AREA_BENCH_1);
	gb_write8(WCE08_ADDR, (alakazam_at.f & 0x10u) != 0u ? alakazam_at.a : PLAY_AREA_ARENA);
	HandleAIDamageSwapResult target = HandleAIDamageSwap_CheckForTargetInBench();
	if ((target.f & 0x10u) != 0u)
		return target;

	uint8_t alakazam_location = gb_read8(WCE08_ADDR);
	hTempCardIndex_ff9f = GetTurnDuelistVariable((uint8_t)(alakazam_location + DUELVARS_ARENA_CARD)).a;
	hTemp_ffa0 = alakazam_location;
	(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER, 0u, 0u, 0u, 0u);
	(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT, 0u, 0u, 0u, 0u);
	for (uint8_t counters = gb_read8(WCE06_ADDR); counters != 0u; counters--) {
		for (uint8_t delay = 30u; delay != 0u; delay--)
			DoFrame();
		target = HandleAIDamageSwap_CheckForTargetInBench();
		if ((target.f & 0x10u) != 0u)
			break;
		hTempRetreatCostCards = target.a;
		hAIPkmnPowerEffectParam = PLAY_AREA_ARENA;
		(void)AIMakeDecision(OPPACTION_6B15, 0u, 0u, 0u, 0u);
	}
	for (uint8_t delay = 60u; delay != 0u; delay--)
		DoFrame();
	AIMakeDecisionResult scene = AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE, 0u, 0u, 0u, 0u);
	return (HandleAIDamageSwapResult){scene.a, scene.f};
}
/* <<< factory HandleAIDamageSwap */
/* >>> factory HandleAIPkmnPowers */
HandleAIPkmnPowersResult HandleAIPkmnPowers(void)
{
	/* pkmn_powers.asm:413-420: `ccf / ret nc` keeps the callee's Z and clears
	 * N, H and the flipped carry. */
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return (HandleAIPkmnPowersResult){muk.a, (uint8_t)(muk.f & 0x80u)};

	AIChooseRandomlyNotToDoActionResult skip = AIChooseRandomlyNotToDoAction();
	if (skip.f & 0x10u)
		return (HandleAIPkmnPowersResult){skip.a, (uint8_t)(skip.f & 0x80u)};

	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	uint8_t c = PLAY_AREA_ARENA;
	if (status & CNF_SLP_PRZ)
		c++;
	while (c != count) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + c)).a;
		gb_write8(WCE08_ADDR, deck_index);
		hTempPlayAreaLocation_ff9d = c;
		AttackCopyResult copied = CopyAttackDataAndDamage_FromDeckIndex(deck_index, FIRST_ATTACK_OR_PKMN_POWER);
		(void)copied;
		if (wLoadedAttackCategory == POKEMON_POWER) {
			TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_2, 0u, 0u, 0u);
			if (!(effect.f & 0x10u)) {
				CardId card_id = GetCardIDFromDeckIndex(deck_index);
				if (card_id == VILEPLUME)
					(void)HandleAIHeal(c);
				else if (card_id == VENOMOTH)
					(void)HandleAIShift(c);
				else if (card_id == MANKEY)
					(void)HandleAIPeek(c);
				else if (card_id == SLOWBRO)
					(void)HandleAIStrangeBehavior(c, 0u, 0u, 0u);
				else if (card_id == GENGAR) {
					HandleAICurseResult curse = HandleAICurse(c);
					if (curse.f & 0x10u)
						return (HandleAIPkmnPowersResult){curse.a, curse.f};
				}
			}
		}
		c++;
	}
	return (HandleAIPkmnPowersResult){c, 0xC0u};
}
/* <<< factory HandleAIPkmnPowers */
/* >>> factory HandleAICowardice */
HandleAICowardiceResult HandleAICowardice(void)
{
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return (HandleAICowardiceResult){muk.a, muk.f};

	AIChooseRandomlyNotToDoActionResult skip = AIChooseRandomlyNotToDoAction();
	if (skip.f & 0x10u)
		return (HandleAICowardiceResult){skip.a, skip.f};

	DuelistVarResult count_result = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t count = count_result.a;
	uint8_t count_flags = (uint8_t)(0x40u | (count == 1u ? 0x80u : 0u) | (count < 1u ? 0x30u : 0u));
	if (count == 1u)
		return (HandleAICowardiceResult){count, count_flags};

	uint8_t b = count;
	uint8_t c = PLAY_AREA_ARENA;
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	if (status & CNF_SLP_PRZ)
		c++;
	/* pkmn_powers.asm:968-993: after a Tentacool uses Cowardice the scan
	 * restarts from the arena with one Pokemon fewer, and stops with `cp b`'s
	 * flags once only one is left; the plain end of the scan is `cp b`'s Z. */
	for (;;) {
		if (c == b)
			return (HandleAICowardiceResult){c, 0xC0u};
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + c)).a;
		wce08 = deck_index;
		CardId card_id = GetCardIDFromDeckIndex(deck_index);
		/* `cp TENTACOOL` then `jr nc, .next`: a card whose id is below
		 * Tentacool's leaves carry set and takes the "used Cowardice" path
		 * without using anything (the ROM's own bug, kept). */
		uint8_t used = card_id < TENTACOOL;
		if (card_id == TENTACOOL) {
			hTemp_ffa0 = c;
			uint8_t flags = GetTurnDuelistVariable(
				(uint8_t)(DUELVARS_ARENA_CARD_FLAGS + c)).a;
			if ((flags & CAN_EVOLVE_THIS_TURN) == 0u) {
				c++;
				continue;
			}
			CardDamageResult damage = GetCardDamageAndMaxHP(c);
			if (damage.a != 0u) {
				uint8_t effect_param;
				if (c != PLAY_AREA_ARENA) {
					effect_param = 0xffu;
				} else {
					AIDecideBenchPokemonToSwitchToResult retreat =
						AIDecideBenchPokemonToSwitchTo(0u);
					effect_param = retreat.a;
				}
				hTempCardIndex_ff9f = wce08;
				(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER, 0u, 0u, 0u, 0u);
				hAIPkmnPowerEffectParam = effect_param;
				(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT, 0u, 0u, 0u, 0u);
				(void)AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE, 0u, 0u, 0u, 0u);
				used = 1u;
			}
		}
		if (used) {
			b--;
			if (b == 1u)
				return (HandleAICowardiceResult){1u, 0xC0u};
			c = PLAY_AREA_ARENA;
			continue;
		}
		c++;
	}
}
/* <<< factory HandleAICowardice */
/* === factory AIEnergyTransTransferEnergyToBench */
/* === factory HandleAIEnergyTrans */
/* === factory HandleAIGoGoRainDanceEnergy */
