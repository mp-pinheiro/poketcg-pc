#include "home/write_number.h"
#include "probe.h"

static void adapt_TwoByteNumberToText(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TwoByteNumberToText(s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

static void adapt_WriteBCDDigitInTextFormat(ProbeState *s)
{
	s->a = WriteBCDDigitInTextFormat(s->a, &s->hl);
}

static void adapt_WriteBCDNumberInTextFormat(ProbeState *s)
{
	s->a = WriteBCDNumberInTextFormat(s->a, &s->hl);
}

static void adapt_WriteTwoDigitBCDNumber(ProbeState *s)
{
	WriteTwoDigitBCDNumber(s->a, s->b, s->c);
}

static void adapt_WriteFourDigitBCDNumber(ProbeState *s)
{
	WriteFourDigitBCDNumber(s->hl, s->b, s->c);
}

static void adapt_WriteOneDigitBCDNumber(ProbeState *s)
{
	WriteOneDigitBCDNumber(s->a, s->b, s->c);
}

static void adapt_WriteOneByteNumber(ProbeState *s)
{
	WriteOneByteNumber(s->a, s->b, s->c);
}

static void adapt_WriteTwoByteNumber(ProbeState *s)
{
	WriteTwoByteNumber(s->hl, s->b, s->c);
}

const ProbeEntry probe_entries_write_number[] = {
	{ "TwoByteNumberToText", adapt_TwoByteNumberToText },
	{ "WriteBCDDigitInTextFormat", adapt_WriteBCDDigitInTextFormat },
	{ "WriteBCDNumberInTextFormat", adapt_WriteBCDNumberInTextFormat },
	{ "WriteTwoDigitBCDNumber", adapt_WriteTwoDigitBCDNumber },
	{ "WriteFourDigitBCDNumber", adapt_WriteFourDigitBCDNumber },
	{ "WriteOneDigitBCDNumber", adapt_WriteOneDigitBCDNumber },
	{ "WriteOneByteNumber", adapt_WriteOneByteNumber },
	{ "WriteTwoByteNumber", adapt_WriteTwoByteNumber },
	{ NULL, NULL },
};
