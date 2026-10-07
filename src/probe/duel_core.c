/* >>> part includes */
#include "home/duel_core.h"
#include "probe.h"
/* <<< part includes */

/* >>> part pair */
static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}
/* <<< part pair */

/* >>> factory ConvertSpecialTrainerCardToPokemon */
static void adapt_ConvertSpecialTrainerCardToPokemon(ProbeState *s)
{
	TrainerConvertResult r = ConvertSpecialTrainerCardToPokemon(s->a, s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ConvertSpecialTrainerCardToPokemon */

/* >>> factory ResetAttackAnimationIsPlaying */
static void adapt_ResetAttackAnimationIsPlaying(ProbeState *s)
{
	(void)s;
	ResetAttackAnimationIsPlaying();
}
/* <<< factory ResetAttackAnimationIsPlaying */

/* >>> factory ClearNonTurnTemporaryDuelvars */
static void adapt_ClearNonTurnTemporaryDuelvars(ProbeState *s)
{
	(void)s;
	ClearNonTurnTemporaryDuelvars();
}
/* <<< factory ClearNonTurnTemporaryDuelvars */

/* >>> factory ClearNonTurnTemporaryDuelvars_CopyStatus */
static void adapt_ClearNonTurnTemporaryDuelvars_CopyStatus(ProbeState *s)
{
	(void)s;
	ClearNonTurnTemporaryDuelvars_CopyStatus();
}
/* <<< factory ClearNonTurnTemporaryDuelvars_CopyStatus */

/* >>> factory UpdateArenaCardLastTurnDamage */
static void adapt_UpdateArenaCardLastTurnDamage(ProbeState *s)
{
	(void)s;
	UpdateArenaCardLastTurnDamage();
}
/* <<< factory UpdateArenaCardLastTurnDamage */

/* >>> factory PrintThereWasNoEffectFromStatusText */
static void adapt_PrintThereWasNoEffectFromStatusText(ProbeState *s)
{
	(void)s;
	s->hl = PrintThereWasNoEffectFromStatusText();
}
/* <<< factory PrintThereWasNoEffectFromStatusText */

/* >>> factory WaitAttackAnimation */
static void adapt_WaitAttackAnimation(ProbeState *s)
{
	(void)s;
	WaitAttackAnimation();
}
/* <<< factory WaitAttackAnimation */

/* >>> factory ApplyStatusConditionQueue */
static void adapt_ApplyStatusConditionQueue(ProbeState *s)
{
	(void)s;
	s->f = ApplyStatusConditionQueue();
}
/* <<< factory ApplyStatusConditionQueue */

/* >>> factory GetCardOneStageBelow */
static void adapt_GetCardOneStageBelow(ProbeState *s)
{
	CardOneStageBelowResult r = GetCardOneStageBelow(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory GetCardOneStageBelow */

/* >>> factory SetDefaultConsolePalettes */
static void adapt_SetDefaultConsolePalettes(ProbeState *s)
{
	(void)s;
	SetDefaultConsolePalettes();
}
/* <<< factory SetDefaultConsolePalettes */

/* >>> part probe_entries_duel_core */
const ProbeEntry probe_entries_duel_core[] = {
	{ "ConvertSpecialTrainerCardToPokemon", adapt_ConvertSpecialTrainerCardToPokemon },
	{ "ResetAttackAnimationIsPlaying", adapt_ResetAttackAnimationIsPlaying },
	{ "ClearNonTurnTemporaryDuelvars", adapt_ClearNonTurnTemporaryDuelvars },
	{ "ClearNonTurnTemporaryDuelvars_CopyStatus", adapt_ClearNonTurnTemporaryDuelvars_CopyStatus },
	{ "UpdateArenaCardLastTurnDamage", adapt_UpdateArenaCardLastTurnDamage },
	{ "PrintThereWasNoEffectFromStatusText", adapt_PrintThereWasNoEffectFromStatusText },
	{ "WaitAttackAnimation", adapt_WaitAttackAnimation },
	{ "ApplyStatusConditionQueue", adapt_ApplyStatusConditionQueue },
	{ "GetCardOneStageBelow", adapt_GetCardOneStageBelow },
	{ "SetDefaultConsolePalettes", adapt_SetDefaultConsolePalettes },
	{ NULL, NULL },
};
/* <<< part probe_entries_duel_core */
