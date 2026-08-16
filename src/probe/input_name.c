#include "home/input_name.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DeckNamingScreen_GetCharInfoFromPos */
static void adapt_DeckNamingScreen_GetCharInfoFromPos(ProbeState *s)
{
	s->hl = DeckNamingScreen_GetCharInfoFromPos(s->hl);
}
/* <<< factory DeckNamingScreen_GetCharInfoFromPos */

/* >>> factory ClearMemory_Bank6 */
static void adapt_ClearMemory_Bank6(ProbeState *s)
{
	ClearMemory_Bank6(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank6 */

/* >>> factory DrawTextboxForKeyboard */
static void adapt_DrawTextboxForKeyboard(ProbeState *s)
{
	DrawTextboxForKeyboard(&s->hl, s->a);
}
/* <<< factory DrawTextboxForKeyboard */

/* >>> factory TransformCharacter */
static void adapt_TransformCharacter(ProbeState *s)
{
	TransformCharacterResult r = TransformCharacter(s->hl, s->d, s->e);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory TransformCharacter */

/* >>> factory PlayerNamingScreen_GetCharInfoFromPos */
static void adapt_PlayerNamingScreen_GetCharInfoFromPos(ProbeState *s)
{
	s->hl = PlayerNamingScreen_GetCharInfoFromPos(s->hl);
}
/* <<< factory PlayerNamingScreen_GetCharInfoFromPos */

const ProbeEntry probe_entries_input_name[] = {
	{ "DeckNamingScreen_GetCharInfoFromPos", adapt_DeckNamingScreen_GetCharInfoFromPos },
	{ "ClearMemory_Bank6", adapt_ClearMemory_Bank6 },
	{ "DrawTextboxForKeyboard", adapt_DrawTextboxForKeyboard },
	{ "TransformCharacter", adapt_TransformCharacter },
	{ "PlayerNamingScreen_GetCharInfoFromPos", adapt_PlayerNamingScreen_GetCharInfoFromPos },
	{ NULL, NULL },
};
