/* >>> part includes */
#include "home/card_data.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory GetCardType */
static void adapt_GetCardType(ProbeState *s)
{
	s->a = GetCardType(s->e);
}
/* <<< factory GetCardType */

/* >>> factory GetCardName */
static void adapt_GetCardName(ProbeState *s)
{
	uint16_t de = GetCardName(s->e);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory GetCardName */

/* >>> factory GetCardTypeRarityAndSet */
static void adapt_GetCardTypeRarityAndSet(ProbeState *s)
{
	CardTRS r = GetCardTypeRarityAndSet(s->a);
	s->a = r.type;
	s->b = r.rarity;
	s->c = r.set;
}
/* <<< factory GetCardTypeRarityAndSet */

/* >>> factory LoadCardDataToBuffer1_FromCardID */
static void adapt_LoadCardDataToBuffer1_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer1_FromCardID(s->e);
}
/* <<< factory LoadCardDataToBuffer1_FromCardID */

/* >>> factory LoadCardDataToBuffer2_FromCardID */
static void adapt_LoadCardDataToBuffer2_FromCardID(ProbeState *s)
{
	LoadCardDataToBuffer2_FromCardID(s->e);
}
/* <<< factory LoadCardDataToBuffer2_FromCardID */

/* >>> factory LoadCardDataToBuffer1_FromName */
static void adapt_LoadCardDataToBuffer1_FromName(ProbeState *s)
{
	LoadCardDataToBuffer1_FromName((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadCardDataToBuffer1_FromName */

/* >>> factory LoadCardGfx */
static void adapt_LoadCardGfx(ProbeState *s)
{
	LoadCardGfx(s->hl, (uint16_t)(s->d << 8 | s->e), s->b, s->c);
}
/* <<< factory LoadCardGfx */

/* >>> factory GetCardPointer */
static void adapt_GetCardPointer(ProbeState *s)
{
	CardPtrResult r = GetCardPointer(s->e);
	s->hl = r.hl;
	s->f = r.carry ? (uint8_t)(0x10u | (r.bound_zero ? 0x80u : 0u)) : 0x00u;
}
/* <<< factory GetCardPointer */

/* >>> factory LoadCardDataToHL_FromCardID */
static void adapt_LoadCardDataToHL_FromCardID(ProbeState *s)
{
	LoadCardDataToHL_FromCardID(s->e, &s->hl, s->stack[0]);
}
/* <<< factory LoadCardDataToHL_FromCardID */

/* >>> factory CopyFontsOrDuelGraphicsTiles2 */
static void adapt_CopyFontsOrDuelGraphicsTiles2(ProbeState *s)
{
	CopyFontsOrDuelGraphicsTiles2(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory CopyFontsOrDuelGraphicsTiles2 */

/* >>> part probe_entries_card_data */
const ProbeEntry probe_entries_card_data[] = {
	{ "GetCardType", adapt_GetCardType },
	{ "GetCardName", adapt_GetCardName },
	{ "GetCardTypeRarityAndSet", adapt_GetCardTypeRarityAndSet },
	{ "LoadCardDataToBuffer1_FromCardID", adapt_LoadCardDataToBuffer1_FromCardID },
	{ "LoadCardDataToBuffer2_FromCardID", adapt_LoadCardDataToBuffer2_FromCardID },
	{ "LoadCardDataToBuffer1_FromName", adapt_LoadCardDataToBuffer1_FromName },
	{ "LoadCardGfx", adapt_LoadCardGfx },
	{ "GetCardPointer", adapt_GetCardPointer },
	{ "LoadCardDataToHL_FromCardID", adapt_LoadCardDataToHL_FromCardID },
	{ "CopyFontsOrDuelGraphicsTiles2", adapt_CopyFontsOrDuelGraphicsTiles2 },
	{ NULL, NULL },
};
/* <<< part probe_entries_card_data */
