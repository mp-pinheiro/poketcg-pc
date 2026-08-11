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

const ProbeEntry probe_entries_animation[] = {
	{ "ClearNumLoadedFramesetSubgroups", adapt_ClearNumLoadedFramesetSubgroups },
	{ "ClearOWFramesetSubgroups", adapt_ClearOWFramesetSubgroups },
	{ "GetOWFramesetSubgroupData", adapt_GetOWFramesetSubgroupData },
	{ "LoadOWFramesetSubgroup", adapt_LoadOWFramesetSubgroup },
	{ "StoreOWFramesetSubgroup", adapt_StoreOWFramesetSubgroup },
	{ NULL, NULL },
};
