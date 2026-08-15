#include "home/commands.h"
#include "probe.h"

/* >>> factory AnimationCommand_AnimEnd2 */
static void adapt_AnimationCommand_AnimEnd2(ProbeState *s)
{
	s->a = AnimationCommand_AnimEnd2(s->a);
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


/* >>> factory DuelAnim153 */
static void adapt_DuelAnim153(ProbeState *s)
{
	(void)s;
	DuelAnim153();
}
/* <<< factory DuelAnim153 */

/* >>> factory AnimationCommand_AnimEnd */
static void adapt_AnimationCommand_AnimEnd(ProbeState *s)
{
	AnimationCommand_AnimEnd();
}
/* <<< factory AnimationCommand_AnimEnd */


const ProbeEntry probe_entries_commands[] = {
	{ "UpdateDuelAnimationScreen", adapt_UpdateDuelAnimationScreen },
	{ "DuelAnim153", adapt_DuelAnim153 },
	{ "AnimationCommand_AnimEnd2", adapt_AnimationCommand_AnimEnd2 },
	{ "AnimationCommand_AnimEnd", adapt_AnimationCommand_AnimEnd },
	{ NULL, NULL },
};
