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

/* >>> factory Func_1a025 */
static void adapt_Func_1a025(ProbeState *s)
{
	Func_1a025();
	(void)s;
}
/* <<< factory Func_1a025 */

/* >>> factory ResetPrinterCommunicationSettings */
static void adapt_ResetPrinterCommunicationSettings(ProbeState *s)
{
	ResetPrinterCommunicationSettingsResult result = ResetPrinterCommunicationSettings(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ResetPrinterCommunicationSettings */

/* >>> factory ClearPrinterGfxBuffer */
static void adapt_ClearPrinterGfxBuffer(ProbeState *s)
{
	ClearPrinterGfxBufferResult result = ClearPrinterGfxBuffer(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ClearPrinterGfxBuffer */

/* >>> factory GetPrinterContrastSerialData */
static void adapt_GetPrinterContrastSerialData(ProbeState *s)
{
	GetPrinterContrastSerialDataResult r = GetPrinterContrastSerialData();
	s->a = r.a;
	s->hl = r.hl;
}
/* <<< factory GetPrinterContrastSerialData */

/* >>> factory PrepareForPrinterCommunications */
static void adapt_PrepareForPrinterCommunications(ProbeState *s)
{
	PrepareForPrinterCommunicationsResult r = PrepareForPrinterCommunications(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PrepareForPrinterCommunications */

/* >>> factory CheckDataCompression */
static void adapt_CheckDataCompression(ProbeState *s)
{
	CheckDataCompressionResult r = CheckDataCompression(s->c, s->hl);
	s->a = r.a; s->e = r.e; s->f = r.f; s->hl = r.hl;
}
/* <<< factory CheckDataCompression */

/* >>> factory CompressDataForPrinterSerialTransfer */
static void adapt_CompressDataForPrinterSerialTransfer(ProbeState *s)
{
	CompressDataForPrinterSerialTransferResult r = CompressDataForPrinterSerialTransfer();
	s->b = (uint8_t)(r.bc >> 8); s->c = (uint8_t)r.bc;
	s->hl = r.hl; s->d = r.d; s->e = r.e;
}
/* <<< factory CompressDataForPrinterSerialTransfer */

/* >>> factory LoadCardInfoForPrinter */
static void adapt_LoadCardInfoForPrinter(ProbeState *s)
{
	LoadCardInfoForPrinter(s->b, s->c, &s->hl);
}
/* <<< factory LoadCardInfoForPrinter */

const ProbeEntry probe_entries_printer[] = {
	{ "SendNextPrinterPacketByte", adapt_SendNextPrinterPacketByte },
	{ "SendByteThroughSerialData", adapt_SendByteThroughSerialData },
	{ "ExecutePrinterPacketSequence", adapt_ExecutePrinterPacketSequence },
	{ "Func_1a14b", adapt_Func_1a14b },
	{ "Func_1a025", adapt_Func_1a025 },
	{ "ResetPrinterCommunicationSettings", adapt_ResetPrinterCommunicationSettings },
	{ "ClearPrinterGfxBuffer", adapt_ClearPrinterGfxBuffer },
	{ "GetPrinterContrastSerialData", adapt_GetPrinterContrastSerialData },
	{ "PrepareForPrinterCommunications", adapt_PrepareForPrinterCommunications },
	{ "CheckDataCompression", adapt_CheckDataCompression },
	{ "CompressDataForPrinterSerialTransfer", adapt_CompressDataForPrinterSerialTransfer },
	{ "LoadCardInfoForPrinter", adapt_LoadCardInfoForPrinter },
	{ NULL, NULL },
};
