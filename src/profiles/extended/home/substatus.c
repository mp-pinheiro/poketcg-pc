/* --- part includes_2 */
/* >>> factory CountTurnDuelistPokemonWithActivePkmnPower */
/* substatus.asm:544-590. Counts arena (if not status-incapable) plus bench
 * slots matching the target id. The bench walk ends at its $FF terminator. */
PkmnPowerCountResult CountTurnDuelistPokemonWithActivePkmnPower(CardId target)
{
	uint16_t target_addr = wTempPokemonID_ADDR;
	card_id_write(&target_addr, target);
	uint8_t count = 0;
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	if (arena != 0xFF) {
		CardId arena_id = GetCardIDFromDeckIndex(arena);
		if (arena_id == card_id_read_at(wTempPokemonID_ADDR)) {
			uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
			if (!(status & CNF_SLP_PRZ))
				count++;
		}
	}
	uint16_t bench = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
	while (gb_read8(bench) != 0xFF) {
		CardId slot_id = GetCardIDFromDeckIndex(gb_read8(bench));
		if (slot_id == card_id_read_at(wTempPokemonID_ADDR))
			count++;
		bench++;
	}
	return (PkmnPowerCountResult){count, count ? 0x10u : 0x80u, target};
}
/* <<< factory CountTurnDuelistPokemonWithActivePkmnPower */
/* >>> factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
PkmnPowerCountResult CountPokemonWithActivePkmnPowerInBothPlayAreas(CardId target)
{
	PkmnPowerCountResult turn = CountTurnDuelistPokemonWithActivePkmnPower(target);
	SwapTurn();
	PkmnPowerCountResult other = CountTurnDuelistPokemonWithActivePkmnPower(target);
	SwapTurn();
	uint8_t count = (uint8_t)(turn.a + other.a);
	return (PkmnPowerCountResult){count, count ? 0x10u : 0x80u, target};
}
/* <<< factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
/* --- part buggy_halve_damage */
/* === part reduce_by */
/* >>> part cphl_value */
static uint8_t cphl_value(CardId id, CardId value)
{
	uint8_t result = (uint8_t)(id >> 8);
	if ((uint8_t)(id >> 8) == (uint8_t)(value >> 8))
		result = (uint8_t)id;
	return result;
}
/* <<< part cphl_value */
/* >>> part f_cp16 */
static uint8_t f_cp16(CardId id, CardId value)
{
	return CompareDEtoBC((uint8_t)(id >> 8), (uint8_t)id,
		(uint8_t)(value >> 8), (uint8_t)value);
}
/* <<< part f_cp16 */
/* >>> part halve_damage */
static uint16_t halve_damage(uint16_t de)
{
	uint8_t d = (uint8_t)(de >> 8);
	uint8_t e = (uint8_t)de;
	uint8_t sra_carry = (uint8_t)(d & 1u);
	d = (uint8_t)((d >> 1) | (d & 0x80u));
	e = (uint8_t)((sra_carry << 7) | (e >> 1));
	de = (uint16_t)((uint16_t)d << 8 | e);
	if (!(e & 1u))
		return de;
	return reduce_by(de, 5);
}
/* <<< part halve_damage */
/* >>> factory HandleDamageReductionExceptSubstatus2 */
uint16_t HandleDamageReductionExceptSubstatus2(uint16_t de)
{
	if (gb_read8(wNoDamageOrEffect_ADDR) != 0)
		return 0;

	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	if (sub1.a != 0) {
		if (sub1.a == SUBSTATUS1_NO_DAMAGE_STIFFEN || sub1.a == SUBSTATUS1_NO_DAMAGE_WITHDRAW ||
		    sub1.a == SUBSTATUS1_NO_DAMAGE_HIDE_IN_SHELL || sub1.a == SUBSTATUS1_NO_DAMAGE_SCRUNCH)
			return 0;
		if (sub1.a == SUBSTATUS1_REDUCE_BY_10)
			return reduce_by(de, 10);
		if (sub1.a == SUBSTATUS1_REDUCE_BY_20)
			return reduce_by(de, 20);
		if (sub1.a == SUBSTATUS1_PREVENT_LESS_THAN_40) {
			if (CompareDEtoBC((uint8_t)(de >> 8), (uint8_t)de, 0, 40) & 0x10u)
				return 0;
			return de;
		}
		if (sub1.a == SUBSTATUS1_HALVE_DAMAGE)
			return halve_damage(de);
	}

	if (CheckIsIncapableOfUsingPkmnPower_ArenaCard().f & 0x10u)
		return de;
	return HandleDamageReductionExceptSubstatus2_PkmnPower(de);
}
/* <<< factory HandleDamageReductionExceptSubstatus2 */
/* >>> part HandleDamageReductionExceptSubstatus2_PkmnPower */
uint16_t HandleDamageReductionExceptSubstatus2_PkmnPower(uint16_t de)
{
	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER)
		return de;
	CardId defender = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	if (defender == MR_MIME) {
		if (CompareDEtoBC((uint8_t)(de >> 8), (uint8_t)de, 0, 30) & 0x10u)
			return de;
		return 0;
	}
	if (defender == KABUTO)
		return halve_damage(de);
	return de;
}
/* <<< part HandleDamageReductionExceptSubstatus2_PkmnPower */
/* >>> factory HandleNoDamageOrEffectSubstatus */
NoDamageOrEffectResult HandleNoDamageOrEffectSubstatus(uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wNoDamageOrEffect_ADDR, 0);
	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER)
		return (NoDamageOrEffectResult){0xC0u, d, e, hl};

	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);

	e = NO_DAMAGE_OR_EFFECT_FLY;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID;
	if (sub1.a == SUBSTATUS1_FLY) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, d, e, hl};
	}

	e = NO_DAMAGE_OR_EFFECT_BARRIER;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID;
	if (sub1.a == SUBSTATUS1_BARRIER) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, d, e, hl};
	}

	e = NO_DAMAGE_OR_EFFECT_AGILITY;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID;
	if (sub1.a == SUBSTATUS1_AGILITY) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, d, e, hl};
	}

	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	hl = incapable.hl;
	if (!(incapable.f & 0x10u))
		return HandleNoDamageOrEffectSubstatus_PkmnPower(d, e,
			wTempNonTurnDuelistCardID_ADDR);
	return (NoDamageOrEffectResult){0x00u, d, e, incapable.hl};
}
/* <<< factory HandleNoDamageOrEffectSubstatus */
/* >>> part HandleNoDamageOrEffectSubstatus_PkmnPower */
NoDamageOrEffectResult HandleNoDamageOrEffectSubstatus_PkmnPower(uint8_t d, uint8_t e, uint16_t hl)
{
	CardId defender = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	uint8_t a = cphl_value(defender, MEW_LV8);
	if (defender != MEW_LV8)
		return (NoDamageOrEffectResult){a ? 0x00u : 0x80u, d, e, hl};

	if (gb_read8(wIsDamageToSelf_ADDR) != 0)
		return (NoDamageOrEffectResult){0x00u, d, e, hl};

	CardId turn_id = card_id_read_at(wTempTurnDuelistCardID_ADDR);
	d = (uint8_t)(turn_id >> 8);
	e = (uint8_t)turn_id;
	LoadCardDataToBuffer2_FromCardID(turn_id);
	if (gb_read8(wLoadedCard2Stage_ADDR) == 0)
		return (NoDamageOrEffectResult){0x80u, d, e, hl};

	e = NO_DAMAGE_OR_EFFECT_NSHIELD;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID;
	gb_write8(wNoDamageOrEffect_ADDR, e);
	return (NoDamageOrEffectResult){0x10u, d, e, hl};
}
/* <<< part HandleNoDamageOrEffectSubstatus_PkmnPower */
/* >>> factory IsClairvoyanceActive */
PkmnPowerCountResult IsClairvoyanceActive(void)
{
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return (PkmnPowerCountResult){muk.a, 0x00u, muk.de};
	return CountTurnDuelistPokemonWithActivePkmnPower(OMANYTE);
}
/* <<< factory IsClairvoyanceActive */
/* === factory GetLoadedCard1RetreatCost */
/* >>> factory IsPrehistoricPowerActive */
PrehistoricPowerResult IsPrehistoricPowerActive(uint16_t hl)
{
	PkmnPowerCountResult aero = CountPokemonWithActivePkmnPowerInBothPlayAreas(AERODACTYL);
	if (!(aero.f & 0x10u))
		return (PrehistoricPowerResult){aero.a, aero.f, aero.de, hl};
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	uint8_t f = (muk.f & 0x10u) ? 0x00u : 0x90u;
	return (PrehistoricPowerResult){muk.a, f, muk.de, UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID};
}
/* <<< factory IsPrehistoricPowerActive */
/* >>> factory IsRainDanceActive */
PkmnPowerCountResult IsRainDanceActive(void)
{
	PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
	if (!(blastoise.f & 0x10u))
		return blastoise;
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	uint8_t f = (muk.f & 0x10u) ? 0x00u : 0x90u;
	return (PkmnPowerCountResult){muk.a, f, muk.de};
}
/* <<< factory IsRainDanceActive */
/* === factory ClearChangedTypesIfMuk */
/* >>> factory CheckRainDanceScenario */
RainDanceResult CheckRainDanceScenario(void)
{
	uint8_t card_idx = hTempCardIndex_ff98;
	uint16_t card_id = GetCardIDFromDeckIndex(card_idx);
	uint8_t card_type = GetCardType(card_id);
	if (card_type != TYPE_ENERGY_WATER)
		return (RainDanceResult){card_type, (uint8_t)(card_type == 0u ? 0x80u : 0u)};
	uint8_t color = GetPlayAreaCardColor(hTempPlayAreaLocation_ff9d);
	if (color != TYPE_PKMN_WATER)
		return (RainDanceResult){color, (uint8_t)(color == 0u ? 0x80u : 0u)};
	return (RainDanceResult){TYPE_PKMN_WATER, 0x90u};
}
/* <<< factory CheckRainDanceScenario */
/* --- part MACHAMP_ID */
/* --- part MUK_ID */
/* >>> factory HandleStrikesBack_AgainstDamagingAttack */
StrikesBackResult HandleStrikesBack_AgainstDamagingAttack(uint16_t de, uint16_t hl)
{
	uint8_t a;
	uint16_t entry_hl = hl;
	if (!de)
		return (StrikesBackResult){0u, 0x80u, 0u, 0u, entry_hl};
	a = wIsDamageToSelf;
	if (a)
		return (StrikesBackResult){a, f_or(a), (uint8_t)(de >> 8), (uint8_t)de, entry_hl};
	CardId defender = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	hl = wTempNonTurnDuelistCardID_ADDR;
	a = cphl_value(defender, MACHAMP);
	if (defender != MACHAMP)
		return (StrikesBackResult){a, f_cp16(defender, MACHAMP),
			(uint8_t)(de >> 8), (uint8_t)de, hl};
	PkmnPowerCountResult count = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (count.f & 0x10u)
		return (StrikesBackResult){count.a, count.f,
			(uint8_t)(count.de >> 8), (uint8_t)count.de, hl};
	a = wLoadedAttackCategory;
	if (a == 0x04u)
		return (StrikesBackResult){a, f_cp(a, 0x04u),
			(uint8_t)(count.de >> 8), (uint8_t)count.de, hl};
	if (!wTempPlayAreaLocation_cceb) {
		uint8_t inc_f = CheckIsIncapableOfUsingPkmnPower_ArenaCard().f;
		if (inc_f & 0x10u)
			return (StrikesBackResult){a, inc_f,
				(uint8_t)(count.de >> 8), (uint8_t)count.de, hl};
	}
	SwapTurn();
	uint8_t deck_idx = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	LoadCardDataToBuffer2_FromDeckIndex(deck_idx);
	DuelistVarResult hp_var = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t hp = hp_var.a;
	(void)SubtractHP(hp_var.hl, 10);
	uint16_t temp_non_turn_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_non_turn_id, card_id_read_at(wLoadedCard2ID_ADDR));
	LoadTxRam3(10);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard2Name_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DrawWideTextBox_WaitForInput(RECEIVES_DAMAGE_DUE_TO_STRIKES_BACK_TEXT);
	if (hp)
		PrintPlayAreaCardKnockedOutIfNoHP(0);
	SwapTurn();
	return (StrikesBackResult){0u, 0x10u,
		(uint8_t)(count.de >> 8), (uint8_t)count.de, hl};
}
/* <<< factory HandleStrikesBack_AgainstDamagingAttack */
/* >>> factory ApplyStrikesBack_AgainstResidualAttack */
ApplyStrikesBackResult ApplyStrikesBack_AgainstResidualAttack(uint16_t hl)
{
	LoadTxRam3(hl);
	CardId card_id = card_id_read_at(wTempTurnDuelistCardID_ADDR);
	LoadCardDataToBuffer2_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard2Name_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	(void)SubtractHP(hp.hl, hl);
	(void)DrawWideTextBox_PrintText(ReceivesDamageDueToStrikesBackText);
	if (hp.a == 0)
		return (ApplyStrikesBackResult){0, 0x80u};
	(void)WaitForWideTextBoxInput();
	(void)PrintPlayAreaCardKnockedOutIfNoHP(PLAY_AREA_ARENA);
	DrawDuelHUDs();
	return (ApplyStrikesBackResult){0, 0x10u};
}

/* <<< factory ApplyStrikesBack_AgainstResidualAttack */
/* >>> factory HandleStrikesBack_AgainstResidualAttack */
HandleStrikesBackResidualResult HandleStrikesBack_AgainstResidualAttack(void)
{
	CardId card_id = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	uint8_t a = cphl_value(card_id, MACHAMP);
	if (card_id != MACHAMP) {
		uint8_t f = f_cp16(card_id, MACHAMP);
		return (HandleStrikesBackResidualResult){a, f};
	}
	uint8_t category = wLoadedAttackCategory;
	uint8_t residual = (uint8_t)(category & RESIDUAL);
	if (residual)
		return (HandleStrikesBackResidualResult){residual, 0x20u};
	uint8_t damage = wDealtDamage;
	if (!damage)
		return (HandleStrikesBackResidualResult){0x00u, 0x80u};
	SwapTurn();
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	SwapTurn();
	if (incapable.f & 0x10u)
		return (HandleStrikesBackResidualResult){0x00u, incapable.f};
	ApplyStrikesBackResult applied = ApplyStrikesBack_AgainstResidualAttack(10u);
	if (!(applied.f & 0x10u)) {
		WaitResult waited = WaitForWideTextBoxInput();
		return (HandleStrikesBackResidualResult){applied.a, waited.f};
	}
	return (HandleStrikesBackResidualResult){applied.a, applied.f};
}
/* <<< factory HandleStrikesBack_AgainstResidualAttack */
/* >>> factory HandleNShieldAndTransparency */
HandleNShieldAndTransparencyResult HandleNShieldAndTransparency(uint16_t de)
{
	uint8_t e = (uint8_t)de;
	DuelistVarResult arena = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e));
	CardId card_id = GetCardIDFromDeckIndex(arena.a);
	if (card_id == MEW_LV8) {
		DuelistVarResult stage = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STAGE);
		if (stage.a != 0u) {
			gb_write8(wNoDamageOrEffect_ADDR, NO_DAMAGE_OR_EFFECT_NSHIELD);
			(void)DrawWideTextBox_WaitForInput(NoDamageOrEffectDueToNShieldText);
			return (HandleNShieldAndTransparencyResult){0u, 0x90u, (uint8_t)(de >> 8), e,
				NoDamageOrEffectDueToNShieldText};
		}
		return (HandleNShieldAndTransparencyResult){stage.a, stage.a ? 0u : 0x80u,
			(uint8_t)(de >> 8), e, stage.hl};
	}
	if (card_id == HAUNTER_LV17) {
		wDuelDisplayedScreen = 0u;
		TossCoinRoutineResult toss = TossCoin(TransparencyCheckText, arena.hl);
		if (toss.f & 0x10u) {
			gb_write8(wNoDamageOrEffect_ADDR, NO_DAMAGE_OR_EFFECT_TRANSPARENCY);
			(void)DrawWideTextBox_WaitForInput(NoDamageOrEffectDueToTransparencyText);
			return (HandleNShieldAndTransparencyResult){0u, 0x90u, (uint8_t)(de >> 8), e,
				NoDamageOrEffectDueToTransparencyText};
		}
		return (HandleNShieldAndTransparencyResult){toss.a, toss.a ? 0u : 0x80u,
			(uint8_t)(de >> 8), e, toss.hl};
	}
	uint8_t compare_a = (uint8_t)(card_id >> 8);
	if (compare_a == (uint8_t)(MEW_LV8 >> 8))
		compare_a = (uint8_t)card_id;
	return (HandleNShieldAndTransparencyResult){compare_a, compare_a ? 0u : 0x80u,
		(uint8_t)(de >> 8), e, arena.hl};
}
/* <<< factory HandleNShieldAndTransparency */
/* >>> factory HandleTransparency */
HandleTransparencyResult HandleTransparency(uint16_t hl)
{
	CardId card = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	uint8_t a = cphl_value(card, HAUNTER_LV17);
	if (card != HAUNTER_LV17)
		return (HandleTransparencyResult){a, a ? 0u : 0x80u,
			wTempNonTurnDuelistCardID_ADDR};

	uint8_t category = wLoadedAttackCategory;
	if (category == POKEMON_POWER) {
		return (HandleTransparencyResult){category, category ? 0u : 0x80u,
			wTempNonTurnDuelistCardID_ADDR};
	}

	uint8_t location = wTempPlayAreaLocation_cceb;
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	if (incapable.f & 0x10u)
		return (HandleTransparencyResult){location, location ? 0u : 0x80u, incapable.hl};

	wDuelDisplayedScreen = 0u;
	TossCoinRoutineResult toss = TossCoin(TransparencyCheckText, hl);
	if (!(toss.f & 0x10u))
		return (HandleTransparencyResult){toss.a, toss.f, toss.hl};

	wNoDamageOrEffect = NO_DAMAGE_OR_EFFECT_TRANSPARENCY;
	return (HandleTransparencyResult){NO_DAMAGE_OR_EFFECT_TRANSPARENCY, 0x10u, NoDamageOrEffectDueToTransparencyText};
}
/* <<< factory HandleTransparency */
/* >>> factory HandleDamageReductionOrNoDamageFromPkmnPowerEffects */
HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult HandleDamageReductionOrNoDamageFromPkmnPowerEffects(uint16_t de, uint16_t hl)
{
	uint8_t category = wLoadedAttackCategory;
	if (category == POKEMON_POWER)
		return (HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult){0xC0u, de, hl};

	PkmnPowerCountResult powers = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (powers.f & 0x10u)
		return (HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult){powers.f, de, hl};

	uint8_t location = wTempPlayAreaLocation_cceb;
	if (location != 0)
		de = HandleDamageReductionExceptSubstatus2_PkmnPower(de);

	uint16_t damage = de;
	NoDamageOrEffectResult no_damage = HandleNoDamageOrEffectSubstatus_PkmnPower((uint8_t)(de >> 8), location, hl);
	if (card_id_read_at(wTempNonTurnDuelistCardID_ADDR) != MEW_LV8) {
		no_damage.f = location == 0u ? 0x80u : 0x00u;
		no_damage.hl = wTempNonTurnDuelistCardID_ADDR;
	}
	uint8_t f = no_damage.f;
	hl = no_damage.hl;
	if (!(f & 0x10u)) {
		if (card_id_read_at(wTempNonTurnDuelistCardID_ADDR) == HAUNTER_LV17) {
			HandleTransparencyResult transparency = HandleTransparency(hl);
			f = transparency.f;
			hl = transparency.hl;
			if (f & 0x10u)
				damage = 0;
		}
	} else {
		damage = 0;
	}
	return (HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult){f, damage, hl};
}
/* <<< factory HandleDamageReductionOrNoDamageFromPkmnPowerEffects */
/* === factory CheckIsIncapableOfUsingPkmnPower */
