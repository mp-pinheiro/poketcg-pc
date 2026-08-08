#include "home/duel.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_CopyPlayerName(ProbeState *s)
{
	CopyTextResult r = CopyPlayerName(pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_CopyOpponentName(ProbeState *s)
{
	CopyTextResult r = CopyOpponentName(pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_GetTurnDuelistVariable(ProbeState *s)
{
	DuelistVarResult r = GetTurnDuelistVariable(s->a);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_GetNonTurnDuelistVariable(ProbeState *s)
{
	DuelistVarResult r = GetNonTurnDuelistVariable(s->a);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_SwapTurn(ProbeState *s)
{
	SwapTurn();
}

static void adapt__GetCardIDFromDeckIndex(ProbeState *s)
{
	DeckCardResult r = _GetCardIDFromDeckIndex(s->a);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_GetCardIDFromDeckIndex(ProbeState *s)
{
	uint16_t id = GetCardIDFromDeckIndex(s->a);
	s->d = (uint8_t)(id >> 8);
	s->e = (uint8_t)id;
}

static void adapt_GetCardIDFromDeckIndex_bc(ProbeState *s)
{
	DeckCardResult r = GetCardIDFromDeckIndex_bc(s->a, s->hl);
	s->a = r.a;
	s->b = 0;
	s->c = r.a;
	s->hl = r.hl;
}

static void adapt_GetCardInDuelTempList_OnlyDeckIndex(ProbeState *s)
{
	DeckCardResult r = GetCardInDuelTempList_OnlyDeckIndex(s->a, s->hl);
	s->a = r.a;
	s->hl = r.hl;
}

static void adapt_GetCardInDuelTempList(ProbeState *s)
{
	DeckEntryResult r = GetCardInDuelTempList(s->a, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_duel[] = {
	{ "CopyPlayerName", adapt_CopyPlayerName },
	{ "CopyOpponentName", adapt_CopyOpponentName },
	{ "GetTurnDuelistVariable", adapt_GetTurnDuelistVariable },
	{ "GetNonTurnDuelistVariable", adapt_GetNonTurnDuelistVariable },
	{ "SwapTurn", adapt_SwapTurn },
	{ "_GetCardIDFromDeckIndex", adapt__GetCardIDFromDeckIndex },
	{ "GetCardIDFromDeckIndex", adapt_GetCardIDFromDeckIndex },
	{ "GetCardIDFromDeckIndex_bc", adapt_GetCardIDFromDeckIndex_bc },
	{ "GetCardInDuelTempList_OnlyDeckIndex", adapt_GetCardInDuelTempList_OnlyDeckIndex },
	{ "GetCardInDuelTempList", adapt_GetCardInDuelTempList },
	{ NULL, NULL },
};
