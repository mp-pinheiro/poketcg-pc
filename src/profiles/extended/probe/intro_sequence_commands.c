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
const ProbeEntry probe_entries_intro_sequence_commands[] = {
	{ "AnimateRandomTitleScreenOrb", adapt_AnimateRandomTitleScreenOrb },
	{ "AdvanceIntroSequenceCmdPtr", adapt_AdvanceIntroSequenceCmdPtr },
	{ "AdvanceIntroSequenceCmdPtrBy2", adapt_AdvanceIntroSequenceCmdPtrBy2 },
	{ "AdvanceIntroSequenceCmdPtrBy4", adapt_AdvanceIntroSequenceCmdPtrBy4 },
	{ "IntroSequenceEmptyFunc", adapt_IntroSequenceEmptyFunc },
	{ "IntroSequenceCmd_FadeIn", adapt_IntroSequenceCmd_FadeIn },
	{ "IntroSequenceCmd_WaitSFX", adapt_IntroSequenceCmd_WaitSFX },
	{ "IntroSequenceCmd_WaitOrbsAnimation", adapt_IntroSequenceCmd_WaitOrbsAnimation },
	{ "IntroSequenceCmd_SetOrbsAnimations", adapt_IntroSequenceCmd_SetOrbsAnimations },
	{ "IntroSequenceCmd_SetOrbsCoordinates", adapt_IntroSequenceCmd_SetOrbsCoordinates },
	{ "IntroSequenceCmd_PlayTitleScreenMusic", adapt_IntroSequenceCmd_PlayTitleScreenMusic },
	{ "IntroSequenceCmd_FadeOut", adapt_IntroSequenceCmd_FadeOut },
	{ "AdvanceIntroSequenceCmdPtrBy3", adapt_AdvanceIntroSequenceCmdPtrBy3 },
	{ "IntroSequenceCmd_Wait", adapt_IntroSequenceCmd_Wait },
	{ "IntroSequenceCmd_PlaySFX", adapt_IntroSequenceCmd_PlaySFX },
	{ "LoadOpeningScene", adapt_LoadOpeningScene },
	{ "IntroSequenceCmd_LoadCharizardScene", adapt_IntroSequenceCmd_LoadCharizardScene },
	{ "IntroSequenceCmd_LoadTitleScreenScene", adapt_IntroSequenceCmd_LoadTitleScreenScene },
	{ "IntroSequenceCmd_LoadScytherScene", adapt_IntroSequenceCmd_LoadScytherScene },
	{ "IntroSequenceCmd_LoadAerodactylScene", adapt_IntroSequenceCmd_LoadAerodactylScene },
	{ "ExecuteIntroSequenceCmd", adapt_ExecuteIntroSequenceCmd },
	{ NULL, NULL },
};
/* <<< part probe_entries_intro_sequence_commands */
