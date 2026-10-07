/* >>> part includes */
#include "home/warp.h"
#include "probe.h"
/* <<< part includes */
/* >>> factory _HandleMapWarp */
static void adapt_HandleMapWarp(ProbeState *s){HandleMapWarpResult r=_HandleMapWarp();s->a=r.a;s->f=r.f;}
/* <<< factory _HandleMapWarp */
/* >>> part probe_entries_warp */
const ProbeEntry probe_entries_warp[]={{"_HandleMapWarp",adapt_HandleMapWarp},{NULL,NULL}};
/* <<< part probe_entries_warp */
