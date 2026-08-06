#include "home/memory.h"
#include "generated/hram.h"
#include "probe.h"

/* Both wrappers exit with `a` holding the bank they restored (memory.asm:12,29). */
static void adapt_DecompressDataFromBank(ProbeState *s)
{
	DecompressDataFromBank((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
	s->a = hBankROM;
}

static void adapt_CopyBankedDataToDE(ProbeState *s)
{
	CopyBankedDataToDE((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
	s->a = hBankROM;
}

static void adapt_FillMemoryWithA(ProbeState *s)
{
	FillMemoryWithA(s->hl, (uint16_t)(s->b << 8 | s->c), s->a);
}

static void adapt_FillMemoryWithDE(ProbeState *s)
{
	FillMemoryWithDE(s->hl, (uint16_t)(s->b << 8 | s->c), s->d, s->e);
}

static void adapt_GetFarByte(ProbeState *s)
{
	s->a = GetFarByte(s->a, s->hl);
}

const ProbeEntry probe_entries_memory[] = {
	{ "DecompressDataFromBank", adapt_DecompressDataFromBank },
	{ "CopyBankedDataToDE", adapt_CopyBankedDataToDE },
	{ "FillMemoryWithA", adapt_FillMemoryWithA },
	{ "FillMemoryWithDE", adapt_FillMemoryWithDE },
	{ "GetFarByte", adapt_GetFarByte },
	{ NULL, NULL },
};
