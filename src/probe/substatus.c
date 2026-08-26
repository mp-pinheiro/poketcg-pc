#include "home/substatus.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_CheckSandAttackOrSmokescreenSubstatus(ProbeState *s)
{
	SandAttackCheckResult r = CheckSandAttackOrSmokescreenSubstatus(pair(s->d, s->e));
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}

static void adapt_CountTurnDuelistPokemonWithActivePkmnPower(ProbeState *s)
{
	PkmnPowerCountResult r = CountTurnDuelistPokemonWithActivePkmnPower(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CountPokemonWithActivePkmnPowerInBothPlayAreas(ProbeState *s)
{
	PkmnPowerCountResult r = CountPokemonWithActivePkmnPowerInBothPlayAreas(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CheckIsIncapableOfUsingPkmnPower(ProbeState *s)
{
	PkmnPowerIncapableResult r = CheckIsIncapableOfUsingPkmnPower(s->a);
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CheckIsIncapableOfUsingPkmnPower_ArenaCard(ProbeState *s)
{
	PkmnPowerIncapableResult r = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_HandleDoubleDamageSubstatus(ProbeState *s)
{
	uint16_t de = HandleDoubleDamageSubstatus(pair(s->d, s->e));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_HandleDamageReductionExceptSubstatus2(ProbeState *s)
{
	uint16_t de = HandleDamageReductionExceptSubstatus2(pair(s->d, s->e));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_HandleDamageReduction(ProbeState *s)
{
	uint16_t de = HandleDamageReduction(pair(s->d, s->e));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_HandleCantAttackSubstatus(ProbeState *s)
{
	CantAttackResult r = HandleCantAttackSubstatus();
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_HandleAmnesiaSubstatus(ProbeState *s)
{
	AmnesiaResult r = HandleAmnesiaSubstatus();
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_HandleNoDamageOrEffectSubstatus(ProbeState *s)
{
	NoDamageOrEffectResult r = HandleNoDamageOrEffectSubstatus(s->e, s->hl);
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_CheckNoDamageOrEffect(ProbeState *s)
{
	NoDamageOrEffectCheckResult r = CheckNoDamageOrEffect(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_IsClairvoyanceActive(ProbeState *s)
{
	PkmnPowerCountResult r = IsClairvoyanceActive();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_GetLoadedCard1RetreatCost(ProbeState *s)
{
	s->a = GetLoadedCard1RetreatCost();
}

static void adapt_CheckUnableToRetreatDueToEffect(ProbeState *s)
{
	RetreatEffectResult r = CheckUnableToRetreatDueToEffect();
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CheckCantUseTrainerDueToEffect(ProbeState *s)
{
	TrainerEffectResult r = CheckCantUseTrainerDueToEffect();
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_IsPrehistoricPowerActive(ProbeState *s)
{
	PrehistoricPowerResult r = IsPrehistoricPowerActive(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ClearDamageReductionSubstatus2(ProbeState *s)
{
	(void)s;
	ClearDamageReductionSubstatus2();
}

static void adapt_UpdateSubstatusConditions_StartOfTurn(ProbeState *s)
{
	(void)s;
	UpdateSubstatusConditions_StartOfTurn();
}

static void adapt_UpdateSubstatusConditions_EndOfTurn(ProbeState *s)
{
	(void)s;
	UpdateSubstatusConditions_EndOfTurn();
}

static void adapt_IsRainDanceActive(ProbeState *s)
{
	PkmnPowerCountResult r = IsRainDanceActive();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_ClearChangedTypesIfMuk(ProbeState *s)
{
	ClearChangedTypesIfMuk(s->a);
}
static void adapt_HandleStrikesBack_AgainstDamagingAttack(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	StrikesBackResult r = HandleStrikesBack_AgainstDamagingAttack(de);
	s->a = r.a;
	s->f = r.f;
}
static void adapt_CheckRainDanceScenario(ProbeState *s) { RainDanceResult r = CheckRainDanceScenario(); s->a = r.a; s->f = r.f; }

/* >>> factory ApplyStrikesBack_AgainstResidualAttack */
static void adapt_ApplyStrikesBack_AgainstResidualAttack(ProbeState *s)
{
	ApplyStrikesBackResult r = ApplyStrikesBack_AgainstResidualAttack(s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ApplyStrikesBack_AgainstResidualAttack */

/* >>> factory HandleStrikesBack_AgainstResidualAttack */
static void adapt_HandleStrikesBack_AgainstResidualAttack(ProbeState *s)
{
	HandleStrikesBackResidualResult r = HandleStrikesBack_AgainstResidualAttack();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleStrikesBack_AgainstResidualAttack */

/* >>> factory HandleDestinyBondSubstatus */
static void adapt_HandleDestinyBondSubstatus(ProbeState *s)
{
	DestinyBondResult r = HandleDestinyBondSubstatus();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory HandleDestinyBondSubstatus */

const ProbeEntry probe_entries_substatus[] = {
	{ "CheckSandAttackOrSmokescreenSubstatus", adapt_CheckSandAttackOrSmokescreenSubstatus },
	{ "CountTurnDuelistPokemonWithActivePkmnPower", adapt_CountTurnDuelistPokemonWithActivePkmnPower },
	{ "CountPokemonWithActivePkmnPowerInBothPlayAreas", adapt_CountPokemonWithActivePkmnPowerInBothPlayAreas },
	{ "CheckIsIncapableOfUsingPkmnPower", adapt_CheckIsIncapableOfUsingPkmnPower },
	{ "CheckIsIncapableOfUsingPkmnPower_ArenaCard", adapt_CheckIsIncapableOfUsingPkmnPower_ArenaCard },
	{ "HandleDoubleDamageSubstatus", adapt_HandleDoubleDamageSubstatus },
	{ "HandleDamageReductionExceptSubstatus2", adapt_HandleDamageReductionExceptSubstatus2 },
	{ "HandleDamageReduction", adapt_HandleDamageReduction },
	{ "HandleCantAttackSubstatus", adapt_HandleCantAttackSubstatus },
	{ "HandleAmnesiaSubstatus", adapt_HandleAmnesiaSubstatus },
	{ "HandleNoDamageOrEffectSubstatus", adapt_HandleNoDamageOrEffectSubstatus },
	{ "CheckNoDamageOrEffect", adapt_CheckNoDamageOrEffect },
	{ "IsClairvoyanceActive", adapt_IsClairvoyanceActive },
	{ "GetLoadedCard1RetreatCost", adapt_GetLoadedCard1RetreatCost },
	{ "CheckUnableToRetreatDueToEffect", adapt_CheckUnableToRetreatDueToEffect },
	{ "CheckCantUseTrainerDueToEffect", adapt_CheckCantUseTrainerDueToEffect },
	{ "IsPrehistoricPowerActive", adapt_IsPrehistoricPowerActive },
	{ "ClearDamageReductionSubstatus2", adapt_ClearDamageReductionSubstatus2 },
	{ "UpdateSubstatusConditions_StartOfTurn", adapt_UpdateSubstatusConditions_StartOfTurn },
	{ "UpdateSubstatusConditions_EndOfTurn", adapt_UpdateSubstatusConditions_EndOfTurn },
	{ "IsRainDanceActive", adapt_IsRainDanceActive },
	{ "CheckRainDanceScenario", adapt_CheckRainDanceScenario },
	{ "ClearChangedTypesIfMuk", adapt_ClearChangedTypesIfMuk },
	{ "HandleStrikesBack_AgainstDamagingAttack", adapt_HandleStrikesBack_AgainstDamagingAttack },
	{ "ApplyStrikesBack_AgainstResidualAttack", adapt_ApplyStrikesBack_AgainstResidualAttack },
	{ "HandleStrikesBack_AgainstResidualAttack", adapt_HandleStrikesBack_AgainstResidualAttack },
	{ "HandleDestinyBondSubstatus", adapt_HandleDestinyBondSubstatus },
	{ NULL, NULL },
};
