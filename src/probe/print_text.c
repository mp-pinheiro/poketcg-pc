/* >>> part includes */
#include "home/print_text.h"
#include "probe.h"
/* <<< part includes */

/* >>> part pair */
static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}
/* <<< part pair */

/* >>> part split */
static void split(uint16_t value, uint8_t *hi, uint8_t *lo)
{
	*hi = (uint8_t)(value >> 8);
	*lo = (uint8_t)value;
}
/* <<< part split */

/* >>> factory GetTextOffsetFromTextID */
static void adapt_GetTextOffsetFromTextID(ProbeState *s) { s->hl = GetTextOffsetFromTextID(s->hl); }
/* <<< factory GetTextOffsetFromTextID */
/* >>> factory GetPointerToTextHeader */
static void adapt_GetPointerToTextHeader(ProbeState *s) { s->hl = GetPointerToTextHeader(); }
/* <<< factory GetPointerToTextHeader */
/* >>> factory ReadTextHeader */
static void adapt_ReadTextHeader(ProbeState *s) { s->hl = ReadTextHeader(); }
/* <<< factory ReadTextHeader */
/* >>> factory WriteToTextHeader */
static void adapt_WriteToTextHeader(ProbeState *s)
{
	TextHeaderWrite r = WriteToTextHeader(s->hl);
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory WriteToTextHeader */
/* >>> factory WriteToTextHeader_MoveToNext */
static void adapt_WriteToTextHeader_MoveToNext(ProbeState *s)
{
	TextHeaderWrite r = WriteToTextHeader_MoveToNext(s->hl);
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory WriteToTextHeader_MoveToNext */
/* >>> factory ResetTxRam_WriteToTextHeader */
static void adapt_ResetTxRam_WriteToTextHeader(ProbeState *s)
{
	TextHeaderWrite r = ResetTxRam_WriteToTextHeader(s->hl);
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ResetTxRam_WriteToTextHeader */
/* >>> factory TwoByteNumberToText_CountLeadingZeros */
static void adapt_TwoByteNumberToText_CountLeadingZeros(ProbeState *s)
{
	LeadingZerosResult r = TwoByteNumberToText_CountLeadingZeros(s->hl, s->c, pair(s->d, s->e));
	s->c = r.c;
	split(r.de, &s->d, &s->e);
	s->hl = r.hl;
}
/* <<< factory TwoByteNumberToText_CountLeadingZeros */
/* >>> factory CopyText */
static void adapt_CopyText(ProbeState *s)
{
	CopyTextResult r = CopyText(s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CopyText */
/* >>> factory CountLinesOfTextFromID */
static void adapt_CountLinesOfTextFromID(ProbeState *s) { s->a = CountLinesOfTextFromID(s->hl); }
/* <<< factory CountLinesOfTextFromID */
/* >>> factory LoadTxRam2 */
static void adapt_LoadTxRam2(ProbeState *s) { LoadTxRam2(s->hl); }
/* <<< factory LoadTxRam2 */
/* >>> factory LoadTxRam3 */
static void adapt_LoadTxRam3(ProbeState *s) { LoadTxRam3(s->hl); }
/* <<< factory LoadTxRam3 */
/* >>> factory ProcessTextHeader */
static void adapt_ProcessTextHeader(ProbeState *s)
{
	ProcessTextHeaderResult r = ProcessTextHeader(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ProcessTextHeader */

/* >>> factory HandleTxRam2Or3 */
static void adapt_HandleTxRam2Or3(ProbeState *s)
{
	TxRamSlot r = HandleTxRam2Or3(pair(s->d, s->e), s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory HandleTxRam2Or3 */

/* >>> factory CopyTextData_FromTextID */
static void adapt_CopyTextData_FromTextID(ProbeState *s)
{
	CopyTextResult r = CopyTextData_FromTextID(s->a, s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CopyTextData_FromTextID */

/* >>> factory CopyPlayerNameOrTurnDuelistName */
static void adapt_CopyPlayerNameOrTurnDuelistName(ProbeState *s)
{
	CopyTextResult r = CopyPlayerNameOrTurnDuelistName();
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CopyPlayerNameOrTurnDuelistName */

/* >>> factory InitTextPrinting_ProcessTextFromID */
static void adapt_InitTextPrinting_ProcessTextFromID(ProbeState *s)
{
	ProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromID(s->d, s->e, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory InitTextPrinting_ProcessTextFromID */

/* >>> factory InitTextPrinting_ProcessTextFromPointerToID */
static void adapt_InitTextPrinting_ProcessTextFromPointerToID(ProbeState *s)
{
	ProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromPointerToID(s->d, s->e, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory InitTextPrinting_ProcessTextFromPointerToID */

/* >>> factory ProcessTextFromID */
static void adapt_ProcessTextFromID(ProbeState *s)
{
	ProcessTextHeaderResult r = ProcessTextFromID(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ProcessTextFromID */

/* >>> factory ProcessTextFromPointerToID */
static void adapt_ProcessTextFromPointerToID(ProbeState *s)
{
	ProcessTextHeaderResult r = ProcessTextFromPointerToID(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ProcessTextFromPointerToID */

/* >>> factory PlaceTextItems */
static void adapt_PlaceTextItems(ProbeState *s)
{
	TextResult r = PlaceTextItems(s->hl);
	s->d = r.d;
	s->hl = r.hl;
}
/* <<< factory PlaceTextItems */

/* >>> factory PrintText */
static void adapt_PrintText(ProbeState *s)
{
	TextResult r = PrintText(s->hl, s->d, s->e);
	s->hl = r.hl;
}
/* <<< factory PrintText */

/* >>> factory PrintTextNoDelay */
static void adapt_PrintTextNoDelay(ProbeState *s)
{
	TextResult r = PrintTextNoDelay(s->hl, s->d, s->e);
	s->hl = r.hl;
}
/* <<< factory PrintTextNoDelay */

/* >>> factory DrawTextReadyLabeledOrRegularTextBox */
static void adapt_DrawTextReadyLabeledOrRegularTextBox(ProbeState *s)
{
	TextResult r = DrawTextReadyLabeledOrRegularTextBox(s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DrawTextReadyLabeledOrRegularTextBox */

/* >>> factory WaitForPlayerToAdvanceText */
static void adapt_WaitForPlayerToAdvanceText(ProbeState *s)
{
	s->f = WaitForPlayerToAdvanceText().f;
}
/* <<< factory WaitForPlayerToAdvanceText */

/* >>> factory PrintScrollableText */
static void adapt_PrintScrollableText(ProbeState *s)
{
	TextResult r = PrintScrollableText(s->a, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PrintScrollableText */

/* >>> factory PrintScrollableText_NoTextBoxLabel */
static void adapt_PrintScrollableText_NoTextBoxLabel(ProbeState *s)
{
	s->f = PrintScrollableText_NoTextBoxLabel(s->hl).f;
}
/* <<< factory PrintScrollableText_NoTextBoxLabel */

/* >>> factory PrintScrollableText_WithTextBoxLabel_NoWait */
static void adapt_PrintScrollableText_WithTextBoxLabel_NoWait(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	TextResult r = PrintScrollableText_WithTextBoxLabel_NoWait(s->hl, de);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PrintScrollableText_WithTextBoxLabel_NoWait */

/* >>> factory PrintScrollableText_WithTextBoxLabel */
static void adapt_PrintScrollableText_WithTextBoxLabel(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	s->f = PrintScrollableText_WithTextBoxLabel(s->hl, de).f;
}
/* <<< factory PrintScrollableText_WithTextBoxLabel */

/* >>> part probe_entries_print_text */
const ProbeEntry probe_entries_print_text[] = {
	{ "GetTextOffsetFromTextID", adapt_GetTextOffsetFromTextID },
	{ "GetPointerToTextHeader", adapt_GetPointerToTextHeader },
	{ "ReadTextHeader", adapt_ReadTextHeader },
	{ "WriteToTextHeader", adapt_WriteToTextHeader },
	{ "WriteToTextHeader_MoveToNext", adapt_WriteToTextHeader_MoveToNext },
	{ "ResetTxRam_WriteToTextHeader", adapt_ResetTxRam_WriteToTextHeader },
	{ "TwoByteNumberToText_CountLeadingZeros", adapt_TwoByteNumberToText_CountLeadingZeros },
	{ "CopyText", adapt_CopyText },
	{ "CountLinesOfTextFromID", adapt_CountLinesOfTextFromID },
	{ "LoadTxRam2", adapt_LoadTxRam2 },
	{ "LoadTxRam3", adapt_LoadTxRam3 },
	{ "ProcessTextHeader", adapt_ProcessTextHeader },
	{ "HandleTxRam2Or3", adapt_HandleTxRam2Or3 },
	{ "CopyTextData_FromTextID", adapt_CopyTextData_FromTextID },
	{ "CopyPlayerNameOrTurnDuelistName", adapt_CopyPlayerNameOrTurnDuelistName },
	{ "InitTextPrinting_ProcessTextFromID", adapt_InitTextPrinting_ProcessTextFromID },
	{ "InitTextPrinting_ProcessTextFromPointerToID", adapt_InitTextPrinting_ProcessTextFromPointerToID },
	{ "ProcessTextFromID", adapt_ProcessTextFromID },
	{ "ProcessTextFromPointerToID", adapt_ProcessTextFromPointerToID },
	{ "PlaceTextItems", adapt_PlaceTextItems },
	{ "PrintText", adapt_PrintText },
	{ "PrintTextNoDelay", adapt_PrintTextNoDelay },
	{ "DrawTextReadyLabeledOrRegularTextBox", adapt_DrawTextReadyLabeledOrRegularTextBox },
	{ "WaitForPlayerToAdvanceText", adapt_WaitForPlayerToAdvanceText },
	{ "PrintScrollableText", adapt_PrintScrollableText },
	{ "PrintScrollableText_NoTextBoxLabel", adapt_PrintScrollableText_NoTextBoxLabel },
	{ "PrintScrollableText_WithTextBoxLabel_NoWait", adapt_PrintScrollableText_WithTextBoxLabel_NoWait },
	{ "PrintScrollableText_WithTextBoxLabel", adapt_PrintScrollableText_WithTextBoxLabel },
	{ NULL, NULL },
};
/* <<< part probe_entries_print_text */
