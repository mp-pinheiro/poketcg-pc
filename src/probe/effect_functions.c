#include "home/effect_functions.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"




/* >>> factory UpdateExpectedAIDamage */
static void adapt_UpdateExpectedAIDamage(ProbeState *s)
{
	UpdateExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage */


/* >>> factory SetExpectedAIDamage */
static void adapt_SetExpectedAIDamage(ProbeState *s)
{
	SetExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory SetExpectedAIDamage */


/* >>> factory IsPlayerTurn */
static void adapt_IsPlayerTurn(ProbeState *s)
{
	IsPlayerTurnResult r = IsPlayerTurn();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory IsPlayerTurn */


/* >>> factory UpdateExpectedAIDamage_AccountForPoison */
static void adapt_UpdateExpectedAIDamage_AccountForPoison(ProbeState *s)
{
	UpdateExpectedAIDamage_AccountForPoison(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage_AccountForPoison */

/* >>> factory ApplySubstatus1ToAttackingCard */
static void adapt_ApplySubstatus1ToAttackingCard(ProbeState *s)
{
	s->hl = ApplySubstatus1ToAttackingCard(s->a);
}
/* <<< factory ApplySubstatus1ToAttackingCard */


/* >>> factory SetNoEffectFromStatus */
static void adapt_SetNoEffectFromStatus(ProbeState *s)
{
	(void)s;
	SetNoEffectFromStatus();
}
/* <<< factory SetNoEffectFromStatus */

/* >>> factory SetDefiniteAIDamage */
static void adapt_SetDefiniteAIDamage(ProbeState *s)
{
	(void)s;
	SetDefiniteAIDamage();
}
/* <<< factory SetDefiniteAIDamage */

/* >>> factory PickRandomPlayAreaCard */
static void adapt_PickRandomPlayAreaCard(ProbeState *s)
{
	PickRandomPlayAreaCardResult r = PickRandomPlayAreaCard();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PickRandomPlayAreaCard */

/* >>> factory GetNextPositionInTempList */
static void adapt_GetNextPositionInTempList(ProbeState *s)
{
	s->hl = GetNextPositionInTempList();
}
/* <<< factory GetNextPositionInTempList */

const ProbeEntry probe_entries_effect_functions[] = {
	{ "UpdateExpectedAIDamage", adapt_UpdateExpectedAIDamage },
	{ "SetExpectedAIDamage", adapt_SetExpectedAIDamage },
	{ "UpdateExpectedAIDamage_AccountForPoison", adapt_UpdateExpectedAIDamage_AccountForPoison },
	{ "IsPlayerTurn", adapt_IsPlayerTurn },
	{ "ApplySubstatus1ToAttackingCard", adapt_ApplySubstatus1ToAttackingCard },
	{ "SetNoEffectFromStatus", adapt_SetNoEffectFromStatus },
	{ "SetDefiniteAIDamage", adapt_SetDefiniteAIDamage },
	{ "PickRandomPlayAreaCard", adapt_PickRandomPlayAreaCard },
	{ "GetNextPositionInTempList", adapt_GetNextPositionInTempList },
	{ NULL, NULL },
};
