#include "mem.h"
#include "probe.h"

static void adapt_MBC5ConformanceVector(ProbeState *s)
{
	(void)s;
	mbc5_conformance_vector();
}

const ProbeEntry probe_entries_mapper_conformance[] = {
	{ "MBC5ConformanceVector", adapt_MBC5ConformanceVector },
	{ NULL, NULL },
};
