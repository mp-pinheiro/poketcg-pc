/* >>> part includes */
#include "home/input.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */
/* >>> factory Reset */
static void adapt_Reset(ProbeState *s)
{
	s->a = wInitialA;
	(void)Reset();
}
/* <<< factory Reset */
