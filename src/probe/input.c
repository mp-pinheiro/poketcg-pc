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

const ProbeEntry probe_entries_input[] = {
	{ "ReadJoypad", adapt_ReadJoypad },
	{ "SaveButtonsHeld", adapt_SaveButtonsHeld },
	{ "ClearJoypad", adapt_ClearJoypad },
	{ NULL, NULL },
};
