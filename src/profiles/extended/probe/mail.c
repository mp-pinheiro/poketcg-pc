/* >>> factory GetPCPackNameTextID */
static void adapt_GetPCPackNameTextID(ProbeState *s)
{
	uint16_t text_id = GetPCPackNameTextID(s->a);
	s->d = (uint8_t)(text_id >> 8);
	s->e = (uint8_t)text_id;
}
/* <<< factory GetPCPackNameTextID */
