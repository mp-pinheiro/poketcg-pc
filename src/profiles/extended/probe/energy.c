/* >>> factory AIProcessAndTryToPlayEnergy */
static void adapt_AIProcessAndTryToPlayEnergy(ProbeState *s)
{
	AIEnergyResult r = AIProcessAndTryToPlayEnergy();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AIProcessAndTryToPlayEnergy */
/* --- factory Func_16488 */
/* >>> part probe_entries_energy */
const ProbeEntry probe_entries_energy[] = {
	{ "RetrievePlayAreaAIScoreFromBackup1", adapt_RetrievePlayAreaAIScoreFromBackup1 },
	{ "FindPlayAreaCardWithHighestAIScore", adapt_FindPlayAreaCardWithHighestAIScore },
	{ "CheckSpecificDecksToAttachDoubleColorless", adapt_CheckSpecificDecksToAttachDoubleColorless },
	{ "GetEnergyCardForDiscardOrEnergyBoostAttack", adapt_GetEnergyCardForDiscardOrEnergyBoostAttack },
	{ "CheckIfEvolutionNeedsEnergyForAttack", adapt_CheckIfEvolutionNeedsEnergyForAttack },
	{ "AITryToPlayEnergyCard", adapt_AITryToPlayEnergyCard },
	{ "DetermineAIScoreOfAttackEnergyRequirement", adapt_DetermineAIScoreOfAttackEnergyRequirement },
	{ "AIProcessEnergyCards", adapt_AIProcessEnergyCards },
	{ "AIProcessAndTryToPlayEnergy", adapt_AIProcessAndTryToPlayEnergy },
	{ "AIProcessButDontPlayEnergy_SkipEvolution", adapt_AIProcessButDontPlayEnergy_SkipEvolution },
	{ "AIProcessButDontPlayEnergy_SkipEvolutionAndArena", adapt_AIProcessButDontPlayEnergy_SkipEvolutionAndArena },
	{ NULL, NULL },
};
/* <<< part probe_entries_energy */
