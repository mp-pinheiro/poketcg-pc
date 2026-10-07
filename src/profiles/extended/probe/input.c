/* >>> part includes */
#include "home/input.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ReadJoypad */
static void adapt_ReadJoypad(ProbeState *s)
{
	(void)s;
	ReadJoypad();
}
/* <<< factory ReadJoypad */

/* >>> factory SaveButtonsHeld */
static void adapt_SaveButtonsHeld(ProbeState *s)
{
	SaveButtonsHeld(s->c);
}
/* <<< factory SaveButtonsHeld */

/* >>> factory ClearJoypad */
static void adapt_ClearJoypad(ProbeState *s)
{
	ClearJoypad(&s->hl);
}
/* <<< factory ClearJoypad */

/* >>> factory Reset */
static void adapt_Reset(ProbeState *s)
{
	s->a = wInitialA;
	(void)Reset();
}
/* <<< factory Reset */

/* >>> part probe_entries_input */
const ProbeEntry probe_entries_input[] = {
	{ "ReadJoypad", adapt_ReadJoypad },
	{ "SaveButtonsHeld", adapt_SaveButtonsHeld },
	{ "ClearJoypad", adapt_ClearJoypad },
	{ "Reset", adapt_Reset },
	{ NULL, NULL },
};
/* <<< part probe_entries_input */
