/* >>> part includes */
#include "mem.h"
#include "probe.h"
/* <<< part includes */

/* >>> part MBC5ConformanceVector */
static void adapt_MBC5ConformanceVector(ProbeState *s)
{
	(void)s;
	mbc5_conformance_vector();
}
/* <<< part MBC5ConformanceVector */

/* >>> part probe_entries_mapper_conformance */
const ProbeEntry probe_entries_mapper_conformance[] = {
	{ "MBC5ConformanceVector", adapt_MBC5ConformanceVector },
	{ NULL, NULL },
};
/* <<< part probe_entries_mapper_conformance */
