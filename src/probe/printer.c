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

/* >>> factory PrinterMenu_QuitPrint */
static void adapt_PrinterMenu_QuitPrint(ProbeState *s)
{
	s->f = PrinterMenu_QuitPrint(s->stack[0]);
}
/* <<< factory PrinterMenu_QuitPrint */

/* >>> factory DrawBottomCardInfoInSRAMGfxBuffer0 */
static void adapt_DrawBottomCardInfoInSRAMGfxBuffer0(ProbeState *s)
{
	(void)s;
	DrawBottomCardInfoInSRAMGfxBuffer0();
}
/* <<< factory DrawBottomCardInfoInSRAMGfxBuffer0 */

/* >>> factory ShowPrinterTransmitting */
static void adapt_ShowPrinterTransmitting(ProbeState *s)
{
	(void)s;
	ShowPrinterTransmitting();
}
/* <<< factory ShowPrinterTransmitting */


/* >>> factory SendPrinterPacket */
static void adapt_SendPrinterPacket(ProbeState *s)
{
	SendPrinterPacketResult r = SendPrinterPacket(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory SendPrinterPacket */

/* >>> factory SendTilesToPrinter */
static void adapt_SendTilesToPrinter(ProbeState *s)
{
	SendTilesToPrinterResult r = SendTilesToPrinter(s->hl, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SendTilesToPrinter */


/* >>> factory ShowPrinterConnectionErrorScene */
static void adapt_ShowPrinterConnectionErrorScene(ProbeState *s)
{
	ShowPrinterConnectionErrorSceneResult r = ShowPrinterConnectionErrorScene(s->a, s->f, s->d, s->e, s->hl);
	s->f = r.f;
}
/* <<< factory ShowPrinterConnectionErrorScene */

/* >>> factory TryInitPrinterCommunications */
static void adapt_TryInitPrinterCommunications(ProbeState *s)
{
	TryInitPrinterCommunicationsResult r = TryInitPrinterCommunications();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory TryInitPrinterCommunications */

/* >>> factory ShowPrinterIsNotConnected */
static void adapt_ShowPrinterIsNotConnected(ProbeState *s)
{
	ShowPrinterIsNotConnectedResult result = ShowPrinterIsNotConnected(s->a, s->f, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory ShowPrinterIsNotConnected */

/* >>> factory HandlePrinterError */
static void adapt_HandlePrinterError(ProbeState *s)
{
	HandlePrinterErrorResult result = HandlePrinterError(s->f, s->d, s->e);
	s->f = result.f;
}
/* <<< factory HandlePrinterError */

/* >>> factory SendPrinterInstructionPacket */
static void adapt_SendPrinterInstructionPacket(ProbeState *s)
{
	SendPrinterInstructionPacketResult result = SendPrinterInstructionPacket(s->hl, s->stack[0]);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory SendPrinterInstructionPacket */

/* >>> factory SendPrinterInstructionPacket_1Sheet */
static void adapt_SendPrinterInstructionPacket_1Sheet(ProbeState *s)
{
	SendPrinterInstructionPacket_1SheetResult result = SendPrinterInstructionPacket_1Sheet();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory SendPrinterInstructionPacket_1Sheet */

/* >>> factory SendPrinterInstructionPacket_1Sheet_3LineFeeds */
static void adapt_SendPrinterInstructionPacket_1Sheet_3LineFeeds(ProbeState *s)
{
	SendPrinterInstructionPacket_1SheetResult result =
		SendPrinterInstructionPacket_1Sheet_3LineFeeds();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory SendPrinterInstructionPacket_1Sheet_3LineFeeds */

/* >>> factory LoadGfxBufferForPrinter */
static void adapt_LoadGfxBufferForPrinter(ProbeState *s)
{
	LoadGfxBufferForPrinterResult result = LoadGfxBufferForPrinter(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory LoadGfxBufferForPrinter */

/* >>> factory AddToPrinterGfxBuffer */
static void adapt_AddToPrinterGfxBuffer(ProbeState *s)
{
	AddToPrinterGfxBufferResult result = AddToPrinterGfxBuffer(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory AddToPrinterGfxBuffer */

/* >>> factory _PreparePrinterConnection */
static void adapt__PreparePrinterConnection(ProbeState *s)
{
	PreparePrinterConnectionResult result = _PreparePrinterConnection(s->hl);
	s->f = result.f;
}
/* <<< factory _PreparePrinterConnection */

/* >>> factory SendCardListToPrinter */
static void adapt_SendCardListToPrinter(ProbeState *s)
{
	SendCardListToPrinterResult result = SendCardListToPrinter(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory SendCardListToPrinter */

/* >>> factory Func_19f87 */
static void adapt_Func_19f87(ProbeState *s)
{
	(void)s;
	Func_19f87Result result = Func_19f87();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_19f87 */

/* >>> factory Func_1a011 */
static void adapt_Func_1a011(ProbeState *s)
{
	Func_1a011Result result = Func_1a011();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_1a011 */

/* >>> factory Func_19f99 */
static void adapt_Func_19f99(ProbeState *s)
{
	Func_19f99Result result = Func_19f99();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_19f99 */

/* >>> factory _PrintDeckConfiguration */
static void adapt__PrintDeckConfiguration(ProbeState *s)
{
	_PrintDeckConfiguration(s->a);
}
/* <<< factory _PrintDeckConfiguration */

/* >>> factory Func_1a080 */
static void adapt_Func_1a080(ProbeState *s)
{
	Func_1a080Result r = Func_1a080(s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_1a080 */

/* >>> factory _RequestToPrintCard */
static void adapt__RequestToPrintCard(ProbeState *s)
{
	RequestToPrintCardResult result = _RequestToPrintCard(s->a);
	s->f = result.f;
}
/* <<< factory _RequestToPrintCard */

/* >>> factory _PrintCardList */
static void adapt__PrintCardList(ProbeState *s)
{
	PrintCardListResult result = _PrintCardList();
	s->f = result.f;
}
/* <<< factory _PrintCardList */

/* >>> factory PrinterMenu_CardList */
static void adapt_PrinterMenu_CardList(ProbeState *s)
{
	PrinterMenu_CardList();
	(void)s;
}
/* <<< factory PrinterMenu_CardList */

/* >>> factory PrinterMenu_PokemonCards */
static void adapt_PrinterMenu_PokemonCards(ProbeState *s)
{
	PrinterMenu_PokemonCards();
}
/* <<< factory PrinterMenu_PokemonCards */

const ProbeEntry probe_entries_printer[] = {
	{ "ShowPrinterConnectionErrorScene", adapt_ShowPrinterConnectionErrorScene },
	{ "SendPrinterPacket", adapt_SendPrinterPacket },
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
	{ "PrinterMenu_QuitPrint", adapt_PrinterMenu_QuitPrint },
	{ "DrawBottomCardInfoInSRAMGfxBuffer0", adapt_DrawBottomCardInfoInSRAMGfxBuffer0 },
	{ "ShowPrinterTransmitting", adapt_ShowPrinterTransmitting },
	{ "TryInitPrinterCommunications", adapt_TryInitPrinterCommunications },
	{ "ShowPrinterIsNotConnected", adapt_ShowPrinterIsNotConnected },
	{ "HandlePrinterError", adapt_HandlePrinterError },
	{ "SendTilesToPrinter", adapt_SendTilesToPrinter },
	{ "SendPrinterInstructionPacket", adapt_SendPrinterInstructionPacket },
	{ "SendPrinterInstructionPacket_1Sheet", adapt_SendPrinterInstructionPacket_1Sheet },
	{ "SendPrinterInstructionPacket_1Sheet_3LineFeeds", adapt_SendPrinterInstructionPacket_1Sheet_3LineFeeds },
	{ "LoadGfxBufferForPrinter", adapt_LoadGfxBufferForPrinter },
	{ "AddToPrinterGfxBuffer", adapt_AddToPrinterGfxBuffer },
	{ "_PreparePrinterConnection", adapt__PreparePrinterConnection },
	{ "SendCardListToPrinter", adapt_SendCardListToPrinter },
	{ "Func_19f87", adapt_Func_19f87 },
	{ "Func_1a011", adapt_Func_1a011 },
	{ "Func_19f99", adapt_Func_19f99 },
	{ "_PrintDeckConfiguration", adapt__PrintDeckConfiguration },
	{ "Func_1a080", adapt_Func_1a080 },
	{ "_RequestToPrintCard", adapt__RequestToPrintCard },
	{ "_PrintCardList", adapt__PrintCardList },
	{ "PrinterMenu_CardList", adapt_PrinterMenu_CardList },
	{ "PrinterMenu_PokemonCards", adapt_PrinterMenu_PokemonCards },
	{ NULL, NULL },
};
