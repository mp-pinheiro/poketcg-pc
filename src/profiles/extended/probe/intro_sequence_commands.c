/* --- factory LoadOpeningSceneAndUpdateSGBBorder */
/* >>> factory IntroSequenceCmd_LoadCharizardScene */
static void adapt_IntroSequenceCmd_LoadCharizardScene(ProbeState *s)
{
	IntroSequenceCmdLoadSceneResult r = IntroSequenceCmd_LoadCharizardScene();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory IntroSequenceCmd_LoadCharizardScene */
/* >>> factory IntroSequenceCmd_LoadAerodactylScene */
static void adapt_IntroSequenceCmd_LoadAerodactylScene(ProbeState *s)
{
	IntroSequenceCmdLoadSceneResult r = IntroSequenceCmd_LoadAerodactylScene();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory IntroSequenceCmd_LoadAerodactylScene */
/* >>> factory IntroSequenceCmd_LoadScytherScene */
static void adapt_IntroSequenceCmd_LoadScytherScene(ProbeState *s)
{
	IntroSequenceCmdLoadSceneResult r = IntroSequenceCmd_LoadScytherScene();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory IntroSequenceCmd_LoadScytherScene */
/* >>> part probe_entries_intro_sequence_commands */
/* <<< part probe_entries_intro_sequence_commands */
