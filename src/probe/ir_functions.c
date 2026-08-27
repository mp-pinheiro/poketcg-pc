#include "home/ir_functions.h"
#include "probe.h"

static void adapt_PlayCardPopSong(ProbeState *s)
{
	PlayCardPopSong();
	(void)s;
}

/* >>> factory InitIRCommunications */
static void adapt_InitIRCommunications(ProbeState *s)
{
	InitIRCommunications(s->a);
}
/* <<< factory InitIRCommunications */


/* >>> factory LoadLinkConnectingScene */
static void adapt_LoadLinkConnectingScene(ProbeState *s)
{
	LoadLinkConnectingScene(s->hl);
}
/* <<< factory LoadLinkConnectingScene */

/* >>> factory ClearRPAndRestoreVBlankFunction */
static void adapt_ClearRPAndRestoreVBlankFunction(ProbeState *s)
{
	(void)s;
	ClearRPAndRestoreVBlankFunction();
}
/* <<< factory ClearRPAndRestoreVBlankFunction */

const ProbeEntry probe_entries_ir_functions[] = {
	{ "PlayCardPopSong", adapt_PlayCardPopSong },
	{ "InitIRCommunications", adapt_InitIRCommunications },
	{ "LoadLinkConnectingScene", adapt_LoadLinkConnectingScene },
	{ "ClearRPAndRestoreVBlankFunction", adapt_ClearRPAndRestoreVBlankFunction },
	{ NULL, NULL },
};
