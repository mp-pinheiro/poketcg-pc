#include "home/serial.h"
#include "probe.h"

static void adapt_SerialTimerHandler(ProbeState *s)
{
	(void)s;
	SerialTimerHandler();
}

const ProbeEntry probe_entries_serial[] = {
	{ "SerialTimerHandler", adapt_SerialTimerHandler },
	{ NULL, NULL },
};
