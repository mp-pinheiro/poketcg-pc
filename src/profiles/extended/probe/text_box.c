/* >>> part includes */
#include "home/text_box.h"
#include "probe.h"
/* <<< part includes */

/* >>> part pair */
static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)(hi << 8 | lo);
}
/* <<< part pair */

/* >>> part split */
static void split(uint16_t value, uint8_t *hi, uint8_t *lo)
{
	*hi = (uint8_t)(value >> 8);
	*lo = (uint8_t)value;
}
/* <<< part split */

/* >>> factory SafeCopyDataDEtoHL */
static void adapt_SafeCopyDataDEtoHL(ProbeState *s)
{
	uint16_t de = pair(s->d, s->e);
	s->a = SafeCopyDataDEtoHL(&de, &s->hl, s->c);
	split(de, &s->d, &s->e);
}
/* <<< factory SafeCopyDataDEtoHL */

/* >>> factory DECoordToBGMap0Address */
static void adapt_DECoordToBGMap0Address(ProbeState *s)
{
	s->hl = DECoordToBGMap0Address(s->d, s->e);
}
/* <<< factory DECoordToBGMap0Address */

/* >>> factory AdjustCoordinatesForBGScroll */
static void adapt_AdjustCoordinatesForBGScroll(ProbeState *s)
{
	AdjustCoordinatesForBGScroll(&s->d, &s->e);
}
/* <<< factory AdjustCoordinatesForBGScroll */
/* >>> factory CopyLine */
static void adapt_CopyLine(ProbeState *s)
{
	uint16_t original_hl = s->hl;
	CopyLine(&s->hl, s->a, s->b, s->d, s->e);
	split(original_hl, &s->d, &s->e);
}
/* <<< factory CopyLine */

/* >>> factory DrawRegularTextBox */
static void adapt_DrawRegularTextBox(ProbeState *s)
{
	DrawRegularTextBox(&s->hl, s->a, s->b, s->c, s->d, s->e);
}
/* <<< factory DrawRegularTextBox */
/* >>> factory ContinueDrawingTextBoxDMG */
static void adapt_ContinueDrawingTextBoxDMG(ProbeState *s)
{
	ContinueDrawingTextBoxDMG(&s->hl, s->a, s->b, s->c, s->d, s->e);
}
/* <<< factory ContinueDrawingTextBoxDMG */

/* >>> factory DrawRegularTextBoxCGB */
static void adapt_DrawRegularTextBoxCGB(ProbeState *s)
{
	DrawRegularTextBoxCGB(&s->hl, s->a, s->b, s->c, s->d, s->e);
}
/* <<< factory DrawRegularTextBoxCGB */

/* >>> factory ContinueDrawingTextBoxCGB */
static void adapt_ContinueDrawingTextBoxCGB(ProbeState *s)
{
	ContinueDrawingTextBoxCGB(&s->hl, s->a, s->b, s->c, s->d, s->e);
}
/* <<< factory ContinueDrawingTextBoxCGB */

/* >>> factory CopyCurrentLineTilesAndAttrCGB */
static void adapt_CopyCurrentLineTilesAndAttrCGB(ProbeState *s)
{
	CopyCurrentLineTilesAndAttrCGB(&s->hl, s->a, s->b, s->d, s->e);
}
/* <<< factory CopyCurrentLineTilesAndAttrCGB */

/* >>> factory CopyCurrentLineAttrCGB */
static void adapt_CopyCurrentLineAttrCGB(ProbeState *s)
{
	CopyCurrentLineAttrCGB(&s->hl, s->a, s->b, s->d, s->e);
}
/* <<< factory CopyCurrentLineAttrCGB */


/* >>> factory DrawLabeledTextBox */
static void adapt_DrawLabeledTextBox(ProbeState *s)
{
	DrawLabeledTextBox(&s->hl, s->a, s->b, s->c, s->d, s->e);
}
/* <<< factory DrawLabeledTextBox */

/* >>> part probe_entries_text_box */
const ProbeEntry probe_entries_text_box[] = {
	{ "SafeCopyDataDEtoHL", adapt_SafeCopyDataDEtoHL },
	{ "DECoordToBGMap0Address", adapt_DECoordToBGMap0Address },
	{ "AdjustCoordinatesForBGScroll", adapt_AdjustCoordinatesForBGScroll },
	{ "CopyLine", adapt_CopyLine },
	{ "DrawRegularTextBox", adapt_DrawRegularTextBox },
	{ "ContinueDrawingTextBoxDMG", adapt_ContinueDrawingTextBoxDMG },
	{ "DrawRegularTextBoxCGB", adapt_DrawRegularTextBoxCGB },
	{ "ContinueDrawingTextBoxCGB", adapt_ContinueDrawingTextBoxCGB },
	{ "CopyCurrentLineTilesAndAttrCGB", adapt_CopyCurrentLineTilesAndAttrCGB },
	{ "CopyCurrentLineAttrCGB", adapt_CopyCurrentLineAttrCGB },
	{ "DrawLabeledTextBox", adapt_DrawLabeledTextBox },
};
/* <<< part probe_entries_text_box */
