#include "home/print_text.h"
#include "generated/wram.h"
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

static void adapt_GetTextOffsetFromTextID(ProbeState *s)
{
	s->hl = GetTextOffsetFromTextID(s->hl);
}

static void adapt_GetPointerToTextHeader(ProbeState *s)
{
	s->hl = GetPointerToTextHeader();
}

static void adapt_ReadTextHeader(ProbeState *s)
{
	s->hl = ReadTextHeader();
}

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

static void adapt_ResetTxRam_WriteToTextHeader(ProbeState *s)
{
	s->hl = ResetTxRam_WriteToTextHeader(s->hl);
}
static void adapt_TwoByteNumberToText_CountLeadingZeros(ProbeState *s)
{
	uint16_t text = 0;
	s->c = TwoByteNumberToText_CountLeadingZeros(s->hl, &text);
	if (wFontWidth)
		split(0xCAA5u, &s->d, &s->e);
	s->hl = text;
}
static void adapt_CopyText(ProbeState *s)
{
	uint16_t destination = pair(s->d, s->e);
	s->hl = CopyText(s->hl, &destination);
	split(destination, &s->d, &s->e);
}

static void adapt_CountLinesOfTextFromID(ProbeState *s)
{
	s->a = CountLinesOfTextFromID(s->hl);
}

static void adapt_LoadTxRam2(ProbeState *s)
{
	LoadTxRam2(s->hl);
}

static void adapt_LoadTxRam3(ProbeState *s)
{
	LoadTxRam3(s->hl);
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
	{ NULL, NULL },
};
