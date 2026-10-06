#include "home/card_data.h"
#include "generated/hram.h"
#include "probe.h"

static CardId probe_card_id(const ProbeState *s)
{
	return (CardId)(((uint16_t)s->d << 8) | s->e);
}

static void adapt_GetCardType(ProbeState *s)
{
	s->a = GetCardType(probe_card_id(s));
}

static void adapt_GetCardName(ProbeState *s)
{
	uint16_t de = GetCardName(probe_card_id(s));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_GetCardTypeRarityAndSet(ProbeState *s)
{
	CardTRS r = GetCardTypeRarityAndSet(probe_card_id(s));
	s->a = r.type;
	if (r.carry)
		return;
	s->e = r.type;
	s->b = r.rarity;
	s->c = r.set;
}

static void adapt_LoadCardDataToBuffer1_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer1_FromCardID(probe_card_id(s));
}

static void adapt_LoadCardDataToBuffer2_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer2_FromCardID(probe_card_id(s));
}

static void adapt_LoadCardDataToBuffer1_FromName(ProbeState *s)
{
	LoadCardDataToBuffer1_FromName((uint16_t)(s->d << 8 | s->e));
}

static void adapt_GetCardPointer(ProbeState *s)
{
	CardPtrResult r = GetCardPointer(probe_card_id(s));
	s->hl = r.hl;
	if (r.carry) {
		s->a = hBankROM;
		s->f = (uint8_t)((s->f & 0x80u) | 0x10u);
	} else {
		s->a = r.bank;
		s->f = r.bank == 0u ? 0x80u : 0x00u;
	}
}

/* >>> factory LoadCardDataToHL_FromCardID */
static void adapt_LoadCardDataToHL_FromCardID(ProbeState *s)
{
	LoadCardDataToHL_FromCardID(probe_card_id(s), &s->hl, s->stack[0]);
}
/* <<< factory LoadCardDataToHL_FromCardID */

const ProbeEntry probe_entries_card_data[] = {
	{ "GetCardType", adapt_GetCardType },
	{ "GetCardName", adapt_GetCardName },
	{ "GetCardTypeRarityAndSet", adapt_GetCardTypeRarityAndSet },
	{ "LoadCardDataToBuffer1_FromCardID", adapt_LoadCardDataToBuffer1_FromCardID },
	{ "LoadCardDataToBuffer2_FromCardID", adapt_LoadCardDataToBuffer2_FromCardID },
	{ "LoadCardDataToBuffer1_FromName", adapt_LoadCardDataToBuffer1_FromName },
	{ "GetCardPointer", adapt_GetCardPointer },
	{ "LoadCardDataToHL_FromCardID", adapt_LoadCardDataToHL_FromCardID },
	{ NULL, NULL },
};
