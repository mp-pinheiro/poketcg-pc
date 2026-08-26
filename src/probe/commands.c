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

/* >>> factory GetDamageText */
static void adapt_GetDamageText(ProbeState *s)
{
	s->hl = GetDamageText(s->hl);
}
/* <<< factory GetDamageText */

/* >>> factory PlayAttackAnimationCommands_NextCommand */
static void adapt_PlayAttackAnimationCommands_NextCommand(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = PlayAttackAnimationCommands_NextCommand(s->a, s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory PlayAttackAnimationCommands_NextCommand */

/* >>> factory AnimationCommand_AnimNormal */
static void adapt_AnimationCommand_AnimNormal(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = AnimationCommand_AnimNormal(s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory AnimationCommand_AnimNormal */

/* >>> factory AnimationCommand_AnimPlayer */
static void adapt_AnimationCommand_AnimPlayer(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = AnimationCommand_AnimPlayer(s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory AnimationCommand_AnimPlayer */

/* >>> factory AnimationCommand_AnimOpponent */
static void adapt_AnimationCommand_AnimOpponent(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = AnimationCommand_AnimOpponent(s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory AnimationCommand_AnimOpponent */

/* >>> factory AnimationCommand_AnimPlayArea */
static void adapt_AnimationCommand_AnimPlayArea(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = AnimationCommand_AnimPlayArea(s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory AnimationCommand_AnimPlayArea */

/* >>> factory AnimationCommand_AnimScreen */
static void adapt_AnimationCommand_AnimScreen(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = AnimationCommand_AnimScreen(s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory AnimationCommand_AnimScreen */

/* >>> factory DuelAnim157 */
static void adapt_DuelAnim157(ProbeState *s)
{
	(void)s;
	DuelAnim157();
}
/* <<< factory DuelAnim157 */

/* >>> factory PrintDamageText */
static void adapt_PrintDamageText(ProbeState *s)
{
	PrintDamageTextResult result = PrintDamageText(s->b, s->c, s->d, s->e, s->hl);
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory PrintDamageText */

/* >>> factory UpdateMainSceneHUD */
static void adapt_UpdateMainSceneHUD(ProbeState *s)
{
	(void)s;
	UpdateMainSceneHUD();
}
/* <<< factory UpdateMainSceneHUD */

/* >>> factory SetScreenForDuelAnimation */
static void adapt_SetScreenForDuelAnimation(ProbeState *s)
{
	SetScreenForDuelAnimation(s->hl);
}
/* <<< factory SetScreenForDuelAnimation */

/* >>> factory PlayAttackAnimationCommands */
static void adapt_PlayAttackAnimationCommands(ProbeState *s)
{
	PlayAttackAnimationCommands_NextCommandResult r = PlayAttackAnimationCommands(s->a, s->d, s->e);
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory PlayAttackAnimationCommands */

const ProbeEntry probe_entries_commands[] = {
	{ "UpdateDuelAnimationScreen", adapt_UpdateDuelAnimationScreen },
	{ "DuelAnim153", adapt_DuelAnim153 },
	{ "AnimationCommand_AnimEnd2", adapt_AnimationCommand_AnimEnd2 },
	{ "AnimationCommand_AnimEnd", adapt_AnimationCommand_AnimEnd },
	{ "DuelAnim154", adapt_DuelAnim154 },
	{ "DuelAnim155", adapt_DuelAnim155 },
	{ "DuelAnim156", adapt_DuelAnim156 },
	{ "GetDamageText", adapt_GetDamageText },
	{ "PlayAttackAnimationCommands_NextCommand", adapt_PlayAttackAnimationCommands_NextCommand },
	{ "AnimationCommand_AnimNormal", adapt_AnimationCommand_AnimNormal },
	{ "AnimationCommand_AnimPlayer", adapt_AnimationCommand_AnimPlayer },
	{ "AnimationCommand_AnimOpponent", adapt_AnimationCommand_AnimOpponent },
	{ "AnimationCommand_AnimPlayArea", adapt_AnimationCommand_AnimPlayArea },
	{ "AnimationCommand_AnimScreen", adapt_AnimationCommand_AnimScreen },
	{ "DuelAnim157", adapt_DuelAnim157 },
	{ "PrintDamageText", adapt_PrintDamageText },
	{ "UpdateMainSceneHUD", adapt_UpdateMainSceneHUD },
	{ "SetScreenForDuelAnimation", adapt_SetScreenForDuelAnimation },
	{ "PlayAttackAnimationCommands", adapt_PlayAttackAnimationCommands },
	{ NULL, NULL },
};
