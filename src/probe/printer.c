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

const ProbeEntry probe_entries_printer[] = {
	{ "SendNextPrinterPacketByte", adapt_SendNextPrinterPacketByte },
	{ "SendByteThroughSerialData", adapt_SendByteThroughSerialData },
	{ "ExecutePrinterPacketSequence", adapt_ExecutePrinterPacketSequence },
	{ NULL, NULL },
};
