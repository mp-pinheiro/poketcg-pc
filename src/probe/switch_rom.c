#include "home/switch_rom.h"
#include "probe.h"

static void adapt_BankswitchROM(ProbeState *s)
{
	BankswitchROM(s->a);
}

/* >>> factory BankpushROM */
static void adapt_BankpushROM(ProbeState *s)
{
	BankpushROMResult r = BankpushROM(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory BankpushROM */

/* >>> factory BankpushROM2 */
static void adapt_BankpushROM2(ProbeState *s)
{
	BankpushROM2Result r = BankpushROM2(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory BankpushROM2 */

/* >>> factory BankpopROM */
static void adapt_BankpopROM(ProbeState *s)
{
	BankpopROMResult out = BankpopROM(s->b, s->c, s->d, s->e, s->hl, s->stack[0], s->stack[1]);
	s->a = out.a;
	s->f = out.f;
	s->b = out.b;
	s->c = out.c;
	s->d = out.d;
	s->e = out.e;
	s->hl = out.hl;
}
/* <<< factory BankpopROM */

const ProbeEntry probe_entries_switch_rom[] = {
	{ "BankswitchROM", adapt_BankswitchROM },
	{ "BankpushROM", adapt_BankpushROM },
	{ "BankpushROM2", adapt_BankpushROM2 },
	{ "BankpopROM", adapt_BankpopROM },
	{ NULL, NULL },
};
