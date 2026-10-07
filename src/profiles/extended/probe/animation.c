/* >>> part includes */
#include "home/animation.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ClearNumLoadedFramesetSubgroups */
static void adapt_ClearNumLoadedFramesetSubgroups(ProbeState *s)
{
	(void)s;
	ClearNumLoadedFramesetSubgroups();
}
/* <<< factory ClearNumLoadedFramesetSubgroups */

/* >>> factory ClearOWFramesetSubgroups */
static void adapt_ClearOWFramesetSubgroups(ProbeState *s)
{
	(void)s;
	ClearOWFramesetSubgroups();
}
/* <<< factory ClearOWFramesetSubgroups */

/* >>> factory GetOWFramesetSubgroupData */
static void adapt_GetOWFramesetSubgroupData(ProbeState *s)
{
	GetOWFramesetSubgroupData(s->hl, s->c);
}
/* <<< factory GetOWFramesetSubgroupData */

/* >>> factory LoadOWFramesetSubgroup */
static void adapt_LoadOWFramesetSubgroup(ProbeState *s)
{
	s->a = LoadOWFramesetSubgroup(s->c);
}
/* <<< factory LoadOWFramesetSubgroup */

/* >>> factory StoreOWFramesetSubgroup */
static void adapt_StoreOWFramesetSubgroup(ProbeState *s)
{
	StoreOWFramesetSubgroup(s->c);
}
/* <<< factory StoreOWFramesetSubgroup */

/* >>> factory LoadOWFrameTiles */
static void adapt_LoadOWFrameTiles(ProbeState *s)
{
	(void)s;
	LoadOWFrameTiles();
}
/* <<< factory LoadOWFrameTiles */


/* >>> factory DoLoadedFramesetSubgroupsFrame */
static void adapt_DoLoadedFramesetSubgroupsFrame(ProbeState *s)
{
	(void)s;
	DoLoadedFramesetSubgroupsFrame();
}
/* <<< factory DoLoadedFramesetSubgroupsFrame */

/* >>> factory ProcessOWFrameset */
static void adapt_ProcessOWFrameset(ProbeState *s)
{
	ProcessOWFrameset(s->hl);
}
/* <<< factory ProcessOWFrameset */

/* >>> factory DoMapOWFrame */
static void adapt_DoMapOWFrame(ProbeState *s)
{
	(void)s;
	DoMapOWFrame();
}
/* <<< factory DoMapOWFrame */

/* >>> part probe_entries_animation */
const ProbeEntry probe_entries_animation[] = {
	{ "ClearNumLoadedFramesetSubgroups", adapt_ClearNumLoadedFramesetSubgroups },
	{ "ClearOWFramesetSubgroups", adapt_ClearOWFramesetSubgroups },
	{ "GetOWFramesetSubgroupData", adapt_GetOWFramesetSubgroupData },
	{ "LoadOWFramesetSubgroup", adapt_LoadOWFramesetSubgroup },
	{ "StoreOWFramesetSubgroup", adapt_StoreOWFramesetSubgroup },
	{ "LoadOWFrameTiles", adapt_LoadOWFrameTiles },
	{ "DoLoadedFramesetSubgroupsFrame", adapt_DoLoadedFramesetSubgroupsFrame },
	{ "ProcessOWFrameset", adapt_ProcessOWFrameset },
	{ "DoMapOWFrame", adapt_DoMapOWFrame },
	{ NULL, NULL },
};
/* <<< part probe_entries_animation */
