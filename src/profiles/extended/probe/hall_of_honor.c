/* >>> part includes */
#include "home/hall_of_honor.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory HallOfHonorLoadMap */
static void adapt_HallOfHonorLoadMap(ProbeState *s)
{
	(void)s;
	HallOfHonorLoadMap();
}
/* <<< factory HallOfHonorLoadMap */

/* >>> part probe_entries_hall_of_honor */
const ProbeEntry probe_entries_hall_of_honor[] = {
	{ "HallOfHonorLoadMap", adapt_HallOfHonorLoadMap },
	{ NULL, NULL },
};
/* <<< part probe_entries_hall_of_honor */
