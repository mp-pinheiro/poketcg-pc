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
	{ "ContinueDrawingTextBoxDMG", adapt_ContinueDrawingTextBoxDMG },
/* <<< part probe_entries_text_box */
