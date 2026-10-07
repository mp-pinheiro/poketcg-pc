/* >>> part includes */
#include "home/substatus.h"
#include "probe.h"
/* <<< part includes */

/* >>> part pair */
static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}
/* <<< part pair */

/* >>> factory CheckSandAttackOrSmokescreenSubstatus */
static void adapt_CheckSandAttackOrSmokescreenSubstatus(ProbeState *s)
{
	SandAttackCheckResult r = CheckSandAttackOrSmokescreenSubstatus(pair(s->d, s->e));
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory CheckSandAttackOrSmokescreenSubstatus */

/* >>> factory CountTurnDuelistPokemonWithActivePkmnPower */
static void adapt_CountTurnDuelistPokemonWithActivePkmnPower(ProbeState *s)
{
	CardId target = (CardId)(((uint16_t)s->d << 8) | s->e);
	PkmnPowerCountResult r = CountTurnDuelistPokemonWithActivePkmnPower(target);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CountTurnDuelistPokemonWithActivePkmnPower */

/* >>> factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
static void adapt_CountPokemonWithActivePkmnPowerInBothPlayAreas(ProbeState *s)
{
	CardId target = (CardId)(((uint16_t)s->d << 8) | s->e);
	PkmnPowerCountResult r = CountPokemonWithActivePkmnPowerInBothPlayAreas(target);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CountPokemonWithActivePkmnPowerInBothPlayAreas */

/* >>> factory CheckIsIncapableOfUsingPkmnPower */
static void adapt_CheckIsIncapableOfUsingPkmnPower(ProbeState *s)
{
	PkmnPowerIncapableResult r = CheckIsIncapableOfUsingPkmnPower(s->a);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckIsIncapableOfUsingPkmnPower */

/* >>> factory CheckIsIncapableOfUsingPkmnPower_ArenaCard */
static void adapt_CheckIsIncapableOfUsingPkmnPower_ArenaCard(ProbeState *s)
{
	PkmnPowerIncapableResult r = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckIsIncapableOfUsingPkmnPower_ArenaCard */

/* >>> factory HandleDoubleDamageSubstatus */
static void adapt_HandleDoubleDamageSubstatus(ProbeState *s)
{
	uint16_t de = HandleDoubleDamageSubstatus(pair(s->d, s->e));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory HandleDoubleDamageSubstatus */

/* >>> factory HandleDamageReductionExceptSubstatus2 */
static void adapt_HandleDamageReductionExceptSubstatus2(ProbeState *s)
{
	uint16_t de = HandleDamageReductionExceptSubstatus2(pair(s->d, s->e));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory HandleDamageReductionExceptSubstatus2 */

/* >>> factory HandleDamageReduction */
static void adapt_HandleDamageReduction(ProbeState *s)
{
	uint16_t de = HandleDamageReduction(pair(s->d, s->e));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory HandleDamageReduction */

/* >>> factory HandleCantAttackSubstatus */
static void adapt_HandleCantAttackSubstatus(ProbeState *s)
{
	CantAttackResult r = HandleCantAttackSubstatus();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory HandleCantAttackSubstatus */

/* >>> factory HandleAmnesiaSubstatus */
static void adapt_HandleAmnesiaSubstatus(ProbeState *s)
{
	AmnesiaResult r = HandleAmnesiaSubstatus();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory HandleAmnesiaSubstatus */

/* >>> factory HandleNoDamageOrEffectSubstatus */
static void adapt_HandleNoDamageOrEffectSubstatus(ProbeState *s)
{
	NoDamageOrEffectResult r = HandleNoDamageOrEffectSubstatus(s->d, s->e, s->hl);
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory HandleNoDamageOrEffectSubstatus */

/* >>> factory CheckNoDamageOrEffect */
static void adapt_CheckNoDamageOrEffect(ProbeState *s)
{
	NoDamageOrEffectCheckResult r = CheckNoDamageOrEffect(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckNoDamageOrEffect */

/* >>> factory IsClairvoyanceActive */
static void adapt_IsClairvoyanceActive(ProbeState *s)
{
	PkmnPowerCountResult r = IsClairvoyanceActive();
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory IsClairvoyanceActive */

/* >>> factory GetLoadedCard1RetreatCost */
static void adapt_GetLoadedCard1RetreatCost(ProbeState *s)
{
	s->a = GetLoadedCard1RetreatCost();
}
/* <<< factory GetLoadedCard1RetreatCost */

/* >>> factory CheckUnableToRetreatDueToEffect */
static void adapt_CheckUnableToRetreatDueToEffect(ProbeState *s)
{
	RetreatEffectResult r = CheckUnableToRetreatDueToEffect();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckUnableToRetreatDueToEffect */

/* >>> factory CheckCantUseTrainerDueToEffect */
static void adapt_CheckCantUseTrainerDueToEffect(ProbeState *s)
{
	TrainerEffectResult r = CheckCantUseTrainerDueToEffect();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckCantUseTrainerDueToEffect */

/* >>> factory IsPrehistoricPowerActive */
static void adapt_IsPrehistoricPowerActive(ProbeState *s)
{
	PrehistoricPowerResult r = IsPrehistoricPowerActive(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory IsPrehistoricPowerActive */

/* >>> factory ClearDamageReductionSubstatus2 */
static void adapt_ClearDamageReductionSubstatus2(ProbeState *s)
{
	(void)s;
	ClearDamageReductionSubstatus2();
}
/* <<< factory ClearDamageReductionSubstatus2 */

/* >>> factory UpdateSubstatusConditions_StartOfTurn */
static void adapt_UpdateSubstatusConditions_StartOfTurn(ProbeState *s)
{
	(void)s;
	UpdateSubstatusConditions_StartOfTurn();
}
/* <<< factory UpdateSubstatusConditions_StartOfTurn */

/* >>> factory UpdateSubstatusConditions_EndOfTurn */
static void adapt_UpdateSubstatusConditions_EndOfTurn(ProbeState *s)
{
	(void)s;
	UpdateSubstatusConditions_EndOfTurn();
}
/* <<< factory UpdateSubstatusConditions_EndOfTurn */

/* >>> factory IsRainDanceActive */
static void adapt_IsRainDanceActive(ProbeState *s)
{
	PkmnPowerCountResult r = IsRainDanceActive();
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory IsRainDanceActive */

/* >>> factory ClearChangedTypesIfMuk */
static void adapt_ClearChangedTypesIfMuk(ProbeState *s)
{
	ClearChangedTypesIfMuk(s->a);
}
/* <<< factory ClearChangedTypesIfMuk */
/* >>> factory HandleStrikesBack_AgainstDamagingAttack */
static void adapt_HandleStrikesBack_AgainstDamagingAttack(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	StrikesBackResult r = HandleStrikesBack_AgainstDamagingAttack(de, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory HandleStrikesBack_AgainstDamagingAttack */
/* >>> factory CheckRainDanceScenario */
static void adapt_CheckRainDanceScenario(ProbeState *s) { RainDanceResult r = CheckRainDanceScenario(); s->a = r.a; s->f = r.f; }
/* <<< factory CheckRainDanceScenario */

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

/* >>> factory HandleNShieldAndTransparency */
static void adapt_HandleNShieldAndTransparency(ProbeState *s)
{
	HandleNShieldAndTransparencyResult result = HandleNShieldAndTransparency((uint16_t)(((uint16_t)s->d << 8u) | s->e));
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory HandleNShieldAndTransparency */

/* >>> factory HandleTransparency */
static void adapt_HandleTransparency(ProbeState *s)
{
	HandleTransparencyResult result = HandleTransparency(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory HandleTransparency */

/* >>> factory HandleDamageReductionOrNoDamageFromPkmnPowerEffects */
static void adapt_HandleDamageReductionOrNoDamageFromPkmnPowerEffects(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult r = HandleDamageReductionOrNoDamageFromPkmnPowerEffects(de, s->hl);
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory HandleDamageReductionOrNoDamageFromPkmnPowerEffects */

/* >>> factory HandleSandAttackOrSmokescreenSubstatus */
static void adapt_HandleSandAttackOrSmokescreenSubstatus(ProbeState *s)
{
	HandleSandAttackOrSmokescreenSubstatusResult result = HandleSandAttackOrSmokescreenSubstatus((uint16_t)(((uint16_t)s->d << 8) | s->e), s->hl);
	s->a = result.a;
	s->f = result.f;
	s->d = (uint8_t)(result.de >> 8);
	s->e = (uint8_t)result.de;
	s->hl = result.hl;
	if (result.f & 0x10u) {
		s->b = (uint8_t)(result.bc >> 8);
		s->c = (uint8_t)result.bc;
	}
}
/* <<< factory HandleSandAttackOrSmokescreenSubstatus */

/* >>> part probe_entries_substatus */
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
	{ "HandleNShieldAndTransparency", adapt_HandleNShieldAndTransparency },
	{ "HandleTransparency", adapt_HandleTransparency },
	{ "HandleDamageReductionOrNoDamageFromPkmnPowerEffects", adapt_HandleDamageReductionOrNoDamageFromPkmnPowerEffects },
	{ "HandleSandAttackOrSmokescreenSubstatus", adapt_HandleSandAttackOrSmokescreenSubstatus },
	{ NULL, NULL },
};
/* <<< part probe_entries_substatus */
