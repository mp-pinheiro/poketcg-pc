#include "home/commands.h"
#include "probe.h"

/* >>> factory AnimationCommand_AnimEnd2 */
static void adapt_AnimationCommand_AnimEnd2(ProbeState *s)
{
	AnimationCommand_AnimEnd2();
	(void)s;
}
/* <<< factory AnimationCommand_AnimEnd2 */


/* >>> factory UpdateDuelAnimationScreen */
static void adapt_UpdateDuelAnimationScreen(ProbeState *s)
{
	UpdateDuelAnimationScreenResult result = UpdateDuelAnimationScreen(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory UpdateDuelAnimationScreen */


const ProbeEntry probe_entries_commands[] = {
	{ "AnimationCommand_AnimEnd2", adapt_AnimationCommand_AnimEnd2 },
	{ "UpdateDuelAnimationScreen", adapt_UpdateDuelAnimationScreen },
	{ NULL, NULL },
};
