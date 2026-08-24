#include "generated/hram.h"
#include "home/effect_commands.h"
#include "probe.h"

static void adapt_CheckMatchingCommand(ProbeState *s)
{
	uint16_t list = s->hl;
	uint8_t cmd = s->a;
	EffectCmdLookup r = CheckMatchingCommand(cmd, list);
	s->c = cmd;
	s->hl = r.hl;
	if (list == 0)
		s->f = 0x90u;
	else if (r.carry)
		s->f = 0x10u;
	else
		s->f = (uint8_t)(hBankROM == 0 ? 0x80u : 0u);
}

/* >>> factory TryExecuteEffectCommandFunction */
static void adapt_TryExecuteEffectCommandFunction(ProbeState *s)
{
	TryExecuteEffectCommandFunctionResult r = TryExecuteEffectCommandFunction(s->a);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory TryExecuteEffectCommandFunction */

const ProbeEntry probe_entries_effect_commands[] = {
	{ "CheckMatchingCommand", adapt_CheckMatchingCommand },
	{ "TryExecuteEffectCommandFunction", adapt_TryExecuteEffectCommandFunction },
	{ NULL, NULL },
};
