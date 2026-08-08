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

static void adapt_LoadCardDataToBuffer1_FromDeckIndex(ProbeState *s)
{
	s->a = LoadCardDataToBuffer1_FromDeckIndex(s->a);
}

static void adapt_LoadCardDataToBuffer2_FromDeckIndex(ProbeState *s)
{
	s->a = LoadCardDataToBuffer2_FromDeckIndex(s->a);
}

static void adapt_SubtractHP(ProbeState *s)
{
	SubtractHPResult r = SubtractHP(s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CreateDeckCardList(ProbeState *s)
{
	CardListResult r = CreateDeckCardList(s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CreateDiscardPileCardList(ProbeState *s)
{
	CardListResult r = CreateDiscardPileCardList(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_RemoveCardFromDuelTempList(ProbeState *s)
{
	TempListResult r = RemoveCardFromDuelTempList(s->a);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_CountCardsInDuelTempList(ProbeState *s)
{
	TempListResult r = CountCardsInDuelTempList();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_FindLastCardInHand(ProbeState *s)
{
	HandListResult r = FindLastCardInHand(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CreateHandCardList(ProbeState *s)
{
	HandListResult r = CreateHandCardList(s->c);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_CreateArenaOrBenchEnergyCardList(ProbeState *s)
{
	HandListResult r = CreateArenaOrBenchEnergyCardList(s->a);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ShuffleCards(ProbeState *s)
{
	ShuffleCardsResult r = ShuffleCards(s->a, s->hl);
	s->a = r.a;
	s->f = r.f;
}

static void adapt_SortCardsInListByID(ProbeState *s)
{
	SortResult r = SortCardsInListByID(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SortCardsInDuelTempListByID(ProbeState *s)
{
	SortResult r = SortCardsInDuelTempListByID(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_SortHandCardsByID(ProbeState *s)
{
	HandSortResult r = SortHandCardsByID();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_TranslateColorToWR(ProbeState *s)
{
	s->a = TranslateColorToWR(s->a);
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
	{ "LoadCardDataToBuffer1_FromDeckIndex", adapt_LoadCardDataToBuffer1_FromDeckIndex },
	{ "LoadCardDataToBuffer2_FromDeckIndex", adapt_LoadCardDataToBuffer2_FromDeckIndex },
	{ "SubtractHP", adapt_SubtractHP },
	{ "CreateDeckCardList", adapt_CreateDeckCardList },
	{ "CreateDiscardPileCardList", adapt_CreateDiscardPileCardList },
	{ "RemoveCardFromDuelTempList", adapt_RemoveCardFromDuelTempList },
	{ "CountCardsInDuelTempList", adapt_CountCardsInDuelTempList },
	{ "FindLastCardInHand", adapt_FindLastCardInHand },
	{ "CreateHandCardList", adapt_CreateHandCardList },
	{ "CreateArenaOrBenchEnergyCardList", adapt_CreateArenaOrBenchEnergyCardList },
	{ "ShuffleCards", adapt_ShuffleCards },
	{ "SortCardsInListByID", adapt_SortCardsInListByID },
	{ "SortCardsInDuelTempListByID", adapt_SortCardsInDuelTempListByID },
	{ "SortHandCardsByID", adapt_SortHandCardsByID },
	{ "TranslateColorToWR", adapt_TranslateColorToWR },
	{ NULL, NULL },
};
