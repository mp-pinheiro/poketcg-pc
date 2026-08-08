#include "home/duel_core.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_ConvertSpecialTrainerCardToPokemon(ProbeState *s)
{
	TrainerConvertResult r = ConvertSpecialTrainerCardToPokemon(s->a, s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
}

static void adapt_ResetAttackAnimationIsPlaying(ProbeState *s)
{
	(void)s;
	ResetAttackAnimationIsPlaying();
}

static void adapt_ClearNonTurnTemporaryDuelvars(ProbeState *s)
{
	(void)s;
	ClearNonTurnTemporaryDuelvars();
}

static void adapt_ClearNonTurnTemporaryDuelvars_CopyStatus(ProbeState *s)
{
	(void)s;
	ClearNonTurnTemporaryDuelvars_CopyStatus();
}

static void adapt_UpdateArenaCardLastTurnDamage(ProbeState *s)
{
	(void)s;
	UpdateArenaCardLastTurnDamage();
}

static void adapt_PrintThereWasNoEffectFromStatusText(ProbeState *s)
{
	(void)s;
	s->hl = PrintThereWasNoEffectFromStatusText();
}

static void adapt_WaitAttackAnimation(ProbeState *s)
{
	(void)s;
	WaitAttackAnimation();
}

static void adapt_ApplyStatusConditionQueue(ProbeState *s)
{
	(void)s;
	s->f = ApplyStatusConditionQueue();
}



static void adapt_GetCardOneStageBelow(ProbeState *s)
{
	CardOneStageBelowResult r = GetCardOneStageBelow(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
	s->f = r.f;
}

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
	{ NULL, NULL },
};
