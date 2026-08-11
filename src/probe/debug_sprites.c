#include "home/debug_sprites.h"
#include "probe.h"
#include "generated/hram.h"
#include "mem.h"

static void adapt_Func_1c865(ProbeState *s)
{
	Func_1c865();
}

static void adapt_Func_1c866(ProbeState *s)
{
	Func_1c866();
	s->a = gb_read8(hSCY_ADDR);
	s->b = gb_read8(hSCX_ADDR);
	s->c = gb_read8(hSCY_ADDR);
}

static void adapt_Func_1c890(ProbeState *s)
{
	s->a = Func_1c890(&s->c, &s->hl);
}

const ProbeEntry probe_entries_debug_sprites[] = {
	{ "Func_1c865", adapt_Func_1c865 },
	{ "Func_1c866", adapt_Func_1c866 },
	{ "Func_1c890", adapt_Func_1c890 },
	{ NULL, NULL },
};
