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


/* >>> factory DuelAnim154 */
static void adapt_DuelAnim154(ProbeState *s)
{
	DuelAnim154();
}
/* <<< factory DuelAnim154 */

/* >>> factory DuelAnim155 */
static void adapt_DuelAnim155(ProbeState *s)
{
	DuelAnim155();
}
/* <<< factory DuelAnim155 */

/* >>> factory DuelAnim156 */
static void adapt_DuelAnim156(ProbeState *s)
{
	DuelAnim156();
}
/* <<< factory DuelAnim156 */

const ProbeEntry probe_entries_commands[] = {
	{ "UpdateDuelAnimationScreen", adapt_UpdateDuelAnimationScreen },
	{ "DuelAnim153", adapt_DuelAnim153 },
	{ "AnimationCommand_AnimEnd2", adapt_AnimationCommand_AnimEnd2 },
	{ "AnimationCommand_AnimEnd", adapt_AnimationCommand_AnimEnd },
	{ "DuelAnim154", adapt_DuelAnim154 },
	{ "DuelAnim155", adapt_DuelAnim155 },
	{ "DuelAnim156", adapt_DuelAnim156 },
	{ NULL, NULL },
};
