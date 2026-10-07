/* >>> part includes */
#include "home/clear_sram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ClearSRAMBank */
static void adapt_ClearSRAMBank(ProbeState *s)
{
	ClearSRAMResult result = ClearSRAMBank(s->a, s->f);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory ClearSRAMBank */

/* >>> factory RestartSRAM */
static void adapt_RestartSRAM(ProbeState *s)
{
	ClearSRAMResult result = RestartSRAM();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory RestartSRAM */

/* >>> factory ValidateSRAM */
static void adapt_ValidateSRAM(ProbeState *s)
{
	(void)s;
	ValidateSRAM();
}
/* <<< factory ValidateSRAM */

/* >>> part probe_entries_clear_sram */
const ProbeEntry probe_entries_clear_sram[] = {
	{ "ClearSRAMBank", adapt_ClearSRAMBank },
	{ "RestartSRAM", adapt_RestartSRAM },
	{ "ValidateSRAM", adapt_ValidateSRAM },
	{ NULL, NULL },
};
/* <<< part probe_entries_clear_sram */
