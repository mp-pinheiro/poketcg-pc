#include "home/animation.h"
#include "probe.h"

static void adapt_ClearNumLoadedFramesetSubgroups(ProbeState *s)
{
	(void)s;
	ClearNumLoadedFramesetSubgroups();
}

static void adapt_ClearOWFramesetSubgroups(ProbeState *s)
{
	(void)s;
	ClearOWFramesetSubgroups();
}

static void adapt_GetOWFramesetSubgroupData(ProbeState *s)
{
	GetOWFramesetSubgroupData(s->hl, s->c);
}

static void adapt_LoadOWFramesetSubgroup(ProbeState *s)
{
	s->a = LoadOWFramesetSubgroup(s->c);
}

static void adapt_StoreOWFramesetSubgroup(ProbeState *s)
{
	StoreOWFramesetSubgroup(s->c);
}

/* >>> factory LoadOWFrameTiles */
static void adapt_LoadOWFrameTiles(ProbeState *s)
{
	(void)s;
	LoadOWFrameTiles();
}
/* <<< factory LoadOWFrameTiles */


const ProbeEntry probe_entries_animation[] = {
	{ "ClearNumLoadedFramesetSubgroups", adapt_ClearNumLoadedFramesetSubgroups },
	{ "ClearOWFramesetSubgroups", adapt_ClearOWFramesetSubgroups },
	{ "GetOWFramesetSubgroupData", adapt_GetOWFramesetSubgroupData },
	{ "LoadOWFramesetSubgroup", adapt_LoadOWFramesetSubgroup },
	{ "StoreOWFramesetSubgroup", adapt_StoreOWFramesetSubgroup },
	{ "LoadOWFrameTiles", adapt_LoadOWFrameTiles },
	{ NULL, NULL },
};
