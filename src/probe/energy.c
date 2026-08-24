#include "home/energy.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory RetrievePlayAreaAIScoreFromBackup1 */
static void adapt_RetrievePlayAreaAIScoreFromBackup1(ProbeState *s)
{
	Backup1Result r = RetrievePlayAreaAIScoreFromBackup1();
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory RetrievePlayAreaAIScoreFromBackup1 */

/* >>> factory FindPlayAreaCardWithHighestAIScore */
static void adapt_FindPlayAreaCardWithHighestAIScore(ProbeState *s)
{
	AIScoreResult r = FindPlayAreaCardWithHighestAIScore(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FindPlayAreaCardWithHighestAIScore */

/* >>> factory CheckSpecificDecksToAttachDoubleColorless */
static void adapt_CheckSpecificDecksToAttachDoubleColorless(ProbeState *s)
{
	CheckSpecificDecksToAttachDoubleColorlessResult r =
		CheckSpecificDecksToAttachDoubleColorless(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory CheckSpecificDecksToAttachDoubleColorless */

/* >>> factory GetEnergyCardForDiscardOrEnergyBoostAttack */
static void adapt_GetEnergyCardForDiscardOrEnergyBoostAttack(ProbeState *s)
{
	GetEnergyCardForDiscardOrEnergyBoostAttackResult r = GetEnergyCardForDiscardOrEnergyBoostAttack(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory GetEnergyCardForDiscardOrEnergyBoostAttack */

/* >>> factory CheckIfEvolutionNeedsEnergyForAttack */
static void adapt_CheckIfEvolutionNeedsEnergyForAttack(ProbeState *s)
{
	CheckIfEvolutionNeedsEnergyForAttackResult r = CheckIfEvolutionNeedsEnergyForAttack(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CheckIfEvolutionNeedsEnergyForAttack */

/* >>> factory AITryToPlayEnergyCard */
static void adapt_AITryToPlayEnergyCard(ProbeState *s)
{
	s->a = AITryToPlayEnergyCard();
}
/* <<< factory AITryToPlayEnergyCard */

const ProbeEntry probe_entries_energy[] = {
	{ "RetrievePlayAreaAIScoreFromBackup1", adapt_RetrievePlayAreaAIScoreFromBackup1 },
	{ "FindPlayAreaCardWithHighestAIScore", adapt_FindPlayAreaCardWithHighestAIScore },
	{ "CheckSpecificDecksToAttachDoubleColorless", adapt_CheckSpecificDecksToAttachDoubleColorless },
	{ "GetEnergyCardForDiscardOrEnergyBoostAttack", adapt_GetEnergyCardForDiscardOrEnergyBoostAttack },
	{ "CheckIfEvolutionNeedsEnergyForAttack", adapt_CheckIfEvolutionNeedsEnergyForAttack },
	{ "AITryToPlayEnergyCard", adapt_AITryToPlayEnergyCard },
	{ NULL, NULL },
};
