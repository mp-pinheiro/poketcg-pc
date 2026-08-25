#include "home/intro_sequence_commands.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AnimateRandomTitleScreenOrb */
static void adapt_AnimateRandomTitleScreenOrb(ProbeState *s)
{
	s->a = AnimateRandomTitleScreenOrb();
}
/* <<< factory AnimateRandomTitleScreenOrb */

/* >>> factory AdvanceIntroSequenceCmdPtr */
static void adapt_AdvanceIntroSequenceCmdPtr(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrResult result = AdvanceIntroSequenceCmdPtr(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AdvanceIntroSequenceCmdPtr */

/* >>> factory AdvanceIntroSequenceCmdPtrBy2 */
static void adapt_AdvanceIntroSequenceCmdPtrBy2(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrBy2();
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy2 */

/* >>> factory AdvanceIntroSequenceCmdPtrBy4 */
static void adapt_AdvanceIntroSequenceCmdPtrBy4(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrBy4();
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy4 */

/* >>> factory IntroSequenceEmptyFunc */
static void adapt_IntroSequenceEmptyFunc(ProbeState *s)
{
	(void)s;
	IntroSequenceEmptyFunc();
}
/* <<< factory IntroSequenceEmptyFunc */

/* >>> factory IntroSequenceCmd_FadeIn */
static void adapt_IntroSequenceCmd_FadeIn(ProbeState *s)
{
	IntroSequenceCmd_FadeInResult r = IntroSequenceCmd_FadeIn();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_FadeIn */

/* >>> factory IntroSequenceCmd_WaitSFX */
static void adapt_IntroSequenceCmd_WaitSFX(ProbeState *s)
{
	IntroSequenceCmdWaitSFXResult r = IntroSequenceCmd_WaitSFX();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_WaitSFX */

/* >>> factory IntroSequenceCmd_WaitOrbsAnimation */
static void adapt_IntroSequenceCmd_WaitOrbsAnimation(ProbeState *s)
{
	IntroSequenceCmdWaitOrbsAnimationResult r = IntroSequenceCmd_WaitOrbsAnimation();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_WaitOrbsAnimation */

/* >>> factory IntroSequenceCmd_SetOrbsAnimations */
static void adapt_IntroSequenceCmd_SetOrbsAnimations(ProbeState *s)
{
	IntroSequenceCmdSetOrbsAnimationsResult r = IntroSequenceCmd_SetOrbsAnimations(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory IntroSequenceCmd_SetOrbsAnimations */

/* >>> factory IntroSequenceCmd_SetOrbsCoordinates */
static void adapt_IntroSequenceCmd_SetOrbsCoordinates(ProbeState *s)
{
	IntroSequenceCmdSetOrbsCoordinatesResult r = IntroSequenceCmd_SetOrbsCoordinates(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory IntroSequenceCmd_SetOrbsCoordinates */

/* >>> factory IntroSequenceCmd_PlayTitleScreenMusic */
static void adapt_IntroSequenceCmd_PlayTitleScreenMusic(ProbeState *s)
{
	IntroSequenceCmd_PlayTitleScreenMusicResult r = IntroSequenceCmd_PlayTitleScreenMusic();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_PlayTitleScreenMusic */

/* >>> factory IntroSequenceCmd_FadeOut */
static void adapt_IntroSequenceCmd_FadeOut(ProbeState *s)
{
	IntroSequenceCmd_FadeOutResult r = IntroSequenceCmd_FadeOut();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_FadeOut */

/* >>> factory AdvanceIntroSequenceCmdPtrBy3 */
static void adapt_AdvanceIntroSequenceCmdPtrBy3(ProbeState *s)
{
	AdvanceIntroSequenceCmdPtrBy3();
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy3 */

/* >>> factory IntroSequenceCmd_Wait */
static void adapt_IntroSequenceCmd_Wait(ProbeState *s)
{
	IntroSequenceCmdWaitResult r = IntroSequenceCmd_Wait(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_Wait */

/* >>> factory IntroSequenceCmd_PlaySFX */
static void adapt_IntroSequenceCmd_PlaySFX(ProbeState *s)
{
	IntroSequenceCmdPlaySFXResult r = IntroSequenceCmd_PlaySFX(s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_PlaySFX */

/* >>> factory LoadOpeningScene */
static void adapt_LoadOpeningScene(ProbeState *s)
{
	LoadOpeningScene(s->a, s->b, s->c);
}
/* <<< factory LoadOpeningScene */

/* >>> factory LoadOpeningSceneAndUpdateSGBBorder */
static void adapt_LoadOpeningSceneAndUpdateSGBBorder(ProbeState *s)
{
	LoadOpeningSceneAndUpdateSGBBorderResult r = LoadOpeningSceneAndUpdateSGBBorder(s->a, s->b, s->c);
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory LoadOpeningSceneAndUpdateSGBBorder */

/* >>> factory IntroSequenceCmd_LoadCharizardScene */
static void adapt_IntroSequenceCmd_LoadCharizardScene(ProbeState *s)
{
	LoadOpeningSceneAndUpdateSGBBorderResult r = IntroSequenceCmd_LoadCharizardScene();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory IntroSequenceCmd_LoadCharizardScene */

/* >>> factory IntroSequenceCmd_LoadTitleScreenScene */
static void adapt_IntroSequenceCmd_LoadTitleScreenScene(ProbeState *s)
{
	IntroSequenceCmdLoadTitleScreenSceneResult r = IntroSequenceCmd_LoadTitleScreenScene();
	s->f = r.f;
}
/* <<< factory IntroSequenceCmd_LoadTitleScreenScene */

/* >>> factory IntroSequenceCmd_LoadAerodactylScene */
static void adapt_IntroSequenceCmd_LoadAerodactylScene(ProbeState *s)
{
	LoadOpeningSceneAndUpdateSGBBorderResult r = IntroSequenceCmd_LoadAerodactylScene();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory IntroSequenceCmd_LoadAerodactylScene */

/* >>> factory IntroSequenceCmd_LoadScytherScene */
static void adapt_IntroSequenceCmd_LoadScytherScene(ProbeState *s)
{
	LoadOpeningSceneAndUpdateSGBBorderResult r = IntroSequenceCmd_LoadScytherScene();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory IntroSequenceCmd_LoadScytherScene */

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
	{ "LoadOpeningSceneAndUpdateSGBBorder", adapt_LoadOpeningSceneAndUpdateSGBBorder },
	{ "IntroSequenceCmd_LoadCharizardScene", adapt_IntroSequenceCmd_LoadCharizardScene },
	{ "IntroSequenceCmd_LoadTitleScreenScene", adapt_IntroSequenceCmd_LoadTitleScreenScene },
	{ "IntroSequenceCmd_LoadScytherScene", adapt_IntroSequenceCmd_LoadScytherScene },
	{ "IntroSequenceCmd_LoadAerodactylScene", adapt_IntroSequenceCmd_LoadAerodactylScene },
	{ NULL, NULL },
};
