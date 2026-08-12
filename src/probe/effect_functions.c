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

/* >>> factory QueueStatusCondition */
static void adapt_QueueStatusCondition(ProbeState *s)
{
	QueueStatusConditionResult r = QueueStatusCondition(s->b, s->c);
	s->f = r.f;
}
/* <<< factory QueueStatusCondition */

/* >>> factory CommentedOut_2c086 */
static void adapt_CommentedOut_2c086(ProbeState *s)
{
	s->a = CommentedOut_2c086(s->a);
}
/* <<< factory CommentedOut_2c086 */

/* >>> factory SetWasUnsuccessful */
static void adapt_SetWasUnsuccessful(ProbeState *s)
{
	(void)s;
	SetWasUnsuccessful();
}
/* <<< factory SetWasUnsuccessful */

/* >>> factory Teleport_SwitchEffect */
static void adapt_Teleport_SwitchEffect(ProbeState *s)
{
	Teleport_SwitchEffect();
}
/* <<< factory Teleport_SwitchEffect */

/* >>> factory SetDamageToATimes20 */
static void adapt_SetDamageToATimes20(ProbeState *s)
{
	SetDamageToATimes20(s->a);
}
/* <<< factory SetDamageToATimes20 */

/* >>> factory CreateTrainerCardListFromDiscardPile */
static void adapt_CreateTrainerCardListFromDiscardPile(ProbeState *s)
{
	CreateTrainerCardListFromDiscardPileResult r = CreateTrainerCardListFromDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateTrainerCardListFromDiscardPile */

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
	{ "QueueStatusCondition", adapt_QueueStatusCondition },
	{ "CommentedOut_2c086", adapt_CommentedOut_2c086 },
	{ "SetWasUnsuccessful", adapt_SetWasUnsuccessful },
	{ "Teleport_SwitchEffect", adapt_Teleport_SwitchEffect },
	{ "SetDamageToATimes20", adapt_SetDamageToATimes20 },
	{ "CreateTrainerCardListFromDiscardPile", adapt_CreateTrainerCardListFromDiscardPile },
	{ NULL, NULL },
};
