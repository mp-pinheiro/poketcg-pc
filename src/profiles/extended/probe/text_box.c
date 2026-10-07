/* --- factory DrawRegularTextBoxDMG */
/* --- factory ContinueDrawingTextBoxDMGorSGB */
/* === factory DrawRegularTextBox */
/* >>> factory ContinueDrawingTextBoxDMG */
static void adapt_ContinueDrawingTextBoxDMG(ProbeState *s)
{
	ContinueDrawingTextBoxDMG(&s->hl, s->a, s->b, s->c, s->d, s->e);
}
/* <<< factory ContinueDrawingTextBoxDMG */
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
