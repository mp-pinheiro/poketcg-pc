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

const ProbeEntry probe_entries_input_name[] = {
	{ "DeckNamingScreen_GetCharInfoFromPos", adapt_DeckNamingScreen_GetCharInfoFromPos },
	{ "ClearMemory_Bank6", adapt_ClearMemory_Bank6 },
	{ "DrawTextboxForKeyboard", adapt_DrawTextboxForKeyboard },
	{ NULL, NULL },
};
