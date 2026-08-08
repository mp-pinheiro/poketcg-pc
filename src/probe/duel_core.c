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

const ProbeEntry probe_entries_duel_core[] = {
	{ "ConvertSpecialTrainerCardToPokemon", adapt_ConvertSpecialTrainerCardToPokemon },
	{ "ResetAttackAnimationIsPlaying", adapt_ResetAttackAnimationIsPlaying },
	{ "ClearNonTurnTemporaryDuelvars", adapt_ClearNonTurnTemporaryDuelvars },
	{ "ClearNonTurnTemporaryDuelvars_CopyStatus", adapt_ClearNonTurnTemporaryDuelvars_CopyStatus },
	{ "UpdateArenaCardLastTurnDamage", adapt_UpdateArenaCardLastTurnDamage },
	{ "PrintThereWasNoEffectFromStatusText", adapt_PrintThereWasNoEffectFromStatusText },
	{ NULL, NULL },
};
