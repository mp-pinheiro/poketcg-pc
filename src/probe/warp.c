#include "home/warp.h"
#include "probe.h"
static void adapt_HandleMapWarp(ProbeState *s){HandleMapWarpResult r=_HandleMapWarp();s->a=r.a;s->f=r.f;}
const ProbeEntry probe_entries_warp[]={{"_HandleMapWarp",adapt_HandleMapWarp},{NULL,NULL}};
