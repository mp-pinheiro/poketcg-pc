/* >>> part includes */
#include "home/medal.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ShowMedalReceivedScreen */
static void adapt_ShowMedalReceivedScreen(ProbeState *s)
{
	ShowMedalReceivedScreen(s->a);
}
/* <<< factory ShowMedalReceivedScreen */

/* >>> part probe_entries_medal */
const ProbeEntry probe_entries_medal[] = {
	{ "ShowMedalReceivedScreen", adapt_ShowMedalReceivedScreen },
	{ NULL, NULL },
};
/* <<< part probe_entries_medal */
