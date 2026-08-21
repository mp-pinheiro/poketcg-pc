#include "home/printer.h"
#include "probe.h"

static void adapt_SendNextPrinterPacketByte(ProbeState *s)
{
	SendNextPrinterPacketByteResult r = SendNextPrinterPacketByte();
	s->d = r.d;
	s->e = r.e;
}

static void adapt_SendByteThroughSerialData(ProbeState *s)
{
	SendByteThroughSerialData(s->a);
}

static void adapt_ExecutePrinterPacketSequence(ProbeState *s)
{
	ExecutePrinterPacketSequenceResult r = ExecutePrinterPacketSequence(s->a, s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
}

/* >>> factory Func_1a14b */
static void adapt_Func_1a14b(ProbeState *s)
{
	Func_1a14bResult result = Func_1a14b(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory Func_1a14b */

const ProbeEntry probe_entries_printer[] = {
	{ "SendNextPrinterPacketByte", adapt_SendNextPrinterPacketByte },
	{ "SendByteThroughSerialData", adapt_SendByteThroughSerialData },
	{ "ExecutePrinterPacketSequence", adapt_ExecutePrinterPacketSequence },
	{ "Func_1a14b", adapt_Func_1a14b },
	{ NULL, NULL },
};
