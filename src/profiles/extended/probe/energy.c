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
/* <<< part probe_entries_energy */
