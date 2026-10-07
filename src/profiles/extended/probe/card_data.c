/* >>> part includes */
#include "home/card_data.h"
#include "generated/hram.h"
#include "probe.h"
/* <<< part includes */

/* >>> part probe_card_id */
static CardId probe_card_id(const ProbeState *s)
{
	return (CardId)(((uint16_t)s->d << 8) | s->e);
}
/* <<< part probe_card_id */

/* >>> factory GetCardType */
static void adapt_GetCardType(ProbeState *s)
{
	s->a = GetCardType(probe_card_id(s));
}
/* <<< factory GetCardType */

/* >>> factory GetCardName */
static void adapt_GetCardName(ProbeState *s)
{
	uint16_t de = GetCardName(probe_card_id(s));
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory GetCardName */

/* >>> factory GetCardTypeRarityAndSet */
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
/* <<< factory GetCardTypeRarityAndSet */

/* >>> factory LoadCardDataToBuffer1_FromCardID */
static void adapt_LoadCardDataToBuffer1_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer1_FromCardID(probe_card_id(s));
}
/* <<< factory LoadCardDataToBuffer1_FromCardID */

/* >>> factory LoadCardDataToBuffer2_FromCardID */
static void adapt_LoadCardDataToBuffer2_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer2_FromCardID(probe_card_id(s));
}
/* <<< factory LoadCardDataToBuffer2_FromCardID */

/* >>> factory LoadCardDataToBuffer1_FromName */
static void adapt_LoadCardDataToBuffer1_FromName(ProbeState *s)
{
	LoadCardDataToBuffer1_FromName((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadCardDataToBuffer1_FromName */

/* >>> factory GetCardPointer */
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
/* <<< factory GetCardPointer */

/* >>> factory LoadCardDataToHL_FromCardID */
static void adapt_LoadCardDataToHL_FromCardID(ProbeState *s)
{
	LoadCardDataToHL_FromCardID(probe_card_id(s), &s->hl, s->stack[0]);
}
/* <<< factory LoadCardDataToHL_FromCardID */

/* >>> part probe_entries_card_data */
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
/* <<< part probe_entries_card_data */
