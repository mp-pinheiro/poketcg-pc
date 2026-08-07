#include "home/card_color.h"
#include "probe.h"

static void adapt_GetCardWeakness(ProbeState *s) { s->a = GetCardWeakness(s->a); }
static void adapt_GetArenaCardWeakness(ProbeState *s) { s->a = GetArenaCardWeakness(); }
static void adapt_GetPlayAreaCardWeakness(ProbeState *s) { s->a = GetPlayAreaCardWeakness(s->a); }
static void adapt_GetCardResistance(ProbeState *s) { s->a = GetCardResistance(s->a); }
static void adapt_GetArenaCardResistance(ProbeState *s) { s->a = GetArenaCardResistance(); }
static void adapt_GetPlayAreaCardResistance(ProbeState *s) { s->a = GetPlayAreaCardResistance(s->a); }

const ProbeEntry probe_entries_card_color[] = {
	{ "GetCardWeakness", adapt_GetCardWeakness },
	{ "GetArenaCardWeakness", adapt_GetArenaCardWeakness },
	{ "GetPlayAreaCardWeakness", adapt_GetPlayAreaCardWeakness },
	{ "GetCardResistance", adapt_GetCardResistance },
	{ "GetArenaCardResistance", adapt_GetArenaCardResistance },
	{ "GetPlayAreaCardResistance", adapt_GetPlayAreaCardResistance },
	{ NULL, NULL },
};
