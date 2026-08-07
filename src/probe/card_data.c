#include "home/card_data.h"
#include "probe.h"

static void adapt_GetCardType(ProbeState *s)
{
	s->a = GetCardType(s->e);
}

static void adapt_GetCardName(ProbeState *s)
{
	uint16_t de = GetCardName(s->e);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_GetCardTypeRarityAndSet(ProbeState *s)
{
	CardTRS r = GetCardTypeRarityAndSet(s->a);
	s->a = r.type;
	s->b = r.rarity;
	s->c = r.set;
}

static void adapt_LoadCardDataToBuffer1_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer1_FromCardID(s->e);
}

static void adapt_LoadCardDataToBuffer2_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer2_FromCardID(s->e);
}

static void adapt_LoadCardDataToBuffer1_FromName(ProbeState *s)
{
	LoadCardDataToBuffer1_FromName((uint16_t)(s->d << 8 | s->e));
}

static void adapt_LoadCardGfx(ProbeState *s)
{
	LoadCardGfx(s->hl, (uint16_t)(s->d << 8 | s->e), s->b, s->c);
}

const ProbeEntry probe_entries_card_data[] = {
	{ "GetCardType", adapt_GetCardType },
	{ "GetCardName", adapt_GetCardName },
	{ "GetCardTypeRarityAndSet", adapt_GetCardTypeRarityAndSet },
	{ "LoadCardDataToBuffer1_FromCardID", adapt_LoadCardDataToBuffer1_FromCardID },
	{ "LoadCardDataToBuffer2_FromCardID", adapt_LoadCardDataToBuffer2_FromCardID },
	{ "LoadCardDataToBuffer1_FromName", adapt_LoadCardDataToBuffer1_FromName },
	{ "LoadCardGfx", adapt_LoadCardGfx },
	{ NULL, NULL },
};
