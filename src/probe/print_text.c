#include "home/print_text.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void split(uint16_t value, uint8_t *hi, uint8_t *lo)
{
	*hi = (uint8_t)(value >> 8);
	*lo = (uint8_t)value;
}

static void adapt_GetTextOffsetFromTextID(ProbeState *s) { s->hl = GetTextOffsetFromTextID(s->hl); }
static void adapt_GetPointerToTextHeader(ProbeState *s) { s->hl = GetPointerToTextHeader(); }
static void adapt_ReadTextHeader(ProbeState *s) { s->hl = ReadTextHeader(); }
static void adapt_WriteToTextHeader(ProbeState *s)
{
	uint16_t text = s->hl;
	s->hl = WriteToTextHeader(text);
	split(text, &s->b, &s->c);
}
static void adapt_WriteToTextHeader_MoveToNext(ProbeState *s)
{
	uint16_t text = s->hl;
	s->hl = WriteToTextHeader_MoveToNext(text);
	split(text, &s->b, &s->c);
}
static void adapt_ResetTxRam_WriteToTextHeader(ProbeState *s) { s->hl = ResetTxRam_WriteToTextHeader(s->hl); }
static void adapt_TwoByteNumberToText_CountLeadingZeros(ProbeState *s)
{
	LeadingZerosResult r = TwoByteNumberToText_CountLeadingZeros(s->hl, s->c, pair(s->d, s->e));
	s->c = r.c;
	split(r.de, &s->d, &s->e);
	s->hl = r.hl;
}
static void adapt_CopyText(ProbeState *s)
{
	CopyTextResult r = CopyText(s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
static void adapt_CountLinesOfTextFromID(ProbeState *s) { s->a = CountLinesOfTextFromID(s->hl); }
static void adapt_LoadTxRam2(ProbeState *s) { LoadTxRam2(s->hl); }
static void adapt_LoadTxRam3(ProbeState *s) { LoadTxRam3(s->hl); }
static void adapt_ProcessTextHeader(ProbeState *s)
{
	ProcessTextHeaderResult r = ProcessTextHeader(s->d, s->e);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_HandleTxRam2Or3(ProbeState *s)
{
	s->hl = HandleTxRam2Or3(pair(s->d, s->e), s->hl);
}

static void adapt_CopyTextData_FromTextID(ProbeState *s)
{
	CopyTextResult r = CopyTextData_FromTextID(s->a, s->hl, pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_CopyPlayerNameOrTurnDuelistName(ProbeState *s)
{
	CopyTextResult r = CopyPlayerNameOrTurnDuelistName();
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_InitTextPrinting_ProcessTextFromID(ProbeState *s)
{
	ProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromID(s->d, s->e, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_InitTextPrinting_ProcessTextFromPointerToID(ProbeState *s)
{
	ProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromPointerToID(s->d, s->e, s->hl);
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ProcessTextFromID(ProbeState *s)
{
	ProcessTextHeaderResult r = ProcessTextFromID(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_ProcessTextFromPointerToID(ProbeState *s)
{
	ProcessTextHeaderResult r = ProcessTextFromPointerToID(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

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
	{ NULL, NULL },
};
