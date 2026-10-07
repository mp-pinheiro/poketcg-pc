/* === part includes */
/* >>> part probe_card_id */
static CardId probe_card_id(const ProbeState *s)
{
	return (CardId)(((uint16_t)s->d << 8) | s->e);
}
/* <<< part probe_card_id */
/* >>> factory _ShowPromotionalCardScreen */
static void adapt__ShowPromotionalCardScreen(ProbeState *s)
{
	_ShowPromotionalCardScreen(probe_card_id(s));
}
/* <<< factory _ShowPromotionalCardScreen */
