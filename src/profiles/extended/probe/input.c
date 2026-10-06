#include "home/input.h"
#include "probe.h"

static void adapt_ReadJoypad(ProbeState *s)
{
	(void)s;
	ReadJoypad();
}

static void adapt_SaveButtonsHeld(ProbeState *s)
{
	SaveButtonsHeld(s->c);
}

static void adapt_ClearJoypad(ProbeState *s)
{
	ClearJoypad(&s->hl);
}

/* >>> factory Reset */
static void adapt_Reset(ProbeState *s)
{
	s->a = Reset();
}
/* <<< factory Reset */

const ProbeEntry probe_entries_input[] = {
	{ "ReadJoypad", adapt_ReadJoypad },
	{ "SaveButtonsHeld", adapt_SaveButtonsHeld },
	{ "ClearJoypad", adapt_ClearJoypad },
	{ "Reset", adapt_Reset },
	{ NULL, NULL },
};
